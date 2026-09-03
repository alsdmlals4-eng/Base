# Grill Me 의사결정 인터뷰 프로토콜

Grill Me는 `managing-project-intake-and-work-contract`의 `clarify` Skill Mode에서 사용하는 프로젝트 핵심 결정 인터뷰다. 독립 Skill ID를 추가하지 않는다. 기존의 요구 확인·상태·사용자 승인 계약을 유지하면서 질문 품질, 승인 즉시 동기화와 종료 기준을 강화한다.

공용 동기화 계약은 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다.

## 1. 사용 조건

다음 중 하나 이상이 프로젝트 방향이나 결과를 바꿀 때 사용한다.

- 프로젝트 코어·플레이어 판타지·Core Loop
- 뾰족한 재미의 우선순위
- 서로 충돌하는 시스템·UX·콘텐츠 원칙
- MVP와 확장 범위
- KEEP / AMPLIFY / CHANGE / DEFER / REMOVE
- 실패·복구·보상 의미
- 경쟁작 대비 차별화
- PoC·Vertical Slice의 가장 위험한 가설
- GPT와 Codex의 책임·승인·구현 경계
- 기존 승인 정본을 대체하는 중요 방향 변경

오탈자, 단일 파일 기계 수정, 같은 입력의 검사 재실행, 저장소에서 이미 확인 가능한 사실에는 사용하지 않는다.

## 2. 질문 전 필수 대조

각 질문 전에 다음을 순서대로 확인한다.

```text
프로젝트 GitHub main 최신 HEAD
→ 동일 Goal의 열린 Issue·PR·Branch
→ 최근 병합 PR과 후속·대체 링크
→ 프로젝트 AGENTS·START_HERE·ACTIVE_CONTEXT
→ CURRENT_CONFIRMED_DECISIONS.md
→ 관련 분야 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 정확한 Project Notion Home과 관련 사람용 source/destination
→ 알려진 unique legacy Sheet material의 migration 상태(있을 때만, `COMPATIBILITY_ONLY`)
→ 현재 대화
→ 질문 필요성 판정
```

다음 질문 전 게이트를 모두 통과해야 한다.

1. 저장소·책임 원본·Project Notion Home·현재 대화에서 답을 찾을 수 없는가? legacy Sheet는 알려진 unique material의 migration 조사일 때만 비교한다.
2. 사용자가 이미 같은 결정에 답하지 않았는가?
3. 최신 Decision으로 대체·폐기·보류되지 않았는가?
4. 실제로 프로젝트 방향·플레이 경험·범위·제작 가능성을 바꾸는가?
5. 구현자가 정할 기술 세부나 초기 시험값이 아니라 사용자 결정인가?
6. 동일 Goal의 열린 PR 또는 최근 병합 PR에서 이미 처리되지 않았는가?
7. 이전 승인 건이 `SYNCED` 상태인가?

하나라도 질문이 불필요하다고 판정되면 묻지 않는다.

## 3. 중복 질문 판정

질문 문구가 달라도 결정 대상과 프로젝트 영향이 같으면 중복이다.

다음은 기존 질문으로 처리한다.

- 같은 시스템·기능의 같은 방향을 다시 선택하게 함
- 이전 승인안을 표현만 바꿔 다시 제시함
- `SUPERSEDED`, `REJECTED`, `DEFERRED`된 안을 새 안처럼 제시함
- 정본에는 있으나 현재 대화에 없다는 이유로 다시 물음
- GitHub 또는 Project Notion Home에 이미 확정된 답이 있는데 projection/readback이 늦다는 이유로 다시 물음
- 단계 이름만 다르고 플레이어 결과와 범위가 같음

기존 Decision이 유효하면 질문 없이 적용한다.

```text
기존 Decision ID 확인
→ 승인 당시 전제와 현재 사실 비교
→ 전제가 유지되면 그대로 적용
→ 달라진 사실만 기록
→ 중요 기획 충돌일 때만 재결정 질문
```

기존 결정을 다시 논의할 때는 처음부터 같은 질문을 반복하지 않고 기존 Decision ID, 승인일, 기존 결정, 새 사실, 충돌, 유지·변경 영향과 GPT 권장안을 제시한다.

승인 요청에서 사용자가 확정한 선택은 그대로 집행한다. 그 선택을 벤치마킹 결과만으로 되돌리거나 다른 기본값으로 바꾸지 않는다. 승인 외 변경만 벤치마킹·현업 비교·충돌·누락 조사와 적대적 검토를 거쳐 장기적으로 더 나은 안을 제안한다.

## 4. 사용자 결정과 권장 기본값 분리

### 4.1 `RECOMMENDED_DEFAULT`

프로젝트 방향을 바꾸지 않고 정본·기술 표준·테스트로 최소 안전안이 정해지는 항목은 묻지 않는다.

- 파일·함수·클래스·노드 명명과 내부 분리
- 일반적인 Godot 노드 구성과 내부 데이터 형식
- 오류 처리·로그·테스트 구성
- UI 여백·정렬의 초기값
- 입력 버퍼·전환 시간·쿨다운의 초기 시험값
- 플레이테스트 전 밸런스 초깃값
- 기존 정본을 그대로 구현하기 위한 기술 선택
- 명백한 참조 누락·테스트 실패·표준 위반 수정

