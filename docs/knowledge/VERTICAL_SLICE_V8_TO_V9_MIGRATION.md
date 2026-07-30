---
document_role: MIGRATION_TRACEABILITY
active_authority: false
implementation_authority: NONE
status: SUPERSEDED_COMPATIBILITY
current_execution_contract: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
---

# Vertical Slice v8 → v9 이관표

## 목적

v9는 v6~v8에서 이미 진행된 기획·정본·구현을 폐기하지 않는다. 이 문서는 과거 첨부물이 현재 실행 권한이 아님을 명확히 하고, 프로젝트별 복원·감사에서 어떤 항목을 비교해야 하는지 제공한다.

## 첨부 입력 식별

| 입력 | SHA-256 | 분류 | 처리 |
| --- | --- | --- | --- |
| 사용자 `VERTICAL_SLICE_MASTER_REFERENCE_v6.md` | `005B330261E70A2F4F1F0A51C0729C21EE3BF55CA0A0BE8178711691B35A6963` | `LEGACY_REFERENCE_INPUT` | 요구사항 추적에만 사용 |
| 사용자 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` | `62B2BA32E7CDDCCAD4BA0DA8A4FE018B92D7EBFCBEB3ECE1FC6C5E15161F08C0` | `LEGACY_REFERENCE_INPUT` | 비교에만 사용 |
| 사용자 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md` | `835EAEEC6205DD3D0BB5D9CE49A8B4940ED07A108E15F6C1B04299446FD5868F` | `LEGACY_REFERENCE_INPUT` | Base v8과 변형됨을 기록 |
| Base v9.0 릴리스 시점 v8 | `39AF1CAFE1C8D132667F68AC731AB970615E7B55A09AEA93CFB56141803D0506` | `LEGACY_REFERENCE_INPUT` | `585a53a25be1b04c543196f5901551deb49c7691`, blob `039c84d2f69d92ab81f72b4b101427b7b2cd2969`; 사용자 첨부 v8과 hash가 다름 |
| Base `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md` | `835EAEEC6205DD3D0BB5D9CE49A8B4940ED07A108E15F6C1B04299446FD5868F` | `SUPERSEDED_COMPATIBILITY` | `origin/main` `1fd27e1d65c1235166435eb4d87029fadf5a4f27`, blob `dfeaa9ef60f7f8f510650763a1f5b60b631b306f`; 삭제하지 않고 호환 이력 유지 |

사용자 첨부 v8과 Base v9.0 릴리스 시점 v8의 raw SHA-256은 다르다. 이후 Base v8은 `origin/main`에서 사용자 첨부와 같은 bytes가 되었지만, 어느 파일이 더 옳다고 가정하지 말고 각 조항을 최신 프로젝트 정본·구현·Decision에 대조한다.

## 이전 용어의 판정 규칙

| 이전 용어 | 자동 처리 금지 | 가능한 상태 | 필요한 근거 |
| --- | --- | --- | --- |
| `CORE_POC` | v9 Slice로 이름 변경 금지 | `CURRENT`, `LEGACY_REFERENCE_ALLOWED`, `CANON_CONFLICT`, `STALE_REFERENCE` | 현재 정본과 실제 구현 |
| `SLICE_VALIDATION` | 통과로 간주 금지 | 같은 네 상태 | 테스트/사람/기기 증거 |
| `VERTICAL_SLICE_FULL_PROFILE` | 현행 프로필로 승격 금지 | 같은 네 상태 | 프로젝트 Application Binding |
| v6~v8 Skill ID·경로 | 현재 route로 추측 치환 금지 | `CURRENT` 또는 legacy 상태 | Snapshot·Registry·실제 파일 |

## v9에서 보강한 책임

- `APPLICATION_BINDING`: Base 핀, Snapshot, router, 보호 경로, main, Sheet 상태를 첫 단계로 고정한다.
- `RECONCILIATION_PLANNING_PROFILE`: 첫 파동의 감사·계획과 구현/정본/Sheet 쓰기를 분리한다.
- `INTERMEDIATE_VISUAL_CHECKPOINT`: 현재 정본을 바탕으로 화면 해석 차이를 검토하되 생성물을 정본이나 런타임 증거로 승격하지 않는다.
- `Source / Consumer / Propagation Map`: 변경 전 소비자와 재조회 방법을 명시한다.
- `Critical Gate`: OM/PE 평균 점수로 보호 경계·사람/기기 미검증을 감추지 않는다.

## 유지되는 v8 원칙

`DUPLICATE_OMISSION_CONFLICT_AUDIT`, `EVIDENCE_PACK`, `APPROVAL_BUNDLE`, `PROPAGATION_AUDIT`, `DEMO_FIRST_VERTICAL_SLICE`, `DEMO_VALIDATION`, `TECHNICAL_SPIKE`, `PROJECT_SHEET_SEMANTIC_TABS`, `GPT_PLANNING_VISUALIZATION`, `GPT_FINAL_VISUAL_CANDIDATE_REVIEW`, `AGENT_MERGE_REQUIRED`은 폐기된 개념이 아니다. v9의 Application Binding과 감사 프로필 아래에서 프로젝트 상태에 맞게 사용한다.
