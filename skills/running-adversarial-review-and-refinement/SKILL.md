---
name: running-adversarial-review-and-refinement
description: Use when a work product, repository, PR, or merged decision must be attacked for failure, its criticisms validated, and approved findings regression-checked.
---

# Running Adversarial Review and Refinement

## Purpose and separation

적대적 검토는 승인 거부 증거를 찾는 공격 단계다. 그러나 **비판도 오류·취향·과잉 요구**일 수 있으므로 공격과 검증을 분리하고, 검증된 문제만 최소 수정한다.

사용자안과 AI 최초안은 같은 평가 기준으로 공격·검증한다. 검토 목적은 이견 생산이 아니라 실패 가능성 감소다. 사용자안이 반례·위험 검토를 통과해 가장 강한 결론이면 근거와 함께 동의할 수 있다.

Registry의 `칭찬·균형 평가만 요청` 비사용 조건은 결정·권장안이 없는 설명형 칭찬·균형 요약에만 적용한다. L1 이상 기능·설계·아키텍처·정책·방향 결정이나 중요 권장안이 포함된 균형 비교는 적대 검토 대상이다.

실제 diff·정적·런타임·접근성·성능 증거는 `reviewing-and-validating-project-changes`, 프로젝트 코어 판정·확정은 관련 코어 Skill이 책임진다. 승인 결정·GitHub·Google Sheets 동기화는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다. 구형본의 archive·compatibility·삭제는 `governing-legacy-retention-and-archives`, 정본·경로·ID·Template·Test 전파는 `auditing-canonical-reference-freshness`가 책임진다.

## Skill Modes

- `attack`: 작업물이 실패했다고 가정하고 결함·모순·누락·악용·경계 실패를 찾는다.
- `validate-critique`: 공격 결과의 사실성·발생 가능성·영향·범위·비용·코어 위험을 재검증한다.
- `refine-approved-findings`: `MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정한다.
- `regression-recheck`: 수정 전후의 정상 경로·코어·데이터·호환성·새 결함을 다시 공격한다.
- `decision-report`: 반영·보류·기각·미검증과 남은 위험을 기록한다.
- `post-merge-review`: 병합 또는 직접 `main` 결정 Commit 뒤 새 `main`·Decision·정본·실제 diff·Sheets·PR·branch를 다시 검토한다.
- `repository-wide-audit`: 저장소 전체의 권한 지도, 중복·stale·고아 파일, 구형 계약, untouched 소비자, Prompt·파생본 drift를 공격하고 전문 Skill로 처리를 라우팅한다.

일반 작업은 `attack → validate-critique → refine-approved-findings → regression-recheck → decision-report`를 사용한다. 저장소 전체 감사는 `references/repository-wide-audit-protocol.md`, 세부 Finding·회귀 판정은 `references/finding-and-regression-protocol.md`를 필요할 때만 읽는다.

구현 전 PLAN 사전판정은 아직 수정할 작업물이 없으므로 `attack → validate-critique → decision-report`까지만 실행한다. 승인 finding은 `refine-approved-findings`에서 주 책임 분야 Skill이 한 번만 구현·수정하며, 이 Skill은 분야 작성 책임을 빼앗거나 이미 구현된 finding을 다시 수정하지 않는다. 그 뒤 `regression-recheck → decision-report`로 복귀해야 전체 루프가 완료된다.

기본 Work Mode는 `REVIEW → 필요한 경우 BUILD → REVIEW`다. 같은 수행자가 맡아도 단계별 입력과 출력을 섞지 않는다.

PR 병합 또는 직접 `main` 결정 Commit 뒤에는 다음 확장 루트를 사용한다.

```text
new-main-baseline
→ canonical-and-sync-compare
→ attack
→ validate-critique
→ refine-approved-findings
→ regression-recheck
→ post-merge-decision-report
```

저장소 전체 감사에서는 다음 루트를 사용한다.

```text
repository-scope-map
→ canonical-authority-map
→ full-file-inventory
→ stale-and-duplicate-attack
→ untouched-consumer-attack
→ derivative-and-prompt-drift-attack
→ validate-critique
→ legacy-classification
→ approved-minimal-fix
→ regression-and-freshness-recheck
→ repository-audit-report
```

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
google_sheet_state:
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

코어가 확정되지 않았다면 핵심 충돌은 `UNVERIFIED`로 둔다. Google Sheets 또는 Repository 설정을 읽지 못했으면 일치나 branch 삭제를 추정하지 않는다. 저장소 전체 tracked 목록을 얻지 못했으면 검색 결과를 전수 감사로 표현하지 않고 미검증 범위를 기록한다.

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
6. `decision-report`는 반영·보류·기각·미검증과 남은 위험을 모두 기록한다.
7. 병합 뒤에는 설명이나 기존 PR 승인만 신뢰하지 않고 새 `main` HEAD와 실제 diff를 다시 읽는다.
8. 질문 전·병합 후 동일 Goal의 열린 PR, 최근 병합 PR, 대체·후속 링크를 확인한다.
9. 실행하지 않은 CI·런타임·렌더·Sheets 조회·branch 삭제를 통과로 표시하지 않는다.
10. 저장소 전체 감사에서 검색 API 결과만으로 전체 파일을 검수했다고 주장하지 않는다.
11. 파일명·버전·날짜만으로 구형 파일을 삭제하지 않고 권한·고유 정보·활성 소비자·복구 가능성을 판정한다.
12. 변경된 파일뿐 아니라 변경됐어야 할 untouched 소비자·Template·Test·파생본을 공격한다.
13. 새 광역 Skill을 만들기 전에 이 mode와 reference-freshness·legacy-governance 조합으로 해결 가능한지 확인한다.
14. 유지된 변경은 `POST_CHANGE_MONITOR_LOOP`의 PR·consumer·회귀·exact-head 검사를 닫기 전 완료로 보고하지 않는다.

## Repository-wide attack lenses

`repository-wide-audit`에서는 다음을 필수 공격한다.

- 한 질문에 둘 이상의 현행 정본이 있는가.
- 최신 승인 Decision이 누락되거나 `SUPERSEDED / REJECTED / DEFERRED` 결정이 부활했는가.
- 구형 경로·ID·Schema·Skill·제품 단계·Prompt 계약이 활성 권한으로 남았는가.
- 새 정책·Template·Skill을 소비해야 할 README·START_HERE·기획서·Registry·Test가 untouched인가.
- 파일은 존재하지만 실제 routing·실행·검증 경로가 없는가.
- PDF·DOCX·Dashboard·Manifest·생성본이 원본보다 오래됐는가.
- 동일 Goal·기능·문서·질문·PR·branch가 중복됐는가.
- Base Template·프로젝트 Sheet·프로젝트 상태의 권한이 혼동됐는가.
- 별도 `CORE_POC`처럼 대체된 Gate가 현행 흐름으로 부활했는가.

상세 권한 분류·`UNTOUCHED_CONSUMER` 표·처리 라우팅은 `references/repository-wide-audit-protocol.md`를 따른다.

## Post-merge attack lenses

모든 병합과 직접 `main` 결정 Commit 뒤 다음을 공격한다.

- 최근 사용자 승인 Decision이 누락됐는가
- `SUPERSEDED`, `REJECTED`, `DEFERRED`된 결정이 다시 활성화됐는가
- `CURRENT_CONFIRMED_DECISIONS.md`와 분야 책임 원본이 충돌하는가
- 실제 diff가 승인 범위나 프로젝트 코어를 벗어났는가
- 관련 정본·Registry·Template·Test·파생본 일부가 untouched인가
- 동일 Goal·기능·문서·질문·PR이 중복됐는가
- GitHub `main`과 프로젝트 Google Sheets의 Decision·Commit·대체 관계가 다른가
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
→ Google Sheets
→ open and recent PRs
→ reference freshness·static·runtime·regression evidence
```

