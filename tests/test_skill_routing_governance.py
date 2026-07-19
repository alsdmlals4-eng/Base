from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPOSITORY_ROOT / "templates/project-operations/github/check_skill_routing_governance.py"


class SkillRoutingGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.config_path = self.root / "governance.json"
        self.hub = self.root / "[기획서]/00_프로젝트_허브"
        self.registry_path = self.hub / "SKILL_REGISTRY.json"
        self.markdown = self.hub / "PROJECT_SKILL_MAP.md"
        self.pdf = self.hub / "PROJECT_SKILL_MAP.pdf"
        self.assets = self.hub / "PROJECT_SKILL_MAP.assets"
        self.manifest = self.hub / "SKILL_MAP_PUBLICATION_MANIFEST.json"
        self.skill_path = self.root / "skills/foundation/test-skill/SKILL.md"
        self.learning_log = self.root / "skills/foundation/test-skill/LEARNING_LOG.md"
        self.hub.mkdir(parents=True)
        self.assets.mkdir(parents=True)
        self.skill_path.parent.mkdir(parents=True)
        self.skill_path.write_text("# Test Skill\n", encoding="utf-8")
        self.learning_log.write_text("# Learning Log\n", encoding="utf-8")
        self._write_registry()
        self._write_publication()
        self._write_config()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    @staticmethod
    def _digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _registry_data(self) -> dict:
        return {
            "schema_version": 3,
            "registry_role": "project-skill-router-and-learning-index",
            "routing_policy": {
                "load_all_skills": False,
                "default_selection": "none",
                "require_trigger_match": True,
                "max_primary_discipline_skills": 1,
                "max_foundation_skills": 3,
            },
            "human_presentation": {
                "primary_reading_format": "PROJECT_SKILL_MAP.pdf",
                "editable_derivative": None,
                "diagram_directory": "PROJECT_SKILL_MAP.assets",
                "publication_manifest": "SKILL_MAP_PUBLICATION_MANIFEST.json",
                "generator": "tools/build_project_skill_map.py",
                "source_of_truth": "SKILL_REGISTRY.json",
                "markdown_summary": "PROJECT_SKILL_MAP.md",
            },
            "skills": [{
                "skill_id": "test-skill",
                "layer": "foundation",
                "discipline": "project-operations",
                "path": "skills/foundation/test-skill/SKILL.md",
                "status": "ACTIVE",
                "load_by_default": False,
                "trigger_tags": ["test-trigger"],
                "use_when": ["테스트 작업에서 사용한다."],
                "do_not_use_when": ["테스트 범위가 아닐 때 사용하지 않는다."],
                "learning_log": "skills/foundation/test-skill/LEARNING_LOG.md",
                "review_triggers": ["테스트 실패"],
                "last_reviewed_at": "2026-07-19",
                "last_reviewed_commit": "test-commit",
                "knowledge_state": "OBSERVATION",
            }],
            "selected_disciplines": ["사운드"],
            "discipline_entrypoints": {"사운드": ["test-skill"]},
        }

    def _write_registry(self, data: dict | None = None) -> None:
        self.registry_path.write_text(
            json.dumps(data or self._registry_data(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _write_publication(self) -> None:
        self.pdf.write_bytes(b"%PDF-1.4\npdf")
        image = self.assets / "skill-flow.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nflow")
        registry_hash = self._digest(self.registry_path)
        self.markdown.write_text(
            "<!-- 자동 생성 파생본: 수동 편집 금지 -->\n"
            f"<!-- source_sha256: {registry_hash} -->\n# 프로젝트 스킬 맵\n",
            encoding="utf-8",
        )
        zero = "0" * 64
        self.manifest.write_text(json.dumps({
            "schema_version": 3,
            "publication_id": "project-skill-map",
            "role": "human-readable-derivative",
            "source_path": "SKILL_REGISTRY.json",
            "source_format": "skill-registry",
            "source_sha256": registry_hash,
            "input_sha256": zero,
            "generator": "tools/build_project_skill_map.py",
            "generator_sha256": zero,
            "source_commit": "test",
            "output_pdf": "PROJECT_SKILL_MAP.pdf",
            "output_pdf_sha256": self._digest(self.pdf),
            "output_docx": None,
            "output_docx_sha256": None,
            "markdown_summary": "PROJECT_SKILL_MAP.md",
            "markdown_summary_sha256": self._digest(self.markdown),
            "generated_assets": {
                "PROJECT_SKILL_MAP.assets/skill-flow.png": self._digest(image),
            },
            "sync_status": "CURRENT",
            "automated_render_review": "PASSED",
            "human_visual_review": "NOT_RUN",
            "human_visual_review_pdf_sha256": None,
            "rendered_page_count": 1,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _write_config(self) -> None:
        self.config_path.write_text(json.dumps({
            "design_root": "[기획서]",
            "enforce_top_level_design_root": True,
            "skill_registry": "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json",
            "enforce_skill_registry": True,
            "skill_map_publication_manifest": "[기획서]/00_프로젝트_허브/SKILL_MAP_PUBLICATION_MANIFEST.json",
            "enforce_skill_map_publication": True,
            "require_human_skill_map_visual_review": False,
            "required_skill_disciplines": [],
            "skill_change_globs": ["skills/**/SKILL.md"],
            "skill_map_generator_globs": ["tools/build_project_skill_map.py"],
            "skill_map_sync_paths": [
                "[기획서]/00_프로젝트_허브/PROJECT_SKILL_MAP.md",
                "[기획서]/00_프로젝트_허브/PROJECT_SKILL_MAP.pdf",
                "[기획서]/00_프로젝트_허브/PROJECT_SKILL_MAP.assets/skill-flow.png",
                "[기획서]/00_프로젝트_허브/SKILL_MAP_PUBLICATION_MANIFEST.json",
            ],
            "learning_log_globs": ["skills/**/LEARNING_LOG.md"],
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _run_checker(self, base: str = "", head: str = "HEAD") -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(CHECKER), "--config", str(self.config_path)]
        if base:
            command += ["--base", base, "--head", head]
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            command, cwd=self.root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", env=env,
        )

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args], cwd=self.root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", check=True,
        )
        return result.stdout.strip()

    def test_valid_root_registry_and_publication_pass(self) -> None:
        result = self._run_checker()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_nested_duplicate_design_root_fails(self) -> None:
        (self.root / "docs/[기획서]").mkdir(parents=True)
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Nested duplicate design root", result.stdout)

    def test_load_all_skills_policy_fails(self) -> None:
        data = self._registry_data()
        data["routing_policy"]["load_all_skills"] = True
        self._write_registry(data)
        self._write_publication()
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("load_all_skills must be false", result.stdout)

    def test_only_selected_discipline_requires_entrypoint(self) -> None:
        data = self._registry_data()
        data["discipline_entrypoints"]["사운드"] = []
        self._write_registry(data)
        self._write_publication()
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing active skill entrypoint for discipline: 사운드", result.stdout)
        self.assertNotIn("게임 디자인", result.stdout)

    def test_missing_learning_log_fails(self) -> None:
        self.learning_log.unlink()
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("learning_log missing", result.stdout)

    def test_stale_skill_map_fails(self) -> None:
        data = self._registry_data()
        data["skills"][0]["use_when"] = ["변경된 조건"]
        self._write_registry(data)
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("registry input changed", result.stdout)

    def test_generated_markdown_modification_fails(self) -> None:
        self.markdown.write_text("# 수동으로 바꿈\n", encoding="utf-8")
        result = self._run_checker()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Markdown summary", result.stdout)

    def test_skill_change_requires_registry_publications_and_learning_log_sync(self) -> None:
        self._git("init")
        self._git("config", "user.email", "test@example.com")
        self._git("config", "user.name", "Test User")
        self._git("add", ".")
        self._git("commit", "-m", "baseline")
        base = self._git("rev-parse", "HEAD")
        self.skill_path.write_text("# Changed Test Skill\n", encoding="utf-8")
        self._git("add", str(self.skill_path.relative_to(self.root)))
        self._git("commit", "-m", "change skill only")
        head = self._git("rev-parse", "HEAD")
        result = self._run_checker(base, head)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("update registry", result.stdout)
        self.assertIn("regenerate and update", result.stdout)
        self.assertIn("update at least one Learning Log", result.stdout)


if __name__ == "__main__":
    unittest.main()
