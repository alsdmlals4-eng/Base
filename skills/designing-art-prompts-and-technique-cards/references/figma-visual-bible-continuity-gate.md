# Figma Visual Bible Continuity Gate

이 reference는 `designing-art-prompts-and-technique-cards`의 이미지·UI 시각 자료 생성/편집/검수에서 프로젝트별 Figma Visual Bible을 **승인 시각 레퍼런스 작업면**으로 소비하고, 화면 시각화의 해석·흐름을 다시 Figma에 연결하는 절차를 정의한다.

## Trigger

다음 조건 중 하나가 참이면 적용한다.

- 사용자가 프로젝트 이미지 생성 또는 이미지 편집을 요청했다.
- UI/HUD/icon/VFX/environment/character/battlefield/marketing visual을 새로 만든다.
- 기존 시각 자료와의 일관성 유지가 완료 기준이다.
- 프로젝트 Visual Artifact Registry가 Figma Artifact를 가리킨다.
- 사용자가 Figma를 시각 레퍼런스 보관소 또는 화면 Flow 작업면으로 사용한다고 선언했다.

단, 이미지 생성 자체의 필요성은 상위 `Visual Requirement Gate`가 먼저 판정한다.

## Conditional module routing

이 gate는 `FIGMA_DIRECT_VISUAL_ORGANIZATION`의 공통 진입점이다. 현재 작업에 필요한 reference만 추가로 읽는다.

| 조건 | 추가 reference |
|---|---|
| Figma에 생성 결과를 배치·정리하거나 승인 위치를 정해야 함 | `figma-direct-placement-and-canon.md` |
| 캐릭터 identity를 유지하며 표정·시선·머리 방향을 바꿈 | `character-identity-expression-controls.md` |
| pose/action/sprite sequence·pose sheet·atlas 후보를 만듦 | `sprite-pose-sequence-controls.md` |
| VFX/effect stage·alpha/compositing 후보를 만듦 | `effect-stage-compositing-controls.md` |
| 여러 후보 비교·선택 또는 primary-use 이후 재사용 판정 | `candidate-review-and-reusable-harvest.md` |
| Tool Hub/Expression/Sprite 로컬 런타임을 정상 경로로 쓸지 판단해야 함 | `local-visual-tool-lessons-and-fallback.md` |

모든 모듈을 기본 로드하지 않는다. 일반 이미지 작업은 기존 art Skill trigger로 이 gate에 들어오며, 별도 Figma/Expression/Sprite broad Skill을 만들지 않는다.

## Authority

```text
최신 사용자 지시
→ 프로젝트 정본·Decision·실제 사용 화면
→ APPROVED_VISUAL_REFERENCE Figma frame/node
→ 승인된 프로젝트 asset
→ WIP·Rejected·외부 발견 reference
```

Figma가 GitHub/GDD/Decision을 덮어쓰지 않는다. Figma와 정본이 충돌하면 `VISUAL_CANONICAL_CONFLICT`다.

실제 이미지 bytes의 후보·제품 자산 권위는 `PROJECT_LOCAL_ASSET_VAULT_POLICY`와 tracked asset lifecycle에 남는다.

## Required context

가능하면 다음을 확보한다.

```yaml
project_name:
requirement_id:
responsible_document_id:
related_decision_ids: []
figma_status:
figma_file_url:
figma_file_key:
approved_reference_ids: []
approved_frame_or_node_ids: []
comparison_scope:
keep: []
avoid: []
do_not_drift: []
wip_target:
screen_id:
flow_id:
interpretation_record_id:
```

프로젝트에 Figma가 구성되지 않았다면 `NOT_CONFIGURED`는 정상 상태다.

## Gate procedure

### 1. Confirm project canon

- 최신 프로젝트 정본과 Decision을 먼저 읽는다.
- 실제 시각 자료가 사용될 화면·상태·플랫폼·해상도·입력을 확인한다.
- 오래된 Figma 이미지가 최신 정본보다 우선하지 않게 한다.

### 2. Resolve Figma evidence

