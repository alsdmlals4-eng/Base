from io import BytesIO
from pathlib import Path

from PIL import Image

from tests.test_api import client_for
from tests.test_models import valid_payload
from expression_studio.app import _MAX_REQUEST_BODY_BYTES


def png(color: tuple[int, int, int, int], *, size: tuple[int, int] = (8, 8)) -> bytes:
    output = BytesIO()
    Image.new("RGBA", size, color).save(output, format="PNG")
    return output.getvalue()


def import_parts(*images: bytes, declared_source: str = "CHATGPT_INCLUDED") -> tuple[dict[str, str], list[tuple[str, tuple[str, bytes, str]]]]:
    data = {
        "request_json": __import__("json").dumps(valid_payload()),
        "declared_source": declared_source,
    }
    files = [("candidates", (f"browser-{index}.png", image, "image/png")) for index, image in enumerate(images)]
    return data, files


def test_import_expression_candidates_without_a_provider_call(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    data, files = import_parts(png((255, 0, 0, 255)), png((0, 0, 255, 255)))

    response = client.post("/api/import-runs", data=data, files=files)

    assert response.status_code == 201
    run = response.json()
    assert run["status"] == "generated"
    assert run["candidate_count"] == 2
    assert run["engine"]["provenance"] == "subscription_handoff_import"
    assert run["engine"]["adapter_id"] == "expression.import.v1"
    assert run["cost"] == {"cost_route": "INCLUDED_OR_LOCAL_HANDOFF", "provider_call_made": False}
    assert run["cost_route"] == "INCLUDED_OR_LOCAL_HANDOFF"
    assert run["provider_call_made"] is False
    assert run["declared_source"] == "CHATGPT_INCLUDED"
    assert run["imported_files"][0]["index"] == 0
    assert run["imported_files"][0]["format"] == "PNG"
    assert client.get(f"/api/runs/{run['run_id']}/candidates/0").status_code == 200
    assert client.get(f"/api/runs/{run['run_id']}/candidates/1").status_code == 200


def test_import_mode_rejects_the_json_generation_route(tmp_path: Path) -> None:
    response = client_for(tmp_path, run_mode="subscription_handoff_import").post("/api/runs", json=valid_payload())

    assert response.status_code == 409
    assert response.json()["detail"] == "MODE_NOT_AVAILABLE"


def test_import_rejects_wrong_candidate_count_without_staging_candidates(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    data, files = import_parts(png((255, 0, 0, 255)))

    response = client.post("/api/import-runs", data=data, files=files)

    assert response.status_code == 422
    assert "expected 2" in response.json()["detail"]
    assert not list((tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio").rglob("candidate-*.png"))


def test_import_rejects_candidate_count_before_decoding_file_bodies(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")

    response = client.post(
        "/api/import-runs",
        data={"request_json": __import__("json").dumps(valid_payload()), "declared_source": "CHATGPT_INCLUDED"},
        files=[("candidates", ("ignored.bin", b"not-an-image", "application/octet-stream"))],
    )

    assert response.status_code == 422
    assert "expected 2" in response.json()["detail"]


def test_app_rejects_an_oversize_request_before_multipart_parsing(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")

    response = client.post(
        "/api/import-runs",
        content=b"not parsed",
        headers={"Content-Type": "multipart/form-data; boundary=ignored", "Content-Length": str(202 * 1024 * 1024 + 1)},
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "request body exceeds the configured safety limit"


def test_request_limit_covers_all_eight_documented_25_mib_candidates_plus_multipart_overhead() -> None:
    assert _MAX_REQUEST_BODY_BYTES >= (8 * 25 + 2) * 1024 * 1024


def test_import_rejects_transparent_anchor_identical_and_duplicate_candidates(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    cases = [
        (png((0, 0, 0, 0)), png((0, 0, 255, 255)), "transparent"),
        (png((255, 255, 255, 255)), png((0, 0, 255, 255)), "anchor"),
        (png((255, 0, 0, 255)), png((255, 0, 0, 255)), "pixel-duplicates"),
    ]

    for first, second, expected in cases:
        data, files = import_parts(first, second)
        response = client.post("/api/import-runs", data=data, files=files)
        assert response.status_code == 422
        assert expected in response.json()["detail"]


def test_import_rejects_malformed_request_and_unknown_declared_source(tmp_path: Path) -> None:
    client = client_for(tmp_path, run_mode="subscription_handoff_import")
    image_files = [("candidates", ("ignored.png", png((255, 0, 0, 255)), "image/png"))] * 2

    malformed = client.post(
        "/api/import-runs",
        data={"request_json": "{", "declared_source": "CHATGPT_INCLUDED"},
        files=image_files,
    )
    unknown = client.post(
        "/api/import-runs",
        data={"request_json": __import__("json").dumps(valid_payload()), "declared_source": "PAID_API"},
        files=image_files,
    )

    assert malformed.status_code == 422
    assert unknown.status_code == 422
