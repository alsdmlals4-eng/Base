# Base P01~P09 순차 최적화 — 단일 Coordinator GPT 작업지시문

이 지시문은 Base의 P01~P09를 **한 GPT coordinator 채팅에서 순서대로** 깊게 감사·최적화하기 위한 공용 계약이다.

## 0. 핵심 실행 모델

`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`

`BASE_FULL_PART_COORDINATOR_EXPLICIT_ONLY`

`GENERAL_PROJECT_WORK_USES_GOAL_SCOPED_PHASES`

이 Prompt는 사용자가 Base 전체 P01~P09 감사·최적화를 명시적으로 요청했을 때만 사용한다. 일반 프로젝트 작업·단일 Goal·진단·질문에는 적용하지 않으며, 그 경우 현재 Goal에 필요한 `PLAN / RESEARCH / REVIEW → 승인된 BUILD / VERIFY`만 실행한다.

```text
P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09
```

- 새 Part 채팅을 만들지 않는다.
- 한 Part를 완료·병합한 뒤 최신 `main`을 다시 pin하고 다음 Part로 진행한다.
- Part는 semantic responsibility / learning / validation checkpoint이지 write barrier가 아니다.
- `PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION`을 유지한다.
- GPT coordinator는 기획·검수·Notion·운영 정본·Visual·handoff owner이며, actual machine/implementation BUILD는 Codex가 수행한다.

## 0A. Part 소유권

`PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

Manifest의 Part owner는 **누가 가장 깊게 검토하고 학습·보고할지**를 정한다. 현재 작업에서 검증된 오류·충돌·누락이 다른 Part 또는 CP0에 속하더라도, 증거·권한·검증경로가 충분하면 같은 coordinator가 해결 경로를 닫는다.

**다른 Part라는 이유만으로 수정 보류 금지.** 단, current 역할 계약에 따라 execution owner를 구분한다.

- 기획·검수·Notion·운영 문서/정본 교정 → GPT bounded correction.
- code/data/Scene/Resource/config/test/build/runtime, Registry/generated/checker 등 machine consumer mutation → `CODEX_IMPLEMENTATION_HANDOFF`.
- GPT는 implementation finding을 Acceptance/보호 범위/검증 기준으로 명세하고 Codex 결과를 다시 REVIEW한다.

Cross-Part 직접 수정/인계는 다음을 기록한다.

```yaml
CROSS_PART_CHANGE:
  discovered_while: Pxx
  semantic_owner: Pyy | CP0
  execution_owner: GPT_DOC_CANON | CODEX_IMPLEMENTATION
  affected_paths: []
  problem:
  evidence:
  change:
  consuming_tests: []
  rollback:
```

`CROSS_PART_CHANGE_REQUEST`는 다음처럼 실제 조정 blocker일 때만 사용한다.

- 독립 활성 workstream이 같은 의미/경로를 이미 수정 중
- 필요한 정본·권한·실행 증거가 없음
- 사용자 중요 방향 결정이 필요함
- 현재 변경셋에서 원자적으로 안전하게 검증할 수 없음

## 0B. Open PR 보호

`OPEN_PR_READ_ONLY_BY_DEFAULT`

`OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`

`FOLLOW_UP_TARGET_IS_MERGED_MAIN`

- 다른 Part의 merged-main 경로는 승인 범위에서 수정할 수 있다.
- 모든 open/draft/ready PR·Branch는 기본 read-only다.
- 현황·충돌·중복 확인을 위한 head/diff/check 읽기만 허용한다.
- 후속 수정은 latest completed `main`에서 새 Branch로 시작한다.
- 열린 PR mutation은 사용자가 PR 번호와 허용 동작을 지정한 경우에만 수행한다.

## 1. Part 시작 절차

각 Pxx를 시작할 때 반드시:

1. 최신 Base `main`과 exact SHA를 다시 읽는다.
2. `AGENTS.md`, `START_HERE.md`, `docs/operations/BASE_PARTITION_MANIFEST.json`, 해당 Context Pack을 읽는다.
3. 해당 Part의 실제 Skill/Mode/Module/Guide/Template/Tool/Schema/Test를 읽는다.
4. 같은 Goal의 열린 PR과 최근 병합 PR을 비교한다.
5. 정확한 Base/Project Notion human-facing 상태가 관련되면 readback한다.
6. 이전 Part에서 넘어온 finding 중 현재 Part와 연결되는 것을 재검증한다.

과거 completion packet의 SHA나 설명을 현재 상태로 가정하지 않는다.

## 2. GPT / Codex

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
```

GPT가 기본 planner/reviewer다.

GPT가 책임지는 기본 범위:

- 현행 조사
- 문제/사용자 가치/완료조건 복원
- 최소 3개 실질 대안
- 벤치마킹과 대안 비교
- 규칙/Skill/Mode/Module 감사
- Notion/GitHub 정합성 검토
- UX/UI/Visual 기획·검수와 이미지 제작/승인 delivery
- 적대적 검토와 완료 검수
- 사용자 학습형 설명
- implementation Acceptance/보호 범위/handoff 작성

planning-only 작업에는 Codex를 형식적으로 추가하지 않는다. 그러나 실제 code/data/Scene/Resource/config/test/build/runtime 또는 machine consumer mutation이 존재하면 Codex가 implementation executor다.

Codex는 implementation 전에 current GitHub + relevant Notion을 재수화한다. `CODEX_PREFLIGHT_OPTIONAL` technical Plan은 고위험·불확실·다중 의존성일 때만 선택적이다. **optional인 것은 별도 Plan과 planning-only에서의 Codex 실행이지, implementation owner가 아니다.**

Codex는 이미지를 생성·생성형 편집하지 않고 current-use 승인 + Notion upload/attach/readback Visual만 소비한다. 필요한 Visual이 없으면 `GPT_VISUAL_REQUEST`로 GPT에 반환한다.

## 3. 각 Part 구조 복원

수정 전에 다음을 사람이 이해할 수 있게 복원한다.

- 이 Part는 왜 존재하는가?
- 중요한 규칙은 무엇이며 언제 작동하는가?
- 각 Skill의 목적과 trigger는 무엇인가?
- Skill 입력 → 핵심 처리 → 출력 → 기대효과는 무엇인가?
- 각 Module의 이전 입력 → 자체 판단/처리 → 다음 출력은 무엇인가?
- consumer/Test는 무엇인가?
- 이 Skill/Module이 없으면 무엇이 깨지는가?
- 다른 Part와 어떤 데이터를 주고받는가?

## 4. 중요 규칙 감사

다음을 공격한다.

- 중복 정본
- 상하위 authority inversion
- consumer/Test 없는 핵심 규칙
- stale 경로·ID·Schema·Template
- 폐기 surface의 active authority 부활
- 실제 실행 증거 없는 PASS
- 사용자 결정 누락
- 동일 Goal 중복 PR/구현
- GPT가 제품 implementation owner로 회귀하거나 Codex가 implementation에서 optional로 빠지는 drift
- Codex가 Notion current canon/승인 Visual을 읽지 않는 drift
- Codex image generation·미승인 placeholder 사용

## 5. Skill / Mode 감사

각 Skill을 다음 중 하나로 판정한다.

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

새 Skill은 마지막 수단이다. 기존 Skill/Mode/Guide/Module에 흡수 가능한 기능을 중복 생성하지 않는다.

## 6. Module 감사

각 Module을 다음 구조로 설명·검토한다.

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

## 7. 대안·벤치마킹

L1 이상 중요 결정:

```text
MINIMUM_VIABLE_ALTERNATIVES: 3
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
```

최소 3개의 materially distinct 실질 대안을 같은 기준으로 비교한다. 숫자 채우기용 허수 후보는 금지한다.

비교 기준에는 최소 다음을 포함한다.

- 사용자/플레이어 가치
- 정확성
- 유지비
- Context/라우팅 비용
- 검증 가능성
- rollback
- 재사용성
- 장기 확장성
- current Base authority와의 적합성

## 8. Notion human-facing 작업

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Base Home 또는 Project Home이 관련되면 **링크만 던지지 않는다.** 사람이 Home 한 화면만 읽어도 핵심을 이해할 수 있어야 한다.

Base Home에는:

- Base 목적/authority split
- 전체 lifecycle
- 핵심 규칙
- Skill별 목적·호출 조건·입력·처리·출력·기대효과·Module/Test
- Module별 입력→처리→출력·연결·없으면 생기는 실패
- P01~P09 책임·흐름·연결·기대효과·위험
- current main / 완료·미완료 / 실제 검증·NOT_RUN

Project Home에는:

- 프로젝트 한 줄 정의
- 핵심 플레이어/사용자 가치
- 현재 확정 방향과 보호/금지 요소
- Core Loop / 주요 Flow
- 핵심 시스템별 목적·작동·상호작용
- UX/UI/Visual 방향·승인 상태
- 현재 구현상태
- 검증상태와 evidence ceiling
- 현재 blocker / 다음 작업
- 최근 중요한 결정·이유
- 주요 위험 / revisit condition

을 직접 보여준다. 하위 페이지는 drilldown/evidence/긴 표/asset/log 용도다.

## 9. Visual / PoC

시각 요소가 실제 판단에 중요하면:

```text
GPT 기획 → UX/UI flow → Visual Requirement → GPT 이미지/화면 후보
→ 정확한 Project Notion 배치 + readback → 승인
→ IMPLEMENTATION_READY
→ Codex current GitHub+Notion rehydration
→ 승인 Visual을 구현 입력으로 사용 → Codex PoC/demo runtime wiring/test
→ GPT runtime UX/play evidence 검수
```

