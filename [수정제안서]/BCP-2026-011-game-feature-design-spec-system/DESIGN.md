# Game Feature Design Spec System — Design

## 1. 목표

Base의 기존 기획·문서·검증 책임을 유지하면서, **PoC를 통과한 주요 기능을 실제 제작 가능한 수준으로 상세화하는 공용 기능 설계 계층**을 추가한다.

이 설계는 새 광역 Skill을 만들지 않고 다음 기존 책임을 조합한다.

```text
analyzing-and-refining-game-concepts
→ 위험 가설·벤치마크·PoC·시스템 설계

managing-design-documents
→ 승인 가능한 Feature Design Spec 정본 작성·갱신

running-adversarial-review-and-refinement
→ 누락·충돌·과설계·전문 분야 경계 실패 공격

FEATURE_SPEC_TRACEABILITY_PACKET + validation
→ 승인된 Requirement의 구현·검증 추적
```

## 2. 문제 정의

현재 Base에는 프로젝트 방향, 시스템 설계, GDD 작업면, 전문 분야 Template, 승인 후 Traceability가 존재한다. 그러나 다음 질문을 한 공용 형식으로 닫는 계층이 약하다.

> “이 기능을 구현할 프로그래머·UI·아트·오디오·QA가 별도 구두 해석 없이 플레이어 경험, 상태, 규칙, 예외, 데이터, 피드백, 제작 입력, 검증 기준을 같은 의미로 이해할 수 있는가?”

기존 Traceability Packet은 **무엇이 어디에 구현·검증됐는지**를 연결하는 문서이며, Feature Design Spec은 **무엇을 어떻게 동작하게 만들어야 하는지**를 설명한다. 두 책임을 합치지 않는다.

## 3. 설계 원칙

### 3.1 Progressive Detail

상세도는 위험 감소에 따라 증가한다.

```text
L0 PROJECT DIRECTION
→ L1 FEATURE BRIEF
→ benchmark / prototype / PoC / adversarial review
→ L2 GAME FEATURE DESIGN SPEC
→ approval
→ L3 TRACEABILITY & PRODUCTION
```

초기 아이디어에 L2 문서를 강제하지 않는다.

### 3.2 One Question, One Authority

- 프로젝트 전체 Vision/Pillar/Loop: 기존 프로젝트 방향 정본.
- 기능의 상세 동작 의미: 등록된 Feature Design Spec.
- 현재 승인 Decision: `CURRENT_CONFIRMED_DECISIONS`.
- 실제 구현 상태: 코드·데이터·Scene·Resource·자산·테스트.
- Requirement→Task→검증 연결: Traceability Packet.
- 사람용 전체 현황: 프로젝트 Google Sheets GDD.

같은 내용을 여러 surface에 전문 복제하지 않는다.

### 3.3 Specialist Composition

Feature Spec은 전문 분야 문서를 대체하지 않는다.

예:

- 전투 AI의 공격 예산·공정성 상세는 전투 AI 계약을 참조.
- UX/UI 컴포넌트·focus·motion 상세는 UX/UI 정본을 참조.
- 아트 방향·Technique Card는 아트 정본을 참조.

Feature Spec에는 **이 기능이 해당 전문 분야에서 무엇을 필요로 하는지와 연결 ID/경로**만 둔다. 전문 규칙을 복사하지 않는다.

### 3.4 Evidence Before Detail

벤치마크와 PoC가 기능의 생존 여부를 바꿀 수 있다면 상세화보다 먼저 수행한다.

`KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST` 판정 이후 살아남은 기능만 상세화한다.

## 4. 문서 계층

### L0 — Project Direction

책임:

- 한 문장 플레이어 약속.
- Game Vision.
- Design Pillars.
- Core/Session/Meta Loop.
- Resource Flow.
- 핵심 제약·금지 방향.

기존 Base GDD와 project canon을 사용하며 새 Template을 만들지 않는다.

### L1 — Feature Brief

목적: 상세 설계 투자 전에 기능의 존재 이유와 가장 위험한 질문을 빠르게 닫는다.

최소 필드:

```yaml
feature_id:
working_title:
related_decision_ids: []
player_problem:
player_value:
experience_intent:
core_alignment:
primary_player_verbs: []
include_scope: []
exclude_scope: []
riskiest_assumption:
benchmark_question:
poc_question:
kill_or_cut_condition:
status: IDEA | RESEARCH | POC | SURVIVED | DEFERRED | REMOVED
```

