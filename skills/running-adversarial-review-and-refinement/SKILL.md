---
name: running-adversarial-review-and-refinement
description: Use when a work product, repository, PR, or merged decision must be attacked for failure, its criticisms validated, and approved findings regression-checked.
---

# Running Adversarial Review and Refinement

## Purpose and separation

적대적 검토는 승인 거부 증거를 찾는 공격 단계다. 그러나 **비판도 오류·취향·과잉 요구**일 수 있으므로 공격과 검증을 분리하고, 검증된 문제만 최소 수정한다.

사용자안과 AI 최초안은 같은 평가 기준으로 공격·검증한다. 검토 목적은 이견 생산이 아니라 실패 가능성 감소다. 사용자안이 반례·위험 검토를 통과해 가장 강한 결론이면 근거와 함께 동의할 수 있다.

Registry의 `칭찬·균형 평가만 요청` 비사용 조건은 결정·권장안이 없는 설명형 칭찬·균형 요약에만 적용한다. L1 이상 기능·설계·아키텍처·정책·방향 결정이나 중요 권장안이 포함된 균형 비교는 적대 검토 대상이다.

실제 diff·정적·런타임·접근성·성능 증거는 `reviewing-and-validating-project-changes`, 프로젝트 코어 판정·확정은 관련 코어 Skill이 책임진다. 승인 결정·GitHub·Notion/GitHub 동기화는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다. 구형본의 archive·compatibility·삭제는 `governing-legacy-retention-and-archives`, 정본·경로·ID·Template·Test 전파는 `auditing-canonical-reference-freshness`가 책임진다.

## Skill Modes

- `attack`: 작업물이 실패했다고 가정하고 결함·모순·누락·악용·경계 실패를 찾는다.
- `validate-critique`: 공격 결과의 사실성·발생 가능성·영향·범위·비용·코어 위험을 재검증한다.
- `refine-approved-findings`: `MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정한다.
- `regression-recheck`: 수정 전후의 정상 경로·코어·데이터·호환성·새 결함을 다시 공격한다.
- `decision-report`: 반영·보류·기각·미검증과 남은 위험을 기록한다.
- `post-merge-review`: 병합 또는 직접 `main` 결정 Commit 뒤 새 `main`·Decision·정본·실제 diff·Notion/GitHub sync·PR·branch를 다시 검토한다.
- `repository-wide-audit`: 저장소 전체의 권한 지도, 중복·stale·고아 파일, 구형 계약, untouched 소비자, Prompt·파생본 drift를 공격하고 전문 Skill로 처리를 라우팅한다.

일반 작업은 `attack → validate-critique → refine-approved-findings → regression-recheck → decision-report`를 사용한다. 저장소 전체 감사는 `references/repository-wide-audit-protocol.md`, 세부 Finding·회귀 판정은 `references/finding-and-regression-protocol.md`를 필요할 때만 읽는다.

### Finding validation evidence guard

`FIX_GUIDED_VERIFICATION_WHEN_EXECUTABLE: REQUIRED`

구체적 수정으로 재현 가능한 Finding은 같은 acceptance/evidence ceiling에서 baseline과 candidate를 비교해 비판 자체를 재검증한다. candidate가 원 실패를 줄이지 못하거나 새 회귀를 만들면 심각도와 채택 여부를 다시 판정한다. 순수 기획·미감처럼 동등한 실행 비교가 불가능한 문제에는 억지로 적용하지 않는다. 세부 기록은 `references/finding-and-regression-protocol.md`를 따른다. 실제 runtime/build/render PASS 권위는 해당 validation owner를 넘지 않는다.

### Adversarial review until clean invariant

이 Skill을 L1 이상 작업물·PR·저장소 감사·병합 후 결과의 적대적 검토로 호출하면 **최소 5회의 완전한 전체 개선 루프를 수행하고, 그 이후 CLEAN_REVIEW_EXIT까지 전체 검토·개선 생명주기를 반복한다.** `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`다. 5회는 종료 quota나 최대치가 아니라 최소 floor다. 앞 회차의 수정 결과와 새 증거 자체가 다음 회차의 공격 입력이다.

```text
ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS
FULL_SCOPE_REVIEW
FIND → VALIDATE → REFINE → VERIFY → RE-ATTACK
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_RECHECK
CLEAN_REVIEW_EXIT
```

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`: `Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`처럼 서로 다른 관점을 각각 한 번 검사한 것은 여러 full loop로 계수하지 않는다. Scope·UX·CI·security·cost·long-term 등 필요한 lens는 **각 counted loop 안에서** 전체 승인 범위를 다시 공격하기 위한 coverage로 사용한다. 회차별 대표 finding을 기록할 수는 있지만 대표 finding이 그 회차의 검토 범위를 뜻하지 않는다.

