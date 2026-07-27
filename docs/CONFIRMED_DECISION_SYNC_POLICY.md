# 승인 결정 즉시 동기화 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 기획·Grill Me·검수 중 확정된 결정을 누락 없이 복원하고, 같은 질문 반복·정본 drift·PR 누적을 막기 위한 공용 정본이다.

GitHub 객체의 생명주기는 `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`, Work Mode와 Skill 라우팅은 `docs/WORK_MODE_AND_SKILL_ROUTING.md`, 문서 책임 원본과 발행은 `skills/managing-design-documents/SKILL.md`, 실제 변경 검증은 `skills/reviewing-and-validating-project-changes/SKILL.md`가 계속 책임진다.

## 1. 목표

- 질문 전에 기존 승인 사항과 현재 구현을 확인해 같은 결정을 다시 묻지 않는다.
- 사용자에게는 프로젝트 코어·중요 기획·방향성·정본 충돌만 결정 요청한다.
- 승인된 결정은 같은 승인 단위에서 GitHub 정본, `main`, 프로젝트 Google Sheets에 반영한다.
- 장시간 인터뷰가 중단돼도 `CURRENT_CONFIRMED_DECISIONS.md` 하나로 현재 승인 상태를 복원한다.
- 구현 PR은 하나의 Goal에 하나만 유지하고 검증 완료 뒤 즉시 병합한다.
- 모든 병합 뒤 적대적 검토로 최근 승인 누락·정본 충돌·회귀를 재검사한다.

## 2. 책임과 우선순위

### 2.1 책임 surface

| Surface | 책임 | 정본 여부 |
|---|---|---|
| 최신 사용자 지시 | 현재 요청과 승인 원문 | 최우선 요구 권한 |
| GitHub Issue·PR 댓글 | 질문, 사용자 답변, 승인 시점, 검토 대화의 추적 증거 | 최종 정본 아님 |
| `CURRENT_CONFIRMED_DECISIONS.md` | 현재 승인 결정의 요약, 대체 관계, 반영 위치, 동기화 상태 | 승인 결정 복원 정본 |
| 등록된 분야 Markdown·JSON | 시스템·서사·아트·UI 등 상세 규칙과 예외 | 질문별 상세 책임 원본 |
| `ACTIVE_CONTEXT.md` | 현재 단계·작업·위험·다음 행동 | 현재 상태 원본 |
| GitHub `main` | 반영된 문서·코드·데이터·자산의 실제 저장소 상태 | 통합 상태 |
| 프로젝트 Google Sheets | 사용자가 확인·편집하는 동기화 작업면 | GitHub 정본의 운영 mirror |
| 과거 PR·Commit | 검토·변경·롤백 이력 | 과거 증거 |

`CURRENT_CONFIRMED_DECISIONS.md`는 상세 기획서를 장문 복제하지 않는다. 결정의 핵심, 보호 범위, 대체 관계와 상세 책임 원본 경로를 기록한다. 상세 규칙 충돌 시 최신 사용자 승인과 등록된 분야 책임 원본을 대조해 해결한다.

### 2.2 충돌 우선순위

```text
최신 사용자 승인
→ 프로젝트 AGENTS·보안·엔진·데이터 규칙
→ CURRENT_CONFIRMED_DECISIONS.md의 현재 Decision
→ 등록된 분야 책임 원본
→ ACTIVE_CONTEXT·승인된 작업 계약
→ 실제 main 코드·데이터·자산·테스트
→ 프로젝트에 동기화된 Base 기준
→ 외부 근거·과거 대화·추정
```

실제 구현과 승인 정본이 다르면 어느 한쪽을 자동으로 진실로 간주하지 않는다. 구현 누락인지 정본 미갱신인지 판정하고 `CANON_CONFLICT`로 보고한다.

## 3. 새 채팅·새 작업 시작 입력

가능하면 다음을 받는다.

```text
Base repository URL
Project name and GitHub repository URL
Project Google Sheets URL
현재 요청
```

링크가 이미 대화나 프로젝트 정본에 있으면 다시 묻지 않는다. 저장소·Google Drive connector로 확인 가능한 정보도 사용자에게 되묻지 않는다.

## 4. 모든 L1 이상 작업의 사전 대조

새 질문·기획·검수·구현 계획 전에 다음 순서로 확인한다.

```text
프로젝트 GitHub main 최신 HEAD
→ 동일 Goal의 열린 Issue·PR·Branch
→ 최근 병합 PR과 후속·대체 링크
→ 프로젝트 AGENTS·START_HERE·ACTIVE_CONTEXT
→ CURRENT_CONFIRMED_DECISIONS.md
→ 관련 분야 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 프로젝트 Google Sheets 최신 행·탭
→ 마지막 Decision ID·Commit SHA·Sheet row 비교
→ 중복·충돌·미반영·미검증 판정
→ 작업 시작
```

