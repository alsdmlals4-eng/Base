---
name: running-adversarial-critique-validation-refinement
description: Use when any meaningful artifact, design, document, code change, UI, workflow, plan, or operational result needs a structured adversarial critique, independent finding validation, targeted refinement, and regression verification before approval or integration.
---

# Running Adversarial Critique, Validation, and Refinement

## Core principle

산출물을 개선하려면 **비판을 생성하는 역할**, **그 비판의 타당성을 판정하는 역할**, **승인된 문제만 수정하는 역할**, **수정 결과를 독립 검증하는 역할**을 분리한다.

이 스킬은 프로젝트 코어 전용이 아니다. 기획·문서·코드·데이터·UI·아트·사운드·QA·프로덕션·분석·운영 등 모든 분야에서 사용할 수 있는 범용 Foundation 검토 절차다.

> 레드팀은 최대한 공격하고, 판정자는 그 비판마저 의심하며, 개선자는 검증된 문제만 최소 변경으로 수정하고, 재검증자는 원래 문제와 새 회귀를 다시 확인한다.

## Use when

- 초안·기획·명세·코드·데이터·UI·아트·운영 절차의 품질을 체계적으로 높여야 한다.
- 중요한 게이트, 승인, 통합, 배포 전에 실패 조건을 적극적으로 찾아야 한다.
- 기존 검토가 칭찬·문장 다듬기에 치우쳐 실제 결함을 놓친다.
- 여러 대안 중 취향이 아니라 근거와 실패 위험으로 선택해야 한다.
- 구현 완료 주장과 실제 결과가 일치하는지 공격적으로 확인해야 한다.
- 반복되는 결함을 비평→판정→개선→회귀검증으로 닫아야 한다.
- 외부 AI가 아닌 내부 작업물도 독립적인 검토가 필요하다.

## Do not use when

- 오탈자·명백한 L0 수정이다.
- 아직 평가할 산출물·목표·기준이 없는 자유 브레인스토밍 단계다.
- 단순히 부정적인 의견을 많이 생성하는 것이 목적이다.
- 보안 침투 테스트, 법률 검토, 의료 검토처럼 별도 자격·도구·전문 절차가 필요한 작업을 이 스킬만으로 대체하려 한다.
- 외부 AI 산출물의 출처·허위 경로·격리 브랜치 검수가 핵심이면 `reviewing-external-ai-drafts`의 고유 절차를 생략하려 한다.

## Required inputs

```yaml
review_target:
review_target_type:
baseline_ref:
objective:
user_or_player_value:
acceptance_criteria: []
canonical_sources: []
actual_evidence: []
protected_properties: []
out_of_scope: []
known_constraints: []
verification_methods: []
risk_level: low/medium/high/critical
project_core_ref:
required_approvals: []
```

입력이 부족하면 결함을 발명하지 않는다. 확인 가능한 사실, 가정, 제안, 미검증을 분리한다.

## Review modes

### Lightweight

작은 L1 산출물에 사용한다.

```text
비평 1회 → 지적 판정 → 승인된 수정 → 핵심 회귀 확인
```

### Standard

L2 또는 여러 영역에 영향을 주는 일반 작업에 사용한다.

```text
기준선 고정 → 적대적 비평 → 독립 판정 → 수정 계획 → 개선 → 독립 재검증
```

### Gate

L3 이상, 배포·병합·마일스톤·핵심 구조 변경에 사용한다.

```text
증거 지도 → 다중 관점 공격 → 재현·심각도 판정 → 승인 게이트
→ 단계별 개선 → 정상·경계·회귀·실패 경로 검증 → 잔여 위험 승인
```

검토 강도는 위험에 비례해야 하며, 모든 작업에 Gate 모드를 강제하지 않는다.

## Select review lenses

현재 대상에 필요한 관점만 선택한다. 모든 관점을 무조건 호출하지 않는다.

| 분야 | 적대적 질문 |
|---|---|
| 목적·기획 | 해결하려는 문제와 산출물이 어긋나는가? 숨은 전제와 범위 팽창이 있는가? |
| 게임 디자인 | 핵심 재미가 반복 피로·악용·경제 붕괴·무의미한 선택으로 무너지는가? |
| 내러티브 | 인과·동기·규칙·시점·톤이 충돌하거나 플레이 경험을 방해하는가? |
| UX·UI·접근성 | 사용자가 다음 행동과 결과를 이해하는가? 오류·빈 상태·접근성에서 깨지는가? |
| 엔지니어링 | 정상 경로만 맞고 오류·경계·동시성·성능·보안·호환성에서 실패하는가? |
| 데이터·저장 | 스키마·ID·마이그레이션·재시도·중복·손상에서 문제가 생기는가? |
| 아트·테크니컬 아트 | 목적 있는 차이를 결함으로 오인하는가? 실제 엔진·해상도·파이프라인에서 유지되는가? |
| 사운드 | 정보 전달·반복 피로·우선순위·플랫폼 출력·접근성에서 실패하는가? |
| QA | 증상을 실제로 재현하는가? 테스트가 구현을 확인하는 척만 하는가? |
| 프로덕션·PM | 의존성·책임·완료 정의·승인·일정·복구 계획이 빠졌는가? |
| 분석·유저리서치 | 지표 정의·표본·인과 추론·세그먼트·계측이 결론을 지지하는가? |
| 문서·운영 | 책임 원본·경로·상태·실제 실행 결과가 일치하는가? |

