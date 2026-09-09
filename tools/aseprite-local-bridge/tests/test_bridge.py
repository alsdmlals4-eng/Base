from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


BRIDGE_ROOT = Path(__file__).resolve().parents[1]
SRC = BRIDGE_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aseprite_local_bridge.bridge import (  # noqa: E402
    AsepriteBridge,
    BridgeConfig,
    BridgeError,
)


PNG_BYTES = b"\x89PNG\r\n\x1a\nFAKE-PNG-DATA"


class FakeRunner:
    def __init__(self) -> None:
        self.calls: list[tuple[list[str], dict[str, object]]] = []
        self.fail_export = False
        self.generation = 1

    def __call__(self, args: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        self.calls.append((list(args), dict(kwargs)))
        if "--version" in args:
            return subprocess.CompletedProcess(args, 0, "Aseprite 1.3.18.4\n", "")
        if "--list-layer-hierarchy" in args and "--sheet" not in args:
            return subprocess.CompletedProcess(args, 0, "Body\nFX/\n  Glow\n", "")
        if "--list-tags" in args and "--sheet" not in args:
            return subprocess.CompletedProcess(args, 0, "Idle\nAttack\n", "")
        if "--list-slices" in args and "--sheet" not in args:
            return subprocess.CompletedProcess(args, 0, "hurtbox\norigin\n", "")
        if "--sheet" in args:
            sheet = Path(args[args.index("--sheet") + 1])
            data = Path(args[args.index("--data") + 1])
            sheet.parent.mkdir(parents=True, exist_ok=True)
            sheet.write_bytes(PNG_BYTES + bytes([self.generation]))
            data.write_text(
                json.dumps(
                    {
                        "frames": [
                            {
                                "filename": f"frame-{self.generation}",
                                "frame": {"x": 0, "y": 0, "w": 16, "h": 16},
                                "duration": 100,
                            }
                        ],
                        "meta": {
                            "frameTags": [{"name": "Idle", "from": 0, "to": 0}],
                            "layers": [{"name": "Body"}],
                            "slices": [],
                        },
                    }
                ),
                encoding="utf-8",
            )
            if self.fail_export:
                return subprocess.CompletedProcess(args, 9, "", "simulated export failure")
            return subprocess.CompletedProcess(args, 0, "exported\n", "")
        raise AssertionError(f"unexpected subprocess call: {args}")


class BridgeFixture(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name).resolve()
        self.source_root = self.project / ".asset-vault" / "library"
        self.source_root.mkdir(parents=True)
        self.source = self.source_root / "hero.aseprite"
        self.source.write_bytes(b"ASEPRITE-SOURCE-V1")
        self.output_root = self.source_root / "aseprite-generated"
        self.config_path = self.project / ".aseprite-bridge.json"
        self.config_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "source_roots": [".asset-vault/library"],
                    "candidate_output_root": ".asset-vault/library/aseprite-generated",
                    "allowed_source_extensions": [".aseprite", ".ase"],
                    "sheet_type": "rows",
                    "border_padding": 0,
                    "shape_padding": 1,
                    "inner_padding": 0,
                    "timeout_seconds": 60,
                    "use_noinapp": True,
                }
            ),
            encoding="utf-8",
        )
        self.executable = self.project / "Aseprite.exe"
        self.executable.write_bytes(b"fake")
        self.runner = FakeRunner()
        self.config = BridgeConfig.load(self.project, self.config_path)
        self.bridge = AsepriteBridge(
            self.config,
            executable=self.executable,
            runner=self.runner,
            environ={},
        )

    def tearDown(self) -> None:
        self.temp.cleanup()


