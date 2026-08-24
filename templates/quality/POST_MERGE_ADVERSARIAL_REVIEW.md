# 병합 후 적대적 검토 결과

`CONFIGURED_PROJECT_WORKSPACE: CONDITIONAL`

별도 사람용 프로젝트 작업면은 현행 authority contract가 설정하고 현재 검토 책임을 배정한 경우에만 읽는다. 설정되지 않았으면 `NOT_CONFIGURED`로 기록하며, 폐기·migration-only surface를 일반 완료 Gate로 부활시키지 않는다.

## 1. 병합 정보

```yaml
repository:
work_item:
pr_number:
direct_commit:
merge_method: SQUASH | MERGE | REBASE | DIRECT_MAIN_DECISION_SYNC
base_before:
main_head_after:
merged_at:
head_branch:
branch_cleanup: DELETED | AUTO_DELETE_ENABLED | NOT_APPLICABLE | UNVERIFIED_REPOSITORY_SETTING
related_decision_ids:
reviewed_by:
```

## 2. 검토 범위

- 승인된 목표·범위:
- 보호할 프로젝트 코어·장점:
- `CURRENT_CONFIRMED_DECISIONS.md`:
- 관련 분야 책임 원본:
- 실제 diff·변경 파일:
- 최근 승인 Decision:
- 관련 열린·최근 병합 PR:
- configured project workspace: `NOT_CONFIGURED | <workspace + assigned responsibility>`
- 실제 코드·데이터·Scene·Resource·자산·테스트:
- 실행 가능한 검증 환경:

## 3. 공격 가정

변경이 성공했다는 설명을 신뢰하지 않고 다음 실패를 가정한다.

- 최근 승인 사항이 빠졌다.
- 이전에 대체된 결정이 다시 살아났다.
- 프로젝트 코어 또는 플레이어 약속과 충돌한다.
- 일부 정본·템플릿·테스트·참조만 갱신됐다.
- PR 범위를 벗어난 변경이 포함됐다.
- 동일 Goal·기능·문서·질문이 중복됐다.
- repository 정본과 configured workspace의 assigned responsibility가 다르다.
- 기존 정상 경로나 롤백 경로가 회귀했다.
- 임시값·플레이스홀더가 확정값으로 남았다.
- 필요한 CI·런타임·렌더 검증을 실행하지 않았다.

## 4. 정본·동기화 비교

| 검사 | 기준 | 관찰 결과 | 판정 | 증거 |
|---|---|---|---|---|
| main HEAD | 병합 결과 SHA |  | PASS / FAIL / UNVERIFIED |  |
| 현재 확정 Decision | 최신 CURRENT·LATEST_OVERRIDE |  | PASS / FAIL / UNVERIFIED |  |
| 분야 책임 원본 | 등록된 Markdown·JSON |  | PASS / FAIL / UNVERIFIED |  |
| 최근 승인 누락 | 병합 전후 Decision ID |  | PASS / FAIL / UNVERIFIED |  |
| 대체 관계 | SUPERSEDED·REJECTED·DEFERRED |  | PASS / FAIL / UNVERIFIED |  |
| configured workspace | assigned responsibility만 |  | PASS / FAIL / NOT_CONFIGURED / UNVERIFIED |  |
| 열린·중복 PR | 동일 Goal |  | PASS / FAIL / UNVERIFIED |  |
| branch cleanup | 병합 head branch |  | PASS / FAIL / UNVERIFIED |  |

## 5. Finding과 비판 검증

| ID | 공격 관점 | 주장 | 사실 근거 | 발생 가능성 | 영향 | 범위 | 비판 판정 | 최종 분류 |
|---|---|---|---|---|---|---|---|---|

최종 분류:

```text
MUST_FIX
SHOULD_FIX
USER_DECISION_REQUIRED
DEFER
REJECTED_CRITIQUE
BLOCKED_UNVERIFIED
```

실행 가능한 구체적 수정 Finding은 `finding-and-regression-protocol.md`의 `FIX_GUIDED_VERIFICATION_WHEN_EXECUTABLE`로 baseline/candidate를 같은 acceptance에서 비교한다.

## 6. 실제 반영한 최소 수정

| Finding | 수정 내용 | 영향 파일 | 보호한 범위 | 검증 | Commit·PR |
|---|---|---|---|---|---|

