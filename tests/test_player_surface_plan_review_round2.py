"""Independent-review round-2 regressions; structural only, never runtime proof."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/validate_player_surface_plan.py"
FIXTURE_FILE = ROOT / "tests/test_player_surface_plan.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PlayerSurfacePlanReviewRound2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.checker = _load(CHECKER, "surface_plan_checker_round2")
        cls.fixtures = _load(FIXTURE_FILE, "surface_plan_fixtures_round2")

    def rejected(self, packet, code: str, gate: str = "plan"):
        errors = self.checker.validate_packet(packet, gate)
        self.assertTrue(any(code in error for error in errors), (code, errors))

    def test_packet_repository_must_be_canonical_owner_repo_identity(self):
        packet = self.fixtures.packet()
        packet["repository"] = "https://github.com/example/fixture-game"
        self.rejected(packet, "SOURCE_IDENTITY")

    def test_invalid_project_identity_cannot_make_own_repository_external(self):
        packet = self.fixtures.packet()
        packet["repository"] = "https://github.com/example/fixture-game"
        packet["references"][0]["source"] = "https://github.com/example/fixture-game/blob/main/ui.gd"
        packet["references"][0]["source_repository"] = "example/fixture-game"
        self.rejected(packet, "EXTERNAL_BENCHMARK_REQUIRED")

    def test_native_family_cannot_claim_raster_modules(self):
        packet = self.fixtures.add_modular_parts(self.fixtures.packet())
        self.rejected(packet, "NATIVE_FAMILY_RASTER_CONTRADICTION")

    def test_raster_module_used_in_composition_still_needs_non_native_family_owner(self):
        packet = self.fixtures.add_modular_parts(self.fixtures.packet())
        self.rejected(packet, "RASTER_MODULE_UNCONTRACTED")

    def _run_cli(self, *arguments: str):
        return subprocess.run(
            [sys.executable, str(CHECKER), *arguments],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def _assert_structured_input_error(self, result):
        self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
        self.assertEqual(result.stderr, "")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["result"], "INPUT_ERROR")
        self.assertEqual(payload["evidence_ceiling"], "STRUCTURE_ONLY_NOT_RUNTIME_OR_USER_APPROVAL")

    def test_missing_required_cli_argument_is_structured_json(self):
        self._assert_structured_input_error(self._run_cli())

    def test_invalid_gate_is_structured_json(self):
        with tempfile.TemporaryDirectory() as temporary:
            packet_path = Path(temporary) / "packet.json"
            packet_path.write_text(json.dumps(self.fixtures.packet()), encoding="utf-8")
            self._assert_structured_input_error(
                self._run_cli("--packet", str(packet_path), "--gate", "runtime")
            )

    def test_help_remains_a_normal_successful_cli_path(self):
        result = self._run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("--packet", result.stdout)


if __name__ == "__main__":
    unittest.main()
