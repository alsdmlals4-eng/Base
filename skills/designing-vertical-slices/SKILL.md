---
name: designing-vertical-slices
description: Use when one playable segment must prove core experience, target quality, system integration, production pipeline, playtest, accessibility, or performance.
---

# Designing Vertical Slices

## Core principle

게임 전체를 얕게 만드는 대신, 핵심 경험을 대표하는 작은 구간을 최종 품질에 가까운 깊이로 연결해 **재미·품질·제작성·실제 플레이 증거**를 동시에 검증한다.

`RELEASE_NEAR_VERTICAL_SLICE_FIRST`: 기획·검수 뒤 플레이어 경험을 판정하는 첫 인간 플레이 테스트는 짧더라도 release-near/shipping-intent Vertical Slice에서 수행한다.

`SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED`: 실제 게임 사용 후보인 UI/UX, 이미지·아트, 애니메이션/연출, 음악·효과음, VFX/피드백, 핵심 시스템·데이터·콘텐츠가 한 대표 흐름에서 서로 연결되어야 한다. 플레이어가 보는·듣는·조작하는 경로에는 임시 `player-facing placeholder`나 dummy presentation을 남기지 않으며, 해당 요소가 이후 튜닝·교체될 수 있어도 현재 Slice 자체는 production-candidate 품질이어야 한다.

`SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE`: 시스템-only PoC는 기술 가능성·알고리즘·성능·호환성 같은 좁은 질문의 `TECHNICAL_SPIKE_INTERNAL_ONLY` evidence다. 재미·몰입·가독성·첫인상·판매력·감정·기억·전체 UX의 PASS 근거로 사용하지 않는다.

`EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT`: shipping-intent 품질을 위해 무조건 새로 만들지 않는다. 승인된 프로젝트 자산·기존 구현·검증된 라이브러리/도구를 먼저 조사하고 프로젝트 정체성에 맞게 `ADOPT / ADAPT / REJECT`한다.

`PLAYER_VALUE_TRACE_REQUIRED`: Slice 범위를 정하기 전에 아래 추적을 고정한다. 기능 존재나 화면 완성도를 플레이어 가치의 대리 지표로 사용하지 않는다.

```yaml
player_promise:
meaningful_choice:
expected_experience:
research_question:
observable_signal:
evidence_ceiling:
slice_acceptance:
```

`evidence_ceiling`은 현재 확보 가능한 증거가 어디까지 주장할 수 있는지의 상한이다. 자동 테스트·정적 문서·UI 렌더만 있으면 사람의 이해·감정·고민·기억을 PASS로 올리지 않는다. `slice_acceptance`는 관찰 신호와 다음 개발 결정을 연결하며, 필요한 사람 플레이가 미실행이면 해당 경험 판정은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 남긴다.

## Distinguish

| 형태 | 검증 대상 |
|---|---|
| Prototype | 핵심 가설 또는 기술 가능성 |
| Vertical Slice | 대표 경험, 목표 품질, 시스템 연결, 제작 파이프라인, 실제 플레이 증거 |
| MVP | 최소 전체 제품 구조 |
| Demo | 외부 플레이어를 설득하는 공개 구간 |

## Modes

- `slice-contract`: 핵심 가설, 대표 구간, 포함·제외 범위와 다음 결정을 고정한다.
- `quality-bar`: 조작·정보·아트·UI·사운드·접근성·성능의 관찰 가능한 목표 품질을 정한다.
- `pipeline-proof`: 기획→데이터→자산→구현→QA→문서화 흐름과 반복 생산 비용을 실제로 통과시킨다.
- `playtest-evidence`: 내부·외부 테스터 집단, 과제, 피드백 채널, 행동 이벤트·퍼널과 관찰 결과를 수집한다.
- `decision-gate`: 재미·품질·제작성 증거로 확장·재작업·보류·중단을 판정한다.

## Required inputs

```yaml
core_player_promise_and_loop:
highest_risk_fun_technical_production_hypotheses:
current_system_asset_and_pipeline_state:
target_platform_quality_time_and_team_constraints:
representative_and_worst_case_play_flow:
visual_requirement_gate:
  selected_requirement_ids:
  p0_p1_required:
  p2_needed_for_consistency:
  deferred_p3:
accessibility_and_performance_targets:
playtest_contract:
  build_and_version:
  tester_segment_and_prior_exposure:
  recruitment_and_access:
  tasks_or_play_window:
  observation_points:
  feedback_channel:
  telemetry_events_and_funnel:
  success_failure_stop:
```

