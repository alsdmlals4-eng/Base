# Sequential Part Coordinator and Human-Facing Notion Design

## Goal

Base를 하나의 GPT coordinator 채팅에서 P01→P09 순서로 깊게 최적화하되, Part의 전문성·학습·검증 추적성은 유지하고 Part 경계가 실제 오류 수정의 장벽이 되지 않게 한다. 동시에 Base/프로젝트 Notion Home을 사람이 하위 페이지로 이동하지 않아도 핵심 구조·규칙·Skill·Module·현재 상태를 이해할 수 있는 자립형 human-facing view로 만든다.

## Current problems

1. 기존 `ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END` 모델은 P01~P09마다 새 채팅을 요구해 인계·컨텍스트 재수화 비용이 크다.
2. `owned_write_paths`가 실제로는 책임 지도였지만 worker prompt와 scope checker에서 hard write barrier처럼 작동해, 다른 Part 문제를 발견해도 직접 수정하지 못하는 deadlock이 발생했다.
3. Notion Base Home은 Part/Skill 이름과 링크는 보여주지만 각 Skill의 목적·작동 시점·입력/처리/출력·기대효과, Module 단계의 이유와 연결, Part 간 실제 작업 흐름을 충분히 설명하지 않는다.
4. 프로젝트 Home도 핵심 방향은 제공하지만 시스템 상세·UX/UI·검증·현재 구현상태를 하위 페이지로 넘기는 경우가 있어 한 화면에서 프로젝트를 완전히 이해하기 어렵다.
5. 적대적 검토 정본은 이미 full-scope loop를 요구하지만, 실제 완료보고에서 `Loop 1=scope`, `Loop 2=player value`, `Loop 3=consumer`처럼 서로 다른 관점을 각각 한 회차로 보고해 fixed-lens 관행이 되살아났다.

## Selected architecture

### 1. One coordinator chat, sequential Parts

Canonical policy token:

`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`

- 한 GPT coordinator 채팅이 P01→P09를 순서대로 수행한다.
- Part는 Base를 쪼개는 실행 격리가 아니라 전문 조사·학습·보고·검증 checkpoint다.
- 일반적으로 한 Part를 완료·병합한 뒤 최신 `main`을 다시 pin하고 다음 Part로 간다.
- rollback과 provenance를 위해 GitHub PR은 Part 단위로 유지하는 것을 기본으로 한다.
- 필요하면 같은 Part PR에서 다른 Part/CP0 경로도 수정할 수 있다. 단, 실제 변경 이유·semantic owner·consumer·test를 기록한다.

### 2. Semantic ownership, not write prohibition

Canonical policy token:

`PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

- `owned_write_paths`는 주 책임자와 기본 검토 owner를 뜻한다.
- 현재 coordinator 작업에서 발견된 검증된 오류·충돌·누락이 다른 Part/CP0에 속해도 수정할 수 있다.
- cross-Part 수정은 `CROSS_PART_CHANGE`로 기록해 변경 원인, semantic owner, affected paths, tests, rollback을 남긴다.
- `CROSS_PART_CHANGE_REQUEST`는 다른 독립 workstream의 승인이 필요하거나 현재 evidence/권한이 부족할 때만 사용한다.
- 다른 Part라는 이유만으로 유효한 MUST_FIX/SHOULD_FIX를 미루지 않는다.

### 3. Independent active workstream protection remains

Canonical policy token:

`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`

- open/draft/ready PR의 branch/worktree를 임의로 수정·rebase·close·merge하지 않는다.
- 같은 의미 변경이 필요하면 최신 completed `main`에서 coordinator-owned 새 branch/PR로 해결하거나, 기존 active PR이 완료된 뒤 재평가한다.
- 사용자가 특정 active PR을 현재 coordinator가 인수하라고 명시한 경우만 직접 이어받는다.

이 규칙은 Part 경계 해제와 별개다. **Part가 다름은 수정 금지 이유가 아니지만, 다른 독립 작업자의 활성 workstream이라는 사실은 보호 이유다.**

## Adversarial review contract

Canonical policy token:

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

`FULL_LOOP_COUNT_MINIMUM: 5`와 `CLEAN_REVIEW_EXIT`는 유지한다.

한 회차는 다음 전체 lifecycle을 전부 포함해야 한다.

```text
CURRENT STATE / CANON / ACTUAL IMPLEMENTATION READBACK
→ MINIMUM 3 MATERIAL ALTERNATIVES / CURRENT OPTION RECHECK
→ FULL-SCOPE ATTACK
→ VALIDATE CRITIQUE
→ FIX / REFINE VERIFIED FINDINGS
→ EXECUTION / REGRESSION / REFERENCE VERIFICATION
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE-ATTACK THE WHOLE RESULTING STATE
```

- `Loop 1 = scope`, `Loop 2 = UX`, `Loop 3 = CI`, `Loop 4 = long-term`, `Loop 5 = review`처럼 관점 하나만 수행한 것은 **5회의 full loop가 아니다**.
- 여러 관점은 한 full loop 내부의 attack coverage다.
- 회차 보고에서 그 회차의 대표 finding을 강조할 수 있지만, 그 finding이 회차의 전체 검토 범위를 대체하지 않는다.
- 최소 5번 전체 lifecycle을 실제 반복하고 이후에도 오류가 있으면 N회까지 계속한다.

## Notion human-facing design

Canonical policy token:

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

### Base Home

`Base · 작업 시스템 & Skill 지도` 메인 화면만 읽어도 다음을 이해할 수 있어야 한다.

1. Base가 무엇을 소유하는가.
2. 전체 작업 lifecycle과 각 단계의 목적.
3. 중요 상위 규칙과 작동 조건.
4. 각 active Skill의:
   - 목적
   - 언제 호출되는가
   - 입력
   - 핵심 처리
   - 출력
   - 기대효과
   - 연결 Module/consumer/test
5. 핵심 Module의:
   - 책임
   - 이전 단계에서 받는 입력
   - 수행하는 결정/처리
   - 다음 단계로 보내는 출력
   - 없으면 생기는 실패
6. P01~P09 각각의:
   - 담당 책임
   - 대표 Skill/Module
   - 작업 순서
   - 다른 Part와 연결
   - 기대효과
   - 주요 위험/재검토 조건
7. 현재 Base main, 중요한 진행/미완료 상태, 실제 검증과 NOT_RUN.

하위 Part 페이지는 더 깊은 evidence, Learning Log, Source, 변경 이력용이다. 메인 이해에 필수 링크가 되어서는 안 된다.

### Project Home

각 Project Home도 추가 이동 없이 다음을 이해할 수 있어야 한다.

- 프로젝트 한 줄 정의와 핵심 플레이어/사용자 가치
- 현재 확정 방향과 금지/보호 요소
- Core Loop / 주요 Flow
- 핵심 시스템별 목적·작동·상호작용
- UX/UI/Visual 방향과 승인 상태
- 현재 구현상태와 runtime truth 연결
- 검증상태: static/runtime/device/human/accessibility/store 등 evidence ceiling 분리
- 현재 blocker / 다음 작업
- 최근 중요한 결정과 이유
- 주요 위험과 revisit condition

하위 페이지/DB는 세부 수치·전체 Asset·Reference·로그·긴 표를 보관하는 drilldown이다.

## Notion update rule

- GitHub는 structured/runtime truth, Notion은 human-facing canon이다.
- `main`에 유지된 중요한 구조·Skill·Module·프로젝트 결정이 바뀌면 Home summary도 post-merge readback 기준으로 갱신한다.
- 링크만 추가해서 "상세는 여기"로 끝내지 않는다. Home에 핵심 설명을 먼저 적고 링크는 증거/심화용으로 둔다.
- 같은 설명을 모든 하위 페이지에 중복 복사하지 않는다. Home은 요약 정본, 하위 페이지는 상세 정본이라는 역할을 구분한다.

## Sequential Part workflow

```text
LATEST MAIN PIN
→ P01 deep review / fixes / learning / PR / merge
→ latest main pin
→ P02
→ ...
→ P09
→ final Base-wide Integration
→ minimum 5 full adversarial loops until clean
→ final Notion Base + Project Home readback
```

다른 Part 문제가 P04 작업 중 발견되면:

```text
validate finding
→ active independent PR collision check
→ no active collision: fix now and record CROSS_PART_CHANGE
→ active collision: preserve foreign PR and either solve on completed main without touching it or defer with exact blocker
```

## Current P01~P09 integration rule

- 이미 병합된 Part 결과는 현재 `main` 사실로 취급하고 재구현하지 않는다.
- open/draft/ready Part PR은 완료로 취급하지 않는다.
- 기존 Part completion packet의 cross-Part requests는 최신 main에서 다시 검증하고, 여전히 유효한 것만 coordinator가 직접 해결한다.
- P07 completed packet은 already merged work이며 재개·재작성하지 않는다. Its evidence ceiling must remain intact: `ACTIVE_IN_MAIN` is publication lifecycle only, not runtime/device/human/store PASS.
- P03/P08 open workstreams remain protected until this coordinator contract change is merged; afterward current state is re-evaluated and finishing work uses current user authority without silently mutating their existing branches.

## Alternatives considered

### A. Keep nine separate chats and loosen cross-Part writes

Low migration cost, but preserves the largest user burden: repeated chat setup, context rehydration, completion packet handoff, and ownership deadlocks.

### B. One coordinator chat + sequential Part checkpoints + semantic ownership

**Selected.** Preserves Part depth and rollback while removing chat fragmentation and cross-Part deadlocks.

### C. Remove Part model entirely

Simpler surface, but loses structured coverage, Part-specific learning, Source routing, and confidence that every major Base responsibility received deep review.

## Long-term fit

Selected B is preferred while Base is operated by one user with GPT as primary planner/reviewer. It reduces coordination overhead without losing Part-level auditability. Revisit if multiple human/AI workers routinely write simultaneously, cross-Part changes become too broad for meaningful Part checkpoints, or repository size makes a single coordinator conversation impractical.

## Acceptance criteria

- Base no longer instructs the user to open nine Part chats.
- Base explicitly says one coordinator chat executes P01→P09 sequentially.
- A validated cross-Part finding can be fixed in the current coordinator work even when the semantic owner differs.
- Active independent PR/worktree protection remains explicit.
- Scope/validation contract distinguishes semantic owner attribution from forbidden foreign-workstream mutation.
- Adversarial review tests reject fixed-lens counting as full-loop evidence.
- Base Notion Home contains self-contained detailed Skill, Module, Part, lifecycle, validation, and current-state explanations.
- Project Home contract requires self-contained project understanding before drilldown.
- Current Part integration finishes only after minimum five true full-scope loops and zero valid blockers.
