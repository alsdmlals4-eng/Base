"""Localhost-only FastAPI entrypoint for Sprite Animation Studio."""

import argparse
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from .curation import CurationState, FrameTransform
from .engine import FakeSpriteEngine, PinnedSpriteGenEngine, SpriteEngine
from .models import SpriteAnimationRequest
from .service import RunBlockedError, RunNotFoundError, SpriteAnimationService


class CurationPayload(CurationState):
    pass


def _curation(payload: CurationPayload) -> CurationState:
    transforms = {int(index): transform for index, transform in payload.transforms.items()}
    return CurationState(selected=payload.selected, transforms=transforms, rejected=payload.rejected)


def create_app(project_root: Path, engine: SpriteEngine) -> FastAPI:
    """Create the API bound by the CLI to loopback only."""
    service = SpriteAnimationService(project_root, engine)
    app = FastAPI(title="Sprite Animation Studio", docs_url=None, redoc_url=None)

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

    web_root = Path(__file__).parents[2] / "web"
    if web_root.is_dir():
        app.mount("/", StaticFiles(directory=web_root, html=True), name="web")
    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Sprite Animation Studio on localhost.")
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--sprite-gen-executable", type=Path)
    parser.add_argument("--fake-engine", action="store_true", help="Use deterministic fixtures only; never generates art.")
    args = parser.parse_args()
    if args.fake_engine:
        engine: SpriteEngine = FakeSpriteEngine()
    elif args.sprite_gen_executable:
        engine = PinnedSpriteGenEngine(args.sprite_gen_executable, args.project_root)
    else:
        parser.error("provide --sprite-gen-executable or explicitly choose --fake-engine")
    uvicorn.run(create_app(args.project_root, engine), host="127.0.0.1", port=8765)


if __name__ == "__main__":
    main()
