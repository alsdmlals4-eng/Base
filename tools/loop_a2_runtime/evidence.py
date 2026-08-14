from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

_SENSITIVE = {
    "authorization", "api_key", "openai_api_key", "token", "secret", "password",
    "cookie", "set-cookie", "proxy-authorization",
}


def redact_sensitive(value: Any) -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if str(key).casefold().replace("-", "_") in {name.replace("-", "_") for name in _SENSITIVE}:
                result[str(key)] = "[REDACTED]"
            else:
                result[str(key)] = redact_sensitive(item)
        return result
    if isinstance(value, (list, tuple)):
        return [redact_sensitive(item) for item in value]
    return deepcopy(value)


def canonical_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    clean = redact_sensitive(dict(payload))
    canonical = json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {**clean, "receipt_digest": hashlib.sha256(canonical).hexdigest()}
