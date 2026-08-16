# Reusable Visual Asset Harvest Pipeline Design

## Status

```yaml
status_scope: DESIGN_APPROVAL_SNAPSHOT
work_mode: PLAN
base_main: 66818010e52b10d1f0a8ab9d008ec1450450ed75
design_direction: APPROVED_BY_USER
benchmark_validation: COMPLETED
implementation: NOT_STARTED_AT_DESIGN_APPROVAL
runtime_or_figma_mutation: NOT_RUN_AT_DESIGN_APPROVAL
implementation_tracking: PR_433_BODY_AND_EXACT_HEAD_CI
open_pr_428_boundary: READ_ONLY_NOT_MODIFIED
new_skill_or_mode: NONE
```

## 1. Direction anchor

시각 작업의 기본 목적은 완성 이미지 한 장을 만드는 데서 끝나지 않는다. 먼저 **현재 플레이어/사용자 경험을 위한 좋은 이미지를 제안하고 승인받아 실제 목적에 사용**한 뒤, 그 결과에서 반복 가치가 검증된 요소만 구조화하여 프로젝트의 다음 시각 작업이 더 빠르고 더 일관되게 시작하도록 한다.

사용자에게 보이는 기본 순서는 다음과 같다.

```text
이미지/사진 시각안 제안
→ 사용자 승인
→ 이미지 제작
→ 원래 목적에 실제 사용
→ 완성 결과 분석
→ 재사용 가치가 있는 요소만 분류
→ 필요한 요소만 구조화·레이어화·재구축
→ 재사용 자산/구조/Visual DNA로 축적
→ 다음 작업에서 우선 재사용 또는 변형
```

새 이미지를 제안하기 전 내부 preflight에서는 기존 승인 자산·Figma Visual Bible·프로젝트 Visual DNA를 조회해 중복 생성을 피한다. 이 preflight는 사용자 승인 Gate를 생략하지 않는다.

## 2. Benchmark and practice findings

### 2.1 Figma design-system pattern — REUSE

Figma의 Components/Instances/Libraries/Variants는 한 번 만든 요소를 여러 화면에서 재사용하고, 원본 변경을 여러 instance에 전달하며, predictable variation을 component set으로 관리한다. 이는 `재사용 가능한 요소를 별도 owner로 승격하고 변형은 variant로 관리`하는 구조를 지지한다.

- Components: https://help.figma.com/hc/en-us/articles/360038662654-Guide-to%20-components-in-Figma
- Libraries: https://help.figma.com/hc/en-us/articles/39723547036055-Components-collection-Library-fundamentals
- Variants: https://help.figma.com/hc/en-us/articles/39636737843735-Components-collection-Variants-and-component-set-fundamentals

Disposition:

```yaml
figma_components_and_variants: REUSE_PRINCIPLE
publish_every_visual_as_component: REJECT
```

모든 화면을 component로 만들지 않는다. 실제 반복 가치가 있는 버튼·패널·아이콘·레이아웃 패턴만 component/variant 후보가 된다.

### 2.2 Game production cases — REUSE + PRESERVE TITLE IDENTITY

King의 게임 디자인 운영 사례에서는 Figma 도입 전 일러스트·아이콘·transition·sound가 여러 출처에 흩어져 있고 공용 component library가 부족했으며, 이후 한 작업면과 공용 프로세스로 협업성과 가시성을 높였다. 게임 엔진 최적화와 art direction 정렬은 별도 중요 경계로 남는다.

- https://www.figma.com/customers/how-king-brings-game-design-together/

Capcom은 variables와 component-based templates로 반복 재발명을 줄이고 과거 자산 재사용을 촉진하면서, 각 게임 타이틀의 고유 visual identity를 방해하지 않도록 공용 시스템 자체는 가능한 primitive/character-neutral하게 유지하는 방향을 설명한다.

