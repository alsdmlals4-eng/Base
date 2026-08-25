from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE_PATH = ROOT / "docs/knowledge/research/WEB_PLATFORM_NATIVE_UI_CAPABILITY_GUIDE.md"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class WebPlatformNativeUICapabilityTests(unittest.TestCase):
    def test_platform_native_guide_and_routing_contract(self) -> None:
        self.assertTrue(
            GUIDE_PATH.exists(),
            "approved Web Platform native UI capability Guide must exist",
        )
        guide = GUIDE_PATH.read_text(encoding="utf-8")
        knowledge = read("docs/knowledge/README.md")
        retirement = read("docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md")

        for term in (
            "PLATFORM_NATIVE_FIRST",
            "CAPABILITY_NOT_DEVICE_LABEL",
            "PROGRESSIVE_ENHANCEMENT_REQUIRED_FOR_NEWLY_AVAILABLE",
            "NATIVE_IS_NOT_AUTOMATIC_UX_PASS",
            "SUPPORT_STATUS_IS_DATED_EVIDENCE",
            "ACCESSIBILITY_INPUT_FALLBACK_REQUIRED",
            "LIVE_BEHAVIOR_EVIDENCE_OVER_CODE_SNIPPET",
            "RETIRED_SURFACE_IS_NOT_REACTIVATED",
        ):
            self.assertIn(term, guide)

        selection_order = (
            "Semantic HTML",
            "Native CSS",
            "Browser API",
            "기존 Base/프로젝트 구현",
            "검증된 경량 dependency",
            "Minimal Custom Implementation",
        )
        positions = [guide.index(term) for term in selection_order]
        self.assertEqual(positions, sorted(positions))

        for term in (
            "any-pointer",
            "any-hover",
            "keyboard",
            "hover-only",
            "verified_at",
            "WIDELY_AVAILABLE",
            "NEWLY_AVAILABLE",
            "LIMITED_OR_EXPERIMENTAL",
            "@supports",
            "fallback",
        ):
            self.assertIn(term, guide)

        self.assertIn("WEB_PLATFORM_NATIVE_UI_CAPABILITY_GUIDE.md", knowledge)
        self.assertIn("TOOL_HUB_RETIRED_FROM_ACTIVE_PROJECT_FLOW", retirement)
        self.assertIn("QA_EVIDENCE_STUDIO_RETIRED_FROM_ACTIVE_PROJECT_FLOW", retirement)


if __name__ == "__main__":
    unittest.main()
