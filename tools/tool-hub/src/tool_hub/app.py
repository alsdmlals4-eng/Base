"""Minimal reviewed Tool Hub catalog, project binding, and typed launcher."""

from __future__ import annotations

import argparse
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
import uvicorn

from .launcher import LaunchError
from .projects import ProjectBindingError, ProjectLocator
from .registry import HubRegistryError, load_reviewed_tools
from .security import HubSecurity, install_security
from .supervisor import ProcessSupervisor


class ProjectRegistration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_root: str


class LaunchPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tool_id: str
    project_id: str


def create_app(
    base_root: Path,
    project_config: Path,
    *,
    bind_origin: str = "http://127.0.0.1:8764",
    test_mode: bool = False,
    launch_supported: bool | None = None,
) -> FastAPI:
    root = base_root.resolve()
    try:
        tools = load_reviewed_tools(root, launch_supported=launch_supported)
    except HubRegistryError as error:
        raise RuntimeError("Tool Hub cannot start without its reviewed registry") from error
    locator = ProjectLocator(project_config)
    launcher = ProcessSupervisor(
        project_config.parent / "runtime",
        root,
        locator,
        tools,
    )
    security = HubSecurity(bind_origin, test_mode=test_mode)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            yield
        finally:
            launcher.stop_all()

    app = FastAPI(title="Base Tool Hub", docs_url=None, redoc_url=None, lifespan=lifespan)
    install_security(app, security)

    @app.get("/api/config")
    def config(response: Response) -> dict[str, str]:
        response.set_cookie("hub_session", security.session_id, httponly=True, samesite="strict")
        return {"tool_id": "base-tool-hub", "csrf_token": security.csrf_token}

    @app.get("/api/catalog")
    def catalog() -> dict[str, object]:
        public_tools = [
            {
                "tool_id": item["tool_id"],
                "display_name": item["display_name"],
                "capabilities": item["capabilities"],
                "launch_state": (
                    "RUNNABLE" if item.get("_launch_supported") is True else "BLOCKED_PLATFORM"
                ),
            }
            for item in tools
        ]
        return {"tools": public_tools, "projects": locator.public_projects()}

    @app.post("/api/projects", status_code=201)
    def register_project(payload: ProjectRegistration) -> dict[str, str]:
        try:
            return locator.register(Path(payload.project_root)).public_view()
        except ProjectBindingError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.post("/api/launch")
    def launch(payload: LaunchPayload) -> dict[str, object]:
        try:
            return launcher.start(payload.tool_id, payload.project_id).public_view()
        except LaunchError as error:
            state = launcher.view(payload.tool_id, payload.project_id).status
            status_code = 409 if state.startswith("BLOCKED_") else 503
            raise HTTPException(status_code=status_code, detail=str(error)) from error

    web_root = Path(__file__).parents[2] / "web"
    app.mount("/", StaticFiles(directory=web_root, html=True), name="web")
    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Base Tool Hub on localhost only.")
    parser.add_argument("--base-root", type=Path, required=True)
    parser.add_argument("--project-config", type=Path, required=True)
    parser.add_argument("--port", type=int, default=8764)
    args = parser.parse_args()
    origin = f"http://127.0.0.1:{args.port}"
    uvicorn.run(
        create_app(args.base_root, args.project_config, bind_origin=origin),
        host="127.0.0.1",
        port=args.port,
    )


if __name__ == "__main__":
    main()
