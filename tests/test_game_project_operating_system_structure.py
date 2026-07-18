from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GameProjectOperatingSystemStructureTests(unittest.TestCase):
    def test_required_operating_system_paths_exist(self) -> None:
        required = [
            "START_HERE.md",
            "AGENTS.md",
            "README.md",
            "docs/DOCUMENTATION_MAP.md",
            "docs/MVP_WORKFLOW_CHECKLIST.md",
            "docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md",
            "docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md",
            "docs/knowledge/methods/EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md",
            "docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md",
            "docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md",
            "skills/SKILL_REGISTRY.json",
            "skills/SKILL_LEARNING_LOG.md",
            "skills/routing-project-work-by-discipline/SKILL.md",
            "skills/maintaining-project-context-and-handoff/SKILL.md",
            "skills/verifying-game-project-operating-system/SKILL.md",
            "skills/installing-game-project-operating-system/SKILL.md",
            "skills/migrating-existing-game-project-structure/SKILL.md",
            "skills/evolving-project-discipline-skills/SKILL.md",
            "skills/publishing-discipline-bibles/SKILL.md",
            "tools/build_project_skill_map.py",
            "tools/skill_map_diagrams.py",
            "tools/build_design_documents.py",
            "tools/design_document_diagrams.py",
            "templates/project-operations/PROJECT_START_HERE.md",
            "templates/project-operations/ACTIVE_CONTEXT.md",
            "templates/project-operations/HANDOFF.md",
            "templates/project-operations/ROADMAP.md",
            "templates/project-operations/DECISION_LOG.md",
            "templates/project-operations/CHANGELOG.md",
            "templates/project-operations/BASE_RULES_VERSION.md",
            "templates/project-operations/PROJECT_DOCUMENTATION_MAP.md",
            "templates/project-operations/DEVELOPMENT_GATES.md",
            "templates/project-operations/DESIGN_DOCUMENT.json",
            "templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json",
            "templates/project-operations/SKILL_REGISTRY.json",
            "templates/project-operations/OPERATING_SYSTEM_HEALTH_REPORT.md",
            "templates/project-operations/EXISTING_PROJECT_MIGRATION_AUDIT.md",
            "templates/project-operations/LIFECYCLE_AREAS.md",
            "templates/project-operations/skills/FOUNDATION_SKILL.md",
            "templates/project-operations/skills/DISCIPLINE_SKILL.md",
            "templates/project-operations/skills/SKILL_LEARNING_LOG.md",
            "templates/project-operations/github/check_documentation_governance.py",
            "templates/project-operations/github/check_skill_routing_governance.py",
            "templates/project-operations/github/check_design_document_publications.py",
            "templates/project-operations/github/documentation-governance.json",
            "templates/project-operations/github/documentation-governance.yml",
            "templates/project-operations/github/ISSUE_TEMPLATE.yml",
            "templates/project-operations/github/PULL_REQUEST_TEMPLATE.md",
            "templates/project-operations/github/CODEOWNERS.example",
            "tests/test_design_document_publication_governance.py",
            "tests/test_design_document_generation.py",
        ]
        missing = [path for path in required if not (ROOT / path).exists()]
        self.assertEqual(missing, [], f"Missing operating-system paths: {missing}")

    def test_deprecated_markdown_bible_templates_are_absent(self) -> None:
        forbidden = [
            "templates/project-operations/DISCIPLINE_BIBLE.md",
            "templates/project-operations/PROJECT_SKILL_MAP.md",
            "templates/project-operations/DISCIPLINE_PDF_PUBLICATION.md",
            "templates/project-operations/PUBLICATION_MANIFEST.json",
        ]
        present = [path for path in forbidden if (ROOT / path).exists()]
        self.assertEqual(present, [], f"Deprecated active templates still exist: {present}")

    def test_minimum_base_invocation_is_preserved(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/alsdmlals4-eng/Base", start)
        for term in [
            "DESIGN_DOCUMENT_REGISTRY.json",
            "기획서 JSON",
            "기획서 PDF",
            "기획서 DOCX",
            "PROJECT_SKILL_MAP.pdf",
            "PROJECT_SKILL_MAP.docx",
        ]:
            self.assertIn(term, start)
        for skill in [
            "routing-project-work-by-discipline",
            "migrating-existing-game-project-structure",
            "publishing-discipline-bibles",
            "evolving-project-discipline-skills",
            "maintaining-project-context-and-handoff",
            "verifying-game-project-operating-system",
        ]:
            self.assertIn(skill, start)

    def test_gate_contract_contains_work_and_product_gates(self) -> None:
        text = (ROOT / "docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md").read_text(encoding="utf-8")
        for term in [
            "Definition of Ready",
            "Implementation Gate",
            "Verification Gate",
            "Documentation Gate",
            "Integration·Completion Gate",
            "Vertical Slice",
            "Feature Complete",
            "Content Complete",
            "Release Candidate",
        ]:
            self.assertIn(term, text)

    def test_skill_front_matter_names_are_unique(self) -> None:
        skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
        names: dict[str, Path] = {}
        for path in skill_files:
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^name:\s*['\"]?([^'\"\n]+)", text, re.MULTILINE)
            self.assertIsNotNone(match, f"Missing skill name: {path}")
            name = match.group(1).strip()
            self.assertNotIn(name, names, f"Duplicate skill name {name}: {names.get(name)} and {path}")
            names[name] = path

    def test_base_skill_registry_is_valid_and_selective(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        policy = registry["routing_policy"]
        self.assertFalse(policy["load_all_skills"])
        self.assertEqual(policy["default_selection"], "none")
        self.assertTrue(policy["require_trigger_match"])
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

    def test_project_skill_registry_defines_human_publications(self) -> None:
        registry = json.loads((ROOT / "templates/project-operations/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        human = registry["human_presentation"]
        self.assertEqual(human["source_of_truth"], "SKILL_REGISTRY.json")
        self.assertEqual(human["primary_reading_format"], "PROJECT_SKILL_MAP.pdf")
        self.assertEqual(human["editable_derivative"], "PROJECT_SKILL_MAP.docx")
        self.assertEqual(human["diagram_directory"], "PROJECT_SKILL_MAP.assets")
        self.assertFalse(human["markdown_skill_map_allowed"])
        self.assertEqual(set(registry["discipline_entrypoints"]), {
            "설정·내러티브", "게임 디자인", "UX·UI·접근성", "개발·엔지니어링",
            "테크니컬 아트·파이프라인", "아트", "사운드", "QA", "프로덕션·PM",
            "분석·유저리서치", "통합검수",
        })

    def test_design_document_templates_define_json_and_human_outputs(self) -> None:
        source = json.loads((ROOT / "templates/project-operations/DESIGN_DOCUMENT.json").read_text(encoding="utf-8"))
        registry = json.loads((ROOT / "templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertIn("document_id", source)
        self.assertIn("overview", source)
        self.assertIn("workflow", source)
        self.assertIn("approved_visuals", source)
        self.assertIn("definition_of_done", source)
        human = registry["human_presentation"]
        self.assertEqual(human["primary_reading_format"], "PDF")
        self.assertEqual(human["editable_review_format"], "DOCX")
        self.assertTrue(human["diagram_assets_required"])
        self.assertTrue(human["approved_visuals_embedded"])
        self.assertFalse(human["markdown_design_bibles_allowed"])
        example = registry["document_contract_example"]
        for field in ("source_json", "output_docx", "output_pdf", "asset_dir", "publication_manifest", "generator"):
            self.assertTrue(example[field])

    def test_project_template_places_design_folder_at_repository_root(self) -> None:
        for relative in [
            "templates/project-operations/README.md",
            "templates/project-operations/PROJECT_START_HERE.md",
            "templates/project-operations/PROJECT_DOCUMENTATION_MAP.md",
        ]:
            with self.subTest(path=relative):
                text = (ROOT / relative).read_text(encoding="utf-8")
                self.assertIn("저장소 루트", text)
                self.assertIn("[기획서]", text)
        config = json.loads((ROOT / "templates/project-operations/github/documentation-governance.json").read_text(encoding="utf-8"))
        self.assertEqual(config["design_root"], "[기획서]")
        self.assertTrue(config["enforce_top_level_design_root"])
        self.assertTrue(config["enforce_skill_map_publication"])
        self.assertTrue(config["enforce_design_document_publications"])
        self.assertEqual(config["design_document_registry"], "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json")

    def test_json_templates_are_valid(self) -> None:
        for relative in [
            "skills/SKILL_REGISTRY.json",
            "templates/project-operations/SKILL_REGISTRY.json",
            "templates/project-operations/DESIGN_DOCUMENT.json",
            "templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json",
            "templates/project-operations/github/documentation-governance.json",
        ]:
            with self.subTest(path=relative):
                json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_design_publication_contract_requires_full_process_and_approved_images(self) -> None:
        text = (ROOT / "docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md").read_text(encoding="utf-8")
        for term in [
            "AI용 구조화 JSON 책임 원본",
            "DOCX",
            "PDF",
            "workflow.png",
            "승인 이미지",
            "DESIGN_DOCUMENT_REGISTRY.json",
            "SHA-256",
            "전 페이지",
        ]:
            self.assertIn(term, text)

    def test_migration_contract_requires_audit_and_preservation(self) -> None:
        text = (ROOT / "docs/knowledge/methods/EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md").read_text(encoding="utf-8")
        for term in ["Audit only", "절대 보존 대상", "사용자 승인", "변경 전후 보존 검증", "[백업]", "[보류]", "[제거 후보]"]:
            self.assertIn(term, text)

    def test_skill_evolution_contract_requires_always_learning_without_forced_rewrites(self) -> None:
        text = (ROOT / "docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md").read_text(encoding="utf-8")
        for term in ["실패", "중요한 결정", "실제 검증 결과", "Learning Log", "load_by_default", "trigger_tags", "verifying-game-project-operating-system"]:
            self.assertIn(term, text)

    def test_project_kit_exposes_optional_discipline_catalog(self) -> None:
        config = json.loads((ROOT / "templates/project-operations/github/documentation-governance.json").read_text(encoding="utf-8"))
        registry = json.loads((ROOT / "templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(config["required_design_document_coverage"], ["프로젝트 전체"])
        self.assertEqual(config["required_skill_disciplines"], [])
        self.assertIn("게임 디자인", config["available_discipline_catalog"])
        self.assertEqual(registry["required_responsibility_coverage"], ["프로젝트 전체"])

    def test_direct_request_and_local_base_contracts_are_explicit(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        routing = (ROOT / "skills/routing-project-work-by-discipline/SKILL.md").read_text(encoding="utf-8")
        migration = (ROOT / "templates/project-operations/EXISTING_PROJECT_MIGRATION_AUDIT.md").read_text(encoding="utf-8")
        project_readme = (ROOT / "templates/project-operations/README.md").read_text(encoding="utf-8")
        self.assertIn("approved_direct_request", agents)
        self.assertIn("approved_direct_request", routing)
        self.assertNotIn("`PROJECT_SKILL_MAP.md`를 읽", routing)
        self.assertIn("기존 책임 원본", migration)
        self.assertIn("BASE_RULES_VERSION.md", project_readme)
        self.assertIn("프로젝트에 동기화된 Base", project_readme)

    def test_generic_publication_review_states_are_separate(self) -> None:
        config = json.loads((ROOT / "templates/project-operations/github/documentation-governance.json").read_text(encoding="utf-8"))
        checker = (ROOT / "templates/project-operations/github/check_documentation_governance.py").read_text(encoding="utf-8")
        self.assertFalse(config["require_human_publication_visual_review"])
        self.assertIn("automated_render_review", checker)
        self.assertIn("human_visual_review", checker)

    def test_missing_environment_contract_requests_user_action(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        shared = (ROOT / "docs/AI_SHARED_WORK_RULES.md").read_text(encoding="utf-8")
        project_agents = (ROOT / "templates/AGENTS.project.md").read_text(encoding="utf-8")
        for text in (agents, shared, project_agents):
            self.assertIn("설치", text)
            self.assertIn("권한", text)
            self.assertIn("확인", text)
            self.assertIn("사용자", text)
        self.assertIn("required_tools_and_files", agents)
        self.assertIn("required_permissions", agents)


if __name__ == "__main__":
    unittest.main()
