from __future__ import annotations

import hashlib
from pathlib import Path

import expression_studio.app as app_module
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


def test_duplicate_handoff_candidates_fail_without_consuming_pending_run(tmp_path: Path) -> None:
    client = confirmed_client(tmp_path, RecordingSender())
    run_id = client.post("/api/handoff-runs", json=valid_payload()).json()["run_id"]
    duplicate = png((220, 30, 30, 255))

    invalid = client.post(
        f"/api/handoff-runs/{run_id}/import",
        files=[
            ("candidates", ("duplicate-a.png", duplicate, "image/png")),
            ("candidates", ("duplicate-b.png", duplicate, "image/png")),
        ],
    )
    valid = client.post(f"/api/handoff-runs/{run_id}/import", files=candidate_files())

    assert invalid.status_code == 422
    assert "pixel-duplicates" in invalid.json()["detail"]
    assert valid.status_code == 201, valid.text
    assert valid.json()["run_id"] == run_id


def test_unknown_handoff_run_fails_before_candidate_staging(tmp_path: Path) -> None:
    client = confirmed_client(tmp_path, RecordingSender())

    response = client.post(f"/api/handoff-runs/{'f' * 32}/import", files=candidate_files())

    assert response.status_code == 404
    generated = tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio"
    assert not generated.exists()


def test_unknown_handoff_run_is_rejected_before_candidate_bytes_are_read(tmp_path: Path, monkeypatch) -> None:
    client = confirmed_client(tmp_path, RecordingSender())

    async def should_not_read(_upload):
        raise AssertionError("unknown handoff must be rejected before candidate bytes are read")

    monkeypatch.setattr(app_module, "read_upload_limited", should_not_read)

    response = client.post(f"/api/handoff-runs/{'e' * 32}/import", files=candidate_files())

    assert response.status_code == 404


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


def test_same_run_handoff_composes_through_confirm_and_verified_receipt(tmp_path: Path) -> None:
    sender = RecordingSender()
    client = confirmed_client(tmp_path, sender)
    prepared = client.post("/api/handoff-runs", json=valid_payload())
    assert prepared.status_code == 201, prepared.text
    run_id = prepared.json()["run_id"]

    imported = client.post(f"/api/handoff-runs/{run_id}/import", files=candidate_files())
    assert imported.status_code == 201, imported.text
    assert imported.json()["run_id"] == run_id

    confirmed = client.post(
        f"/api/runs/{run_id}/confirm-delivery",
        json={"selected_candidate": 0},
    )
    assert confirmed.status_code == 200, confirmed.text
    confirmation = confirmed.json()
    assert confirmation["project_save"] == "SAVED"
    assert confirmation["figma_delivery"] == "BRIDGE_REQUIRED"
    assert confirmation["delivery_state"] == "DELIVERY_PENDING"
    assert sender.calls[0][0] == run_id
    assert sender.calls[0][2] == "image/png"
    assert confirmation["content_sha256"] == hashlib.sha256(sender.calls[0][1]).hexdigest()

    sender.verified = True
    verified = client.get(confirmation["delivery_status_url"])
    assert verified.status_code == 200, verified.text
    receipt = verified.json()
    assert receipt["figma_delivery"] == "VERIFIED"
    assert receipt["bridge_state"] == "BRIDGE_PAIRED"
    assert receipt["delivery_state"] == "FIGMA_DELIVERED_VERIFIED"
    assert receipt["delivery_id"] == confirmation["delivery_id"]
    assert receipt["content_sha256"] == confirmation["content_sha256"]
