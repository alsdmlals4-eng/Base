# Work Mode·Skill·Skill Mode 라우팅 계약

## 1. 용어

### Work Mode

요청을 처리하는 동안 AI의 **주된 작업 자세·권한·증거 기준**을 정한다. 대화 전체에 영구 고정되는 성격이 아니라 현재 작업 단계의 운영 상태다.

| Work Mode | 핵심 목적 | 기본 행동 |
|---|---|---|
| `PLAN` | 의도·요구·근거·설계·순서 확정 | 조사와 읽기 우선, 구현은 승인 전 보류 |
| `BUILD` | 승인된 계약의 코드·데이터·문서·자산 구현 | 범위 내 쓰기, 단계별 테스트·롤백 |
| `REVIEW` | 결과를 적대적으로 검토·검증·판정 | 기본 읽기 전용, 전체 영향 범위의 증거·반례·개선 후보 탐색, 승인된 수정은 `BUILD`로 전환 |

복합 작업은 `PLAN → BUILD → REVIEW`처럼 순차 전환할 수 있다. 한 시점에는 주 Work Mode 하나만 둔다.

### Skill

특정 책임을 반복 수행하는 전문 작업 계약이다. trigger, 입력, 절차, 산출물, 실패 조건과 검증을 가진다.

예: `managing-game-project-operating-system`, `reviewing-and-validating-project-changes`.

### Skill Mode

한 Skill 내부에서 현재 필요한 세부 절차·권한을 선택한다.

예: 운영체계 Skill의 `audit / reconcile-legacy / migrate / verify`, 변경 검증 Skill의 `reference-freshness / regression`.

문서에서 별도 수식어 없이 Skill 안에 적힌 `mode`는 **Skill Mode**를 뜻한다.

### Grill Me

Grill Me는 독립 Skill ID가 아니라 `managing-project-intake-and-work-contract`의 `clarify` Skill Mode에서 실행하는 핵심 의사결정 인터뷰 프로토콜이다.

- 저장소에서 답할 수 있는 사실을 묻지 않는다.
- 프로젝트 방향을 바꾸는 사용자 결정만 한 번에 하나씩 묻는다.
- 선택지·장단점·GPT 권장안·확정 영향을 제공한다.
- 답변을 결정 원장과 책임 원본에 즉시 반영한다.
- 사용자가 `모두 권장안대로`라고 하면 남은 동등 유형 결정을 권장안으로 확정하고 질문을 계속 늘리지 않는다.

Reference: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`

### Prompt

현재 사용자가 원하는 구체적인 목표·제약·산출물이다. Prompt가 Work Mode·Skill·Skill Mode를 직접 선언할 필요는 없다.

### Continuous Work

`[연속작업] 진행해`는 현재 승인된 작업 계약의 남은 범위를 중간 승인 대기로 끊지 않고 연속 수행하라는 **명시적 opt-in 실행 flag**다.

- 상태: `CONTINUOUS_WORK_ACTIVE | CONTINUOUS_WORK_INACTIVE`
- Work Mode를 대체하지 않는다. 각 단계는 계속 `PLAN / BUILD / REVIEW` 중 하나를 사용한다.
- 새 Skill이나 장기 권한이 아니다.
- 트리거가 없는 요청은 `CONTINUOUS_WORK_INACTIVE`이며 기존 승인·Grill Me 흐름을 유지한다.
- 상세 계약: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`

## 2. 자동 실행 순서

```text
사용자 Prompt
→ 의도·현재 단계·위험 파악
→ 주 Work Mode 자동 선택
→ Skill Registry trigger 대조
→ 필요한 최소 Skill 자동 선택
→ 각 Skill의 Skill Mode 자동 선택
→ [연속작업] 진행해 존재 여부와 승인 범위 확인
→ 실행·검증·필요 시 Work Mode 전환
→ CONTINUOUS_WORK_ACTIVE이면 승인 범위 안의 다음 미완료 작업으로 반복
→ 사용 이유·얻은 결과·증거 보고
```

