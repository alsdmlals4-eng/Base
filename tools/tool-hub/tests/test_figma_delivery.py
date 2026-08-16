from __future__ import annotations

import binascii
import json
from pathlib import Path
import struct
import zlib

import pytest

from base_tool_contracts import ProjectFigmaRegistry
from test_projects import make_project
from tool_hub.figma_delivery import BridgeReceipt, DeliveryError, FigmaDeliveryService
from tool_hub.projects import ProjectLocator


BASE_ROOT = Path(__file__).resolve().parents[3]


def png_bytes(width: int = 1, height: int = 1) -> bytes:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", binascii.crc32(body) & 0xFFFFFFFF)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    raw = b"".join(b"\x00" + (b"\x00\x00\x00\xff" * width) for _ in range(height))
    return signature + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def registry() -> ProjectFigmaRegistry:
    return ProjectFigmaRegistry.load(BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json")


def paired_token(service: FigmaDeliveryService, project_id: str) -> str:
    target = registry().resolve_ready_target(project_id)
    pairing = service.create_pairing(project_id)
    return service.pair(project_id, target.figma_file_key, pairing.pairing_code, "bridge-test").token


def test_delivery_queue_binds_project_and_canonical_figma_target(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry())

    job = service.enqueue("expression-studio", "coc-fiction", "run-1", png_bytes(), "image/png")
    target = registry().resolve_ready_target("coc-fiction")

    assert job.project_id == "coc-fiction"
    assert job.figma_file_key == target.figma_file_key
    assert job.generation_area_node_id == target.generation_area_node_id
    assert job.state == "QUEUED"
    assert (project / ".asset-vault" / "tool-hub-delivery" / job.delivery_id / "content.bin").is_file()


def test_enqueue_rejects_unreviewed_or_invalid_raster_bytes(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry())

    with pytest.raises(DeliveryError, match="DELIVERY_MEDIA_TYPE_UNSUPPORTED"):
        service.enqueue("expression-studio", "coc-fiction", "svg", b"<svg/>", "image/svg+xml")
    with pytest.raises(DeliveryError, match="DELIVERY_IMAGE_INVALID"):
        service.enqueue("expression-studio", "coc-fiction", "bad", b"not-a-png", "image/png")
    with pytest.raises(DeliveryError, match="DELIVERY_IMAGE_DIMENSIONS_EXCEEDED"):
        service.enqueue("expression-studio", "coc-fiction", "wide", png_bytes(4097, 1), "image/png")
    with pytest.raises(DeliveryError, match="DELIVERY_IMAGE_TOO_LARGE"):
        service.enqueue("expression-studio", "coc-fiction", "huge", b"x" * (10 * 1024 * 1024 + 1), "image/png")


def test_pairing_is_one_time_and_bound_to_exact_project_figma_file(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    target = registry().resolve_ready_target("coc-fiction")

    pairing = service.create_pairing("coc-fiction")
    with pytest.raises(DeliveryError, match="FIGMA_ROUTE_MISMATCH"):
        service.pair("coc-fiction", "wrong-file-key", pairing.pairing_code, "bridge-test")

    session = service.pair("coc-fiction", target.figma_file_key, pairing.pairing_code, "bridge-test")
    assert session.project_id == "coc-fiction"
    assert session.figma_file_key == target.figma_file_key
    assert session.token

    with pytest.raises(DeliveryError, match="PAIRING_CODE_INVALID"):
        service.pair("coc-fiction", target.figma_file_key, pairing.pairing_code, "bridge-test")


def test_bridge_session_claims_and_reads_only_its_project_jobs(tmp_path: Path) -> None:
    coc = make_project(tmp_path / "coc", "coc-fiction")
    omen = make_project(tmp_path / "omen", "omenward")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(coc, "coc-fiction")
    locator.register(omen, "omenward")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    coc_token = paired_token(service, "coc-fiction")
    omen_token = paired_token(service, "omenward")
    coc_bytes = png_bytes()
    omen_bytes = png_bytes(2, 1)
    coc_job = service.enqueue("expression-studio", "coc-fiction", "run-coc", coc_bytes, "image/png")
    omen_job = service.enqueue("expression-studio", "omenward", "run-omen", omen_bytes, "image/png")

    coc_claim = service.claim_next(coc_token)
    omen_claim = service.claim_next(omen_token)

    assert coc_claim is not None and coc_claim.delivery_id == coc_job.delivery_id
    assert omen_claim is not None and omen_claim.delivery_id == omen_job.delivery_id
    assert service.content(coc_token, coc_job.delivery_id) == coc_bytes
    assert service.content(omen_token, omen_job.delivery_id) == omen_bytes
    with pytest.raises(DeliveryError, match="DELIVERY_SCOPE_MISMATCH"):
        service.content(coc_token, omen_job.delivery_id)


def test_release_returns_claimed_job_to_same_project_queue(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    token = paired_token(service, "coc-fiction")
    job = service.enqueue("expression-studio", "coc-fiction", "run-retry", png_bytes(), "image/png")

    claimed = service.claim_next(token)
    assert claimed is not None and claimed.state == "CLAIMED"
    released = service.release(token, job.delivery_id)
    assert released.state == "QUEUED"
    reclaimed = service.claim_next(token)
    assert reclaimed is not None and reclaimed.delivery_id == job.delivery_id


def test_content_hash_is_revalidated_after_queue_tamper(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    token = paired_token(service, "coc-fiction")
    job = service.enqueue("expression-studio", "coc-fiction", "run-tamper", png_bytes(), "image/png")
    assert service.claim_next(token) is not None

    content = project / ".asset-vault" / "tool-hub-delivery" / job.delivery_id / "content.bin"
    content.write_bytes(png_bytes(2, 1))

    with pytest.raises(DeliveryError, match="DELIVERY_CONTENT_CHANGED"):
        service.content(token, job.delivery_id)


def test_pairing_and_queued_job_expire_fail_closed(tmp_path: Path) -> None:
    now = [1000.0]
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry(), clock=lambda: now[0])
    target = registry().resolve_ready_target("coc-fiction")

    expired_pairing = service.create_pairing("coc-fiction")
    now[0] += 301
    with pytest.raises(DeliveryError, match="PAIRING_CODE_EXPIRED"):
        service.pair("coc-fiction", target.figma_file_key, expired_pairing.pairing_code, "bridge-test")

    token = paired_token(service, "coc-fiction")
    job = service.enqueue("expression-studio", "coc-fiction", "run-expired", png_bytes(), "image/png")
    now[0] += 901
    assert service.claim_next(token) is None
    assert service.job_view("coc-fiction", job.delivery_id).state == "EXPIRED"


def test_finalize_validates_receipt_and_writes_secret_free_immutable_evidence(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry())
    token = paired_token(service, "coc-fiction")
    job = service.enqueue("expression-studio", "coc-fiction", "run-final", png_bytes(), "image/png")
    claimed = service.claim_next(token)
    assert claimed is not None

    with pytest.raises(DeliveryError, match="FIGMA_TARGET_MISMATCH"):
        service.finalize(token, job.delivery_id, BridgeReceipt(
            "999:1", claimed.node_name, "999:999", claimed.content_sha256, "bridge-test", "image-hash"
        ))
    with pytest.raises(DeliveryError, match="DELIVERY_HASH_MISMATCH"):
        service.finalize(token, job.delivery_id, BridgeReceipt(
            "999:1", claimed.node_name, claimed.target_node_id, "0" * 64, "bridge-test", "image-hash"
        ))
    with pytest.raises(DeliveryError, match="FIGMA_NODE_IDENTITY_MISMATCH"):
        service.finalize(token, job.delivery_id, BridgeReceipt(
            "999:1", "wrong-name", claimed.target_node_id, claimed.content_sha256, "bridge-test", "image-hash"
        ))

    receipt = service.finalize(token, job.delivery_id, BridgeReceipt(
        "999:1", claimed.node_name, claimed.target_node_id, claimed.content_sha256, "bridge-test", "image-hash"
    ))
    assert receipt.state == "DELIVERED_VERIFIED"
    evidence = project / ".asset-vault" / "tool-hub-delivery" / job.delivery_id / "FIGMA_DELIVERY_RECEIPT.json"
    stored = json.loads(evidence.read_text(encoding="utf-8"))
    assert stored["delivery_id"] == job.delivery_id
    assert stored["created_node_id"] == "999:1"
    assert stored["content_sha256"] == claimed.content_sha256
    assert stored["target_node_id"] == claimed.target_node_id
    assert stored["tool_route_id"] == claimed.tool_route_id
    serialized = json.dumps(stored)
    assert token not in serialized
    assert str(project.resolve()) not in serialized
    assert "pairing_code" not in serialized

    with pytest.raises(DeliveryError, match="DELIVERY_ALREADY_VERIFIED"):
        service.finalize(token, job.delivery_id, BridgeReceipt(
            "999:2", claimed.node_name, claimed.target_node_id, claimed.content_sha256, "bridge-test", "image-hash-2"
        ))