다음 형식으로 기록하고 진행한다.

```yaml
classification: RECOMMENDED_DEFAULT
selected_value:
reason:
canonical_impact: NONE | TECHNICAL_ONLY
adjustment_condition:
validation:
```

### 4.2 `USER_DECISION_REQUIRED`

다음은 사용자에게 한 번에 하나씩 묻는다.

- 프로젝트 코어·플레이어 판타지·Core Loop 변경
- 장르·플랫폼·타깃·세션 구조 변경
- 중요 시스템·주요 UX·아트 방향·서사 의미 변경
- 기존 승인 Decision의 폐기·대체
- 분야 책임 원본끼리의 기획 충돌
- 범위·비용·출시·사업 방향의 큰 변경
- 되돌리기 어렵거나 다른 시스템에 광범위한 영향을 주는 결정

수치라도 난이도, 경제, 성장 속도, 세션 길이, 빌드 우열, 보상 체감과 선택 의미를 근본적으로 바꾸면 사용자 결정이다.

## 5. 한 번에 하나

- 한 메시지에는 하나의 결정 질문만 둔다.
- 여러 결정이 필요하면 의존성이 높은 것부터 순차적으로 묻는다.
- 질문 수를 채우기 위해 비차단 질문을 만들지 않는다.
- 사용자가 `모두 권장안대로`라고 하면 남은 동등 유형 결정을 권장안으로 일괄 확정하고 질문을 계속 늘리지 않는다.
- 이전 승인 건의 repository 정본·main·적용 가능한 Notion destination readback이 완료되기 전에 다음 질문으로 넘어가지 않는다.

## 6. GitHub 질문 기록

질문 전에 같은 인터뷰·Goal의 활성 GitHub Issue 또는 PR conversation을 찾는다. 새 질문마다 PR을 만들지 않고 하나의 활성 추적 surface를 재사용한다.

```markdown
## 질문 — DEC-YYYY-MM-DD-NNN

- Work Mode:
- 분야:
- 기존 Decision ID:
- 확인한 정본:
- main HEAD:
- 관련 열린 PR:
- 최근 병합 PR:
- Notion destination / legacy migration 상태:
- 질문:
- 선택지:
- GPT 권장안:
- 프로젝트 영향:
- 상태: AWAITING_USER_DECISION
```

활성 추적 surface가 없고 질문 기록이 필요한 프로젝트에서는 프로젝트 GitHub 운영 규칙에 따라 계획 Issue 하나를 만든다.

## 7. 사용자 질문 형식

```md
## Grill Me — <Decision ID>

### 기존 정본 비교

- 관련 책임 원본:
- 기존 Decision ID:
- 현재 확정 내용:
- main HEAD:
- 관련 열린 PR:
- 최근 병합 PR:
- Notion destination readback / legacy migration 상태:

### 질문

<사용자가 결정해야 하는 하나의 질문>

### 이 결정이 중요한 이유

<프로젝트 코어·플레이 경험·범위·제작 가능성 영향>

### 새로 발생한 사실·충돌

<기존 결정과 달라진 사실, 충돌 또는 UNVERIFIED>

### 선택지

#### A. <선택지>
- 장점:
- 단점:
- 프로젝트 영향:

#### B. <선택지>
- 장점:
- 단점:
- 프로젝트 영향:

#### C. <필요한 경우>
- 장점:
- 단점:
- 프로젝트 영향:

### GPT 권장안

<권장 선택지>

### 권장 이유

<플레이어 가치·프로젝트 코어·제작 가능성 근거>

### 선택 시 확정되는 사항

<영향받는 책임 원본·시스템·범위·후속 작업>

### 답변 형식

A / B / C / 직접 수정안 / 권장안대로
```

## 8. 좋은 질문

- 핵심 플레이어 판타지와 감정을 결정한다.
- 반복 플레이를 만드는 핵심 행동을 결정한다.
- 시스템 충돌의 우선권을 결정한다.
- MVP와 확장 범위를 나눈다.
- 제거·감량·보류 여부를 결정한다.
- 실패와 복구의 의미를 결정한다.
- 제작비와 플레이 가치를 비교한다.
- 경쟁작 대비 차별점과 PoC 가설을 결정한다.
- 기존 승인 정본을 유지할지 대체할지 결정한다.

## 9. 나쁜 질문

- 저장소·Project Notion Home을 보면 알 수 있는 사실
- 파일 경로·기존 상태 확인
- 사소한 명칭·수치·구현 세부
- 이미 답한 질문
- 대체·폐기·보류된 안을 새 안처럼 제시
- 여러 결정을 한 문장에 합친 질문
- 선택지의 영향·권장안이 없는 질문
- 사용자가 전체 권장안을 승인한 뒤 같은 수준의 질문 반복
- 이전 승인 동기화가 실패했는데 다음 질문을 계속함

## 10. 답변 처리와 즉시 동기화

사용자 답변 직후 다음을 같은 승인 단위에서 수행한다.

