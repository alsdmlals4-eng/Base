---
name: defining-and-verifying-project-core
description: Use when a project needs an explicit, evidence-backed core contract, when existing core statements conflict or are incomplete, or before approving changes that may alter the project's identity, primary value, or core loop.
---

# Defining and Verifying Project Core

## Core principle

프로젝트 코어는 홍보 문구가 아니라 **변경 판단의 기준선**이다. 프로젝트의 목적·핵심 사용자 가치·핵심 경험·핵심 루프·보존 불변조건을 실제 근거와 상태로 연결하고, 코어가 불명확한 상태에서는 AI가 임의로 확정하지 않는다.

코어는 다음 질문에 답해야 한다.

> 무엇을 위해 존재하며, 누구에게 어떤 핵심 가치를 어떤 반복 구조로 제공하고, 무엇이 바뀌면 더 이상 같은 프로젝트가 아니게 되는가?

## Use when

- 신규 프로젝트의 방향과 정체성을 처음 형성한다.
- 여러 기획서·코드·대화에서 프로젝트 목적이나 핵심 경험이 서로 충돌한다.
- 프로젝트 코어가 슬로건 수준이고 변경 판단에 사용할 수 없다.
- 피벗, 대규모 리팩터링, 핵심 시스템 교체, 장르·플랫폼·비즈니스 모델 변경을 검토한다.
- 범위 논쟁에서 무엇을 보호하고 무엇을 교체할 수 있는지 판정해야 한다.
- 적대적 검토가 프로젝트 정체성 또는 핵심 가치에 미치는 영향을 판정해야 한다.
- 새 AI가 저장소만으로 프로젝트의 핵심 방향을 재구성하지 못한다.

## Do not use when

- 오탈자·표현 수정처럼 코어 영향이 없는 L0 작업이다.
- 승인된 코어 계약이 존재하고 이번 변경이 비핵심 범위임이 명확하다.
- 일회성 기술 실험·스파이크로 프로젝트 방향을 확정하지 않는다.
- 사용자만 결정할 수 있는 방향을 저장소 근거만으로 대신 확정하려 한다.

## Required inputs

```yaml
latest_user_direction:
project_agents:
project_start_here:
active_context:
documentation_map:
design_document_registry:
canonical_design_sources: []
actual_product_or_prototype_evidence: []
current_stage_and_gate:
target_users_or_players:
known_constraints: []
protected_decisions: []
open_questions: []
```

## Status model

코어 상태를 반드시 하나로 표시한다.

- `CONFIRMED`: 사용자 승인과 책임 원본이 연결되고 실제 결과와 중대한 충돌이 없다.
- `PROVISIONAL`: 작업 가능한 가설이지만 검증·사용자 확인·실제 결과 중 일부가 부족하다.
- `CONFLICTED`: 둘 이상의 책임 원본이나 실제 동작이 서로 양립하지 않는다.
- `MISSING`: 코어 판단에 필요한 정보가 실질적으로 없다.

`PROVISIONAL`, `CONFLICTED`, `MISSING`을 `CONFIRMED`처럼 사용하지 않는다.

## Project Core Contract

```yaml
project_core:
  status: CONFIRMED/PROVISIONAL/CONFLICTED/MISSING
  purpose:
  target_users_or_players:
  core_problem_or_need:
  core_value:
  core_experience:
  core_loop_or_workflow:
  differentiators: []
  invariants: []
  replaceable_elements: []
  explicit_non_goals: []
  success_signals: []
  failure_signals: []
  evidence:
    user_approval_refs: []
    canonical_source_refs: []
    product_or_test_refs: []
  unresolved_conflicts: []
  change_authority:
  review_triggers: []
```

## Process

### Phase 1 — Source audit

1. 최신 사용자 지시와 프로젝트 우선순위를 확인한다.
2. `DOCUMENTATION_MAP.md`와 Registry에서 프로젝트 목적·핵심 경험·핵심 루프를 책임지는 원본을 찾는다.
3. 실제 프로토타입·코드·데이터·테스트·사용자 피드백에서 현재 제공되는 경험을 확인한다.
4. 다음을 분리한다.
   - 승인된 사실
   - 실제 구현 사실
   - 가정
   - 제안
   - 과거 결정
   - 현재 충돌
