from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "tools/build_skill_implementation_evidence.py"
GENERATED_PATH = ROOT / "docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md"
REVIEW_OWNER = ROOT / "skills/reviewing-and-validating-project-changes"
REVIEW_SCRIPT = ROOT / "tools/check_review_evidence.py"
REVIEW_RECORD_SCHEMA = REVIEW_OWNER / "contracts/review-record.schema.json"
REVIEW_RESULT_SCHEMA = REVIEW_OWNER / "contracts/review-result.schema.json"
REVIEW_TEMPLATE = ROOT / "templates/quality/REVIEW_EVIDENCE_RECORD.json"


def load_builder():
    spec = importlib.util.spec_from_file_location("build_skill_implementation_evidence", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_review_checker():
    spec = importlib.util.spec_from_file_location("check_review_evidence", REVIEW_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def active_skill(skill_id: str) -> dict:
    return {
        "skill_id": skill_id,
        "layer": "specialist",
        "discipline": "test-discipline",
        "path": f"skills/{skill_id}/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": [skill_id],
        "use_when": ["test"],
        "do_not_use_when": ["not test"],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["failure"],
        "last_reviewed_at": "2026-08-02",
        "last_reviewed_commit": "test",
        "knowledge_state": "OBSERVATION",
    }


def behavior_case(case_id: str, primary: str, forbidden: str) -> dict:
    return {
        "case_id": case_id,
        "case_type": "positive",
        "prompt": f"Concrete evidence request {case_id} without routing labels.",
        "expected_work_mode": "PLAN",
        "expected_primary_skill": primary,
        "expected_supporting_skills": [],
        "expected_skill_modes": ["run"],
        "forbidden_skills": [forbidden],
        "required_evidence": ["evidence"],
        "expected_user_decision_state": "NOT_REQUIRED",
        "rationale": "Focused evidence fixture.",
    }


class SkillImplementationEvidenceTests(unittest.TestCase):
    def test_builder_and_generated_evidence_exist(self) -> None:
        self.assertTrue(BUILDER_PATH.is_file())
        self.assertTrue(GENERATED_PATH.is_file())

    def build_root(
        self,
        include_beta_entry: bool = True,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        write_json(
            root / "skills/SKILL_REGISTRY.json",
            {
                "schema_version": 1,
                "registry_role": "test",
                "routing_policy": {},
                "skills": [active_skill("alpha-skill"), active_skill("beta-skill")],
            },
        )
        write_json(
            root / "skills/SKILL_BEHAVIOR_EVALS.json",
            {
                "schema_version": 1,
                "artifact_role": "BASE_SKILL_BEHAVIOR_EVAL_SET",
                "status": "ACTIVE",
                "model_run_status": "NOT_RUN",
                "source_issue": "https://example.com/1",
                "cases": [
                    behavior_case("SBE-001", "alpha-skill", "beta-skill"),
                    behavior_case("SBE-002", "beta-skill", "alpha-skill"),
                ],
            },
        )
        entries = [
            {
                "skill_id": "alpha-skill",
                "evidence": [
                    {"kind": "TEST", "path": "tests/test_alpha.py"},
                ],
                "pilot_status": "NOT_RUN",
            }
        ]
        if include_beta_entry:
            entries.append(
                {
                    "skill_id": "beta-skill",
                    "evidence": [
                        {"kind": "CONTRACT", "path": "docs/beta.md"},
                    ],
                    "pilot_status": "PARTIAL",
                }
            )
        write_json(
            root / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json",
            {
                "schema_version": 1,
                "artifact_role": "BASE_SKILL_IMPLEMENTATION_EVIDENCE_INDEX",
                "entries": entries,
            },
        )
        for skill_id in ("alpha-skill", "beta-skill"):
            path = root / f"skills/{skill_id}/SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {skill_id}\n\nMode: `run`\n", encoding="utf-8")
        (root / "tests").mkdir(exist_ok=True)
        (root / "tests/test_alpha.py").write_text("# test\n", encoding="utf-8")
        (root / "docs").mkdir(exist_ok=True)
        (root / "docs/beta.md").write_text("# contract\n", encoding="utf-8")
        return directory, root

    def test_missing_active_skill_evidence_entry_fails(self) -> None:
        if not BUILDER_PATH.is_file():
            self.skipTest("builder not implemented yet")
        builder = load_builder()
        directory, root = self.build_root(include_beta_entry=False)
        self.addCleanup(directory.cleanup)

        errors = builder.validate_evidence_index(root)

        self.assertIn("missing evidence index entry: beta-skill", errors)

    def test_markdown_distinguishes_executable_and_contract_evidence(self) -> None:
        if not BUILDER_PATH.is_file():
            self.skipTest("builder not implemented yet")
        builder = load_builder()
        directory, root = self.build_root()
        self.addCleanup(directory.cleanup)

        markdown = builder.build_evidence_markdown(root)

        self.assertIn("`alpha-skill`", markdown)
        self.assertIn("EXECUTABLE_EVIDENCE", markdown)
        self.assertIn("`beta-skill`", markdown)
        self.assertIn("CONTRACT_EVIDENCE", markdown)
        self.assertEqual(1, markdown.count("`alpha-skill`"))
        self.assertEqual(1, markdown.count("`beta-skill`"))

    def test_markdown_binds_behavior_case_count_and_source_digest(self) -> None:
        builder = load_builder()
        directory, root = self.build_root()
        self.addCleanup(directory.cleanup)

        markdown = builder.build_evidence_markdown(root)

        self.assertIn("> Behavior evaluation case count: `2`", markdown)
        self.assertIn(
            f"> Behavior evaluation source SHA-256: `{builder.behavior_source_digest(root)}`",
            markdown,
        )

    def test_behavior_source_digest_is_newline_invariant(self) -> None:
        builder = load_builder()
        directory, root = self.build_root()
        self.addCleanup(directory.cleanup)

        for relative in builder.EVAL_PATHS:
            path = root / relative
            if not path.is_file():
                continue
            lf_bytes = path.read_bytes().replace(b"\r\n", b"\n")
            path.write_bytes(lf_bytes)
        lf_digest = builder.behavior_source_digest(root)

        for relative in builder.EVAL_PATHS:
            path = root / relative
            if not path.is_file():
                continue
            path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        crlf_digest = builder.behavior_source_digest(root)

        self.assertEqual(lf_digest, crlf_digest)

    def test_youtube_skill_has_executable_repository_evidence(self) -> None:
        builder = load_builder()
        self.assertEqual([], builder.validate_evidence_index(ROOT))
        markdown = builder.build_evidence_markdown(ROOT)
        row = next(
            line for line in markdown.splitlines()
            if line.startswith("| `producing-game-development-youtube-videos`")
        )
        self.assertIn("PASS", row)
        self.assertIn("EXECUTABLE_EVIDENCE", row)
        self.assertIn("tests/test_game_development_youtube_skill.py", row)

    def test_checked_in_evidence_is_current(self) -> None:
        if not BUILDER_PATH.is_file() or not GENERATED_PATH.is_file():
            self.skipTest("builder not implemented yet")
        builder = load_builder()

        generated = builder.build_evidence_markdown(ROOT)
        checked_in = GENERATED_PATH.read_text(encoding="utf-8")

        self.assertEqual(generated, checked_in)

    def test_bcp008_existing_owners_have_executable_repository_evidence(self) -> None:
        builder = load_builder()
        self.assertEqual([], builder.validate_evidence_index(ROOT))
        markdown = builder.build_evidence_markdown(ROOT)
        expected = {
            "managing-project-intake-and-work-contract": "tests/test_feature_spec_traceability_contract.py",
            "managing-design-documents": "tests/test_feature_spec_traceability_contract.py",
            "reviewing-and-validating-project-changes": "tests/test_feature_spec_traceability_contract.py",
            "running-adversarial-review-and-refinement": "tests/test_cross_discipline_review_lenses.py",
            "auditing-and-refining-ui-art": "tests/test_bcp008_behavior_and_procurement_pilot.py",
        }
        for skill_id, path in expected.items():
            row = next(line for line in markdown.splitlines() if line.startswith(f"| `{skill_id}`"))
            self.assertIn("EXECUTABLE_EVIDENCE", row)
            self.assertIn(path, row)

    def test_base_change_proposal_candidate_boundary_has_learning_record(self) -> None:
        skill = (ROOT / "skills/managing-base-change-proposals/SKILL.md").read_text(
            encoding="utf-8"
        )
        learning_log = (ROOT / "skills/SKILL_LEARNING_LOG.md").read_text(encoding="utf-8")

        for token in (
            "CANDIDATE_REPORT_IS_NOT_BASE_CANON",
            "COMMON_LESSON_AND_CORRECTION_REQUEST_REQUIRED",
            "MINIMUM_OWNER_CORRECTION_REQUEST",
            "EVIDENCE_CEILING_AND_NONUSE_CONDITIONS",
        ):
            self.assertIn(token, skill)
        self.assertIn(
            "CANDIDATE_REPORT_BOUNDARY_AND_MINIMAL_CORRECTION_REQUEST",
            learning_log,
        )

    def test_serial_fiction_skill_has_executable_repository_evidence(self) -> None:
        builder = load_builder()
        self.assertEqual([], builder.validate_evidence_index(ROOT))
        markdown = builder.build_evidence_markdown(ROOT)
        row = next(
            line for line in markdown.splitlines()
            if line.startswith("| `developing-and-revising-serial-fiction`")
        )
        self.assertIn("PASS", row)
        self.assertIn("EXECUTABLE_EVIDENCE", row)
        self.assertIn("tests/test_serial_fiction_discipline.py", row)


class ReviewEvidenceExecutionIntegrationTests(unittest.TestCase):
    def test_review_checker_runs_against_exact_git_state_and_refuses_not_run(self) -> None:
        checker = load_review_checker()
        self.assertTrue(checker.matches("src/file.py", ["src/*.py"]))
        self.assertFalse(checker.matches("src/nested/file.py", ["src/*.py"]))

        record_schema = json.loads(REVIEW_RECORD_SCHEMA.read_text(encoding="utf-8"))
        result_schema = json.loads(REVIEW_RESULT_SCHEMA.read_text(encoding="utf-8"))
        template = json.loads(REVIEW_TEMPLATE.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(record_schema)
        Draft202012Validator.check_schema(result_schema)
        Draft202012Validator(record_schema).validate(template)

        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)

        def git(*arguments: str) -> str:
            completed = subprocess.run(
                ["git", *arguments],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            return completed.stdout.strip()

        git("init", "-b", "main")
        git("config", "user.email", "review@example.invalid")
        git("config", "user.name", "Review Evidence Test")
        contract_root = root / "skills/reviewing-and-validating-project-changes/contracts"
        contract_root.mkdir(parents=True)
        (contract_root / "review-record.schema.json").write_text(
            REVIEW_RECORD_SCHEMA.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (contract_root / "review-result.schema.json").write_text(
            REVIEW_RESULT_SCHEMA.read_text(encoding="utf-8"), encoding="utf-8"
        )
        (root / "src").mkdir()
        (root / "src/feature.txt").write_text("old\n", encoding="utf-8")
        git("add", ".")
        git("commit", "-m", "baseline")
        base_sha = git("rev-parse", "HEAD")

        record = {
            "schema_version": 1,
            "artifact_role": "REVIEW_EVIDENCE_RECORD",
            "scope": {
                "allowed_changed_paths": ["records/review.json", "src/feature.txt"],
                "protected_paths": [],
            },
            "claims": [
                {
                    "claim_id": "CLAIM-001",
                    "claim_type": "IMPLEMENTATION",
                    "claim_text": "The approved feature is implemented.",
                    "acceptance_ids": ["AC-001"],
                    "check_ids": ["CHECK-001"],
                }
            ],
            "acceptance": [
                {
                    "intent_id": "AC-001",
                    "approved_intent": "The implemented marker is present.",
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
        record_path = root / "records/review.json"
        write_json(record_path, record)
        (root / "src/feature.txt").write_text("implemented\n", encoding="utf-8")
        git("add", ".")
        git("commit", "-m", "feature")
        head_sha = git("rev-parse", "HEAD")

        result, errors = checker.check_record(
            root,
            record_path,
            base_sha,
            execute_checks=True,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertEqual([], errors)
        self.assertEqual("PASS", result["final_status"])
        self.assertEqual(base_sha, result["subject"]["base_sha"])
        self.assertEqual(head_sha, result["subject"]["head_sha"])
        self.assertEqual("PASS", result["gates"]["implementation"]["status"])
        self.assertEqual("PASS", result["gates"]["verification"]["status"])
        self.assertEqual("PASS", result["gates"]["intent"]["status"])
        self.assertEqual(
            "BLOCKED_UNVERIFIED",
            result["gates"]["integration"]["status"],
        )

        not_run, not_run_errors = checker.check_record(
            root,
            record_path,
            base_sha,
            execute_checks=False,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertEqual("FAIL", not_run["final_status"])
        self.assertEqual("NOT_RUN", not_run["gates"]["verification"]["status"])
        self.assertTrue(
            any("not executed" in message for message in not_run_errors),
            not_run_errors,
        )

        record["checks"][0]["argv"] = [
            "{python}",
            "-c",
            (
                "from pathlib import Path; "
                "Path('src/feature.txt').write_text('mutated\\n', encoding='utf-8'); "
                "print('REVIEW_CHECK: PASS')"
            ),
        ]
        write_json(record_path, record)
        git("add", "records/review.json")
        git("commit", "-m", "mutation check")
        mutated, mutation_errors = checker.check_record(
            root,
            record_path,
            base_sha,
            execute_checks=True,
            allowed_programs=(),
            approved_levels={},
        )
        self.assertEqual("FAIL", mutated["final_status"])
        self.assertTrue(
            any("repository state changed during checks" in message for message in mutation_errors),
            mutation_errors,
        )


class ClaimIntentImplementationEvidenceIntegrationTests(unittest.TestCase):
    def test_repository_projection_coverage_is_bound_to_generated_evidence(self) -> None:
        coverage = json.loads(
            (ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")
        )
        case = next(item for item in coverage["cases"] if item["case_id"] == "SBE-031")
        self.assertIn("repository human projection", case["prompt"])
        self.assertIn("exact-SHA destination readback", case["required_evidence"])
        markdown = load_builder().build_evidence_markdown(ROOT)
        self.assertIn(
            f"> Behavior evaluation source SHA-256: `{load_builder().behavior_source_digest(ROOT)}`",
            markdown,
        )

    def test_claim_intent_contract_is_linked_without_claiming_a_model_run(self) -> None:
        index = json.loads((ROOT / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json").read_text(encoding="utf-8"))
        owner = next(entry for entry in index["entries"] if entry["skill_id"] == "reviewing-and-validating-project-changes")
        self.assertIn(
            {"kind": "TEST", "path": "tests/test_claim_and_intent_verification_contract.py"},
            owner["evidence"],
        )
        markdown = load_builder().build_evidence_markdown(ROOT)
        self.assertIn("External model behavior run: `NOT_RUN`", markdown)
        owner_line = next(line for line in markdown.splitlines() if line.startswith("| `reviewing-and-validating-project-changes`"))
        self.assertIn("EXECUTABLE_EVIDENCE", owner_line)
        self.assertIn("tests/test_claim_and_intent_verification_contract.py", owner_line)

    def test_github_connector_fallback_has_executable_evidence(self) -> None:
        index = json.loads((ROOT / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json").read_text(encoding="utf-8"))
        owner = next(
            entry
            for entry in index["entries"]
            if entry["skill_id"] == "synchronizing-local-and-github-state"
        )
        self.assertIn(
            {"kind": "TEST", "path": "tests/test_github_connector_fallback_policy.py"},
            owner["evidence"],
        )
        owner_line = next(
            line
            for line in load_builder().build_evidence_markdown(ROOT).splitlines()
            if line.startswith("| `synchronizing-local-and-github-state`")
        )
        self.assertIn("EXECUTABLE_EVIDENCE", owner_line)
        self.assertIn("tests/test_github_connector_fallback_policy.py", owner_line)


if __name__ == "__main__":
    unittest.main()