## Role separation

가능하면 서로 다른 작업자·에이전트·컨텍스트로 역할을 분리한다. 같은 AI가 수행해야 하면 각 단계에서 이전 역할의 결론을 정당화하지 않도록 입력과 출력 계약을 분리한다.

- `Critic`: 실패 근거와 공격 시나리오를 찾는다.
- `Judge`: 각 지적의 근거·재현성·관련성·비용 대비 가치를 판정한다.
- `Refiner`: 승인된 지적만 최소 변경으로 해결한다.
- `Verifier`: 수정자가 제시한 설명이 아니라 실제 결과를 재검증한다.

한 역할의 출력은 다음 역할의 **입력**일 뿐, 자동 승인된 사실이 아니다.

## Process

### Phase 0 — Freeze the baseline

1. 검토 대상의 파일·문서·브랜치·커밋·렌더·버전을 고정한다.
2. 목표, 완료 기준, 보호할 동작, 제외 범위를 기록한다.
3. 책임 원본과 실제 결과를 확인한다.
4. 프로젝트 코어가 존재하면 관련 불변조건만 가져온다.
5. 코어가 없더라도 일반 개선은 진행할 수 있다. 다만 정체성·핵심 경험을 바꾸는 판단이 필요하면 `defining-and-verifying-project-core`를 먼저 호출한다.

### Phase 1 — Build an evidence map

| 주장·요구 | 근거 | 실제 상태 | 검증 방법 | 상태 |
|---|---|---|---|---|
|  |  |  |  | CONFIRMED/ASSUMED/PROPOSED/UNVERIFIED/CONFLICTED |

다음을 혼합하지 않는다.

- 사용자의 의도
- 승인된 요구사항
- 실제 구현·실행 사실
- 외부 출처
- 추정
- 개선 제안

### Phase 2 — Adversarial critique

산출물이 실패했다고 가정하고 실패를 일으키는 가장 강한 근거를 찾는다.

각 finding은 다음 형식을 사용한다.

```yaml
finding_id: ADV-001
lens:
claim:
evidence:
failure_scenario:
affected_requirement_or_value:
impact:
likelihood: high/medium/low/unknown
severity: critical/high/medium/low
confidence: high/medium/low
reproduction_or_observation:
proposed_direction:
```

Critic 규칙:

- 칭찬과 장점 요약은 생략하고 결함 탐색에 집중한다.
- 단순 취향을 요구사항 위반처럼 표현하지 않는다.
- 근거 없는 가능성을 확정 결함으로 쓰지 않는다.
- 동일 원인의 증상을 여러 finding으로 부풀리지 않는다.
- 실제 파일·실행·렌더를 확인할 수 있으면 설명보다 증거를 우선한다.
- 사용자 의도와 프로젝트 고유 선택을 보편 규칙으로 공격하지 않는다.
- 비판의 수보다 영향과 재현 가능성을 우선한다.

### Phase 3 — Independent finding validation

Judge는 Critic의 결론을 그대로 받아들이지 않는다. 각 finding을 다음 기준으로 검증한다.

1. 승인된 목표·요구·책임 원본과 관련 있는가?
2. 실제 근거나 재현 가능한 실패 시나리오가 있는가?
3. 프로젝트 고유 의도와 단순 취향 차이를 구분했는가?
4. 발생 가능성과 영향이 과장되지 않았는가?
5. 수정 효과가 비용·복잡도·새 회귀 위험보다 큰가?
6. 다른 finding과 원인이 중복되는가?
7. 현재 단계에서 해결해야 하는가?

판정:

- `MUST_FIX`: 승인·통합·배포 전에 반드시 해결한다.
- `SHOULD_FIX`: 비용 대비 효과가 높고 현재 범위에서 수정 권장이다.
- `DEFER`: 유효하지만 현재 단계·범위·의존성 때문에 후속 작업으로 분리한다.
- `REJECT`: 근거 부족, 비관련, 취향, 중복, 잘못된 전제로 기각한다.
- `NEEDS_DECISION`: 사용자·책임자만 결정할 수 있어 자동 수정하지 않는다.

