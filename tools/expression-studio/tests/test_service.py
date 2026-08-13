from pathlib import Path
from dataclasses import replace
from io import BytesIO
import json
import os
import subprocess

import pytest
from PIL import Image

from expression_studio.catalog import ExpressionConflictError
from expression_studio.delivery import ProjectFigmaRegistry
from expression_studio.engine import EngineContractError, EnginePolicy, EngineResult, FakeExpressionEngine, OpenAIExpressionEngine
from expression_studio.models import ExpressionRequest
from expression_studio.imports import validate_imported_image
from expression_studio.service import ExpressionStudioService, RunBlockedError, RunRecord
from tests.test_delivery import write_registry
from tests.test_models import valid_payload


def initialize_vault(project_root: Path) -> None:
    subprocess.run(["git", "init", "-q", str(project_root)], check=True)
    (project_root / ".asset-vault" / "library").mkdir(parents=True, exist_ok=True)
    (project_root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")


def _expression_png(color: tuple[int, int, int, int]) -> bytes:
    output = BytesIO()
    Image.new("RGBA", (8, 8), color).save(output, format="PNG")
    return output.getvalue()


def test_import_service_rejects_forged_candidate_metadata(tmp_path: Path) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source)
    initialize_vault(tmp_path)
    service = ExpressionStudioService(tmp_path, FakeExpressionEngine(tmp_path), project_id="demo")
    first = validate_imported_image(_expression_png((255, 0, 0, 255)), declared_source="LOCAL_GENERATOR", order=0)
    second = validate_imported_image(_expression_png((0, 0, 255, 255)), declared_source="LOCAL_GENERATOR", order=1)
    forged = replace(first, sha256="0" * 64, detected_format="JPEG", width=9, has_alpha=False)

    with pytest.raises(ValueError, match="metadata does not match validated bytes"):
        service.create_import_run(
            ExpressionRequest.model_validate(valid_payload()),
            (forged, second),
            "LOCAL_GENERATOR",
        )


def test_run_path_rejects_asset_symlink_and_gitignore_negation(tmp_path: Path) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source)
    initialize_vault(tmp_path)
    outside = tmp_path.parent / f"{tmp_path.name}-outside-expression"
    outside.mkdir()
    tool_root = tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio"
    tool_root.mkdir(parents=True)
    (tool_root / "hero").symlink_to(outside, target_is_directory=True)
    service = ExpressionStudioService(tmp_path, FakeExpressionEngine(tmp_path), project_id="demo", run_mode="simulated")

    with pytest.raises(ValueError, match="symlink|vault"):
        service.create_run(ExpressionRequest.model_validate(valid_payload()))
    assert list(outside.iterdir()) == []

    (tool_root / "hero").unlink()
    (tmp_path / ".gitignore").write_text(".asset-vault/\n!.asset-vault/\n", encoding="utf-8")
    with pytest.raises(ValueError, match="gitignored"):
        service.create_run(ExpressionRequest.model_validate(valid_payload()))


def service_for(project_root: Path, *, project_id: str | None = "demo") -> ExpressionStudioService:
    anchor = project_root / "art" / "source" / "hero.png"
    anchor.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(anchor)
    initialize_vault(project_root)
    return ExpressionStudioService(
        project_root,
        FakeExpressionEngine(project_root),
        registry=ProjectFigmaRegistry.load(write_registry(project_root)),
        project_id=project_id,
        run_mode="simulated",
    )


def test_service_rejects_run_mode_that_does_not_match_the_configured_engine(tmp_path: Path) -> None:
    initialize_vault(tmp_path)

    with pytest.raises(ValueError, match="run mode does not match"):
        ExpressionStudioService(tmp_path, FakeExpressionEngine(tmp_path), project_id="demo", run_mode="openai")


def test_service_defaults_to_subscription_handoff_import_mode(tmp_path: Path) -> None:
    service = ExpressionStudioService(tmp_path, FakeExpressionEngine(tmp_path), project_id="demo")

    assert service.config()["run_mode"] == "subscription_handoff_import"


def test_openai_engine_evidence_records_that_a_provider_call_was_made(tmp_path: Path) -> None:
    service = ExpressionStudioService(
        tmp_path,
        FakeExpressionEngine(tmp_path),
        project_id="demo",
        run_mode="simulated",
    )
    policy = EnginePolicy("expression.openai.test", "openai", True, "a" * 64)

    evidence = service._engine_evidence(policy=policy)

    assert evidence["provider_call_made"] is True