한 전체 회차:

```text
FULL_SCOPE_REVIEW
→ attack
→ validate-critique
→ refine-approved-findings
→ regression-recheck / execution verification
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ decision-report
→ RE-ATTACK resulting state
```

각 회차는 사용자 의도·핵심 방향·정본/owner/routing·Skill/Tool/Module·실제 구현·데이터·자산·실패복구·보안·동시성·비용·벤치마크·장기 유지·증거·완료조건을 전체적으로 다시 본다.

각 loop evidence:

```yaml
loop_index: 1..N
input_state_or_head:
evidence_delta: []
full_scope_findings: []
validated_findings: []
changes_applied: []
verification: []
better_alternative_result:
long_term_fit:
unresolved: []
output_state_or_head:
clean_exit_candidate: true | false
```

종료 규칙:

1. **1~5회는 의무 전체 루프다.** 최소 5회의 완전한 전체 개선 루프를 실제 수행하기 전에는 중간 회차 finding이 0이어도 `CLEAN_REVIEW_EXIT`를 선언하지 않는다.
2. 새 유효 `MUST_FIX`, P0/P1, acceptance blocker가 하나라도 나오면 수정·검증 뒤 다음 전체 회차를 수행한다.
3. 정본·consumer·reference·Schema drift, 정상 경로 회귀, evidence ceiling 위반이 발견되면 종료하지 않는다.
4. `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_RECHECK`에서 현재 승인 범위 안의 더 강한 개선이 확인되면 적용 후 다시 전체 검토한다.
5. `NOT_RUN`, `BLOCKED_UNVERIFIED`, `CANCELLED`는 PASS가 아니며, 완료 조건에 필요한 증거가 없으면 clean exit가 아니다.
6. **5회 이후에도** 새로운 유효 오류·충돌·누락·blocking finding, 정본 충돌, acceptance failure 또는 회귀가 하나라도 나오면 수정·검증 후 6..N번째 전체 루프를 계속한다. 최대 회차 수는 고정하지 않는다.
7. 동일 finding을 표현만 바꿔 반복 계수하거나, 최소 횟수를 채우기 위해 가짜 finding/불필요한 변경을 만들지 않는다. full-scope attack·검증·대안·장기 적합성 재검사를 실제 수행했다면 finding과 changes가 0인 clean loop도 유효한 의무 회차다.
8. **최소 5회를 완료한 뒤 전체 재공격 결과 새로운 유효 오류·충돌·누락·blocking finding이 0이고, 기존 수정 회귀 0, acceptance criteria 충족, 정본/참조 신선도와 evidence ceiling이 모두 닫힐 때만 `CLEAN_REVIEW_EXIT`다.**

구현 전 PLAN에서는 수정 대상이 아직 없을 수 있으므로 공격·검증 결과를 계약 입력으로 사용한다. 실제 BUILD/수정 뒤에는 검증된 출력 상태를 다시 전체 공격한다. PR 병합 후에도 새 `main`을 입력으로 같은 clean-exit 규칙을 적용한다.

### `POST_CHANGE_MONITOR_LOOP`

모든 유지된 repository/project 변경은 **변경을 완료로 보고하기 전** 이 루프를 닫는다. 병합이 있는 경우 같은 Goal의 PR·정본·파생 상태가 바뀔 수 있으므로 **병합 뒤** 새 `main`에서도 다시 확인한다.

