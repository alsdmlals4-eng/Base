from __future__ import annotations

import binascii
from pathlib import Path
import struct
import zlib

import pytest

from base_tool_contracts import ProjectFigmaRegistry
from test_projects import make_project
from tool_hub.figma_delivery import DeliveryError, FigmaDeliveryService
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
