# Base Partition Operating Model v2

## 목적

Base는 **하나의 통합 시스템(ONE BASE)** 이다. P01~P09는 Base를 9개의 실행 시스템이나 9개의 별도 채팅으로 분해하는 구조가 아니라, 큰 저장소를 분야별로 깊게 조사·학습·검증하고 결과를 추적하기 위한 **안정적인 semantic responsibility / maintenance / learning view**다.

기계적 책임 지도는 `docs/operations/BASE_PARTITION_MANIFEST.json`이 소유한다. 실제 작업은 언제나 최신 `main`을 다시 읽어 exact baseline을 pin한 뒤 수행한다.

## 현재 실행 계약

`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`

`BASE_FULL_PART_COORDINATOR_EXPLICIT_ONLY`

`GENERAL_PROJECT_WORK_USES_GOAL_SCOPED_PHASES`

이 실행 계약은 사용자가 **Base 전체 P01~P09 감사·최적화**를 명시적으로 요청한 maintenance session에만 활성화한다. 일반 프로젝트 작업, 단일 Goal 수정, 진단, 질문 답변의 기본 구조가 아니다. 일반 L1+ 작업은 현재 Goal에 필요한 범위만 `PLAN / RESEARCH / REVIEW → 승인된 BUILD / VERIFY`로 진행하며 모든 Part를 순회하지 않는다.

한 GPT coordinator 채팅이 다음 순서로 Part를 하나씩 깊게 처리한다.

```text
latest main pin
→ P01
→ merge / post-merge readback
→ latest main repin
→ P02
→ ...
→ P09
→ final whole-Base integration
```

정확한 기본 순서:

```text
P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09
```

- 새 Part 채팅을 9개 만들지 않는다.
- Part가 바뀌어도 같은 coordinator 채팅의 사용자 결정·학습·미완료 finding 맥락을 유지한다.
- rollback·변경 attribution·검증을 명확히 하기 위해 **Part별 PR/checkpoint는 유지**하는 것을 기본으로 한다.
- 한 Part를 병합한 뒤 다음 Part를 시작하기 전에 최신 `main`을 다시 pin한다.
- Part 순서는 coverage와 사용자 학습을 위한 기본 순서이며, 긴급한 검증된 cross-Part blocker를 지금 고치는 것을 막는 장벽이 아니다.

## Part 소유권의 의미

`PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

Manifest의 `owned_write_paths`, `owned_skill_ids`, Module은 다음을 뜻한다.

- 누가 해당 의미를 가장 깊게 이해·감사해야 하는가
- 어떤 Part의 Learning Log에 교훈을 남길 것인가
- 완료보고에서 어느 Part 성과로 설명할 것인가
- 어떤 consumer/Test를 우선 검증할 것인가

**다른 Part라는 이유만으로 검증된 오류·충돌·누락·MUST_FIX/가치 있는 SHOULD_FIX를 수정 보류하지 않는다.** 현재 coordinator가 문제를 발견했고 증거·수정권한·검증경로가 충분하면 semantic owner가 다른 경로와 CP0도 같은 작업에서 수정할 수 있다.

그 경우 다음처럼 기록한다.

```yaml
CROSS_PART_CHANGE:
  discovered_while: Pxx
  semantic_owner: Pyy | CP0
  affected_paths: []
  problem:
  evidence:
  change:
  consuming_tests: []
  rollback:
```

`CROSS_PART_CHANGE_REQUEST`는 단순히 “다른 Part다”라는 이유로 쓰지 않는다. 다음처럼 **실제 조정 blocker**가 있을 때만 사용한다.

- 다른 독립 활성 workstream이 같은 의미/경로를 이미 수정 중
- 현재 세션에 필요한 권한·정본·실행 증거가 없음
- 사용자 중요 방향 결정이 필요함
- 현재 변경셋에서 안전하게 원자적으로 검증할 수 없음

## 독립 workstream과 open PR 보호

`OPEN_PR_READ_ONLY_BY_DEFAULT`

`OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`

`FOLLOW_UP_TARGET_IS_MERGED_MAIN`

Part 경계와 PR 보호는 서로 다른 개념이다. 현재 작업 범위 안에서 다른 Part의 **merged-main** 오류를 고칠 수는 있지만, `open/draft/ready` PR·Branch는 현재 작업자 증거와 무관하게 기본 read-only다.

- 열린 PR의 head/diff/check는 현행·충돌·중복 확인을 위해 읽을 수 있다.
- checkout/write/rebase/close/merge/selective-copy/material-delta 흡수는 하지 않는다.
- 일반 후속 변경은 latest completed `main`에서 새 Branch로 시작하고 main에 실제 유지된 의미만 대상으로 한다.
- 사용자가 열린 PR을 변경하려면 현재 작업에서 PR 번호와 허용 동작을 명시해야 한다.
- “현재 채팅만 활성”, 같은 Goal, owner evidence 부재는 mutation 권한이 아니다.

## ONE BASE와 P01~P09 관계

```text
                         ONE BASE
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
      Foundation        Production        Delivery
      P01 P02 P03       P04 P05 P06       P07 P08 P09
          │                 │                 │
          └──────────── semantic links ──────┘
                            │
                  Coordinator Integration
                            │
                         ONE BASE
