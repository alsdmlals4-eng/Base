import json
import hashlib
from pathlib import Path
import subprocess
import zipfile

import pytest

from base_tool_contracts import ProjectFigmaRegistry, ProjectIdentityError, validate_project_identity
from tool_hub.projects import ProjectBindingError, ProjectLocator


BASE_ROOT = Path(__file__).resolve().parents[3]


def make_project(
    root: Path,
    project_id: str = "demo-game",
    *,
    schema_version: int = 2,
    partial_adapter: bool = False,
) -> Path:
    root.mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(root), "config", "user.name", "Test"], check=True)
    (root / ".gitignore").write_text(".asset-vault/\n", encoding="utf-8")
    (root / ".asset-vault" / "library").mkdir(parents=True)
    (root / "game").mkdir()
    (root / "project.godot").write_text("[application]\n", encoding="utf-8")
    project_registry = b'{"skills":[]}\n'
    (root / "skills").mkdir()
    (root / "skills" / "SKILL_REGISTRY.json").write_bytes(project_registry)
    legacy = {"protected_paths": ["project.godot", "game/**"]}
    (root / "skills" / "LEGACY_PROJECT_ADAPTER.json").write_text(json.dumps(legacy), encoding="utf-8")
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "baseline"], check=True)
    baseline = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "fetch", "-q", "origin", f"{baseline}:refs/remotes/origin/main"], check=True)
    adapter = json.loads(
        (BASE_ROOT / "templates" / "project-operations" / "PROJECT_BASE_ADAPTER_V2.json").read_text(encoding="utf-8")
    )
    adapter["schema_version"] = schema_version
    adapter["project"] = {
        "project_id": project_id,
        "repository": f"owner/{project_id}",
        "engine": "Godot 4.7",
        "root": ".",
    }
    base_lock = json.loads((BASE_ROOT / "base-v9.3.lock.json").read_text(encoding="utf-8"))
    adapter["base_release"].update(
        repository="alsdmlals4-eng/Base",
        version="9.3.0",
        release_commit=base_lock["candidate_release_commit"],
        release_evidence_commit=base_lock["candidate_release_evidence_commit"],
    )
    adapter["base_release"].pop("finalization_commit", None)
    adapter["skill_registry"]["base"] = base_lock["candidate_registry"]
    adapter["skill_registry"]["project"]["sha256"] = hashlib.sha256(project_registry).hexdigest()
    policy = (json.dumps(legacy["protected_paths"], ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    adapter["protected_baseline"].update(
        commit=baseline,
        authority_kind="REMOTE_TRACKING_REF",
        authority_ref="refs/remotes/origin/main",
        policy_source_type="FIRST_MIGRATION_LEGACY_SOURCE",
        policy_source_path="skills/LEGACY_PROJECT_ADAPTER.json",
        policy_sha256=hashlib.sha256(policy).hexdigest(),
    )
    adapter["protected_paths"] = legacy["protected_paths"]
    if partial_adapter:
        adapter = {
            "schema_version": schema_version,
            "artifact_role": "PROJECT_BASE_ADAPTER",
            "project": adapter["project"],
        }
    (root / "skills" / "PROJECT_BASE_ADAPTER.json").write_text(
        json.dumps(adapter, indent=2) + "\n", encoding="utf-8"
    )
    subprocess.run(["git", "-C", str(root), "add", "."], check=True)
    subprocess.run(["git", "-C", str(root), "commit", "-qm", "adapter"], check=True)
    return root


def test_locator_registers_exact_v2_project_and_redacts_root(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Project With Spaces")
    locator = ProjectLocator(tmp_path / "machine-projects.json")

    binding = locator.register(project)
    public = locator.public_projects()

    assert binding.project_id == "demo-game"
    assert binding.root == project.resolve()
    assert public == [{"project_id": "demo-game", "display_name": "demo-game", "state": "READY"}]
    assert str(project.resolve()) not in json.dumps(public)


def test_locator_reloads_and_revalidates_fingerprint(tmp_path: Path) -> None:
    project = make_project(tmp_path / "demo")
    config = tmp_path / "machine-projects.json"
    ProjectLocator(config).register(project)

    assert ProjectLocator(config).resolve("demo-game").root == project.resolve()


def test_locator_rejects_v1_and_invalid_project_identity(tmp_path: Path) -> None:
    with pytest.raises(ProjectBindingError, match="IDENTITY_MIGRATION_REQUIRED"):
        ProjectLocator(tmp_path / "one.json").register(
            make_project(tmp_path / "v1", schema_version=1)
        )
    with pytest.raises(ProjectBindingError, match="PROJECT_IDENTITY_ADAPTER_INVALID"):
        ProjectLocator(tmp_path / "two.json").register(
            make_project(tmp_path / "invalid", project_id="Invalid ID")
        )


def test_locator_rejects_partial_document_that_only_claims_v2(tmp_path: Path) -> None:
    with pytest.raises(ProjectBindingError, match="PROJECT_IDENTITY_ADAPTER_INVALID"):
        ProjectLocator(tmp_path / "projects.json").register(
            make_project(tmp_path / "partial", partial_adapter=True)
        )


def test_locator_rejects_non_git_or_unignored_vault(tmp_path: Path) -> None:
    non_git = tmp_path / "non-git"
    non_git.mkdir()
    with pytest.raises(ProjectBindingError, match="PROJECT_IDENTITY_PATH_BLOCKED"):
        ProjectLocator(tmp_path / "one.json").register(non_git)

    project = make_project(tmp_path / "tracked")
    (project / ".gitignore").write_text("", encoding="utf-8")
    with pytest.raises(ProjectBindingError, match="PROJECT_ASSET_VAULT_NOT_GITIGNORED"):
        ProjectLocator(tmp_path / "two.json").register(project)


def test_locator_rejects_a_vault_beneath_a_symlinked_component(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    outside = tmp_path / "outside-vault"
    (outside / "library").mkdir(parents=True)
    original = project / ".asset-vault-original"
    (project / ".asset-vault").rename(original)
    (project / ".asset-vault").symlink_to(outside, target_is_directory=True)

    with pytest.raises(ProjectBindingError, match="PROJECT_IDENTITY_PATH_BLOCKED"):
        ProjectLocator(tmp_path / "projects.json").register(project)


def test_locator_does_not_execute_project_fsmonitor(tmp_path: Path) -> None:
    project = make_project(tmp_path / "demo")
    marker = tmp_path / "fsmonitor-ran"
    hook = tmp_path / "fsmonitor.sh"
    hook.write_text(f"#!/bin/sh\ntouch '{marker}'\necho\n", encoding="utf-8")
    hook.chmod(0o755)
    subprocess.run(["git", "-C", str(project), "config", "core.fsmonitor", str(hook)], check=True)

    ProjectLocator(tmp_path / "projects.json").register(project)

    assert not marker.exists()


def test_locator_rejects_untracked_canonical_adapter(tmp_path: Path) -> None:
    project = make_project(tmp_path / "demo")
    subprocess.run(
        ["git", "-C", str(project), "rm", "--cached", "skills/PROJECT_BASE_ADAPTER.json"],
        check=True,
        capture_output=True,
    )

    with pytest.raises(ProjectBindingError, match="PROJECT_IDENTITY_VALIDATOR_BLOCKED"):
        ProjectLocator(tmp_path / "projects.json").register(project)


def test_locator_rejects_symlinked_root_component(tmp_path: Path) -> None:
    project = make_project(tmp_path / "demo")
    alias = tmp_path / "alias"
    alias.symlink_to(tmp_path, target_is_directory=True)

    with pytest.raises(ProjectBindingError, match="PROJECT_IDENTITY_PATH_BLOCKED"):
        ProjectLocator(tmp_path / "projects.json").register(alias / project.name)


def test_identity_evidence_owns_repository_and_engine_metadata(tmp_path: Path) -> None:
    project = make_project(tmp_path / "demo")

    evidence = validate_project_identity(project, "demo-game", BASE_ROOT)

    assert evidence.repository == "owner/demo-game"
    assert evidence.engine == "Godot 4.7"


def test_locator_ignores_a_fake_git_on_the_caller_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project = make_project(tmp_path / "demo")
    attacker = tmp_path / "attacker-bin"
    attacker.mkdir()
    marker = tmp_path / "fake-git-ran"
    fake_git = attacker / "git"
    fake_git.write_text(f"#!/bin/sh\ntouch '{marker}'\nexit 0\n", encoding="utf-8")
    fake_git.chmod(0o755)
    monkeypatch.setenv("PATH", str(attacker))

    ProjectLocator(tmp_path / "projects.json").register(project)

    assert not marker.exists()


def test_identity_rejects_an_untracked_base_importable_module(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    base_copy = tmp_path / "base-copy"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(BASE_ROOT), str(base_copy)], check=True)
    marker = tmp_path / "shadow-imported"
    (base_copy / "tools" / "jsonschema.py").write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('ran')\n",
        encoding="utf-8",
    )

    with pytest.raises(ProjectIdentityError, match="PROJECT_IDENTITY_VALIDATOR_BLOCKED"):
        validate_project_identity(project, "demo-game", base_copy)
    assert not marker.exists()


def test_identity_rejects_dirty_fixed_validator_bytes(tmp_path: Path) -> None:
    project = make_project(tmp_path / "project")
    base_copy = tmp_path / "base-copy"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(BASE_ROOT), str(base_copy)], check=True)
    checker = base_copy / "tools" / "project_operating_contract.py"
    checker.write_text(checker.read_text(encoding="utf-8") + "\n# dirty\n", encoding="utf-8")

    with pytest.raises(ProjectIdentityError, match="PROJECT_IDENTITY_VALIDATOR_BLOCKED"):
        validate_project_identity(project, "demo-game", base_copy)


