from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from PIL import Image
from docx import Document

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = REPOSITORY_ROOT / "tools/build_design_documents.py"
DIAGRAM_GENERATOR = REPOSITORY_ROOT / "tools/design_document_diagrams.py"


@unittest.skipUnless(shutil.which("libreoffice") and shutil.which("pdftoppm"), "LibreOffice and pdftoppm are required")
class DesignDocumentGenerationTests(unittest.TestCase):
    def test_json_generates_docx_pdf_diagrams_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            tools = root / "tools"
            tools.mkdir()
            shutil.copy2(GENERATOR, tools / GENERATOR.name)
            shutil.copy2(DIAGRAM_GENERATOR, tools / DIAGRAM_GENERATOR.name)
            hub = root / "[기획서]/00_프로젝트_허브"
            folder = root / "[기획서]/02_게임_디자인"
            approved = folder / "게임_기획서.assets/approved/reference.png"
            approved.parent.mkdir(parents=True)
            Image.new("RGB", (1000, 560), "#E8EEFF").save(approved)
            source = folder / "게임_기획서.json"
            source.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "document_id": "game-design-bible",
                        "document_kind": "discipline-bible",
                        "project": "Test Project",
                        "title": "게임 디자인 기획서",
                        "discipline": "게임 디자인",
                        "owner": "Game Design",
                        "status": "ACTIVE",
                        "metadata": {"last_reviewed": "2026-07-19"},
                        "overview": {"purpose": "목적", "player_value": "가치", "summary": "현재 요약"},
                        "responsibilities": {"owns": ["규칙"], "does_not_own": ["코드 구조"], "interfaces": []},
                        "workflow": [{"step": "입력"}, {"step": "검증"}],
                        "current_state": [{"item": "핵심 루프", "confirmed": "확정", "implemented": "진행", "validated": "미검증"}],
                        "approved_visuals": [{"asset_id": "IMG-1", "title": "Reference", "path": "../02_게임_디자인/게임_기획서.assets/approved/reference.png", "status": "DIRECTION_APPROVED", "include_in_publication": True}],
                        "definition_of_ready": ["목적이 명확하다."],
                        "definition_of_done": ["JSON·DOCX·PDF가 최신이다."],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            hub.mkdir(parents=True)
            registry = hub / "DESIGN_DOCUMENT_REGISTRY.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "documents": [{
                            "document_id": "game-design-bible",
                            "status": "ACTIVE",
                            "source_json": "../02_게임_디자인/게임_기획서.json",
                            "output_docx": "../02_게임_디자인/게임_기획서.docx",
                            "output_pdf": "../02_게임_디자인/게임_기획서.pdf",
                            "asset_dir": "../02_게임_디자인/게임_기획서.assets",
                            "publication_manifest": "../02_게임_디자인/게임_기획서_PUBLICATION_MANIFEST.json",
                            "generator": "tools/build_design_documents.py",
                        }],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(tools / GENERATOR.name), "--registry", str(registry), "--source-commit", "test"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            docx_path = folder / "게임_기획서.docx"
            pdf_path = folder / "게임_기획서.pdf"
            manifest_path = folder / "게임_기획서_PUBLICATION_MANIFEST.json"
            self.assertTrue(docx_path.is_file())
            self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF-"))
            self.assertTrue((folder / "게임_기획서.assets/generated/workflow.png").is_file())
            self.assertTrue((folder / "게임_기획서.assets/generated/status-summary.png").is_file())
            self.assertTrue((folder / "게임_기획서.assets/generated/responsibility-map.png").is_file())
            with zipfile.ZipFile(docx_path) as archive:
                self.assertIn("word/document.xml", archive.namelist())
                self.assertTrue(any(name.startswith("word/media/") for name in archive.namelist()))
            document = Document(docx_path)
            self.assertTrue(any("게임 디자인 기획서" in paragraph.text for paragraph in document.paragraphs))
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["automated_render_review"], "PASSED")
            self.assertGreaterEqual(manifest["rendered_page_count"], 1)
            self.assertEqual(len(manifest["generated_diagrams"]), 3)
            self.assertEqual(len(manifest["approved_visuals"]), 1)


if __name__ == "__main__":
    unittest.main()
