from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_p01_intake_uses_notion_default_and_sheets_only_for_legacy_migration() -> None:
    skill = text("skills/managing-project-intake-and-work-contract/SKILL.md")

    for token in (
        "NOTION_DEFAULT_PROJECT_WORKSPACE",
        "NOTION_HUMAN_FACING_CANON",
        "COMPATIBILITY_ONLY",
        "google_sheet_compatibility_source",
    ):
        assert token in skill

    assert "USER_FACING_GDD_WORKSPACE" not in skill
    assert "project_google_sheet:" not in skill


def test_p01_project_os_uses_notion_as_human_workspace_not_google_sheets() -> None:
    skill = text("skills/managing-game-project-operating-system/SKILL.md")

    for token in (
        "NOTION_DEFAULT_PROJECT_WORKSPACE",
        "NOTION_HUMAN_FACING_CANON",
        "REPOSITORY_STRUCTURED_CANON",
        "COMPATIBILITY_ONLY",
        "google_sheet_compatibility_source",
    ):
        assert token in skill

    assert "USER_FACING_GDD_WORKSPACE" not in skill
    assert "project_google_sheet:" not in skill


def test_grill_me_batch_does_not_require_google_sheets_for_active_sync() -> None:
    policy = text("docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md")

    for token in (
        "NOTION_HUMAN_FACING_CANON",
        "REPOSITORY_STRUCTURED_CANON",
        "COMPATIBILITY_ONLY",
        "destination readback",
    ):
        assert token in policy

    assert "구성된 Sheet 행을 APPROVED_PENDING_MERGE로 기록·재조회" not in policy
    assert "Decision ID·Branch Commit·정본 내용·Sheet 행 불일치" not in policy


def test_stricter_work_contract_can_forbid_open_pr_absorption() -> None:
    intake = text("skills/managing-project-intake-and-work-contract/SKILL.md")
    continuous = text(
        "skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md"
    )

    for source in (intake, continuous):
        assert "STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION" in source
        assert "explicit absorption authorization" in source