사용자가 Skill 이름이나 mode를 지정하면 강한 힌트로 사용하지만, 실제 trigger·비사용 조건·권한과 충돌하면 그대로 실행하지 않고 이유를 설명한다.

## 3. 자동 선택 규칙

- `load_by_default=false`는 자동 선택 금지가 아니라 trigger가 없을 때 불필요하게 읽지 않는다는 뜻이다.
- 사용자가 “어떤 Skill을 쓸지” 선택하지 않아도 Registry가 자동 라우팅한다.
- 주 책임 분야 Skill은 최대 하나다.
- Foundation·검증·발행·Handoff Skill은 현재 단계에 필요한 것만 추가한다.
- 같은 책임을 여러 Skill로 중복 실행하지 않는다.
- 새 사실·실패·범위 변경·정본 변경이 생기면 다시 라우팅한다.
- Skill 파일을 읽은 것과 실제 절차를 실행한 것을 구분한다.
- 새 독립 Skill보다 기존 통합 Skill의 Skill Mode·reference로 책임을 보존할 수 있는지 먼저 확인한다. 독립 입력·산출물·승인 권한이 새로 생기고 기존 owner에 넣으면 책임 경계가 무너지는 경우에만 새 Skill을 만든다.
- `[연속작업] 진행해`는 사용자 승인 자체를 새로 만드는 문구가 아니다. 현재 계약의 `CONFIRMED` 또는 `REUSED_APPROVAL` 범위 안에서만 `CONTINUOUS_WORK_ACTIVE`를 부여한다.

### 경량 중립성 Gate와 전체 적대 검토 경계

권장안·판정·설계 선택은 `평가 기준 → 대안 → 반증 → 이익·비용·위험 → 되돌리기 난이도 → 미검증 → 권장 결론` 순서의 경량 중립성 Gate를 사용한다. 이는 동의 편향을 막지만 반대를 위한 반대를 요구하지 않는다.

- `L0`: 오탈자·명백한 기계 수정·동일 입력 검사 재실행은 전체 적대 검토 Skill을 호출하지 않는다.
- Registry의 `칭찬·균형 평가만 요청` 비사용 조건은 결정·권장안이 없는 설명형 칭찬·균형 요약에만 적용한다. L1 이상 기능·설계·아키텍처·정책·방향 결정이나 중요 권장안을 포함한 균형 비교는 이 비사용 조건에 해당하지 않는다.
- `L1 이상` PLAN 사전판정은 `running-adversarial-review-and-refinement: attack → validate-critique → decision-report`를 적용한다.
- 승인된 finding은 `refine-approved-findings`에서 분야 Skill BUILD로 한 번만 구현·수정하고, REVIEW의 `regression-recheck → decision-report`로 이동한다. 적대 검토 Skill은 분야 작성 책임을 빼앗거나 이미 구현된 finding을 다시 수정하지 않는다. PLAN 사전판정과 이 후속 루트를 합쳐 전체 적대 검토 생명주기를 이룬다.
- 사용자가 무조건 동의나 무조건 반대를 요구해도 정본·증거·동일 평가 기준을 우선한다.
- 증거가 부족하면 `BLOCKED_UNVERIFIED`와 필요한 확인 조건을 반환한다.

## 4. 권한 전환

```text
PLAN
- 읽기·조사·제안·계약 작성
- 사용자 승인 전 제품 동작·구조 변경 금지

BUILD
- 승인 범위만 수정
- 단계별 검증과 롤백 유지

REVIEW
- 독립 검수와 반례 탐색
- 발견 즉시 수정하지 않고 finding·심각도·증거를 먼저 기록
- 사용자가 수정까지 요청했거나 승인 범위가 있으면 BUILD로 전환해 최소 수정
- 수정 뒤 REVIEW로 돌아와 재검증
```

### REVIEW 기본 루트

