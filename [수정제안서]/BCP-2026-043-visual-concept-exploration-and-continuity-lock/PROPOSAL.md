# BCP-2026-043 · Visual Concept Exploration & Continuity Lock

## 0. 상태

```yaml
proposal_id: BCP-2026-043
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: USER_CHAT_2026-08-27_CONCEPT_OPTIONS_THEN_STYLE_CONTINUITY
source_base_main: 1213aa45f2965c4aab67d6284367c6240e98dc2c
incremental_cost: 0
```

## 1. 사용자 승인 목표

새 프로젝트 또는 아직 확정되지 않은 중요한 Visual Direction은 처음부터 최종 자산 한 장으로 고정하지 않는다.

```text
몇 가지 실질 컨셉·그림체·분위기 예시를 비교
→ 사용자 선택
→ 컨셉시안·Flow/Screen anchor와 Visual Direction 확정
→ 확정된 분위기·그림체·색감·재질·광원·카메라 문법으로 후속 자산 생산
→ 실제 화면에서 일관성 검증
```

사용자가 제공한 두 비교 예시는 다음 운영 의도를 증명한다.

- 같은 보드·화면 소비처·기본 구도를 유지한 채 궁정 전술실, 투기장, 마법 성소, 전쟁 지휘실처럼 분위기·세계 표현을 비교한다.
- 여러 픽셀 아트 계열을 나란히 놓고 캐릭터 비례·클러스터·렌더 밀도·배경 표현 차이를 비교한다.

이 예시는 프로젝트 정본이나 제품 자산이 아니라 **비교 방식의 사용자 승인 evidence**다.

## 2. 실제 Base 감사

Current Base에는 필요한 개별 기능이 이미 존재한다.

### 기존 owner

- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
  - Concept Exploration에서 서로 다른 방향 3개 안팎과 동일 조건 비교를 요구한다.
  - Concept → Art Bible → Asset Specification을 소유한다.
- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
  - actual consumer, Visual Requirement Gate, candidate lifecycle, Visual continuity, runtime 검수를 소유한다.
- `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
  - text brief → 다음 사용자 승인 → 한 생성 결과 → stop을 소유한다.
- `candidate-review-and-reusable-harvest.md`
  - 여러 후보의 실제 역할 기반 비교와 candidate state를 소유한다.
- `notion-project-visual-continuity-gate.md`
  - Project relation, approved reference, Flow/Screen, Keep/Avoid/Do Not Drift를 소유한다.
- `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`
  - 승인 reference/style anchor, objective acceptance, runtime validation과 Codex 전달을 소유한다.

### 확인된 gap

위 기능들이 다음 하나의 실행 경로로 연결되지 않았다.

```text
explore several controlled directions
→ select one
→ record adopted/rejected elements
→ lock mood/style/flow anchors
→ scale production consistently
→ revalidate affected scope on drift
```

특히 다음 경계가 명시적으로 부족했다.

1. 새/중요 Visual Direction에서 후보 비교가 production scale보다 선행해야 함
2. 비교 시트 1장은 명시적 exploration artifact이며 N개 runtime deliverable을 합친 것이 아님
3. 사용자 선택을 `APPROVED_VISUAL_DIRECTION_PACKET`으로 정본화
4. Flow/Screen anchor와 시각 문법을 후속 local asset/Codex/runtime acceptance에 전달
5. 일관성이 모든 장소를 똑같이 만드는 경직성이 아니라 허용 변형을 가진 공통 문법임
6. 방향·Flow drift가 생기면 영향받는 가장 이른 Visual scope만 다시 열고 프로젝트 전체를 재시작하지 않음

## 3. 비교한 대안

| 대안 | 장점 | 실패 모드 | 판정 |
|---|---|---|---|
| 처음부터 최종 자산 1개 제작 | 빠름 | 방향 오류 발견 시 대량 재작업, 사용자 선택 근거 없음 | REJECT |
| 후보마다 독립 고해상도 production asset 제작 | 비교 품질 높음 | 탐색비 과다, 생성/승인 chain 증가, 버려지는 bytes 폭증 | REJECT |
| 통제된 비교 board로 방향 탐색 후 selected anchor만 상세화 | 동일 조건에서 차이 판단, 비용 제한, 사용자 선택 명확 | board와 runtime asset 경계·lock packet 필요 | ADOPT |
| style lock 없이 매 자산 자유 생성 | 다양성 | 같은 프로젝트가 서로 다른 작품처럼 보임 | REJECT |
| 모든 대상에 rigid 동일 스타일 강제 | 표면 일관성 | 장소·진영·챕터 변주와 정보 구분성 손실 | REJECT |

## 4. 채택 설계

기존 상세 owner를 조합하는 얇은 계약을 추가한다.

```text
VISUAL_DIRECTION_EXPLORATION_BEFORE_SCALE
→ CONCEPT_OPTIONS_BEFORE_PRODUCTION_LOCK
→ USER_SELECTED_VISUAL_DIRECTION_REQUIRED
→ APPROVED_VISUAL_DIRECTION_PACKET
→ CONSISTENCY_REVIEW_AGAINST_VISUAL_DIRECTION_LOCK
```

새 owner:

```text
docs/knowledge/game-development/VISUAL_CONCEPT_EXPLORATION_AND_CONTINUITY_LOCK.md
```

이 owner는 Art Bible이나 이미지 정책의 두 번째 정본이 아니다.

```text
THIN_CONTRACT_NOT_SECOND_ART_BIBLE
```

### 적용 trigger

- 새 프로젝트의 첫 material Visual Direction
- 새 핵심 Slice의 대표 화면·환경·캐릭터 visual family
- 현재 approved direction 부재 또는 충돌
- 분위기·그림체·렌더 방식·카메라·밀도를 material하게 바꾸는 재설계

현재 approved Art Bible/Visual Direction이 있고 전제가 유지되는 bounded asset 제작에서는 기존 anchor를 재사용하며 매 자산마다 탐색을 반복하지 않는다.

### Concept options

```text
MINIMUM_VIABLE_CONCEPT_DIRECTIONS: 3
NO_FAKE_CONCEPT_OPTION
SAME_CONSUMER_CONTROLLED_COMPARISON
CONTROLLED_VARIABLE_COMPARISON_REQUIRED
```

최소 3개는 유효한 실질 대안이 있을 때 적용한다. 세 안을 만들 수 없으면 허수 후보를 만들지 않고 이유를 기록한다.

가능한 한 같은 consumer, 카메라, 프레이밍, 화면 점유율, 기본 내용 조건에서 선언한 비교축만 바꾼다.

### Explicit comparison board

```text
EXPLICIT_CONCEPT_COMPARISON_BOARD
ONE_EXPLORATION_BOARD_NOT_N_RUNTIME_DELIVERABLES
CONCEPT_COMPARISON_BOARD_IS_EXPLORATION_NOT_RUNTIME_ASSET
```

사용자가 비교 board를 명시적으로 승인한 경우 한 board는 existing `GENERATE_EXACTLY_ONE`의 한 exploration 결과가 될 수 있다. 그러나 이것은 여러 independent runtime asset을 한 이미지로 납품한 것이 아니며 `PROJECT_ASSET_APPROVED`나 runtime evidence가 아니다.

### Selection and lock

사용자 선택은 다음 두 receipt로 남긴다.

```yaml
CONCEPT_DIRECTION_SELECTION:
  selected_candidate_id:
  adopted_elements: []
  rejected_elements: []
  selection_reason:
  allowed_variation: []
  visual_direction_lock_output:

