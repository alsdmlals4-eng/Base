"""Regression for connected-tool discovery; not proof that any external action succeeded."""
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ConnectedToolCapabilityDiscoveryContractTests(unittest.TestCase):
    def test_unavailable_claim_requires_discovery_attempt_and_specific_failure_class(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for token in [
            "CONNECTED_TOOL_CAPABILITY_DISCOVERY_BEFORE_UNAVAILABLE_CLAIM",
            "api_tool.list_resources",
            "SCHEMA_NOT_LOADED",
            "CONNECTOR_NOT_CONNECTED",
            "PERMISSION_DENIED",
            "RULESET_OR_REQUIRED_CHECK_BLOCKED",
            "ACTION_UNSUPPORTED",
            "NO_NEW_PLUGIN_WHEN_CONNECTED_CAPABILITY_EXISTS",
            "actual connector attempt",
        ]:
            with self.subTest(token=token):
                self.assertIn(token, text)

    def test_discovery_is_not_reported_as_write_or_merge_success(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("DISCOVERY_IS_NOT_EXECUTION_EVIDENCE", text)
        self.assertIn("branch/ref mutation", text)
        self.assertIn("exact HEAD", text)


if __name__ == "__main__":
    unittest.main()
