from __future__ import annotations

from pathlib import Path

from expression_studio.app import _MAX_REQUEST_BODY_BYTES
from tests.test_confirm_delivery import RecordingSender, confirmed_client
from tests.test_import_api import png
from tests.test_models import valid_payload


def candidate_files():
    return [
        ("candidates", ("chatgpt-red.png", png((220, 30, 30, 255)), "image/png")),
        ("candidates", ("chatgpt-blue.png", png((30, 30, 220, 255)), "image/png")),
    ]


def test_prepare_handoff_returns_server_run_and_fixed_subscription_truth(tmp_path: Path) -> None:
    client = confirmed_client(tmp_path, RecordingSender())

    response = client.post("/api/handoff-runs", json=valid_payload())

    assert response.status_code == 201, response.text
    body = response.json()
    assert len(body["run_id"]) == 32
    assert body["state"] == "GPT_PRO_HANDOFF_READY"
    assert body["generation_surface"] == "CHATGPT_PRO_SUBSCRIPTION"
    assert body["run_mode"] == "subscription_handoff_import"
    assert body["declared_source"] == "CHATGPT_INCLUDED"
    assert body["provider_call_made"] is False
    assert body["requires_additional_payment"] is False
    assert body["run_id"] in body["prompt"]
    assert "https://www.figma.com/" not in body["prompt"]
    assert str(tmp_path) not in body["prompt"]
    assert body["source"]["filename"] == "hero.png"
    assert len(body["source"]["sha256"]) == 64


def test_handoff_candidate_import_uses_exact_server_run_and_consumes_once(tmp_path: Path) -> None:
    client = confirmed_client(tmp_path, RecordingSender())
    prepared = client.post("/api/handoff-runs", json=valid_payload()).json()
    run_id = prepared["run_id"]

    response = client.post(f"/api/handoff-runs/{run_id}/import", files=candidate_files())
    replay = client.post(f"/api/handoff-runs/{run_id}/import", files=candidate_files())

    assert response.status_code == 201, response.text
    run = response.json()
    assert run["run_id"] == run_id
    assert run["status"] == "generated"
    assert run["run_mode"] == "subscription_handoff_import"
    assert run["declared_source"] == "CHATGPT_INCLUDED"
    assert run["provider_call_made"] is False
    assert replay.status_code == 404
    assert client.get(f"/api/runs/{run_id}/candidates/0").status_code == 200
    assert client.get(f"/api/runs/{run_id}/candidates/1").status_code == 200


def test_failed_handoff_import_keeps_same_server_run_retryable(tmp_path: Path) -> None:
    client = confirmed_client(tmp_path, RecordingSender())
    run_id = client.post("/api/handoff-runs", json=valid_payload()).json()["run_id"]

    invalid = client.post(
        f"/api/handoff-runs/{run_id}/import",
        files=[candidate_files()[0]],
    )
    valid = client.post(f"/api/handoff-runs/{run_id}/import", files=candidate_files())

    assert invalid.status_code == 422
    assert "expected 2" in invalid.json()["detail"]
    assert valid.status_code == 201, valid.text
    assert valid.json()["run_id"] == run_id


def test_unknown_handoff_run_fails_before_candidate_staging(tmp_path: Path) -> None:
    client = confirmed_client(tmp_path, RecordingSender())

    response = client.post(f"/api/handoff-runs/{'f' * 32}/import", files=candidate_files())

    assert response.status_code == 404
    generated = tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio"
    assert not generated.exists()


def test_handoff_import_does_not_accept_browser_supplied_request_or_source_truth(tmp_path: Path) -> None:
    client = confirmed_client(tmp_path, RecordingSender())
    run_id = client.post("/api/handoff-runs", json=valid_payload()).json()["run_id"]

    response = client.post(
        f"/api/handoff-runs/{run_id}/import",
        data={
            "project_id": "other-project",
            "request_json": "{}",
            "declared_source": "OTHER_USER_SUPPLIED",
        },
        files=candidate_files(),
    )

    assert response.status_code == 201, response.text
    assert response.json()["run_id"] == run_id
    assert response.json()["declared_source"] == "CHATGPT_INCLUDED"


def test_handoff_import_rejects_oversize_before_multipart_parsing(tmp_path: Path) -> None:
    client = confirmed_client(tmp_path, RecordingSender())
    run_id = client.post("/api/handoff-runs", json=valid_payload()).json()["run_id"]

    response = client.post(
        f"/api/handoff-runs/{run_id}/import",
        content=b"not parsed",
        headers={
            "Content-Type": "multipart/form-data; boundary=ignored",
            "Content-Length": str(_MAX_REQUEST_BODY_BYTES + 1),
        },
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "request body exceeds the configured safety limit"