```text
retained-change-or-merge
→ attack
→ validate-critique
→ same-goal-open-and-recent-pr-recheck
→ untouched-consumer-and-derivative-recheck
→ omission-conflict-complement-gap-classification
→ approved-minimal-fix-if-needed
→ regression-recheck
→ exact-head-validation
→ merge-or-post-merge-main-readback
→ post-merge-pr-and-canon-recheck
→ completion-report
```

후속 finding은 다음처럼 분류한다.

- `OMISSION`: 바뀌어야 할 책임 원본·활성 consumer·Template·Test·reference·파생본이 누락됐다.
- `CONFLICT`: 현행 정본·사용자 승인 Decision·실제 diff·열린/최근 병합 PR·병합 결과가 서로 충돌한다.
- `COMPLEMENT_GAP`: 주 변경은 맞지만 내구성을 위해 작은 Test·reference·checklist·freshness·consumer 보완이 실질적으로 필요하다.
- `DUPLICATE_WORK`: 동일 Goal을 다른 열린·최근 PR 또는 후속 작업이 이미 소유한다.
- `NO_MATERIAL_FOLLOWUP`: 누락·충돌·중복·실질 보완 필요가 없어 추가 repository 변경이 정당화되지 않는다.

`OMISSION`, `CONFLICT`, `COMPLEMENT_GAP`, `DUPLICATE_WORK`는 기존 `MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED` 심각도·처리 판정과 별개인 **후속 원인 분류**다. 해결은 Existing Solution First로 기존 owner에 흡수하고, 보호된 의미 변경은 기존 사용자/BCP Gate를 그대로 따른다.

`NO_MATERIAL_FOLLOWUP`이면 루프를 채우기 위해 **새 변경을 만들지 않는다**. 이 계약은 현재 작업·검토의 완료 조건이며 scheduler·webhook·**백그라운드 실행을 의미하지 않는다**. 실제 반복 감시가 별도 자동화로 실행되더라도 그 결과는 같은 evidence ceiling·authority·PR·exact-head Gate를 다시 따른다.

### Completion-candidate remaining-work invariant

`REMAINING_WORK_COMPLETION_GATE`는 Base와 모든 프로젝트 작업에서 계획된 남은 작업 목록이 소진된 순간을 **완료가 아니라 완료 후보**로 취급한다. 먼저 actual repository/project state를 기준으로 `REMAINING_WORK_RECALCULATION_REQUIRED`를 수행하고, actionable work가 0일 때만 `IMPLEMENTATION_CORRECTION_RESCAN`으로 진입한다.

```text
planned work exhausted
→ REMAINING_WORK_RECALCULATION_REQUIRED
   ├─ remaining > 0 → BUILD / verification 계속
   └─ remaining = 0 → COMPLETION_CANDIDATE
→ IMPLEMENTATION_CORRECTION_RESCAN
   implementation / canon / test / consumer / PR / sync / readback / evidence
   ├─ valid finding → NEW_FINDING_REOPENS_REMAINING_WORK
   │  → refine through existing owner
   │  → regression/readback
   │  → remaining-work recalculation again
   └─ no required finding → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
→ POST_CHANGE_MONITOR_LOOP on the final candidate
→ minimum 5 full-scope loops on that same final state lineage
→ CLEAN_REVIEW_EXIT
→ FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
→ completion-report
```

`IMPLEMENTATION_CORRECTION_RESCAN`은 단순히 기존 체크리스트의 미체크 항목만 세지 않는다. 실제 diff/runtime, 승인 Intent, 정본과 applicable Notion/Repository sync, untouched consumer·Test·Template·reference, 동일 Goal의 열린/최근 PR, 실패·복구·rollback, evidence ceiling을 다시 공격해 “계획에는 없었지만 현재 완료를 막는 구현/교정 누락”을 찾는다. 유효한 `OMISSION`, `CONFLICT`, `COMPLEMENT_GAP` 또는 승인 범위의 blocking finding은 `NEW_FINDING_REOPENS_REMAINING_WORK`로 남은 작업에 편입한다.

`POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`는 새 review framework나 **두 번째 5회 루프가 아니다.** 최종 completion candidate를 입력으로 수행하는 기존 `POST_CHANGE_MONITOR_LOOP` 자체를 뜻하며, 그 동일 loop lineage가 `ADVERSARIAL_REVIEW_UNTIL_CLEAN`의 최소 5회와 `CLEAN_REVIEW_EXIT`를 충족한다. 마지막 구현·교정으로 후보 상태가 바뀌면 그 새 상태를 다시 공격해야 하지만, 같은 최종 후보를 대상으로 이미 수행한 full loop를 중복 실행하지 않는다. `NO_MATERIAL_FOLLOWUP`인 clean loop는 유효하지만 가짜 finding이나 불필요한 수정은 만들지 않는다.

`FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK`는 **현재 승인 범위에서** 필요한 구현·교정·검증이 0이고 완료 acceptance에 필요한 `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, 미해결 `DEFER`가 없을 때만 `전체 완료`를 허용한다. 범위 밖 future improvement는 `DEFER` 또는 후보로 남길 수 있지만 현재 범위의 미완료를 숨겨서는 안 된다. blocker/defer가 승인 범위 안에 남아 있으면 전체 완료가 아니라 partial/blocked/deferred 상태와 재개 조건을 보고한다.

## Required inputs

```yaml
work_product:
approved_requirements_and_scope:
project_core:
canonical_sources_and_actual_diff:
current_confirmed_decisions:
recent_approved_decision_ids:
merged_pr_or_direct_commit:
main_head_before:
main_head_after:
open_and_recent_prs:
notion_and_repository_sync_state:
acceptance_criteria:
protected_strengths_and_assets:
constraints_and_validation_environment:
change_authority:
branch_cleanup_state:
repository_audit:
  repository_search_roots:
  active_entrypoints_and_templates:
  registries_maps_and_aliases:
  actual_tracked_files_or_inventory_evidence:
  known_renames_replacements_and_legacy_terms:
  generated_derivatives_and_manifests:
  prompt_contracts:
  protected_paths_and_archive_roots:
