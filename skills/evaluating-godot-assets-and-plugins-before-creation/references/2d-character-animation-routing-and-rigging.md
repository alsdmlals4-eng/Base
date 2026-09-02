# 2D Character Animation Routing and Rigging

## 역할과 경계

이 문서는 2D 캐릭터·생물·초상·전투 유닛의 애니메이션 제작 방식을 정하기 위한 `evaluating-godot-assets-and-plugins-before-creation`의 조건부 reference다. 특정 상용 제품을 기본 의존성으로 지정하지 않고, 실제 consumer와 프로젝트 제약을 기준으로 프레임·Godot 내장 리그·외부 런타임·베이크 경로를 비교한다.

```text
MINIMUM_MATERIALLY_DISTINCT_ALTERNATIVES: 3
FRAME_DEFAULT_UNLESS_EVIDENCE
SPINE_CANDIDATE_NOT_DEFAULT_DEPENDENCY
NO_AUTOMATIC_PURCHASE_INSTALL_OR_FLEET_ROLLOUT
```

이 reference는 새 Skill, 두 번째 자산 정본, 애니메이션 런타임, 구매 승인 또는 모든 프로젝트 일괄 도입 권한이 아니다. Base의 retired Sprite Animation Studio를 재활성화하지 않는다. 프로젝트의 최신 `AGENTS.md`, Visual/Asset owner, 실제 Scene·Resource·code·test·runtime과 채택된 Base 계약이 우선한다.

## 1. 먼저 해결할 플레이어 문제

도구 이름보다 플레이어가 실제로 보게 될 가치와 반복 제작 병목을 먼저 고정한다.

```yaml
actual_consumer:
consumer_surface:
player_value:
camera_scale:
screen_time:
concurrent_instance_peak:
animation_count:
direction_count:
outfit_variant_count:
weapon_attachment_count:
expression_variant_count:
requires_continuous_deformation:
requires_extreme_smear_or_redraw:
silhouette_priority:
target_platforms: []
performance_budget:
current_asset_and_animation_path:
```

`actual_consumer`가 없거나 장식적 미래 가능성만 있으면 새 리그·외부 런타임·구매를 시작하지 않는다. 기존 승인 자산, `AnimatedSprite2D`·`SpriteFrames`, `AnimationPlayer`, `Skeleton2D`·`Bone2D`, 현재 addon과 실제 사용 경로를 먼저 조사한다.

## 2. 비교할 네 경로

| Route | 기본 적합 조건 | 핵심 이익 | 주요 비용·실패 조건 |
|---|---|---|---|
| `FRAME` | 픽셀 아트, 강한 키 포즈·스미어·형태 재설계, 동작·변형 수가 작음, 다수 동시 개체 | 최종 실루엣 통제, 단순한 Godot 소비, 외부 런타임 없음 | 방향·상태·의상 증가 시 프레임·Atlas 제작량과 메모리 증가 |
| `GODOT_NATIVE_RIG` | 파츠 기반 캐릭터, 단순한 연속 변형, 외부 도구 없이 엔진 통합이 중요 | 무료·내장, `Skeleton2D`/`Bone2D`와 Godot 애니메이션·효과 통합 | 리깅·가중치 authoring UX, 복잡한 Skin/Attachment 제작 효율, exact Godot 버전별 동작을 실제 검증해야 함 |
| `EXTERNAL_RIG_RUNTIME` | 화면에 오래 보이는 소수 핵심 캐릭터, 동작·의상·무기·표정 재사용이 큼, 런타임 혼합이 실제 필요 | 전문 리깅·Skin·Attachment·mesh 변형과 동적 조합 | 유료/외부 라이선스, version lock, native dependency, export·플랫폼·성능·제거 비용 |
| `EXTERNAL_RIG_BAKED` | 외부 리그의 제작 재사용은 유용하지만 다수 개체·모바일·단순 런타임이 중요 | 제작은 리그로 반복 절감, 제품은 `SpriteFrames` 등 단순 경로 유지 | 런타임 Skin/혼합 상실, 베이크·Atlas 크기 증가, source→export 계보 관리 필요 |

비교표의 수만 채우기 위한 허수 대안을 만들지 않는다. 최소 `FRAME`, `GODOT_NATIVE_RIG`, 외부 리그의 `RUNTIME` 또는 `BAKED`를 같은 consumer와 같은 기준으로 대조하고, 네 경로 중 적용 불가능한 경로는 증거와 함께 `NOT_APPLICABLE`로 둔다.

## 3. Route 선택 규칙

### `FRAME`

다음에 기본값으로 유지한다.

