from __future__ import annotations

from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
import subprocess
import time

import httpx
from PIL import Image
import pytest

from test_api import client_for
from test_projects import make_project


FIGMA_ROUTES = {
    "coc-fiction": "PEa5zDbPHll3eHiNKX0e1k",
    "ten-paces-hidden-moves": "pVQ2e6aK45iL8BLBJWDSw4",
}


def png(color: tuple[int, int, int, int]) -> bytes:
    output = BytesIO()
    Image.new("RGBA", (8, 8), color).save(output, format="PNG")
    return output.getvalue()


def figma_node_url(project_id: str) -> str:
    return f"https://www.figma.com/design/{FIGMA_ROUTES[project_id]}/smoke-anchor?node-id=1-2"


def make_visual_project(root: Path, project_id: str) -> Path:
    project = make_project(root, project_id)
    sources = {
        "art/source/hero.png": png((245, 245, 245, 255)),
        "art/source/idle.png": png((220, 220, 220, 255)),
        "art/source/effect.png": png((180, 180, 180, 180)),
    }
    for relative, data in sources.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    anchors = {
        "version": 1,
        "entries": [
            {
                "project_id": project_id,
                "source_path": relative,
                "figma_node_url": figma_node_url(project_id),
                "source_sha256": sha256(data).hexdigest(),
                "approval_state": "APPROVED",
                "evidence": {
                    "kind": "EXPORTED_SNAPSHOT",
                    "ref": f"fixture://{project_id}/{Path(relative).stem}",
                    "checked_at": "2026-08-13T00:00:00Z",
                },
            }
            for relative, data in sources.items()
        ],
    }
    registry = project / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    registry.parent.mkdir(parents=True, exist_ok=True)
    registry.write_text(json.dumps(anchors, indent=2) + "\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(project), "add", "art", "docs/APPROVED_VISUAL_ANCHORS.json"], check=True)
    subprocess.run(["git", "-C", str(project), "commit", "-qm", "canonical visual smoke fixtures"], check=True)
    return project


def studio_client(url: str) -> httpx.Client:
    client = httpx.Client(base_url=url, headers={"Origin": url}, timeout=20)
    config = client.get("/api/config")
    config.raise_for_status()
    client.headers["X-Studio-CSRF"] = config.json()["csrf_token"]
    return client


def expression_request(project_id: str) -> dict[str, object]:
    return {
        "project_id": project_id,
        "asset_id": "hero",
        "anchor": {
            "source_path": "art/source/hero.png",
            "figma_node_url": figma_node_url(project_id),
            "approval_status": "approved",
        },
        "controls": [{"code": "AU46", "intensity": "C", "side": "left"}],
        "gaze": "center",
        "head_pose": "neutral",
        "candidate_count": 2,
    }


def sprite_request(project_id: str, *, effect: bool) -> dict[str, object]:
    return {
        "project_id": project_id,
        "asset_id": "impact" if effect else "hero",
        "asset_kind": "effect" if effect else "character",
        "mode": "effect_stages" if effect else "sprite_action",
        "anchor": {
            "source_path": "art/source/effect.png" if effect else "art/source/idle.png",
            "figma_node_url": figma_node_url(project_id),
            "approval_status": "approved",
        },
        "action": {
            "name": "burst" if effect else "attack",
            "direction": "none" if effect else "left",
            "frame_count": 4,
            "fps": 8,
            "loop_mode": "none",
            "prompt": "Four reviewed import frames for the Linux Tool Hub smoke.",
        },
    }


def import_expression(client: httpx.Client, project_id: str) -> tuple[dict[str, object], dict[str, object]]:
    response = client.post(
        "/api/import-runs",
        data={"request_json": json.dumps(expression_request(project_id)), "declared_source": "CHATGPT_INCLUDED"},
        files=[
            ("candidates", ("candidate-0.png", png((220, 30, 30, 255)), "image/png")),
            ("candidates", ("candidate-1.png", png((30, 30, 220, 255)), "image/png")),
        ],
    )
    response.raise_for_status()
    imported = response.json()
    exported_response = client.post(
        f"/api/runs/{imported['run_id']}/export", json={"selected_candidate": 1}
    )
    exported_response.raise_for_status()
    exported = exported_response.json()
    assert exported["status"] == "exported"
    assert exported["selected_candidate"] == 1
    return imported, exported


def import_sprite(
    client: httpx.Client, project_id: str, *, effect: bool
) -> tuple[dict[str, object], dict[str, object]]:
    colors = [
        (20, 40, 60, 255),
        (60, 80, 100, 255),
        (100, 120, 140, 255),
        (140, 160, 180, 255),
    ]
    response = client.post(
        "/api/import-runs",
        data={"request_json": json.dumps(sprite_request(project_id, effect=effect)), "declared_source": "LOCAL_GENERATOR"},
        files=[("frames", (f"frame-{index}.png", png(color), "image/png")) for index, color in enumerate(colors)],
    )
    response.raise_for_status()
    imported = response.json()
    curation = {"selected": [0, 1, 2, 3], "transforms": {}, "rejected": []}
    exported_response = client.post(f"/api/runs/{imported['run_id']}/export", json=curation)
    exported_response.raise_for_status()
    exported = exported_response.json()
    assert exported["status"] == "exported"
    assert exported["selected"] == [0, 1, 2, 3]
    return imported, exported


def run_directory(project: Path, run_id: str) -> Path:
    matches = [path for path in (project / ".asset-vault" / "library" / "generated").rglob(run_id) if path.is_dir()]
    assert len(matches) == 1
    return matches[0]


def assert_process_exited(process_id: int) -> None:
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            os.kill(process_id, 0)
        except ProcessLookupError:
            return
        time.sleep(0.05)
    pytest.fail(f"child process {process_id} survived Tool Hub lifespan shutdown")


@pytest.mark.skipif(__import__("sys").platform != "linux", reason="real four-child lifecycle evidence is Linux-only")
def test_linux_four_process_import_workflows_are_project_isolated(tmp_path: Path) -> None:
    left = make_visual_project(tmp_path / "Project Alpha With Spaces", "coc-fiction")
    right = make_visual_project(tmp_path / "Project Beta With Spaces", "ten-paces-hidden-moves")
    hub = client_for(tmp_path)
    studio_clients: list[httpx.Client] = []
    process_ids: list[int] = []
    with hub:
        try:
            assert hub.post(
                "/api/projects", json={"project_id": "coc-fiction", "project_root": str(left)}
            ).status_code == 201
            assert hub.post(
                "/api/projects",
                json={"project_id": "ten-paces-hidden-moves", "project_root": str(right)},
            ).status_code == 201
            launches: dict[tuple[str, str], dict[str, object]] = {}
            for project_id in ("coc-fiction", "ten-paces-hidden-moves"):
                for tool_id in ("expression-studio", "sprite-animation-studio"):
                    response = hub.post("/api/launch", json={"tool_id": tool_id, "project_id": project_id})
                    assert response.status_code == 200, response.text
                    launches[(project_id, tool_id)] = response.json()

            ports = {urlsplit(str(launch["url"])).port for launch in launches.values()}
            assert None not in ports
            assert len(ports) == 4
            statuses: dict[tuple[str, str], dict[str, object]] = {}
            for key, launch in launches.items():
                child = studio_client(str(launch["url"]))
                studio_clients.append(child)
                config = child.get("/api/config").json()
                status = child.get("/api/status").json()
                statuses[key] = status
                assert config["run_mode"] == "subscription_handoff_import"
                assert config["cost_route"] == "INCLUDED_OR_LOCAL_HANDOFF"
                assert config["provider_call_made"] is False
                assert status["project_id"] == key[0]
                assert status["tool_id"] == key[1]
                assert status["status"] == "ready"
                assert status["engine_provenance"] == "subscription_handoff_import"
            process_ids = [int(status["process_id"]) for status in statuses.values()]
            assert len(set(process_ids)) == 4

            clients = dict(zip(launches, studio_clients, strict=True))
            expression_run, expression_export = import_expression(
                clients[("coc-fiction", "expression-studio")], "coc-fiction"
            )
            action_run, action_export = import_sprite(
                clients[("coc-fiction", "sprite-animation-studio")], "coc-fiction", effect=False
            )
            effect_run, effect_export = import_sprite(
                clients[("ten-paces-hidden-moves", "sprite-animation-studio")],
                "ten-paces-hidden-moves",
                effect=True,
            )

            for run in (
                expression_run,
                expression_export,
                action_run,
                action_export,
                effect_run,
                effect_export,
            ):
                assert run["run_mode"] == "subscription_handoff_import"
                assert run["cost_route"] == "INCLUDED_OR_LOCAL_HANDOFF"
                assert run["provider_call_made"] is False
            assert expression_run["candidate_count"] == 2
            assert action_run["frame_count"] == 4
            assert effect_run["frame_count"] == 4
            packets = json.dumps(
                [expression_run, expression_export, action_run, action_export, effect_run, effect_export],
                sort_keys=True,
            )
            assert str(left.resolve()) not in packets
            assert str(right.resolve()) not in packets

            expression_dir = run_directory(left, str(expression_run["run_id"]))
            action_dir = run_directory(left, str(action_run["run_id"]))
            effect_dir = run_directory(right, str(effect_run["run_id"]))
            assert left.resolve() in expression_dir.resolve().parents
            assert left.resolve() in action_dir.resolve().parents
            assert right.resolve() in effect_dir.resolve().parents
            assert not list(right.rglob(str(expression_run["run_id"])))
            assert not list(right.rglob(str(action_run["run_id"])))
            assert not list(left.rglob(str(effect_run["run_id"])))
        finally:
            for client in studio_clients:
                client.close()

    for process_id in process_ids:
        assert_process_exited(process_id)
    assert not list((tmp_path / "runtime").glob("launch-*"))
