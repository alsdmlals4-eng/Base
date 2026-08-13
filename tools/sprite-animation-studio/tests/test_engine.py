from pathlib import Path
import subprocess

import pytest

from sprite_animation_studio.engine import EngineContractError, FakeSpriteEngine, PinnedSpriteGenEngine, PINNED_SPRITE_GEN_COMMIT, build_sprite_gen_request
from sprite_animation_studio.models import SpriteAnimationRequest
from tests.test_models import valid_payload


def test_fake_engine_creates_the_exact_requested_frame_count(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload(action={"name": "attack", "direction": "left", "frame_count": 3, "fps": 8, "loop_mode": "none", "prompt": "strike"}))

    frames = tmp_path / "frames"
    engine_run = tmp_path / "engine"
    frames.mkdir()
    engine_run.mkdir()
    result = FakeSpriteEngine().generate(request, frames, engine_run)

    assert [frame.name for frame in result.frames] == ["frame-000.png", "frame-001.png", "frame-002.png"]
    assert all(frame.is_file() for frame in result.frames)


def test_engine_result_rejects_a_wrong_frame_count(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload())
    frames = tmp_path / "frames"
    engine_run = tmp_path / "engine"
    frames.mkdir()
    engine_run.mkdir()

    with pytest.raises(EngineContractError, match="expected 4 frames"):
        FakeSpriteEngine(frame_count=3).generate(request, frames, engine_run)


def test_pinned_engine_blocks_until_an_os_isolated_workspace_is_available(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    anchor = project_root / "art" / "source" / "idle.png"
    anchor.parent.mkdir(parents=True)
    anchor.write_bytes(b"anchor")
    repository = tmp_path / "sprite-gen-repository"
    repository.mkdir()
    executable = repository / "sprite-gen"
    executable.write_text("stub", encoding="utf-8")
    monkeypatch.setattr(PinnedSpriteGenEngine, "_verify_repository_pin", lambda _self: True)
    request = SpriteAnimationRequest.model_validate(valid_payload())
    frames = tmp_path / "frames"
    engine_run = tmp_path / "engine"
    frames.mkdir()
    engine_run.mkdir()

    engine = PinnedSpriteGenEngine(executable, project_root, sprite_gen_repository=repository)
    with pytest.raises(EngineContractError, match="OS-isolated workspace"):
        engine.generate(request, frames, engine_run)
    assert engine.delivery_eligible is False


def test_sprite_gen_request_serializes_mode_specific_generation_guidance() -> None:
    expression = build_sprite_gen_request(SpriteAnimationRequest.model_validate(valid_payload(mode="expression_variation")))
    pose = build_sprite_gen_request(SpriteAnimationRequest.model_validate(valid_payload(mode="pose_sequence")))

    assert "facial expression" in expression["character"]["description"]
    assert "pose sequence" in pose["character"]["description"]
    assert expression["states"]["attack"]["action"] != pose["states"]["attack"]["action"]


def test_pinned_engine_blocks_when_the_verified_executable_changes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project_root = tmp_path / "project"
    anchor = project_root / "art" / "source" / "idle.png"
    anchor.parent.mkdir(parents=True)
    anchor.write_bytes(b"anchor")
    repository = tmp_path / "sprite-gen-repository"
    repository.mkdir()
    executable = repository / "sprite-gen"
    executable.write_text("verified", encoding="utf-8")
    monkeypatch.setattr(PinnedSpriteGenEngine, "_verify_repository_pin", lambda _self: True)
    engine = PinnedSpriteGenEngine(executable, project_root, sprite_gen_repository=repository)
    executable.write_text("replaced", encoding="utf-8")

    assert engine.delivery_eligible is False


def test_pinned_engine_rejects_an_untracked_repository_executable(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repository = tmp_path / "sprite-gen-repository"
    repository.mkdir()
    executable = repository / "malicious-sprite-gen"
    executable.write_text("untracked", encoding="utf-8")

    def fake_run(command: list[str], **_: object) -> subprocess.CompletedProcess:
        if "rev-parse" in command:
            return subprocess.CompletedProcess(command, 0, PINNED_SPRITE_GEN_COMMIT + "\n", "")
        if "status" in command:
            return subprocess.CompletedProcess(command, 0, "?? malicious-sprite-gen\n", "")
        if "ls-files" in command:
            return subprocess.CompletedProcess(command, 1, "", "")
        return subprocess.CompletedProcess(command, 1, b"", b"")

    monkeypatch.setattr("sprite_animation_studio.engine.subprocess.run", fake_run)
    engine = PinnedSpriteGenEngine(executable, tmp_path / "project", sprite_gen_repository=repository)

    assert engine.delivery_eligible is False
