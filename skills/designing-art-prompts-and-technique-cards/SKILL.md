---
name: designing-art-prompts-and-technique-cards
description: Use when designing art or UI image prompts, generating planning or candidate visuals, recording techniques, or reviewing generated images before approval.
---

# Designing Art Prompts and Technique Cards

이 Skill은 생성·편집 전 프롬프트, GPT 이미지·목업 후보, 기술 카드와 승인 전 시각 검수를 책임진다. 이미 구현된 Godot/Web UI의 실제 시각 품질 감사와 승인된 개선은 `auditing-and-refining-ui-art`를 사용한다.

프로젝트용 이미지 후보의 **누락 탐지**는 `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`의 `Visual Asset Coverage Preflight`를 먼저 사용하고, **필요성·우선순위·재사용·제작 방식 선정**은 이 Skill이 새로 판단하지 않는다. `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`가 선정 책임을 소유하고, 이 Skill은 선정된 requirement를 생성·편집·검수 계약으로 변환한다.

`NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`: coverage gap은 이미지 생성·batch 확대·다음 variant 자동 제작 권한이 아니다. 기존 사용자 승인과 Image Conversation Approval Gate를 그대로 적용한다.

프로젝트 시각 작업이면 `references/notion-project-visual-continuity-gate.md`를 적용한다. 이 gate는 `PROJECT_RELATION_REQUIRED`, 현재 Project Decision, `APPROVED_VISUAL_REFERENCE`, Screen/flow record, readback 및 repository/runtime authority 경계를 연결한다.

## Conditional visual modules

현재 task에 필요한 reference만 추가로 읽는다. 매 이미지 작업에서 전부 로드하지 않는다.

- Visual asset coverage: `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`
- Technique card output: `templates/planning/ART_TECHNIQUE_CARD.md`
- Prompt-recipe research card: `templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md`
- Project continuity / approval / screen-flow: `references/notion-project-visual-continuity-gate.md`
- 캐릭터 identity·표정·시선·머리 방향: `references/character-identity-expression-controls.md`
- pose/action/sprite sequence·atlas 후보: `references/sprite-pose-sequence-controls.md`
- VFX/effect stage·alpha/compositing: `references/effect-stage-compositing-controls.md`
- 후보 비교·선택·재사용 Harvest: `references/candidate-review-and-reusable-harvest.md`

별도 Figma/Expression/Sprite broad Skill이나 localhost delivery runtime을 기본 경로로 요구하지 않는다.

## Skill modes

- `technique-card`: 재사용 가능한 아트·UI 기술과 프롬프트 패턴을 `templates/planning/ART_TECHNIQUE_CARD.md`에 기록한다.
- `planning-visualization`: 세계관·인물·핵심루프·시스템·UI·대표 장면을 시각화해 방향과 모순을 비교한다.
- `intermediate-visual-checkpoint`: 사용자가 중간 점검·예상 게임 화면·UI 포함 화면을 요청하거나 P1 해석 위험이 있을 때, 현재 Project canon만으로 한 화면 흐름을 `DRAFT_VISUAL` 또는 대체 와이어프레임으로 검토한다.
- `final-visual-candidate`: 승인된 기획을 바탕으로 Demo-First·상점·홍보·UI·캐릭터·시스템 설명에 사용할 고품질 후보를 만든다.
- `visual-qa-and-approval`: 생성물의 기획 일치성·실제 화면·구현 가능성·권리·오류·재사용성을 검수하고 승인 후보 상태를 판정한다.

## Core principle

좋은 아트 프롬프트는 형용사를 많이 나열하는 문장이 아니라 **사용 목적, 유지할 정체성, 변경할 축, 화면 구성, 산출물 규격, 실패 기준**을 가진 제작 계약이다. **생성 결과는 자동 최종 자산이 아니다.**

## Required inputs

프로젝트 작업에서 필요한 범위만 확인한다.

