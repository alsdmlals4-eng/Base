from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_skill_behavior_evals.py"
BUILDER_PATH = ROOT / "tools/build_skill_implementation_evidence.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_skill_behavior_evals", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_builder():
    spec = importlib.util.spec_from_file_location(
        "build_skill_implementation_evidence", BUILDER_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluation_digest(root: Path) -> str:
    hasher = hashlib.sha256()
    for relative in (
        "skills/SKILL_BEHAVIOR_EVALS.json",
        "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json",
    ):
        path = root / relative
        if not path.is_file():
            continue
        hasher.update(relative.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def minimal_eval_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["schema_version", "artifact_role", "status", "model_run_status", "cases"],
        "properties": {
            "schema_version": {"const": 1},
            "artifact_role": {"type": "string"},
            "status": {"type": "string"},
            "model_run_status": {"type": "string"},
            "cases": {"type": "array", "items": {"type": "object"}},
        },
    }


def minimal_result_schema() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version",
            "artifact_role",
            "run_status",
            "repository",
            "commit_sha",
            "generated_at",
            "model",
            "source_identity",
            "review",
            "results",
        ],
        "properties": {
            "schema_version": {"const": 1},
            "artifact_role": {"const": "BASE_SKILL_BEHAVIOR_RESULTS"},
            "run_status": {"enum": ["NOT_RUN", "COMPLETED"]},
            "repository": {"const": "alsdmlals4-eng/Base"},
            "commit_sha": {"type": "string", "pattern": "^[0-9a-f]{40}$"},
            "generated_at": {"type": "string"},
            "model": {
                "type": "object",
                "required": ["provider", "model", "version"],
                "properties": {
                    "provider": {"type": "string"},
                    "model": {"type": "string"},
                    "version": {"type": "string"},
                    "reasoning": {"type": "string"},
                },
            },
            "source_identity": {
                "type": "object",
                "required": [
                    "registry_path",
                    "registry_sha256",
                    "evaluation_paths",
                    "evaluation_sha256",
                ],
                "properties": {
                    "registry_path": {"const": "skills/SKILL_REGISTRY.json"},
                    "registry_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                    "evaluation_paths": {"type": "array", "items": {"type": "string"}},
                    "evaluation_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
                },
            },
            "review": {
                "type": "object",
                "required": [
                    "author_context_id",
                    "reviewer_context_id",
                    "independent",
                    "author_summary_visible",
                ],
                "properties": {
                    "author_context_id": {"type": "string"},
                    "reviewer_context_id": {"type": "string"},
                    "independent": {"type": "boolean"},
                    "author_summary_visible": {"type": "boolean"},
                },
            },
            "results": {"type": "array", "items": {"type": "object"}},
        },
    }


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


def behavior_case(
    case_id: str,
    primary: str,
    forbidden: list[str],
    case_type: str,
) -> dict:
    return {
        "case_id": case_id,
        "case_type": case_type,
        "prompt": f"Concrete request number {case_id[-3:]} without routing labels.",
        "expected_work_mode": "PLAN",
        "expected_primary_skill": primary,
        "expected_supporting_skills": [],
        "expected_skill_modes": ["run"],
        "forbidden_skills": forbidden,
        "required_evidence": ["evidence"],
        "expected_user_decision_state": "NOT_REQUIRED",
        "rationale": "Focused test fixture.",
    }


def complete_cases() -> list[dict]:
    case_types = ["positive", "negative", "boundary", "cross-skill"]
    cases: list[dict] = []
    for index in range(8):
        primary = "alpha-skill" if index % 2 == 0 else "beta-skill"
        forbidden = ["beta-skill"] if primary == "alpha-skill" else ["alpha-skill"]
        cases.append(
            behavior_case(
                f"CASE-{index + 1:03d}",
                primary,
                forbidden,
                case_types[index % len(case_types)],
            )
        )
    return cases


def expected_results(cases: list[dict]) -> list[dict]:
    return [
        {
            "case_id": case["case_id"],
            "work_mode": case["expected_work_mode"],
            "primary_skill": case["expected_primary_skill"],
            "supporting_skills": case["expected_supporting_skills"],
            "skill_modes": case["expected_skill_modes"],
            "evidence": case["required_evidence"],
            "user_decision_state": case["expected_user_decision_state"],
            "notes": "test",
        }
        for case in cases
    ]


class SkillBehaviorCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = load_checker()
        self.builder = load_builder()

    def build_root(
        self,
        cases: list[dict],
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
                "cases": cases,
            },
        )
        write_json(root / "schemas/skill-behavior-eval-v1.schema.json", minimal_eval_schema())
        write_json(root / "schemas/skill-behavior-results-v1.schema.json", minimal_result_schema())
        for skill_id in ("alpha-skill", "beta-skill"):
            path = root / f"skills/{skill_id}/SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {skill_id}\n\nMode: `run`\n", encoding="utf-8")
        return directory, root

    @staticmethod
    def initialize_git(root: Path) -> str:
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=root, check=True, capture_output=True)
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()

    def valid_result_document(self, root: Path, cases: list[dict], commit_sha: str) -> dict:
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
                "registry_sha256": digest(root / "skills/SKILL_REGISTRY.json"),
                "evaluation_paths": ["skills/SKILL_BEHAVIOR_EVALS.json"],
                "evaluation_sha256": evaluation_digest(root),
            },
            "review": {
                "author_context_id": "author-context",
                "reviewer_context_id": "reviewer-context",
                "independent": True,
                "author_summary_visible": False,
            },
            "results": expected_results(cases),
        }

    def test_contract_rejects_active_skill_without_primary_case(self) -> None:
        cases = complete_cases()
        for case in cases:
            case["expected_primary_skill"] = "alpha-skill"
            case["forbidden_skills"] = ["beta-skill"]
        directory, root = self.build_root(cases)
        self.addCleanup(directory.cleanup)

        errors = self.checker.validate_contract(root)

        self.assertIn("beta-skill: missing primary behavior coverage", errors)

    def test_contract_rejects_active_skill_without_non_selection_case(self) -> None:
        cases = complete_cases()
        for case in cases:
            case["forbidden_skills"] = [
                skill_id for skill_id in case["forbidden_skills"] if skill_id != "alpha-skill"
            ]
        directory, root = self.build_root(cases)
        self.addCleanup(directory.cleanup)

        errors = self.checker.validate_contract(root)

        self.assertIn("alpha-skill: missing non-selection behavior coverage", errors)

    def test_complete_primary_and_non_selection_coverage_passes(self) -> None:
        directory, root = self.build_root(complete_cases())
        self.addCleanup(directory.cleanup)

        errors = self.checker.validate_contract(root)

        self.assertEqual([], errors)

    def test_implementation_digest_ignores_checkout_newlines(self) -> None:
        directory, root = self.build_root(complete_cases())
        self.addCleanup(directory.cleanup)
        path = root / "skills/SKILL_BEHAVIOR_EVALS.json"
        path.write_bytes(path.read_bytes().replace(b"\r\n", b"\n"))
        lf_digest = self.builder.behavior_source_digest(root)

        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))

        self.assertEqual(lf_digest, self.builder.behavior_source_digest(root))

    def test_result_rejects_stale_registry_hash(self) -> None:
        cases = complete_cases()
        directory, root = self.build_root(cases)
        self.addCleanup(directory.cleanup)
        commit_sha = self.initialize_git(root)
        result = self.valid_result_document(root, cases, commit_sha)
        result["source_identity"]["registry_sha256"] = "0" * 64
        result_path = root / "result.json"
        write_json(result_path, result)

        errors = self.checker.score_results(root, result_path)

        self.assertIn("result registry SHA-256 does not match current source", errors)

    def test_result_rejects_stale_evaluation_hash(self) -> None:
        cases = complete_cases()
        directory, root = self.build_root(cases)
        self.addCleanup(directory.cleanup)
        commit_sha = self.initialize_git(root)
        result = self.valid_result_document(root, cases, commit_sha)
        result["source_identity"]["evaluation_sha256"] = "0" * 64
        result_path = root / "result.json"
        write_json(result_path, result)

        errors = self.checker.score_results(root, result_path)

        self.assertIn("result evaluation SHA-256 does not match current source", errors)

    def test_current_youtube_skill_has_primary_and_non_selection_coverage(self) -> None:
        evals = self.checker.load_eval_set(ROOT)
        primary = [
            case for case in evals["cases"]
            if case["expected_primary_skill"] == "producing-game-development-youtube-videos"
        ]
        forbidden = [
            case for case in evals["cases"]
            if "producing-game-development-youtube-videos" in case["forbidden_skills"]
        ]
        self.assertGreaterEqual(len(primary), 3)
        self.assertGreaterEqual(len(forbidden), 2)
        self.assertEqual([], self.checker.validate_contract(ROOT))

    def test_result_rejects_non_independent_review_context(self) -> None:
        cases = complete_cases()
        directory, root = self.build_root(cases)
        self.addCleanup(directory.cleanup)
        commit_sha = self.initialize_git(root)
        result = self.valid_result_document(root, cases, commit_sha)
        result["review"]["reviewer_context_id"] = result["review"]["author_context_id"]
        result_path = root / "result.json"
        write_json(result_path, result)

        errors = self.checker.score_results(root, result_path)

        self.assertIn("result review context is not independent", errors)

    def test_bcp008_cases_add_positive_negative_and_fail_closed_pressure(self) -> None:
        evals = self.checker.load_eval_set(ROOT)
        cases = {case["case_id"]: case for case in evals["cases"]}
        self.assertTrue({"SBE-901", "SBE-902", "SBE-903", "SBE-904"}.issubset(cases))
        self.assertEqual(
            "managing-project-intake-and-work-contract",
            cases["SBE-901"]["expected_primary_skill"],
        )
        self.assertEqual("negative", cases["SBE-902"]["case_type"])
        self.assertIn("auditing-and-refining-ui-art", cases["SBE-903"]["expected_supporting_skills"])
        self.assertIn("auditing-and-refining-ui-art", cases["SBE-904"]["forbidden_skills"])
        self.assertEqual("NOT_RUN", evals["model_run_status"])
        self.assertEqual([], self.checker.validate_contract(ROOT))


    def test_serial_fiction_skill_has_primary_and_non_selection_coverage(self) -> None:
        evals = self.checker.load_eval_set(ROOT)
        primary = [
            case for case in evals["cases"]
            if case["expected_primary_skill"] == "developing-and-revising-serial-fiction"
        ]
        forbidden = [
            case for case in evals["cases"]
            if "developing-and-revising-serial-fiction" in case["forbidden_skills"]
        ]
        self.assertGreaterEqual(len(primary), 1)
        self.assertGreaterEqual(len(forbidden), 1)
        self.assertEqual([], self.checker.validate_contract(ROOT))


