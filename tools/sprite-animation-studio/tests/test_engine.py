from pathlib import Path
import subprocess

import pytest

from sprite_animation_studio.engine import EngineContractError, FakeSpriteEngine, PinnedSpriteGenEngine
from sprite_animation_studio.models import SpriteAnimationRequest
from tests.test_models import valid_payload


def test_fake_engine_creates_the_exact_requested_frame_count(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload(action={"name": "attack", "direction": "left", "frame_count": 3, "fps": 8, "loop_mode": "none", "prompt": "strike"}))

    result = FakeSpriteEngine().generate(request, tmp_path)

    assert [frame.name for frame in result.frames] == ["frame-000.png", "frame-001.png", "frame-002.png"]
    assert all(frame.is_file() for frame in result.frames)


def test_engine_result_rejects_a_wrong_frame_count(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload())

    with pytest.raises(EngineContractError, match="expected 4 frames"):
        FakeSpriteEngine(frame_count=3).generate(request, tmp_path)


def test_pinned_engine_uses_the_sprite_gen_component_row_pipeline(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    anchor = project_root / "art" / "source" / "idle.png"
    anchor.parent.mkdir(parents=True)
    anchor.write_bytes(b"anchor")
    executable = tmp_path / "sprite-gen"
    executable.write_text("stub", encoding="utf-8")
    calls: list[list[str]] = []

    def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        if command[1] == "extract":
            frames = Path(command[command.index("--run-dir") + 1]) / "frames" / "attack"
            frames.mkdir(parents=True)
            for index in range(4):
                from PIL import Image
                Image.new("RGBA", (8, 8), (0, 0, 0, 0)).save(frames / f"frame-{index:03d}.png")
        return subprocess.CompletedProcess(command, 0, "ok", "")

    monkeypatch.setattr("sprite_animation_studio.engine.subprocess.run", fake_run)
    request = SpriteAnimationRequest.model_validate(valid_payload())

    result = PinnedSpriteGenEngine(executable, project_root).generate(request, tmp_path / "run")

    assert [command[1] for command in calls] == ["prepare", "gen", "extract"]
    assert "--provider" in calls[1] and calls[1][calls[1].index("--provider") + 1] == "codex"
    assert len(result.frames) == 4
