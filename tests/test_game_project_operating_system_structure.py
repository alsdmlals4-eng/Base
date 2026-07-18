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
            "templates/project-operations/PROJECT_START_HERE.md",
            "templates/project-operations/PROJECT_DOCUMENTATION_MAP.md",
            "templates/project-operations/DEVELOPMENT_GATES.md",
            "templates/project-operations/DISCIPLINE_BIBLE.md",
            "templates/project-operations/PROJECT_SKILL_MAP.md",
            "templates/project-operations/SKILL_REGISTRY.json",
            "templates/project-operations/OPERATING_SYSTEM_HEALTH_REPORT.md",
            "templates/project-operations/DISCIPLINE_PDF_PUBLICATION.md",
            "templates/project-operations/PUBLICATION_MANIFEST.json",
            "templates/project-operations/EXISTING_PROJECT_MIGRATION_AUDIT.md",
            "templates/project-operations/LIFECYCLE_AREAS.md",
            "templates/project-operations/skills/FOUNDATION_SKILL.md",
            "templates/project-operations/skills/DISCIPLINE_SKILL.md",
            "templates/project-operations/skills/SKILL_LEARNING_LOG.md",
            "templates/project-operations/github/check_documentation_governance.py",
            "templates/project-operations/github/check_skill_routing_governance.py",
            "templates/project-operations/github/documentation-governance.json",
            "templates/project-operations/github/documentation-governance.yml",
            "templates/project-operations/github/ISSUE_TEMPLATE.yml",
            "templates/project-operations/github/PULL_REQUEST_TEMPLATE.md",
            "templates/project-operations/github/CODEOWNERS.example",
        ]
        missing = [path for path in required if not (ROOT / path).exists()]
        self.assertEqual(missing, [], f"Missing operating-system paths: {missing}")

    def test_minimum_base_invocation_is_preserved(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/alsdmlals4-eng/Base", start)
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
        text = (
            ROOT / "docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md"
        ).read_text(encoding="utf-8")
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
            self.assertNotIn(
                name,
                names,
                f"Duplicate skill name {name}: {names.get(name)} and {path}",
            )
            names[name] = path

    def test_base_skill_registry_is_valid_and_selective(self) -> None:
        registry = json.loads(
            (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        )
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

    def test_project_skill_map_covers_all_responsibility_disciplines(self) -> None:
        text = (
            ROOT / "templates/project-operations/PROJECT_SKILL_MAP.md"
        ).read_text(encoding="utf-8")
        disciplines = [
            "설정·내러티브",
            "게임 디자인",
            "UX·UI·접근성",
            "개발·엔지니어링",
            "테크니컬 아트·파이프라인",
            "아트",
            "사운드",
            "QA",
            "프로덕션·PM",
            "분석·유저리서치",
            "통합검수",
        ]
        missing = [discipline for discipline in disciplines if discipline not in text]
        self.assertEqual(missing, [], f"Missing discipline skill routes: {missing}")
        self.assertIn("SKILL_REGISTRY.json", text)
        self.assertIn("전체 스킬 자동 로드: 금지", text)
        self.assertIn("모든 의미 있는 스킬 호출", text)

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

        config = json.loads(
            (
                ROOT
                / "templates/project-operations/github/documentation-governance.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(config["design_root"], "[기획서]")
        self.assertTrue(config["enforce_top_level_design_root"])

    def test_json_templates_are_valid(self) -> None:
        for relative in [
            "skills/SKILL_REGISTRY.json",
            "templates/project-operations/SKILL_REGISTRY.json",
            "templates/project-operations/PUBLICATION_MANIFEST.json",
            "templates/project-operations/github/documentation-governance.json",
        ]:
            with self.subTest(path=relative):
                json.loads((ROOT / relative).read_text(encoding="utf-8"))

    def test_pdf_contract_requires_full_process_and_approved_images(self) -> None:
        text = (
            ROOT / "docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md"
        ).read_text(encoding="utf-8")
        for term in [
            "전체 작업 흐름",
            "승인된 이미지",
            "실제 게임 캡처",
            "Publication Manifest",
            "content hash",
            "read_only_derivative",
        ]:
            self.assertIn(term, text)

    def test_migration_contract_requires_audit_and_preservation(self) -> None:
        text = (
            ROOT / "docs/knowledge/methods/EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md"
        ).read_text(encoding="utf-8")
        for term in [
            "Audit only",
            "절대 보존 대상",
            "사용자 승인",
            "변경 전후 보존 검증",
            "[백업]",
            "[보류]",
            "[제거 후보]",
        ]:
            self.assertIn(term, text)

    def test_skill_evolution_contract_requires_always_learning_without_forced_rewrites(self) -> None:
        text = (
            ROOT / "docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md"
        ).read_text(encoding="utf-8")
        for term in [
            "모든 의미 있는 호출",
            "Learning Log",
            "load_by_default",
            "trigger_tags",
            "변경 없음",
            "verifying-game-project-operating-system",
        ]:
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
