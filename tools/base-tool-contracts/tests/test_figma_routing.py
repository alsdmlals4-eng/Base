import importlib
import json
from pathlib import Path
import subprocess

import pytest
import hashlib
from PIL import Image


ROOT = Path(__file__).parents[3]


def write_registry(tmp_path: Path, *, file_key: str = "abc123") -> Path:
    payload = {
        "version": 1,
        "purpose": "test routing only",
        "default_delivery_page": "Sprite Animation Studio",
        "default_generation_area": "Generated Assets",
        "entries": [
            {
                "project_id": "demo",
                "display_name": "Demo",
                "figma_file_key": file_key,
                "figma_url": f"https://www.figma.com/design/{file_key}/demo?node-id=0-1",
                "delivery_status": "READY_FOR_DELIVERY",
                "delivery_page_node_id": "10:2",
                "generation_area_node_id": "10:3",
            }
        ],
    }
    path = tmp_path / "registry.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def routing_module():
    return importlib.import_module("base_tool_contracts.figma_routing")


def test_schema_accepts_the_canonical_base_registry() -> None:
    import jsonschema

    schema = json.loads((ROOT / "schemas" / "project-figma-target-registry-v1.schema.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json").read_text(encoding="utf-8"))

    jsonschema.validate(registry, schema)


def test_loader_resolves_ready_target_and_routing_state(tmp_path: Path) -> None:
    module = routing_module()
    registry = module.ProjectFigmaRegistry.load(write_registry(tmp_path))

    target = registry.resolve_ready_target("demo")

    assert target.figma_file_key == "abc123"
    assert target.generation_area_node_id == "10:3"
    assert registry.routing_state("demo") == "ROUTING_CONFIGURED"


def test_loader_rejects_registry_beneath_a_symlinked_parent(tmp_path: Path) -> None:
    module = routing_module()
    real_parent = tmp_path / "real"
    real_parent.mkdir()
    path = write_registry(real_parent)
    alias = tmp_path / "alias"
    alias.symlink_to(real_parent, target_is_directory=True)

    with pytest.raises(ValueError, match="unavailable|symlink"):
        module.ProjectFigmaRegistry.load(alias / path.name)


def test_figma_registry_requires_the_committed_canonical_base_path(tmp_path: Path) -> None:
    module = routing_module()
    canonical = module.ProjectFigmaRegistry.load(
        ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
    )
    canonical.assert_canonical(ROOT)

    copied = module.ProjectFigmaRegistry.load(write_registry(tmp_path))
    with pytest.raises(module.DeliveryBlockedError, match="canonical"):
        copied.assert_canonical(ROOT)


def test_archived_figma_route_never_collapses_to_a_registered_route(tmp_path: Path) -> None:
    module = routing_module()
    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"][0]["delivery_status"] = "ARCHIVED"
    payload["entries"][0]["delivery_page_node_id"] = None
    payload["entries"][0]["generation_area_node_id"] = None
    path.write_text(json.dumps(payload), encoding="utf-8")

    registry = module.ProjectFigmaRegistry.load(path)

    assert registry.routing_state("demo") == "ROUTING_ARCHIVED"
    assert registry.registration_state("demo") == "ROUTING_ARCHIVED"


def test_registered_no_mutation_is_distinct_from_ready_delivery(tmp_path: Path) -> None:
    module = routing_module()
    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"][0]["delivery_status"] = "REGISTERED_NO_MUTATION"
    payload["entries"][0]["delivery_page_node_id"] = None
    payload["entries"][0]["generation_area_node_id"] = None
    path.write_text(json.dumps(payload), encoding="utf-8")

    registry = module.ProjectFigmaRegistry.load(path)

    assert registry.registration_state("demo") == "ROUTING_REGISTERED"
    assert registry.routing_state("demo") == "ROUTING_BLOCKED"


def test_anchor_validation_binds_file_key_and_normalizes_node_id(tmp_path: Path) -> None:
    module = routing_module()
    registry = module.ProjectFigmaRegistry.load(write_registry(tmp_path))

    assert registry.validate_anchor_url(
        "demo", "https://www.figma.com/design/abc123/source?node-id=123-456"
    ) == "123:456"

    with pytest.raises(module.DeliveryBlockedError, match="bound project"):
        registry.validate_anchor_url("demo", "https://www.figma.com/design/wrong/source?node-id=1-2")


def test_loader_rejects_duplicate_project_and_mismatched_url_key(tmp_path: Path) -> None:
    module = routing_module()
    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"].append(dict(payload["entries"][0]))
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate project_id"):
        module.ProjectFigmaRegistry.load(path)


