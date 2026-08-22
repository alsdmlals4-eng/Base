# Context-Driven Reuse Synthesis

이 문서는 기존 `REVERSE_ENGINEERING_REUSE_PIPELINE.md`의 두 번째 candidate-origin 경로를 정의한다. 목적은 실제 반복 구현·실패 기록이나 외부 benchmark가 아직 없어도 **프로젝트 정본, 승인 계획, roadmap, 책임 경계와 예상 반복비용을 읽어 더 나은 공용 구조를 가설로 설계**할 수 있게 하는 것이다.

```text
SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS
CONTEXT_SYNTHESIS_CAN_DEFINE_CONTRACT
CONTEXT_SYNTHESIS_IS_NOT_VALIDATION
EVIDENCE_REQUIRED_FOR_PROMOTION
VAGUE_FUTURE_USE_IS_NOT_A_TRIGGER
```

## 1. Candidate origin

```yaml
candidate_origin: EVIDENCE_DERIVED | CONTEXT_SYNTHESIZED | HYBRID
maturity: HYPOTHESIS | MODULE_CONTRACT_DEFINED | REFERENCE_IMPLEMENTATION_EXISTS | PROJECT_ADAPTER_VERIFIED | PROJECT_MERGED
validation_state: VALIDATION_NOT_RUN | FOCUSED_VERIFIED | MULTI_CONTEXT_VERIFIED | PLAYER_OR_USER_VERIFIED
```

- `EVIDENCE_DERIVED`: 실제 코드, 반복 병목, benchmark, 실패, 운영 기록에서 반복 불변원리를 추출한다.
- `CONTEXT_SYNTHESIZED`: 아직 반복 증거가 없어도 현재 구조와 승인된 미래 consumer를 바탕으로 더 작은 계약을 설계한다.
- `HYBRID`: context hypothesis를 외부/내부 evidence로 공격하거나 evidence에서 얻은 패턴을 프로젝트 구조와 새로 재조합한다.

origin은 아이디어가 어디서 시작됐는지를 말한다. maturity는 구현/채택 수준, validation은 그 수준을 뒷받침하는 직접 증거를 말한다. 세 축을 합쳐서 하나의 모호한 `완료` 상태로 만들지 않는다.

## 2. Context synthesis trigger

다음 신호 중 하나 이상이 현재 정본에서 구체적으로 식별될 때만 candidate를 만든다.

1. `PLANNED_MULTI_CONSUMER` — roadmap 또는 승인 계획에 둘 이상의 실제 consumer가 예정돼 있다.
2. `PREDICTED_REPEAT_COST` — 현재 설계대로 확장하면 같은 코드·데이터 입력·수작업이 반복될 구조다.
3. `ONE_INPUT_MULTI_OUTPUT` — 같은 사실을 여러 문서·화면·검증기에 다시 입력하고 있다.
4. `RESPONSIBILITY_TANGLE` — 독립적으로 변해야 하는 책임이 한 owner에 과도하게 결합돼 있다.
5. `COMPOSITION_OPPORTUNITY` — 여러 기존 시스템을 작은 neutral primitive + thin adapter로 단순화할 수 있다.
6. `CROSS_PROJECT_PLAN_PATTERN` — 구현 전이라도 서로 다른 프로젝트의 승인 계획에 같은 shape가 나타난다.
7. `USER_REUSE_INTENT` — 사용자가 장기 재사용·모듈화·공용 구조 설계를 명시적으로 요구했다.

`VAGUE_FUTURE_USE_IS_NOT_A_TRIGGER`: “언젠가 쓸 수도 있다”, “보통 있으면 좋다”, “유명한 패턴이다”만으로 durable module을 만들지 않는다.

## 3. Required context packet

Context-Synthesized 또는 Hybrid 후보는 최소 다음을 기록한다.

```yaml
candidate_id:
candidate_origin: CONTEXT_SYNTHESIZED | HYBRID
context_basis:
planned_consumers: []
predicted_repeat_or_tangle:
why_now:
existing_solution_search:
proposed_contract:
expected_value:
likely_failure_modes: []
falsification_test:
smallest_pilot:
rollback_or_discard_condition:
maturity: HYPOTHESIS | MODULE_CONTRACT_DEFINED
validation_state: VALIDATION_NOT_RUN
```

`context_basis`는 현재 정본·승인 roadmap·실제 owner 구조처럼 재확인 가능한 내부 근거를 가리킨다. `planned_consumers`는 이름을 붙일 수 있는 실제 consumer여야 하며 막연한 “다른 프로젝트들”은 인정하지 않는다.

## 4. Falsification and smallest pilot

