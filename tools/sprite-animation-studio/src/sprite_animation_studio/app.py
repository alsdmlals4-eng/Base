"""Localhost-only FastAPI entrypoint for Sprite Animation Studio."""

import argparse
import hashlib
import os
from pathlib import Path
from typing import Annotated, Sequence

from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from base_tool_contracts import ApprovedAnchorRegistry, BoundedRequestBodyMiddleware, HubStartupError, hub_identity_from_environment, open_loopback_listener, write_startup_report

from .curation import CurationState, FrameTransform
from .delivery import DeliveryBlockedError, ProjectFigmaRegistry
from .engine import FakeSpriteEngine, PinnedSpriteGenEngine, SpriteEngine
from .imports import DECLARED_SOURCES, DeclaredSource, read_upload_limited, validate_imported_image
from .models import SpriteAnimationRequest
from .service import RunBlockedError, RunNotFoundError, SpriteAnimationService
from .security import StudioSecurity, install_security


_MAX_REQUEST_BODY_BYTES = 402 * 1024 * 1024


class CurationPayload(CurationState):
    pass


def _curation(payload: CurationPayload) -> CurationState:
    transforms = {int(index): transform for index, transform in payload.transforms.items()}
    return CurationState(selected=payload.selected, transforms=transforms, rejected=payload.rejected)


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
) -> FastAPI:
    """Create the API bound by the CLI to loopback only."""
    service = SpriteAnimationService(project_root, engine, registry=registry, project_id=project_id, anchor_registry=anchor_registry, run_mode=run_mode)
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

    @app.post("/api/runs/{run_id}/figma-delivery")
    def prepare_figma_delivery(run_id: str) -> dict[str, object]:
        try:
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
