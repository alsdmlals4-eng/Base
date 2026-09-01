from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "base-v9.4.1.lock.json"
LOCK_SCHEMA_PATH = ROOT / "schemas/base-v9-4-1-release-lock-v1.schema.json"
EVIDENCE_PATH = ROOT / "docs/operations/BASE_V9_4_1_RELEASE_EVIDENCE.json"
EVIDENCE_SCHEMA_PATH = ROOT / "schemas/base-v9-4-1-release-evidence-v1.schema.json"
RELEASE_CONTRACT_PATH = ROOT / "docs/operations/BASE_V9_4_1_RELEASE_CONTRACT.md"
VERSION_PATH = ROOT / "docs/BASE_RULES_VERSION.md"
RELEASE_INDEX_PATH = ROOT / "tools/base_release_index.py"
RELEASE_CHECKER_PATH = ROOT / "tools/check_base_v9_4_1_release.py"
WORKFLOW_PATH = ROOT / ".github/workflows/validate-base-v9-rc.yml"
PREDECESSOR_LOCK_PATH = ROOT / "base-v9.4.lock.json"
PROJECT_CLI_PATHS = (
    ROOT / "tools/check_project_operating_contract.py",
    ROOT / "tools/build_project_operating_artifacts.py",
    ROOT / "tools/migrate_project_operating_contract.py",
)

PAYLOAD_COMMIT = "3f2c4a624d302b704c1b5322eb5c9f34ad55abb9"
EVIDENCE_COMMIT = "ff117d24d5bdb121314e109a6aa9b4f552e0fdc1"
REGISTRY_SHA256 = "693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59"
PREDECESSOR_PAYLOAD = "a728712cb776ec98f4875914a580fcf7d0156593"
PREDECESSOR_EVIDENCE = "ef1fba11167e4da0b298123b0c85ebd268191a42"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class BaseV941CompatibilityReleaseTests(unittest.TestCase):
    def test_release_artifacts_exist_and_validate(self) -> None:
        for path in (
            LOCK_PATH,
            LOCK_SCHEMA_PATH,
            EVIDENCE_PATH,
            EVIDENCE_SCHEMA_PATH,
            RELEASE_CONTRACT_PATH,
            VERSION_PATH,
            RELEASE_INDEX_PATH,
            RELEASE_CHECKER_PATH,
        ):
            self.assertTrue(path.is_file(), f"missing release artifact: {path.relative_to(ROOT)}")

        lock = load_json(LOCK_PATH)
        lock_schema = load_json(LOCK_SCHEMA_PATH)
        evidence = load_json(EVIDENCE_PATH)
        evidence_schema = load_json(EVIDENCE_SCHEMA_PATH)
        self.assertEqual([], list(Draft202012Validator(lock_schema).iter_errors(lock)))
        self.assertEqual([], list(Draft202012Validator(evidence_schema).iter_errors(evidence)))

    def test_release_identity_preserves_v940_and_binds_payload(self) -> None:
        predecessor = load_json(PREDECESSOR_LOCK_PATH)
        self.assertEqual("v9.4.0", predecessor["release_line"])
        self.assertEqual(PREDECESSOR_PAYLOAD, predecessor["candidate_release_commit"])
        self.assertEqual(PREDECESSOR_EVIDENCE, predecessor["candidate_release_evidence_commit"])
        self.assertEqual(REGISTRY_SHA256, predecessor["candidate_registry"]["sha256"])

        lock = load_json(LOCK_PATH)
        evidence = load_json(EVIDENCE_PATH)
        self.assertEqual("v9.4.1", lock["release_line"])
        self.assertEqual("BASE_RELEASED", lock["release_state"])
        self.assertEqual(PAYLOAD_COMMIT, lock["candidate_release_commit"])
        self.assertEqual(EVIDENCE_COMMIT, lock["candidate_release_evidence_commit"])
        self.assertEqual(REGISTRY_SHA256, lock["candidate_registry"]["sha256"])
        self.assertEqual(PAYLOAD_COMMIT, evidence["payload_commit"])
        self.assertEqual(REGISTRY_SHA256, evidence["registry_sha256"])
        self.assertEqual(139, lock["release_issue"])
        self.assertEqual(138, lock["source_pr"])

    def test_version_document_preserves_v941_historical_identity(self) -> None:
        text = VERSION_PATH.read_text(encoding="utf-8")
        self.assertIn("## Base v9.4.1 released compatible line", text)
        self.assertIn(PAYLOAD_COMMIT, text)
        self.assertIn(EVIDENCE_COMMIT, text)
        self.assertIn("base-v9.4.1.lock.json", text)

    def test_release_index_installs_v941_for_all_project_clis(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import sys; sys.path.insert(0, 'tools'); "
                    "import project_operating_contract as contract; "
                    "from base_release_index import install_release_lock_paths; "
                    "install_release_lock_paths(contract); "
                    "print(contract.release_lock_path('9.4.1').as_posix())"
                ),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual("base-v9.4.1.lock.json", result.stdout.strip())

        for path in PROJECT_CLI_PATHS:
            text = path.read_text(encoding="utf-8")
            self.assertIn("import project_operating_contract as contract", text)
            self.assertIn("from base_release_index import install_release_lock_paths", text)
            self.assertIn("install_release_lock_paths(contract)", text)

    def test_release_checker_accepts_current_trusted_history(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(RELEASE_CHECKER_PATH),
                "--trusted-history-commit",
                "HEAD",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("Base v9.4.1 compatibility release check passed", result.stdout)

    def test_release_checker_uses_canonical_git_blobs_not_checkout_line_endings(self) -> None:
        source = RELEASE_CHECKER_PATH.read_text(encoding="utf-8")
        self.assertIn('working_tree_evidence = blob_at("HEAD", EVIDENCE_PATH.relative_to(ROOT).as_posix())', source)
        self.assertIn("working tree evidence file is dirty", source)
        self.assertNotIn("evidence_blob != EVIDENCE_PATH.read_bytes()", source)

    def test_required_workflow_executes_v941_release_contract(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertIn('base-v9.4.1.lock.json', workflow)
        self.assertIn('tests.test_base_v9_4_1_compatibility_release', workflow)
        self.assertIn('python tools/check_base_v9_4_1_release.py', workflow)


if __name__ == "__main__":
    unittest.main()