- `Visual Asset Coverage Preflight`의 `coverage_item_id`, `coverage_status`, `state_family`, `state_family_status` — 적용 범위가 있을 때.
- `Visual Requirement Gate`의 `requirement_id`, role, priority, disposition, Delete Test, consumer, validation.
- `project_relation`과 Project Key.
- 관련 세계관·핵심루프·인물·시스템·아트·UI 책임 원본과 Decision ID.
- `approved_visual_reference_ids`와 `Keep / Avoid / Do Not Drift` continuity constraints.
- 필요할 때 `screen_id`, `flow_id`, `visual_map_status`.
- 원본 이미지 또는 캐릭터 디자인 카드.
- 유지해야 할 identity·의상·소품·스타일.
- 변경할 표정·포즈·색·구도·상태·정보 레이아웃.
- 출력 비율·해상도·크롭·알파·텍스트 처리 방식.
- 실제 consumer에 필요한 engine consumption 조건: filter/mipmap/compression/atlas/slicing/pivot/nine-patch/localization 등 해당 항목만.
- `PLATFORM_REQUIRED`이면 current official specification/rule readback 상태.
- 사용할 모델·서비스·버전과 실제 확인 가능한 기능.
- 외부 reference라면 source provenance, rights/license 상태, similarity risk.

사용자가 현재 대화에서 특정 이미지 한 장의 생성·편집을 명시적으로 요청했다면 그 요청을 현재 작업의 임시 requirement로 사용할 수 있다. 이 예외는 프로젝트 전체 자산 목록 선정·승인이나 `ASSET_MANIFEST.yml` 승격을 자동으로 만들지 않는다. 또한 해당 한 장과 무관한 coverage gap을 자동 생성 queue로 변환하지 않는다.

## Process

1. 프로젝트의 화면·캐릭터·시스템·asset set과 연결되는 작업이면 `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`에서 현재 consumer와 직접 관련된 coverage item만 확인한다. `COVERED_EXISTING / REQUIREMENT_LINKED / GAP_BLOCKING / GAP_NONBLOCKING / NOT_APPLICABLE`을 구분하고 **`NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`**를 적용한다.
2. 프로젝트 자산 작업이면 `Visual Requirement Gate` 선정 결과를 확인한다. `DEFER / CUT / REUSE_SYSTEM / REUSE_PROJECT`를 이미지 생성으로 임의 변환하지 않는다.
3. `PROJECT_RELATION_REQUIRED`를 확인한다. Project가 불명확하면 다른 프로젝트 자료를 빌리지 말고 `BLOCKED_UNVERIFIED`로 둔다.
4. `references/notion-project-visual-continuity-gate.md`에서 승인 reference와 `Keep / Avoid / Do Not Drift`를 확인한다. 승인 기준이 부족하면 `MISSING_CANON`, 상충하면 `VISUAL_CANONICAL_CONFLICT`다.
5. `planning-visualization`, `intermediate-visual-checkpoint`, `final-visual-candidate` 중 필요한 mode를 정한다.
6. 결과물이 쓰일 화면과 가장 먼저 전달할 정보를 정한다.
7. `STATE_FAMILY_COMPLETENESS`를 적용해 대표 한 장뿐 아니라 현재 consumer가 요구하는 Normal/Hover/Pressed/Disabled/Focus, Wind-up/Active/Recovery 같은 상태군을 확인한다. 불필요한 상태는 `NOT_APPLICABLE`로 둔다.
8. 원본에서 **유지할 요소 / 변경할 요소**를 분리하고, identity-preserving task라면 unchanged identity를 hard constraint로 둔다.
9. target resolution/aspect/crop과 필요한 engine consumption 조건을 정한다. pixel art, sprite sheet, UI 9-patch, mipmap/texture import 같은 조건은 실제 사용처에 필요할 때만 추가한다.
10. Pinterest를 포함한 발견 reference는 원작자·원출처·license·유사성을 확인하고 표면 복제를 금지한다.
11. 프롬프트를 다음 모듈로 작성한다.

```text
coverage_item_id · coverage_status · state_family_status
→ requirement_id · project_relation · 목적/역할
→ 관련 canon / Decision
→ approved_visual_reference_ids · Keep/Avoid/Do Not Drift
→ 변경할 표정·포즈·상태
→ 구도와 정보 위계
→ 형태·색·재질·광원
→ 텍스트·레이아웃 슬롯
→ 실제 화면비·해상도·크롭
→ 필요한 engine consumption constraints
→ 금지·보호 요소
→ QA·readback·재생성 기준
```