```

세 묶음은 설명용 cluster일 뿐 별도 채팅/동시 실행 요구가 아니다.

## P01~P09 상세 책임 지도

| Part | 핵심 책임 | 대표 Skill / Module | 입력 → 처리 → 출력 | 주요 연결 | 기대효과 |
|---|---|---|---|---|---|
| **P01 · Project Planning, Operations & Notion** | 사용자 의도·범위·완료조건을 실행 가능한 계약으로 만들고 Project OS·Notion human view·handoff·continuity를 유지 | `managing-project-intake-and-work-contract`, `managing-game-project-operating-system`, Design Docs, Handoff/Continuity | 사용자 목표·현재 결정 → 범위/권위/계획/결정 복원 → 실행 계약·Notion Home·handoff | P02 정본, P03 검토, P04~P09 프로젝트 입력 | 반복 질문·결정 손실·Notion/GitHub 권위 혼동 감소 |
| **P02 · Skill Governance, Canon Freshness & Legacy** | Skill 생명주기, canonical reference freshness, BCP, stale/legacy 흡수·보존·제거 | Skill Lifecycle, Reference Freshness, BCP, Simplification, Pruning, Legacy | Registry·정본·consumer → 중복/드리프트/UNIQUE 판정 → 단일 owner·신선한 참조·안전한 retirement | 모든 Part | Skill 과잉·구형 정본 부활·파괴적 삭제 감소 |
| **P03 · Adversarial Quality, Refactoring & Git Integrity** | 전체 적대적 검토, finding 검증, contract-preserving refactor, Git 상태·workstream 정합성 | `running-adversarial-review-and-refinement`, refactor, Git sync | 승인 범위·실제 diff·증거 → attack/validate/refine/regression → clean finding set·안전한 변경 | P02 freshness, P07 evidence | 잘못된 PASS·과잉 수정·동시작업 손상 감소 |
| **P04 · Game Design, Core, Player Research & Vertical Slice** | 플레이어 가치·Concept·Core·기능/밸런스·연구질문·Vertical Slice 설계 | Concept/Core/User Research/Vertical Slice | player promise·시장/벤치마크 → 선택·경험·관찰신호 설계 → 검증 가능한 slice/acceptance | P05 Visual, P06 runtime, P07 evidence | 기능 나열이 아니라 플레이어 가치와 실제 검증 연결 |
| **P05 · Art, UX/UI & Visual Assets** | 아트 방향, 이미지 후보 lifecycle, UX/UI 가독성, Visual QA, 재사용/구조화 | Art Prompt, UI Art Audit, Visual/Asset workflow | 시각 요구·프로젝트 분위기 → 후보 생성/비교/승인/구조화 → 승인 Visual·UX flow·재사용 자산 | P04 요구, P06 구현, P07 rights/evidence | AI 티·스타일 drift·가독성 저하·일회성 자산 낭비 감소 |
| **P06 · Godot, Runtime & Technical Toolchain** | Godot authoring/runtime, diagnostics, addon/plugin 평가, adapter, local execution | Runtime Diagnostics, Godot Asset/Plugin Evaluation | 설계·Visual·프로젝트 상태 → 실제 editor/runtime/tool 검증 → 구현·diagnostic evidence | P04 acceptance, P05 visual, P07 validation | “설계됨”과 “실제로 돌아감” 혼동 감소 |
| **P07 · Platform, Release & Execution Validation** | 실제 diff/정적/runtime evidence, platform/store/rights/build/release readiness | Change Validation, Evidence Ledger, Platform/Release | 구현·빌드·플랫폼 요구 → evidence ceiling으로 검증 → PASS/PARTIAL/NOT_RUN/blocked delivery state | P03 critique, P06 runtime, P01 evidence template | 문서 존재를 실행 증거로 오인하는 오류 감소 |
| **P08 · AI Operations & External Executors** | GPT/외부 executor 역할, model/cost routing, source research, worktree/rehydration | AI Instruction/Context, Model/Cost, External Executor | 작업 요구·비용상태·현재 canon → 최소 Skill/Tool/executor 선택 → 검토 가능한 결과·handoff | P01 계약, P03 isolation, P07 evidence | 도구 과다 호출·불필요 과금·stale context 실행 감소 |
| **P09 · Content, Narrative & Publication** | 연재서사, 캐릭터/voice, game-dev YouTube, publication evidence | Serial Fiction, Narrative/Voice, YouTube | project canon·실제 build evidence → 작성/편집/발행 판단 → 일관된 콘텐츠·학습 | P04 world fit, P05 visual, P07 rights/platform | 정사 drift·표현 복제·콘텐츠와 runtime 완료 혼동 감소 |

## Part checkpoint에서 반드시 설명할 것

각 Part 작업은 파일 목록이 아니라 다음을 설명한다.

1. 이 Part가 왜 존재하는가.
2. 가장 중요한 규칙은 무엇이며 언제 작동하는가.
3. 각 핵심 Skill은 **목적 / 호출 조건 / 입력 / 처리 / 출력 / 기대효과 / consumer/Test**가 무엇인가.
4. 각 Module은 **이전 단계 입력 → 자체 판단/처리 → 다음 단계 출력**이 무엇인가.
5. Module/Skill이 없으면 어떤 실패가 생기는가.
6. 유지·개선·흡수·제거·의도적 비추가가 무엇인가.
7. BEFORE → AFTER → 사용자/플레이어 효과 → trade-off.
8. 실제 실행 증거, `NOT_RUN`, `BLOCKED_UNVERIFIED`, 남은 위험.
9. 다음 Part로 넘겨야 할 학습과 재검토 조건.

## Scope Checker

Strict Part 모드는 semantic owner 경계를 검증하는 **전문/legacy 모드**로 남긴다.

```powershell
python tools/check_base_partition_scope.py --part P04 --files <paths...>
```

현재 기본 coordinator 작업은 다음을 사용한다.

```powershell
python tools/check_base_partition_scope.py --coordinator --base <BASELINE_SHA> --head HEAD
```

Coordinator mode는 다른 Part/CP0 경로를 실패시키는 대신 semantic owner를 표시한다.

```text
PASS  SEMANTIC_OWNER:P01  ...
PASS  SEMANTIC_OWNER:P04  ...
PASS  CONTROL_PLANE_COORDINATOR_WRITE  ...
```

경로가 어떤 Part에도 매핑되지 않으면 `SEMANTIC_OWNER:UNASSIGNED_REVIEW_REQUIRED`로 표시하고 실제 owner/consumer를 검토한다. 이 상태는 자동 자유영역을 뜻하지 않는다.

## Control Plane (CP0)

CP0는 전역 routing/registry/generated/partition 계약의 semantic owner다. coordinator는 현재 사용자 승인 범위에서 필요한 CP0 수정을 할 수 있지만 다음을 지킨다.

- 전역 정본은 한 번만 수정한다.
- generated artifact는 원본 변경 후 재생성한다.
- Registry/route 의미를 바꾸면 실제 consumer와 focused regression을 함께 갱신한다.
- 다른 active workstream이 동일 CP0 의미를 수정 중인지 먼저 확인한다.

대표 CP0:

- `AGENTS.md`, `START_HERE.md`, global operating/routing docs
- Partition Manifest/Prompt/Context contracts
- `skills/SKILL_REGISTRY.json`, shared routes, central evals
- `docs/generated/**`
- `.github/**`
- Base global schemas/integrity/generation

## GPT / Codex

GPT가 기본 planner/reviewer다. 현행 조사·대안·벤치마킹·규칙/Skill/Module 검토·Notion/GitHub 대조·적대적 검토는 GPT에서 닫는다.

`OPTIONAL_CODEX_EXECUTOR`는 실제 code/Scene/Resource/data 변경, 대량 기계 처리, 로컬 Godot/runtime/build/performance 검증처럼 실행 권위가 필요할 때만 사용한다. GPT 작업이 끝났다는 이유만으로 다음 단계처럼 강제하지 않는다.

## Learning + Source

P01~P09 각각의 Learning Log와 Source Radar는 유지한다. 한 채팅을 사용하더라도 현재 Part가 바뀔 때:

- 해당 Part Learning Checkpoint를 기록한다.
- `PART_ONLY / PROJECT_ONLY / BASE_PROMOTION_CANDIDATE / NO_NEW_REUSABLE_LESSON`을 구분한다.
- 기존 Periodic Source Scan Queue의 관련 domain/questions를 사용한다.
- Source 발견 자체를 학습/정본 승격으로 간주하지 않는다.

## 적대적 검토

`FULL_LOOP_COUNT_MINIMUM: 5`

`MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

각 회차는 관점 하나가 아니라 **현재 승인 범위 전체의 완전한 lifecycle**이다. `Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI` 식으로 서로 다른 lens를 한 번씩 돌린 것은 3개의 full loop가 아니며 최소 5회 요건을 충족하지 않는다.

한 counted loop는 최소 다음을 모두 반복한다.

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

회차 보고에 “이번 회차 대표 finding: CI”라고 적을 수는 있지만 **그 대표 finding이 회차의 검토 범위를 뜻하지 않는다.** 최소 5회의 전체 lifecycle을 수행하고, 5회 이후에도 유효 오류·충돌·누락·blocking finding·회귀가 있으면 6..N회를 계속한다.

## Human-facing Home 계약

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Notion의 Base Home과 Project Home은 링크 허브가 아니다. **사람이 Home 한 화면을 읽는 것만으로 핵심을 이해할 수 있어야 하고**, 하위 페이지는 심화·증거·긴 표·전체 asset/log를 보는 drilldown이어야 한다.

### Base Home에 직접 보여줄 것

- Base 목적과 GitHub/Notion authority split
- 전체 lifecycle의 각 단계가 왜 필요한지
- 중요 규칙과 작동 조건
- **Skill 목적 / 호출 조건 / 입력 / 처리 / 출력 / 기대효과 / 연결 Module·consumer·Test**
- Module별 입력→판단/처리→출력→다음 단계, 그리고 **없으면** 생기는 실패
- **P01~P09** 각 책임·대표 Skill/Module·진행 흐름·다른 Part 연결·기대효과·위험/revisit
- 현재 `main`, 완료/미완료 상태, 실제 검증과 `NOT_RUN`

### Project Home에 직접 보여줄 것

- 프로젝트 한 줄 정의와 핵심 플레이어/사용자 가치
- 현재 확정 방향·보호/금지 요소
- Core Loop / 주요 Flow
- 핵심 시스템별 목적·작동·상호작용
- UX/UI/Visual 방향·승인 상태
- 현재 구현상태와 repository/runtime truth 연결
- 검증상태와 evidence ceiling
- 현재 blocker / 다음 작업
- 최근 중요한 결정·이유
- 주요 위험 / revisit condition

하위 페이지가 존재해도 Home의 핵심 설명을 “상세는 링크 참조”로 대체하지 않는다.

## 대안 검토

### A · 9개 별도 채팅 유지 + cross-Part 예외 허용

초기 변경량은 작지만 반복적인 context rehydration, completion packet 전달, chat 관리 비용이 남는다. **REJECT**.

### B · 한 coordinator 채팅 + 순차 Part checkpoint + semantic ownership

Part별 깊이·학습·rollback은 보존하면서 채팅 분산과 cross-Part deadlock을 제거한다. **ADOPT**.

### C · Part 자체 제거 + Base 전체 단일 감사

겉으로 단순하지만 분야별 coverage/학습/Source routing/책임 추적을 잃는다. **REJECT**.

### BETTER_ALTERNATIVE_SEARCH

한 채팅 + 하나의 거대한 P01~P09 PR도 검토했지만 rollback·회귀 원인 추적·사용자 학습 checkpoint가 약해진다. 따라서 **채팅은 하나, Part PR/checkpoint는 순차 유지**가 현재 규모에서 더 강하다.

### LONG_TERM_PLAN_FIT_REQUIRED

1인 개발 + GPT primary 환경에서는 coordinator 방식이 context와 관리비를 가장 적게 만든다. 다음이면 재검토한다.

- 여러 독립 작업자가 Base를 실제로 동시에 자주 수정함
- 한 Part 변경이 지속적으로 대부분의 다른 Part를 함께 바꿔 Part checkpoint 의미가 사라짐
- Base가 한 coordinator conversation의 practical context를 반복적으로 초과함
- semantic owner를 자동 dependency graph로 생성하는 편이 수동 Part map보다 안정적으로 검증됨

## Legacy

Figma, Google Sheets, external HTML workspace, 폐기된 custom local Tool/Hub는 신규 기본 작업면으로 부활시키지 않는다. `UNIQUE / DUPLICATE / OBSOLETE`를 판정하고 UNIQUE의 현행 owner 이관·readback·consumer 확인 후 retirement한다.

## 완료

P01→P09 순차 작업 뒤 같은 coordinator 채팅이 whole-Base Integration을 수행한다.

1. latest main pin
2. 완료된 Part/PR/학습 readback
3. 아직 유효한 cross-Part/CP0 finding 직접 해결
4. Registry/Documentation/generated/Notion 동기화
5. repository-wide regression / Required CI
6. 최소 5회 **진짜 full-scope adversarial loop**, 이후 clean까지 계속
7. exact-head merge
8. post-merge GitHub + Notion Home readback
9. 사용자 학습형 최종보고
