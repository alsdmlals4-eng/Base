# Work 5단계 버티컬 슬라이스 · 프로젝트 정본 대조 사례

> 이 문서는 2026-08-27 Base와 여러 프로젝트 current owner를 실제 대조한 **evidence case**다. 프로젝트 전용 상태·ID·Art Direction을 공용 실행 권한으로 만들지 않는다.

```text
ACTUAL_BASE_AND_PROJECT_CANON_AUDIT
FIVE_PHASE_INTERFACE_NEEDED
PROJECT_NATIVE_STATE_MAPPING_NOT_MIGRATION
AUTOMATED_READY_IS_NOT_USER_VALIDATED
```

## 1. 감사 질문

사용자가 요구한 다음 5단계가 실제 Base·프로젝트 정본에서 서로 구분되는지 확인했다.

```text
1. 기획
2. 검수
3. 이미지·사운드·UI·Data·VFX 등 요소 생성
4. Codex 구현·Machine QA
5. 사용자 실제 검증
```

확인 기준:

- 단계별 owner·입력·출력·진입·종료 Gate가 있는가?
- Phase 1 핵심 기획이 사용자 공동설계인가?
- routine 자동 승인이 core meaning까지 자동 승인하는가?
- 구현 전 검수와 구현 후 검수가 구분되는가?
- 버티컬 슬라이스 자동화 완료와 사용자 검증 완료가 구분되는가?
- 프로젝트 고유 Task/Decision/Gate를 보존하면서 공용 흐름을 복원할 수 있는가?

## 2. Base current owner 대조

### 존재한 기능

- `WORK_PROJECT_START_CANON_CHECKLIST.md`
  - 핵심 재미·핵심 시스템·SWOT·current stage·남은 작업·작업순서·정본 선교정
- `PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`
  - PLAN 우선, 기획 충돌, 사용자 결정, Grill Me Gate
- `grill-me-protocol.md`
  - 프로젝트 코어·player fantasy·Core Loop·pointed fun·MVP·차별점·가장 위험한 Vertical Slice 가설
- Work v4.9 / v4.8 r5.4
  - Reuse First, benchmark, 최소 3안, Visual, IRG, Implementation Ready, Codex, play evidence, merge/readback
- `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
  - Work preparation → Codex single window → Work final review → user-validation pending
- `designing-vertical-slices`
  - 대표 경험·목표 품질·시스템 연결·제작 파이프라인·실제 play evidence

### 실제 누락

기능 자체보다 하나의 명확한 phase interface가 없었다.

```text
Stage A Work preparation
= 기획 + 구현 전 검수 + asset/input 제작
```

따라서 `기획 확정`, `검수 통과`, `요소 제작 완료`가 독립 상태로 보이지 않았다.

또한:

```text
AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

은 존재하지만 실제 사용자 플레이 뒤의 공용 terminal state와 feedback reopen map이 약했다.

## 3. 프로젝트 current owner 대조

### MylittleBoat

- Project core loop와 protected rest-first identity는 GitHub `AGENTS.md`에서 명확했다.
- Notion Home은 North Star·핵심 감정·핵심 약속·Visual GDD·제작 순서를 사람이 읽을 수 있게 제공했다.
- image production → Codex integration → runtime verification 흐름은 존재했지만 preproduction review가 독립 phase로 보이지 않았다.

### OMENWARD

- Decision index·Active Context가 current planning과 implementation authorization을 소유했다.
- core identity와 Visual boundary가 강했다.
- 프로젝트 전용 Decision/state는 정교하지만 공용 5단계 명칭은 사용하지 않았다.

### Ten-Paces Hidden Moves

- `PLAN / BUILD / REVIEW`와 Implementation Ready·Human evidence 분리가 존재했다.
- `REVIEW`가 구현 전 기획 검수와 구현 후 결과 검수 양쪽을 가리킬 수 있어 사용자 2단계의 의미를 고정할 필요가 있었다.

### urban-legend

- `PLAN → BUILD → REVIEW`, planning complete, runtime implementation authorization이 분리됐다.
- Phase 1과 Phase 4 authorization은 명확했지만 Work asset production은 독립 상태가 아니었다.

### Switchy Express

- planning/implementation/package candidate/physical-human gate가 상세하게 분리됐다.
- package·automation evidence를 current Human/Player evidence로 승격하지 않는 경계가 강했다.
- 프로젝트 전용 candidate/Decision 상태를 Base 공용 이름으로 rename할 이유는 없었다.

### Tetris

- actual consumer 없는 production image 금지와 독립 Human Evidence 계약이 존재했다.
- Human validation은 명확하지만 Phase 1~4의 Work 사용자 인터페이스는 프로젝트 고유 owner에 분산됐다.

### GRIMOIRE

가장 직접적인 현재 evidence였다.

```text
MERGED_MAIN_AUTOMATED_VERTICAL_SLICE_READY
→ TASK9_USER_VERTICAL_SLICE_VALIDATION_PENDING
```

- actual product root·test·runtime·CI는 준비됐다.
- 사람 UX·Player Experience·기기·성능·출시는 `NOT_RUN`이었다.
- 따라서 자동화 완료가 사용자 검증 완료가 아니라는 점이 실제 current project state에서 확인됐다.

### Blacksmith

- 현재 `PLAN` Gate와 pre-work research·brainstorming·TDD·review가 강했다.
- implementation은 planning declaration 전 차단됐다.
- planning과 review는 강하지만 Phase 3 asset/input readiness와 Phase 4 전환을 공용 상태로 볼 수 없었다.

### Ninja Survival

