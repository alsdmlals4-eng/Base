from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GithubConnectorFallbackPolicyTests(unittest.TestCase):
    def test_sync_skill_routes_missing_optional_cli_to_connector(self) -> None:
        skill = (
            ROOT / "skills/synchronizing-local-and-github-state/SKILL.md"
        ).read_text(encoding="utf-8")

        for token in (
            "GITHUB_CAPABILITY_FALLBACK",
            "github_connector",
            "local_git",
            "gh_cli",
            "MISSING_OPTIONAL_CLI",
            "BLOCKED_UNVERIFIED",
            "create_blob",
            "create_tree",
            "create_commit",
            "update_ref(force=false)",
            "반복 설치·재인증을 요청하지 않는다",
        ):
            self.assertIn(token, skill)

        self.assertIn("`gh` 부재만으로 전체 작업을 중단하지 않는다", skill)
        self.assertIn(
            "GitHub CLI or local push authentication is unavailable", skill
        )
        self.assertIn("expected_head_sha", skill)
        self.assertIn("CONCURRENT_CHANGE_PREFLIGHT", skill)

    def test_base_entrypoint_and_registry_make_fallback_discoverable(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        registry = json.loads(
            (ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8")
        )
        entry = next(
            item
            for item in registry["skills"]
            if item["skill_id"] == "synchronizing-local-and-github-state"
        )

        self.assertIn("GitHub plugin/connector", agents)
        self.assertIn("missing `gh` alone is not a blocker", agents)
        for trigger in (
            "github-cli-missing",
            "gh-auth-missing",
            "github-connector-fallback",
        ):
            self.assertIn(trigger, entry["trigger_tags"])
        for review_trigger in (
            "optional gh absence treated as global blocker",
            "repeated user re-authentication despite connector coverage",
        ):
            self.assertIn(review_trigger, entry["review_triggers"])
        self.assertTrue(
            any("connector" in value and "gh" in value for value in entry["use_when"])
        )

    def test_learning_log_records_observed_failure_and_security_boundary(self) -> None:
        learning = (
            ROOT / "skills/synchronizing-local-and-github-state/LEARNING_LOG.md"
        ).read_text(encoding="utf-8")

        for token in (
            "2026-08-14",
            "gh: command not found",
            "OBSERVED_FAILURE",
            "GitHub connector",
            "Windows token",
            "GH_TOKEN",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, learning)


if __name__ == "__main__":
    unittest.main()
