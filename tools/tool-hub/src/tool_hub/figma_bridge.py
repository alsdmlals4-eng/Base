"""Fail-closed project-scoped delivery contracts for the localhost Figma Bridge."""

from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
from pathlib import Path
import secrets
import time
from typing import Callable

from base_tool_contracts import ProjectFigmaTarget


_ALLOWED_MEDIA_TYPES = frozenset({"image/png", "image/jpeg", "image/gif", "image/webp"})


class BridgeError(RuntimeError):
    """Raised when a Figma Bridge request cannot satisfy the reviewed contract."""


@dataclass(frozen=True)
class PairingSession:
    project_id: str
    figma_file_key: str
    generation_area_node_id: str
    expires_at: float
    pairing_code: str = ""
    capability_token: str = ""


@dataclass(frozen=True)
class DeliveryJob:
    delivery_id: str
    tool_id: str
    project_id: str
    run_id: str
    figma_file_key: str
    generation_area_node_id: str
    artifact_sha256: str
    artifact_byte_length: int
    media_type: str
    created_at: float
    expires_at: float
    _export_path: Path

    def public_view(self) -> dict[str, object]:
        return {
            "delivery_id": self.delivery_id,
            "tool_id": self.tool_id,
            "project_id": self.project_id,
            "run_id": self.run_id,
            "figma_file_key": self.figma_file_key,
            "generation_area_node_id": self.generation_area_node_id,
            "artifact_sha256": self.artifact_sha256,
            "artifact_byte_length": self.artifact_byte_length,
            "media_type": self.media_type,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
        }


@dataclass(frozen=True)
class DeliveryReceipt:
    delivery_id: str
    project_id: str
    figma_file_key: str
    generation_area_node_id: str
    created_node_id: str
    artifact_sha256: str
    artifact_byte_length: int
    width: int
    height: int
    status: str = "FIGMA_DELIVERY_PENDING"

    def public_view(self) -> dict[str, object]:
        return {
            "delivery_id": self.delivery_id,
            "project_id": self.project_id,
            "figma_file_key": self.figma_file_key,
            "generation_area_node_id": self.generation_area_node_id,
            "created_node_id": self.created_node_id,
            "artifact_sha256": self.artifact_sha256,
            "artifact_byte_length": self.artifact_byte_length,
            "width": self.width,
            "height": self.height,
            "status": self.status,
        }


