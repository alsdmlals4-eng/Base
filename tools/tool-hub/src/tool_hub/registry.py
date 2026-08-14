"""Read the single reviewed Base tool registry owner."""

from __future__ import annotations

from pathlib import Path
from types import ModuleType

from .runtime_trust import RuntimeTrustError, assert_committed_file, capture_runtime_pins


class HubRegistryError(ValueError):
    pass


def load_reviewed_tools(base_root: Path) -> tuple[dict[str, object], ...]:
    root = base_root.resolve()
    try:
        validator_relative = Path("tools/validate_tool_registry.py")
        validator_bytes = assert_committed_file(root, validator_relative)
        assert_committed_file(root, Path("tools/TOOL_REGISTRY.json"))
        assert_committed_file(root, Path("schemas/base-tool-registry-v1.schema.json"))
    except RuntimeTrustError as error:
        raise HubRegistryError("reviewed tool registry is invalid") from error
    validator_path = root / "tools" / "validate_tool_registry.py"
    module = ModuleType("base_tool_registry_validator")
    module.__file__ = str(validator_path)
    exec(compile(validator_bytes, str(validator_path), "exec"), module.__dict__)
    try:
        reviewed = module.load_registry(base_root, base_root / "tools" / "TOOL_REGISTRY.json")
        interpreter = root / ".venv" / "bin" / "python"
        pinned: list[dict[str, object]] = []
        for raw in reviewed:
            tool = dict(raw)
            tool.update(capture_runtime_pins(root, str(tool["owner_path"]), interpreter))
            pinned.append(tool)
        return tuple(pinned)
    except (OSError, ValueError, RuntimeTrustError) as error:
        raise HubRegistryError("reviewed tool registry is invalid") from error