L1은 별도 영구 정본을 강제하지 않는다. 기존 Approval Bundle, concept review, issue 또는 분야 정본의 짧은 section으로 존재할 수 있다.

### L2 — Game Feature Design Spec

목적: 제작자가 기능의 의미를 재해석하지 않고 구현할 수 있도록 상세 동작을 정의한다.

#### A. Identity & Authority

```yaml
feature_id:
title:
status: DRAFT | REVIEW | APPROVED | SUPERSEDED | BLOCKED_UNVERIFIED
related_decision_ids: []
project_direction_sources: []
canonical_owner:
source_commit:
upstream_brief_or_poc:
specialist_documents: []
```

#### B. Player Problem & Experience Intent

- 해결하는 플레이어 문제/욕구.
- 기능이 없을 때 발생하는 경험 문제.
- 플레이어가 반복할 행동.
- 유도할 판단.
- 즉시 피드백.
- 성공 감정·실패 학습.
- Pillar/Core Loop 중 강화하는 요소.

#### C. Scope & Non-goals

```yaml
included:
excluded:
non_goals:
protected_existing_behavior:
cut_first_if_scope_pressure:
```

#### D. Player Verbs & Input Contract

| Verb ID | 입력 | 선행 상태 | 플레이어 의도 | 취소 가능 | 반복 가능 | 결과 |
|---|---|---|---|---|---|---|

입력 장치별 차이가 핵심이면 플랫폼별 mapping은 전문 입력/UX 문서로 연결한다.

#### E. Entry / Exit / Lifecycle

- 기능이 언제 활성화되는가.
- 진입 조건.
- 정상 종료.
- 취소·이탈.
- 사망·패배·중단.
- 저장·불러오기 후 복귀.
- 세션/스테이지 전환 시 상태.

#### F. Core Flow

기본 표현:

```text
조건
→ 플레이어 입력
→ 시스템 처리
→ 판정
→ 즉시 피드백
→ 상태·자원 변화
→ 결과
→ 다음 선택
```

복잡한 기능은 상태도/flowchart를 연결할 수 있으나 문서가 다이어그램만으로 이해되어서는 안 된다.

#### G. State & Rule Contract

| State/Rule ID | 조건 | 처리 | 우선순위 | 출력 | 다음 상태 | 예외 |
|---|---|---|---|---|---|---|

규칙 충돌 시 우선순위를 명시한다. 숨은 임의 규칙을 구현 단계에서 추가하지 않는다.

#### H. Feedback Contract

| Event | 반드시 전달할 정보 | UI | VFX/Animation | Audio/Haptic | 접근성 대안 |
|---|---|---|---|---|---|

피드백은 장식이 아니라 플레이어가 상태·원인·결과를 이해하는 정보 계약이다.

#### I. Success / Failure / Recovery

- 성공 조건.
- 부분 성공.
- 실패 조건.
- 실패 원인의 가시성.
- 손실.
- 복구 가능성.
- 재시도.
- 중복 보상 방지.

#### J. Edge Cases

최소 검사:

- 자원 부족.
- 조건이 사라지는 중 입력.
- 빠른 연타/중복 입력.
- 동일 이벤트 중복 수신.
- 이미 변경된 상태.
- pause/scene transition.
- 저장/불러오기 중간 상태.
- disconnect/reconnect가 적용되는 경우.
- 취소 후 복귀.
- 재시도와 보상 중복.
- UI 표시와 실제 state 불일치.

관련 없는 항목은 이유를 가진 `NOT_APPLICABLE`로 표시한다.

#### K. Data & Balance

| Parameter ID | 의미 | 단위 | 초기 시험값 | 조정 범위 | 공식/관계 | 플레이어 영향 | 데이터 정본 | 재조정 조건 |
|---|---|---|---|---|---|---|---|---|

대량 콘텐츠 값은 Spec에 복제하지 않고 구조화 데이터/Sheet 경로를 참조한다.

#### L. Cross-discipline Production Inputs

```yaml
ux_ui:
  required_surfaces: []
  specialist_source: null
art:
  required_assets: []
  specialist_source: null
audio:
  required_events: []
  specialist_source: null
narrative:
  required_content_or_rules: []
  specialist_source: null
engineering:
  constraints: []
  architecture_source: null
qa:
  special_risk_areas: []
```

