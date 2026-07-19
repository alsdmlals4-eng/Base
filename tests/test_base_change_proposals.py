from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "check_base_change_proposals",
    ROOT / "tools/check_base_change_proposals.py",
)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class BaseChangeProposalTests(unittest.TestCase):
    def test_current_proposals_validate(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(registry["proposal_root"], "[수정제안서]")

    def test_new_proposal_pr_cannot_change_active_base(self) -> None:
        previous = {"proposals": []}
        current = {
            "proposals": [
                {
                    "proposal_id": "BCP-2026-999-example",
                    "status": "SUBMITTED",
                }
            ]
        }
        errors = CHECKER.enforce_proposal_only_diff(
            current,
            previous,
            ["[수정제안서]/BCP-2026-999-example/PROPOSAL.md", "AGENTS.md"],
        )
        self.assertTrue(any("active Base paths" in error for error in errors))

    def test_new_proposal_starts_submitted(self) -> None:
        previous = {"proposals": []}
        current = {
            "proposals": [
                {
                    "proposal_id": "BCP-2026-999-example",
                    "status": "APPROVED_FOR_IMPLEMENTATION",
                }
            ]
        }
        errors = CHECKER.enforce_proposal_only_diff(
            current,
            previous,
            ["[수정제안서]/BCP-2026-999-example/PROPOSAL.md"],
        )
        self.assertTrue(any("must start as SUBMITTED" in error for error in errors))

    def test_bootstrap_pr_is_explicitly_allowed(self) -> None:
        current = {"proposals": [{"proposal_id": "BCP-2026-001-bootstrap", "status": "SUBMITTED"}]}
        self.assertEqual(CHECKER.enforce_proposal_only_diff(current, None, ["AGENTS.md"]), [])

    def test_git_paths_preserve_non_ascii_proposal_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            proposal = root / "[수정제안서]" / "BCP-2026-999-example" / "PROPOSAL.md"
            proposal.parent.mkdir(parents=True)
            proposal.write_text("proposal\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            paths = CHECKER.git_paths(root, "diff", "--cached", "--name-only", "-z")
            self.assertEqual(paths, ["[수정제안서]/BCP-2026-999-example/PROPOSAL.md"])


if __name__ == "__main__":
    unittest.main()
