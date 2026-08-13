"""Local candidate-engine protocol and deterministic test implementation."""

import base64
import binascii
from dataclasses import dataclass
import hashlib
from io import BytesIO
import json
import os
from pathlib import Path
import re
from typing import Protocol

from PIL import Image, UnidentifiedImageError
from base_tool_contracts import safe_staging_write_bytes, staging_read_bytes

from .catalog import ResolvedExpression
from .models import ExpressionRequest


IDENTITY_PREFIX = (
    "Preserve the exact same character: face geometry, hairstyle, costume, palette, framing, lighting, "
    "and art style. Edit only the requested facial expression, gaze, and head pose."
)

SAFE_PROVIDER_ERROR_CODES = frozenset(
    {
        "insufficient_quota",
        "credit_balance_exhausted",
        "rate_limit_exceeded",
        "model_not_found",
        "invalid_api_key",
        "permission_denied",
    }
)
SAFE_PROVIDER_EXCEPTION_NAMES = frozenset(
    {
        "APIConnectionError",
        "APITimeoutError",
        "AuthenticationError",
        "BadRequestError",
        "ConflictError",
        "InternalServerError",
        "NotFoundError",
        "PermissionDeniedError",
        "RateLimitError",
        "UnprocessableEntityError",
    }
)
REVIEWED_OPENAI_MODEL = "gpt-image-2-2026-04-21"
REVIEWED_OPENAI_QUALITY = "medium"
REVIEWED_OPENAI_SIZE = "auto"
REVIEWED_OPENAI_BASE_URL = "https://api.openai.com/v1"
MAX_OPENAI_IMAGE_BYTES = 20 * 1024 * 1024
MAX_OPENAI_IMAGE_DIMENSION = 4096
INTENSITY_PHRASES = {
    "A": "very subtle intensity",
    "B": "subtle intensity",
    "C": "moderate intensity",
    "D": "strong intensity",
    "E": "maximum readable intensity",
}


class EngineContractError(RuntimeError):
    """Raised when a local engine cannot satisfy the reviewed request contract."""

    def __init__(self, message: str, *, provider_call_made: bool = False) -> None:
        super().__init__(message)
        self.provider_call_made = provider_call_made


@dataclass(frozen=True)
class EngineResult:
    candidates: list[Path]
    generation_instruction: str
    provenance: str = "unverified"
    delivery_eligible: bool = False
    provider_call_made: bool = False


@dataclass(frozen=True)
class EnginePolicy:
    adapter_id: str
    provenance: str
    delivery_eligible: bool
    config_sha256: str


class ExpressionEngine(Protocol):
    provenance: str
    delivery_eligible: bool

    def generate(self, request: ExpressionRequest, resolved: ResolvedExpression, candidates_dir: Path) -> EngineResult:
        """Generate local candidate PNGs without mutating the approved anchor."""


def generation_instruction(resolved: ResolvedExpression) -> str:
    movements = "; ".join(resolved.movement_phrases) or "keep a neutral facial expression"
    intensities = ", ".join(f"{control.code}: {INTENSITY_PHRASES[control.intensity]}" for control in resolved.controls) or "neutral intensity"
    return " ".join(
        (
            IDENTITY_PREFIX,
            f"Facial movement: {movements} ({intensities}).",
            f"Gaze: {resolved.gaze_phrase}.",
            f"Head pose: {resolved.head_pose_phrase}.",
        )
    )


