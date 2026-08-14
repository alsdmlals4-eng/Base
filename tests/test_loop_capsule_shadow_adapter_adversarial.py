from __future__ import annotations

import json
import subprocess
import sys
import unittest

from tests.test_loop_capsule_shadow_adapter import (
    LoopCapsuleShadowAdapterTests,
    ROOT,
    SOURCE_SHA,
)


class LoopCapsuleShadowAdapterAdversarialTests(LoopCapsuleShadowAdapterTests):
    def test_planning_conflict_and_unverified_state_stop_at_adapter_boundary(self) -> None:
        api = self._api()
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)
        for drift in ("PLANNING_CONFLICT", "UNVERIFIED"):
            with self.subTest(drift=drift):
                with self.assertRaises(api.AdapterError) as raised:
                    self._build(capsule_path, planning_drift=drift)
                self.assertIn("PLANNING", str(raised.exception).upper())

    def test_existing_visual_conflict_and_unverified_state_stop_at_adapter_boundary(self) -> None:
        api = self._api()
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)

        package_path = capsule_path.parent / "IMPLEMENTATION_PACKAGE.json"
        package = json.loads(package_path.read_text(encoding="utf-8"))
        package["visual_impact"] = "EXISTING_LOCKED"
        package["visual_lock_requirement"] = "VISUAL_LOCKED"
        package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")

        visual_path = capsule_path.parent / "VISUAL_LOCK.json"
        visual = json.loads(visual_path.read_text(encoding="utf-8"))
        visual["status"] = "VISUAL_LOCKED"
        visual["provider"] = "FIGMA_VISUAL_BIBLE"
        visual["reference_ids"] = ["FIGMA_NODE_001"]
        visual["keep"] = ["approved composition"]
        visual["do_not_drift"] = ["approved hierarchy"]
        visual_path.write_text(json.dumps(visual, indent=2) + "\n", encoding="utf-8")

        for drift in ("VISUAL_CONFLICT", "UNVERIFIED"):
            with self.subTest(drift=drift):
                with self.assertRaises(api.AdapterError) as raised:
                    self._build(capsule_path, visual_drift=drift)
                self.assertIn("VISUAL", str(raised.exception).upper())

    def test_callers_cannot_inject_outputs_budgets_or_authority(self) -> None:
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)
        for injected in (
            {"changed_paths": ["scripts/unauthorized.gd"]},
            {"allowed_paths": ["scripts/unauthorized.gd"]},
            {"max_transitions": 256},
            {"references": [{"project_id": "OTHER", "kind": "CANON", "path": "x"}]},
        ):
            with self.subTest(injected=injected):
                with self.assertRaises(TypeError):
                    self._api().build_shadow_request(
                        capsule_path,
                        run_id="RUN_ADAPTER_001",
                        observed_main_sha=SOURCE_SHA,
                        planning_drift="NO_DRIFT",
                        visual_drift="NOT_APPLICABLE",
                        **injected,
                    )

    def test_direct_cli_emits_closed_request_without_state_or_product_write(self) -> None:
        temporary, capsule_path = self._bundle()
        self.addCleanup(temporary.cleanup)
        completed = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools/loop_capsule_to_shadow.py"),
                str(capsule_path),
                "--run-id",
                "RUN_ADAPTER_CLI",
                "--observed-main-sha",
                SOURCE_SHA,
                "--planning-drift",
                "NO_DRIFT",
                "--visual-drift",
                "NOT_APPLICABLE",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["contract_role"], "LOOP_SHADOW_REQUEST")
        self.assertEqual(payload["run_id"], "RUN_ADAPTER_CLI")
        self.assertFalse((capsule_path.parent / ".loop-engineering").exists())


if __name__ == "__main__":
    unittest.main()
