from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

from base_tool_contracts import ApprovedAnchorRegistry


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
