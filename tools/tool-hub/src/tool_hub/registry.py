"""Read the single reviewed Base tool registry owner."""

from __future__ import annotations

import importlib.util
from pathlib import Path


class HubRegistryError(ValueError):
    pass


def load_reviewed_tools(base_root: Path) -> tuple[dict[str, object], ...]:
    validator_path = base_root.resolve() / "tools" / "validate_tool_registry.py"
    spec = importlib.util.spec_from_file_location("base_tool_registry_validator", validator_path)
    if spec is None or spec.loader is None:
        raise HubRegistryError("reviewed tool registry validator is unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        return module.load_registry(base_root, base_root / "tools" / "TOOL_REGISTRY.json")
    except (OSError, ValueError) as error:
        raise HubRegistryError("reviewed tool registry is invalid") from error