APPROVED_VISUAL_DIRECTION_PACKET:
  visual_direction_lock_id:
  source_candidate_ids: []
  approved_flow_or_screen_anchor_ids: []
  mood_and_emotion:
  style_and_rendering_language:
  palette_value_material_lighting:
  camera_framing_density:
  keep: []
  avoid: []
  do_not_drift: []
  allowed_variation: []
```

Flow/Screen anchor는 `CONFIRMED`인 project record만 사용한다. `DISCOVERED_IDEA`나 `AI_ASSUMPTION`을 잠긴 requirement로 승격하지 않는다.

### Production continuity

후속 asset은 lock을 `approved_reference_or_style_anchor`로 소비하고, 실제 화면에서 다음을 검수한다.

- mood/emotion
- rendering/line/material language
- palette/value/lighting
- shape/silhouette/proportion
- camera/framing/density
- UI/VFX family와 정보 위계
- allowed variation과 Do Not Drift

```text
ALLOWED_VARIATION_WITHOUT_UNAUTHORIZED_STYLE_DRIFT
```

지역·진영·챕터별 색감·소재 차이는 허용할 수 있지만 공통 문법과 protected identity를 벗어나면 drift다.

### Drift reopen

```text
VISUAL_DIRECTION_OR_FLOW_DRIFT_REVALIDATION_REQUIRED
EARLIEST_AFFECTED_VISUAL_SCOPE_REOPENS
NO_FULL_PROJECT_VISUAL_RESTART_FOR_LOCAL_DRIFT
```

material direction/Flow 변경은 영향받는 candidate·asset family·screen만 stale 처리하고 downstream evidence를 영향 범위만큼 재검증한다.

## 5. TDD

### RED

Exact RED head `b3b2ecbe033faf52193b116c0a023d3721173c87`:

- Base v9 Operating Contracts: PASS
- docs / Ubuntu governance / publication validation: PASS
- Game Project OS whole core regression: expected FAIL
- 기능 실패:
  - composed Visual lock contract 부재
  - continuity gate route 부재
- 별도 topology finding:
  - 최초 test filename이 P01 `*continuity*`와 P05 `*visual*`에 동시에 걸림
  - root cause 확인 후 `tests/test_visual_concept_exploration_lock.py`로 P05 단일 소유 정규화

### GREEN 요구

- 새 thin contract
- continuity gate의 조건부 route
- focused/core regression
- open PR path overlap 0
- 최소 5회 full-scope adversarial review
- exact-head required checks와 safe squash merge
- post-merge main/readback

## 6. 보호 범위

- 이미지 생성 자체 없음
- 프로젝트별 Art Bible·Flow·Asset 일괄 migration 없음
- 기존 approved direction 자동 교체 없음
- `PROPOSAL_REGISTRY.json` 수정 없음 — PR #678 ownership 종료 뒤 별도 reconciliation
- PR #713 UI/Visual owner 경로와 PR #748 five-stage 경로 read-only
- 새 Skill·Tool·provider·dependency·비용 없음
- direct main·force·ruleset/admin bypass 없음

## 7. Evidence ceiling

이 변경은 Base process/contract를 검증한다.

```text
STATIC_CONTRACT_PASS
!= actual candidate quality
!= user project selection
!= PROJECT_ASSET_APPROVED
!= runtime visual consistency PASS
!= Human usability / Player Experience PASS
```

## 8. Rollback

구현 squash commit을 revert하고 continuity gate에서 새 contract route를 제거한다. 기존 Art Direction, image policy, candidate review, local Visual delivery와 Project canon은 그대로 유지된다.
