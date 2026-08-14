from __future__ import annotations

import binascii
from pathlib import Path
import struct
import zlib

from base_tool_contracts import ProjectFigmaRegistry
from test_projects import make_project
from tool_hub.figma_delivery import FigmaDeliveryService
from tool_hub.projects import ProjectLocator


BASE_ROOT = Path(__file__).resolve().parents[3]


def png_bytes() -> bytes:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", binascii.crc32(body) & 0xFFFFFFFF)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)
    raw = b"\x00\x00\x00\x00\xff"
    return signature + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")


def test_delivery_queue_binds_project_and_canonical_figma_target(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project", "coc-fiction")
    locator = ProjectLocator(tmp_path / "machine-projects.json")
    locator.register(project, "coc-fiction")
    registry = ProjectFigmaRegistry.load(BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json")
    service = FigmaDeliveryService(tmp_path / "runtime", locator, registry)

    job = service.enqueue("expression-studio", "coc-fiction", "run-1", png_bytes(), "image/png")
    target = registry.resolve_ready_target("coc-fiction")

    assert job.project_id == "coc-fiction"
    assert job.figma_file_key == target.figma_file_key
    assert job.generation_area_node_id == target.generation_area_node_id
    assert job.state == "QUEUED"
    assert (project / ".asset-vault" / "tool-hub-delivery" / job.delivery_id / "content.bin").is_file()
