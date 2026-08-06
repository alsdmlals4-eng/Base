from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools import godot_multi_project_pilot as runner
from tools.godot_project_pilot_evidence import VerifiedRuntimeEvidence


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class GodotPilotArtifactBundleTests(unittest.TestCase):
    def test_exported_bundle_contains_reverifiable_runtime_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            output = root / "output"
            scene = workspace / ".godot-live-editor-pilot/scratch.tscn"
            runtime_result = workspace / "artifacts/godot-project-pilot/runtime-result.json"
            scene.parent.mkdir(parents=True)
            runtime_result.parent.mkdir(parents=True)
            scene.write_text("[gd_scene format=3]\n", encoding="utf-8")
            runtime_result.write_text(
                json.dumps({"status": "PASS"}, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            verified = VerifiedRuntimeEvidence(
                repository="owner/game",
                source_commit="a" * 40,
                base_pilot_commit="b" * 40,
                saved_scene_path="res://.godot-live-editor-pilot/scratch.tscn",
                saved_scene_sha256=_sha256(scene),
                runtime_result_sha256=_sha256(runtime_result),
                ledger_states=("COMPLETED", "COMPLETED"),
            )

            exported = runner.export_runtime_evidence_bundle(
                workspace,
                runtime_result,
                output,
                verified,
            )

            self.assertEqual(output / "runtime-result.json", exported.runtime_result)
            self.assertEqual(output / "scratch.tscn", exported.saved_scene)
            self.assertEqual(verified.runtime_result_sha256, _sha256(exported.runtime_result))
            self.assertEqual(verified.saved_scene_sha256, _sha256(exported.saved_scene))

    def test_export_rejects_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            output = root / "output"
            scene = workspace / ".godot-live-editor-pilot/scratch.tscn"
            runtime_result = workspace / "artifacts/godot-project-pilot/runtime-result.json"
            scene.parent.mkdir(parents=True)
            runtime_result.parent.mkdir(parents=True)
            scene.write_text("[gd_scene format=3]\n", encoding="utf-8")
            runtime_result.write_text("{}\n", encoding="utf-8")
            verified = VerifiedRuntimeEvidence(
                repository="owner/game",
                source_commit="a" * 40,
                base_pilot_commit="b" * 40,
                saved_scene_path="res://.godot-live-editor-pilot/scratch.tscn",
                saved_scene_sha256="0" * 64,
                runtime_result_sha256=_sha256(runtime_result),
                ledger_states=("COMPLETED", "COMPLETED"),
            )

            with self.assertRaisesRegex(ValueError, "ARTIFACT_BYTE_HASH_MISMATCH"):
                runner.export_runtime_evidence_bundle(
                    workspace,
                    runtime_result,
                    output,
                    verified,
                )


if __name__ == "__main__":
    unittest.main()
