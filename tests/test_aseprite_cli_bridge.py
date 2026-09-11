from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import stat
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "aseprite_cli_bridge.py"
SPEC = importlib.util.spec_from_file_location("aseprite_cli_bridge", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load aseprite_cli_bridge module spec")
bridge = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bridge
SPEC.loader.exec_module(bridge)


PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"candidate"
METADATA = {"frames": [], "meta": {"app": "fake-aseprite"}}


class BridgeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.project_root = self.root / "project"
        self.project_root.mkdir()
        self.source_root = self.project_root / ".asset-vault" / "library"
        self.source_root.mkdir(parents=True)
        self.source = self.source_root / "hero.aseprite"
        self.source.write_bytes(b"aseprite-source")
        self.executable = bridge.ExecutableInfo(
            path=self.root / "Aseprite.exe", discovery_source="test"
        )
        self.executable.path.write_bytes(b"fake")
        self.config = bridge.load_config(self.project_root, None)

    def _write_profile(self, value: dict[str, object]) -> Path:
        path = self.root / "profile.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def _profile_with_overwrite(self) -> bridge.BridgeConfig:
        profile = self._write_profile({"allow_overwrite": True})
        return bridge.load_config(self.project_root, profile)


def completed(
    args: list[str], stdout: str = "", stderr: str = "", returncode: int = 0
):
    return bridge.subprocess.CompletedProcess(
        args=args, returncode=returncode, stdout=stdout, stderr=stderr
    )


class ConfigurationAndPathTests(BridgeTestCase):
    def test_safe_defaults_and_strict_asset_id(self) -> None:
        self.assertEqual(
            self.config.candidate_output_root,
            self.project_root / ".asset-vault" / "library" / "aseprite-generated",
        )
        self.assertFalse(self.config.allow_overwrite)
        self.assertEqual(self.config.timeout_seconds, 60)
        self.assertEqual(bridge.validate_asset_id("HERO_IDLE_01"), "HERO_IDLE_01")
        for invalid in ("../hero", "hero idle", "hero.png", "", "a" * 65):
            with self.subTest(invalid=invalid):
                with self.assertRaises(bridge.BridgeError):
                    bridge.validate_asset_id(invalid)

    def test_source_outside_project_is_rejected(self) -> None:
        outside = self.root / "outside.aseprite"
        outside.write_bytes(b"outside")
        with self.assertRaises(bridge.BridgeError):
            bridge.resolve_source(self.config, outside)

    def test_wrong_extension_is_rejected(self) -> None:
        png = self.source_root / "not-source.png"
        png.write_bytes(PNG_BYTES)
        with self.assertRaises(bridge.BridgeError):
            bridge.resolve_source(self.config, png)

    def test_profile_rejects_absolute_or_escaping_roots(self) -> None:
        profiles = (
            {"source_roots": ["../outside"]},
            {"candidate_output_root": "../outside"},
            {"candidate_output_root": str((self.root / "absolute").resolve())},
        )
        for value in profiles:
            with self.subTest(profile=value):
                with self.assertRaises(bridge.BridgeError):
                    bridge.load_config(self.project_root, self._write_profile(value))

    def test_profile_rejects_unknown_keys_unsupported_extensions_and_values(self) -> None:
        profiles = (
            {"mystery": True},
            {"allowed_source_extensions": [".png"]},
            {"sheet_type": "freeform"},
            {"timeout_seconds": 0},
            {"timeout_seconds": True},
            {"allow_overwrite": "false"},
            {"adoption_state": "PRODUCTION_READY"},
        )
        for value in profiles:
            with self.subTest(profile=value):
                with self.assertRaises(bridge.BridgeError):
                    bridge.load_config(self.project_root, self._write_profile(value))

    def test_profile_accepts_base_adoption_states(self) -> None:
        for value in (
            "CANDIDATE",
            "TRIAL_APPROVED",
            "ADOPTED_ACTIVE",
            "ADOPTED_DISABLED",
            "DEFERRED",
            "REJECTED",
            "INSTALLED_UNUSED",
            "REMOVAL_PENDING",
            "REMOVED",
        ):
            with self.subTest(state=value):
                config = bridge.load_config(
                    self.project_root, self._write_profile({"adoption_state": value})
                )
                self.assertEqual(config.adoption_state, value)

    def test_source_symlink_is_rejected_even_when_target_is_inside_allowed_root(self) -> None:
        link = self.source_root / "linked.aseprite"
        try:
            link.symlink_to(self.source)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        with self.assertRaises(bridge.BridgeError):
            bridge.resolve_source(self.config, link)

    def test_profile_symlink_root_is_rejected_even_when_target_is_inside_project(self) -> None:
        real_root = self.project_root / "real-source"
        real_root.mkdir()
        link_root = self.project_root / "linked-source"
        try:
            link_root.symlink_to(real_root, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")
        profile = self._write_profile({"source_roots": ["linked-source"]})
        with self.assertRaises(bridge.BridgeError):
            bridge.load_config(self.project_root, profile)

    def test_link_like_helper_recognizes_windows_junction_contract(self) -> None:
        path = self.project_root / "junction-like"
        with unittest.mock.patch.object(
            Path,
            "is_junction",
            autospec=True,
            return_value=True,
            create=True,
        ):
            self.assertTrue(bridge._is_link_like(path))


class DiscoveryAndInspectionTests(BridgeTestCase):
    def test_explicit_executable_wins_over_environment(self) -> None:
        explicit = self.root / "explicit.exe"
        environment = self.root / "environment.exe"
        explicit.write_bytes(b"explicit")
        environment.write_bytes(b"environment")
        result = bridge.discover_aseprite(
            explicit, {"ASEPRITE_PATH": str(environment), "PATH": ""}
        )
        self.assertEqual(result.path, explicit.resolve())
        self.assertEqual(result.discovery_source, "explicit")

    def test_environment_wins_over_path(self) -> None:
        environment = self.root / "environment.exe"
        environment.write_bytes(b"environment")
        with unittest.mock.patch.object(bridge.shutil, "which") as which:
            result = bridge.discover_aseprite(
                None, {"ASEPRITE_PATH": str(environment), "PATH": "ignored"}
            )
        which.assert_not_called()
        self.assertEqual(result.path, environment.resolve())
        self.assertEqual(result.discovery_source, "environment")

    def test_missing_explicit_executable_fails_without_fallback(self) -> None:
        fallback = self.root / "fallback.exe"
        fallback.write_bytes(b"fallback")
        with self.assertRaises(bridge.BridgeError):
            bridge.discover_aseprite(
                self.root / "missing.exe",
                {"ASEPRITE_PATH": str(fallback), "PATH": ""},
            )

    def test_inspect_uses_fixed_read_only_command_and_redacted_paths(self) -> None:
        metadata = {"frames": [], "meta": {"layers": [], "tags": [], "slices": []}}
        calls: list[list[str]] = []

        def run_side_effect(args, **kwargs):
            calls.append(list(args))
            if list(args)[1:] == ["--version"]:
                return completed(list(args), stdout="Aseprite 1.3-test\n")
            return completed(list(args), stdout=json.dumps(metadata))

        with unittest.mock.patch.object(
            bridge.subprocess, "run", side_effect=run_side_effect
        ):
            result = bridge.inspect_source(self.config, self.executable, self.source)

        self.assertEqual(result["source"], ".asset-vault/library/hero.aseprite")
        self.assertNotIn(str(self.project_root), json.dumps(result))
        self.assertEqual(result["metadata"], metadata)
        self.assertEqual(
            calls[1],
            [
                str(self.executable.path),
                "-b",
                "--list-layer-hierarchy",
                "--list-tags",
                "--list-slices",
                "--data=",
                str(self.source),
            ],
        )

    def test_inspect_rejects_non_json_output(self) -> None:
        with unittest.mock.patch.object(
            bridge.subprocess,
            "run",
            side_effect=(
                completed(["version"], stdout="Aseprite 1.3-test\n"),
                completed(["inspect"], stdout="not-json"),
            ),
        ):
            with self.assertRaises(bridge.BridgeError):
                bridge.inspect_source(self.config, self.executable, self.source)


class ExportAndReceiptTests(BridgeTestCase):
    def _run_effect(self, calls: list[list[str]]):
        def side_effect(args, **kwargs):
            values = list(args)
            calls.append(values)
            if values[1:] == ["--version"]:
                return completed(values, stdout="Aseprite 1.3-test\n")
            png = Path(values[values.index("--sheet") + 1])
            data = Path(values[values.index("--data") + 1])
            png.write_bytes(PNG_BYTES)
            data.write_text(json.dumps(METADATA), encoding="utf-8")
            return completed(values)

        return side_effect

    def test_export_requires_profile_permission_and_explicit_overwrite(self) -> None:
        candidate = bridge.resolve_candidate_dir(self.config, "HERO_IDLE_01")
        candidate.mkdir(parents=True)
        (candidate / "HERO_IDLE_01.png").write_bytes(b"existing")

        with self.assertRaises(bridge.BridgeError):
            bridge.export_candidate(
                self.config, self.executable, self.source, "HERO_IDLE_01"
            )
        with self.assertRaises(bridge.BridgeError):
            bridge.export_candidate(
                self.config,
                self.executable,
                self.source,
                "HERO_IDLE_01",
                overwrite=True,
            )

    def test_export_rejects_link_like_final_output_even_with_explicit_overwrite(self) -> None:
        config = self._profile_with_overwrite()
        candidate = bridge.resolve_candidate_dir(config, "HERO_IDLE_01")
        candidate.mkdir(parents=True)
        target = self.project_root / "protected.png"
        target.write_bytes(b"protected")
        linked_output = candidate / "HERO_IDLE_01.png"
        try:
            linked_output.symlink_to(target)
        except OSError as error:
            self.skipTest(f"symlink creation unavailable: {error}")

        with unittest.mock.patch.object(bridge.subprocess, "run") as run:
            with self.assertRaises(bridge.BridgeError) as context:
                bridge.export_candidate(
                    config,
                    self.executable,
                    self.source,
                    "HERO_IDLE_01",
                    overwrite=True,
                )

        run.assert_not_called()
        self.assertEqual(target.read_bytes(), b"protected")
        self.assertIn("symlink", str(context.exception).lower())

    def test_export_creates_valid_candidate_and_redacted_receipt(self) -> None:
        calls: list[list[str]] = []
        with unittest.mock.patch.object(
            bridge.subprocess, "run", side_effect=self._run_effect(calls)
        ):
            result = bridge.export_candidate(
                self.config, self.executable, self.source, "HERO_IDLE_01"
            )

        candidate = bridge.resolve_candidate_dir(self.config, "HERO_IDLE_01")
        png = candidate / "HERO_IDLE_01.png"
        metadata = candidate / "HERO_IDLE_01.json"
        receipt_path = candidate / "HERO_IDLE_01.receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(png.read_bytes(), PNG_BYTES)
        self.assertEqual(json.loads(metadata.read_text(encoding="utf-8")), METADATA)
        self.assertEqual(receipt["source_sha256"], bridge.sha256_file(self.source))
        self.assertEqual(receipt["outputs"]["spritesheet_png"]["sha256"], bridge.sha256_file(png))
        self.assertEqual(receipt["outputs"]["metadata_json"]["sha256"], bridge.sha256_file(metadata))
        self.assertNotIn(str(self.project_root), json.dumps(receipt))
        self.assertNotIn(str(self.executable.path), json.dumps(receipt))

        export_command = calls[1]
        source_index = export_command.index(str(self.source))
        sheet_index = export_command.index("--sheet")
        self.assertLess(source_index, sheet_index)
        self.assertNotIn("--list-layers", export_command)
        for expected in (
            "-b",
            "--list-layer-hierarchy",
            "--list-tags",
            "--list-slices",
            "--sheet",
            "--data",
            "--format",
            "json-array",
            "--sheet-type",
            "rows",
        ):
            self.assertIn(expected, export_command)

    def test_validate_detects_output_drift(self) -> None:
        with unittest.mock.patch.object(
            bridge.subprocess, "run", side_effect=self._run_effect([])
        ):
            bridge.export_candidate(
                self.config, self.executable, self.source, "HERO_IDLE_01"
            )
        candidate = bridge.resolve_candidate_dir(self.config, "HERO_IDLE_01")
        (candidate / "HERO_IDLE_01.png").write_bytes(PNG_BYTES + b"changed")
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_candidate(self.config, "HERO_IDLE_01")

    def test_validate_rejects_weakened_command_contract(self) -> None:
        with unittest.mock.patch.object(
            bridge.subprocess, "run", side_effect=self._run_effect([])
        ):
            bridge.export_candidate(
                self.config, self.executable, self.source, "HERO_IDLE_01"
            )
        candidate = bridge.resolve_candidate_dir(self.config, "HERO_IDLE_01")
        receipt_path = candidate / "HERO_IDLE_01.receipt.json"
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["command_contract"]["arbitrary_lua"] = True
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        with self.assertRaises(bridge.BridgeError):
            bridge.validate_candidate(self.config, "HERO_IDLE_01")

    def test_overwrite_replaces_all_candidate_files_when_double_gated(self) -> None:
        config = self._profile_with_overwrite()
        calls: list[list[str]] = []
        with unittest.mock.patch.object(
            bridge.subprocess, "run", side_effect=self._run_effect(calls)
        ):
            bridge.export_candidate(
                config, self.executable, self.source, "HERO_IDLE_01"
            )
        candidate = bridge.resolve_candidate_dir(config, "HERO_IDLE_01")
        old_receipt = (candidate / "HERO_IDLE_01.receipt.json").read_bytes()
        with unittest.mock.patch.object(
            bridge.subprocess, "run", side_effect=self._run_effect(calls)
        ):
            result = bridge.export_candidate(
                config,
                self.executable,
                self.source,
                "HERO_IDLE_01",
                overwrite=True,
            )
        self.assertEqual(result["status"], "PASS")
        self.assertTrue((candidate / "HERO_IDLE_01.png").is_file())
        self.assertTrue((candidate / "HERO_IDLE_01.json").is_file())
        self.assertNotEqual(
            (candidate / "HERO_IDLE_01.receipt.json").read_bytes(), b""
        )
        self.assertGreaterEqual(len(old_receipt), 1)


class CommandLineTests(BridgeTestCase):
    def test_doctor_prints_json_and_returns_zero(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with unittest.mock.patch.object(
            bridge,
            "discover_aseprite",
            return_value=self.executable,
        ), unittest.mock.patch.object(
            bridge,
            "read_aseprite_version",
            return_value="Aseprite 1.3-test",
        ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = bridge.main(
                ["doctor", "--project-root", str(self.project_root)]
            )
        self.assertEqual(status, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["operation"], "doctor")
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(stderr.getvalue(), "")

    def test_bridge_error_is_concise_and_returns_two(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with unittest.mock.patch.object(
            bridge,
            "discover_aseprite",
            side_effect=bridge.BridgeError("not installed"),
        ), contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            status = bridge.main(
                ["doctor", "--project-root", str(self.project_root)]
            )
        self.assertEqual(status, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(
            stderr.getvalue(), "ASEPRITE_BRIDGE_ERROR: not installed\n"
        )
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_export_overwrite_flag_is_explicit(self) -> None:
        parser = bridge.build_parser()
        default = parser.parse_args(
            [
                "export",
                "--source",
                "hero.aseprite",
                "--asset-id",
                "HERO_IDLE_01",
            ]
        )
        explicit = parser.parse_args(
            [
                "export",
                "--source",
                "hero.aseprite",
                "--asset-id",
                "HERO_IDLE_01",
                "--overwrite",
            ]
        )
        self.assertFalse(default.overwrite)
        self.assertTrue(explicit.overwrite)


class ProcessBoundaryCanaryTests(BridgeTestCase):
    @unittest.skipIf(os.name == "nt", "POSIX fake executable canary")
    def test_real_fake_executable_process_supports_all_commands(self) -> None:
        fake = self.root / "fake-aseprite"
        fake.write_text(
            """#!/usr/bin/env python3
import json
import pathlib
import sys

args = sys.argv[1:]
if args == ["--version"]:
    print("Aseprite 1.3-fake")
    raise SystemExit(0)
if "--sheet" in args and "--data" in args:
    png = pathlib.Path(args[args.index("--sheet") + 1])
    data = pathlib.Path(args[args.index("--data") + 1])
    png.write_bytes(bytes.fromhex("89504e470d0a1a0a") + b"fake")
    data.write_text(json.dumps({"frames": [], "meta": {"app": "fake"}}), encoding="utf-8")
    raise SystemExit(0)
if "--data=" in args:
    print(json.dumps({"frames": [], "meta": {"app": "fake"}}))
    raise SystemExit(0)
print("unexpected arguments", args, file=sys.stderr)
raise SystemExit(9)
""",
            encoding="utf-8",
        )
        fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
        executable = bridge.discover_aseprite(fake, {})
        self.assertEqual(
            bridge.read_aseprite_version(executable, 10), "Aseprite 1.3-fake"
        )
        inspected = bridge.inspect_source(self.config, executable, self.source)
        self.assertEqual(inspected["metadata"]["meta"]["app"], "fake")
        exported = bridge.export_candidate(
            self.config, executable, self.source, "HERO_IDLE_01"
        )
        self.assertEqual(exported["status"], "PASS")
        validated = bridge.validate_candidate(self.config, "HERO_IDLE_01")
        self.assertEqual(validated["status"], "PASS")


class RepositoryArtifactContractTests(unittest.TestCase):
    def test_checked_in_profile_loads_with_safe_candidate_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(temporary_directory)
            profile = (
                ROOT
                / "templates"
                / "project-operations"
                / "ASEPRITE_LOCAL_BRIDGE_PROFILE.json"
            )
            config = bridge.load_config(project_root, profile)
        self.assertEqual(config.adoption_state, "CANDIDATE")
        self.assertEqual(
            config.candidate_output_root,
            project_root
            / ".asset-vault"
            / "library"
            / "aseprite-generated",
        )
        self.assertFalse(config.allow_overwrite)
        self.assertEqual(config.allowed_source_extensions, (".aseprite", ".ase"))

    def test_guide_uses_project_profile_after_copy_and_resets_overwrite(self) -> None:
        guide = (
            ROOT
            / "docs"
            / "knowledge"
            / "game-development"
            / "ASEPRITE_LOCAL_CLI_BRIDGE_GUIDE.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            '$Profile = Join-Path $ProjectRoot "config\\tools\\aseprite-local-bridge.json"',
            guide,
        )
        self.assertIn("$Config.allow_overwrite = $false", guide)
        self.assertIn("python $VaultTool sync --project-root $ProjectRoot", guide)
        post_copy = guide.split("## 7. `.aseprite` 원본 준비", maxsplit=1)[1]
        self.assertNotIn(
            "templates\\project-operations\\ASEPRITE_LOCAL_BRIDGE_PROFILE.json",
            post_copy,
        )
        self.assertNotIn("$TargetProfile", post_copy)


if __name__ == "__main__":
    unittest.main()
