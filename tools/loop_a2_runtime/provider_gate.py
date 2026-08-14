from __future__ import annotations

import os
from typing import Any


def real_provider_gate() -> dict[str, Any]:
    approved = os.environ.get("LOOP_A2_REAL_PROVIDER_APPROVED") == "1"
    configured = bool(os.environ.get("OPENAI_API_KEY"))
    if not approved or not configured:
        return {
            "status": "USER_DECISION_REQUIRED",
            "code": "REAL_PROVIDER_NOT_APPROVED",
            "message": "Explicit paid-provider approval and configured transport are required.",
        }

    builder_model = os.environ.get("LOOP_A2_BUILDER_MODEL", "").strip()
    critic_model = os.environ.get("LOOP_A2_CRITIC_MODEL", "").strip()
    if not builder_model or not critic_model:
        return {
            "status": "USER_DECISION_REQUIRED",
            "code": "REAL_PROVIDER_MODELS_NOT_SELECTED",
            "message": "Explicit Builder and independent Critic model selections are required.",
        }
    if builder_model == critic_model:
        return {
            "status": "USER_DECISION_REQUIRED",
            "code": "REAL_PROVIDER_MODELS_NOT_INDEPENDENT",
            "message": "Builder and Critic model selections must be distinct.",
        }

    return {
        "status": "READY",
        "code": "REAL_PROVIDER_GATE_PASS",
        "message": "Provider transport gate passed; model behavior is still unverified.",
    }
