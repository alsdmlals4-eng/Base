from __future__ import annotations

import os
import unittest

from tools.loop_a2_runtime.evidence import canonical_receipt, redact_sensitive
from tools.loop_a2_runtime.provider_gate import real_provider_gate


class AdversarialTests(unittest.TestCase):
    def test_sensitive_values_are_redacted_recursively(self) -> None:
        value = {
            "OPENAI_API_KEY": "sk-secret",
            "nested": {"authorization": "Bearer abc", "safe": "ok"},
        }
        redacted = redact_sensitive(value)
        self.assertEqual(redacted["OPENAI_API_KEY"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["authorization"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["safe"], "ok")

    def test_receipt_digest_is_deterministic(self) -> None:
        first = canonical_receipt({"b": 2, "a": 1})
        second = canonical_receipt({"a": 1, "b": 2})
        self.assertEqual(first["receipt_digest"], second["receipt_digest"])

    def test_real_provider_is_fail_closed_without_explicit_approval(self) -> None:
        old_approval = os.environ.pop("LOOP_A2_REAL_PROVIDER_APPROVED", None)
        old_key = os.environ.pop("OPENAI_API_KEY", None)
        try:
            result = real_provider_gate()
        finally:
            if old_approval is not None:
                os.environ["LOOP_A2_REAL_PROVIDER_APPROVED"] = old_approval
            if old_key is not None:
                os.environ["OPENAI_API_KEY"] = old_key
        self.assertEqual(result["status"], "USER_DECISION_REQUIRED")
        self.assertNotIn("credential", str(result).lower())


if __name__ == "__main__":
    unittest.main()
