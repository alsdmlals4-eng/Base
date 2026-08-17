from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

import pytest

from base_tool_contracts import ApprovedAnchorRegistry
from base_tool_contracts.approved_anchor import AnchorEvidenceError


def git(root: Path, *args: str) -> None:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        check=False,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_approved_anchor_registry_load_ownership_and_revalidation_are_cross_platform(tmp_path: Path) -> None:
    root = tmp_path / "project"
    registry_path = root / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    source = root / "art" / "source" / "hero.png"
    registry_path.parent.mkdir(parents=True)
    source.parent.mkdir(parents=True)
    source_bytes = b"approved-anchor-fixture"
    source.write_bytes(source_bytes)
    registry_path.write_text(
        json.dumps(
            {
                "version": 1,
                "entries": [
                    {
                        "project_id": "demo",
                        "source_path": "art/source/hero.png",
                        "figma_node_url": "https://www.figma.com/design/abc123/demo?node-id=1-2",
                        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                        "approval_state": "APPROVED",
                        "evidence": {
                            "kind": "EXPORTED_SNAPSHOT",
                            "ref": "portable-test",
                            "checked_at": "2026-08-15T00:00:00Z",
                        },
                    }
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "Test")
    git(root, "add", "docs/APPROVED_VISUAL_ANCHORS.json", "art/source/hero.png")
    git(root, "commit", "-qm", "approved anchor")

    registry = ApprovedAnchorRegistry.load(registry_path)
    registry.assert_project_owned(root)
    registry.assert_unchanged()

    assert registry.expected_source_sha256(
        project_id="demo",
        source_path="art/source/hero.png",
        figma_node_url="https://www.figma.com/design/abc123/demo?node-id=1-2",
    ) == hashlib.sha256(source_bytes).hexdigest()


def _canonical_visual_anchor_payload(source_bytes: bytes) -> dict[str, object]:
    return {
        "version": 1,
        "purpose": (
            "Project-owned approved visual reference anchors. This registry grants visual-reference "
            "authority only and does not grant PROJECT_ASSET_APPROVED or replace tracked gameplay assets."
        ),
        "entries": [
            {
                "project_id": "urban-legend",
                "subject_id": "kwon_narae",
                "subject_name": "Kwon Narae",
                "anchor_role": "CHARACTER_EXPRESSION_IDENTITY",
                "approval_state": "APPROVED",
                "source_path": "assets/source/mvp043_character_v1/kwon_narae.png",
                "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                "figma_node_url": "https://www.figma.com/design/Z7J3eLeavEytKN20H4HfoP/urban-legend?node-id=33-2",
                "evidence": {
                    "kind": "FIGMA_CONNECTOR",
                    "ref": "node=33:2;bytes=337727;sha256=" + hashlib.sha256(source_bytes).hexdigest(),
                    "checked_at": "2026-08-16T13:51:03Z",
                },
                "product_asset_approval": "NOT_GRANTED",
            }
        ],
    }


def test_approved_anchor_registry_accepts_canonical_visual_metadata(tmp_path: Path) -> None:
    registry_path = tmp_path / "APPROVED_VISUAL_ANCHORS.json"
    source_bytes = b"kwon-narae-approved-anchor"
    registry_path.write_text(
        json.dumps(_canonical_visual_anchor_payload(source_bytes), indent=2) + "\n",
        encoding="utf-8",
    )

    registry = ApprovedAnchorRegistry.load(registry_path)

    assert registry.expected_source_sha256(
        project_id="urban-legend",
        source_path="assets/source/mvp043_character_v1/kwon_narae.png",
        figma_node_url="https://www.figma.com/design/Z7J3eLeavEytKN20H4HfoP/urban-legend?node-id=33-2",
    ) == hashlib.sha256(source_bytes).hexdigest()


def test_approved_anchor_registry_still_rejects_unknown_metadata(tmp_path: Path) -> None:
    registry_path = tmp_path / "APPROVED_VISUAL_ANCHORS.json"
    payload = _canonical_visual_anchor_payload(b"anchor")
    payload["unexpected_contract_escape"] = True
    registry_path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    with pytest.raises(AnchorEvidenceError, match="approved-anchor registry is invalid"):
        ApprovedAnchorRegistry.load(registry_path)


def test_visual_anchor_registry_cannot_grant_product_asset_approval(tmp_path: Path) -> None:
    registry_path = tmp_path / "APPROVED_VISUAL_ANCHORS.json"
    payload = _canonical_visual_anchor_payload(b"anchor")
    payload["entries"][0]["product_asset_approval"] = "GRANTED"  # type: ignore[index]
    registry_path.write_text(json.dumps(payload) + "\n", encoding="utf-8")

    with pytest.raises(AnchorEvidenceError, match="approved-anchor registry is invalid"):
        ApprovedAnchorRegistry.load(registry_path)