def test_identity_skips_sitecustomize_from_the_selected_interpreter(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import base_tool_contracts.project_identity as identity_module
    import sys

    project = make_project(tmp_path / "project")
    environment = tmp_path / "hostile-venv"
    subprocess.run([sys.executable, "-m", "venv", "--system-site-packages", str(environment)], check=True)
    interpreter = environment / "bin" / "python"
    site_packages = subprocess.run(
        [str(interpreter), "-c", "import site; print(site.getsitepackages()[0])"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    marker = tmp_path / "sitecustomize-ran"
    Path(site_packages, "sitecustomize.py").write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('ran')\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(identity_module.sys, "executable", str(interpreter))

    evidence = validate_project_identity(project, "demo-game", BASE_ROOT)

    assert evidence.project_id == "demo-game"
    assert not marker.exists()


def test_identity_holds_the_original_root_across_an_aba_rename(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import base_tool_contracts.project_identity as identity_module

    original = make_project(tmp_path / "project")
    replacement = make_project(tmp_path / "replacement")
    (original / "project.godot").write_text("[application]\nrun/main_scene='changed'\n", encoding="utf-8")
    held = tmp_path / "held-original"
    replacement_home = replacement
    real_run = identity_module.subprocess.run
    swapped = False

    def run_with_aba(command, *args, **kwargs):
        nonlocal swapped
        if not swapped and isinstance(command, list) and "-I" in command:
            swapped = True
            original.rename(held)
            replacement_home.rename(original)
            try:
                return real_run(command, *args, **kwargs)
            finally:
                original.rename(replacement_home)
                held.rename(original)
        return real_run(command, *args, **kwargs)

    monkeypatch.setattr(identity_module.subprocess, "run", run_with_aba)

    with pytest.raises(ProjectIdentityError, match="PROJECT_IDENTITY_VALIDATOR_BLOCKED"):
        validate_project_identity(original, "demo-game", BASE_ROOT)
    assert swapped is True


def test_identity_rejects_a_permanent_root_replacement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import base_tool_contracts.project_identity as identity_module

    original = make_project(tmp_path / "project", project_id="demo-game")
    replacement = make_project(tmp_path / "replacement", project_id="other-game")
    held = tmp_path / "held-original"
    real_run = identity_module.subprocess.run
    swapped = False

    def run_with_replacement(command, *args, **kwargs):
        nonlocal swapped
        result = real_run(command, *args, **kwargs)
        if not swapped and isinstance(command, list) and "-I" in command:
            swapped = True
            original.rename(held)
            replacement.rename(original)
        return result

    monkeypatch.setattr(identity_module.subprocess, "run", run_with_replacement)

    try:
        with pytest.raises(ProjectIdentityError, match="PROJECT_IDENTITY_SNAPSHOT_CHANGED"):
            validate_project_identity(original, "demo-game", BASE_ROOT)
    finally:
        if original.exists():
            original.rename(replacement)
        if held.exists():
            held.rename(original)
    assert swapped is True


def test_identity_rejects_private_validator_runtime_replacement(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import base_tool_contracts.project_identity as identity_module

    project = make_project(tmp_path / "project")
    (project / "project.godot").write_text("[application]\nrun/main_scene='changed'\n", encoding="utf-8")
    real_run = identity_module.subprocess.run
    replaced = False

    def replace_private_checker(command, *args, **kwargs):
        nonlocal replaced
        if not replaced and isinstance(command, list) and "-I" in command:
            runtime = Path(command[command.index("-c") + 2])
            try:
                with runtime.open("wb") as stream:
                    with zipfile.ZipFile(stream, "w") as archive:
                        archive.writestr("check_project_operating_contract.py", "raise SystemExit(0)\n")
            except OSError:
                replaced = True
                return real_run(command, *args, **kwargs)
            replaced = True
        return real_run(command, *args, **kwargs)

    monkeypatch.setattr(identity_module.subprocess, "run", replace_private_checker)

    with pytest.raises(ProjectIdentityError, match="PROJECT_IDENTITY_VALIDATOR_BLOCKED"):
        validate_project_identity(project, "demo-game", BASE_ROOT)
    assert replaced is True


def test_visual_preflight_requires_the_canonical_base_figma_registry(tmp_path: Path) -> None:
    from base_tool_contracts import ApprovedAnchorRegistry

    project = make_project(tmp_path / "project", project_id="coc-fiction")
    locator = ProjectLocator(tmp_path / "projects.json")
    locator.register(project)
    canonical = ProjectFigmaRegistry.load(
        BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
    )

    anchor_path = project / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    anchor_path.parent.mkdir(exist_ok=True)
    anchor_path.write_text('{"version":1,"entries":[]}', encoding="utf-8")
    subprocess.run(["git", "-C", str(project), "add", anchor_path.relative_to(project).as_posix()], check=True)
    subprocess.run(["git", "-C", str(project), "commit", "-qm", "visual anchors"], check=True)
    anchors = ApprovedAnchorRegistry.load(anchor_path)

    binding = locator.preflight_visual("coc-fiction", canonical, anchors)

    assert binding.project_id == "coc-fiction"
    copied_path = tmp_path / "copied-figma-registry.json"
    copied_path.write_bytes(canonical.source_path.read_bytes())
    copied = ProjectFigmaRegistry.load(copied_path)
    with pytest.raises(ProjectBindingError, match="PROJECT_FIGMA_ROUTING_UNAVAILABLE"):
        locator.preflight_visual("coc-fiction", copied, anchors)


def test_visual_preflight_rejects_untracked_anchor_registry(tmp_path: Path) -> None:
    from base_tool_contracts import ApprovedAnchorRegistry

    project = make_project(tmp_path / "project", project_id="coc-fiction")
    locator = ProjectLocator(tmp_path / "projects.json")
    locator.register(project)
    figma = ProjectFigmaRegistry.load(
        BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
    )
    anchor_path = project / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    anchor_path.parent.mkdir(exist_ok=True)
    anchor_path.write_text('{"version":1,"entries":[]}', encoding="utf-8")
    anchors = ApprovedAnchorRegistry.load(anchor_path)

    with pytest.raises(ProjectBindingError, match="PROJECT_ANCHOR_EVIDENCE_UNAVAILABLE"):
        locator.preflight_visual("coc-fiction", figma, anchors)
