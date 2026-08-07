from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def dependabot_blocks(text: str) -> dict[str, str]:
    matches = list(
        re.finditer(
            r'^  - package-ecosystem: "([^"]+)"\s*$',
            text,
            flags=re.MULTILINE,
        )
    )
    blocks: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        ecosystem = match.group(1)
        if ecosystem in blocks:
            raise AssertionError(f"duplicate Dependabot ecosystem: {ecosystem}")
        blocks[ecosystem] = text[match.start() : end]
    return blocks


def workflow_job(workflow: str, job_name: str, next_job_name: str) -> str:
    match = re.search(
        rf"(?ms)^  {re.escape(job_name)}:\n(?P<body>.*?)(?=^  {re.escape(next_job_name)}:\n)",
        workflow,
    )
    if match is None:
        raise AssertionError(f"workflow job not found: {job_name}")
    return match.group("body")


def repository_profile() -> dict[str, str]:
    profile_path = ROOT / "docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md"
    if not profile_path.is_file():
        raise AssertionError("mutable Base repository governance profile is missing")
    profile = profile_path.read_text(encoding="utf-8")
    match = re.search(r"(?ms)^repository:\s*$\n(?P<body>(?:  [^\n]+\n)+)", profile)
    if match is None:
        raise AssertionError("repository block is missing from mutable governance profile")
    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        key, separator, value = line.strip().partition(":")
        if not separator or not value.strip():
            raise AssertionError(f"invalid repository profile line: {line!r}")
        values[key] = value.strip()
    return values