- https://www.figma.com/customers/how-capcom-elevates-speed-quality-and-creative-vision-with-figma/

Unity의 Survival Kids 사례는 최종 게임 자산을 재사용 가능한 prefab building blocks로 구성해 whitebox에 가까운 빠른 level iteration을 가능하게 했다.

- https://unity.com/blog/level-layout-and-terrain-workflows-in-survival-kids

Disposition:

```yaml
shared_visual_primitives: REUSE
project_or_title_specific_identity: PROTECT
one_off_visuals_forced_into_library: REJECT
```

### 2.3 Mature design-system promotion gate — ADOPT

GOV.UK Design System은 공용 component/pattern 제안에 여러 팀/서비스에서 유용하다는 증거와 기존 component와의 비중복성을 요구하고, 개발 전에 `Start with what exists`를 권장한다.

- https://design-system.service.gov.uk/community/contribution-criteria/
- https://design-system.service.gov.uk/community/develop-a-component-or-pattern/

Base에는 이를 시각 자산에 맞춰 다음처럼 변형 적용한다.

```text
잘라낼 수 있다 ≠ 재사용 자산이다
반복 가치가 있다 + 기존 것과 중복되지 않는다 + 독립 사용이 가능하다
→ 구조화 후보
```

### 2.4 Godot reuse model — REUSE

Godot scenes는 재사용·인스턴스화 가능한 구조이며 `PackedScene`은 여러 번 instantiate할 수 있다. `Resource`는 이미지·scene·animation·font 등을 포함한 data container이고, UI `Theme`은 같은 type의 Control에 공통 스타일을 적용할 수 있다. 작은 texture는 필요할 때 atlas로 묶어 draw-call/memory 비용을 줄일 수 있다.

- https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html
- https://docs.godotengine.org/en/4.6/getting_started/step_by_step/instancing.html
- https://docs.godotengine.org/en/stable/classes/class_theme.html
- https://docs.godotengine.org/en/stable/classes/class_atlastexture.html

따라서 재사용 결과는 PNG 조각만 의미하지 않는다. 경우에 따라 Godot Theme, reusable scene, Resource, atlas-ready texture set으로 승격하는 편이 더 적합하다.

### 2.5 Layer decomposition research — HYBRID_ONLY

SAM 2는 이미지/비디오의 객체 segmentation에 강한 기반을 제공하지만 segmentation 자체는 가려진 픽셀을 복원하지 않는다.

- https://ai.meta.com/research/publications/sam-2-segment-anything-in-images-and-videos/

CVPR 2025 LayerDecomp은 clean background와 transparent foreground, shadow/reflection 같은 visual effects를 포함한 layer decomposition을 다루고, CVPR 2026 DiffDecompose와 Qwen-Image-Layered 등은 alpha-composited/semantic RGBA layer decomposition을 확장한다. 동시에 투명·반투명 layer, occlusion, shading/reflection은 여전히 어려운 문제로 명시된다.

- https://openaccess.thecvf.com/content/CVPR2025/html/Yang_Generative_Image_Layer_Decomposition_with_Visual_Effects_CVPR_2025_paper.html
- https://openaccess.thecvf.com/content/CVPR2026/html/Wang_DiffDecompose_Layer-Wise_Decomposition_of_Alpha-Composited_Images_via_Diffusion_Transformers_CVPR_2026_paper.html
- https://openaccess.thecvf.com/content/CVPR2026/html/Yin_Qwen-Image-Layered_Towards_Inherent_Editability_via_Layer_Decomposition_CVPR_2026_paper.html

Disposition:

```yaml
mask_or_cutout_for_visible_pixels: REUSE_AS_OPTION
occlusion_recovery: EXPERIMENTAL_DERIVED_PIXELS
fully_automatic_decompose_and_auto_promote: REJECT
human_review_before_reuse: REQUIRED
```

## 3. Selected architecture — Produce first, harvest second

### Loop A — Production loop