판정 기록:

```yaml
finding_id:
decision:
reason:
validated_evidence:
required_approval:
refinement_scope:
regression_risks: []
```

### Phase 4 — Build the refinement plan

`MUST_FIX`와 승인된 `SHOULD_FIX`만 구현 계획에 넣는다.

- finding과 변경 항목을 1:1 또는 명시적 N:1로 연결한다.
- 최소 diff를 우선한다.
- 프로젝트 코어·보호 동작·공개 인터페이스를 유지한다.
- 불필요한 기능 추가와 기회성 리팩터링을 분리한다.
- `DEFER`, `REJECT`, `NEEDS_DECISION`을 몰래 구현하지 않는다.
- 변경마다 검증 방법과 회귀 위험을 미리 기록한다.

### Phase 5 — Refine

1. 승인된 범위만 수정한다.
2. 기존 사용자 변경과 고유 결정을 보존한다.
3. 수정 중 새 요구가 발견되면 범위를 자동 확대하지 않는다.
4. 수정 전후 diff·렌더·행동 차이를 남긴다.
5. 설명이나 문서만 바꿔 실제 결함을 숨기지 않는다.

### Phase 6 — Independent re-verification

Verifier는 다음을 독립적으로 확인한다.

- 원래 failure scenario가 더 이상 재현되지 않는가?
- 승인된 완료 기준을 실제 결과가 충족하는가?
- 정상·경계·오류·회귀 경로를 확인했는가?
- 코어 불변조건과 보호 동작이 유지되는가?
- 수정으로 새 결함·복잡도·성능 저하가 생기지 않았는가?
- 문서·상태·완료 보고가 실제 결과와 일치하는가?

수정자가 작성한 “해결됨” 설명을 검증 증거로 사용하지 않는다.

### Phase 7 — Bounded loop and stop conditions

기본 반복 한도:

- Lightweight: 최대 1회 개선
- Standard: 최대 2회 개선
- Gate: 최대 3회 개선, 이후 책임자 결정

다음이면 반복을 종료한다.

- 모든 `MUST_FIX`가 검증됐다.
- 남은 finding이 `DEFER`, `REJECT`, `NEEDS_DECISION`뿐이다.
- 추가 개선의 기대 가치보다 비용·회귀 위험이 크다.
- 새로운 근거 없이 표현만 바꾼 동일 비판이 반복된다.
- 사용자 승인이나 외부 의존성이 필요하다.

끝없이 결함을 생성하는 것을 품질 향상으로 오인하지 않는다.

## Severity guide

| 심각도 | 기준 |
|---|---|
| critical | 핵심 데이터 손실, 보안·안전 문제, 프로젝트 코어 붕괴, 주요 배포 차단 |
| high | 핵심 기능 실패, 다수 사용자 경험 손상, 중요한 요구 위반, 복구 비용 큼 |
| medium | 부분 기능·이해·품질 저하, 우회 가능하지만 반복 영향 존재 |
| low | 제한적 불편, 표현·일관성 문제, 현재 게이트를 막지 않음 |

심각도와 수정 우선순위는 동일하지 않다. 발생 가능성, 현재 단계, 비용, 의존성을 함께 판정한다.

## Output contract

```md
# 적대적 비평–검증–개선 보고서

## 검토 기준선
- 대상·버전·커밋:
- 목적·완료 기준:
- 책임 원본·실제 증거:
- 보호 대상·제외 범위:
- 적용한 검토 관점:

## 적대적 비평 Findings
| ID | 문제 | 근거·재현 | 영향 | 가능성 | 심각도 | 신뢰도 |
|---|---|---|---|---|---|---|

## 지적 검증
| ID | 판정 | 근거 | 승인 필요 | 수정 범위 |
|---|---|---|---|---|

## 개선 계획과 실제 변경
| Finding | 변경 | 변경하지 않은 것 | 검증 |
|---|---|---|---|

## 독립 재검증
- 정상 경로:
- 경계·오류 경로:
- 회귀:
- 코어·보호 동작:

## 잔여 위험·보류·사용자 결정

## 최종 판정
- APPROVE / APPROVE_WITH_RISK / CHANGES_REQUIRED / BLOCKED / UNVERIFIED
```

## Automatic rejection of findings

다음 finding은 판정 단계에서 기각하거나 다시 작성한다.