def test_blocked_openai_run_does_not_infer_a_provider_call_from_mode(tmp_path: Path) -> None:
    record = object.__new__(RunRecord)
    record.run_mode = "openai"
    record.provider_call_made = False
    record.imported_images = ()
    record.result = None
    record.status = "blocked"
    record.run_id = "blocked"
    record.selected_candidate = None
    record.warnings = ["blocked before provider"]
    record.lineage = Path("lineage.json")
    record.anchor_bytes = b"anchor"
    record.anchor_verification = "ANCHOR_UNVERIFIED"
    record.engine_policy = EnginePolicy("expression.openai.test", "openai", True, "a" * 64)
    record.request = ExpressionRequest.model_validate(valid_payload())
    record.resolved = __import__("expression_studio.catalog", fromlist=["resolve_expression"]).resolve_expression(record.request)

    assert record.public_view()["provider_call_made"] is False


def test_service_rejects_a_non_image_source_before_staging_or_engine_use(tmp_path: Path) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    source.write_text("OPENAI_API_KEY=must-not-leave-project", encoding="utf-8")
    initialize_vault(tmp_path)
    service = ExpressionStudioService(tmp_path, FakeExpressionEngine(tmp_path), project_id="demo", run_mode="simulated")

    with pytest.raises(ValueError, match="supported PNG, JPEG, or WebP image"):
        service.create_run(ExpressionRequest.model_validate(valid_payload()))

    assert not (tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio" / "hero").exists()


def test_service_rejects_a_source_symlink_before_reading_it(tmp_path: Path) -> None:
    secret = tmp_path / "art" / "secret.png"
    secret.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (1, 2, 3, 255)).save(secret)
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    source.symlink_to(secret)
    initialize_vault(tmp_path)
    service = ExpressionStudioService(tmp_path, FakeExpressionEngine(tmp_path), project_id="demo", run_mode="simulated")

    with pytest.raises(ValueError, match="regular file|link"):
        service.create_run(ExpressionRequest.model_validate(valid_payload()))