판정 상태:

```text
CANON_MATCH
CANON_CONFLICT
SHEET_OUTDATED
GITHUB_OUTDATED
OPEN_PR_EXISTS
DUPLICATE_WORK
DUPLICATE_QUESTION
MISSING_DECISION_SYNC
BLOCKED_UNVERIFIED
```

`CANON_CONFLICT`, `DUPLICATE_WORK`, `DUPLICATE_QUESTION`, `MISSING_DECISION_SYNC`가 발견되면 새 질문이나 새 PR보다 기존 상태 복원을 먼저 수행한다.

## 5. 중복 질문 방지

질문 문구가 달라도 결정 대상과 결과가 같으면 중복 질문이다.

다음은 다시 묻지 않는다.

- 이미 `CURRENT`인 Decision과 동일한 방향 선택
- 이전 승인안을 표현만 바꾼 선택지
- `SUPERSEDED` 또는 `REJECTED`된 안을 새 안처럼 제시하는 질문
- GitHub에는 있으나 Sheets가 늦다는 이유로 같은 결정을 재질문하는 경우
- 현재 대화에 없다는 이유만으로 정본에 있는 결정을 재질문하는 경우
- 단계 이름만 달라지고 실제 프로젝트 영향이 같은 질문

기존 결정이 있으면 다음처럼 처리한다.

```text
기존 Decision ID 확인
→ 현재 전제가 유지되는지 검사
→ 유효하면 질문 없이 적용
→ 달라진 사실만 비교
→ 프로젝트 방향을 바꾸는 충돌일 때만 재결정 요청
```

재결정 질문에는 기존 Decision ID, 승인일, 기존 결정, 새 사실, 충돌, 유지·변경 영향, GPT 권장안을 포함한다.

## 6. 사용자 질문과 권장 기본값 분리

### 6.1 `RECOMMENDED_DEFAULT`

프로젝트 방향을 바꾸지 않고 최소 안전안이 정본·기술 표준·테스트로 결정되는 사항은 사용자에게 묻지 않는다.

예:

- 파일·폴더·함수·클래스 명명과 분리
- 일반적인 Godot 노드 구성과 내부 데이터 구조
- 오류 처리·로그·테스트 구성
- 임시 디버그 설정
- UI 여백·정렬의 초기값
- 입력 버퍼·전환 시간·쿨다운의 초기 시험값
- 플레이테스트 전 밸런스 초깃값
- 기존 정본을 그대로 구현하기 위한 기술 선택
- 명백한 참조 누락·테스트 실패·표준 위반 수정

기록 형식:

```yaml
classification: RECOMMENDED_DEFAULT
selected_value:
reason:
canonical_impact: NONE | TECHNICAL_ONLY
adjustment_condition:
validation:
```

### 6.2 `USER_DECISION_REQUIRED`

다음은 사용자와 논의한다.

- 프로젝트 코어·플레이어 판타지·Core Loop 변경
- 장르·플랫폼·타깃·세션 구조 변경
- 중요 시스템 추가·삭제·우선순위 변경
- 주요 UI·UX·아트 방향·서사 의미 변경
- 기존 승인 결정 폐기·대체
- 분야 책임 원본끼리의 기획 충돌
- 범위·비용·출시·사업 방향의 큰 변경
- 되돌리기 어렵거나 다른 시스템에 광범위한 영향을 주는 결정

수치도 난이도, 경제, 성장 속도, 세션 길이, 빌드 우열, 보상 체감, 선택 의미를 근본적으로 바꾸면 기획 결정이다.

## 7. 질문 기록

질문은 하나의 활성 GitHub 추적 surface에 댓글로 남긴다. 같은 인터뷰·Goal에서는 새 PR을 만들지 않고 기존 Issue 또는 PR conversation을 재사용한다. 활성 surface가 없다면 프로젝트 운영 규칙에 따라 계획 Issue 하나를 만든다.

```markdown
## 질문 — DEC-YYYY-MM-DD-NNN

- Work Mode:
- 분야:
- 기존 Decision ID:
- 확인한 정본:
- main HEAD:
- 관련 열린 PR:
- 최근 병합 PR:
- Sheet 동기화 상태:
- 질문:
- 선택지:
- GPT 권장안:
- 프로젝트 영향:
- 상태: AWAITING_USER_DECISION
```

질문은 한 번에 하나의 중요 결정만 포함한다.

## 8. 승인 즉시 동기화

사용자 답변 직후 다음을 같은 승인 단위에서 완료한다.

