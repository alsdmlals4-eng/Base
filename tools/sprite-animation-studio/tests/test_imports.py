from io import BytesIO

from fastapi import UploadFile
from PIL import Image
import pytest

from sprite_animation_studio.imports import MAX_IMPORT_BYTES, discard_import_bytes, read_upload_limited, validate_imported_image


def encoded_image(image_format: str, *, size: tuple[int, int] = (7, 5), color: tuple[int, ...] = (10, 20, 30, 128)) -> bytes:
    mode = "RGBA" if len(color) == 4 else "RGB"
    image = Image.new(mode, size, color)
    output = BytesIO()
    if image_format == "JPEG":
        image = image.convert("RGB")
    image.save(output, format=image_format)
    return output.getvalue()


@pytest.mark.parametrize(
    ("image_format", "expected_format", "has_alpha"),
    [("PNG", "PNG", True), ("JPEG", "JPEG", False), ("WEBP", "WEBP", True)],
)
def test_validate_imported_image_reports_hand_checked_metadata(image_format: str, expected_format: str, has_alpha: bool) -> None:
    result = validate_imported_image(
        encoded_image(image_format),
        declared_source="CHATGPT_INCLUDED",
        order=2,
    )

    assert result.detected_format == expected_format
    assert (result.width, result.height) == (7, 5)
    assert result.has_alpha is has_alpha
    assert result.declared_source == "CHATGPT_INCLUDED"
    assert result.order == 2
    assert len(result.sha256) == 64


def test_validate_imported_image_rejects_unknown_bytes() -> None:
    with pytest.raises(ValueError, match="PNG, JPEG, or WebP"):
        validate_imported_image(b"not an image", declared_source="LOCAL_GENERATOR", order=0)


def test_discard_import_bytes_keeps_only_durable_metadata() -> None:
    imported = validate_imported_image(encoded_image("PNG"), declared_source="LOCAL_GENERATOR", order=0)

    retained = discard_import_bytes(imported)

    assert retained.data == b""
    assert retained.sha256 == imported.sha256
    assert retained.detected_format == imported.detected_format


def test_validate_imported_image_rejects_dimensions_over_4096_before_pixel_processing() -> None:
    data = encoded_image("PNG", size=(4097, 1))

    with pytest.raises(ValueError, match="dimensions"):
        validate_imported_image(data, declared_source="FIGMA_INCLUDED", order=0)


@pytest.mark.anyio
async def test_read_upload_limited_rejects_byte_25_mib_plus_one() -> None:
    upload = UploadFile(filename="ignored.png", file=BytesIO(b"x" * (MAX_IMPORT_BYTES + 1)))

    with pytest.raises(ValueError, match="25 MiB"):
        await read_upload_limited(upload)
