from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from tools.loop_a2_runtime.contract_bridge import ContractBridgeError, build_request_from_capsule
from tools.loop_a2_runtime.protocol import Budgets


class ContractBridgeTests(unittest.TestCase):
    def _project(self, root: Path, *, visual_impact: str = "NONE") -> None:
        loop = root / "docs/operations/loop"
        loop.mkdir(parents=True)
        capsule = {
            "project_id": "BLACKSMITH",
            "status": "ADOPTED",
            "autonomy": "A2_EXECUTE_ISOLATED",
            "source_main_sha": "a" * 40,
            "implementation_package_path": "IMPLEMENTATION_PACKAGE.json",
        }
        package = {
            "project_id": "BLACKSMITH",
            "package_id": "PACKAGE_001",
            "source_main_sha": "a" * 40,
            "execution_gate": "AUTONOMOUS_IMPLEMENTATION_READY",
            "visual_impact": visual_impact,
            "allowed_paths": ["scripts/feature/**", "tests/**"],
            "forbidden_paths": ["project.godot", ".github/**"],
            "resource_locks": ["SAVE_SCHEMA"],
            "requirement_ids": ["REQ_001"],
        }
        (loop / "PROJECT_EXECUTION_CAPSULE.json").write_text(json.dumps(capsule), encoding="utf-8")
        (loop / "IMPLEMENTATION_PACKAGE.json").write_text(json.dumps(package), encoding="utf-8")

    def test_scope_is_derived_from_package_not_caller(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._project(root)
            request = build_request_from_capsule(
                project_root=root,
                capsule_relative="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
                run_id="RUN_001",
                provider_mode="FAKE",
                budgets=Budgets(12, 2, 600),
                bundle_validator=lambda _: (),
            )
            self.assertEqual(request.allowed_paths, ("scripts/feature/**", "tests/**"))
            self.assertEqual(request.forbidden_paths, ("project.godot", ".github/**"))
            self.assertEqual(request.requirement_ids, ("REQ_001",))

    def test_bundle_findings_block_request(self) -> None:
        class Finding:
            code = "UNMAPPED_REQUIREMENT"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._project(root)
            with self.assertRaisesRegex(ContractBridgeError, "UNMAPPED_REQUIREMENT"):
                build_request_from_capsule(
                    project_root=root,
                    capsule_relative="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
                    run_id="RUN_001",
                    provider_mode="FAKE",
                    budgets=Budgets(12, 2, 600),
                    bundle_validator=lambda _: (Finding(),),
                )

    def test_new_visual_required_blocks_autonomous_request(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self._project(root, visual_impact="NEW_VISUAL_REQUIRED")
            with self.assertRaisesRegex(ContractBridgeError, "user decision"):
                build_request_from_capsule(
                    project_root=root,
                    capsule_relative="docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json",
                    run_id="RUN_001",
                    provider_mode="FAKE",
                    budgets=Budgets(12, 2, 600),
                    bundle_validator=lambda _: (),
                )

    def test_repository_m2_template_derives_request(self) -> None:
        repository_root = Path(__file__).resolve().parents[1]
        template_root = repository_root / "templates/project-operations/loop"
        if not (template_root / "PROJECT_EXECUTION_CAPSULE.json").is_file():
            self.skipTest("M2 repository template is unavailable in the isolated foundation fixture")
        request = build_request_from_capsule(
            project_root=template_root,
            capsule_relative="PROJECT_EXECUTION_CAPSULE.json",
            run_id="RUN_001",
            provider_mode="FAKE",
            budgets=Budgets(12, 2, 600),
        )
        self.assertEqual(request.project_id, "EXAMPLE_GAME")
        self.assertEqual(request.package_id, "PACKAGE_001")
        self.assertEqual(request.requirement_ids, ("REQ_001",))
        self.assertEqual(request.allowed_paths, ("scripts/example.gd",))


if __name__ == "__main__":
    unittest.main()