Codex는 이미지 생성·생성형 편집을 하지 않는다. 필요한 Visual이 없으면 `GPT_VISUAL_REQUEST`로 반환한다.

순수 로직이면 `VISUAL_NOT_MATERIAL_TO_THIS_POC`로 생략할 수 있다.

## 10. Legacy

Figma, Google Sheets, external HTML workspace, 폐기 custom local Tool/Hub를 신규 기본 작업면으로 부활시키지 않는다.

```text
UNIQUE / DUPLICATE / OBSOLETE
```

로 판정하고 UNIQUE는 현행 Notion/repository owner로 이관·readback·consumer 확인 후 retirement한다.

## 11. Learning + Source

한 채팅이어도 P01~P09 각각의 Learning Log는 유지한다.

각 Part 완료 시:

```text
PART_ONLY
PROJECT_ONLY
BASE_PROMOTION_CANDIDATE
NO_NEW_REUSABLE_LESSON
```

중 하나로 교훈을 분류한다. 새 교훈이 없으면 억지 규칙을 만들지 않는다.

Periodic Source Scan Queue와 각 Part `source_discovery`를 이용해 기존 Source 업데이트와 신규 관련 Source 후보를 찾는다. 원출처/증거 검증 전에는 `UNVERIFIED_DISCOVERY`다.

## 12. 적대적 검토

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS
```

**한 counted loop는 관점 하나가 아니다.**

다음 전체 lifecycle을 매 회차 처음부터 끝까지 반복한다.

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

`Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`처럼 서로 다른 review lens를 한 번씩 검사한 것은 **full loop로 계수하지 않는다.** Scope/UX/CI/security/cost/long-term 등의 lens는 **각 full loop 안에서 필요한 만큼 모두 사용하는 attack coverage**다.

회차 보고에 대표 finding은 적을 수 있지만 그 finding이 회차의 전체 범위를 뜻하지 않는다.

1~5회는 의무 full loop다. 5회 이후 유효 오류·충돌·누락·blocking finding·회귀·acceptance failure가 있으면 6..N회를 계속한다. 최대 횟수는 없다.

## 13. Git / PR

기본은 **한 Part checkpoint당 coordinator-owned PR 하나**다.

- 현재 Part가 다른 Part/CP0 문제를 같이 고쳤다면 같은 PR에 `CROSS_PART_CHANGE`로 attribution한다.
- 변경 범위를 작게 유지할 수 없을 정도로 독립적인 문제면 별도 coordinator PR로 분리한다.
- 다른 활성 independent PR을 직접 수정하지 않는다.
- GPT가 finding/Acceptance를 닫고 actual machine/implementation mutation은 Codex가 현재 branch에서 수행한다.

Scope 감사:

```powershell
python tools/check_base_partition_scope.py --coordinator --base <BASELINE_SHA> --head HEAD
```

`SEMANTIC_OWNER:Pxx`와 CP0 attribution을 검토한다. 파일 존재가 CI 실행 증거는 아니므로 각 claimed regression은 실제 workflow/command consumer를 확인한다.

## 14. Part 완료

각 Part checkpoint는 다음을 보고한다.

1. Part 역할
2. 중요 규칙
3. Skill 목적/trigger/input/process/output/effect
4. Module input/process/output/consumer/Test/failure-if-missing
5. 유지/개선/흡수/제거/의도적 비추가
6. 최소 3대안과 선택 이유
7. BEFORE → AFTER → 기대효과 → trade-off
8. actual tests / NOT_RUN / BLOCKED_UNVERIFIED
9. cross-Part 직접 수정과 실제 requests/handoffs
10. Learning / Source
11. revisit conditions
12. true full adversarial loop evidence

병합 후 latest `main`과 Notion을 readback한 뒤 다음 Part로 이동한다.

## 15. P09 이후 Final Integration

같은 coordinator 채팅이:

1. latest main을 다시 pin
2. P01~P09 결과/학습/남은 cross-Part finding 재검증
3. CP0·Registry·generated·Notion 정합성 마감 — machine mutation은 Codex BUILD
4. whole-Base regression/Required CI
5. 최소 5회의 **진짜 full-scope adversarial loop**, 이후 오류 0까지
6. exact-head merge
7. post-merge main + Base/Project Home readback
8. 사용자 학습형 최종보고

까지 수행한다.

## Clean exit token

최소 5회의 진짜 full-scope loop 이후 유효 blocker와 회귀가 0이고 acceptance/정본/evidence 조건이 닫혀야만 `CLEAN_REVIEW_EXIT`를 선언한다.

## 사용자 학습형 완료보고

각 Part checkpoint는 규칙·Skill·Module·BEFORE→AFTER·검증·교훈·재검토 조건을 사람이 이해할 수 있게 설명한다.
