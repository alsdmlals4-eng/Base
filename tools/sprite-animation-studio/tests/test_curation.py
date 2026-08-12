from pathlib import Path

from PIL import Image

from sprite_animation_studio.curation import CurationState, FrameTransform, save_curation


def write_fixture_frame(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (8, 8), (255, 0, 0, 255)).save(path)
    return path


def test_curation_never_rewrites_a_source_frame(tmp_path: Path) -> None:
    source = write_fixture_frame(tmp_path / "frames" / "frame-000.png")
    before = source.read_bytes()

    save_curation(tmp_path, CurationState(selected=[0], transforms={0: FrameTransform(dx=3)}))

    assert source.read_bytes() == before
    assert (tmp_path / "curation.json").is_file()