def test_figma_registry_detects_post_startup_mutation(tmp_path: Path) -> None:
    module = routing_module()
    path = write_registry(tmp_path)
    registry = module.ProjectFigmaRegistry.load(path)
    path.write_text("{}", encoding="utf-8")

    with pytest.raises(module.DeliveryBlockedError, match="changed"):
        registry.assert_unchanged()

    path = write_registry(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["entries"][0]["figma_url"] = "https://www.figma.com/design/wrong/demo?node-id=0-1"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(ValueError, match="does not match"):
        module.ProjectFigmaRegistry.load(path)


def test_project_owned_anchor_evidence_requires_exact_url_and_source_hash(tmp_path: Path) -> None:
    from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry

    source = tmp_path / "hero.png"
    Image.new("RGBA", (4, 4), (255, 0, 0, 255)).save(source)
    url = "https://www.figma.com/design/abc123/source?node-id=1-2"
    payload = {
        "version": 1,
        "entries": [{
            "project_id": "demo",
            "source_path": "art/hero.png",
            "figma_node_url": url,
            "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "approval_state": "APPROVED",
            "evidence": {"kind": "EXPORTED_SNAPSHOT", "ref": "review-42", "checked_at": "2026-08-12T12:00:00Z"},
        }],
    }
    path = tmp_path / "anchors.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    import jsonschema
    schema = json.loads((ROOT / "schemas" / "project-approved-anchor-registry-v1.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(payload, schema)
    registry = ApprovedAnchorRegistry.load(path)

    assert registry.verify(project_id="demo", source_path="art/hero.png", figma_node_url=url, source_bytes=source.read_bytes()) == "ANCHOR_EVIDENCE_VERIFIED"
    with pytest.raises(AnchorEvidenceError, match="SHA-256"):
        registry.verify(project_id="demo", source_path="art/hero.png", figma_node_url=url, source_bytes=b"changed")


def test_anchor_registry_must_match_the_committed_project_blob(tmp_path: Path) -> None:
    from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "Test"], check=True)
    registry_path = tmp_path / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    registry_path.parent.mkdir()
    registry_path.write_text('{"version":1,"entries":[]}', encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", registry_path.relative_to(tmp_path).as_posix()], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "anchor evidence"], check=True)
    registry_path.write_text('{"version":1,"entries":[] }', encoding="utf-8")

    registry = ApprovedAnchorRegistry.load(registry_path)
    with pytest.raises(AnchorEvidenceError, match="committed project blob"):
        registry.assert_project_owned(tmp_path)


def test_anchor_registry_rejects_a_symlinked_parent(tmp_path: Path) -> None:
    from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry

    real_parent = tmp_path / "real"
    real_parent.mkdir()
    path = real_parent / "anchors.json"
    path.write_text('{"version":1,"entries":[]}', encoding="utf-8")
    alias = tmp_path / "alias"
    alias.symlink_to(real_parent, target_is_directory=True)

    with pytest.raises(AnchorEvidenceError, match="invalid|symlink"):
        ApprovedAnchorRegistry.load(alias / path.name)


def test_anchor_registry_accepts_only_line_ending_normalization_of_a_clean_blob(tmp_path: Path) -> None:
    from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "core.autocrlf", "true"], check=True)
    (tmp_path / ".gitattributes").write_text("*.json text\n", encoding="utf-8")
    registry_path = tmp_path / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    registry_path.parent.mkdir()
    registry_path.write_bytes(b'{"version":1,"entries":[]}\n')
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "anchor evidence"], check=True)
    registry_path.write_bytes(b'{"version":1,"entries":[]}\r\n')

    ApprovedAnchorRegistry.load(registry_path).assert_project_owned(tmp_path)

    registry_path.write_bytes(b'{"version": 1,"entries":[]}\r\n')
    with pytest.raises(AnchorEvidenceError, match="committed project blob"):
        ApprovedAnchorRegistry.load(registry_path).assert_project_owned(tmp_path)


def test_anchor_registry_rejects_a_noncanonical_tracked_project_path(tmp_path: Path) -> None:
    from base_tool_contracts import AnchorEvidenceError, ApprovedAnchorRegistry

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "config", "user.name", "Test"], check=True)
    registry_path = tmp_path / "docs" / "ATTACKER_ANCHORS.json"
    registry_path.parent.mkdir()
    registry_path.write_text('{"version":1,"entries":[]}', encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "."], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "attacker anchors"], check=True)

    with pytest.raises(AnchorEvidenceError, match="canonical project path"):
        ApprovedAnchorRegistry.load(registry_path).assert_project_owned(tmp_path)


def test_staging_revalidation_rejects_a_post_create_symlink_swap(tmp_path: Path) -> None:
    from base_tool_contracts import StagingViolation, assert_verified_staging_path, create_verified_run_directories, stable_staging_path, staging_identity

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (tmp_path / ".asset-vault" / "library").mkdir(parents=True)
    run_dir, _ = create_verified_run_directories(tmp_path, dynamic_components=("generated", "tool", "asset", "run"), leaf_directories=("frames",))
    identity = staging_identity(run_dir)
    with stable_staging_path(tmp_path, run_dir, identity) as stable:
        original = run_dir.with_name("run-original")
        run_dir.rename(original)
        outside = tmp_path.parent / f"{tmp_path.name}-outside"
        outside.mkdir()
        run_dir.symlink_to(outside, target_is_directory=True)
        (stable / "frames" / "safe.txt").write_text("confined", encoding="utf-8")

    assert (original / "frames" / "safe.txt").read_text(encoding="utf-8") == "confined"
    assert not (outside / "frames" / "safe.txt").exists()

    with pytest.raises(StagingViolation, match="symlink"):
        assert_verified_staging_path(tmp_path, run_dir)


