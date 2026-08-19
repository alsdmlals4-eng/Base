from __future__ import annotations

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/reuse_modules/reuse_adoption.py"
SOURCE_REL = "templates/reuse-modules/godot/grid_placement_rule_engine.gd"
DEST_REL = "vendor/base-reuse/grid_placement_rule_engine.gd"
BASE_COMMIT = "8553678f70e22f193a2336b591f677dcfa5a8965"


def load_module():
    spec = importlib.util.spec_from_file_location("reuse_adoption_safety", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def manifest() -> dict:
    return {
        "schema_version": 1,
        "base_source_commit": BASE_COMMIT,
        "modules": {
            "RM-SYS-001": {
                "state": "enabled",
                "source": SOURCE_REL,
                "destination": DEST_REL,
            }
        },
    }


class ReuseAdoptionSafetyTests(unittest.TestCase):
    def test_identical_existing_file_can_be_bootstrapped_into_lock(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            destination = project_root / DEST_REL
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / SOURCE_REL, destination)

            report = module.apply_adoption(ROOT, project_root, manifest())

            self.assertTrue(report["ok"], report)
            self.assertTrue((project_root / ".base-reuse/adoption-lock.json").is_file())
            self.assertTrue(module.check_adoption(ROOT, project_root, manifest())["ok"])

    def test_locked_destination_symlink_escape_is_refused_without_mutating_target(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            project_root = root / "project"
            project_root.mkdir()
            outside = root / "outside.gd"
            outside.write_text("outside-owned-content\n", encoding="utf-8")
            original_outside = outside.read_text(encoding="utf-8")

            destination = project_root / DEST_REL
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                os.symlink(outside, destination)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symlink unavailable: {exc}")

            source_hash = module._sha256(ROOT / SOURCE_REL)
            installed_hash = module._sha256(outside)
            lock_path = project_root / ".base-reuse/adoption-lock.json"
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            lock_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "base_source_commit": BASE_COMMIT,
                        "modules": {
                            "RM-SYS-001": {
                                "source": SOURCE_REL,
                                "destination": DEST_REL,
                                "source_sha256": source_hash,
                                "installed_sha256": installed_hash,
                            }
                        },
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )

            report = module.apply_adoption(ROOT, project_root, manifest())

            self.assertFalse(report["ok"], report)
            self.assertIn("PATH_ESCAPE_OR_SYMLINK", {item["code"] for item in report["violations"]})
            self.assertEqual(original_outside, outside.read_text(encoding="utf-8"))

    def test_manifest_requires_exact_commit_and_unique_non_reserved_destinations(self) -> None:
        module = load_module()
        invalid_commit = manifest()
        invalid_commit["base_source_commit"] = "not-a-git-sha"
        with self.assertRaises(ValueError):
            module.validate_manifest(invalid_commit)

        duplicate_destination = manifest()
        duplicate_destination["modules"]["RM-VIS-001"] = {
            "state": "enabled",
            "source": "templates/reuse-modules/godot/semantic_ui_skin_kit.gd",
            "destination": DEST_REL,
        }
        with self.assertRaises(ValueError):
            module.validate_manifest(duplicate_destination)

        reserved_destination = manifest()
        reserved_destination["modules"]["RM-SYS-001"]["destination"] = ".base-reuse/adoption-lock.json"
        with self.assertRaises(ValueError):
            module.validate_manifest(reserved_destination)

    def test_corrupt_adoption_lock_fails_closed_instead_of_crashing(self) -> None:
        module = load_module()
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            lock_path = project_root / ".base-reuse/adoption-lock.json"
            lock_path.parent.mkdir(parents=True, exist_ok=True)
            lock_path.write_text("{not-json", encoding="utf-8")

            apply_report = module.apply_adoption(ROOT, project_root, manifest())
            check_report = module.check_adoption(ROOT, project_root, manifest())

            self.assertFalse(apply_report["ok"])
            self.assertFalse(check_report["ok"])
            self.assertIn("INVALID_LOCK", {item["code"] for item in apply_report["violations"]})
            self.assertIn("INVALID_LOCK", {item["code"] for item in check_report["violations"]})


if __name__ == "__main__":
    unittest.main()
