from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md"


class InputEventRatePerformanceValidationTests(unittest.TestCase):
    def test_input_event_rate_is_a_reproducible_performance_condition(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")

        for token in (
            "input_device_event_rate_and_accumulation",
            "polling/event rate",
            "accumulation/coalescing",
            "같은 Scene이라도 이벤트 빈도가 다르면 별도 workload",
            "exact engine version·OS·input mode·event rate·accumulation",
        ):
            self.assertIn(token, text)

    def test_godot_case_is_version_bounded_and_primary_source_linked(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")

        for token in (
            "Godot의 2026-08-24 Windows high-polling mouse 성능 사례",
            "Godot 4.7.2",
            "보편 임계값으로 사용하지 않고",
            "godotengine.org/article/fixing-high-polling-rate-mice-on-windows/",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
