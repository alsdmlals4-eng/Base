"""Exact tool-route enforcement layered over the hardened project-scoped Figma queue."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
import re
import secrets
import time
from typing import Callable

from base_tool_contracts import (
    DeliveryBlockedError,
    ProjectFigmaRegistry,
    ProjectFigmaToolRoute,
    ProjectFigmaToolRouteRegistry,
)

from . import _figma_delivery_base as _base
from .projects import ProjectBindingError, ProjectLocator


DeliveryError = _base.DeliveryError
PairingView = _base.PairingView
BridgeSession = _base.BridgeSession
BridgeReceipt = _base.BridgeReceipt


@dataclass(frozen=True)
class DeliveryJob(_base.DeliveryJob):
    tool_route_id: str = ""
    route_parent_node_id: str = ""
    target_node_id: str = ""
    target_node_name: str = ""
    project_marker_node_id: str = ""
    project_marker_name: str = ""


@dataclass(frozen=True)
class DeliveryReceipt(_base.DeliveryReceipt):
    tool_route_id: str = ""
    target_node_name: str = ""


_TOOL_ROUTE_IDS = {
    "expression-studio": frozenset({"character_expression_runs"}),
    "sprite-animation-studio": frozenset({"sprite_action_runs", "effect_runs"}),
}


def _requested_route_id(tool_id: str, requested: str | None) -> str:
    allowed = _TOOL_ROUTE_IDS.get(tool_id)
    if allowed is None:
        raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    if requested is None:
        if tool_id == "expression-studio":
            return "character_expression_runs"
        raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    if requested not in allowed:
        raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    return requested


class FigmaDeliveryService(_base.FigmaDeliveryService):
    """Fail closed unless a tool output resolves to an exact reviewed descendant node."""

    def __init__(
        self,
        runtime_root: Path,
        locator: ProjectLocator,
        registry: ProjectFigmaRegistry,
        *,
        tool_routes: ProjectFigmaToolRouteRegistry | None = None,
        base_root: Path | None = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        root = Path(base_root) if base_root is not None else Path(__file__).resolve().parents[4]
        root = root.resolve()
        routes = tool_routes or ProjectFigmaToolRouteRegistry.load(
            root / "docs" / "operations" / "PROJECT_FIGMA_TOOL_ROUTE_REGISTRY.json"
        )
        try:
            routes.assert_canonical(root)
        except DeliveryBlockedError as error:
            raise DeliveryError("DELIVERY_TOOL_ROUTE_REGISTRY_UNAVAILABLE") from error
        self._tool_routes = routes
        self._base_root = root
        super().__init__(runtime_root, locator, registry, clock=clock)

    def _resolve_tool_route(
        self,
        tool_id: str,
        project_id: str,
        tool_route_id: str | None = None,
    ) -> ProjectFigmaToolRoute:
        route_id = _requested_route_id(tool_id, tool_route_id)
        try:
            self._registry.assert_unchanged()
            self._tool_routes.assert_unchanged()
            return self._tool_routes.resolve_ready_route(project_id, route_id, self._registry)
        except DeliveryBlockedError as error:
            raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE") from error

    def _assert_current_job_route(self, job: _base.DeliveryJob) -> ProjectFigmaToolRoute:
        if not isinstance(job, DeliveryJob) or not job.tool_route_id:
            raise DeliveryError("FIGMA_TOOL_ROUTE_IDENTITY_MISMATCH")
        route = self._resolve_tool_route(job.tool_id, job.project_id, job.tool_route_id)
        expected = (
            route.tool_route_id,
            route.parent_node_id,
            route.destination_node_id,
            route.destination_name,
            route.project_marker_node_id,
            route.project_marker_name,
        )
        actual = (
            job.tool_route_id,
            job.route_parent_node_id,
            job.target_node_id,
            job.target_node_name,
            job.project_marker_node_id,
            job.project_marker_name,
        )
        if actual != expected or job.generation_area_node_id != route.parent_node_id:
            raise DeliveryError("FIGMA_TOOL_ROUTE_IDENTITY_MISMATCH")
        return route

    def _verify_content(self, job: _base.DeliveryJob) -> bytes:
        self._assert_current_job_route(job)
        return super()._verify_content(job)

    def enqueue(
        self,
        tool_id: str,
        project_id: str,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
        *,
        tool_route_id: str | None = None,
    ) -> DeliveryJob:
        """Persist the exact route identity in the first authoritative JOB write."""
        if not tool_id or not project_id or not run_id:
            raise DeliveryError("DELIVERY_IDENTITY_REQUIRED")
        if not isinstance(image_bytes, bytes) or not image_bytes:
            raise DeliveryError("DELIVERY_CONTENT_REQUIRED")
        route = self._resolve_tool_route(tool_id, project_id, tool_route_id)
        width, height = self._validate_raster(image_bytes, media_type)
        try:
            binding = self._locator.resolve(project_id)
            target = self._registry.resolve_ready_target(project_id)
            self._registry.assert_unchanged()
        except (ProjectBindingError, DeliveryBlockedError) as error:
            raise DeliveryError("DELIVERY_PROJECT_ROUTE_UNAVAILABLE") from error
        if (
            target.figma_file_key != route.figma_file_key
            or target.generation_area_node_id != route.parent_node_id
        ):
            raise DeliveryError("FIGMA_TOOL_ROUTE_PARENT_MISMATCH")
        vault_root = self._validated_vault(binding.root)
        delivery_id = secrets.token_hex(16)
        delivery_root = vault_root / "tool-hub-delivery" / delivery_id
        try:
            delivery_root.mkdir(parents=True, exist_ok=False)
        except OSError as error:
            raise DeliveryError("DELIVERY_QUEUE_WRITE_FAILED") from error
        now = float(self._clock())
        job = DeliveryJob(
            delivery_id=delivery_id,
            tool_id=tool_id,
            project_id=project_id,
            run_id=run_id,
            content_sha256=hashlib.sha256(image_bytes).hexdigest(),
            byte_length=len(image_bytes),
            media_type=media_type,
            width=width,
            height=height,
            figma_file_key=target.figma_file_key,
            figma_url=target.figma_url,
            delivery_page_node_id=target.delivery_page_node_id,
            generation_area_node_id=target.generation_area_node_id,
            node_name=self._node_name(tool_id, run_id, delivery_id),
            state="QUEUED",
            created_at=now,
            expires_at=now + self.JOB_TTL_SECONDS,
            tool_route_id=route.tool_route_id,
            route_parent_node_id=route.parent_node_id,
            target_node_id=route.destination_node_id,
            target_node_name=route.destination_name,
            project_marker_node_id=route.project_marker_node_id,
            project_marker_name=route.project_marker_name,
        )
        try:
            self._atomic_write_bytes(delivery_root / "content.bin", image_bytes)
            self._write_job(delivery_root, job)
        except OSError as error:
            try:
                (delivery_root / "JOB.json").unlink(missing_ok=True)
            except OSError:
                pass
            raise DeliveryError("DELIVERY_QUEUE_WRITE_FAILED") from error
        with self._state_lock:
            self._jobs[delivery_id] = job
            self._job_roots[delivery_id] = delivery_root
        return job

    @staticmethod
    def _stored_route_id(job: _base.DeliveryJob) -> str:
        if isinstance(job, DeliveryJob) and job.tool_route_id:
            return job.tool_route_id
        if job.tool_id == "expression-studio":
            return "character_expression_runs"
        raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")

    def enqueue_idempotent(
        self,
        tool_id: str,
        project_id: str,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
        *,
        tool_route_id: str | None = None,
    ) -> tuple[DeliveryJob, bool]:
        """Queue one immutable run/route payload, reusing only an exact live or verified retry."""
        requested_route = _requested_route_id(tool_id, tool_route_id)
        digest = hashlib.sha256(image_bytes).hexdigest()
        with self._state_lock:
            matching = [
                job
                for job in self._jobs.values()
                if job.tool_id == tool_id
                and job.project_id == project_id
                and job.run_id == run_id
            ]
            for job in matching:
                if self._stored_route_id(job) != requested_route:
                    raise DeliveryError("DELIVERY_RUN_ROUTE_MISMATCH")
            if any(not hmac.compare_digest(job.content_sha256, digest) for job in matching):
                raise DeliveryError("DELIVERY_RUN_CONTENT_MISMATCH")
            reusable = sorted(
                (job for job in matching if job.state != "EXPIRED"),
                key=lambda item: (item.created_at, item.delivery_id),
            )
            if reusable:
                job = reusable[0]
                self._verify_content(job)
                if not isinstance(job, DeliveryJob):
                    raise DeliveryError("FIGMA_TOOL_ROUTE_IDENTITY_MISMATCH")
                return job, False
            return self.enqueue(
                tool_id,
                project_id,
                run_id,
                image_bytes,
                media_type,
                tool_route_id=requested_route,
            ), True

    def finalize(
        self,
        token: str,
        delivery_id: str,
        receipt: BridgeReceipt,
    ) -> DeliveryReceipt:
        session = self._require_session(token)
        with self._state_lock:
            job = self._job_for_session(session, delivery_id)
            if job.state == "DELIVERED_VERIFIED":
                raise DeliveryError("DELIVERY_ALREADY_VERIFIED")
            if job.state != "CLAIMED":
                raise DeliveryError("DELIVERY_NOT_CLAIMED")
            if float(self._clock()) > job.expires_at:
                self._set_state(job, "EXPIRED")
                raise DeliveryError("DELIVERY_EXPIRED")
            self._verify_content(job)
            if not isinstance(job, DeliveryJob) or receipt.target_node_id != job.target_node_id:
                raise DeliveryError("FIGMA_TARGET_MISMATCH")
            if not hmac.compare_digest(receipt.content_sha256, job.content_sha256):
                raise DeliveryError("DELIVERY_HASH_MISMATCH")
            if (
                receipt.created_node_name != job.node_name
                or not re.fullmatch(r"\d+[:-]\d+", receipt.created_node_id)
            ):
                raise DeliveryError("FIGMA_NODE_IDENTITY_MISMATCH")
            if not receipt.image_hash:
                raise DeliveryError("FIGMA_IMAGE_HASH_REQUIRED")
            if receipt.bridge_version != session.bridge_version:
                raise DeliveryError("BRIDGE_VERSION_MISMATCH")
            verified = DeliveryReceipt(
                delivery_id=job.delivery_id,
                tool_id=job.tool_id,
                project_id=job.project_id,
                run_id=job.run_id,
                content_sha256=job.content_sha256,
                byte_length=job.byte_length,
                media_type=job.media_type,
                figma_file_key=job.figma_file_key,
                target_node_id=job.target_node_id,
                created_node_id=receipt.created_node_id,
                created_node_name=receipt.created_node_name,
                bridge_version=receipt.bridge_version,
                image_hash=receipt.image_hash,
                verified_at=float(self._clock()),
                tool_route_id=job.tool_route_id,
                target_node_name=job.target_node_name,
            )
            root = self._job_roots.get(job.delivery_id)
            if root is None:
                raise DeliveryError("DELIVERY_NOT_FOUND")
            evidence_path = root / "FIGMA_DELIVERY_RECEIPT.json"
            try:
                self._atomic_write_text(
                    evidence_path,
                    json.dumps(
                        self._receipt_document(verified),
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n",
                )
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

    @staticmethod
    def _job_document(job: _base.DeliveryJob) -> dict[str, object]:
        document = _base.FigmaDeliveryService._job_document(job)
        if isinstance(job, DeliveryJob):
            document.update(
                {
                    "tool_route_id": job.tool_route_id,
                    "route_parent_node_id": job.route_parent_node_id,
                    "target_node_id": job.target_node_id,
                    "target_node_name": job.target_node_name,
                    "project_marker_node_id": job.project_marker_node_id,
                    "project_marker_name": job.project_marker_name,
                }
            )
        return document

    @staticmethod
    def _receipt_document(receipt: _base.DeliveryReceipt) -> dict[str, object]:
        document = _base.FigmaDeliveryService._receipt_document(receipt)
        if isinstance(receipt, DeliveryReceipt):
            document.update(
                {
                    "tool_route_id": receipt.tool_route_id,
                    "target_node_name": receipt.target_node_name,
                }
            )
        return document

    def _route_from_job_document(
        self,
        job: _base.DeliveryJob,
        document: dict[str, object],
    ) -> ProjectFigmaToolRoute:
        raw_route = document.get("tool_route_id")
        if raw_route is None:
            if job.tool_id != "expression-studio":
                raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
            route_id = "character_expression_runs"
        elif not isinstance(raw_route, str):
            raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
        else:
            route_id = raw_route
        return self._resolve_tool_route(job.tool_id, job.project_id, route_id)

    def _valid_recovered_receipt(self, root: Path, job: _base.DeliveryJob) -> bool:
        try:
            job_doc = json.loads((root / "JOB.json").read_text(encoding="utf-8"))
            if not isinstance(job_doc, dict):
                return False
            route = self._route_from_job_document(job, job_doc)
        except (OSError, UnicodeError, json.JSONDecodeError, DeliveryError):
            return False
        path = root / "FIGMA_DELIVERY_RECEIPT.json"
        if path.is_symlink() or not path.is_file():
            return False
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return False
        if not isinstance(doc, dict):
            return False
        receipt_route = doc.get("tool_route_id")
        if receipt_route is None and job.tool_id == "expression-studio":
            receipt_route = "character_expression_runs"
        return bool(
            doc.get("state") == "DELIVERED_VERIFIED"
            and doc.get("delivery_id") == job.delivery_id
            and doc.get("project_id") == job.project_id
            and doc.get("content_sha256") == job.content_sha256
            and doc.get("figma_file_key") == job.figma_file_key
            and doc.get("target_node_id") == route.destination_node_id
            and receipt_route == route.tool_route_id
            and doc.get("created_node_name") == job.node_name
        )

    def _recover_one(self, project_id: str, target: object, queue_root: Path, child: Path) -> None:
        super()._recover_one(project_id, target, queue_root, child)
        base_job = self._jobs.get(child.name)
        if base_job is None:
            return
        try:
            raw = (child / "JOB.json").read_text(encoding="utf-8")
            doc = json.loads(raw)
            if not isinstance(doc, dict):
                raise DeliveryError("FIGMA_TOOL_ROUTE_RECOVERY_MISMATCH")
            route = self._route_from_job_document(base_job, doc)
            expected = {
                "tool_route_id": route.tool_route_id,
                "route_parent_node_id": route.parent_node_id,
                "target_node_id": route.destination_node_id,
                "target_node_name": route.destination_name,
                "project_marker_node_id": route.project_marker_node_id,
                "project_marker_name": route.project_marker_name,
            }
            present = {key: doc.get(key) for key in expected}
            if any(value is not None and value != expected[key] for key, value in present.items()):
                raise DeliveryError("FIGMA_TOOL_ROUTE_RECOVERY_MISMATCH")
            job = DeliveryJob(**base_job.__dict__, **expected)
            self._jobs[job.delivery_id] = job
            if present != expected:
                self._write_job(child, job)
        except (OSError, UnicodeError, json.JSONDecodeError, DeliveryError, TypeError):
            self._jobs.pop(child.name, None)
            self._job_roots.pop(child.name, None)
