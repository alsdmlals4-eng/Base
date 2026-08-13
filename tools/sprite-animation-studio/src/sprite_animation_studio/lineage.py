"""Durable visual-lineage records for review and downstream handoff."""

import hashlib
import json
from pathlib import Path
from base_tool_contracts import safe_staging_write_text

from .models import SpriteAnimationRequest


def write_lineage(request: SpriteAnimationRequest, anchor_bytes: bytes, output_dir: Path, *, engine: dict[str, object], anchor_verification: str = "ANCHOR_UNVERIFIED", anchor_evidence: dict[str, str] | None = None, imported_images: list[dict[str, object]] | None = None, run_mode: str = "simulated") -> Path:
    """Write a stable record tying an accepted anchor to its Figma source."""
    output_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "action": request.action.model_dump(mode="json"),
        "anchor": {
            "approval_status": request.anchor.approval_status,
            "verification_state": anchor_verification,
            "evidence": anchor_evidence or {},
            "figma_node_url": str(request.anchor.figma_node_url),
            "sha256": hashlib.sha256(anchor_bytes).hexdigest(),
            "source_path": request.anchor.source_path,
        },
        "asset_id": request.asset_id,
        "asset_kind": request.asset_kind,
        "engine": engine,
        "imports": imported_images or [],
        "run_mode": run_mode,
        "mode": request.mode,
        "staging_root": ".asset-vault/library/generated/sprite-animation-studio",
        "project_id": request.project_id,
    }
    return safe_staging_write_text(output_dir, "lineage.json", json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
