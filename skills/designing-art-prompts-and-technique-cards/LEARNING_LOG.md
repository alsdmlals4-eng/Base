# Designing Art Prompts and Technique Cards Learning Log

## 2026-08-26 — 이미지 생성 전 Visual Asset Coverage를 별도 preflight로 확인한다

### Trigger

이미지 생성 Skill이 선정된 `requirement_id`를 정확히 실행하더라도, 프로젝트·화면군·캐릭터군 차원에서는 버튼 state, enemy telegraph, interaction feedback, input prompt, accessibility cue, store/platform asset처럼 **인접한 필수 시각 자산 자체가 requirement 후보로 떠오르지 않는 누락**이 남을 수 있다는 문제가 확인됐다.

### Evidence reviewed

- Base `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`, `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`, `VISUAL_COLLABORATION_TOOL_POLICY.md`, image plan과 current art Skill
- Godot official multiple-resolution, import process, texture/compression guidance
- Steamworks current graphical asset overview/rules/screenshot requirements
- W3C WCAG 2.1 Use of Color의 non-color redundant visual cue 원칙
- current open visual workstream의 path ownership과 existing explicit image approval boundary

### Lesson

이미지 생성 직전의 **누락 탐지**와 실제 **제작 선정·승인**은 다른 책임이어야 한다.

```text
Visual Asset Coverage Preflight
→ relevant gap discovery
→ Visual Requirement Gate
→ explicit image approval
→ generation / review / promotion / runtime evidence
```

- Coverage는 `COVERAGE_CHECK_ONLY`이며 second asset canon이 아니다.
- `NOT_APPLICABLE`을 허용해 장르·단계와 무관한 asset scope explosion을 막는다.
- 대표 이미지 하나가 아니라 consumer가 요구하는 `STATE_FAMILY_COMPLETENESS`를 확인한다.
- gap 발견은 `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`; 다음 이미지·variant·batch를 자동 승인하지 않는다.
- 실제 target resolution/aspect와 필요한 import/filter/mipmap/atlas/slicing/pivot/localization 조건을 requirement/handoff에 연결한다.
- store/platform asset은 stale fixed size를 Base 장기 정답으로 두지 않고 `PLATFORM_SPEC_RECHECK_REQUIRED`로 release 시 current official rule을 다시 확인한다.

### Base change

- `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`를 subordinate coverage guide로 추가한다.
- `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`가 넓은 시각 범위 작업에서 coverage preflight를 Visual Requirement Gate보다 먼저 확인한다.
- 이 Skill은 `coverage_item_id / coverage_status / state_family_status`를 입력으로 소비하되 gap을 자동 생성 queue로 바꾸지 않는다.
- 기존 Image Conversation Approval Gate, Asset lifecycle, Notion authority, runtime evidence는 유지한다.

### Guardrail

- coverage status != asset lifecycle
- gap != generation approval
- concept/reference != runtime/gameplay evidence
- current platform specification은 release 시 official source를 다시 확인한다.

### Validation state

```yaml
coverage_static_contract: IMPLEMENTED_ON_PR_717
focused_regression: IN_CI
canonical_freshness_companion_sync: IMPLEMENTED_ON_PR_717
project_image_generation: NOT_RUN
notion_delivery: NOT_RUN
runtime_asset_validation: NOT_RUN
```

---

## 2026-08-19 — 시각 작업면은 Notion Project relation으로 통합하고 도구별 지식은 중립 모듈로 흡수한다

### Trigger

실제 프로젝트 작업에서 시각 자료·작업계획·자산 도서관·UI/관계 Flow를 여러 링크와 별도 실행면으로 분산하면 최신 Project를 오인하기 쉽다는 문제가 확인됐다. 동일 시점에 이미지 생성 → Notion 파일 업로드 → 페이지 배치 → Version 교체 → readback, Asset DB Gallery와 AI/System metadata 분리가 실제 파일럿에서 성공했다.

### Evidence reviewed

- 단일 Notion workspace 안의 8개 Project Registry와 Project-filtered linked view readback
- 이미지 파일 5 MiB 이하 upload → Notion-owned attachment → Version replacement → fetch readback
- 구형 localhost 시각 실행 경로의 반복 실패·stop-loss 기록
- 기존 character identity/expression, pose/sequence, effect stage/compositing, candidate/reuse Harvest reference
- `Visual Requirement Gate`, Asset Vault, runtime QA의 기존 권위 경계

### Lesson