```text
0. existing approved asset / Visual Bible lookup
1. visual proposal
2. user approval
3. image production
4. primary-use placement or design consumption
5. primary-use review
```

규칙:

- 우선 목표는 해당 화면·배경·인게임 장면이 자신의 목적을 잘 수행하는 것이다.
- 재사용성을 위해 원래 이미지 품질·감정·정보 위계를 희생하지 않는다.
- 생성 중 분리 가능성을 보존할 수 있는 경우 clean plate, textless version, transparency-friendly source 같은 저비용 보조 산출물을 만들 수 있지만 **사전 자산화가 본 제작을 지배하지 않는다**.

### Loop B — Harvest loop

Primary-use review를 통과한 결과만 다음 질문을 받는다.

```text
이 요소가 다른 화면/장면에서 동일 역할로 다시 쓰일 가능성이 높은가?
→ 기존 reusable asset과 중복되는가?
→ 독립적으로 편집/배치 가능한가?
→ 분리 비용보다 다음 사용에서 줄일 비용이 큰가?
→ 고유 장면의 정체성을 훼손하지 않는가?
```

통과 후보만 구조화한다.

## 4. Harvest classifications

| classification | 의미 | 대표 예 |
| --- | --- | --- |
| `REUSE_AS_IS` | 동일 bytes/구조를 그대로 재사용 | 아이콘, 프레임, prop |
| `VARIANT_SEED` | 기준 자산에서 상태/색/테마 변형 | normal/hover/pressed, day/night |
| `STRUCTURE_PATTERN` | 픽셀이 아니라 배치·hierarchy·interaction 구조 재사용 | 전투 HUD, 보상 화면 layout |
| `STYLE_DNA` | palette·shape·material·lighting·camera·spacing 규칙 재사용 | 프로젝트 시각 문법 |
| `REBUILD_FOR_REUSE` | raster 추출보다 component/scene/theme로 다시 만드는 것이 안전 | 버튼, scalable panel, UI skin |
| `ONE_OFF_KEEP` | 현재 결과에는 중요하지만 공용화 가치가 낮음 | 특정 이벤트 일러스트 |
| `REJECT_REUSE` | 오류·중복·저품질·권리·정체성 위험 때문에 재사용 금지 | 잘못 분리된 손/그림자 |

한 후보가 `REUSE_AS_IS + STYLE_DNA`처럼 둘 이상의 의미를 가질 수 있지만 bytes owner와 style rule owner는 분리한다.

## 5. Asset-type-specific rules

### 5.1 In-game composite / scene concept

우선 분리 후보:

- background depth layer
- foreground overlay
- 독립 prop
- character/object silhouette가 다른 장면에서도 필요한 경우
- 독립 FX가 의미 있게 재사용 가능한 경우

단, 특정 장면의 조명·그림자·접촉 효과가 오브젝트 관계에 의존하면 무리하게 공용 layer로 만들지 않는다.

### 5.2 Background

다음 사용처가 있을 때만 depth/parallax layer화를 우선한다.

- camera pan/parallax
- day/night/season variant
- foreground occluder 재배치
- 동일 장소의 여러 장면 재사용

정적인 단발 일러스트는 `ONE_OFF_KEEP`가 정상 판정일 수 있다.

### 5.3 UX/UI screen

생성된 UX 화면에서 버튼·panel을 단순 crop해서 장기 자산으로 쓰는 것을 기본값으로 하지 않는다.

```text
화면에서 구조/스타일 발견
→ reusable primitive 여부 판정
→ Figma component/variant 또는 Godot Theme/scene으로 semantic rebuild
→ 상태·입력·localization·accessibility 검증
```

픽셀 추출은 icon/illustration/decorative texture처럼 raster 자체가 의미 있는 경우에 우선한다.

## 6. Decomposition ladder

가장 낮은 위험 방법부터 사용한다.

