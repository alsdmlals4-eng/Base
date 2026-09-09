from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
import unittest


BRIDGE_ROOT = Path(__file__).resolve().parents[1]
SRC = BRIDGE_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aseprite_local_bridge.bridge import BridgeError  # noqa: E402
from aseprite_local_bridge.cli import main  # noqa: E402


class FakeBridge:
    def doctor(self) -> dict[str, object]:
        return {"status": "PASS", "operation": "doctor"}

    def inspect(self, source: str) -> dict[str, object]:
        return {"status": "PASS", "operation": "inspect", "source": source}

    def export_candidate(
        self,
        source: str,
        asset_id: str,
        replace_candidate: bool = False,
    ) -> dict[str, object]:
        return {
            "status": "PASS",
            "operation": "export_candidate",
            "source": source,
            "asset_id": asset_id,
            "replace_candidate": replace_candidate,
        }

    def validate_candidate(self, asset_id: str) -> dict[str, object]:
        return {"status": "PASS", "operation": "validate_candidate", "asset_id": asset_id}


class ErrorBridge(FakeBridge):
    def doctor(self) -> dict[str, object]:
        raise BridgeError("ASEPRITE_UNAVAILABLE", "set ASEPRITE_PATH")


class CliTests(unittest.TestCase):
    def run_cli(self, argv: list[str], bridge: object) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(argv, bridge_factory=lambda **_: bridge)
        return code, stdout.getvalue(), stderr.getvalue()

    def test_doctor_prints_one_json_object_and_returns_zero(self) -> None:
        code, stdout, stderr = self.run_cli(["doctor", "--project-root", "."], FakeBridge())

        self.assertEqual(code, 0)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload, {"operation": "doctor", "status": "PASS"})
        self.assertEqual(stdout.count("\n"), 1)

    def test_expected_bridge_error_returns_two_without_traceback(self) -> None:
        code, stdout, stderr = self.run_cli(["doctor", "--project-root", "."], ErrorBridge())

        self.assertEqual(code, 2)
        self.assertEqual(stderr, "")
        payload = json.loads(stdout)
        self.assertEqual(payload["status"], "BLOCKED")
        self.assertEqual(payload["code"], "ASEPRITE_UNAVAILABLE")
        self.assertNotIn("Traceback", stdout)

    def test_export_routes_explicit_replace_flag(self) -> None:
        code, stdout, _ = self.run_cli(
            [
                "export-candidate",
                "--project-root",
                ".",
                "--source",
                ".asset-vault/library/hero.aseprite",
                "--asset-id",
                "HERO_IDLE_01",
                "--replace-candidate",
            ],
            FakeBridge(),
        )

        self.assertEqual(code, 0)
        payload = json.loads(stdout)
        self.assertIs(payload["replace_candidate"], True)
        self.assertEqual(payload["asset_id"], "HERO_IDLE_01")

    def test_validate_routes_asset_id(self) -> None:
        code, stdout, _ = self.run_cli(
            ["validate-candidate", "--project-root", ".", "--asset-id", "HERO_IDLE_01"],
            FakeBridge(),
        )

        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stdout)["operation"], "validate_candidate")


if __name__ == "__main__":
    unittest.main()
