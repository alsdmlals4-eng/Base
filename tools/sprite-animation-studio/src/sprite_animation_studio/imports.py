"""Bounded validation for user-supplied sprite frames."""

from dataclasses import asdict, dataclass, replace
import hashlib
from io import BytesIO
from typing import Literal

from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError


DeclaredSource = Literal[
    "CHATGPT_INCLUDED",
    "FIGMA_INCLUDED",
    "LOCAL_GENERATOR",
    "OTHER_USER_SUPPLIED",
]
MAX_IMPORT_BYTES = 25 * 1024 * 1024
MAX_IMPORT_DIMENSION = 4096
ALLOWED_IMPORT_FORMATS = {"PNG", "JPEG", "WEBP"}
DECLARED_SOURCES = {
    "CHATGPT_INCLUDED",
    "FIGMA_INCLUDED",
    "LOCAL_GENERATOR",
    "OTHER_USER_SUPPLIED",
}


@dataclass(frozen=True)
class ImportedImage:
    data: bytes
    sha256: str
    detected_format: str
    width: int
    height: int
    has_alpha: bool
    declared_source: DeclaredSource
    order: int


async def read_upload_limited(upload: UploadFile) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = await upload.read(min(1024 * 1024, MAX_IMPORT_BYTES + 1 - total))
        if not chunk:
            break
        total += len(chunk)
        if total > MAX_IMPORT_BYTES:
            raise ValueError("import image exceeds the 25 MiB safety limit")
        chunks.append(chunk)
    return b"".join(chunks)


def validate_imported_image(data: bytes, *, declared_source: DeclaredSource, order: int) -> ImportedImage:
    if declared_source not in DECLARED_SOURCES:
        raise ValueError("declared_source is not supported")
    if len(data) > MAX_IMPORT_BYTES:
        raise ValueError("import image exceeds the 25 MiB safety limit")
    try:
        with Image.open(BytesIO(data)) as probe:
            detected_format = probe.format
            width, height = probe.size
            has_alpha = "A" in probe.getbands() or "transparency" in probe.info
            if detected_format not in ALLOWED_IMPORT_FORMATS:
                raise ValueError("import must be a supported PNG, JPEG, or WebP image")
            if min(width, height) < 1 or max(width, height) > MAX_IMPORT_DIMENSION:
                raise ValueError("import image dimensions are outside the supported range")
            probe.verify()
        with Image.open(BytesIO(data)) as decoded:
            decoded.load()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
        raise ValueError("import must be a supported PNG, JPEG, or WebP image") from error
    return ImportedImage(
        data=data,
        sha256=hashlib.sha256(data).hexdigest(),
        detected_format=detected_format,
        width=width,
        height=height,
        has_alpha=has_alpha,
        declared_source=declared_source,
        order=order,
    )


def import_metadata(image: ImportedImage) -> dict[str, object]:
    metadata = asdict(image)
    metadata.pop("data")
    return metadata


def discard_import_bytes(image: ImportedImage) -> ImportedImage:
    """Return metadata-only provenance after the validated bytes have been staged."""
    return replace(image, data=b"")


def revalidate_imported_image(image: ImportedImage) -> ImportedImage:
    """Rebuild metadata from bytes so service callers cannot self-attest provenance."""
    validated = validate_imported_image(
        image.data,
        declared_source=image.declared_source,
        order=image.order,
    )
    if validated != image:
        raise ValueError("import frame metadata does not match validated bytes")
    return validated