```text
1. SOURCE_LAYER
   원본 제작 단계에서 이미 독립 layer/file이 있음

2. MASK_CUTOUT
   현재 보이는 픽셀만 mask/matting으로 분리

3. MANUAL_OR_SEMANTIC_REBUILD
   UI component, scalable panel, structured prop을 다시 제작

4. GENERATIVE_OCCLUSION_RECOVERY
   가려진 영역이 독립 재사용에 반드시 필요한 경우만 생성 복원
```

`GENERATIVE_OCCLUSION_RECOVERY` 결과는 원본에 없던 추정 픽셀을 포함하므로 provenance에 `DERIVED_GENERATIVE_RECOVERY`를 기록하고 원본 사실로 간주하지 않는다.

## 7. Recomposition and reuse gate

구조화 완료는 파일 생성으로 판정하지 않는다.

필수 검토:

1. 원래 primary-use 이미지와 의미·구도·정체성이 유지되는가
2. 독립 layer/component가 잘못된 halo, edge, shadow, alpha artifact를 갖지 않는가
3. recomposed preview가 의도한 원본 표현을 충분히 재현하는가
4. 재사용 target에서 scale/crop/state/localization 문제가 없는가
5. 기존 reusable asset과 역할 중복이 없는가
6. source/rights/provenance가 추적되는가
7. Figma/Godot에서 무엇이 visual reference이고 무엇이 runtime asset인지 구분되는가

숫자 하나의 자동 similarity score만으로 승인하지 않는다.

## 8. Authority and storage

```text
GitHub canonical planning / Decision
  → 왜 필요한지, 승인, 사용 규칙

Figma Visual Bible
  → 승인 시각 방향, WIP 비교, reusable component/pattern reference

.asset-vault
  → 실제 후보 bytes, 구조화 산출물, review candidate

ASSET_MANIFEST.yml + promote
  → PROJECT_ASSET_APPROVED 이후 tracked 제품 자산

Godot Scene / Resource / Theme + runtime evidence
  → 실제 게임 재사용과 검증
```

Figma의 `04_FINAL`이나 component 등록만으로 `PROJECT_ASSET_APPROVED`가 되지 않는다. Asset Vault의 구조화 후보도 자동 promote하지 않는다.

## 9. Reuse-first behavior on the next task

새 시각 요청이 들어오면 다음을 내부적으로 먼저 확인한다.

```text
기존 APPROVED visual/reference
→ REUSE_AS_IS 가능?
→ VARIANT_SEED로 해결 가능?
→ STRUCTURE_PATTERN/STYLE_DNA를 적용해 새 제안 가능?
→ 모두 아니면 신규 visual proposal
```

사용자에게는 신규 제작이 필요한 경우 **시각안 제안 → 승인 → 제작** Gate를 그대로 유지한다.

## 10. Adversarial review

### Attack A — “모든 완성 이미지를 자동 layer pack으로 만들면 더 많이 재사용할 수 있다”

판정: `REJECTED_CRITIQUE_OF_SELECTED_DESIGN`가 아니라 **대안 자체를 REJECT**.

근거:

- 일회성 자산까지 공용 library에 들어가 탐색 비용과 중복이 증가한다.
- 투명/반투명·그림자·reflection·occlusion은 자동 decomposition 오류가 발생할 수 있다.
- UI는 raster crop보다 component/theme로 재구축해야 상태·크기·localization을 안전하게 다룰 수 있다.

### Attack B — “사용 후에만 생각하면 재사용하기 좋은 source를 놓친다”

판정: `SHOULD_FIX` → selected design에 반영.

최소 개선:

- 제작 중 **저비용 separation hint**만 보존한다.
- textless/clean plate/transparent source가 자연스럽게 가능한 경우 유지한다.
- 하지만 실제 구조화·library 승격은 primary-use 이후 Harvest Gate가 결정한다.

### Attack C — “한 번 쓰였다고 재사용 가치가 증명되는 것은 아니다”

