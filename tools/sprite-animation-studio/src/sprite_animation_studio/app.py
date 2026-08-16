"""Localhost-only FastAPI entrypoint for Sprite Animation Studio."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import threading
from typing import Annotated, Sequence
from urllib.parse import urlsplit

from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from base_tool_contracts import (
    ApprovedAnchorRegistry,
    BoundedRequestBodyMiddleware,
    HubDeliveryError,
    HubDeliverySender,
    HubStartupError,
    hub_identity_from_environment,
    open_loopback_listener,
    sender_from_environment,
    write_startup_report,
)

from .curation import CurationState, FrameTransform
from .delivery import DeliveryBlockedError, ProjectFigmaRegistry
from .delivery_routes import SPRITE_DELIVERY_TARGETS
from .engine import FakeSpriteEngine, PinnedSpriteGenEngine, SpriteEngine
from .imports import DECLARED_SOURCES, DeclaredSource, read_upload_limited, validate_imported_image
from .models import SpriteAnimationRequest
from .service import RunBlockedError, RunNotFoundError, SpriteAnimationService, _read_staged_file
from .security import StudioSecurity, install_security


_MAX_REQUEST_BODY_BYTES = 402 * 1024 * 1024
_PAIRING_CODE = re.compile(r"^\d{6}$")
_DELIVERY_STATES = frozenset({"QUEUED", "CLAIMED", "EXPIRED", "DELIVERED_VERIFIED"})
_BRIDGE_STATES = frozenset({"PAIRING_REQUIRED", "BRIDGE_PAIRED"})
_PUBLIC_DELIVERY_STATES = frozenset({"DELIVERY_PENDING", "FIGMA_DELIVERED_VERIFIED", "NO_PENDING_DELIVERY"})


class CurationPayload(CurationState):
    pass


def _curation(payload: CurationPayload) -> CurationState:
    transforms = {int(index): transform for index, transform in payload.transforms.items()}
    return CurationState(selected=payload.selected, transforms=transforms, rejected=payload.rejected)


def _validated_figma_url(value: object) -> str:
    if not isinstance(value, str):
        raise HubDeliveryError("Tool Hub Figma URL is invalid")
    parsed = urlsplit(value)
    if (
        parsed.scheme != "https"
        or parsed.hostname != "www.figma.com"
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port not in {None, 443}
        or not parsed.path.startswith("/design/")
        or parsed.fragment
    ):
        raise HubDeliveryError("Tool Hub Figma URL is invalid")
    return value


def _normalize_delivery_payload(
    delivery: dict[str, object],
    *,
    project_id: str,
    run_id: str,
    content_sha256: str,
    expected_tool_route_id: str,
    expected_target_node_name: str,
    expected_delivery_id: str | None = None,
) -> dict[str, object]:
    delivery_id = delivery.get("delivery_id")
    status = delivery.get("status")
    bridge_state = delivery.get("bridge_state")
    delivery_state = delivery.get("delivery_state")
    if (
        delivery.get("tool_id") != "sprite-animation-studio"
        or delivery.get("project_id") != project_id
        or delivery.get("run_id") != run_id
        or delivery.get("content_sha256") != content_sha256
        or delivery.get("tool_route_id") != expected_tool_route_id
        or delivery.get("target_node_name") != expected_target_node_name
        or not isinstance(delivery_id, str)
        or not delivery_id
        or status not in _DELIVERY_STATES
        or bridge_state not in _BRIDGE_STATES
        or delivery_state not in _PUBLIC_DELIVERY_STATES
    ):
        raise HubDeliveryError("Tool Hub delivery response did not match the confirmed atlas")
    if expected_delivery_id is not None and delivery_id != expected_delivery_id:
        raise HubDeliveryError("Tool Hub delivery status changed delivery identity")
    figma_url = _validated_figma_url(delivery.get("figma_url"))
    normalized: dict[str, object] = {
        "status": status,
        "delivery_id": delivery_id,
        "tool_route_id": expected_tool_route_id,
        "target_node_name": expected_target_node_name,
        "bridge_state": bridge_state,
        "delivery_state": delivery_state,
        "figma_url": figma_url,
    }
    if status == "DELIVERED_VERIFIED":
        if bridge_state != "BRIDGE_PAIRED" or delivery_state != "FIGMA_DELIVERED_VERIFIED":
            raise HubDeliveryError("Tool Hub verified delivery state is inconsistent")
    elif status in {"QUEUED", "CLAIMED"}:
        if delivery_state != "DELIVERY_PENDING":
            raise HubDeliveryError("Tool Hub pending delivery state is inconsistent")
    elif status == "EXPIRED" and delivery_state != "NO_PENDING_DELIVERY":
        raise HubDeliveryError("Tool Hub expired delivery state is inconsistent")
    if bridge_state == "PAIRING_REQUIRED" and status != "EXPIRED":
        pairing_code = delivery.get("pairing_code")
        pairing_expires_at = delivery.get("pairing_expires_at")
        if (
            not isinstance(pairing_code, str)
            or _PAIRING_CODE.fullmatch(pairing_code) is None
            or not isinstance(pairing_expires_at, (int, float))
            or pairing_expires_at <= 0
        ):
            raise HubDeliveryError("Tool Hub pairing identity is invalid")
        normalized["pairing_code"] = pairing_code
        normalized["pairing_expires_at"] = float(pairing_expires_at)
    return normalized


def _confirmation_response(
    *,
    record: object,
    run_id: str,
    content_sha256: str,
    delivery: dict[str, object],
) -> dict[str, object]:
    status = str(delivery["status"])
    bridge_state = str(delivery["bridge_state"])
    if status == "DELIVERED_VERIFIED":
        public_status = "CONFIRMED_AND_VERIFIED"
        figma_delivery = "VERIFIED"
    elif status == "EXPIRED":
        public_status = "CONFIRMED_DELIVERY_EXPIRED"
        figma_delivery = "EXPIRED"
    elif bridge_state == "PAIRING_REQUIRED":
        public_status = "CONFIRMED_BRIDGE_REQUIRED"
        figma_delivery = "BRIDGE_REQUIRED"
    else:
        public_status = "CONFIRMED_AND_QUEUED"
        figma_delivery = "QUEUED"
    response: dict[str, object] = {
        "status": public_status,
        "project_save": "SAVED",
        "figma_delivery": figma_delivery,
        "bridge_state": delivery["bridge_state"],
        "delivery_state": delivery["delivery_state"],
        "figma_url": delivery["figma_url"],
        "delivery_status_url": f"/api/runs/{run_id}/delivery-status",
        "download_state": "DOWNLOAD_READY",
        "download_url": f"/api/runs/{run_id}/confirmed-download",
        "delivery_id": delivery["delivery_id"],
        "content_sha256": content_sha256,
        "tool_route_id": delivery["tool_route_id"],
        "target_node_name": delivery["target_node_name"],
        "provider_call_made": bool(getattr(record, "provider_call_made", False)),
    }
    if "pairing_code" in delivery:
        response["pairing_code"] = delivery["pairing_code"]
        response["pairing_expires_at"] = delivery["pairing_expires_at"]
    return response


def create_app(
    project_root: Path,
    engine: SpriteEngine,
    registry: ProjectFigmaRegistry | None = None,
    project_id: str | None = None,
    launch_nonce: str | None = None,
    bind_origin: str = "http://127.0.0.1:8765",
    test_mode: bool = False,
    anchor_registry: ApprovedAnchorRegistry | None = None,
    run_mode: str = "subscription_handoff_import",
    adapter_sha256: str | None = None,
    root_fingerprint: str | None = None,
    hub_delivery_sender: HubDeliverySender | None = None,
) -> FastAPI:
    """Create the API bound by the CLI to loopback only."""
    project_root = project_root.resolve()
    service = SpriteAnimationService(project_root, engine, registry=registry, project_id=project_id, anchor_registry=anchor_registry, run_mode=run_mode)
    sender = hub_delivery_sender if hub_delivery_sender is not None else sender_from_environment()
    confirmed_deliveries: dict[str, dict[str, object]] = {}
    confirmed_delivery_lock = threading.Lock()
    app = FastAPI(title="Sprite Animation Studio", docs_url=None, redoc_url=None)
    app.add_middleware(BoundedRequestBodyMiddleware, max_body_bytes=_MAX_REQUEST_BODY_BYTES, path="/api/import-runs")
    config_identity = service.config()
    security = StudioSecurity(
        "sprite-animation-studio",
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
    def create_run(request: SpriteAnimationRequest) -> dict[str, object]:
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
        frames: list[UploadFile] = File(...),
    ) -> dict[str, object]:
        try:
            if declared_source not in DECLARED_SOURCES:
                raise ValueError("declared_source is not supported")
            request = SpriteAnimationRequest.model_validate_json(request_json)
            if len(frames) != request.action.frame_count:
                raise ValueError(f"import returned {len(frames)} frames; expected {request.action.frame_count}")
            source: DeclaredSource = declared_source  # type: ignore[assignment]
            imported = []
            for index, upload in enumerate(frames):
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

    @app.get("/api/runs/{run_id}/frames/{frame_index}")
    def get_candidate_frame(run_id: str, frame_index: int) -> Response:
        try:
            return Response(content=service.candidate_frame(run_id, frame_index), media_type="image/png")
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.get("/api/runs/{run_id}/anchor")
    def get_approved_anchor(run_id: str) -> Response:
        try:
            return Response(content=service.approved_anchor(run_id), media_type="image/png")
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/runs/{run_id}/curation")
    def save_run_curation(run_id: str, payload: CurationPayload) -> dict[str, object]:
        try:
            return service.save_curation(run_id, _curation(payload)).public_view()
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/runs/{run_id}/export")
    def export_run_endpoint(run_id: str, payload: CurationPayload) -> dict[str, object]:
        try:
            return service.export(run_id, _curation(payload)).public_view()
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except RunBlockedError as error:
            return JSONResponse(status_code=409, content={"run_id": run_id, "status": "blocked", "detail": str(error)})
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.post("/api/runs/{run_id}/confirm-delivery")
    def confirm_delivery(run_id: str) -> dict[str, object]:
        try:
            with confirmed_delivery_lock:
                prior = confirmed_deliveries.get(run_id)
                if prior is not None:
                    return dict(prior)

                record = service.get_run(run_id)
                if record.status != "exported" or record.export is None:
                    raise RunBlockedError("an exported run is required before confirmation")
                service.prepare_figma_delivery(run_id)
                route_id = service.delivery_route_id(run_id)
                target_name = SPRITE_DELIVERY_TARGETS[route_id]
                expected_sha256 = record.export_output_sha256.get("atlas")
                if expected_sha256 is None:
                    raise RunBlockedError("confirmed atlas hash evidence is unavailable")
                atlas_bytes = _read_staged_file(
                    project_root,
                    record.export.atlas,
                    expected_sha256=expected_sha256,
                )
                content_sha256 = hashlib.sha256(atlas_bytes).hexdigest()
                if content_sha256 != expected_sha256:
                    raise RunBlockedError("confirmed atlas hash evidence does not match the export")
                if sender is None:
                    raise HubDeliveryError("Tool Hub confirmed delivery is unavailable")
                delivery = sender(run_id, atlas_bytes, "image/png", route_id)
                normalized = _normalize_delivery_payload(
                    delivery,
                    project_id=record.request.project_id,
                    run_id=run_id,
                    content_sha256=content_sha256,
                    expected_tool_route_id=route_id,
                    expected_target_node_name=target_name,
                )
                response = _confirmation_response(
                    record=record,
                    run_id=run_id,
                    content_sha256=content_sha256,
                    delivery=normalized,
                )
                confirmed_deliveries[run_id] = dict(response)
                return response
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, DeliveryBlockedError, HubDeliveryError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.get("/api/runs/{run_id}/delivery-status")
    def delivery_status(run_id: str) -> dict[str, object]:
        try:
            with confirmed_delivery_lock:
                prior = confirmed_deliveries.get(run_id)
                if prior is None:
                    raise RunBlockedError("confirmation is required before delivery status refresh")
                prior = dict(prior)
            record = service.get_run(run_id)
            if record.export is None:
                raise RunBlockedError("confirmed atlas export is unavailable")
            content_sha256 = prior.get("content_sha256")
            delivery_id = prior.get("delivery_id")
            route_id = prior.get("tool_route_id")
            target_name = prior.get("target_node_name")
            if (
                not isinstance(content_sha256, str)
                or not isinstance(delivery_id, str)
                or not isinstance(route_id, str)
                or not isinstance(target_name, str)
                or record.export_output_sha256.get("atlas") != content_sha256
            ):
                raise RunBlockedError("confirmed atlas delivery evidence is unavailable")
            _read_staged_file(project_root, record.export.atlas, expected_sha256=content_sha256)
            if sender is None:
                raise HubDeliveryError("Tool Hub confirmed delivery is unavailable")
            current = sender.status(delivery_id)
            normalized = _normalize_delivery_payload(
                current,
                project_id=record.request.project_id,
                run_id=run_id,
                content_sha256=content_sha256,
                expected_tool_route_id=route_id,
                expected_target_node_name=target_name,
                expected_delivery_id=delivery_id,
            )
            response = _confirmation_response(
                record=record,
                run_id=run_id,
                content_sha256=content_sha256,
                delivery=normalized,
            )
            with confirmed_delivery_lock:
                if run_id not in confirmed_deliveries:
                    raise RunBlockedError("confirmed delivery identity changed during status refresh")
                confirmed_deliveries[run_id] = dict(response)
            return response
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, HubDeliveryError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.get("/api/runs/{run_id}/confirmed-download")
    def confirmed_download(run_id: str) -> Response:
        try:
            with confirmed_delivery_lock:
                prior = confirmed_deliveries.get(run_id)
                if prior is None:
                    raise RunBlockedError("confirmation is required before download")
                confirmed_sha256 = prior.get("content_sha256")
            if not isinstance(confirmed_sha256, str):
                raise RunBlockedError("confirmed atlas download evidence is unavailable")
            record = service.get_run(run_id)
            if record.export is None:
                raise RunBlockedError("confirmed atlas export is unavailable")
            expected_sha256 = record.export_output_sha256.get("atlas")
            if expected_sha256 is None or expected_sha256 != confirmed_sha256:
                raise RunBlockedError("confirmed atlas hash evidence does not match delivery")
            atlas_bytes = _read_staged_file(
                project_root,
                record.export.atlas,
                expected_sha256=expected_sha256,
            )
            if hashlib.sha256(atlas_bytes).hexdigest() != confirmed_sha256:
                raise RunBlockedError("confirmed atlas changed after delivery confirmation")
            filename = f"atlas-{run_id[:12]}.png"
            return Response(
                content=atlas_bytes,
                media_type="image/png",
                headers={
                    "Content-Disposition": f'attachment; filename="{filename}"',
                    "X-Content-SHA256": confirmed_sha256,
                },
            )
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/runs/{run_id}/figma-delivery")
    def prepare_figma_delivery(run_id: str) -> dict[str, object]:
        try:
            with confirmed_delivery_lock:
                if run_id in confirmed_deliveries:
                    raise RunBlockedError("direct Figma delivery is already queued for this run")
            return service.prepare_figma_delivery(run_id).public_view()
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, DeliveryBlockedError) as error:
            return JSONResponse(status_code=409, content={"run_id": run_id, "status": "blocked", "detail": str(error)})

    web_root = Path(__file__).parents[2] / "web"
    if web_root.is_dir():
        app.mount("/", StaticFiles(directory=web_root, html=True), name="web")
    return app


def _port(value: str) -> int:
    port = int(value)
    if not 0 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 0 and 65535")
    return port


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Sprite Animation Studio on localhost.")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--sprite-gen-executable", type=Path)
    parser.add_argument("--sprite-gen-repository", type=Path)
    parser.add_argument("--figma-target-registry", type=Path, help="Project routing JSON; enables guarded project-GPT Figma delivery packets.")
    parser.add_argument("--project-id", required=True, help="Canonical project ID bound immutably to this Studio instance.")
    parser.add_argument("--approved-anchor-registry", type=Path)
    parser.add_argument("--fake-engine", action="store_true", help="Use deterministic fixtures only; never generates art.")
    parser.add_argument("--run-mode", choices=("subscription_handoff_import", "simulated", "pinned_sprite_gen"), default="subscription_handoff_import")
    parser.add_argument("--port", type=_port, default=8765)
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
    if args.run_mode == "subscription_handoff_import":
        engine = FakeSpriteEngine()
    elif args.fake_engine or args.run_mode == "simulated":
        engine: SpriteEngine = FakeSpriteEngine()
    elif args.sprite_gen_executable and args.sprite_gen_repository:
        engine = PinnedSpriteGenEngine(args.sprite_gen_executable, args.project_root, sprite_gen_repository=args.sprite_gen_repository)
    else:
        parser.error("provide --sprite-gen-executable with --sprite-gen-repository or explicitly choose --fake-engine")
    try:
        registry = ProjectFigmaRegistry.load(args.figma_target_registry) if args.figma_target_registry else None
        anchor_registry = ApprovedAnchorRegistry.load(args.approved_anchor_registry) if args.approved_anchor_registry else None
    except ValueError as error:
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
                    "tool_id": "sprite-animation-studio",
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
    uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=actual_port)).run(
        sockets=[listener]
    )


if __name__ == "__main__":
    main()
