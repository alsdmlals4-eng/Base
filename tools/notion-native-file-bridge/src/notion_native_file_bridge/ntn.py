from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import shutil
import subprocess
from typing import Callable


NOTION_VERSION = "2026-03-11"


class BridgeError(RuntimeError):
    def __init__(self, code: str, detail: str = "") -> None:
        self.code = code
        self.detail = detail
        message = code if not detail else f"{code}: {detail}"
        super().__init__(message)


@dataclass(frozen=True)
class UploadReceipt:
    status: str
    operation: str
    upload_id: str
    filename: str
    content_type: str
    content_length: int
    source_sha256: str
    notion_status: str


Runner = Callable[..., subprocess.CompletedProcess[bytes]]


class NtnClient:
    def __init__(self, executable: str | None = None, runner: Runner = subprocess.run) -> None:
        if executable is None:
            executable = shutil.which("ntn")
            if not executable:
                raise BridgeError("NTN_UNAVAILABLE", "official Notion CLI 'ntn' was not found on PATH")
        self.executable = executable
        self.runner = runner

    @staticmethod
    def _redact(value: str) -> str:
        token = os.environ.get("NOTION_API_TOKEN")
        if token:
            value = value.replace(token, "<REDACTED>")
        return value

    def _run(self, argv: list[str], *, input_bytes: bytes | None = None) -> str:
        command = [self.executable, *argv]
        result = self.runner(
            command,
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        stdout = self._redact((result.stdout or b"").decode("utf-8", errors="replace"))
        stderr = self._redact((result.stderr or b"").decode("utf-8", errors="replace"))
        if result.returncode != 0:
            detail = stderr.strip() or stdout.strip() or f"exit={result.returncode}"
            raise BridgeError("NTN_COMMAND_FAILED", detail)
        return stdout

    def _json(self, argv: list[str]) -> dict[str, object]:
        raw = self._run(argv).strip()
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise BridgeError("INVALID_NTN_JSON", self._redact(raw[:500])) from exc
        if not isinstance(value, dict):
            raise BridgeError("INVALID_NTN_JSON", "expected a JSON object")
        return value

    def preflight(self) -> dict[str, object]:
        version = self._run(["--version"]).strip()
        probe = self._json(["api", "v1/users/me", "--notion-version", NOTION_VERSION])
        if not probe.get("id"):
            raise BridgeError("AUTH_READBACK_FAILED", "v1/users/me did not return a user id")
        return {
            "status": "PASS",
            "operation": "preflight",
            "api_version": NOTION_VERSION,
            "ntn_version": version,
        }

    def upload(self, path: Path) -> UploadReceipt:
        source = Path(path).expanduser()
        if not source.is_file():
            raise BridgeError("FILE_NOT_FOUND", str(source))
        content_type, _ = mimetypes.guess_type(source.name)
        if not content_type:
            raise BridgeError("UNSUPPORTED_CONTENT_TYPE", source.name)
        payload = source.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        output = self._run(
            [
                "files",
                "create",
                "--plain",
                "--filename",
                source.name,
                "--content-type",
                content_type,
            ],
            input_bytes=payload,
        ).strip()
        first_line = output.splitlines()[0] if output else ""
        upload_id = first_line.split("\t", 1)[0].strip()
        if not upload_id:
            raise BridgeError("UPLOAD_ID_MISSING", "ntn files create --plain returned no upload id")
        readback = self._json(["files", "get", upload_id, "--json"])
        if readback.get("id") != upload_id or readback.get("status") != "uploaded":
            raise BridgeError(
                "UPLOAD_READBACK_MISMATCH",
                f"expected id={upload_id} status=uploaded; got id={readback.get('id')} status={readback.get('status')}",
            )
        return UploadReceipt(
            status="PASS",
            operation="upload",
            upload_id=upload_id,
            filename=source.name,
            content_type=content_type,
            content_length=len(payload),
            source_sha256=digest,
            notion_status="uploaded",
        )

    def append_image(self, page_id: str, upload_id: str) -> dict[str, object]:
        response = self._json(
            [
                "api",
                f"v1/blocks/{page_id}/children",
                "-X",
                "PATCH",
                "children[0][type]=image",
                "children[0][image][type]=file_upload",
                f"children[0][image][file_upload][id]={upload_id}",
                "--notion-version",
                NOTION_VERSION,
            ]
        )
        results = response.get("results")
        if not isinstance(results, list) or not results or not isinstance(results[0], dict):
            raise BridgeError("DESTINATION_READBACK_FAILED", "append response did not include a created block")
        block_id = results[0].get("id")
        if not isinstance(block_id, str) or not block_id:
            raise BridgeError("DESTINATION_READBACK_FAILED", "created image block id missing")
        try:
            block = self._json(["api", f"v1/blocks/{block_id}", "--notion-version", NOTION_VERSION])
        except BridgeError as exc:
            raise BridgeError(
                "AMBIGUOUS_DESTINATION_STATE",
                f"append returned block_id={block_id}, but readback failed; inspect the destination before retrying to avoid a duplicate image block ({exc.code})",
            ) from exc
        if block.get("id") != block_id or block.get("type") != "image":
            raise BridgeError("DESTINATION_READBACK_FAILED", "created block did not read back as image")
        return {
            "status": "PASS",
            "operation": "append-image",
            "page_id": page_id,
            "upload_id": upload_id,
            "block_id": block_id,
        }

    def set_cover(self, page_id: str, upload_id: str) -> dict[str, object]:
        self._json(
            [
                "api",
                f"v1/pages/{page_id}",
                "-X",
                "PATCH",
                "cover[type]=file_upload",
                f"cover[file_upload][id]={upload_id}",
                "--notion-version",
                NOTION_VERSION,
            ]
        )
        page = self._json(["api", f"v1/pages/{page_id}", "--notion-version", NOTION_VERSION])
        cover = page.get("cover")
        if not isinstance(cover, dict) or cover.get("type") != "file":
            raise BridgeError("DESTINATION_READBACK_FAILED", "page cover did not read back as a Notion-hosted file")
        return {
            "status": "PASS",
            "operation": "set-cover",
            "page_id": page_id,
            "upload_id": upload_id,
        }

    def set_files_property(
        self,
        page_id: str,
        property_name: str,
        upload_id: str,
        filename: str,
    ) -> dict[str, object]:
        prefix = f"properties[{property_name}][files][0]"
        self._json(
            [
                "api",
                f"v1/pages/{page_id}",
                "-X",
                "PATCH",
                f"{prefix}[type]=file_upload",
                f"{prefix}[file_upload][id]={upload_id}",
                f"{prefix}[name]={filename}",
                "--notion-version",
                NOTION_VERSION,
            ]
        )
        page = self._json(["api", f"v1/pages/{page_id}", "--notion-version", NOTION_VERSION])
        properties = page.get("properties")
        prop = properties.get(property_name) if isinstance(properties, dict) else None
        files = prop.get("files") if isinstance(prop, dict) else None
        if not isinstance(files, list) or not files:
            raise BridgeError("DESTINATION_READBACK_FAILED", f"Files property '{property_name}' is empty after update")
        return {
            "status": "PASS",
            "operation": "set-files-property",
            "page_id": page_id,
            "property": property_name,
            "upload_id": upload_id,
            "filename": filename,
        }
