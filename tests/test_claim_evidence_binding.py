from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_review_evidence.py"
RECORD_SCHEMA = ROOT / "skills/reviewing-and-validating-project-changes/contracts/review-record.schema.json"
RESULT_SCHEMA = ROOT / "skills/reviewing-and-validating-project-changes/contracts/review-result.schema.json"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_review_evidence", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


class ReviewRecordBehaviorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checker = load_checker()

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        git(self.root, "init", "-b", "main")
        git(self.root, "config", "user.email", "test@example.com")
        git(self.root, "config", "user.name", "Test User")
        target = self.root / "skills/reviewing-and-validating-project-changes/contracts"
        target.mkdir(parents=True)
        (target / "review-record.schema.json").write_text(
            RECORD_SCHEMA.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (target / "review-result.schema.json").write_text(
            RESULT_SCHEMA.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (self.root / "src").mkdir()
        (self.root / "src/feature.txt").write_text("old\n", encoding="utf-8")
        (self.root / "docs").mkdir()
        (self.root / "docs/canon.md").write_text("protected\n", encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-m", "baseline")
        self.base = git(self.root, "rev-parse", "HEAD").stdout.strip()
        (self.root / "records").mkdir()
        self.record_path = self.root / "records/review.json"

    def record(self) -> dict:
        return {
            "schema_version": 1,
            "artifact_role": "REVIEW_EVIDENCE_RECORD",
            "scope": {
                "allowed_changed_paths": ["records/review.json", "src/feature.txt"],
                "protected_paths": ["docs/canon.md"],
            },
            "claims": [
                {
                    "claim_id": "CLAIM-001",
                    "claim_type": "IMPLEMENTATION",
                    "claim_text": "Feature is implemented.",
                    "acceptance_ids": ["AC-001"],
                    "check_ids": ["CHECK-001"],
                }
            ],
            "acceptance": [
                {
                    "intent_id": "AC-001",
                    "approved_intent": "Feature marker is present.",
                    "implementation_paths": ["src/feature.txt"],
                    "required_level": "TEST",
                }
            ],
            "checks": [
                {
                    "check_id": "CHECK-001",
                    "argv": [
                        "{python}",
                        "-c",
                        (
                            "from pathlib import Path; "
                            "assert Path('src/feature.txt').read_text(encoding='utf-8') "
                            "== 'implemented\\n'; print('REVIEW_CHECK: PASS')"
                        ),
                    ],
                    "working_directory": ".",
                    "timeout_seconds": 30,
                    "declared_level": "TEST",
                    "acceptance_ids": ["AC-001"],
                    "markers": ["REVIEW_CHECK: PASS"],
                }
            ],
        }

    def commit(self, record: dict | None = None, feature: str = "implemented\n") -> str:
        self.record_path.write_text(
            json.dumps(record or self.record(), indent=2) + "\n", encoding="utf-8"
        )
        (self.root / "src/feature.txt").write_text(feature, encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-m", "feature")
        return git(self.root, "rev-parse", "HEAD").stdout.strip()

    def check(
        self,
        record: dict | None = None,
        feature: str = "implemented\n",
        *,
        execute: bool = True,
        approvals: dict[str, str] | None = None,
    ):
        self.commit(record, feature)
        return self.checker.check_record(
            self.root,
            self.record_path,
            self.base,
            execute_checks=execute,
            allowed_programs=(),
            approved_levels=approvals or {},
        )

    def test_valid_record_passes_and_binds_exact_git_state(self) -> None:
        result, errors = self.check()
        self.assertEqual([], errors)
        self.assertEqual("PASS", result["final_status"])
        self.assertEqual(self.base, result["subject"]["base_sha"])
        self.assertEqual("PASS", result["gates"]["implementation"]["status"])
        self.assertEqual("PASS", result["gates"]["verification"]["status"])
        self.assertEqual("PASS", result["gates"]["intent"]["status"])
        self.assertEqual("BLOCKED_UNVERIFIED", result["gates"]["integration"]["status"])
        self.assertEqual("CLAIM_VERIFIED", result["claims"][0]["status"])

    def test_valid_record_passes_without_vendored_review_schemas(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        git(root, "init", "-b", "main")
        git(root, "config", "user.email", "thin-adapter@example.invalid")
        git(root, "config", "user.name", "Thin Adapter Test")
        (root / "src").mkdir()
        (root / "src/feature.txt").write_text("old\n", encoding="utf-8")
        git(root, "add", ".")
        git(root, "commit", "-m", "baseline")
        base = git(root, "rev-parse", "HEAD").stdout.strip()

        record_path = root / "records/review.json"
        record_path.parent.mkdir()
        record_path.write_text(
            json.dumps(self.record(), indent=2) + "\n", encoding="utf-8"
        )
        (root / "src/feature.txt").write_text("implemented\n", encoding="utf-8")
        git(root, "add", ".")
        git(root, "commit", "-m", "feature")

        self.assertFalse((root / "skills").exists())
        result, errors = self.checker.check_record(
            root,
            record_path,
            base,
            execute_checks=True,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertEqual([], errors)
        self.assertEqual("PASS", result["final_status"])

    def test_no_execution_is_not_pass(self) -> None:
        result, errors = self.check(execute=False)
        self.assertEqual("NOT_RUN", result["gates"]["verification"]["status"])
        self.assertTrue(any("not executed" in item for item in errors), errors)
        self.assertEqual("CLAIM_UNVERIFIED", result["claims"][0]["status"])

    def test_unchanged_implementation_path_fails(self) -> None:
        (self.root / "src/unchanged.txt").write_text("same\n", encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-m", "unchanged baseline")
        self.base = git(self.root, "rev-parse", "HEAD").stdout.strip()
        record = self.record()
        record["acceptance"][0]["implementation_paths"] = ["src/unchanged.txt"]
        result, errors = self.check(record)
        self.assertEqual("FAIL", result["gates"]["implementation"]["status"])
        self.assertTrue(any("not changed" in item for item in errors), errors)

    def test_failed_check_overrides_confident_claim(self) -> None:
        result, errors = self.check(feature="wrong\n")
        self.assertEqual("FAIL", result["gates"]["verification"]["status"])
        self.assertNotEqual(0, result["gates"]["verification"]["checks"][0]["exit_code"])
        self.assertTrue(any("failed with exit code" in item for item in errors), errors)

    def test_evidence_ceiling_blocks_runtime_claim(self) -> None:
        record = self.record()
        record["acceptance"][0]["required_level"] = "RUNTIME"
        result, errors = self.check(record)
        acceptance = result["gates"]["intent"]["acceptance_results"][0]
        self.assertEqual("TEST", acceptance["observed_level"])
        self.assertEqual("FAIL", acceptance["status"])
        self.assertTrue(any("evidence ceiling" in item for item in errors), errors)

    def test_protected_change_fails(self) -> None:
        record = self.record()
        record["scope"]["allowed_changed_paths"].append("docs/canon.md")
        self.commit(record)
        (self.root / "docs/canon.md").write_text("tampered\n", encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-m", "tamper")
        result, errors = self.checker.check_record(
            self.root,
            self.record_path,
            self.base,
            execute_checks=True,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertEqual("FAIL", result["gates"]["implementation"]["status"])
        self.assertTrue(any("protected path changed" in item for item in errors), errors)

    def test_base_equal_head_fails_empty_diff(self) -> None:
        head = self.commit()
        result, errors = self.checker.check_record(
            self.root,
            self.record_path,
            head,
            execute_checks=True,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertEqual("FAIL", result["final_status"])
        self.assertTrue(any("no changed files" in item for item in errors), errors)

    def test_unapproved_program_fails_before_execution(self) -> None:
        record = self.record()
        record["checks"][0]["argv"] = ["git", "status", "--short"]
        result, errors = self.check(record)
        self.assertEqual("FAIL", result["gates"]["verification"]["status"])
        self.assertTrue(any("program is not approved" in item for item in errors), errors)

    def test_zero_exit_without_marker_fails(self) -> None:
        record = self.record()
        record["checks"][0]["argv"] = ["{python}", "-c", "print('other')"]
        result, errors = self.check(record)
        self.assertEqual("FAIL", result["gates"]["verification"]["status"])
        self.assertTrue(any("missing required marker" in item for item in errors), errors)

    def test_self_declared_runtime_is_capped_at_test(self) -> None:
        record = self.record()
        record["acceptance"][0]["required_level"] = "RUNTIME"
        record["checks"][0]["declared_level"] = "RUNTIME"
        result, errors = self.check(record)
        check = result["gates"]["verification"]["checks"][0]
        self.assertEqual("TEST", check["observed_level"])
        self.assertTrue(any("evidence ceiling" in item for item in errors), errors)

    def test_explicit_runtime_approval_is_accepted(self) -> None:
        record = self.record()
        record["acceptance"][0]["required_level"] = "RUNTIME"
        record["checks"][0]["declared_level"] = "RUNTIME"
        result, errors = self.check(record, approvals={"CHECK-001": "RUNTIME"})
        self.assertEqual([], errors)
        self.assertEqual("PASS", result["final_status"])
        self.assertEqual("RUNTIME", result["gates"]["verification"]["checks"][0]["observed_level"])

    def test_undeclared_changed_path_fails(self) -> None:
        self.commit()
        (self.root / "docs/extra.md").write_text("extra\n", encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-m", "extra")
        result, errors = self.checker.check_record(
            self.root,
            self.record_path,
            self.base,
            execute_checks=True,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertEqual("FAIL", result["gates"]["implementation"]["status"])
        self.assertTrue(any("outside allowed scope" in item for item in errors), errors)

    def test_dirty_worktree_fails(self) -> None:
        self.commit()
        (self.root / "src/feature.txt").write_text("dirty\n", encoding="utf-8")
        result, errors = self.checker.check_record(
            self.root,
            self.record_path,
            self.base,
            execute_checks=True,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertEqual("FAIL", result["gates"]["implementation"]["status"])
        self.assertTrue(any("worktree must be clean" in item for item in errors), errors)

    def test_literal_brackets_in_repository_paths_are_matched(self) -> None:
        (self.root / "[proposal]").mkdir()
        (self.root / "[proposal]/note.md").write_text("old\n", encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-m", "bracket baseline")
        self.base = git(self.root, "rev-parse", "HEAD").stdout.strip()
        record = self.record()
        record["scope"]["allowed_changed_paths"].append("[proposal]/**")
        record["acceptance"][0]["implementation_paths"] = ["[proposal]/note.md"]
        self.record_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        (self.root / "[proposal]/note.md").write_text("new\n", encoding="utf-8")
        git(self.root, "add", ".")
        git(self.root, "commit", "-m", "bracket change")
        result, errors = self.checker.check_record(
            self.root,
            self.record_path,
            self.base,
            execute_checks=True,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertFalse(any("outside allowed scope: [proposal]/note.md" in item for item in errors), errors)
        self.assertEqual("PASS", result["gates"]["implementation"]["status"])


class IntakeParallelPrPolicyBindingTests(unittest.TestCase):
    def test_user_directed_parallel_pr_policy_is_bound_to_existing_intake_owner(self) -> None:
        skill = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        reference = (
            ROOT
            / "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"
        ).read_text(encoding="utf-8")
        sync = (
            ROOT
            / "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"
        ).read_text(encoding="utf-8")

        for text in (skill, reference):
            for term in (
                "USER_DIRECTED_PARALLEL_PR",
                "current completed main",
                "separate branch/PR",
                "same-goal",
                "in-progress PR",
                "scheduled/periodic",
                "PROVISIONAL_INTEGRATION",
                "synchronizing-local-and-github-state",
                "BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16",
            ):
                self.assertIn(term, text)
        self.assertIn("do not modify/rebase/update", reference)
        self.assertIn("superseded", reference)
        self.assertIn("read-only overlap evidence", skill)
        self.assertIn("selective copy", reference)
        self.assertIn("absorbed_owner_deltas", reference)
        self.assertIn("residual_owner_deltas", reference)
        self.assertIn("owner PR이 열려 있다는 사실만으로", reference)
        for term in (
            "BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16",
            "owner PR branches",
            "semantic reconciliation",
            "selective copy",
            "absorbed_owner_deltas",
            "residual_owner_deltas",
        ):
            self.assertIn(term, sync)
        self.assertNotIn("owner가 해결되기 전에는 merge하지 않는다", reference)


if __name__ == "__main__":
    unittest.main()
