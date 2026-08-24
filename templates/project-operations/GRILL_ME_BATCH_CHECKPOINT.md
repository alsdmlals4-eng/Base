# Grill Me 결정 배치 체크포인트

## 배치 상태

```yaml
grill_me_batch_id: GM-BATCH-YYYY-MM-DD-NN
related_goal_or_issue:
baseline_main_commit:
active_batch_branch:
max_approved_decisions_per_batch: 10
approved_decision_count: 0
checkpoint_reason: TEN_APPROVALS | HIGH_IMPACT | CANON_CONFLICT | IMPLEMENTATION_BLOCKED | SESSION_END | USER_REQUEST | DIFF_SIZE
batch_status: COLLECTING | CHECKPOINT_REQUIRED | BATCH_PR_OPEN | CHECKS_RUNNING | REVIEW_REQUIRED | MERGED | SYNCED_TO_MAIN | BLOCKED
batch_pr:
batch_exact_head:
required_checks: NOT_RUN | PASS | FAIL
adversarial_review: NOT_RUN | PASS | FAIL
unresolved_thread_count:
p0_p1_finding_count:
merge_commit:
merged_main_readback: NOT_RUN | PASS | FAIL
notion_sync_status: NOT_CONFIGURED | APPROVED_PENDING_MERGE | NOTION_UPDATED | SYNCED_TO_MAIN | BLOCKED_UNVERIFIED
notion_readback: NOT_CONFIGURED | NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
legacy_sheet_migration_status: NOT_PRESENT | UNMIGRATED_UNIQUE_MATERIAL | MIGRATED_READBACK_VERIFIED | ARCHIVED_APPROVED | BLOCKED_UNVERIFIED
updated_at:
```

## 기획 우선 Gate

- [ ] `L1` 이상 작업이다.
- [ ] 최신 정본·실제 구현·열린/최근 PR을 확인했다.
- [ ] 대안·기획 충돌·완료 기준·검증·롤백을 기록했다.
- [ ] 사용자 승인 또는 기존 승인된 실행 계약이 있다.
- [ ] 승인 전 `BUILD`로 진입하지 않았다.
- [ ] `L0` 예외라면 오탈자·명백한 단일 파일 기계 수정·동일 입력 검사 재실행임을 기록했다.

## 결정 분류

| Decision ID | 질문·항목 | 분류 | GPT 권장안 | 사용자 승인 | Branch Commit | 정본 위치 | Notion 상태 |
|---|---|---|---|---|---|---|---|

분류:

```text
DETAILED_NUMERIC_DEFAULT / RECOMMENDED_DEFAULT
PLANNING_CONFLICT / USER_DECISION_REQUIRED / GRILL_ME_REQUIRED
```

## 수치 기본값 검증

| 항목 | 초기값 | 근거 | 가역성 | 프로젝트 방향 불변 | 조정 조건 | 검증 | 증거 한계 |
|---|---:|---|---|---|---|---|---|

- [ ] 난이도 곡선·경제·성장 속도·세션 길이·빌드 우열·보상 의미·핵심 플레이 경험을 바꾸는 수치는 `PLANNING_CONFLICT`로 승격했다.
- [ ] 실제 플레이테스트 전 값을 확정 밸런스로 보고하지 않았다.

## 승인별 즉시 기록

- [ ] 사용자 답변 원문과 동일 Decision ID를 GitHub 추적 surface에 기록했다.
- [ ] 활성 배치 Branch의 `CURRENT_CONFIRMED_DECISIONS`와 분야 책임 원본을 갱신했다.
- [ ] Decision별 논리 Commit을 만들었다.
- [ ] 적용 가능한 Notion destination을 `APPROVED_PENDING_MERGE`로 갱신하고 readback했다.
- [ ] legacy Sheet가 unique material을 가질 때만 `COMPATIBILITY_ONLY` migration 상태를 기록했다.
- [ ] 병합 전 main 동기화 완료를 주장하지 않았다.

## 체크포인트 판정

- 승인 수:
- 조기 체크포인트 사유:
- 10번째 승인 뒤 11번째 질문 차단:
- 10건 미만 세션 종료 시 잔여 배치 종료:
- 같은 Goal의 다른 활성 Grill Me 배치 PR 존재 여부:

## PR exact-head 검사

```yaml
batch_pr:
batch_exact_head:
required_checks:
changed_files:
protected_scope_preserved:
unresolved_thread_count:
```

- [ ] required checks가 latest exact-head에서 실행됐다.
- [ ] 이전 Commit의 성공 결과를 재사용하지 않았다.
- [ ] 임시 Workflow·생성 실패 산출물·범위 밖 파일이 최종 diff에 없다.

## 적대적 검토

```text
attack → validate-critique → regression-recheck → decision-report
```

| Finding | 심각도 | 증거 | 판정 | 수정·기각 이유 | 재검증 |
|---|---|---|---|---|---|

심각도:

```text
MUST_FIX / SHOULD_FIX / OPTIONAL / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED
```

필수 공격:

- [ ] 기획 우선이 불필요한 폭포수 절차가 되지 않았는가?
- [ ] GPT 권장 수치가 기획 충돌을 숨기지 않았는가?
- [ ] 저장소로 답할 사실을 사용자에게 묻지 않았는가?
- [ ] 배치가 자기완결 검토 단위를 넘지 않았는가?
- [ ] 승인 내용이 대화 메모리에만 남지 않았는가?
- [ ] Notion destination이 병합 전 main 동기화를 주장하지 않았는가?
- [ ] legacy Sheet가 `COMPATIBILITY_ONLY`를 벗어나 active authority로 복원되지 않았는가?
- [ ] 같은 Goal에 여러 활성 PR이 생기지 않았는가?
- [ ] 적대적 검토가 반대를 위한 반대가 되지 않았는가?

병합 Gate:

- [ ] required checks PASS
- [ ] adversarial review PASS
- [ ] unresolved thread 0
- [ ] P0/P1 0
- [ ] 미해결 `PLANNING_CONFLICT` 0
- [ ] `BLOCKED_UNVERIFIED` 0

## 병합 후 재동기화

```yaml
merge_commit:
merged_main_readback:
canonical_readback:
notion_readback:
legacy_sheet_migration_status:
final_state: SYNCED_TO_MAIN | BLOCKED_UNVERIFIED
```

- [ ] squash merge 결과와 merged main SHA를 재조회했다.
- [ ] GitHub 정본의 Decision ID·결정·대체 관계를 재조회했다.
- [ ] 적용 가능한 Notion destination의 `APPROVED_PENDING_MERGE` projection을 merge Commit으로 갱신했다.
- [ ] Notion destination을 재조회했다.
- [ ] GitHub main과 Notion destination이 일치할 때만 `SYNCED_TO_MAIN`으로 판정했다.
- [ ] legacy Sheet가 unique material을 가진 경우에만 `COMPATIBILITY_ONLY` 이관·readback 상태를 남겼다.

## 증거 한계

```yaml
real_project_batch_execution: NOT_RUN | PASS | FAIL
external_model_behavior: NOT_RUN | PASS | FAIL
human_process_usability: NOT_RUN | PASS | FAIL
runtime_device_accessibility: NOT_RUN | PASS | FAIL | NOT_APPLICABLE
```
