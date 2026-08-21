# Postmerge Issue Successor Freshness Policy

Status: `ISSUE_SUCCESSOR_FRESHNESS_REQUIRED`
Owner loop: `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`
Invariant: `OPEN_ISSUE_STATUS_IS_NOT_AUTHORITY`

## 목적

프로젝트가 GitHub Issues를 사용한다면, 병합된 변경이 **exact new main**에 실제로 들어온 뒤 open Issue를 다시 읽어 현재 정본·실제 구현·검증 증거와 대조한다.

Issue가 `open`이라는 사실만으로 다음 구현 권한·현재 정본·남은 작업을 만들지 않는다. 반대로 오래된 Issue라는 이유만으로 자동 종료하지도 않는다. 현재 책임은 최신 사용자 지시, 프로젝트 current canon, exact new main의 실제 구현·테스트·증거가 소유한다.

이 정책은 새 Skill이나 별도 수명주기를 만들지 않는다. 기존 `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`의 postmerge readback 단계에 Issue successor freshness를 추가한다.

## 왜 필요한가

병합 후 PR·main만 확인하면 다음 유형의 왜곡이 남을 수 있다.

- 이미 successor 구현이 main에 들어왔는데 predecessor Issue가 open으로 남아 다음 AI가 같은 작업을 재실행함
- 과거 기획 Issue가 최신 canon과 충돌하지만 open이라는 이유로 현재 요구처럼 소비됨
- 실제 미완료 Issue를 일괄 정리하면서 필요한 deferred 작업까지 잃어버림
- 과거 Human QA Issue를 닫은 사실을 현재 Human QA PASS로 잘못 해석함

따라서 Issue 상태는 작업 큐의 보조 신호일 뿐, 현재 권위 그 자체가 아니다.

## Trigger

다음 조건을 모두 만족하면 `ISSUE_SUCCESSOR_FRESHNESS_REQUIRED`를 실행한다.

1. 프로젝트가 GitHub Issues를 실제 작업 추적에 사용한다.
2. 승인 범위의 PR 또는 변경이 default branch에 병합됐다.
3. exact new main SHA를 다시 읽었다.
4. 병합 후 현재 정본·실제 구현·검증 상태를 재판정해야 한다.

GitHub Issues를 사용하지 않는 프로젝트에는 `NOT_APPLICABLE`로 기록할 수 있다.

## 필수 순서

```text
merge
→ exact new main readback
→ open/draft/ready PR inventory read-only
→ open Issue inventory
→ current canon / actual main / evidence cross-check
→ Issue successor classification
→ 필요한 Issue disposition
→ GitHub readback
→ 필요한 Notion current-state sync
→ Notion readback
→ adversarial review
→ progress readback
```

### 1. open PR을 먼저 읽는다

진행 중 `open/draft/ready` PR은 이 정책의 수정 대상이 아니다.

- PR이 소유한 경로·Issue·결정이 있으면 읽기 전용으로 존중한다.
- 현재 Issue 판정이 그 PR의 결과에 의존하면 성급하게 완료/대체 처리하지 않는다.
- 다른 postmerge 교정 PR에서 진행 중 PR의 변경 파일·의미 범위를 흡수하거나 재작성하지 않는다.

### 2. open Issue를 전수 또는 승인 범위에 맞게 열거한다

가능하면 저장소 open Issue 전체를 조회한다. 규모상 전체 조회가 비현실적이면 이번 변경과 동일한 current canon·subsystem·milestone에 연결된 범위를 명시하고, 누락 가능성을 남긴다.

Issue마다 최소한 다음을 대조한다.

- Issue 목적과 완료 기준
- current canon / current planning
- exact new main의 실제 code/data/Scene/doc/test
- merged/closed successor PR 또는 Issue
- 자동 검증과 runtime evidence
- Human QA / device / accessibility evidence
- 아직 유효한 blocker·PLAN_LOCK·승인 경계

## 분류

모든 확인된 Issue는 최소 다음 상태 중 하나로 판정한다.

### `CURRENT_VALID`

현재 정본과 일치하고 실제로 아직 완료되지 않은 작업이다.

- open 유지
- 다음 작업 후보가 될 수 있음
- 단, 별도 승인 Gate가 있으면 그 Gate를 우회하지 않음

### `DEFERRED_VALID`

현재 방향에는 유효하지만 `PLAN_LOCK`, 미충족 선행조건, 권한 부재, 다른 단계 우선 등의 이유로 지금 실행하면 안 되는 작업이다.

- open 유지
- 제목/본문/라벨 등 프로젝트 규칙이 허용하는 방식으로 deferred 상태를 명확히 할 수 있음
- open이라는 이유로 즉시 구현 권한을 부여하지 않음

### `COMPLETED`

exact new main과 필요한 증거가 Issue 책임을 이미 충족한다.