## Process

### 1. Slice contract

1. `PLAYER_VALUE_TRACE_REQUIRED`의 플레이어 약속·의미 있는 선택·예상 경험·연구 질문·관찰 신호·증거 상한·Slice acceptance를 먼저 고정한다.
2. 한 문장 핵심 가설과 이 구간이 바꿀 개발 결정을 정한다.
3. 진입→행동→판단→반응→결과→기록·복귀가 연결되는 대표 구간을 고른다.
4. 핵심 세일즈포인트와 일반 플레이를 함께 보여주는지 확인한다.
5. 포함 시스템·콘텐츠·아트·UI·사운드·데이터를 최소화한다.
6. `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`에서 이 구간에 필요한 시각 requirement를 고른다. 기본적으로 핵심 흐름을 막는 `P0 BLOCKER`, 이해·세일즈포인트에 필요한 `P1 CLARITY`, 반복 제작성을 증명하는 데 필요한 일부 `P2 CONSISTENCY`만 포함하고, P0~P2를 증명하기 전 `P3 DELIGHT` 대량 제작은 보류한다.
7. 전체 분량, 모든 캐릭터, 장기 경제 등 제외 범위를 고정한다.
8. 성공·실패·미검증 시 다음 개발 결정을 미리 정의한다.

`Visual Requirement Gate`는 Slice 자산 목록의 새 권위를 만들지 않는다. 선정된 `requirement_id`를 기존 Art/UX 문서와 자산 제작·검수 경로가 소비한다.

### 2. Quality bar

조작감, 정보 전달, 아트, 연출, 사운드, 접근성, 성능의 품질 기준을 관찰 가능하게 쓴다.

```yaml
controls_and_feedback:
readability_and_information:
art_animation_audio:
accessibility_barriers_and_alternatives:
target_hardware_frame_time_memory_loading:
content_and_system_integrity:
save_resume_error_recovery:
```

“완성도 높음”, “부드러움”, “접근 가능함”처럼 측정할 수 없는 표현만으로 통과시키지 않는다.

### 3. Pipeline proof

기획→데이터→자산→구현→QA→문서화의 제작 흐름을 실제로 한 번 통과시킨다.

- 각 단계의 입력·출력·소유자·도구·검증·재작업 원인을 기록한다.
- 대표 자산과 일반 반복 자산을 모두 포함한다.
- 포함된 자산은 연결 `requirement_id`, 역할, 우선순위, disposition과 모순되지 않아야 한다.
- 임시 자산만으로 목표 품질을 증명하지 않는다.
- 제작 시간보다 병목·대기·반복 가능성·자동화 후보를 우선 기록한다.
- 같은 유형의 두 번째 콘텐츠를 만들 수 없는 구조라면 Production 준비로 판정하지 않는다.

### 4. Playtest evidence

`analyzing-and-refining-game-concepts: playtest-and-experiment`에서 정의한 가설과 표본 계약을 이어받는다.

- 빌드·버전·대상 플레이어·이전 노출을 고정한다.
- 내부 팀의 숙련된 플레이와 목표 플레이어의 첫 경험을 구분한다.
- 외부 테스트는 피드백 위치와 원하는 질문을 게임 안팎에 명확히 안내한다.
- 기존 지식이 결과를 오염시키면 새로운 테스터 집단으로 반복한다.
- 관찰된 행동, 이벤트·퍼널, 인터뷰·설문 반응을 분리한다.
- 핵심 흐름의 진입·이해·선택·실패·보상·복귀 단계와 소요 시간·이탈을 기록한다.
- 플레이어가 제안한 해결책보다 혼란·기대·행동 이유·중단 지점을 먼저 분석한다.
- 접근성 장벽과 목표 플랫폼 성능은 `reviewing-and-validating-project-changes`의 전문 mode로 독립 검증한다.

Steam Playtest 같은 분리된 테스트 배포를 사용할 수 있지만, 테스트 기능 존재만으로 플레이 증거가 만들어지는 것은 아니다. 피드백 채널·표본·빌드·판정 기준을 별도 계약한다.

### 5. Decision gate

```text
재미 가설
+ 목표 품질
+ 접근성·성능
+ 시스템 연결
+ 제작 반복성
+ 플레이테스트 행동·반응
→ EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP
```

