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
                "name": "local-skill-sync",
                "when_changed": ["skills/**/SKILL.md"],
                "exclude_when_changed": [
                    "skills/shared-skill/SKILL.md",
                    "skills/provider-evaluation/SKILL.md",
                ],
                "ignore_frontmatter_only_keys": ["description"],
                "require_all_changed": ["skills/SKILL_LEARNING_LOG.md"],
                "require_any_changed": ["tests/test_local_skill.py"],
            }, {
                "name": "skill-identity-registry-sync",
                "when_changed": ["skills/**/SKILL.md"],
                "exclude_when_changed": [],
                "when_frontmatter_keys_changed": ["name"],
                "require_all_changed": ["skills/SKILL_REGISTRY.json"],
                "require_any_changed": ["tests/test_local_skill.py"],
            }, {
                "name": "skill-description-learning-test-sync",
                "when_changed": ["skills/**/SKILL.md"],
                "exclude_when_changed": [],
                "when_frontmatter_keys_changed": ["description"],
                "require_all_changed": ["skills/SKILL_LEARNING_LOG.md"],
                "require_any_changed": ["tests/test_local_skill.py"],
            }, {
                "name": "shared-skill-sync",
                "when_changed": ["skills/shared-skill/SKILL.md"],
                "exclude_when_changed": [],
                "ignore_frontmatter_only_keys": ["description"],
                "require_all_changed": [
                    "skills/BASE_SHARED_SKILL_ROUTES.json",
                    "skills/shared-skill/LEARNING_LOG.md",
                ],
                "require_any_changed": ["tests/test_shared_skill.py"],
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

    def _init_git(self) -> str:
        self._git("init")
        self._git("config", "user.email", "test@example.com")
        self._git("config", "user.name", "Test User")
        self._git("add", ".")
        self._git("commit", "-m", "baseline")
        return self._git("rev-parse", "HEAD")

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

    def test_local_skill_body_change_requires_learning_log_and_test(self) -> None:
        skill = self.root / "skills/new-skill/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("# Skill\n", encoding="utf-8")
        (self.root / "skills/SKILL_REGISTRY.json").write_text("{}\n", encoding="utf-8")
        (self.root / "skills/SKILL_LEARNING_LOG.md").write_text("# Log\n", encoding="utf-8")
        (self.root / "tests/test_local_skill.py").write_text("# test\n", encoding="utf-8")
        base = self._init_git()
        skill.write_text("# Changed Skill\n", encoding="utf-8")
        self._git("add", "skills/new-skill/SKILL.md")
        self._git("commit", "-m", "change local skill only")
        result = self._run(base, self._git("rev-parse", "HEAD"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires changed companions", result.stdout)
        self.assertIn("requires at least one changed companion", result.stdout)

    def test_skill_name_change_requires_registry_even_when_learning_and_test_change(self) -> None:
        skill = self.root / "skills/new-skill/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(
            "---\nname: old-name\ndescription: Use when needed.\n---\n# Skill\n",
            encoding="utf-8",
        )
        registry = self.root / "skills/SKILL_REGISTRY.json"
        learning = self.root / "skills/SKILL_LEARNING_LOG.md"
        test = self.root / "tests/test_local_skill.py"
        registry.write_text("{}\n", encoding="utf-8")
        learning.write_text("# Log\n", encoding="utf-8")
        test.write_text("# test\n", encoding="utf-8")
        base = self._init_git()
        skill.write_text(
            "---\nname: new-name\ndescription: Use when needed.\n---\n# Skill\n",
            encoding="utf-8",
        )
        learning.write_text("# Updated Log\n", encoding="utf-8")
        test.write_text("# updated test\n", encoding="utf-8")
        self._git("add", "skills/new-skill/SKILL.md", "skills/SKILL_LEARNING_LOG.md", "tests/test_local_skill.py")
        self._git("commit", "-m", "rename skill without registry")
        result = self._run(base, self._git("rev-parse", "HEAD"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skill-identity-registry-sync", result.stdout)
        self.assertIn("skills/SKILL_REGISTRY.json", result.stdout)

    def test_description_only_change_requires_learning_and_test_but_not_registry(self) -> None:
        skill = self.root / "skills/new-skill/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(
            "---\nname: new-skill\ndescription: Use when the old wording applies.\n---\n# Skill\n",
            encoding="utf-8",
        )
        registry = self.root / "skills/SKILL_REGISTRY.json"
        learning = self.root / "skills/SKILL_LEARNING_LOG.md"
        test = self.root / "tests/test_local_skill.py"
        registry.write_text("{}\n", encoding="utf-8")
        learning.write_text("# Log\n", encoding="utf-8")
        test.write_text("# test\n", encoding="utf-8")
        base = self._init_git()
        skill.write_text(
            "---\nname: new-skill\ndescription: Use when the shorter wording applies.\n---\n# Skill\n",
            encoding="utf-8",
        )
        learning.write_text("# Updated Log\n", encoding="utf-8")
        test.write_text("# updated test\n", encoding="utf-8")
        self._git("add", "skills/new-skill/SKILL.md", "skills/SKILL_LEARNING_LOG.md", "tests/test_local_skill.py")
        self._git("commit", "-m", "shorten discovery description")
        result = self._run(base, self._git("rev-parse", "HEAD"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_description_only_change_without_learning_and_test_fails(self) -> None:
        skill = self.root / "skills/new-skill/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text(
            "---\nname: new-skill\ndescription: Use when the old wording applies.\n---\n# Skill\n",
            encoding="utf-8",
        )
        (self.root / "skills/SKILL_REGISTRY.json").write_text("{}\n", encoding="utf-8")
        (self.root / "skills/SKILL_LEARNING_LOG.md").write_text("# Log\n", encoding="utf-8")
        (self.root / "tests/test_local_skill.py").write_text("# test\n", encoding="utf-8")
        base = self._init_git()
        skill.write_text(
            "---\nname: new-skill\ndescription: Use when materially different routing applies.\n---\n# Skill\n",
            encoding="utf-8",
        )
        self._git("add", "skills/new-skill/SKILL.md")
        self._git("commit", "-m", "change discovery authority without evidence")
        result = self._run(base, self._git("rev-parse", "HEAD"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skill-description-learning-test-sync", result.stdout)
        self.assertIn("skills/SKILL_LEARNING_LOG.md", result.stdout)

    def test_shared_skill_change_uses_route_and_package_log_not_local_registry(self) -> None:
        skill = self.root / "skills/shared-skill/SKILL.md"
        log = self.root / "skills/shared-skill/LEARNING_LOG.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("# Shared Skill\n", encoding="utf-8")
        log.write_text("# Log\n", encoding="utf-8")
        (self.root / "skills/BASE_SHARED_SKILL_ROUTES.json").write_text("{}\n", encoding="utf-8")
        (self.root / "tests/test_shared_skill.py").write_text("# test\n", encoding="utf-8")
        base = self._init_git()
        skill.write_text("# Changed Shared Skill\n", encoding="utf-8")
        log.write_text("# Updated Log\n", encoding="utf-8")
        (self.root / "skills/BASE_SHARED_SKILL_ROUTES.json").write_text('{"changed": true}\n', encoding="utf-8")
        (self.root / "tests/test_shared_skill.py").write_text("# updated test\n", encoding="utf-8")
        self._git("add", ".")
        self._git("commit", "-m", "change shared skill companions")
        result = self._run(base, self._git("rev-parse", "HEAD"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_shared_skill_change_without_package_log_fails(self) -> None:
        skill = self.root / "skills/shared-skill/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("# Shared Skill\n", encoding="utf-8")
        (self.root / "skills/shared-skill/LEARNING_LOG.md").write_text("# Log\n", encoding="utf-8")
        (self.root / "skills/BASE_SHARED_SKILL_ROUTES.json").write_text("{}\n", encoding="utf-8")
        (self.root / "tests/test_shared_skill.py").write_text("# test\n", encoding="utf-8")
        base = self._init_git()
        skill.write_text("# Changed Shared Skill\n", encoding="utf-8")
        (self.root / "skills/BASE_SHARED_SKILL_ROUTES.json").write_text('{"changed": true}\n', encoding="utf-8")
        (self.root / "tests/test_shared_skill.py").write_text("# updated test\n", encoding="utf-8")
        self._git("add", ".")
        self._git("commit", "-m", "omit shared log")
        result = self._run(base, self._git("rev-parse", "HEAD"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("skills/shared-skill/LEARNING_LOG.md", result.stdout)

    def test_provider_evaluation_change_requires_route_log_and_test(self) -> None:
        self.config["coupled_change_rules"].append({
            "name": "provider-evaluation-sync",
            "when_changed": ["skills/provider-evaluation/SKILL.md"],
            "exclude_when_changed": [],
            "require_all_changed": [
                "skills/BASE_SHARED_SKILL_ROUTES.json",
                "skills/provider-evaluation/LEARNING_LOG.md",
            ],
            "require_any_changed": ["tests/test_provider_evaluation.py"],
        })
        provider = self.root / "skills/provider-evaluation"
        provider.mkdir(parents=True)
        skill = provider / "SKILL.md"
        log = provider / "LEARNING_LOG.md"
        routes = self.root / "skills/BASE_SHARED_SKILL_ROUTES.json"
        test = self.root / "tests/test_provider_evaluation.py"
        skill.write_text("# Provider evaluation\n", encoding="utf-8")
        log.write_text("# Learning\n", encoding="utf-8")
        routes.write_text("{}\n", encoding="utf-8")
        test.write_text("# contract test\n", encoding="utf-8")
        self._write_config()
        base = self._init_git()

        skill.write_text("# Provider evaluation with inventory\n", encoding="utf-8")
        self._git("add", "skills/provider-evaluation/SKILL.md")
        self._git("commit", "-m", "change provider owner without companions")
        failed = self._run(base, self._git("rev-parse", "HEAD"))
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("provider-evaluation-sync", failed.stdout)

        log.write_text("# Learning\n\nInventory before build.\n", encoding="utf-8")
        routes.write_text('{"provider": "updated"}\n', encoding="utf-8")
        test.write_text("# provider inventory contract\n", encoding="utf-8")
        self._git(
            "add",
            "skills/provider-evaluation/LEARNING_LOG.md",
            "skills/BASE_SHARED_SKILL_ROUTES.json",
            "tests/test_provider_evaluation.py",
        )
        self._git("commit", "-m", "add provider evaluation companions")
        passed = self._run(base, self._git("rev-parse", "HEAD"))
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)

    def test_completion_correction_gate_has_a_recognized_freshness_companion(self) -> None:
        live_config = json.loads((ROOT / ".github/reference-freshness.json").read_text(encoding="utf-8"))
        rule = next(
            item
            for item in live_config["coupled_change_rules"]
            if item["name"] == "local-skill-contract-learning-test-sync"
        )
        self.assertIn("tests/test_reference_freshness.py", rule["require_any_changed"])

        focused = (ROOT / "tests/test_completion_correction_adversarial_gate.py").read_text(
            encoding="utf-8"
        )
        for marker in (
            "REMAINING_WORK_COMPLETION_GATE",
            "IMPLEMENTATION_CORRECTION_RESCAN",
            "NEW_FINDING_REOPENS_REMAINING_WORK",
            "POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED",
            "CLEAN_REVIEW_EXIT",
        ):
            self.assertIn(marker, focused)

    def test_reuse_first_preflight_has_a_recognized_freshness_companion(self) -> None:
        live_config = json.loads((ROOT / ".github/reference-freshness.json").read_text(encoding="utf-8"))
        rule = next(
            item
            for item in live_config["coupled_change_rules"]
            if item["name"] == "local-skill-contract-learning-test-sync"
        )
        self.assertIn("tests/test_reference_freshness.py", rule["require_any_changed"])

        focused = (ROOT / "tests/test_reuse_first_preflight_enforcement.py").read_text(
            encoding="utf-8"
        )
        for marker in (
            "REUSE_FIRST_PREFLIGHT_REQUIRED",
            "REUSE_LEARNING_HANDOFF_REQUIRED",
            "BASE_ACCUMULATED_KNOWLEDGE_CASE_REFERENCE",
            "TARGETED_CROSS_PROJECT_VERIFIED_EVIDENCE",
            "NO_NEW_REUSE_LEARNING",
        ):
            self.assertIn(marker, focused)

    def test_repository_freshness_skill_declares_verified_successor_state_contract(self) -> None:
        skill = (ROOT / "skills/auditing-canonical-reference-freshness/SKILL.md").read_text(
            encoding="utf-8"
        )
        for marker in (
            "VERIFIED_SUCCESSOR_STATE",
            "PREDECESSOR_CEILING_FREEZE",
            "CURRENT_MUTABLE",
            "HISTORICAL_DISCOVERY",
            "NOT_RUN",
        ):
            self.assertIn(marker, skill)
        self.assertIn("historical provenance", skill)
        self.assertIn("MISSING_PROPAGATION", skill)
        self.assertIn("CONFLICTING_SOURCE", skill)


if __name__ == "__main__":
    unittest.main()
