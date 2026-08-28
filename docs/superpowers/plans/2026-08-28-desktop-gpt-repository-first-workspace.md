# Desktop GPT Repository-First Workspace 전환 구현 계획

> 상태: `IMPLEMENTATION_IN_PROGRESS`
> 기준 main: `af870522d15abf391a0b13553de690514ac8579a`
> 사용자 승인: 2026-08-28 — Desktop GPT 사용으로 Notion 중간 작업을 제거하고 작업 효율을 최적화

## 1. 목표

프로젝트 작업의 기본 경로를 다음으로 교정한다.

```text
Desktop GPT Work에서 기획·조사·검수·시각자료 제작
→ 프로젝트 repository 정본 갱신
→ 필요 Gate에서 사람용 상세 기획서 PDF 생성
→ exact repository SHA 기준 Codex 구현 인계
→ 구현·테스트·runtime evidence를 repository에 반영
```

Notion은 더 이상 필수 작업면·사람용 정본·이미지 delivery gate가 아니다. 기존 Notion-only 자료가 있는 프로젝트에서는 자료 손실을 막기 위한 migration source로만 읽고, 신규 쓰기는 기본 중단한다.

## 2. 대안 비교와 결정

### A. 기존 Notion 필수 흐름 유지 — REJECT

- 장점: 기존 문서와 테스트를 그대로 유지할 수 있다.
- 단점: Work → Notion → repository 이중 작성, 이중 readback, 정본 drift가 계속된다.
- 판정: 현재 1인 Desktop GPT 중심 운영에서 유지비가 가치보다 크다.

### B. Notion과 repository를 동등 선택지로 운영 — REJECT

- 장점: 프로젝트마다 자유롭게 선택할 수 있다.
- 단점: 어느 쪽이 current인지 매번 판정해야 하고 Codex 인계가 불안정해진다.
- 판정: 전환기 compatibility에는 사용할 수 있으나 장기 기본값으로는 부적합하다.

### C. repository 단일 정본 + PDF 파생뷰 + Notion legacy read-only — ADOPT

- 장점: Git diff·PR·SHA·rollback·runtime path와 기획 정본이 한곳에 모인다.
- 장점: 사람은 PDF로 전체를 검토하고 AI/Codex는 Markdown·JSON·asset manifest를 직접 소비한다.
- 단점: 기존 Notion-only 고유 자료를 프로젝트별로 한 번 이관해야 한다.
- 판정: 장기 총비용, 추적성, 구현 인계, 자료 손실 방지 측면에서 최선이다.

## 3. 변경 범위

### 새 활성 owner

- `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`
- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`

### 항상 적용되는 route

- root `AGENTS.md`

### 이관 도구

- `templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md`

### 회귀 계약

- `tests/test_repository_first_workspace_contract.py`

## 4. 동시성 경계

- 모든 기존 open/draft PR은 read-only다.
- PR #660이 소유한 `docs/DOCUMENTATION_MAP.md`, `tests/test_notion_project_workspace_contract.py` 등은 수정하지 않는다.
- 기존 `PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` V3와 역사 Notion 문서는 삭제하지 않는다.
- V3는 전환기 compatibility/역사 계약으로 남기고, root `AGENTS.md`가 V4를 active contract로 라우팅한다.
- PR #660 종료 뒤 별도 후속에서 V3 테스트·문서의 명칭과 compatibility 상태를 정리할 수 있다. 이 후속은 현재 전환의 기능적 완료 조건이 아니다.

## 5. 구현 순서

1. RED-first focused test를 추가한다.
2. V4 machine contract를 추가한다.
3. repository-first human policy를 추가한다.
4. Notion migration checklist를 추가한다.
5. root `AGENTS.md`의 workspace·정본·postmerge route를 교정한다.
6. branch diff와 exact file readback을 확인한다.
7. focused test와 repository CI를 exact HEAD에서 확인한다.
8. 최소 5회 전체 결과 적대적 검토를 수행한다.
9. review thread·required check·latest-main reconciliation 뒤 squash merge한다.
10. postmerge main readback과 남은 작업을 재계산한다.

## 6. Acceptance Criteria

- root `AGENTS.md`가 `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`와 V4 contract를 active owner로 지시한다.
- 신규 프로젝트 작업은 `NO_NEW_NOTION_WRITE_BY_DEFAULT`다.
- repository가 기획·데이터·에셋·구현·테스트·evidence의 primary canon이다.
- 사람용 PDF는 `PDF_IS_DERIVED_SNAPSHOT_NOT_CANON`이며 source SHA를 가진다.
- AI용 상세 기획·구현 명세는 repository Markdown으로 저장된다.
- Codex는 `CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA`를 따른다.
- 승인 이미지 소비는 repository path + SHA-256 + asset manifest로 검증한다.
- ChatGPT Work와 Library는 정본으로 승격되지 않는다.
- 기존 Notion 자료는 삭제하지 않고 zero-count migration gate로 보호한다.
- 기존 open PR 소유 경계를 침범하지 않는다.

## 7. 이관 완료 Gate

프로젝트별로 다음 값이 모두 0이어야 Notion을 active dependency에서 제거했다고 판정한다.

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

이전까지는 `LEGACY_READ_ONLY`다. 완전 퇴역을 위해 Notion 공간을 삭제할 필요는 없다: `NO_DELETE_REQUIRED_FOR_RETIREMENT`.

## 8. 검증 상한

이 Base 변경은 **새 기본 운영 계약**을 확립한다. 각 프로젝트의 실제 Notion-only 자료 이관 완료, 모든 runtime asset의 repository 존재, 사용자 PDF 시각 검수 완료까지 자동으로 증명하지 않는다. 해당 증거는 프로젝트별 checklist와 exact repository readback으로 따로 확보한다.

## 9. Rollback

문제가 확인되면 이 PR을 하나의 squash commit으로 revert한다. 기존 V3 contract와 Notion 역사 문서는 삭제하지 않으므로 rollback 시 자료 손실이 없어야 한다.