class BridgeConfigTests(BridgeFixture):
    def test_loads_project_relative_roots(self) -> None:
        self.assertEqual(self.config.project_root, self.project)
        self.assertEqual(self.config.source_roots, (self.source_root.resolve(),))
        self.assertEqual(self.config.candidate_output_root, self.output_root.resolve())

    def test_rejects_absolute_configured_root(self) -> None:
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        data["source_roots"] = [str(self.source_root.resolve())]
        self.config_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(BridgeError) as caught:
            BridgeConfig.load(self.project, self.config_path)

        self.assertEqual(caught.exception.code, "INVALID_CONFIG")

    def test_rejects_missing_source_root_directory(self) -> None:
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        data["source_roots"] = [".asset-vault/missing-library"]
        data["candidate_output_root"] = ".asset-vault/missing-library/generated"
        self.config_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(BridgeError) as caught:
            BridgeConfig.load(self.project, self.config_path)

        self.assertEqual(caught.exception.code, "INVALID_CONFIG")
        self.assertIn("source_root is not a directory", caught.exception.detail)

    def test_rejects_candidate_root_equal_to_project(self) -> None:
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        data["candidate_output_root"] = "."
        self.config_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(BridgeError) as caught:
            BridgeConfig.load(self.project, self.config_path)

        self.assertEqual(caught.exception.code, "INVALID_CONFIG")

    def test_rejects_candidate_root_outside_configured_source_roots(self) -> None:
        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        data["candidate_output_root"] = "assets/_vault_local/aseprite-generated"
        self.config_path.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(BridgeError) as caught:
            BridgeConfig.load(self.project, self.config_path)

        self.assertEqual(caught.exception.code, "INVALID_CONFIG")
        self.assertIn("inside one source_root", caught.exception.detail)

    def test_rejects_symlinked_candidate_root_even_when_target_stays_inside_source_root(self) -> None:
        real_output = self.source_root / "real-generated"
        real_output.mkdir()
        link = self.source_root / "aseprite-generated"
        try:
            link.symlink_to(real_output, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("directory symlinks are unavailable in this environment")

        with self.assertRaises(BridgeError) as caught:
            BridgeConfig.load(self.project, self.config_path)

        self.assertEqual(caught.exception.code, "INVALID_CONFIG")
        self.assertIn("candidate_output_root", caught.exception.detail)

    def test_rejects_source_outside_allowed_roots(self) -> None:
        outside = self.project / "outside.aseprite"
        outside.write_bytes(b"outside")

        with self.assertRaises(BridgeError) as caught:
            self.bridge.inspect(str(outside.relative_to(self.project)))

        self.assertEqual(caught.exception.code, "SOURCE_OUTSIDE_ALLOWED_ROOTS")

    def test_rejects_unsupported_source_extension(self) -> None:
        wrong = self.source_root / "hero.png"
        wrong.write_bytes(PNG_BYTES)

        with self.assertRaises(BridgeError) as caught:
            self.bridge.inspect(str(wrong.relative_to(self.project)))

        self.assertEqual(caught.exception.code, "UNSUPPORTED_SOURCE_EXTENSION")

    def test_rejects_invalid_asset_id(self) -> None:
        with self.assertRaises(BridgeError) as caught:
            self.bridge.export_candidate(
                str(self.source.relative_to(self.project)),
                "../hero",
            )

        self.assertEqual(caught.exception.code, "INVALID_ASSET_ID")

    def test_rejects_windows_reserved_asset_id(self) -> None:
        with self.assertRaises(BridgeError) as caught:
            self.bridge.export_candidate(
                str(self.source.relative_to(self.project)),
                "CON",
            )

        self.assertEqual(caught.exception.code, "INVALID_ASSET_ID")
        self.assertIn("Windows device name", caught.exception.detail)

    def test_rejects_symlinked_source_even_when_target_stays_inside_root(self) -> None:
        target = self.source_root / "real.aseprite"
        target.write_bytes(b"REAL")
        link = self.source_root / "linked.aseprite"
        try:
            link.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("symlinks are unavailable in this environment")

        with self.assertRaises(BridgeError) as caught:
            self.bridge.inspect(str(link.relative_to(self.project)))

        self.assertEqual(caught.exception.code, "SOURCE_SYMLINK_FORBIDDEN")


class AsepriteBridgeTests(BridgeFixture):
    def test_doctor_returns_version_and_uses_no_shell(self) -> None:
        result = self.bridge.doctor()

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["aseprite_version"], "Aseprite 1.3.18.4")
        args, kwargs = self.runner.calls[0]
        self.assertEqual(args, [str(self.executable), "--version"])
        self.assertIs(kwargs["shell"], False)
        self.assertEqual(kwargs["timeout"], 60)

    def test_discovery_prefers_environment_path_after_explicit_is_absent(self) -> None:
        bridge = AsepriteBridge(
            self.config,
            runner=self.runner,
            environ={"ASEPRITE_PATH": str(self.executable)},
        )

        self.assertEqual(bridge.executable, self.executable.resolve())

    def test_inspect_uses_fixed_official_list_commands(self) -> None:
        result = self.bridge.inspect(str(self.source.relative_to(self.project)))

        self.assertEqual(result["layers"], ["Body", "FX/", "Glow"])
        self.assertEqual(result["tags"], ["Idle", "Attack"])
        self.assertEqual(result["slices"], ["hurtbox", "origin"])
        source = str(self.source.resolve())
        expected = [
            [str(self.executable), "-b", "--noinapp", "--list-layer-hierarchy", source],
            [str(self.executable), "-b", "--noinapp", "--list-tags", source],
            [str(self.executable), "-b", "--noinapp", "--list-slices", source],
        ]
        self.assertEqual([call[0] for call in self.runner.calls], expected)
        self.assertTrue(all(call[1]["shell"] is False for call in self.runner.calls))

    def test_export_creates_validated_candidate_and_relative_receipt(self) -> None:
        result = self.bridge.export_candidate(
            str(self.source.relative_to(self.project)),
            "HERO_IDLE_01",
        )

        self.assertEqual(result["status"], "PASS")
        candidate = self.output_root / "HERO_IDLE_01"
        png = candidate / "HERO_IDLE_01.png"
        data = candidate / "HERO_IDLE_01.json"
        receipt_path = candidate / "HERO_IDLE_01.receipt.json"
        self.assertTrue(png.is_file())
        self.assertTrue(data.is_file())
        self.assertTrue(receipt_path.is_file())
        receipt_text = receipt_path.read_text(encoding="utf-8")
        receipt = json.loads(receipt_text)
        self.assertEqual(receipt["asset_id"], "HERO_IDLE_01")
        self.assertEqual(
            receipt["evidence_ceiling"],
            "CLI_EXPORT_AND_READBACK_ONLY_NOT_GODOT_RUNTIME_NOT_HUMAN_APPROVAL",
        )
        self.assertNotIn(str(self.project), receipt_text)
        self.assertEqual(result["receipt"], receipt)

        export_args, export_kwargs = self.runner.calls[-1]
        self.assertIs(export_kwargs["shell"], False)
        self.assertEqual(export_args[0:7], [
            str(self.executable),
            "-b",
            "--noinapp",
            "--list-layer-hierarchy",
            "--list-tags",
            "--list-slices",
            str(self.source.resolve()),
        ])
        self.assertIn("--sheet", export_args)
        self.assertIn("--data", export_args)
        self.assertIn("--format", export_args)
        self.assertIn("json-array", export_args)
        self.assertIn("--sheet-type", export_args)
        self.assertIn("rows", export_args)

    def test_export_fails_when_candidate_exists_without_explicit_replace(self) -> None:
        self.bridge.export_candidate(str(self.source.relative_to(self.project)), "HERO_IDLE_01")

        with self.assertRaises(BridgeError) as caught:
            self.bridge.export_candidate(str(self.source.relative_to(self.project)), "HERO_IDLE_01")

        self.assertEqual(caught.exception.code, "CANDIDATE_EXISTS")

    def test_explicit_replace_publishes_new_valid_candidate(self) -> None:
        first = self.bridge.export_candidate(str(self.source.relative_to(self.project)), "HERO_IDLE_01")
        first_png_hash = first["receipt"]["outputs"][0]["sha256"]
        self.source.write_bytes(b"ASEPRITE-SOURCE-V2")
        self.runner.generation = 2

        second = self.bridge.export_candidate(
            str(self.source.relative_to(self.project)),
            "HERO_IDLE_01",
            replace_candidate=True,
        )

        self.assertNotEqual(first_png_hash, second["receipt"]["outputs"][0]["sha256"])
        self.assertEqual(
            second["receipt"]["source"]["bytes"],
            len(b"ASEPRITE-SOURCE-V2"),
        )
        self.assertFalse(any(path.name.startswith(".HERO_IDLE_01-") for path in self.output_root.iterdir()))

    def test_failed_export_does_not_publish_partial_candidate(self) -> None:
        self.runner.fail_export = True

        with self.assertRaises(BridgeError) as caught:
            self.bridge.export_candidate(str(self.source.relative_to(self.project)), "HERO_IDLE_01")

        self.assertEqual(caught.exception.code, "ASEPRITE_COMMAND_FAILED")
        self.assertFalse((self.output_root / "HERO_IDLE_01").exists())
        if self.output_root.exists():
            self.assertEqual(list(self.output_root.iterdir()), [])

    def test_validate_detects_output_hash_mismatch(self) -> None:
        self.bridge.export_candidate(str(self.source.relative_to(self.project)), "HERO_IDLE_01")
        png = self.output_root / "HERO_IDLE_01" / "HERO_IDLE_01.png"
        png.write_bytes(PNG_BYTES + b"tampered")

        with self.assertRaises(BridgeError) as caught:
            self.bridge.validate_candidate("HERO_IDLE_01")

        self.assertEqual(caught.exception.code, "RECEIPT_MISMATCH")

    def test_validate_detects_source_hash_mismatch(self) -> None:
        self.bridge.export_candidate(str(self.source.relative_to(self.project)), "HERO_IDLE_01")
        self.source.write_bytes(b"tampered source")

        with self.assertRaises(BridgeError) as caught:
            self.bridge.validate_candidate("HERO_IDLE_01")

        self.assertEqual(caught.exception.code, "RECEIPT_MISMATCH")


if __name__ == "__main__":
    unittest.main()
