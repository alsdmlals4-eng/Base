from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OLD_SKILL_PATHS = (
    "skills/routing-project-work-by-discipline/SKILL.md",
    "skills/conducting-deep-requirement-interviews/SKILL.md",
    "skills/transforming-requests-into-prompts/SKILL.md",
    "skills/installing-game-project-operating-system/SKILL.md",
    "skills/migrating-existing-game-project-structure/SKILL.md",
    "skills/verifying-game-project-operating-system/SKILL.md",
    "skills/writing-game-design-documents/SKILL.md",
    "skills/publishing-discipline-bibles/SKILL.md",
    "skills/promoting-project-knowledge/SKILL.md",
    "skills/reviewing-and-implementing-base-change-proposals/SKILL.md",
    "skills/reviewing-external-ai-drafts/SKILL.md",
)
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py"}


def skill_package_text(skill_id: str) -> str:
    skill_dir = ROOT / "skills" / skill_id
    paths = [skill_dir / "SKILL.md"]
    references = skill_dir / "references"
    if references.is_dir():
        paths.extend(sorted(path for path in references.rglob("*") if path.is_file()))
    return "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in paths)


class ConsolidatedSkillReferenceTests(unittest.TestCase):
    def test_active_entrypoints_and_templates_have_no_deleted_skill_paths(self) -> None:
        candidates = [
            ROOT / "AGENTS.md",
            ROOT / "START_HERE.md",
            ROOT / "README.md",
            ROOT / "docs/OPERATING_MODEL.md",
            ROOT / "docs/DOCUMENTATION_MAP.md",
            ROOT / "docs/AI_SHARED_WORK_RULES.md",
            ROOT / "docs/AI_WORKFLOW_RULES.md",
            ROOT / "docs/AI_SKILL_ADOPTION_GUIDE.md",
            ROOT / "docs/MVP_WORKFLOW_CHECKLIST.md",
        ]
        candidates += [
            path for path in (ROOT / "templates").rglob("*")
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
        ]
        candidates += [
            path for path in (ROOT / "skills").rglob("*")
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
            and path.name != "LEGACY_SKILL_ALIASES.md"
        ]
        stale: list[str] = []
        for path in sorted(set(candidates)):
            text = path.read_text(encoding="utf-8", errors="replace")
            for old_path in OLD_SKILL_PATHS:
                if old_path in text:
                    stale.append(f"{path.relative_to(ROOT)} -> {old_path}")
        self.assertEqual(stale, [], "Deleted skill paths remain in active entrypoints/templates:\n" + "\n".join(stale))

    def test_new_skill_paths_are_present_in_active_entrypoints(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in (
                ROOT / "AGENTS.md",
                ROOT / "START_HERE.md",
                ROOT / "README.md",
                ROOT / "docs/OPERATING_MODEL.md",
                ROOT / "docs/DOCUMENTATION_MAP.md",
                ROOT / "templates/project-operations/AI_WORKFLOW.md",
            )
        )
        for skill_id in (
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "managing-design-documents",
            "managing-base-change-proposals",
            "analyzing-and-refining-game-concepts",
            "reviewing-and-validating-project-changes",
            "auditing-canonical-reference-freshness",
        ):
            self.assertIn(skill_id, combined)

    def test_digital_dopamine_design_contract_is_explicit_and_bounded(self) -> None:
        package = skill_package_text("analyzing-and-refining-game-concepts")
        template = (ROOT / "templates/planning/GAME_CONCEPT_DIRECTION_REVIEW.md").read_text(encoding="utf-8")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")

        for term in (
            "Digital Dopamine Design",
            "첫 의미 있는 보상",
            "Action-feedback latency",
            "Reward legibility",
            "Reward ladder",
            "Fatigue and inflation",
            "실제 도파민 분비량",
            "뾰족한 재미를 빠르게 전달",
        ):
            self.assertIn(term, package)

        for term in (
            "첫 의미 있는 보상까지의 시간",
            "행동 → 피드백 지연",
            "Micro → Session → Meta 보상 사다리",
            "실제 도파민 분비나 의학적 중독",
        ):
            self.assertIn(term, template)

        for tag in (
            "digital-dopamine-design",
            "rapid-reward",
            "instant-feedback",
            "reward-latency",
        ):
            self.assertIn(tag, registry)

        self.assertIn("의미 있는 선택 없이 빠른 보상만 반복", package)
        self.assertIn("외부 자료에서 정의되지 않은 DDD", package)

    def test_benchmark_and_work_sequence_are_integrated_modes_not_new_skills(self) -> None:
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        concepts = (ROOT / "skills/analyzing-and-refining-game-concepts/SKILL.md").read_text(encoding="utf-8")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")

        self.assertIn("`decompose-and-sequence`", intake)
        self.assertIn("BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES", intake)
        self.assertIn("`benchmark-and-player-research`", concepts)
        self.assertIn("`playtest-and-experiment`", concepts)
        for decision in ("ADOPT", "ADAPT", "AVOID", "TEST", "IGNORE"):
            self.assertIn(decision, concepts)
        for tag in (
            "work-decomposition",
            "dependency-map",
            "benchmark-research",
            "player-reviews",
            "playtest-design",
            "funnel-analysis",
            "ab-testing",
        ):
            self.assertIn(tag, registry)

        for path in (
            "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md",
            "skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md",
            "templates/planning/EXECUTION_SEQUENCE_PLAN.md",
            "templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_playtest_accessibility_and_performance_gaps_are_integrated(self) -> None:
        concepts = skill_package_text("analyzing-and-refining-game-concepts")
        vertical = (ROOT / "skills/designing-vertical-slices/SKILL.md").read_text(encoding="utf-8")
        validation = (ROOT / "skills/reviewing-and-validating-project-changes/SKILL.md").read_text(encoding="utf-8")
        reference = (ROOT / "skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md").read_text(encoding="utf-8")
        operating = (ROOT / "docs/OPERATING_MODEL.md").read_text(encoding="utf-8")
        workflow = (ROOT / "templates/project-operations/AI_WORKFLOW.md").read_text(encoding="utf-8")

        for term in ("feedback_channel", "telemetry_events", "funnel_steps", "control_and_variants"):
            self.assertIn(term, concepts)
        for mode in ("slice-contract", "quality-bar", "pipeline-proof", "playtest-evidence", "decision-gate"):
            self.assertIn(f"`{mode}`", vertical)
        for mode in ("accessibility-review", "performance-profile"):
            self.assertIn(f"`{mode}`", validation)
            self.assertIn(mode, operating)
            self.assertIn(mode, workflow)
        for term in (
            "Xbox Accessibility Guidelines",
            "법적 준수",
            "frame time",
            "CPU·GPU·메모리·네트워크",
            "target player",
        ):
            self.assertIn(term, reference)

    def test_official_evidence_sources_are_recorded(self) -> None:
        benchmark = (ROOT / "skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md").read_text(encoding="utf-8")
        sequence = (ROOT / "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md").read_text(encoding="utf-8")
        quality = (ROOT / "skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md").read_text(encoding="utf-8")

        for source in (
            "partner.steamgames.com/doc/store/reviews",
            "partner.steamgames.com/doc/features/playtest",
            "docs.unity.com/en-us/analytics/events/events",
            "docs.unity.com/en-us/analytics/funnels/funnels",
            "docs.unity.com/en-us/game-overrides/ab-testing",
        ):
            self.assertIn(source, benchmark)
        for source in ("scrumguides.org/scrum-guide.html", "docs.github.com/en/issues"):
            self.assertIn(source, sequence)
        for source in ("learn.microsoft.com/en-us/xbox/accessibility", "dev.epicgames.com/documentation", "docs.unity3d.com"):
            self.assertIn(source, quality)


if __name__ == "__main__":
    unittest.main()
