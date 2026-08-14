from __future__ import annotations

from pathlib import Path

from test_api import client_for


def rendered_html(tmp_path: Path) -> str:
    response = client_for(tmp_path).get("/")
    assert response.status_code == 200
    return response.text


def test_project_first_structure(tmp_path: Path) -> None:
    html = rendered_html(tmp_path)
    for expected in (
        'id="project-registration"',
        'id="known-project"',
        'id="known-project-list"',
        'id="registered-project-list"',
        'id="tool-catalog"',
        'id="windows-launcher-install"',
        'id="hub-shutdown"',
        "프로젝트를 먼저 연결",
    ):
        assert expected in html, expected


def test_reviewed_tool_and_evidence_labels(tmp_path: Path) -> None:
    html = rendered_html(tmp_path)
    for expected in (
        "QA Evidence Studio",
        "Expression Studio",
        "Sprite Animation Studio",
        "ROUTING_REGISTERED",
        "ANCHOR_EVIDENCE_MISSING",
        "BLOCKED_UNVERIFIED",
        "INCLUDED_OR_LOCAL_HANDOFF",
        "Figma 업로드 증거가 아닙니다",
        "AI 생성 증거가 아닙니다",
    ):
        assert expected in html, expected


def test_no_raw_command_surface(tmp_path: Path) -> None:
    html = rendered_html(tmp_path)
    lowered = html.lower()
    for forbidden in ("command", "shell", "<iframe", "marketplace", "balance"):
        assert forbidden not in lowered, forbidden
    for forbidden in ("C:\\", "/home/", 'id="project-root"'):
        assert forbidden not in html, forbidden
