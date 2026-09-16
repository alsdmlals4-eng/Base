---
name: orchestrating-deepseek-worktrees
description: Use when a large drafting, classification, comparison, or repetitive transformation can be isolated for an external model.
---

# Orchestrating DeepSeek Worktrees

## Core principle

외부 AI가 실제로 유용한 대용량 초안·분류·비교는 별도 worktree/branch에 격리하고 결과를 **REVIEW_PENDING 입력**으로 취급한다. 현재 Work가 repository current canon·diff·근거를 검수한 뒤 승인 범위만 반영한다.

이 Skill은 선택적 external-AI isolation을 담당한다. `docs/GPT_CODEX_WORKFLOW_POLICY.md`의 통합 Work 실행을 기본으로 하며 제품 구현을 이유로 별도 Codex 단계를 만들지 않는다.

## Authority contract

```text
UNIFIED_WORK_EXECUTION
CAPABILITY_BASED_EXECUTOR_SELECTION
CAPABILITY_IS_NOT_AUTHORIZATION
REPOSITORY_PRIMARY_CANON
ZERO_INCREMENTAL_COST_REQUIRED
EXTERNAL_AI_RESULT: REVIEW_PENDING
```

- 외부 AI 사용은 optional이다.
- 현재 승인된 capable Work가 기획·상세 설계·제품 구현·테스트·검토·허용된 통합을 이어간다.
- Base Python test/Registry/generated/CI와 게임 제품 코드 모두 승인 범위·보호 경로·실제 capability로 판단한다. 파일 종류는 실행자 변경 사유가 아니다.
- 사용자 요청·실제 capability 부족·근거 있는 격리 필요 때만 필요한 범위를 다른 executor에 인계한다. 같은 세션에서 수행 가능하면 별도 handoff 파일을 강제하지 않는다.
- 도구 가용성은 사용자 승인·repository 권한·외부 전송·비용 권한을 확대하지 않는다.

## Use when

- 긴 문서 초안·요약·분류·표 변환
- 후보안/데이터 카드 등 반복 산출물
- 같은 기준 문맥의 여러 독립 하위 작업
- 외부 모델을 검수 대기 초안 생성기로 사용할 때

## Do not use when

- 보안·결제·파괴적 저장 migration의 최종 판단
- 실제 제품 버그의 최종 판정·승인·통합을 검수 대기 외부 AI 결과에 맡기려는 경우
- 사용자 승인 없이 제품 방향·정본 확정
- 비밀값/권한 없는 비공개 자료를 외부 모델에 전달해야 하는 경우
- 작은 작업인데 단지 외부 모델이 있다는 이유로 우회

## Required inputs

- 승인 목표와 사용자 가치
- 기준 문서 allowlist
- 허용/보호 경로
- 산출물 스키마와 검수 기준
- 기준 branch/commit
- 외부 전송 허용 자료
- 최종 검수 owner와 승인·권한 경계
- 결과의 실제 product/operation consumer와 필요한 capability·검증

## `EXECUTOR_REHYDRATION_GATE`

외부 AI나 후속 worker는 handoff 요약만 믿지 않는다.

```text
latest applicable user instruction
→ project/Base AGENTS.md
→ current Active Context / confirmed decisions
→ repository current canon / exact source SHA / approved asset manifest
→ explicitly scoped V4 Notion exception or required legacy migration source only
→ exact branch/commit
→ allowlist / protected paths
→ relevant canonical files/tests
→ current worktree dirty/integration state
```

- handoff와 current truth가 다르면 current truth 우선
- 다른 project/worktree/branch 상태 재사용 금지
- 오래된 외부 AI 결과를 그대로 canon 승격 금지
- 실행하지 않은 것을 실행했다고 주장 금지

## Workspace contract

```text
main worktree                 실제 기준선·최종 반영
.worktrees/deepseek-<topic>/  외부 AI 초안/후보
branch: ai/deepseek-<topic>   격리 작업 branch
```

- `.worktrees/` ignore 여부 확인
- 한 branch = 한 목적
- 기존 active branch 재사용 금지
- dirty/unintegrated 결과가 있으면 자동 삭제 금지

