from __future__ import annotations

import importlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = ROOT / "templates/project-operations/loop"
SOURCE_SHA = "a" * 40


class LoopCapsuleShadowAdapterTests(unittest.TestCase):
    maxDiff = None

    def _api(self):
        spec = importlib.util.find_spec("tools.loop_capsule_shadow_adapter")
        self.assertIsNotNone(spec, "tools.loop_capsule_shadow_adapter production package is missing")
        return importlib.import_module("tools.loop_capsule_shadow_adapter")

    def _bundle(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        shutil.copytree(TEMPLATE_ROOT, root, dirs_exist_ok=True)

        for relative in (
            "PROJECT_EXECUTION_CAPSULE.json",
            "PLANNING_LOCK.json",
            "VISUAL_LOCK.json",
            "IMPLEMENTATION_PACKAGE.json",
            "REQUIREMENT_COVERAGE_LEDGER.json",
            "ACTIVE_LOOP_RUN.json",
            "runs/IMMUTABLE_RUN.json",
        ):
            path = root / relative
            value = json.loads(path.read_text(encoding="utf-8"))
            if relative == "PROJECT_EXECUTION_CAPSULE.json":
                value["source_main_sha"] = SOURCE_SHA
            elif relative in {"PLANNING_LOCK.json", "VISUAL_LOCK.json"}:
                value["source_commit"] = SOURCE_SHA
                if relative == "PLANNING_LOCK.json":
                    for source in value["authority_sources"]:
                        source["source_commit"] = SOURCE_SHA
            else:
                value["source_main_sha"] = SOURCE_SHA
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return temporary, root / "PROJECT_EXECUTION_CAPSULE.json"

    def _build(self, capsule_path: Path, **overrides: str):
        api = self._api()
        arguments = {
            "run_id": "RUN_ADAPTER_001",
            "observed_main_sha": SOURCE_SHA,
            "planning_drift": "NO_DRIFT",
            "visual_drift": "NOT_APPLICABLE",
        }
        arguments.update(overrides)
        return api.build_shadow_request(capsule_path, **arguments)

    def test_valid_bundle_translates_only_authoritative_fields(self) -> None:
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)

        request = self._build(capsule_path)

        self.assertEqual(request["contract_role"], "LOOP_SHADOW_REQUEST")
        self.assertEqual(request["project_id"], "EXAMPLE_GAME")
        self.assertEqual(request["package_id"], "PACKAGE_001")
        self.assertEqual(request["source_main_sha"], SOURCE_SHA)
        self.assertEqual(request["observed_main_sha"], SOURCE_SHA)
        self.assertEqual(request["planning_status"], "PLANNING_LOCKED")
        self.assertEqual(request["visual_impact"], "NONE")
        self.assertEqual(request["visual_status"], "VISUAL_NOT_APPLICABLE")
        self.assertEqual(request["approved_requirements"], ["REQ_001"])
        self.assertEqual(request["package_requirement_ids"], ["REQ_001"])
        self.assertEqual(request["allowed_paths"], ["scripts/example.gd"])
        self.assertEqual(request["changed_paths"], ["scripts/example.gd"])
        self.assertEqual(request["required_evidence"], ["E1_STATIC", "E2_TEST"])
        self.assertEqual(request["resource_locks"], ["EXAMPLE_DOMAIN"])
        self.assertEqual(request["references"], [
            {"project_id": "EXAMPLE_GAME", "kind": "CANON", "path": "docs/GDD.md"}
        ])
        self.assertEqual(request["budgets"], {"max_transitions": 16, "max_repeated_failures": 2})
        self.assertEqual(request["autonomy"], "A2_EXECUTE_ISOLATED")
        self.assertEqual(request["a3_auto_merge_allowlist"], [])
        self.assertEqual(request["scheduler_runtime_provider"], "NOT_CONFIGURED")

    def test_invalid_m2_bundle_blocks_before_translation(self) -> None:
        api = self._api()
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)
        planning_path = capsule_path.parent / "PLANNING_LOCK.json"
        planning = json.loads(planning_path.read_text(encoding="utf-8"))
        planning["project_id"] = "OTHER_GAME"
        planning_path.write_text(json.dumps(planning, indent=2) + "\n", encoding="utf-8")

        with self.assertRaises(api.AdapterError) as raised:
            self._build(capsule_path)
        self.assertIn("PROJECT_ID_MISMATCH", str(raised.exception))

    def test_observed_main_mismatch_and_invalid_runtime_observation_fail_closed(self) -> None:
        api = self._api()
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)
        cases = (
            {"observed_main_sha": "b" * 40},
            {"run_id": "../RUN"},
            {"planning_drift": "TRUST_ME"},
            {"visual_drift": "TRUST_ME"},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides):
                with self.assertRaises(api.AdapterError):
                    self._build(capsule_path, **overrides)

    def test_new_visual_required_never_translates_to_autonomous_request(self) -> None:
        api = self._api()
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)
        package_path = capsule_path.parent / "IMPLEMENTATION_PACKAGE.json"
        package = json.loads(package_path.read_text(encoding="utf-8"))
        package["visual_impact"] = "NEW_VISUAL_REQUIRED"
        package["visual_lock_requirement"] = "VISUAL_LOCKED"
        package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")
        visual_path = capsule_path.parent / "VISUAL_LOCK.json"
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        visual["status"] = "VISUAL_LOCKED"
        visual["provider"] = "FIGMA_VISUAL_BIBLE"
        visual["reference_ids"] = ["FIGMA_NODE_001"]
        visual_path.write_text(json.dumps(visual, indent=2) + "\n", encoding="utf-8")

        with self.assertRaises(api.AdapterError) as raised:
            self._build(capsule_path, visual_drift="UNVERIFIED")
        self.assertIn("USER_DECISION_REQUIRED", str(raised.exception))

    def test_changed_paths_are_derived_from_coverage_and_normalized_deterministically(self) -> None:
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)
        package_path = capsule_path.parent / "IMPLEMENTATION_PACKAGE.json"
        package = json.loads(package_path.read_text(encoding="utf-8"))
        package["allowed_paths"] = ["scripts/z.gd", "scripts\\cafe\u0301.gd"]
        package_path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        coverage_path = capsule_path.parent / "REQUIREMENT_COVERAGE_LEDGER.json"
        coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
        coverage["requirements"][0]["outputs"] = ["scripts\\cafe\u0301.gd", "scripts/z.gd"]
        coverage_path.write_text(json.dumps(coverage, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        first = self._build(capsule_path)
        second = self._build(capsule_path)

        self.assertEqual(first, second)
        self.assertEqual(first["changed_paths"], ["scripts/café.gd", "scripts/z.gd"])
        self.assertEqual(first["allowed_paths"], ["scripts/z.gd", "scripts/café.gd"])

    def test_source_documents_are_not_mutated(self) -> None:
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)
        before = {
            path.relative_to(capsule_path.parent).as_posix(): path.read_bytes()
            for path in capsule_path.parent.rglob("*.json")
        }

        self._build(capsule_path)

        after = {
            path.relative_to(capsule_path.parent).as_posix(): path.read_bytes()
            for path in capsule_path.parent.rglob("*.json")
        }
        self.assertEqual(after, before)

    def test_adapter_source_has_no_model_network_subprocess_or_git_writer_imports(self) -> None:
        self._api()
        import ast
        package_root = ROOT / "tools/loop_capsule_shadow_adapter"
        forbidden = {"openai", "requests", "httpx", "socket", "subprocess", "urllib", "git"}
        violations: list[str] = []
        for path in package_root.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.split(".")[0] in forbidden:
                            violations.append(f"{path.name}:{alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.split(".")[0] in forbidden:
                        violations.append(f"{path.name}:{node.module}")
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