class FakeExpressionEngine:
    """Copies an anchor into valid candidates for local lifecycle testing only."""

    provenance = "simulated"
    delivery_eligible = False

    def __init__(self, project_root: Path) -> None:
        self._project_root = project_root.resolve()

    def generate(self, request: ExpressionRequest, resolved: ResolvedExpression, candidates_dir: Path) -> EngineResult:
        anchor_reference = self._project_root / request.anchor.source_path
        anchor = anchor_reference.resolve()
        if self._project_root not in anchor.parents or not anchor.is_file():
            raise EngineContractError("approved anchor source_path must point to an existing project image")
        try:
            with Image.open(anchor_reference) as source:
                source_rgba = source.convert("RGBA")
        except (OSError, UnidentifiedImageError) as error:
            raise EngineContractError("approved anchor source_path must be a readable image") from error

        candidates: list[Path] = []
        for index in range(request.candidate_count):
            encoded = BytesIO()
            source_rgba.save(encoded, format="PNG")
            candidate = safe_staging_write_bytes(candidates_dir, f"candidate-{index:03d}.png", encoded.getvalue())
            candidates.append(candidate)
        return EngineResult(
            candidates=candidates,
            generation_instruction=generation_instruction(resolved),
            provenance="simulated",
            delivery_eligible=False,
        )


