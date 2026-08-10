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

    def test_merged_continuity_and_diagnostic_proposals_retain_approval_and_implementation_links(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual(errors, [])
        proposal_ids = {
            "BCP-2026-002-actions-node24-compatibility",
            "BCP-2026-013-post-merge-continuation-state-reconciliation",
            "BCP-2026-014-handoff-machine-consumer-compatibility-closeout",
            "BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation",
            "BCP-2026-018-godot-pilot-failure-diagnostic-preservation",
            "BCP-2026-019-ten-paces-handoff-machine-consumer-compatibility",
        }
        approved = {
            item["proposal_id"]: item
            for item in registry["proposals"]
            if item["proposal_id"] in proposal_ids
        }
        self.assertEqual(proposal_ids, set(approved))
        implementation_prs = {
            "BCP-2026-002-actions-node24-compatibility": "https://github.com/alsdmlals4-eng/Base/pull/262",
            "BCP-2026-013-post-merge-continuation-state-reconciliation": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-014-handoff-machine-consumer-compatibility-closeout": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-018-godot-pilot-failure-diagnostic-preservation": "https://github.com/alsdmlals4-eng/Base/pull/261",
            "BCP-2026-019-ten-paces-handoff-machine-consumer-compatibility": "https://github.com/alsdmlals4-eng/Base/pull/260",
        }
        for proposal_id, item in approved.items():
            self.assertEqual("IMPLEMENTED", item["status"])
            self.assertEqual(
                "docs/superpowers/specs/2026-08-10-approved-base-continuity-diagnostics-actions-design.md",
                item["approval_ref"],
            )
            self.assertEqual(implementation_prs[proposal_id], item["implementation_pr"])

    def test_merged_and_newly_approved_proposals_have_distinct_lifecycle_states(self) -> None:
        registry, errors = CHECKER.validate_repository(ROOT)
        self.assertEqual([], errors)
        entries = {item["proposal_id"]: item for item in registry["proposals"]}
        implemented = {
            "BCP-2026-002-actions-node24-compatibility": "https://github.com/alsdmlals4-eng/Base/pull/262",
            "BCP-2026-013-post-merge-continuation-state-reconciliation": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-014-handoff-machine-consumer-compatibility-closeout": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-016-live-source-handoff-semantic-consumer-reconciliation": "https://github.com/alsdmlals4-eng/Base/pull/260",
            "BCP-2026-018-godot-pilot-failure-diagnostic-preservation": "https://github.com/alsdmlals4-eng/Base/pull/261",
            "BCP-2026-019-ten-paces-handoff-machine-consumer-compatibility": "https://github.com/alsdmlals4-eng/Base/pull/260",
        }
        for proposal_id, implementation_pr in implemented.items():
            self.assertEqual("IMPLEMENTED", entries[proposal_id]["status"])
            self.assertEqual(implementation_pr, entries[proposal_id]["implementation_pr"])

        approved = {
            "BCP-2026-001-base-skill-map-publication",
            "BCP-2026-012-serial-fiction-canon-migration-debt",
            "BCP-2026-015-external-runtime-session-same-snapshot-recovery",
            "BCP-2026-017-serial-fiction-reconciliation-frontier-and-derived-continuity-guard",
        }
        for proposal_id in approved:
            self.assertEqual("APPROVED_FOR_IMPLEMENTATION", entries[proposal_id]["status"])
            self.assertTrue(entries[proposal_id]["approval_ref"])
            self.assertIsNone(entries[proposal_id]["implementation_pr"])

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
