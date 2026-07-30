---
document_role: PROJECT_V9_APPLICATION_CONTRACT
contract_source: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
shared_body_policy: REFERENCE_ONLY_NO_COPY
execution_profile: SELECT_AT_RUNTIME_FROM_ACTIVE_V9_CONTRACT
---

# [프로젝트명] Vertical Slice v9 적용 계약

## 1. 실행 바인딩

| 항목 | 값 |
| --- | --- |
| 프로젝트 `origin/main` SHA | `[실행 시 기록]` |
| Base release commit | `[프로젝트에 고정된 Base v9.3 또는 호환 release pin]` |
| Base evidence commit | `[프로젝트에 고정된 Base v9.3 또는 호환 evidence pin]` |
| Adapter / Snapshot / router | `[경로와 hash]` |
| 로컬 Registry / 프로젝트 전용 Skill | `[경로와 hash]` |
| Google Sheet | `[읽기 상태와 마지막 main SHA]` |
| 보호 경로 | `[코드·Scene·데이터·에셋 범위]` |

## 2. 읽기 순서와 책임 원본

1. `[Active Context]`
2. `[Decision Log 또는 Registry]`
3. `[설계 문서 지도와 현재 구현 상태]`
4. `[프로젝트 Base adapter / snapshot / router]`
5. `Base v9` 공용 계약
6. `[v6~v8 legacy reference와 판정]`

## 3. 실행 프로필과 범위

- `REPOSITORY_FIRST_INTERVIEW` 뒤에 현재 요청·승인 범위·Critical Gate로 실행 프로필을 선택한다.
- 감사·복원·중간 시각화·보완 계획만 요청했거나 차단 충돌이 있으면 `RECONCILIATION_PLANNING_PROFILE`을 사용한다. 이 경우 제품 코드, Scene, 데이터, 에셋, 승인 Decision, Google Sheet 값은 변경하지 않는다.
- 구현이 요청·승인되고 Issue/Goal·수용 기준·보호 경로 검증이 있으면 `INTEGRATED_DELIVERY_PROFILE`로 기획·Codex 인계·구현·검수·병합 후 동기화를 수행한다.
- 현재 Gate와 사람/실기기/런타임 증거는 실제 근거가 없으면 올리지 않는다.

## 4. 프로젝트 고유 경계

| 구분 | Base 공용 능력 | 프로젝트 전용 책임 |
| --- | --- | --- |
| 라우팅·감사·검증 | Base Registry route | `[실제 local SKILL.md]` |
| 기획·게임 규칙 | 계약·증거 형식 | `[프로젝트 정본]` |
| UX/UI·시각 검토 | Intermediate Visual Checkpoint | `[플랫폼/아트/입력 제약]` |

## 5. 기본 중간 시각화 시나리오

| 항목 | 값 |
| --- | --- |
| 한 화면 흐름 | `[프로젝트별 기본 화면]` |
| 관련 Decision / 책임 정본 | `[ID 및 경로]` |
| 플랫폼·해상도·입력 | `[사실만 기입]` |
| 확인할 해석 위험 | `[P1 또는 주요 불확실성]` |
| 산출물 | `DRAFT_VISUAL` 또는 Screen Brief·와이어프레임 대체안 |

생성물은 정본·최종 자산·Figma 구현 명세·Godot 완료·런타임/사람 검증 증거가 아니다. `Screen Interpretation Review`와 사용자 Decision 없이는 승격하지 않는다.

## 6. 현재 Critical Gate와 다음 사용자 결정

| Gate | 현재 상태 | 근거 | 다음 결정/증거 |
| --- | --- | --- | --- |
| `[Gate ID]` | `[상태]` | `[경로/commit]` | `[사용자 또는 검증]` |

## 7. 감사 산출물 연결

- Baseline Recovery Record: `[경로]`
- Legacy Requirement Traceability: `[경로]`
- Source / Consumer / Propagation Map: `[경로]`
- Finding Ledger: `[경로]`
- Readiness / Critical Gate: `[경로]`
- Approval Bundle / Change Plan: `[경로]`
