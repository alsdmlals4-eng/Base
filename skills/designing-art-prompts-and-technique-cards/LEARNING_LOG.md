# Designing Art Prompts and Technique Cards Learning Log

## 2026-08-12 — 프로젝트 Figma는 승인 시각 레퍼런스 작업면으로 소비한다

### Trigger

프로젝트마다 이미지·UI·시각 자료를 Figma에 축적하고, 이후 생성·편집에서 승인된 시각 자료를 다시 확인하여 캐릭터 비율·실루엣·색·카메라·UI 계층의 drift를 줄이려는 반복 운영 요구가 확인됐다.

### Existing solution reviewed

- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`의 Figma/Whimsical 권위와 Artifact lifecycle
- `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`의 file/page/frame/node·Decision·snapshot 추적
- 이 Skill의 기존 생성·QA 책임
- `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`의 실제 이미지 bytes 후보·제품 승격 권위
- Figma 공식 Pages, Sections, Components/Styles/Libraries, naming, version history/branch 운영 가이드

### Lesson

- 별도 `figma-*` Skill을 만드는 것보다 기존 Art Skill이 승인된 Figma Artifact를 **조건부 입력**으로 소비하는 편이 책임 중복이 적다.
- Figma는 게임 규칙의 두 번째 canon이나 이미지 bytes 원본 저장소가 아니라 **Visual Bible / 승인 시각 레퍼런스 작업면**으로 두는 것이 안전하다.
- `00_DIRECTION / 01_APPROVED_REFERENCE / 02_WIP / 03_REJECTED / 04_FINAL`은 사람·AI가 탐색하는 Figma 조직 규칙이며 Base의 Artifact lifecycle을 대체하지 않는다.
- `04_FINAL`은 시각적으로 확정된 표현을 모으는 위치일 뿐 `PROJECT_ASSET_APPROVED`, tracked asset, Godot runtime proof를 자동 의미하지 않는다.
- 이미지 생성 전에는 최신 canon·Decision을 먼저 확인하고, 실제로 읽을 수 있는 `APPROVED_VISUAL_REFERENCE`만 `Keep / Avoid / Do Not Drift` 계약으로 추출한다.
- Figma 접근 실패는 과거 대화나 파일명으로 메우지 않고 `LINK_UNVERIFIED / AUTH_REQUIRED / ACCESS_DENIED / BLOCKED_UNVERIFIED`처럼 fail closed한다.

### Base change

- 기존 `VISUAL_COLLABORATION_TOOL_POLICY`에 Project Figma Visual Bible 경계를 흡수했다.
- 프로젝트 로컬 `FIGMA_VISUAL_BIBLE_PROFILE.md` Template을 추가했다.
- 기존 Art Skill 아래 `figma-visual-bible-continuity-gate.md` reference를 추가하고 Skill 본문에서 명시 소비한다.
- `GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`에 Figma 승인 reference·WIP·sync 상태를 연결했다.
- 신규 Figma Skill은 추가하지 않았다.

### Guardrail

Figma가 없는 프로젝트에 Figma 도입을 강제하지 않는다. 프로젝트의 최신 정본과 Figma가 충돌하면 Figma를 자동 갱신하거나 기획을 덮어쓰지 않고 `VISUAL_CANONICAL_CONFLICT`로 분리한다. 실제 제품 자산 승격은 기존 asset-vault·provenance·runtime 검증 절차를 그대로 따른다.

### Validation state

```yaml
figma_visual_bible_profile: IMPLEMENTED_ON_FEATURE_BRANCH
art_skill_continuity_gate: IMPLEMENTED_ON_FEATURE_BRANCH
visual_contract_tests: IMPLEMENTED_ON_FEATURE_BRANCH
project_specific_figma_pilot: NOT_RUN
figma_live_file_write_and_read_validation: NOT_RUN
runtime_asset_validation: NOT_RUN
```

실제 프로젝트별 Figma file/page/frame 구조와 레퍼런스 품질은 각 프로젝트에서 pilot 후 조정한다.

---

## 2026-08-08 — 프로젝트 시각물은 생성 전에 필요성부터 선정한다

### Trigger

프로젝트마다 필요한 이미지·시각 자산·UI 컴포넌트를 일관된 기준으로 고르고, 불필요한 생성·중복 컴포넌트·장식 과잉을 줄이면서 Art/UX/Vertical Slice/Asset Vault의 기존 책임을 보존할 필요가 생겼다.

### Evidence reviewed

- Base `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`, `GAME_UX_UI_SYSTEM.md`, GPT 이미지 정책, Vertical Slice Skill
- `evaluating-godot-assets-and-plugins-before-creation`의 Existing Solution First Gate
- 프로젝트 로컬 Asset Vault의 후보 파일·promotion·Manifest 권위 경계
- Apple·Atlassian·Godot·Xbox Accessibility·W3C·GDC의 요소 필요성, 재사용, 접근성, pre-production 평가 관행

### Lesson

- 이미지나 컴포넌트 제작법보다 먼저 `왜 필요한가`를 판정해야 한다.
- 공용 판단은 `Visual Requirement Gate`의 `필요성 → Delete Test → 재사용 → role → P0~P3 → disposition → validation` 순서로 충분하며 새 광역 Skill은 필요하지 않다.
- 단발 이미지 생성 요청과 프로젝트 전체 자산 선정은 분리한다. 단발 요청은 현재 작업의 임시 requirement가 될 수 있지만 지속 자산 목록이나 승인 상태를 자동 생성하지 않는다.
- Vertical Slice는 모든 시각물을 미리 만들지 않고 P0/P1과 제작성을 증명하는 필요한 P2만 우선한다.
- `Visual Requirement Gate`, `ASSET_MANIFEST.yml`, Asset Vault는 각각 필요성 판단, 승인 자산 의미, 실제 로컬 파일을 소유하며 하나의 원장으로 합치지 않는다.

### Base change

- 새 `selecting-project-visual-assets` 같은 광역 Skill을 추가하지 않았다.
- 기존 Art Guide에 Gate를 흡수하고 Art prompt·Vertical Slice·Art/UX 템플릿·이미지 정책이 이를 소비하게 했다.
- 전용 회귀 테스트와 기존 BCA 시각 워크플로 회귀를 함께 사용한다.

### Guardrail

이 학습은 모든 시각물을 삭제하거나 모든 단발 이미지 요청에 문서 작성을 강제하지 않는다. `DECORATIVE`도 코어 감정·정체성에 관찰 가능한 가치가 있으면 우선순위를 올릴 수 있으며, 프로젝트 외 단발 이미지 요청은 현 작업 범위에서 바로 생성할 수 있다.

### Validation state

```yaml
visual_requirement_contract_test: IMPLEMENTED
existing_bca_companion_test: IMPLEMENTED
project_pilot: NOT_RUN
human_art_pipeline_validation: HUMAN_NOT_RUN
runtime_asset_validation: NOT_RUN
```

프로젝트 Pilot과 실제 제작 반복성이 쌓이기 전에는 세부 숫자나 특정 자산 목록을 공용 강제 규칙으로 승격하지 않는다.