12. 짧은 제어어가 필요하면 자연어 설명 뒤에 code/tag를 보조 어휘로 쓴다. FACS AU는 참고 어휘이지 모델 공식 명령 체계로 가정하지 않는다.
13. 포스터·UI mockup은 일러스트, 정보 슬롯, 실제 타이포그래피를 분리해 수정 가능하게 만든다.
14. 성공 사례뿐 아니라 실패 조건과 수정 프롬프트를 기록한다.
15. 생성 뒤 `visual-qa-and-approval`을 실행하고 `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`에 기록한다. coverage link와 state family가 실제 결과에서 유지됐는지도 확인한다.
16. 생성물을 correct Project의 candidate record/page에 붙이고 **readback**한다. upload success만으로 delivery success를 주장하지 않는다.
17. 승인된 Decision만 `PROJECT_ASSET_APPROVED`로 promotion하고 repository implementation task와 연결한다.
18. 실제 consumer에서 requirement/asset/runtime evidence가 확인되면 연결된 coverage row를 readback한다. coverage 자체를 runtime proof로 사용하지 않는다.
19. 모델·버전·입력 이미지·승인 reference·Project canon·target platform specification이 달라지면 필요한 범위를 재검증한다.

## Intermediate visual checkpoint

정본·Decision ID·화면 제약이 없는 경우에는 이미지를 추정 생성하지 말고 `MISSING_CANON`으로 반환한다. 한 번에 한 화면 흐름을 우선하고, 화면 목적·첫 시선·주요 행동·플랫폼/화면비/입력·위험/비용/보상·성공/실패/복구·긴 한글·접근성·확인 사실과 미결정을 Brief에 쓴다.

이미지 생성이 필요 없거나 적절하지 않으면 텍스트 와이어프레임·Mermaid·구조화 Screen record로 검토할 수 있다.

생성 직후 `Screen Interpretation Review`에 canon과 일치한 요소, `MISSING_CANON`, `VISUAL_CANONICAL_CONFLICT`, `TECHNICAL_REVIEW_PROPOSAL`, `DISCOVERED_IDEA`, `AI_ASSUMPTION`, 버린 표현을 기록한다. 이 mode의 결과는 `DRAFT_VISUAL`이며 최종 자산·license 승인·Godot 구현·runtime 검증을 뜻하지 않는다. **사용자 Decision 없이** project approval 상태로 올리지 않는다.

## Status lifecycle

```text
PLANNED
→ GENERATED_EXPLORATION
→ IN_REVIEW
├─ REVISION_REQUIRED
├─ REJECTED
└─ APPROVED_CANDIDATE
   → PROJECT_ASSET_APPROVED
   → APPLIED_AND_RUNTIME_VERIFIED
```

`GENERATED_EXPLORATION`과 `APPROVED_CANDIDATE`는 최종 제품 자산이나 runtime proof가 아니다. Coverage 상태는 이 lifecycle과 별개이며 둘을 합치지 않는다.

## Identity-preserving expression control

권장 형식:

```text
원본 캐릭터의 얼굴 비율, 헤어, 의상, 소품, 채색과 배경을 유지한다.
표정만 한쪽 눈의 자연스러운 윙크로 변경한다.
보조 제어 어휘: FACS AU46 Wink, 약한 미소는 AU12B.
닫힌 눈의 속눈썹·안경테·눈썹이 겹치지 않게 한다.
```

- AU 번호만 단독 입력하는 방식은 빠른 탐색용이다.
- 최종 편집에는 자연어, 좌우 방향, 강도, 보호 요소를 함께 쓴다.
- 제공된 reference grid의 번호가 표준 FACS와 다를 수 있으므로 `docs/knowledge/research/FACS_ACTION_UNIT_PROMPT_REFERENCE.md`와 구분한다.

## Pose / sprite / effect controls