GitHub와 Sheets가 다르면 최신 사용자 승인, Decision ID, Commit SHA와 분야 책임 원본을 비교해 어느 쪽이 누락됐는지 판정한다. 자동으로 양쪽 중 하나를 진실로 가정하지 않는다.

## Output contract

```md
## 검토 mode·공격 관점과 실패 가정
## 기준 Branch·Commit·Decision·정본·실제 diff
## 열린·최근 병합 PR·중복 작업 비교
## Google Sheets 동기화 비교
## 저장소 감사 범위·권한 지도·미검증 범위
## stale·중복·고아·untouched 소비자·파생본 Finding
## MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER
## REJECTED_CRITIQUE / BLOCKED_UNVERIFIED / ALLOWED_LEGACY
## 실제 반영한 최소 변경
## 보호한 코어·고유 정보·장점·범위
## reference freshness·정적·런타임·회귀 재검사
## branch cleanup 상태
## 최종 판정·남은 위험·다음 조건
```

병합 후 표준 양식은 `templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md`를 사용한다.

## Post-merge final decisions

- `NO_CONFLICT`: 정본·최근 승인·diff·Sheets·적용 검증에서 확인된 충돌이 없다.
- `CONFLICT_FIXED`: 검증된 충돌을 승인 범위 안에서 최소 수정하고 재검사했다.
- `USER_DECISION_REQUIRED`: 기술적으로 단일 답을 정할 수 없는 중요 기획 충돌이 남았다.
- `BLOCKED_UNVERIFIED`: 필요한 도구·권한·정본·CI·런타임·Sheets 증거가 없어 완료 판정할 수 없다.

## Quality gate

`MUST_FIX`·승인된 `SHOULD_FIX` 외 항목을 몰래 반영하지 않고, 프로젝트 코어를 바꾸거나 기능을 팽창시키지 않으며, 수정 뒤 `regression-recheck`를 수행한다.

병합 후에는 다음을 모두 만족해야 `NO_CONFLICT` 또는 `CONFLICT_FIXED`를 사용할 수 있다.

- 새 `main` HEAD와 실제 diff를 확인했다.
- 현재 확정 Decision과 관련 분야 정본을 비교했다.
- 최근 승인 누락과 이전 Decision 부활을 검사했다.
- 동일 Goal의 열린·중복 PR을 확인했다.
- 프로젝트가 Sheets를 사용하면 해당 Decision 행을 재조회했다.
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
