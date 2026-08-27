# BCP-2026-040 — Work 5단계 버티컬 슬라이스 실행 인터페이스

## 0. 출처·상태

```yaml
proposal_id: BCP-2026-040
submitted_at: 2026-08-27
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: 2026-08-27 current user instruction
source_base_main: 9b45125d087521fa98696cbd1e857bf2ffbf816a
incremental_cost: 0
```

사용자가 승인한 목표 흐름은 다음과 같다.

```text
1. 기획
2. 검수
3. 이미지·사운드·UI·데이터·VFX 등 요소 생성
4. Codex 제품 구현
5. 사용자 실제 검증
```

핵심 기획은 자동 권장안만으로 닫지 않고, current canon·Grill Me·벤치마킹·최소 3개 실질 대안을 사용해 사용자와 공동 설계한다. routine 기술 세부의 standing approval은 핵심 재미·Core Loop·핵심 시스템·주요 UX·경제·서사·Art Direction의 제품 의미를 자동 확정하는 권한이 아니다.

## 1. 실제 Base 상태 감사

Base current main에는 각 책임이 존재하지만 하나의 5단계 상태기계로 연결되어 있지 않다.

- `WORK_PROJECT_START_CANON_CHECKLIST.md`
  - 핵심 재미·핵심 시스템·SWOT·current stage·남은 작업·작업순서·정본 선교정을 소유한다.
- `PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md` + `grill-me-protocol.md`
  - 프로젝트 코어·플레이어 판타지·Core Loop·뾰족한 재미·MVP·차별점·Vertical Slice 위험 가설의 사용자 결정을 소유한다.
- Work v4.9 / v4.8 r5.4
  - 기획·벤치마킹·검수·Visual·Implementation Ready·Codex·play evidence·merge/readback을 소유한다.