- `VISUAL_ARTIFACT_REGISTRY.json` 또는 프로젝트 책임 문서에서 관련 Figma Artifact를 찾는다.
- `01_APPROVED_REFERENCE`에 해당하는 Artifact는 최소 `APPROVED_VISUAL_REFERENCE`인지 확인한다.
- file/page/frame/node 식별자가 있으면 실제 접근 가능한 도구로 해당 node를 확인한다.
- node-specific evidence가 필요한데 file-level link만 있으면 그 한계를 기록한다.

### 3. Fail closed on access

다음 상태에서는 내용을 본 것으로 주장하지 않는다.

- `AUTH_REQUIRED`
- `ACCESS_DENIED`
- `READ_ONLY` (write 요청일 때)
- `LINK_UNVERIFIED`
- `UNVERIFIED`
- `SNAPSHOT_MISSING` (고정 snapshot이 완료 조건일 때)

이 경우 접근 가능한 승인 asset, Markdown art direction, text wireframe, 사용자가 현재 대화에 제공한 이미지로 fallback한다.

### 4. Extract continuity contract

승인 레퍼런스에서 단순히 “비슷하게”가 아니라 다음 축을 분리한다.

```text
identity/proportion
silhouette/shape language
palette/contrast
line/texture/material
lighting
camera/composition
UI density/hierarchy
icon language
text/localization constraints
protected motifs
forbidden drift
```

이를 `Keep / Avoid / Do Not Drift`로 변환한다.

### 5. Generate or edit

생성 계약 순서:

```text
목적·사용 화면·플레이어 경험
→ 최신 canon·Decision
→ approved Figma reference IDs
→ Keep / Avoid / Do Not Drift
→ 변경할 축
→ 구도·정보 위계
→ 형태·색·재질·광원
→ 화면비·해상도·크롭
→ 실패 조건·QA
```

승인 reference 자체의 식별 가능한 외부 IP/작가 스타일을 모사하도록 사용하지 않는다. 권리·유사성 검토는 기존 reference-to-original 정책을 따른다.

### 6. Put new work in review state

새 결과는 기본적으로 다음 중 하나다.

- `DRAFT_VISUAL`
- `REVIEW_CANDIDATE`
- 이미지 lifecycle의 `GENERATED_EXPLORATION / IN_REVIEW`

사용자 Decision 전에는 `01_APPROVED_REFERENCE`, `04_FINAL`, `PROJECT_ASSET_APPROVED`로 자동 승격하지 않는다.

Figma가 `CONFIGURED`이고 쓰기 가능하면 새 결과를 `02_WIP`에 배치하고 frame/node ID를 기록한다. 화면 시각화라면 다음 `INTERPRETATION_RECORD`도 화면 옆의 편집 가능한 text/annotation으로 남길 수 있다.

```yaml
screen_id:
flow_id:
visual_artifact_id:
related_decision_ids: []
source_commit:
confirmed: []
discovered_idea: []
ai_assumption: []
missing_canon: []
visual_canonical_conflict: []
rejected_expression: []
next_gate:
```

- `CONFIRMED`: 최신 정본과 일치.
- `DISCOVERED_IDEA`: 시각화가 제안한 미승인 아이디어.
- `AI_ASSUMPTION`: 정본 근거 없이 모델이 채워 넣은 요소.

`DISCOVERED_IDEA`와 `AI_ASSUMPTION`은 사용자 Decision 전에는 다음 프롬프트의 확정 조건이나 구현 요구로 자동 재사용하지 않는다.

### 7. Compare against approved references

최소 비교 항목:

- [ ] 캐릭터/오브젝트 비율
- [ ] 실루엣과 shape language
- [ ] palette·contrast
- [ ] line·texture·material
- [ ] lighting
- [ ] camera distance·angle·composition
- [ ] UI hierarchy·density·readability
- [ ] icon/VFX visual grammar
- [ ] 세계관·캐릭터·시스템 정본
- [ ] 실제 사용 화면에서의 가독성

판정:

```text
PASS
REVISION_REQUIRED
VISUAL_CANONICAL_CONFLICT
BLOCKED_UNVERIFIED
```

### 8. Update visual flow when screens connect

