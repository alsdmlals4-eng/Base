from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "tools/check_skill_behavior_evals.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_skill_behavior_evals", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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


class SkillBehaviorCoverageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.checker = load_checker()

    def build_root(self, cases: list[dict]) -> tuple[tempfile.TemporaryDirectory[str], Path]:
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
        for skill_id in ("alpha-skill", "beta-skill"):
            path = root / f"skills/{skill_id}/SKILL.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {skill_id}\n\nMode: `run`\n", encoding="utf-8")
        return directory, root

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


if __name__ == "__main__":
    unittest.main()