## Process

1. current baseline/dirty/start commit 기록
2. 한 문장 목표와 검수 가능한 단위로 분해
3. isolated branch/worktree
4. `templates/ai/DEEPSEEK_WORK_PACKAGE.md` 계약 작성
5. 필요한 context만 allowlist로 제공
6. `EXECUTOR_REHYDRATION_GATE`
7. 고정 Markdown/JSON schema로 결과 회수
8. 근거·가정·미확인·변경 후보 분리
9. current review owner가 repository canon·diff·근거와 결과를 검수
10. 현재 승인된 capable Work가 product/operation 구분 없이 필요한 최소 변경 구현·검증
11. 사용자 요청·실제 capability 부족·근거 있는 격리 필요 때만 해당 범위를 조건부 인계
12. 검증/readback 후 소유권·미통합 변경을 확인하고 허용된 worktree 정리 또는 보존

## Capability-based implementation boundary

현재 Work가 project canon의 engine adapter와 실제 capability로 제품 구현을 이어간다. Godot 프로젝트의 예:

```text
actual game-project Godot product implementation
= GDScript / Scene / Resource / runtime wiring / build/export / implementation-runtime-play test
```

인계는 다음 조건에서 필요한 범위만 선택한다.

```text
explicit user request
real missing authoring / test / runtime capability
justified isolated executor with authorized access
```

Codex가 실제로 선택되면 기존 `CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF`는 호환 값으로 사용할 수 있다. 받는 executor는 해당 repository exact SHA·current canon·승인 자산 manifest·engine/version·권한을 다시 읽는다. Notion은 기본 재수화 정본이 아니다.

runtime capability가 없으면 해당 검증은 `NOT_RUN`으로 유지하며 독립적으로 준비된 승인 구현·정적 검사는 계속한다. 필수 runtime 증거가 없는 전체 완료·release PASS는 주장하지 않는다.

## Token/context efficiency

- stable prefix + task-specific suffix
- 같은 문서 전체 반복 금지
- 관련 없는 Skill/Tool preload 금지
- 서로 독립인 대량 작업만 병렬화
- 같은 파일 다중 모델 동시 수정 금지
- 별도 API 비용은 사용자 승인된 경우에만 사용

## Output contract

- work package
- worktree/branch/start commit
- rehydration 결과
- 후보 파일
- 초안 산출물
- 근거/가정/미확인
- current review owner의 검수 포인트
- `godot_product_implementation_required: true | false`
- 조건부 인계가 실제로 필요하면 사유·선택 executor·범위·기존 계약 위치
- actual validation / NOT_RUN / evidence ceiling / remaining work
- worktree cleanup/preserve state

## Failure conditions

- 외부 AI가 main/활성 worktree 직접 수정
- 초안과 승인 canon 혼합
- 모델 보고만 믿고 diff/근거 미확인
- `EXECUTOR_REHYDRATION_GATE` 생략
- 앱 이름이나 파일 종류만으로 필수 인계 또는 실행 금지
- capability를 사용자 승인·repository 권한으로 오인
- 외부 AI 결과에 실제 제품의 최종 승인·검증·통합을 위임
- runtime NOT_RUN을 숨기거나 독립 구현 전체를 자동 중단
- 미검증 변경 자동 push
- 비용/보안/호환성 검증 생략

## Validation scenarios

1. 기획서 통합: 외부 AI 후보 → current Work 검수 → repository owner 반영·readback.
2. Base 데이터 카드/문서 분류: 외부 AI 후보 → current Work의 승인된 최소 수정과 검증.
3. 실제 게임 버그: 외부 AI 분석·후보 → current Work 검수 → capable Work가 구현·테스트. 별도 executor는 실제 필요 때만 선택.
4. runtime 없는 Work: 독립 구현·정적 검사 계속, runtime은 NOT_RUN과 완료 상한으로 기록.
5. repository 또는 명시된 V4 exception 변경: 결과 적용 전 exact SHA·권한·current canon fresh rehydration.

Templates:

- `templates/ai/DEEPSEEK_WORK_PACKAGE.md`
- `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md`
