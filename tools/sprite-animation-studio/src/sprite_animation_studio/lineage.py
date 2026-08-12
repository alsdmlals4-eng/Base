"""Durable visual-lineage records for review and downstream handoff."""

import hashlib
import json
from pathlib import Path

from .models import SpriteAnimationRequest


def write_lineage(request: SpriteAnimationRequest, anchor_bytes: bytes, output_dir: Path) -> Path:
    """Write a stable record tying an accepted anchor to its Figma source."""
    output_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "action": request.action.model_dump(mode="json"),
        "anchor": {
            "approval_status": request.anchor.approval_status,
            "figma_node_url": str(request.anchor.figma_node_url),
            "sha256": hashlib.sha256(anchor_bytes).hexdigest(),
            "source_path": request.anchor.source_path,
        },
        "asset_id": request.asset_id,
        "asset_kind": request.asset_kind,
        "output_root": request.output_root,
        "project_id": request.project_id,
    }
    target = output_dir / "lineage.json"
    target.write_text(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target