```text
사용자 답변 원문 보존
→ 기존 댓글 흐름에 승인 결과 기록
→ Decision 상태 판정
→ CURRENT_CONFIRMED_DECISIONS.md 갱신
→ 영향받는 분야 책임 원본 갱신
→ 필요한 ACTIVE_CONTEXT·작업 계약 갱신
→ 승인 결정 문서를 main에 반영
→ main Commit SHA 재조회
→ 프로젝트 Google Sheets 행 추가·수정
→ GitHub 댓글에 Commit·Sheet 위치 기록
→ GitHub main과 Sheet를 재조회
→ 내용·Decision ID·Commit·대체 관계 비교
→ SYNCED 판정
→ 다음 질문
```

승인 결과 댓글:

```markdown
## 승인 결과 — DEC-YYYY-MM-DD-NNN

- 사용자 답변:
- 최종 결정:
- 상태: CONFIRMED | LATEST_OVERRIDE | SUPERSEDED | REJECTED | DEFERRED
- 대체되는 Decision:
- 영향받는 책임 원본:
- main Commit:
- Google Sheets tab·row:
- 동기화 판정: SYNCED | SYNC_FAILED | BLOCKED_UNVERIFIED
```

### 8.1 직접 `main` 반영 허용 범위

사용자가 이 운영 방식을 승인했고 Repository Ruleset이 허용하는 프로젝트에서는 다음 승인 기록을 별도 PR 없이 `main`에 직접 반영할 수 있다.

- `CURRENT_CONFIRMED_DECISIONS.md`
- 승인된 기획 책임 원본의 해당 Section
- `ACTIVE_CONTEXT.md`의 현재 결정 요약
- Decision 상태·Registry의 해당 메타데이터

직접 반영은 승인 한 건당 논리 Commit 하나를 기본값으로 한다.

```text
docs(decision): confirm DEC-YYYY-MM-DD-NNN <decision-title>
```

### 8.2 반드시 구현 PR을 사용하는 범위

- Godot·Web 런타임 코드
- Scene·Resource·게임 데이터 Schema
- 저장 호환성·마이그레이션
- GitHub Actions·Ruleset·자동화
- 대규모 파일 이동·삭제·재구조화
- Base 공용 정책·Skill·Template 변경
- 독립 검증·롤백이 필요한 자산 교체

승인 문서 반영과 실제 구현 완료를 혼동하지 않는다.

## 9. Google Sheets 동기화

프로젝트 Sheet에는 `확정 결정` 또는 프로젝트가 선언한 동일 책임 탭을 사용한다.

권장 열:

```text
Decision ID
승인일
분야
질문
사용자 답변
최종 결정
분류
플레이어 영향
구현 영향
대체 Decision
분야 정본 경로
main Commit SHA
GitHub 추적 surface
동기화 상태
후속 작업
```

Sheets 쓰기 전 정확한 Spreadsheet ID, tab 이름, sheetId, headers, target row를 읽는다. 쓰기 후 해당 행을 다시 읽어 GitHub 정본과 대조한다.

GitHub와 Sheets가 다르면 자동으로 둘 중 하나를 덮어쓰지 않는다. 최신 사용자 승인, Decision ID, Commit SHA, 수정 시각, 분야 정본을 비교해 어느 쪽이 누락됐는지 판정한다. GitHub `main`의 승인 정본이 반영돼 있고 Sheet만 늦으면 `SHEET_OUTDATED`로 복구한다.

## 10. 동기화 상태

```text
QUESTION_RECORDED
AWAITING_USER_DECISION
APPROVED_PENDING_CANON
CANON_UPDATED
MAIN_UPDATED
SHEET_UPDATED
SYNCED
SYNC_FAILED
SUPERSEDED
BLOCKED_UNVERIFIED
```

정상 종료는 `SYNCED`다.

- GitHub 쓰기 실패: 기존 댓글에 실패와 재개 조건을 기록한다.
- Sheet 쓰기 실패: GitHub 정본은 유지하고 `SYNC_FAILED`와 재동기화 대상 Decision ID를 기록한다.
- 권한·연결·탭을 확인할 수 없음: `BLOCKED_UNVERIFIED`로 남긴다.
- `SYNCED`가 아닌 승인 건이 있으면 다음 비차단 질문을 계속 늘리지 않는다.

## 11. PR 중복과 누적 방지

새 PR 전에 다음을 확인한다.

```text
원본 Issue·승인된 Goal
→ 같은 Goal의 열린 PR
→ 같은 작업 Branch
→ 최근 병합 PR
→ 대체·후속 PR
→ 새 PR 필요 여부
```