전문 내용의 상세 규칙은 specialist source가 소유한다.

#### M. Technical & Platform Constraints

- 목표 플랫폼.
- 성능 budget에 영향을 주는 부분.
- 저장/동기화 책임.
- online/offline 조건.
- 데이터 schema/compatibility 영향.
- 접근성 또는 입력 장벽.
- 필요한 engine/tool 제약.

확인하지 않은 수치를 확정 값으로 만들지 않는다.

#### N. Content Pipeline

반복 제작되는 기능이면 다음을 명시한다.

- 어떤 데이터를 입력하면 콘텐츠가 만들어지는가.
- 누가/무엇이 제작하는가.
- validation은 어디서 하는가.
- 수작업 예외는 무엇인가.
- 대표 콘텐츠 1개가 전체 production path를 증명하는가.

#### O. Benchmark & Evidence Decision

| Evidence ID | 비교 질문 | 관찰 | 다른 전제 | 판정 | 현재 설계에 반영한 내용 | 검증 |
|---|---|---|---|---|---|---|

판정:

`ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`.

#### P. Risk / PoC Evidence

```yaml
riskiest_assumption:
poc_build_or_artifact:
predeclared_success_criteria:
observed_result:
decision: KEEP | AMPLIFY | CHANGE | REMOVE | DEFER | RETEST
remaining_unknowns: []
```

결과를 본 뒤 성공 기준을 바꾸지 않는다.

#### Q. Acceptance Contract

각 Acceptance는 다음 형식으로 작성한다.

```text
Given <조건>
When <플레이어 행동 또는 외부 사건>
Then <관찰 가능한 게임 결과>
And <필요한 상태·피드백·저장 결과>
```

Acceptance는 구현 방법이 아니라 외부에서 확인 가능한 의미를 책임진다.

#### R. Telemetry / Playtest

- 관찰할 행동.
- 성공/실패 이유를 확인할 질문.
- 필요한 event/funnel.
- 사람 관찰이 필요한 항목.
- 중단 조건.
- 재조정 trigger.

텔레메트리만으로 감정과 원인을 확정하지 않는다.

#### S. Cut-down / Rollback

- `MUST_KEEP`: 기능 정체성을 유지하는 최소 부분.
- `CUT_FIRST`: 일정 압박 시 우선 제거.
- `DEFER`: 후속 버전으로 이동 가능.
- `ROLLBACK_TRIGGER`: 구현/플레이 결과가 어느 조건이면 이전 설계로 돌아가는가.
- `COMPATIBILITY`: 저장·데이터·콘텐츠 호환성 보호.

#### T. Open Decisions & Evidence Ceiling

```yaml
open_decisions:
  - id:
    status: CONFIRMED | RECOMMENDED_DEFAULT | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
    question:
    next_evidence:
verification_ceiling:
  design_contract:
  poc:
  runtime:
  target_device:
  human_playtest:
```

실행하지 않은 evidence는 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 남긴다.

### L3 — Traceability & Production

기존 `FEATURE_SPEC_TRACEABILITY_PACKET`이 담당한다.

추가 연결만 필요하다.

```yaml
design_spec:
  design_spec_id:
  canonical_design_spec_path:
  source_commit:
```

Traceability Packet에 L2 본문을 복사하지 않는다.

## 5. 작성/승격 Workflow

```text
BASELINE_RECOVERY
→ 기존 Decision·정본·구현·같은 Goal PR 확인
→ FEATURE_BRIEF
→ benchmark question
→ player/professional evidence
→ riskiest assumption
→ PoC / prototype
→ adversarial attack
→ validate critique
→ KEEP / CHANGE / REMOVE / DEFER / RETEST
→ 살아남은 기능만 FEATURE_DESIGN_SPEC 작성
→ specialist boundary links
→ cross-discipline completeness attack
→ Acceptance 확정
→ user approval / reused approval
→ canonical sync
→ TRACEABILITY_PACKET
→ implementation
→ runtime/playtest/telemetry
→ recalibration
```

## 6. Adversarial Review Lens

Feature Spec 검토 시 최소 다음 실패를 공격한다.

### Player Experience

- 기능은 존재하지만 플레이어가 왜 쓰는지 불명확한가.
- 행동·선택을 자동화/수치가 대신하는가.
- 성공/실패 원인을 피드백으로 이해할 수 있는가.

