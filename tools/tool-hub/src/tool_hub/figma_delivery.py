"""Project-scoped local queue for exact raster bytes destined for canonical Figma targets."""

from __future__ import annotations

import binascii
from dataclasses import dataclass, replace
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import struct
import tempfile
import threading
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
    width: int
    height: int
    figma_file_key: str
    figma_url: str
    delivery_page_node_id: str
    generation_area_node_id: str
    node_name: str
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
class BridgeReceipt:
    created_node_id: str
    created_node_name: str
    target_node_id: str
    content_sha256: str
    bridge_version: str
    image_hash: str


@dataclass(frozen=True)
class DeliveryReceipt:
    delivery_id: str
    tool_id: str
    project_id: str
    run_id: str
    content_sha256: str
    byte_length: int
    media_type: str
    figma_file_key: str
    target_node_id: str
    created_node_id: str
    created_node_name: str
    bridge_version: str
    image_hash: str
    verified_at: float
    state: str = "DELIVERED_VERIFIED"


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
    _JOB_STATES = frozenset({"QUEUED", "CLAIMED", "EXPIRED", "DELIVERED_VERIFIED"})

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
        self._state_lock = threading.RLock()
        self._pairings: dict[str, _PairingRecord] = {}
        self._sessions: dict[str, BridgeSession] = {}
        self._jobs: dict[str, DeliveryJob] = {}
        self._job_roots: dict[str, Path] = {}
        self._recover_jobs()

    def create_pairing(self, project_id: str) -> PairingView:
        try:
            self._locator.resolve(project_id)
            target = self._registry.resolve_ready_target(project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
        now = float(self._clock())
        with self._state_lock:
            self._prune_pairings(now)
            for digest, record in tuple(self._pairings.items()):
                if record.project_id == project_id:
                    self._pairings.pop(digest, None)
            code = ""
            digest = ""
            for _ in range(100):
                candidate = f"{secrets.randbelow(1_000_000):06d}"
                candidate_digest = hashlib.sha256(candidate.encode("ascii")).hexdigest()
                if candidate_digest not in self._pairings:
                    code, digest = candidate, candidate_digest
                    break
            if not code:
                raise DeliveryError("PAIRING_CODE_UNAVAILABLE")
            self._pairings[digest] = _PairingRecord(project_id, target.figma_file_key, digest, now + self.PAIRING_TTL_SECONDS)
        return PairingView(project_id, code, target.figma_url, now + self.PAIRING_TTL_SECONDS)

    def pair_by_code(self, pairing_code: str, bridge_version: str) -> BridgeSession:
        if not bridge_version:
            raise DeliveryError("BRIDGE_VERSION_REQUIRED")
        digest = hashlib.sha256(pairing_code.encode("utf-8")).hexdigest()
        now = float(self._clock())
        with self._state_lock:
            record = self._pairings.get(digest)
            if record is None:
                self._prune_pairings(now)
                raise DeliveryError("PAIRING_CODE_INVALID")
            if now > record.expires_at:
                self._pairings.pop(digest, None)
                raise DeliveryError("PAIRING_CODE_EXPIRED")
            try:
                self._locator.resolve(record.project_id)
                target = self._registry.resolve_ready_target(record.project_id)
                self._registry.assert_unchanged()
            except (ProjectBindingError, DeliveryBlockedError) as error:
                raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
            if target.figma_file_key != record.figma_file_key:
                raise DeliveryError("FIGMA_ROUTE_MISMATCH")
            self._pairings.pop(digest, None)
            token = secrets.token_urlsafe(32)
            session = BridgeSession(token, record.project_id, record.figma_file_key, bridge_version)
            self._sessions[token] = session
            return session

    def pair(self, project_id: str, figma_file_key: str, pairing_code: str, bridge_version: str) -> BridgeSession:
        try:
            self._locator.resolve(project_id)
            target = self._registry.resolve_ready_target(project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
        if figma_file_key != target.figma_file_key:
            raise DeliveryError("FIGMA_ROUTE_MISMATCH")
        digest = hashlib.sha256(pairing_code.encode("utf-8")).hexdigest()
        with self._state_lock:
            record = self._pairings.get(digest)
            if record is None or record.project_id != project_id:
                raise DeliveryError("PAIRING_CODE_INVALID")
        return self.pair_by_code(pairing_code, bridge_version)

    def enqueue(self, tool_id: str, project_id: str, run_id: str, image_bytes: bytes, media_type: str) -> DeliveryJob:
        if not tool_id or not project_id or not run_id:
            raise DeliveryError("DELIVERY_IDENTITY_REQUIRED")
        if not isinstance(image_bytes, bytes) or not image_bytes:
            raise DeliveryError("DELIVERY_CONTENT_REQUIRED")
        width, height = self._validate_raster(image_bytes, media_type)
        try:
            binding = self._locator.resolve(project_id)
            target = self._registry.resolve_ready_target(project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
        vault_root = self._validated_vault(binding.root)
        delivery_id = secrets.token_hex(16)
        delivery_root = vault_root / "tool-hub-delivery" / delivery_id
        try:
            delivery_root.mkdir(parents=True, exist_ok=False)
        except OSError as error:
            raise DeliveryError("DELIVERY_QUEUE_WRITE_FAILED") from error
        now = float(self._clock())
        job = DeliveryJob(
            delivery_id=delivery_id, tool_id=tool_id, project_id=project_id, run_id=run_id,
            content_sha256=hashlib.sha256(image_bytes).hexdigest(), byte_length=len(image_bytes), media_type=media_type,
            width=width, height=height, figma_file_key=target.figma_file_key, figma_url=target.figma_url,
            delivery_page_node_id=target.delivery_page_node_id, generation_area_node_id=target.generation_area_node_id,
            node_name=self._node_name(tool_id, run_id, delivery_id), state="QUEUED", created_at=now,
            expires_at=now + self.JOB_TTL_SECONDS,
        )
        try:
            self._atomic_write_bytes(delivery_root / "content.bin", image_bytes)
            self._write_job(delivery_root, job)
        except OSError as error:
            raise DeliveryError("DELIVERY_QUEUE_WRITE_FAILED") from error
        with self._state_lock:
            self._jobs[delivery_id] = job
            self._job_roots[delivery_id] = delivery_root
        return job

    def claim_next(self, token: str) -> DeliveryJob | None:
        session = self._require_session(token)
        self._assert_session_route(session)
        candidates = sorted(
            (job for job in self._jobs.values() if job.project_id == session.project_id and job.state == "QUEUED"),
            key=lambda item: (item.created_at, item.delivery_id),
        )
        for job in candidates:
            if float(self._clock()) > job.expires_at:
                self._set_state(job, "EXPIRED")
                continue
            self._verify_content(job)
            return self._set_state(job, "CLAIMED")
        return None

    def content(self, token: str, delivery_id: str) -> bytes:
        session = self._require_session(token)
        job = self._job_for_session(session, delivery_id)
        if job.state != "CLAIMED":
            raise DeliveryError("DELIVERY_NOT_CLAIMED")
        if float(self._clock()) > job.expires_at:
            self._set_state(job, "EXPIRED")
            raise DeliveryError("DELIVERY_EXPIRED")
        return self._verify_content(job)

    def release(self, token: str, delivery_id: str) -> DeliveryJob:
        session = self._require_session(token)
        job = self._job_for_session(session, delivery_id)
        if job.state != "CLAIMED":
            raise DeliveryError("DELIVERY_NOT_CLAIMED")
        if float(self._clock()) > job.expires_at:
            return self._set_state(job, "EXPIRED")
        self._verify_content(job)
        return self._set_state(job, "QUEUED")

    def job_view(self, project_id: str, delivery_id: str) -> DeliveryJob:
        job = self._jobs.get(delivery_id)
        if job is None:
            raise DeliveryError("DELIVERY_NOT_FOUND")
        if job.project_id != project_id:
            raise DeliveryError("DELIVERY_SCOPE_MISMATCH")
        if job.state in {"QUEUED", "CLAIMED"} and float(self._clock()) > job.expires_at:
            return self._set_state(job, "EXPIRED")
        return job

    def public_status(self, project_id: str) -> dict[str, object]:
        try:
            self._locator.resolve(project_id)
            self._registry.resolve_ready_target(project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
        pending = verified = expired = 0
        for job in tuple(self._jobs.values()):
            if job.project_id != project_id:
                continue
            current = job
            if current.state in {"QUEUED", "CLAIMED"} and float(self._clock()) > current.expires_at:
                current = self._set_state(current, "EXPIRED")
            if current.state in {"QUEUED", "CLAIMED"}:
                pending += 1
            elif current.state == "DELIVERED_VERIFIED":
                verified += 1
            elif current.state == "EXPIRED":
                expired += 1
        paired = any(session.project_id == project_id for session in self._sessions.values())
        return {
            "project_id": project_id,
            "bridge_state": "BRIDGE_PAIRED" if paired else "PAIRING_REQUIRED",
            "delivery_state": "DELIVERY_PENDING" if pending else ("FIGMA_DELIVERED_VERIFIED" if verified else "NO_PENDING_DELIVERY"),
            "pending_count": pending, "verified_count": verified, "expired_count": expired,
        }

    def finalize(self, token: str, delivery_id: str, receipt: BridgeReceipt) -> DeliveryReceipt:
        session = self._require_session(token)
        job = self._job_for_session(session, delivery_id)
        if job.state == "DELIVERED_VERIFIED":
            raise DeliveryError("DELIVERY_ALREADY_VERIFIED")
        if job.state != "CLAIMED":
            raise DeliveryError("DELIVERY_NOT_CLAIMED")
        if float(self._clock()) > job.expires_at:
            self._set_state(job, "EXPIRED")
            raise DeliveryError("DELIVERY_EXPIRED")
        self._verify_content(job)
        if receipt.target_node_id != job.generation_area_node_id:
            raise DeliveryError("FIGMA_TARGET_MISMATCH")
        if not hmac.compare_digest(receipt.content_sha256, job.content_sha256):
            raise DeliveryError("DELIVERY_HASH_MISMATCH")
        if receipt.created_node_name != job.node_name or not re.fullmatch(r"\d+[:-]\d+", receipt.created_node_id):
            raise DeliveryError("FIGMA_NODE_IDENTITY_MISMATCH")
        if not receipt.image_hash:
            raise DeliveryError("FIGMA_IMAGE_HASH_REQUIRED")
        if receipt.bridge_version != session.bridge_version:
            raise DeliveryError("BRIDGE_VERSION_MISMATCH")
        verified = DeliveryReceipt(
            delivery_id=job.delivery_id, tool_id=job.tool_id, project_id=job.project_id, run_id=job.run_id,
            content_sha256=job.content_sha256, byte_length=job.byte_length, media_type=job.media_type,
            figma_file_key=job.figma_file_key, target_node_id=job.generation_area_node_id,
            created_node_id=receipt.created_node_id, created_node_name=receipt.created_node_name,
            bridge_version=receipt.bridge_version, image_hash=receipt.image_hash, verified_at=float(self._clock()),
        )
        root = self._job_roots.get(job.delivery_id)
        if root is None:
            raise DeliveryError("DELIVERY_NOT_FOUND")
        evidence_path = root / "FIGMA_DELIVERY_RECEIPT.json"
        try:
            self._atomic_write_text(evidence_path, json.dumps(self._receipt_document(verified), ensure_ascii=False, indent=2, sort_keys=True) + "\n")
            self._set_state(job, "DELIVERED_VERIFIED")
        except OSError as error:
            try:
                evidence_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise DeliveryError("DELIVERY_RECEIPT_WRITE_FAILED") from error
        except DeliveryError:
            try:
                evidence_path.unlink(missing_ok=True)
            except OSError:
                pass
            raise
        return verified

    def _prune_pairings(self, now: float) -> None:
        for digest, record in tuple(self._pairings.items()):
            if now > record.expires_at:
                self._pairings.pop(digest, None)

    def _require_session(self, token: str) -> BridgeSession:
        session = self._sessions.get(token)
        if session is None:
            raise DeliveryError("BRIDGE_AUTH_REQUIRED")
        return session

    def _assert_session_route(self, session: BridgeSession) -> None:
        try:
            self._locator.resolve(session.project_id)
            target = self._registry.resolve_ready_target(session.project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
        if target.figma_file_key != session.figma_file_key:
            raise DeliveryError("FIGMA_ROUTE_MISMATCH")

    def _job_for_session(self, session: BridgeSession, delivery_id: str) -> DeliveryJob:
        self._assert_session_route(session)
        job = self._jobs.get(delivery_id)
        if job is None:
            raise DeliveryError("DELIVERY_NOT_FOUND")
        if job.project_id != session.project_id or job.figma_file_key != session.figma_file_key:
            raise DeliveryError("DELIVERY_SCOPE_MISMATCH")
        return job

    def _verify_content(self, job: DeliveryJob) -> bytes:
        root = self._job_roots.get(job.delivery_id)
        if root is None:
            raise DeliveryError("DELIVERY_NOT_FOUND")
        try:
            data = (root / "content.bin").read_bytes()
        except OSError as error:
            raise DeliveryError("DELIVERY_CONTENT_UNAVAILABLE") from error
        if len(data) != job.byte_length or not hmac.compare_digest(hashlib.sha256(data).hexdigest(), job.content_sha256):
            raise DeliveryError("DELIVERY_CONTENT_CHANGED")
        return data

    def _set_state(self, job: DeliveryJob, state: str) -> DeliveryJob:
        updated = replace(job, state=state)
        root = self._job_roots.get(job.delivery_id)
        if root is None:
            raise DeliveryError("DELIVERY_NOT_FOUND")
        try:
            self._write_job(root, updated)
        except OSError as error:
            raise DeliveryError("DELIVERY_QUEUE_WRITE_FAILED") from error
        self._jobs[job.delivery_id] = updated
        return updated

    def _recover_jobs(self) -> None:
        try:
            projects = self._registry.public_projects()
            self._registry.assert_unchanged()
        except (ValueError, DeliveryBlockedError):
            return
        for public in projects:
            project_id = str(public.get("project_id", ""))
            if not project_id:
                continue
            try:
                binding = self._locator.resolve(project_id)
                target = self._registry.resolve_ready_target(project_id)
                vault = self._validated_vault(binding.root)
            except (ProjectBindingError, DeliveryBlockedError, DeliveryError):
                continue
            queue_root = vault / "tool-hub-delivery"
            if not queue_root.is_dir() or queue_root.is_symlink():
                continue
            try:
                children = tuple(queue_root.iterdir())
            except OSError:
                continue
            for child in children:
                self._recover_one(project_id, target, queue_root, child)

    def _recover_one(self, project_id: str, target: object, queue_root: Path, child: Path) -> None:
        if child.is_symlink() or not child.is_dir() or not re.fullmatch(r"[0-9a-f]{32}", child.name):
            return
        try:
            resolved = child.resolve(strict=True)
            if resolved.parent != queue_root.resolve(strict=True):
                return
            raw = (resolved / "JOB.json").read_bytes()
            if len(raw) > 64 * 1024:
                return
            doc = json.loads(raw.decode("utf-8"))
            if not isinstance(doc, dict) or doc.get("schema_version") != 1:
                return
            required = {
                "delivery_id", "tool_id", "project_id", "run_id", "content_sha256", "byte_length", "media_type",
                "width", "height", "figma_file_key", "delivery_page_node_id", "generation_area_node_id", "node_name",
                "state", "created_at", "expires_at"
            }
            if not required.issubset(doc):
                return
            if doc["delivery_id"] != child.name or doc["project_id"] != project_id or doc["state"] not in self._JOB_STATES:
                return
            if doc["figma_file_key"] != target.figma_file_key or doc["delivery_page_node_id"] != target.delivery_page_node_id or doc["generation_area_node_id"] != target.generation_area_node_id:
                return
            content_path = resolved / "content.bin"
            if content_path.is_symlink():
                return
            data = content_path.read_bytes()
            width, height = self._validate_raster(data, str(doc["media_type"]))
            if int(doc["byte_length"]) != len(data) or str(doc["content_sha256"]) != hashlib.sha256(data).hexdigest():
                return
            if int(doc["width"]) != width or int(doc["height"]) != height:
                return
            expected_name = self._node_name(str(doc["tool_id"]), str(doc["run_id"]), child.name)
            if doc["node_name"] != expected_name:
                return
            job = DeliveryJob(
                delivery_id=child.name, tool_id=str(doc["tool_id"]), project_id=project_id, run_id=str(doc["run_id"]),
                content_sha256=str(doc["content_sha256"]), byte_length=len(data), media_type=str(doc["media_type"]),
                width=width, height=height, figma_file_key=target.figma_file_key, figma_url=target.figma_url,
                delivery_page_node_id=target.delivery_page_node_id, generation_area_node_id=target.generation_area_node_id,
                node_name=expected_name, state=str(doc["state"]), created_at=float(doc["created_at"]), expires_at=float(doc["expires_at"]),
            )
            if job.state == "DELIVERED_VERIFIED" and not self._valid_recovered_receipt(resolved, job):
                return
            self._jobs[job.delivery_id] = job
            self._job_roots[job.delivery_id] = resolved
            now = float(self._clock())
            if job.state in {"QUEUED", "CLAIMED"} and now > job.expires_at:
                self._set_state(job, "EXPIRED")
            elif job.state == "CLAIMED":
                self._set_state(job, "QUEUED")
        except (OSError, ValueError, TypeError, json.JSONDecodeError, DeliveryError):
            self._jobs.pop(child.name, None)
            self._job_roots.pop(child.name, None)

    def _valid_recovered_receipt(self, root: Path, job: DeliveryJob) -> bool:
        path = root / "FIGMA_DELIVERY_RECEIPT.json"
        if path.is_symlink() or not path.is_file():
            return False
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return False
        return bool(
            isinstance(doc, dict) and doc.get("state") == "DELIVERED_VERIFIED"
            and doc.get("delivery_id") == job.delivery_id and doc.get("project_id") == job.project_id
            and doc.get("content_sha256") == job.content_sha256 and doc.get("figma_file_key") == job.figma_file_key
            and doc.get("target_node_id") == job.generation_area_node_id and doc.get("created_node_name") == job.node_name
        )

    @staticmethod
    def _validated_vault(project_root: Path) -> Path:
        vault = project_root / ".asset-vault"
        try:
            vault_root = vault.resolve(strict=True)
        except OSError as error:
            raise DeliveryError("PROJECT_DELIVERY_AREA_UNAVAILABLE") from error
        if vault_root != project_root.resolve() / ".asset-vault" or not vault_root.is_dir() or vault.is_symlink():
            raise DeliveryError("PROJECT_DELIVERY_AREA_UNAVAILABLE")
        return vault_root

    @classmethod
    def _validate_raster(cls, image_bytes: bytes, media_type: str) -> tuple[int, int]:
        if len(image_bytes) > cls.MAX_IMAGE_BYTES:
            raise DeliveryError("DELIVERY_IMAGE_TOO_LARGE")
        if media_type != "image/png":
            raise DeliveryError("DELIVERY_MEDIA_TYPE_UNSUPPORTED")
        if len(image_bytes) < 33 or image_bytes[:8] != b"\x89PNG\r\n\x1a\n":
            raise DeliveryError("DELIVERY_IMAGE_INVALID")
        offset = 8
        width = height = 0
        saw_idat = saw_iend = False
        first = True
        while offset < len(image_bytes):
            if offset + 12 > len(image_bytes):
                raise DeliveryError("DELIVERY_IMAGE_INVALID")
            length = struct.unpack(">I", image_bytes[offset:offset + 4])[0]
            kind = image_bytes[offset + 4:offset + 8]
            end = offset + 12 + length
            if end > len(image_bytes):
                raise DeliveryError("DELIVERY_IMAGE_INVALID")
            payload = image_bytes[offset + 8:offset + 8 + length]
            expected_crc = struct.unpack(">I", image_bytes[offset + 8 + length:end])[0]
            if expected_crc != (binascii.crc32(kind + payload) & 0xFFFFFFFF):
                raise DeliveryError("DELIVERY_IMAGE_INVALID")
            if first:
                if kind != b"IHDR" or length != 13:
                    raise DeliveryError("DELIVERY_IMAGE_INVALID")
                width, height = struct.unpack(">II", payload[:8])
                first = False
            elif kind == b"IHDR":
                raise DeliveryError("DELIVERY_IMAGE_INVALID")
            if kind == b"IDAT":
                saw_idat = True
            if kind == b"IEND":
                if length != 0 or end != len(image_bytes):
                    raise DeliveryError("DELIVERY_IMAGE_INVALID")
                saw_iend = True
                offset = end
                break
            offset = end
        if not width or not height or not saw_idat or not saw_iend or offset != len(image_bytes):
            raise DeliveryError("DELIVERY_IMAGE_INVALID")
        if width > cls.MAX_IMAGE_DIMENSION or height > cls.MAX_IMAGE_DIMENSION:
            raise DeliveryError("DELIVERY_IMAGE_DIMENSIONS_EXCEEDED")
        return width, height

    @staticmethod
    def _node_name(tool_id: str, run_id: str, delivery_id: str) -> str:
        safe_tool = re.sub(r"[^A-Za-z0-9_-]+", "-", tool_id).strip("-")[:32] or "tool"
        safe_run = re.sub(r"[^A-Za-z0-9_-]+", "-", run_id).strip("-")[:48] or "run"
        return f"BaseToolHub__{safe_tool}__{safe_run}__{delivery_id[:12]}"

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

    @classmethod
    def _write_job(cls, root: Path, job: DeliveryJob) -> None:
        cls._atomic_write_text(root / "JOB.json", json.dumps(cls._job_document(job), ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    @staticmethod
    def _job_document(job: DeliveryJob) -> dict[str, object]:
        return {
            "schema_version": 1, "delivery_id": job.delivery_id, "tool_id": job.tool_id, "project_id": job.project_id,
            "run_id": job.run_id, "content_sha256": job.content_sha256, "byte_length": job.byte_length,
            "media_type": job.media_type, "width": job.width, "height": job.height, "figma_file_key": job.figma_file_key,
            "delivery_page_node_id": job.delivery_page_node_id, "generation_area_node_id": job.generation_area_node_id,
            "node_name": job.node_name, "state": job.state, "created_at": job.created_at, "expires_at": job.expires_at,
        }

    @staticmethod
    def _receipt_document(receipt: DeliveryReceipt) -> dict[str, object]:
        return {
            "schema_version": 1, "delivery_id": receipt.delivery_id, "tool_id": receipt.tool_id,
            "project_id": receipt.project_id, "run_id": receipt.run_id, "content_sha256": receipt.content_sha256,
            "byte_length": receipt.byte_length, "media_type": receipt.media_type, "figma_file_key": receipt.figma_file_key,
            "target_node_id": receipt.target_node_id, "created_node_id": receipt.created_node_id,
            "created_node_name": receipt.created_node_name, "bridge_version": receipt.bridge_version,
            "image_hash": receipt.image_hash, "verified_at": receipt.verified_at, "state": receipt.state,
        }
