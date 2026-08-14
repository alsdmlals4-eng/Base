# Socratic Questioning Review Lenses

## 목적과 권한

`Socratic Review Lens`는 `running-adversarial-review-and-refinement`의 질문 구조를 강화하는 선택형 검토 reference다. 적대적 검토의 Finding 판정, 분야 작성 책임, 사용자 결정권을 소유하지 않는다.

Foundation for Critical Thinking의 Richard Paul·Linda Elder 계열 Socratic questioning 분류에서 반복되는 clarification, assumptions, reasons/evidence, viewpoints, implications/consequences, questions about the question을 Base의 적대적 검토에 맞게 변형한다. 교육용 대화 절차 전체를 복제하지 않고, 검토자가 자신의 주장·비판·근거까지 재검증하는 데 필요한 질문 구조만 채택한다.

## 선택 규칙

- 현재 Requirement·주장·Finding·위험과 직접 **관련된 Lens만** 선택한다.
- 모든 Lens를 채우기 위해 **가짜 Finding**을 만들지 않는다.
- L0 오탈자·명백한 기계 수정·동일 입력 검사 재실행에는 기본 적용하지 않는다.
- 질문 후보가 생기면 먼저 **저장소·정본·실제 구현·도구**로 답할 수 있는지 조사한다.
- 확인 가능한 사실을 사용자 인터뷰로 대체하지 않는다. **사용자 질문은 마지막 수단**이다.
- 질문의 답이 결론·완료·코어에 영향을 주지 않으면 `NOT_APPLICABLE`, `DEFER`, `REJECTED_CRITIQUE` 중 현재 계약에 맞는 상태로 정리한다.
- 필요한 기술 증거가 없어 판정할 수 없으면 `BLOCKED_UNVERIFIED`와 확인 조건을 기록한다.
- 둘 이상의 유효한 선택이 프로젝트 코어·중요 기획·방향성을 다르게 만들 때만 `USER_DECISION_REQUIRED`로 올리고, 기존 intake/Grill Me 규칙에 따라 가장 중요한 사용자 질문 하나를 사용한다.

## Clarification

### 목적

주장·용어·Requirement·완료 기준의 의미를 고정한 뒤 공격한다. 애매한 표현을 임의 해석해 결함으로 확정하지 않는다.

### attack prompts

- 정확히 무엇을 주장하고 있는가?
- 이 용어는 현재 정본에서 어떤 의미인가?
- 성공·실패·완료를 가르는 관찰 가능한 기준은 무엇인가?
- 서로 다른 문장이 같은 대상을 가리키는가, 아니면 별도 요구인가?

### validate rule

정본·코드·데이터·테스트·승인 Decision에서 의미를 복원할 수 있으면 그 증거를 사용한다. 복원 불가능하지만 결론에 중요하면 `BLOCKED_UNVERIFIED` 또는 `USER_DECISION_REQUIRED` 경계를 적용한다.

### non-escalation

파일·Schema·Decision·실제 구현이 이미 답을 제공하면 사용자에게 다시 묻지 않는다.

## Assumptions

### 목적

결론이 성립하려면 사실이어야 하는 숨은 전제·의존성·환경 조건을 드러낸다.

### attack prompts

- 무엇이 사실이라고 가정해야 이 결론이 성립하는가?
- 검증 없이 정상이라고 간주한 플랫폼·도구·데이터·권한·사용자 행동은 무엇인가?
- 사용자안과 AI 최초안에 서로 다른 가정을 적용하고 있지 않은가?
- 과거 상태나 외부 사례를 현재 정본으로 착각하고 있지 않은가?

### validate rule

가정을 실제 증거와 분리한다. 가정이 틀려도 결론이 유지되면 핵심 Finding으로 승격하지 않는다. 가정이 핵심이고 증거가 없으면 `BLOCKED_UNVERIFIED`다.

### non-escalation

추측을 새 사실로 만들지 않으며, 이미 저장소·정본에서 확인되는 전제는 사용자 질문으로 올리지 않는다.

## Reasons / Evidence

### 목적

주장·비판·권장안과 실제 근거의 연결을 검사한다.

### attack prompts

- 이 결론을 지지하는 정본·실제 diff·코드·데이터·테스트는 무엇인가?
- 같은 수준 이상의 반증은 무엇인가?
- 문서에 테스트가 정의됐다는 사실을 실제 실행 성공으로 오인하고 있지 않은가?
- 외부 근거가 필요하다면 공식·1차 출처와 현재 환경에 맞는가?

### validate rule

증거의 권한·직접성·최신성·실행 여부를 비교한다. 실행하지 않은 CI·런타임·렌더·사람 검증을 통과로 올리지 않는다.

### non-escalation

증거 부족은 자신감 있는 추정으로 메우지 않는다. 판정에 필요한 근거가 없으면 `BLOCKED_UNVERIFIED`와 확인 조건을 남긴다.

