# Grill Me 결정 원장

## 문서 상태

```yaml
project:
interview_stage: GRILL_ME_0 | GRILL_ME_1 | GRILL_ME_2 | GRILL_ME_3
status: IN_PROGRESS | READY_FOR_APPROVAL | COMPLETE | BLOCKED | UNVERIFIED
baseline_branch: main
baseline_commit:
current_confirmed_decisions:
google_sheet:
active_tracking_surface:
last_synced_decision:
updated_at:
```

## 인터뷰 목적

- 이번 단계에서 해소할 핵심 결정:
- 이미 확정되어 다시 묻지 않을 내용:
- 저장소·PR·Google Sheets 조사로 확인할 내용:
- 사용자만 결정할 수 있는 내용:
- `RECOMMENDED_DEFAULT`로 처리할 기술·초기 수치:

## 질문 전 대조

| 항목 | 확인 위치 | 마지막 확인값 | 상태 | 비고 |
|---|---|---|---|---|
| GitHub main HEAD |  |  | MATCH / OUTDATED / UNVERIFIED |  |
| 동일 Goal 열린 PR |  |  | NONE / EXISTS / UNVERIFIED |  |
| 최근 병합 PR |  |  | CHECKED / UNVERIFIED |  |
| CURRENT_CONFIRMED_DECISIONS |  |  | MATCH / CONFLICT / MISSING |  |
| 분야 책임 원본 |  |  | MATCH / CONFLICT / MISSING |  |
| 실제 구현·데이터·자산·테스트 |  |  | MATCH / CONFLICT / UNVERIFIED |  |
| Google Sheets |  |  | MATCH / OUTDATED / UNVERIFIED |  |
| 미동기화 Decision |  |  | NONE / EXISTS |  |

## 질문 기록

| Decision ID | 질문 | 분류 | 기존 Decision | GPT 권장안 | 사용자 답변 | 최종 결정 | 분야 정본 | main Commit | Sheet 위치 | 동기화 상태 |
|---|---|---|---|---|---|---|---|---|---|---|

분류:

```text
USER_DECISION_REQUIRED
RECOMMENDED_DEFAULT
```

동기화 상태:

```text
QUESTION_RECORDED
AWAITING_USER_DECISION
APPROVED_PENDING_CANON
CANON_UPDATED
MAIN_UPDATED
SHEET_UPDATED
SYNCED
SYNC_FAILED
BLOCKED_UNVERIFIED
```

## 질문별 상세

### Grill Me — DEC-YYYY-MM-DD-NNN

#### 기존 정본 비교

- 관련 책임 원본:
- 기존 Decision ID:
- 기존 확정 내용:
- 현재 전제 유지 여부:
- main HEAD:
- 관련 열린 PR:
- 최근 병합 PR:
- Google Sheets 상태:
- 중복 질문 판정:

#### 질문

사용자가 결정해야 하는 하나의 중요 기획 질문만 적는다.

#### 이 결정이 중요한 이유

프로젝트 코어, 플레이어 경험, 범위 또는 제작 가능성에 미치는 영향을 적는다.

#### 새로 발생한 사실·충돌

기존 Decision과 달라진 사실, 정본 충돌 또는 `UNVERIFIED`를 적는다.

#### 선택지

##### A.

- 장점:
- 단점:
- 프로젝트 영향:

##### B.

- 장점:
- 단점:
- 프로젝트 영향:

##### C.

- 장점:
- 단점:
- 프로젝트 영향:

#### GPT 권장안

#### 권장 이유

#### 선택 시 확정되는 사항

#### GitHub 질문 댓글

- 추적 surface:
- comment ID·URL:
- 기록 상태: QUESTION_RECORDED | FAILED | UNVERIFIED

#### 사용자 답변

#### 최종 결정

```yaml
status: CONFIRMED | LATEST_OVERRIDE | SUPERSEDED | REJECTED | DEFERRED | UNRESOLVED
classification: USER_DECISION_REQUIRED | RECOMMENDED_DEFAULT
supersedes:
protected_scope:
reconsider_when:
```

#### 반영 위치

- `CURRENT_CONFIRMED_DECISIONS.md`:
- 분야 책임 원본:
- Active Context·작업 계약:
- main Commit:
- Google Sheets tab·row:
- GitHub 승인 댓글:

#### 동기화 검증

- GitHub main 재조회:
- 분야 정본 재조회:
- Google Sheets 재조회:
- Decision ID·Commit·대체 관계 일치:
- 최종 상태: SYNCED | SYNC_FAILED | BLOCKED_UNVERIFIED
- 실패·재개 조건:

## 권장 기본값

| 항목 | 권장값 | 이유 | 정본 영향 | 조정 조건 | 검증 | 반영 위치 |
|---|---|---|---|---|---|---|

## 비타협 조건

- 없음

## 변경 가능한 요소

- 없음

## 제거·보류·기각 요소

| 항목 | 상태 | 이유 | 관련 Decision | 다시 제안하지 않을 범위 | 재검토 조건 |
|---|---|---|---|---|---|

## 남은 질문

| 우선순위 | 질문 | 기존 Decision 대조 | 결정권자 | 차단 여부 | 다음 조건 |
|---|---|---|---|---|---|

## 종료 점검

- [ ] 최신 main·열린 PR·최근 병합 PR을 확인했다.
- [ ] `CURRENT_CONFIRMED_DECISIONS.md`와 분야 책임 원본을 확인했다.
- [ ] Google Sheets의 마지막 Decision ID와 Commit을 확인했다.
- [ ] 저장소와 도구에서 답할 수 있는 질문을 사용자에게 하지 않았다.
- [ ] 이미 답한 질문이나 최신 결정으로 대체된 질문을 반복하지 않았다.
- [ ] 기술 세부와 초기 수치는 `RECOMMENDED_DEFAULT`로 처리했다.
- [ ] 질문은 한 번에 하나였다.
- [ ] 각 질문에 선택지·영향·GPT 권장안이 있었다.
- [ ] 질문과 사용자 답변 원문이 GitHub 추적 surface에 기록됐다.
- [ ] 승인 Decision이 `CURRENT_CONFIRMED_DECISIONS.md`에 반영됐다.
- [ ] 승인 Decision이 분야 책임 원본에 반영됐다.
- [ ] 승인 문서가 `main`에 반영되고 Commit SHA가 기록됐다.
- [ ] Google Sheets를 갱신하고 해당 행을 재조회했다.
- [ ] GitHub와 Sheet의 Decision·Commit·대체 관계가 일치한다.
- [ ] 모든 승인 건이 `SYNCED`이거나 명시적 `BLOCKED_UNVERIFIED`다.
- [ ] 핵심 결정 분기가 해소됐다.
- [ ] 비타협·변경 가능·제거·보류 요소가 기록됐다.
- [ ] 남은 질문은 구현 세부 또는 비차단 수준이다.
