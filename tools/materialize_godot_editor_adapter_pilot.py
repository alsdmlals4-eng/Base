from __future__ import annotations

import json
import shutil
from pathlib import Path

from tools.godot_editor_adapter_materialization import (
    build_configured_manifest,
    copy_canonical_addon,
    sha256_file,
)


FIXTURE_RELATIVE = Path("examples/godot-live-editor-v2-editor-pilot")
MANIFEST_NAME = "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"


def materialize(source_root: Path, destination: Path) -> Path:
    source_root = Path(source_root).resolve()
    destination = Path(destination).resolve()
    fixture = source_root / FIXTURE_RELATIVE
    if not fixture.is_dir():
        raise FileNotFoundError(f"missing Pilot fixture: {fixture}")
    if destination.exists():
        raise FileExistsError(f"destination already exists: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        fixture,
        destination,
        ignore=shutil.ignore_patterns(".godot", "artifacts", "*.uid"),
    )
    copy_canonical_addon(source_root, destination)
    for generated in destination.rglob("*.uid"):
        generated.unlink()

    project_file = destination / "project.godot"
    manifest = build_configured_manifest(destination, sha256_file(project_file))
    (destination / MANIFEST_NAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return destination


__all__ = ["materialize"]
