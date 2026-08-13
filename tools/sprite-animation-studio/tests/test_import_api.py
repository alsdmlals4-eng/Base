from io import BytesIO
import json
from pathlib import Path

from PIL import Image
import pytest

from tests.test_api import client_for
from tests.test_models import valid_payload
from sprite_animation_studio.app import _MAX_REQUEST_BODY_BYTES


def png(color: tuple[int, int, int, int], *, size: tuple[int, int] = (8, 8)) -> bytes:
    output = BytesIO()
    Image.new("RGBA", size, color).save(output, format="PNG")
    return output.getvalue()


def jpeg(color: tuple[int, int, int], *, size: tuple[int, int] = (8, 8)) -> bytes:
    output = BytesIO()
    Image.new("RGB", size, color).save(output, format="JPEG")
    return output.getvalue()


def parts(images: list[bytes], *, payload: dict[str, object] | None = None) -> tuple[dict[str, str], list[tuple[str, tuple[str, bytes, str]]]]:
    return (
        {"request_json": json.dumps(payload or valid_payload()), "declared_source": "LOCAL_GENERATOR"},
        [("frames", (f"browser-{index}.png", image, "image/png")) for index, image in enumerate(images)],
    )


def test_import_sprite_frames_preserves_order_without_a_provider_call(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    colors = [(255, 0, 0, 255), (0, 255, 0, 255), (0, 0, 255, 255), (255, 255, 0, 255)]
    data, files = parts([png(color) for color in colors])

    response = client.post("/api/import-runs", data=data, files=files)

    assert response.status_code == 201
    run = response.json()
    assert run["status"] == "generated"
    assert run["frame_count"] == 4
    assert [item["order"] for item in run["imports"]] == [0, 1, 2, 3]
    assert run["engine"]["adapter_id"] == "sprite.import.v1"
    assert run["cost"] == {"cost_route": "INCLUDED_OR_LOCAL_HANDOFF", "provider_call_made": False}
    assert run["cost_route"] == "INCLUDED_OR_LOCAL_HANDOFF"
    assert run["provider_call_made"] is False
    assert run["declared_source"] == "LOCAL_GENERATOR"
    assert run["imported_files"][0]["index"] == 0


def test_import_mode_rejects_json_generation(tmp_path: Path) -> None:
    response = client_for(tmp_path, run_mode="subscription_handoff_import").post("/api/runs", json=valid_payload())

    assert response.status_code == 409
    assert response.json()["detail"] == "MODE_NOT_AVAILABLE"


def test_import_sprite_rejects_wrong_count_dimensions_transparency_and_duplicates(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    valid = [png((index * 40, 10, 20, 255)) for index in range(4)]
    cases = [
        (valid[:3], "expected 4"),
        ([valid[0], png((1, 2, 3, 255), size=(9, 8)), valid[2], valid[3]], "dimensions"),
        ([valid[0], png((0, 0, 0, 0)), valid[2], valid[3]], "transparent"),
        ([valid[0], valid[1], valid[1], valid[3]], "pixel-duplicates"),
    ]

    for images, expected in cases:
        data, files = parts(images)
        response = client.post("/api/import-runs", data=data, files=files)
        assert response.status_code == 422
        assert expected in response.json()["detail"]


def test_import_rejects_frame_count_before_decoding_file_bodies(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")

    response = client.post(
        "/api/import-runs",
        data={"request_json": json.dumps(valid_payload()), "declared_source": "LOCAL_GENERATOR"},
        files=[("frames", ("ignored.bin", b"not-an-image", "application/octet-stream"))],
    )

    assert response.status_code == 422
    assert "expected 4" in response.json()["detail"]


def test_app_rejects_an_oversize_request_before_multipart_parsing(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")

    response = client.post(
        "/api/import-runs",
        content=b"not parsed",
        headers={"Content-Type": "multipart/form-data; boundary=ignored", "Content-Length": str(402 * 1024 * 1024 + 1)},
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "request body exceeds the configured safety limit"


def test_request_limit_covers_all_sixteen_documented_25_mib_frames_plus_multipart_overhead() -> None:
    assert _MAX_REQUEST_BODY_BYTES >= (16 * 25 + 2) * 1024 * 1024


def test_effect_import_without_alpha_is_allowed_with_a_warning(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    payload = valid_payload(asset_kind="effect", mode="effect_stages")
    rgb_frames = [jpeg((index * 40, 20, 30)) for index in range(4)]
    data, files = parts(rgb_frames, payload=payload)

    response = client.post("/api/import-runs", data=data, files=files)

    assert response.status_code == 201
    assert any("alpha" in warning for warning in response.json()["warnings"])


def test_import_rejects_a_non_image_anchor_before_staging(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    source = tmp_path / "art" / "source" / "idle.png"
    source.write_text("OPENAI_API_KEY=must-not-leave-project", encoding="utf-8")
    data, files = parts([png((index * 40, 10, 20, 255)) for index in range(4)])

    response = client.post("/api/import-runs", data=data, files=files)

    assert response.status_code == 422
    assert "supported PNG, JPEG, or WebP image" in response.json()["detail"]
    generated_root = tmp_path / ".asset-vault" / "library" / "generated" / "sprite-animation-studio"
    assert not generated_root.exists()


def test_import_rejects_an_anchor_symlink_before_reading_it(tmp_path: Path) -> None:
    if not hasattr(Path, "symlink_to"):
        pytest.skip("symlink support is unavailable")
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    target = tmp_path / "art" / "source" / "target.png"
    Image.new("RGBA", (8, 8), (1, 2, 3, 255)).save(target)
    source = tmp_path / "art" / "source" / "idle.png"
    source.unlink()
    source.symlink_to(target)
    data, files = parts([png((index * 40, 10, 20, 255)) for index in range(4)])

    response = client.post("/api/import-runs", data=data, files=files)

    assert response.status_code == 422
    assert "regular file" in response.json()["detail"] or "link" in response.json()["detail"]