1. `CONFIRMED / LATEST_OVERRIDE / SUPERSEDED / REJECTED / DEFERRED / UNRESOLVED / UNVERIFIED_CONTEXT`로 판정한다.
2. 기존 GitHub 댓글 흐름에 사용자 답변 원문과 최종 Decision을 기록한다.
3. `templates/project-operations/GRILL_ME_DECISION_RECORD.md`에 기록한다.
4. 프로젝트 `CURRENT_CONFIRMED_DECISIONS.md`를 갱신한다.
5. 영향받는 기획 책임 원본과 실행 계약을 갱신한다.
6. 필요한 경우 `ACTIVE_CONTEXT.md`를 갱신한다.
7. 승인 결정 문서가 직접 `main` 반영 허용 범위면 논리 Commit 하나로 반영한다.
8. 새 `main` HEAD와 Commit SHA를 재조회한다.
9. 적용 가능한 Project Notion destination에 사람용 Decision projection을 추가·수정한다.
10. 해당 Notion destination을 재조회해 Decision ID·결정·Commit·대체 관계를 비교한다.
11. GitHub 댓글에 정본 경로, Commit SHA, Notion destination과 readback 판정을 기록한다.
12. `SYNCED`면 다음 질문 필요성을 재평가한다.

직접 `main` 반영 허용 범위와 구현 PR 분리는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다.

GPT 제안은 사용자 승인 전까지 확정이 아니다.

## 11. 동기화 실패

```text
QUESTION_RECORDED
AWAITING_USER_DECISION
APPROVED_PENDING_CANON
CANON_UPDATED
MAIN_UPDATED
NOTION_UPDATED
SYNCED
SYNC_FAILED
BLOCKED_UNVERIFIED
```

- GitHub 쓰기 실패: 댓글에 실패·영향·재개 조건을 기록한다.
- Notion destination 쓰기 또는 readback 실패: repository 정본은 유지하고 `SYNC_FAILED`와 재동기화 Decision ID를 남긴다.
- legacy Sheet가 unique material을 가진 경우에는 `COMPATIBILITY_ONLY`로 source·owner·이관 상태를 기록한다. legacy Sheet의 쓰기 실패는 current canon을 막지 않으며, unique material이 미이관이면 `BLOCKED_UNVERIFIED`로 남긴다.
- 권한·연결·destination을 확인할 수 없음: `BLOCKED_UNVERIFIED`로 남긴다.
- `SYNCED`가 아닌 승인 건이 있으면 비차단 질문을 계속 늘리지 않는다.

## 12. 적용 단계

- `GRILL_ME_0`: 저장소 조사 후 초기 의도·비타협 조건 확인
- `GRILL_ME_1`: 초기 코어·Core Loop·시스템 우선순위 검수
- `GRILL_ME_2`: 벤치마킹·제작 범위·PoC·Vertical Slice 검수
- `GRILL_ME_3`: 적대적 검토 후 최종 코어·MVP·구현 인계 승인

사용자가 이미 명확히 답한 항목은 단계가 달라도 다시 질문하지 않는다.

## 13. 종료 조건

다음을 모두 만족하면 종료한다.

- 핵심 결정 분기가 해소됐다.
- 사용자의 우선순위와 비타협 조건이 명확하다.
- 변경 가능·제거·보류 요소가 기록됐다.
- 서로 충돌하는 사용자 답변이 없다.
- 모든 승인 Decision이 `CURRENT_CONFIRMED_DECISIONS.md`와 분야 책임 원본에 반영됐다.
- 승인 문서가 `main`에 반영되고 Commit SHA가 기록됐다.
- 적용 가능한 Project Notion destination readback 결과가 repository 정본과 일치한다.
- 모든 승인 건의 동기화 상태가 `SYNCED` 또는 명시적 `BLOCKED_UNVERIFIED`다.
- 남은 질문이 구현 세부 또는 비차단 수준이다.

최종 프로젝트 코어와 구현 인계는 사용자 승인 후에만 다음 상태를 사용한다.

```text
CORE_CONFIRMED
READY_FOR_IMPLEMENTATION_HANDOFF
```

## 14. 실패 조건

- 저장소·정본·Project Notion Home에서 확인할 사실을 질문함
- 같은 Decision을 표현만 바꿔 다시 질문함
- 한 번에 여러 결정을 질문함
- 권장안과 영향 분석을 누락함
- 기술 세부·초기 시험값을 사용자 결정으로 전가함
- 사용자 답변을 GitHub 추적 surface에 기록하지 않음
- 승인 답변을 checkpoint까지 임시 누적함
- `CURRENT_CONFIRMED_DECISIONS.md`만 갱신하고 분야 책임 원본을 누락함
- repository 또는 적용 가능한 Notion destination 한쪽만 갱신하고 `SYNCED`로 보고함
- 승인 전 `CORE_CONFIRMED` 사용
- 제거·보류·기각 항목을 누락으로 재제안함
- `모두 권장안대로` 승인 뒤 불필요한 질문을 계속함
- 동기화 실패를 숨기고 다음 질문으로 이동함
