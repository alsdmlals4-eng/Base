"""Private Studio-to-Hub delivery API for confirmed project-owned raster bytes."""

from __future__ import annotations

import re
import threading
import time

from fastapi import FastAPI, Header, HTTPException, Request, Response

from .delivery_supervisor import ProcessSupervisor
from .figma_delivery import DeliveryError, FigmaDeliveryService, PairingView
from .launcher import LaunchError


_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
_ALLOWED_ROUTES = {
    "expression-studio": frozenset({"character_expression_runs"}),
    "sprite-animation-studio": frozenset({"sprite_action_runs", "effect_runs"}),
}


def _bearer(authorization: str | None) -> str:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="STUDIO_DELIVERY_AUTH_REQUIRED")
    token = authorization[len("Bearer "):].strip()
    if len(token) < 32:
        raise HTTPException(status_code=401, detail="STUDIO_DELIVERY_AUTH_REQUIRED")
    return token


async def _bounded_png(request: Request) -> bytes:
    media_type = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()
    if media_type != "image/png":
        raise HTTPException(status_code=415, detail="DELIVERY_MEDIA_TYPE_UNSUPPORTED")
    data = bytearray()
    async for chunk in request.stream():
        data.extend(chunk)
        if len(data) > FigmaDeliveryService.MAX_IMAGE_BYTES:
            raise HTTPException(status_code=413, detail="DELIVERY_IMAGE_TOO_LARGE")
    if not data:
        raise HTTPException(status_code=422, detail="DELIVERY_CONTENT_REQUIRED")
    return bytes(data)


def _requested_route(tool_id: str, requested: str | None) -> str:
    allowed = _ALLOWED_ROUTES.get(tool_id)
    if allowed is None:
        raise HTTPException(status_code=409, detail="DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    if tool_id == "expression-studio" and requested is None:
        return "character_expression_runs"
    if requested is None or requested not in allowed:
        raise HTTPException(status_code=409, detail="DELIVERY_TOOL_ROUTE_UNAVAILABLE")
    return requested


def install_studio_delivery_api(
    app: FastAPI,
    launcher: ProcessSupervisor,
    figma_delivery: FigmaDeliveryService,
) -> None:
    """Install credential-bound delivery/status endpoints with canonical Figma pairing hints."""
    pending_pairings: dict[str, PairingView] = {}
    pairing_lock = threading.RLock()

    def authorize(authorization: str | None) -> tuple[str, str]:
        token = _bearer(authorization)
        try:
            return launcher.authorize_delivery_token(token)
        except LaunchError as error:
            raise HTTPException(status_code=401, detail="STUDIO_DELIVERY_AUTH_REQUIRED") from error

    def bridge_fields(project_id: str, figma_url: str) -> dict[str, object]:
        try:
            public = figma_delivery.public_status(project_id)
        except DeliveryError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        fields: dict[str, object] = {
            "bridge_state": public["bridge_state"],
            "delivery_state": public["delivery_state"],
            "figma_url": figma_url,
        }
        with pairing_lock:
            if public["bridge_state"] == "BRIDGE_PAIRED":
                pending_pairings.pop(project_id, None)
                return fields
            pairing = pending_pairings.get(project_id)
            if pairing is None or pairing.expires_at <= time.time():
                try:
                    pairing = figma_delivery.create_pairing(project_id)
                except DeliveryError as error:
                    raise HTTPException(status_code=409, detail=str(error)) from error
                pending_pairings[project_id] = pairing
            fields.update(
                {
                    "pairing_code": pairing.pairing_code,
                    "pairing_expires_at": pairing.expires_at,
                }
            )
        return fields

    @app.post("/internal/studio-delivery/{run_id}")
    async def studio_delivery(
        run_id: str,
        request: Request,
        response: Response,
        authorization: str | None = Header(default=None),
        x_base_tool_route: str | None = Header(default=None, alias="X-Base-Tool-Route"),
    ) -> dict[str, object]:
        if _RUN_ID.fullmatch(run_id) is None:
            raise HTTPException(status_code=422, detail="DELIVERY_RUN_ID_INVALID")
        tool_id, project_id = authorize(authorization)
        route_id = _requested_route(tool_id, x_base_tool_route)
        image_bytes = await _bounded_png(request)
        try:
            job, created = figma_delivery.enqueue_idempotent(
                tool_id,
                project_id,
                run_id,
                image_bytes,
                "image/png",
                tool_route_id=route_id,
            )
        except DeliveryError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        response.status_code = 201 if created else 200
        return {
            "status": job.state,
            "delivery_id": job.delivery_id,
            "tool_id": job.tool_id,
            "project_id": job.project_id,
            "run_id": job.run_id,
            "content_sha256": job.content_sha256,
            "tool_route_id": job.tool_route_id,
            "target_node_id": job.target_node_id,
            "target_node_name": job.target_node_name,
            **bridge_fields(project_id, job.figma_url),
        }

    @app.get("/internal/studio-delivery/{delivery_id}/status")
    def studio_delivery_status(
        delivery_id: str,
        authorization: str | None = Header(default=None),
    ) -> dict[str, object]:
        tool_id, project_id = authorize(authorization)
        if tool_id not in _ALLOWED_ROUTES:
            raise HTTPException(status_code=409, detail="DELIVERY_TOOL_ROUTE_UNAVAILABLE")
        try:
            job = figma_delivery.job_view(project_id, delivery_id)
        except DeliveryError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        if job.tool_id != tool_id:
            raise HTTPException(status_code=409, detail="DELIVERY_SCOPE_MISMATCH")
        return {
            "status": job.state,
            "delivery_id": job.delivery_id,
            "tool_id": job.tool_id,
            "project_id": job.project_id,
            "run_id": job.run_id,
            "content_sha256": job.content_sha256,
            "tool_route_id": job.tool_route_id,
            "target_node_id": job.target_node_id,
            "target_node_name": job.target_node_name,
            **bridge_fields(project_id, job.figma_url),
        }
