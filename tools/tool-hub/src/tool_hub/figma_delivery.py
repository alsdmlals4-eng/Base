"""Exact tool-route enforcement layered over the hardened project-scoped Figma queue."""

from __future__ import annotations

from dataclasses import dataclass, replace
import hmac
import json
from pathlib import Path
import re
import time
from typing import Callable

from base_tool_contracts import (
    DeliveryBlockedError,
    ProjectFigmaRegistry,
    ProjectFigmaToolRoute,
    ProjectFigmaToolRouteRegistry,
)

from . import _figma_delivery_base as _base
from .projects import ProjectLocator


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
    "expression-studio": "character_expression_runs",
}


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

    def _resolve_tool_route(self, tool_id: str, project_id: str) -> ProjectFigmaToolRoute:
        route_id = _TOOL_ROUTE_IDS.get(tool_id)
        if route_id is None:
            raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE")
        try:
            self._registry.assert_unchanged()
            self._tool_routes.assert_unchanged()
            return self._tool_routes.resolve_ready_route(project_id, route_id, self._registry)
        except DeliveryBlockedError as error:
            raise DeliveryError("DELIVERY_TOOL_ROUTE_UNAVAILABLE") from error

    def _assert_current_job_route(self, job: _base.DeliveryJob) -> ProjectFigmaToolRoute:
        route = self._resolve_tool_route(job.tool_id, job.project_id)
        if not isinstance(job, DeliveryJob):
            raise DeliveryError("FIGMA_TOOL_ROUTE_IDENTITY_MISMATCH")
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

    def _verify_content(self, job: _base.DeliveryJob) -> None:
        self._assert_current_job_route(job)
        super()._verify_content(job)

    def enqueue(
        self,
        tool_id: str,
        project_id: str,
        run_id: str,
        image_bytes: bytes,
        media_type: str,
    ) -> DeliveryJob:
        route = self._resolve_tool_route(tool_id, project_id)
        base_job = super().enqueue(tool_id, project_id, run_id, image_bytes, media_type)
        if base_job.generation_area_node_id != route.parent_node_id:
            raise DeliveryError("FIGMA_TOOL_ROUTE_PARENT_MISMATCH")
        job = DeliveryJob(
            **base_job.__dict__,
            tool_route_id=route.tool_route_id,
            route_parent_node_id=route.parent_node_id,
            target_node_id=route.destination_node_id,
            target_node_name=route.destination_name,
            project_marker_node_id=route.project_marker_node_id,
            project_marker_name=route.project_marker_name,
        )
        root = self._job_roots.get(job.delivery_id)
        if root is None:
            raise DeliveryError("DELIVERY_NOT_FOUND")
        try:
            self._write_job(root, job)
        except OSError as error:
            self._jobs.pop(job.delivery_id, None)
            self._job_roots.pop(job.delivery_id, None)
            raise DeliveryError("DELIVERY_QUEUE_WRITE_FAILED") from error
        with self._state_lock:
            self._jobs[job.delivery_id] = job
        return job

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

    def _valid_recovered_receipt(self, root: Path, job: _base.DeliveryJob) -> bool:
        try:
            route = self._resolve_tool_route(job.tool_id, job.project_id)
        except DeliveryError:
            return False
        path = root / "FIGMA_DELIVERY_RECEIPT.json"
        if path.is_symlink() or not path.is_file():
            return False
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError):
            return False
        return bool(
            isinstance(doc, dict)
            and doc.get("state") == "DELIVERED_VERIFIED"
            and doc.get("delivery_id") == job.delivery_id
            and doc.get("project_id") == job.project_id
            and doc.get("content_sha256") == job.content_sha256
            and doc.get("figma_file_key") == job.figma_file_key
            and doc.get("target_node_id") == route.destination_node_id
            and doc.get("tool_route_id") == route.tool_route_id
            and doc.get("created_node_name") == job.node_name
        )

    def _recover_one(self, project_id: str, target: object, queue_root: Path, child: Path) -> None:
        super()._recover_one(project_id, target, queue_root, child)
        base_job = self._jobs.get(child.name)
        if base_job is None:
            return
        try:
            route = self._resolve_tool_route(base_job.tool_id, base_job.project_id)
            raw = (child / "JOB.json").read_text(encoding="utf-8")
            doc = json.loads(raw)
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
