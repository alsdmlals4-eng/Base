from __future__ import annotations

import io
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "tools" / "aseprite-local-bridge"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-09-09-aseprite-local-bridge-design.md"
PLAN = ROOT / "docs" / "superpowers" / "plans" / "2026-09-09-aseprite-local-bridge.md"
DOC_MAP = ROOT / "docs" / "DOCUMENTATION_MAP.md"
GUIDE = ROOT / "docs" / "knowledge" / "game-development" / "ASEPRITE_LOCAL_BRIDGE_GUIDE.md"
SRC = BRIDGE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


class AsepriteLocalBridgeContractTests(unittest.TestCase):
    def test_package_docs_examples_and_windows_onboarding_exist(self) -> None:
        for path in (
            BRIDGE / "pyproject.toml",
            BRIDGE / "README.md",
            BRIDGE / "bridge_config.example.json",
            BRIDGE / "project_profile.example.json",
            BRIDGE / "run_bridge.py",
            BRIDGE / "src" / "aseprite_local_bridge" / "__init__.py",
            BRIDGE / "src" / "aseprite_local_bridge" / "bridge.py",
            BRIDGE / "src" / "aseprite_local_bridge" / "cli.py",
            BRIDGE / "windows" / "Install_Aseprite_Local_Bridge.ps1",
            SPEC,
            PLAN,
            GUIDE,
        ):
            self.assertTrue(path.is_file(), path)

    def test_package_has_no_runtime_dependency_or_network_server(self) -> None:
        pyproject = (BRIDGE / "pyproject.toml").read_text(encoding="utf-8")
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (BRIDGE / "src" / "aseprite_local_bridge").glob("*.py")
        )

        self.assertIn("dependencies = []", pyproject)
        for forbidden in (
            "requests",
            "httpx",
            "websocket",
            "socketserver",
            "run_lua",
            "execute_lua",
            "--script",
            "shell=True",
        ):
            self.assertNotIn(forbidden, source)
        self.assertIn("shell=False", source)

    def test_default_config_matches_local_asset_vault_boundary(self) -> None:
        config = json.loads((BRIDGE / "bridge_config.example.json").read_text(encoding="utf-8"))

        self.assertEqual(config["source_roots"], [".asset-vault/library"])
        self.assertEqual(
            config["candidate_output_root"],
            ".asset-vault/library/aseprite-generated",
        )
        self.assertIs(config["use_noinapp"], True)

    def test_design_records_three_alternatives_and_evidence_ceiling(self) -> None:
        text = SPEC.read_text(encoding="utf-8")

        self.assertIn("live community Aseprite MCP", text)
        self.assertIn("Thin local wrapper over the official Aseprite CLI", text)
        self.assertIn("bounded STDIO MCP", text)
        self.assertIn("CLI_EXPORT_AND_READBACK_ONLY_NOT_GODOT_RUNTIME_NOT_HUMAN_APPROVAL", text)
        self.assertIn("No raw Lua", text)
        self.assertIn("HiGodot", text)

    def test_readme_has_beginner_setup_official_links_and_rollback(self) -> None:
        text = (BRIDGE / "README.md").read_text(encoding="utf-8")

        for expected in (
            "https://www.aseprite.org/docs/cli/",
            "https://developers.openai.com/codex/mcp",
            "ASEPRITE_PATH",
            "doctor",
            "inspect",
            "export-candidate",
            "validate-candidate",
            "PROJECT_ASSET_APPROVED",
            "ASEPRITE_RUNTIME_NOT_RUN",
            "pip uninstall aseprite-local-bridge",
        ):
            self.assertIn(expected, text)

    def test_guide_routes_to_existing_asset_vault_and_godot_owners(self) -> None:
        text = GUIDE.read_text(encoding="utf-8")
        self.assertIn("docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md", text)
        self.assertIn("tools/project_asset_vault.py sync", text)
        self.assertIn("PROJECT_ASSET_APPROVED", text)
        self.assertIn("HiGodot", text)
        self.assertIn("tools/aseprite-local-bridge/README.md", text)
        self.assertNotIn("second Godot authoring authority", text)

    def test_project_profile_preserves_candidate_and_evidence_states(self) -> None:
        profile = json.loads((BRIDGE / "project_profile.example.json").read_text(encoding="utf-8"))

        self.assertEqual(profile["adoption_state"], "CANDIDATE")
        self.assertEqual(profile["exact_bridge_version"], "0.1.0")
        self.assertEqual(profile["validation"]["aseprite_runtime"], "NOT_RUN")
        self.assertEqual(profile["validation"]["godot_runtime"], "NOT_RUN")
        self.assertEqual(profile["validation"]["ux_human"], "NOT_RUN")
        self.assertIn("Separately licensed", profile["license"]["aseprite"])

    def test_readme_does_not_auto_install_mcp_or_godot_addon(self) -> None:
        text = (BRIDGE / "README.md").read_text(encoding="utf-8")

        self.assertIn("REFERENCE_ONLY / TRIAL_CANDIDATE", text)
        self.assertIn("phase 1에서는 별도 서버를 추가하지 않는다", text)
        self.assertIn("Aseprite 브리지는 Godot 파일을 수정하지 않는다", text)
        self.assertNotIn("pip install aseprite-mcp", text)
        self.assertNotIn("uvx aseprite-mcp", text)

    def test_direct_runner_loads_only_the_checked_in_local_package(self) -> None:
        source = (BRIDGE / "run_bridge.py").read_text(encoding="utf-8")

        self.assertIn('Path(__file__).resolve().parent / "src"', source)
        self.assertIn("from aseprite_local_bridge.cli import main", source)
        for forbidden in ("pip", "site-packages", "urllib", "requests", "httpx"):
            self.assertNotIn(forbidden, source)

    def test_windows_installer_rejects_an_explicit_invalid_aseprite_path(self) -> None:
        script = (BRIDGE / "windows" / "Install_Aseprite_Local_Bridge.ps1").read_text(encoding="utf-8")

        explicit_block = script.index('if (-not [string]::IsNullOrWhiteSpace($ExplicitPath))')
        env_lookup = script.index('$env:ASEPRITE_PATH')
        self.assertLess(explicit_block, env_lookup)
        self.assertIn("AsepritePath does not point to a file", script)
        self.assertIn("Asset Vault is not initialized", script)

    def test_package_unit_suite_is_consumed_by_root_regression(self) -> None:
        suite = unittest.defaultTestLoader.discover(str(BRIDGE / "tests"), pattern="test_*.py")
        output = io.StringIO()
        result = unittest.TextTestRunner(stream=output, verbosity=1).run(suite)
        if not result.wasSuccessful():
            self.fail("nested Aseprite bridge unit suite failed:\n" + output.getvalue())
        self.assertGreaterEqual(result.testsRun, 15)

    def test_windows_installer_is_explicit_about_persistence_and_runs_doctor(self) -> None:
        script = (BRIDGE / "windows" / "Install_Aseprite_Local_Bridge.ps1").read_text(encoding="utf-8")

        self.assertIn("PersistAsepritePath", script)
        self.assertIn("[Environment]::SetEnvironmentVariable", script)
        self.assertIn('"doctor"', script)
        self.assertIn("Test-Python311", script)
        self.assertIn('Aseprite_Local_Bridge.ps1', script)
        self.assertIn('`$BridgeArgs = @(`$args)', script)
        self.assertIn('& `$PythonCommand @PythonArgs', script)
        self.assertIn('$PythonCommand = $Python.Command', script)
        self.assertIn('& $PythonCommand @PythonPrefixArgs', script)
        self.assertNotIn('& `$PythonCommand @(`$PythonArgs)', script)
        self.assertIn('run_bridge.py', script)
        self.assertNotIn('site --user-site', script)
        self.assertNotIn('aseprite_local_bridge.pth', script)
        self.assertNotIn('pip install', script)
        self.assertNotIn("Invoke-WebRequest", script)


if __name__ == "__main__":
    unittest.main()
