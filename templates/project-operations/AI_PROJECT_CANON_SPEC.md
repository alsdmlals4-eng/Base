# AI Project Canon and Implementation Specification

> Status: `PROJECT_TEMPLATE`
> Authority: repository canonical Markdown
> Human derivative: `HUMAN_GDD_PDF_DERIVED_VIEW`
> Notion requirement: none by default

## 0. Canon identity

```yaml
project_id:
project_name:
canon_version:
source_commit:
last_approved_at:
last_approved_by:
project_agents_path: AGENTS.md
active_context_path: ACTIVE_CONTEXT.md
confirmed_decisions_path: CURRENT_CONFIRMED_DECISIONS.md
current_codex_handoff_path: docs/handoffs/CURRENT_CODEX_HANDOFF.md
asset_manifest_path: assets/ASSET_MANIFEST.json
supersedes:
```

## 1. Project definition and player value

### project_definition

- 한 문장 정의:
- 장르·플랫폼·대상 플레이 상황:
- 플레이어가 반복해서 하는 핵심 행동:
- 다른 게임과 구분되는 핵심 약속:

### player_outcome

- 플레이어가 이번 프로젝트/현재 목표에서 얻어야 하는 결과:
- 첫인상:
- 핵심 감정:
- 기억에 남아야 할 순간:
- 판매·차별 포인트:

### meaningful_choices

| Choice ID | 선택 상황 | 선택지 | 얻는 것 | 포기하는 것 | 정보와 피드백 | 장기 영향 |
|---|---|---|---|---|---|---|
| CHOICE-001 |  |  |  |  |  |  |

## 2. Protected direction

```yaml
protected_core:
protected_player_experience:
protected_rules:
protected_visual_identity:
protected_story_or_canon:
protected_approved_assets:
change_requires_user_decision:
```

- 현재 방향을 바꾸지 않는 범위:
- 기술 구현자가 자율 결정할 범위:
- `CHANGE_PROPOSAL`이 필요한 조건:

## 3. Core loop and full flow

### core_loop

```text
player intent
→ action / input
→ system resolution
→ readable feedback
→ consequence / reward / failure
→ next meaningful decision
```

### full_game_flow

| Flow ID | 진입 조건 | 화면·씬 | 플레이어 행동 | 시스템 처리 | 결과·피드백 | 다음 Flow |
|---|---|---|---|---|---|---|
| FLOW-001 |  |  |  |  |  |  |

### current_play_meaningful_slice

```yaml
work_slice_id:
entry_state:
player_action_and_choice:
expected_player_outcome:
exit_state:
approved_scope:
explicit_non_scope:
```

## 4. core_systems_and_content

각 시스템은 기능 목록이 아니라 플레이어 판단·감정·보상과 연결한다.

### System card

```yaml
system_id:
name:
player_purpose:
trigger:
inputs:
state:
rules:
outputs:
feedback:
meaningful_choice:
reward_or_consequence:
content_consumed:
dependencies:
edge_cases:
implementation_status:
evidence_ceiling:
```

### Content catalog

| Content ID | 유형 | 플레이 역할 | 획득·등장 조건 | 시스템 소비처 | 변형·상태 | 구현 상태 |
|---|---|---|---|---|---|---|
| CONTENT-001 |  |  |  |  |  |  |

### Progression and economy

- 성장 단위:
- 자원 source/sink:
- 선택 압력과 trade-off:
- 실패 복구:
- snowball/softlock 방지:
- 수치 정본 경로:
- scenario test 경로:

## 5. UX/UI and information architecture

### ui_ux_flow

| Screen ID | 화면 목적 | 진입 | 핵심 정보 | 주요 조작 | 상태·오류 | 다음 화면 | runtime consumer |
|---|---|---|---|---|---|---|---|
| SCREEN-001 |  |  |  |  |  |  |  |

### Interaction states

- default:
- hover/focus:
- pressed/selected:
- disabled/locked:
- warning/error:
- loading/empty:
- success/reward:
- accessibility alternatives:

### Readability contract

- 플레이어가 설명 없이 알아야 하는 것:
- 정보를 보여주는 시점:
- 우선순위와 visual hierarchy:
- controller/keyboard/touch 차이:
- 해상도·safe area·localization 제약:

