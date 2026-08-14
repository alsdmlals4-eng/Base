from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

from base_tool_contracts import ProjectFigmaRegistry
from test_projects import BASE_ROOT, make_project
from tool_hub.onboarding import ProjectOnboardingService
from tool_hub.projects import ProjectLocator


CATALOG = BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
REPOSITORY_URL = "https://github.com/alsdmlals4-eng/Coc-Fiction.git"


def set_origin(project: Path, url: str = REPOSITORY_URL) -> None:
    subprocess.run(["git", "-C", str(project), "remote", "set-url", "origin", url], check=True)


def service(tmp_path: Path, *, clone_runner=None) -> ProjectOnboardingService:
    return ProjectOnboardingService(
        ProjectLocator(tmp_path / "machine" / "projects.json"),
        ProjectFigmaRegistry.load(CATALOG),
        managed_root=tmp_path / "Documents" / "GitHub",
        home_root=tmp_path,
        clone_runner=clone_runner,
    )


def test_status_finds_only_the_exact_reviewed_repository_name(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Documents" / "GitHub" / "Coc-Fiction", "coc-fiction")
    set_origin(project)
    unrelated = make_project(tmp_path / "Documents" / "GitHub" / "nested" / "Coc-Fiction", "coc-fiction")
    set_origin(unrelated)

    state = service(tmp_path).status("coc-fiction")

    assert state.public_view() == {
        "project_id": "coc-fiction",
        "local_state": "FOUND_UNREGISTERED",
        "action_label": "PC에서 찾기",
    }
    assert str(tmp_path) not in str(state.public_view())


def test_status_reports_clone_available_without_scanning_unrelated_paths(tmp_path: Path) -> None:
    unrelated = make_project(tmp_path / "elsewhere" / "Coc-Fiction", "coc-fiction")
    set_origin(unrelated)

    assert service(tmp_path).status("coc-fiction").local_state == "CLONE_AVAILABLE"


def test_status_rejects_wrong_origin_and_occupied_destination(tmp_path: Path) -> None:
    wrong = make_project(tmp_path / "Documents" / "GitHub" / "Coc-Fiction", "coc-fiction")
    set_origin(wrong, "https://github.com/other/project.git")
    assert service(tmp_path).status("coc-fiction").local_state == "IDENTITY_MISMATCH"

    shutil.rmtree(wrong)
    occupied = tmp_path / "Documents" / "GitHub" / "Coc-Fiction"
    occupied.parent.mkdir(parents=True, exist_ok=True)
    occupied.write_text("not a repository", encoding="utf-8")
    assert service(tmp_path).status("coc-fiction").local_state == "PATH_OCCUPIED"


def test_onboard_registers_an_existing_exact_checkout_idempotently(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Documents" / "GitHub" / "Coc-Fiction", "coc-fiction")
    set_origin(project)
    owner = service(tmp_path)

    first = owner.onboard("coc-fiction")
    second = owner.onboard("coc-fiction")

    assert first.local_state == "REGISTERED"
    assert second.local_state == "REGISTERED"
    assert owner.locator.resolve("coc-fiction").root == project.resolve()


def test_onboard_clones_to_a_random_stage_then_publishes_and_registers(tmp_path: Path) -> None:
    source = make_project(tmp_path / "source", "coc-fiction")
    set_origin(source)
    shutil.rmtree(source / ".asset-vault")
    calls: list[tuple[str, Path]] = []

    def clone_runner(repository_url: str, destination: Path) -> None:
        calls.append((repository_url, destination))
        shutil.copytree(source, destination, dirs_exist_ok=True)

    owner = service(tmp_path, clone_runner=clone_runner)
    result = owner.onboard("coc-fiction")
    final = tmp_path / "Documents" / "GitHub" / "Coc-Fiction"

    assert result.local_state == "REGISTERED"
    assert calls[0][0] == REPOSITORY_URL
    assert calls[0][1].name != "Coc-Fiction"
    assert final.is_dir()
    assert (final / ".asset-vault" / "library").is_dir()
    assert owner.locator.resolve("coc-fiction").root == final.resolve()


def test_failed_clone_never_registers_or_exposes_diagnostics(tmp_path: Path) -> None:
    def failed_clone(repository_url: str, destination: Path) -> None:
        raise RuntimeError(f"secret failure at {destination} for {repository_url}")

    owner = service(tmp_path, clone_runner=failed_clone)
    result = owner.onboard("coc-fiction")

    assert result.local_state == "CLONE_FAILED"
    assert owner.locator.public_projects() == []
    assert str(tmp_path) not in str(result.public_view())
    assert REPOSITORY_URL not in str(result.public_view())


def test_registered_project_must_still_match_the_reviewed_origin(tmp_path: Path) -> None:
    project = make_project(tmp_path / "manual", "coc-fiction")
    owner = service(tmp_path)
    owner.locator.register(project, "coc-fiction")

    assert owner.status("coc-fiction").local_state == "IDENTITY_MISMATCH"


def test_repository_identity_uses_the_raw_origin_not_insteadof_rewriting(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Documents" / "GitHub" / "Coc-Fiction", "coc-fiction")
    attacker = "https://evil.example/attacker.git"
    set_origin(project, attacker)
    subprocess.run(
        [
            "git",
            "-C",
            str(project),
            "config",
            "--local",
            f"url.{REPOSITORY_URL}.insteadOf",
            attacker,
        ],
        check=True,
    )

    assert service(tmp_path).status("coc-fiction").local_state == "IDENTITY_MISMATCH"


def test_clone_rejects_a_linked_asset_vault_without_touching_its_target(tmp_path: Path) -> None:
    source = make_project(tmp_path / "source-linked", "coc-fiction")
    set_origin(source)
    shutil.rmtree(source / ".asset-vault")
    outside = tmp_path / "outside"
    outside.mkdir()

    def clone_runner(repository_url: str, destination: Path) -> None:
        shutil.copytree(source, destination, dirs_exist_ok=True)
        (destination / ".asset-vault").symlink_to(outside, target_is_directory=True)

    result = service(tmp_path, clone_runner=clone_runner).onboard("coc-fiction")

    assert result.local_state == "PROJECT_SETUP_REQUIRED"
    assert list(outside.iterdir()) == []


def test_failed_clone_cleanup_never_deletes_a_substituted_directory(tmp_path: Path) -> None:
    replacement: dict[str, Path] = {}

    def replaced_clone(repository_url: str, destination: Path) -> None:
        held = destination.with_name(f"{destination.name}-held")
        destination.rename(held)
        destination.mkdir()
        marker = destination / "preexisting-user-data.txt"
        marker.write_text("keep", encoding="utf-8")
        replacement.update({"marker": marker, "held": held})
        raise RuntimeError("clone failed after path replacement")

    result = service(tmp_path, clone_runner=replaced_clone).onboard("coc-fiction")

    assert result.local_state == "CLONE_FAILED"
    assert replacement["marker"].read_text(encoding="utf-8") == "keep"
    assert replacement["held"].is_dir()
