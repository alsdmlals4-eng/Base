from __future__ import annotations

import binascii
from pathlib import Path
import struct

import pytest

from test_figma_delivery import png_bytes, registry
from test_projects import make_project
from tool_hub.figma_delivery import DeliveryError, FigmaDeliveryService
from tool_hub.projects import ProjectLocator


def configured_service(tmp_path: Path) -> tuple[FigmaDeliveryService, ProjectLocator, Path, Path]:
    coc = make_project(tmp_path / "coc", "coc-fiction")
    omen = make_project(tmp_path / "omen", "omenward")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(coc, "coc-fiction")
    locator.register(omen, "omenward")
    return FigmaDeliveryService(tmp_path / "runtime", locator, registry()), locator, coc, omen


def test_pairing_codes_are_globally_unique_and_resolve_without_client_project_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    service, _, _, _ = configured_service(tmp_path)
    generated = iter((123456, 123456, 654321))
    monkeypatch.setattr("tool_hub._figma_delivery_base.secrets.randbelow", lambda _: next(generated))

    coc = service.create_pairing("coc-fiction")
    omen = service.create_pairing("omenward")

    assert coc.pairing_code == "123456"
    assert omen.pairing_code == "654321"
    coc_session = service.pair_by_code(coc.pairing_code, "bridge-test")
    omen_session = service.pair_by_code(omen.pairing_code, "bridge-test")
    assert coc_session.project_id == "coc-fiction"
    assert omen_session.project_id == "omenward"


def test_png_crc_and_terminal_chunk_are_validated_before_queueing(tmp_path: Path) -> None:
    service, _, _, _ = configured_service(tmp_path)
    valid = png_bytes()

    corrupted = bytearray(valid)
    corrupted[-5] ^= 0x01
    with pytest.raises(DeliveryError, match="DELIVERY_IMAGE_INVALID"):
        service.enqueue("expression-studio", "coc-fiction", "bad-crc", bytes(corrupted), "image/png")

    without_iend = valid[:-12]
    with pytest.raises(DeliveryError, match="DELIVERY_IMAGE_INVALID"):
        service.enqueue("expression-studio", "coc-fiction", "no-iend", without_iend, "image/png")

    with_trailing_bytes = valid + b"unexpected"
    with pytest.raises(DeliveryError, match="DELIVERY_IMAGE_INVALID"):
        service.enqueue("expression-studio", "coc-fiction", "trailing", with_trailing_bytes, "image/png")


def test_queued_job_recovers_after_hub_restart_and_can_be_claimed(tmp_path: Path) -> None:
    service, locator, _, _ = configured_service(tmp_path)
    payload = png_bytes(2, 1)
    job = service.enqueue("expression-studio", "coc-fiction", "run-restart", payload, "image/png")

    restarted = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    pairing = restarted.create_pairing("coc-fiction")
    token = restarted.pair_by_code(pairing.pairing_code, "bridge-test").token
    recovered = restarted.claim_next(token)

    assert recovered is not None
    assert recovered.delivery_id == job.delivery_id
    assert recovered.state == "CLAIMED"
    assert restarted.content(token, job.delivery_id) == payload


def test_claimed_job_is_safely_requeued_after_hub_restart(tmp_path: Path) -> None:
    service, locator, _, _ = configured_service(tmp_path)
    job = service.enqueue("expression-studio", "coc-fiction", "run-crash", png_bytes(), "image/png")
    pairing = service.create_pairing("coc-fiction")
    token = service.pair_by_code(pairing.pairing_code, "bridge-test").token
    claimed = service.claim_next(token)
    assert claimed is not None and claimed.delivery_id == job.delivery_id

    restarted = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    new_pairing = restarted.create_pairing("coc-fiction")
    new_token = restarted.pair_by_code(new_pairing.pairing_code, "bridge-test").token
    recovered = restarted.claim_next(new_token)

    assert recovered is not None
    assert recovered.delivery_id == job.delivery_id
    assert recovered.state == "CLAIMED"


def test_tampered_durable_job_is_not_recovered_or_deleted(tmp_path: Path) -> None:
    service, locator, coc, _ = configured_service(tmp_path)
    job = service.enqueue("expression-studio", "coc-fiction", "run-tampered", png_bytes(), "image/png")
    job_path = coc / ".asset-vault" / "tool-hub-delivery" / job.delivery_id / "JOB.json"
    original = job_path.read_bytes()
    job_path.write_bytes(original.replace(b'"project_id": "coc-fiction"', b'"project_id": "omenward"'))

    restarted = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    pairing = restarted.create_pairing("coc-fiction")
    token = restarted.pair_by_code(pairing.pairing_code, "bridge-test").token

    assert restarted.claim_next(token) is None
    assert job_path.is_file()
    assert job_path.read_bytes() != original
