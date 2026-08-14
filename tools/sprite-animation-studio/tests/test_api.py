from pathlib import Path
from dataclasses import replace
from io import BytesIO
import os
import subprocess

from fastapi.testclient import TestClient
from PIL import Image
import pytest

from sprite_animation_studio.app import create_app
from sprite_animation_studio.delivery import ProjectFigmaRegistry
from sprite_animation_studio.engine import EnginePolicy, EngineResult, FakeSpriteEngine, PinnedSpriteGenEngine, SpriteEngine
from sprite_animation_studio.service import SpriteAnimationService
from sprite_animation_studio.imports import validate_imported_image
from sprite_animation_studio.models import SpriteAnimationRequest
from tests.test_models import valid_payload
from tests.test_delivery import write_registry


class EligibleSpriteEngine(FakeSpriteEngine):
    def generate(self, request: object, frames_dir: Path, engine_dir: Path) -> EngineResult:
        result = super().generate(request, frames_dir, engine_dir)
        return EngineResult(frames=result.frames, provenance="pinned_sprite_gen", delivery_eligible=True)


def _sprite_png(color: tuple[int, int, int, int], *, size: tuple[int, int] = (8, 8)) -> bytes:
    output = BytesIO()
    Image.new("RGBA", size, color).save(output, format="PNG")
    return output.getvalue()


