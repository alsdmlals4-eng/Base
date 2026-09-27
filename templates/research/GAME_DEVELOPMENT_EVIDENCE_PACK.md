# 게임 개발 Evidence Pack

> 현재 프로젝트의 기획·아트·개발·AI·벤치마킹 결정을 외부 근거와 실제 증거로 검토할 때 사용한다. 조사 자료 모음이 아니라 **결정 질문→근거→판정→정본 반영→검증**을 연결한다.

## 0. 메타데이터

```yaml
evidence_pack_id:
project:
repository:
baseline_branch:
baseline_commit:
created_at:
updated_at:
owner:
work_mode: PLAN | BUILD | REVIEW
status: DRAFT | IN_RESEARCH | READY_FOR_DECISION | DECIDED | VALIDATED | SUPERSEDED
related_issue_pr_plan:
```

## 1. 결정 질문

```text
[대상 플레이어]가 [플레이 상황]에서 [핵심 행동·판단]을 이해하고 반복하게 만들기 위해,
[현재 결정 또는 대안] 중 무엇을 유지·변경·시험해야 하는가?
```

- 현재 결정:
- 바뀔 수 있는 결정:
- 보호할 프로젝트 코어:
- 비목표:
- 결정권자:
- 결정 기한 또는 Gate:

## 2. 플레이어 가치

- 대상 플레이어:
- 플레이 상황·세션 길이·플랫폼:
- 기대 감정·판타지:
- 핵심 선택·고민:
- 즉시 피드백·보상·기억:
- 차별 원리·세일즈포인트:
- 실패 후 학습·복구:

## 3. Coverage 선택

상태: `NOT_STARTED / IN_PROGRESS / EVIDENCED / NOT_APPLICABLE / BLOCKED`

| Coverage | 선택 | 상태 | 필요한 이유 | 책임 원본·Skill | 현재 Evidence ID | 누락 |
|---|---|---|---|---|---|---|
| 프로젝트 코어·게임 기획 |  |  |  |  |  |  |
| 플레이어 경험·게임 필·보상·난이도 |  |  |  |  |  |  |
| 아트 디렉션·캐릭터·환경·UI·애니메이션 |  |  |  |  |  |  |
| 내러티브·세계관·콘텐츠 설계 |  |  |  |  |  |  |
| UX·UI·접근성 |  |  |  |  |  |  |
| 사운드·음악·오디오 정보 전달 |  |  |  |  |  |  |
| Godot·데이터·저장·성능·플랫폼 기술 기획 |  |  |  |  |  |  |
| QA·자동화·런타임·회귀 검증 |  |  |  |  |  |  |
| 프로덕션·범위·Vertical Slice·반복 제작성 |  |  |  |  |  |  |
| 벤치마킹·Games User Research·텔레메트리 |  |  |  |  |  |  |
| AI 협업·Prompt·Evals·보안·권리·독립 검수 |  |  |  |  |  |  |
| 출시·스토어·마케팅 약속·출시 후 학습 |  |  |  |  |  |  |

`NOT_APPLICABLE`에는 이유를 반드시 적는다.

## 4. Source Plan

| 알고 싶은 것 | 필요한 근거 층 | 우선 출처 | 비교 차원 | 실패·반례 자료 | 중단 조건 |
|---|---|---|---|---|---|
| 실제 규칙·정책·기술 사실 | `T1_PRIMARY_OFFICIAL` |  |  |  |  |
| 현업 제작 과정·실패 | `T2_PROFESSIONAL_PRACTICE` |  |  |  |  |
| 플레이어가 실제로 한 행동 | `T3_PLAYER_BEHAVIOR` |  |  |  |  |
| 플레이어의 기대·감정·이유 | `T4_PLAYER_SELF_REPORT` |  |  |  |  |
| 여러 자료의 종합 | `T5_SYNTHESIS` |  |  |  |  |
| AI의 요약·가설 | `T6_AI_INFERENCE` |  |  |  |  |

## 5. Evidence 목록

근거 층:

- `T1_PRIMARY_OFFICIAL`
- `T2_PROFESSIONAL_PRACTICE`
- `T3_PLAYER_BEHAVIOR`
- `T4_PLAYER_SELF_REPORT`
- `T5_SYNTHESIS`
- `T6_AI_INFERENCE`

근거 상태:

- `VERIFIED_SOURCE`
- `PARTIALLY_VERIFIED`
- `CONTEXT_LIMITED`
- `STALE_RECHECK_REQUIRED`
- `CONFLICTING_EVIDENCE`
- `UNVERIFIED`