### Rules & State

- 상태 전이가 빠졌는가.
- 동시에 성립하는 규칙 우선순위가 모호한가.
- 저장/재시도/중복 입력에서 깨지는가.

### Production

- UI·아트·오디오·데이터 제작 입력이 빠졌는가.
- 한 번만 수작업 가능한 구조를 반복 production-ready로 착각했는가.
- 필요한 전문 문서를 복제하거나 반대로 아무 연결도 하지 않았는가.

### Validation

- Acceptance가 주관적 문장인가.
- 실제 플레이 없이 “재미있다”를 완료 조건으로 사용했는가.
- 텔레메트리만으로 감정을 추론하는가.
- PoC 기준을 결과 뒤 바꿨는가.

### Scope

- Feature Spec이 Roadmap/Task/Test ledger까지 소유하려 하는가.
- 초기 아이디어를 지나치게 상세화했는가.
- Cut-down path가 없어 일정 압박 시 코어까지 무작위 삭제될 위험이 있는가.

## 7. Base 통합 경계

승인 후 최소 통합안:

1. `templates/planning/GAME_FEATURE_DESIGN_SPEC.md` 생성.
2. `managing-design-documents`에 작성/갱신 owner 연결.
3. `analyzing-and-refining-game-concepts`에 PoC 생존 기능의 L2 승격 조건 연결.
4. `DESIGN_DOCUMENT_SYSTEM`에 L0-L3 계층 연결.
5. 기존 Traceability Packet에 upstream spec identity만 연결.
6. Sheet에는 Feature ID, Decision ID, 한 문장 요약, 정본 경로, 구현/검증 상태만 노출.
7. 새 ACTIVE Skill은 추가하지 않음.

## 8. 검증 설계

구현 단계에서 최소 다음 테스트가 필요하다.

### Contract tests

- Template에 모든 핵심 영역이 존재한다.
- Task/실제 테스트 결과를 소유하지 않는다는 경계가 존재한다.
- L0/L1에는 강제되지 않는다.
- specialist document composition 규칙이 존재한다.
- Traceability Packet이 upstream Spec identity를 소비한다.

### Routing tests

- “핵심 컨셉을 브레인스토밍” 요청은 Feature Spec으로 과라우팅하지 않는다.
- “전투 시스템 세부 규칙을 구현 전에 명세”는 concept + design document 경로로 연결된다.
- “승인된 기능의 파일별 구현 상태 추적”은 Feature Spec이 아니라 Traceability로 간다.

### Governance tests

- new Skill count 0.
- Registry 불필요 변경 없음 또는 trigger를 바꿔야 할 명확한 근거가 있을 때만 최소 수정.
- reference-freshness 소비자 연결.
- Sheet 상세 전문 복제 금지.
- 관련 필수 CI에서 신규 테스트 실제 실행.

### Project Pilot ceiling

Base contract 통과는 실제 프로젝트에서 이해도·개발 효율·품질 개선을 증명하지 않는다.

최소 실제 Pilot 후에만 다음을 평가한다.

- 구현자가 추가 기획 질문 없이 작업 가능한가.
- QA가 Spec만으로 주요 정상/실패/복구 경로를 도출 가능한가.
- UI/아트/오디오 누락이 줄었는가.
- 문서 유지 비용이 과도하지 않은가.
- PoC 이전 과설계가 실제로 억제되는가.

## 9. 롤백

proposal 단계:

- 이 BCP branch/PR을 닫으면 활성 Base 동작에는 변화가 없다.

구현 단계:

- 신규 Template과 기존 owner의 조건부 연결을 함께 revert한다.
- 기존 Feature Spec을 사용한 프로젝트가 있다면 문서를 삭제하지 않고 project-specific source로 유지하거나 당시 Base pin을 보존한다.
- 기존 Traceability Packet의 이전 schema/format 소비를 깨뜨리는 migration은 허용하지 않는다.

## 10. Self-review

```yaml
placeholder_scan: PASS
internal_consistency: PASS
scope_check: PASS
ambiguity_check: PASS
new_active_skill: NO
monolithic_gdd: REJECTED
traceability_duplication: REJECTED
specialist_document_replacement: REJECTED
implementation: NOT_STARTED
project_pilot: NOT_RUN
human_usability: HUMAN_NOT_RUN
```
