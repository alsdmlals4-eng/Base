from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "developing-and-revising-serial-fiction"
SKILL_PATH = ROOT / "skills" / SKILL_ID / "SKILL.md"
GUIDE_ROOT = ROOT / "docs" / "knowledge" / "serial-fiction"
REFERENCE_ROOT = ROOT / "skills" / SKILL_ID / "references"


class SerialFictionDisciplineContractTests(unittest.TestCase):
    def test_skill_and_knowledge_hub_exist(self) -> None:
        self.assertTrue(SKILL_PATH.is_file())
        for name in (
            "README.md",
            "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md",
            "SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md",
            "SERIAL_NARRATIVE_INFORMATION_AND_HIGHLIGHT_GUIDE.md",
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

    def test_character_and_opponent_integrity_is_a_real_contract_surface(self) -> None:
        skill = SKILL_PATH.read_text(encoding="utf-8")
        reference_path = REFERENCE_ROOT / "character-distinctiveness-and-opponent-threat.md"
        self.assertTrue(reference_path.is_file())
        reference = reference_path.read_text(encoding="utf-8")
        combined = skill + "\n" + reference
        for token in (
            "character-and-opponent-integrity",
            "CHARACTER_IDENTITY_BLUR",
            "OPPONENT_THREAT_UNPROVEN",
            "OFFSCREEN_STRENGTH_ONLY",
            "VICTORY_BY_OPPONENT_DEFLATION",
            "SUPPORTING_CAST_STEALS_CLIMAX",
            "own turn",
            "KEEP / RESTORE / REWORK / NEW / REMOVE",
            "SKILL",
            "TACTIC",
            "RULE",
            "RELATION",
        ):
            self.assertIn(token, combined)

    def test_information_choice_highlight_and_foreshadow_contract_is_explicit(self) -> None:
        guide = (
            GUIDE_ROOT / "SERIAL_NARRATIVE_INFORMATION_AND_HIGHLIGHT_GUIDE.md"
        ).read_text(encoding="utf-8")
        for token in (
            "WITHHOLD_INFORMATION_NOT_CONTEXT",
            "CONTEXT_WITHHELD_AS_MYSTERY",
            "CHOICE_PROOF",
            "SURPRISING_BUT_COHERENT",
            "IDENTITY + COMPETENCE + COST + CHOICE + CONSEQUENCE",
            "HIGHLIGHT_WITHOUT_COST_OR_CHOICE",
            "RECONTEXTUALIZE",
            "AFTERMATH",
            "READER_KNOWLEDGE_MATRIX",
            "FALSE_SUSPENSE_BY_POV_SUPPRESSION",
        ):
            self.assertIn(token, guide)

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

    def test_canon_migration_contract_distinguishes_enforcement_and_completion(self) -> None:
        """Catch a migration contract that lets known legacy debt become completion."""
        skill = SKILL_PATH.read_text(encoding="utf-8")
        guide = (
            GUIDE_ROOT / "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md"
        ).read_text(encoding="utf-8")
        combined = skill + "\n" + guide
        for token in (
            "STRICT_NOW",
            "FORBIDDEN_IN_NEW_OR_REVISED",
            "BOUNDED_LEGACY_RECONCILIATION_DEBT",
            "SCOPED_STRICT",
            "actual_legacy_debt_consumers == declared_debt_consumers",
            "PASS_WITH_KNOWN_DEBT",
            "CANON_MIGRATION_COMPLETE",
            "archive/reference-only",
            "CANON_MIGRATION_DEBT_EXPANDED",
            "CANON_MIGRATION_COMPLETION_OVERCLAIM",
        ):
            self.assertIn(token, combined)

    def test_reconciliation_frontier_contract_blocks_false_continuity_and_promotion(self) -> None:
        """Catch an unvalidated frontier that invents normal legacy continuity."""
        skill = SKILL_PATH.read_text(encoding="utf-8")
        guide = (
            GUIDE_ROOT / "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md"
        ).read_text(encoding="utf-8")
        freshness = (
            ROOT / "skills" / "auditing-canonical-reference-freshness" / "SKILL.md"
        ).read_text(encoding="utf-8")
        combined = skill + "\n" + guide + "\n" + freshness
        for token in (
            "VERIFIED_PREFIX",
            "DECLARED_MIGRATION_BOUNDARY",
            "LEGACY_TAIL",
            "FRONTIER_VERIFICATION_STATUS",
            "candidate frontier",
            "derived consumer",
            "normal continuity",
            "FRONTIER_PROMOTION_WITHOUT_VALIDATION",
            "UNVERIFIED_MIGRATION_BOUNDARY_CONTINUITY",
            "DUPLICATE_CURRENT_AUTHORITY",
        ):
            self.assertIn(token, combined)

    def test_cold_start_routes_to_serial_fiction_owner(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs" / "DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        operating = (ROOT / "docs" / "OPERATING_MODEL.md").read_text(encoding="utf-8")
        for text in (start, docs, operating):
            self.assertIn(SKILL_ID, text)
        self.assertIn("연재소설", operating)
        self.assertIn("연재소설", docs)
        self.assertNotIn("Base는 게임 프로젝트가", operating)
        self.assertNotIn("Base는 여러 게임 프로젝트가", docs)

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
        combined_cases = primary["cases"] + coverage["cases"]
        self.assertTrue(
            any(SKILL_ID in case.get("forbidden_skills", []) for case in combined_cases)
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
