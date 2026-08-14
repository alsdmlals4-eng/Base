"""Minimal reviewed Tool Hub catalog, project binding, and typed launcher."""

from __future__ import annotations

import argparse
from contextlib import asynccontextmanager
import hashlib
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
from typing import Callable
from urllib.parse import urlsplit

from base_tool_contracts import DeliveryBlockedError, ProjectFigmaRegistry
from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
import uvicorn

from .launcher import LaunchError
from .onboarding import CloneRunner, ProjectOnboardingService
from .projects import ProjectBindingError, ProjectLocator
from .registry import HubRegistryError, load_reviewed_tools
from .security import HubSecurity, install_security
from .supervisor import ProcessSupervisor
from .windows_launcher import (
    LauncherError,
    WindowsLauncherInstaller,
    hub_runtime_fingerprint,
    project_config_fingerprint,
)


class ProjectRegistration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    project_id: str
    project_root: str


class LaunchPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tool_id: str
    project_id: str


class EmptyPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")


def configure_bounded_runtime_logging(log_directory: Path) -> RotatingFileHandler:
    directory = Path(log_directory).absolute()
    directory.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        directory / "tool-hub.log",
        maxBytes=1024 * 1024,
        backupCount=2,
        encoding="utf-8",
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    return handler


def create_app(
    base_root: Path,
    project_config: Path,
    *,
    bind_origin: str = "http://127.0.0.1:8764",
    test_mode: bool = False,
    launch_supported: bool | None = None,
    onboarding_home: Path | None = None,
    managed_project_root: Path | None = None,
    onboarding_clone_runner: CloneRunner | None = None,
    launcher_token: str | None = None,
    shutdown_callback: Callable[[], None] | None = None,
    windows_launcher_installer: WindowsLauncherInstaller | None = None,
) -> FastAPI:
    if onboarding_clone_runner is not None and not test_mode:
        raise ValueError("test clone runner requires test mode")
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
    onboarding = ProjectOnboardingService(
        locator,
        figma_registry,
        home_root=onboarding_home,
        managed_root=managed_project_root,
        clone_runner=onboarding_clone_runner,
    )
    launcher = ProcessSupervisor(
        project_config.parent / "runtime",
        root,
        locator,
        tools,
    )
    security = HubSecurity(bind_origin, test_mode=test_mode)
    root_stat = root.stat()
    root_fingerprint = hashlib.sha256(
        f"{root}:{root_stat.st_dev}:{root_stat.st_ino}".encode()
    ).hexdigest()
    effective_launcher_token = launcher_token or os.environ.get("BASE_TOOL_HUB_LAUNCHER_TOKEN")
    parsed_origin = urlsplit(bind_origin)
    hub_port = parsed_origin.port or (443 if parsed_origin.scheme == "https" else 80)
    installer = windows_launcher_installer
    if installer is None and os.name == "nt":
        installer = WindowsLauncherInstaller(root, project_config)

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
        return {
            "tool_id": "base-tool-hub",
            "csrf_token": security.csrf_token,
            "windows_launcher_state": installer.status() if installer else "BLOCKED_PLATFORM",
        }

    @app.get("/api/launcher-status")
    def launcher_status(
        response: Response,
        x_hub_launcher_token: str | None = Header(default=None),
    ) -> dict[str, object]:
        if not effective_launcher_token or x_hub_launcher_token != effective_launcher_token:
            raise HTTPException(status_code=403, detail="LAUNCHER_IDENTITY_REQUIRED")
        return {
            "tool_id": "base-tool-hub",
            "root_fingerprint": root_fingerprint,
            "project_config_fingerprint": project_config_fingerprint(project_config),
            "hub_runtime_fingerprint": hub_runtime_fingerprint(root),
            "port": hub_port,
            "process_id": os.getpid(),
        }

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
        public_known_projects = [
            {**project, **onboarding.status(project["project_id"]).public_view()}
            for project in known_projects
        ]
        return {
            "tools": public_tools,
            "known_projects": public_known_projects,
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

    @app.post("/api/projects/{project_id}/onboard")
    def onboard_project(project_id: str, payload: EmptyPayload) -> dict[str, str]:
        if project_id not in known_project_ids:
            raise HTTPException(status_code=422, detail="PROJECT_CATALOG_ENTRY_REQUIRED")
        result = onboarding.onboard(project_id)
        if result.local_state != "REGISTERED":
            raise HTTPException(status_code=409, detail=result.local_state)
        return result.public_view()

    @app.post("/api/windows-launcher/install")
    def install_windows_launcher(payload: EmptyPayload) -> dict[str, str]:
        if installer is None:
            raise HTTPException(status_code=409, detail="BLOCKED_PLATFORM")
        try:
            return installer.install().public_view()
        except LauncherError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/shutdown")
    def shutdown(payload: EmptyPayload) -> dict[str, str]:
        launcher.stop_all()
        if shutdown_callback is not None:
            shutdown_callback()
        return {"state": "SHUTTING_DOWN"}

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
    holder: dict[str, uvicorn.Server] = {}

    def request_shutdown() -> None:
        holder["server"].should_exit = True

    app = create_app(
        args.base_root,
        args.project_config,
        bind_origin=origin,
        shutdown_callback=request_shutdown,
    )
    runtime_handler: RotatingFileHandler | None = None
    configured_loggers: list[logging.Logger] = []
    if local_app_data := os.environ.get("LOCALAPPDATA"):
        runtime_handler = configure_bounded_runtime_logging(
            Path(local_app_data) / "BaseToolHub" / "logs"
        )
        for logger_name in ("uvicorn", "uvicorn.error"):
            logger = logging.getLogger(logger_name)
            logger.handlers = [runtime_handler]
            logger.propagate = False
            configured_loggers.append(logger)
    server = uvicorn.Server(
        uvicorn.Config(
            app,
            host="127.0.0.1",
            port=args.port,
            access_log=False,
            log_config=None,
        )
    )
    holder["server"] = server
    try:
        server.run()
    finally:
        for logger in configured_loggers:
            logger.handlers = []
        if runtime_handler is not None:
            runtime_handler.close()


if __name__ == "__main__":
    main()
