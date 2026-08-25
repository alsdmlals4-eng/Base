# P06 · Godot, Runtime & Technical Toolchain — Context Pack

## 현재 실행 계약
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

이 Part는 semantic responsibility / learning / validation checkpoint다. 현재 coordinator가 다른 Part/CP0의 검증된 오류·충돌·누락을 발견하면 다른 Part라는 이유만으로 보류하지 않고 `CROSS_PART_CHANGE`로 owner를 기록해 직접 수정할 수 있다. 단, 다른 독립 open/draft/ready PR·branch·worktree는 `ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`에 따라 read-only다.


## 역할
Godot authoring/runtime/debugging, addon/plugin 평가, editor/runtime adapter, QA technical tooling과 로컬 실행환경을 책임진다.

## 핵심 Skill
`diagnosing-game-engine-runtime-failures`, `evaluating-godot-assets-and-plugins-before-creation`.

## 중요 규칙
HiGodot single authority when adopted, Existing Solution First, actual runtime evidence before PASS, project-dedicated environment, no authoring bypass.

## Runtime UI acceptance hardening

외부 runtime-QA 도구가 semantic UI tree 또는 접근 가능한 UI identity를 제공하면 새 provider를 추가하지 않고 기존 P06/Hera live-QA 경계에 다음 provider-neutral 증거 계약만 흡수한다. 현재 provider가 이 surface를 제공하지 않으면 강제로 설치·교체하지 않고 해당 semantic 검증만 `NOT_CONFIGURED` 또는 `NOT_RUN`으로 남긴다.

- `SEMANTIC_UI_TARGET_BEFORE_COORDINATE`: UI acceptance의 대상 identity는 가능한 경우 `stable id → role+name/text+scope/state` 순으로 좁혀 **정확히 하나**를 선택한다. strict query가 0개 또는 복수 후보를 반환하면 `EXACTLY_ONE_OR_FAIL`이며 임의 first-match로 통과시키지 않는다. text/name 기반 selector는 locale·copy 변경에 민감하므로 locale을 evidence context에 결합하고 stable id보다 강한 identity로 과장하지 않는다.
- `COORDINATE_FALLBACK`: semantic identity가 실제 provider에서 관측되지 않거나 좌표 자체가 검증 대상일 때만 사용한다. 좌표 fallback 증거는 platform·resolution·renderer/layout context에 결합하고 layout 변화에도 안정적인 semantic proof로 승격하지 않는다.
- `ACTION_DISPATCH_IS_NOT_COMPLETION`: click/key/input 요청이 accepted·queued·sent 됐다는 사실은 acceptance completion이 아니다. 실제 host/runtime이 action을 처리했다는 관측과 **그 뒤 fresh runtime state/event가 기대 결과를 만족했다는 별도 assertion**이 필요하다. 둘 중 하나를 관측할 수 없으면 `INCONCLUSIVE_NOT_PASS`다.
- semantic selector를 만들기 위해 사용자-facing 의미·게임 규칙·접근성 label을 임의 변경하지 않는다. 기존 identity로 충분하지 않아 product instrumentation 변경이 필요하면 일반 persistent-authoring 변경으로 취급해 diff·검증·승인 경계를 따른다.
- `STRUCTURED_STATE_BEFORE_SCREENSHOT`와 `WALL_CLOCK_APPROX_REPLAY_IS_NOT_DETERMINISTIC_STATE_REPLAY`는 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`의 기존 정본을 재사용한다. semantic targeting은 screenshot을 금지하지 않고, semantic recording도 seed/frame/state causality 검증 없이 deterministic replay가 되지 않는다.

```yaml
runtime_ui_step:
  target:
    strategy: STABLE_ID | ROLE_AND_NAME | TEXT_AND_STATE | COORDINATE_FALLBACK
    selector:
    expected_count: 1
    locale_when_textual:
  action:
  completion:
    dispatch_ack_is_completion: false
    host_observation_required: true
    expected_state_or_event:
  coordinate_fallback_context:
    platform:
    resolution:
    renderer_or_layout_identity:
```

## 핵심 Module
Authoring Authority → Runtime Diagnostics → Addon Evaluation → Adapter → QA Technical Tooling → Local Execution.

## 경계
Part 경계는 수정 금지선이 아니라 semantic owner 지도다. 다른 Part/CP0 finding도 현재 coordinator가 증거와 검증 경로를 확보하면 직접 수정한다. 다른 독립 활성 workstream만 read-only로 보호하며, 실제 조정 blocker만 `CROSS_PART_CHANGE_REQUEST`로 남긴다.

## 우선 공격 대상
중복 writer, process 존재를 readiness로 오판, 사용자 PC에서 실행하지 않은 테스트 PASS, 불필요 addon/tool, QA/local tool unique 기능 없는 잔존, 좌표/이미지 first UI selector로 인한 layout-brittle 테스트, action dispatch acknowledgement를 실제 gameplay 결과로 오판하는 false PASS.

## 검증/완료
Godot focused tests와 가능한 실제 runtime evidence를 분리 보고. 최소 5회 전체 적대적 개선 후 clean까지.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P06_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: GAME_DEVELOPMENT, CODE_ENGINEERING.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.