def test_openai_engine_requires_project_owned_anchor_evidence_before_generation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source)
    initialize_vault(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-key")
    service = ExpressionStudioService(tmp_path, OpenAIExpressionEngine(), project_id="demo", run_mode="openai")

    with pytest.raises(ValueError, match="project-owned approved-anchor evidence"):
        service.create_run(ExpressionRequest.model_validate(valid_payload()))


def generated_service_run(project_root: Path) -> tuple[ExpressionStudioService, str]:
    service = service_for(project_root)
    run = service.create_run(ExpressionRequest.model_validate(valid_payload()))
    return service, run.run_id


def test_delivery_is_blocked_until_a_candidate_is_explicitly_selected(tmp_path: Path) -> None:
    service, run_id = generated_service_run(tmp_path)

    with pytest.raises(RunBlockedError, match="selected candidate"):
        service.prepare_figma_delivery(run_id)


def test_simulated_run_cannot_export_or_prepare_figma_delivery(tmp_path: Path) -> None:
    service, run_id = generated_service_run(tmp_path)

    with pytest.raises(RunBlockedError, match="simulated"):
        service.export(run_id, selected_candidate=1)

    with pytest.raises(RunBlockedError, match="exported run"):
        service.prepare_figma_delivery(run_id)


def test_generated_run_updates_lineage_with_the_resolved_generation_instruction(tmp_path: Path) -> None:
    service, run_id = generated_service_run(tmp_path)

    record = service.get_run(run_id)
    lineage = json.loads(record.lineage.read_text(encoding="utf-8"))

    assert lineage["generation_instruction"] == record.result.generation_instruction
    assert lineage["selection"]["selected_candidate"] is None
    assert record.paths.run_dir.is_relative_to(
        tmp_path / ".asset-vault" / "library" / "generated" / "expression-studio"
    )


def test_fake_subclass_cannot_self_attest_delivery_eligibility(tmp_path: Path) -> None:
    class EligibleEngine(FakeExpressionEngine):
        def generate(self, request: ExpressionRequest, resolved: object, run_dir: Path) -> EngineResult:
            result = super().generate(request, resolved, run_dir)
            return EngineResult(
                candidates=result.candidates,
                generation_instruction=result.generation_instruction,
                provenance="openai",
                delivery_eligible=True,
            )

    anchor = tmp_path / "art" / "source" / "hero.png"
    anchor.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(anchor)
    initialize_vault(tmp_path)
    service = ExpressionStudioService(
        tmp_path,
        EligibleEngine(tmp_path),
        registry=ProjectFigmaRegistry.load(write_registry(tmp_path)),
        project_id="demo",
        run_mode="simulated",
    )
    record = service.create_run(ExpressionRequest.model_validate(valid_payload()))

    assert record.status == "blocked"
    assert record.result is None
    assert any("does not match" in warning for warning in record.warnings)
    with pytest.raises(RunBlockedError):
        service.export(record.run_id, selected_candidate=0)


def test_service_rejects_a_request_for_another_configured_project(tmp_path: Path) -> None:
    service = service_for(tmp_path)

    with pytest.raises(ValueError, match="configured project_id"):
        service.create_run(ExpressionRequest.model_validate(valid_payload(project_id="other")))


def test_service_requires_a_canonical_project_id_when_a_figma_registry_is_present(tmp_path: Path) -> None:
    anchor = tmp_path / "art" / "source" / "hero.png"
    anchor.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(anchor)

    with pytest.raises(ValueError, match="canonical project_id"):
        ExpressionStudioService(
            tmp_path,
            FakeExpressionEngine(tmp_path),
            registry=ProjectFigmaRegistry.load(write_registry(tmp_path)),
        )


def test_service_rejects_conflicting_controls_before_engine_invocation(tmp_path: Path) -> None:
    service = service_for(tmp_path)
    request = ExpressionRequest.model_validate(
        valid_payload(controls=[{"code": "AU43", "intensity": "B"}, {"code": "AU5", "intensity": "B"}])
    )

    with pytest.raises(ExpressionConflictError, match=r"AU43.*AU5"):
        service.create_run(request)


def test_engine_receives_a_run_local_anchor_copy_instead_of_the_approved_source(tmp_path: Path) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source)
    initialize_vault(tmp_path)
    original_bytes = source.read_bytes()

    class AnchorMutatingEngine:
        def generate(self, request: ExpressionRequest, _resolved: object, candidates_dir: Path) -> object:
            supplied_anchor = tmp_path / request.anchor.source_path
            supplied_anchor.write_bytes(b"engine-mutated-anchor")
            candidate = candidates_dir / "candidate-000.png"
            Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(candidate)
            return type("Result", (), {"candidates": [candidate], "generation_instruction": "test"})()

    service = ExpressionStudioService(tmp_path, AnchorMutatingEngine(), project_id="demo", run_mode="simulated")
    request = ExpressionRequest.model_validate(valid_payload(candidate_count=1))

    run = service.create_run(request)

    assert run.status == "generated"
    assert source.read_bytes() == original_bytes


def test_service_blocks_without_overwriting_when_original_anchor_changes(tmp_path: Path) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source)
    initialize_vault(tmp_path)
    class OriginalMutatingEngine:
        def generate(self, _request: ExpressionRequest, _resolved: object, candidates_dir: Path) -> EngineResult:
            source.write_bytes(b"malicious-original-overwrite")
            candidate = candidates_dir / "candidate-000.png"
            Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(candidate)
            return EngineResult(candidates=[candidate], generation_instruction="test")

    service = ExpressionStudioService(tmp_path, OriginalMutatingEngine(), project_id="demo", run_mode="simulated")

    run = service.create_run(ExpressionRequest.model_validate(valid_payload(candidate_count=1)))

    assert run.status == "blocked"
    assert source.read_bytes() == b"malicious-original-overwrite"
    assert any("without overwriting" in warning for warning in run.warnings)


def test_service_blocks_engine_candidates_outside_the_run_candidate_directory(tmp_path: Path) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source)
    initialize_vault(tmp_path)
    outside = tmp_path / "art" / "outside.png"
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(outside)

    class OutsideCandidateEngine:
        def generate(self, _request: ExpressionRequest, _resolved: object, _run_dir: Path) -> EngineResult:
            return EngineResult(candidates=[outside], generation_instruction="test")

    service = ExpressionStudioService(tmp_path, OutsideCandidateEngine(), project_id="demo", run_mode="simulated")

    run = service.create_run(ExpressionRequest.model_validate(valid_payload(candidate_count=1)))

    assert run.status == "blocked"
    assert run.result is None
    assert any("candidate" in warning for warning in run.warnings)


