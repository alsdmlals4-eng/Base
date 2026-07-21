from __future__ import annotations

import hashlib
import json
import os
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
SUPPORT = REPOSITORY_ROOT / "tools/publication_v3.py"
DIAGRAM_GENERATOR = REPOSITORY_ROOT / "tools/skill_map_diagrams.py"
SCHEMAS = REPOSITORY_ROOT / "schemas"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def publication_tools_available() -> bool:
    libreoffice = os.environ.get("BASE_LIBREOFFICE") or shutil.which("libreoffice") or shutil.which("soffice")
    pdftoppm = os.environ.get("BASE_PDFTOPPM") or shutil.which("pdftoppm")
    return bool(libreoffice and Path(libreoffice).is_file() and pdftoppm and Path(pdftoppm).is_file())


@unittest.skipUnless(
    publication_tools_available(),
    "LibreOffice and pdftoppm are required",
)
class ProjectSkillMapGenerationTests(unittest.TestCase):
    def test_registry_generates_optional_markdown_docx_pdf_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            tools = root / "tools"
            tools.mkdir()
            for source in (GENERATOR, SUPPORT, DIAGRAM_GENERATOR):
                shutil.copy2(source, tools / source.name)
            shutil.copytree(SCHEMAS, root / "schemas")
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
                        "schema_version": 3,
                        "registry_role": "project-skill-router-and-learning-index",
                        "routing_policy": {
                            "load_all_skills": False,
                            "default_selection": "automatic-trigger-match",
                            "automatic_selection": True,
                            "user_skill_declaration_required": False,
                            "require_trigger_match": True,
                            "require_execution_report": True,
                            "work_modes": ["PLAN", "BUILD", "REVIEW"],
                            "max_primary_discipline_skills": 1,
                            "max_foundation_skills": 3,
                        },
                        "human_presentation": {
                            "primary_reading_format": "PROJECT_SKILL_MAP.pdf",
                            "editable_derivative": "PROJECT_SKILL_MAP.docx",
                            "diagram_directory": "PROJECT_SKILL_MAP.assets",
                            "publication_manifest": "SKILL_MAP_PUBLICATION_MANIFEST.json",
                            "generator": "tools/build_project_skill_map.py",
                            "source_of_truth": "SKILL_REGISTRY.json",
                            "markdown_summary": "PROJECT_SKILL_MAP.md",
                        },
                        "skills": [{
                            "skill_id": "test-skill", "layer": "foundation", "discipline": "project-operations",
                            "path": "skills/foundation/test-skill/SKILL.md", "status": "ACTIVE", "load_by_default": False,
                            "trigger_tags": ["test"], "use_when": ["테스트에서 사용"], "do_not_use_when": ["테스트 외 사용하지 않음"],
                            "learning_log": "skills/foundation/test-skill/LEARNING_LOG.md", "review_triggers": ["실패"],
                            "last_reviewed_at": "2026-07-19", "last_reviewed_commit": "test", "knowledge_state": "OBSERVATION",
                        }],
                        "selected_disciplines": ["게임 디자인"],
                        "discipline_entrypoints": {discipline: (["test-skill"] if discipline == "게임 디자인" else []) for discipline in disciplines},
                    },
                    ensure_ascii=False,
                    indent=2,
                ) + "\n",
                encoding="utf-8",
            )
            command = [
                sys.executable, str(tools / GENERATOR.name), "--registry", str(registry), "--output-dir", str(hub),
                "--project-name", "Test Project", "--source-commit", "test",
            ]
            first = subprocess.run(command, cwd=root, capture_output=True, text=True, errors="replace", check=False)
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            paths = [
                hub / "PROJECT_SKILL_MAP.md", hub / "PROJECT_SKILL_MAP.docx", hub / "PROJECT_SKILL_MAP.pdf",
                hub / "SKILL_MAP_PUBLICATION_MANIFEST.json",
                hub / "PROJECT_SKILL_MAP.assets/skill-flow.png",
                hub / "PROJECT_SKILL_MAP.assets/discipline-routing.png",
                hub / "PROJECT_SKILL_MAP.assets/skill-matrix.png",
            ]
            hashes = {path: digest(path) for path in paths}
            second = subprocess.run(command, cwd=root, capture_output=True, text=True, errors="replace", check=False)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            self.assertEqual(hashes, {path: digest(path) for path in paths})
            self.assertIn("자동 생성 파생본", paths[0].read_text(encoding="utf-8"))
            self.assertIn(digest(registry), paths[0].read_text(encoding="utf-8"))
            with zipfile.ZipFile(paths[1]) as archive:
                self.assertIn("word/document.xml", archive.namelist())
                self.assertTrue(any(name.startswith("word/media/") for name in archive.namelist()))
            document = Document(paths[1])
            self.assertTrue(any("프로젝트 스킬 지도" in paragraph.text for paragraph in document.paragraphs))
            manifest = json.loads(paths[3].read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], 3)
            self.assertEqual(manifest["sync_status"], "CURRENT")
            self.assertEqual(manifest["automated_render_review"], "PASSED")
            self.assertEqual(manifest["human_visual_review"], "NOT_RUN")
            self.assertEqual(len(manifest["generated_assets"]), 3)


if __name__ == "__main__":
    unittest.main()
