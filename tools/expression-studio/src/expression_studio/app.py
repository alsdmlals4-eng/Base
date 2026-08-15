"""Localhost-only FastAPI entrypoint for Expression Studio."""

import argparse
import hashlib
import os
from pathlib import Path
from typing import Sequence

from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from base_tool_contracts import (
    ApprovedAnchorRegistry,
    BoundedRequestBodyMiddleware,
    HubStartupError,
    hub_identity_from_environment,
    open_loopback_listener,
    write_startup_report,
)
from pydantic import BaseModel, ConfigDict, Field

from .delivery import DeliveryBlockedError, ProjectFigmaRegistry
from .engine import EngineContractError, FakeExpressionEngine, OpenAIExpressionEngine, ExpressionEngine
from .hub_delivery import HubDeliveryError, HubDeliverySender, sender_from_environment
from .imports import DECLARED_SOURCES, DeclaredSource, read_upload_limited, validate_imported_image
from .models import ExpressionRequest
from .service import ExpressionStudioService, RunBlockedError, RunNotFoundError, _read_staged_file
from .security import StudioSecurity, install_security


_MAX_REQUEST_BODY_BYTES = 202 * 1024 * 1024


class SelectionPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selected_candidate: int = Field(ge=0)


def create_app(
    project_root: Path,
    engine: ExpressionEngine,
    registry: ProjectFigmaRegistry | None = None,
    project_id: str | None = None,
    launch_nonce: str | None = None,
    bind_origin: str = "http://127.0.0.1:8766",
    test_mode: bool = False,
    anchor_registry: ApprovedAnchorRegistry | None = None,
    run_mode: str = "subscription_handoff_import",
    adapter_sha256: str | None = None,
    root_fingerprint: str | None = None,
    hub_delivery_sender: HubDeliverySender | None = None,
) -> FastAPI:
    """Create an API bound by the CLI to loopback only."""
    service = ExpressionStudioService(project_root, engine, registry=registry, project_id=project_id, anchor_registry=anchor_registry, run_mode=run_mode)
    sender = hub_delivery_sender if hub_delivery_sender is not None else sender_from_environment()
    app = FastAPI(title="Expression Studio", docs_url=None, redoc_url=None)
    app.add_middleware(BoundedRequestBodyMiddleware, max_body_bytes=_MAX_REQUEST_BODY_BYTES, path="/api/import-runs")
    config_identity = service.config()
    security = StudioSecurity(
        "expression-studio",
        project_root=project_root,
        expected_origin=bind_origin,
        engine_config_sha256=str(config_identity["engine_config_sha256"]),
        figma_registry_sha256=registry.config_sha256 if registry else hashlib.sha256(b"NOT_CONFIGURED").hexdigest(),
        anchor_registry_sha256=anchor_registry.config_sha256 if anchor_registry else hashlib.sha256(b"NOT_CONFIGURED").hexdigest(),
        launch_nonce=launch_nonce,
        adapter_sha256=adapter_sha256,
        root_fingerprint=root_fingerprint,
        test_mode=test_mode,
    )
    install_security(app, security)

    @app.get("/api/config")
    def config(response: Response) -> dict[str, object]:
        response.set_cookie("studio_session", security.session_id, httponly=True, samesite="strict")
        return {**service.config(), "csrf_token": security.csrf_token}

    @app.get("/api/status")
    def status() -> dict[str, object]:
        return security.status_payload(service.config())

    @app.post("/api/runs", status_code=201)
    def create_run(request: ExpressionRequest) -> dict[str, object]:
        try:
            return service.create_run(request).public_view()
        except RunBlockedError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.post("/api/import-runs", status_code=201)
    async def create_import_run(
        request_json: str = Form(...),
        declared_source: str = Form(...),
        candidates: list[UploadFile] = File(...),
    ) -> dict[str, object]:
        try:
            if declared_source not in DECLARED_SOURCES:
                raise ValueError("declared_source is not supported")
            request = ExpressionRequest.model_validate_json(request_json)
            if len(candidates) != request.candidate_count:
                raise ValueError(f"import returned {len(candidates)} candidates; expected {request.candidate_count}")
            source: DeclaredSource = declared_source  # type: ignore[assignment]
            imported = []
            for index, upload in enumerate(candidates):
                data = await read_upload_limited(upload)
                imported.append(validate_imported_image(data, declared_source=source, order=index))
            return service.create_import_run(request, tuple(imported), source).public_view()
        except RunBlockedError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, object]:
        try:
            return service.get_run(run_id).public_view()
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error

    @app.get("/api/runs/{run_id}/candidates/{candidate_index}")
    def candidate(run_id: str, candidate_index: int) -> Response:
        try:
            return Response(content=service.candidate(run_id, candidate_index), media_type="image/png")
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.get("/api/runs/{run_id}/anchor")
    def anchor(run_id: str) -> Response:
        try:
            return Response(content=service.approved_anchor(run_id), media_type="image/png")
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/runs/{run_id}/export")
    def export(run_id: str, payload: SelectionPayload) -> dict[str, object]:
        try:
            return service.export(run_id, payload.selected_candidate).public_view()
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/runs/{run_id}/confirm-delivery")
    def confirm_delivery(run_id: str, payload: SelectionPayload) -> dict[str, object]:
        try:
            record = service.get_run(run_id)
            if record.status == "generated":
                record = service.export(run_id, payload.selected_candidate)
            elif record.status == "exported":
                if record.selected_candidate != payload.selected_candidate:
                    raise RunBlockedError("confirmed candidate cannot change after export")
            else:
                raise RunBlockedError("a generated or exported run is required before confirmation")
            service.prepare_figma_delivery(run_id)
            record = service.get_run(run_id)
            if record.export is None:
                raise RunBlockedError("confirmed export is unavailable")
            expected_sha256 = record.export_output_sha256.get("selected")
            if expected_sha256 is None:
                raise RunBlockedError("confirmed export hash evidence is unavailable")
            selected_bytes = _read_staged_file(
                project_root.resolve(),
                record.export.selected,
                expected_sha256=expected_sha256,
            )
            if sender is None:
                raise HubDeliveryError("Tool Hub confirmed delivery is unavailable")
            delivery = sender(run_id, selected_bytes, "image/png")
            content_sha256 = hashlib.sha256(selected_bytes).hexdigest()
            if (
                delivery.get("tool_id") != "expression-studio"
                or delivery.get("project_id") != record.request.project_id
                or delivery.get("run_id") != run_id
                or delivery.get("content_sha256") != content_sha256
                or not isinstance(delivery.get("delivery_id"), str)
                or not isinstance(delivery.get("tool_route_id"), str)
                or not isinstance(delivery.get("target_node_name"), str)
            ):
                raise HubDeliveryError("Tool Hub delivery response did not match the confirmed export")
            hub_state = str(delivery.get("status", ""))
            verified = hub_state == "DELIVERED_VERIFIED"
            return {
                "status": "CONFIRMED_AND_VERIFIED" if verified else "CONFIRMED_AND_QUEUED",
                "project_save": "SAVED",
                "figma_delivery": "VERIFIED" if verified else "QUEUED",
                "delivery_id": delivery["delivery_id"],
                "content_sha256": content_sha256,
                "tool_route_id": delivery["tool_route_id"],
                "target_node_name": delivery["target_node_name"],
            }
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, DeliveryBlockedError, HubDeliveryError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/runs/{run_id}/figma-delivery")
    def figma_delivery(run_id: str) -> dict[str, object]:
        try:
            return service.prepare_figma_delivery(run_id).public_view()
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, DeliveryBlockedError) as error:
            return JSONResponse(status_code=409, content={"run_id": run_id, "status": "blocked", "detail": str(error)})

    web_root = Path(__file__).parents[2] / "web"
    app.mount("/", StaticFiles(directory=web_root, html=True), name="web")
    return app


