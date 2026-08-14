import json
from pathlib import Path
import subprocess

from fastapi.testclient import TestClient

from test_projects import make_project
from tool_hub.app import create_app


BASE_ROOT = Path(__file__).resolve().parents[3]


def client_for(
    tmp_path: Path,
    *,
    bootstrap: bool = True,
    onboarding_home: Path | None = None,
) -> TestClient:
    client = TestClient(
        create_app(
            BASE_ROOT,
            tmp_path / "machine-projects.json",
            bind_origin="http://testserver",
            test_mode=True,
            onboarding_home=onboarding_home,
            managed_project_root=(onboarding_home / "Documents" / "GitHub") if onboarding_home else None,
        )
    )
    client.headers["Origin"] = "http://testserver"
    if bootstrap:
        config = client.get("/api/config").json()
        client.headers["X-Hub-CSRF"] = config["csrf_token"]
    return client


def test_platform_without_descriptor_runtime_starts_in_catalog_only_mode(tmp_path: Path) -> None:
    client = TestClient(
        create_app(
            BASE_ROOT,
            tmp_path / "machine-projects.json",
            bind_origin="http://testserver",
            test_mode=True,
            launch_supported=False,
        )
    )

    response = client.get("/api/catalog")

    assert response.status_code == 200
    assert {
        item["tool_id"]: item["launch_state"] for item in response.json()["tools"]
    } == {
        "expression-studio": "BLOCKED_PLATFORM",
        "qa-evidence-studio": "BLOCKED_PLATFORM",
        "sprite-animation-studio": "BLOCKED_PLATFORM",
    }


