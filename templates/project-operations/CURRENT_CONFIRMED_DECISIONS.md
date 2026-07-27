# 현재 확정 결정

이 문서는 새 채팅·새 AI·새 작업자가 **한 파일만 먼저 읽어도 현재 승인 사항, 보호 범위, 대체 관계와 동기화 상태를 복원**하기 위한 프로젝트 승인 결정 정본이다.

상세 시스템 규칙은 등록된 분야 책임 원본이 담당한다. 이 문서는 상세 기획서를 장문 복제하지 않고 Decision의 핵심과 상세 원본 경로를 연결한다.

## 1. 문서 상태

```yaml
project:
repository:
google_sheet:
status: CURRENT | SYNC_FAILED | BLOCKED_UNVERIFIED
baseline_branch: main
baseline_commit:
last_decision_id:
last_synced_at:
updated_by:
```

## 2. 현재 프로젝트 약속

- 프로젝트 한 문장:
- 목표 플레이어:
- 핵심 플레이어 판타지:
- Core Loop:
- 뾰족한 재미:
- 목표 플랫폼:
- 현재 제품 단계:
- 현재 Work Mode:
- 상세 책임 원본:

## 3. 보호 결정

현재 작업에서 사용자 재승인 없이 변경하지 않을 항목만 적는다.

| 영역 | 보호 결정 | Decision ID | 상세 정본 | 재검토 조건 |
|---|---|---|---|---|

## 4. 현재 확정 Decision

| Decision ID | 승인일 | 분야 | 상태 | 최종 결정 | 플레이어·프로젝트 영향 | 상세 책임 원본 | 대체 Decision | main Commit | Sheet 위치 | GitHub 추적 |
|---|---|---|---|---|---|---|---|---|---|---|

상태:

```text
CURRENT
LATEST_OVERRIDE
SUPERSEDED
REJECTED
DEFERRED
UNRESOLVED
BLOCKED_UNVERIFIED
```

`CURRENT`와 `LATEST_OVERRIDE`만 현재 적용 결정이다. `SUPERSEDED`, `REJECTED`, `DEFERRED`는 같은 질문을 다시 제안하지 않도록 이유와 재검토 조건을 남긴다.

## 5. Decision 상세

### DEC-YYYY-MM-DD-NNN — 결정 제목

```yaml
status: CURRENT
approved_at:
approved_by: user
classification: USER_DECISION_REQUIRED | RECOMMENDED_DEFAULT
area:
question:
user_answer:
final_decision:
reason:
player_impact:
implementation_impact:
protected_scope:
excluded_scope:
supersedes:
superseded_by:
detailed_canonical_sources:
tracking_surface:
main_commit:
google_sheet_tab:
google_sheet_row:
sync_status: SYNCED | SYNC_FAILED | BLOCKED_UNVERIFIED
reconsider_when:
```

## 6. 권장 기본값 기록

프로젝트 방향을 바꾸지 않는 기술·초기 튜닝은 사용자 질문 대신 여기에 필요한 만큼만 기록한다.

| 항목 | 권장값 | 이유 | 정본 영향 | 검증·조정 조건 | 반영 위치 |
|---|---|---|---|---|---|

권장 기본값은 플레이테스트·런타임 증거가 나오면 조정할 수 있다. 핵심 재미·경제·난이도·세션 길이·주요 UX를 바꾸는 수치는 사용자 결정으로 승격한다.

## 7. 대체·폐기 관계

| 이전 Decision | 상태 | 현재 Decision | 대체 이유 | 다시 제안하지 않을 범위 | 재검토 조건 |
|---|---|---|---|---|---|

## 8. 미결정·보류·차단

| 항목 | 상태 | 사용자 결정 필요 여부 | 차단 영향 | 다음 조건 | 관련 정본·Issue·PR |
|---|---|---|---|---|---|

상태:

```text
UNRESOLVED
DEFERRED
BLOCKED_UNVERIFIED
SYNC_FAILED
```

## 9. GitHub·Google Sheets 동기화 상태

```yaml
main_head:
last_confirmed_decision:
last_decision_commit:
google_sheet_id:
google_sheet_tab:
last_sheet_row:
last_sheet_read_at:
last_sync_result: SYNCED | SYNC_FAILED | BLOCKED_UNVERIFIED
open_active_pr:
recent_merged_pr:
branch_cleanup: DELETED | AUTO_DELETE_ENABLED | NOT_APPLICABLE | UNVERIFIED_REPOSITORY_SETTING
```

### 미동기화 항목

| Decision ID | GitHub main | 분야 정본 | Google Sheets | GitHub 댓글 | 복구 작업 | 상태 |
|---|---|---|---|---|---|---|

## 10. 질문 전 중복 검사

새 질문 전에 확인한다.

- [ ] 최신 `main` HEAD를 확인했다.
- [ ] 동일 Goal의 열린 Issue·PR·Branch를 확인했다.
- [ ] 최근 병합 PR과 후속·대체 링크를 확인했다.
- [ ] 이 문서의 현재·대체·폐기 Decision을 확인했다.
- [ ] 관련 분야 책임 원본을 확인했다.
- [ ] 실제 구현·데이터·자산·테스트를 확인했다.
- [ ] Google Sheets의 마지막 Decision ID와 Commit SHA를 확인했다.
- [ ] 기존에 답한 질문과 실질적으로 동일하지 않다.
- [ ] 기술 기본값이 아니라 사용자만 결정할 수 있는 중요 기획이다.

## 11. 승인 즉시 동기화 점검

- [ ] 사용자 답변 원문을 GitHub 추적 surface에 기록했다.
- [ ] Decision ID와 상태를 확정했다.
- [ ] 이 문서를 갱신했다.
- [ ] 관련 분야 책임 원본을 갱신했다.
- [ ] 필요한 Active Context·작업 계약을 갱신했다.
- [ ] 승인 문서를 `main`에 반영했다.
- [ ] main Commit SHA를 재조회했다.
- [ ] Google Sheets 행을 추가·수정했다.
- [ ] Google Sheets 행을 재조회했다.
- [ ] GitHub와 Sheet의 Decision·Commit·대체 관계가 일치한다.
- [ ] GitHub 댓글에 반영 위치와 동기화 판정을 기록했다.
- [ ] 최종 상태가 `SYNCED`다.

## 12. 병합 후 적대적 검토 최근 결과

| 날짜 | PR·Commit | 새 main HEAD | 관련 Decision | 정본 충돌 | 승인 누락 | Sheet 불일치 | 회귀 | 최종 판정 | 보고 경로 |
|---|---|---|---|---|---|---|---|---|---|

최종 판정:

```text
NO_CONFLICT
CONFLICT_FIXED
USER_DECISION_REQUIRED
BLOCKED_UNVERIFIED
```

## 13. 변경 원칙

- 승인 전 제안은 현재 확정 Decision으로 넣지 않는다.
- 동일 질문의 장문 규칙을 이 문서와 분야 정본 양쪽에 복제하지 않는다.
- 최신 승인으로 대체된 이전 Decision을 삭제하지 않고 관계를 남긴다.
- GitHub 댓글·Sheet만 갱신하고 정본 갱신 완료를 주장하지 않는다.
- `SYNCED`가 아닌 승인 건은 숨기지 않는다.
- 실제 실행하지 않은 CI·런타임·Sheets 확인을 통과로 표시하지 않는다.
