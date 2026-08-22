from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/evidence/2026-08-20-v47-workflow-alignment-adversarial-review.md"
WORKFLOW = ROOT / ".github/workflows/validate-game-project-operating-system.yml"
RETIREMENT = ROOT / "docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md"


class V47SupersededPrClosureTests(unittest.TestCase):
    def test_stale_556_evidence_is_closed_by_fresh_main_573(self) -> None:
        text = EVIDENCE.read_text(encoding="utf-8")
        for term in (
            "Superseded draft PR: #556",
            "Fresh-main implementation PR: #573",
            "af96707bb42dbbb8a36708242574802404b44e80",
            "182f98b1c1a0f0fa578994b453d0d5f7b57a57c7",
            "CLEAN_REVIEW_EXIT: true",
            "all required exact-head workflows: PASS",
        ):
            self.assertIn(term, text)
        self.assertNotIn("CLEAN_REVIEW_EXIT: PENDING_FINAL_EXACT_HEAD_CI_AND_PR_GATE", text)

    def test_retired_qa_studio_is_absent_from_active_required_ci(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        retirement = RETIREMENT.read_text(encoding="utf-8")

        self.assertIn("QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW", retirement)
        self.assertIn("신규 작업의 자동 라우팅·필수 preflight·완료 조건에 넣지 않는다", retirement)

        for stale_active_consumer in (
            "tools/qa-evidence-studio/*",
            "Install Windows QA Evidence Studio dependencies",
            "Run Windows QA Evidence Studio smoke",
            "tools/qa-evidence-studio/tests",
            "qa_evidence_studio",
        ):
            self.assertNotIn(stale_active_consumer, workflow)


if __name__ == "__main__":
    unittest.main()
