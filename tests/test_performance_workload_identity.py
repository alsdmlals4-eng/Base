from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md"


class PerformanceWorkloadIdentityTests(unittest.TestCase):
    def test_display_geometry_is_part_of_reproducible_performance_capture(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")

        for token in (
            "display_viewport_render_scale_and_coordinate_space",
            "viewport/window 크기",
            "render scale/stretch/embedded-window",
            "배치 밀도·픽셀 부하·충돌/상호작용 수",
            "같은 workload로 직접 비교하지 않는다",
        ):
            self.assertIn(token, text)

    def test_godot_benchmark_failure_case_is_source_linked_and_bounded(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")

        for token in (
            "Godot Benchmarks의 2026-08-25 workload-identity 교정 사례",
            "get_viewport_rect().size",
            "godotengine/godot-benchmarks/pull/141",
            "godotengine/godot-benchmarks/issues/140",
            "보편 성능 수치나 임계값으로 승격하지 않는다",
        ):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
