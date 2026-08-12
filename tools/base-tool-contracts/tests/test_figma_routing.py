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
