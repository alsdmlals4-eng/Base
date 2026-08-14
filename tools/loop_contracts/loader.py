from __future__ import annotations

import json
from pathlib import Path


def resolve_project_relative(root: Path, relative: str) -> Path:
    normalized = relative.replace("\\", "/")
    raw = Path(normalized)
    if not normalized or normalized.startswith("/") or ":/" in normalized[:3] or ".." in raw.parts:
        raise ValueError(relative)
    resolved_root = root.resolve(strict=True)
    candidate = (resolved_root / raw).resolve(strict=False)
    if candidate != resolved_root and resolved_root not in candidate.parents:
        raise ValueError(relative)
    return candidate


def load_object(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value
