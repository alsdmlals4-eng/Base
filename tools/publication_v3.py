from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator
from PIL import Image, ImageChops
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, ByteStringObject


SCHEMA_VERSION = 3
ACTIVE_STATUSES = {"ACTIVE", "CURRENT", "SUPPORT"}


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return data


def validate_json(data: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = load_json(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda item: list(item.path))
    if errors:
        messages = []
        for error in errors:
            location = ".".join(str(part) for part in error.path) or "<root>"
            messages.append(f"{label} {location}: {error.message}")
        raise ValueError("Schema validation failed:\n- " + "\n- ".join(messages))


def require_schema_v3(data: dict[str, Any], label: str) -> None:
    version = data.get("schema_version")
    if version != SCHEMA_VERSION:
        raise ValueError(
            f"{label} uses schema_version={version!r}; schema v3 is required. "
            "Follow docs/migrations/v2.2.0-to-v3.0.0.md."
        )


def resolve(base: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path).resolve()


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def combined_digest(items: Iterable[tuple[str, str]]) -> str:
    hasher = hashlib.sha256()
    for label, value in sorted(items):
        hasher.update(label.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(value.encode("ascii"))
        hasher.update(b"\0")
    return hasher.hexdigest()


def source_epoch(source_commit: str = "") -> int:
    configured = os.environ.get("SOURCE_DATE_EPOCH", "").strip()
    if configured:
        return int(configured)
    if source_commit:
        result = subprocess.run(
            ["git", "show", "-s", "--format=%ct", source_commit],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip().isdigit():
            return int(result.stdout.strip())
    return 0


def stable_timestamp(epoch: int) -> str:
    return datetime.fromtimestamp(max(epoch, 0), timezone.utc).replace(microsecond=0).isoformat()


def find_executable(env_name: str, names: Iterable[str], known_paths: Iterable[str] = ()) -> str | None:
    configured = os.environ.get(env_name, "").strip()
    candidates = [configured] if configured else []
    candidates.extend(filter(None, (shutil.which(name) for name in names)))
    candidates.extend(known_paths)
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(Path(candidate).resolve())
    return None


def libreoffice_path() -> str | None:
    return find_executable(
        "BASE_LIBREOFFICE",
        ("libreoffice", "soffice"),
        (
            "C:/Program Files/LibreOffice/program/soffice.exe",
            "C:/Program Files (x86)/LibreOffice/program/soffice.exe",
        ),
    )


def pdftoppm_path() -> str | None:
    return find_executable("BASE_PDFTOPPM", ("pdftoppm",))


def mermaid_cli_path(repository_root: Path) -> str | None:
    suffix = ".cmd" if os.name == "nt" else ""
    return find_executable(
        "BASE_MERMAID_CLI",
        ("mmdc",),
        (str(repository_root / "node_modules" / ".bin" / f"mmdc{suffix}"),),
    )


def chrome_path() -> str | None:
    return find_executable(
        "PUPPETEER_EXECUTABLE_PATH",
        ("google-chrome", "chromium", "chromium-browser"),
        (
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        ),
    )


def font_paths() -> tuple[str | None, str | None]:
    regular = find_executable(
        "BASE_FONT_REGULAR",
        (),
        (
            "C:/Windows/Fonts/malgun.ttf",
            "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
            "/usr/share/opentype/noto/NotoSansCJK-Regular.ttc",
        ),
    )
    bold = find_executable(
        "BASE_FONT_BOLD",
        (),
        (
            "C:/Windows/Fonts/malgunbd.ttf",
            "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
            "/usr/share/opentype/noto/NotoSansCJK-Bold.ttc",
        ),
    )
    return regular, bold


def normalize_docx(path: Path, epoch: int) -> None:
    del epoch  # ZIP cannot represent dates before 1980; use a stable fixed value.
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False, dir=path.parent) as stream:
        temporary = Path(stream.name)
    try:
        with zipfile.ZipFile(path, "r") as source, zipfile.ZipFile(
            temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
        ) as target:
            for name in sorted(source.namelist()):
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o600 << 16
                info.create_system = 0
                target.writestr(info, source.read(name))
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def normalize_pdf(path: Path, epoch: int, identity_hash: str) -> None:
    reader = PdfReader(str(path))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    timestamp = datetime.fromtimestamp(max(epoch, 0), timezone.utc).strftime("D:%Y%m%d%H%M%S+00'00'")
    writer.add_metadata(
        {
            "/Producer": "Base schema v3 deterministic publisher",
            "/Creator": "Base schema v3",
            "/CreationDate": timestamp,
            "/ModDate": timestamp,
        }
    )
    identifier = bytes.fromhex(identity_hash[:32])
    writer._ID = ArrayObject([ByteStringObject(identifier), ByteStringObject(identifier)])
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=path.parent) as stream:
        temporary = Path(stream.name)
        writer.write(stream)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def render_pdf_for_review(pdf_path: Path, output_dir: Path) -> list[Path]:
    executable = pdftoppm_path()
    if not executable:
        raise RuntimeError("pdftoppm is required; install Poppler or set BASE_PDFTOPPM.")
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = output_dir / "page"
    result = subprocess.run(
        [executable, "-png", "-r", "120", str(pdf_path), str(prefix)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    pages = sorted(output_dir.glob("page-*.png"))
    if not pages:
        raise RuntimeError("PDF render review produced no pages.")
    for page in pages:
        with Image.open(page).convert("RGB") as image:
            if image.width < 500 or image.height < 500:
                raise RuntimeError(f"Rendered page is unexpectedly small: {page}")
            white = Image.new("RGB", image.size, "white")
            if ImageChops.difference(image, white).getbbox() is None:
                raise RuntimeError(f"Rendered page is blank: {page}")
    return pages


def atomic_replace(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    os.replace(source, destination)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
