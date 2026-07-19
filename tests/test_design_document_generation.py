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

from PIL import Image
from docx import Document

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
GENERATOR = REPOSITORY_ROOT / "tools/build_design_documents.py"
SUPPORT = REPOSITORY_ROOT / "tools/publication_v3.py"
DIAGRAM_GENERATOR = REPOSITORY_ROOT / "tools/design_document_diagrams.py"
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
class DesignDocumentGenerationTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.tools = self.root / "tools"
        self.tools.mkdir()
        for source in (GENERATOR, SUPPORT, DIAGRAM_GENERATOR):
            shutil.copy2(source, self.tools / source.name)
        shutil.copytree(SCHEMAS, self.root / "schemas")
        shutil.copy2(REPOSITORY_ROOT / "pnpm-lock.yaml", self.root / "pnpm-lock.yaml")
        self.hub = self.root / "[기획서]/00_프로젝트_허브"
        self.folder = self.root / "[기획서]/02_게임_디자인"
        self.hub.mkdir(parents=True)
        self.folder.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _run(self, registry: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        mermaid = REPOSITORY_ROOT / "node_modules/.bin/mmdc.cmd"
        chrome = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
        if mermaid.exists():
            env["BASE_MERMAID_CLI"] = str(mermaid)
        if chrome.exists():
            env["PUPPETEER_EXECUTABLE_PATH"] = str(chrome)
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, str(self.tools / GENERATOR.name), "--registry", str(registry), "--source-commit", "test", *extra],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            check=False,
        )

    def _registry(self, entry: dict) -> Path:
        registry = self.hub / "DESIGN_DOCUMENT_REGISTRY.json"
        registry.write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "registry_role": "ai-design-document-router-and-publication-index",
                    "project_name": "Test Project",
                    "documents": [entry],
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        return registry

    def test_json_generation_is_deterministic_and_failure_preserves_outputs(self) -> None:
        approved = self.folder / "게임_기획서.assets/approved/reference.png"
        approved.parent.mkdir(parents=True)
        Image.new("RGB", (1000, 560), "#E8EEFF").save(approved)
        source = self.folder / "게임_기획서.json"
        source.write_text(
            json.dumps(
                {
                    "schema_version": 3,
                    "document_id": "game-design-bible",
                    "document_kind": "discipline-bible",
                    "project": "Test Project",
                    "title": "게임 디자인 기획서",
                    "discipline": "게임 디자인",
                    "owner": "Game Design",
                    "status": "ACTIVE",
                    "metadata": {"last_reviewed": "2026-07-19"},
                    "overview": {"purpose": "목적", "player_value": "가치", "summary": "현재 요약", "next_action": "다음 작업"},
                    "quality_bar": ["동일 입력 재실행 diff 0"],
                    "responsibilities": {"owns": ["규칙"], "does_not_own": ["코드 구조"], "interfaces": ["개발·엔지니어링"]},
                    "workflow": [{"step": "입력"}, {"step": "검증"}],
                    "validation": [],
                    "current_state": [{"item": "핵심 루프", "confirmed": "확정", "implemented": "진행", "validated": "미검증"}],
                    "approved_visuals": [{"asset_id": "IMG-1", "title": "Reference", "path": "../02_게임_디자인/게임_기획서.assets/approved/reference.png", "status": "DIRECTION_APPROVED", "caption": "승인 기준", "include_in_publication": True}],
                    "definition_of_ready": ["목적이 명확하다."],
                    "definition_of_done": ["책임 원본과 PDF가 최신이다."],
                },
                ensure_ascii=False,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
        entry = {
            "document_id": "game-design-bible",
            "title": "게임 디자인 기획서",
            "discipline": "게임 디자인",
            "responsibility_coverage": ["게임 디자인"],
            "status": "ACTIVE",
            "source_path": "../02_게임_디자인/게임_기획서.json",
            "source_format": "json",
            "source_role": "structured_data",
            "publication_policy": "always_sync",
            "output_docx": "../02_게임_디자인/게임_기획서.docx",
            "output_pdf": "../02_게임_디자인/게임_기획서.pdf",
            "asset_dir": "../02_게임_디자인/게임_기획서.assets",
            "diagram_policy": "generated",
            "publication_manifest": "../02_게임_디자인/게임_기획서_PUBLICATION_MANIFEST.json",
            "generator": "tools/build_design_documents.py",
        }
        registry = self._registry(entry)
        first = self._run(registry, "--force")
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        outputs = [
            self.folder / "게임_기획서.docx",
            self.folder / "게임_기획서.pdf",
            self.folder / "게임_기획서_PUBLICATION_MANIFEST.json",
            self.folder / "게임_기획서.assets/generated/workflow.png",
            self.folder / "게임_기획서.assets/generated/status-summary.png",
            self.folder / "게임_기획서.assets/generated/responsibility-map.png",
        ]
        first_hashes = {path: digest(path) for path in outputs}
        second = self._run(registry)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(first_hashes, {path: digest(path) for path in outputs})
        with zipfile.ZipFile(outputs[0]) as archive:
            self.assertIn("word/document.xml", archive.namelist())
            self.assertTrue(any(name.startswith("word/media/") for name in archive.namelist()))
        document = Document(outputs[0])
        self.assertTrue(any("게임 디자인 기획서" in paragraph.text for paragraph in document.paragraphs))
        manifest = json.loads(outputs[2].read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 3)
        self.assertEqual(manifest["sync_status"], "CURRENT")
        self.assertEqual(manifest["human_visual_review"], "NOT_RUN")
        self.assertEqual(manifest["human_visual_review_pdf_sha256"], None)
        self.assertEqual(len(manifest["generated_assets"]), 3)

        source.write_text("{ invalid", encoding="utf-8")
        failed = self._run(registry, "--force")
        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual(first_hashes, {path: digest(path) for path in outputs})

    def test_markdown_generates_pdf_without_published_docx(self) -> None:
        source = self.folder / "게임_기획서.md"
        source.write_text(
            """# 게임 디자인 기획서

## 목표

**명확한 목표**와 `검증 가능한 규칙`을 둔다.

## 배경과 의도

[Base](https://github.com/alsdmlals4-eng/Base)를 기준으로 한다.

## 범위

- 포함 범위
- 제외 범위

## 규칙과 제약

| 규칙 | 상태 |
|---|---|
| PDF 상시 동기화 | 확정 |

## 검증과 완료 기준

```text
python -m unittest
```
""",
            encoding="utf-8",
        )
        registry = self._registry(
            {
                "document_id": "game-design-bible",
                "title": "게임 디자인 기획서",
                "discipline": "게임 디자인",
                "responsibility_coverage": ["게임 디자인"],
                "status": "ACTIVE",
                "source_path": "../02_게임_디자인/게임_기획서.md",
                "source_format": "markdown",
                "source_role": "narrative_spec",
                "publication_policy": "always_sync",
                "output_docx": None,
                "output_pdf": "../02_게임_디자인/게임_기획서.pdf",
                "asset_dir": None,
                "diagram_policy": "none",
                "publication_manifest": "../02_게임_디자인/게임_기획서_PUBLICATION_MANIFEST.json",
                "generator": "tools/build_design_documents.py",
                "required_sections": ["목표", "배경과 의도", "범위", "규칙과 제약", "검증과 완료 기준"],
            }
        )
        result = self._run(registry, "--force")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.folder / "게임_기획서.pdf").read_bytes().startswith(b"%PDF-"))
        self.assertFalse((self.folder / "게임_기획서.docx").exists())
        manifest = json.loads((self.folder / "게임_기획서_PUBLICATION_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertIsNone(manifest["output_docx"])
        self.assertEqual(manifest["source_format"], "markdown")

    def test_schema_v2_registry_fails_with_migration_message(self) -> None:
        registry = self.hub / "DESIGN_DOCUMENT_REGISTRY.json"
        registry.write_text('{"schema_version": 1, "documents": []}\n', encoding="utf-8")
        result = self._run(registry)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema v3 is required", result.stderr + result.stdout)

    @unittest.skipUnless(
        (REPOSITORY_ROOT / "node_modules/.bin/mmdc.cmd").exists()
        and Path("C:/Program Files/Google/Chrome/Application/chrome.exe").exists(),
        "Fixed Mermaid CLI and Chrome are required",
    )
    def test_markdown_mermaid_generates_source_svg_and_png(self) -> None:
        source = self.folder / "게임_기획서.md"
        source.write_text(
            """# 게임 디자인 기획서

## 목표

다이어그램이 포함된 문서를 검증한다.

## 배경과 의도

편집 가능한 원본과 삽입 자산을 함께 보존한다.

## 범위

Mermaid 한 개를 포함한다.

## 규칙과 제약

```mermaid
flowchart LR
    A[의도] --> B[검증]
```

## 검증과 완료 기준

MMD·SVG·PNG 해시가 Manifest에 기록된다.
""",
            encoding="utf-8",
        )
        registry = self._registry({
            "document_id": "game-design-bible",
            "title": "게임 디자인 기획서",
            "discipline": "게임 디자인",
            "responsibility_coverage": ["게임 디자인"],
            "status": "ACTIVE",
            "source_path": "../02_게임_디자인/게임_기획서.md",
            "source_format": "markdown",
            "source_role": "narrative_spec",
            "publication_policy": "always_sync",
            "output_docx": None,
            "output_pdf": "../02_게임_디자인/게임_기획서.pdf",
            "asset_dir": "../02_게임_디자인/게임_기획서.assets",
            "diagram_policy": "mermaid",
            "publication_manifest": "../02_게임_디자인/게임_기획서_PUBLICATION_MANIFEST.json",
            "generator": "tools/build_design_documents.py",
            "required_sections": ["목표", "배경과 의도", "범위", "규칙과 제약", "검증과 완료 기준"],
        })
        result = self._run(registry, "--force")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        assets = self.folder / "게임_기획서.assets/generated"
        self.assertTrue((assets / "mermaid-01.mmd").is_file())
        self.assertTrue((assets / "mermaid-01.svg").is_file())
        self.assertTrue((assets / "mermaid-01.png").is_file())
        manifest = json.loads((self.folder / "게임_기획서_PUBLICATION_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["mermaid_sources"]), 1)
        self.assertEqual(len(manifest["mermaid_svg"]), 1)
        self.assertEqual(len(manifest["mermaid_png"]), 1)


if __name__ == "__main__":
    unittest.main()
