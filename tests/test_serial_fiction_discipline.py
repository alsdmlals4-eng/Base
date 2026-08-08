from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "developing-and-revising-serial-fiction"
SKILL_PATH = ROOT / "skills" / SKILL_ID / "SKILL.md"
GUIDE_ROOT = ROOT / "docs" / "knowledge" / "serial-fiction"


class SerialFictionDisciplineContractTests(unittest.TestCase):
    def test_skill_and_knowledge_hub_exist(self) -> None:
        self.assertTrue(SKILL_PATH.is_file())
        for name in (
            "README.md",
            "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md",
            "SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md",
            "READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md",
        ):
            self.assertTrue((GUIDE_ROOT / name).is_file(), name)

    def test_registry_routes_serial_fiction_without_overrouting(self) -> None:
        registry = json.loads(
            (ROOT / "skills" / "SKILL_REGISTRY.json").read_text(encoding="utf-8")
        )
        matches = [
            entry for entry in registry["skills"] if entry["skill_id"] == SKILL_ID
        ]
        self.assertEqual(len(matches), 1)
        entry = matches[0]
        self.assertEqual(entry["status"], "ACTIVE")
        joined = "\n".join(
            entry["trigger_tags"] + entry["use_when"] + entry["do_not_use_when"]
        ).lower()
        for token in (
            "webnovel",
            "serial-fiction",
            "pov",
            "reader-feedback",
            "proofreading",
            "game",
        ):
            self.assertIn(token, joined)

    def test_craft_contract_prefers_episode_value_over_fixed_character_counts(self) -> None:
        writing = (
            GUIDE_ROOT / "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md"
        ).read_text(encoding="utf-8")
        pacing = (
            GUIDE_ROOT / "SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md"
        ).read_text(encoding="utf-8")
        combined = writing + "\n" + pacing
        for token in (
            "Reader Promise",
            "Episode Value",
            "Local Payoff",
            "Open Loop",
            "Information Legibility",
            "Pattern Variation",
            "Consequence Memory",
            "Setup–Payoff",
            "FRAMEWORK_OVERFIT",
            "PLATFORM_REVERIFY_REQUIRED",
        ):
            self.assertIn(token, combined)
        self.assertIn("universal", combined.lower())
        self.assertIn("production target", combined.lower())

    def test_reader_feedback_is_evidence_not_canon(self) -> None:
        text = (
            GUIDE_ROOT / "READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md"
        ).read_text(encoding="utf-8")
        for token in (
            "RAW_REACTION",
            "SYMPTOM_CLUSTER",
            "REVISION_HYPOTHESIS",
            "PRODUCT_FACT",
            "READER_RESPONSE",
            "CRAFT_HYPOTHESIS",
            "TRANSFER_DECISION",
        ):
            self.assertIn(token, text)
        self.assertIn("not canon", text.lower())
        self.assertIn("REJECT_COPY", text)

    def test_cold_start_routes_to_serial_fiction_owner(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs" / "DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        operating = (ROOT / "docs" / "OPERATING_MODEL.md").read_text(encoding="utf-8")
        for text in (start, docs, operating):
            self.assertIn(SKILL_ID, text)

    def test_behavior_evals_cover_primary_and_non_selection(self) -> None:
        primary = json.loads(
            (ROOT / "skills" / "SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8")
        )
        coverage = json.loads(
            (ROOT / "skills" / "SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(
            any(case.get("expected_primary_skill") == SKILL_ID for case in primary["cases"])
        )
        self.assertTrue(
            any(
                case.get("target_skill") == SKILL_ID
                and case.get("expected_selected") is False
                for case in coverage["cases"]
            )
        )

    def test_frozen_v9_release_artifacts_remain_frozen(self) -> None:
        snapshot = json.loads(
            (ROOT / "skills" / "BASE_V9_SKILL_SNAPSHOT.json").read_text(encoding="utf-8")
        )
        frozen_ids = {
            entry["skill_id"]
            for entry in snapshot.get("skills", snapshot.get("active_skills", []))
            if isinstance(entry, dict) and "skill_id" in entry
        }
        self.assertNotIn(SKILL_ID, frozen_ids)


if __name__ == "__main__":
    unittest.main()
