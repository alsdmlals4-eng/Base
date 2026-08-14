from __future__ import annotations

import importlib.util
import os
import unittest

from tools.loop_a2_runtime.provider_gate import real_provider_gate


class OpenAITransportRedContractTests(unittest.TestCase):
    def test_bounded_openai_transport_module_exists(self) -> None:
        self.assertIsNotNone(
            importlib.util.find_spec("tools.loop_a2_runtime.openai_transport"),
            "bounded OpenAI A2 transport module is not implemented",
        )

    def test_real_gate_requires_explicit_distinct_builder_and_critic_models(self) -> None:
        keys = (
            "LOOP_A2_REAL_PROVIDER_APPROVED",
            "OPENAI_API_KEY",
            "LOOP_A2_BUILDER_MODEL",
            "LOOP_A2_CRITIC_MODEL",
        )
        previous = {key: os.environ.get(key) for key in keys}
        try:
            os.environ["LOOP_A2_REAL_PROVIDER_APPROVED"] = "1"
            os.environ["OPENAI_API_KEY"] = "test-only-redacted-placeholder"
            os.environ.pop("LOOP_A2_BUILDER_MODEL", None)
            os.environ.pop("LOOP_A2_CRITIC_MODEL", None)
            missing = real_provider_gate()
            self.assertEqual(missing["status"], "USER_DECISION_REQUIRED")
            self.assertEqual(missing["code"], "REAL_PROVIDER_MODELS_NOT_SELECTED")

            os.environ["LOOP_A2_BUILDER_MODEL"] = "MODEL_A"
            os.environ["LOOP_A2_CRITIC_MODEL"] = "MODEL_A"
            same = real_provider_gate()
            self.assertEqual(same["status"], "USER_DECISION_REQUIRED")
            self.assertEqual(same["code"], "REAL_PROVIDER_MODELS_NOT_INDEPENDENT")

            os.environ["LOOP_A2_CRITIC_MODEL"] = "MODEL_B"
            ready = real_provider_gate()
            self.assertEqual(ready["status"], "READY")
            self.assertEqual(ready["code"], "REAL_PROVIDER_GATE_PASS")
        finally:
            for key, value in previous.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value


if __name__ == "__main__":
    unittest.main()
