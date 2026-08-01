from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "skills" / "SKILL_REGISTRY.json"
EVALS = ROOT / "skills" / "SKILL_BEHAVIOR_EVALS.json"
SCHEMA = ROOT / "schemas" / "skill-behavior-eval-v1.schema.json"
CHECKER = ROOT / "tools" / "check_skill_behavior_evals.py"
EXPECTED_V94_REGISTRY_SHA256 = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def active_skill_entries() -> list[dict]:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return [entry for entry in data["skills"] if entry["status"] == "ACTIVE"]


def frontmatter_description(path: Path) -> str:
    match = re.search(r"^description:\s*([^\n]+?)\s*$", path.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip("'\"")


def valid_model_results() -> dict:
    evals = json.loads(EVALS.read_text(encoding="utf-8"))
    return {
        "schema_version": 1,
        "results": [
            {
                "case_id": case["case_id"],
                "work_mode": case["expected_work_mode"],
                "primary_skill": case["expected_primary_skill"],
                "supporting_skills": list(case["expected_supporting_skills"]),
                "skill_modes": list(case["expected_skill_modes"]),
                "evidence": list(case["required_evidence"]),
                "user_decision_state": case["expected_user_decision_state"],
            }
            for case in evals["cases"]
        ],
    }


def run_checker(results: dict | list, *, root: Path = ROOT) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        result_path = Path(directory) / "results.json"
        result_path.write_text(json.dumps(results, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(root), "--results", str(result_path)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )


class BaseV95SkillOperatingRefinementTests(unittest.TestCase):
    maxDiff = None

    def test_released_v94_registry_identity_is_unchanged(self) -> None:
        self.assertEqual(EXPECTED_V94_REGISTRY_SHA256, hashlib.sha256(REGISTRY.read_bytes()).hexdigest())
        lock = json.loads((ROOT / "base-v9.4.lock.json").read_text(encoding="utf-8"))
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(EXPECTED_V94_REGISTRY_SHA256, lock["candidate_registry"]["sha256"])

    def test_active_skill_discovery_metadata_fits_the_shared_budget(self) -> None:
        total = 0
        for entry in active_skill_entries():
            description = frontmatter_description(ROOT / entry["path"])
            self.assertTrue(description.startswith("Use when"), entry["skill_id"])
            total += len(entry["skill_id"]) + len(description) + len(entry["path"])
        self.assertLessEqual(total, 8000, f"active Skill discovery metadata uses {total} characters")

    def test_behavior_eval_contract_has_realistic_coverage(self) -> None:
        self.assertTrue(SCHEMA.is_file(), "behavior-eval schema is missing")
        self.assertTrue(EVALS.is_file(), "behavior-eval fixture is missing")
        data = json.loads(EVALS.read_text(encoding="utf-8"))
        cases = data["cases"]
        self.assertGreaterEqual(len(cases), 8)
        self.assertEqual({"positive", "negative", "boundary", "cross-skill"}, {case["case_type"] for case in cases})
        active_ids = {entry["skill_id"] for entry in active_skill_entries()}
        prompts: set[str] = set()
        for case in cases:
            self.assertNotIn(case["prompt"], prompts)
            prompts.add(case["prompt"])
            self.assertNotRegex(case["prompt"], r"managing-|reviewing-|auditing-|evolving-|Skill Mode")
            self.assertIn(case["expected_primary_skill"], active_ids)
            self.assertTrue(set(case["expected_supporting_skills"]).issubset(active_ids))
            self.assertTrue(set(case["forbidden_skills"]).issubset(active_ids))
            self.assertTrue(case["required_evidence"])

    def test_behavior_eval_checker_validates_contract_and_reports_model_not_run(self) -> None:
        self.assertTrue(CHECKER.is_file(), "behavior-eval checker is missing")
        result = subprocess.run(
            [sys.executable, str(CHECKER)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("CONTRACT_STATUS: PASS", result.stdout)
        self.assertIn("MODEL_RUN_STATUS: NOT_RUN", result.stdout)

    def test_behavior_eval_checker_rejects_non_object_result_documents_without_traceback(self) -> None:
        result = run_checker([])
        self.assertNotEqual(0, result.returncode)
        self.assertIn("MODEL_RUN_STATUS: FAIL", result.stdout)
        self.assertIn("result document must be an object", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_behavior_eval_checker_rejects_non_string_collection_items_without_traceback(self) -> None:
        for field in ("supporting_skills", "skill_modes"):
            with self.subTest(field=field):
                results = valid_model_results()
                results["results"][0][field] = [{}]
                result = run_checker(results)
                self.assertNotEqual(0, result.returncode)
                self.assertIn(f"{field} must contain only strings", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_behavior_eval_fixture_cannot_claim_a_model_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "skills", root / "skills")
            (root / "schemas").mkdir()
            shutil.copy2(SCHEMA, root / "schemas" / SCHEMA.name)
            evals = json.loads((root / "skills" / EVALS.name).read_text(encoding="utf-8"))
            evals["model_run_status"] = "PASSED"
            (root / "skills" / EVALS.name).write_text(
                json.dumps(evals, ensure_ascii=False), encoding="utf-8"
            )
            result = subprocess.run(
                [sys.executable, str(CHECKER), "--root", str(root)],
                cwd=ROOT,
                text=True,
                encoding="utf-8",
                capture_output=True,
                check=False,
            )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("CONTRACT_STATUS: FAIL", result.stdout)
        self.assertIn("model_run_status", result.stdout)

    def test_behavior_eval_checker_rejects_each_routing_and_evidence_mismatch(self) -> None:
        evals = json.loads(EVALS.read_text(encoding="utf-8"))
        first = evals["cases"][0]
        mutations = {
            "wrong Work Mode": lambda item: item.update(work_mode="BUILD"),
            "wrong primary Skill": lambda item: item.update(primary_skill="creating-user-learning-notes"),
            "forbidden Skills selected": lambda item: item["supporting_skills"].append(first["forbidden_skills"][0]),
            "missing required evidence": lambda item: item.update(evidence=[]),
        }
        for expected_error, mutate in mutations.items():
            with self.subTest(expected_error=expected_error):
                results = valid_model_results()
                mutate(results["results"][0])
                result = run_checker(results)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("MODEL_RUN_STATUS: FAIL", result.stdout)
                self.assertIn(expected_error, result.stdout)

    def test_issue_74_contract_is_integrated_without_a_new_broad_skill(self) -> None:
        decomposition = read("skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md")
        review = read("skills/reviewing-and-validating-project-changes/SKILL.md")
        evolution = read("skills/evolving-project-discipline-skills/SKILL.md")
        report = read("templates/project-operations/SKILL_EXECUTION_REPORT.md")
        for term in (
            "Build-Measure-Learn",
            "minimum_test_unit",
            "observation_method",
            "success_threshold",
            "failure_threshold",
            "KEEP / REVISE / REDUCE / REMOVE / RETEST",
            "element_purpose",
            "integration_interface",
        ):
            self.assertIn(term, decomposition)
        for term in (
            "Simplify",
            "Style Guide",
            "Domain Review",
            "Security/Safety/Trust Boundary",
            "Golden Path",
            "Edge",
            "Regression",
        ):
            self.assertIn(term, review)
        self.assertIn("behavior-eval", evolution)
        self.assertIn("Base 공용 후보", report)
        self.assertIn("프로젝트 전용", report)

    def test_active_skill_count_is_observational_not_a_fixed_limit(self) -> None:
        readme = read("README.md")
        evolution = read("skills/evolving-project-discipline-skills/SKILL.md")
        self.assertIn("활성 Skill 수는 Registry 관찰값이며 설계 제약이 아니다", readme)
        self.assertIn("활성 Skill 개수는 고정 목표나 상한이 아니다", evolution)
        self.assertIn("독립 입력·산출물·Quality Bar·검증·승인 경계", evolution)

    def test_authority_and_release_history_are_unambiguous(self) -> None:
        version = read("docs/BASE_RULES_VERSION.md")
        readme = read("README.md")
        release = read("docs/operations/BASE_V9_4_RELEASE_CONTRACT.md")
        changelog = read("docs/CHANGELOG.md")
        coverage = read("docs/SKILL_COVERAGE_MAP.md")

        for term in (
            "Immutable rules baseline",
            "Latest released compatible line",
            "Current routing authority",
            "Frozen v9.0 release derivatives",
        ):
            self.assertIn(term, version)
        self.assertIn("frozen v9.0 release derivatives", readme)

        completed = release.split("## 4. 완료된 릴리스 단계", 1)[1].split("## 5.", 1)[0]
        self.assertNotIn("six project adoption audits", completed)
        self.assertIn("project_adoption: NOT_STARTED", release)

        self.assertNotRegex(changelog, r"(?m)^### Base v9\.4")
        self.assertRegex(changelog, r"(?m)^## .*Base v9\.4")
        self.assertLess(changelog.index("Base v9.4 AI operations candidate"), changelog.index("## 2026-07-30"))
        v2_section = changelog.split("## v2.0.0", 1)[1]
        self.assertNotIn("Base v9.4", v2_section)
        self.assertIn("SUPERSEDED", changelog)
        self.assertNotIn("GPT 검수→사용자 병합 승인", coverage)
        self.assertIn("AGENT_MERGE_REQUIRED", coverage)


if __name__ == "__main__":
    unittest.main()
