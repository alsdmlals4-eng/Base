from pathlib import Path
import subprocess

from fastapi.testclient import TestClient
from PIL import Image

from expression_studio.app import create_app
from expression_studio.delivery import ProjectFigmaRegistry
from expression_studio.engine import FakeExpressionEngine
from tests.test_delivery import write_registry
from tests.test_models import valid_payload


def client_for(project_root: Path, *, initialize_vault: bool = True, bootstrap_security: bool = True) -> TestClient:
    anchor = project_root / "art" / "source" / "hero.png"
    anchor.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(anchor)
    if initialize_vault:
        subprocess.run(["git", "init", "-q", str(project_root)], check=True)
        (project_root / ".asset-vault" / "library").mkdir(parents=True, exist_ok=True)
        (project_root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    client = TestClient(
        create_app(
            project_root,
            FakeExpressionEngine(project_root),
            registry=ProjectFigmaRegistry.load(write_registry(project_root)),
            project_id="demo",
            bind_origin="http://testserver",
            test_mode=True,
        )
    )
    client.headers["Origin"] = "http://testserver"
    if bootstrap_security:
        config = client.get("/api/config").json()
        if "csrf_token" in config:
            client.headers["X-Studio-CSRF"] = config["csrf_token"]
    return client


def test_api_returns_conflict_details_before_generation(tmp_path: Path) -> None:
    response = client_for(tmp_path).post(
        "/api/runs",
        json=valid_payload(controls=[{"code": "AU43", "intensity": "B"}, {"code": "AU5", "intensity": "B"}]),
    )

    assert response.status_code == 422
    assert "AU43" in response.json()["detail"]


def test_config_exposes_bound_project_and_simulated_state(tmp_path: Path) -> None:
    response = client_for(tmp_path).get("/api/config")

    assert response.status_code == 200
    payload = response.json()
    assert payload["project_id"] == "demo"
    assert payload["engine_provenance"] == "simulated"
    assert payload["delivery_eligible"] is False
    assert payload["routing_state"] == "ROUTING_CONFIGURED"
    assert len(payload["csrf_token"]) >= 32


def test_status_exposes_immutable_child_identity(tmp_path: Path) -> None:
    payload = client_for(tmp_path).get("/api/status").json()

    assert payload["tool_id"] == "expression-studio"
    assert payload["project_id"] == "demo"
    assert payload["engine_provenance"] == "simulated"
    assert len(payload["launch_nonce"]) >= 32
    assert len(payload["config_hash"]) == 64
    assert len(payload["root_fingerprint"]) == 64
    assert len(payload["figma_registry_sha256"]) == 64
    assert len(payload["engine_config_sha256"]) == 64
    assert payload["process_id"] > 0


def test_status_identity_changes_across_project_roots(tmp_path: Path) -> None:
    left = tmp_path / "left"
    right = tmp_path / "right"
    left.mkdir()
    right.mkdir()

    left_status = client_for(left).get("/api/status").json()
    right_status = client_for(right).get("/api/status").json()

    assert left_status["root_fingerprint"] != right_status["root_fingerprint"]
    assert left_status["config_hash"] != right_status["config_hash"]


def test_production_app_does_not_allow_testserver_host(tmp_path: Path) -> None:
    app = create_app(tmp_path, FakeExpressionEngine(tmp_path), project_id="demo")
    assert TestClient(app).get("/api/config").status_code == 400


def test_mutation_rejects_missing_csrf_and_hostile_origin(tmp_path: Path) -> None:
    raw_client = client_for(tmp_path, bootstrap_security=False)
    missing = raw_client.post("/api/runs", json=valid_payload())
    client = client_for(tmp_path)
    foreign = client.post("/api/runs", json=valid_payload(), headers={"Origin": "https://evil.example"})
    hostile_host = client.post("/api/runs", json=valid_payload(), headers={"Host": "evil.example"})
    wrong_port = client.post("/api/runs", json=valid_payload(), headers={"Origin": "http://testserver:9999"})
    wrong_scheme = client.post("/api/runs", json=valid_payload(), headers={"Origin": "https://testserver"})
    missing_origin = client.post("/api/runs", json=valid_payload(), headers={"Origin": ""})

    assert missing.status_code == 403
    assert foreign.status_code == 403
    assert hostile_host.status_code == 400
    assert wrong_port.status_code == 403
    assert wrong_scheme.status_code == 403
    assert missing_origin.status_code == 403


def test_api_rejects_an_anchor_from_another_figma_file(tmp_path: Path) -> None:
    payload = valid_payload()
    payload["anchor"] = {
        "source_path": "art/source/hero.png",
        "figma_node_url": "https://www.figma.com/design/WRONG/source?node-id=1-2",
        "approval_status": "approved",
    }

    response = client_for(tmp_path).post("/api/runs", json=payload)

    assert response.status_code == 422
    assert "bound project" in response.json()["detail"]


def test_api_blocks_generation_when_project_asset_vault_is_missing(tmp_path: Path) -> None:
    response = client_for(tmp_path, initialize_vault=False).post("/api/runs", json=valid_payload())

    assert response.status_code == 422
    assert "asset vault" in response.json()["detail"]


def test_api_makes_generated_candidate_and_anchor_available_locally(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run = client.post("/api/runs", json=valid_payload()).json()
    run_id = run["run_id"]

    candidate = client.get(f"/api/runs/{run_id}/candidates/0")
    anchor = client.get(f"/api/runs/{run_id}/anchor")

    assert candidate.status_code == 200
    assert candidate.headers["content-type"] == "image/png"
    assert anchor.status_code == 200
    assert anchor.headers["content-type"] == "image/png"
    assert len(run["lineage"]["anchor_sha256"]) == 64
    assert run["resolved_expression"]["controls"] == [{"code": "AU46", "intensity": "C", "side": "left"}]


def test_api_marks_fake_generation_simulated_and_blocks_export(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run = client.post("/api/runs", json=valid_payload()).json()
    run_id = run["run_id"]

    export = client.post(f"/api/runs/{run_id}/export", json={"selected_candidate": 0})
    delivery = client.post(f"/api/runs/{run_id}/figma-delivery")

    assert run["engine"]["provenance"] == "simulated"
    assert run["engine"]["delivery_eligible"] is False
    assert run["engine"]["adapter_id"] == "expression.fake.v1"
    assert export.status_code == 409
    assert "simulated" in export.json()["detail"]
    assert delivery.status_code == 409
    assert delivery.json()["status"] == "blocked"
