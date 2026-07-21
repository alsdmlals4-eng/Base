from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location(
    "check_skill_system_coverage",
    ROOT / "tools/check_skill_system_coverage.py",
)
checker = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(checker)


def package_text(skill_id: str) -> str:
    skill_dir = ROOT / "skills" / skill_id
    paths = [skill_dir / "SKILL.md"]
    references = skill_dir / "references"
    if references.is_dir():
        paths.extend(sorted(path for path in references.rglob("*") if path.is_file()))
    return "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in paths)


class SkillSystemCoverageTests(unittest.TestCase):
    def test_source_responsibilities_are_mapped_to_active_skills(self) -> None:
        self.assertEqual(checker.validate(), [])

    def test_requested_independent_skills_remain_distinct_and_optional(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in registry["skills"]}
        required = {
            "refactoring-with-contract-preservation",
            "simplifying-skill-bodies",
            "pruning-stale-and-nonfunctional-material",
            "synchronizing-local-and-github-state",
            "maintaining-long-running-task-continuity",
            "governing-game-user-research-coverage",
            "creating-user-learning-notes",
            "building-project-visual-dashboards",
            "diagnosing-game-engine-runtime-failures",
        }
        self.assertTrue(required.issubset(by_id))
        for skill_id in required:
            self.assertEqual(by_id[skill_id]["status"], "ACTIVE")
            self.assertFalse(by_id[skill_id]["load_by_default"], skill_id)
            self.assertTrue(by_id[skill_id]["trigger_tags"], skill_id)
            self.assertTrue(by_id[skill_id]["use_when"], skill_id)
            self.assertTrue(by_id[skill_id]["do_not_use_when"], skill_id)

    def test_games_user_research_contract_has_exactly_eleven_domains(self) -> None:
        text = (ROOT / "skills/governing-game-user-research-coverage/SKILL.md").read_text(encoding="utf-8")
        numbered = [
            line for line in text.splitlines()
            if re.match(r"^(?:[1-9]|10|11)\. ", line)
        ]
        self.assertEqual(len(numbered), 11)
        self.assertTrue(numbered[0].startswith("1. "))
        self.assertTrue(numbered[-1].startswith("11. "))

    def test_optimized_existing_skills_preserve_legacy_capabilities(self) -> None:
        required_terms = {
            "identifying-project-core": (
                "PROJECT_CORE",
                "CORE_SUPPORT",
                "MVP_SUPPORT",
                "CONTENT_VARIANT",
                "PRESENTATION_SHELL",
                "TECHNICAL_FOUNDATION",
                "candidate:",
                "dependents:",
                "CORE",
                "BOTH",
                "LATER",
                "IDENTIFIED",
                "PARTIAL",
                "CONFLICTED",
                "UNVERIFIED",
                "저장·호환성",
                "읽기 전용",
            ),
            "establishing-project-core": (
                "CORE_SEED",
                "CORE_PROPOSED",
                "CORE_STRESS_TESTED",
                "CORE_CONFIRMED",
                "CORE_REVISE",
                "CORE_REJECTED",
                "CORE_RECORDED",
                "INVARIANT",
                "CHANGEABLE",
                "REQUIRES_REAPPROVAL",
                "OUT_OF_SCOPE",
                "사용자 승인",
                "PoC·플레이테스트",
                "마이그레이션",
            ),
            "running-adversarial-review-and-refinement": (
                "작성자·블루팀",
                "레드팀",
                "검증자",
                "개선자",
                "회귀 검토자",
                "finding_id",
                "MUST_FIX",
                "SHOULD_FIX",
                "DEFER",
                "REJECT",
                "UNVERIFIED",
                "PASS_WITH_FOLLOWUP",
                "REVISE_AGAIN",
                "REJECT_CHANGE",
                "CRITICAL",
                "Schema",
                "롤백",
            ),
            "evolving-project-discipline-skills": (
                "Consolidation-first",
                "기존 통합 Skill의 mode",
                "load_all_skills",
                "automatic_selection",
                "require_trigger_match",
                "max_primary_discipline_skills",
                "max_foundation_skills",
                "LEGACY_SKILL_ALIASES.md",
                "OBSERVATION",
                "HYPOTHESIS",
                "PATTERN",
                "VERIFIED",
                "PROMOTION_CANDIDATE",
                "untouched 소비자",
            ),
            "analyzing-and-refining-game-concepts": (
                "`frame`",
                "`constrain`",
                "`sharpen`",
                "`structure`",
                "`benchmark-and-player-research`",
                "`playtest-and-experiment`",
                "`poc-contract`",
                "`recalibrate`",
                "`production-gate`",
                "BIG BLIND",
                "AMPLIFY",
                "SUPPORT",
                "NEUTRAL",
                "CONFLICT",
                "UNPROVEN",
                "Action-feedback latency",
                "Reward legibility",
                "Reward ladder",
                "Fatigue and inflation",
                "feedback_channel",
                "telemetry_events",
                "funnel_steps",
                "control_and_variants",
                "ADOPT",
                "ADAPT",
                "AVOID",
                "TEST",
                "IGNORE",
                "KEEP",
                "REMOVE",
                "RETEST",
                "PRODUCTION_READY",
                "REPEAT_POC",
                "HOLD",
                "STOP",
            ),
        }
        for skill_id, terms in required_terms.items():
            text = package_text(skill_id)
            for term in terms:
                self.assertIn(term, text, f"{skill_id} lost contract term: {term}")

    def test_optimization_report_and_machine_coverage_exist(self) -> None:
        self.assertTrue((ROOT / "docs/SKILL_SYSTEM_OPTIMIZATION_REPORT.md").is_file())
        self.assertTrue((ROOT / "docs/SKILL_COVERAGE_MAP.md").is_file())
        self.assertTrue((ROOT / "skills/SKILL_COVERAGE.json").is_file())


if __name__ == "__main__":
    unittest.main()
