import json
import hashlib
import os
from pathlib import Path

from PIL import Image
import pytest

from sprite_animation_studio.curation import CurationState
from sprite_animation_studio.exporter import export_run
from sprite_animation_studio.models import SpriteAnimationRequest
from tests.test_models import valid_payload
from base_tool_contracts import StagingViolation


def run_with_four_frames(root: Path) -> Path:
    frames = root / "frames"
    frames.mkdir(parents=True)
    for index in range(4):
        Image.new("RGBA", (8, 8), (index * 20, 0, 0, 255)).save(frames / f"frame-{index:03d}.png")
    return root


def frame_hashes(frames: Path) -> tuple[str, ...]:
    return tuple(hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(frames.glob("*.png")))


def test_export_manifest_preserves_selected_order_fps_and_loop(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload())
    run_dir = run_with_four_frames(tmp_path)
    exports = run_dir / "exports"
    selected = exports / "frames" / request.action.name
    godot = exports / "godot"
    selected.mkdir(parents=True)
    godot.mkdir(parents=True)
    result = export_run(run_dir, run_dir / "frames", exports, selected, godot, request, CurationState(selected=[2, 0, 3, 1]), frame_sha256=frame_hashes(run_dir / "frames"), engine={"provenance": "test"}, anchor_sha256="0" * 64)
    manifest = json.loads(result.manifest.read_text(encoding="utf-8"))

    assert manifest["animation"]["rows"]["attack"]["fps"] == 8
    assert manifest["animation"]["rows"]["attack"]["loop"] is False
    assert [frame["source_index"] for frame in manifest["selected_frames"]] == [2, 0, 3, 1]
    assert result.gif.is_file()
    assert result.atlas.is_file()


def test_export_hashes_verified_output_bytes_without_reopening_final_paths(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload())
    run_dir = run_with_four_frames(tmp_path)
    expected = frame_hashes(run_dir / "frames")
    exports = run_dir / "exports"
    selected = exports / "frames" / request.action.name
    godot = exports / "godot"
    selected.mkdir(parents=True)
    godot.mkdir(parents=True)
    monkeypatch.setattr(Path, "read_bytes", lambda self: (_ for _ in ()).throw(AssertionError(f"lexical output read: {self}")))

    result = export_run(
        run_dir,
        run_dir / "frames",
        exports,
        selected,
        godot,
        request,
        CurationState(selected=[0, 1, 2, 3]),
        frame_sha256=expected,
        engine={"provenance": "test"},
        anchor_sha256="0" * 64,
    )

    assert result.manifest.is_file()


def test_export_handoff_uses_logical_paths_across_independent_directory_handles(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload())
    run_dir = run_with_four_frames(tmp_path)
    exports = run_dir / "exports"
    selected = exports / "frames" / request.action.name
    godot = exports / "godot"
    selected.mkdir(parents=True)
    godot.mkdir(parents=True)
    descriptors = [os.open(path, os.O_RDONLY | os.O_DIRECTORY) for path in (run_dir, run_dir / "frames", exports, selected, godot)]
    aliases = [Path(f"/proc/self/fd/{descriptor}") for descriptor in descriptors]
    try:
        result = export_run(*aliases, request, CurationState(selected=[0, 1, 2, 3]), frame_sha256=frame_hashes(run_dir / "frames"), engine={"provenance": "test"}, anchor_sha256="0" * 64)
        handoff = json.loads(result.godot_handoff.read_text(encoding="utf-8"))
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)

    assert handoff["frame_files"] == [
        "frames/attack/frame-000.png",
        "frames/attack/frame-001.png",
        "frames/attack/frame-002.png",
        "frames/attack/frame-003.png",
    ]


def test_export_rejects_a_frame_symlink_swap_after_generation_hashing(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload())
    run_dir = run_with_four_frames(tmp_path)
    hashes = frame_hashes(run_dir / "frames")
    outside = tmp_path / "outside.png"
    Image.new("RGBA", (8, 8), (0, 255, 0, 255)).save(outside)
    frame = run_dir / "frames" / "frame-000.png"
    frame.unlink()
    frame.symlink_to(outside)
    exports = run_dir / "exports"
    selected = exports / "frames" / request.action.name
    godot = exports / "godot"
    selected.mkdir(parents=True)
    godot.mkdir(parents=True)

    with pytest.raises(StagingViolation, match="regular file"):
        export_run(run_dir, run_dir / "frames", exports, selected, godot, request, CurationState(selected=[0, 1, 2, 3]), frame_sha256=hashes, engine={"provenance": "test"}, anchor_sha256="0" * 64)
