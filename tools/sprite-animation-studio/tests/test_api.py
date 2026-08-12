from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from sprite_animation_studio.app import create_app
from sprite_animation_studio.engine import FakeSpriteEngine
from tests.test_models import valid_payload


def client_for(project_root: Path) -> TestClient:
    source = project_root / "art" / "source"
    source.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source / "idle.png")
    return TestClient(create_app(project_root, FakeSpriteEngine()))


def test_create_run_returns_422_without_an_approved_anchor(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    payload = valid_payload(anchor={"source_path": "art/source/idle.png", "figma_node_url": "https://www.figma.com/design/demo?node-id=1-2", "approval_status": "draft"})

    response = client.post("/api/runs", json=payload)

    assert response.status_code == 422


def test_export_rejects_an_incomplete_selection(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    response = client.post("/api/runs", json=valid_payload())
    run_id = response.json()["run_id"]

    export = client.post(f"/api/runs/{run_id}/export", json={"selected": [0, 1, 2]})

    assert export.status_code == 409
    assert export.json()["status"] == "blocked"


def test_generated_candidate_frame_is_available_to_the_local_workspace(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]

    frame = client.get(f"/api/runs/{run_id}/frames/0")

    assert frame.status_code == 200
    assert frame.headers["content-type"] == "image/png"


def test_approved_anchor_image_is_available_to_the_local_workspace(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]

    anchor = client.get(f"/api/runs/{run_id}/anchor")

    assert anchor.status_code == 200
    assert anchor.headers["content-type"] == "image/png"


def test_curation_persists_transform_values_from_the_browser_shape(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]

    response = client.post(f"/api/runs/{run_id}/curation", json={"selected": [0, 1, 2, 3], "transforms": {"1": {"dx": 3, "dy": -2, "scale": 1.2}}})

    assert response.status_code == 200
    assert response.json()["status"] == "curated"


def test_export_writes_project_local_outputs_after_full_selection(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run_id = client.post("/api/runs", json=valid_payload(output_root="art/derived/knight")).json()["run_id"]

    response = client.post(f"/api/runs/{run_id}/export", json={"selected": [0, 1, 2, 3]})

    assert response.status_code == 200
    assert response.json()["status"] == "exported"
    assert list((tmp_path / "art" / "derived" / "knight").glob("*/exports/atlas.png"))
