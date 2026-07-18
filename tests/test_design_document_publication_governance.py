from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "templates/project-operations/github/check_design_document_publications.py"


class DesignDocumentPublicationGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.hub = self.root / "[기획서]/00_프로젝트_허브"
        self.folder = self.root / "[기획서]/02_게임_디자인"
        self.tools = self.root / "tools"
        self.hub.mkdir(parents=True)
        self.folder.mkdir(parents=True)
        self.tools.mkdir(parents=True)
        self.source = self.folder / "게임_기획서.json"
        self.docx = self.folder / "게임_기획서.docx"
        self.pdf = self.folder / "게임_기획서.pdf"
        self.assets = self.folder / "게임_기획서.assets/generated"
        self.assets.mkdir(parents=True)
        self.diagram = self.assets / "workflow.png"
        self.approved = self.folder / "게임_기획서.assets/approved.png"
        self.manifest = self.folder / "게임_기획서_PUBLICATION_MANIFEST.json"
        self.registry = self.hub / "DESIGN_DOCUMENT_REGISTRY.json"
        self.config = self.root / "governance.json"
        self.generator = self.tools / "build_design_documents.py"
        self.diagram_generator = self.tools / "design_document_diagrams.py"
        self.generator.write_text("# generator\n", encoding="utf-8")
        self.diagram_generator.write_text("# diagram generator\n", encoding="utf-8")
        self._write_source()
        self._write_outputs()
        self._write_registry()
        self._write_config()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    @staticmethod
    def _digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _write_source(self) -> None:
        self.source.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "document_id": "game-design-bible",
                    "title": "게임 디자인 기획서",
                    "discipline": "게임 디자인",
                    "status": "ACTIVE",
                    "approved_visuals": [],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def _write_outputs(self) -> None:
        self.docx.write_bytes(b"PK\x03\x04docx")
        self.pdf.write_bytes(b"%PDF-1.4\npdf")
        self.diagram.write_bytes(b"\x89PNG\r\n\x1a\ndiagram")
        self.approved.write_bytes(b"\x89PNG\r\n\x1a\napproved")
        self.manifest.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "publication_id": "game-design-bible",
                    "role": "human-readable-derivative",
                    "source_json": "../02_게임_디자인/게임_기획서.json",
                    "source_sha256": self._digest(self.source),
                    "generator": "tools/build_design_documents.py",
                    "generator_sha256": self._digest(self.generator),
                    "diagram_generator_sha256": self._digest(self.diagram_generator),
                    "output_docx": "../02_게임_디자인/게임_기획서.docx",
                    "output_docx_sha256": self._digest(self.docx),
                    "output_pdf": "../02_게임_디자인/게임_기획서.pdf",
                    "output_pdf_sha256": self._digest(self.pdf),
                    "generated_diagrams": {
                        "../02_게임_디자인/게임_기획서.assets/generated/workflow.png": self._digest(self.diagram)
                    },
                    "approved_visuals": {
                        "../02_게임_디자인/게임_기획서.assets/approved.png": self._digest(self.approved)
                    },
                    "status": "CURRENT",
                    "automated_render_review": "PASSED",
                    "rendered_page_count": 1,
                    "human_visual_review": "NOT_RUN",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def _write_registry(self) -> None:
        self.registry.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "registry_role": "ai-design-document-router-and-publication-index",
                    "human_presentation": {
                        "primary_reading_format": "PDF",
                        "editable_review_format": "DOCX",
                        "diagram_assets_required": True,
                        "approved_visuals_embedded": True,
                        "markdown_design_bibles_allowed": False,
                    },
                    "documents": [
                        {
                            "document_id": "game-design-bible",
                            "discipline": "게임 디자인",
                            "responsibility_coverage": ["게임 디자인"],
                            "status": "ACTIVE",
                            "source_json": "../02_게임_디자인/게임_기획서.json",
                            "output_docx": "../02_게임_디자인/게임_기획서.docx",
                            "output_pdf": "../02_게임_디자인/게임_기획서.pdf",
                            "asset_dir": "../02_게임_디자인/게임_기획서.assets",
                            "publication_manifest": "../02_게임_디자인/게임_기획서_PUBLICATION_MANIFEST.json",
                            "generator": "tools/build_design_documents.py",
                        }
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def _write_config(self) -> None:
        self.config.write_text(
            json.dumps(
                {
                    "design_root": "[기획서]",
                    "design_document_registry": "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json",
                    "enforce_design_document_publications": True,
                    "require_human_design_document_visual_review": False,
                    "design_document_diagram_generator": "tools/design_document_diagrams.py",
                    "required_design_document_coverage": ["게임 디자인"],
                    "forbidden_markdown_design_bible_names": ["DISCIPLINE_BIBLE.md"],
                    "forbidden_markdown_design_bible_suffixes": ["_기획서.md"],
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    def _run(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--config", str(self.config)],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_current_publication_passes(self) -> None:
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Design document publication governance passed.", result.stdout)

    def test_stale_source_fails(self) -> None:
        self.source.write_text(self.source.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source JSON changed", result.stdout)

    def test_generator_change_fails(self) -> None:
        self.generator.write_text("# changed generator\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("generator changed", result.stdout)

    def test_missing_diagram_fails(self) -> None:
        self.diagram.unlink()
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Diagram missing", result.stdout)

    def test_markdown_design_bible_fails(self) -> None:
        (self.folder / "게임_기획서.md").write_text("# forbidden\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Active Markdown design bible is forbidden", result.stdout)

    def test_missing_responsibility_coverage_fails(self) -> None:
        config = json.loads(self.config.read_text(encoding="utf-8"))
        config["required_design_document_coverage"] = ["게임 디자인", "QA"]
        self.config.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing active design document responsibility coverage: QA", result.stdout)

    def test_invalid_pdf_header_fails(self) -> None:
        self.pdf.write_bytes(b"not-a-pdf")
        manifest = json.loads(self.manifest.read_text(encoding="utf-8"))
        manifest["output_pdf_sha256"] = self._digest(self.pdf)
        self.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PDF has invalid file header", result.stdout)


if __name__ == "__main__":
    unittest.main()