- `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
  - 현재는 `Stage A Work preparation → Stage B Codex implementation → Stage C Work final review → user validation`의 3단계 실행 흐름이다.
- `designing-vertical-slices`
  - Vertical Slice를 대표 경험·목표 품질·시스템 연결·제작 파이프라인·실제 플레이 증거로 정의한다.

따라서 기능 누락보다 **단계 인터페이스와 완료 상태 명칭의 불명확성**이 문제다.

## 2. 프로젝트 정본 실검증

2026-08-27 다음 프로젝트 GitHub `AGENTS.md`, current state owner와 Project Notion Home을 fresh-read했다.

| 프로젝트 | current project 표현 | 5단계 관점 finding |
|---|---|---|
| MylittleBoat | core direction + visual production order + Codex integration + runtime check | 기획·요소 제작·구현은 있으나 독립 구현 전 검수 Gate가 사람에게 명확하지 않음 |
| OMENWARD | Decision/Active Context router + autonomous required images + runtime evidence | current Decision은 강하지만 공용 5단계 상태명이 없음 |
| Ten-Paces | `PLAN / BUILD / REVIEW` + Implementation Ready + Human evidence 분리 | Review가 구현 전·후를 모두 가리켜 사용자 2단계 `검수`와 충돌 가능 |
| urban-legend | `PLAN → BUILD → REVIEW`, Planning complete, runtime authorization 별도 | 기획 완료와 구현 허가의 경계는 강하지만 요소 제작 단계가 독립 상태가 아님 |
| Switchy Express | 기획/구현/package candidate/physical-human gates | 자동 package readiness와 사람 검증 분리는 강하지만 프로젝트 전용 상태명이 많음 |
| Tetris | production canon + consumer-first images + 독립 Human Evidence 계약 | Human 검증 경계는 강하지만 Work 1~4단계 공용 인터페이스가 없음 |
| GRIMOIRE | `MERGED_MAIN_AUTOMATED_VERTICAL_SLICE_READY → USER_VERTICAL_SLICE_VALIDATION_PENDING` | 4단계와 5단계의 분리를 가장 명확히 증명하는 현재 사례 |
| Blacksmith | PLAN Gate + research + TDD + review + implementation blocked | 기획·검수는 강하지만 3단계 요소 제작과 4단계 전환 상태가 공용화되지 않음 |
| Ninja Survival | PLAN/DoR/BUILD/verification/review/merge + release-near Human Slice | 전체 책임은 존재하지만 사용자의 5단계 명칭과 직접 대응하지 않음 |
| Coc-Fiction | 비게임 서사 production, Godot `NOT_APPLICABLE` | 공용 인터페이스는 game-only owner가 아니라 domain-adaptable이어야 함 |

Notion Homes는 사람용 North Star·핵심 루프·Visual·현재 evidence를 잘 보여주지만, Work 실행 5단계를 프로젝트마다 동일하게 표시하지 않는다. 프로젝트별 고유 Task/Decision/Gate를 Base 5단계로 강제 rename하는 것은 두 번째 정본과 migration churn을 만든다.

## 3. 확인된 문제

### P1. 현재 3단계 프로필이 사용자 요구 5단계를 압축한다

`Stage A Work preparation` 안에 기획·검수·요소 제작이 함께 들어 있다. 따라서 다음 경계가 약하다.

```text
기획 핵심 Decision 승인
!= 구현 전 검수 통과
!= 실제 요소 제작 완료
```

### P2. `검수`가 두 의미로 사용된다

- 구현 전에 기획·scope·feasibility·asset requirement를 검수하는 단계
- Codex 구현 뒤 실제 diff·runtime·build를 검수하는 단계

사용자 5단계에서 `2. 검수`는 **구현 전 생산 검수**로 고정하고, Codex 결과 최종검수는 4단계 closeout에 포함해야 한다.

### P3. routine 자동 승인이 핵심 공동기획까지 덮을 위험

현재 profile은 routine 권장안을 자동 승인한다. 그러나 사용자 최신 지시는 핵심 재미·Core Loop·핵심 시스템·차별점·Vertical Slice 가설을 Grill Me와 벤치마킹으로 함께 설계하라는 것이다.

```text
DELEGATED_ROUTINE_APPROVAL
!= CORE_PRODUCT_MEANING_APPROVAL
```

### P4. 자동화 완료와 Vertical Slice 완료가 혼동될 수 있다

현재 `AUTOMATED_VERTICAL_SLICE_READY`와 `READY_FOR_USER_VERTICAL_SLICE_VALIDATION`은 존재하지만, 사용자 검증 뒤의 최종 상태와 재진입 규칙이 공용 상태명으로 충분히 명확하지 않다.

### P5. 프로젝트별 표현을 강제 변경하면 정본 churn이 발생한다

프로젝트는 `PLAN/BUILD/REVIEW`, Task, Decision, package candidate, Human Gate 등 고유 상태를 소유한다. Base는 이를 교체하지 않고 **매핑 receipt**를 제공해야 한다.

## 4. 비교한 대안

| 대안 | 장점 | 실패 모드 | 판정 |
|---|---|---|---|
| 기존 3단계 유지 + 설명만 추가 | 변경 작음 | 기획/검수/요소 생성 경계가 계속 압축됨 | REJECT |
| 모든 프로젝트 정본을 동일 5단계 명칭으로 migration | 표면 통일 | 고유 Decision·Task·Gate 손실, 대량 churn, 두 번째 정본 | REJECT |
| Base에 5단계 공용 interface를 추가하고 프로젝트 상태를 mapping | 명확한 사용자 UX, 기존 owner 보존, 새 Work 재개 용이 | mapping·Gate contract와 회귀 테스트 필요 | ADOPT |

## 5. 채택 설계

```text
PHASE_1_PLANNING_CO_DESIGN
→ PHASE_2_PREPRODUCTION_REVIEW
→ PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
→ PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
→ PHASE_5_USER_VERTICAL_SLICE_VALIDATION
```

### Phase 1 — 기획·사용자 공동설계

필수 핵심 범위:

```text
project goal / player promise / pointed fun
core/session/meta loop
core systems / supporting systems
meaningful choices / tension / trade-off
reward / failure learning
emotional target / first-session memory
project differentiation / sales point
protected strengths / scope / non-scope
Vertical Slice fun·production·technical hypothesis
```

규칙:

- 새 프로젝트·새 핵심 Slice·Core 의미 변경은 `CORE_PLANNING_CO_DESIGN_REQUIRED`다.
- current canon과 실제 구현을 먼저 읽는다.
- decision-relevant benchmark와 성공·실패/혼합 사례를 조사한다.
- 중요한 선택은 최소 3개 materially distinct 대안을 비교한다.
- 저장소로 답할 수 없는 핵심 결정만 Grill Me로 한 번에 하나씩 묻는다.
- 이미 승인된 핵심 Decision은 다시 묻지 않는다.
- routine standing approval은 Phase 1 핵심 제품 의미를 자동 확정하지 않는다.

출력:

```text
CORE_PLANNING_DECISION_PACKET
PHASE_1_USER_CONFIRMED
```

### Phase 2 — 구현 전 검수

Phase 1 산출물을 다음 관점으로 재공격한다.

- 핵심 재미·선택·보상 연결
- scope와 대표성
- 기존 구현·재사용·기술 가능성
- UI/UX·정보 이해
- 데이터·save/schema·경제·밸런스
- Visual/Audio/VFX actual consumer와 coverage
- 권리·provenance·비용
- acceptance·test·runtime·rollback
- Codex 재작업 위험과 Work↔Codex 전환 수
- 프로젝트 정본 충돌과 untouched consumer

유효 finding이 core meaning을 바꾸면 Phase 1로 돌아간다. 검수 통과 전 serial asset production과 Codex implementation을 시작하지 않는다.

출력:

```text
REVIEWED_SLICE_PRODUCTION_CONTRACT
APPROVED_FOR_INGAME_ELEMENT_PRODUCTION
```

### Phase 3 — 이미지·사운드·UI·Data·VFX 등 Work 제작

Work가 가능한 비코딩 제품 입력을 한 번에 닫는다.

- actual-consumer Visual
- Audio/music/SFX 또는 권리 검증된 source/procedural spec
- UI/UX states·copy·flow
- data/state contract와 tunable range
- VFX/feedback requirement
- localization/accessibility readiness
- provenance/rights
- test/runtime/Hera scenario

Visual binary는 explicit local profile에서 project-local candidate → approved tracked asset + manifest → commit/push/remote readback을 따른다. Notion은 구조·Art Direction·사람용 상태 참고를 유지하며 binary upload는 필수가 아니다.

출력:

```text
WORK_PRODUCTION_INPUT_PACKET
READY_FOR_SINGLE_CODEX_WINDOW
```

### Phase 4 — Codex 구현·Machine QA·Work 최종 구현검수

한 Codex window에서 실제 product code·Scene·Resource·runtime wiring·test·build를 구현한다. 작은 finding마다 Work로 왕복하지 않고 consolidated packet으로 반환한다.

Phase 4 closeout에는 다음이 포함된다.

```text
Codex actual implementation
→ deterministic/import/parse/runtime/build QA
→ GUT/Hera or evidence-equivalent machine QA
→ Work actual diff/evidence final review
→ valid implementation correction
→ exact-head CI / safe merge / post-merge readback
→ downloadable internal build + validation packet
```

출력:

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

이 상태는 Vertical Slice 최종 완료 또는 Player Experience PASS가 아니다.

### Phase 5 — 사용자 실제 플레이 검증

사용자가 exact build를 실제로 실행하고 representative flow를 플레이한다.

최소 관찰:

- 시작·목표·다음 행동 이해
- 핵심 행동과 의미 있는 선택
- 결과·피드백·보상·실패 학습
- 시각·사운드·UI 가독성
- 조작·입력·피로·막힘
- 핵심 감정·기억·차별점의 방향성

판정:

```text
USER_VALIDATED_VERTICAL_SLICE_PASS
USER_VALIDATED_WITH_FOLLOWUP
REWORK_REQUIRED
BLOCKED_USER_VALIDATION
```

feedback이 core meaning을 바꾸면 Phase 1, 설계·가독성이면 Phase 2, 누락 자산이면 Phase 3, bug·runtime이면 Phase 4로 bounded reopen한다.

## 6. Vertical Slice 완료 정의

Unity 공식 학습 자료는 Vertical Slice를 더 큰 게임의 작동하는 일부로서 최종 게임이 어떻게 보이고 플레이될지를 시험하는 구간으로 설명한다. Unity production guidance는 짧은 gameplay를 의도한 시각 fidelity에 가깝게 만들고 이 시점부터 실제 performance profiling을 시작할 것을 권장한다. Base `designing-vertical-slices`는 대표 경험·목표 품질·시스템 연결·제작 파이프라인·실제 플레이 증거를 요구한다.

따라서 다음을 구분한다.

### `AUTOMATED_VERTICAL_SLICE_READY` — Phase 4 완료

- representative flow가 actual build에서 실행 가능
- core systems와 실제 consumer가 연결
- shipping-intent UI/Visual/Audio/VFX/feedback이 필요한 범위에서 존재
- player-facing critical placeholder 없음
- deterministic/runtime/build evidence
- exact build/commit identity
- downloadable launch route
- merge/readback·remaining machine work 0
- Human/Player evidence는 `NOT_RUN`

### `USER_VALIDATED_VERTICAL_SLICE` — Phase 5 완료

위 Phase 4 조건에 추가해:

- 사용자가 exact build를 실제 실행
- representative action→choice→result→feedback flow 완료
- blocking usability issue 0 또는 명시적 rework 판정
- 핵심 재미·감정·기억·차별점의 방향성에 사용자 판정
- feedback·finding·next decision 기록
- Canonical Reflection After Play

전체 게임의 모든 콘텐츠·최종 밸런스·모든 플랫폼·최종 localization·스토어/법적 출시 PASS는 Vertical Slice 완료 조건이 아니다. 현재 Slice가 약속한 대표 경험의 release-near/shipping-intent 품질과 사용자 검증이 조건이다.

## 7. 프로젝트 상태 매핑

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

- `PLAN/DoR/BUILD/REVIEW`는 해당 Gate의 실제 의미에 따라 1/2/4로 매핑한다.
- `AUTOMATED_VERTICAL_SLICE_READY`는 Phase 4 완료·Phase 5 대기다.
- `PLANNING_COMPLETE + runtime implementation unauthorized`는 Phase 1 완료 여부와 Phase 2/4 authorization을 별도 판정한다.
- narrative/non-game 프로젝트는 Phase 3·4를 domain production에 맞게 adapt하고 Godot 전용 evidence를 `NOT_APPLICABLE`로 둔다.

프로젝트 고유 상태명을 rename하거나 historical receipts를 일괄 migration하지 않는다.

## 8. 외부 벤치마크

- Unity Learn, 2D Roguelike: Vertical Slice는 더 큰 게임의 functioning part이며 final game의 look/play를 시험한다.
  - https://learn.unity.com/tutorial/66f53a14edbc2a0e75d4fe90
- Unity profiling guidance: production 초기에 intended final visual fidelity에 가까운 짧은 gameplay slice에서 profiling을 시작한다.
  - https://unity.com/blog/games/pick-up-these-helpful-tips-on-advanced-profiling
- Steamworks Playtest: 실제 플레이테스트 데이터를 별도 low-risk 배포로 수집할 수 있지만, 기능 존재만으로 evidence가 되지는 않는다.
  - https://partner.steamgames.com/doc/features/playtest
- Google Engineering Practices: self-contained small change는 검토·rollback·merge가 쉽고 누락을 줄인다.
  - https://google.github.io/eng-practices/review/developer/small-cls.html

## 9. 예상 구현

```text
templates/project-operations/WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md
templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md
templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_LOCAL_VISUAL_STARTER_PROMPT.md
docs/knowledge/cases/WORK_FIVE_PHASE_VERTICAL_SLICE_PROJECT_CANON_CASE.md
docs/superpowers/plans/2026-08-27-work-five-phase-vertical-slice.md
tests/test_work_five_phase_vertical_slice_contract.py
```

`WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`의 세부 packet·approval·QA·merge owner는 그대로 재사용하고, 새 계약은 사용자에게 보이는 5단계 interface와 phase transition만 소유한다.

## 10. 회귀 검증

- RED: current main에는 exact 5 phase·Grill Me core co-design·Phase 4/5 completion split이 없어 focused test 실패
- GREEN: 새 phase owner + router/starter routing
- existing core bundle, local Visual, safe Git/Godot, IRG, Human/Player evidence ceiling 비퇴행
- project-specific values가 active generic policy에 유출되지 않는 negative test
- exact-head current required workflows
- 최소 5회 full-scope adversarial review
- squash merge + post-merge main/file/workflow readback

## 11. 위험·제외

- 프로젝트별 Task/Decision/Gate rename 금지
- 전 프로젝트 Notion IA 대량 migration 금지
- 핵심 기획을 standing routine approval로 자동 확정 금지
- 사용자 검증 전 `USER_VALIDATED_VERTICAL_SLICE` 주장 금지
- 전체 게임 완료와 Vertical Slice 완료 혼동 금지
- non-game 프로젝트에 Godot 강제 금지
- 새 Skill/provider/dependency/유료 경로 추가 금지
- direct main/force/admin/ruleset bypass 금지

## 12. 롤백

구현 squash commit을 revert하고 router/starter에서 새 phase owner link를 제거한다. 기존 startup checklist, Grill Me owner, minimum-transition profile, local Visual owner와 프로젝트 고유 상태는 그대로 유지한다.