한 작업이 다른 화면으로의 진입·전환·복귀를 만들면 `FLOW_MAP`에서 `screen_id / flow_id`와 화살표 연결을 갱신한다. 실제 클릭 검토가 필요할 때만 `PROTOTYPE_FLOW`를 추가한다.

최소 흐름 점검:

- [ ] 진입점이 명확하다.
- [ ] primary path가 연결된다.
- [ ] 취소/뒤로가기 목적지가 정해져 있다.
- [ ] 실패·오류 뒤 복구 경로가 있다.
- [ ] 동일 기능을 불필요하게 여러 화면에서 왕복하지 않는다.

Prototype은 실제 Godot runtime proof가 아니다.

### 9. Approval sync

사용자 승인 뒤에만 수행한다.

```text
Decision
→ responsible art/UI/system document
→ Visual Artifact Registry
→ Figma Approved/Final organization
→ project Sheet image approval log (configured only)
```

제품 asset인 경우 별도:

```text
PROJECT_ASSET_APPROVED
→ asset-vault promote
→ tracked asset
→ ASSET_MANIFEST/provenance
→ Godot consumer
→ runtime validation
```

### 10. Compare implementation when runtime evidence exists

`IMPLEMENTATION_PINNED` 화면의 실제 `RUNTIME_CAPTURE`가 확보되면 승인 시각 참조와 `COMPARE_BOARD`에서 비교한다.

```text
MATCHED
INTENDED_DIFFERENCE
IMPLEMENTATION_GAP
PLANNING_CHANGE_REQUIRED
AI_MOCKUP_ERROR
VISUAL_CANONICAL_CONFLICT
BLOCKED_UNVERIFIED
```

실제 runtime 캡처가 없으면 `MATCHED`로 표시하지 않는다.

## Figma organization mapping

| Figma | Workflow meaning |
|---|---|
| `00_DIRECTION / 00.8_VISUAL_FLOW_HUB` | 방향·금지 drift·대표 `FLOW_MAP` 확인 |
| `01_APPROVED_REFERENCE` | 승인 비교 기준 |
| `02_WIP / 02.5_FLOW_PROTOTYPE` | 생성·수정·Prototype 비교 중 |
| `02_WIP / 02.6_GPT_INTERPRETATION` | `INTERPRETATION_RECORD` 편집·검토 |
| `03_REJECTED` | 불채택 및 이유 보존 |
| `04_FINAL / 04.2_IMPLEMENTATION_COMPARE` | 시각적 확정 표현과 runtime 비교; 제품 승인과 별개 |

프로젝트 세부 구조는 `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`를 따른다.

## Adversarial regression check

작업 종료 전 다음을 공격한다.

1. WIP나 Rejected를 승인 reference처럼 사용했는가.
2. 오래된 Figma가 최신 Decision을 덮었는가.
3. 접근하지 못한 node를 봤다고 주장했는가.
4. 시각적으로 Final이라는 이유로 제품 asset 승인까지 건너뛰었는가.
5. 새 결과가 기존 캐릭터/UI/환경 visual grammar를 이유 없이 바꿨는가.
6. 일관성 유지를 핑계로 새로운 요구의 의도까지 억제했는가.
7. Figma만 갱신하고 Registry/Decision 연결을 잊었는가.
8. `DISCOVERED_IDEA`나 `AI_ASSUMPTION`을 승인 없이 다음 요구로 굳혔는가.
9. Prototype을 runtime proof로 과장했는가.
10. 실제 구현 drift를 초기 AI 목업과 비교하면서 현재 정본·Decision을 건너뛰었는가.
11. Figma write 요청 성공만 보고 readback 없이 `AUTO_PLACE_WIP` 성공을 주장했는가.
12. 정상 이미지 작업을 이유 없이 Tool Hub/PowerShell/localhost delivery 경로로 되돌렸는가.

P0/P1 충돌이 남으면 승인 승격을 멈춘다.

## Output contract

완료 보고에는 최소 다음을 분리한다.

```yaml
figma_reference_checked:
reference_ids: []
continuity_pass:
interpretation_record_status:
flow_map_status:
changes_made:
protected_elements:
known_drift_or_conflicts: []
figma_sync_status:
asset_promotion_status:
runtime_compare_status:
validation_status:
unverified: []
```