def _port(value: str) -> int:
    port = int(value)
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 0 and 65535")
    return port


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Expression Studio on localhost only.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--figma-target-registry", type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--approved-anchor-registry", type=Path)
    parser.add_argument("--run-mode", choices=("subscription_handoff_import", "simulated", "openai"), default="subscription_handoff_import")
    parser.add_argument("--port", type=_port, default=8766)
    parser.add_argument("--startup-file", type=Path)
    return parser


def parse_cli_args(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    args = parser.parse_args(arguments)
    if args.port == 0 and args.startup_file is None:
        parser.error("port 0 requires --startup-file")
    if args.port != 0 and args.startup_file is not None:
        parser.error("--startup-file is reserved for Tool Hub port 0 mode")
    return args


def main() -> None:
    parser = build_parser()
    args = parse_cli_args()
    hub_identity = None
    if args.port == 0:
        try:
            hub_identity = hub_identity_from_environment()
        except HubStartupError as error:
            parser.error(str(error))
    registry = ProjectFigmaRegistry.load(args.figma_target_registry) if args.figma_target_registry else None
    anchor_registry = ApprovedAnchorRegistry.load(args.approved_anchor_registry) if args.approved_anchor_registry else None
    try:
        engine: ExpressionEngine = (
            OpenAIExpressionEngine()
            if args.run_mode == "openai"
            else FakeExpressionEngine(args.project_root)
        )
    except EngineContractError as error:
        parser.error(str(error))
    listener = open_loopback_listener(args.port)
    actual_port = listener.getsockname()[1]
    app = create_app(
        args.project_root,
        engine,
        registry=registry,
        project_id=args.project_id,
        launch_nonce=hub_identity.launch_nonce if hub_identity else None,
        bind_origin=f"http://127.0.0.1:{actual_port}",
        anchor_registry=anchor_registry,
        run_mode=args.run_mode,
        adapter_sha256=hub_identity.adapter_sha256 if hub_identity else None,
        root_fingerprint=hub_identity.root_fingerprint if hub_identity else None,
    )
    if hub_identity and args.startup_file:
        try:
            write_startup_report(
                args.startup_file,
                {
                    "tool_id": "expression-studio",
                    "project_id": args.project_id,
                    "process_id": os.getpid(),
                    "port": actual_port,
                    "launch_nonce": hub_identity.launch_nonce,
                    "adapter_sha256": hub_identity.adapter_sha256,
                    "root_fingerprint": hub_identity.root_fingerprint,
                },
            )
        except HubStartupError as error:
            listener.close()
            parser.error(str(error))
    uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=actual_port)).run(sockets=[listener])


if __name__ == "__main__":
    main()