def test_catalog_lists_reviewed_tools_and_redacts_registered_root(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Project With Spaces", "coc-fiction")
    client = client_for(tmp_path)

    created = client.post(
        "/api/projects",
        json={"project_id": "coc-fiction", "project_root": str(project)},
    )
    catalog = client.get("/api/catalog").json()

    assert created.status_code == 201
    assert [item["tool_id"] for item in catalog["tools"]] == [
        "expression-studio",
        "qa-evidence-studio",
        "sprite-animation-studio",
    ]
    assert catalog["projects"][0]["project_id"] == "coc-fiction"
    assert catalog["projects"][0]["display_name"] == "coc소설"
    assert str(project.resolve()) not in str(catalog)


def test_catalog_lists_known_projects_separately_from_machine_registrations(tmp_path: Path) -> None:
    catalog = client_for(tmp_path).get("/api/catalog").json()

    assert catalog["projects"] == []
    assert [project["project_id"] for project in catalog["known_projects"]] == [
        "coc-fiction",
        "ten-paces-hidden-moves",
        "ninja-survival",
        "switchy-express-cargo-puzzle",
        "urban-legend",
        "grimoire-how-to-rewrite-the-world",
        "blacksmith",
        "omenward",
    ]
    assert catalog["known_projects"][0] == {
        "project_id": "coc-fiction",
        "display_name": "coc소설",
        "repository_name": "Coc-Fiction",
        "routing_state": "ROUTING_REGISTERED",
        "local_state": "CLONE_AVAILABLE",
        "action_label": "자동 설치 및 연결",
    }
    assert "figma_file_key" not in str(catalog)
    assert "figma_url" not in str(catalog)


def test_onboard_endpoint_finds_an_exact_checkout_without_a_browser_path(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Documents" / "GitHub" / "Coc-Fiction", "coc-fiction")
    subprocess.run(
        ["git", "-C", str(project), "remote", "set-url", "origin", "https://github.com/alsdmlals4-eng/Coc-Fiction.git"],
        check=True,
    )
    client = client_for(tmp_path, onboarding_home=tmp_path)

    response = client.post("/api/projects/coc-fiction/onboard", json={})

    assert response.status_code == 200
    assert response.json()["local_state"] == "REGISTERED"
    assert str(tmp_path) not in response.text
    assert client.get("/api/catalog").json()["projects"][0]["project_id"] == "coc-fiction"


def test_onboard_endpoint_runs_a_real_git_clone_for_an_absent_project(tmp_path: Path) -> None:
    source = make_project(tmp_path / "fixture-remote" / "omenward", "omenward")
    adapter = json.loads(
        (source / "skills" / "PROJECT_BASE_ADAPTER.json").read_text(encoding="utf-8")
    )
    protected_baseline = adapter["protected_baseline"]["commit"]

    def real_git_clone(repository_url: str, destination: Path) -> None:
        subprocess.run(
            ["git", "clone", "--no-local", "--", str(source), str(destination)],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(destination), "remote", "set-url", "origin", repository_url],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(destination),
                "update-ref",
                "refs/remotes/origin/main",
                protected_baseline,
            ],
            check=True,
        )

    client = TestClient(
        create_app(
            BASE_ROOT,
            tmp_path / "machine-projects.json",
            bind_origin="http://testserver",
            test_mode=True,
            onboarding_home=tmp_path,
            managed_project_root=tmp_path / "Documents" / "GitHub",
            onboarding_clone_runner=real_git_clone,
        )
    )
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Hub-CSRF"] = config["csrf_token"]

    response = client.post("/api/projects/omenward/onboard", json={})

    assert response.status_code == 200
    assert response.json()["local_state"] == "REGISTERED"
    final = tmp_path / "Documents" / "GitHub" / "omenward"
    assert final.is_dir()
    assert subprocess.run(
        ["git", "-C", str(final), "rev-parse", "--is-inside-work-tree"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip() == "true"


def test_onboard_endpoint_rejects_unknown_projects_and_request_fields(tmp_path: Path) -> None:
    client = client_for(tmp_path, onboarding_home=tmp_path)

    assert client.post("/api/projects/not-reviewed/onboard", json={}).status_code == 422
    extra = client.post("/api/projects/coc-fiction/onboard", json={"repository_url": "https://evil.example/repo.git"})

    assert extra.status_code == 422


def test_launcher_status_is_token_bound_and_shutdown_is_csrf_protected(tmp_path: Path) -> None:
    stopped: list[str] = []
    app = create_app(
        BASE_ROOT,
        tmp_path / "projects.json",
        bind_origin="http://testserver",
        test_mode=True,
        launch_supported=False,
        launcher_token="launcher-secret",
        shutdown_callback=lambda: stopped.append("stop"),
    )
    client = TestClient(app)

    assert client.get("/api/launcher-status").status_code == 403
    status = client.get("/api/launcher-status", headers={"X-Hub-Launcher-Token": "launcher-secret"})
    assert status.status_code == 200
    assert status.json()["tool_id"] == "base-tool-hub"
    assert len(status.json()["project_config_fingerprint"]) == 64
    assert len(status.json()["hub_runtime_fingerprint"]) == 64
    assert "base_root" not in status.text

    assert client.post("/api/shutdown", json={}).status_code == 403
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Hub-CSRF"] = config["csrf_token"]
    shutdown = client.post("/api/shutdown", json={})
    assert shutdown.status_code == 200
    assert shutdown.json() == {"state": "SHUTTING_DOWN"}
    assert stopped == ["stop"]


def test_windows_launcher_install_endpoint_has_no_path_or_command_payload(tmp_path: Path) -> None:
    class FakeInstaller:
        def install(self):
            class Result:
                def public_view(self):
                    return {"state": "INSTALLED", "desktop_entry": "Base Tool Hub.lnk"}
            return Result()

        def status(self):
            return "NOT_INSTALLED"

    client = TestClient(create_app(
        BASE_ROOT,
        tmp_path / "projects.json",
        bind_origin="http://testserver",
        test_mode=True,
        windows_launcher_installer=FakeInstaller(),
    ))
    client.headers["Origin"] = "http://testserver"
    config = client.get("/api/config").json()
    client.headers["X-Hub-CSRF"] = config["csrf_token"]

    assert client.post("/api/windows-launcher/install", json={}).json()["state"] == "INSTALLED"
    assert client.post("/api/windows-launcher/install", json={"command": "evil"}).status_code == 422


def test_registration_requires_catalog_id_to_match_the_project_adapter(tmp_path: Path) -> None:
    project = make_project(tmp_path / "Project With Spaces", "coc-fiction")
    client = client_for(tmp_path)

    mismatch = client.post(
        "/api/projects",
        json={"project_id": "omenward", "project_root": str(project)},
    )
    unknown = client.post(
        "/api/projects",
        json={"project_id": "demo-game", "project_root": str(project)},
    )
    accepted = client.post(
        "/api/projects",
        json={"project_id": "coc-fiction", "project_root": str(project)},
    )

    assert mismatch.status_code == 422
    assert mismatch.json()["detail"] == "PROJECT_IDENTITY_MISMATCH"
    assert unknown.status_code == 422
    assert unknown.json()["detail"] == "PROJECT_CATALOG_ENTRY_REQUIRED"
    assert accepted.status_code == 201
    assert accepted.json()["project_id"] == "coc-fiction"


def test_mutation_requires_exact_origin_session_and_csrf(tmp_path: Path) -> None:
    project = make_project(tmp_path / "demo")
    raw = client_for(tmp_path, bootstrap=False)
    missing = raw.post("/api/projects", json={"project_root": str(project)})
    client = client_for(tmp_path)
    foreign = client.post(
        "/api/projects",
        json={"project_root": str(project)},
        headers={"Origin": "https://evil.example"},
    )
    hostile_host = client.post(
        "/api/projects", json={"project_root": str(project)}, headers={"Host": "evil.example"}
    )

    assert missing.status_code == 403
    assert foreign.status_code == 403
    assert hostile_host.status_code == 400


def test_project_registration_error_is_bounded(tmp_path: Path) -> None:
    response = client_for(tmp_path).post(
        "/api/projects",
        json={"project_id": "coc-fiction", "project_root": str(tmp_path / "secret-path")},
    )

    assert response.status_code == 422
    assert str(tmp_path) not in response.json()["detail"]


def make_visual_project(root: Path, project_id: str) -> Path:
    project = make_project(root, project_id)
    anchors = project / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    anchors.parent.mkdir(exist_ok=True)
    anchors.write_text('{"version":1,"entries":[]}', encoding="utf-8")
    subprocess.run(["git", "-C", str(project), "add", "docs/APPROVED_VISUAL_ANCHORS.json"], check=True)
    subprocess.run(["git", "-C", str(project), "commit", "-qm", "visual anchors"], check=True)
    return project


def test_visual_studios_launch_only_for_a_registered_verified_project(tmp_path: Path) -> None:
    project = make_visual_project(tmp_path / "Project With Spaces", "coc-fiction")
    client = client_for(tmp_path)
    with client:
        missing = client.post(
            "/api/launch", json={"tool_id": "expression-studio", "project_id": "coc-fiction"}
        )
        assert missing.status_code == 409

        assert client.post(
            "/api/projects",
            json={"project_id": "coc-fiction", "project_root": str(project)},
        ).status_code == 201
        expression = client.post(
            "/api/launch", json={"tool_id": "expression-studio", "project_id": "coc-fiction"}
        )
        sprite = client.post(
            "/api/launch", json={"tool_id": "sprite-animation-studio", "project_id": "coc-fiction"}
        )

        assert expression.status_code == 200
        assert sprite.status_code == 200
        assert expression.json()["status"] == "RUNNING"
        assert sprite.json()["status"] == "RUNNING"
        assert expression.json()["url"] != sprite.json()["url"]
        assert str(project.resolve()) not in expression.text + sprite.text


def test_blocked_visual_start_cannot_affect_qa_or_another_project(tmp_path: Path) -> None:
    qa_project = make_project(tmp_path / "qa-project", "omenward")
    visual_project = make_visual_project(tmp_path / "visual-project", "ten-paces-hidden-moves")
    client = client_for(tmp_path)
    with client:
        assert client.post(
            "/api/projects", json={"project_id": "omenward", "project_root": str(qa_project)}
        ).status_code == 201
        assert client.post(
            "/api/projects",
            json={"project_id": "ten-paces-hidden-moves", "project_root": str(visual_project)},
        ).status_code == 201
        qa = client.post(
            "/api/launch", json={"tool_id": "qa-evidence-studio", "project_id": "omenward"}
        )
        blocked = client.post(
            "/api/launch", json={"tool_id": "expression-studio", "project_id": "omenward"}
        )
        other = client.post(
            "/api/launch",
            json={"tool_id": "sprite-animation-studio", "project_id": "ten-paces-hidden-moves"},
        )
        repeated_qa = client.post(
            "/api/launch", json={"tool_id": "qa-evidence-studio", "project_id": "omenward"}
        )

        assert qa.status_code == 200
        assert blocked.status_code == 409
        assert other.status_code == 200
        assert repeated_qa.status_code == 200
        assert repeated_qa.json()["url"] == qa.json()["url"]
        assert other.json()["url"] != qa.json()["url"]
