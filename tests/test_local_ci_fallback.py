from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import run_local_ci_fallback as fallback


class LocalCiFallbackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.remote = self.root / "remote.git"
        self.work = self.root / "work"
        self.fake_gh = self.root / "fake_gh.py"
        self.scenario = self.root / "scenario.json"
        self.gh_log = self.root / "gh-log.jsonl"
        self.gh_state = self.root / "gh-state.json"

        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, capture_output=True)
        subprocess.run(["git", "init", "-b", "main", str(self.work)], check=True, capture_output=True)
        self.git("config", "user.name", "CI Fallback Test")
        self.git("config", "user.email", "ci-fallback@example.invalid")
        (self.work / "tools").mkdir()
        (self.work / "tools/run_local_validation.py").write_text(
            "from __future__ import annotations\n"
            "import os\n"
            "raise SystemExit(int(os.environ.get('FAKE_VALIDATION_EXIT', '0')))\n",
            encoding="utf-8",
        )
        (self.work / "tracked.txt").write_text("base\n", encoding="utf-8")
        self.git("add", "tools/run_local_validation.py", "tracked.txt")
        self.git("commit", "-m", "base")
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")
        self.base_sha = self.git_output("rev-parse", "HEAD")

        self.git("checkout", "-b", "feature")
        (self.work / "tracked.txt").write_text("feature\n", encoding="utf-8")
        self.git("add", "tracked.txt")
        self.git("commit", "-m", "feature")
        self.git("push", "-u", "origin", "feature")
        self.head_sha = self.git_output("rev-parse", "HEAD")
        self.merge_sha = "f" * 40

        self.write_fake_gh()
        self.write_scenario()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=self.work, check=True, capture_output=True, text=True)

    def git_output(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args],
            cwd=self.work,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def write_fake_gh(self) -> None:
        self.fake_gh.write_text(
            "from __future__ import annotations\n"
            "import json\n"
            "import os\n"
            "import sys\n"
            "from pathlib import Path\n"
            "\n"
            "args = sys.argv[1:]\n"
            "scenario_path = Path(os.environ['FAKE_GH_SCENARIO'])\n"
            "log_path = Path(os.environ['FAKE_GH_LOG'])\n"
            "state_path = Path(os.environ['FAKE_GH_STATE'])\n"
            "scenario = json.loads(scenario_path.read_text(encoding='utf-8'))\n"
            "with log_path.open('a', encoding='utf-8') as handle:\n"
            "    handle.write(json.dumps(args) + '\\n')\n"
            "if args[:2] == ['auth', 'status']:\n"
            "    raise SystemExit(int(scenario.get('auth_exit', 0)))\n"
            "if not args or args[0] != 'api':\n"
            "    raise SystemExit(90)\n"
            "method = 'GET'\n"
            "if '--method' in args:\n"
            "    method = args[args.index('--method') + 1]\n"
            "path = next((value for value in args[1:] if not value.startswith('-') and value not in {'GET', 'POST'}), '')\n"
            "if '/pulls/' in path and method == 'GET':\n"
            "    print(json.dumps(scenario['pr']))\n"
            "    raise SystemExit(0)\n"
            "if path.endswith('/check-runs') and method == 'GET':\n"
            "    sha = path.split('/commits/', 1)[1].split('/check-runs', 1)[0]\n"
            "    state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}\n"
            "    count = int(state.get(sha, 0))\n"
            "    state[sha] = count + 1\n"
            "    state_path.write_text(json.dumps(state), encoding='utf-8')\n"
            "    checks = scenario.get('checks', {}).get(sha, [])\n"
            "    if scenario.get('race_sha') == sha and count >= 1:\n"
            "        checks = [{'name': 'ci-gate', 'status': 'queued', 'conclusion': None}]\n"
            "    print(json.dumps({'check_runs': checks}))\n"
            "    raise SystemExit(0)\n"
            "if '/statuses/' in path and method == 'POST':\n"
            "    print(json.dumps({'created': True}))\n"
            "    raise SystemExit(0)\n"
            "raise SystemExit(91)\n",
            encoding="utf-8",
        )

    def write_scenario(
        self,
        *,
        head_sha: str | None = None,
        base_ref: str = "main",
        checks: dict[str, list[dict[str, object]]] | None = None,
        race_sha: str | None = None,
    ) -> None:
        payload = {
            "pr": {
                "state": "open",
                "head": {"sha": head_sha or self.head_sha},
                "base": {"ref": base_ref},
                "merge_commit_sha": self.merge_sha,
            },
            "checks": checks or {},
        }
        if race_sha is not None:
            payload["race_sha"] = race_sha
        self.scenario.write_text(json.dumps(payload), encoding="utf-8")
        if self.gh_state.exists():
            self.gh_state.unlink()
        if self.gh_log.exists():
            self.gh_log.unlink()

    def environment(self, **extra: str) -> dict[str, str]:
        env = dict(os.environ)
        env.update(
            {
                "FAKE_GH_SCENARIO": str(self.scenario),
                "FAKE_GH_LOG": str(self.gh_log),
                "FAKE_GH_STATE": str(self.gh_state),
                "FAKE_VALIDATION_EXIT": "0",
            }
        )
        env.update(extra)
        return env

    def run_fallback(self, **env_overrides: str) -> int:
        return fallback.run_local_fallback(
            self.work,
            "alsdmlals4-eng/Base",
            1,
            "main",
            self.base_sha,
            sys.executable,
            environment=self.environment(**env_overrides),
            gh_command=(sys.executable, str(self.fake_gh)),
        )

    def logged_gh_calls(self) -> list[list[str]]:
        if not self.gh_log.exists():
            return []
        return [json.loads(line) for line in self.gh_log.read_text(encoding="utf-8").splitlines()]

    def assert_no_status_post(self) -> None:
        self.assertFalse(
            any("POST" in call and any("/statuses/" in arg for arg in call) for call in self.logged_gh_calls())
        )

    def test_refuses_when_worktree_is_dirty(self) -> None:
        (self.work / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "worktree must be clean"):
            self.run_fallback()
        self.assert_no_status_post()

    def test_refuses_when_local_head_differs_from_pr_head(self) -> None:
        self.write_scenario(head_sha="0" * 40)
        with self.assertRaisesRegex(RuntimeError, "does not match PR head"):
            self.run_fallback()
        self.assert_no_status_post()

    def test_refuses_when_base_is_not_ancestor_of_head(self) -> None:
        self.git("checkout", "main")
        (self.work / "base-only.txt").write_text("new base\n", encoding="utf-8")
        self.git("add", "base-only.txt")
        self.git("commit", "-m", "advance base")
        self.git("push", "origin", "main")
        self.git("checkout", "feature")
        with self.assertRaisesRegex(RuntimeError, "not up to date with origin/main"):
            self.run_fallback()
        self.assert_no_status_post()

    def test_refuses_when_ci_gate_check_exists_on_head(self) -> None:
        self.write_scenario(checks={self.head_sha: [{"name": "ci-gate", "status": "completed", "conclusion": "failure"}]})
        with self.assertRaisesRegex(RuntimeError, "ci-gate Check Run already exists"):
            self.run_fallback()
        self.assert_no_status_post()

    def test_refuses_when_ci_gate_check_exists_on_test_merge_commit(self) -> None:
        self.write_scenario(checks={self.merge_sha: [{"name": "ci-gate", "status": "queued", "conclusion": None}]})
        with self.assertRaisesRegex(RuntimeError, "ci-gate Check Run already exists"):
            self.run_fallback()
        self.assert_no_status_post()

    def test_validation_failure_never_publishes_success_status(self) -> None:
        self.assertEqual(7, self.run_fallback(FAKE_VALIDATION_EXIT="7"))
        self.assert_no_status_post()

    def test_ci_gate_appearing_after_validation_prevents_status_publish(self) -> None:
        self.write_scenario(race_sha=self.head_sha)
        with self.assertRaisesRegex(RuntimeError, "ci-gate Check Run already exists"):
            self.run_fallback()
        self.assert_no_status_post()

    def test_success_publishes_ci_gate_for_exact_head_sha(self) -> None:
        self.assertEqual(0, self.run_fallback())
        posts = [
            call
            for call in self.logged_gh_calls()
            if "POST" in call and any("/statuses/" in arg for arg in call)
        ]
        self.assertEqual(1, len(posts))
        self.assertIn(f"repos/alsdmlals4-eng/Base/statuses/{self.head_sha}", posts[0])
        self.assertIn("state=success", posts[0])
        self.assertIn("context=ci-gate", posts[0])


if __name__ == "__main__":
    unittest.main()
