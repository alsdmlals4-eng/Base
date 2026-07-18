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
            "skills/installing-game-project-operating-system/SKILL.md",
            "skills/migrating-existing-game-project-structure/SKILL.md",
            "skills/evolving-project-discipline-skills/SKILL.md",
            "skills/publishing-discipline-bibles/SKILL.md",
            "templates/project-operations/PROJECT_START_HERE.md",
            "templates/project-operations/PROJECT_DOCUMENTATION_MAP.md",
            "templates/project-operations/DEVELOPMENT_GATES.md",
            "templates/project-operations/DISCIPLINE_BIBLE.md",
            "templates/project-operations/PROJECT_SKILL_MAP.md",
            "templates/project-operations/DISCIPLINE_PDF_PUBLICATION.md",
            "templates/project-operations/PUBLICATION_MANIFEST.json",
            "templates/project-operations/EXISTING_PROJECT_MIGRATION_AUDIT.md",
            "templates/project-operations/LIFECYCLE_AREAS.md",
            "templates/project-operations/skills/FOUNDATION_SKILL.md",
            "templates/project-operations/skills/DISCIPLINE_SKILL.md",
            "templates/project-operations/skills/SKILL_LEARNING_LOG.md",
            "templates/project-operations/github/check_documentation_governance.py",
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
        self.assertIn("migrating-existing-game-project-structure", start)
        self.assertIn("publishing-discipline-bibles", start)
        self.assertIn("evolving-project-discipline-skills", start)

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
            self.assertNotIn(name, names, f"Duplicate skill name {name}: {names.get(name)} and {path}")
            names[name] = path

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

    def test_json_templates_are_valid(self) -> None:
        for relative in [
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


if __name__ == "__main__":
    unittest.main()
