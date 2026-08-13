"""Deterministic project-local sprite outputs."""

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import hashlib
from io import BytesIO

from PIL import Image
from base_tool_contracts import safe_staging_write_bytes, safe_staging_write_text, staging_read_bytes

from .curation import CurationState, FrameTransform, save_curation
from .models import SpriteAnimationRequest


@dataclass(frozen=True)
class ExportResult:
    frames_dir: Path
    atlas: Path
    contact_sheet: Path
    gif: Path
    manifest: Path
    godot_handoff: Path


def _source_frames(frames_dir: Path, expected_sha256: tuple[str, ...]) -> list[tuple[Path, bytes]]:
    frames = sorted(frames_dir.glob("*.png"))
    if not frames:
        raise ValueError("run contains no candidate frames")
    if len(frames) != len(expected_sha256):
        raise ValueError("frame hash evidence does not match generated frames")
    return [
        (frame, staging_read_bytes(frames_dir, frame.name, expected_sha256=expected_sha256[index]))
        for index, frame in enumerate(frames)
    ]


def _transformed(image: Image.Image, transform: FrameTransform) -> Image.Image:
    if transform.scale <= 0:
        raise ValueError("frame scale must be positive")
    width = max(1, round(image.width * transform.scale))
    height = max(1, round(image.height * transform.scale))
    return image.resize((width, height), Image.Resampling.NEAREST)


def export_run(
    run_dir: Path,
    frames_dir: Path,
    exports: Path,
    selected_dir: Path,
    godot_dir: Path,
    request: SpriteAnimationRequest,
    curation: CurationState,
    *,
    frame_sha256: tuple[str, ...],
    engine: dict[str, object],
    anchor_sha256: str,
    anchor_verification: str = "ANCHOR_UNVERIFIED",
    anchor_evidence: dict[str, str] | None = None,
) -> ExportResult:
    """Export selected copies, preview GIF, atlas, manifest, and Godot handoff JSON."""
    source_frames = _source_frames(frames_dir, frame_sha256)
    if not curation.selected:
        raise ValueError("at least one frame must be selected")
    if any(index < 0 or index >= len(source_frames) for index in curation.selected):
        raise ValueError("selected frame index is outside candidate frames")
    save_curation(run_dir, curation)

    selected_sources = [(index, source_frames[index]) for index in curation.selected]
    selected_paths: list[Path] = []
    prepared: list[tuple[int, Image.Image, FrameTransform]] = []
    for position, (source_index, (source, source_bytes)) in enumerate(selected_sources):
        target = safe_staging_write_bytes(selected_dir, f"frame-{position:03d}.png", source_bytes)
        selected_paths.append(target)
        transform = curation.transforms.get(source_index, FrameTransform())
        with Image.open(BytesIO(source_bytes)) as opened:
            prepared.append((source_index, _transformed(opened.convert("RGBA"), transform), transform))

    max_width = max(image.width + abs(transform.dx) for _, image, transform in prepared)
    max_height = max(image.height + abs(transform.dy) for _, image, transform in prepared)
    rendered: list[Image.Image] = []
    for _, image, transform in prepared:
        frame = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))
        x = max(0, transform.dx)
        y = max(0, transform.dy)
        frame.alpha_composite(image, (x, y))
        rendered.append(frame)

    atlas_image = Image.new("RGBA", (max_width * len(rendered), max_height), (0, 0, 0, 0))
    rectangles = []
    for position, (source_index, frame) in enumerate(zip(curation.selected, rendered)):
        x = position * max_width
        atlas_image.alpha_composite(frame, (x, 0))
        rectangles.append({"source_index": source_index, "x": x, "y": 0, "w": max_width, "h": max_height})
    atlas_encoded = BytesIO()
    atlas_image.save(atlas_encoded, format="PNG")
    atlas = safe_staging_write_bytes(exports, "atlas.png", atlas_encoded.getvalue())

    contact_sheet = safe_staging_write_bytes(exports, "contact-sheet.png", atlas_encoded.getvalue())
    duration = round(1000 / request.action.fps)
    gif_encoded = BytesIO()
    rendered[0].save(gif_encoded, format="GIF", save_all=True, append_images=rendered[1:], duration=duration, loop=0 if request.action.loop_mode != "none" else 1, disposal=2)
    gif = safe_staging_write_bytes(exports, "preview.gif", gif_encoded.getvalue())

    godot_handoff = safe_staging_write_text(
        godot_dir,
        f"{request.action.name}.spriteframes.json",
        json.dumps({"status": "handoff_only", "animation": request.action.name, "atlas_manifest": "../manifest.json", "frame_files": [f"frames/{request.action.name}/{path.name}" for path in selected_paths]}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )
    manifest_payload = {
        "anchor_sha256": anchor_sha256,
        "anchor_verification": anchor_verification,
        "anchor_evidence": anchor_evidence or {},
        "animation": {"rows": {request.action.name: {"fps": request.action.fps, "loop": request.action.loop_mode != "none"}}},
        "atlas": {"file": atlas.name, "frame_size": {"w": max_width, "h": max_height}},
        "selected_frames": rectangles,
        "selected_sha256": [hashlib.sha256(path.read_bytes()).hexdigest() for path in selected_paths],
        "atlas_sha256": hashlib.sha256(atlas.read_bytes()).hexdigest(),
        "contact_sheet_sha256": hashlib.sha256(contact_sheet.read_bytes()).hexdigest(),
        "preview_gif_sha256": hashlib.sha256(gif.read_bytes()).hexdigest(),
        "godot_handoff_sha256": hashlib.sha256(godot_handoff.read_bytes()).hexdigest(),
        "engine": engine,
    }
    manifest = safe_staging_write_text(exports, "manifest.json", json.dumps(manifest_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return ExportResult(selected_dir, atlas, contact_sheet, gif, manifest, godot_handoff)