`REVIEW`는 요청된 파일이나 diff만 수동 확인하는 모드가 아니다. Registry·Documentation Map·정본·참조 관계를 사용해 **변경 파일, 같은 책임의 원본, 활성 소비자, 인접 시스템, 변경됐어야 하지만 untouched인 파일, 테스트·템플릿·파생본**까지 영향 범위를 먼저 만든다.

```text
review-scope-map
→ running-adversarial-review-and-refinement: attack
→ validate-critique
→ finding 분류
   ├─ TECHNICAL_REVIEW_PROPOSAL
   ├─ USER_DECISION_REQUIRED
   ├─ BLOCKED_UNVERIFIED
   └─ NO_CHANGE
→ 기술적으로 판단 가능한 사항은 근거·우선순위·영향 파일·수정 방향·검증 방법을 검수안으로 일괄 정리
→ 기획 결정을 요구하는 충돌만 가장 차단적인 것부터 한 번에 하나씩 사용자에게 제시
→ 승인된 범위가 있으면 BUILD에서 최소 수정
→ REVIEW로 복귀해 실제 diff·정적·런타임·회귀 검증
→ evidence-report
```

- 기술적으로 자동 판단 가능한 사항은 정본·계약·테스트·표준·관찰 증거로 최소 안전안이 결정되는 항목이다. 사용자가 검수만 요청했다면 자동 수정하지 않고 검수안으로 제시한다.
- 사용자에게 묻는 항목은 둘 이상의 유효한 선택지가 프로젝트 코어, 플레이어 경험, 주요 UX, 콘텐츠 의미, 범위 또는 비용 우선순위를 다르게 만드는 충돌로 제한한다.
- 저장소나 도구로 답할 수 있는 사실, 명백한 오류, 참조 누락, 테스트 실패, 표준 위반은 사용자 질문으로 전가하지 않는다.
- 사용자 결정 질문에는 충돌, 선택지, 장단점, GPT 권장안, 확정 영향을 포함한다. 여러 충돌을 한꺼번에 묻지 않는다.
- 답변을 받으면 결정 원장과 책임 원본을 갱신하고 다음 충돌로 이동한다. 사용자가 `모두 권장안대로`라고 하면 남은 동등 유형 충돌을 권장안으로 확정한다.
- 전체 저장소를 무조건 정독하지 않는다. 영향 지도를 근거로 범위를 넓히며, 새로운 연결 누락이 발견되면 재라우팅한다.

담당 절차:

- 공격·비판 검증·finding 분류·기획 충돌 큐: `running-adversarial-review-and-refinement`
- 실제 diff·정적·런타임·접근성·성능·회귀 증거: `reviewing-and-validating-project-changes`
- 사용자 결정 인터뷰: `managing-project-intake-and-work-contract: clarify`와 Grill Me 프로토콜

### 4.1 `[연속작업] 진행해` 권한 전환 루프

`CONTINUOUS_WORK_ACTIVE`에서는 현재 승인된 작업 계약의 실행 순서에서 다음 미완료 결과를 자동 선택한다.

```text
현재 승인된 작업 계약
→ 다음 미완료 작업
→ BUILD
→ REVIEW attack → validate-critique
→ finding 분류
   ├─ 범위 안의 기술적 단일 최소 안전 권장안
   │  → 권장안 자동 승인 간주
   │  → BUILD 최소 반영
   │  → REVIEW regression-recheck → decision-report
   │  → 다음 미완료 작업
   ├─ USER_DECISION_REQUIRED
   │  → STOPPED_USER_DECISION
   └─ BLOCKED_UNVERIFIED
      → BLOCKED_UNVERIFIED
→ 완료 기준 충족까지 반복
→ 최종 보고
```

자동 승인 조건은 **현재 승인 범위 + 적대 검토로 유효성이 확인된 기술적 단일 최소 안전안 + 되돌리기 가능한 범위**다. 다음은 자동 승인하지 않는다.

