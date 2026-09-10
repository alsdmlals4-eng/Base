from __future__ import annotations

import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from tools.run_project_work_gate import REQUIRED_BASE_CLOSURE


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "run_project_work_gate.py"
OWNER = ROOT / "docs" / "operations" / "BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md"
DOCUMENTATION_MAP = ROOT / "docs" / "DOCUMENTATION_MAP.md"
LEARNING_LOG = (
    ROOT
    / "skills"
    / "managing-project-intake-and-work-contract"
    / "references"
    / "base-current-project-work-bootstrap"
    / "LEARNING_LOG.md"
)
ATTRIBUTES = ROOT / ".gitattributes"


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
            ".gitattributes",
            "AGENTS.md",
            "START_HERE.md",
            "docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md",
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
            self.assertIn(required_path, REQUIRED_BASE_CLOSURE)

    def test_every_raw_compared_closure_path_is_pinned_to_lf(self) -> None:
        attributes = ATTRIBUTES.read_text(encoding="utf-8")
        for relative in REQUIRED_BASE_CLOSURE:
            with self.subTest(relative=relative):
                self.assertIn(f"{relative} text eol=lf", attributes)

        git = shutil.which("git")
        self.assertIsNotNone(git)
        result = subprocess.run(
            [git, "-C", str(ROOT), "check-attr", "eol", "--", *REQUIRED_BASE_CLOSURE],
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        observed = {
            line.split(": eol: ", 1)[0]: line.split(": eol: ", 1)[1]
            for line in result.stdout.splitlines()
            if ": eol: " in line
        }
        for relative in REQUIRED_BASE_CLOSURE:
            with self.subTest(check_attr=relative):
                self.assertEqual("lf", observed.get(relative))

    def test_documented_launcher_disables_lazy_fetch_and_git_rewrites(self) -> None:
        text = OWNER.read_text(encoding="utf-8")
        invocation = text.split("Conceptual command shape:", 1)[1].split(
            "## 6. Verified operational closure", 1
        )[0]
        for required in (
            "GIT_CONFIG_NOSYSTEM=1",
            "GIT_CONFIG_GLOBAL=<null-device>",
            "GIT_CONFIG_COUNT=0",
            "GIT_NO_REPLACE_OBJECTS=1",
            "GIT_NO_LAZY_FETCH=1",
            "GIT_GRAFT_FILE=<null-device>",
            "--no-replace-objects",
        ):
            self.assertIn(required, invocation)

    def test_documentation_map_routes_ordinary_project_work(self) -> None:
        text = DOCUMENTATION_MAP.read_text(encoding="utf-8")
        self.assertIn("BASE_CURRENT_OPERATIONAL_BOOTSTRAP", text)
        self.assertIn("ordinary target-project work", text)
        self.assertIn("BASE_CURRENT_PROJECT_WORK_BOOTSTRAP.md", text)
        self.assertNotIn("when current scope requires **Base-only maintenance**", text)

    def test_learning_log_records_regular_file_only_receipt_transport(self) -> None:
        text = LEARNING_LOG.read_text(encoding="utf-8")
        self.assertIn("REGULAR_BOUNDED_RECEIPT_ONLY", text)
        self.assertIn("STDIN_RECEIPT_REJECTED", text)
        self.assertNotIn("bounded stdin", text.lower())

    def test_local_commit_type_and_closeout_ancestry_are_required(self) -> None:
        source = TOOL.read_text(encoding="utf-8")
        self.assertIn('"cat-file", "-t"', source)
        self.assertIn('"merge-base"', source)
        self.assertIn('"--is-ancestor"', source)
        self.assertIn("GIT_GRAFT_FILE", source)
        self.assertNotIn('f"{sha}^{{commit}}"', source)

    def test_receipt_input_and_identity_output_are_fail_closed(self) -> None:
        source = TOOL.read_text(encoding="utf-8")
        self.assertIn("stdin receipt mode is not supported", source)
        self.assertIn("parse_constant", source)
        self.assertIn("object_pairs_hook", source)
        self.assertIn("json.dumps(value", source)
        for required in (
            "MAX_WORK_ITEMS",
            "MAX_DEPENDENCY_EDGES",
            "MAX_RECEIPT_CONTAINER_NODES",
            "MAX_RECEIPT_NESTING",
            "_validate_receipt_complexity",
        ):
            self.assertIn(required, source)

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
                DOCUMENTATION_MAP.read_text(encoding="utf-8"),
            )
        )
        self.assertIn("ordinary target-project work", combined)
        self.assertNotIn("when current scope requires **Base-only maintenance**", combined)


if __name__ == "__main__":
    unittest.main()
