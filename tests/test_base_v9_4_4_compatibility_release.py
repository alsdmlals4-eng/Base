from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "base-v9.4.4.lock.json"
LOCK_SCHEMA_PATH = ROOT / "schemas/base-v9-4-4-release-lock-v1.schema.json"
EVIDENCE_PATH = ROOT / "docs/operations/BASE_V9_4_4_RELEASE_EVIDENCE.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas/base-v9-4-4-release-evidence-v1.schema.json"
RELEASE_CONTRACT_PATH = ROOT / "docs/operations/BASE_V9_4_4_RELEASE_CONTRACT.md"
VERSION_PATH = ROOT / "docs/BASE_RULES_VERSION.md"
RELEASE_INDEX_PATH = ROOT / "tools/base_release_index.py"
RELEASE_CHECKER_PATH = ROOT / "tools/check_base_v9_4_4_release.py"
WORKFLOW_PATH = ROOT / ".github/workflows/validate-base-v9-rc.yml"
PREDECESSOR_LOCK_PATH = ROOT / "base-v9.4.3.lock.json"
REGISTRY_PATH = ROOT / "skills/SKILL_REGISTRY.json"

PAYLOAD_COMMIT = "210ec78292fa12ed7563ba743b322dd36103ae4a"
EVIDENCE_COMMIT = "bb61e68dc3028421b60c11b87ba2abd297ee6f78"
FINALIZATION_COMMIT = "5adc196c0185951f50e49ab5e51586eff8d60886"
SOURCE_EXACT_HEAD = "e9a081b0aa9d046bfdec819ef2b88b7d1f115ec8"
PREDECESSOR_PAYLOAD = "7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8"
PREDECESSOR_EVIDENCE = "da33a350d61b8adc52df97fccc7001708a933370"
PREDECESSOR_REGISTRY = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"
RELEASED_PATHS = {
    "AGENTS.md",
    "START_HERE.md",
    "skills/managing-project-intake-and-work-contract/SKILL.md",
    "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json",
    "tests/test_reuse_first_preflight_enforcement.py",
    "tests/test_reference_freshness.py",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class BaseV944CompatibilityReleaseTests(unittest.TestCase):
    def test_release_artifacts_exist_and_validate(self) -> None:
        for path in (
            LOCK_PATH,
            LOCK_SCHEMA_PATH,
            EVIDENCE_PATH,
            EVIDENCE_SCHEMA_PATH,
            RELEASE_CONTRACT_PATH,
            RELEASE_INDEX_PATH,
            RELEASE_CHECKER_PATH,
        ):
            self.assertTrue(path.is_file(), f"missing release artifact: {path.relative_to(ROOT)}")
        lock = load_json(LOCK_PATH)
        evidence = load_json(EVIDENCE_PATH)
        self.assertEqual([], list(Draft202012Validator(load_json(LOCK_SCHEMA_PATH)).iter_errors(lock)))
        self.assertEqual([], list(Draft202012Validator(load_json(EVIDENCE_SCHEMA_PATH)).iter_errors(evidence)))

    def test_released_identity_preserves_v943_and_binds_reuse_first_payload(self) -> None:
        predecessor = load_json(PREDECESSOR_LOCK_PATH)
        self.assertEqual("v9.4.3", predecessor["release_line"])
        self.assertEqual("BASE_RELEASED", predecessor["release_state"])
        self.assertEqual(PREDECESSOR_PAYLOAD, predecessor["candidate_release_commit"])
        self.assertEqual(PREDECESSOR_EVIDENCE, predecessor["candidate_release_evidence_commit"])
        self.assertEqual(PREDECESSOR_REGISTRY, predecessor["candidate_registry"]["sha256"])

        lock = load_json(LOCK_PATH)
        evidence = load_json(EVIDENCE_PATH)
        self.assertEqual("v9.4.4", lock["release_line"])
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(EVIDENCE_COMMIT, lock["candidate_release_evidence_commit"])
        self.assertEqual(670, lock["release_issue"])
        self.assertEqual(669, lock["source_pr"])
        self.assertEqual(PAYLOAD_COMMIT, lock["candidate_release_commit"])
        self.assertEqual(RELEASED_PATHS, set(lock["released_validator_paths"]))
        self.assertEqual(PAYLOAD_COMMIT, evidence["payload_commit"])
        self.assertEqual(SOURCE_EXACT_HEAD, evidence["verification"]["source_exact_head"])
        self.assertEqual("NOT_RUN", evidence["limitations"]["real_project_adapter_execution"])
        self.assertEqual(lock["candidate_registry"]["sha256"], evidence["registry_sha256"])

        actual_registry = hashlib.sha256(REGISTRY_PATH.read_bytes()).hexdigest()
        self.assertEqual(
            actual_registry,
            lock["candidate_registry"]["sha256"],
            f"payload Registry SHA-256 is {actual_registry}",
        )

    def test_reuse_first_payload_contains_release_markers(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
        handoff = load_json(ROOT / "docs/knowledge/game-development/reuse/adoption/PROJECT_WORK_REUSE_HANDOFF.json")
        self.assertIn("REUSE_FIRST_PREFLIGHT_REQUIRED", agents)
        self.assertIn("REUSE_LEARNING_HANDOFF_REQUIRED", intake)
        self.assertEqual("REUSE_FIRST_PREFLIGHT_REQUIRED", handoff["preflight_gate"]["id"])
        self.assertEqual("REUSE_LEARNING_HANDOFF_REQUIRED", handoff["exit_learning_gate"]["id"])

    def test_release_index_installs_v944_candidate_path(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; sys.path.insert(0, 'tools'); "
                    "import project_operating_contract as contract; "
                    "from base_release_index import install_release_lock_paths; "
                    "install_release_lock_paths(contract); "
                    "print(contract.release_lock_path('9.4.4').as_posix())"
                ),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("base-v9.4.4.lock.json", result.stdout.strip())

    def test_release_index_pins_v944_finalization_identity(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; sys.path.insert(0, 'tools'); "
                    "from base_release_index import RELEASE_FINALIZATION_COMMITS; "
                    "print(RELEASE_FINALIZATION_COMMITS.get('9.4.4', 'MISSING'))"
                ),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(FINALIZATION_COMMIT, result.stdout.strip())

    def test_release_checker_accepts_released_candidate(self) -> None:
        result = subprocess.run(
            [sys.executable, str(RELEASE_CHECKER_PATH), "--trusted-history-commit", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Base v9.4.4 compatibility release check passed", result.stdout)

    def test_required_workflow_executes_v944_release_contract(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("base-v9.4.4.lock.json", workflow)
        self.assertIn("tests.test_base_v9_4_4_compatibility_release", workflow)
        self.assertIn("python tools/check_base_v9_4_4_release.py", workflow)

    def test_version_document_declares_latest_compatible_release(self) -> None:
        text = VERSION_PATH.read_text(encoding="utf-8")
        self.assertIn("Latest released compatible line | `v9.4.4`", text)
        self.assertIn(PAYLOAD_COMMIT, text)
        self.assertIn(EVIDENCE_COMMIT, text)
        self.assertIn("base-v9.4.4.lock.json", text)


if __name__ == "__main__":
    unittest.main()