- 프로젝트 코어·플레이어 경험·주요 UX·콘텐츠 의미·비용/범위 우선순위를 새로 바꾸는 결정
- 기존 계약을 넘어서는 새 Goal이나 범위 확대
- 결제, 계정 삭제, 보안·권한 확대 또는 별도 사용자 자격 확인이 필요한 외부 고위험 행위
- `USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`
- 사용자의 중지·범위 변경

짧은 진행 업데이트는 허용하지만 승인 질문으로 사용하지 않는다. `CONTINUOUS_WORK_ACTIVE`는 현재 응답·에이전트 실행 세션의 orchestration이며 scheduler, webhook, 백그라운드 실행 또는 다른 채팅 자동 메시지 전달을 뜻하지 않는다. 상세 기준은 `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`가 책임진다.

## 5. GPT → Codex 구현 라우팅

공용 정본: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

기본 라우팅은 `ON_DEMAND_CODEX_HANDOFF`다.

```text
GPT 평상시 작업
→ 기획·조사·설계
→ 필요한 범위의 Godot 구현 보조·POC·직접 플레이
→ 문제 발견 시 GPT에서 재설계
→ 기획·구현·POC 누적

USER_REQUESTED_CODEX_HANDOFF
→ GPT가 현재 의도·실제 상태·보호 범위·Acceptance Criteria를 Codex 실행 명세로 압축
→ Codex가 실제 GitHub + 프로젝트 파일 + Godot 상태를 직접 조사

CODEX_PREFLIGHT_OPTIONAL
→ 고위험·불확실·다중 의존성일 때만 읽기 전용 Codex Plan
→ 기술 개선·CHANGE_PROPOSAL·사용자 결정 보고

Codex BUILD
→ 지정 Branch에서 실제 구현·리팩터링·테스트·Godot 오류 확인·Commit·Push

GPT REVIEW
→ diff·Commit·테스트·기획 일치·과설계·성능·용량·회귀 적대 검수
→ 패키지 게이트 판정

담당 에이전트
→ 필수 게이트 통과 시 AGENT_MERGE_REQUIRED 실행
```

### GPT 권한

- 기획·조사·설계·비-Godot 파일·GitHub 계약
- 승인 범위의 Godot 사전 제작·POC·코드 초안·구현 보조
- L2 이상이면 마스터 구현계획과 패키지 계약
- `USER_REQUESTED_CODEX_HANDOFF` 시 실행 명세 작성
- 선택적 Codex Plan 결과 반영과 구현 결과 검수

### Codex Plan 권한

`CODEX_PREFLIGHT_OPTIONAL`이 선택된 경우에만 별도 단계로 사용한다.

- 최신 저장소 읽기·분석·제안
- 파일·Commit·Push·PR·Issue 수정 금지

### Codex Build 권한

- 지정 Branch의 Godot 런타임 파일
- 별도 Plan을 생략했어도 구현 전 실제 저장소·프로젝트·Godot 상태 선조사 필수
- 독립 Commit과 지정 Branch Push
- `main` 직접 Push, force push, amend, PR 생성·병합 금지

### 변경 권한

동일한 플레이어 결과와 데이터 계약을 유지하는 구조·성능·안정성·테스트 개선은 기술 변경이다. 프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 저장 호환성 파괴는 `CHANGE_PROPOSAL`로 GPT 단계에 반환한다.

## 6. 구현 패키지와 승인 게이트

L2 이상·다중 의존성 작업은 전체 설계를 마스터 구현계획 하나로 유지하고 구현을 검증 가능한 결과 단위의 패키지로 순차 진행한다. 작은 국소 작업에는 패키지 체계를 형식적으로 강제하지 않는다.

