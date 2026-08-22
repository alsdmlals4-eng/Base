# Copilot Repository Instructions Template

이 파일은 repository-wide 규칙을 전부 복제하는 문서가 아니라 **repository bootstrap**이다. 공통 진입점·정본 경계·검증 기준만 짧게 두고, 특정 경로·기능·엔진 규칙은 nearest `AGENTS.md` 또는 path-specific instructions와 현재 책임 원본에서 읽는다.

## Project

- Engine:
- Language:
- Main scenes:
- Main scripts:
- Data folder:
- Active Context:
- Documentation Map:

## Authority bootstrap

```text
latest user instruction
→ project AGENTS.md + security/engine/data rules
→ Active Context + approved work contract
→ registered domain canon + actual files/tests/runtime evidence
→ adopted current Base contract
→ external references / memory / inference
```

모든 과거 Base 파일을 고정 목록으로 읽지 않는다. 현재 Documentation Map, router, nearest `AGENTS.md`, path-specific instructions가 현재 작업에 필요한 owner를 결정한다.

## DOMAIN_SPLIT_CANON

- `NOTION_HUMAN_FACING_CANON`: 사람이 읽고 비교·수정하는 프로젝트 개요·기획·Visual/Asset·사람용 표·Flow/Storyboard.
- `REPOSITORY_STRUCTURED_CANON`: Markdown·JSON·게임 데이터·코드·씬·리소스·config·tests.
- `REPOSITORY_RUNTIME_TRUTH`: 실제 build/runtime/test evidence.
- Google Sheets는 unique unmigrated material이 남은 경우의 `MIGRATION_ONLY_UNTIL_REMOVAL` compatibility source다.

## Rules

- 현재 Issue/Goal/승인된 직접 요청 범위 밖 기능을 추가하지 않는다.
- 기존 사용자 변경과 현재 open PR 보호 규칙을 지킨다.
- 실제 파일과 현재 책임 원본을 확인한 뒤 수정한다.
- Notion 승인·정적 mockup·문서 문구를 runtime 성공으로 간주하지 않는다.
- 테스트하지 못한 항목은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 보고한다.
- repository-wide 지침과 path-specific 지침이 충돌하면 최신 사용자 지시와 더 구체적인 현재 프로젝트 규칙을 우선한다.

## Validation

- Run:
- Test:
- Manual check:
- Runtime evidence:
- Destination readback:
