# Base P01~P09 최종 Integration — 동일 Coordinator 채팅 작업지시문

P01→P09 순차 checkpoint를 완료한 **같은 coordinator 채팅**이 최종 ONE BASE 정합성을 닫는다.

## 0. 실행 위치

`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`

`BASE_FULL_PART_COORDINATOR_EXPLICIT_ONLY`

`GENERAL_PROJECT_WORK_USES_GOAL_SCOPED_PHASES`

이 Prompt는 명시적으로 시작된 Base 전체 P01~P09 maintenance session의 최종 통합에만 사용한다. 일반 프로젝트 작업·단일 Goal·진단·질문에는 적용하지 않는다.

현재 이 동일 coordinator 채팅의 canonical 이름은 `CURRENT_COORDINATOR_CHAT`이다.

별도 Integration 채팅을 만들지 않는다. P01~P09를 작업한 현재 채팅이 그대로:

- CP0
- cross-Part 정합성
- Registry/generated surfaces
- Notion Base/Project Home
- 전체 회귀
- 최종 merge/readback

을 책임진다.

## 1. 입력

- latest Base `main` exact SHA
- P01~P09의 실제 merged results / Learning Logs
- 아직 open/draft/ready인 독립 PR 목록
- `CROSS_PART_CHANGE` 기록
- 해결되지 않은 `CROSS_PART_CHANGE_REQUEST`
- current Skill Registry / Module / consumer / Test map
- Base Notion Home과 관련 Project Homes
- 실제 runtime/evidence states

과거 completion packet은 힌트이지 현재 정본이 아니다. 반드시 latest main과 실제 PR 상태를 다시 읽는다.

## 2. Semantic ownership

`PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

다른 Part 또는 CP0 문제라도 현재 Integration에서 검증된 오류·충돌·누락이고 안전한 수정·검증이 가능하면 직접 고친다.

```yaml
CROSS_PART_CHANGE:
  discovered_while: FINAL_INTEGRATION
  semantic_owner: Pxx | CP0
  affected_paths: []
  evidence:
  change:
  consuming_tests: []
  rollback:
```

단순히 owner가 다르다는 이유로 defer하지 않는다.

## 3. Open PR 보호

`OPEN_PR_READ_ONLY_BY_DEFAULT`

`OPEN_PR_MUTATION_REQUIRES_EXPLICIT_NAMED_AUTHORIZATION`

`FOLLOW_UP_TARGET_IS_MERGED_MAIN`

모든 open/draft/ready PR·Branch는 기본 read-only다. latest main과의 차이, 충돌, 중복 여부는 읽을 수 있지만 직접 완료·흡수·종료·병합하지 않는다. 후속 수정은 latest completed `main`에서 새 Branch로 시작한다. 예외는 사용자가 현재 작업에서 PR 번호와 허용 동작을 명시한 경우뿐이다.

## 4. Current-state reconciliation

각 Part에 대해:

1. latest main에 실제 merge됐는가
2. completion packet의 finding이 이미 다른 merge로 해결됐는가
3. 아직 유효한 cross-Part/CP0 문제인가
4. 다른 active workstream과 changed-path/semantic collision이 있는가
5. claimed test가 실제 workflow/command에서 실행되는가
6. Notion human-facing state가 merged facts와 일치하는가

를 다시 판정한다.

## 5. CP0 / Registry / generated

Coordinator는 승인 범위에서 CP0를 수정할 수 있다.

- 전역 owner는 한 번만 수정
- route/Registry 변화는 actual consumer + regression과 함께
- generated artifact는 authority에서 재생성
- stale path/ID/schema/template/test를 active authority로 남기지 않음
- Part semantic owner attribution은 유지

Scope 감사:

```powershell
python tools/check_base_partition_scope.py --coordinator --base <BASELINE_SHA> --head HEAD
```

## 6. Notion

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

### Base Home

메인 한 화면만으로 다음을 이해할 수 있게 한다.

- Base 목적 / authority split
- 전체 lifecycle와 각 단계 목적
- 중요한 규칙과 trigger
- active Skill별 목적·호출 조건·입력·처리·출력·기대효과·Module/Test
- Module별 입력→처리→출력·다음 consumer·없으면 발생하는 실패
- P01~P09 책임·작업흐름·연결·기대효과·위험
- current main / completed / open / NOT_RUN

### Project Home

하위 페이지를 열지 않아도 프로젝트 정의·플레이어 가치·방향·Core Loop·핵심 시스템·UX/UI/Visual·구현상태·검증/evidence ceiling·blocker/다음 작업·중요 결정·위험/revisit을 이해할 수 있게 한다.

하위 페이지는 drilldown/evidence/긴 표/asset/log다.

## 7. Legacy

Figma / Google Sheets / external HTML / retired local Tool/Hub는 신규 authority로 되살리지 않는다. UNIQUE material의 현행 owner 이관·readback·consumer zero를 확인한 뒤 retirement한다.

## 8. Learning / Source

P01~P09 Learning Logs에서:

- PART_ONLY
- PROJECT_ONLY
- BASE_PROMOTION_CANDIDATE
- NO_NEW_REUSABLE_LESSON

을 구분하고 중복 candidate를 합친다. Source Queue 발견은 원출처/증거 검증 전 `UNVERIFIED_DISCOVERY`다.

## 9. 적대적 검토

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS
```

각 counted loop는 다음 전체 lifecycle을 전부 반복한다.

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

`Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`와 같은 lens 분할은 full loop로 계수하지 않는다. 각 full loop에서 필요한 모든 lens를 다시 사용한다.

최소 5회 이후에도 valid error/conflict/omission/blocker/regression/acceptance failure가 하나라도 있으면 6..N회를 계속한다.

## 10. Evidence ceiling

- 파일 존재 != 실행됨
- CI 파일 존재 != 해당 테스트가 실제 workflow에서 실행됨
- Notion 승인 != runtime PASS
- Base guide `ACTIVE_IN_MAIN` != project/device/human/store PASS
- cancelled/superseded CI != PASS
- main이 전진하면 이전 merge-ref readiness evidence는 현재 base에 대해 재검증

## 11. Merge / Post-merge

다음을 모두 만족해야 merge한다.

- current exact head
- Required CI Green
- claimed regression actual consumer 확인
- unresolved review thread 0
- reference/generated freshness closed
- 최소 5 true full loops
- `CLEAN_REVIEW_EXIT`

병합 뒤 새 main과 Notion Base/Project Home을 다시 읽고 실제 반영을 확인한다.

## 12. 최종 사용자 학습형 보고

- Base가 지금 어떻게 작동하는가
- P01~P09가 각각 무엇을 책임지는가
- 핵심 규칙/Skill/Module과 연결
- BEFORE → AFTER
- 실제 수정한 cross-Part/CP0 문제
- 유지/흡수/제거/의도적 비추가
- 실제 CI/runtime/Notion evidence
- NOT_RUN / 남은 위험
- 장기 효과 / trade-off / revisit conditions
- true full adversarial loop 수와 주요 finding
