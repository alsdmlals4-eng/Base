from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import project_operating_contract as contract
from base_release_index import install_release_lock_paths


# Exercise the exact compatibility installer used by check_project_operating_contract.py
# and by the Tool Hub sealed validator runtimes on Linux and Windows.
install_release_lock_paths(contract)


class ProtectedBaselineAuthorityTests(unittest.TestCase):
    PROTECTED_PATHS = ["protected/"]

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        self._git("init", "-q")
        self._git("config", "user.email", "contract-test@example.invalid")
        self._git("config", "user.name", "Base Contract Test")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _git(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.repo), *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout.strip()

    def _write(self, relative: str, text: str) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _commit(self, message: str) -> str:
        self._git("add", "-A")
        self._git("commit", "-q", "-m", message)
        return self._git("rev-parse", "HEAD")

    def _baseline(self) -> tuple[str, dict]:
        self._write(
            "skills/PROJECT_BASE_ADAPTER.json",
            json.dumps(
                {"protected_paths": self.PROTECTED_PATHS},
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
        )
        self._write("protected/state.txt", "baseline\n")
        baseline = self._commit("baseline")
        adapter = {
            "protected_paths": list(self.PROTECTED_PATHS),
            "protected_baseline": {
                "authority_kind": "REMOTE_TRACKING_REF",
                "authority_ref": "refs/remotes/origin/main",
                "commit": baseline,
                "policy_sha256": contract._protected_policy_hash(self.PROTECTED_PATHS),
                "policy_source_path": "skills/PROJECT_BASE_ADAPTER.json",
                "policy_source_type": "CANONICAL_ADAPTER_SOURCE",
                "protected_paths_pointer": "/protected_paths",
            },
        }
        return baseline, adapter

    def _set_authority(self, commit: str) -> None:
        self._git("update-ref", "refs/remotes/origin/main", commit)

    def test_equal_remote_authority_remains_valid(self) -> None:
        baseline, adapter = self._baseline()
        self._set_authority(baseline)

        trusted, errors = contract._trusted_protected_base(
            self.repo,
            adapter["protected_baseline"],
            "",
        )

        self.assertEqual([], errors)
        self.assertEqual(baseline, trusted)

    def test_ancestor_remote_baseline_is_accepted_and_returned(self) -> None:
        baseline, adapter = self._baseline()
        self._write("docs/note.md", "metadata only\n")
        authority = self._commit("metadata descendant")
        self._set_authority(authority)

        trusted, errors = contract._trusted_protected_base(
            self.repo,
            adapter["protected_baseline"],
            "",
        )

        self.assertEqual([], errors)
        self.assertEqual(baseline, trusted)

    def test_missing_baseline_commit_fails_closed(self) -> None:
        baseline, adapter = self._baseline()
        self._set_authority(baseline)
        missing = "0" * 40
        adapter["protected_baseline"]["commit"] = missing

        trusted, errors = contract._trusted_protected_base(
            self.repo,
            adapter["protected_baseline"],
            "",
        )

        self.assertIsNone(trusted)
        self.assertEqual([f"Protected baseline commit is absent: {missing}"], errors)

    def test_divergent_remote_authority_fails_closed(self) -> None:
        baseline, adapter = self._baseline()
        self._git("checkout", "-q", "--orphan", "divergent")
        self._git("rm", "-q", "-rf", ".")
        self._write("other.txt", "unrelated history\n")
        divergent = self._commit("divergent authority")
        self._set_authority(divergent)

        trusted, errors = contract._trusted_protected_base(
            self.repo,
            adapter["protected_baseline"],
            "",
        )

        self.assertIsNone(trusted)
        self.assertTrue(any("ancestor" in error.lower() for error in errors), errors)
        self.assertTrue(all(baseline in error for error in errors), errors)

    def test_unprotected_descendant_passes_full_policy_validation(self) -> None:
        _, adapter = self._baseline()
        self._write("docs/note.md", "metadata only\n")
        authority = self._commit("metadata descendant")
        self._set_authority(authority)

        errors = contract._protected_policy_errors(self.repo, adapter, "")

        self.assertEqual([], errors)

    def test_protected_descendant_is_still_diffed_from_historical_baseline(self) -> None:
        _, adapter = self._baseline()
        self._write("protected/state.txt", "changed\n")
        authority = self._commit("protected descendant")
        self._set_authority(authority)

        errors = contract._protected_policy_errors(self.repo, adapter, "")

        self.assertIn("Protected-path changes detected: protected/state.txt", errors)

    def test_explicit_override_still_requires_exact_adapter_baseline(self) -> None:
        baseline, adapter = self._baseline()
        self._write("docs/note.md", "metadata only\n")
        descendant = self._commit("override descendant")
        self._set_authority(descendant)

        trusted, errors = contract._trusted_protected_base(
            self.repo,
            adapter["protected_baseline"],
            descendant,
        )

        self.assertIsNone(trusted)
        self.assertEqual(
            [
                "Trusted --protected-base must equal adapter baseline commit: "
                f"{descendant} != {baseline}"
            ],
            errors,
        )

    def test_github_pr_base_without_override_remains_fail_closed(self) -> None:
        _, adapter = self._baseline()
        adapter["protected_baseline"]["authority_kind"] = "GITHUB_PR_BASE"
        adapter["protected_baseline"]["authority_ref"] = "github.event.pull_request.base.sha"

        trusted, errors = contract._trusted_protected_base(
            self.repo,
            adapter["protected_baseline"],
            "",
        )

        self.assertIsNone(trusted)
        self.assertEqual(
            [
                "GITHUB_PR_BASE requires trusted --protected-base from "
                "github.event.pull_request.base.sha"
            ],
            errors,
        )


if __name__ == "__main__":
    unittest.main()
