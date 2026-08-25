---
name: auditing-and-refining-ui-art
description: Use when planning, polishing, or auditing game UX, UI structure, interaction, input, accessibility, Godot UI, or rendered interface quality.
---

# 게임 UX/UI 설계·폴리싱·감사

## 역할과 경계

플레이어 경험을 화면·정보·입력·상태·피드백·접근성·Godot 구현 계약으로 변환하고, 준비된 UI를 증거 기반으로 폴리싱하며, 구현된 Godot 또는 Web UI를 실제 렌더와 증거로 감사한다.

- UX/UI는 표시 데이터를 입력받고 **사용자 의도**를 `Signal` 또는 명시적 이벤트로 반환한다.
- 피해·보상·저장·진행 등 **도메인 규칙**을 UI에서 재계산하거나 새 상태 책임 원본으로 소유하지 않는다.
- 게임 코어·벤치마크·플레이어 반응은 `analyzing-and-refining-game-concepts`, 문서 발행은 `managing-design-documents`, 공격 검토는 `running-adversarial-review-and-refinement`, 통합 증거는 `reviewing-and-validating-project-changes`가 책임진다.
- 최종 이미지 생성·아트 기술 카드는 `designing-art-prompts-and-technique-cards`가 책임진다.

## Skill Modes

### 설계

- `experience-contract`: 플레이어 감정·판단·행동·보상과 관찰 가능한 성공 기준을 정의한다.
- `flow-and-information-architecture`: 사용자 여정, 화면별 중심 질문, 첫 시선, 상시/상세/결과 정보, 진입·취소·복귀를 구조화한다.
- `pattern-selection`: 반복 문제를 패턴 카드와 대조하고 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 판정한다.
- `design-system-contract`: 토큰·컴포넌트·상태·피드백 채널·문구·빈 상태·오류·파괴적 행동·재사용 경계를 정의한다.
- `godot-ui-contract`: 기존 구조를 조사하고 `Theme`, `Control`, `Container`, 재사용 Scene, `Signal`, 포커스, 입력 액션과 상태 소유 경계를 정한다.
- `accessibility-gate`: 정보·입력·탐색·시간·모션·음향·텍스트·인지 장벽과 동등한 경로를 설계한다.
- `playtest-contract`: build·commit·해상도·입력·참가자·과제·가설·행동/설명 증거·중단/통과 기준을 고정한다.

### 폴리싱

- `polishing-pass`: 기능·정보 구조·상태 소유권이 충분히 안정된 화면에서 `P0 BLOCKER → P1 CLARITY → P2 CONSISTENCY → P3 DELIGHT` 순서로 계층·가독성·상태·피드백·모션·음향·햅틱·반복 사용·중단·재진입·성능을 마감하고 전후 증거를 만든다.

### 구현 결과 감사

- `runtime-ui-audit`: 실제 실행 화면과 승인 방향을 A~E 영역으로 감사하고 정적 후보를 증거와 대조한다.
- `refine-approved-findings`: 사용자 승인 finding만 구조→계층→타이포그래피→상태→장식 순으로 최소 개선한다.
- `reaudit`: 기존 판단을 보지 않은 새 검사 컨텍스트에서 전후 렌더·입력·해상도·폴백·회귀를 다시 검수한다.

## 사용 조건

- 신규 화면·HUD·카드·팝업·메뉴·튜토리얼·조사판·결과/복기 흐름을 설계한다.
- 정보 계층, 점진 공개, 선택 비교, 예상 결과, 오류 복구, 포커스와 입력 계약이 필요하다.
- Godot `Control`, `Container`, `Theme`, `StyleBox`, 재사용 Scene의 책임과 상태를 정한다.
- 구현된 Godot/Web UI의 구조·간격·타이포그래피·색상·상태·접근성을 감사한다.
- 실제 사용자 이해 가설과 플레이테스트 계약을 정의한다.
- 기능과 정보 구조가 준비된 화면의 UI 폴리싱 우선순위·피드백 예산·반복 피로·중단·재진입·전후 증거를 정의한다.

다음에는 주 Skill로 사용하지 않는다.

- UI와 무관한 전투·경제·저장·네트워크 로직만 변경한다.
- 최종 이미지 프롬프트나 아트 자산 제작만 수행한다.
- 실제 화면 없이 미감 취향만 평가한다.
- HTML 기획 대시보드·프로젝트 현황판 제작은 요청 범위에 포함하지 않는다.
- 명확한 단일 기계 수정이며 UX·상태·입력 계약이 바뀌지 않는다.

## 설계 절차

