"""Deterministic project-local sprite outputs."""

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import hashlib

from PIL import Image

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


def _source_frames(run_dir: Path) -> list[Path]:
    frames = sorted((run_dir / "frames").glob("*.png"))
    if not frames:
        raise ValueError("run contains no candidate frames")
    return frames


def _transformed(image: Image.Image, transform: FrameTransform) -> Image.Image:
    if transform.scale <= 0:
        raise ValueError("frame scale must be positive")
    width = max(1, round(image.width * transform.scale))
    height = max(1, round(image.height * transform.scale))
    return image.resize((width, height), Image.Resampling.NEAREST)


def export_run(run_dir: Path, request: SpriteAnimationRequest, curation: CurationState, *, engine: dict[str, object], anchor_sha256: str, anchor_verification: str = "ANCHOR_UNVERIFIED", anchor_evidence: dict[str, str] | None = None) -> ExportResult:
    """Export selected copies, preview GIF, atlas, manifest, and Godot handoff JSON."""
    source_frames = _source_frames(run_dir)
    if not curation.selected:
        raise ValueError("at least one frame must be selected")
    if any(index < 0 or index >= len(source_frames) for index in curation.selected):
        raise ValueError("selected frame index is outside candidate frames")
    save_curation(run_dir, curation)

    exports = run_dir / "exports"
    selected_dir = exports / "frames" / request.action.name
    selected_dir.mkdir(parents=True, exist_ok=True)
    selected_sources = [(index, source_frames[index]) for index in curation.selected]
    selected_paths: list[Path] = []
    prepared: list[tuple[int, Image.Image, FrameTransform]] = []
    for position, (source_index, source) in enumerate(selected_sources):
        target = selected_dir / f"frame-{position:03d}.png"
        shutil.copy2(source, target)
        selected_paths.append(target)
        transform = curation.transforms.get(source_index, FrameTransform())
        with Image.open(source) as opened:
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

    atlas = exports / "atlas.png"
    atlas_image = Image.new("RGBA", (max_width * len(rendered), max_height), (0, 0, 0, 0))
    rectangles = []
    for position, (source_index, frame) in enumerate(zip(curation.selected, rendered)):
        x = position * max_width
        atlas_image.alpha_composite(frame, (x, 0))
        rectangles.append({"source_index": source_index, "x": x, "y": 0, "w": max_width, "h": max_height})
    atlas_image.save(atlas)

    contact_sheet = exports / "contact-sheet.png"
    atlas_image.save(contact_sheet)
    gif = exports / "preview.gif"
    duration = round(1000 / request.action.fps)
    rendered[0].save(gif, save_all=True, append_images=rendered[1:], duration=duration, loop=0 if request.action.loop_mode != "none" else 1, disposal=2)

    godot_dir = exports / "godot"
    godot_dir.mkdir(parents=True, exist_ok=True)
    godot_handoff = godot_dir / f"{request.action.name}.spriteframes.json"
    godot_handoff.write_text(
        json.dumps({"status": "handoff_only", "animation": request.action.name, "atlas_manifest": "../manifest.json", "frame_files": [str(path.relative_to(exports)) for path in selected_paths]}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    manifest = exports / "manifest.json"
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
    manifest.write_text(json.dumps(manifest_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return ExportResult(selected_dir, atlas, contact_sheet, gif, manifest, godot_handoff)
