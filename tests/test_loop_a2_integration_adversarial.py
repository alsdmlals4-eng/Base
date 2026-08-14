from __future__ import annotations

import ast
import os
import unittest
from pathlib import Path

from tests.test_loop_a2_integration import FakePRProvider, LoopA2IntegrationTests
from tools.loop_a2_runtime.evidence import canonical_receipt
from tools.loop_a2_runtime.integration import (
    A2Integration,
    GhPullRequestProvider,
    IntegrationError,
    compute_worktree_diff_sha256,
)


class TrustedFakePRProvider(FakePRProvider):
    requires_trusted_attestation = True


class LoopA2IntegrationAdversarialTests(LoopA2IntegrationTests):
    def eligible_receipt(self, **overrides: object) -> dict[str, object]:
        value = self.receipt(
            provider_mode="REAL",
            integration_eligible=True,
        )
        unsigned = dict(value)
        unsigned.pop("receipt_digest", None)
        unsigned.update(overrides)
        return canonical_receipt(unsigned)

    def test_operational_provider_rejects_fake_or_noneligible_receipt(self) -> None:
        provider = TrustedFakePRProvider()
        for receipt in (
            self.receipt(),
            self.eligible_receipt(integration_eligible=False),
            self.eligible_receipt(provider_mode="FAKE"),
        ):
            with self.subTest(receipt=receipt):
                with self.assertRaises(IntegrationError) as raised:
                    A2Integration(repo_root=self.repo, provider=provider).handoff(
                        receipt=receipt,
                        expected_project_id="EXAMPLE_GAME",
                        expected_run_id="RUN_001",
                        expected_package_id="PACKAGE_001",
                    )
                self.assertIn("INTEGRATION", str(raised.exception))

    def test_operational_handoff_requires_reviewed_content_attestation(self) -> None:
        provider = TrustedFakePRProvider()
        receipt = self.eligible_receipt()
        with self.assertRaises(IntegrationError) as raised:
            A2Integration(repo_root=self.repo, provider=provider).handoff(
                receipt=receipt,
                expected_project_id="EXAMPLE_GAME",
                expected_run_id="RUN_001",
                expected_package_id="PACKAGE_001",
            )
        self.assertIn("DIFF_ATTESTATION_REQUIRED", str(raised.exception))

    def test_same_path_content_drift_after_review_is_detected(self) -> None:
        provider = TrustedFakePRProvider()
        receipt = self.eligible_receipt()
        reviewed_digest = compute_worktree_diff_sha256(self.repo)
        (self.repo / "scripts/example.gd").write_text("changed after review\n", encoding="utf-8")

        with self.assertRaises(IntegrationError) as raised:
            A2Integration(repo_root=self.repo, provider=provider).handoff(
                receipt=receipt,
                expected_project_id="EXAMPLE_GAME",
                expected_run_id="RUN_001",
                expected_package_id="PACKAGE_001",
                reviewed_diff_sha256=reviewed_digest,
            )
        self.assertIn("DIFF_ATTESTATION_MISMATCH", str(raised.exception))

    def test_reviewed_content_attestation_allows_unchanged_operational_handoff(self) -> None:
        provider = TrustedFakePRProvider()
        receipt = self.eligible_receipt()
        reviewed_digest = compute_worktree_diff_sha256(self.repo)

        result = A2Integration(repo_root=self.repo, provider=provider).handoff(
            receipt=receipt,
            expected_project_id="EXAMPLE_GAME",
            expected_run_id="RUN_001",
            expected_package_id="PACKAGE_001",
            reviewed_diff_sha256=reviewed_digest,
        )
        self.assertEqual(result.reviewed_diff_sha256, reviewed_digest)

    def test_gh_provider_fails_closed_when_cli_is_unavailable(self) -> None:
        provider = GhPullRequestProvider(
            repo_root=self.repo,
            executable=self.root / "missing-gh",
        )
        with self.assertRaises(IntegrationError) as raised:
            provider.preflight()
        self.assertIn("GH_UNAVAILABLE", str(raised.exception))

    def test_integration_subprocesses_never_use_shell_or_force_push(self) -> None:
        import tools.loop_a2_runtime.integration as integration

        source = Path(integration.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        shell_true: list[int] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        shell_true.append(node.lineno)
        self.assertEqual(shell_true, [])
        self.assertNotIn('"--force"', source)
        self.assertNotIn("'--force'", source)

    def test_git_and_gh_subprocess_environment_excludes_parent_secrets(self) -> None:
        import tools.loop_a2_runtime.integration as integration

        previous_openai = os.environ.get("OPENAI_API_KEY")
        previous_github = os.environ.get("GITHUB_TOKEN")
        os.environ["OPENAI_API_KEY"] = "must-not-cross"
        os.environ["GITHUB_TOKEN"] = "must-not-cross"
        try:
            environment = integration._safe_environment()
            self.assertNotIn("OPENAI_API_KEY", environment)
            self.assertNotIn("GITHUB_TOKEN", environment)
        finally:
            if previous_openai is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous_openai
            if previous_github is None:
                os.environ.pop("GITHUB_TOKEN", None)
            else:
                os.environ["GITHUB_TOKEN"] = previous_github


if __name__ == "__main__":
    unittest.main()