- `EXPAND`: 대표 경험과 반복 생산 흐름이 증명됐다.
- `REWORK`: 핵심 가설은 유효하지만 품질·장벽·파이프라인 문제가 명확하다.
- `REPEAT_SLICE`: 표본·구간·가설이 대표적이지 않아 다른 조건으로 다시 검증한다.
- `HOLD`: 외부 의존성·환경·비용 때문에 판정을 보류한다.
- `STOP`: 핵심 재미·제작성·제품 약속이 함께 성립하지 않는다.

판정은 `PLAYER_VALUE_TRACE_REQUIRED`의 `observable_signal`, `evidence_ceiling`, `slice_acceptance`를 넘어서지 않는다. 기술·UI·파이프라인 증거만 통과한 상태에서 사람 경험을 근거로 `EXPAND`하지 않는다.

## Platform and asset proof gate

공용 기준은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`다. Vertical Slice는 대표 콘텐츠와 대표 자산을 포함하므로 목표 등급·권리·참조 독립성의 조기 증거도 제공해야 한다.

- `content_rating_target`과 `target_audience`를 분리한다.
- 청소년이용불가·18+를 피하기 위해 대표 공포·전투·언어·온라인·AI 콘텐츠를 숨기지 않는다.
- shipping·store·trailer에 사용하는 대표 자산은 `ASSET_RIGHTS_AND_PROVENANCE_RECORD`와 연결한다.
- 직접 포함 자산의 `distribution_in_game_build`가 확인돼야 한다.
- `REFERENCE_TO_ORIGINAL`은 원본이 build에 없고 `reference_brief`, `final_asset_record`, `reference_similarity_status`가 있어야 한다.
- open-source NOTICE·attribution·source, AI terms·input rights, 외주·음성 계약 범위를 확인한다.

대표 자산이 `UNKNOWN`, 참조 원본이 build에 존재하거나 목표 등급이 콘텐츠 은폐에 의존하면 `pipeline-proof`와 Production proof는 `RELEASE_BLOCKED_UNVERIFIED`다. 이 상태에서는 `EXPAND`를 선택하지 않는다.

## Output contract

- 검증 목적과 핵심 가설
- `player_promise → meaningful_choice → expected_experience → research_question → observable_signal → evidence_ceiling → slice_acceptance` 추적
- 목표 플레이어 경험
- 대표 플레이 흐름과 예상 시간
- 포함·제외 범위
- `Visual Requirement Gate`의 Slice용 `requirement_id`·P0/P1·필요 P2·보류 P3
- 시스템·콘텐츠·자산 목록
- 조작·정보·아트·UI·사운드·접근성·성능 품질 기준
- 제작 파이프라인·병목·반복 생산 비용
- 기술·콘텐츠·플랫폼 위험
- 목표 등급·타깃 연령·대표 콘텐츠 위험
- 대표 자산 권리·출처·참조 독립 제작 증거
- 테스터 집단·빌드·과제·피드백 채널
- 이벤트·퍼널·행동·자기보고 결과
- 성공·실패·중단 기준
- `EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP` 판정
- 후속 개발 결정

## Definition of Done

- 처음부터 끝까지 플레이 가능한 대표 구간이다.
- 플레이어 약속·의미 있는 선택·예상 경험이 관찰 신호와 Slice acceptance로 추적된다.
- 핵심 세일즈포인트와 일반 반복 플레이를 함께 검증한다.
- 목표 품질이 관찰 가능한 기준과 실제 결과로 대조됐다.
- 핵심 정보·입력·시간·난이도에서 주요 접근성 장벽을 확인했다.
- 목표 플랫폼의 대표·최악 장면 성능을 예산과 비교했다.
- 실제 제작 파이프라인을 통과하고 다음 콘텐츠 반복 가능성을 확인했다.
- 대표 자산의 제품 포함 권리와 참조 독립 제작 상태가 확인됐다.
- 등급 전략이 대표 콘텐츠를 숨기지 않고 프로젝트 코어와 맞는다.
- 내부·외부 플레이테스트의 빌드·표본·행동·자기보고가 분리 기록됐다.
- 사람 경험 판정이 `evidence_ceiling`을 넘지 않는다.
- 결과가 다음 개발 결정으로 연결됐다.

## Failure conditions

- 기능 목록만 있고 처음부터 끝까지 플레이할 수 없음
- 플레이어 약속·의미 있는 선택과 관찰 신호의 연결 없이 기능/화면 존재만 Slice acceptance로 사용함
- `Visual Requirement Gate` 없이 “보여주면 좋을 것”인 자산을 Slice 범위에 누적함
- P0/P1 미검증 상태에서 P3 장식 제작을 우선함
- 특수 보스전처럼 일반 제작성을 대표하지 않는 구간
- 임시 자산만 사용해 목표 품질을 검증할 수 없음
- 전체 게임 분량을 슬라이스에 포함
- “재미있다”, “완성도 높다”만 있고 관찰 기준이 없음
- 제작 시간과 반복 생산 가능성을 기록하지 않음
- 내부 개발자 반응만으로 목표 플레이어 검증을 대체함
- 빌드·버전·표본·피드백 채널 없이 리뷰·감상을 모음
- 자기보고만으로 실제 행동을, 퍼널만으로 감정·원인을 단정함
- 자동 테스트·정적 문서·UI 렌더만으로 사람 이해·감정·기억을 PASS 처리함
- 평균 FPS나 옵션 존재만으로 성능·접근성 통과를 주장함
- 참조 원본이 build에 포함되거나 필수 권리가 `UNKNOWN`인데 Production proof를 주장함
- 등급 설문에서 대표 콘텐츠를 숨겨 낮은 등급을 목표로 함

## Validation scenarios

1. 카드 전투 게임은 카드 획득→선택→사용→적 반응→보상→덱 상태 기록까지 한 전투 구간으로 연결한다.
2. 조사 게임은 사건 진입→관찰→규칙 추론→위험 선택→기록·회수 결과까지 연결한다.
3. Prototype 결과가 좋더라도 아트·UI·사운드·접근성·성능·파이프라인이 검증되지 않으면 Vertical Slice 완료로 표시하지 않는다.
4. 상위 능력·특수 장면·보너스 결말이 선택적 하이라이트라면 보유·미보유 양쪽 경로가 최종 구간에 진입하고 정상 완료되는지 검증한다.
5. 대표 자산의 권리·출처·참조 독립 제작이 미확인되면 `RELEASE_BLOCKED_UNVERIFIED`로 남긴다.
6. 사람 플레이 없이 자동 검증만 끝났다면 기술·UI·파이프라인 상태만 갱신하고 `PLAYER_EXPERIENCE_EVIDENCE`는 `NOT_RUN`으로 유지한다.

## Applied case — 선택적 하이라이트와 정상 완주 경로

한 대회형 프로젝트는 높은 성과와 성장 운으로 최종전 직전에 대표 상위 능력을 조기 해금하게 설계했다. 이 능력은 공개 데모의 기억점이지만 모든 회차에 보장되지 않았다.

다음 세 접근을 비교했다.

- 하이라이트 필수: 대표 장면은 보장하지만 기본 루프와 성장 선택을 진행 게이트로 왜곡한다.
- 하이라이트 제거: 제작 범위는 줄지만 상위 품질과 장기 성장 약속을 검증하지 못한다.
- 선택적 하이라이트: 획득하면 새 선택과 연출을 제공하되, 미획득 회차도 기존 빌드와 판단으로 정상 완주한다.

채택한 완료 기준은 다음과 같다.

```text
보유 경로
- 신규 선택과 연출이 작동한다.
- 사용을 강제하지 않는다.
- 핵심 판단을 자동 정답으로 대체하지 않는다.

