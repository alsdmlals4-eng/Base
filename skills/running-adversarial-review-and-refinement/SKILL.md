---
name: running-adversarial-review-and-refinement
description: Use when a design, plan, document, code proposal, data change, UX flow, merged pull request, direct main decision commit, or other work product should be attacked as if it failed, its criticisms independently validated, only justified findings refined, and the revised result regression-checked without changing project core or adding unnecessary scope.
---

# Running Adversarial Review and Refinement

## Purpose and separation

적대적 검토는 승인 거부 증거를 찾는 공격 단계다. 그러나 **비판도 오류·취향·과잉 요구**일 수 있으므로 공격과 검증을 분리하고, 검증된 문제만 최소 수정한다.

실제 diff·정적·런타임·접근성·성능 증거는 `reviewing-and-validating-project-changes`, 프로젝트 코어 판정·확정은 관련 코어 Skill이 책임진다. 승인 결정·GitHub·Google Sheets 동기화는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다.

## Workflow

`attack → validate-critique → refine-approved-findings → regression-recheck → decision-report`

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
```

코어가 확정되지 않았다면 핵심 충돌은 `UNVERIFIED`로 둔다. Google Sheets 또는 Repository 설정을 읽지 못했으면 일치나 branch 삭제를 추정하지 않는다.

## Finding decisions

- `MUST_FIX`: 완료·안전·정합성을 막는 검증된 결함.
- `SHOULD_FIX`: 범위 안에서 가치가 크고 회귀 위험이 통제된다.
- `USER_DECISION_REQUIRED`: 둘 이상의 유효한 선택지가 프로젝트 코어·중요 기획·방향성을 다르게 만든다.
- `DEFER`: 유효하지만 현재 범위·근거·비용상 보류한다.
- `REJECTED_CRITIQUE`: 취향, 중복, 잘못된 전제, 범위 밖 요구다.
- `BLOCKED_UNVERIFIED`: 필요한 정본·도구·권한·실행 증거가 없어 판정할 수 없다.

기존 `REJECT`와 `UNVERIFIED` 기록은 각각 `REJECTED_CRITIQUE`, `BLOCKED_UNVERIFIED`로 해석한다.

상세 공격 렌즈·판정표·회귀 프로토콜은 `references/finding-and-regression-protocol.md`를 필요할 때만 읽는다.

## Rules

1. `attack`은 실패·모순·악용·누락·경계 조건을 최대한 찾는다.
2. `validate-critique`는 사실성, 발생 가능성, 영향, 범위, 수정 비용을 재판정한다.
3. `refine-approved-findings`는 `MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정한다.
4. 기획 방향을 바꾸는 finding은 몰래 수정하지 않고 `USER_DECISION_REQUIRED`로 분리한다.
5. `regression-recheck`는 기존 장점·정상 경로·코어·범위와 새 결함을 다시 공격한다.
6. `decision-report`는 반영·보류·기각·미검증과 남은 위험을 모두 기록한다.
7. 병합 뒤에는 설명이나 기존 PR 승인만 신뢰하지 않고 새 `main` HEAD와 실제 diff를 다시 읽는다.
8. 질문 전·병합 후 동일 Goal의 열린 PR, 최근 병합 PR, 대체·후속 링크를 확인한다.
9. 실행하지 않은 CI·런타임·렌더·Sheets 조회·branch 삭제를 통과로 표시하지 않는다.

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
## 공격 관점과 실패 가정
## 병합 정보·새 main HEAD·관련 Decision
## CURRENT_CONFIRMED_DECISIONS·분야 정본·실제 diff 비교
## 열린·최근 병합 PR·중복 작업 비교
## Google Sheets 동기화 비교
## finding·근거·심각도
## MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED
## 실제 반영한 최소 변경
## 보호한 코어·장점·범위
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

Learning Log: `skills/SKILL_LEARNING_LOG.md`
