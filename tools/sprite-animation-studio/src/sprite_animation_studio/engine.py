"""Fail-closed bridge to a locally configured sprite-generation engine."""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Protocol

from PIL import Image

from .models import SpriteAnimationRequest


MODE_GUIDANCE = {
    "expression_variation": "Preserve the exact character silhouette, costume, palette, and facing direction; vary only the requested facial expression with readable stepped transitions.",
    "pose_sequence": "Preserve the exact character identity and facing direction; create a continuous anticipation, action, impact, and recovery pose sequence.",
    "effect_stages": "Preserve the exact effect palette and style; create ordered startup, active, impact, and fade stages around the requested origin.",
    "sprite_action": "Preserve the approved anchor identity, silhouette, palette, and pixel-art style across the complete action row.",
}
PINNED_SPRITE_GEN_COMMIT = "88f2ea17cac2ef066536beee7e3f40b2f8d29c87"


class EngineContractError(RuntimeError):
    """Raised when an engine cannot prove it produced the requested frames."""


@dataclass(frozen=True)
class EngineResult:
    frames: tuple[Path, ...]
    provenance: str = "unverified"
    delivery_eligible: bool = False
    stdout: str = ""
    stderr: str = ""


@dataclass(frozen=True)
class EnginePolicy:
    adapter_id: str
    provenance: str
    delivery_eligible: bool
    config_sha256: str


class SpriteEngine(Protocol):
    provenance: str
    delivery_eligible: bool

    def generate(self, request: SpriteAnimationRequest, run_dir: Path) -> EngineResult:
        """Generate exactly the requested count of candidate PNG frames."""


def _verify_frames(frames_dir: Path, expected_count: int) -> tuple[Path, ...]:
    frames = tuple(sorted(frames_dir.glob("*.png")))
    if len(frames) != expected_count:
        raise EngineContractError(f"expected {expected_count} frames, received {len(frames)}")
    for frame in frames:
        try:
            with Image.open(frame) as image:
                image.verify()
        except (OSError, SyntaxError) as error:
            raise EngineContractError(f"invalid PNG output: {frame.name}") from error
    return frames


class FakeSpriteEngine:
    """Deterministic transparent-frame producer used only by automated tests."""

    provenance = "simulated"
    delivery_eligible = False

    def __init__(self, frame_count: int | None = None) -> None:
        self._frame_count = frame_count

    def generate(self, request: SpriteAnimationRequest, run_dir: Path) -> EngineResult:
        frames_dir = run_dir / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        frame_count = self._frame_count if self._frame_count is not None else request.action.frame_count
        for index in range(frame_count):
            Image.new("RGBA", (32, 32), (0, 0, 0, 0)).save(frames_dir / f"frame-{index:03d}.png")
        return EngineResult(
            frames=_verify_frames(frames_dir, request.action.frame_count),
            provenance="simulated",
            delivery_eligible=False,
        )


