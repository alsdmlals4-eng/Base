"""Localhost-only API and CLI for QA Evidence Studio."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import socket
import tempfile

from fastapi import FastAPI, File, HTTPException, Response, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
import uvicorn

from .models import CreateSessionRequest, ReviewStatus
from .security import QaSecurity, install_security
from .service import QaEvidenceError, QaEvidenceService


_MAX_IMAGE_BYTES = 25 * 1024 * 1024


class ReadinessPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    acknowledgement: str = Field(min_length=1, max_length=500)


class ResultPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    item_id: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    status: ReviewStatus
    note: str = Field(default="", max_length=1000)


def _public_session(session: dict[str, object]) -> dict[str, object]:
    public = {key: value for key, value in session.items() if key != "packet_path"}
    if "packet_path" in session:
        public["packet_relative_path"] = (
            f".asset-vault/library/generated/qa-evidence-studio/{session['session_id']}/QA_EVIDENCE_PACKET.json"
        )
    return public


def create_app(
    project_root: Path,
    project_id: str,
    *,
    launch_nonce: str | None = None,
    bind_origin: str = "http://127.0.0.1:8767",
    test_mode: bool = False,
) -> FastAPI:
    service = QaEvidenceService(project_root, project_id)
    security = QaSecurity(
        project_root,
        project_id,
        bind_origin,
        launch_nonce=launch_nonce,
        test_mode=test_mode,
    )
    app = FastAPI(title="QA Evidence Studio", docs_url=None, redoc_url=None)
    install_security(app, security)

    @app.get("/api/config")
    def config(response: Response) -> dict[str, str]:
        response.set_cookie("qa_session", security.session_id, httponly=True, samesite="strict")
        return {
            "tool_id": "qa-evidence-studio",
            "project_id": project_id,
            "reviewer_role": "DEVELOPER_OWNER",
            "external_tester_status": "NOT_AVAILABLE_NOT_REQUIRED_FOR_PHASE_1",
            "android_status": "DEFERRED_NOT_CONNECTED",
            "actual_review_gate": "AFTER_IMAGE_AND_UX_PLACEMENT",
            "csrf_token": security.csrf_token,
        }

    @app.get("/api/status")
    def status() -> dict[str, object]:
        return security.status()

    @app.post("/api/sessions", status_code=201)
    def create_session(payload: CreateSessionRequest) -> dict[str, object]:
        try:
            return _public_session(service.create_session(payload))
        except QaEvidenceError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.get("/api/sessions/{session_id}")
    def get_session(session_id: str) -> dict[str, object]:
        try:
            return _public_session(service.get_session(session_id))
        except QaEvidenceError as error:
            raise HTTPException(status_code=404, detail="QA session not found") from error

    @app.post("/api/sessions/{session_id}/visual-ux-ready")
    def visual_ux_ready(session_id: str, payload: ReadinessPayload) -> dict[str, object]:
        try:
            return _public_session(service.mark_visual_ux_ready(session_id, payload.acknowledgement))
        except QaEvidenceError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/sessions/{session_id}/results")
    def record_result(session_id: str, payload: ResultPayload) -> dict[str, object]:
        try:
            return _public_session(
                service.record_result(session_id, payload.item_id, payload.status, payload.note)
            )
        except QaEvidenceError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    @app.post("/api/sessions/{session_id}/evidence", status_code=201)
    async def add_evidence(session_id: str, image: UploadFile = File(...)) -> dict[str, object]:
        data = await image.read(_MAX_IMAGE_BYTES + 1)
        try:
            return service.add_image_evidence(
                session_id,
                image.filename or "evidence",
                image.content_type or "application/octet-stream",
                data,
            )
        except QaEvidenceError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

    @app.post("/api/sessions/{session_id}/finalize")
    def finalize(session_id: str) -> dict[str, object]:
        try:
            return _public_session(service.finalize(session_id))
        except QaEvidenceError as error:
            raise HTTPException(status_code=409, detail=str(error)) from error

    web_root = Path(__file__).parents[2] / "web"
    app.mount("/", StaticFiles(directory=web_root, html=True), name="web")
    return app


def _write_startup(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".qa-startup-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Run QA Evidence Studio on localhost only.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--port", type=int, default=8767)
    parser.add_argument("--launch-nonce")
    parser.add_argument("--startup-file", type=Path)
    args = parser.parse_args()
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", args.port))
    listener.listen(128)
    actual_port = listener.getsockname()[1]
    origin = f"http://127.0.0.1:{actual_port}"
    app = create_app(
        args.project_root,
        args.project_id,
        launch_nonce=args.launch_nonce,
        bind_origin=origin,
    )
    if args.startup_file:
        _write_startup(
            args.startup_file,
            {
                "tool_id": "qa-evidence-studio",
                "project_id": args.project_id,
                "port": actual_port,
                "launch_nonce": args.launch_nonce,
                "process_id": os.getpid(),
            },
        )
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=actual_port))
    server.run(sockets=[listener])


if __name__ == "__main__":
    main()
