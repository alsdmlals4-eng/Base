# Designing Art Prompts and Technique Cards Learning Log

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