@pytest.mark.parametrize("candidate_count, candidate_bytes", [(0, None), (1, b"not-a-png")])
def test_service_blocks_wrong_count_or_invalid_engine_candidate(
    tmp_path: Path, candidate_count: int, candidate_bytes: bytes | None
) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source)
    initialize_vault(tmp_path)

    class InvalidCandidateEngine:
        def generate(self, _request: ExpressionRequest, _resolved: object, candidates_dir: Path) -> EngineResult:
            if candidate_count == 0:
                return EngineResult(candidates=[], generation_instruction="test")
            candidate = candidates_dir / "candidate-000.png"
            candidate.write_bytes(candidate_bytes or b"")
            return EngineResult(candidates=[candidate], generation_instruction="test")

    service = ExpressionStudioService(tmp_path, InvalidCandidateEngine(), project_id="demo", run_mode="simulated")
    run = service.create_run(ExpressionRequest.model_validate(valid_payload(candidate_count=1)))

    assert run.status == "blocked"
    assert run.result is None
    assert any("engine" in warning for warning in run.warnings)


def test_delivery_eligible_engine_rejects_pixel_duplicate_candidates(tmp_path: Path) -> None:
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    anchor = tmp_path / "anchor.png"
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(anchor)
    first = candidates_dir / "candidate-000.png"
    second = candidates_dir / "candidate-001.png"
    Image.new("RGBA", (8, 8), (20, 30, 40, 255)).save(first)
    second.write_bytes(first.read_bytes())

    with pytest.raises(EngineContractError, match="pixel-duplicate"):
        ExpressionStudioService._validate_engine_result(
            EngineResult(candidates=[first, second], generation_instruction="test"),
            2,
            candidates_dir,
            anchor.read_bytes(),
            delivery_eligible=True,
            project_root=tmp_path,
        )


def test_delivery_eligible_engine_rejects_any_candidate_identical_to_anchor(tmp_path: Path) -> None:
    candidates_dir = tmp_path / "candidates"
    candidates_dir.mkdir()
    anchor = tmp_path / "anchor.png"
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(anchor)
    unchanged = candidates_dir / "candidate-000.png"
    changed = candidates_dir / "candidate-001.png"
    unchanged.write_bytes(anchor.read_bytes())
    Image.new("RGBA", (8, 8), (20, 30, 40, 255)).save(changed)

    with pytest.raises(EngineContractError, match="each visibly differ"):
        ExpressionStudioService._validate_engine_result(
            EngineResult(candidates=[unchanged, changed], generation_instruction="test"),
            2,
            candidates_dir,
            anchor.read_bytes(),
            delivery_eligible=True,
            project_root=tmp_path,
        )


def test_engine_candidate_handle_prevents_leaf_symlink_swap_escape(tmp_path: Path) -> None:
    source = tmp_path / "art" / "source" / "hero.png"
    source.parent.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source)
    initialize_vault(tmp_path)
    outside = tmp_path.parent / f"{tmp_path.name}-expression-leaf-outside"
    outside.mkdir()

    class LeafSwappingEngine:
        def generate(self, _request: ExpressionRequest, _resolved: object, candidates_dir: Path) -> EngineResult:
            lexical_candidates = Path(os.readlink(candidates_dir))
            original_candidates = lexical_candidates.with_name("candidates-original")
            lexical_candidates.rename(original_candidates)
            lexical_candidates.symlink_to(outside, target_is_directory=True)
            candidate = candidates_dir / "candidate-000.png"
            Image.new("RGBA", (8, 8), (255, 0, 0, 255)).save(candidate)
            return EngineResult(candidates=[candidate], generation_instruction="test")

    service = ExpressionStudioService(tmp_path, LeafSwappingEngine(), project_id="demo", run_mode="simulated")
    run = service.create_run(ExpressionRequest.model_validate(valid_payload(candidate_count=1)))

    original_candidates = run.paths.run_dir / "candidates-original"
    assert (original_candidates / "candidate-000.png").is_file()
    assert not (outside / "candidate-000.png").exists()
    assert run.status == "blocked"
