from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from docx import Document

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = REPOSITORY_ROOT / "tools/build_project_skill_map.py"
DIAGRAM_GENERATOR = REPOSITORY_ROOT / "tools/skill_map_diagrams.py"


@unittest.skipUnless(
    (shutil.which("libreoffice") or shutil.which("soffice")) and shutil.which("pdftoppm"),
    "LibreOffice and pdftoppm are required",
)
class ProjectSkillMapGenerationTests(unittest.TestCase):
    def test_registry_generates_docx_pdf_diagrams_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            tools = root / "tools"
            tools.mkdir()
            shutil.copy2(GENERATOR, tools / GENERATOR.name)
            shutil.copy2(DIAGRAM_GENERATOR, tools / DIAGRAM_GENERATOR.name)
            hub = root / "[기획서]/00_프로젝트_허브"
            skill = root / "skills/foundation/test-skill/SKILL.md"
            log = root / "skills/foundation/test-skill/LEARNING_LOG.md"
            hub.mkdir(parents=True)
            skill.parent.mkdir(parents=True)
            skill.write_text("# Skill\n", encoding="utf-8")
            log.write_text("# Log\n", encoding="utf-8")
            disciplines = [
                "설정·내러티브", "게임 디자인", "UX·UI·접근성", "개발·엔지니어링",
                "테크니컬 아트·파이프라인", "아트", "사운드", "QA", "프로덕션·PM",
                "분석·유저리서치", "통합검수",
            ]
            registry = hub / "SKILL_REGISTRY.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "routing_policy": {
                            "load_all_skills": False,
                            "default_selection": "none",
                            "require_trigger_match": True,
                            "max_primary_discipline_skills": 1,
                            "max_foundation_skills": 3,
                        },
                        "human_presentation": {
                            "primary_reading_format": "PROJECT_SKILL_MAP.pdf",
                            "editable_derivative": "PROJECT_SKILL_MAP.docx",
                            "diagram_directory": "PROJECT_SKILL_MAP.assets",
                            "publication_manifest": "SKILL_MAP_PUBLICATION_MANIFEST.json",
                            "source_of_truth": "SKILL_REGISTRY.json",
                            "markdown_skill_map_allowed": False,
                        },
                        "skills": [{
                            "skill_id": "test-skill",
                            "layer": "foundation",
                            "discipline": "project-operations",
                            "path": "skills/foundation/test-skill/SKILL.md",
                            "status": "ACTIVE",
                            "load_by_default": False,
                            "trigger_tags": ["test"],
                            "use_when": ["테스트에서 사용"],
                            "do_not_use_when": ["테스트 외 사용하지 않음"],
                            "learning_log": "skills/foundation/test-skill/LEARNING_LOG.md",
                            "review_triggers": ["실패"],
                            "last_reviewed_at": "2026-07-19",
                            "last_reviewed_commit": "test",
                            "knowledge_state": "OBSERVATION",
                        }],
                        "discipline_entrypoints": {discipline: ["test-skill"] for discipline in disciplines},
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(tools / GENERATOR.name),
                    "--registry",
                    str(registry),
                    "--output-dir",
                    str(hub),
                    "--project-name",
                    "Test Project",
                    "--source-commit",
                    "test",
                ],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            docx_path = hub / "PROJECT_SKILL_MAP.docx"
            pdf_path = hub / "PROJECT_SKILL_MAP.pdf"
            manifest_path = hub / "SKILL_MAP_PUBLICATION_MANIFEST.json"
            self.assertTrue(docx_path.is_file())
            self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF-"))
            for name in ("skill-flow.png", "discipline-routing.png", "skill-matrix.png"):
                self.assertTrue((hub / "PROJECT_SKILL_MAP.assets" / name).is_file())
            with zipfile.ZipFile(docx_path) as archive:
                self.assertIn("word/document.xml", archive.namelist())
                self.assertTrue(any(name.startswith("word/media/") for name in archive.namelist()))
            document = Document(docx_path)
            self.assertTrue(any("프로젝트 스킬 지도" in paragraph.text for paragraph in document.paragraphs))
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "CURRENT")
            self.assertEqual(manifest["automated_render_review"], "PASSED")
            self.assertEqual(len(manifest["diagram_paths"]), 3)


if __name__ == "__main__":
    unittest.main()
