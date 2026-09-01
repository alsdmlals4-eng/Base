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
                ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md",
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
            "governing-legacy-retention-and-archives",
            "evaluating-godot-assets-and-plugins-before-creation",
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

    def test_benchmark_work_sequence_and_feature_contract_routing_are_integrated_modes(self) -> None:
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        operating = (ROOT / "skills/managing-game-project-operating-system/SKILL.md").read_text(encoding="utf-8")
        design = (ROOT / "skills/managing-design-documents/SKILL.md").read_text(encoding="utf-8")
        concepts = (ROOT / "skills/analyzing-and-refining-game-concepts/SKILL.md").read_text(encoding="utf-8")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        decomposition = (ROOT / "skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md").read_text(encoding="utf-8")
        sequence_plan = (ROOT / "templates/planning/EXECUTION_SEQUENCE_PLAN.md").read_text(encoding="utf-8")

        self.assertIn("`decompose-and-sequence`", intake)
        self.assertIn("BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES", intake)
        self.assertIn("`benchmark-and-player-research`", concepts)
        self.assertIn("`playtest-and-experiment`", concepts)
        for decision in ("ADOPT", "ADAPT", "AVOID", "TEST", "IGNORE"):
            self.assertIn(decision, concepts)
        for tag in (
            "work-decomposition",
            "dependency-map",
            "feature-code-contract-modularity",
            "feature-contract-change",
            "feature-boundary-change",
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

        self.assertIn("작업 분해가 필요하지 않은 작은 기능을 포함해 `references/work-decomposition-and-sequencing.md`", intake)
        self.assertIn("## 2.2 기능별 코드·계약 모듈화", decomposition)
        self.assertIn("## 기능별 코드·계약 경계", sequence_plan)
        for source in (intake, operating, design):
            for token in (
                "PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json",
                "REPOSITORY_PRIMARY_CANON",
                "V4_NOTION_EXCEPTION_ONLY",
                "NO_NEW_NOTION_WRITE_BY_DEFAULT",
            ):
                self.assertIn(token, source)
        for source in (intake, decomposition, sequence_plan):
            self.assertIn("validate_work_contract_receipt.py", source)

    def test_benchmark_reverse_engineering_pipeline_is_required_check_consumed(self) -> None:
        guide = (ROOT / "docs/BENCHMARKING_REFERENCE_GUIDE.md").read_text(encoding="utf-8")
        method = (ROOT / "docs/knowledge/research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md").read_text(encoding="utf-8")
        benchmark = (ROOT / "templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md").read_text(encoding="utf-8")
        skill_guide = (ROOT / "docs/AI_SKILL_ADOPTION_GUIDE.md").read_text(encoding="utf-8")

        for surface in (guide, method, benchmark):
            for token in (
                "BENCHMARK_REVERSE_ENGINEERING_PATTERN_REUSE",
                "REUSABLE_UNIT_DISCOVERY",
                "MULTI_SOURCE_EXTRACTION",
                "MECHANIC_PATTERN_LIBRARY",
                "GENRE_FOUNDATION_REFERENCE",
                "NOVELTY_DELTA",
                "CLEAN_ROOM_REIMPLEMENTATION",
            ):
                self.assertIn(token, surface)

        for token in (
            "SYSTEM_PATTERN",
            "TOOL_PATTERN",
            "ASSET_MATERIAL_PATTERN",
            "UI_UX_PATTERN",
            "CONTENT_PATTERN",
            "WORKFLOW_PATTERN",
            "SKILL_PATTERN",
        ):
            self.assertIn(token, benchmark)

        for token in (
            "REVERSE_ENGINEERED_SKILL_WORKFLOW_CANDIDATE",
            "PATTERN_NOT_PACKAGE_COPY",
            "EVAL_BEFORE_PROMOTION",
        ):
            self.assertIn(token, skill_guide)

        for owner in (
            "AI_SKILL_ADOPTION_GUIDE.md",
            "PROJECT_LOCAL_ASSET_VAULT_POLICY.md",
            "CAPABILITY_COMPOSITION_MAP.md",
        ):
            self.assertIn(owner, guide)

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

    def test_grill_me_and_godot_product_handoff_are_integrated_modes(self) -> None:
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        aliases = (ROOT / "skills/LEGACY_SKILL_ALIASES.md").read_text(encoding="utf-8")
        intake = skill_package_text("managing-project-intake-and-work-contract")
        handoff = skill_package_text("maintaining-project-context-and-handoff")

        for tag in (
            "grill-me",
            "decision-interview",
            "godot-product-implementation-handoff",
            "godot-work-instruction",
            "godot-package-handoff",
            "gdscripting",
            "godot-runtime-test",
            "ci-cost-optimization",
            "ci-gate",
        ):
            self.assertIn(tag, registry)

        for alias in ("`grill-me`", "`grillme`", "`Grill Me`"):
            self.assertIn(alias, aliases)
        self.assertIn("managing-project-intake-and-work-contract", aliases)
        self.assertIn("한 번에 하나", intake)
        self.assertIn("모두 권장안대로", intake)
        for marker in (
            "CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER",
            "CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR",
            "CHANGE_PROPOSAL",
            "GPT_VISUAL_REQUEST",
        ):
            self.assertIn(marker, handoff)
        self.assertNotIn("PLAN_REVIEW_ONLY", handoff)
        self.assertNotIn("godot_runtime_files_only", handoff)

        for path in (
            "skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md",
            "skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md",
            "templates/project-operations/GRILL_ME_DECISION_RECORD.md",
            "templates/project-operations/MASTER_IMPLEMENTATION_PLAN.md",
            "templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md",
            "templates/project-operations/IMPLEMENTATION_PACKAGE_CONTRACT.md",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_first_prompt_aliases_and_alignment_are_integrated_modes(self) -> None:
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        aliases = (ROOT / "skills/LEGACY_SKILL_ALIASES.md").read_text(encoding="utf-8")
        intake = skill_package_text("managing-project-intake-and-work-contract")
        method = (ROOT / "docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md").read_text(encoding="utf-8")
        reference_path = ROOT / "skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md"

        self.assertTrue(reference_path.is_file())
        for term in (
            "`first-prompt`",
            "DIRECTION_ANCHOR",
            "TASK_AND_SUCCESS",
            "CONTEXT_AND_SOURCES",
            "CONSTRAINTS_AND_PROTECTED_SCOPE",
            "OUTPUT_AND_VALIDATION",
            "Grill Me alignment gate",
            "exact contract already approved",
            "approval reference",
        ):
            self.assertIn(term, intake)
        for alias in ("[좋은 프롬프트]", "좋은 프롬프트", "퍼스트 프롬프트", "first prompt"):
            self.assertIn(alias, aliases)
        self.assertIn("`first-prompt` + `contract` + `clarify`", aliases)
        self.assertIn("First-prompt direction anchoring", method)
        self.assertIn("instruction/context", method)
        self.assertNotIn('"skill_id":"first-prompt"', registry.replace(" ", ""))

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

    def test_confirmed_decision_sync_and_post_merge_review_contract(self) -> None:
        policy = (ROOT / "docs/CONFIRMED_DECISION_SYNC_POLICY.md").read_text(encoding="utf-8")
        grill = skill_package_text("managing-project-intake-and-work-contract")
        design = (ROOT / "skills/managing-design-documents/SKILL.md").read_text(encoding="utf-8")
        adversarial = skill_package_text("running-adversarial-review-and-refinement")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")

        for term in (
            "DUPLICATE_QUESTION",
            "RECOMMENDED_DEFAULT",
            "USER_DECISION_REQUIRED",
            "APPROVED_PENDING_CANON",
            "SHEET_UPDATED",
            "SYNCED",
            "NO_CONFLICT",
            "CONFLICT_FIXED",
        ):
            self.assertIn(term, policy)
        for file_path in (
            "templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md",
            "templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md",
        ):
            self.assertTrue((ROOT / file_path).is_file(), file_path)
        for term in ("질문 전 필수 대조", "중복 질문 판정", "답변 처리와 즉시 동기화"):
            self.assertIn(term, grill)
        self.assertIn("Preserve approved decisions immediately", design)
        self.assertIn("Post-merge attack lenses", adversarial)
        for tag in (
            "confirmed-decision-sync",
            "legacy-sheet-migration",
            "post-merge-review",
            "canonical-conflict",
        ):
            self.assertIn(tag, registry)

    def test_confirmed_decisions_are_consumed_by_intake_and_project_os(self) -> None:
        doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        operating = (ROOT / "skills/managing-game-project-operating-system/SKILL.md").read_text(encoding="utf-8")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")

        self.assertIn("→ CURRENT_CONFIRMED_DECISIONS.md", doc_map)
        for term in ("current_confirmed_decisions", "project_google_sheet", "related_open_and_recent_prs"):
            self.assertIn(term, intake)
            self.assertIn(term, operating)
        for term in ("RECOMMENDED_DEFAULT", "USER_DECISION_REQUIRED"):
            self.assertIn(term, intake)
        for term in ("install", "audit", "verify", "콜드 스타트"):
            self.assertIn(term, operating)
        for tag in ("decision-recovery", "pr-preflight", "project-cold-start"):
            self.assertIn(tag, registry)

    def test_repository_wide_audit_is_an_integrated_mode_with_consumers(self) -> None:
        adversarial = skill_package_text("running-adversarial-review-and-refinement")
        registry = (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        doc_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        prompt = (ROOT / "templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md").read_text(encoding="utf-8")

        for term in (
            "`repository-wide-audit`",
            "references/repository-wide-audit-protocol.md",
            "CURRENT_AUTHORITY",
            "UNTOUCHED_CONSUMER",
            "ALLOWED_LEGACY",
            "STALE_PROMPT_CONTRACT",
        ):
            self.assertIn(term, adversarial)

        for tag in (
            "repository-wide-audit",
            "full-file-audit",
            "stale-file-audit",
            "untouched-consumer-audit",
            "prompt-drift",
        ):
            self.assertIn(tag, registry)

        self.assertIn("repository-wide-audit", doc_map)
        self.assertIn("repository-wide-audit", prompt)
        self.assertNotIn('"skill_id":"repository-wide-adversarial-audit"', registry)


class ClaimIntentConsolidatedReferenceTests(unittest.TestCase):
    def test_claim_intent_gate_is_integrated_without_a_duplicate_skill(self) -> None:
        import json

        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        active = [entry for entry in registry["skills"] if entry["status"] == "ACTIVE"]
        self.assertEqual(30, len(active))
        owners = [entry for entry in active if entry["skill_id"] == "reviewing-and-validating-project-changes"]
        self.assertEqual(1, len(owners))
        owner = owners[0]
        for trigger in ("completion-claim", "claim-evidence", "intent-conformance", "hallucination-audit"):
            self.assertIn(trigger, owner["trigger_tags"])

        skill = (ROOT / owner["path"]).read_text(encoding="utf-8")
        reference_path = ROOT / "skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md"
        template = (ROOT / "templates/quality/PROJECT_CHANGE_VALIDATION.md").read_text(encoding="utf-8")
        operating = (ROOT / "docs/OPERATING_MODEL.md").read_text(encoding="utf-8")
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")

        self.assertTrue(reference_path.is_file())
        for token in (
            "`claim-and-intent-verification`",
            "MATERIAL_CLAIM_LEDGER",
            "INTENT_IMPLEMENTATION_FIDELITY_MATRIX",
            "COMPLETION_CLAIM_GATE",
        ):
            self.assertIn(token, skill)
        for token in ("Material Claim Ledger", "Intent–Implementation Fidelity Matrix", "Completion Claim Gate"):
            self.assertIn(token, template)
        for text in (operating, routing):
            self.assertIn("CLAIM_AND_INTENT_VERIFICATION_GATE", text)
            self.assertIn("BLOCKED_UNVERIFIED", text)


if __name__ == "__main__":
    unittest.main()