| Evidence ID | 제목·기관·저자 | URL·파일·Commit | 게시일·버전 | 확인일 | 근거 층 | 근거 상태 | 확인된 사실 | 해석 | 프로젝트 차이 | 사용 한계 |
|---|---|---|---|---|---|---|---|---|---|---|
| EVD-001 |  |  |  |  |  |  |  |  |  |  |

### Evidence 상세

```yaml
Evidence ID:
title:
organization_or_author:
source_url_or_path:
published_or_version:
checked_at:
evidence_tier:
evidence_status:
verified_facts:
interpretation:
conflicts_of_interest:
platform_language_playtime_patch_context:
project_similarities:
project_differences:
limitations:
recheck_condition:
related_case_card:
```

## 6. 공식 사실·현업 사례·플레이어 증거 분리

### 공식 사실

-

### 현업·개발자 경험

-

### 플레이어 행동

-

### 플레이어 자기보고

-

### AI 추론·추가 가설

-

AI 추론은 원출처와 실제 프로젝트 증거 없이 공식 사실로 승격하지 않는다.

## 7. 성공·실패·혼합 사례

| Case Card | 분류 | 해결하려던 문제 | 접근 | 결과 | 성공 조건 | 실패·비복제 요소 | 프로젝트 관련성 |
|---|---|---|---|---|---|---|---|
|  | `SUCCESS / FAILURE / MIXED` |  |  |  |  |  |  |

## 8. 상충 근거

### 상충 근거

| 충돌 ID | Evidence A | Evidence B | 충돌 내용 | 조건 차이 | 현재 해석 | 추가 검증 |
|---|---|---|---|---|---|---|
| CONFLICT-001 |  |  |  |  |  |  |

신뢰 가능한 근거가 충돌하면 하나를 숨기지 않고 `CONFLICTING_EVIDENCE`로 유지한다.

## 9. 개선 후보

개선 판정:

- `ADOPT`
- `ADAPT`
- `TEST`
- `AVOID`
- `IGNORE`
- `REFERENCE_ONLY`

| 개선 ID | 후보 | 플레이어 가치 | 코어 정렬 | 제작 비용 | 기술 위험 | 접근성·성능 | 보안·라이선스 | Evidence ID | 개선 판정 | 이유 |
|---|---|---|---|---|---|---|---|---|---|---|
| IMP-001 |  |  |  |  |  |  |  |  |  |  |

## 10. 개선 판정

### 채택·변형·시험

- `ADOPT`:
- `ADAPT`:
- `TEST`:

### 제외·보존

- `AVOID`:
- `IGNORE`:
- `REFERENCE_ONLY`:

### 제거·축소 검토

```text
REMOVE
→ REDUCE
→ MERGE
→ CLARIFY
→ FEEDBACK 강화
→ ADD
```

- 제거:
- 축소:
- 통합:
- 명확화:
- 피드백 강화:
- 추가:

## 11. 정본 반영 위치

### 정본 반영 위치

| 결정·개선 | 책임 원본 | Project Sheet tab | Issue·Plan | 실제 코드·데이터·자산 | 반영 상태 |
|---|---|---|---|---|---|
|  |  |  |  |  | `NOT_STARTED / UPDATED / VERIFIED / SUPERSEDED` |

외부 자료가 최종 기획 권한을 소유하지 않는다. 프로젝트 책임 원본과 실제 파일에 명시적으로 반영한다.

## 12. 제작 가능성

### 기획

- 코어·선택·루프와 연결되는가?
- 기능 목록이 핵심 경험을 흐리지 않는가?

### 아트·콘텐츠

- Art Bible·Asset Specification이 필요한가?
- 같은 유형의 두 번째 자산·콘텐츠를 만들 수 있는가?
- AI·외주·기존 에셋의 원출처·권리가 확인됐는가?

### Godot·기술

- Scene·Resource·Autoload·데이터 책임은 명확한가?
- 저장 Schema·마이그레이션·결정론이 필요한가?
- 목표 해상도·입력·성능·접근성 위험은 무엇인가?

### 프로덕션

- 작업 순서·의존성·병목·롤백은 무엇인가?
- Vertical Slice에서 무엇을 증명할 것인가?

## 13. 적대적 검토

| Finding ID | 공격 가설 | 근거 | 판정 | 우선순위 | 수정·비수정 이유 | 재검증 |
|---|---|---|---|---|---|---|
| ADV-001 |  |  | `MUST_FIX / SHOULD_FIX / DEFER / REJECT / NO_CHANGE / UNVERIFIED` |  |  |  |

필수 공격:

