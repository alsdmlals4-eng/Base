"""Local candidate-engine protocol and deterministic test implementation."""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Protocol

from PIL import Image, UnidentifiedImageError

from .catalog import ResolvedExpression
from .models import ExpressionRequest


IDENTITY_PREFIX = (
    "Preserve the exact same character: face geometry, hairstyle, costume, palette, framing, lighting, "
    "and art style. Edit only the requested facial expression, gaze, and head pose."
)
INTENSITY_PHRASES = {
    "A": "very subtle intensity",
    "B": "subtle intensity",
    "C": "moderate intensity",
    "D": "strong intensity",
    "E": "maximum readable intensity",
}


class EngineContractError(RuntimeError):
    """Raised when a local engine cannot satisfy the reviewed request contract."""


@dataclass(frozen=True)
class EngineResult:
    candidates: list[Path]
    generation_instruction: str
    provenance: str = "unverified"
    delivery_eligible: bool = False


@dataclass(frozen=True)
class EnginePolicy:
    adapter_id: str
    provenance: str
    delivery_eligible: bool
    config_sha256: str


class ExpressionEngine(Protocol):
    provenance: str
    delivery_eligible: bool

    def generate(self, request: ExpressionRequest, resolved: ResolvedExpression, run_dir: Path) -> EngineResult:
        """Generate local candidate PNGs without mutating the approved anchor."""


def generation_instruction(resolved: ResolvedExpression) -> str:
    movements = "; ".join(resolved.movement_phrases) or "keep a neutral facial expression"
    intensities = ", ".join(f"{control.code}: {INTENSITY_PHRASES[control.intensity]}" for control in resolved.controls) or "neutral intensity"
    return " ".join(
        (
            IDENTITY_PREFIX,
            f"Facial movement: {movements} ({intensities}).",
            f"Gaze: {resolved.gaze_phrase}.",
            f"Head pose: {resolved.head_pose_phrase}.",
        )
    )


class FakeExpressionEngine:
    """Copies an anchor into valid candidates for local lifecycle testing only."""

    provenance = "simulated"
    delivery_eligible = False

    def __init__(self, project_root: Path) -> None:
        self._project_root = project_root.resolve()

    def generate(self, request: ExpressionRequest, resolved: ResolvedExpression, run_dir: Path) -> EngineResult:
        anchor_reference = self._project_root / request.anchor.source_path
        anchor = anchor_reference.resolve()
        if self._project_root not in anchor.parents or not anchor.is_file():
            raise EngineContractError("approved anchor source_path must point to an existing project image")
        try:
            with Image.open(anchor_reference) as source:
                source_rgba = source.convert("RGBA")
        except (OSError, UnidentifiedImageError) as error:
            raise EngineContractError("approved anchor source_path must be a readable image") from error

        candidates_dir = run_dir / "candidates"
        candidates_dir.mkdir(parents=True, exist_ok=True)
        candidates: list[Path] = []
        for index in range(request.candidate_count):
            candidate = candidates_dir / f"candidate-{index:03d}.png"
            source_rgba.save(candidate)
            candidates.append(candidate)
        return EngineResult(
            candidates=candidates,
            generation_instruction=generation_instruction(resolved),
            provenance="simulated",
            delivery_eligible=False,
        )


def trusted_engine_policy(engine: ExpressionEngine) -> EnginePolicy:
    """Return service-owned policy; engine results cannot grant themselves eligibility."""
    if type(engine) is FakeExpressionEngine:
        adapter_id, provenance, eligible = "expression.fake.v1", "simulated", False
    else:
        adapter_id, provenance, eligible = "expression.unverified", "unverified", False
    encoded = json.dumps(
        {"adapter_id": adapter_id, "engine_class": f"{type(engine).__module__}.{type(engine).__qualname__}", "provenance": provenance, "delivery_eligible": eligible},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return EnginePolicy(adapter_id, provenance, eligible, hashlib.sha256(encoded).hexdigest())
