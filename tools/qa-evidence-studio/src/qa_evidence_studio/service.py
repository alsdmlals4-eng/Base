"""Developer-only PC QA session state machine and evidence packets."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import secrets
import subprocess
from typing import Any

from .models import CreateSessionRequest, ReviewStatus
from .paths import QaPathError, assert_session_directory, atomic_write_bytes, prepare_session_directory


class QaEvidenceError(ValueError):
    pass


_SESSION_ID = re.compile(r"^qa-[0-9a-f]{16}$")
_PROJECT_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_MAX_IMAGE_BYTES = 25 * 1024 * 1024
_IMAGE_TYPES = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _is_expected_image(content_type: str, data: bytes) -> bool:
    if content_type == "image/png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type == "image/jpeg":
        return data.startswith(b"\xff\xd8\xff")
    if content_type == "image/webp":
        return len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP"
    return False


class QaEvidenceService:
    def __init__(self, project_root: Path, project_id: str) -> None:
        if not _PROJECT_ID.fullmatch(project_id):
            raise QaEvidenceError("project_id must be canonical kebab-case")
        self.project_root = project_root.resolve()
        self.project_id = project_id
        self.sessions_root = self.project_root / ".asset-vault" / "library" / "generated" / "qa-evidence-studio"

    def _session_dir(self, session_id: str) -> Path:
        if not _SESSION_ID.fullmatch(session_id):
            raise QaEvidenceError("session_id is invalid")
        path = self.sessions_root / session_id
        try:
            assert_session_directory(self.project_root, path)
        except QaPathError as error:
            raise QaEvidenceError(str(error)) from error
        return path

    def _load(self, session_id: str) -> tuple[Path, dict[str, Any]]:
        directory = self._session_dir(session_id)
        try:
            session = json.loads((directory / "session.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise QaEvidenceError("QA session was not found or is unreadable") from error
        if not isinstance(session, dict) or session.get("session_id") != session_id or session.get("project_id") != self.project_id:
            raise QaEvidenceError("QA session identity does not match the bound project")
        return directory, session

    def _save(self, directory: Path, session: dict[str, Any]) -> None:
        session["updated_at"] = _now()
        try:
            atomic_write_bytes(
                directory,
                "session.json",
                (json.dumps(session, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(),
            )
        except QaPathError as error:
            raise QaEvidenceError(str(error)) from error

    def create_session(self, request: CreateSessionRequest) -> dict[str, Any]:
        commit = subprocess.run(
            ["git", "-C", str(self.project_root), "cat-file", "-t", request.build_commit],
            capture_output=True,
            text=True,
            check=False,
        )
        if commit.returncode != 0 or commit.stdout.strip() != "commit":
            raise QaEvidenceError("build commit must exist in the bound project repository")
        session_id = f"qa-{secrets.token_hex(8)}"
        try:
            directory = prepare_session_directory(self.project_root, session_id)
        except QaPathError as error:
            raise QaEvidenceError(str(error)) from error
        created = _now()
        session: dict[str, Any] = {
            "schema_version": 1,
            "session_id": session_id,
            "project_id": self.project_id,
            "title": request.title,
            "build_commit": request.build_commit,
            "stage": "PREPARING_VISUAL_UX",
            "visual_ux_placement": {"status": "NOT_READY", "developer_acknowledgement": None},
            "reviewer": {"role": "DEVELOPER_OWNER", "count": 1},
            "external_tester_status": "NOT_AVAILABLE_NOT_REQUIRED_FOR_PHASE_1",
            "platforms": {
                "pc": {"status": "NOT_RUN"},
                "android": {
                    "status": "DEFERRED_NOT_CONNECTED",
                    "gate": "AFTER_PC_IMPLEMENTATION_BEFORE_RELEASE",
                },
            },
            "checklist": [
                {**item.model_dump(), "status": "NOT_RUN", "note": ""}
                for item in request.checklist
            ],
            "evidence": [],
            "overall_result": "NOT_RUN",
            "created_at": created,
            "updated_at": created,
        }
        self._save(directory, session)
        return session

    def get_session(self, session_id: str) -> dict[str, Any]:
        return self._load(session_id)[1]

    def mark_visual_ux_ready(self, session_id: str, acknowledgement: str) -> dict[str, Any]:
        if not acknowledgement.strip():
            raise QaEvidenceError("developer acknowledgement is required")
        directory, session = self._load(session_id)
        if session["stage"] != "PREPARING_VISUAL_UX":
            raise QaEvidenceError("visual and UX readiness can only be confirmed once")
        session["visual_ux_placement"] = {
            "status": "COMPLETE_FOR_PC_REVIEW",
            "developer_acknowledgement": acknowledgement.strip(),
        }
        session["stage"] = "READY_FOR_DEVELOPER_PC_REVIEW"
        self._save(directory, session)
        return session

    def record_result(
        self, session_id: str, item_id: str, status: ReviewStatus, note: str
    ) -> dict[str, Any]:
        directory, session = self._load(session_id)
        if session["visual_ux_placement"]["status"] != "COMPLETE_FOR_PC_REVIEW":
            raise QaEvidenceError("image and UX placement must be complete before actual review")
        if session["stage"] == "DEVELOPER_PC_REVIEW_COMPLETE":
            raise QaEvidenceError("completed QA session is immutable")
        if status not in {"PASS", "FAIL", "BLOCKED", "NOT_RUN"}:
            raise QaEvidenceError("review status is invalid")
        target = next((item for item in session["checklist"] if item["item_id"] == item_id), None)
        if target is None:
            raise QaEvidenceError("checklist item was not found")
        target["status"] = status
        target["note"] = note.strip()
        session["stage"] = "DEVELOPER_PC_REVIEW_IN_PROGRESS"
        self._save(directory, session)
        return session

    def add_image_evidence(
        self, session_id: str, original_filename: str, content_type: str, data: bytes
    ) -> dict[str, Any]:
        if len(data) > _MAX_IMAGE_BYTES:
            raise QaEvidenceError("image evidence must be 25 MiB or smaller")
        if content_type not in _IMAGE_TYPES or not _is_expected_image(content_type, data):
            raise QaEvidenceError("evidence must be a valid PNG, JPEG, or WebP image")
        directory, session = self._load(session_id)
        if session["stage"] == "DEVELOPER_PC_REVIEW_COMPLETE":
            raise QaEvidenceError("completed QA session is immutable")
        digest = hashlib.sha256(data).hexdigest()
        filename = f"evidence-{len(session['evidence']) + 1:03d}{_IMAGE_TYPES[content_type]}"
        try:
            path = atomic_write_bytes(directory / "evidence", filename, data)
        except QaPathError as error:
            raise QaEvidenceError(str(error)) from error
        record = {
            "evidence_id": f"image-{len(session['evidence']) + 1:03d}",
            "kind": "IMAGE",
            "original_filename": Path(original_filename).name,
            "stored_path": f"evidence/{filename}",
            "content_type": content_type,
            "bytes": len(data),
            "sha256": digest,
        }
        session["evidence"].append(record)
        self._save(directory, session)
        return record

    def finalize(self, session_id: str) -> dict[str, Any]:
        directory, session = self._load(session_id)
        if session["visual_ux_placement"]["status"] != "COMPLETE_FOR_PC_REVIEW":
            raise QaEvidenceError("image and UX placement is not ready")
        required = [item for item in session["checklist"] if item["required"]]
        if any(item["status"] == "NOT_RUN" for item in required):
            raise QaEvidenceError("every required checklist item must have an actual result")
        if not session["evidence"]:
            raise QaEvidenceError("at least one image evidence file is required")
        statuses = {item["status"] for item in required}
        overall = "FAIL" if "FAIL" in statuses else "BLOCKED" if "BLOCKED" in statuses else "PASS"
        session["overall_result"] = overall
        session["platforms"]["pc"]["status"] = overall
        session["stage"] = "DEVELOPER_PC_REVIEW_COMPLETE"
        self._save(directory, session)
        packet = {key: value for key, value in session.items() if key != "packet_path"}
        try:
            packet_path = atomic_write_bytes(
                directory,
                "QA_EVIDENCE_PACKET.json",
                (json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(),
            )
        except QaPathError as error:
            raise QaEvidenceError(str(error)) from error
        return {**session, "packet_path": str(packet_path)}