class ClaimIntentBehaviorEvidenceHardeningTests(unittest.TestCase):
    def test_sbe_038_is_unique_fail_closed_and_not_model_run(self) -> None:
        documents = [
            json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")),
        ]
        cases = [case for document in documents for case in document["cases"] if case["case_id"] == "SBE-038"]
        self.assertEqual(1, len(cases))
        case = cases[0]
        self.assertEqual("REVIEW", case["expected_work_mode"])
        self.assertEqual("reviewing-and-validating-project-changes", case["expected_primary_skill"])
        self.assertIn("claim-and-intent-verification", case["expected_skill_modes"])
        required = chr(10).join(case["required_evidence"])
        for token in ("exact-ref", "실제 diff", "미검증", "main readback"):
            self.assertIn(token, required)
        self.assertEqual("NOT_RUN", documents[0]["model_run_status"])

    def test_sbe_039_is_unique_capability_driven_and_not_model_run(self) -> None:
        documents = [
            json.loads((ROOT / "skills/SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8")),
            json.loads((ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")),
        ]
        cases = [
            case
            for document in documents
            for case in document["cases"]
            if case["case_id"] == "SBE-039"
        ]
        self.assertEqual(1, len(cases))
        case = cases[0]
        self.assertEqual("synchronizing-local-and-github-state", case["expected_primary_skill"])
        self.assertEqual(["recover", "publish", "verify"], case["expected_skill_modes"])
        required = chr(10).join(case["required_evidence"])
        for token in (
            "GITHUB_CAPABILITY_FALLBACK",
            "CONCURRENT_CHANGE_PREFLIGHT",
            "expected HEAD",
            "force=false",
            "post-merge",
        ):
            self.assertIn(token, required)
        self.assertEqual("NOT_RUN", documents[0]["model_run_status"])

    def test_sbe_031_requires_repository_projection_evidence(self) -> None:
        coverage = json.loads(
            (ROOT / "skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8")
        )
        case = next(item for item in coverage["cases"] if item["case_id"] == "SBE-031")
        self.assertEqual("building-project-visual-dashboards", case["expected_primary_skill"])
        self.assertIn("repository human projection", case["prompt"])
        self.assertIn("exact-SHA destination readback", case["required_evidence"])


if __name__ == "__main__":
    unittest.main()
