from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: str, replacements: list[tuple[str, str]]) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    for old, new in replacements:
        if old not in text:
            raise SystemExit(f"MISSING_PATTERN {path}: {old}")
        text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")

patch(
    "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md",
    [
        ("GOOGLE_SHEETS_COMPATIBILITY_ONLY", "GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL"),
        ("EXTERNAL_HTML_TOOL_CATALOG: DERIVED_DISCOVERY_SURFACE", "EXTERNAL_HTML_WORKSPACE_RETIRED"),
        ("### `GOOGLE_SHEETS_COMPATIBILITY_ONLY`", "### `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL`"),
        ("기존 Google Sheet는 고유 unmigrated material이 남아 있을 때만 compatibility/migration source로 읽는다. 검증된 migration과 readback 뒤에는 새 프로젝트 작업면으로 사용하지 않는다.", "기존 Google Sheet는 고유 unmigrated material을 한 번 이관하기 위한 migration-only source다. `UNIQUE / DUPLICATE / OBSOLETE` 분류와 destination readback 뒤 unique material이 0이면 활성 검색·라우팅·템플릿에서 제거한다."),
        ("### `EXTERNAL_HTML_TOOL_CATALOG: DERIVED_DISCOVERY_SURFACE`", "### `EXTERNAL_HTML_WORKSPACE_RETIRED`"),
        ("외부 HTML catalog/dashboard는 발견·보조 surface일 뿐 정본이나 실행 증거가 아니다.", "외부 HTML catalog/dashboard는 신규 기본 작업면으로 사용하지 않는다. 고유 정보가 있으면 현재 Notion/repository owner로 한 번 흡수·검증한 뒤 활성 surface와 참조를 제거한다."),
    ],
)

patch(
    "skills/running-adversarial-review-and-refinement/SKILL.md",
    [
        ("정본·실제 diff·Sheets·PR·branch", "정본·실제 diff·Notion/GitHub sync·PR·branch"),
        ("google_sheet_state:", "notion_and_repository_sync_state:"),
        ("Google Sheets 또는 Repository 설정을 읽지 못했으면", "Notion 또는 Repository 설정을 읽지 못했으면"),
        ("CI·런타임·렌더·Sheets 조회·branch 삭제", "CI·런타임·렌더·Notion readback·branch 삭제"),
        ("Base Template·프로젝트 Sheet·프로젝트 상태의 권한", "Base Template·프로젝트 Notion·프로젝트 상태의 권한"),
        ("GitHub `main`과 프로젝트 Google Sheets의 Decision·Commit·대체 관계", "GitHub `main`과 프로젝트 Notion의 Decision·Commit·대체 관계"),
        ("→ Google Sheets\n", "→ Project Notion\n"),
        ("GitHub와 Sheets가 다르면", "GitHub와 Notion이 다르면"),
        ("diff·Sheets·적용 검증", "diff·Notion readback·적용 검증"),
        ("프로젝트가 Sheets를 사용하면 해당 Decision 행을 재조회했다.", "사람용 변경이 있으면 정확한 Project의 Notion destination을 readback했다."),
    ],
)

patch(
    "tests/test_base_long_horizon_work_contract.py",
    [
        ("\"GOOGLE_SHEETS_COMPATIBILITY_ONLY\",", "\"GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL\","),
        ("\"EXTERNAL_HTML_TOOL_CATALOG: DERIVED_DISCOVERY_SURFACE\",", "\"EXTERNAL_HTML_WORKSPACE_RETIRED\","),
    ],
)

Path(__file__).unlink()
print("RETIRED_SURFACES_RECONCILED")
