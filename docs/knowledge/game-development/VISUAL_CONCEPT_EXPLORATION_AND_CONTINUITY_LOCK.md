# Visual Concept Exploration and Continuity Lock

> 이 문서는 **새롭거나 material하게 변경되는 프로젝트 Visual Direction을 여러 실질 후보로 탐색하고, 사용자가 선택한 방향을 Flow/Screen anchor와 함께 잠근 뒤, 후속 자산을 일관되게 생산·검수하는 전이 계약**이다. Art Bible, 이미지 생성 정책, 후보 검수, 로컬 자산 전달의 상세 절차를 복제하지 않는다.

```text
VISUAL_DIRECTION_EXPLORATION_BEFORE_SCALE
THIN_CONTRACT_NOT_SECOND_ART_BIBLE
PROJECT_CANON_AND_ACTUAL_IMPLEMENTATION_FIRST
ACTUAL_CONSUMER_REQUIRED
CURRENT_SPECIALIST_OWNER_WINS_ON_DETAIL_DRIFT
NO_AUTOMATIC_IMAGE_GENERATION_AUTHORITY
```

## 0. 조합하는 current owner

작업 시점의 Base latest completed main과 exact Project canon에서 다음 상세 owner를 fresh-read한다.

- 필요성·actual consumer·candidate lifecycle·검수: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Concept Exploration·Visual Pillar·Art Bible·Asset Specification: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- 생성 대화 승인과 한 결과 checkpoint: `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- 후보 비교·선정·재사용 판정: `skills/designing-art-prompts-and-technique-cards/references/candidate-review-and-reusable-harvest.md`
- Project relation·Flow/Screen·Keep/Avoid/Do Not Drift: `skills/designing-art-prompts-and-technique-cards/references/notion-project-visual-continuity-gate.md`
- 프로젝트 로컬 후보·승격·Codex 전달: `templates/project-operations/WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`

이 문서의 packet은 프로젝트 Art Bible을 대체하지 않는다. 프로젝트별 분위기·팔레트·캐릭터 비례·Flow·실제 asset ID는 Project GitHub/Notion 정본에 기록한다.

---

## 1. 적용 여부 Gate

### 1.1 탐색이 필요한 경우

다음 중 하나가 current evidence로 확인될 때 이 계약을 적용한다.

- 새 프로젝트의 첫 material Visual Direction
- 새 핵심 Slice의 대표 화면·환경·캐릭터·UI visual family
- approved Art Bible/Visual Direction이 없거나 서로 충돌함
- 그림체·렌더 방식·카메라·장식 밀도·분위기·색/광원 문법을 material하게 바꾸는 재설계
- 현재 Flow/Screen이 바뀌어 기존 visual anchor가 대표 소비처를 더 이상 설명하지 못함
- 반복 production을 시작하기 전에 어떤 방향이 장기 제작성과 player promise에 맞는지 결정해야 함

### 1.2 탐색을 반복하지 않는 경우

```text
CURRENT_APPROVED_VISUAL_DIRECTION_REUSE
NO_REEXPLORATION_FOR_EVERY_BOUNDED_ASSET
```

다음이 모두 유지되면 기존 lock을 재사용한다.

- current approved Visual Direction/Art Bible이 존재함
- actual consumer와 Flow/Screen 의미가 material하게 바뀌지 않음
- protected identity와 production constraints가 유지됨
- 새 evidence가 기존 방향을 무효화하지 않음

버튼 하나, 기존 캐릭터의 bounded pose, 같은 환경군의 소품처럼 current lock 안에서 해결되는 작업마다 컨셉 후보 3개를 다시 만들지 않는다.

### 1.3 Fail closed

Project identity, actual consumer, approved direction 상태 또는 필요한 Flow/Screen 정본을 읽지 못하면 다른 프로젝트·과거 채팅·draft 이미지를 빌려 추측하지 않는다.

```text
MISSING_VISUAL_DIRECTION_CANON
VISUAL_CANONICAL_CONFLICT
BLOCKED_UNVERIFIED
```

---

## 2. 전체 전이

```text
CONCEPT_OPTIONS_BEFORE_PRODUCTION_LOCK
→ USER_SELECTED_VISUAL_DIRECTION_REQUIRED
→ APPROVED_VISUAL_DIRECTION_PACKET
→ CONSISTENCY_REVIEW_AGAINST_VISUAL_DIRECTION_LOCK
```

세부 흐름:

```text
Project canon / actual implementation / approved references fresh-read
→ actual consumer와 이번 시각 결정 질문 정의
→ Reuse First + reference/benchmark axes
→ 통제된 실질 후보 제시
→ 사용자 비교·선택
→ adopted/rejected 요소와 허용 변형 기록
→ confirmed Flow/Screen anchor 연결
→ Visual Direction lock readback
→ 후속 production brief/asset/Codex packet에 lock identity 전달
→ target-size/runtime consistency validation
```

`CONCEPT_OPTIONS_BEFORE_PRODUCTION_LOCK`은 방향을 찾는 단계다. 후보나 비교 board가 존재한다는 이유로 production scale을 시작하지 않는다.

---

## 3. 후보 방향 설계

```text
MINIMUM_VIABLE_CONCEPT_DIRECTIONS: 3
NO_FAKE_CONCEPT_OPTION
SAME_CONSUMER_CONTROLLED_COMPARISON
CONTROLLED_VARIABLE_COMPARISON_REQUIRED
```

### 3.1 최소 3개 실질 후보

중요한 방향 선택에는 가능한 경우 최소 3개의 materially distinct 후보를 비교한다.

유효한 후보는 다음 중 하나 이상의 실제 trade-off가 다르다.

- 현실성 ↔ 도식성
- 귀여움 ↔ 위엄
- 따뜻함 ↔ 불안
- 픽셀 클러스터·렌더 밀도
- 형태 복잡도·장식 밀도
- 색 채도·명도 구조·광원
- 카메라 거리·프레이밍
- 제작 난이도·반복 생산성
- UI/VFX와의 결합성
- 첫인상·세일즈포인트·장르 신호

이름·팔레트만 약간 바꾼 허수 후보로 수를 채우지 않는다. 3개의 실질 대안이 존재하지 않으면 그 이유와 비교 가능한 실제 후보 수를 기록한다.

### 3.2 동일 조건 비교

가능한 범위에서 후보는 같은 조건으로 비교한다.

```yaml
CONTROLLED_CONCEPT_COMPARISON:
  decision_question:
  actual_consumer:
  invariant_content:
  invariant_camera_and_framing:
  invariant_scale_and_viewing_distance:
  declared_variable_axes: []
  candidate_ids: []
  evaluation_dimensions: []
  constraints_that_cannot_be_equalized: []
