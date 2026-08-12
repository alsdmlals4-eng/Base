# Figma Visual Bible Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 Base 시각 협업·이미지 생성 체계에 프로젝트별 Figma Visual Bible, 화면 Flow, GPT 해석 기록, 구현 비교를 중복 없이 연결한다.

**Architecture:** `VISUAL_COLLABORATION_TOOL_POLICY`가 권위와 lifecycle을 유지하고, project-local profile template이 Figma 구조를 제공한다. 기존 이미지 생성 Skill과 continuity reference가 승인 Figma reference를 소비하고 생성 뒤 `INTERPRETATION_RECORD / FLOW_MAP / PROTOTYPE_FLOW`를 연결한다. 기존 Visual Artifact Registry와 asset-vault 권위를 그대로 사용하며 runtime 비교는 실제 캡처가 있을 때만 수행한다.

**Tech Stack:** Markdown policy/template, JSON registry contract, Python unittest, GitHub Actions.

## Global Constraints

- Figma는 GitHub/GDD/Decision 정본을 대체하지 않는다.
- 실제 이미지 bytes 권위는 `.asset-vault`/tracked asset 흐름을 유지한다.
- 신규 `figma-*` Skill을 만들지 않는다.
- 기존 lifecycle을 새로 복제하지 않는다.
- Figma 접근 불가 시 내용을 추정하지 않는다.
- `FINAL` Figma page는 제품 자산 승인이나 runtime verification을 자동 의미하지 않는다.
- `DISCOVERED_IDEA / AI_ASSUMPTION`은 사용자 Decision 전 확정 요구가 아니다.
- Prototype은 실제 Godot runtime proof가 아니다.

---

### Task 1: Base 압축 운영 규칙

**Files:**
- Modify: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`

**Produces:** Project Figma Visual Bible + Project Visual Flow Workspace의 authority/page/artifact mapping.

- [x] 기존 policy의 authority boundary를 보존한다.
- [x] `Project Figma Visual Bible`과 `Project Visual Flow Workspace`를 기존 policy에 흡수한다.
- [x] `00_DIRECTION / 01_APPROVED_REFERENCE / 02_WIP / 03_REJECTED / 04_FINAL` mapping을 명시한다.
- [x] `FLOW_MAP / PROTOTYPE_FLOW / INTERPRETATION_RECORD / RUNTIME_CAPTURE / COMPARE_BOARD` 경계를 명시한다.
- [x] Figma가 제품 asset bytes나 runtime proof가 아님을 명시한다.

### Task 2: 프로젝트 로컬 적용판 + 실제 구조 예시

**Files:**
- Create: `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`
- Modify: `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`

**Produces:** 각 프로젝트가 복제·최적화할 수 있는 Figma profile과 page/frame/Flow/interpretation naming 예시.

- [x] project identity/Figma link/Decision boundary fields를 제공한다.
- [x] 5개 기본 page와 선택 page를 제공한다.
- [x] `00.8_VISUAL_FLOW_HUB`, `02.5_FLOW_PROTOTYPE`, `02.6_GPT_INTERPRETATION`, `04.2_IMPLEMENTATION_COMPARE` 예시를 제공한다.
- [x] `CHAR_ / UI_ / FLOW_ / INT_ / CMP_` 등 stable ID 예시를 제공한다.
- [x] Approved/WIP/GPT interpretation/Flow/runtime compare 카드를 제공한다.
- [x] Registry에서 `screen_id / flow_id / interpretation_status / runtime_compare_status`를 추적한다.
- [x] 새 profile은 policy와 Art Skill에서 직접 링크해 한 단계 발견 가능하게 한다.

### Task 3: 이미지 생성 내부 작업 절차 연결

**Files:**
- Modify: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- Create/Modify: `skills/designing-art-prompts-and-technique-cards/references/figma-visual-bible-continuity-gate.md`
- Modify: `skills/designing-art-prompts-and-technique-cards/LEARNING_LOG.md`
- Modify: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`

**Produces:** 승인 Figma reference 확인 → WIP → GPT 해석 기록 → Flow 갱신 → 승인 → runtime compare의 continuity gate.

- [x] Required inputs에 Figma Visual Bible/approved reference를 선택 입력으로 추가한다.
- [x] Process에 Figma continuity gate를 추가한다.
- [x] `CONFIRMED / DISCOVERED_IDEA / AI_ASSUMPTION` 해석 분류를 추가한다.
- [x] 생성/검수 plan에 `screen_id / flow_id`, Figma interpretation, runtime compare fields를 추가한다.
- [x] 화면 연결 시 `FLOW_MAP`을 갱신하고 필요할 때만 `PROTOTYPE_FLOW`를 추가한다.
- [x] 실제 `RUNTIME_CAPTURE`가 있을 때만 `COMPARE_BOARD`와 drift classification을 사용한다.
- [x] approval sync에 Figma/Visual Artifact Registry 갱신 체크를 추가한다.

### Task 4: 회귀 계약과 CI

**Files:**
- Modify: `tests/test_bca_visual_sheet_workflow.py`
- Modify: `tests/test_visual_collaboration_capability_contract.py`
- Modify: `.github/workflows/validate-bca-visual-sheet-workflow.yml`

**Produces:** Visual Bible + Visual Flow + interpretation contract가 삭제·분리되지 않도록 자동 검증.

- [x] policy에 Visual Bible/Flow/artifact/authority tokens가 있는지 검사한다.
- [x] project profile template의 page/naming/interpretation/runtime compare tokens를 검사한다.
- [x] art skill과 image review plan의 Figma continuity tokens를 검사한다.
- [x] Registry의 Flow/interpretation/runtime fields를 검사한다.
- [x] CI path filter와 unittest 실행에 새 template/test를 포함한다.

### Task 5: 적대적 재검토 및 PR 검증

**Files:**
- Review all changed files.

**Produces:** scope 충돌·중복 lifecycle·중복 PR 정리와 exact-head CI 결과.

- [x] 신규 canon/lifecycle/Skill 중복이 없는지 재검사한다.
- [x] Figma `FINAL`과 `PROJECT_ASSET_APPROVED`가 분리돼 있는지 검사한다.
- [x] Figma 접근 실패 fallback이 있는지 검사한다.
- [x] 동일 Goal의 병렬 PR을 발견하고 한 PR로 흡수하기로 판정한다.
- [x] feature branch 전체 diff를 검토한다.
- [ ] latest exact-head GitHub Actions가 모두 통과하는지 확인한다.
- [ ] 중복 PR을 닫고 최종 PR을 ready-for-review로 전환한다.
