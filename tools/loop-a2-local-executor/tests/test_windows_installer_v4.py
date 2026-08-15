from __future__ import annotations

import os
from pathlib import Path
import subprocess
import unittest


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parents[1]
INSTALLER = PACKAGE_ROOT / "windows" / "Base_Loop_A2_Local_Executor_Installer_v4.cmd"
OWNER_DOC = REPO_ROOT / "docs" / "LOOP_A2_LOCAL_EXECUTOR.md"
EVIDENCE = REPO_ROOT / "docs" / "evidence" / "2026-08-15-local-executor-docker-capability-resolver.md"
IMAGE_REF = "python:3.12-slim@sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65"


class WindowsInstallerV4ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = INSTALLER.read_text(encoding="utf-8")
        cls.folded = cls.text.casefold()

    def test_v4_is_double_clickable_and_preserves_diagnostics(self) -> None:
        self.assertIn("Base Loop A2 Installer v4", self.text)
        self.assertIn('start "Base Loop A2 Installer v4" "%ComSpec%" /d /k', self.text)
        self.assertIn("Base_Loop_A2_Installer.log", self.text)
        self.assertIn("INSTALLATION_BLOCKED", self.text)
        self.assertIn("INSTALLER_V4_CONTRACT_OK", self.text)

    def test_v4_preserves_install_state_and_exact_reviewed_image_identity(self) -> None:
        for literal in (
            r"%LOCALAPPDATA%\BaseLoopA2LocalExecutorApp",
            r"%LOCALAPPDATA%\BaseLoopA2LocalExecutor",
            r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup",
            IMAGE_REF,
        ):
            self.assertIn(literal, self.text)

        self.assertIn("fetch origin main --prune", self.text)
        self.assertIn("checkout --detach origin/main", self.text)
        self.assertIn("pip install --disable-pip-version-check -e", self.text)

    def test_v4_discovers_docker_from_path_then_trusted_per_user_then_all_users_locations(self) -> None:
        per_user = r"%LOCALAPPDATA%\Programs\DockerDesktop\resources\bin\docker.exe"
        all_users = r"%ProgramFiles%\Docker\Docker\resources\bin\docker.exe"
        resolver_call = (
            'call :resolve DOCKER_CMD docker '
            '"%LOCALAPPDATA%\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" '
            '"%ProgramFiles%\\Docker\\Docker\\resources\\bin\\docker.exe"'
        )

        self.assertIn(per_user, self.text)
        self.assertIn(all_users, self.text)
        self.assertIn(resolver_call, self.text)
        self.assertIn('if not defined %~1 if exist "%~4" set "%~1=%~4"', self.text)
        self.assertLess(self.text.index(per_user), self.text.index(all_users))

    def test_v4_uses_executor_preflight_as_docker_truth_and_only_pulls_exact_digest_on_missing_image(self) -> None:
        self.assertIn("loop-a2-local-executor.exe", self.text)
        self.assertGreaterEqual(self.text.count("call :capture_preflight"), 2)
        self.assertIn("DOCKER_IMAGE_NOT_PRELOADED", self.text)
        self.assertIn('"!DOCKER_CMD!" pull "!IMAGE_REF!"', self.text)
        self.assertNotIn("docker image ls", self.folded)
        self.assertNotIn("docker images", self.folded)
        self.assertNotIn("python:3.12-slim ", self.text)

        first_preflight = self.text.index("Executor shared preflight")
        missing_image = self.text.index("DOCKER_IMAGE_NOT_PRELOADED")
        pull = self.text.index('"!DOCKER_CMD!" pull "!IMAGE_REF!"')
        second_preflight = self.text.index("Executor shared preflight after exact image pull")
        self.assertLess(first_preflight, missing_image)
        self.assertLess(missing_image, pull)
        self.assertLess(pull, second_preflight)

    def test_v4_restarts_only_the_owned_daemon_and_confirms_exact_process_identity(self) -> None:
        self.assertIn(":stop_existing_daemon", self.text)
        self.assertIn(":confirm_daemon", self.text)
        self.assertIn("Get-CimInstance Win32_Process", self.text)
        self.assertIn("ExecutablePath", self.text)
        self.assertIn("loop_a2_local_executor.cli", self.text)
        self.assertIn("STATE_ROOT", self.text)
        self.assertNotIn("taskkill /im pythonw.exe", self.folded)
        self.assertNotIn("taskkill /f /im pythonw.exe", self.folded)
        self.assertIn("LOCAL_EXECUTOR_DAEMON_RUNNING", self.text)
        self.assertIn("Background:   STARTED", self.text)
        self.assertIn("Startup:      REGISTERED", self.text)

        daemon_confirmed = self.text.index("LOCAL_EXECUTOR_DAEMON_RUNNING")
        ready_banner = self.text.rindex("LOCAL_EXECUTOR_READY")
        self.assertLess(daemon_confirmed, ready_banner)

    def test_owner_and_durable_evidence_describe_the_same_resolver_and_live_ceiling(self) -> None:
        owner = OWNER_DOC.read_text(encoding="utf-8")
        evidence = EVIDENCE.read_text(encoding="utf-8")

        for term in (
            "docker image inspect --platform",
            "DOCKER_IMAGE_NOT_PRELOADED",
            "Base_Loop_A2_Local_Executor_Installer_v4.cmd",
            "shared preflight",
        ):
            self.assertIn(term, owner)

        for term in (
            "#419",
            "#420",
            "31851656420",
            "31851800827",
            "DOCKER_IMAGE_NOT_PRELOADED",
            "LOCAL_EXECUTOR_READY",
            "real_a2_burnin_runs: 0",
            "live_v4_user_pc_preflight: NOT_RUN",
        ):
            self.assertIn(term, evidence)

    @unittest.skipUnless(os.name == "nt", "Windows cmd contract smoke")
    def test_v4_contract_mode_parses_without_running_installer(self) -> None:
        completed = subprocess.run(
            [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", str(INSTALLER), "--contract-test"],
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("INSTALLER_V4_CONTRACT_OK", completed.stdout)
        self.assertNotIn("LOCAL_EXECUTOR_READY", completed.stdout)


if __name__ == "__main__":
    unittest.main()