class PinnedSpriteGenEngine:
    """Invoke the pinned upstream ``sprite-gen`` component-row pipeline."""

    provenance = "pinned_sprite_gen"
    delivery_eligible = True

    def __init__(self, sprite_gen_executable: Path, project_root: Path, provider: str = "codex", sprite_gen_repository: Path | None = None) -> None:
        self._executable = sprite_gen_executable
        self._project_root = project_root.resolve()
        self._provider = provider
        self._repository = sprite_gen_repository.resolve() if sprite_gen_repository else None
        self._pin_verified = self._verify_repository_pin()
        self._executable_sha256 = self._hash_executable() if self._pin_verified else "UNVERIFIED"

    @property
    def delivery_eligible(self) -> bool:
        return self._pin_verified

    def _hash_executable(self) -> str:
        try:
            return hashlib.sha256(self._executable.resolve().read_bytes()).hexdigest()
        except OSError as error:
            raise EngineContractError("configured sprite-gen executable is unreadable") from error

    def _verify_repository_pin(self) -> bool:
        if self._repository is None or not self._repository.is_dir() or not self._executable.is_file():
            return False
        executable = self._executable.resolve()
        if self._repository != executable and self._repository not in executable.parents:
            return False
        relative = executable.relative_to(self._repository).as_posix()
        head = subprocess.run(["git", "-C", str(self._repository), "rev-parse", "HEAD"], capture_output=True, text=True, check=False)
        dirty = subprocess.run(["git", "-C", str(self._repository), "status", "--porcelain"], capture_output=True, text=True, check=False)
        tracked = subprocess.run(["git", "-C", str(self._repository), "ls-files", "--error-unmatch", "--", relative], capture_output=True, text=True, check=False)
        committed = subprocess.run(["git", "-C", str(self._repository), "show", f"HEAD:{relative}"], capture_output=True, check=False)
        return (
            head.returncode == 0
            and head.stdout.strip() == PINNED_SPRITE_GEN_COMMIT
            and dirty.returncode == 0
            and not dirty.stdout.strip()
            and tracked.returncode == 0
            and committed.returncode == 0
            and committed.stdout == executable.read_bytes()
        )

    def generate(self, request: SpriteAnimationRequest, run_dir: Path) -> EngineResult:
        if not self._verify_repository_pin():
            raise EngineContractError("sprite-gen repository/executable is not verified at the required pinned commit")
        if self._hash_executable() != self._executable_sha256:
            raise EngineContractError("configured sprite-gen executable changed after adapter verification")

        run_dir.mkdir(parents=True, exist_ok=True)
        engine_run_dir = run_dir / "sprite-gen-run"
        anchor_reference = self._project_root / request.anchor.source_path
        anchor_path = anchor_reference.resolve()
        if anchor_path != self._project_root and self._project_root not in anchor_path.parents:
            raise EngineContractError("approved anchor escapes project root")
        if not anchor_path.is_file():
            raise EngineContractError("approved anchor file is unavailable")
        generation_prompt = f"{MODE_GUIDANCE[request.mode]}\n\nRequested action: {request.action.prompt}"
        engine_request = {
            "version": 1,
            "kind": "sprite-gen-request",
            "engine": "component-row",
            "character": {"id": request.asset_id, "description": generation_prompt},
            "states": {
                request.action.name: {
                    "frames": request.action.frame_count,
                    "fps": request.action.fps,
                    "loop": request.action.loop_mode != "none",
                    "action": generation_prompt,
                }
            },
        }
        request_json = json.dumps(engine_request, ensure_ascii=False, sort_keys=True)
        commands = [
            [str(self._executable), "prepare", "--out-dir", str(engine_run_dir), "--character-id", request.asset_id,
             "--base-image", str(anchor_reference), "--description", generation_prompt, "--subject", request.asset_kind,
             "--request-json", request_json],
            [str(self._executable), "gen", "--provider", self._provider,
             "--prompt-file", str(engine_run_dir / "prompts" / f"{request.action.name}.txt"),
             "--out", str(engine_run_dir / "raw" / f"{request.action.name}.png"), "--ref", str(anchor_reference)],
            [str(self._executable), "extract", "--run-dir", str(engine_run_dir), "--states", request.action.name],
        ]
        output: list[str] = []
        inherited: set[int] = set()
        for path in (run_dir, Path(request.anchor.source_path)):
            if len(path.parts) >= 5 and path.parts[:4] == ("/", "proc", "self", "fd"):
                inherited.add(int(path.parts[4]))
        inherited_fds = tuple(sorted(inherited))
        for command in commands:
            completed = subprocess.run(command, capture_output=True, check=False, text=True, pass_fds=inherited_fds)
            output.extend(part for part in (completed.stdout, completed.stderr) if part)
            if completed.returncode != 0:
                detail = completed.stderr.strip() or completed.stdout.strip() or "no output"
                raise EngineContractError(f"sprite-gen {command[1]} failed with exit {completed.returncode}: {detail}")

        extracted = tuple(sorted((engine_run_dir / "frames").rglob("*.png")))
        if len(extracted) != request.action.frame_count:
            raise EngineContractError(f"expected {request.action.frame_count} frames, received {len(extracted)}")
        frames_dir = run_dir / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        for index, frame in enumerate(extracted):
            shutil.copy2(frame, frames_dir / f"frame-{index:03d}.png")
        frames = _verify_frames(frames_dir, request.action.frame_count)
        if not self._verify_repository_pin() or self._hash_executable() != self._executable_sha256:
            raise EngineContractError("configured sprite-gen repository or executable changed during generation")
        return EngineResult(
            frames=frames,
            provenance="pinned_sprite_gen",
            delivery_eligible=True,
            stdout="\n".join(output),
        )


def trusted_engine_policy(engine: SpriteEngine) -> EnginePolicy:
    """Bind delivery eligibility to an exact reviewed adapter class."""
    if type(engine) is FakeSpriteEngine:
        adapter_id, provenance, eligible = "sprite.fake.v1", "simulated", False
        adapter_config = {"frame_count": engine._frame_count}
    elif type(engine) is PinnedSpriteGenEngine:
        eligible = engine._verify_repository_pin() and engine._hash_executable() == engine._executable_sha256
        adapter_id, provenance = "sprite.sprite-gen.pinned.v1", "pinned_sprite_gen"
        adapter_config = {
            "executable": str(engine._executable.resolve()),
            "executable_sha256": engine._executable_sha256,
            "repository_commit": PINNED_SPRITE_GEN_COMMIT if engine._pin_verified else "UNVERIFIED",
            "provider": engine._provider,
        }
    else:
        adapter_id, provenance, eligible = "sprite.unverified", "unverified", False
        adapter_config = {}
    encoded = json.dumps(
        {"adapter_id": adapter_id, "engine_class": f"{type(engine).__module__}.{type(engine).__qualname__}", "provenance": provenance, "delivery_eligible": eligible, "config": adapter_config},
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return EnginePolicy(adapter_id, provenance, eligible, hashlib.sha256(encoded).hexdigest())