def test_stable_staging_tree_pins_mutable_leaf_and_nested_directories(tmp_path: Path) -> None:
    """A same-user name swap must not redirect writes outside the opened directory handles."""
    from base_tool_contracts import create_verified_run_directories, stable_staging_tree, staging_identity

    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (tmp_path / ".asset-vault" / "library").mkdir(parents=True)
    run_dir, _ = create_verified_run_directories(
        tmp_path,
        dynamic_components=("generated", "tool", "asset", "run"),
        leaf_directories=("frames", "exports"),
    )
    outside = tmp_path.parent / f"{tmp_path.name}-leaf-outside"
    outside.mkdir()

    with stable_staging_tree(tmp_path, run_dir, staging_identity(run_dir)) as stable:
        stable_frames = stable.open_directory("frames")
        stable_selected = stable.open_directory("exports/frames/attack", create=True)

        original_frames = run_dir / "frames-original"
        (run_dir / "frames").rename(original_frames)
        (run_dir / "frames").symlink_to(outside, target_is_directory=True)

        original_selected = run_dir / "exports" / "frames" / "attack-original"
        (run_dir / "exports" / "frames" / "attack").rename(original_selected)
        (run_dir / "exports" / "frames" / "attack").symlink_to(outside, target_is_directory=True)

        (stable_frames / "frame.png").write_bytes(b"frame")
        (stable_selected / "selected.png").write_bytes(b"selected")

    assert (original_frames / "frame.png").read_bytes() == b"frame"
    assert (original_selected / "selected.png").read_bytes() == b"selected"
    assert not (outside / "frame.png").exists()
    assert not (outside / "selected.png").exists()


def test_staging_write_rejects_a_file_symlink_without_following_it(tmp_path: Path) -> None:
    from base_tool_contracts import StagingViolation, safe_staging_write_bytes

    output = tmp_path / "output"
    output.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_bytes(b"protected")
    (output / "manifest.json").symlink_to(outside)

    with pytest.raises(StagingViolation, match="regular file"):
        safe_staging_write_bytes(output, "manifest.json", b"safe")

    assert outside.read_bytes() == b"protected"
    assert (output / "manifest.json").is_symlink()


def test_staging_read_rejects_final_symlink_and_sha_mismatch(tmp_path: Path) -> None:
    from base_tool_contracts import StagingViolation, staging_read_bytes

    output = tmp_path / "output"
    output.mkdir()
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"outside")
    (output / "frame.png").symlink_to(outside)

    with pytest.raises(StagingViolation, match="regular file"):
        staging_read_bytes(output, "frame.png")

    (output / "frame.png").unlink()
    (output / "frame.png").write_bytes(b"inside")
    with pytest.raises(StagingViolation, match="SHA-256"):
        staging_read_bytes(output, "frame.png", expected_sha256="0" * 64)


def test_confined_staging_read_rejects_an_intermediate_symlink_swap(tmp_path: Path) -> None:
    from base_tool_contracts import StagingViolation, confined_staging_read_bytes

    run = tmp_path / "vault" / "run"
    frames = run / "frames"
    frames.mkdir(parents=True)
    (frames / "frame.png").write_bytes(b"inside")
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "frame.png").write_bytes(b"outside")
    original = run.with_name("run-original")
    run.rename(original)
    run.symlink_to(outside, target_is_directory=True)

    with pytest.raises(StagingViolation, match="link|regular"):
        confined_staging_read_bytes(tmp_path, run / "frame.png")


def test_staging_write_detects_destination_swap_while_holding_the_original_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    import os
    from base_tool_contracts import StagingViolation, safe_staging_write_bytes

    output = tmp_path / "output"
    output.mkdir()
    target = output / "manifest.json"
    target.write_bytes(b"old")
    outside = tmp_path / "outside.txt"
    outside.write_bytes(b"protected")
    original_fsync = os.fsync

    def replace_destination(descriptor: int) -> None:
        original_fsync(descriptor)
        target.rename(output / "manifest-original.json")
        target.symlink_to(outside)

    monkeypatch.setattr(os, "fsync", replace_destination)

    with pytest.raises(StagingViolation, match="identity changed"):
        safe_staging_write_bytes(output, "manifest.json", b"safe")
    assert outside.read_bytes() == b"protected"
    assert (output / "manifest-original.json").read_bytes() == b"safe"


def test_staging_write_replaces_a_hard_link_without_overwriting_its_external_inode(tmp_path: Path) -> None:
    from base_tool_contracts import safe_staging_write_bytes

    output = tmp_path / "output"
    output.mkdir()
    outside = tmp_path / "protected.txt"
    outside.write_bytes(b"protected")
    target = output / "manifest.json"
    target.hardlink_to(outside)

    safe_staging_write_bytes(output, "manifest.json", b"safe")

    assert outside.read_bytes() == b"protected"
    assert target.read_bytes() == b"safe"
    assert target.stat().st_ino != outside.stat().st_ino