사용자 승인이나 변경 권한이 없는 finding은 몰래 반영하지 않는다.

## 7. 회귀 재검사

| 검사 | 실행 방법 | 결과 | 증거 | 미실행 사유·재개 조건 |
|---|---|---|---|---|
| 승인 계약·diff 대조 |  | PASS / FAIL / NOT_RUN |  |  |
| reference freshness |  | PASS / FAIL / NOT_RUN |  |  |
| 정적 검사 |  | PASS / FAIL / NOT_RUN |  |  |
| CI·Required Check |  | PASS / FAIL / NOT_RUN |  |  |
| 런타임·빌드·렌더 |  | PASS / FAIL / NOT_RUN |  |  |
| 대표 정상 경로 |  | PASS / FAIL / NOT_RUN |  |  |
| 경계·반례 |  | PASS / FAIL / NOT_RUN |  |  |
| 인접 기능 |  | PASS / FAIL / NOT_RUN |  |  |
| 롤백·복구 |  | PASS / FAIL / NOT_RUN |  |  |
| repository + configured workspace readback |  | PASS / FAIL / NOT_CONFIGURED / NOT_RUN |  |  |

## 8. Whole-state adversarial loop receipts

각 loop는 현재 exact head와 전체 정본·소비처·검증 상태를 다시 읽은 뒤, 서로 다른 대안을 실제 근거로 비교하고 Finding을 비판·수정·회귀 검사·재공격까지 닫는다. 한 Finding만 반복하거나 이전 loop의 부분 결과를 전체 상태 검토로 승격하지 않는다.

| loop_index | exact_head | whole_state_readback | alternatives | finding | validation | refinement | regression | whole_state_re_attack | result |
|---|---|---|---|---|---|---|---|---|---|
| 1 |  |  |  |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |  |  |  |
| 3 |  |  |  |  |  |  |  |  |  |
| 4 |  |  |  |  |  |  |  |  |  |
| 5 |  |  |  |  |  |  |  |  |  |

`CLEAN_REVIEW_EXIT`는 at least five completed rows가 있고, 모든 행에 `whole_state_re_attack` 증거가 있으며, 마지막 재공격에서 유효한 차단 Finding이 없을 때만 기록할 수 있다. 그 전에는 `REVIEW_INCOMPLETE`로 남긴다.

## 9. 최종 판정

```text
NO_CONFLICT
CONFLICT_FIXED
USER_DECISION_REQUIRED
BLOCKED_UNVERIFIED
REVIEW_INCOMPLETE
CLEAN_REVIEW_EXIT
```

- 판정:
- 근거:
- 정본 충돌:
- 최근 승인 누락:
- configured workspace 불일치:
- 범위 외 변경:
- 중복 구현·PR:
- 회귀:
- 미검증:
- whole-state loop 상태:

## 10. 후속 조치

- 즉시 수정:
- 사용자 결정 필요:
- 보류:
- 재개 조건:
- 롤백:
- 다음 작업:

## 11. 완료 점검

- [ ] 병합 뒤 새 `main` HEAD를 재조회했다.
- [ ] 병합 PR·Commit의 실제 diff를 확인했다.
- [ ] 현재 확정 Decision과 분야 책임 원본을 비교했다.
- [ ] 최근 승인 누락과 이전 Decision 부활을 검사했다.
- [ ] `CONFIGURED_PROJECT_WORKSPACE`가 있으면 assigned responsibility를 재조회했고, 없으면 `NOT_CONFIGURED`로 기록했다.
- [ ] 동일 Goal의 열린·중복 PR을 확인했다.
- [ ] head branch 삭제 또는 자동 삭제 설정을 확인했다.
- [ ] 공격과 비판 검증을 분리했다.
- [ ] 실행 가능한 구체적 Finding은 필요 시 fix-guided 반사실 검증으로 재판정했다.
- [ ] 필요한 최소 수정 뒤 회귀 재검사를 수행했다.
- [ ] 최소 다섯 개의 whole-state adversarial loop를 exact head 기준으로 완료하고 마지막 loop를 재공격했다.
- [ ] 실행하지 못한 검사를 통과로 표시하지 않았다.
- [ ] 최종 판정과 남은 위험을 보고했다.