- `PLAN/canon/Decision → DoR → BUILD → verification → adversarial review → merge/readback`이 존재했다.
- release-near Human Vertical Slice를 full content expansion 전에 요구했다.
- 사용자 5단계와 의미가 호환되지만 이름과 phase boundary는 프로젝트 전용이었다.

### Coc-Fiction

- 게임 runtime 프로젝트가 아니며 Godot는 `NOT_APPLICABLE`이었다.
- 따라서 공용 5단계는 engine-hardcoded workflow가 아니라 domain-adaptable interface여야 했다.

## 4. Notion 감사 결과

Project Homes는 다음 기능을 잘 수행했다.

- North Star·player promise·core loop·핵심 시스템
- 사람이 보는 Visual·Flow·현재 상태
- GitHub/실제 runtime과 분리된 human-facing truth

그러나 모든 Home에 동일한 5단계 상태를 추가하거나 기존 IA를 다시 이동하는 것은 다음 문제를 만든다.

- 프로젝트 고유 Decision·Task·Gate 중복
- stale phase snapshot
- 검증된 Home IA churn
- Base interface와 Project canon의 두 번째 정본화

따라서 `FIVE_PHASE_PROJECT_MAPPING`을 current execution receipt로 만들고, 실제 current state 오해·충돌만 bounded correction하는 방식을 채택했다.

## 5. 대안 비교

| 방법 | 장점 | 실패 | 판정 |
|---|---|---|---|
| 기존 3단계 profile 유지 | 변경 최소 | Phase 1~3 경계 불명확 | REJECT |
| 모든 프로젝트 state·Notion을 5단계로 rename | 표면 통일 | 대량 churn·project-specific owner 손실 | REJECT |
| Base 5단계 interface + project-native mapping | 사용자 이해·새 Work 재개·비퇴행 균형 | mapping contract 필요 | ADOPT |

## 6. 채택한 공용 원리

```text
DELEGATED_ROUTINE_APPROVAL
!= CORE_PRODUCT_MEANING_APPROVAL
```

```text
Phase 1 핵심 기획
→ current canon·benchmark·3 alternatives·Grill Me 공동설계

Phase 2
→ 구현 전 substantive review

Phase 3
→ Work가 실제 구현 입력 일괄 완성

Phase 4
→ Codex implementation + Machine QA + Work final implementation review

Phase 5
→ user actually plays exact build
```

## 7. Vertical Slice 완료 경계

### Phase 4

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

증명:

- representative flow가 exact build에서 실행 가능
- 시스템·UI·Visual·Audio·VFX·Data actual consumer 연결
- machine QA·runtime/build·CI·merge/readback
- 다운로드·실행 route

증명하지 않음:

- Human usability
- Player Experience
- 전체 게임 완료
- release readiness

### Phase 5

```text
USER_ACTUALLY_PLAYS_EXACT_BUILD
→ USER_VALIDATED_VERTICAL_SLICE
```

추가 증명:

- representative action→choice→result→feedback 실제 사용자 완료
- blocking usability finding 처리
- 핵심 재미·감정·기억·차별점 방향 판단
- feedback에 따른 bounded reopen과 Canonical Reflection After Play

## 8. 왜 사용자 한 명의 검증이 필요한가

Machine QA는 다음을 검증할 수 있다.

- code·state·Scene·Resource·import·build
- 입력 연결과 화면 존재
- 정해진 상태 전이
- screenshot과 runtime diagnostics

Machine QA만으로는 다음을 증명하지 못한다.

- 처음 보는 사람이 목표·선택·다음 행동을 이해하는가?
- 핵심 고민이 실제 고민으로 느껴지는가?
- 보상·실패 학습·피드백이 의미 있게 읽히는가?
- 편안함·긴장·성취·애착 등 의도 감정이 발생하는가?
- 무엇이 기억에 남고 차별점으로 인식되는가?

한 명의 사용자 검증은 시장 적합성 표본이 아니라 **현재 owner 사용자의 제품 방향 Gate**다. 더 넓은 target-player 검증은 별도 playtest contract가 필요하다.

## 9. 프로젝트 교정 방식

```text
current Project GitHub + Notion + actual implementation
→ project-native state 복원
→ phase 1~5 mapping
→ ambiguity/drift 발견
→ 현재 owner의 stale stage·next gate·evidence ceiling만 최소 교정
→ destination readback
```

하지 않는 것:

- 모든 project state rename
- 모든 Notion Home에 중복 status dashboard 생성
- 역사 Task/Decision 일괄 수정
- 비게임 프로젝트에 Godot Gate 강제

## 10. Evidence ceiling

이 Case는 Base·프로젝트 정본 구조 감사 evidence다.

```text
project canon inspected
!= every project migrated
!= product implementation changed
!= build created
!= user play executed
!= USER_VALIDATED_VERTICAL_SLICE
```

실제 각 프로젝트는 다음 Work 시작 시 current mapping receipt와 phase evidence를 별도로 남긴다.

## 11. 재사용 조건

사용 trigger:

- 새 Work가 현재 프로젝트 stage를 복원해야 할 때
- planning complete와 implementation ready가 혼동될 때
- asset production이 planning review 전에 시작될 위험이 있을 때
- automated-ready를 Human/Player PASS로 올릴 위험이 있을 때
- user feedback 이후 어느 단계로 돌아가야 할지 불명확할 때

비사용:

- 단순 오탈자·L0 maintenance
- 이미 current phase와 next Gate가 명확하고 source/evidence가 바뀌지 않은 동일 continuation

## 12. 롤백

5단계 interface를 revert하더라도 프로젝트 고유 canon·Task·Decision·Notion IA는 변경하지 않았으므로 기존 current owners로 돌아갈 수 있다.
