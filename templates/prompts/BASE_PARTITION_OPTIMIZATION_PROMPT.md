# Base P01~P09 순차 최적화 — 단일 Coordinator GPT 작업지시문

이 지시문은 Base의 P01~P09를 **한 GPT coordinator 채팅에서 순서대로** 감사·최적화하기 위한 공용 계약이다.

## 0. 핵심 실행 모델

```text
SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS
BASE_FULL_PART_COORDINATOR_EXPLICIT_ONLY
GENERAL_PROJECT_WORK_USES_GOAL_SCOPED_PHASES
PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER
OPEN_PR_READ_ONLY_BY_DEFAULT
```

이 Prompt는 사용자가 Base 전체 감사를 명시 요청했을 때만 사용한다.

```text
P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09
```

- 새 Part 채팅을 만들지 않는다.
- 한 Part 완료/병합 뒤 latest `main`을 다시 pin한다.
- Part는 semantic responsibility / learning / validation checkpoint다.
- Base 작업은 **전부 GPT maintenance 영역**이다.

## 0A. Codex 사용 금지 경계 — Base 자체

```text
BASE_GOVERNANCE = GPT
BASE_POLICY_SKILL_GUIDE_TEMPLATE = GPT
BASE_REGISTRY_GENERATED_MANIFEST = GPT
BASE_PYTHON_TEST_CI_CHECKER = GPT
BASE_NOTION = GPT
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
```

Base 내부에 `.py`, `.json`, workflow, checker가 있어도 Codex 작업으로 넘기지 않는다.

`Base Python contract test·Registry/generated·CI policy` 역시 GPT-owned Base maintenance다.

Codex는 이 Prompt가 다루는 Base repository 자체를 구현하는 worker가 아니다. 별도의 **게임 프로젝트에 실제 Godot 제품 구현이 필요해졌을 때만** 그 프로젝트용 Codex Godot Work Instruction을 작성한다.

## 1. Part 시작 절차

각 Pxx 시작 시:

1. 최신 Base `main` exact SHA 확인
2. `AGENTS.md`, `START_HERE.md`, `BASE_PARTITION_MANIFEST.json`, 해당 Context Pack 확인
3. 해당 Part의 Skill/Mode/Module/Guide/Template/Tool/Schema/Test 읽기
4. 같은 Goal의 open/recent merged PR 비교
5. 관련 Notion human-facing 상태 readback
6. 이전 Part finding 재검증

과거 completion packet의 SHA를 current truth로 가정하지 않는다.

## 2. Part 소유권

`PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

**다른 Part라는 이유만으로 수정 보류 금지.** Base의 다른 Part/CP0 finding도 현재 GPT coordinator가 증거·권한·검증경로를 확보하면 직접 교정한다.

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

`CROSS_PART_CHANGE_REQUEST`는 실제 coordination blocker에만 쓴다.

## 3. Open PR 보호

```text
OPEN_PR_READ_ONLY_BY_DEFAULT
OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION
FOLLOW_UP_TARGET_IS_MERGED_MAIN
```

- 다른 open/draft/ready PR·Branch는 read-only
- head/diff/check read만 가능
- checkout/write/rebase/close/merge/absorb 금지
- 열린 PR을 바꾸려면 사용자가 **PR 번호와 허용 동작**을 지정
- 일반 후속 작업은 latest completed main에서 시작

## 4. 각 Part 구조 복원

수정 전에 다음을 설명한다.

- 왜 존재하는가
- 중요 규칙과 trigger
- Skill 목적 / input / process / output / expected effect
- Module input → decision/process → output
- consumer/Test
- 없으면 어떤 실패가 생기는가
- 다른 Part와의 데이터 연결

## 5. 중요 규칙 감사

공격 대상:

- 중복 정본
- authority inversion
- consumer/Test 없는 핵심 규칙
- stale path/ID/Schema/Template
- retired surface 부활
- 실제 실행 증거 없는 PASS
- 사용자 결정 누락
- 동일 Goal 중복 PR/구현
- GPT/Codex owner drift

Base의 owner drift 기준:

- Base/Notion/문서/Registry/generated/CI/test → GPT
- 실제 게임 프로젝트 Godot runtime 구현 → 별도 프로젝트 Codex handoff

## 6. Skill / Mode 감사

```text
KEEP
IMPROVE
MERGE
ABSORB
SPLIT
RECLASSIFY
DEPRECATE
ARCHIVE
BLOCKED_UNVERIFIED
```

새 Skill은 마지막 수단이다. Existing Solution First를 적용한다.

## 7. Module 감사

```yaml
module:
  responsibility:
  inputs: []
  decision_or_process:
  outputs: []
  consumers: []
  related_skills: []
  tests: []
  failure_if_missing:
```

응집도·결합도·canonical owner·interface·재사용·rollback·독립 검증 가능성을 본다.

## 8. 대안·벤치마킹

```text
MINIMUM_VIABLE_ALTERNATIVES: 3
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
```

최소 3개 materially distinct 대안을 같은 기준으로 비교한다.

- 사용자/플레이어 가치
- 정확성
- 유지비
- Context/routing 비용
- 검증 가능성
- rollback
- 재사용성
- 장기 확장성
- current Base authority 적합성

## 9. Notion human-facing 작업

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Base Home에는 목적·authority split·lifecycle·규칙·Skill/Module·P01~P09·상태·검증을 직접 보여준다.

Project Home에는 프로젝트 정의·player value·확정 방향·Core Loop·Flow·핵심 시스템·표·UX/UI/Visual·구현상태·검증·blocker·결정을 직접 보여준다.

Notion 작업은 GPT가 수행하고 destination readback한다.

## 10. Visual

Base/Project Visual 기획·생성·편집·검수·Notion 배치는 GPT 역할이다.

```text
GPT 기획
→ Visual Requirement
→ GPT image/mock/diagram
→ Project Notion upload/attach/readback
→ 승인
```

그 Visual을 실제 게임 runtime에 연결하는 별도 Godot 구현이 생기면 그때 **해당 게임 프로젝트** Codex Work Instruction을 만든다.

Codex가 Base 작업 안에서 이미지를 만들거나 Base 문서를 구현하는 흐름을 만들지 않는다.

## 11. Legacy

Figma, Google Sheets, external HTML workspace, retired custom local Tool/Hub를 신규 기본 작업면으로 부활시키지 않는다.

```text
UNIQUE / DUPLICATE / OBSOLETE
```

UNIQUE만 현행 Notion/repository owner로 이관하고 readback 후 retirement한다.

## 12. Learning + Source

각 Part 완료 시:

```text
PART_ONLY
PROJECT_ONLY
BASE_PROMOTION_CANDIDATE
NO_NEW_REUSABLE_LESSON
```

Periodic Source Scan Queue를 사용하되 discovery를 곧바로 canon으로 승격하지 않는다.

## 13. 적대적 검토

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS
```

한 counted loop는 다음 전체 lifecycle이다.

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

1~5회는 의무이고, 5회 이후에도 오류·충돌·누락·blocker가 있으면 계속한다.

## 14. Git / PR

기본은 Part checkpoint당 coordinator-owned PR 하나다.

- 다른 Part/CP0 Base finding은 `CROSS_PART_CHANGE` attribution으로 같은 GPT workstream에서 수정 가능
- independent open PR은 직접 수정하지 않음
- Scope checker:

```powershell
python tools/check_base_partition_scope.py --coordinator --base <BASELINE_SHA> --head HEAD
```

`SEMANTIC_OWNER:Pxx`와 `CONTROL_PLANE_COORDINATOR_WRITE`를 검토한다.

## 15. Part 완료

각 Part는 다음을 보고한다.

1. 역할
2. 중요 규칙
3. Skill purpose/trigger/input/process/output/effect
4. Module input/process/output/consumer/Test/failure-if-missing
5. 유지/개선/흡수/제거
6. 최소 3대안과 선택 이유
7. BEFORE → AFTER → 기대효과 → trade-off
8. actual tests / NOT_RUN / BLOCKED_UNVERIFIED
9. cross-Part Base 수정
10. Learning / Source
11. revisit conditions
12. full adversarial loop evidence

병합 후 latest main과 Notion을 readback하고 다음 Part로 간다.

## 16. P09 이후 Final Integration

같은 GPT coordinator가:

1. latest main repin
2. P01~P09 결과/학습/finding 재검증
3. CP0·Registry·generated·Notion 정합성 **직접 마감**
4. whole-Base regression/Required CI
5. 최소 5회 full-scope adversarial loop, 이후 오류 0까지
6. exact-head merge
7. post-merge main + Base/Project Home readback
8. 사용자 학습형 최종보고

까지 수행한다.

## Clean exit token

최소 5회 full-scope loop 이후 blocker·회귀·acceptance·정본·evidence 문제가 0이어야 `CLEAN_REVIEW_EXIT`다.

## 사용자 학습형 완료보고

최종 보고는 `작업 전 → 개선된 기능 → 실제 사용 예 → 기대효과 → 아직 개선되지 않은 범위`를 중심으로 사람이 이해할 수 있게 설명한다.

## 현재 역할 한 줄

> **Base 최적화는 GPT가 끝까지 수행한다. Codex는 Base 작업자가 아니라 실제 게임 프로젝트의 Godot 제품 구현자다.**
