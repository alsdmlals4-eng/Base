from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md"


class BaseSquashOnlyGovernanceEvidenceTests(unittest.TestCase):
    def test_profile_records_current_squash_only_repository_state(self) -> None:
        profile = PROFILE.read_text(encoding="utf-8")
        for token in (
            "last_verified_at: 2026-08-23",
            "repository_allow_squash_merge: true",
            "repository_allow_merge_commit: false",
            "repository_allow_rebase_merge: false",
            "repository_merge_methods_status: VERIFIED_SQUASH_ONLY",
            "id: 19688076",
            "name: solo-main-safety",
            "enforcement: active",
            "allowed_merge_methods:",
            "- squash",
            "required_check_context: ci-gate",
            "repository_merge_methods: VERIFIED_SQUASH_ONLY",
            "allow_merge_commit=false",
            "allow_rebase_merge=false",
        ):
            with self.subTest(token=token):
                self.assertIn(token, profile)

        self.assertNotIn(
            "repository-level settings currently also allow merge commits and rebase merges",
            profile,
        )
        self.assertNotIn(
            "repository-level merge/rebase settings remain enabled",
            profile,
        )


if __name__ == "__main__":
    unittest.main()
