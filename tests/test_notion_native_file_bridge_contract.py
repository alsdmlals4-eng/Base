from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BRIDGE = ROOT / "tools" / "notion-native-file-bridge"
SPEC = ROOT / "docs" / "superpowers" / "specs" / "2026-08-22-notion-native-file-bridge-design.md"
LAYOUT = ROOT / "docs" / "knowledge" / "game-development" / "NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md"
CI = ROOT / ".github" / "workflows" / "validate-game-project-operating-system.yml"
SRC = BRIDGE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from notion_native_file_bridge.ntn import NOTION_VERSION, NtnClient  # noqa: E402


class QueueRunner:
    def __init__(self, responses: list[subprocess.CompletedProcess[bytes]]) -> None:
        self.responses = list(responses)
        self.calls: list[list[str]] = []

    def __call__(self, args: list[str], **_: object) -> subprocess.CompletedProcess[bytes]:
        self.calls.append(list(args))
        if not self.responses:
            raise AssertionError(f"unexpected subprocess call: {args}")
        return self.responses.pop(0)


def completed(stdout: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.CompletedProcess(["ntn"], 0, stdout.encode("utf-8"), b"")


class NotionNativeFileBridgeContractTests(unittest.TestCase):
    def test_bridge_package_and_windows_onboarding_exist(self) -> None:
        for path in (
            BRIDGE / "pyproject.toml",
            BRIDGE / "src" / "notion_native_file_bridge" / "ntn.py",
            BRIDGE / "src" / "notion_native_file_bridge" / "cli.py",
            BRIDGE / "README.md",
            BRIDGE / "windows" / "Install_Notion_Native_File_Bridge.ps1",
        ):
            self.assertTrue(path.is_file(), path)

    def test_design_uses_official_ntn_and_preserves_device_evidence_ceiling(self) -> None:
        text = SPEC.read_text(encoding="utf-8")
        self.assertIn("official `ntn` CLI", text)
        self.assertIn("READBACK_PASS != HUMAN_VISIBLE_PASS", text)
        self.assertIn("No replacement for Notion MCP", text)
        self.assertIn("No external image CDN", text)

    def test_transport_has_no_custom_python_http_stack(self) -> None:
        pyproject = (BRIDGE / "pyproject.toml").read_text(encoding="utf-8")
        source = (BRIDGE / "src" / "notion_native_file_bridge" / "ntn.py").read_text(encoding="utf-8")

        self.assertIn('dependencies = []', pyproject)
        self.assertNotIn("requests", source)
        self.assertNotIn("httpx", source)
        self.assertNotIn("urllib.request", source)
        self.assertIn('"ntn"', source)

    def test_core_regression_executes_real_typed_image_command_construction(self) -> None:
        runner = QueueRunner(
            [
                completed('{"object":"list","results":[{"id":"block-1","type":"image"}]}'),
                completed('{"object":"block","id":"block-1","type":"image","image":{"type":"file"}}'),
            ]
        )
        client = NtnClient(executable="ntn", runner=runner)

        result = client.append_image("page-1", "upload-1")

        self.assertEqual(result["status"], "PASS")
        self.assertIn("children[0][image][type]=file_upload", runner.calls[0])
        self.assertIn("children[0][image][file_upload][id]=upload-1", runner.calls[0])
        self.assertEqual(
            runner.calls[1],
            ["ntn", "api", "v1/blocks/block-1", "--notion-version", NOTION_VERSION],
        )

    def test_visual_layout_contract_routes_binary_media_without_false_android_pass(self) -> None:
        text = LAYOUT.read_text(encoding="utf-8")
        self.assertIn("Notion Native File Bridge", text)
        self.assertIn("typed `file_upload`", text)
        self.assertIn("Android", text)
        self.assertIn("HUMAN_VISIBLE_PASS", text)
        self.assertIn("external host/CDN", text)

    def test_core_regression_discovers_root_test_suite(self) -> None:
        text = CI.read_text(encoding="utf-8")
        self.assertIn("python -m unittest discover -s tests -v", text)


if __name__ == "__main__":
    unittest.main()
