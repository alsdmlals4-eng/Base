"""Durable records connecting an expression request to its approved source."""

import hashlib
import json
from pathlib import Path
from base_tool_contracts import safe_staging_write_text

from .catalog import ResolvedExpression
from .models import ExpressionRequest


def write_lineage(
    request: ExpressionRequest,
    resolved: ResolvedExpression,
    anchor_bytes: bytes,
    output_dir: Path,
    generation_instruction: str | None = None,
    selected_candidate: int | None = None,
    engine: dict[str, object] | None = None,
    anchor_verification: str = "ANCHOR_UNVERIFIED",
    anchor_evidence: dict[str, str] | None = None,
    imported_images: list[dict[str, object]] | None = None,
    run_mode: str = "simulated",
) -> Path:
    """Write request and resolved-expression evidence before candidate generation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "anchor": {
            "approval_status": request.anchor.approval_status,
            "verification_state": anchor_verification,
            "evidence": anchor_evidence or {},
            "figma_node_url": str(request.anchor.figma_node_url),
            "sha256": hashlib.sha256(anchor_bytes).hexdigest(),
            "source_path": request.anchor.source_path,
        },
        "asset_id": request.asset_id,
        "imports": imported_images or [],
        "run_mode": run_mode,
        "engine": engine or {"validation_state": "NOT_RUN"},
        "generation_instruction": generation_instruction,
        "project_id": request.project_id,
        "requested_expression": {
            "candidate_count": request.candidate_count,
            "controls": [control.model_dump(mode="json") for control in request.controls],
            "gaze": request.gaze,
            "head_pose": request.head_pose,
            "preset": request.preset,
        },
        "resolved_expression": {
            "controls": [control.model_dump(mode="json") for control in resolved.controls],
            "gaze": resolved.gaze,
            "gaze_phrase": resolved.gaze_phrase,
            "head_pose": resolved.head_pose,
            "head_pose_phrase": resolved.head_pose_phrase,
            "movement_phrases": list(resolved.movement_phrases),
            "preset": resolved.preset,
        },
        "selection": {"selected_candidate": selected_candidate},
        "tool_version": "0.1.0",
    }
    return safe_staging_write_text(output_dir, "lineage.json", json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