class OpenAIExpressionEngine:
    """Reviewed OpenAI Images edit adapter for real expression candidates."""

    provenance = "openai"
    delivery_eligible = True

    def __init__(
        self,
        *,
        client: object | None = None,
        model: str = REVIEWED_OPENAI_MODEL,
        quality: str = REVIEWED_OPENAI_QUALITY,
        size: str = REVIEWED_OPENAI_SIZE,
    ) -> None:
        if (model, quality, size) != (
            REVIEWED_OPENAI_MODEL,
            REVIEWED_OPENAI_QUALITY,
            REVIEWED_OPENAI_SIZE,
        ):
            raise EngineContractError("OpenAI engine requires the reviewed production configuration")
        self._production_client_expected = client is None
        if client is None:
            if not os.environ.get("OPENAI_API_KEY"):
                raise EngineContractError("OPENAI_API_KEY is required for the OpenAI production engine")
            try:
                from openai import OpenAI
            except ImportError as error:
                raise EngineContractError("the OpenAI Python SDK is required for the production engine") from error
            client = OpenAI(base_url=REVIEWED_OPENAI_BASE_URL)
        self._client = client
        self.model = model
        self.quality = quality
        self.size = size
        self.output_format = "png"
        self.provenance = "openai" if self.production_client_verified else "unverified"
        self.delivery_eligible = self.production_client_verified

    @property
    def production_client_verified(self) -> bool:
        if not self._production_client_expected:
            return False
        try:
            from openai import OpenAI
        except ImportError:
            return False
        actual_base_url = str(getattr(self._client, "base_url", "")).rstrip("/")
        return (
            type(self._client) is OpenAI
            and actual_base_url == REVIEWED_OPENAI_BASE_URL
            and self.model == REVIEWED_OPENAI_MODEL
            and self.quality == REVIEWED_OPENAI_QUALITY
            and self.size == REVIEWED_OPENAI_SIZE
            and self.output_format == "png"
        )

    def policy_config(self) -> dict[str, str]:
        return {
            "model": self.model,
            "quality": self.quality,
            "size": self.size,
            "output_format": self.output_format,
            "base_url": REVIEWED_OPENAI_BASE_URL,
        }

    def generate(self, request: ExpressionRequest, resolved: ResolvedExpression, candidates_dir: Path) -> EngineResult:
        if self._production_client_expected and not self.production_client_verified:
            raise EngineContractError("OpenAI production client identity or endpoint changed after configuration")
        anchor = Path(request.anchor.source_path)
        anchor_match = re.fullmatch(r"approved-anchor-([0-9a-f]{64})(\.[A-Za-z0-9]+)", anchor.name)
        if anchor_match is None:
            raise EngineContractError("run-local approved anchor has no pinned SHA-256 identity")
        try:
            anchor_bytes = staging_read_bytes(
                anchor.parent,
                anchor.name,
                expected_sha256=anchor_match.group(1),
            )
        except ValueError as error:
            raise EngineContractError("run-local approved anchor is unavailable or changed") from error
        if not anchor_bytes:
            raise EngineContractError("run-local approved anchor is unavailable")
        instruction = generation_instruction(resolved)
        provider_failure: str | None = None
        response: object | None = None
        try:
            with BytesIO(anchor_bytes) as source:
                source.name = anchor.name
                response = self._client.images.edit(
                    model=self.model,
                    image=source,
                    prompt=instruction,
                    n=request.candidate_count,
                    output_format=self.output_format,
                    quality=self.quality,
                    size=self.size,
                )
        except Exception as error:
            provider_code = getattr(error, "code", None)
            exception_name = type(error).__name__
            safe_exception_name = (
                exception_name if exception_name in SAFE_PROVIDER_EXCEPTION_NAMES else "ProviderError"
            )
            code_suffix = (
                f", code={provider_code}"
                if isinstance(provider_code, str) and provider_code in SAFE_PROVIDER_ERROR_CODES
                else ""
            )
            provider_failure = (
                f"OpenAI image edit failed ({safe_exception_name}{code_suffix}); "
                "inspect provider billing, limits, model access, and connectivity"
            )
        if provider_failure is not None:
            raise EngineContractError(provider_failure, provider_call_made=True)

        data = getattr(response, "data", None)
        if not isinstance(data, list) or len(data) != request.candidate_count:
            raise EngineContractError("OpenAI image edit returned the wrong image count", provider_call_made=True)
        decoded: list[bytes] = []
        try:
            for item in data:
                encoded = getattr(item, "b64_json", None)
                if not isinstance(encoded, str) or not encoded:
                    raise ValueError("missing image bytes")
                maximum_encoded_length = ((MAX_OPENAI_IMAGE_BYTES + 2) // 3) * 4
                if len(encoded) > maximum_encoded_length:
                    raise ValueError("image size limit exceeded")
                image_bytes = base64.b64decode(encoded, validate=True)
                if len(image_bytes) > MAX_OPENAI_IMAGE_BYTES:
                    raise ValueError("image size limit exceeded")
                with Image.open(BytesIO(image_bytes)) as image:
                    if image.format != "PNG":
                        raise ValueError("wrong image format")
                    if image.width > MAX_OPENAI_IMAGE_DIMENSION or image.height > MAX_OPENAI_IMAGE_DIMENSION:
                        raise ValueError("image dimensions exceeded")
                    image.verify()
                decoded.append(image_bytes)
        except (ValueError, binascii.Error, OSError, UnidentifiedImageError) as error:
            message = "OpenAI image edit exceeded the reviewed size limit" if "exceed" in str(error) else "OpenAI image edit returned an unreadable PNG"
            raise EngineContractError(message, provider_call_made=True) from None

        candidates = [
            safe_staging_write_bytes(candidates_dir, f"candidate-{index:03d}.png", image_bytes)
            for index, image_bytes in enumerate(decoded)
        ]
        return EngineResult(
            candidates=candidates,
            generation_instruction=instruction,
            provenance=self.provenance,
            delivery_eligible=self.delivery_eligible,
            provider_call_made=True,
        )


def trusted_engine_policy(engine: ExpressionEngine) -> EnginePolicy:
    """Return service-owned policy; engine results cannot grant themselves eligibility."""
    if type(engine) is FakeExpressionEngine:
        adapter_id, provenance, eligible = "expression.fake.v1", "simulated", False
        engine_config: dict[str, str] = {}
    elif type(engine) is OpenAIExpressionEngine:
        if engine.production_client_verified:
            adapter_id, provenance, eligible = "expression.openai-images-edit.v1", "openai", True
        else:
            adapter_id, provenance, eligible = "expression.openai-images-edit.test-double.v1", "unverified", False
        engine_config = engine.policy_config()
    else:
        adapter_id, provenance, eligible = "expression.unverified", "unverified", False
        engine_config = {}
    encoded = json.dumps(
        {
            "adapter_id": adapter_id,
            "engine_class": f"{type(engine).__module__}.{type(engine).__qualname__}",
            "provenance": provenance,
            "delivery_eligible": eligible,
            "engine_config": engine_config,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return EnginePolicy(adapter_id, provenance, eligible, hashlib.sha256(encoded).hexdigest())
