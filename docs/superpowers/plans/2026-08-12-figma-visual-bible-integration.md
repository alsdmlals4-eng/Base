# Figma Visual Bible Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 Base 시각 협업·이미지 생성 체계에 프로젝트별 Figma Visual Bible 운영을 중복 없이 연결한다.

**Architecture:** `VISUAL_COLLABORATION_TOOL_POLICY`가 권위와 lifecycle을 유지하고, 새 project-local profile template이 Figma 구조를 제공한다. 기존 이미지 생성 Skill과 생성/검수 plan이 승인 Figma reference를 소비하며, 기존 Visual Artifact Registry와 asset-vault 권위를 그대로 사용한다.

**Tech Stack:** Markdown policy/template, JSON registry contract, Python unittest, GitHub Actions.

## Global Constraints

- Figma는 GitHub/GDD/Decision 정본을 대체하지 않는다.
- 실제 이미지 bytes 권위는 `.asset-vault`/tracked asset 흐름을 유지한다.
- 신규 `figma-*` Skill을 만들지 않는다.
- 기존 lifecycle을 확장하지 않고 Figma page mapping만 추가한다.
- Figma 접근 불가 시 내용을 추정하지 않는다.
- `FINAL` Figma page는 제품 자산 승인이나 runtime verification을 자동 의미하지 않는다.

---

### Task 1: Base 압축 운영 규칙

**Files:**
- Modify: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`

**Produces:** Project Figma Visual Bible의 최소 운영 규칙과 authority/page mapping.

- [ ] 기존 policy의 authority boundary를 보존한다.
- [ ] `Project Figma Visual Bible` 섹션을 추가한다.
- [ ] `00_DIRECTION / 01_APPROVED_REFERENCE / 02_WIP / 03_REJECTED / 04_FINAL` mapping을 명시한다.
- [ ] Figma가 제품 asset bytes나 runtime proof가 아님을 명시한다.

### Task 2: 프로젝트 로컬 적용판 + 실제 구조 예시

**Files:**
- Create: `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Produces:** 각 프로젝트가 복제·최적화할 수 있는 Figma profile과 page/frame naming 예시.

- [ ] project identity/Figma link/Decision boundary fields를 제공한다.
- [ ] 5개 기본 page와 선택 page를 제공한다.
- [ ] `CHAR_ / UNIT_ / ENV_ / UI_ / ICON_ / VFX_ / MKT_` frame ID 예시를 제공한다.
- [ ] `Keep / Avoid / Notes` 카드와 WIP→approval 흐름을 제공한다.
- [ ] DOCUMENTATION_MAP에서 template을 찾을 수 있게 한다.

### Task 3: 이미지 생성 내부 작업 절차 연결

**Files:**
- Modify: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- Modify: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`

**Produces:** 이미지/시각 자료 생성 전에 승인 Figma reference를 확인하고 생성 후 WIP/approval sync를 수행하는 continuity gate.

- [ ] Required inputs에 Figma Visual Bible/approved reference를 선택 입력으로 추가한다.
- [ ] Process에 Figma continuity gate를 추가한다.
- [ ] 생성/검수 plan에 Figma status, file URL, approved reference IDs, WIP target fields를 추가한다.
- [ ] approval sync에 Figma/Visual Artifact Registry 갱신 체크를 추가한다.

### Task 4: 회귀 계약과 CI

**Files:**
- Modify: `tests/test_visual_collaboration_capability_contract.py`
- Modify: `.github/workflows/validate-bca-visual-sheet-workflow.yml`

**Produces:** 새 template과 Figma continuity gate가 삭제·분리되지 않도록 하는 자동 검증.

- [ ] policy에 Visual Bible/page mapping이 있는지 검사한다.
- [ ] project profile template의 필수 page/naming/authority tokens를 검사한다.
- [ ] art skill과 image review plan의 Figma continuity tokens를 검사한다.
- [ ] CI path filter와 unittest 실행에 새 template/test를 포함한다.

### Task 5: 적대적 재검토 및 PR 검증

**Files:**
- Review all changed files.

**Produces:** scope 충돌 0, 중복 lifecycle 0, CI 결과.

- [ ] 신규 canon/lifecycle/Skill 중복이 없는지 재검사한다.
- [ ] Figma `FINAL`과 `PROJECT_ASSET_APPROVED`가 분리돼 있는지 검사한다.
- [ ] Figma 접근 실패 fallback이 있는지 검사한다.
- [ ] feature branch diff를 검토한다.
- [ ] PR을 열고 GitHub Actions 결과를 확인한다.