- 픽셀 그리드·수작업 윤곽·프레임별 비율 변화가 정체성이다.
- 공격 스미어, squash/stretch, 순간적인 신체 재설계가 중요하다.
- 화면에 작은 유닛이 많이 등장하고 동시 인스턴스가 많다.
- 상태와 방향 수가 제한돼 있고 장비·의상 교체가 적다.
- 기존 승인 프레임·Atlas가 이미 목표 품질과 성능을 충족한다.

### `GODOT_NATIVE_RIG`

다음에 먼저 시험한다.

- 호흡, 고개, 시선, 옷자락처럼 단순하고 지속적인 변형이 필요하다.
- 소수 파츠와 제한된 bone hierarchy로 충분하다.
- 외부 라이선스·custom runtime 없이 Godot 안에서 효과·사운드·속성과 함께 authoring하는 이익이 크다.
- `Skeleton2D`, `Bone2D`, `Polygon2D`, 필요 시 exact-version IK/modification API를 샘플 Scene에서 검증할 수 있다.

Godot 4.7의 공식 2D skeleton tutorial은 페이지 자체가 업데이트 지연 가능성을 경고하므로, tutorial 문구만으로 호환성을 확정하지 않는다. 현재 프로젝트의 exact Godot class API와 실제 Scene import·edit·runtime evidence를 사용한다.

### `EXTERNAL_RIG_RUNTIME`

다음 조건을 모두 만족할 때만 `TRIAL_APPROVED` 후보가 된다.

- 실제 player-facing consumer가 있고 화면 체류 시간이 충분하다.
- 동작·Skin·Attachment·표정 반복량이 초기 리깅 비용을 상쇄한다.
- 런타임에서 동적 혼합·교체가 필요하며 베이크로는 가치가 사라진다.
- 목표 플랫폼의 native binary·export template·업데이트·rollback을 유지할 수 있다.
- `FRAME`과 `GODOT_NATIVE_RIG` 기준선보다 품질·제작 시간·메모리·frame time의 장기 총비용이 낫다는 시험 계획이 있다.

### `EXTERNAL_RIG_BAKED`

다음에 우선 검토한다.

- 제작 단계의 공통 리그·pose 재사용은 크지만 제품 런타임 의존성은 원하지 않는다.
- 일반 병력·군중처럼 concurrent_instance_peak가 높다.
- 모바일·저사양·다중 플랫폼에서 단순한 texture animation이 더 예측 가능하다.
- 장비·의상 조합이 런타임 중 바뀌지 않거나 제한된 variant를 미리 베이크할 수 있다.

## 4. Rig-ready source art 계약

리그 경로 가능성이 있으면 완성 평면 일러스트를 만든 뒤 억지로 절단하지 않는다. 이미지·원화 brief 단계에서 파츠와 숨겨진 겹침을 먼저 설계한다.

예시 파츠군은 실제 consumer에 필요한 것만 사용한다.

```text
Head
HairFront / HairBack / HairSide
FaceBase / Eye / Brow / Mouth
Neck / Torso / Pelvis
UpperArm_L/R / Forearm_L/R / Hand_L/R
Thigh_L/R / Shin_L/R / Foot_L/R
Cape / Cloth / Accessory
Weapon / Tool / WeaponHandAnchor
Shadow
```

각 파츠 record는 다음을 가진다.

```yaml
part_id:
pivot:
parent_bone:
draw_order:
hidden_underlap:
overlap_margin:
deformation_safe_area:
attachment_slot:
skin_group:
mirror_allowed:
source_path:
source_sha256:
```

- 관절은 현재 포즈에서 보이는 윤곽만 자르지 않고 회전·변형해도 틈이 생기지 않는 `hidden_underlap`과 `overlap_margin`을 둔다.
- 얼굴·손·무기·장식은 교체가 실제 필요한 경우에만 `attachment_slot`으로 분리한다.
- mesh 변형이 필요하지 않은 단단한 파츠를 불필요하게 세분화하지 않는다.
- 파츠 이름과 bone 이름은 프로젝트 convention을 따르고, 이미지 모델 출력의 우연한 layer 구성을 runtime contract로 가정하지 않는다.
- 픽셀 아트, 극단적 스미어, 프레임별 실루엣 재설계에는 이 계약을 강제하지 않는다.

```text
RIG_READY_SOURCE_IS_NOT_RUNTIME_ASSET
```

파츠 원화와 rig source가 준비돼도 import, animation, performance, player-facing 품질, 권리, 승격은 별도 상태다.

## 5. 행동 상태군과 단계

대표 이미지 한 장이 아니라 실제 consumer가 요구하는 상태군을 선언한다. 필요하지 않은 상태는 사유가 있는 `NOT_APPLICABLE`로 둔다.

```text
Idle
Locomotion
Turn
Wind-up
Active
Recovery
Guard
Evade
Hit
Stagger
Knockdown
Rise
Defeat
Interaction
Expression
Transition
```

