# Base Partition Operating Model v2

## 목적

Base는 **하나의 통합 시스템(ONE BASE)** 이다. P01~P09는 별도 runtime이나 9개 채팅이 아니라 semantic responsibility / maintenance / learning view다.

기계 책임 지도는 `docs/operations/BASE_PARTITION_MANIFEST.json`이 소유한다.

## 현재 실행 계약

```text
SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS
BASE_FULL_PART_COORDINATOR_EXPLICIT_ONLY
GENERAL_PROJECT_WORK_USES_GOAL_SCOPED_PHASES
PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER
```

Base 전체 감사를 명시 요청했을 때 한 GPT coordinator가 순차 처리한다.

```text
latest main pin
→ P01 → merge/postmerge readback
→ latest main repin
→ P02
→ ...
→ P09
→ final whole-Base integration
```

정확한 순서:

```text
P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09
```

새 Part 채팅을 만들지 않는다. Part checkpoint는 rollback·검증·학습 attribution을 위해 유지한다.

## Base 작업의 실행 Owner

**Base 자체 P01~P09와 CP0 maintenance는 전부 GPT가 담당한다.**

```text
BASE_PARTITION_MAINTENANCE_OWNER = GPT
BASE_POLICY_SKILL_GUIDE_TEMPLATE = GPT
BASE_REGISTRY_GENERATED_MANIFEST = GPT
BASE_PYTHON_TEST_AND_CI_CONTRACT = GPT
BASE_NOTION = GPT
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
```

Base의 Python test, Registry/generated checker, CI workflow가 코드라는 이유로 Codex에 넘기지 않는다. `Base Python tests, Registry/generated/CI`는 GPT-owned Base maintenance다.

Codex가 등장하는 경우는 Base maintenance 자체가 아니라, **별도의 실제 게임 프로젝트에서 Godot 제품 구현 task가 생성됐을 때**다.

```text
Base/P04/P05/P06 기획·검수 finding
→ GPT가 Base/Notion/설계 정본화
→ 특정 게임 프로젝트에 실제 Godot 구현이 필요함
→ 그 프로젝트용 Codex Godot Work Instruction
→ Codex가 해당 프로젝트 GitHub+Notion을 읽고 구현
```

## Part 소유권의 의미

`PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

Manifest의 owner는 다음을 뜻한다.

- 누가 해당 의미를 가장 깊게 이해·감사하는가
- 어느 Learning Log에 교훈을 남기는가
- 완료보고에서 어느 Part 성과인가
- 어떤 consumer/Test를 우선 검증하는가

**다른 Part라는 이유만으로 수정 보류 금지.** GPT coordinator가 증거와 검증 경로를 확보하면 다른 Part/CP0의 Base finding도 현재 workstream 안에서 교정할 수 있다.

```yaml
CROSS_PART_CHANGE:
  discovered_while: Pxx
  semantic_owner: Pyy | CP0
  execution_owner: GPT_BASE_MAINTENANCE
  affected_paths: []
  problem:
  evidence:
  change:
  consuming_tests: []
  rollback:
```

`CROSS_PART_CHANGE_REQUEST`는 실제 조정 blocker에만 쓴다.

- 다른 독립 active workstream이 같은 의미/경로를 수정 중
- 필요한 권한·정본·증거가 없음
- 사용자 중요 제품 결정 필요
- 현재 change set에서 안전한 원자 검증 불가

## Open PR 보호

```text
OPEN_PR_READ_ONLY_BY_DEFAULT
OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION
FOLLOW_UP_TARGET_IS_MERGED_MAIN
```

모든 `open/draft/ready` PR·Branch는 기본 read-only다.

- head/diff/check 읽기: 허용
- checkout/write/rebase/close/merge/selective-copy/material-delta 흡수: 금지
- 일반 후속 작업은 latest completed main에서 시작
- 열린 PR mutation은 사용자가 **PR 번호와 허용 동작**을 지정한 경우에만 수행

현재 task의 명시된 PR은 standing current-work authorization 범위에서만 처리한다.

## ONE BASE와 P01~P09

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
                   GPT Coordinator
                            │
                         ONE BASE
```

## P01~P09 책임

| Part | 책임 | 대표 출력 |
|---|---|---|
| P01 | Project Planning, Operations & Notion | 작업 계약·Home·handoff·continuity |
| P02 | Skill Governance, Canon Freshness & Legacy | Registry/owner/freshness/retirement |
| P03 | Adversarial Quality, Refactoring & Git Integrity | finding·회귀·Git 안전 |
| P04 | Game Design, Core, Player Research & Vertical Slice | player promise·Core·slice acceptance |
| P05 | Art, UX/UI & Visual Assets | Visual direction·UX flow·승인 asset |
| P06 | Godot, Runtime & Technical Toolchain | Godot 구현 요구·runtime 기준·toolchain 계약 |
| P07 | Platform, Release & Execution Validation | evidence ceiling·build/release readiness |
| P08 | AI Operations & External Executors | GPT/Codex/외부 AI 역할·cost/context routing |
| P09 | Content, Narrative & Publication | canon/voice/publication evidence |

