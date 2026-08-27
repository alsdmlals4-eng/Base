from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/validate-game-project-operating-system.yml"
CASE = ROOT / "docs/knowledge/cases/WINDOWS_PUBLICATION_DEPENDENCY_DOWNLOAD_TRANSPORT_FAILURE_CASE.md"
PROPOSAL = ROOT / "[수정제안서]/BCP-2026-041-windows-publication-download-recovery/PROPOSAL.md"


class WindowsPublicationDependencyDownloadRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def _windows_install_step(self) -> str:
        match = re.search(
            r"- name: Install Windows system publication dependencies\n"
            r"(?P<body>.*?)(?=\n\s+- name: Install Windows Python publication dependencies)",
            self.workflow,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        return match.group("body")

    def test_windows_dependency_download_uses_bounded_retry_and_fallback(self) -> None:
        body = self._windows_install_step()
        for token in (
            "function Invoke-VerifiedDownload",
            "$maxAttempts = 3",
            "Start-Sleep -Seconds",
            "curl.exe",
            "--fail",
            "--location",
            "--retry",
            "--retry-all-errors",
            "TRANSPORT_RETRY_EXHAUSTED",
        ):
            self.assertIn(token, body)

    def test_partial_downloads_are_removed_and_hash_verification_is_not_weakened(self) -> None:
        body = self._windows_install_step()
        for token in (
            "if (Test-Path -LiteralPath $OutFile)",
            "Remove-Item -LiteralPath $OutFile -Force",
            "Get-FileHash -Algorithm SHA256",
            "DOWNLOAD_SHA256_MISMATCH",
            "$ExpectedSha256.ToLowerInvariant()",
        ):
            self.assertIn(token, body)
        self.assertIn(
            '$libreOfficeSha256 = "468d1fb3880af3bcddac002e9054155912c70b45d105bfa1c82036f33456133d"',
            body,
        )
        self.assertIn(
            '$popplerSha256 = "58A6F9AE269756231D2F9AA6CBA39D75FEC6DEACAF3C4A50683383B5F3D5A527"',
            body,
        )

    def test_same_verified_helper_is_used_for_libreoffice_and_poppler(self) -> None:
        body = self._windows_install_step()
        self.assertRegex(
            body,
            r"Invoke-VerifiedDownload\s+"
            r"-Uri \$libreOfficeUrl\s+"
            r"-OutFile \$libreOfficeMsi\s+"
            r"-ExpectedSha256 \$libreOfficeSha256",
        )
        self.assertRegex(
            body,
            r"Invoke-VerifiedDownload\s+"
            r"-Uri \$popplerUrl\s+"
            r"-OutFile \$popplerZip\s+"
            r"-ExpectedSha256 \$popplerSha256",
        )

    def test_incident_case_and_approved_proposal_are_durable(self) -> None:
        self.assertTrue(CASE.exists())
        case = CASE.read_text(encoding="utf-8")
        for token in (
            "WINDOWS_PUBLICATION_DEPENDENCY_DOWNLOAD_TRANSPORT_FAILURE",
            "unexpected EOF",
            "forcibly closed",
            "33041116377",
            "core-regression: PASS",
            "NO_TEST_OR_HASH_WEAKENING",
            "bounded retry",
            "curl.exe fallback",
        ):
            self.assertIn(token, case)

        self.assertTrue(PROPOSAL.exists())
        proposal = PROPOSAL.read_text(encoding="utf-8")
        self.assertIn("BCP-2026-041", proposal)
        self.assertIn("APPROVED_FOR_IMPLEMENTATION", proposal)
        self.assertIn("ZERO_INCREMENTAL_COST_REQUIRED", proposal)


if __name__ == "__main__":
    unittest.main()