Context hypothesis는 좋은 설명만으로 유지하지 않는다.

`falsification_test`는 최소 하나의 실패 조건을 적는다. 예:

- 두 번째 consumer에서 예외 분기가 core보다 커진다.
- 공통 input보다 project-specific input이 더 많다.
- 동일 정보를 한 번 입력하는 대신 adapter maintenance가 더 비싸진다.
- neutral primitive가 프로젝트 core decision을 약화시킨다.
- human edit/QA total effort가 기존 방식보다 줄지 않는다.

`smallest_pilot`은 위 가설을 확인할 수 있는 가장 작은 실제 소비 경로다. 새 GUI, broad Skill, global manager, 새로운 SaaS를 먼저 만들지 않는다.

```text
HYPOTHESIS
→ EXISTING_SOLUTION_FIRST
→ SMALLEST_PILOT
→ FALSIFICATION_CHECK
→ KEEP | NARROW | PROJECT_ONLY | DISCARD
```

## 5. Existing Solution First

Context-driven 설계도 `Existing Solution First`를 우회하지 않는다.

```text
project-local existing owner
→ Base / other-project existing module
→ official/open-source/licensed solution
→ adapter/composition
→ only remaining gap may define a new contract
```

기존 owner 설정이나 thin adapter로 해결되면 새 module/Tool/Skill을 만들지 않는다. 새 후보는 owner를 대체하는 것이 아니라 owner가 소비할 수 있는 bounded contract여야 한다.

## 6. Promotion ceiling

```text
CONTEXT_SYNTHESIS_IS_NOT_VALIDATION
REFERENCE_IMPLEMENTATION_IS_NOT_PROJECT_ADOPTION
PROJECT_ADAPTER_VERIFIED_IS_NOT_PLAYER_VALUE_PASS
EVIDENCE_REQUIRED_FOR_PROMOTION
```

- Context만으로 `HYPOTHESIS` 또는 `MODULE_CONTRACT_DEFINED`까지 갈 수 있다.
- `REFERENCE_IMPLEMENTATION_EXISTS`는 실제 Base 구현/테스트가 있어야 한다.
- `PROJECT_ADAPTER_VERIFIED`는 실제 project adapter 또는 project-owned consumer evidence가 있어야 한다.
- `PROJECT_MERGED`는 해당 프로젝트 main에 실제 반영된 증거가 있어야 한다.
- 재미, 몰입, UX 품질, visual quality는 해당 human/player/runtime evidence 없이 승격하지 않는다.
- `BASE_ACTIVE_METHOD` 성격의 운영 승격은 실제 반복 소비와 현재 owner 승인/검증이 필요하다.

## 7. Evidence can arrive after invention

벤치마크는 발명 허가증이 아니라 비교·공격 도구다. Context-Synthesized 후보를 먼저 만든 뒤 외부 사례·실패 사례를 찾아 다음을 확인할 수 있다.

- 비슷한 구조가 실제로 어떤 tradeoff를 만들었는가.
- 우리가 놓친 failure/recovery가 있는가.
- direct licensed reuse가 새 구현보다 나은가.
- 후보의 범위를 줄여야 하는가.

이 경우 origin은 `HYBRID`로 바꿀 수 있지만 validation state는 직접 실행 증거가 생기기 전까지 자동 상승하지 않는다.

## 8. YAGNI and rollback gate

다음 중 하나면 기본 판정은 `DEFER` 또는 `DISCARD`다.

- 실명 가능한 consumer가 1개뿐이고 두 번째 consumer 계획도 없다.
- project-specific 예외가 neutral contract보다 크다.
- 기존 owner의 단순 함수/데이터 schema로 충분하다.
- 새로운 dependency·권한·유료 서비스가 예상 절감보다 크다.
- failure mode를 관찰할 방법이 없다.
- rollback 또는 discard 조건을 정의할 수 없다.

`rollback_or_discard_condition`이 발동하면 module ID를 보존하기 위해 불필요한 구현을 유지하지 않는다. project-only pattern 또는 research note로 낮출 수 있다.

## 9. Output and authority

Context synthesis 결과는 기존 Reuse Pipeline의 `REUSABLE_CONTRACT_EXTRACTION → EXISTING_SOLUTION_FIRST → PROJECT_FIT_AND_NOVELTY_DELTA → REUSE_OWNER_ROUTING`으로 합류한다.

```text
context candidate != project canon
context candidate != runtime proof
context candidate != asset approval
context candidate != new Skill approval
context candidate != player-value PASS
```

실제 프로젝트 적용과 Base 공용 승격은 각 기존 owner가 책임진다.
