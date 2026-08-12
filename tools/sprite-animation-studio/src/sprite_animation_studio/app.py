"""Localhost-only FastAPI entrypoint for Sprite Animation Studio."""

import argparse
import hashlib
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from base_tool_contracts import ApprovedAnchorRegistry

from .curation import CurationState, FrameTransform
from .delivery import DeliveryBlockedError, ProjectFigmaRegistry
from .engine import FakeSpriteEngine, PinnedSpriteGenEngine, SpriteEngine
from .models import SpriteAnimationRequest
from .service import RunBlockedError, RunNotFoundError, SpriteAnimationService
from .security import StudioSecurity, install_security


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
) -> FastAPI:
    """Create the API bound by the CLI to loopback only."""
    service = SpriteAnimationService(project_root, engine, registry=registry, project_id=project_id, anchor_registry=anchor_registry)
    app = FastAPI(title="Sprite Animation Studio", docs_url=None, redoc_url=None)
    config_identity = service.config()
    security = StudioSecurity(
        "sprite-animation-studio",
        project_root=project_root,
        expected_origin=bind_origin,
        engine_config_sha256=str(config_identity["engine_config_sha256"]),
        figma_registry_sha256=registry.config_sha256 if registry else hashlib.sha256(b"NOT_CONFIGURED").hexdigest(),
        anchor_registry_sha256=anchor_registry.config_sha256 if anchor_registry else hashlib.sha256(b"NOT_CONFIGURED").hexdigest(),
        launch_nonce=launch_nonce,
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
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.get("/api/runs/{run_id}")
    def get_run(run_id: str) -> dict[str, object]:
        try:
            return service.get_run(run_id).public_view()
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error

    @app.get("/api/runs/{run_id}/frames/{frame_index}")
    def get_candidate_frame(run_id: str, frame_index: int) -> FileResponse:
        try:
            return FileResponse(service.candidate_frame(run_id, frame_index), media_type="image/png")
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.get("/api/runs/{run_id}/anchor")
    def get_approved_anchor(run_id: str) -> FileResponse:
        try:
            return FileResponse(service.approved_anchor(run_id), media_type="image/png")
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
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
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
    parser.add_argument("--launch-nonce")
    parser.add_argument("--port", type=_port, default=8765)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.fake_engine:
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
    uvicorn.run(
        create_app(
            args.project_root,
            engine,
            registry=registry,
            project_id=args.project_id,
            launch_nonce=args.launch_nonce,
            bind_origin=f"http://127.0.0.1:{args.port}",
            anchor_registry=anchor_registry,
        ),
        host="127.0.0.1",
        port=args.port,
    )


if __name__ == "__main__":
    main()
