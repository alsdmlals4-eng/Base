"""Bounded guard composition and pilot-spec checks; no live model is invoked."""
from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from tools import check_skill_behavior_evals as identity
from tools import run_local_validation as runner

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = Path("skills/maintaining-project-context-and-handoff/references")
PILOT = REFERENCE / "long-horizon-failure-recovery-pilot.json"

# This test-only composition is not a production authorization or model grader.
CHECK_IDENTITY = """
import json, sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import check_skill_behavior_evals as identity
root = Path.cwd()
errors = identity.validate_result_identity(root, identity.load_json(root / 'result.json'))
(root / 'guard-errors.json').write_text(json.dumps(errors), encoding='utf-8')
raise SystemExit(1 if errors else 0)
"""
RECORD_EFFECT = """
from pathlib import Path
p = Path('effect-count.txt')
n = int(p.read_text()) if p.exists() else 0
p.write_text(str(n + 1), encoding='utf-8')
"""


class GuardCompositionTests(unittest.TestCase):
    """Real Git/files/subprocesses; synthetic receipts, not actual agent evidence."""

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        self.env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        self.git("init", "-q")
        self.write(identity.REGISTRY_PATH, {"fixture": "registry"})
        self.write(identity.EVAL_PATH, {"fixture": "evaluation"})
        schema = self.root / identity.RESULT_SCHEMA_PATH
        schema.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / identity.RESULT_SCHEMA_PATH, schema)
        self.git("add", ".")
        self.git("commit", "-qm", "synthetic fixture baseline")
        self.result = {
            "schema_version": 1,
            "artifact_role": "BASE_SKILL_BEHAVIOR_RESULTS",
            "run_status": "COMPLETED",
            "repository": "alsdmlals4-eng/Base",
            "commit_sha": self.git("rev-parse", "HEAD"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "model": {"provider": "synthetic-fixture", "model": "no-model-run", "version": "1"},
            "source_identity": {
                "registry_path": identity.REGISTRY_PATH.as_posix(),
                "registry_sha256": identity.file_sha256(self.root / identity.REGISTRY_PATH),
                "evaluation_paths": [identity.EVAL_PATH.as_posix()],
                "evaluation_sha256": identity.evaluation_sha256(self.root),
            },
            # Schema-shaped input only; these identifiers do not attest a real review.
            "review": {
                "author_context_id": "fixture-author",
                "reviewer_context_id": "fixture-reviewer",
                "independent": True,
                "author_summary_visible": False,
            },
            "results": [{
                "case_id": "SBE-001", "work_mode": "REVIEW",
                "primary_skill": "fixture-only", "supporting_skills": [],
                "skill_modes": ["fixture"], "evidence": ["synthetic input, not model evidence"],
                "user_decision_state": "NOT_REQUIRED",
            }],
        }
        self.write(Path("result.json"), self.result)

    def git(self, *arguments: str) -> str:
        return subprocess.run(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
             "-c", "commit.gpgsign=false", "-c", f"core.hooksPath={self.root / 'no-hooks'}",
             *arguments], cwd=self.root, env=self.env, check=True, capture_output=True,
            text=True, encoding="utf-8", timeout=15,
        ).stdout.strip()

    def write(self, relative: Path, value: object) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + "\n", encoding="utf-8")

    def run_guard(self) -> int:
        with contextlib.redirect_stdout(io.StringIO()):
            return runner.run_validation(self.root, [
                (sys.executable, "-c", CHECK_IDENTITY, str(ROOT / "tools")),
                (sys.executable, "-c", RECORD_EFFECT),
            ], self.env)

    def assert_blocked(self, reason: str, previous_effects: int = 0) -> None:
        self.assertEqual(1, self.run_guard())
        errors = json.loads((self.root / "guard-errors.json").read_text(encoding="utf-8"))
        self.assertIn(reason, "\n".join(errors))
        effect = self.root / "effect-count.txt"
        self.assertEqual(previous_effects, int(effect.read_text()) if effect.exists() else 0)
        self.assertFalse((self.root / ".tmp").exists())

    def test_current_receipt_allows_one_local_effect(self) -> None:
        self.assertEqual(0, self.run_guard())
        self.assertEqual("1", (self.root / "effect-count.txt").read_text())
        self.assertFalse((self.root / ".tmp").exists())

    def test_late_old_receipt_cannot_repeat_effect_after_head_moves(self) -> None:
        self.assertEqual(0, self.run_guard())
        self.git("commit", "--allow-empty", "-qm", "new fixture revision")
        self.assert_blocked("commit SHA does not match", previous_effects=1)

    def test_dirty_evaluation_blocks_effect_even_without_new_commit(self) -> None:
        self.write(identity.EVAL_PATH, {"fixture": "changed evaluation"})
        self.assertEqual(self.result["commit_sha"], self.git("rev-parse", "HEAD"))
        self.assert_blocked("evaluation SHA-256 does not match")

    def test_dirty_registry_blocks_effect(self) -> None:
        self.write(identity.REGISTRY_PATH, {"fixture": "changed registry"})
        self.assert_blocked("registry SHA-256 does not match")

    def test_changed_evaluation_file_set_blocks_effect(self) -> None:
        self.write(identity.COVERAGE_EVAL_PATH, {"fixture": "new coverage source"})
        self.assert_blocked("evaluation paths do not match")

    def test_not_run_receipt_cannot_authorize_effect(self) -> None:
        self.result.update(run_status="NOT_RUN", results=[])
        self.write(Path("result.json"), self.result)
        self.assert_blocked("run_status must be COMPLETED")

    def test_same_review_context_cannot_authorize_effect(self) -> None:
        self.result["review"]["reviewer_context_id"] = "fixture-author"
        self.write(Path("result.json"), self.result)
        self.assert_blocked("review context is not independent")

    def test_missing_result_schema_blocks_effect(self) -> None:
        (self.root / identity.RESULT_SCHEMA_PATH).unlink()
        self.assert_blocked("result schema unavailable or invalid")

    def test_failed_prerequisite_stops_following_effect_and_preserves_foreign_temp(self) -> None:
        foreign = self.root / ".tmp" / "other-session" / "keep.txt"
        foreign.parent.mkdir(parents=True)
        foreign.write_text("keep", encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            status = runner.run_validation(self.root, [
                (sys.executable, "-c", "raise SystemExit(7)"),
                (sys.executable, "-c", RECORD_EFFECT),
            ], self.env)
        self.assertEqual(7, status)
        self.assertFalse((self.root / "effect-count.txt").exists())
        self.assertEqual("keep", foreign.read_text())
        self.assertEqual(["other-session"], sorted(p.name for p in foreign.parent.parent.iterdir()))

    def test_missing_executable_stops_following_effect(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(FileNotFoundError):
            runner.run_validation(self.root, [
                (str(self.root / "nonexistent-executable"),),
                (sys.executable, "-c", RECORD_EFFECT),
            ], self.env)
        self.assertFalse((self.root / "effect-count.txt").exists())
        self.assertFalse((self.root / ".tmp").exists())


class PilotSpecificationTests(unittest.TestCase):
    def load_pilot(self) -> dict:
        self.assertTrue((ROOT / PILOT).is_file(), "missing bounded recovery pilot specification")
        return json.loads((ROOT / PILOT).read_text(encoding="utf-8"))

    def test_six_distinct_failure_cases_have_observable_negative_controls(self) -> None:
        pilot = self.load_pilot()
        cases = pilot["cases"]
        self.assertEqual([f"LHR-{i:02d}" for i in range(1, 7)], [c["case_id"] for c in cases])
        for case in cases:
            with self.subTest(case=case["case_id"]):
                for field in ("setup", "injection", "pass_observation", "negative_control", "owner"):
                    self.assertTrue(case[field].strip(), field)
                self.assertTrue(case["live_observation_required"])
                self.assertEqual("NOT_RUN", case["live_status"])
                self.assertEqual([], case["observed_evidence"])

    def test_specification_is_not_an_executed_result_or_automatic_install(self) -> None:
        pilot = self.load_pilot()
        self.assertEqual("PILOT_SPECIFICATION_NOT_RESULT", pilot["artifact_role"])
        self.assertEqual("NOT_RUN", pilot["live_model_run_status"])
        self.assertFalse(pilot["automatic_execution"])
        self.assertFalse(pilot["allow_paid_api_fallback"])
        self.assertIsNone(pilot["measured_improvement"])
        self.assertEqual("UNIT_GUARD_ONLY", pilot["unit_evidence_ceiling"])

    def test_comparison_keeps_safety_fixed_and_unsupported_features_unverified(self) -> None:
        comparison = self.load_pilot()["comparison"]
        self.assertEqual("ONE_SUPPORTED_FEATURE_AT_A_TIME", comparison["difference"])
        self.assertEqual("NOT_RUN", comparison["unsupported_feature_result"])
        self.assertFalse(comparison["disable_safety_for_control"])
        self.assertFalse(comparison["manual_reset_proves_native_compaction"])
        self.assertTrue(comparison["fresh_isolated_workspace_per_arm"])
        self.assertTrue(comparison["same_revision_task_model_budget"])

    def test_current_bootstrap_routes_to_pilot_without_upgrading_evidence(self) -> None:
        bootstrap = (ROOT / REFERENCE / "fresh-read-project-bootstrap.md").read_text(encoding="utf-8")
        self.assertIn("long-horizon-failure-recovery-pilot.md", bootstrap)
        guide = ROOT / REFERENCE / "long-horizon-failure-recovery-pilot.md"
        self.assertTrue(guide.is_file(), "missing pilot guide")
        text = guide.read_text(encoding="utf-8")
        for token in (PILOT.name, "UNIT_GUARD_ONLY", "MODEL_RUN_STATUS: NOT_RUN",
                      "TRANSFER_ACCEPTED_NOT_CLAIMED", "NO_PRODUCTION_AUTHORIZATION_GATE"):
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