```

코어가 확정되지 않았다면 핵심 충돌은 `UNVERIFIED`로 둔다. Notion 또는 Repository 설정을 읽지 못했으면 일치나 branch 삭제를 추정하지 않는다. 저장소 전체 tracked 목록을 얻지 못했으면 검색 결과를 전수 감사로 표현하지 않고 미검증 범위를 기록한다.

## Finding decisions

- `MUST_FIX`: 완료·안전·정합성을 막는 검증된 결함.
- `SHOULD_FIX`: 범위 안에서 가치가 크고 회귀 위험이 통제된다.
- `USER_DECISION_REQUIRED`: 둘 이상의 유효한 선택지가 프로젝트 코어·중요 기획·방향성을 다르게 만든다.
- `DEFER`: 유효하지만 현재 범위·근거·비용상 보류한다.
- `REJECTED_CRITIQUE`: 취향, 중복, 잘못된 전제, 범위 밖 요구다.
- `BLOCKED_UNVERIFIED`: 필요한 정본·도구·권한·실행 증거가 없어 판정할 수 없다.
- `ALLOWED_LEGACY`: 역사·Migration·Compatibility·Test fixture에서 현행 권한 없이 의도적으로 유지한다.

기존 `REJECT`와 `UNVERIFIED` 기록은 각각 `REJECTED_CRITIQUE`, `BLOCKED_UNVERIFIED`로 해석한다.

## Rules

1. `attack`은 실패·모순·악용·누락·경계 조건을 최대한 찾는다.
2. `validate-critique`는 사실성, 발생 가능성, 영향, 범위, 수정 비용을 재판정한다.
- 사용자안과 AI 최초안을 동일한 사실성·영향·비용·코어·호환성 기준으로 비교한다.
- 사용자가 동의를 요구했다는 이유로 비판을 생략하지 않고, 적대 검토를 반대를 위한 반대로 오용하지 않는다.
- 장점과 정상 경로도 보존하며 유효한 비판이 없으면 `REJECTED_CRITIQUE` 또는 근거 있는 동의로 판정한다.
3. `refine-approved-findings`는 `MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정한다.
4. 기획 방향을 바꾸는 finding은 몰래 수정하지 않고 `USER_DECISION_REQUIRED`로 분리한다.
5. `regression-recheck`는 기존 장점·정상 경로·코어·범위와 새 결함을 다시 공격한다.
- 이미 구현된 finding을 다시 수정하지 않는다. 입력 상태가 바뀌지 않은 이미 구현·검증 finding은 재수정하지 않으며, 새 증거·회귀·정본 변화가 있을 때만 재개방한다.
6. `decision-report`는 반영·보류·기각·미검증과 남은 위험을 모두 기록한다.
7. 병합 뒤에는 설명이나 기존 PR 승인만 신뢰하지 않고 새 `main` HEAD와 실제 diff를 다시 읽는다.
8. 질문 전·병합 후 동일 Goal의 열린 PR, 최근 병합 PR, 대체·후속 링크를 확인한다.
9. 실행하지 않은 CI·런타임·렌더·Notion readback·branch 삭제를 통과로 표시하지 않는다.
10. 저장소 전체 감사에서 검색 API 결과만으로 전체 파일을 검수했다고 주장하지 않는다.
11. 파일명·버전·날짜만으로 구형 파일을 삭제하지 않고 권한·고유 정보·활성 소비자·복구 가능성을 판정한다.
12. 변경된 파일뿐 아니라 변경됐어야 할 untouched 소비자·Template·Test·파생본을 공격한다.
13. 새 광역 Skill을 만들기 전에 이 mode와 reference-freshness·legacy-governance 조합으로 해결 가능한지 확인한다.
14. 유지된 변경은 `POST_CHANGE_MONITOR_LOOP`의 PR·consumer·회귀·exact-head 검사를 닫기 전 완료로 보고하지 않는다.
15. L1 이상 material decision은 `AGENTS.md`와 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`의 `MINIMUM_VIABLE_ALTERNATIVES: 3`, `BETTER_ALTERNATIVE_SEARCH`, `LONG_TERM_PLAN_FIT_REQUIRED`를 함께 적용한다.
16. Base/project 완료 후보는 `REMAINING_WORK_RECALCULATION_REQUIRED → IMPLEMENTATION_CORRECTION_RESCAN → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`를 닫기 전 `전체 완료`로 보고하지 않는다. 새 유효 finding은 `NEW_FINDING_REOPENS_REMAINING_WORK`로 BUILD/refinement를 재개한다. `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`는 최종 후보의 기존 `POST_CHANGE_MONITOR_LOOP`와 동일한 loop lineage이며 별도 중복 루프를 만들지 않는다.

## Repository-wide attack lenses

`repository-wide-audit`에서는 다음을 필수 공격한다. 이 목록은 각 전체 개선 루프에서 다시 사용하는 검토 표면이며 loop 번호가 아니다.

- 한 질문에 둘 이상의 현행 정본이 있는가.
- 최신 승인 Decision이 누락되거나 `SUPERSEDED / REJECTED / DEFERRED` 결정이 부활했는가.
- 구형 경로·ID·Schema·Skill·제품 단계·Prompt 계약이 활성 권한으로 남았는가.
- 새 정책·Template·Skill을 소비해야 할 README·START_HERE·기획서·Registry·Test가 untouched인가.
- 파일은 존재하지만 실제 routing·실행·검증 경로가 없는가.
- PDF·DOCX·Dashboard·Manifest·생성본이 원본보다 오래됐는가.
- 동일 Goal·기능·문서·질문·PR·branch가 중복됐는가.
- Base Template·프로젝트 Notion·프로젝트 상태의 권한이 혼동됐는가.
- 별도 `CORE_POC`처럼 대체된 Gate가 현행 흐름으로 부활했는가.

상세 권한 분류·`UNTOUCHED_CONSUMER` 표·처리 라우팅은 `references/repository-wide-audit-protocol.md`를 따른다.

## Post-merge attack lenses

모든 병합과 직접 `main` 결정 Commit 뒤 다음을 공격한다. 이 목록도 각 전체 개선 루프에서 재사용하는 surface다.

- 최근 사용자 승인 Decision이 누락됐는가
- `SUPERSEDED`, `REJECTED`, `DEFERRED`된 결정이 다시 활성화됐는가
- `CURRENT_CONFIRMED_DECISIONS.md`와 분야 책임 원본이 충돌하는가
- 실제 diff가 승인 범위나 프로젝트 코어를 벗어났는가
- 관련 정본·Registry·Template·Test·파생본 일부가 untouched인가
- 동일 Goal·기능·문서·질문·PR이 중복됐는가
- GitHub `main`과 프로젝트 Notion의 Decision·Commit·대체 관계가 다른가
- 기존 정상 경로·저장 호환성·롤백 경로가 회귀했는가
- 임시값·플레이스홀더·미검증 주장이 확정 상태로 남았는가
- 병합된 head branch가 안전 조건을 만족했는데 불필요하게 남았는가

## Post-merge comparison order

```text
merged PR or direct commit
→ new main HEAD
→ CURRENT_CONFIRMED_DECISIONS.md
→ affected domain canon
→ recent approved Decision IDs
→ actual code·data·assets·tests
→ Project Notion
→ open and recent PRs
→ reference freshness·static·runtime·regression evidence
```

GitHub와 Notion이 다르면 최신 사용자 승인, Decision ID, Commit SHA와 분야 책임 원본을 비교해 어느 쪽이 누락됐는지 판정한다. 자동으로 양쪽 중 하나를 진실로 가정하지 않는다.

## Output contract

```md
## 검토 mode·전체 개선 loop와 실패 가정
## 기준 Branch·Commit·Decision·정본·실제 diff
## 최소 3개 실질 대안·벤치마크·trade study
## 열린·최근 병합 PR·중복 작업 비교
## Notion/GitHub 동기화 비교
## 저장소 감사 범위·권한 지도·미검증 범위
## stale·중복·고아·untouched 소비자·파생본 Finding
## MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER
## REJECTED_CRITIQUE / BLOCKED_UNVERIFIED / ALLOWED_LEGACY
## REMAINING_WORK_RECALCULATION_REQUIRED 결과
## IMPLEMENTATION_CORRECTION_RESCAN 결과와 NEW_FINDING_REOPENS_REMAINING_WORK 내역
## POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED / CLEAN_REVIEW_EXIT 상태
## 실제 반영한 최소 변경과 회차별 verification
## BETTER_ALTERNATIVE_SEARCH 결과
## LONG_TERM_PLAN_FIT_RECHECK 결과
## 보호한 코어·고유 정보·장점·범위
## reference freshness·정적·런타임·회귀 재검사
## branch cleanup 상태
## 최종 판정·남은 위험·다음 조건
```

병합 후 표준 양식은 `templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md`를 사용한다.

## Post-merge final decisions

- `NO_CONFLICT`: 정본·최근 승인·diff·Notion readback·적용 검증에서 확인된 충돌이 없다.
- `CONFLICT_FIXED`: 검증된 충돌을 승인 범위 안에서 최소 수정하고 재검사했다.
- `USER_DECISION_REQUIRED`: 기술적으로 단일 답을 정할 수 없는 중요 기획 충돌이 남았다.
- `BLOCKED_UNVERIFIED`: 필요한 도구·권한·정본·CI·런타임·Notion readback/sync 증거가 없어 완료 판정할 수 없다.

## Quality gate

`MUST_FIX`·승인된 `SHOULD_FIX` 외 항목을 몰래 반영하지 않고, 프로젝트 코어를 바꾸거나 기능을 팽창시키지 않으며, 수정 뒤 `regression-recheck`를 수행한다.

병합 후에는 다음을 모두 만족해야 `NO_CONFLICT` 또는 `CONFLICT_FIXED`를 사용할 수 있다.

- 새 `main` HEAD와 실제 diff를 확인했다.
- 현재 확정 Decision과 관련 분야 정본을 비교했다.
- 최근 승인 누락과 이전 Decision 부활을 검사했다.
- 동일 Goal의 열린·중복 PR을 확인했다.
- 사람용 변경이 있으면 정확한 Project의 Notion destination을 readback했다.
- 가능한 reference freshness·정적·런타임·회귀 검사를 실제 실행했다.
- 실행하지 못한 검사를 성공으로 표시하지 않았다.

`repository-wide-audit` 완료에는 추가로 다음이 필요하다.

- tracked inventory 또는 정확한 미검증 범위를 기록했다.
- `CURRENT_AUTHORITY`와 활성 소비자를 연결했다.
- `UNTOUCHED_CONSUMER`와 변경 전파 누락을 판정했다.
- 활성 stale와 `ALLOWED_LEGACY`를 구분했다.
- Prompt·파생본·Manifest drift를 검사했다.
- archive·compatibility·삭제 처리를 전문 Skill로 라우팅했다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`

## BCP-008 교차 분야 검토 Lens

L2 이상 다분야 결정, 저장소 전체 감사, 외부 코드·디자인 조달에서는 `references/cross-discipline-review-lenses.md`에서 현재 위험과 직접 관련된 Lens만 선택한다. Lens는 BMAD식 관점 확장을 제공하지만 **주 책임 Skill의 결정을 소유하지 않는다**.

- 관련 없는 Lens는 억지 Finding을 만들지 않고 `NOT_APPLICABLE`과 이유를 기록한다.
- 각 Finding은 `lens`, `evidence`, `affected_requirement`, `severity`, `owner_skill`, `status`를 포함한다.
- Lens 간 결론이 충돌하면 사실·영향·비용·코어·되돌리기 난이도로 `validate-critique`하고, 중요 방향 차이는 `USER_DECISION_REQUIRED`로 보낸다.
- Named Agent별 별도 정본·PRD·Architecture 복제본을 만들지 않는다.

## Socratic Review Lens

주장·비판의 의미, 숨은 가정, 근거, 대안 관점, 파급, 질문 자체의 중요성이 현재 결론을 바꿀 수 있을 때만 `references/socratic-questioning-lenses.md`에서 **관련된 Lens만** 선택한다. 모든 질문군을 채우기 위한 **가짜 Finding**을 만들지 않는다.

