from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "run_project_work_gate.py"
OWNER = ROOT / "docs" / "operations" / "BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md"


class BaseCurrentProjectWorkBootstrapReviewTests(unittest.TestCase):
    def test_entrypoint_requires_trusted_commit_stream_and_absolute_git(self) -> None:
        source = TOOL.read_text(encoding="utf-8")
        for required in (
            '"--entrypoint-source"',
            '"commit-stream"',
            '"--base-root"',
            '"--git-executable"',
            "GIT_NO_LAZY_FETCH",
            "GIT_NO_REPLACE_OBJECTS",
        ):
            self.assertIn(required, source)
        self.assertNotIn("os.execv(", source)
        self.assertNotIn('importlib.util.spec_from_file_location', source)
        self.assertNotIn('sys.stdin.buffer.read', source)

    def test_operational_authority_closure_covers_consumed_base_inputs(self) -> None:
        source = TOOL.read_text(encoding="utf-8")
        for required_path in (
            "AGENTS.md",
            "START_HERE.md",
            "docs/operations/BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md",
            "templates/project-operations/PROJECT_WORK_ITEM_CHECKLIST.md",
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "templates/project-operations/PROJECT_START_HERE.md",
            "templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md",
            "templates/project-operations/.agents/skills/base-project-router/SKILL.md",
            "tools/run_project_work_gate.py",
            "tools/validate_work_contract_receipt.py",
            "tools/project_work_tracking.py",
        ):
            self.assertIn(required_path, source)

    def test_local_commit_type_and_closeout_ancestry_are_required(self) -> None:
        source = TOOL.read_text(encoding="utf-8")
        self.assertIn('"cat-file", "-t"', source)
        self.assertIn('"merge-base", "--is-ancestor"', source)
        self.assertNotIn('f"{sha}^{{commit}}"', source)

    def test_receipt_input_and_identity_output_are_fail_closed(self) -> None:
        source = TOOL.read_text(encoding="utf-8")
        self.assertIn("stdin receipt mode is not supported", source)
        self.assertIn("parse_constant", source)
        self.assertIn("object_pairs_hook", source)
        self.assertIn("json.dumps(value", source)

    def test_direct_working_copy_entrypoint_is_not_a_supported_trust_boundary(self) -> None:
        result = subprocess.run(
            [sys.executable, "-I", str(TOOL), "--help"],
            text=True,
            capture_output=True,
            check=False,
            timeout=20,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("exact Base commit stream", result.stdout + result.stderr)

    def test_active_routing_targets_ordinary_project_work_not_base_only_maintenance(self) -> None:
        combined = "\n".join(
            (
                (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
                OWNER.read_text(encoding="utf-8"),
                (ROOT / "START_HERE.md").read_text(encoding="utf-8"),
            )
        )
        self.assertIn("ordinary target-project work", combined)
        self.assertNotIn("when current scope requires **Base-only maintenance**", combined)


if __name__ == "__main__":
    unittest.main()