- 시각 작업의 장기 재사용 가치는 특정 도구 runtime이 아니라 **Project identity, source provenance, bounded edit, approval, version/replacement, reuse classification, readback, runtime handoff**에 있다.
- 하나의 workspace를 써도 `PROJECT_RELATION_REQUIRED`와 project-filtered view를 강제하면 Project 간 자료 혼입을 줄일 수 있다.
- 사람은 Preview/Name/Usage/Style/Approved/Reuse 위주 Gallery를 보고, AI/System은 Asset ID·Version·Prompt·Source·Rights·Hash·Implementation Path 같은 상세 metadata를 유지하는 편이 가독성과 자동화를 동시에 만족한다.
- `VISUAL_MAP_DERIVED`는 사람이 한눈에 보는 파생 표현이고 Screen/relationship record가 의미를 소유한다. 그림과 record가 충돌하면 그림을 고친다.
- 이미지 upload 성공만으로 완료를 주장하지 않는다. correct Project target을 다시 읽어 file/preview/version/status를 확인해야 delivery가 완료된다.
- identity-preserving edit, pose sequence, effect stage, reusable harvest는 특정 시각 collaboration product와 무관한 generic reference로 유지할 가치가 있다.
- dedicated localhost visual Studio/bridge를 새로 복구하는 것보다 ChatGPT image generation + Notion attach/readback + repository runtime handoff가 총 수명주기 비용이 낮다.

### Base change

- `notion-project-visual-continuity-gate.md`를 current Project visual continuity gate로 승격했다.
- character / sprite-pose / effect / candidate-reuse generic reference는 유지했다.
- 구형 product-specific placement/continuity/fallback reference는 제거했다.
- `GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`을 Project relation, approved visual reference, readback, semantic Screen/flow, runtime compare 중심으로 전환했다.
- 별도 broad Skill은 추가하지 않았다.

### Guardrail

- Notion approval이나 Visual Map은 Godot/runtime proof가 아니다.
- Project relation이 불명확하면 이웃 Project reference를 추정 재사용하지 않는다.
- Reference/Benchmark는 source/right boundary를 기록하고 identifiable expression을 복제하지 않는다.
- QA Evidence Studio와 Asset Vault처럼 시각 collaboration surface와 독립적인 검증/파일 생명주기 도구는 이 변경으로 폐기하지 않는다.

### Validation state

```yaml
notion_project_relation_workspace: READBACK_VERIFIED
notion_image_upload_replace_readback: VERIFIED
human_ai_view_separation: VERIFIED
neutral_visual_continuity_gate: IMPLEMENTED_ON_PR_528
identity_pose_effect_reuse_modules: PRESERVED
product_specific_visual_runtime: DEPRECATED_REMOVED_ON_PR_528
product_asset_promotion: USER_DECISION_REQUIRED
runtime_asset_validation: NOT_RUN
```

---

## Superseded historical visual-surface lessons

2026-08-12와 2026-08-18에 시각 collaboration surface와 localhost visual runtime을 실험하면서 다음 일반 원칙이 검증됐다. 구현 세부와 과거 page/route 이름은 현재 권위가 아니며 Git history에서만 복구한다.

- 승인 visual reference와 WIP candidate를 구분한다.
- 사용자 Decision 없이 `PROJECT_ASSET_APPROVED`로 올리지 않는다.
- 화면 mockup의 `CONFIRMED / DISCOVERED_IDEA / AI_ASSUMPTION / MISSING_CANON / VISUAL_CANONICAL_CONFLICT`를 구분한다.
- `screen_id / flow_id`를 시각 그림과 별도로 유지한다.
- prototype/preview는 runtime proof가 아니다.
- candidate write/upload 뒤 readback을 요구한다.
- 불안정한 execution wrapper는 stop-loss하고 도메인 지식만 generic reference로 보존한다.
- package integrity를 위해 conditional reference는 주 Skill에서 직접 discoverable하되 필요할 때만 load한다.

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
- 기존 Art Guide에 Gate를 흡수하고 Art prompt·Vertical Slice·Art/UX template·이미지 정책이 이를 소비하게 했다.
- 전용 regression test와 기존 visual workflow regression을 함께 사용한다.

### Guardrail

이 학습은 모든 시각물을 삭제하거나 모든 단발 이미지 요청에 문서 작성을 강제하지 않는다. `DECORATIVE`도 core emotion·identity에 관찰 가능한 가치가 있으면 우선순위를 올릴 수 있으며, 프로젝트 외 단발 이미지 요청은 현 작업 범위에서 바로 생성할 수 있다.

### Validation state

```yaml
visual_requirement_contract_test: IMPLEMENTED
existing_visual_workflow_companion_test: IMPLEMENTED
project_pilot: NOT_RUN
human_art_pipeline_validation: HUMAN_NOT_RUN
runtime_asset_validation: NOT_RUN
```

Project pilot과 실제 제작 반복성이 쌓이기 전에는 세부 숫자나 특정 asset 목록을 공용 강제 규칙으로 승격하지 않는다.
