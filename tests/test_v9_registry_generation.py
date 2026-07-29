from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv/Scripts/python.exe"
GENERATOR = ROOT / "tools/build_base_v9_artifacts.py"
INTEGRITY_CHECK = ROOT / "tools/check_base_v9_integrity.py"
REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"
OUTPUTS = (
    ROOT / ".codex-plugin/plugin.json",
    ROOT / "base.lock.json",
    ROOT / "skills/BASE_V9_SKILL_SNAPSHOT.json",
    ROOT / "docs/generated/BASE_ACTIVE_SKILLS.md",
    ROOT / "docs/operations/BASE_V9_DECISION_REGISTRY.json",
    ROOT / "docs/operations/GITHUB_OBJECT_LEDGER.json",
    ROOT / "docs/operations/ADVERSARIAL_REVIEW_MANIFEST.json",
    ROOT / "docs/operations/SHEET_CONTROL_CONTRACT.json",
)

GENERATOR_SPEC = importlib.util.spec_from_file_location("base_v9_generator", GENERATOR)
assert GENERATOR_SPEC and GENERATOR_SPEC.loader
GENERATOR_MODULE = importlib.util.module_from_spec(GENERATOR_SPEC)
GENERATOR_SPEC.loader.exec_module(GENERATOR_MODULE)


class V9RegistryGenerationTests(unittest.TestCase):
    maxDiff = None

    def run_generator(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(PYTHON), str(GENERATOR), *arguments],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )

    def test_text_source_hash_ignores_line_ending_style(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "source-lf.txt"
            crlf = root / "source-crlf.txt"
            lf.write_bytes(b"alpha\nbeta\n")
            crlf.write_bytes(b"alpha\r\nbeta\r\n")

            self.assertEqual(
                GENERATOR_MODULE.sha256_normalized_text_file(lf),
                GENERATOR_MODULE.sha256_normalized_text_file(crlf),
            )

    def test_generated_artifacts_match_current_registry_and_are_deterministic(self) -> None:
        first = self.run_generator("--write")
        self.assertEqual(first.returncode, 0, first.stderr)
        before = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in OUTPUTS}
        second = self.run_generator("--write")
        self.assertEqual(second.returncode, 0, second.stderr)
        after = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in OUTPUTS}
        self.assertEqual(before, after, "A second generator run changed generated output")
        checked = self.run_generator("--check")
        self.assertEqual(checked.returncode, 0, checked.stderr)

        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        active = [item for item in registry["skills"] if item["status"] == "ACTIVE"]
        snapshot = json.loads((ROOT / "skills/BASE_V9_SKILL_SNAPSHOT.json").read_text(encoding="utf-8"))
        self.assertEqual(snapshot["active_skill_count"], len(active))
        self.assertEqual(
            [item["skill_id"] for item in snapshot["skills"]],
            [item["skill_id"] for item in active],
        )
        for item in snapshot["skills"]:
            self.assertEqual(
                set(item["contract"]),
                {"positive_trigger", "negative_trigger", "owner", "input", "output", "failure", "verification", "next_step"},
            )
            self.assertTrue(all(item["contract"].values()), item["skill_id"])

    def test_lock_plugin_and_control_contracts_keep_base_and_projects_separate(self) -> None:
        generated = self.run_generator("--write")
        self.assertEqual(generated.returncode, 0, generated.stderr)
        lock = json.loads((ROOT / "base.lock.json").read_text(encoding="utf-8"))
        plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        sheet = json.loads((ROOT / "docs/operations/SHEET_CONTROL_CONTRACT.json").read_text(encoding="utf-8"))
        ledger = json.loads((ROOT / "docs/operations/GITHUB_OBJECT_LEDGER.json").read_text(encoding="utf-8"))
        self.assertEqual(lock["release_line"], "v9.0.0")
        self.assertEqual(lock["release_state"], "BASE_RELEASE_PENDING_CI")
        self.assertEqual(lock["project_adoption_state"], "POST_RELEASE_PROJECT_ADOPTION_WAVE")
        self.assertEqual(plugin["version"], "9.0.0")
        self.assertEqual(plugin["author"]["name"], "alsdmlals4-eng")
        self.assertEqual(plugin["skills"], "./skills/")
        self.assertEqual(plugin["interface"]["displayName"], "Base v9")
        self.assertEqual(plugin["base_v9"]["active_skill_count"], lock["active_skill_count"])
        self.assertEqual(sheet["base_sheet_status"], "BASE_EXCLUDED")
        self.assertFalse(sheet["external_sheet_writes_authorized"])
        self.assertTrue(all(project["status"] == "HOLD" for project in sheet["held_projects"]))
        self.assertIn("base-v9-final-lock", sheet["resume_prerequisites"])
        self.assertIn("pr", ledger["object_types"])
        self.assertIn(
            {"type": "issue", "number": 55, "disposition": "POST_RELEASE_ADOPTION"},
            ledger["objects"],
        )

    def test_integrity_checker_reports_generated_drift_orphans_and_cycles(self) -> None:
        generated = self.run_generator("--write")
        self.assertEqual(generated.returncode, 0, generated.stderr)
        result = subprocess.run(
            [str(PYTHON), str(INTEGRITY_CHECK)],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Base v9 integrity check passed", result.stdout)


if __name__ == "__main__":
    unittest.main()
