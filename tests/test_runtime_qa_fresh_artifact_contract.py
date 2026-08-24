from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORCHESTRATION = ROOT / "docs" / "knowledge" / "vertical-slice" / "SKILL_ORCHESTRATION_AND_EVIDENCE.md"


class RuntimeQaFreshArtifactContractTests(unittest.TestCase):
    def test_runtime_artifact_freshness_is_fail_closed_and_existing_owner_scoped(self) -> None:
        text = ORCHESTRATION.read_text(encoding="utf-8")
        for marker in (
            "FRESH_RUNTIME_ARTIFACT_GATE",
            "PRIOR_ARTIFACT_EXISTENCE_IS_NOT_FRESH_EVIDENCE",
            "STALE_ARTIFACT_FALSE_PASS",
            "INCONCLUSIVE_NOT_PASS",
            "BLOCKED_UNVERIFIED",
            "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md",
            "claim-and-intent-verification",
        ):
            self.assertIn(marker, text)

    def test_freshness_requires_regeneration_and_identity_without_overclaiming_quality(self) -> None:
        text = ORCHESTRATION.read_text(encoding="utf-8")
        for marker in (
            "이전 transient output을 삭제·격리하거나 unique run directory 사용",
            "이번 run이 expected artifact를 새로 생성했는지 확인",
            "artifact path + bytes/hash + run/build identity",
            "baseline identity를 pin",
            "baseline 교체는 별도 review",
            "fresh screenshot도 디자인 품질·가독성·접근성·재미·human approval을 자동 증명하지 않는다",
            "structured assertion",
        ):
            self.assertIn(marker, text)


if __name__ == "__main__":
    unittest.main()
