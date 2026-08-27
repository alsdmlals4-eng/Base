from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCAL_STARTER = ROOT / "templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md"
CURRENT_ROUTER = ROOT / "templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md"


class WorkFinalStarterRouterContractTests(unittest.TestCase):
    def test_local_visual_starter_enters_through_current_router(self) -> None:
        self.assertTrue(LOCAL_STARTER.exists())
        self.assertTrue(CURRENT_ROUTER.exists())

        starter = LOCAL_STARTER.read_text(encoding="utf-8")
        router = CURRENT_ROUTER.read_text(encoding="utf-8")

        for token in (
            "WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md",
            "THIN_ROUTER_NOT_SECOND_CANON",
            "PROJECT_LOCAL_VISUAL_BINARY_FIRST",
            "NOTION_VISUAL_STRUCTURE_REFERENCE_ONLY",
            "NO_NOTION_BINARY_UPLOAD_REQUIRED",
            "PROJECT_START_CANON_CHECKLIST",
            "CODEX_SINGLE_IMPLEMENTATION_WINDOW",
            "USER_DOWNLOADABLE_BUILD_ARTIFACT_REQUIRED",
            "HUMAN_USABILITY_EVIDENCE: NOT_RUN",
            "PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN",
        ):
            self.assertIn(token, starter)

        for routed_owner in (
            "WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
            "WORK_PROJECT_START_CANON_CHECKLIST.md",
            "WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md",
            "WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md",
            "WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md",
        ):
            self.assertIn(routed_owner, router)

        self.assertLess(len(starter.splitlines()), 90, "starter must remain a thin copy-paste entry")
        self.assertNotIn(
            "1. templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md",
            starter,
            "starter must not freeze a parallel owner list; the current router owns routing",
        )


if __name__ == "__main__":
    unittest.main()