```

예를 들어 같은 전술 보드 화면의 장소 분위기를 비교한다면 보드 크기·카메라·UI 점유율·대표 정보는 유지하고, 건축 언어·광원·재질·분위기처럼 선언한 축만 바꾼다.

그림체를 비교한다면 같은 캐릭터 역할·대략적 포즈·화면 크기·배경 역할을 유지해 픽셀 밀도·비례·클러스터·렌더 언어의 차이를 판독할 수 있게 한다.

비교 조건을 같게 만들 수 없는 항목은 숨기지 않고 `constraints_that_cannot_be_equalized`에 기록한다.

### 3.3 후보 설명

후보마다 다음을 실제 텍스트 owner에 기록한다.

```yaml
CONCEPT_DIRECTION_CANDIDATE:
  candidate_id:
  title:
  actual_consumer:
  player_experience_strengthened:
  information_or_experience_weakened:
  mood_and_style_axes:
  sales_point:
  production_cost_and_repeatability:
  technical_or_platform_risk:
  reference_and_rights_boundary:
  observable_acceptance:
```

후보 ID·제목·장단점은 생성 이미지 속 pseudo-text에 의존하지 않는다. 비교 board 안의 문자가 불안정하면 실제 텍스트 caption/Notion/Markdown record가 의미를 소유한다.

---

## 4. Explicit Concept Comparison Board

```text
EXPLICIT_CONCEPT_COMPARISON_BOARD
ONE_EXPLORATION_BOARD_NOT_N_RUNTIME_DELIVERABLES
CONCEPT_COMPARISON_BOARD_IS_EXPLORATION_NOT_RUNTIME_ASSET
```

### 4.1 언제 한 board를 사용할 수 있는가

사용자가 여러 방향을 한 화면에서 비교하려는 목적을 명시적으로 승인하고, text brief가 다음을 포함하면 하나의 comparison board를 만들 수 있다.

- 비교할 actual consumer 또는 visual family
- 후보 수와 candidate ID
- 동일하게 유지할 조건
- 후보마다 바꿀 축
- board가 exploration이라는 상태
- 선택 뒤 상세화할 방향

이 board는 existing conversation Gate의 **one explicit comparison artifact**다. 하나의 board 안에 여러 option panel이 있어도 `GENERATE_EXACTLY_ONE`의 한 생성 결과로 취급할 수 있다.

```text
TEXT_BRIEF_STOP_REQUIRED
→ NEXT_USER_EXPLICIT_APPROVAL
→ GENERATE_EXACTLY_ONE explicit comparison artifact
→ STOP_REQUIRED_AFTER_GENERATION
```

### 4.2 무엇을 의미하지 않는가

comparison board는 다음이 아니다.

- 여러 개의 independent runtime asset을 한 장에 압축 납품한 것
- 각 panel의 독립 고해상도 source
- `PROJECT_ASSET_APPROVED`
- Godot import/Scene 소비 증거
- 실제 화면 가독성·Human/Player PASS

```text
comparison board = GENERATED_EXPLORATION
comparison board = not runtime evidence
comparison board != independent runtime asset delivery
```

사용자가 선택한 방향을 실제 gameplay 배경·캐릭터·UI·VFX로 소비하려면 해당 consumer에 맞는 독립 production deliverable, format, crop/alpha, source path, manifest와 runtime validation이 별도로 필요하다.

### 4.3 Collage 오용 방지

runtime에서 각각 독립 파일로 필요한 N개 자산을 comparison board 하나로 생성해 `N requested assets = delivered`라고 주장하지 않는다. 비교 board 승인과 production batch 승인도 분리한다.

---

## 5. 사용자 선택과 방향 잠금

```text
USER_SELECTED_VISUAL_DIRECTION_REQUIRED
CONCEPT_DIRECTION_SELECTION
```

후보 결과를 “가장 예쁜 것”만으로 고르지 않는다. current Project player promise, actual-use readability, identity, production 반복성, 기술 적합성, rights/reference 위험을 함께 비교한다.

사용자 선택 뒤 다음 receipt를 Project structured/human canon에 기록하고 readback한다.

```yaml
CONCEPT_DIRECTION_SELECTION:
  selected_candidate_id:
  adopted_elements: []
  rejected_elements: []
  selection_reason:
  conditions_or_assumptions:
  allowed_variation: []
  superseded_direction_ids: []
  visual_direction_lock_output:
  approval_ref:
```

`adopted_elements`와 `rejected_elements`는 후보 전체를 무비판적으로 복사하지 않게 한다. 사용자는 A의 분위기, B의 UI 절제, C의 카메라처럼 명시적으로 조합할 수 있으며 조합 결과를 새로운 lock으로 기록한다.

---

## 6. Approved Visual Direction Packet

```text
APPROVED_VISUAL_DIRECTION_PACKET
FLOW_AND_SCREEN_ANCHORS_LOCKED_BEFORE_SCALE
```

```yaml
APPROVED_VISUAL_DIRECTION_PACKET:
  project:
  visual_direction_lock_id:
  lock_version:
  source_candidate_ids: []
  selection_and_approval_ref:
  actual_consumer_families: []
  approved_flow_or_screen_anchor_ids: []
  mood_and_emotion:
  style_and_rendering_language:
  shape_silhouette_and_proportion:
  palette_value_material_lighting:
  camera_framing_density:
  ui_iconography_vfx_family:
  typography_or_text_rendering_boundary:
  keep: []
  avoid: []
  do_not_drift: []
  allowed_variation: []
  production_constraints: []
  rights_and_reference_boundary:
  target_size_and_runtime_checks: []
  supersedes: []
  status: CURRENT | SUPERSEDED | CONFLICT | BLOCKED_UNVERIFIED
