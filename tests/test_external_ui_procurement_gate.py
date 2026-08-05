from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_external_ui_gate_is_fail_closed_and_platform_aware() -> None:
    reference = read(
        "skills/auditing-and-refining-ui-art/references/"
        "ux-ui-design-system-method.md"
    )
    for token in (
        "registry_source",
        "exact_version_or_commit",
        "content_hash",
        "license",
        "dependencies",
        "scripts",
        "secrets",
        "files_added_or_replaced",
        "accessibility_review",
        "runtime_review",
        "rollback",
        "BLOCKED_UNVERIFIED",
        "ADOPT",
        "ADAPT",
        "REJECT",
    ):
        assert token in reference
    assert "MCP 연결 성공" in reference
    assert "설치 승인" in reference
    assert "Godot" in reference
    assert "Web" in reference
    assert "Design Read" in reference
    assert "실제 렌더" in reference


def test_ui_method_routes_procurement_only_when_external_code_is_requested() -> None:
    skill = read("skills/auditing-and-refining-ui-art/SKILL.md")
    method = read(
        "skills/auditing-and-refining-ui-art/references/"
        "ux-ui-design-system-method.md"
    )
    assert "ux-ui-design-system-method.md" in skill
    assert "### 6.2 External UI Procurement and Anti-Generic Quality Gate" in method
    assert "외부 Web UI" in method
    assert "기본 설치" not in skill