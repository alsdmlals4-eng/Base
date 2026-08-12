import hashlib
from pathlib import Path

from PIL import Image

from expression_studio.catalog import resolve_expression
from expression_studio.engine import FakeExpressionEngine, IDENTITY_PREFIX
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

    result = FakeExpressionEngine(project_root).generate(request, resolve_expression(request), tmp_path / "run")

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

    result = FakeExpressionEngine(project_root).generate(request, resolve_expression(request), tmp_path / "run")

    assert hashlib.sha256(anchor.read_bytes()).hexdigest() == initial_hash
    assert IDENTITY_PREFIX in result.generation_instruction
    assert "wink the left eye" in result.generation_instruction
    assert "moderate intensity" in result.generation_instruction
