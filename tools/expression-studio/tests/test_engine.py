import base64
import hashlib
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
import traceback

import pytest

from PIL import Image

from expression_studio.catalog import resolve_expression
from expression_studio.engine import (
    EngineContractError,
    FakeExpressionEngine,
    IDENTITY_PREFIX,
    OpenAIExpressionEngine,
    trusted_engine_policy,
)
from expression_studio.models import ExpressionRequest
from tests.test_models import valid_payload


def wink_request() -> ExpressionRequest:
    return ExpressionRequest.model_validate(valid_payload(candidate_count=2))


def test_fake_engine_creates_the_requested_number_of_valid_candidate_pngs(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    anchor = project_root / "art" / "source" / "hero.png"
    anchor.parent.mkdir(parents=True)
    Image.new("RGBA", (9, 7), (255, 255, 255, 255)).save(anchor)
    request = wink_request()

    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    result = FakeExpressionEngine(project_root).generate(request, resolve_expression(request), candidates_dir)

    assert [candidate.name for candidate in result.candidates] == ["candidate-000.png", "candidate-001.png"]
    assert all(candidate.is_file() for candidate in result.candidates)
    assert all(Image.open(candidate).size == (9, 7) for candidate in result.candidates)


def test_fake_engine_keeps_the_anchor_bytes_unchanged_and_resolves_identity_prompt(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    anchor = project_root / "art" / "source" / "hero.png"
    anchor.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (10, 20, 30, 255)).save(anchor)
    initial_hash = hashlib.sha256(anchor.read_bytes()).hexdigest()
    request = wink_request()

    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    result = FakeExpressionEngine(project_root).generate(request, resolve_expression(request), candidates_dir)

    assert hashlib.sha256(anchor.read_bytes()).hexdigest() == initial_hash
    assert IDENTITY_PREFIX in result.generation_instruction
    assert "wink the left eye" in result.generation_instruction
    assert "moderate intensity" in result.generation_instruction


def _png_bytes(color: tuple[int, int, int, int]) -> bytes:
    encoded = BytesIO()
    Image.new("RGBA", (8, 8), color).save(encoded, format="PNG")
    return encoded.getvalue()


def _write_hashed_anchor(tmp_path: Path, data: bytes) -> Path:
    anchor = tmp_path / f"approved-anchor-{hashlib.sha256(data).hexdigest()}.png"
    anchor.write_bytes(data)
    return anchor


class _RecordingImages:
    def __init__(self, outputs: list[bytes] | None = None, error: Exception | None = None) -> None:
        self.outputs = outputs or []
        self.error = error
        self.calls: list[dict[str, object]] = []

    def edit(self, **kwargs: object) -> SimpleNamespace:
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return SimpleNamespace(
            data=[SimpleNamespace(b64_json=base64.b64encode(output).decode("ascii")) for output in self.outputs]
        )


class _RecordingClient:
    def __init__(self, images: _RecordingImages) -> None:
        self.images = images


def test_openai_engine_edits_the_run_local_anchor_with_the_reviewed_snapshot(tmp_path: Path) -> None:
    anchor = _write_hashed_anchor(tmp_path, _png_bytes((10, 20, 30, 255)))
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    images = _RecordingImages([_png_bytes((20, 30, 40, 255)), _png_bytes((30, 40, 50, 255))])
    request = wink_request().model_copy(
        update={"anchor": wink_request().anchor.model_copy(update={"source_path": str(anchor)})}
    )

    result = OpenAIExpressionEngine(client=_RecordingClient(images)).generate(
        request,
        resolve_expression(request),
        candidates_dir,
    )

    assert [path.name for path in result.candidates] == ["candidate-000.png", "candidate-001.png"]
    assert [path.read_bytes() for path in result.candidates] == images.outputs
    assert result.provenance == "unverified"
    assert result.delivery_eligible is False
    assert len(images.calls) == 1
    call = images.calls[0]
    assert call["model"] == "gpt-image-2-2026-04-21"
    assert call["n"] == 2
    assert call["output_format"] == "png"
    assert call["quality"] == "medium"
    assert call["size"] == "auto"
    assert "input_fidelity" not in call
    assert "wink the left eye" in str(call["prompt"])


def test_openai_engine_rejects_malformed_response_before_writing_any_candidate(tmp_path: Path) -> None:
    anchor = _write_hashed_anchor(tmp_path, _png_bytes((10, 20, 30, 255)))
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    images = _RecordingImages([_png_bytes((20, 30, 40, 255))])
    request = wink_request().model_copy(
        update={"anchor": wink_request().anchor.model_copy(update={"source_path": str(anchor)})}
    )

    with pytest.raises(EngineContractError, match="wrong image count") as caught:
        OpenAIExpressionEngine(client=_RecordingClient(images)).generate(
            request,
            resolve_expression(request),
            candidates_dir,
        )

    assert list(candidates_dir.iterdir()) == []
    assert caught.value.provider_call_made is True


def test_openai_engine_rejects_oversized_provider_output_before_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    anchor = _write_hashed_anchor(tmp_path, _png_bytes((10, 20, 30, 255)))
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    monkeypatch.setattr("expression_studio.engine.MAX_OPENAI_IMAGE_BYTES", 16)
    images = _RecordingImages([_png_bytes((20, 30, 40, 255)), _png_bytes((30, 40, 50, 255))])
    request = wink_request().model_copy(
        update={"anchor": wink_request().anchor.model_copy(update={"source_path": str(anchor)})}
    )

    with pytest.raises(EngineContractError, match="size limit") as caught:
        OpenAIExpressionEngine(client=_RecordingClient(images)).generate(
            request,
            resolve_expression(request),
            candidates_dir,
        )

    assert list(candidates_dir.iterdir()) == []
    assert caught.value.provider_call_made is True


def test_openai_engine_sanitizes_provider_errors(tmp_path: Path) -> None:
    anchor = _write_hashed_anchor(tmp_path, _png_bytes((10, 20, 30, 255)))
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    images = _RecordingImages(error=RuntimeError("sk-secret must never be shown"))
    request = wink_request().model_copy(
        update={"anchor": wink_request().anchor.model_copy(update={"source_path": str(anchor)})}
    )

    engine = OpenAIExpressionEngine(client=_RecordingClient(images))
    with pytest.raises(EngineContractError) as caught:
        engine.generate(
            request,
            resolve_expression(request),
            candidates_dir,
        )

    assert "sk-secret" not in str(caught.value)
    assert caught.value.__cause__ is None
    assert caught.value.__context__ is None
    rendered = "".join(traceback.format_exception(caught.type, caught.value, caught.tb))
    assert "sk-secret" not in rendered
    assert list(candidates_dir.iterdir()) == []
    assert caught.value.provider_call_made is True


def test_openai_engine_preserves_only_a_safe_provider_error_code(tmp_path: Path) -> None:
    class QuotaError(RuntimeError):
        code = "credit_balance_exhausted"

    anchor = _write_hashed_anchor(tmp_path, _png_bytes((10, 20, 30, 255)))
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    images = _RecordingImages(error=QuotaError("sk-secret and account details"))
    request = wink_request().model_copy(
        update={"anchor": wink_request().anchor.model_copy(update={"source_path": str(anchor)})}
    )

    with pytest.raises(EngineContractError) as caught:
        OpenAIExpressionEngine(client=_RecordingClient(images)).generate(
            request,
            resolve_expression(request),
            candidates_dir,
        )

    assert "code=credit_balance_exhausted" in str(caught.value)
    assert "sk-secret" not in str(caught.value)


def test_openai_engine_has_service_owned_delivery_policy(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    engine = OpenAIExpressionEngine()
    policy = trusted_engine_policy(engine)

    assert policy.adapter_id == "expression.openai-images-edit.v1"
    assert policy.provenance == "openai"
    assert policy.delivery_eligible is True
    assert str(engine._client.base_url).rstrip("/") == "https://api.openai.com/v1"

    class UnreviewedSubclass(OpenAIExpressionEngine):
        pass

    unreviewed = trusted_engine_policy(UnreviewedSubclass())
    assert unreviewed.provenance == "unverified"
    assert unreviewed.delivery_eligible is False


def test_openai_engine_ignores_environment_endpoint_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://attacker.invalid/v1")

    engine = OpenAIExpressionEngine()

    assert str(engine._client.base_url).rstrip("/") == "https://api.openai.com/v1"
    assert engine.policy_config()["base_url"] == "https://api.openai.com/v1"


def test_openai_engine_policy_fails_closed_after_runtime_endpoint_mutation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    engine = OpenAIExpressionEngine()
    engine._client.base_url = "https://attacker.invalid/v1"

    policy = trusted_engine_policy(engine)

    assert policy.provenance == "unverified"
    assert policy.delivery_eligible is False


def test_openai_engine_policy_fails_closed_after_runtime_model_mutation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    engine = OpenAIExpressionEngine()
    engine.model = "gpt-image-2"

    policy = trusted_engine_policy(engine)

    assert policy.provenance == "unverified"
    assert policy.delivery_eligible is False


def test_openai_engine_rejects_oversized_base64_before_decoding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    anchor = _write_hashed_anchor(tmp_path, _png_bytes((10, 20, 30, 255)))
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    monkeypatch.setattr("expression_studio.engine.MAX_OPENAI_IMAGE_BYTES", 16)
    images = _RecordingImages()
    images.outputs = [b"x" * 20, b"y" * 20]
    request = wink_request().model_copy(
        update={"anchor": wink_request().anchor.model_copy(update={"source_path": str(anchor)})}
    )

    with pytest.raises(EngineContractError, match="size limit"):
        OpenAIExpressionEngine(client=_RecordingClient(images)).generate(
            request,
            resolve_expression(request),
            candidates_dir,
        )

    assert list(candidates_dir.iterdir()) == []


def test_openai_engine_never_follows_a_swapped_anchor_symlink(tmp_path: Path) -> None:
    expected = _png_bytes((10, 20, 30, 255))
    secret = tmp_path / "secret.png"
    secret.write_bytes(_png_bytes((200, 10, 10, 255)))
    anchor = tmp_path / f"approved-anchor-{hashlib.sha256(expected).hexdigest()}.png"
    anchor.symlink_to(secret)
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    images = _RecordingImages([_png_bytes((20, 30, 40, 255)), _png_bytes((30, 40, 50, 255))])
    request = wink_request().model_copy(
        update={"anchor": wink_request().anchor.model_copy(update={"source_path": str(anchor)})}
    )

    with pytest.raises(EngineContractError, match="unavailable or changed"):
        OpenAIExpressionEngine(client=_RecordingClient(images)).generate(
            request,
            resolve_expression(request),
            candidates_dir,
        )

    assert images.calls == []


def test_injected_openai_client_is_never_delivery_eligible() -> None:
    engine = OpenAIExpressionEngine(client=_RecordingClient(_RecordingImages()))

    policy = trusted_engine_policy(engine)

    assert policy.provenance == "unverified"
    assert policy.delivery_eligible is False


@pytest.mark.parametrize(
    "overrides",
    [
        {"model": "gpt-image-2"},
        {"quality": "high"},
        {"size": "1024x1536"},
    ],
)
def test_openai_engine_rejects_unreviewed_provider_configuration(overrides: dict[str, str]) -> None:
    with pytest.raises(EngineContractError, match="reviewed production configuration"):
        OpenAIExpressionEngine(client=_RecordingClient(_RecordingImages()), **overrides)