## Viewpoints

### 목적

현재 선호안에 갇히지 않고 실질적인 대안·이해관계자 관점을 검토한다.

### attack prompts

- 사용자안과 AI 최초안 외에 실제로 가능한 대안이 있는가?
- 플레이어·개발·QA·운영·접근성 관점에서 비용과 가치가 어떻게 달라지는가?
- 반대 관점이 새 사실을 제공하는가, 아니면 단순 취향 차이인가?
- 다른 관점이 프로젝트 코어 또는 완료 기준을 더 잘 보존하는가?

### validate rule

대안은 동일한 사실성·영향·비용·코어·호환성·되돌리기 기준으로 비교한다. 존재하지 않는 대안을 만들어 균형을 연출하지 않는다.

### non-escalation

기술적으로 한 선택이 명백히 우세하면 불필요한 사용자 투표를 만들지 않는다. 중요 방향이 실제로 갈릴 때만 `USER_DECISION_REQUIRED`다.

## Implications / Consequences

### 목적

결론을 적용했을 때의 정상 경로·실패 경로·복구·회귀·장기 유지·롤백 영향을 추적한다.

### attack prompts

- 이 결론을 적용하면 플레이어/사용자 행동과 가치가 실제로 어떻게 달라지는가?
- 정상 경로 외에 실패·취소·재시도·복구 경로는 무엇이 바뀌는가?
- untouched consumer, Template, Test, 파생본, 호환성에 어떤 파급이 생기는가?
- 되돌려야 할 때 데이터·정본·호환성을 안전하게 복원할 수 있는가?

### validate rule

예상 파급과 실제 dependency/consumer를 분리한다. 영향이 추정뿐이면 미검증으로 남기고, 실행·참조 증거가 있으면 Finding에 연결한다.

### regression-recheck

수정 뒤 같은 Consequence 질문을 다시 사용해 기존 장점·정상 경로·코어·복구·롤백에 새 회귀가 생기지 않았는지 확인한다.

## Meta-question

### 목적

제기한 질문과 비판 자체가 중요한지, 현재 범위인지, 실제 결론을 바꾸는지 검증해 질문 폭주와 반대를 위한 반대를 줄인다.

### validate prompts

- 왜 이 질문이 현재 Requirement에 중요한가?
- **답이 달라지면 실제 결정도 달라지는가?**
- 이 비판은 검증 가능한 실패인가, 취향·중복·범위 밖 요구인가?
- 이미 다른 Lens·Finding·정본이 같은 문제를 해결하고 있지 않은가?
- 질문을 사용자에게 올리기 전에 저장소·정본·실제 구현·도구로 답할 수 있는가?

### decision rule

- 결론을 바꾸지 않고 실질 위험도 없으면 `REJECTED_CRITIQUE` 또는 `NOT_APPLICABLE`로 닫는다.
- 유효하지만 현재 범위/비용상 뒤로 미루면 `DEFER`한다.
- 필요한 증거가 없어 중요 판정을 못 하면 `BLOCKED_UNVERIFIED`다.
- 둘 이상의 유효한 중요 방향이 남을 때만 `USER_DECISION_REQUIRED`로 올린다.

## 실행 단계 연결

```text
attack
→ Clarification
→ Assumptions
→ Reasons / Evidence
→ Viewpoints
→ Implications / Consequences

validate-critique
→ Reasons / Evidence 재검증
→ Assumptions 재검증
→ Meta-question

regression-recheck
→ Implications / Consequences 재검사
→ 필요한 Meta-question 재검사
```

이 순서는 여섯 Lens를 매번 모두 실행하라는 의미가 아니다. 현재 위험과 직접 관련된 Lens만 고른다.

## Finding 연결 예시

```yaml
finding_id: AR-SQ-001
lens: Reasons / Evidence
claim: "새 구조가 기존 테스트를 모두 보존한다"
evidence: "집중 테스트만 실행됨; 전체 회귀는 미실행"
severity: BLOCKED_UNVERIFIED
status: VALIDATED
reason: "전체 보존 주장을 뒷받침할 실행 증거가 없음"
verification: "required regression suite를 exact head에서 실행"
```

Socratic 질문 자체는 Finding이 아니다. 질문을 통해 검증된 실패·충돌·증거 공백만 기존 Finding contract로 승격한다.

## 외부 근거

- Foundation for Critical Thinking, Richard Paul & Linda Elder, *The Thinker's Guide to the Art of Socratic Questioning*: https://www.criticalthinking.org/TGS_files/SocraticQuestioning2006.pdf
- Foundation for Critical Thinking, *The Role of Socratic Questioning in Thinking, Teaching, and Learning*: https://www.criticalthinking.org/pages/the-role-of-socratic-questioning-in-thinking-teaching-learning/522