P06 Base 문서는 GPT가 관리한다. **P06의 설계가 특정 게임 프로젝트의 GDScript/Scene/Resource/runtime 변경으로 이어질 때만 그 프로젝트 구현을 Codex가 수행**한다.

## Part checkpoint 필수 설명

1. 이 Part가 왜 존재하는가
2. 중요한 규칙과 trigger
3. Skill 목적 / 입력 / 처리 / 출력 / 기대효과 / consumer/Test
4. Module 입력 → 판단/처리 → 출력
5. 없으면 어떤 실패가 생기는가
6. KEEP / IMPROVE / ABSORB / RETIRE
7. BEFORE → AFTER → 효과 → trade-off
8. actual evidence / `NOT_RUN` / `BLOCKED_UNVERIFIED`
9. 다음 Part 학습과 revisit condition

## Scope Checker

Strict Part mode:

```powershell
python tools/check_base_partition_scope.py --part P04 --files <paths...>
```

GPT coordinator mode:

```powershell
python tools/check_base_partition_scope.py --coordinator --base <BASELINE_SHA> --head HEAD
```

예상:

```text
PASS SEMANTIC_OWNER:P01
PASS SEMANTIC_OWNER:P04
PASS CONTROL_PLANE_COORDINATOR_WRITE
```

경로가 매핑되지 않으면 `SEMANTIC_OWNER:UNASSIGNED_REVIEW_REQUIRED`다.

## Control Plane (CP0)

CP0는 전역 routing/Registry/generated/partition 계약의 semantic owner다. **CP0 수정 역시 GPT Base maintenance 작업**이다.

대표 CP0:

- `AGENTS.md`, `START_HERE.md`, global routing docs
- Partition Manifest / Prompt / Context contracts
- `skills/SKILL_REGISTRY.json`
- `docs/generated/**`
- `.github/**`
- Base schemas/integrity/generation
- Base Python contract tests

규칙:

- 전역 정본은 한 번만 수정
- generated는 source 변경 후 정식 생성 경로로 재생성
- Registry/route 의미 변경 시 consumer/focused regression 함께 갱신
- 독립 open workstream overlap 먼저 확인

## 적대적 검토

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS
```

한 counted loop는 하나의 lens가 아니라 current scope 전체 lifecycle이다.

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

최소 5회 후에도 finding이 있으면 6..N회를 계속한다.

## Human-facing Home

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Base Home과 Project Home은 링크 허브가 아니다. Home만 읽어도 핵심 목적·Flow·시스템·데이터·Visual·현재 상태·검증·위험을 이해할 수 있어야 한다.

AI/System metadata·raw SHA·test receipt는 상세 운영면에 둔다.

## Learning + Source

Part별 Learning Log와 Source Radar를 유지한다.

```text
PART_ONLY
PROJECT_ONLY
BASE_PROMOTION_CANDIDATE
NO_NEW_REUSABLE_LESSON
```

Source 발견 자체를 정본 승격으로 보지 않는다.

## 대안 검토

### A · 9개 별도 채팅 유지
Context 재수화와 handoff 관리비가 커서 **REJECT**.

### B · 한 coordinator 채팅
Part별 semantic checkpoint와 rollback을 유지하면서 한 GPT coordinator가 순차 처리한다. **ADOPT**. 새 Part 채팅을 9개 만들지 않는다.

### C · Part 자체 제거
책임·학습·source coverage가 흐려져 **REJECT**.

`BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_REQUIRED`를 유지하고, 동시작업·context 규모·Part 결합도가 달라지면 **재검토**한다.

## Final Integration

P01→P09 뒤 같은 GPT coordinator가:

1. latest main pin
2. 모든 Part 결과/학습 readback
3. cross-Part/CP0 Base finding 직접 교정
4. Registry/generated/Documentation/Notion 정합성 마감
5. repository-wide regression / Required CI
6. 최소 5회 full-scope adversarial loop 후 clean
7. exact-head merge
8. post-merge GitHub + Notion readback
9. 사용자 학습형 최종보고

를 수행한다.

## Codex 경계 한 줄

> **Base는 전부 GPT maintenance 영역이다. Codex는 Base 작업자가 아니라 실제 게임 프로젝트의 Godot 제품 구현자다.**
