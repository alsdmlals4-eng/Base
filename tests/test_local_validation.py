from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests.test_cloud_run_game_backend_capability import (
    CloudRunGameBackendCapabilityTests as _CloudRunGameBackendCapabilityTests,
)
from tests.test_godot_editor_transaction_adapter import (
    GodotEditorTransactionAdapterTests as _GodotEditorTransactionAdapterTests,
)
from tests.test_godot_editor_transaction_adapter_runtime import (
    GodotEditorTransactionAdapterRuntimeTests as _GodotEditorTransactionAdapterRuntimeTests,
)
from tests.test_godot_multi_project_pilot import (
    GodotMultiProjectPilotTests as _GodotMultiProjectPilotTests,
)
from tests.test_godot_multi_project_pilot_adversarial import (
    GodotMultiProjectPilotAdversarialTests as _GodotMultiProjectPilotAdversarialTests,
)
from tests.test_godot_live_editor_contract import (
    GodotLiveEditorContractTests as _GodotLiveEditorContractTests,
)
from tests.test_godot_live_editor_contract_v2 import (
    GodotLiveEditorContractV2Tests as _GodotLiveEditorContractV2Tests,
)
from tests.test_godot_live_editor_contract_v2_adversarial import (
    GodotLiveEditorContractV2AdversarialTests as _GodotLiveEditorContractV2AdversarialTests,
)
from tests.test_godot_live_editor_contract_v2_docs import (
    GodotLiveEditorContractV2DocsTests as _GodotLiveEditorContractV2DocsTests,
)
from tests.test_godot_live_editor_runtime_pilot import (
    GodotLiveEditorRuntimePilotTests as _GodotLiveEditorRuntimePilotTests,
)
from tests.test_platform_review_asset_rights_reference_production import (
    PlatformReviewAssetRightsReferenceProductionTests
    as _PlatformReviewAssetRightsReferenceProductionTests,
)
from tests.test_game_entitlement_integrity_drm_capability import (
    GameEntitlementIntegrityDrmCapabilityTests
    as _GameEntitlementIntegrityDrmCapabilityTests,
)
from tests.test_local_ci_fallback import (
    LocalCiFallbackTests as _LocalCiFallbackTests,
)
from tests.test_local_godot_reference_library import (
    LocalGodotReferenceLibraryTests as _LocalGodotReferenceLibraryTests,
)
from tests.test_loop_a2_child_terminal_contract import (
    LoopA2ChildTerminalContractTests as _LoopA2ChildTerminalContractTests,
)
from tests.test_loop_a2_authority_dependency_boundary import (
    LoopA2AuthorityDependencyBoundaryTests
    as _LoopA2AuthorityDependencyBoundaryTests,
)
from tests.test_project_asset_vault import (
    ProjectAssetVaultTests as _ProjectAssetVaultTests,
)
from tests.test_project_protected_baseline_authority import (
    ProtectedBaselineAuthorityTests as _ProtectedBaselineAuthorityTests,
)
from tests.test_serial_fiction_discipline import (
    SerialFictionDisciplineContractTests as _SerialFictionDisciplineContractTests,
)
from tools import run_local_validation as runner


ROOT = Path(__file__).resolve().parents[1]


class LocalValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.evidence = self.root / "child-environment.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def recording_command(self, exit_code: int) -> tuple[str, ...]:
        script = """from __future__ import annotations
import json
import os
import sys
from pathlib import Path

evidence = Path(sys.argv[1])
payload = {name: os.environ[name] for name in ("TMPDIR", "TMP", "TEMP")}
Path(payload["TMPDIR"], "child-temporary.txt").write_text("owned", encoding="utf-8")
evidence.write_text(json.dumps(payload), encoding="utf-8")
raise SystemExit(int(sys.argv[2]))
"""
        return (sys.executable, "-c", script, str(self.evidence), str(exit_code))

    def test_success_uses_owned_temp_environment_and_cleans_it(self) -> None:
        status = runner.run_validation(
            self.root,
            [self.recording_command(exit_code=0)],
        )

        payload = json.loads(self.evidence.read_text(encoding="utf-8"))
        session = Path(payload["TMPDIR"])
        self.assertEqual(payload["TMPDIR"], payload["TMP"])
        self.assertEqual(payload["TMPDIR"], payload["TEMP"])
        self.assertEqual(self.root / ".tmp", session.parent)
        self.assertTrue(session.name.startswith("local-validation-"))
        self.assertEqual(0, status)
        self.assertFalse(session.exists())
        self.assertFalse((self.root / ".tmp").exists())

    def test_failure_status_is_propagated_and_owned_session_is_cleaned(self) -> None:
        status = runner.run_validation(
            self.root,
            [self.recording_command(exit_code=7)],
        )

        session = Path(
            json.loads(self.evidence.read_text(encoding="utf-8"))["TMPDIR"]
        )
        self.assertEqual(7, status)
        self.assertFalse(session.exists())
        self.assertFalse((self.root / ".tmp").exists())

    def test_cleanup_rejects_a_path_outside_the_owned_temp_root(self) -> None:
        outside = self.root / "foreign-session"
        outside.mkdir()
        marker = outside / "keep.txt"
        marker.write_text("keep", encoding="utf-8")

        identity = (outside.lstat().st_dev, outside.lstat().st_ino)
        with self.assertRaisesRegex(ValueError, "owned local validation session"):
            runner._remove_owned_session(self.root, outside, identity)

        self.assertEqual("keep", marker.read_text(encoding="utf-8"))

    @unittest.skipIf(os.name == "nt", "symlink fixture requires POSIX permissions")
    def test_symlinked_temporary_root_is_rejected_without_touching_target(self) -> None:
        target = self.root / "foreign-root"
        target.mkdir()
        marker = target / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        (self.root / ".tmp").symlink_to(target, target_is_directory=True)

        with self.assertRaisesRegex(ValueError, "must not be a symlink"):
            runner.run_validation(self.root, [self.recording_command(exit_code=0)])

        self.assertEqual("keep", marker.read_text(encoding="utf-8"))

    @unittest.skipIf(os.name == "nt", "session replacement fixture requires POSIX symlinks")
    def test_cleanup_attack_does_not_mask_the_original_child_failure(self) -> None:
        foreign = self.root / "foreign-session"
        foreign.mkdir()
        marker = foreign / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        script = """from __future__ import annotations
import json
import os
import shutil
import sys
from pathlib import Path

session = Path(os.environ["TMPDIR"])
Path(sys.argv[1]).write_text(json.dumps({"TMPDIR": str(session)}), encoding="utf-8")
shutil.rmtree(session)
session.symlink_to(Path(sys.argv[2]), target_is_directory=True)
raise SystemExit(7)
"""

        status = runner.run_validation(
            self.root,
            [(sys.executable, "-c", script, str(self.evidence), str(foreign))],
        )

        session = Path(json.loads(self.evidence.read_text(encoding="utf-8"))["TMPDIR"])
        self.assertEqual(7, status)
        self.assertEqual("keep", marker.read_text(encoding="utf-8"))
        self.assertTrue(session.is_symlink())
        session.unlink()
        (self.root / ".tmp").rmdir()

    def test_ignore_contract_hides_only_owned_roots(self) -> None:
        (self.root / ".gitignore").write_text(
            (ROOT / ".gitignore").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

        self.assertTrue(self.git_check_ignore(".venv/probe"))
        self.assertTrue(self.git_check_ignore(".tmp/probe"))
        self.assertFalse(self.git_check_ignore("tmp-user-data/probe"))

    def test_dependency_preflight_reports_missing_required_modules(self) -> None:
        with patch.object(
            runner.importlib.util,
            "find_spec",
            side_effect=lambda name: None if name == "jsonschema" else object(),
        ):
            missing = runner.missing_required_modules()

        self.assertEqual(("jsonschema",), missing)

    def git_check_ignore(self, path: str) -> bool:
        result = subprocess.run(
            ["git", "check-ignore", "--no-index", "--quiet", path],
            cwd=self.root,
            check=False,
        )
        return result.returncode == 0


if __name__ == "__main__":
    unittest.main()