- 성공 사례의 표면 기능 복사
- 다른 장르·팀 규모·플랫폼 과잉 일반화
- 플레이어 행동과 플레이어 자기보고 혼동
- AI 추론을 공식 사실로 사용
- 접근성·성능·권리·비용 누락
- 프로젝트 코어·정본·실제 파일 미확인
- 새 Skill·문서의 중복 책임
- 실행하지 않은 검증 완료 주장

## 14. 검증 계획

### 검증 계획

```yaml
hypothesis:
build_or_artifact_version:
tester_or_eval_segment:
tasks_or_play_window:
observation_points:
telemetry_events:
self_report_channel:
primary_metric:
guardrail_metrics:
normal_failure_edge_counterexample:
accessibility_checks:
performance_budget:
security_license_checks:
success_failure_stop:
rollback:
```

## 15. 검증 결과

- 자동 검사:
- Godot import·runtime·save:
- 목표 기기·플랫폼:
- 접근성:
- 성능:
- 플레이테스트 행동:
- 플레이어 자기보고:
- AI Evals:
- 독립 검수:
- 결과 판정:

## 16. 미검증·한계

### 미검증·한계

- 실행하지 못한 조사:
- 확인하지 못한 원출처:
- 표본·플랫폼·언어·패치 편향:
- 기술·환경 제한:
- 접근성·성능 미실행:
- 출시 정책 재검증 필요:
- 다음 재개 조건:

## 17. 학습·Base 승격

### 공용화 가능한 원리

-

### 프로젝트 전용으로 유지

-

### Base Change Proposal 후보

```yaml
candidate:
source_project_commit:
repeated_cases:
counterexamples:
validation_state:
proposal_status: NOT_PROPOSED | DRAFT | SUBMITTED | DEFERRED
```

한 번의 성공이나 미검증 외부 사례를 공용 강제 규칙으로 승격하지 않는다.

## 18. 자산 권리·플랫폼 출시 특화 증빙

- 자산별 기록: `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- 프로젝트 출시 Pack: `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`
- 공용 방법: `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
- `REFERENCE_TO_ORIGINAL` 참조 입력과 최종 자산은 별도 Record로 연결한다.
- 필수 권리·등급·설문·빌드 일치가 미확인되면 `RELEASE_BLOCKED_UNVERIFIED`다.
- 이 Evidence Pack은 조사와 결정 근거를 연결하고, 두 특화 Template은 실제 자산·출시 상태를 기록한다. 어느 파일도 법률 검토나 플랫폼 승인을 대신하지 않는다.

## 19. Cloud Run 게임 백엔드 특화 증빙

- 공용 판단 Guide: `docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`
- 프로젝트 계약: `templates/project-operations/GAME_BACKEND_SERVICE_CONTRACT.md`
- 서버 필요성·적합성·권위·상태·idempotency·replay·IAM·비밀·WebSocket·비용·장애·rollback을 연결한다.
- 보호된 온라인 동작이 있으면 `AUTHENTICATION_IS_NOT_AUTHORIZATION`, `DENY_BY_DEFAULT`, trusted server-side object/action/property/context authorization을 기록한다. 오프라인 프로젝트는 `ONLINE_IDENTITY_NOT_REQUIRED`로 남기고 서버를 만들지 않는다.
- `AUTHORIZATION_NEGATIVE_MATRIX_REQUIRED`는 최소 두 actor와 서로 다른 같은 유형 resource로 cross-user read/update/delete, cross-tenant 또는 relationship, ordinary-user→administrator function, method/path/operation substitution, sensitive-property injection, bulk/list/export, expired/revoked session을 실행한다.
- 각 거절은 승인된 비공개 오류 class와 `DENIAL_HAS_NO_PROTECTED_SIDE_EFFECT`를 만족해야 한다. authoritative state delta·external effect·private data disclosure·privilege elevation이 없고 redacted audit event가 readback되는지 확인한다.
- session idle/absolute timeout, logout·revocation·privilege-change invalidation, WebSocket revalidation·per-message authorization·browser Origin allowlist, browser/native session-secret storage, 전체 보호 세션 TLS, privileged credential과 self-managed password controls를 연결한다.
- `STATIC_CONTRACT_IS_NOT_RUNTIME_SECURITY_EVIDENCE`: exact revision·configured policy·executable negative tests·state/side-effect/audit readback이 없으면 runtime security와 실제 deployment·load·failure·cost·production readiness를 `NOT_RUN`으로 유지한다.

## 20. Entitlement·integrity·DRM 특화 증빙

- 공용 Guide: `docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`
- 프로젝트 Record: `templates/project-operations/GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md`
- 플랫폼별 entitlement·integrity 신호, server authority, request binding/replay, offline/outage, false-positive, privacy와 sunset 증거를 연결한다.
