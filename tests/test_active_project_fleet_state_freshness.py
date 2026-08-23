from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADOPTION = ROOT / "docs/knowledge/game-development/reuse/adoption"


def load_json(name: str) -> dict:
    return json.loads((ADOPTION / name).read_text(encoding="utf-8"))


class ActiveProjectFleetStateFreshnessTests(unittest.TestCase):
    def test_completed_project_prs_are_not_kept_as_active_adoption_blockers(self) -> None:
        matrix = load_json("ACTIVE_PROJECT_ADOPTION_MATRIX.json")

        switchy = matrix["projects"]["SWITCHY"]
        self.assertNotEqual("DEFERRED_OPEN_PR", switchy["status"])
        self.assertNotIn("open PR #154", switchy.get("blocker", ""))

        tetris = matrix["projects"]["TETRIS"]
        self.assertNotEqual("DEFERRED_OPEN_PR", tetris["status"])
        self.assertNotIn("open PRs #3 and #9", tetris.get("blocker", ""))

    def test_resolved_omenward_validator_issue_is_not_an_active_blocker(self) -> None:
        matrix = load_json("ACTIVE_PROJECT_ADOPTION_MATRIX.json")
        omenward = matrix["projects"]["OMENWARD"]

        self.assertEqual("RESOLVED_BY_PR_201", omenward["followup_issue_state"])
        self.assertNotIn("resolving any relevant Issue #199 authority conflict", omenward.get("revisit", ""))
        self.assertNotIn("Issue #199 tracks", omenward.get("blocker", ""))

    def test_project_work_handoff_uses_current_tetris_and_omenward_routing(self) -> None:
        handoff = load_json("PROJECT_WORK_REUSE_HANDOFF.json")

        tetris = handoff["projects"]["TETRIS"]
        identity = tetris["project_owned_identity"]
        self.assertIn("Shared Player Turn Budget", identity)
        self.assertNotIn("dual-mode timing", identity)
        self.assertNotIn("pause/lock", identity)
        self.assertNotIn("combat clock", identity)
        self.assertNotIn("After current PR work is completed", tetris["next_project_work_action"])

        omenward = handoff["projects"]["OMENWARD"]
        self.assertNotIn("Issue #199 authority", omenward["next_project_work_action"])
        self.assertIn("resolved validator history", omenward["next_project_work_action"])


if __name__ == "__main__":
    unittest.main()
