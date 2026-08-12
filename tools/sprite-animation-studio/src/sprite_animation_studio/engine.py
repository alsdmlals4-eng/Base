"""Fail-closed bridge to a locally configured sprite-generation engine."""

from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
from typing import Protocol

from PIL import Image

from .models import SpriteAnimationRequest


class EngineContractError(RuntimeError):
    """Raised when an engine cannot prove it produced the requested frames."""


@dataclass(frozen=True)
class EngineResult:
    frames: tuple[Path, ...]
    stdout: str = ""
    stderr: str = ""


class SpriteEngine(Protocol):
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

    def __init__(self, frame_count: int | None = None) -> None:
        self._frame_count = frame_count

    def generate(self, request: SpriteAnimationRequest, run_dir: Path) -> EngineResult:
        frames_dir = run_dir / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        frame_count = self._frame_count if self._frame_count is not None else request.action.frame_count
        for index in range(frame_count):
            Image.new("RGBA", (32, 32), (0, 0, 0, 0)).save(frames_dir / f"frame-{index:03d}.png")
        return EngineResult(frames=_verify_frames(frames_dir, request.action.frame_count))


class PinnedSpriteGenEngine:
    """Invoke the pinned upstream ``sprite-gen`` component-row pipeline."""

    def __init__(self, sprite_gen_executable: Path, project_root: Path, provider: str = "codex") -> None:
        self._executable = sprite_gen_executable
        self._project_root = project_root.resolve()
        self._provider = provider

    def generate(self, request: SpriteAnimationRequest, run_dir: Path) -> EngineResult:
        if not self._executable.is_file():
            raise EngineContractError(f"configured sprite-gen executable is unavailable: {self._executable}")

        run_dir.mkdir(parents=True, exist_ok=True)
        engine_run_dir = run_dir / "sprite-gen-run"
        anchor_path = (self._project_root / request.anchor.source_path).resolve()
        if anchor_path != self._project_root and self._project_root not in anchor_path.parents:
            raise EngineContractError("approved anchor escapes project root")
        if not anchor_path.is_file():
            raise EngineContractError("approved anchor file is unavailable")
        engine_request = {
            "version": 1,
            "kind": "sprite-gen-request",
            "engine": "component-row",
            "character": {"id": request.asset_id, "description": request.action.prompt},
            "states": {
                request.action.name: {
                    "frames": request.action.frame_count,
                    "fps": request.action.fps,
                    "loop": request.action.loop_mode != "none",
                    "action": request.action.prompt,
                }
            },
        }
        request_json = json.dumps(engine_request, ensure_ascii=False, sort_keys=True)
        commands = [
            [str(self._executable), "prepare", "--out-dir", str(engine_run_dir), "--character-id", request.asset_id,
             "--base-image", str(anchor_path), "--description", request.action.prompt, "--subject", request.asset_kind,
             "--request-json", request_json],
            [str(self._executable), "gen", "--provider", self._provider,
             "--prompt-file", str(engine_run_dir / "prompts" / f"{request.action.name}.txt"),
             "--out", str(engine_run_dir / "raw" / f"{request.action.name}.png"), "--ref", str(anchor_path)],
            [str(self._executable), "extract", "--run-dir", str(engine_run_dir), "--states", request.action.name],
        ]
        output: list[str] = []
        for command in commands:
            completed = subprocess.run(command, capture_output=True, check=False, text=True)
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
        return EngineResult(frames=frames, stdout="\n".join(output))