Pose sequence는 identity anchor와 action continuity를 먼저 잠근 뒤 프레임별 변화만 정의한다. Effect stage는 subject identity를 덮지 않게 effect-only 변화, alpha/compositing, intensity stage를 분리한다. 세부 계약은 conditional reference가 소유한다.

## Character poster prompt architecture

1. 메인 캐릭터와 전신·반신 포즈.
2. 배경 세계와 상징 오브젝트.
3. 키 컬러와 재질·광원.
4. 이름·엠블럼·태그라인 영역.
5. 특징 설명 모듈.
6. 표정·측면 inset.
7. 타이틀·날짜·하단 정보.
8. 실제 후처리와 현지화 계획.

이미지 모델이 한글을 생성하더라도 최종 제품 텍스트는 편집 가능한 UI/graphics layer로 교체한다. 이미지 안의 typography는 layout prototype 또는 key visual candidate로 취급한다.

## Reference-to-original visual production

공용 기준은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`다. 외부 이미지를 직접 채택하는 작업과 참조해 독립 제작하는 작업을 분리한다.

```yaml
reference_sources:
reference_brief:
forbidden_expression:
final_asset_record:
reference_similarity_status: PASS | REVISION_REQUIRED | BLOCKED_UNVERIFIED | NOT_APPLICABLE
```

`reference_brief`에는 화면 목적, 정보 위계, 기능적 형태·재질·광원 원리와 프로젝트 canon만 남긴다. `forbidden_expression`에는 식별 가능한 캐릭터 디자인, 실루엣·의상·소품 조합, 구도, 로고, UI skin, icon set, 서명적 형태 조합과 특정 작가 스타일 모사를 적는다.

외부 원본은 제품 build/store package에서 제외하고 `REFERENCE` 또는 `BENCHMARK` record로 관리한다. 생성 결과는 별도 `final_asset_record`를 가지며 similarity review를 수행한다. 상업 사용·배포 권리나 독립 제작 근거가 부족하면 `RELEASE_BLOCKED_UNVERIFIED`를 유지한다.

## Primary Use and Reusable Visual Harvest

재사용 최적화가 1차 품질을 망치면 안 된다.

```text
Primary Use Gate
→ primary-use success
→ Reusable Visual Harvest Gate
→ reuse classification
→ optional reuse promotion
→ second-use validation
```

재사용 후보는 `REUSE_AS_IS / VARIANT_SEED / STRUCTURE_PATTERN / STYLE_DNA / REBUILD_FOR_REUSE / ONE_OFF_KEEP / REJECT_REUSE`로 분류할 수 있다. 필요하면 `SOURCE_LAYER / MASK_CUTOUT / MANUAL_OR_SEMANTIC_REBUILD / DERIVED_GENERATIVE_RECOVERY` 같은 decomposition method를 기록한다.

`reuse promotion`은 `PROJECT_ASSET_APPROVED`, rights, title-specific identity를 우회하지 않는다.

## Evidence and readback

최소 기록:

```yaml
project_relation:
coverage_item_id:
coverage_status:
state_family_status:
requirement_id:
mode:
model_or_service:
input_reference_ids: []
approved_visual_reference_ids: []
screen_id:
flow_id:
output_locator:
readback_status:
interpretation_status:
reference_similarity_status:
review_status:
project_asset_status:
runtime_compare_required:
runtime_capture_path:
drift_status:
```

Notion image/file replacement은 target을 다시 fetch해서 expected file/preview/version을 확인한다. Runtime 결과는 별도 build/capture/test evidence가 있어야 `APPLIED_AND_RUNTIME_VERIFIED`다.

## Output

작업 성격에 따라 다음 중 필요한 것만 낸다.

- image generation/edit prompt
- `templates/planning/ART_TECHNIQUE_CARD.md` technique card
- Visual Asset Coverage 연결
- Visual Requirement 연결
- Project continuity card
- Screen Interpretation Review
- candidate QA / revision prompt
- reuse classification / harvest record
- Notion Asset/Knowledge record update
- repository implementation handoff
- explicit unverified / blocker report

완료 보고에는 실제로 생성·업로드·readback·승인·runtime 검증한 항목과 실행하지 않은 항목을 분리한다.