판정: `MUST_FIX` → selected design에 반영.

`primary-use success`와 `reuse promotion`은 별도 판정이다. 재사용 승격은 `다른 사용처에서 유용할 근거 + 비중복 + 독립성`을 추가로 요구한다.

### Attack D — “공용화가 게임 고유 이미지를 평준화한다”

판정: `MUST_FIX` → project identity protection.

공용화 대상은 primitive, pattern, style rule, 반복 prop 중심으로 제한한다. 특정 장면의 영웅 이미지, narrative composition, 타이틀 고유 identity는 `ONE_OFF_KEEP`가 정상이다.

### Attack E — “생성형 occlusion recovery가 원본을 복원한다”

판정: `MUST_FIX` → provenance guard.

가려진 픽셀은 관측된 사실이 아니라 생성 추정일 수 있으므로 `DERIVED_GENERATIVE_RECOVERY`로 분류하고 별도 시각 검토를 요구한다.

## 11. Existing Solution First disposition

```yaml
Visual_Requirement_Gate: REUSE
GPT_Image_Generation_Review_Policy: ABSORB_FUTURE_IMPLEMENTATION
Figma_Visual_Bible: REUSE
Project_Local_Asset_Vault: REUSE
ASSET_MANIFEST_and_promote: REUSE
Godot_Theme_Scene_Resource: REUSE_AS_RUNTIME_TARGET
new_broad_skill: REJECT
new_parallel_asset_canon: REJECT
new_tool_hub_owner: REJECT
layer_decomposition_adapter: DEFER_TO_BOUNDED_FUTURE_IMPLEMENTATION
```

## 12. Scope boundaries

현재 설계가 허용하는 후속 구현 범위:

- 기존 Art Direction / GPT image policy에 Production→Harvest 계약 흡수
- Asset Vault에 구조화 candidate metadata를 추가하는 bounded 설계
- Figma Visual Bible에 reusable component/pattern 연결 규칙 보강
- focused regression contract
- 실제 layer decomposition adapter는 독립 구현/평가 Gate 뒤 선택

현재 제외:

- PR #428 또는 그 owner 파일 수정
- 자동 Figma mutation 구현
- 실제 segmentation/decomposition model 설치
- 모든 기존 프로젝트 자산 일괄 migration
- user approval 없는 asset promotion
- 새 ACTIVE Skill/Mode/Registry owner

## 13. Pilot validation after implementation

첫 pilot은 서로 다른 성격의 세 결과물로 제한한다.

1. 인게임 composite 1개
2. 배경 1개
3. UX screen 1개

각 pilot에서 다음을 기록한다.

```yaml
primary_use_success:
reuse_candidates_found:
rejected_one_off_elements:
reuse_method:
manual_repair_required:
recomposition_result:
second_use_or_variant_result:
style_drift_findings:
asset_duplication_avoided:
runtime_or_figma_validation:
```

숫자 목표는 pilot evidence 없이 미리 강제하지 않는다.

## 14. Completion criteria for this design

- 사용자 순서 `제안 → 승인 → 제작 → 사용 → 구조화 → 재사용`이 보존된다.
- 재사용 때문에 primary visual quality가 희생되지 않는다.
- 모든 이미지를 자동 구조화하지 않는다.
- UX raster crop과 semantic component rebuild를 구분한다.
- generated occlusion pixels는 provenance가 분리된다.
- Figma / Asset Vault / Manifest / Godot 권위가 중복되지 않는다.
- 기존 reusable asset lookup이 다음 생성의 preflight가 된다.
- open PR #428은 수정하지 않는다.

## 15. Rollback

이 설계 단계의 롤백은 이 spec commit/branch를 폐기하는 것으로 끝난다. 제품 코드, 기존 자산, Figma 파일, Asset Vault schema, 프로젝트 데이터는 변경하지 않는다.
