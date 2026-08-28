# Copilot Repository Instructions Template

이 파일은 repository-wide 규칙을 전부 복제하는 문서가 아니라 **repository bootstrap**이다. 공통 진입점·정본 경계·검증 기준만 짧게 두고, 특정 경로·기능·엔진 규칙은 nearest `AGENTS.md`, path-specific instructions와 현재 책임 원본에서 읽는다.

## Project

- Engine:
- Language:
- Main scenes:
- Main scripts:
- Data folder:
- Active Context:
- Confirmed Decisions:
- AI Canon:
- Asset Manifest:
- Current Handoff:
- Documentation Map:

## Authority bootstrap

```text
latest user instruction
→ project AGENTS.md + security/engine/data rules
→ Active Context + approved work contract + confirmed decisions
→ registered repository canon + actual files/assets/tests/runtime evidence
→ adopted current Base contract
→ legacy migration source when required
→ external references / memory / inference
```

모든 과거 Base 파일을 고정 목록으로 읽지 않는다. 현재 Documentation Map, router, nearest `AGENTS.md`, path-specific instructions가 현재 작업에 필요한 owner를 결정한다.

## REPOSITORY_PRIMARY_PROJECT_CANON

- `AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN`: 프로젝트 의미·시스템·콘텐츠·UX·데이터·구현 계약.
- repository Markdown·JSON·게임 데이터·코드·씬·리소스·config·tracked asset·tests가 구조화 정본을 소유한다.
- `REPOSITORY_RUNTIME_AND_EXECUTION_EVIDENCE`: 실제 build/runtime/test evidence.
- `HUMAN_GDD_PDF_DERIVED_VIEW`: exact repository commit에서 생성한 사람용 상세 기획서 PDF이며 독립 정본이 아니다.
- `CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON`과 `CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON`은 실행·참고 surface다.
- Notion과 Google Sheets는 unique unmigrated material이 남은 경우의 `LEGACY_READ_ONLY_MIGRATION_SOURCE`다.

## Rules

- 현재 Issue/Goal/승인된 직접 요청 범위 밖 기능을 추가하지 않는다.
- 기존 사용자 변경과 현재 open PR 보호 규칙을 지킨다.
- 실제 파일과 current owner를 확인한 뒤 수정한다.
- 신규 Notion page/database/write/upload/sync/readback을 기본 작업이나 완료 조건으로 만들지 않는다.
- legacy source를 읽지 못하면 `BLOCKED_UNVERIFIED`로 남기고 duplicate/obsolete로 추정하지 않는다.
- 사람용 PDF·Work·Library·memory·legacy Notion을 repository current truth로 승격하지 않는다.
- actual implementation asset은 repository path, consumer, approval/version, SHA-256, provenance와 implementation status를 가져야 한다.
- 정적 mockup·문서 문구·PDF render PASS를 runtime 성공으로 간주하지 않는다.
- 테스트하지 못한 항목은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 보고한다.
- repository-wide 지침과 path-specific 지침이 충돌하면 최신 사용자 지시와 더 구체적인 현재 프로젝트 규칙을 우선한다.

## Codex/Godot implementation boundary

실제 Godot 제품 구현은 exact repository commit과 current handoff를 사용한다.

```text
EXACT_REPOSITORY_COMMIT
→ AGENTS / Active Context / confirmed decisions / AI canon
→ actual code/data/Scene/Resource/test/evidence
→ REPOSITORY_PATH_MANIFEST_SHA256_READBACK
→ bounded product implementation
→ test/runtime/play evidence
```

Notion 부재만으로 구현을 막지 않는다. 필요한 asset이 repository path와 manifest에 없으면 `GPT_VISUAL_REQUEST` 또는 명시적 blocker로 반환한다.

## Validation

- Source branch:
- Source commit:
- Run:
- Test:
- Manual check:
- Runtime evidence:
- Asset manifest readback:
- Destination readback:
- Evidence ceiling:
- Not run / blocked:
