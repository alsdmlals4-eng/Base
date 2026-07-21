from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_canonical_reference_freshness.py"


class CanonicalReferenceFreshnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / ".github").mkdir()
        (self.root / "skills").mkdir()
        (self.root / "docs").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "skills/LEGACY_SKILL_ALIASES.md").write_text(
            "# Legacy Skill Aliases\n\n"
            "| 이전 Skill ID | 새 Skill ID | Mode |\n"
            "|---|---|---|\n"
            "| `old-skill` | `new-skill` | `run` |\n",
            encoding="utf-8",
        )
        (self.root / "docs/OPERATING_MODEL.md").write_text("# Canonical\n", encoding="utf-8")
        (self.root / "README.md").write_text("See docs/OPERATING_MODEL.md\n", encoding="utf-8")
        self.config = {
            "schema_version": 1,
            "scan_globs": ["*.md", "docs/**/*.md", "skills/**/*.md", "tests/**/*.py"],
            "ignore_globs": [],
            "legacy_aliases_path": "skills/LEGACY_SKILL_ALIASES.md",
            "allowed_legacy_globs": ["skills/LEGACY_SKILL_ALIASES.md", "docs/CHANGELOG.md"],
            "strict_legacy_id_globs": ["README.md"],
            "forbidden_tokens": [],
            "canonical_reference_rules": [{
                "name": "operating-model-entrypoint",
                "canonical_path": "docs/OPERATING_MODEL.md",
                "reference_tokens": ["docs/OPERATING_MODEL.md"],
                "required_consumers": ["README.md"],
            }],
            "coupled_change_rules": [{
                "name": "skill-contract-sync",
                "when_changed": ["skills/**/SKILL.md"],
                "require_all_changed": ["skills/SKILL_REGISTRY.json"],
                "require_any_changed": ["skills/SKILL_LEARNING_LOG.md"],
            }],
        }
        self._write_config()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def _write_config(self) -> None:
        (self.root / ".github/reference-freshness.json").write_text(
            json.dumps(self.config, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _run(self, base: str = "", head: str = "HEAD") -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(CHECKER),
            "--root",
            str(self.root),
            "--config",
            ".github/reference-freshness.json",
        ]
        if base:
            command += ["--base", base, "--head", head]
        return subprocess.run(
            command,
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
        return result.stdout.strip()

    def test_valid_references_pass(self) -> None:
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_legacy_id_in_execution_entrypoint_fails(self) -> None:
        (self.root / "README.md").write_text(
            "See docs/OPERATING_MODEL.md and old-skill\n",
            encoding="utf-8",
        )
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Legacy skill id remains in execution entrypoint", result.stdout)

    def test_bare_legacy_id_in_non_entrypoint_is_not_a_path_failure(self) -> None:
        (self.root / "docs/NOTE.md").write_text(
            "Historical discussion of old-skill.\n",
            encoding="utf-8",
        )
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_deleted_skill_path_fails_outside_strict_entrypoints(self) -> None:
        (self.root / "docs/NOTE.md").write_text(
            "Do not use skills/old-skill/SKILL.md.\n",
            encoding="utf-8",
        )
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Deleted skill path remains in active file", result.stdout)

    def test_missing_canonical_reference_fails(self) -> None:
        (self.root / "README.md").write_text("No current source\n", encoding="utf-8")
        result = self._run()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not reference current canonical source", result.stdout)

    def test_coupled_change_requires_registry_and_learning_log(self) -> None:
        skill = self.root / "skills/new-skill/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("# Skill\n", encoding="utf-8")
        (self.root / "skills/SKILL_REGISTRY.json").write_text("{}\n", encoding="utf-8")
        (self.root / "skills/SKILL_LEARNING_LOG.md").write_text("# Log\n", encoding="utf-8")
        self._git("init")
        self._git("config", "user.email", "test@example.com")
        self._git("config", "user.name", "Test User")
        self._git("add", ".")
        self._git("commit", "-m", "baseline")
        base = self._git("rev-parse", "HEAD")
        skill.write_text("# Changed Skill\n", encoding="utf-8")
        self._git("add", "skills/new-skill/SKILL.md")
        self._git("commit", "-m", "change skill only")
        head = self._git("rev-parse", "HEAD")
        result = self._run(base, head)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires changed companions", result.stdout)
        self.assertIn("requires at least one changed companion", result.stdout)


if __name__ == "__main__":
    unittest.main()