```

### 6.1 Flow/Screen anchor 조건

`approved_flow_or_screen_anchor_ids`에는 Project record가 `CONFIRMED`인 항목만 넣는다.

```text
CONFIRMED → lock anchor 가능
DISCOVERED_IDEA → 참고만 가능
AI_ASSUMPTION → 참고만 가능
```

컨셉 이미지가 새로운 버튼·보드·규칙·화면 전이를 그럴듯하게 보여줬다는 이유로 이를 project requirement로 승격하지 않는다.

### 6.2 Keep / Avoid / Do Not Drift

- `keep`: 프로젝트 정체성과 player experience를 유지하는 핵심 문법
- `avoid`: 이미 검토해 배제한 방향·가독성 실패·pseudo-text·과밀 표현
- `do_not_drift`: 캐릭터 identity, 비례, 실루엣, palette role, material/line language, camera grammar, UI family처럼 후속 production에서 보호할 항목
- `allowed_variation`: 지역·진영·시간대·상태에 따라 의도적으로 바꿀 수 있는 축과 허용 범위

이 packet은 Art Bible 내용을 통째로 복사하지 않고 current owner의 선택·버전·anchor를 연결한다.

---

## 7. 후속 Production과 Codex 전달

```text
CONSISTENCY_REVIEW_AGAINST_VISUAL_DIRECTION_LOCK
ALLOWED_VARIATION_WITHOUT_UNAUTHORIZED_STYLE_DRIFT
```

후속 이미지·UI source·VFX·캐릭터·환경 production은 생성 전부터 current `visual_direction_lock_id`와 actual consumer를 brief에 포함한다.

### 7.1 기존 local Visual packet으로 매핑

`WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`의 기존 packet schema를 바꾸지 않고 다음처럼 채운다.

```yaml
VISUAL_LOCK_TO_LOCAL_PACKET_MAPPING:
  visual_direction_lock_id: APPROVED_VISUAL_DIRECTION_PACKET.visual_direction_lock_id
  approved_flow_or_screen_anchor_ids: APPROVED_VISUAL_DIRECTION_PACKET.approved_flow_or_screen_anchor_ids
  approved_reference_or_style_anchor: visual_direction_lock_id + approved reference locator
  notion_reference_surface: Project Visual Bible / confirmed Flow or Screen locator
  objective_acceptance:
    - lock의 keep / avoid / do_not_drift / allowed_variation 준수
    - target-size readability
    - actual consumer 역할 수행
  runtime_validation:
    runtime_consistency_validation:
    - exact Scene/Screen/consumer에서 mood·style·palette·camera·UI/VFX family 검수
