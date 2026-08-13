import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from tools.validate_tool_registry import RegistryError, load_registry


ROOT = Path(__file__).resolve().parents[1]


def _registry(tmp_path: Path, tools: list[dict[str, object]]) -> Path:
    path = tmp_path / "TOOL_REGISTRY.json"
    path.write_text(json.dumps({"schema_version": 1, "tools": tools}), encoding="utf-8")
    return path


def _entry(**overrides: object) -> dict[str, object]:
    entry: dict[str, object] = {
        "tool_id": "qa-evidence-studio",
        "display_name": "QA Evidence Studio",
        "audience": "HUMAN_INTERACTIVE",
        "owner_path": "tools/qa-evidence-studio",
        "launch_adapter": "qa_evidence_studio",
        "health_path": "/api/status",
        "project_scoped": True,
        "capabilities": ["developer_pc_review", "image_evidence"],
        "production_engine_required_for_delivery": False,
    }
    entry.update(overrides)
    return entry


def test_current_reviewed_registry_loads_only_human_interactive_tools() -> None:
    tools = load_registry(ROOT, ROOT / "tools" / "TOOL_REGISTRY.json")

    assert [item["tool_id"] for item in tools] == [
        "expression-studio",
        "qa-evidence-studio",
        "sprite-animation-studio",
    ]


def test_current_registry_conforms_to_its_single_schema_owner() -> None:
    schema = json.loads((ROOT / "schemas" / "base-tool-registry-v1.schema.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "tools" / "TOOL_REGISTRY.json").read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(registry)


@pytest.mark.parametrize(
    "mutation, message",
    [
        ({"command": "python -m anything"}, "unknown field"),
        ({"owner_path": "/tmp/tool"}, "relative"),
        ({"owner_path": "tools/../outside"}, "traversal"),
        ({"launch_adapter": "arbitrary_shell"}, "adapter"),
        ({"owner_path": "tools/does-not-exist"}, "owner"),
    ],
)
def test_registry_rejects_unreviewed_execution_surfaces(
    tmp_path: Path, mutation: dict[str, object], message: str
) -> None:
    with pytest.raises(RegistryError, match=message):
        load_registry(ROOT, _registry(tmp_path, [_entry(**mutation)]))


def test_registry_rejects_duplicate_tool_ids(tmp_path: Path) -> None:
    with pytest.raises(RegistryError, match="duplicate"):
        load_registry(ROOT, _registry(tmp_path, [_entry(), _entry()]))
