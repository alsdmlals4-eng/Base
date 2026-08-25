---
name: orchestrating-deepseek-worktrees
description: Use when a large drafting, classification, comparison, or repetitive transformation can be isolated for an external model.
---

# Orchestrating DeepSeek Worktrees

## Core principle

대용량 초안·분류·비교는 별도 worktree/branch에 격리하고 외부 AI 결과를 **REVIEW_PENDING 입력**으로 취급한다. GPT가 current canon·diff·근거를 검수한 뒤 필요한 범위만 반영한다.

이 Skill은 external-AI isolation을 담당하며 Codex의 제품 구현 ownership과는 별개다.

## Authority contract

```text
GPT_PRIMARY_REVIEWER
GPT_NONCODING_PROJECT_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
EXTERNAL_AI_RESULT: REVIEW_PENDING
```

- 외부 AI 사용은 optional이다.
- Base/Notion/문서/기획/표/분류 결과는 GPT가 검수·반영한다.
- 외부 AI 결과가 Base Python test/Registry/generated/CI 같은 공용 운영 인프라를 바꾸더라도 GPT Base maintenance 영역이다.
- 외부 AI 결과가 **실제 게임 프로젝트의 Godot 제품 구현**으로 이어질 때만 그 게임 프로젝트 Codex handoff를 만든다.

## Use when

- 긴 문서 초안·요약·분류·표 변환
- 후보안/데이터 카드 등 반복 산출물
- 같은 기준 문맥의 여러 독립 하위 작업
- 외부 모델을 검수 대기 초안 생성기로 사용할 때

## Do not use when

- 보안·결제·파괴적 저장 migration의 최종 판단
- 실제 Godot 버그의 최종 구현을 외부 AI에 맡기려는 경우
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
- 최종 검수 owner = GPT
- 결과가 실제 Godot 제품 구현으로 이어지는지 여부

## `EXECUTOR_REHYDRATION_GATE`

외부 AI나 후속 worker는 handoff 요약만 믿지 않는다.

```text
latest applicable user instruction
→ project/Base AGENTS.md
→ current Active Context / confirmed decisions
→ relevant Notion current canon when configured
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
9. GPT가 current canon과 결과를 검수
10. non-product/Base/Notion/document 결과 → GPT가 필요한 최소 변경 반영
11. 실제 게임 프로젝트 Godot 구현 필요 → 별도 `CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF`
12. 검증/readback 후 worktree 정리

## Godot Codex boundary

Codex로 넘기는 유일한 기본 조건:

```text
actual game-project Godot product implementation
= GDScript / Scene / Resource / runtime wiring / build/export / implementation-runtime-play test
```

다음은 Codex로 넘기지 않는다.

```text
Base governance
Base tests / Registry / generated / CI
Notion
GDD / balance / Flow
image generation/editing
research / benchmark / review
```

Codex handoff가 발생하면 해당 **게임 프로젝트**의 GitHub+Notion을 다시 읽게 한다.

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
- GPT 검수 포인트
- `godot_product_implementation_required: true | false`
- true이면 해당 프로젝트 Codex handoff 위치
- worktree cleanup/preserve state

## Failure conditions

- 외부 AI가 main/활성 worktree 직접 수정
- 초안과 승인 canon 혼합
- 모델 보고만 믿고 diff/근거 미확인
- `EXECUTOR_REHYDRATION_GATE` 생략
- Base/Notion 결과를 Codex에 떠넘김
- 실제 Godot product implementation을 외부 AI에 최종 맡김
- 미검증 변경 자동 push
- 비용/보안/호환성 검증 생략

## Validation scenarios

1. 기획서 통합: 외부 AI 후보 → GPT 검수/Notion 반영. Codex 없음.
2. Base 데이터 카드/문서 분류: 외부 AI 후보 → GPT Base maintenance. Codex 없음.
3. 실제 게임 버그: 외부 AI는 분석 메모 가능 → GPT 검수 → 실제 Godot 구현은 해당 프로젝트 Codex.
4. main/Notion 변경: 결과 적용 전 fresh rehydration.

Templates:

- `templates/ai/DEEPSEEK_WORK_PACKAGE.md`
- `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md`