```

Codex handoff에는 project-relative asset path, manifest identity, exact commit과 함께 `visual_direction_lock_id`와 `approved_flow_or_screen_anchor_ids`를 전달한다. Codex가 임의로 다른 그림체·가짜 기능·temporary placeholder로 교체하지 못하게 acceptance에 포함한다.

### 7.2 일관성 검수 축

각 후속 결과는 최소 다음을 current lock과 비교한다.

```text
mood / emotion
style / rendering / line / cluster language
shape / silhouette / proportion
palette / value / material / lighting
camera / framing / visual density
UI / iconography / VFX family
information hierarchy and actual-use readability
protected identity
allowed variation
```

일관성은 모든 장소·캐릭터·상태를 똑같이 만드는 것이 아니다. 예를 들어 마법 성소와 투기장은 색·소재·장식이 달라도, 픽셀 밀도·카메라·명도 위계·UI family·형태 문법은 같은 프로젝트로 인지되어야 한다.

### 7.3 실제 화면 검증

원본 이미지가 아름답다는 사실만으로 consistency PASS를 주장하지 않는다.

```text
source candidate review
!= imported asset review
!= target-size screen review
!= motion/VFX/HUD composite review
!= Human/Player evidence
```

`runtime_consistency_validation`은 exact consumer, target resolution/aspect, UI/VFX overlay, crop/import 조건과 함께 수행한다.

---

## 8. 상태와 Evidence ceiling

```text
GENERATED_EXPLORATION
→ IN_REVIEW
→ APPROVED_CANDIDATE
→ USER_SELECTED_VISUAL_DIRECTION_REQUIRED
→ APPROVED_VISUAL_DIRECTION_PACKET
→ independent production candidate
→ PROJECT_ASSET_APPROVED
→ repository/runtime integration
→ APPLIED_AND_RUNTIME_VERIFIED
```

다음 상태는 서로 대체하지 않는다.

```text
comparison board exists
!= user selected direction
!= Visual Direction locked
!= production asset approved
!= runtime consistency PASS
!= Human usability / Player Experience PASS
```

Concept candidate와 rejected direction은 필요할 때 provenance/negative knowledge로 보존하되 current Visual Direction과 혼동하지 않는다.

---

## 9. Direction / Flow drift와 bounded reopen

```text
VISUAL_DIRECTION_OR_FLOW_DRIFT_REVALIDATION_REQUIRED
EARLIEST_AFFECTED_VISUAL_SCOPE_REOPENS
NO_FULL_PROJECT_VISUAL_RESTART_FOR_LOCAL_DRIFT
```

### 9.1 Drift trigger

- user Decision이 mood/style/camera/proportion을 material하게 변경
- confirmed Flow/Screen 구조가 변경
- actual consumer 또는 target viewing distance가 변경
- runtime evidence가 lock의 가독성·일관성 실패를 증명
- rights/reference 문제로 anchor 사용 불가
- approved asset bytes가 새로운 style family로 교체

### 9.2 처리

```text
change evidence
→ affected lock field / anchor / asset family 식별
→ 영향을 받은 candidate·production asset·runtime evidence만 stale 처리
→ 필요한 경우 concept selection 또는 lock field 재승인
→ affected downstream assets 재검수
→ destination readback
```

아이콘 하나의 local drift 때문에 프로젝트 전체 Concept Exploration을 처음부터 반복하지 않는다. 반대로 Art Direction master가 변경됐는데 기존 후속 자산을 그대로 PASS로 유지하지 않는다.

---

## 10. 적대적 검토

최소 다음 실패 가정을 전체 상태에서 다시 공격한다.

1. 후보가 실질적으로 같은 허수 3안인가
2. 후보마다 카메라·내용·스케일이 달라 무엇 때문에 좋아 보이는지 비교할 수 없는가
3. comparison board를 여러 runtime 자산 납품으로 오인했는가
4. board 안 pseudo-text가 candidate identity와 장단점을 잘못 전달하는가
5. 선택 이유·adopted/rejected 요소 없이 “이 느낌”만 승인했는가
6. `DISCOVERED_IDEA`·`AI_ASSUMPTION` Flow를 locked requirement로 승격했는가
7. 후속 자산이 lock을 읽지 않아 서로 다른 작품처럼 drift했는가
8. 일관성을 이유로 지역·진영·상태의 필요한 차이를 제거했는가
9. allowed variation이 너무 넓어 사실상 아무 스타일도 보호하지 못하는가
10. 실제 target-size/runtime 검수 없이 원화만 보고 PASS했는가
11. direction/Flow 변경 뒤 stale candidate·asset·runtime evidence를 current로 유지했는가
12. local drift 하나 때문에 프로젝트 전체를 재시작했는가
13. user approval, candidate approval, project asset approval, runtime proof를 혼동했는가
14. 다른 프로젝트 reference나 식별 가능한 상업 표현을 무단 style anchor로 사용했는가

유효 finding이 있으면 관련 가장 이른 Visual scope를 다시 열고, 수정 뒤 전체 affected state를 다시 읽는다.

---

## 11. Clean exit

```yaml
VISUAL_CONCEPT_LOCK_CLEAN_EXIT:
  exact_project_and_consumer_verified: true
  exploration_required_or_reuse_reason:
  real_candidate_count:
  controlled_comparison_evidence:
  user_selection_ref:
  visual_direction_lock_id:
  confirmed_flow_or_screen_anchors: []
  local_packet_mapping_verified:
  runtime_consistency_plan:
  rights_and_reference_status:
  blocking_findings: []
  evidence_ceiling:
  result: READY_FOR_BOUNDED_PRODUCTION | REUSE_CURRENT_LOCK | BLOCKED_UNVERIFIED
```

정적 계약 존재는 실제 이미지 품질·프로젝트 사용자 승인·runtime consistency를 증명하지 않는다.
