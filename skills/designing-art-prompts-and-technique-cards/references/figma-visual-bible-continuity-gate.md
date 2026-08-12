# Figma Visual Bible Continuity Gate

이 reference는 `designing-art-prompts-and-technique-cards`의 이미지·UI 시각 자료 생성/편집/검수에서 프로젝트별 Figma Visual Bible을 **승인 시각 레퍼런스 작업면**으로 소비하는 절차를 정의한다.

## Trigger

다음 조건 중 하나가 참이면 적용한다.

- 사용자가 프로젝트 이미지 생성 또는 이미지 편집을 요청했다.
- UI/HUD/icon/VFX/environment/character/battlefield/marketing visual을 새로 만든다.
- 기존 시각 자료와의 일관성 유지가 완료 기준이다.
- 프로젝트 Visual Artifact Registry가 Figma Artifact를 가리킨다.
- 사용자가 Figma를 시각 레퍼런스 보관소로 사용한다고 선언했다.

단, 이미지 생성 자체의 필요성은 상위 `Visual Requirement Gate`가 먼저 판정한다.

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

### 8. Approval sync

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

## Figma organization mapping

| Figma | Workflow meaning |
|---|---|
| `00_DIRECTION` | 방향·금지 drift 확인 |
| `01_APPROVED_REFERENCE` | 승인 비교 기준 |
| `02_WIP` | 생성·수정·비교 중 |
| `03_REJECTED` | 불채택 및 이유 보존 |
| `04_FINAL` | 시각적 확정 표현; 제품 승인과 별개 |

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

P0/P1 충돌이 남으면 승인 승격을 멈춘다.

## Output contract

완료 보고에는 최소 다음을 분리한다.

```yaml
figma_reference_checked:
reference_ids: []
continuity_pass:
changes_made:
protected_elements:
known_drift_or_conflicts: []
figma_sync_status:
asset_promotion_status:
validation_status:
unverified: []
```