- 실제 요구·근거 없이 “보통 이렇게 한다”만 제시한다.
- 개인 취향을 객관적 결함으로 표현한다.
- 재현·관찰 경로가 전혀 없으면서 치명적이라고 단정한다.
- 프로젝트 코어와 고유 아트·게임 방향을 무시한다.
- 이미 같은 원인으로 등록된 finding을 표현만 바꿔 반복한다.
- 수정안이 원래 문제보다 큰 범위와 위험을 만든다.
- 테스트·렌더·실제 실행 없이 완료를 주장한다.
- 사용자의 승인 권한이 필요한 결정을 자동 수정 대상으로 둔다.

## Relationship with other skills

- `defining-and-verifying-project-core`: 정체성·핵심 경험·핵심 루프 영향이 있을 때 기준선을 형성한다.
- `reviewing-external-ai-drafts`: 외부 모델·계약자·병렬 에이전트 결과의 출처·범위·환각 경로·격리 diff를 추가 검수한다.
- `auditing-and-refining-ui-art`: Godot·Web UI의 목적 있는 디자인, 실제 렌더, A~E 영역 개선이라는 분야 고유 절차를 담당한다.
- `verifying-game-project-operating-system`: 운영체계 전체의 구조·발행·콜드 스타트 Health Review를 담당한다.
- 분야별 스킬: 각 분야의 고유 품질 기준과 실제 검증 방법을 제공한다.

이 스킬은 분야 스킬을 대체하지 않고, 분야별 근거를 **공통 비평–판정–개선–재검증 루프**로 연결한다.

## Definition of Ready

- [ ] 검토 대상과 기준 버전이 고정됐다.
- [ ] 목적·완료 기준·보호 대상·제외 범위가 있다.
- [ ] 필요한 책임 원본과 실제 증거를 확인했다.
- [ ] 위험에 맞는 검토 모드와 최소 관점을 선택했다.
- [ ] 코어 영향 여부와 사용자 승인 필요 여부를 판정했다.

## Definition of Done

- [ ] 모든 finding에 근거·실패 시나리오·심각도·신뢰도가 있다.
- [ ] 각 finding이 독립 판정됐다.
- [ ] 승인된 finding만 수정됐다.
- [ ] 수정 전후와 검증 증거가 연결됐다.
- [ ] 정상·경계·오류·회귀 경로를 위험 수준에 맞게 확인했다.
- [ ] 잔여 위험·보류·사용자 결정이 숨겨지지 않았다.
- [ ] 최종 판정이 실제 증거와 일치한다.

## Failure conditions

- 비판과 개선을 한 단계에서 섞어 최초 결론을 정당화한다.
- Critic의 모든 지적을 검증 없이 반영한다.
- 비판 개수를 품질 척도로 사용한다.
- 사소한 표현 문제를 치명적 위험과 같은 우선순위로 처리한다.
- 프로젝트 고유 선택과 단순 취향을 결함으로 판정한다.
- 수정 범위를 넓혀 새로운 기능·리팩터링을 몰래 포함한다.
- 회귀 검증 없이 “개선됨”을 선언한다.
- 같은 AI가 역할만 이름 바꾸고 동일 근거를 반복한다.
- 종료 조건 없이 무한 반복한다.

## Validation scenarios

1. 게임 경제 기획에서 무한 자원 악용 finding은 재현 가능한 수치 경로가 있으면 `MUST_FIX`, 단순히 보상이 후하다는 취향은 `REJECT`한다.
2. 코드 리뷰에서 정상 테스트만 통과하고 저장 마이그레이션이 깨지면 `high` finding으로 판정하고 실제 이전 데이터 fixture로 재검증한다.
3. UI 검토에서 의도적인 비대칭을 일반 대칭 원칙으로 공격하면 프로젝트 아트 방향 근거를 확인해 `REJECT`한다.
4. 문서 검토에서 책임 원본과 실제 경로가 다르면 문장 미학보다 추적성 결함을 우선 수정한다.
5. 일반 문구 개선처럼 코어와 무관한 작업은 프로젝트 코어 스킬 없이 Lightweight 모드로 수행한다.

## Learning contract

다음이 발생하면 `skills/SKILL_LEARNING_LOG.md`에 기록하고 스킬 계약을 검토한다.

- 거짓 양성 finding이 반복됨
- 중대한 결함이 특정 관점에서 반복 누락됨
- 판정 없이 Critic 지적이 자동 반영됨
- 개선 후 같은 결함 또는 새로운 회귀가 반복됨
- 검토 비용이 위험 대비 과도함
- 분야 스킬과 공통 루프의 책임이 중복됨
- 종료 조건이 작동하지 않아 비평이 무한 반복됨

Template: `templates/review/ADVERSARIAL_CRITIQUE_VALIDATION_REFINEMENT.md`