5. 과거 대화나 홍보 문구를 현행 책임 원본보다 우선하지 않는다.

### Phase 2 — Candidate extraction

근거에서 코어 후보를 추출한다.

- 프로젝트가 해결하려는 핵심 문제 또는 욕구
- 가장 중요한 사용자·플레이어
- 반복적으로 제공해야 하는 핵심 가치와 경험
- 가치가 발생하는 핵심 루프 또는 작업 흐름
- 유사 프로젝트와 구별되는 핵심 차이
- 유지되어야 할 불변조건
- 교체·축소·삭제 가능한 비핵심 요소
- 명시적으로 하지 않을 것

후보가 둘 이상이면 임의로 합치지 않고 충돌 장부에 기록한다.

### Phase 3 — Contradiction and uncertainty ledger

| ID | 주장 A | 주장 B·실제 상태 | 근거 | 영향 | 해결 권한 | 상태 |
|---|---|---|---|---|---|---|
| CORE-C01 |  |  |  |  | 사용자/책임자/증거 | OPEN/RESOLVED |

다음은 사용자 또는 책임자의 결정 없이는 확정하지 않는다.

- 목표 사용자·플레이어의 우선순위
- 핵심 재미·가치의 우선순위
- 장르·제품 정체성 변경
- 코어 루프 교체
- 중요한 비목표를 목표로 전환

이 경우 `conducting-deep-requirement-interviews`를 선행 또는 병행한다.

### Phase 4 — Core formation

코어를 한 문장으로만 압축하지 말고 `Project Core Contract`를 작성한다.

권장 요약문:

> 이 프로젝트는 `[대상]`이 `[핵심 문제·욕구]`를 해결하도록 `[핵심 경험]`을 제공하며, `[핵심 루프]`를 통해 `[핵심 가치]`를 반복적으로 만든다. `[불변조건]`이 훼손되면 프로젝트 정체성이 바뀐다.

요약문은 계약을 찾기 위한 진입점이며 계약을 대체하지 않는다.

### Phase 5 — Core verification tests

각 항목을 실제 근거와 함께 검사한다.

#### Removal test

해당 요소를 제거해도 프로젝트가 같은 핵심 가치를 제공하는가?

- 그렇다: 비핵심 또는 교체 가능 후보
- 아니다: 코어 후보

#### Replacement test

구현 방식·콘텐츠·UI를 다른 방식으로 바꿔도 핵심 경험이 유지되는가?

- 유지된다: 수단 또는 비핵심
- 무너진다: 코어 불변조건 후보

#### Identity test

이 요소가 바뀌었을 때 사용자와 팀이 같은 프로젝트로 인식할 가능성이 높은가?

#### Dependency test

다른 주요 시스템이 이 요소에 의존하는가, 아니면 단순히 현재 구현이 결합돼 있는가?

기술 의존성을 정체성 코어로 오인하지 않는다.

#### Evidence test

코어 주장이 승인 문서·실제 동작·사용자 반응 중 하나 이상으로 지지되는가?

#### Decision test

이 계약만으로 신규 기능의 `보존 / 조정 / 거부 / 사용자 결정 필요`를 일관되게 판정할 수 있는가?

### Phase 6 — Core impact classification

변경안을 다음으로 분류한다.

- `CORE_PRESERVING`: 코어와 불변조건을 유지하며 수단만 개선한다.
- `CORE_SUPPORTING`: 코어 가치를 강화한다.
- `CORE_RISK`: 코어에 영향을 줄 가능성이 있으나 검증이 부족하다.
- `CORE_CHANGING`: 목적·핵심 경험·핵심 루프·불변조건을 바꾼다.
- `CORE_CONFLICT`: 승인된 코어와 직접 충돌한다.

`CORE_CHANGING`과 `CORE_CONFLICT`는 사용자 승인 없이 구현하지 않는다.

### Phase 7 — Persist and connect

1. 프로젝트의 등록된 Markdown 또는 JSON 책임 원본에 코어 계약을 기록한다.
2. `DESIGN_DOCUMENT_REGISTRY.json`, Documentation Map, Active Context에서 코어 원본을 찾을 수 있게 연결한다.
3. 실행 프롬프트·Plan·Issue의 보호 대상과 완료 기준에 필요한 불변조건만 참조한다.
4. 같은 계약을 여러 문서에 장문 복사하지 않는다.
5. 코어 변경 시 영향 문서·코드·데이터·테스트와 재검증 범위를 갱신한다.