공격·주문·도구 사용처럼 결과 원인이 중요한 행동은 최소 다음 의미 단계를 분리한다.

```text
start state
→ Wind-up: 의도·위험·취소 가능성 표시
→ Active: 이미 확정된 결과의 시각적 발생
→ Recovery: 다음 행동 가능 시점과 잔여 위험 표시
→ return / chain / interrupted state
```

프레임 수나 보간 방식은 route 선택 후 실제 timing·input·gameplay 계약으로 정한다. 부드러움 때문에 실루엣, 판정 원인, 타격 순간, 다음 행동 가능 시점이 흐려져서는 안 된다.

## 6. 중단·재진입·접근성 계약

모든 route는 다음을 명시한다.

```yaml
can_interrupt:
interrupt_windows: []
next_state_priority: []
same_state_reentry:
rapid_repeat_behavior:
instant_complete_behavior:
pause_resume:
save_resume_pose:
reduced_motion_fallback:
missing_asset_fallback:
```

- 빠른 반복 입력으로 transform·mix·event가 누적되지 않는다.
- 중단·스킵·즉시 완료·재진입 이후 시각 상태가 canonical gameplay state로 수렴한다.
- `reduced_motion_fallback`은 정보·사건 순서·결과 원인을 보존하면서 2차 물리, 긴 보간, 화면 흔들림을 줄인다.
- 자산·native library 누락 시 crash나 진행 차단 대신 승인된 정적 pose 또는 frame fallback을 사용한다. 단, fallback이 게임 결과를 바꾸지 않는다.

## 7. Domain 권위 경계

```text
ANIMATION_IS_PRESENTATION_CONSUMER_NOT_DOMAIN_AUTHORITY
```

애니메이션 event, 완료 signal, mix 종료, frame callback은 다음 domain outcome의 권위가 아니다.

```text
damage
cost
reward
save
progress
```

게임 도메인이 결과를 exactly once 확정한 뒤 visual adapter가 표현 sequence를 요청한다. 시각 이벤트는 사운드·VFX·카메라·다음 표현 단계처럼 멱등 또는 복구 가능한 presentation cue만 발생시킨다. 애니메이션이 중단·스킵·교체돼도 damage·cost·reward·save·progress는 중복되거나 누락되지 않는다.

## 8. 외부 리그 Runtime trial 기록

외부 runtime은 발견 또는 문서 호환 주장만으로 `ADOPTED_ACTIVE`가 되지 않는다.

```yaml
candidate_name:
adoption_state: CANDIDATE | TRIAL_APPROVED | ADOPTED_ACTIVE | DEFERRED | REJECTED
editor_exact_version:
runtime_exact_version_or_commit:
godot_exact_version:
integration_type: GDEXTENSION | CUSTOM_ENGINE_MODULE | OTHER
export_format:
atlas_profile:
platforms: []
license_evidence:
price_checked_at:
source_available:
consumption_path:
performance_baseline:
platform_export_validation:
removal_or_rollback:
unverified: []
```

시험은 공식 sample 또는 권리가 명확한 최소 asset을 격리된 branch/sample Scene에서 사용한다. 프로젝트 자산·addon·`project.godot`·export preset을 바꾸기 전에 source diff와 제거 절차를 고정한다.

최소 A/B/C 비교는 같은 캐릭터·카메라·해상도·상태에서 수행한다.

```text
A = FRAME baseline
B = GODOT_NATIVE_RIG baseline
C = EXTERNAL_RIG_RUNTIME candidate
optional D = EXTERNAL_RIG_BAKED
```

측정값은 최소 다음을 포함한다.

- authoring/revision time과 필요한 전문 작업.
- visual silhouette·관절 seam·identity 유지.
- 1 / 2 / 예상 peak 인스턴스의 frame time, draw calls, memory, load/unload.
- state transition, interruption, rapid repeat, pause/resume, missing asset fallback.
- 목표 플랫폼 import, debug/runtime, export/package, 실제 기기 또는 명시된 substitute.
- dependency removal 뒤 fallback과 repository clean readback.

## 9. Spine 후보의 현재 1차 자료 snapshot

확인일은 `2026-09-03`이며, 실제 도입 시 다시 읽는다.

```text
SPINE_CANDIDATE_NOT_DEFAULT_DEPENDENCY
REVALIDATE_PRICE_AND_LICENSE_AT_DECISION_TIME
PROJECT_IMPORT_EXPORT_RUNTIME_NOT_RUN
```

