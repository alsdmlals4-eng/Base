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

    def test_real_paid_provider_remains_forbidden_even_when_legacy_env_is_present(self) -> None:
        old_approval = os.environ.get("LOOP_A2_REAL_PROVIDER_APPROVED")
        old_key = os.environ.get("OPENAI_API_KEY")
        os.environ["LOOP_A2_REAL_PROVIDER_APPROVED"] = "1"
        os.environ["OPENAI_API_KEY"] = "sk-legacy-must-not-authorize"
        try:
            result = real_provider_gate()
        finally:
            if old_approval is None:
                os.environ.pop("LOOP_A2_REAL_PROVIDER_APPROVED", None)
            else:
                os.environ["LOOP_A2_REAL_PROVIDER_APPROVED"] = old_approval
            if old_key is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = old_key
        self.assertEqual(result["status"], "NOT_PLANNED")
        self.assertEqual(result["code"], "PAID_OPENAI_API_FORBIDDEN")
        self.assertNotIn("sk-legacy-must-not-authorize", str(result))

    def test_sensitive_token_variants_are_redacted(self) -> None:
        value = {
            "access_token": "a",
            "refresh-token": "b",
            "client_secret": "c",
            "github_token": "d",
        }
        redacted = redact_sensitive(value)
        self.assertEqual(set(redacted.values()), {"[REDACTED]"})

    def test_single_star_does_not_cross_directory_boundary(self) -> None:
        from tools.loop_a2_runtime.scope import validate_changed_paths
        finding_codes = {
            finding.code
            for finding in validate_changed_paths(
                ("scripts/nested/a.gd",), ("scripts/*.gd",), ()
            )
        }
        self.assertIn("OUT_OF_SCOPE_WRITE", finding_codes)

    def test_double_star_directory_pattern_is_recursive(self) -> None:
        from tools.loop_a2_runtime.scope import validate_changed_paths
        self.assertEqual(
            validate_changed_paths(("scripts/nested/a.gd",), ("scripts/**",), ()),
            (),
        )


if __name__ == "__main__":
    unittest.main()
