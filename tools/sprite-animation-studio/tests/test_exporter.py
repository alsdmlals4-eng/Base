import json
from pathlib import Path

from PIL import Image

from sprite_animation_studio.curation import CurationState
from sprite_animation_studio.exporter import export_run
from sprite_animation_studio.models import SpriteAnimationRequest
from tests.test_models import valid_payload


def run_with_four_frames(root: Path) -> Path:
    frames = root / "frames"
    frames.mkdir(parents=True)
    for index in range(4):
        Image.new("RGBA", (8, 8), (index * 20, 0, 0, 255)).save(frames / f"frame-{index:03d}.png")
    return root


def test_export_manifest_preserves_selected_order_fps_and_loop(tmp_path: Path) -> None:
    request = SpriteAnimationRequest.model_validate(valid_payload())
    result = export_run(run_with_four_frames(tmp_path), request, CurationState(selected=[2, 0, 3, 1]))
    manifest = json.loads(result.manifest.read_text(encoding="utf-8"))

    assert manifest["animation"]["rows"]["attack"]["fps"] == 8
    assert manifest["animation"]["rows"]["attack"]["loop"] is False
    assert [frame["source_index"] for frame in manifest["selected_frames"]] == [2, 0, 3, 1]
    assert result.gif.is_file()
    assert result.atlas.is_file()