- 공식 `spine-godot` 문서는 기존 Godot 프로젝트에 넣는 `GDExtension`과 custom C++ engine module을 구분한다. GDExtension은 drop-in 경로지만 `AnimationPlayer` 지원과 전용 C# binding이 없고 일부 editor 기능이 제한된다. custom module은 `AnimationPlayer`를 지원하지만 custom Godot editor와 export template 유지비가 생기므로 기본 경로로 채택하지 않는다.
- 공식 `spine-runtimes` 4.3의 `spine-godot` README는 Spine 4.3.xx export data를 대상으로 하며 two-color tinting과 screen blend mode를 지원 예외로 기록한다.
- 공식 Runtime 저장소의 CI에는 Godot 4.7.1 GDExtension/module build가 포함돼 있지만, 이는 우리 프로젝트의 import·Windows/Android runtime·export·성능 통과 증거가 아니다.
- 공식 구매 페이지는 무료 trial을 제공한다. Essential/Professional 기능·가격·라이선스와 Runtime 배포 조건은 변할 수 있으므로 구매 또는 통합 직전에 원문을 다시 확인한다.
- Spine Editor와 Runtime의 exact compatible version을 lockstep으로 고정하고, export source·runtime commit·Godot version을 함께 변경·검증한다.

Official sources:

- https://esotericsoftware.com/spine-godot
- https://esotericsoftware.com/spine-purchase
- https://esotericsoftware.com/spine-runtimes-license
- https://github.com/EsotericSoftware/spine-runtimes/tree/4.3/spine-godot
- https://github.com/EsotericSoftware/spine-runtimes/blob/4.3/.github/workflows/spine-godot-extension-v4-all.yml
- https://docs.godotengine.org/en/4.7/classes/class_skeleton2d.html
- https://docs.godotengine.org/en/4.7/tutorials/animation/2d_skeletons.html

## 10. 무료·가역적 첫 시험 순서

```text
current project owner + actual consumer
→ existing FRAME baseline
→ Godot native rig feasibility
→ official external-runtime sample and current license read
→ route record 작성
→ isolated sample Scene / branch
→ same-state A/B/C evidence
→ removal and fallback test
→ project-specific adoption decision
```

- 구매 전에는 공식 trial·sample·runtime evaluation 범위와 현재 라이선스를 확인한다.
- Base나 모든 프로젝트에 외부 binary를 복제하지 않는다.
- 실제 consumer와 project-specific trial 없이 `ADOPTED_ACTIVE` 또는 생산 asset batch를 선언하지 않는다.
- custom engine module은 GDExtension·native rig·baked route로 해결할 수 없는 명시적 blocker가 있고 유지비를 감당할 프로젝트에서만 별도 사용자 결정으로 올린다.

## 11. 검증과 증거 상한

```text
RESEARCHED != TRIAL_APPROVED != INSTALLED != IMPORTED != MACHINE_VERIFIED != RUNTIME_VERIFIED != HUMAN_APPROVED != SHIP_APPROVED
```

| Evidence | 증명하는 것 | 증명하지 않는 것 |
|---|---|---|
| 문서·계약 test | route·필드·금지 경계가 repository에 존재 | 실제 Godot import, animation 품질, 성능 |
| 공식 sample import | exact environment에서 최소 import 가능 | 프로젝트 asset·state·platform 전체 적합성 |
| machine/runtime test | 기록한 build에서 동작·성능 predicate | Human 가독성·감정 품질·출시 권리 전체 |
| Human review | 의도한 화면에서 인물성·가독성·피로 | 다른 기기·콘텐츠·release 통과 |
| project adoption | 해당 프로젝트의 exact pin·consumer·rollback 승인 | 다른 프로젝트 자동 채택 |

실행하지 않은 항목은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다. 문서 contract PASS, 테스트 PASS, runtime PASS, Human PASS, 구매·라이선스 검토, 사용자 승인, 출시 승인 상태를 합치지 않는다.

## 12. Rollback과 비사용 조건

다음이면 `FRAME` 유지 또는 외부 runtime을 `DEFERRED / REJECTED`로 둔다.

- 실제 consumer 또는 반복 제작 이익이 없다.
- 픽셀·스미어·프레임별 실루엣 정체성이 리그 보간으로 약해진다.
- native rig 또는 frame route가 더 적은 총비용으로 같은 플레이어 가치를 만든다.
- exact version·license·source·platform binary를 재현할 수 없다.
- 목표 peak에서 frame time·memory·load·draw-call budget을 넘는다.
- 제거 뒤 프로젝트가 열리지 않거나 fallback이 없다.
- 외부 runtime event가 domain authority로 침투한다.

Rollback은 candidate addon/native binary/resource와 소비 adapter만 제거하고, 원본 frame fallback·domain state·save schema·승인 자산을 보존한다. 도입·철회 때 실제 project files, import cache 재생성, export preset, CI, runtime readback을 다시 검증한다.
