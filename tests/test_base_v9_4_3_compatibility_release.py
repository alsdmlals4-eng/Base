from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "base-v9.4.3.lock.json"
LOCK_SCHEMA_PATH = ROOT / "schemas/base-v9-4-3-release-lock-v1.schema.json"
EVIDENCE_PATH = ROOT / "docs/operations/BASE_V9_4_3_RELEASE_EVIDENCE.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas/base-v9-4-3-release-evidence-v1.schema.json"
RELEASE_CONTRACT_PATH = ROOT / "docs/operations/BASE_V9_4_3_RELEASE_CONTRACT.md"
VERSION_PATH = ROOT / "docs/BASE_RULES_VERSION.md"
RELEASE_INDEX_PATH = ROOT / "tools/base_release_index.py"
RELEASE_CHECKER_PATH = ROOT / "tools/check_base_v9_4_3_release.py"
WORKFLOW_PATH = ROOT / ".github/workflows/validate-base-v9-rc.yml"
PREDECESSOR_LOCK_PATH = ROOT / "base-v9.4.2.lock.json"

PAYLOAD_COMMIT = "7dd1a4f80388bc5faca767ff74a3eb32dc9d0ac8"
EVIDENCE_COMMIT = "da33a350d61b8adc52df97fccc7001708a933370"
SOURCE_EXACT_HEAD = "b2cd0f99827e8e2b34c42204de54a2bf5b447225"
REGISTRY_SHA256 = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"
PREDECESSOR_PAYLOAD = "dd705d7f48a7919187bc0507610ba5fc5b43a658"
PREDECESSOR_EVIDENCE = "0c6cdd128bf1f5782e96b3a6240c9585f8d1ef6d"
RELEASED_PATHS = {
    "tests/test_first_prompt_intake_contract.py",
    "tests/test_base_v9_4_ai_operations_contract.py",
    "tests/test_consolidated_skill_references.py",
    "skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class BaseV943CompatibilityReleaseTests(unittest.TestCase):
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

    def test_released_identity_preserves_v942_and_binds_first_prompt_payload(self) -> None:
        predecessor = load_json(PREDECESSOR_LOCK_PATH)
        self.assertEqual("v9.4.2", predecessor["release_line"])
        self.assertEqual(PREDECESSOR_PAYLOAD, predecessor["candidate_release_commit"])
        self.assertEqual(PREDECESSOR_EVIDENCE, predecessor["candidate_release_evidence_commit"])
        self.assertEqual(REGISTRY_SHA256, predecessor["candidate_registry"]["sha256"])

        lock = load_json(LOCK_PATH)
        evidence = load_json(EVIDENCE_PATH)
        self.assertEqual("v9.4.3", lock["release_line"])
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(EVIDENCE_COMMIT, lock["candidate_release_evidence_commit"])
        self.assertEqual(148, lock["release_issue"])
        self.assertEqual(143, lock["source_pr"])
        self.assertEqual(PAYLOAD_COMMIT, lock["candidate_release_commit"])
        self.assertEqual(REGISTRY_SHA256, lock["candidate_registry"]["sha256"])
        self.assertEqual(RELEASED_PATHS, set(lock["released_validator_paths"]))
        self.assertEqual(PAYLOAD_COMMIT, evidence["payload_commit"])
        self.assertEqual(REGISTRY_SHA256, evidence["registry_sha256"])
        self.assertEqual(SOURCE_EXACT_HEAD, evidence["verification"]["source_exact_head"])
        self.assertEqual("NOT_RUN", evidence["limitations"]["real_project_adapter_execution"])

    def test_release_index_installs_v943(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; sys.path.insert(0, 'tools'); "
                    "import project_operating_contract as contract; "
                    "from base_release_index import install_release_lock_paths; "
                    "install_release_lock_paths(contract); "
                    "print(contract.release_lock_path('9.4.3').as_posix())"
                ),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("base-v9.4.3.lock.json", result.stdout.strip())

    def test_release_checker_accepts_released_candidate(self) -> None:
        result = subprocess.run(
            [sys.executable, str(RELEASE_CHECKER_PATH), "--trusted-history-commit", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Base v9.4.3 compatibility release check passed", result.stdout)

    def test_release_checker_uses_canonical_git_blobs_not_checkout_line_endings(self) -> None:
        source = RELEASE_CHECKER_PATH.read_text(encoding="utf-8")
        self.assertIn('working_tree_evidence = blob("HEAD", EVIDENCE_PATH.relative_to(ROOT).as_posix())', source)
        self.assertIn("working tree evidence file is dirty", source)
        self.assertNotIn("evidence_blob != EVIDENCE_PATH.read_bytes()", source)

    def test_required_workflow_executes_v943_release_contract(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn("base-v9.4.3.lock.json", workflow)
        self.assertIn("tests.test_base_v9_4_3_compatibility_release", workflow)
        self.assertIn("python tools/check_base_v9_4_3_release.py", workflow)

    def test_version_document_preserves_v943_historical_identity(self) -> None:
        text = VERSION_PATH.read_text(encoding="utf-8")
        self.assertIn("## Base v9.4.3 released compatible line", text)
        self.assertIn(PAYLOAD_COMMIT, text)
        self.assertIn(EVIDENCE_COMMIT, text)
        self.assertIn("base-v9.4.3.lock.json", text)


if __name__ == "__main__":
    unittest.main()