```text
상위 구현 Issue
├─ 패키지별 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이다.

패키지 종료 상태:

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

기본 병합 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다. 별도 사용자 병합 승인은 필요하지 않다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 사용자의 명시적 승인이 완료된 항목은 동일 승인 범위의 구현·검증·PR에 병합 권한도 상속된다. 동일 범위에 대해 추가 확인·재승인·병합 승인 요청 없이, 동일 HEAD·필수 검사·독립 검토 통과, unresolved thread 0, `USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL`·P0/P1 없음이 확인되면 저장소의 허용된 방식으로 병합한다.

`CONTINUOUS_WORK_ACTIVE`는 이 병합 Gate를 삭제하지 않는다. 연속작업 중 다음 패키지로 이동할 수 있어도 각 PR은 기존 exact-head·필수 검사·독립 검토·thread·P0/P1 조건을 그대로 충족해야 한다.

담당 Skill: `maintaining-project-context-and-handoff`의 `implementation-package-handoff`.

## 7. 필수 실행 보고

L1 이상 작업은 최종 보고에 실제 사용한 항목을 남긴다.

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
reason:
work_performed:
result:
evidence:
status: PASS | PARTIAL | FAIL | UNVERIFIED
```

최소 사용자 표시:

```text
사용한 Work Mode·Skill·Skill Mode
→ 사용한 이유
→ 얻은 결과·증거
```

`CONTINUOUS_WORK_ACTIVE`였다면 완료한 작업, 적대 검토 finding, 자동 승인해 반영한 기술 권장안, 회귀 검증, 최종 종료 상태를 함께 보고한다.

중요 후보를 사용하지 않았으면 `trigger 불일치 / 비사용 조건 / 현재 단계 아님 / 도구·입력 없음`을 기록한다. 모든 Skill을 나열하지 않는다.

## 8. 예시

### 기능 구현

```text
Prompt: 전투 결과 저장 기능을 구현해줘.
GPT PLAN/BUILD: 저장 책임·Schema·호환성 설계, 필요한 POC와 실행 명세 준비
사용자: Codex 전환 요청
GPT: USER_REQUESTED_CODEX_HANDOFF 실행 명세 작성
Codex: 실제 Godot 저장 구조·파일·테스트 조사
CODEX_PREFLIGHT_OPTIONAL: 저장 마이그레이션 위험이 크면 읽기 전용 Plan 추가
Codex BUILD: 지정 Branch 구현·테스트·Commit·Push
GPT REVIEW: 저장·불러오기·경계·회귀·기획 일치 검수
담당 에이전트: 필수 게이트 통과 후 병합
```

### 연속작업

```text
Prompt: [연속작업] 진행해
intake: 현재 승인된 계약과 남은 완료 기준 복원 → CONTINUOUS_WORK_ACTIVE
BUILD: 다음 미완료 작업 수행
REVIEW: attack → validate-critique
기술적 단일 최소 안전 finding: 권장안 자동 승인 간주 → BUILD 최소 수정
REVIEW: regression-recheck → 다음 미완료 작업
USER_DECISION_REQUIRED 또는 BLOCKED_UNVERIFIED: 중지
전체 완료: 최종 보고
```

### 구형 파일 정리

```text
Prompt: 오래된 v2·final 파일을 최신화하고 불필요한 파일을 정리해줘.
PLAN: 운영체계 Skill `audit → reconcile-legacy`
BUILD: 승인된 UPDATE·MERGE·ARCHIVE·DELETE 처리
REVIEW: reference-freshness·발행본·복구 경로 검증
```

### GDD 검수

```text
Prompt: GDD를 적대적으로 검토하고 개선해줘.
REVIEW: 영향 범위 지도 → 적대적 공격·비판 검증
→ 기술 검수안 일괄 정리
→ 기획 충돌만 한 번에 하나씩 사용자 확정
BUILD: 승인된 개선안 반영
REVIEW: 모순·누락·구현 가능성·참조·회귀 재검증
```

### Grill Me

```text
Prompt: Grill Me로 프로젝트 방향을 확실히 정해줘.
PLAN: 저장소·대화 조사
→ `clarify` + Grill Me 프로토콜
→ 결정 질문 하나와 권장안
→ 답변을 결정 원장·책임 원본에 반영
→ 차단 질문이 없으면 종료
```