- 하나의 Goal에는 하나의 활성 PR을 기본값으로 사용한다.
- 리뷰 지적, 테스트 실패, 같은 범위의 문구·데이터·설정 보완은 기존 PR에서 이어간다.
- 승인 결정 문서 동기화는 허용 범위에서 직접 `main`에 반영한다.
- 구현 PR은 검증과 사용자 승인이 끝나면 Squash merge한다.
- 병합된 PR conversation은 장기 검토 증거로 보존한다.
- 안전 조건을 만족한 head branch는 병합 후 삭제한다.
- GitHub connector가 branch 삭제를 지원하지 않으면 Repository의 자동 삭제 설정을 확인하고, 확인하지 못하면 `UNVERIFIED_REPOSITORY_SETTING`으로 보고한다.

## 12. 병합 후 적대적 검토

모든 PR 병합과 직접 `main` 결정 Commit 뒤 다음을 실행한다.

```text
새 main HEAD 고정
→ 병합 PR·Commit diff 확인
→ CURRENT_CONFIRMED_DECISIONS.md 비교
→ 관련 분야 책임 원본 비교
→ 최근 승인 Decision ID 비교
→ Google Sheets 비교
→ attack
→ validate-critique
→ reference freshness·정적·가능한 런타임·회귀 검사
→ finding 분류
→ 필요한 최소 수정
→ regression-recheck
→ 최종 충돌 보고
```

필수 공격 항목:

- 최근 승인 사항이 빠졌는가
- 이전에 대체된 결정이 다시 살아났는가
- 프로젝트 코어·플레이어 약속과 충돌하는가
- 분야 정본 일부만 갱신됐는가
- 실제 diff가 승인 범위를 벗어났는가
- 같은 기능·문서·질문이 중복됐는가
- GitHub와 Sheets가 다른가
- 관련 테스트·템플릿·참조가 untouched로 남았는가
- 기존 정상 경로가 회귀했는가
- 임시값·플레이스홀더를 확정값으로 승격했는가

최종 판정:

```text
NO_CONFLICT
CONFLICT_FIXED
USER_DECISION_REQUIRED
BLOCKED_UNVERIFIED
```

## 13. 병합 후 보고

```markdown
## 병합 후 적대적 검토 결과

### 병합 정보
- 작업:
- PR 또는 직접 Commit:
- 새 main HEAD:
- 관련 Decision ID:
- head branch 처리:

### 정본·동기화 비교
- CURRENT_CONFIRMED_DECISIONS:
- 분야 책임 원본:
- 최근 승인 누락:
- Google Sheets:
- 열린·중복 PR:

### 공격과 비판 검증
- 유효한 finding:
- 기각한 비판:
- 미검증:

### 회귀 재검사
- 실행한 검사:
- 통과:
- 실패:
- 실행하지 못한 검사:

### 최종 판정
- NO_CONFLICT | CONFLICT_FIXED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED

### 후속 조치
- 즉시 수정:
- 사용자 결정:
- 보류·재개 조건:
```

문제가 없더라도 `NO_CONFLICT`와 실제 비교·검사 범위를 명시한다.

## 14. 완료 조건

- 질문 전에 최신 main·정본·PR·Sheet를 비교했다.
- 기존 승인 결정을 다시 묻지 않았다.
- 기술 기본값과 사용자 기획 결정을 구분했다.
- 질문과 승인 원문이 GitHub 추적 surface에 남았다.
- 승인 Decision이 `CURRENT_CONFIRMED_DECISIONS.md`와 분야 정본에 반영됐다.
- 승인 문서가 `main`에 반영되고 Commit SHA가 기록됐다.
- Google Sheets가 갱신되고 재조회 결과가 일치했다.
- 구현 PR은 중복 없이 재사용·병합됐다.
- 병합 후 적대적 검토와 회귀 재검사를 실행했다.
- 미실행·권한·설정은 성공으로 표시하지 않았다.

## 15. 실패 조건

- 정본을 읽지 않고 같은 질문을 반복함
- 사용자에게 파일 경로·명백한 기술 세부·초기 수치를 결정하게 함
- 승인 답변을 대화나 댓글에만 남김
- 승인 결정을 checkpoint까지 임시 누적함
- `CURRENT_CONFIRMED_DECISIONS.md`만 갱신하고 분야 책임 원본을 누락함
- GitHub만 갱신하고 Sheets 동기화를 성공으로 주장함
- Sheets만 갱신하고 `main` 정본 반영을 생략함
- 같은 Goal에 새 PR을 반복 생성함
- 병합된 PR 기록을 삭제 대상으로 오인함
- 병합 뒤 정본·최근 승인·Sheet·회귀 비교를 생략함
- 실행하지 않은 CI·런타임·Sheet 조회를 통과로 보고함
