from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SUITE = ROOT / "Base Tool Hub" / "TOOL_SUITE.json"
REGISTRY = ROOT / "tools" / "TOOL_REGISTRY.json"


def test_suite_manifest_points_to_single_existing_runtime_owners() -> None:
    payload = json.loads(SUITE.read_text(encoding="utf-8"))

    assert payload["suite_root_role"] == "CANONICAL_SUITE_NAVIGATION_AND_MANIFEST"
    assert payload["implementation_policy"] == {
        "single_source_of_truth": True,
        "runtime_source_root": "tools",
        "duplicate_source_trees_allowed": False,
        "symlink_aliases_allowed": False,
        "physical_relocation_state": "DEFERRED_TO_REGISTRY_V2_MIGRATION",
    }

    implementation_paths = []
    for tool in payload["tools"]:
        entry = ROOT / tool["suite_entry"]
        assert entry.is_file()
        assert not entry.is_symlink()
        implementation = tool["implementation_path"]
        if implementation is None:
            continue
        owner = ROOT / implementation
        assert owner.is_dir()
        assert not owner.is_symlink()
        implementation_paths.append(implementation)

    assert len(implementation_paths) == len(set(implementation_paths))


def test_character_studio_suite_entry_matches_reviewed_registry_capabilities() -> None:
    suite = json.loads(SUITE.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    character = next(tool for tool in suite["tools"] if tool["logical_name"] == "Character Studio")
    reviewed = next(tool for tool in registry["tools"] if tool["tool_id"] == "expression-studio")

    assert character["implementation_path"] == reviewed["owner_path"] == "tools/expression-studio"
    assert reviewed["display_name"] == "Character Studio"
    assert reviewed["capabilities"] == [
        "expression_variation",
        "identity_preserving_edit",
        "outfit_variation",
        "scene_relocation",
        "image_import",
        "figma_delivery_packet",
    ]


def test_suite_manifest_does_not_overclaim_direct_local_figma_upload() -> None:
    payload = json.loads(SUITE.read_text(encoding="utf-8"))

    assert payload["figma_delivery"]["registered_projects"] == 8
    assert payload["figma_delivery"]["live_write_readback_verified"] == 8
    assert payload["figma_delivery"]["local_tool_direct_upload"] is False