## 6. Data and state semantics

### Data owner map

| Data ID | 의미 | 저장 형식 | canonical path | runtime consumer | migration/version | validation |
|---|---|---|---|---|---|---|
| DATA-001 |  |  |  |  |  |  |

### State model

```yaml
states:
transitions:
invariants:
invalid_states:
recovery_behavior:
save_load_boundary:
```

## 7. actual_asset_consumers

이미지는 종류별 목록이 아니라 실제 화면·씬·오브젝트·행동·상태에서 역산한다.

| Asset ID | repository_path | actual_consumer | required states/variants | approval_status | version | sha256 | implementation_status |
|---|---|---|---|---|---|---|---|
| ASSET-001 |  |  |  |  |  |  |  |

### Asset rules

- candidate/reference는 runtime asset과 구분한다.
- 승인 전 생성물은 구현 입력으로 사용하지 않는다.
- 실제 소비되지 않는 설명용 시트는 runtime asset 완료율에 포함하지 않는다.
- UI 상태 패밀리, 방향·애니메이션·피격·사망 등 필요한 상태 전체를 추적한다.
- 사운드·VFX도 trigger, consumer, 상태와 구현 경로를 기록한다.
- large editable master는 Library/local source에 둘 수 있으나 runtime input은 repository path와 manifest readback을 가져야 한다.

## 8. implementation_contract

### Meaning contract for Codex

```yaml
source_planning_commit:
work_slice_id:
approved_scope:
explicit_non_scope:
protected_rules:
required_data_and_inputs:
ui_ux_flow:
asset_audio_dependencies:
acceptance_criteria:
review_evidence_expected:
```

### Technical autonomy

Codex가 current repository truth에서 결정:

- Node/Scene/Resource 분해;
- class/function 이름과 내부 구조;
- 테스트 가능성을 위한 bounded refactor;
- 현재 의미를 보존하는 성능·안정성 처리;
- Godot API와 실제 프로젝트 구조에 맞는 구현 방법.

사용자 결정 또는 `CHANGE_PROPOSAL` 필요:

- 코어·경제·주요 UX·서사·Art Direction 의미 변경;
- 승인 asset 교체;
- 플랫폼·비용·보안·저장 호환성 경계 확대;
- explicit_non_scope 편입.

## 9. acceptance_and_evidence

| Claim ID | Acceptance | Automated evidence | Runtime evidence | Play/UX evidence | Current state | Evidence ceiling |
|---|---|---|---|---|---|---|
| AC-001 |  |  |  |  | NOT_RUN |  |

구분:

- static/contract PASS;
- automated test PASS;
- runtime PASS;
- visual/audio consumption PASS;
- UX/player PASS;
- release readiness.

하나가 다른 하나를 자동 증명하지 않는다.

## 10. Risks, blockers, and explicit_non_scope

### blockers

| Blocker ID | 원인 | 영향 | 해제 증거 | owner | 상태 |
|---|---|---|---|---|---|
| BLOCK-001 |  |  |  |  |  |

### risks_and_revisit_conditions

| Risk ID | 위험 | 감지 신호 | 완화 | 재검토 시점 |
|---|---|---|---|---|
| RISK-001 |  |  |  |  |

### explicit_non_scope

- 이번 Slice에서 만들지 않는 것:
- 미래 후보이지만 현재 구현하지 않는 것:
- 별도 승인 없이는 변경하지 않는 것:

## 11. Decision and supersession log

| Decision ID | 결정 | 이유 | 대안 | 승인 상태 | source commit | supersedes |
|---|---|---|---|---|---|---|
| DEC-001 |  |  |  |  |  |  |

## 12. Handoff and completion snapshot

```yaml
current_goal:
current_stage:
completed_scope:
remaining_required_work:
implementation_head:
validated_evidence:
not_run_or_blocked:
rollback:
next_single_milestone:
```

이 문서는 구현 상태를 과장하지 않는다. 계획된 의미는 `APPROVED_FOR_IMPLEMENTATION`, 실제 구현은 repository/runtime evidence가 있을 때만 구현·검증 상태로 승격한다.
