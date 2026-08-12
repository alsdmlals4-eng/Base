"""Localhost-only FastAPI entrypoint for Expression Studio."""

import argparse
import hashlib
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from base_tool_contracts import ApprovedAnchorRegistry
from pydantic import BaseModel, ConfigDict, Field

from .delivery import DeliveryBlockedError, ProjectFigmaRegistry
from .engine import FakeExpressionEngine, ExpressionEngine
from .models import ExpressionRequest
from .service import ExpressionStudioService, RunBlockedError, RunNotFoundError
from .security import StudioSecurity, install_security


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
) -> FastAPI:
    """Create an API bound by the CLI to loopback only."""
    service = ExpressionStudioService(project_root, engine, registry=registry, project_id=project_id, anchor_registry=anchor_registry)
    app = FastAPI(title="Expression Studio", docs_url=None, redoc_url=None)
    config_identity = service.config()
    security = StudioSecurity(
        "expression-studio",
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
    def create_run(request: ExpressionRequest) -> dict[str, object]:
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

    @app.get("/api/runs/{run_id}/candidates/{candidate_index}")
    def candidate(run_id: str, candidate_index: int) -> FileResponse:
        try:
            return FileResponse(service.candidate(run_id, candidate_index), media_type="image/png")
        except RunNotFoundError as error:
            raise HTTPException(status_code=404, detail="run not found") from error
        except (RunBlockedError, ValueError) as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.get("/api/runs/{run_id}/anchor")
    def anchor(run_id: str) -> FileResponse:
        try:
            return FileResponse(service.approved_anchor(run_id), media_type="image/png")
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


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Expression Studio on localhost only.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--figma-target-registry", type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--approved-anchor-registry", type=Path)
    parser.add_argument("--port", type=int, default=8766)
    parser.add_argument("--launch-nonce")
    args = parser.parse_args()
    registry = ProjectFigmaRegistry.load(args.figma_target_registry) if args.figma_target_registry else None
    anchor_registry = ApprovedAnchorRegistry.load(args.approved_anchor_registry) if args.approved_anchor_registry else None
    app = create_app(
        args.project_root,
        FakeExpressionEngine(args.project_root),
        registry=registry,
        project_id=args.project_id,
        launch_nonce=args.launch_nonce,
        bind_origin=f"http://127.0.0.1:{args.port}",
        anchor_registry=anchor_registry,
    )
    uvicorn.run(app, host="127.0.0.1", port=args.port)


if __name__ == "__main__":
    main()