class FigmaBridgeStore:
    """In-memory authority for short-lived Figma delivery jobs and capabilities.

    Absolute export paths are retained only inside this local process. Public views never
    expose them. Durable verified receipts are added by the later persistence slice.
    """

    def __init__(self, private_root: Path, *, now: Callable[[], float] | None = None) -> None:
        self._private_root = private_root.resolve()
        self._private_root.mkdir(parents=True, exist_ok=True)
        self._now = now or time.time
        self._pairings: dict[str, PairingSession] = {}
        self._capabilities: dict[str, PairingSession] = {}
        self._jobs: dict[str, DeliveryJob] = {}
        self._receipts: dict[str, DeliveryReceipt] = {}

    def create_pairing(
        self,
        *,
        project_id: str,
        target: ProjectFigmaTarget,
        ttl_seconds: int = 300,
    ) -> PairingSession:
        if target.project_id != project_id:
            raise BridgeError("pairing project does not match the canonical Figma target")
        if ttl_seconds <= 0:
            raise BridgeError("pairing ttl must be positive")
        code = secrets.token_urlsafe(18)
        session = PairingSession(
            project_id=project_id,
            figma_file_key=target.figma_file_key,
            generation_area_node_id=target.generation_area_node_id,
            expires_at=self._now() + ttl_seconds,
            pairing_code=code,
        )
        self._pairings[code] = session
        return session

    def exchange_pairing(self, *, code: str, current_file_key: str) -> PairingSession:
        matched_key = next(
            (stored for stored in self._pairings if secrets.compare_digest(stored, code)),
            None,
        )
        if matched_key is None:
            raise BridgeError("pairing code is unavailable or already used")
        session = self._pairings.pop(matched_key)
        if self._now() > session.expires_at:
            raise BridgeError("pairing code expired")
        if not secrets.compare_digest(session.figma_file_key, current_file_key):
            raise BridgeError("pairing Figma file does not match the registered project route")
        token = secrets.token_urlsafe(32)
        capability = replace(session, pairing_code="", capability_token=token)
        self._capabilities[token] = capability
        return capability

    def enqueue(
        self,
        *,
        tool_id: str,
        project_id: str,
        run_id: str,
        export_path: Path,
        target: ProjectFigmaTarget,
        media_type: str,
        ttl_seconds: int = 900,
    ) -> DeliveryJob:
        if target.project_id != project_id:
            raise BridgeError("delivery project does not match the canonical Figma target")
        if media_type not in _ALLOWED_MEDIA_TYPES:
            raise BridgeError("delivery media type is not supported")
        if ttl_seconds <= 0:
            raise BridgeError("delivery ttl must be positive")
        resolved = export_path.resolve()
        if not resolved.is_file():
            raise BridgeError("delivery export is unavailable")
        try:
            content = resolved.read_bytes()
        except OSError as error:
            raise BridgeError("delivery export is unreadable") from error
        if not content:
            raise BridgeError("delivery export is empty")
        now = self._now()
        job = DeliveryJob(
            delivery_id=secrets.token_urlsafe(18),
            tool_id=tool_id,
            project_id=project_id,
            run_id=run_id,
            figma_file_key=target.figma_file_key,
            generation_area_node_id=target.generation_area_node_id,
            artifact_sha256=hashlib.sha256(content).hexdigest(),
            artifact_byte_length=len(content),
            media_type=media_type,
            created_at=now,
            expires_at=now + ttl_seconds,
            _export_path=resolved,
        )
        self._jobs[job.delivery_id] = job
        return job

    def claim_next(self, *, capability_token: str, current_file_key: str) -> DeliveryJob | None:
        capability = self._capability(capability_token)
        if not secrets.compare_digest(capability.figma_file_key, current_file_key):
            raise BridgeError("capability Figma file does not match the current file")
        for job in self._jobs.values():
            if job.delivery_id in self._receipts:
                continue
            if self._now() > job.expires_at:
                continue
            if job.project_id != capability.project_id:
                continue
            if not secrets.compare_digest(job.figma_file_key, capability.figma_file_key):
                continue
            return job
        return None

    def artifact_bytes(self, *, capability_token: str, delivery_id: str) -> bytes:
        capability = self._capability(capability_token)
        job = self._job_for_capability(delivery_id, capability)
        if self._now() > job.expires_at:
            raise BridgeError("delivery job expired")
        try:
            content = job._export_path.read_bytes()
        except OSError as error:
            raise BridgeError("delivery export is unavailable") from error
        if len(content) != job.artifact_byte_length or not secrets.compare_digest(
            hashlib.sha256(content).hexdigest(), job.artifact_sha256
        ):
            raise BridgeError("delivery export changed after enqueue")
        return content

    def accept_receipt(
        self,
        *,
        capability_token: str,
        receipt: DeliveryReceipt,
    ) -> DeliveryReceipt:
        capability = self._capability(capability_token)
        job = self._job_for_capability(receipt.delivery_id, capability)
        if self._now() > job.expires_at:
            raise BridgeError("delivery job expired")
        expected = (
            receipt.project_id == job.project_id
            and secrets.compare_digest(receipt.figma_file_key, job.figma_file_key)
            and receipt.generation_area_node_id == job.generation_area_node_id
            and secrets.compare_digest(receipt.artifact_sha256, job.artifact_sha256)
            and receipt.artifact_byte_length == job.artifact_byte_length
            and bool(receipt.created_node_id)
            and receipt.width > 0
            and receipt.height > 0
        )
        if not expected:
            raise BridgeError("delivery receipt does not match the queued job")
        verified = replace(receipt, status="FIGMA_DELIVERED_VERIFIED")
        existing = self._receipts.get(job.delivery_id)
        if existing is not None:
            if existing == verified:
                return existing
            raise BridgeError("delivery receipt conflict")
        self._receipts[job.delivery_id] = verified
        return verified

    def revoke(self, *, capability_token: str) -> None:
        matched_key = next(
            (stored for stored in self._capabilities if secrets.compare_digest(stored, capability_token)),
            None,
        )
        if matched_key is not None:
            self._capabilities.pop(matched_key, None)

    def _capability(self, capability_token: str) -> PairingSession:
        matched_key = next(
            (stored for stored in self._capabilities if secrets.compare_digest(stored, capability_token)),
            None,
        )
        if matched_key is None:
            raise BridgeError("Figma Bridge capability is invalid or revoked")
        capability = self._capabilities[matched_key]
        if self._now() > capability.expires_at:
            self._capabilities.pop(matched_key, None)
            raise BridgeError("Figma Bridge capability expired")
        return capability

    def _job_for_capability(self, delivery_id: str, capability: PairingSession) -> DeliveryJob:
        job = self._jobs.get(delivery_id)
        if job is None:
            raise BridgeError("delivery job is unavailable")
        if job.project_id != capability.project_id or not secrets.compare_digest(
            job.figma_file_key, capability.figma_file_key
        ):
            raise BridgeError("delivery job belongs to a different project route")
        return job
