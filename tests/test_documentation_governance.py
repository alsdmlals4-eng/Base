from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = (
    REPOSITORY_ROOT
    / "templates"
    / "project-operations"
    / "github"
    / "check_documentation_governance.py"
)


class DocumentationGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.config_path = self.root / "governance.json"

        required = [
            "AGENTS.md",
            "[기획서]/00_프로젝트_허브/START_HERE.md",
            "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
            "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md",
            "[기획서]/00_프로젝트_허브/DOCUMENT_UPDATE_MATRIX.md",
            "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
            "[기획서]/00_프로젝트_허브/PROJECT_SKILL_MAP.md",
            "[기획서]/00_프로젝트_허브/AI_WORKFLOW.md",
            "[기획서]/00_프로젝트_허브/PUBLICATION_MANIFEST.json",
            "skills/foundation",
        ]
        for relative in required:
            path = self.root / relative
            if Path(relative).suffix:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# {path.stem}\n", encoding="utf-8")
            else:
                path.mkdir(parents=True, exist_ok=True)

        self.source = self.root / "[기획서]/02_게임_디자인/게임_기획서.md"
        self.source.parent.mkdir(parents=True, exist_ok=True)
        self.source.write_text("# 게임 기획서\n\n현재 책임 원본.\n", encoding="utf-8")

        self.pdf = self.root / "[기획서]/02_게임_디자인/게임_기획서.pdf"
        self.pdf.write_bytes(b"%PDF-1.4\n% test publication\n")

        self.publication_manifest = (
            self.root / "[기획서]/00_프로젝트_허브/PUBLICATION_MANIFEST.json"
        )
        self._write_publication_manifest()
        self._write_config()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _digest(self) -> str:
        relative = "[기획서]/02_게임_디자인/게임_기획서.md"
        digest = hashlib.sha256()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(self.source.read_bytes())
        digest.update(b"\0")
        return digest.hexdigest()

    def _write_publication_manifest(self) -> None:
        data = {
            "schema_version": 1,
            "publications": [
                {
                    "publication_id": "game-design-bible",
                    "discipline": "게임 디자인",
                    "role": "read_only_derivative",
                    "source_files": [
                        "[기획서]/02_게임_디자인/게임_기획서.md"
                    ],
                    "approved_image_paths": [],
                    "output_pdf": "[기획서]/02_게임_디자인/게임_기획서.pdf",
                    "source_commit": "test",
                    "content_sha256": self._digest(),
                    "generated_at": "2026-07-18T00:00:00Z",
                    "generator": "unit-test",
                    "status": "CURRENT",
                    "automated_render_review": "PASSED",
                    "human_visual_review": "NOT_RUN",
                }
            ],
        }
        self.publication_manifest.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _write_config(self) -> None:
        config = {
            "active_roots": ["[기획서]", "skills"],
            "ignored_segments": ["[백업]", "[보류]", "[제거 후보]", "archive"],
            "required_paths": [
                "AGENTS.md",
                "[기획서]/00_프로젝트_허브/START_HERE.md",
                "[기획서]/00_프로젝트_허브/ACTIVE_CONTEXT.md",
                "[기획서]/00_프로젝트_허브/DOCUMENTATION_MAP.md",
                "[기획서]/00_프로젝트_허브/DOCUMENT_UPDATE_MATRIX.md",
                "[기획서]/00_프로젝트_허브/DEVELOPMENT_GATES.md",
                "[기획서]/00_프로젝트_허브/PROJECT_SKILL_MAP.md",
                "[기획서]/00_프로젝트_허브/AI_WORKFLOW.md",
                "[기획서]/00_프로젝트_허브/PUBLICATION_MANIFEST.json",
                "skills/foundation",
            ],
            "forbidden_active_name_patterns": [
                r"(?i)(^|[_-])(v[0-9]+|final|latest|copy|new)([_-]|\.)"
            ],
            "markdown_link_roots": ["[기획서]", "skills"],
            "asset_manifests": [],
            "publication_manifest": "[기획서]/00_프로젝트_허브/PUBLICATION_MANIFEST.json",
            "enforce_publications": True,
            "require_human_publication_visual_review": False,
            "change_rules": [],
        }
        self.config_path.write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _run_checker(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--config",
                str(self.config_path),
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_valid_project_and_current_publication_pass(self) -> None:
        result = self._run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Documentation governance passed.", result.stdout)
        self.assertIn("Checked 1 publication(s).", result.stdout)

    def test_changed_source_without_manifest_hash_fails(self) -> None:
        self.source.write_text("# 게임 기획서\n\n변경된 책임 원본.\n", encoding="utf-8")
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("publication inputs changed", result.stdout)

    def test_forbidden_active_filename_fails(self) -> None:
        forbidden = self.root / "[기획서]/02_게임_디자인/game_final.md"
        forbidden.write_text("# 잘못된 활성 복제본\n", encoding="utf-8")
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Forbidden active filename", result.stdout)

    def test_forbidden_filename_inside_backup_is_ignored(self) -> None:
        backup = self.root / "[기획서]/[백업]/game_final.md"
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_text("# 외부 원본 보존 자료\n", encoding="utf-8")
        result = self._run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_pdf_header_and_automated_render_review_are_required(self) -> None:
        self.pdf.write_text("not a pdf", encoding="utf-8")
        data = json.loads(self.publication_manifest.read_text(encoding="utf-8"))
        data["publications"][0]["automated_render_review"] = "FAILED"
        self.publication_manifest.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a valid PDF header", result.stdout)
        self.assertIn("automated_render_review=PASSED", result.stdout)

    def test_human_review_is_required_only_when_the_gate_enables_it(self) -> None:
        config = json.loads(self.config_path.read_text(encoding="utf-8"))
        config["require_human_publication_visual_review"] = True
        self.config_path.write_text(
            json.dumps(config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("human_visual_review=PASSED", result.stdout)


if __name__ == "__main__":
    unittest.main()
