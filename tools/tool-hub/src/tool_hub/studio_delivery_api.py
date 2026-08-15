"""Private Studio-to-Hub delivery API for confirmed project-owned raster bytes."""

from __future__ import annotations

import re

from fastapi import FastAPI, Header, HTTPException, Request, Response

from .delivery_supervisor import ProcessSupervisor
from .figma_delivery import DeliveryError, FigmaDeliveryService
from .launcher import LaunchError


_RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")


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


def install_studio_delivery_api(
    app: FastAPI,
    launcher: ProcessSupervisor,
    figma_delivery: FigmaDeliveryService,
) -> None:
    """Install one credential-bound endpoint; browser sessions cannot select authority."""

    @app.post("/internal/studio-delivery/{run_id}")
    async def studio_delivery(
        run_id: str,
        request: Request,
        response: Response,
        authorization: str | None = Header(default=None),
    ) -> dict[str, object]:
        if _RUN_ID.fullmatch(run_id) is None:
            raise HTTPException(status_code=422, detail="DELIVERY_RUN_ID_INVALID")
        token = _bearer(authorization)
        try:
            tool_id, project_id = launcher.authorize_delivery_token(token)
        except LaunchError as error:
            raise HTTPException(status_code=401, detail="STUDIO_DELIVERY_AUTH_REQUIRED") from error
        if tool_id != "expression-studio":
            raise HTTPException(status_code=409, detail="DELIVERY_TOOL_ROUTE_UNAVAILABLE")
        image_bytes = await _bounded_png(request)
        try:
            job, created = figma_delivery.enqueue_idempotent(
                tool_id,
                project_id,
                run_id,
                image_bytes,
                "image/png",
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
        }