미보유 경로
- 같은 최종 구간에 정상 진입한다.
- 기존 시스템으로 공략 가능하다.
- 결말과 다음 목표가 완전하게 전달된다.
```

이 패턴은 특수 능력뿐 아니라 관계 장면, 추가 반전, 보너스 동료, 확장 후일담에도 적용할 수 있다. 단, 해당 하이라이트 자체가 제품의 핵심 조작이거나 반드시 전달해야 하는 사실이면 선택 보상으로 두지 않는다.

관련 사례: `docs/knowledge/cases/TEN_PACES_OPTIONAL_HIGHLIGHT_VERTICAL_SLICE_CASE.md`

References and template:

- `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`
- `skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md`
- `templates/planning/VERTICAL_SLICE_PLAN.md`

## Cloud Run backend runtime evidence

`docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`를 소비하는 Vertical Slice는 실제 배포 흐름에서 persistence, reconnect, duplicate submission, dependency failure, rollback과 목표 환경을 검증한다. 정적 문서만으로 `RUNTIME_VERIFIED`를 선언하지 않는다.

## Entitlement and integrity representative flow

`docs/knowledge/game-development/GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md`를 소비하는 Vertical Slice는 정상 entitlement, offline/grace, provider outage, device/account recovery, request replay와 false-positive remediation을 대표 흐름으로 검증한다. 실제 sandbox 근거가 있을 때만 `PLATFORM_SANDBOX_VERIFIED`를 선언한다.