def test_import_service_rejects_forged_frame_metadata_and_dimension_bypass(tmp_path: Path) -> None:
    source = tmp_path / "art" / "source"
    source.mkdir(parents=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source / "idle.png")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".asset-vault" / "library").mkdir(parents=True)
    (tmp_path / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    service = SpriteAnimationService(tmp_path, FakeSpriteEngine(), project_id="demo")
    frames = tuple(
        validate_imported_image(
            _sprite_png((index * 40, 10, 20, 255), size=(8 + index, 8)),
            declared_source="LOCAL_GENERATOR",
            order=index,
        )
        for index in range(4)
    )
    forged = tuple(replace(frame, sha256="0" * 64, width=8, height=8) for frame in frames)

    with pytest.raises(ValueError, match="metadata does not match validated bytes"):
        service.create_import_run(
            SpriteAnimationRequest.model_validate(valid_payload()),
            forged,
            "LOCAL_GENERATOR",
        )


def client_for(
    project_root: Path,
    registry: ProjectFigmaRegistry | None = None,
    project_id: str | None = "demo",
    engine: SpriteEngine | None = None,
    initialize_vault: bool = True,
    bootstrap_security: bool = True,
    run_mode: str = "simulated",
) -> TestClient:
    source = project_root / "art" / "source"
    source.mkdir(parents=True, exist_ok=True)
    Image.new("RGBA", (8, 8), (255, 255, 255, 255)).save(source / "idle.png")
    if initialize_vault:
        subprocess.run(["git", "init", "-q", str(project_root)], check=True)
        (project_root / ".asset-vault" / "library").mkdir(parents=True, exist_ok=True)
        (project_root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    client = TestClient(create_app(project_root, engine or FakeSpriteEngine(), registry=registry, project_id=project_id, bind_origin="http://testserver", test_mode=True, run_mode=run_mode))
    client.headers["Origin"] = "http://testserver"
    if bootstrap_security:
        config = client.get("/api/config").json()
        if "csrf_token" in config:
            client.headers["X-Studio-CSRF"] = config["csrf_token"]
    return client


def test_create_run_returns_422_without_an_approved_anchor(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    payload = valid_payload(anchor={"source_path": "art/source/idle.png", "figma_node_url": "https://www.figma.com/design/demo?node-id=1-2", "approval_status": "draft"})

    response = client.post("/api/runs", json=payload)

    assert response.status_code == 422


def test_config_exposes_bound_project_and_simulated_state(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path))
    response = client_for(tmp_path, registry, project_id="demo").get("/api/config")

    assert response.status_code == 200
    payload = response.json()
    assert payload["project_id"] == "demo"
    assert payload["engine_provenance"] == "simulated"
    assert payload["delivery_eligible"] is False
    assert payload["routing_state"] == "ROUTING_CONFIGURED"
    assert len(payload["csrf_token"]) >= 32


def test_app_and_service_default_to_subscription_handoff_import_mode(tmp_path: Path) -> None:
    app = create_app(
        tmp_path,
        FakeSpriteEngine(),
        project_id="demo",
        bind_origin="http://testserver",
        test_mode=True,
    )
    service = SpriteAnimationService(tmp_path, FakeSpriteEngine(), project_id="demo")

    payload = TestClient(app).get("/api/config").json()

    assert payload["run_mode"] == "subscription_handoff_import"
    assert payload["engine_provenance"] == "subscription_handoff_import"
    assert service.config()["run_mode"] == "subscription_handoff_import"


def test_pinned_engine_evidence_records_that_a_provider_call_was_made(tmp_path: Path) -> None:
    service = SpriteAnimationService(
        tmp_path,
        FakeSpriteEngine(),
        project_id="demo",
        run_mode="simulated",
    )
    policy = EnginePolicy("sprite.pinned.test", "pinned_sprite_gen", True, "b" * 64)

    evidence = service._engine_evidence((), policy=policy)

    assert evidence["provider_call_made"] is True


def test_blocked_pinned_run_does_not_claim_a_provider_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = tmp_path / "sprite-gen"
    repository.mkdir()
    executable = repository / "sprite-gen"
    executable.write_text("stub", encoding="utf-8")
    monkeypatch.setattr(PinnedSpriteGenEngine, "_verify_repository_pin", lambda _self: True)
    engine = PinnedSpriteGenEngine(executable, tmp_path, sprite_gen_repository=repository)
    client = client_for(tmp_path, engine=engine, run_mode="pinned_sprite_gen")

    run = client.post("/api/runs", json=valid_payload()).json()

    assert run["status"] == "blocked"
    assert run["provider_call_made"] is False


def test_app_rejects_run_mode_that_does_not_match_the_configured_engine(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="run mode does not match"):
        create_app(tmp_path, FakeSpriteEngine(), project_id="demo", run_mode="pinned_sprite_gen")


def test_status_exposes_immutable_child_identity(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path))
    payload = client_for(tmp_path, registry, project_id="demo").get("/api/status").json()

    assert payload["tool_id"] == "sprite-animation-studio"
    assert payload["project_id"] == "demo"
    assert payload["engine_provenance"] == "simulated"
    assert len(payload["launch_nonce"]) >= 32
    assert len(payload["config_hash"]) == 64
    assert len(payload["root_fingerprint"]) == 64
    assert len(payload["adapter_sha256"]) == 64
    assert len(payload["figma_registry_sha256"]) == 64
    assert len(payload["engine_config_sha256"]) == 64
    assert payload["process_id"] > 0


def test_status_echoes_hub_supplied_project_identity(tmp_path: Path) -> None:
    app = create_app(
        tmp_path,
        FakeSpriteEngine(),
        project_id="demo",
        launch_nonce="n" * 43,
        adapter_sha256="a" * 64,
        root_fingerprint="b" * 64,
        bind_origin="http://testserver",
        test_mode=True,
    )

    payload = TestClient(app).get("/api/status").json()

    assert payload["launch_nonce"] == "n" * 43
    assert payload["adapter_sha256"] == "a" * 64
    assert payload["root_fingerprint"] == "b" * 64


def test_mutation_rejects_missing_csrf_and_hostile_origin(tmp_path: Path) -> None:
    raw_client = client_for(tmp_path, bootstrap_security=False)
    missing = raw_client.post("/api/runs", json=valid_payload())
    client = client_for(tmp_path)
    foreign = client.post("/api/runs", json=valid_payload(), headers={"Origin": "https://evil.example"})
    hostile_host = client.post("/api/runs", json=valid_payload(), headers={"Host": "evil.example"})
    wrong_port = client.post("/api/runs", json=valid_payload(), headers={"Origin": "http://testserver:9999"})
    wrong_scheme = client.post("/api/runs", json=valid_payload(), headers={"Origin": "https://testserver"})
    missing_origin = client.post("/api/runs", json=valid_payload(), headers={"Origin": ""})

    assert missing.status_code == 403
    assert foreign.status_code == 403
    assert hostile_host.status_code == 400
    assert wrong_port.status_code == 403
    assert wrong_scheme.status_code == 403
    assert missing_origin.status_code == 403


def test_api_rejects_an_anchor_from_another_figma_file(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path))
    payload = valid_payload()
    payload["anchor"] = {
        "source_path": "art/source/idle.png",
        "figma_node_url": "https://www.figma.com/design/WRONG/source?node-id=1-2",
        "approval_status": "approved",
    }

    response = client_for(tmp_path, registry, project_id="demo").post("/api/runs", json=payload)

    assert response.status_code == 422
    assert "bound project" in response.json()["detail"]


def test_api_blocks_generation_when_project_asset_vault_is_missing(tmp_path: Path) -> None:
    response = client_for(tmp_path, initialize_vault=False).post("/api/runs", json=valid_payload())

    assert response.status_code == 422
    assert "asset vault" in response.json()["detail"]


