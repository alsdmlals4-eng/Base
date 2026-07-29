from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class V9MachineContractTests(unittest.TestCase):
    def test_base_version_and_release_contract_keep_rc_and_final_distinct(self) -> None:
        version = read("docs/BASE_RULES_VERSION.md")
        release = read("docs/operations/BASE_V9_RELEASE_CONTRACT.md")

        self.assertIn("v9.0.0-rc.1", version)
        self.assertIn("v9.0.0", release)
        self.assertIn("WAVE_2_HOLD", release)
        self.assertIn("최종 릴리스", release)

    def test_system_map_declares_complete_recoverable_workflow(self) -> None:
        system_map = read("docs/operations/BASE_V9_SYSTEM_MAP.md")

        for term in (
            "PLAN",
            "BUILD",
            "REVIEW",
            "적대적 검토",
            "증거 검증",
            "Base 승격 후보",
            "실패",
            "재개",
        ):
            self.assertIn(term, system_map)

    def test_maturity_model_is_risk_scaled_and_has_five_levels(self) -> None:
        maturity = read("docs/operations/BASE_V9_MATURITY_MODEL.md")

        for level in range(6):
            self.assertIn(f"Level {level}", maturity)
        self.assertIn("규모", maturity)
        self.assertIn("위험", maturity)
        self.assertIn("강제하지 않는다", maturity)

    def test_migration_map_preserves_open_pr_decisions_without_direct_merge(self) -> None:
        migration = read("docs/operations/BASE_V9_MIGRATION_MAP.md")

        for pr in ("#5", "#18", "#28", "#29", "#30"):
            self.assertIn(pr, migration)
        self.assertIn("직접 병합하지 않는다", migration)
        self.assertIn("ROLLBACK", migration)


if __name__ == "__main__":
    unittest.main()
