from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

_SENSITIVE_KEYS = {
    "authorization",
    "apikey",
    "openaiapikey",
    "token",
    "secret",
    "password",
    "cookie",
    "setcookie",
    "proxyauthorization",
    "accesstoken",
    "refreshtoken",
    "clientsecret",
    "githubtoken",
    "bearertoken",
}
_SENSITIVE_SUFFIXES = ("apikey", "token", "secret", "password")


def _normalized_key(value: object) -> str:
    return "".join(character for character in str(value).casefold() if character.isalnum())


def _is_sensitive_key(value: object) -> bool:
    normalized = _normalized_key(value)
    return normalized in _SENSITIVE_KEYS or normalized.endswith(_SENSITIVE_SUFFIXES)


def redact_sensitive(value: Any) -> Any:
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if _is_sensitive_key(key):
                result[str(key)] = "[REDACTED]"
            else:
                result[str(key)] = redact_sensitive(item)
        return result
    if isinstance(value, (list, tuple)):
        return [redact_sensitive(item) for item in value]
    return deepcopy(value)


def canonical_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    clean = redact_sensitive(dict(payload))
    canonical = json.dumps(
        clean,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return {
        **clean,
        "receipt_digest": hashlib.sha256(canonical).hexdigest(),
    }