def test_export_rejects_an_incomplete_selection(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    response = client.post("/api/runs", json=valid_payload())
    run_id = response.json()["run_id"]

    export = client.post(f"/api/runs/{run_id}/export", json={"selected": [0, 1, 2]})

    assert export.status_code == 409
    assert export.json()["status"] == "blocked"


def test_generated_candidate_frame_is_available_to_the_local_workspace(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]

    frame = client.get(f"/api/runs/{run_id}/frames/0")

    assert frame.status_code == 200
    assert frame.headers["content-type"] == "image/png"


def test_approved_anchor_image_is_available_to_the_local_workspace(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]

    anchor = client.get(f"/api/runs/{run_id}/anchor")

    assert anchor.status_code == 200
    assert anchor.headers["content-type"] == "image/png"


def test_curation_persists_transform_values_from_the_browser_shape(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]

    response = client.post(f"/api/runs/{run_id}/curation", json={"selected": [0, 1, 2, 3], "transforms": {"1": {"dx": 3, "dy": -2, "scale": 1.2}}})

    assert response.status_code == 200
    assert response.json()["status"] == "curated"


def test_fake_generation_is_simulated_and_cannot_be_exported(tmp_path: Path) -> None:
    client = client_for(tmp_path)
    run = client.post("/api/runs", json=valid_payload()).json()
    run_id = run["run_id"]

    response = client.post(f"/api/runs/{run_id}/export", json={"selected": [0, 1, 2, 3]})

    assert run["engine"]["provenance"] == "simulated"
    assert run["engine"]["delivery_eligible"] is False
    assert run["engine"]["adapter_id"] == "sprite.fake.v1"
    assert response.status_code == 409
    assert "simulated" in response.json()["detail"]
    assert not list((tmp_path / ".asset-vault" / "library" / "generated" / "sprite-animation-studio").rglob("atlas.png"))


def test_figma_delivery_remains_blocked_for_fake_generation(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path))
    client = client_for(tmp_path, registry, project_id="demo")
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]
    client.post(f"/api/runs/{run_id}/export", json={"selected": [0, 1, 2, 3]})

    response = client.post(f"/api/runs/{run_id}/figma-delivery")

    assert response.status_code == 409
    assert response.json()["status"] == "blocked"


def test_fake_subclass_cannot_self_attest_for_a_protected_project_target(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path, status="REGISTERED_NO_MUTATION"))
    client = client_for(tmp_path, registry, project_id="demo", engine=EligibleSpriteEngine())
    run_id = client.post("/api/runs", json=valid_payload()).json()["run_id"]
    client.post(f"/api/runs/{run_id}/export", json={"selected": [0, 1, 2, 3]})

    response = client.post(f"/api/runs/{run_id}/figma-delivery")

    assert response.status_code == 409
    assert response.json()["status"] == "blocked"
    assert "curated export" in response.json()["detail"]


def test_sprite_engine_cannot_mutate_the_original_anchor(tmp_path: Path) -> None:
    original: bytes = b""

    class MutatingEngine:
        def generate(self, request: object, frames_dir: Path, _engine_dir: Path) -> EngineResult:
            source = tmp_path / "art" / "source" / "idle.png"
            source.write_bytes(b"mutated")
            frames = []
            for index in range(4):
                frame = frames_dir / f"frame-{index:03d}.png"
                Image.new("RGBA", (8, 8), (255, 0, 0, 255)).save(frame)
                frames.append(frame)
            return EngineResult(frames=tuple(frames))

    client = client_for(tmp_path, engine=MutatingEngine())
    original = (tmp_path / "art" / "source" / "idle.png").read_bytes()
    run = client.post("/api/runs", json=valid_payload()).json()

    assert run["status"] == "blocked"
    assert "changed" in " ".join(run["warnings"])
    assert (tmp_path / "art" / "source" / "idle.png").read_bytes() == b"mutated"


def test_figma_delivery_rejects_a_request_for_another_project(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path))
    client = client_for(tmp_path, registry, project_id="demo")

    response = client.post("/api/runs", json=valid_payload(project_id="other-project"))

    assert response.status_code == 422
    assert "configured project_id" in response.json()["detail"]


def test_registry_backed_sprite_service_requires_a_canonical_project_id(tmp_path: Path) -> None:
    registry = ProjectFigmaRegistry.load(write_registry(tmp_path))

    with pytest.raises(ValueError, match="canonical project_id"):
        client_for(tmp_path, registry, project_id=None)


def test_engine_frame_handle_prevents_leaf_symlink_swap_escape(tmp_path: Path) -> None:
    outside = tmp_path.parent / f"{tmp_path.name}-sprite-leaf-outside"
    outside.mkdir()

    class LeafSwappingEngine:
        def generate(self, request: object, frames_dir: Path, _engine_dir: Path) -> EngineResult:
            lexical_frames = Path(os.readlink(frames_dir))
            original_frames = lexical_frames.with_name("frames-original")
            lexical_frames.rename(original_frames)
            lexical_frames.symlink_to(outside, target_is_directory=True)
            frames = []
            for index in range(request.action.frame_count):
                frame = frames_dir / f"frame-{index:03d}.png"
                Image.new("RGBA", (8, 8), (255, 0, 0, 255)).save(frame)
                frames.append(frame)
            return EngineResult(frames=tuple(frames))

    client = client_for(tmp_path, engine=LeafSwappingEngine())
    run = client.post("/api/runs", json=valid_payload()).json()
    original_frames = next(
        (tmp_path / ".asset-vault" / "library" / "generated" / "sprite-animation-studio").rglob("frames-original")
    )

    assert (original_frames / "frame-000.png").is_file()
    assert not (outside / "frame-000.png").exists()
    assert run["status"] == "blocked"
