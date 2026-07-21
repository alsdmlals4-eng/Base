from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class GameProjectOperatingSystemStructureTests(unittest.TestCase):
    def test_base_cold_start_distinguishes_project_templates_from_active_status(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        documentation_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        for required in (
            "Base 저장소 자체를 콜드 스타트할 때",
            "templates/project-operations/",
            "docs/CHANGELOG.md",
            "[수정제안서]/PROPOSAL_REGISTRY.json",
            "GitHub PR·Actions",
            "등록 없음",
        ):
            self.assertIn(required, start)
        self.assertIn("프로젝트 설치 템플릿을 활성 상태 문서로 오인하지 않는다", documentation_map)

    def test_required_operating_system_paths_exist(self) -> None:
        required = [
            "START_HERE.md",
            "AGENTS.md",
            "README.md",
            "docs/OPERATING_MODEL.md",
            "docs/DOCUMENTATION_MAP.md",
            "docs/MVP_WORKFLOW_CHECKLIST.md",
            "docs/WORK_MODE_AND_SKILL_ROUTING.md",
            "docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md",
            "docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md",
            "docs/knowledge/methods/EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md",
            "docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md",
            "docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md",
            "skills/SKILL_REGISTRY.json",
            "skills/LEGACY_SKILL_ALIASES.md",
            "skills/SKILL_LEARNING_LOG.md",
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-project-intake-and-work-contract/references/question-and-source-model.md",
            "skills/managing-project-intake-and-work-contract/references/ambiguity-and-closure.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/managing-design-documents/SKILL.md",
            "skills/managing-base-change-proposals/SKILL.md",
            "skills/evolving-project-discipline-skills/SKILL.md",
            "skills/pruning-stale-and-nonfunctional-material/SKILL.md",
            "skills/simplifying-skill-bodies/SKILL.md",
            "skills/refactoring-with-contract-preservation/SKILL.md",
            "skills/synchronizing-local-and-github-state/SKILL.md",
            "skills/maintaining-long-running-task-continuity/SKILL.md",
            "skills/governing-game-user-research-coverage/SKILL.md",
            "skills/creating-user-learning-notes/SKILL.md",
            "skills/building-project-visual-dashboards/SKILL.md",
            "skills/diagnosing-game-engine-runtime-failures/SKILL.md",
            "skills/SKILL_COVERAGE.json",
            "docs/SKILL_COVERAGE_MAP.md",
            "docs/SKILL_SYSTEM_OPTIMIZATION_REPORT.md",
            "tools/check_skill_system_coverage.py",
            "tests/test_skill_system_coverage.py",
            "skills/maintaining-project-context-and-handoff/SKILL.md",
            "skills/analyzing-and-refining-game-concepts/SKILL.md",
            "skills/identifying-project-core/SKILL.md",
            "skills/establishing-project-core/SKILL.md",
            "skills/running-adversarial-review-and-refinement/SKILL.md",
            "skills/designing-vertical-slices/SKILL.md",
            "skills/orchestrating-deepseek-worktrees/SKILL.md",
            "skills/reviewing-and-validating-project-changes/SKILL.md",
            "skills/auditing-canonical-reference-freshness/SKILL.md",
            "skills/designing-art-prompts-and-technique-cards/SKILL.md",
            "skills/auditing-and-refining-ui-art/SKILL.md",
            "schemas/base-skill-registry-v1.schema.json",
            "schemas/base-change-proposal-registry-v1.schema.json",
            "schemas/interview-registry-v1.schema.json",
            "[수정제안서]/README.md",
            "[수정제안서]/PROPOSAL_REGISTRY.json",
            "templates/BASE_CHANGE_PROPOSAL.md",
            "templates/planning/GAME_CONCEPT_DIRECTION_REVIEW.md",
            "templates/quality/PROJECT_CHANGE_VALIDATION.md",
            "templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md",
            "templates/project-operations/SKILL_EXECUTION_REPORT.md",
            "templates/project-operations/LEGACY_ARTIFACT_RECONCILIATION.md",
            "tools/check_base_change_proposals.py",
            "tools/check_canonical_reference_freshness.py",
            ".github/reference-freshness.json",
            "tests/test_reference_freshness.py",
            "tools/build_project_skill_map.py",
            "tools/build_design_documents.py",
            "tools/build_policy_driven_design_documents.py",
            "tools/check_publication_environment.py",
            "schemas/design-document-registry-v3.schema.json",
            "schemas/structured-design-document-v3.schema.json",
            "schemas/publication-manifest-v3.schema.json",
            "schemas/skill-registry-v3.schema.json",
            "templates/project-operations/PROJECT_START_HERE.md",
            "templates/project-operations/ACTIVE_CONTEXT.md",
            "templates/project-operations/INTERVIEW_REGISTRY.json",
            "templates/project-operations/INTERVIEW_RECORD.md",
            "templates/project-operations/HANDOFF.md",
            "templates/project-operations/ROADMAP.md",
            "templates/project-operations/DECISION_LOG.md",
            "templates/project-operations/CHANGELOG.md",
            "templates/project-operations/BASE_RULES_VERSION.md",
            "templates/project-operations/PROJECT_DOCUMENTATION_MAP.md",
            "templates/project-operations/DEVELOPMENT_GATES.md",
            "templates/project-operations/DESIGN_DOCUMENT.json",
            "templates/project-operations/DESIGN_DOCUMENT.md",
            "templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json",
            "templates/project-operations/SKILL_REGISTRY.json",
            "templates/project-operations/AI_WORKFLOW.md",
            "templates/project-operations/github/check_documentation_governance.py",
            "templates/project-operations/github/check_skill_routing_governance.py",
            "templates/project-operations/github/check_design_document_publications.py",
            "tests/test_design_document_publication_governance.py",
            "tests/test_design_document_generation.py",
        ]
        missing = [path for path in required if not (ROOT / path).exists()]
        self.assertEqual(missing, [], f"Missing operating-system paths: {missing}")

    def test_removed_skill_paths_are_absent(self) -> None:
        removed = [
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
        ]
        present = [path for path in removed if (ROOT / path).exists()]
        self.assertEqual(present, [], f"Merged skill files still active: {present}")

    def test_legacy_aliases_cover_every_removed_skill(self) -> None:
        aliases = (ROOT / "skills/LEGACY_SKILL_ALIASES.md").read_text(encoding="utf-8")
        for skill_id in (
            "routing-project-work-by-discipline",
            "conducting-deep-requirement-interviews",
            "transforming-requests-into-prompts",
            "installing-game-project-operating-system",
            "migrating-existing-game-project-structure",
            "verifying-game-project-operating-system",
            "writing-game-design-documents",
            "publishing-discipline-bibles",
            "promoting-project-knowledge",
            "reviewing-and-implementing-base-change-proposals",
            "reviewing-external-ai-drafts",
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "managing-design-documents",
            "managing-base-change-proposals",
            "reviewing-and-validating-project-changes",
        ):
            self.assertIn(f"`{skill_id}`", aliases)

    def test_minimum_base_invocation_routes_to_consolidated_skills(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        operating = (ROOT / "docs/OPERATING_MODEL.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/alsdmlals4-eng/Base", start)
        for skill in (
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "managing-design-documents",
            "evolving-project-discipline-skills",
            "maintaining-project-context-and-handoff",
            "analyzing-and-refining-game-concepts",
            "identifying-project-core",
            "establishing-project-core",
            "running-adversarial-review-and-refinement",
            "reviewing-and-validating-project-changes",
            "auditing-canonical-reference-freshness",
            "managing-base-change-proposals",
        ):
            self.assertIn(skill, start + operating)
        self.assertIn("LEGACY_SKILL_ALIASES.md", start)

    def test_skill_front_matter_names_are_unique(self) -> None:
        names: dict[str, Path] = {}
        for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^name:\s*['\"]?([^'\"\n]+)", text, re.MULTILINE)
            self.assertIsNotNone(match, f"Missing skill name: {path}")
            name = match.group(1).strip()
            self.assertNotIn(name, names, f"Duplicate skill name {name}: {names.get(name)} and {path}")
            names[name] = path

    def test_base_skill_registry_is_valid_selective_and_consolidated(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas/base-skill-registry-v1.schema.json").read_text(encoding="utf-8"))
        errors = sorted(Draft202012Validator(schema).iter_errors(registry), key=lambda error: list(error.path))
        self.assertEqual(errors, [], [error.message for error in errors])
        policy = registry["routing_policy"]
        self.assertFalse(policy["load_all_skills"])
        self.assertEqual(policy["default_selection"], "automatic-trigger-match")
        self.assertTrue(policy["automatic_selection"])
        self.assertFalse(policy["user_skill_declaration_required"])
        self.assertTrue(policy["require_trigger_match"])
        self.assertTrue(policy["require_execution_report"])
        self.assertEqual(policy["work_modes"], ["PLAN", "BUILD", "REVIEW"])
        self.assertEqual(len(registry["skills"]), 25)
        seen: set[str] = set()
        for item in registry["skills"]:
            skill_id = item["skill_id"]
            self.assertNotIn(skill_id, seen)
            seen.add(skill_id)
            self.assertFalse(item["load_by_default"])
            self.assertTrue(item["trigger_tags"])
            self.assertTrue(item["use_when"])
            self.assertTrue(item["do_not_use_when"])
            self.assertTrue(item["review_triggers"])
            self.assertTrue((ROOT / item["path"]).is_file())
            self.assertTrue((ROOT / item["learning_log"]).is_file())
        self.assertTrue({
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "managing-design-documents",
            "analyzing-and-refining-game-concepts",
            "reviewing-and-validating-project-changes",
            "auditing-canonical-reference-freshness",
            "managing-base-change-proposals",
        }.issubset(seen))

    def test_project_core_and_adversarial_skills_have_distinct_contracts(self) -> None:
        identify = (ROOT / "skills/identifying-project-core/SKILL.md").read_text(encoding="utf-8")
        establish = (ROOT / "skills/establishing-project-core/SKILL.md").read_text(encoding="utf-8")
        adversarial = (ROOT / "skills/running-adversarial-review-and-refinement/SKILL.md").read_text(encoding="utf-8")
        for term in ("PROJECT_CORE", "MVP_SUPPORT", "removal-and-change-test", "UNVERIFIED"):
            self.assertIn(term, identify)
        for term in ("CORE_PROPOSED", "CORE_STRESS_TESTED", "CORE_CONFIRMED", "사용자 승인", "REQUIRES_REAPPROVAL"):
            self.assertIn(term, establish)
        for term in ("attack", "validate-critique", "refine-approved-findings", "regression-recheck", "MUST_FIX", "REJECT"):
            self.assertIn(term, adversarial)
        self.assertIn("읽기 전용", identify)
        self.assertIn("사용자 승인 없이", establish)
        self.assertIn("비판도 오류·취향·과잉 요구", adversarial)

    def test_work_mode_skill_and_skill_mode_are_distinct_and_automatic(self) -> None:
        routing = (ROOT / "docs/WORK_MODE_AND_SKILL_ROUTING.md").read_text(encoding="utf-8")
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        report = (ROOT / "templates/project-operations/SKILL_EXECUTION_REPORT.md").read_text(encoding="utf-8")
        for term in ("Work Mode", "Skill Mode", "PLAN", "BUILD", "REVIEW", "자동 선택"):
            self.assertIn(term, routing)
            self.assertIn(term, intake)
        for term in ("사용한 Work Mode·Skill·Skill Mode", "사용한 이유", "얻은 결과"):
            self.assertIn(term, routing + intake + report)
        self.assertIn("user_skill_declaration_required: false", report)

    def test_unified_skill_modes_preserve_separate_safety_boundaries(self) -> None:
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        operating = (ROOT / "skills/managing-game-project-operating-system/SKILL.md").read_text(encoding="utf-8")
        documents = (ROOT / "skills/managing-design-documents/SKILL.md").read_text(encoding="utf-8")
        concepts = (ROOT / "skills/analyzing-and-refining-game-concepts/SKILL.md").read_text(encoding="utf-8")
        validation = (ROOT / "skills/reviewing-and-validating-project-changes/SKILL.md").read_text(encoding="utf-8")
        freshness = (ROOT / "skills/auditing-canonical-reference-freshness/SKILL.md").read_text(encoding="utf-8")
        proposals = (ROOT / "skills/managing-base-change-proposals/SKILL.md").read_text(encoding="utf-8")
        for mode in ("route", "clarify", "contract", "execution-report"):
            self.assertIn(f"`{mode}`", intake)
        for mode in ("install", "audit", "reconcile-legacy", "migrate", "verify"):
            self.assertIn(f"`{mode}`", operating)
        self.assertIn("읽기 전용", operating)
        self.assertIn("approved_migration_table", operating)
        self.assertIn("approved_legacy_reconciliation_table", operating)
        for decision in ("UPDATE_IN_PLACE", "MERGE_TO_CANONICAL", "COMPATIBILITY_STUB", "ARCHIVE_HISTORY", "DELETE_APPROVED", "KEEP_UNRESOLVED"):
            self.assertIn(decision, operating)
        for mode in ("author", "update", "restructure", "publish", "validate"):
            self.assertIn(f"`{mode}`", documents)
        for policy in ("source_only", "milestone_sync", "always_sync"):
            self.assertIn(policy, documents)
        for mode in ("frame", "constrain", "sharpen", "structure", "analyze", "poc-contract", "recalibrate", "production-gate"):
            self.assertIn(f"`{mode}`", concepts)
        for phase in ("CONCEPT_SEED", "POINTED_FUN_HYPOTHESIS", "POC_BUILD_AND_TEST", "PRODUCTION_READY"):
            self.assertIn(phase, concepts)
        for lens in ("SWOT", "SO", "WO", "ST", "WT", "MDA", "DDE", "DDD"):
            self.assertIn(lens, concepts)
        self.assertIn("임의 해석하지 않는다", concepts)
        for mode in ("contract-check", "external-source-review", "reference-freshness", "static-validation", "runtime-validation", "regression", "evidence-report"):
            self.assertIn(f"`{mode}`", validation)
        for decision in ("ACCEPT", "REVISE", "REJECT", "UNVERIFIED"):
            self.assertIn(decision, validation)
        for mode in ("impact-map", "reference-scan", "content-drift", "derivative-freshness", "propagation-gap", "closure-report"):
            self.assertIn(f"`{mode}`", freshness)
        for finding in ("STALE_REFERENCE", "MISSING_PROPAGATION", "CONFLICTING_SOURCE", "DERIVATIVE_STALE", "ALLOWED_LEGACY"):
            self.assertIn(finding, freshness)
        for mode in ("extract", "submit", "review", "implement", "verify"):
            self.assertIn(f"`{mode}`", proposals)
        self.assertIn("approval_ref", proposals)
        self.assertIn("제안 PR과", proposals)
        self.assertIn("구현 PR", proposals)

    def test_operating_model_is_single_explanatory_source(self) -> None:
        operating = (ROOT / "docs/OPERATING_MODEL.md").read_text(encoding="utf-8")
        for term in (
            "작업 생명주기",
            "책임 원본",
            "source_only",
            "milestone_sync",
            "always_sync",
            "lifecycle_status",
            "approval_status",
            "implementation_status",
            "verification_status",
            "publication_status",
            "뾰족한 재미",
            "Digital Dopamine Design",
            "reviewing-and-validating-project-changes",
            "auditing-canonical-reference-freshness",
            "reference-freshness",
        ):
            self.assertIn(term, operating)
        for relative in ("README.md", "START_HERE.md", "AGENTS.md", "docs/DOCUMENTATION_MAP.md"):
            self.assertIn("docs/OPERATING_MODEL.md", (ROOT / relative).read_text(encoding="utf-8"))

    def test_gate_contract_contains_work_and_product_gates(self) -> None:
        text = (ROOT / "docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md").read_text(encoding="utf-8")
        for term in (
            "Definition of Ready",
            "Implementation Gate",
            "Verification Gate",
            "Documentation Gate",
            "Integration·Completion Gate",
            "Vertical Slice",
            "Feature Complete",
            "Content Complete",
            "Release Candidate",
        ):
            self.assertIn(term, text)

    def test_skill_evolution_is_consolidation_first(self) -> None:
        text = (ROOT / "skills/evolving-project-discipline-skills/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "기존 통합 Skill의 mode",
            "Consolidation-first",
            "LEGACY_SKILL_ALIASES.md",
            "auditing-canonical-reference-freshness",
            "load_by_default",
            "Learning Log",
            "managing-game-project-operating-system",
        ):
            self.assertIn(term, text)

    def test_project_learning_requires_proposal_before_base_implementation(self) -> None:
        proposals = (ROOT / "skills/managing-base-change-proposals/SKILL.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for text in (proposals, agents):
            self.assertIn("[수정제안서]", text)
            self.assertIn("사용자 승인", text)
            self.assertIn("별도 구현 PR", text)
        self.assertIn("제안 PR에는 원칙적으로 `[수정제안서]/**`만", proposals)
        self.assertIn("approval_ref", proposals)

    def test_project_skill_registry_defines_human_publications(self) -> None:
        registry = json.loads((ROOT / "templates/project-operations/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        human = registry["human_presentation"]
        policy = registry["routing_policy"]
        self.assertEqual(human["source_of_truth"], "SKILL_REGISTRY.json")
        self.assertEqual(human["primary_reading_format"], "PROJECT_SKILL_MAP.pdf")
        self.assertIsNone(human["editable_derivative"])
        self.assertEqual(human["diagram_directory"], "PROJECT_SKILL_MAP.assets")
        self.assertEqual(human["markdown_summary"], "PROJECT_SKILL_MAP.md")
        self.assertEqual(registry["schema_version"], 3)
        self.assertEqual(policy["default_selection"], "automatic-trigger-match")
        self.assertTrue(policy["automatic_selection"])
        self.assertFalse(policy["user_skill_declaration_required"])
        self.assertTrue(policy["require_execution_report"])

    def test_design_document_templates_define_hybrid_sources_and_outputs(self) -> None:
        source = json.loads((ROOT / "templates/project-operations/DESIGN_DOCUMENT.json").read_text(encoding="utf-8"))
        registry = json.loads((ROOT / "templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json").read_text(encoding="utf-8"))
        markdown = (ROOT / "templates/project-operations/DESIGN_DOCUMENT.md").read_text(encoding="utf-8")
        self.assertEqual(source["schema_version"], 3)
        self.assertIn("approved_visuals", source)
        self.assertIn("definition_of_done", source)
        self.assertEqual(registry["schema_version"], 3)
        example = registry["document_contract_example"]
        self.assertIn(example["publication_policy"], {"source_only", "milestone_sync", "always_sync"})
        for field in ("source_path", "output_pdf", "publication_manifest", "generator"):
            self.assertTrue(example[field])
        for heading in ("## 목표", "## 배경과 의도", "## 범위", "## 규칙과 제약", "## 검증과 완료 기준"):
            self.assertIn(heading, markdown)

    def test_project_template_places_design_folder_at_repository_root(self) -> None:
        for relative in (
            "templates/project-operations/README.md",
            "templates/project-operations/PROJECT_START_HERE.md",
            "templates/project-operations/PROJECT_DOCUMENTATION_MAP.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("저장소 루트", text)
            self.assertIn("[기획서]", text)
        config = json.loads((ROOT / "templates/project-operations/github/documentation-governance.json").read_text(encoding="utf-8"))
        self.assertEqual(config["design_root"], "[기획서]")
        self.assertTrue(config["enforce_top_level_design_root"])
        self.assertTrue(config["enforce_skill_map_publication"])
        self.assertTrue(config["enforce_design_document_publications"])

    def test_json_templates_are_valid(self) -> None:
        for relative in (
            "skills/SKILL_REGISTRY.json",
            ".github/reference-freshness.json",
            "templates/project-operations/SKILL_REGISTRY.json",
            "templates/project-operations/DESIGN_DOCUMENT.json",
            "templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json",
            "templates/project-operations/github/documentation-governance.json",
        ):
            json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_missing_environment_contract_requests_user_action(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        shared = (ROOT / "docs/AI_SHARED_WORK_RULES.md").read_text(encoding="utf-8")
        project_agents = (ROOT / "templates/AGENTS.project.md").read_text(encoding="utf-8")
        for text in (agents, shared, project_agents):
            self.assertIn("설치", text)
            self.assertIn("권한", text)
            self.assertIn("확인", text)
            self.assertIn("사용자", text)

    def test_project_templates_route_deep_interview_to_unified_intake(self) -> None:
        for relative in (
            "AGENTS.md",
            "START_HERE.md",
            "templates/AGENTS.project.md",
            "templates/project-operations/AI_WORKFLOW.md",
            "templates/project-operations/PROJECT_START_HERE.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertIn("managing-project-intake-and-work-contract", text)
            self.assertIn("사용자", text)


if __name__ == "__main__":
    unittest.main()