- `attack`에서는 주로 Clarification, Assumptions, Reasons / Evidence, Viewpoints, Implications / Consequences를 사용해 애매한 주장·숨은 전제·증거 공백·관점 맹점·파급을 찾는다.
- `validate-critique`에서는 Reasons / Evidence와 Assumptions를 다시 검증하고 Meta-question으로 해당 비판이 실제 Requirement·범위·결론에 중요한지 재판정한다.
- `regression-recheck`에서는 Implications / Consequences를 다시 적용해 정상 경로·복구·호환성·롤백에 새 회귀가 생기지 않았는지 확인한다.
- Socratic 질문 후보가 생기면 먼저 **저장소·정본·실제 구현·도구**로 답할 수 있는지 조사한다. 그 근거로 판정할 수 있으면 사용자에게 묻지 않는다.
- 필요한 증거가 없으면 기존 `BLOCKED_UNVERIFIED`와 확인 조건을 사용한다. 둘 이상의 유효한 선택이 프로젝트 코어·중요 방향을 다르게 만들 때만 기존 `USER_DECISION_REQUIRED`로 올린다.
- Socratic Lens는 새 사용자 인터뷰 Gate나 별도 승인 권한을 만들지 않으며, 기존 intake/Grill Me의 질문 하나 원칙과 Finding decision 의미를 재정의하지 않는다.
