# Work 5단계와 Project Canon 매핑 실검증 Case

## 목적

BCP-2026-040 구현 전에 Base current owner, active game Project `AGENTS.md`/current state, Project Notion Home/Production/Handoff, actual implementation/evidence 표현을 fresh-read해 공용 5단계가 Project-native state를 훼손하지 않고 적용 가능한지 검증한 사례다.

```text
FIVE_PHASE_PROJECT_MAPPING
PROJECT_NATIVE_STATE_NAMES_PRESERVED
NO_PROJECT_WIDE_STATE_RENAME
DOMAIN_ADAPTABLE_FIVE_PHASE_INTERFACE
GODOT_EVIDENCE_NOT_APPLICABLE_FOR_NON_GAME
```

## 확인된 공통 문제

Base는 이미 startup canon, Grill Me, benchmark, Visual/Audio production, Codex handoff, machine QA, Work final review, Human/Player evidence owner를 갖고 있었다. 그러나 minimum-transition profile의 `Stage A — Work preparation` 안에 기획·검수·요소 제작이 함께 들어가 사용자 관점에서는 다음 경계가 압축됐다.

```text
핵심 제품 의미를 사용자와 기획 확정
!= 구현 전 생산 검수 통과
!= actual-consumer 인게임 요소 제작 완료
```

또한 구현 전 `검수`와 Codex 뒤 실제 diff/runtime/build `final review`가 같은 말로 보일 수 있었다. 따라서 전자는 Phase 2, 후자는 Phase 4 closeout으로 분리하는 것이 필요했다.

## Project 실검증 매핑

| Project | current/native 표현 | 공용 5단계 매핑 finding |
|---|---|---|
| MylittleBoat | core direction + Visual production order + Codex integration/runtime check | 기획·요소·구현 책임은 있으나 독립 Phase 2 preproduction review를 공용 owner가 제공해야 함 |
| OMENWARD | Decision/Active Context router + planning/image production + implementation evidence gates | 현재 Project Decision을 그대로 유지하고 공용 phase만 매핑해야 함 |
| Ten-Paces | `PLAN / BUILD / REVIEW` + Implementation Ready + Human evidence 분리 | `PLAN / BUILD / REVIEW`는 macro 5단계명이 아니라 Work Mode/Project gate로 유지 |
| urban-legend | `PLAN → BUILD → REVIEW`, Planning complete, runtime authorization 별도 | 기획 완료와 구현 허가를 Project-native로 유지하고 Phase 2/3/4를 의미로 매핑 |
| Switchy Express | planning/implementation/package candidate/physical-human gates | 자동 package readiness는 Phase 4, 실제 사람 검증은 Phase 5로 매핑 가능 |
| Tetris | production canon + consumer-first Visual + 독립 Human Evidence 계약 | actual-consumer 원칙과 Phase 4/5 evidence ceiling이 공용 계약과 일치 |
| GRIMOIRE | `MERGED_MAIN_AUTOMATED_VERTICAL_SLICE_READY → USER_VERTICAL_SLICE_VALIDATION_PENDING` | Phase 4 완료와 Phase 5 대기를 가장 명확히 증명하는 current 사례 |
| Blacksmith | PLAN Gate + research/TDD/review + implementation blocked/current-specific gates | 공용 5단계로 rename하지 않고 실제 Gate 의미를 1/2/4에 매핑 |
| Ninja Survival | PLAN/DoR/BUILD/verification/review/merge + Human Slice | 전체 책임은 존재하며 DoR/verification을 Phase 2/4 내부 evidence로 유지 |
| Coc-Fiction | 비게임 장편 서사 production, Godot `NOT_APPLICABLE` | 업무 5단계는 narrative production에 adapt 가능하지만 Godot/game evidence는 `NOT_APPLICABLE` |

## Notion 실검증

Project Home/Production/Handoff는 North Star, core loop, Visual direction, 현재 evidence, Human/Player `NOT_RUN` 등을 Project별 구조로 관리한다. 모든 Project Notion을 동일 5단계 이름으로 migration하면 다음 문제가 생긴다.

- Project Decision/Task/Gate의 현재 의미 손실
- historical receipt churn
- Base와 Project에 두 번째 상태 정본 생성
- open PR/current handoff와 충돌 가능성 증가

따라서 공용 5단계는 **실행 interface + mapping receipt**만 소유하고 Notion/Project native state를 rename하지 않는다.

## 채택 매핑

```yaml
FIVE_PHASE_PROJECT_MAPPING:
  project_native_state:
  phase_1_planning:
  phase_2_review:
  phase_3_element_production:
  phase_4_implementation:
  phase_5_user_validation:
  current_phase:
  mapping_evidence:
  ambiguity_or_drift:
```

예:

```text
PLAN / DoR / BUILD / REVIEW
→ 실제 Gate 의미에 따라 Phase 1 / 2 / 4로 매핑

AUTOMATED_VERTICAL_SLICE_READY
→ Phase 4 완료 / Phase 5 대기

PLANNING_COMPLETE + runtime implementation unauthorized
→ Phase 1 완료 여부와 Phase 2/4 authorization을 별도 판정
```

## Vertical Slice 완료 범위 실검증

Base `designing-vertical-slices` owner는 이미 representative experience, target quality, system integration, pipeline, actual play evidence를 요구한다. 따라서 machine QA까지 끝난 Phase 4와 실제 사용자 경험이 검증된 Phase 5를 분리해야 한다.

```text
AUTOMATED_VERTICAL_SLICE_READY
!=
USER_VALIDATED_VERTICAL_SLICE
```

Phase 4에는 actual build, connected core consumers, shipping-intent UI/Visual/Audio/VFX/feedback, deterministic/runtime/build evidence, exact identity, launch route가 필요하고 Human/Player evidence는 아직 `NOT_RUN`이다.

Phase 5에는 사용자가 exact build를 실제 플레이한 evidence, representative action→choice→result→feedback, usability/fun/emotion/memory/differentiation 판단, finding/feedback/next decision, Canonical Reflection After Play가 추가된다.

전체 게임 콘텐츠·최종 전체 밸런스·모든 플랫폼·최종 localization·스토어 공개 출시 PASS는 current Vertical Slice 완료 조건이 아니다.

## 교정 결론

```text
ADOPT: Base에 하나의 5단계 macro owner + Project mapping
ADAPT: Project-native state를 의미 기준으로 phase에 매핑
REJECT: 모든 Project AGENTS/Notion을 동일 phase 이름으로 일괄 rename
```

이 방식이 Work 재개 시 사용자가 보는 작업순서를 고정하면서도 Project 분야별 정본과 실제 구현 evidence를 보존한다.