- 증거를 확인한 뒤 close reason `completed` 사용 가능
- 단순히 비슷한 파일이 존재한다는 이유만으로 완료 처리하지 않음

### `SUPERSEDED`

최신 current canon, successor PR/Issue, 통합 구조가 predecessor 책임을 대체한다.

- 과거 기록은 보존
- 현행 작업면에서는 close reason `not_planned` 사용 가능
- successor 위치를 추적 가능하게 남김

### `CONFLICT_WITH_CURRENT_CANON`

Issue가 open이지만 최신 사용자 지시 또는 current canon과 충돌한다.

- 현재 실행 권한으로 사용하지 않음
- 자동 close하지 말고 충돌 근거와 successor 여부를 검토
- 명백한 successor가 확인되면 `SUPERSEDED`로 재분류 가능

### `REVIEW_REQUIRED`

증거가 부족하거나 진행 중 PR·외부 Gate·부분 구현 때문에 완료/대체 여부를 확정할 수 없다.

- open 유지가 기본
- 추정으로 `completed`/`not_planned` 처리하지 않음

## Mutation 규칙

Issue mutation은 classification 뒤에만 수행한다.

| Classification | 기본 처리 |
|---|---|
| `CURRENT_VALID` | open 유지 |
| `DEFERRED_VALID` | open 유지, deferred 상태 명확화 가능 |
| `COMPLETED` | 증거 확인 후 `completed`로 close 가능 |
| `SUPERSEDED` | successor 확인 후 `not_planned`로 close 가능 |
| `CONFLICT_WITH_CURRENT_CANON` | 실행 금지, review/reconcile |
| `REVIEW_REQUIRED` | open 유지, 추가 증거 필요 |

다음은 금지한다.

- 오래됐다는 이유만으로 일괄 close
- Issue 번호가 낮다는 이유만으로 predecessor 판정
- 체크박스가 미완료라는 이유만으로 실제 main successor를 무시
- open이라는 이유만으로 구현 시작
- 진행 중 PR이 소유한 Issue를 다른 작업에서 임의 close

## Evidence ceiling

Issue 정리는 제품 검증 등급을 자동 승격하지 않는다.

특히 과거 Human Validation 또는 Human QA Issue가 `COMPLETED`/`SUPERSEDED`로 정리되더라도, **현재 제품의 Human QA를 실행하지 않았다면 `NOT_RUN`**이다.

동일한 원칙을 다음에도 적용한다.

- runtime verification
- device QA
- accessibility QA
- new-player validation
- `POC_PASSED`
- production expansion approval

`Issue closed`는 `evidence PASS`의 동의어가 아니다.

## GitHub · Notion 동기화

Issue disposition이 사람이 보는 현재 작업 상태·우선순위·남은 작업 수를 바꾸면, GitHub evidence를 먼저 확정한 뒤 해당 Notion current-state만 최소 갱신한다.

Notion 자체가 구현 완료 증거를 만들지 않는다. 동기화 후에는 GitHub와 Notion 양쪽 destination을 다시 읽어 다음을 확인한다.

- exact new main SHA 일치
- open PR inventory가 의도치 않게 변하지 않음
- open Issue count/list가 classification과 일치
- `CURRENT_VALID` / `DEFERRED_VALID`가 손실되지 않음
- 완료·대체 predecessor가 현행 작업처럼 다시 노출되지 않음
- Human QA 등 evidence ceiling이 그대로 유지됨

## 적대적 검토

postmerge adversarial review에서는 최소 다음을 공격한다.

1. 완료된 predecessor가 여전히 open Issue 때문에 현재처럼 보이는가?
2. 실제 미완료 Issue를 과도하게 닫았는가?
3. 진행 중 PR의 소유권을 침범했는가?
4. Issue closure가 Human QA 또는 runtime PASS처럼 오해될 수 있는가?
5. successor가 여러 갈래일 때 current canon이 하나의 실행 경로를 가리키는가?

P0/P1 finding이 남으면 `POSTMERGE_CORRECTION_REQUIRED`로 새 bounded correction을 만들고 다시 검증한다.

## 종료 조건

`ISSUE_SUCCESSOR_FRESHNESS_REQUIRED`는 다음을 모두 만족해야 완료다.

- exact new main readback 완료
- open PR inventory read-only 확인
- 적용 범위의 open Issue classification 완료
- 필요한 `completed` / `not_planned` disposition 완료 또는 명시적 보류
- GitHub Issue readback 완료
- 필요한 경우 Notion sync + readback 완료
- Human QA/runtime 등 evidence ceiling 보존 확인
- `PROGRESS_READBACK_REQUIRED`로 실제 남은 작업 재계산

이 정책의 목표는 Issue 수를 0으로 만드는 것이 아니라, **현재 남은 작업만 open work surface에 남기고 역사·완료·대체 작업은 current authority에서 분리하는 것**이다.