class RepositoryGovernanceBaselineTests(unittest.TestCase):
    def test_repository_profile_template_can_record_current_owner(self) -> None:
        template = read(
            "templates/project-operations/github/GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md"
        )
        repository_block = re.search(
            r"(?ms)^repository:\s*$\n(?P<body>(?:  [^\n]*\n)+)", template
        )
        self.assertIsNotNone(repository_block)
        self.assertRegex(repository_block.group("body"), r"(?m)^  owner:\s*$")

    def test_each_platform_surface_has_one_unambiguous_location(self) -> None:
        candidates = {
            "license": ("LICENSE", "LICENSE.md", "LICENSE.txt"),
            "security": ("SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"),
            "codeowners": (".github/CODEOWNERS", "CODEOWNERS", "docs/CODEOWNERS"),
            "dependabot": (".github/dependabot.yml", ".github/dependabot.yaml"),
        }
        for surface, paths in candidates.items():
            found = [path for path in paths if (ROOT / path).is_file()]
            with self.subTest(surface=surface):
                self.assertEqual([paths[0]], found)

    def test_mit_license_matches_repository_identity_and_readme(self) -> None:
        license_text = read("LICENSE")
        self.assertEqual(
            "ea8e07e5e79f6abb9849fb8fc91358b00e381aafa89449f098d50ca7d5ea0ab2",
            hashlib.sha256(license_text.encode("utf-8")).hexdigest(),
        )
        for term in (
            "MIT License",
            "Copyright (c) 2026 alsdmlals4-eng",
            "Permission is hereby granted, free of charge",
            "The above copyright notice and this permission notice",
            'THE SOFTWARE IS PROVIDED "AS IS"',
        ):
            with self.subTest(term=term):
                self.assertIn(term, license_text)

        readme = read("README.md")
        self.assertIn("[MIT License](LICENSE)", readme)
        self.assertIn("[Security Policy](SECURITY.md)", readme)

    def test_security_policy_is_private_scope_bound_and_truthful(self) -> None:
        security = read("SECURITY.md")
        for term in (
            "| `main` | Supported |",
            "| Frozen release snapshots | Not supported |",
            "| Downstream project copies | Not supported |",
            "https://github.com/alsdmlals4-eng/Base/security/advisories/new",
            "UNVERIFIED_REPOSITORY_SETTING",
            "Do not disclose sensitive vulnerability details in a public issue",
            "detail-free public issue",
        ):
            with self.subTest(term=term):
                self.assertIn(term, security)

        self.assertNotRegex(security, r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")

    def test_codeowners_uses_the_actual_repository_owner_and_self_owns(self) -> None:
        repository = repository_profile()
        self.assertEqual("public", repository["visibility"])
        self.assertEqual("main", repository["primary_branch"])
        profile_owner, separator, repository_name = repository["name"].partition("/")
        self.assertEqual("/", separator)
        self.assertEqual(repository["owner"], profile_owner)
        self.assertEqual("Base", repository_name)
        if live_repository := os.environ.get("GITHUB_REPOSITORY"):
            self.assertEqual(live_repository, repository["name"])
        owner = "@" + repository["owner"]
        active_lines = [
            line.strip()
            for line in read(".github/CODEOWNERS").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        self.assertEqual([f"* {owner}", f"/.github/ {owner}"], active_lines)
        for line in active_lines:
            self.assertNotRegex(line, r"@[\w.-]+/[\w.-]+")

    def test_dependabot_enables_supported_ecosystems_and_defers_pnpm_11(self) -> None:
        package = json.loads(read("package.json"))
        self.assertRegex(package["packageManager"], r"^pnpm@11\.")
        self.assertTrue((ROOT / "pnpm-lock.yaml").is_file())
        self.assertTrue((ROOT / "requirements-publication.txt").is_file())
        self.assertRegex(
            read(".github/workflows/validate-game-project-operating-system.yml"),
            r"(?m)^\s+uses: [^\s]+@",
        )

        config = read(".github/dependabot.yml")
        self.assertRegex(config, r"(?m)^version: 2$")
        self.assertIn("DEPENDABOT_DEFERRED_PNPM_11", config)
        blocks = dependabot_blocks(config)
        self.assertEqual({"pip", "github-actions"}, set(blocks))
        self.assertNotIn('package-ecosystem: "npm"', config)

        expected_times = {
            "pip": "03:00",
            "github-actions": "03:15",
        }
        for ecosystem, block in blocks.items():
            with self.subTest(ecosystem=ecosystem):
                self.assertIn('directory: "/"', block)
                self.assertIn('interval: "weekly"', block)
                self.assertIn('day: "monday"', block)
                self.assertIn(f'time: "{expected_times[ecosystem]}"', block)
                self.assertIn('timezone: "UTC"', block)
                self.assertIn("open-pull-requests-limit: 5", block)
                self.assertIn('patterns: ["*"]', block)
                self.assertIn('update-types: ["minor", "patch"]', block)
                self.assertNotIn('"major"', block)

    def test_docs_only_governance_changes_execute_this_regression(self) -> None:
        workflow = read(".github/workflows/validate-game-project-operating-system.yml")
        docs_job = workflow_job(workflow, "docs-validation", "ubuntu-contract")
        job_header = docs_job.split("    steps:", 1)[0]
        self.assertNotRegex(job_header, r"(?m)^    if:")
        self.assertIn("tests/test_repository_governance_baseline.py", docs_job)

        docs_case = re.search(
            r"(?m)^                  (?P<patterns>README\.md\|docs/\*\|\*\.md\|\*\.txt\))$",
            workflow,
        )
        self.assertIsNotNone(docs_case)
        patterns = docs_case.group("patterns").removesuffix(")").split("|")
        for changed_path in ("README.md", "SECURITY.md"):
            with self.subTest(changed_path=changed_path):
                self.assertTrue(
                    any(fnmatch.fnmatchcase(changed_path, pattern) for pattern in patterns)
                )

    def test_contract_ci_also_executes_this_regression(self) -> None:
        workflow = read(".github/workflows/validate-game-project-operating-system.yml")
        contract_job = workflow_job(workflow, "ubuntu-contract", "publication-validation")
        self.assertGreaterEqual(
            contract_job.count("tests/test_repository_governance_baseline.py"),
            2,
        )

    def test_one_click_play_handoff_contract_is_explicit_and_project_consumable(self) -> None:
        policy = read("docs/ONE_CLICK_PLAY_HANDOFF_POLICY.md")
        slice_plan = read("templates/planning/VERTICAL_SLICE_PLAN.md")
        validation = read("templates/quality/PROJECT_CHANGE_VALIDATION.md")
        handoff = read("templates/project-operations/HANDOFF.md")

        for term in (
            "Project Play",
            "별도 Scene 선택",
            "성공·실패·복귀",
            "Fetch origin → Pull origin",
            "로컬 HEAD",
            "FAIL · RETEST_REQUIRED",
            "application/run/main_scene",
            "필요한 최소 통합 변경",
            "Task의 주 구현 폴더",
            "Prototype/Test Scene",
            "사용자가 기존 Main Scene을 유지하라고 명시",
        ):
            self.assertIn(term, policy)

        for term in ("Project Play", "별도 Scene 선택", "성공·실패·복귀"):
            self.assertIn(term, slice_plan)
        for term in ("사용자의 기본 실행 시작점", "FAIL · RETEST_REQUIRED"):
            self.assertIn(term, validation)
        for term in (
            "repository",
            "branch",
            "commit SHA",
            "Fetch origin → Pull origin",
            "기대 첫 화면",
            "Project Play",
        ):
            self.assertIn(term, handoff)


if __name__ == "__main__":
    unittest.main()
