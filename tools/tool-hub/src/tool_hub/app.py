"""Minimal reviewed Tool Hub catalog, project binding, and typed launcher."""

from __future__ import annotations

import argparse
from contextlib import asynccontextmanager
from pathlib import Path

from base_tool_contracts import DeliveryBlockedError, ProjectFigmaRegistry
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
    project_id: str
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
    try:
        figma_registry = ProjectFigmaRegistry.load(
            root / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
        )
        figma_registry.assert_canonical(root)
    except (ValueError, DeliveryBlockedError) as error:
        raise RuntimeError("Tool Hub cannot start without its canonical project catalog") from error
    known_projects = figma_registry.public_projects()
    known_project_ids = {item["project_id"] for item in known_projects}
    known_project_names = {
        item["project_id"]: item["display_name"] for item in known_projects
    }
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
        registered_projects = locator.public_projects()
        for project in registered_projects:
            project["display_name"] = known_project_names.get(
                project["project_id"],
                project["display_name"],
            )
        return {
            "tools": public_tools,
            "known_projects": known_projects,
            "projects": registered_projects,
        }

    @app.post("/api/projects", status_code=201)
    def register_project(payload: ProjectRegistration) -> dict[str, str]:
        if payload.project_id not in known_project_ids:
            raise HTTPException(status_code=422, detail="PROJECT_CATALOG_ENTRY_REQUIRED")
        try:
            return locator.register(
                Path(payload.project_root),
                payload.project_id,
            ).public_view()
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