필요한 mode만 순서대로 사용한다.

```text
프로젝트 코어·현재 정본·실제 UI 조사
→ experience-contract
→ flow-and-information-architecture
→ pattern-selection
→ design-system-contract
→ godot-ui-contract
→ accessibility-gate
→ playtest-contract
→ 구현 준비도가 충족되면 polishing-pass
→ runtime-ui-audit
```

1. 화면마다 플레이어의 중심 질문과 가장 중요한 행동을 하나씩 정한다.
2. 상시 정보, 선택 시 상세, 실행 전 예상, 실행 후 결과·복기를 분리한다.
3. 새 기능 추가 전에 `REMOVE → REDUCE → MERGE → CLARIFY → FEEDBACK 강화 → ADD` 순으로 검토한다.
4. 정상·hover·focused·pressed·selected·disabled·locked·loading·error·new 중 필요한 상태를 선언한다.
5. 상태는 색·소리·모션 하나에만 의존하지 않고 텍스트·형태·아이콘·로그 등 동등 신호를 둔다.
6. 취소·되돌리기·파괴적 행동·오류·빈 상태·누락 자산의 복구 경로를 정의한다.
7. 프로젝트의 최소/목표 해상도, 긴 한국어, 안전 영역, 선언된 입력 장치를 검증 조건에 넣는다.
8. 기존 Theme·레이아웃·상태·편집 시스템을 조사한 뒤 가장 작은 재사용 단위를 정한다.
9. 폴리싱은 `P0 BLOCKER → P1 CLARITY → P2 CONSISTENCY → P3 DELIGHT` 순서로 진행하고, P0~P2가 남아 있으면 장식 효과를 보류한다.
10. 자주 반복되는 행동은 낮은 피드백 강도를 사용하고 모션·음향·햅틱을 끈 동등 경로를 둔다.
11. 빠른 반복 입력, 중복 입력, 애니메이션 중단·재진입, modal 재진입에서 결과 중복과 시각 drift를 검사한다.
12. 자동 검사와 사람 이해 증거를 분리하고 실행하지 않은 항목은 `NOT_RUN` 또는 `UNVERIFIED`로 둔다.

## BCP-2026-035 · 생성형 visual 작업 무결성

### `VISUAL_TASK_SCOPE_FIDELITY`

single-screen mock, state sheet, before/after, visual QA reference처럼 경계가 있는 생성형 visual 작업은 생성 전에 `visual_question / target_screen / target_state / excluded_scope`를 고정한다. 결과가 unrelated screen, broad dashboard, 새 게임 규칙·UI처럼 제외 범위를 넘어가면 보기 좋더라도 같은 deliverable의 PASS로 세지 않는다. 먼저 원래 질문에 맞게 좁히거나 별도 작업으로 재분류한다.

### `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`

사용자가 N개의 이미지·결과를 요청하면 기본값은 **독립 검토·교체·배치 가능한 N개 deliverable**이다. N-panel collage는 사용자가 collage를 명시적으로 요청하거나 승인한 경우에만 N개와 동등하게 센다. 의미 손실 없이 분리 가능하면 독립 결과로 분리하고, panel 의존성 때문에 crop이 의미를 훼손하면 원래 bounded brief로 재생성한다. Base는 특정 N값이나 이미지 공급자의 동작을 고정하지 않는다.

### `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`

플레이 판단에 중요한 경로·선택·잠금·상태가 art/background와 경쟁하면 최소한 다음 세 방향을 비교한다: 전체 style 교체, color/intensity만 강화, 기존 정체성을 유지하면서 독립 semantic cue를 중복하는 안. 기존 제품 정체성 보존 가치가 있다면 세 번째 안을 우선 검토하고, 필요에 따라 color, direction, shape, text/icon, brightness/thickness, motion 중 서로 독립적인 신호를 조합한다. 특정 색·화살표·두께를 공용 상수로 만들지 않는다.

이 세 계약은 생성 결과의 scope·산출물 단위·판단 정보 표현을 통제한다. mock/reference나 자동 검사가 `human comprehension`, 접근성, 실제 runtime/device correctness를 증명하지는 않는다. 최종 이미지 생성·아트 기술 카드 owner와 사람/실기기 검증 경계는 기존 책임을 유지한다.

상세 방법은 필요할 때만 읽는다.

- [ux-ui-design-system-method.md](references/ux-ui-design-system-method.md)
- [game-ux-pattern-library.md](references/game-ux-pattern-library.md)
- [ux-ui-reference-library.md](references/ux-ui-reference-library.md)
- [godot-ui-implementation-contract.md](references/godot-ui-implementation-contract.md)
- [project-adapter-contract.md](references/project-adapter-contract.md)
- [ui-polishing-method.md](references/ui-polishing-method.md)

