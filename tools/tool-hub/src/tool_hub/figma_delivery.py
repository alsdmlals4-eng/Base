"""Project-scoped local queue for exact raster bytes destined for canonical Figma targets."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
import os
from pathlib import Path
import secrets
import struct
import tempfile
import time
from typing import Callable

from base_tool_contracts import DeliveryBlockedError, ProjectFigmaRegistry

from .projects import ProjectBindingError, ProjectLocator


class DeliveryError(RuntimeError):
    """Raised when a local Figma delivery operation must fail closed."""


@dataclass(frozen=True)
class DeliveryJob:
    delivery_id: str
    tool_id: str
    project_id: str
    run_id: str
    content_sha256: str
    byte_length: int
    media_type: str
    figma_file_key: str
    figma_url: str
    delivery_page_node_id: str
    generation_area_node_id: str
    state: str
    created_at: float
    expires_at: float


@dataclass(frozen=True)
class PairingView:
    project_id: str
    pairing_code: str
    figma_url: str
    expires_at: float


@dataclass(frozen=True)
class BridgeSession:
    token: str
    project_id: str
    figma_file_key: str
    bridge_version: str


@dataclass(frozen=True)
class _PairingRecord:
    project_id: str
    figma_file_key: str
    code_sha256: str
    expires_at: float


class FigmaDeliveryService:
    """Create local immutable queue entries bound to a reviewed project and Figma route."""

    JOB_TTL_SECONDS = 15 * 60
    PAIRING_TTL_SECONDS = 5 * 60
    MAX_IMAGE_BYTES = 10 * 1024 * 1024
    MAX_IMAGE_DIMENSION = 4096

    def __init__(
        self,
        runtime_root: Path,
        locator: ProjectLocator,
        registry: ProjectFigmaRegistry,
        *,
        clock: Callable[[], float] = time.time,
    ) -> None:
        self._runtime_root = Path(runtime_root)
        self._locator = locator
        self._registry = registry
        self._clock = clock
        self._pairings: dict[str, _PairingRecord] = {}
        self._sessions: dict[str, BridgeSession] = {}

    def create_pairing(self, project_id: str) -> PairingView:
        try:
            self._locator.resolve(project_id)
            target = self._registry.resolve_ready_target(project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
        code = f"{secrets.randbelow(1_000_000):06d}"
        now = float(self._clock())
        self._pairings[project_id] = _PairingRecord(
            project_id=project_id,
            figma_file_key=target.figma_file_key,
            code_sha256=hashlib.sha256(code.encode("ascii")).hexdigest(),
            expires_at=now + self.PAIRING_TTL_SECONDS,
        )
        return PairingView(project_id, code, target.figma_url, now + self.PAIRING_TTL_SECONDS)

    def pair(self, project_id: str, figma_file_key: str, pairing_code: str, bridge_version: str) -> BridgeSession:
        if not bridge_version:
            raise DeliveryError("BRIDGE_VERSION_REQUIRED")
        try:
            self._locator.resolve(project_id)
            target = self._registry.resolve_ready_target(project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
        if figma_file_key != target.figma_file_key:
            raise DeliveryError("FIGMA_ROUTE_MISMATCH")
        record = self._pairings.get(project_id)
        if record is None:
            raise DeliveryError("PAIRING_CODE_INVALID")
        if float(self._clock()) > record.expires_at:
            self._pairings.pop(project_id, None)
            raise DeliveryError("PAIRING_CODE_EXPIRED")
        actual = hashlib.sha256(pairing_code.encode("utf-8")).hexdigest()
        if not hmac.compare_digest(actual, record.code_sha256):
            raise DeliveryError("PAIRING_CODE_INVALID")
        self._pairings.pop(project_id, None)
        token = secrets.token_urlsafe(32)
        session = BridgeSession(token, project_id, target.figma_file_key, bridge_version)
        self._sessions[token] = session
        return session

    def enqueue(
        self,
        tool_id: str,
        project_id: str,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
    ) -> DeliveryJob:
        if not tool_id or not project_id or not run_id:
            raise DeliveryError("DELIVERY_IDENTITY_REQUIRED")
        if not isinstance(image_bytes, bytes) or not image_bytes:
            raise DeliveryError("DELIVERY_CONTENT_REQUIRED")
        self._validate_raster(image_bytes, media_type)
        try:
            binding = self._locator.resolve(project_id)
            target = self._registry.resolve_ready_target(project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error

        vault = binding.root / ".asset-vault"
        try:
            vault_root = vault.resolve(strict=True)
        except OSError as error:
            raise DeliveryError("PROJECT_DELIVERY_AREA_UNAVAILABLE") from error
        expected_vault = binding.root.resolve() / ".asset-vault"
        if vault_root != expected_vault or not vault_root.is_dir():
            raise DeliveryError("PROJECT_DELIVERY_AREA_UNAVAILABLE")

        delivery_id = secrets.token_hex(16)
        delivery_root = vault_root / "tool-hub-delivery" / delivery_id
        try:
            delivery_root.mkdir(parents=True, exist_ok=False)
        except OSError as error:
            raise DeliveryError("DELIVERY_QUEUE_WRITE_FAILED") from error

        now = float(self._clock())
        content_sha256 = hashlib.sha256(image_bytes).hexdigest()
        job = DeliveryJob(
            delivery_id=delivery_id,
            tool_id=tool_id,
            project_id=project_id,
            run_id=run_id,
            content_sha256=content_sha256,
            byte_length=len(image_bytes),
            media_type=media_type,
            figma_file_key=target.figma_file_key,
            figma_url=target.figma_url,
            delivery_page_node_id=target.delivery_page_node_id,
            generation_area_node_id=target.generation_area_node_id,
            state="QUEUED",
            created_at=now,
            expires_at=now + self.JOB_TTL_SECONDS,
        )
        try:
            self._atomic_write_bytes(delivery_root / "content.bin", image_bytes)
            self._atomic_write_text(
                delivery_root / "JOB.json",
                json.dumps(self._job_document(job), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            )
        except OSError as error:
            raise DeliveryError("DELIVERY_QUEUE_WRITE_FAILED") from error
        return job

    @classmethod
    def _validate_raster(cls, image_bytes: bytes, media_type: str) -> tuple[int, int]:
        if len(image_bytes) > cls.MAX_IMAGE_BYTES:
            raise DeliveryError("DELIVERY_IMAGE_TOO_LARGE")
        if media_type != "image/png":
            raise DeliveryError("DELIVERY_MEDIA_TYPE_UNSUPPORTED")
        if len(image_bytes) < 24 or image_bytes[:8] != b"\x89PNG\r\n\x1a\n" or image_bytes[12:16] != b"IHDR":
            raise DeliveryError("DELIVERY_IMAGE_INVALID")
        try:
            width, height = struct.unpack(">II", image_bytes[16:24])
        except struct.error as error:
            raise DeliveryError("DELIVERY_IMAGE_INVALID") from error
        if width < 1 or height < 1:
            raise DeliveryError("DELIVERY_IMAGE_INVALID")
        if width > cls.MAX_IMAGE_DIMENSION or height > cls.MAX_IMAGE_DIMENSION:
            raise DeliveryError("DELIVERY_IMAGE_DIMENSIONS_EXCEEDED")
        return width, height

    @staticmethod
    def _atomic_write_bytes(path: Path, data: bytes) -> None:
        descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}-", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass

    @classmethod
    def _atomic_write_text(cls, path: Path, text: str) -> None:
        cls._atomic_write_bytes(path, text.encode("utf-8"))

    @staticmethod
    def _job_document(job: DeliveryJob) -> dict[str, object]:
        return {
            "schema_version": 1,
            "delivery_id": job.delivery_id,
            "tool_id": job.tool_id,
            "project_id": job.project_id,
            "run_id": job.run_id,
            "content_sha256": job.content_sha256,
            "byte_length": job.byte_length,
            "media_type": job.media_type,
            "figma_file_key": job.figma_file_key,
            "delivery_page_node_id": job.delivery_page_node_id,
            "generation_area_node_id": job.generation_area_node_id,
            "state": job.state,
            "created_at": job.created_at,
            "expires_at": job.expires_at,
        }
