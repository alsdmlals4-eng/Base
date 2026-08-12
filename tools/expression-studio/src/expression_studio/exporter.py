"""Still-image review exports for an explicitly selected expression candidate."""

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import hashlib

from PIL import Image


@dataclass(frozen=True)
class ExportResult:
    selected: Path
    contact_sheet: Path
    manifest: Path


def _contact_sheet(candidates: list[Path], target: Path) -> None:
    opened = [Image.open(candidate).convert("RGBA") for candidate in candidates]
    try:
        cell_width = max(image.width for image in opened)
        cell_height = max(image.height for image in opened)
        columns = min(4, len(opened))
        rows = (len(opened) + columns - 1) // columns
        padding = 8
        sheet = Image.new(
            "RGBA",
            (padding + columns * (cell_width + padding), padding + rows * (cell_height + padding)),
            (0, 0, 0, 0),
        )
        for index, image in enumerate(opened):
            x = padding + (index % columns) * (cell_width + padding)
            y = padding + (index // columns) * (cell_height + padding)
            sheet.alpha_composite(image, (x, y))
        sheet.save(target)
    finally:
        for image in opened:
            image.close()


def export_selected_candidate(
    exports_dir: Path,
    candidates: list[Path],
    selected_candidate: int,
    generation_instruction: str,
    *,
    engine: dict[str, object],
    anchor_sha256: str,
    anchor_verification: str,
    anchor_evidence: dict[str, str],
) -> ExportResult:
    """Create review outputs after validating one existing candidate index."""
    if selected_candidate < 0 or selected_candidate >= len(candidates):
        raise ValueError("selected candidate is outside generated candidates")
    selected = exports_dir / "selected.png"
    shutil.copyfile(candidates[selected_candidate], selected)
    contact_sheet = exports_dir / "contact_sheet.png"
    _contact_sheet(candidates, contact_sheet)
    manifest = exports_dir / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "candidate_count": len(candidates),
                "anchor_sha256": anchor_sha256,
                "anchor_verification": anchor_verification,
                "anchor_evidence": anchor_evidence,
                "engine": engine,
                "generation_instruction": generation_instruction,
                "selected_candidate": selected_candidate,
                "selected_file": selected.name,
                "selected_sha256": hashlib.sha256(selected.read_bytes()).hexdigest(),
                "contact_sheet_sha256": hashlib.sha256(contact_sheet.read_bytes()).hexdigest(),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return ExportResult(selected=selected, contact_sheet=contact_sheet, manifest=manifest)
