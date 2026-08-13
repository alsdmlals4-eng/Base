from pathlib import Path
import subprocess

from fastapi.testclient import TestClient
from PIL import Image

from qa_evidence_studio.app import create_app


def make_project(root: Path) -> Path:
    root.mkdir(exist_ok=True)
    if not (root / ".git").exists():
        subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (root / ".asset-vault" / "library").mkdir(parents=True, exist_ok=True)
    if not (root / "project.godot").exists():
        (root / "project.godot").write_text("[application]\nconfig/name=\"QA Fixture\"\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(root), "add", ".gitignore", "project.godot"], check=True)
        subprocess.run(
            ["git", "-C", str(root), "-c", "user.name=QA", "-c", "user.email=qa@example.invalid", "commit", "-qm", "fixture"],
            check=True,
        )
    return root


def client_for(tmp_path: Path, *, bootstrap: bool = True) -> TestClient:
    project = make_project(tmp_path / "project")
    client = TestClient(
        create_app(
            project,
            "demo-game",
            launch_nonce="n" * 32,
            bind_origin="http://testserver",
            test_mode=True,
        )
    )
    client.headers["Origin"] = "http://testserver"
    if bootstrap:
        config = client.get("/api/config").json()
        client.headers["X-QA-CSRF"] = config["csrf_token"]
    return client


def session_payload(project: Path) -> dict[str, object]:
    return {
        "title": "Main menu review",
        "build_commit": subprocess.check_output(["git", "-C", str(project), "rev-parse", "HEAD"], text=True).strip(),
        "checklist": [
            {"item_id": "visual-readability", "label": "Image readability", "required": True},
            {"item_id": "keyboard-flow", "label": "Keyboard UX", "required": True},
        ],
    }


def image_file(tmp_path: Path) -> Path:
    path = tmp_path / "screen.png"
    Image.new("RGBA", (12, 12), (30, 60, 90, 255)).save(path)
    return path


def test_config_and_status_expose_bound_identity_and_phase_limits(tmp_path: Path) -> None:
    client = client_for(tmp_path)

    config = client.get("/api/config").json()
    status = client.get("/api/status").json()

    assert config["project_id"] == "demo-game"
    assert config["reviewer_role"] == "DEVELOPER_OWNER"
    assert config["android_status"] == "DEFERRED_NOT_CONNECTED"
    assert config["actual_review_gate"] == "AFTER_IMAGE_AND_UX_PLACEMENT"
    assert len(config["csrf_token"]) >= 32
    assert status["tool_id"] == "qa-evidence-studio"
    assert status["project_id"] == "demo-game"
    assert status["launch_nonce"] == "n" * 32
    assert status["process_id"] > 0
    assert len(status["root_fingerprint"]) == 64
    assert len(status["config_hash"]) == 64


def test_api_runs_developer_pc_evidence_flow_without_false_android_pass(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    project = tmp_path / "project"
    created = client.post("/api/sessions", json=session_payload(project))
    session_id = created.json()["session_id"]

    ready = client.post(
        f"/api/sessions/{session_id}/visual-ux-ready",
        json={"acknowledgement": "Images and UX are placed for this PC review."},
    )
    for item_id in ("visual-readability", "keyboard-flow"):
        result = client.post(
            f"/api/sessions/{session_id}/results",
            json={"item_id": item_id, "status": "PASS", "note": "Developer checked on PC"},
        )
        assert result.status_code == 200
    path = image_file(tmp_path)
    with path.open("rb") as stream:
        evidence = client.post(
            f"/api/sessions/{session_id}/evidence",
            files={"image": (path.name, stream, "image/png")},
        )
    final = client.post(f"/api/sessions/{session_id}/finalize")

    assert created.status_code == 201
    assert ready.json()["stage"] == "READY_FOR_DEVELOPER_PC_REVIEW"
    assert evidence.status_code == 201
    assert final.status_code == 200
    payload = final.json()
    assert payload["overall_result"] == "PASS"
    assert payload["platforms"]["android"]["status"] == "DEFERRED_NOT_CONNECTED"
    assert payload["packet_relative_path"].endswith("QA_EVIDENCE_PACKET.json")
    assert str(tmp_path) not in str(payload)


def test_api_blocks_result_before_visual_ux_gate(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    session_id = client.post("/api/sessions", json=session_payload(tmp_path / "project")).json()["session_id"]

    response = client.post(
        f"/api/sessions/{session_id}/results",
        json={"item_id": "visual-readability", "status": "PASS", "note": "premature"},
    )

    assert response.status_code == 409
    assert "image and UX placement" in response.json()["detail"]


def test_mutation_rejects_missing_session_csrf_and_foreign_origin(tmp_path: Path) -> None:
    raw = client_for(tmp_path, bootstrap=False)
    missing = raw.post("/api/sessions", json=session_payload(tmp_path / "project"))
    client = client_for(tmp_path)
    foreign = client.post(
        "/api/sessions", json=session_payload(tmp_path / "project"), headers={"Origin": "https://evil.example"}
    )
    hostile_host = client.post(
        "/api/sessions", json=session_payload(tmp_path / "project"), headers={"Host": "evil.example"}
    )

    assert missing.status_code == 403
    assert foreign.status_code == 403
    assert hostile_host.status_code == 400


def test_production_app_does_not_allow_testserver_host(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    assert TestClient(create_app(project, "demo-game")).get("/api/config").status_code == 400
