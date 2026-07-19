from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "templates/project-operations/github/check_design_document_publications.py"
SCHEMAS = ROOT / "schemas"


class DesignDocumentPublicationGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(SCHEMAS, self.root / "schemas")
        self.checker = self.root / "check.py"
        shutil.copy2(CHECKER, self.checker)
        self.hub = self.root / "[기획서]/00_프로젝트_허브"
        self.folder = self.root / "[기획서]/02_게임_디자인"
        self.tools = self.root / "tools"
        self.hub.mkdir(parents=True)
        self.folder.mkdir(parents=True)
        self.tools.mkdir()
        self.generator = self.tools / "build_design_documents.py"
        self.generator.write_text("# generator\n", encoding="utf-8")
        self.source = self.folder / "게임_기획서.json"
        self.source.write_text(json.dumps({
            "schema_version": 3, "document_id": "game-design-bible", "title": "게임 기획서",
            "discipline": "게임 디자인", "status": "ACTIVE",
            "overview": {"purpose": "목적", "summary": "요약", "next_action": "다음"},
            "workflow": [], "validation": [],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.pdf = self.folder / "게임_기획서.pdf"
        self.pdf.write_bytes(b"%PDF-1.7\n%%EOF")
        self.manifest = self.folder / "게임_기획서_PUBLICATION_MANIFEST.json"
        self.entry = {
            "document_id": "game-design-bible", "title": "게임 기획서", "discipline": "게임 디자인",
            "responsibility_coverage": ["프로젝트 전체"], "status": "ACTIVE",
            "source_path": "../02_게임_디자인/게임_기획서.json", "source_format": "json", "source_role": "structured_data",
            "publication_policy": "always_sync", "output_pdf": "../02_게임_디자인/게임_기획서.pdf", "output_docx": None,
            "asset_dir": None, "diagram_policy": "none",
            "publication_manifest": "../02_게임_디자인/게임_기획서_PUBLICATION_MANIFEST.json",
            "generator": "tools/build_design_documents.py",
        }
        self.registry = self.hub / "DESIGN_DOCUMENT_REGISTRY.json"
        self.config = self.root / "config.json"
        self._write_registry()
        self._write_manifest()
        self._write_config()

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def _digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _write_registry(self) -> None:
        self.registry.write_text(json.dumps({
            "schema_version": 3, "registry_role": "ai-design-document-router-and-publication-index",
            "project_name": "Test", "required_responsibility_coverage": ["프로젝트 전체"], "documents": [self.entry],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _write_manifest(self) -> None:
        data = {
            "schema_version": 3, "publication_id": "game-design-bible", "role": "human-readable-derivative",
            "source_path": self.entry["source_path"], "source_format": self.entry["source_format"],
            "source_sha256": self._digest(self.source), "input_sha256": "0" * 64,
            "generator": "tools/build_design_documents.py", "generator_sha256": self._digest(self.generator),
            "source_commit": "test", "generated_at": "1970-01-01T00:00:00+00:00",
            "output_docx": None, "output_docx_sha256": None,
            "output_pdf": self.entry["output_pdf"], "output_pdf_sha256": self._digest(self.pdf),
            "generated_assets": {}, "approved_visuals": {}, "source_images": {},
            "mermaid_sources": {}, "mermaid_svg": {}, "mermaid_png": {},
            "sync_status": "CURRENT", "automated_render_review": "PASSED", "rendered_page_count": 1,
            "human_visual_review": "NOT_RUN", "human_visual_review_pdf_sha256": None,
        }
        self.manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _write_config(self, human: bool = False) -> None:
        self.config.write_text(json.dumps({
            "design_root": "[기획서]", "design_document_registry": "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json",
            "enforce_design_document_publications": True, "require_human_design_document_visual_review": human,
            "required_design_document_coverage": ["프로젝트 전체"],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _run(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(self.checker), "--config", str(self.config)], cwd=self.root, capture_output=True, text=True, errors="replace", check=False)

    def test_current_json_publication_passes(self) -> None:
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_stale_source_fails(self) -> None:
        self.source.write_text(self.source.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source changed", result.stdout)

    def test_generator_change_fails(self) -> None:
        self.generator.write_text("# changed\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Generator hash mismatch", result.stdout)

    def test_invalid_pdf_header_fails(self) -> None:
        self.pdf.write_text("not pdf", encoding="utf-8")
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        data["output_pdf_sha256"] = self._digest(self.pdf)
        self.manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid file header", result.stdout)

    def test_human_review_hash_is_required_only_at_human_gate(self) -> None:
        self._write_config(human=True)
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("human_visual_review must be PASSED", result.stdout)

    def test_registered_markdown_passes_and_unregistered_copy_fails(self) -> None:
        self.source = self.folder / "게임_기획서.md"
        self.source.write_text("# 게임 기획서\n\n## 목표\nA\n\n## 배경과 의도\nB\n\n## 범위\nC\n\n## 규칙과 제약\nD\n\n## 검증과 완료 기준\nE\n", encoding="utf-8")
        self.entry.update({"source_path": "../02_게임_디자인/게임_기획서.md", "source_format": "markdown", "source_role": "narrative_spec"})
        self._write_registry(); self._write_manifest()
        valid = self._run()
        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
        (self.folder / "복제_기획서.md").write_text("# duplicate\n", encoding="utf-8")
        invalid = self._run()
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("Unregistered active Markdown design source", invalid.stdout)

    def test_schema_v2_registry_fails_with_migration_message(self) -> None:
        self.registry.write_text('{"schema_version": 1, "documents": []}\n', encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema v3 is required", result.stdout)

    def test_markdown_raw_html_is_rejected(self) -> None:
        self.source = self.folder / "게임_기획서.md"
        self.source.write_text(
            "# 게임 기획서\n\n## 목표\nA <span>raw</span>\n\n## 배경과 의도\nB\n\n"
            "## 범위\nC\n\n## 규칙과 제약\nD\n\n## 검증과 완료 기준\nE\n",
            encoding="utf-8",
        )
        self.entry.update({"source_path": "../02_게임_디자인/게임_기획서.md", "source_format": "markdown", "source_role": "narrative_spec"})
        self._write_registry()
        self._write_manifest()
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Raw HTML is forbidden", result.stdout)


if __name__ == "__main__":
    unittest.main()
