from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.loop_a2_runtime.evidence import canonical_receipt
from tools.loop_a2_runtime.integration import (
    A2Integration,
    IntegrationError,
    PostmergeEvidence,
    PullRequestSnapshot,
)


def git(repo: Path, *args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=check,
    )
    return completed.stdout.strip()


class FakePRProvider:
    def __init__(self, *, available: bool = True) -> None:
        self.available = available
        self.opened: list[dict[str, object]] = []

    def preflight(self) -> None:
        if not self.available:
            raise IntegrationError("PR_PROVIDER_UNAVAILABLE", "provider unavailable")

    def open_pull_request(
        self,
        *,
        branch_name: str,
        head_sha: str,
        title: str,
        body: str,
    ) -> PullRequestSnapshot:
        self.opened.append(
            {
                "branch_name": branch_name,
                "head_sha": head_sha,
                "title": title,
                "body": body,
            }
        )
        return PullRequestSnapshot(
            number=77,
            state="open",
            merged=False,
            head_sha=head_sha,
            merge_sha=None,
            required_checks="PENDING",
            unresolved_threads=0,
            current_main_sha=None,
            merge_in_main=False,
        )


class LoopA2IntegrationTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.remote = self.root / "remote.git"
        self.repo.mkdir()
        git(self.repo, "init", "-b", "main")
        git(self.repo, "config", "user.name", "Loop Integration Test")
        git(self.repo, "config", "user.email", "loop@example.invalid")
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts/example.gd").write_text("base\n", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "base")
        self.base_sha = git(self.repo, "rev-parse", "HEAD")
        subprocess.run(
            ["git", "init", "--bare", str(self.remote)],
            text=True,
            capture_output=True,
            check=True,
        )
        git(self.repo, "remote", "add", "origin", str(self.remote))
        git(self.repo, "push", "-u", "origin", "main")
        (self.repo / "scripts/example.gd").write_text("approved change\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def receipt(self, **overrides: object) -> dict[str, object]:
        payload: dict[str, object] = {
            "schema_version": 1,
            "contract_role": "LOOP_A2_RUN_RECEIPT",
            "project_id": "EXAMPLE_GAME",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "expected_main_sha": self.base_sha,
            "state": "WAITING_INTEGRATION",
            "finding_codes": [],
            "changed_paths": ["scripts/example.gd"],
            "provider_mode": "FAKE",
            "integration_eligible": False,
            "a3_auto_merge": "DISABLED",
            "scheduler": "NOT_CONFIGURED",
            "critic_verdict": "PASS",
            "checked_requirement_ids": ["REQ_001"],
        }
        payload.update(overrides)
        return canonical_receipt(payload)

    def integration(self, provider: FakePRProvider | None = None) -> A2Integration:
        return A2Integration(
            repo_root=self.repo,
            provider=provider or FakePRProvider(),
        )

    def test_handoff_commits_reviewed_diff_and_pushes_only_generated_branch(self) -> None:
        provider = FakePRProvider()
        result = self.integration(provider).handoff(
            receipt=self.receipt(),
            expected_project_id="EXAMPLE_GAME",
            expected_run_id="RUN_001",
            expected_package_id="PACKAGE_001",
        )

        self.assertEqual(result.pr.number, 77)
        self.assertEqual(result.branch_name, "loop-a2/example_game/run_001")
        self.assertRegex(result.reviewed_head_sha, r"^[0-9a-f]{40}$")
        self.assertEqual(provider.opened[0]["head_sha"], result.reviewed_head_sha)
        self.assertEqual(git(self.repo, "rev-parse", "main"), self.base_sha)
        remote_heads = git(self.repo, "ls-remote", "--heads", "origin")
        self.assertIn("refs/heads/loop-a2/example_game/run_001", remote_heads)
        self.assertIn("refs/heads/main", remote_heads)
        self.assertEqual(git(self.repo, "status", "--porcelain"), "")

    def test_handoff_requires_clean_waiting_integration_receipt_and_identity(self) -> None:
        cases = (
            self.receipt(state="BLOCKED_UNVERIFIED"),
            self.receipt(finding_codes=["X"]),
            self.receipt(critic_verdict="MUST_FIX"),
            self.receipt(project_id="OTHER_GAME"),
        )
        for receipt in cases:
            with self.subTest(receipt=receipt):
                with self.assertRaises(IntegrationError):
                    self.integration().handoff(
                        receipt=receipt,
                        expected_project_id="EXAMPLE_GAME",
                        expected_run_id="RUN_001",
                        expected_package_id="PACKAGE_001",
                    )

    def test_handoff_rejects_tampered_receipt_or_changed_worktree_after_review(self) -> None:
        tampered = self.receipt()
        tampered["changed_paths"] = ["scripts/other.gd"]
        with self.assertRaises(IntegrationError) as raised:
            self.integration().handoff(
                receipt=tampered,
                expected_project_id="EXAMPLE_GAME",
                expected_run_id="RUN_001",
                expected_package_id="PACKAGE_001",
            )
        self.assertIn("RECEIPT_DIGEST", str(raised.exception))

        clean = self.receipt()
        (self.repo / "scripts/extra.gd").write_text("not reviewed\n", encoding="utf-8")
        with self.assertRaises(IntegrationError) as raised:
            self.integration().handoff(
                receipt=clean,
                expected_project_id="EXAMPLE_GAME",
                expected_run_id="RUN_001",
                expected_package_id="PACKAGE_001",
            )
        self.assertIn("CHANGED_PATHS", str(raised.exception))

    def test_handoff_fails_before_git_mutation_when_pr_provider_unavailable(self) -> None:
        provider = FakePRProvider(available=False)
        with self.assertRaises(IntegrationError) as raised:
            self.integration(provider).handoff(
                receipt=self.receipt(),
                expected_project_id="EXAMPLE_GAME",
                expected_run_id="RUN_001",
                expected_package_id="PACKAGE_001",
            )
        self.assertIn("PR_PROVIDER_UNAVAILABLE", str(raised.exception))
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), self.base_sha)
        self.assertNotEqual(git(self.repo, "status", "--porcelain"), "")

    def test_handoff_rejects_path_like_identifiers_before_branch_generation(self) -> None:
        unsafe = self.receipt(run_id="../RUN")
        with self.assertRaises(IntegrationError) as raised:
            self.integration().handoff(
                receipt=unsafe,
                expected_project_id="EXAMPLE_GAME",
                expected_run_id="../RUN",
                expected_package_id="PACKAGE_001",
            )
        self.assertIn("IDENTIFIER", str(raised.exception))

    def test_postmerge_closure_requires_direct_merged_evidence(self) -> None:
        handoff = self.integration().handoff(
            receipt=self.receipt(),
            expected_project_id="EXAMPLE_GAME",
            expected_run_id="RUN_001",
            expected_package_id="PACKAGE_001",
        )
        evidence = PostmergeEvidence(
            pr_number=handoff.pr.number,
            merged=True,
            pr_head_sha=handoff.reviewed_head_sha,
            merge_sha="b" * 40,
            required_checks="PASS",
            unresolved_threads=0,
            current_main_sha="c" * 40,
            merge_in_main=True,
            project_id="EXAMPLE_GAME",
            run_id="RUN_001",
            package_id="PACKAGE_001",
            coverage_status="COMPLETE",
            planning_drift="NO_DRIFT",
            visual_drift="NOT_APPLICABLE",
        )
        receipt_path = self.root / "closed.json"

        closed = self.integration().close_postmerge(
            run_receipt=self.receipt(),
            handoff=handoff,
            evidence=evidence,
            receipt_path=receipt_path,
        )

        self.assertEqual(closed["state"], "CLOSED")
        self.assertEqual(closed["merge_sha"], "b" * 40)
        self.assertRegex(closed["receipt_digest"], r"^[0-9a-f]{64}$")
        self.assertEqual(json.loads(receipt_path.read_text(encoding="utf-8")), closed)
        with self.assertRaises(IntegrationError) as raised:
            self.integration().close_postmerge(
                run_receipt=self.receipt(),
                handoff=handoff,
                evidence=evidence,
                receipt_path=receipt_path,
            )
        self.assertIn("CLOSURE_EXISTS", str(raised.exception))

    def test_postmerge_closure_fails_closed_on_each_missing_gate(self) -> None:
        handoff = self.integration().handoff(
            receipt=self.receipt(),
            expected_project_id="EXAMPLE_GAME",
            expected_run_id="RUN_001",
            expected_package_id="PACKAGE_001",
        )
        base = {
            "pr_number": handoff.pr.number,
            "merged": True,
            "pr_head_sha": handoff.reviewed_head_sha,
            "merge_sha": "b" * 40,
            "required_checks": "PASS",
            "unresolved_threads": 0,
            "current_main_sha": "c" * 40,
            "merge_in_main": True,
            "project_id": "EXAMPLE_GAME",
            "run_id": "RUN_001",
            "package_id": "PACKAGE_001",
            "coverage_status": "COMPLETE",
            "planning_drift": "NO_DRIFT",
            "visual_drift": "NOT_APPLICABLE",
        }
        cases = (
            {"merged": False},
            {"pr_head_sha": "d" * 40},
            {"merge_sha": None},
            {"required_checks": "PENDING"},
            {"required_checks": "FAIL"},
            {"unresolved_threads": 1},
            {"merge_in_main": False},
            {"project_id": "OTHER_GAME"},
            {"coverage_status": "INCOMPLETE"},
            {"planning_drift": "PLANNING_CONFLICT"},
            {"visual_drift": "VISUAL_CONFLICT"},
        )
        for index, mutation in enumerate(cases):
            with self.subTest(mutation=mutation):
                value = dict(base)
                value.update(mutation)
                with self.assertRaises(IntegrationError):
                    self.integration().close_postmerge(
                        run_receipt=self.receipt(),
                        handoff=handoff,
                        evidence=PostmergeEvidence(**value),
                        receipt_path=self.root / f"closed-{index}.json",
                    )


if __name__ == "__main__":
    unittest.main()
