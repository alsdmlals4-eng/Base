from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_skill_behavior_evals.py"
BUILDER_PATH = ROOT / "tools/build_skill_implementation_evidence.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def copy_contract_files(root: Path) -> None:
    for relative in (
        "schemas/skill-behavior-eval-v1.schema.json",
        "schemas/skill-behavior-results-v1.schema.json",
    ):
        source = ROOT / relative
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


def active_skill(skill_id: str) -> dict:
    return {
        "skill_id": skill_id,
        "layer": "specialist",
        "discipline": "test",
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


def behavior_case(case_id: str, primary: str, forbidden: str, case_type: str) -> dict:
    return {
        "case_id": case_id,
        "case_type": case_type,
        "prompt": f"Concrete metadata boundary request {case_id} without routing labels.",
        "expected_work_mode": "PLAN",
        "expected_primary_skill": primary,
        "expected_supporting_skills": [],
        "expected_skill_modes": ["run"],
        "forbidden_skills": [forbidden],
        "required_evidence": ["evidence"],
        "expected_user_decision_state": "NOT_REQUIRED",
        "rationale": "Focused adversarial boundary fixture.",
    }


def cases() -> list[dict]:
    kinds = ["positive", "negative", "boundary", "cross-skill"]
    values = []
    for index in range(16):
        primary = "alpha-skill" if index % 2 == 0 else "beta-skill"
        forbidden = "beta-skill" if primary == "alpha-skill" else "alpha-skill"
        values.append(behavior_case(f"SBE-{index + 1:03d}", primary, forbidden, kinds[index % 4]))
    return values


class SkillBehaviorAdversarialBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = load_module("check_skill_behavior_evals", CHECKER_PATH)
        self.builder = load_module("build_skill_implementation_evidence", BUILDER_PATH)
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        copy_contract_files(self.root)
        write_json(
            self.root / "skills/SKILL_REGISTRY.json",
            {
                "schema_version": 1,
                "registry_role": "test",
                "routing_policy": {},
                "skills": [active_skill("alpha-skill"), active_skill("beta-skill")],
            },
        )
        write_json(
            self.root / "skills/SKILL_BEHAVIOR_EVALS.json",
            {
                "schema_version": 1,
                "artifact_role": "BASE_SKILL_BEHAVIOR_EVAL_SET",
                "status": "ACTIVE",
                "model_run_status": "NOT_RUN",
                "source_issue": "https://example.com/core",
                "cases": cases()[:8],
            },
        )
        write_json(
            self.root / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json",
            {
                "schema_version": 1,
                "artifact_role": "BASE_SKILL_BEHAVIOR_EVAL_SET",
                "status": "ACTIVE",
                "model_run_status": "NOT_RUN",
                "source_issue": "https://example.com/coverage",
                "cases": cases()[8:],
            },
        )
        for skill_id in ("alpha-skill", "beta-skill"):
            path = self.root / f"skills/{skill_id}/SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {skill_id}\n\nMode: `run`\n", encoding="utf-8")

    def initialize_git(self) -> str:
        subprocess.run(["git", "init"], cwd=self.root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=self.root, check=True, capture_output=True)
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def result_document(self, commit_sha: str) -> dict:
        evals = self.checker.load_eval_set(self.root)
        return {
            "schema_version": 1,
            "artifact_role": "BASE_SKILL_BEHAVIOR_RESULTS",
            "run_status": "COMPLETED",
            "repository": "alsdmlals4-eng/Base",
            "commit_sha": commit_sha,
            "generated_at": "2026-08-02T00:00:00Z",
            "model": {
                "provider": "test-provider",
                "model": "test-model",
                "version": "1",
                "reasoning": "test",
            },
            "source_identity": {
                "registry_path": "skills/SKILL_REGISTRY.json",
                "registry_sha256": self.checker.file_sha256(self.root / "skills/SKILL_REGISTRY.json"),
                "evaluation_paths": [path.as_posix() for path in self.checker.evaluation_paths(self.root)],
                "evaluation_sha256": self.checker.evaluation_sha256(self.root),
            },
            "review": {
                "author_context_id": "author-context",
                "reviewer_context_id": "reviewer-context",
                "independent": True,
                "author_summary_visible": False,
            },
            "results": [
                {
                    "case_id": case["case_id"],
                    "work_mode": case["expected_work_mode"],
                    "primary_skill": case["expected_primary_skill"],
                    "supporting_skills": case["expected_supporting_skills"],
                    "skill_modes": case["expected_skill_modes"],
                    "evidence": case["required_evidence"],
                    "user_decision_state": case["expected_user_decision_state"],
                }
                for case in evals["cases"]
            ],
        }

    def test_coverage_document_metadata_is_validated_independently(self) -> None:
        coverage_path = self.root / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json"
        coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
        coverage["artifact_role"] = "WRONG_ROLE"
        write_json(coverage_path, coverage)

        errors = self.checker.validate_contract(self.root)

        self.assertTrue(
            any("SKILL_BEHAVIOR_COVERAGE_EVALS.json" in error and "artifact_role" in error for error in errors),
            errors,
        )

    def test_completed_result_rejects_placeholder_model_metadata(self) -> None:
        commit_sha = self.initialize_git()
        result = self.result_document(commit_sha)
        result["model"]["provider"] = "UNSET"
        result_path = self.root / "result.json"
        write_json(result_path, result)

        errors = self.checker.score_results(self.root, result_path)

        self.assertIn("completed result contains placeholder model metadata", errors)

    def test_completed_result_rejects_invalid_generated_timestamp(self) -> None:
        commit_sha = self.initialize_git()
        result = self.result_document(commit_sha)
        result["generated_at"] = "not-a-date"
        result_path = self.root / "result.json"
        write_json(result_path, result)

        errors = self.checker.score_results(self.root, result_path)

        self.assertTrue(any("generated_at" in error for error in errors), errors)

    def test_current_youtube_adversarial_cases_block_overclaim_and_small_sample(self) -> None:
        coverage = json.loads(
            (ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")
        )
        cases = {case["case_id"]: case for case in coverage["cases"]}
        publication = cases["SBE-036"]
        self.assertEqual("producing-game-development-youtube-videos", publication["expected_primary_skill"] )
        self.assertIn("BLOCKED_UNVERIFIED", publication["required_evidence"] )
        self.assertIn("RIGHTS_OR_RATING_UNVERIFIED", publication["required_evidence"] )
        analytics = cases["SBE-037"]
        self.assertIn("INSUFFICIENT_SAMPLE", analytics["required_evidence"] )
        self.assertIn("CONVERSION_UNVERIFIED", analytics["required_evidence"] )

    def test_evidence_index_metadata_is_validated(self) -> None:
        write_json(
            self.root / "skills/SKILL_IMPLEMENTATION_EVIDENCE.json",
            {
                "schema_version": 1,
                "artifact_role": "WRONG_ROLE",
                "entries": [
                    {
                        "skill_id": "alpha-skill",
                        "evidence": [
                            {"kind": "CONTRACT", "path": "skills/alpha-skill/SKILL.md"}
                        ],
                    },
                    {
                        "skill_id": "beta-skill",
                        "evidence": [
                            {"kind": "CONTRACT", "path": "skills/beta-skill/SKILL.md"}
                        ],
                    },
                ],
            },
        )

        errors = self.builder.validate_evidence_index(self.root)

        self.assertIn(
            "evidence index artifact_role must be BASE_SKILL_IMPLEMENTATION_EVIDENCE_INDEX",
            errors,
        )

    def test_implementation_digest_ignores_newlines_but_not_semantic_changes(self) -> None:
        path = self.root / "skills/SKILL_BEHAVIOR_EVALS.json"
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
        baseline = self.builder.behavior_source_digest(self.root)

        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.assertEqual(baseline, self.builder.behavior_source_digest(self.root))

        path.write_bytes(
            path.read_bytes().replace(b'"model_run_status": "NOT_RUN"', b'"model_run_status": "COMPLETED"')
        )
        self.assertNotEqual(baseline, self.builder.behavior_source_digest(self.root))

    def test_bcp008_procurement_cases_block_platform_mismatch_and_overclaim(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        cases = {case["case_id"]: case for case in evals["cases"]}
        web = cases["SBE-903"]
        self.assertIn("BLOCKED_UNVERIFIED", web["required_evidence"])
        self.assertIn("external UI procurement receipt", web["required_evidence"])
        godot = cases["SBE-904"]
        self.assertIn("auditing-and-refining-ui-art", godot["forbidden_skills"])
        self.assertIn("Godot", godot["prompt"])


    def test_serial_fiction_cases_preserve_nonselection_and_evidence_boundaries(self) -> None:
        primary = json.loads(
            (ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8")
        )
        coverage = json.loads(
            (ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")
        )
        primary_cases = {case["case_id"]: case for case in primary["cases"]}
        coverage_cases = {case["case_id"]: case for case in coverage["cases"]}
        fiction = primary_cases["SBE-950"]
        self.assertEqual("developing-and-revising-serial-fiction", fiction["expected_primary_skill"])
        self.assertIn("Episode Value", fiction["required_evidence"])
        game = coverage_cases["SBE-951"]
        self.assertEqual("analyzing-and-refining-game-concepts", game["expected_primary_skill"])
        self.assertIn("developing-and-revising-serial-fiction", game["forbidden_skills"])


class ClaimIntentAdversarialBoundaryTests(unittest.TestCase):
    def test_sbe_040_and_041_reject_fast_completion_and_open_pr_mutation(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        cases = {case["case_id"]: case for case in evals["cases"]}
        deliberate = "\n".join(cases["SBE-040"]["required_evidence"])
        continuation = "\n".join(cases["SBE-041"]["required_evidence"])
        for token in ("인터넷 원출처", "최소 3개", "Tool 실행", "5회", "NOT_RUN"):
            self.assertIn(token, deliberate)
        for token in ("exact main SHA", "새 Branch/PR", "destination", "남은 필수 작업"):
            self.assertIn(token, continuation)

    def test_sbe_038_rejects_search_producer_and_stale_sha_shortcuts(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        case = next(case for case in evals["cases"] if case["case_id"] == "SBE-038")
        prompt = case["prompt"]
        required = chr(10).join(case["required_evidence"])
        for token in ("검색 결과", "작업자 설명", "merge SHA", "main readback"):
            self.assertIn(token, prompt + chr(10) + required)
        for token in ("exact-ref", "exact HEAD", "CLAIM_UNVERIFIED", "IMPLEMENTATION_UNVERIFIED"):
            self.assertIn(token, required)
        self.assertEqual("NOT_REQUIRED", case["expected_user_decision_state"])
        self.assertTrue(case["forbidden_skills"])

    def test_sbe_039_rejects_optional_cli_and_stale_sha_shortcuts(self) -> None:
        evals = json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        case = next(case for case in evals["cases"] if case["case_id"] == "SBE-039")
        prompt = case["prompt"]
        required = chr(10).join(case["required_evidence"])
        for token in ("gh가 설치되어 있지", "재인증을 요구하지", "연결된 GitHub 플러그인"):
            self.assertIn(token, prompt)
        for token in ("CONCURRENT_CHANGE_PREFLIGHT", "exact write parent", "force=false", "Required Checks"):
            self.assertIn(token, required)
        self.assertEqual("NOT_REQUIRED", case["expected_user_decision_state"])


if __name__ == "__main__":
    unittest.main()
