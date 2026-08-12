"""Non-destructive frame selection and presentation transforms."""

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path


@dataclass(frozen=True)
class FrameTransform:
    dx: int = 0
    dy: int = 0
    scale: float = 1.0


@dataclass(frozen=True)
class CurationState:
    selected: list[int]
    transforms: dict[int, FrameTransform] = field(default_factory=dict)
    rejected: list[int] = field(default_factory=list)


def save_curation(run_dir: Path, curation: CurationState) -> Path:
    """Persist curation as a sidecar; generated candidate frames stay immutable."""
    if len(curation.selected) != len(set(curation.selected)):
        raise ValueError("selected frame indices must be unique")
    if set(curation.selected) & set(curation.rejected):
        raise ValueError("a frame cannot be both selected and rejected")

    payload = {
        "rejected": curation.rejected,
        "selected": curation.selected,
        "transforms": {str(index): asdict(transform) for index, transform in sorted(curation.transforms.items())},
    }
    target = run_dir / "curation.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target
