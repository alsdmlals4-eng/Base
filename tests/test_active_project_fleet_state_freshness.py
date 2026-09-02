from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADOPTION = ROOT / "docs/knowledge/game-development/reuse/adoption"


def load_json(name: str) -> dict:
    return json.loads((ADOPTION / name).read_text(encoding="utf-8"))


class ActiveProjectFleetStateFreshnessTests(unittest.TestCase):
    def test_current_reuse_routing_has_no_project_mutable_authority(self) -> None:
        handoff = load_json("PROJECT_WORK_REUSE_HANDOFF.json")
        matrix = load_json("ACTIVE_PROJECT_ADOPTION_MATRIX.json")

        self.assertEqual(
            [
                "PROJECT_AGENTS_MD",
                "CURRENT_PROJECT_MAIN",
                "CURRENT_DECISIONS_AND_ACTIVE_CONTEXT",
                "ACTUAL_IMPLEMENTATION_AND_CONSUMERS",
                "OPEN_PR_OVERLAP",
            ],
            handoff["current_project_authority_read_order"],
        )
        self.assertEqual(
            "STABLE_IDENTITY_AND_REUSE_HINTS_ONLY",
            handoff["base_handoff_authority_boundary"],
        )

        routing_actions = [
            *(
                project["next_project_work_action"]
                for project in handoff["projects"].values()
            ),
            *(project["revisit"] for project in matrix["projects"].values()),
        ]
        for routing_action in routing_actions:
            self.assertNotRegex(routing_action, r"\b[A-Z][A-Z0-9_]*-DEC-\d+\b")
            self.assertNotRegex(routing_action, r"\b(?:Issue|PR)\s*#?\d+\b")
            self.assertNotRegex(routing_action, r"\bPhase(?:[-\s]+[A-Z0-9IVX]+)\b")
            self.assertNotIn("Notion", routing_action)

        for stale_current_reference in (
            "SX-DEC-059",
            "TETRIS-CORE-024",
            "TETRIS-TIME-025",
            "exact Notion",
            "Issue #199",
            "PR #201",
            "Phase-C",
            "first-five-duel Phase I–VI",
        ):
            self.assertNotIn(stale_current_reference, "\n".join(routing_actions))

        for project in handoff["projects"].values():
            self.assertIn(
                "CURRENT_PROJECT_AUTHORITY_READ_ORDER",
                project["next_project_work_action"],
            )

        for project in matrix["projects"].values():
            self.assertTrue(
                project["revisit"].startswith(
                    "follow the project handoff current-authority read order"
                )
            )

        readme = (ADOPTION / "README.md").read_text(encoding="utf-8")
        canonical_entry = "PROJECT_WORK_REUSE_HANDOFF.json#current_project_authority_read_order"
        self.assertIn(canonical_entry, readme)
        self.assertLess(
            readme.index(canonical_entry),
            readme.index("ACTIVE_PROJECT_ADOPTION_MATRIX + project profile"),
        )
        self.assertNotIn("fresh project AGENTS / Active Context", readme)

    def test_completed_project_prs_are_not_kept_as_active_adoption_blockers(self) -> None:
        matrix = load_json("ACTIVE_PROJECT_ADOPTION_MATRIX.json")

        switchy = matrix["projects"]["SWITCHY"]
        self.assertNotEqual("DEFERRED_OPEN_PR", switchy["status"])
        self.assertNotIn("open PR #154", switchy.get("blocker", ""))

        tetris = matrix["projects"]["TETRIS"]
        self.assertNotEqual("DEFERRED_OPEN_PR", tetris["status"])
        self.assertNotIn("open PRs #3 and #9", tetris.get("blocker", ""))

    def test_omenward_validator_history_is_not_current_authority(self) -> None:
        matrix = load_json("ACTIVE_PROJECT_ADOPTION_MATRIX.json")
        omenward = matrix["projects"]["OMENWARD"]

        self.assertNotIn("followup_issue", omenward)
        self.assertNotIn("followup_issue_state", omenward)
        self.assertIn("current-authority read order", omenward["revisit"])

    def test_project_work_handoff_uses_current_tetris_and_omenward_routing(self) -> None:
        handoff = load_json("PROJECT_WORK_REUSE_HANDOFF.json")

        tetris = handoff["projects"]["TETRIS"]
        identity = tetris["project_owned_identity"]
        self.assertIn("Shared Player Turn Budget", identity)
        self.assertNotIn("dual-mode timing", identity)
        self.assertNotIn("pause/lock", identity)
        self.assertNotIn("combat clock", identity)
        self.assertNotIn("After current PR work is completed", tetris["next_project_work_action"])
        self.assertIn("CURRENT_PROJECT_AUTHORITY_READ_ORDER", tetris["next_project_work_action"])

        omenward = handoff["projects"]["OMENWARD"]
        self.assertNotIn("Issue #199 authority", omenward["next_project_work_action"])
        self.assertIn("CURRENT_PROJECT_AUTHORITY_READ_ORDER", omenward["next_project_work_action"])

    def test_ten_paces_historical_churn_is_not_current_reuse_blocker(self) -> None:
        matrix = load_json("ACTIVE_PROJECT_ADOPTION_MATRIX.json")
        ten = matrix["projects"]["TEN_PACES"]
        installation = ten["manifest_installation"]

        self.assertEqual("DEFERRED_PHASE_GATE", ten["status"])
        self.assertEqual("DEFERRED_PROJECT_WORK_GATE", installation["state"])
        self.assertIn("historical_attempted_prs", installation)
        self.assertIn("historical_observed_main_commits", installation)
        self.assertNotIn("attempted_prs", installation)
        self.assertNotIn("observed_main_commits", installation)
        self.assertNotIn("concurrent planning main advanced", ten.get("blocker", ""))
        self.assertIn("current approved project task", ten.get("blocker", ""))
        self.assertIn("historical", ten.get("evidence", "").lower())
        self.assertNotIn("Phase I–VI", ten.get("evidence", ""))

        handoff = load_json("PROJECT_WORK_REUSE_HANDOFF.json")
        ten_handoff = handoff["projects"]["TEN_PACES"]
        next_action = ten_handoff["next_project_work_action"]
        self.assertNotIn("After planning main stabilizes", next_action)
        self.assertNotIn("first-five-duel Phase I–VI", next_action)
        self.assertNotIn("exact Notion", next_action)
        self.assertIn("CURRENT_PROJECT_AUTHORITY_READ_ORDER", next_action)
        self.assertTrue(ten_handoff["do_not_flatten_project_identity"])


if __name__ == "__main__":
    unittest.main()