## 기존 UI 감사 절차 보존

1. 프로젝트 책임 원본과 실제 UI 파일을 읽고 현재 화면을 렌더한다.
2. 아트 방향이나 기능·경험·구조가 미확정이면 요청 계약의 `clarify`를 먼저 사용한다.
3. [inspection-areas.md](references/inspection-areas.md)의 A~E를 각각 독립적으로 감사한다.
4. 플랫폼별 구조는 [platform-adapters.md](references/platform-adapters.md)로 해석한다.
5. 필요하면 읽기 전용 후보를 만든다.

```text
python skills/auditing-and-refining-ui-art/scripts/scan_ui_art_signals.py --root <대상> --adapter auto --output-json <findings.json> --output-markdown <findings.md>
```

6. 정적 결과는 `CANDIDATE`이며 결함 확정이 아니다. 실제 화면·의도·접근성·플랫폼과 대조한다.
7. 각 finding에 파일·행·관찰 증거·플레이어 위험·제안·검증 조건을 기록한다.
8. **사용자 승인 전** UI 파일·이미지·Theme·CSS를 수정하지 않는다.
9. 승인 후 A→B→C→D→E 순서로 최소 수정하고 각 영역을 다시 렌더한다.
10. 새 검사 컨텍스트로 **전후 렌더**와 입력·해상도·폴백을 비교한다.

## 설계 출력 계약

```yaml
player_experience:
platform_and_input:
screen_question:
first_attention:
journey_and_flow:
information_layers:
selected_patterns:
state_source:
component_states:
feedback_channels:
polish_readiness:
polish_priority:
feedback_budget:
repetition_and_interruption:
before_after_artifacts:
input_and_focus:
accessibility_barriers:
fallbacks:
godot_contract:
validation_matrix:
human_evidence: HUMAN_NOT_RUN | PARTIAL | PASSED | FAILED
result: PASS | PARTIAL | FAIL | NOT_RUN | BLOCKED
```

## 감사 Finding 계약

```text
finding_id
area
adapter
severity
confidence
file
line
observed_evidence
player_or_design_risk
proposed_change
verification_predicate
status
```

상태는 `CANDIDATE → APPROVED / WAIVED / REJECTED → RESOLVED`다. 목적 있는 표현은 기존 `base-ui-audit: allow <RULE_ID> reason=<이유>` 형식으로 예외 사유를 남길 수 있지만 실행 화면에서 이유가 확인되지 않으면 다시 후보로 올린다.

## 품질 게이트

- 기능 목록보다 플레이어가 보고·판단하고·행동하고·확인하는 흐름이 먼저다.
- 외부 레퍼런스는 변환 축과 차별화 근거로만 사용하고 화면·자산·브랜드 표현을 복제하지 않는다.
- 비활성·잠금·오류 상태는 원인과 가능한 다음 행동을 제공한다.
- UI 폴리싱은 구조·가독성·상태·피드백을 먼저 해결하고 장식은 마지막에 적용한다.
- 반복 사용·빠른 입력·애니메이션 중단·재진입에서 결과 중복, 누적 transform, 입력 지연과 피로를 검증한다.
- 핵심 입력은 프로젝트가 선언한 포인터·키보드·게임패드·터치 경로에서 완결된다.
- 팝업 종료 뒤 이전 의미 있는 포커스로 복귀한다.
- 접근성 설정·모션 감소·음향 끄기·자산 누락이 게임 결과를 바꾸지 않는다.
- 자동화 통과를 사람 이해·실기기·보조기기·법적 준수 증거로 과장하지 않는다.
- 기존 정상 흐름과 프로젝트 코어를 보호한 전후 증거가 없으면 완료가 아니다.

## Base v9.4 UI 모션·상호작용

모션·상호작용 작업에서는 `references/ui-motion-and-interaction-principles.md`를 읽는다. 정보 구조와 상태 소유권이 준비된 뒤 모션 목적·staging·입력 접수/처리 중/결과·중단·즉시 완료·빠른 반복·재진입·Reduced Motion·mute·haptic-off·성능을 설계한다.

`AnimationPlayer`와 `Tween`은 표현을 담당하며 구매·보상·저장·진행의 도메인 상태 권위를 소유하지 않는다. 모션이 중단되거나 즉시 완료돼도 결과는 한 번만 발생해야 한다.