## Interaction with adversarial review

- 일반 문서·코드·UI 개선은 코어 스킬 없이 `running-adversarial-critique-validation-refinement`를 호출할 수 있다.
- 검토 대상이 프로젝트 정체성·핵심 경험·핵심 루프에 영향을 주면 이 스킬을 먼저 호출한다.
- 적대적 검토의 모든 지적을 코어 위반으로 과장하지 않는다.
- 코어는 비판을 막는 방패가 아니라, 유효한 개선과 정체성 훼손을 구분하는 기준이다.

## Output contract

```md
# 프로젝트 코어 확인·형성 보고서

## 상태
- Core status:
- 기준 시점·커밋:

## 프로젝트 코어 계약
- 목적:
- 대상 사용자·플레이어:
- 핵심 문제·욕구:
- 핵심 가치:
- 핵심 경험:
- 핵심 루프·워크플로:
- 차별점:
- 불변조건:
- 교체 가능한 요소:
- 명시적 비목표:

## 근거
- 사용자 승인:
- 책임 원본:
- 실제 제품·테스트:

## 충돌·미확정

## 변경 영향 판정

## 책임 원본 갱신

## 다음 검토 트리거
```

## Definition of Ready

- [ ] 대상 프로젝트와 현재 단계가 식별됐다.
- [ ] 최신 사용자 지시와 책임 원본을 확인했다.
- [ ] 실제 제품·프로토타입 근거를 확인했거나 없음을 표시했다.
- [ ] 사용자만 결정할 내용과 증거로 판정할 내용을 분리했다.

## Definition of Done

- [ ] 코어 상태가 명시됐다.
- [ ] 목적·대상·가치·경험·루프·불변조건·비목표가 연결됐다.
- [ ] 각 핵심 주장에 근거 또는 미검증 표시가 있다.
- [ ] 충돌과 사용자 결정 필요 항목이 숨겨지지 않았다.
- [ ] 책임 원본과 라우팅 문서에서 코어 계약을 찾을 수 있다.
- [ ] 대표 변경안으로 일관된 영향 판정을 재현했다.

## Failure conditions

- 슬로건 한 줄을 코어 계약으로 취급한다.
- 현재 구현된 모든 기능을 코어로 지정한다.
- 기술 부채나 강한 결합을 프로젝트 정체성으로 오인한다.
- 사용자 승인 없이 충돌하는 방향을 하나로 확정한다.
- 비핵심 기능을 보호하기 위해 코어 범위를 계속 확장한다.
- 추상적인 가치만 기록하고 관찰 가능한 핵심 루프·성공 신호를 생략한다.
- 코어 변경을 일반 리팩터링처럼 처리한다.
- 과거 대화의 표현을 현행 책임 원본과 실제 상태보다 우선한다.

## Validation scenarios

1. 강화 게임에서 제작·강화·판매 루프는 제거 시 정체성이 무너지지만 고객 대사 형식은 교체 가능 요소로 분류한다.
2. UI 프레임워크 교체는 핵심 경험이 유지되면 `CORE_PRESERVING`으로 판정한다.
3. 핵심 전투를 제거하고 방치형 경영으로 전환하는 제안은 `CORE_CHANGING`으로 판정하고 사용자 승인을 요구한다.
4. 기획서는 협동 게임이라 쓰지만 실제 프로토타입과 최신 승인 요청은 싱글 플레이면 `CONFLICTED`로 유지한다.

## Learning contract

다음이 발생하면 `skills/SKILL_LEARNING_LOG.md`에 기록하고 스킬 계약을 검토한다.

- 코어 판정이 서로 다른 작업자 사이에서 반복적으로 달라짐
- 코어가 과도하게 넓어 개선을 막음
- 코어가 너무 추상적이라 변경 판정에 실패함
- 실제 사용자 검증이 기존 코어 가정을 반박함
- 코어 변경이 책임 원본·테스트·Handoff에 반영되지 않음

Template: `templates/planning/PROJECT_CORE_CONTRACT.md`
