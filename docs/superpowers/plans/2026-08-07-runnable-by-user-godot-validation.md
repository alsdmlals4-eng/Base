# RUNNABLE_BY_USER Godot Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Godot 구현 작업에서 사용자가 실제 `F5 / Run Project` 진입 경로로 기능을 직접 검증할 수 있어야 하는 경우, 필요한 최소 `project.godot`/Main Scene 통합까지 승인 범위에 포함하고 증거·rollback·회귀 검증을 요구한다.

**Architecture:** 새 광역 Skill을 만들지 않는다. 기존 프로젝트 템플릿 Skill `godot-live-editor-operations`가 실행 권위를 유지하고, 세부 A/B 판단과 `RUNNABLE_BY_USER` 완료 조건은 같은 Skill의 focused reference로 분리한다. 기존 `L2_DESTRUCTIVE_OR_STRUCTURAL_WRITE` Gate를 재사용하여 `project.godot`·Main Scene 변경을 통제한다.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions, Godot 4.x project settings semantics.

## Global Constraints

- HiGodot은 Godot 저작·편집의 단일 실행 권위다.
- 사용자 실검증에 필요한 최소 통합 변경만 허용하며 무관한 Project Settings 정리는 금지한다.
- `project.godot`·Main Scene·Autoload·InputMap 변경은 기존 L2/L3 Gate와 rollback 규칙을 우회하지 않는다.
- 실제 Godot runtime 또는 사람 검증을 실행하지 않았으면 `PASS`로 승격하지 않는다.
- 기존 Prototype/Test Scene의 격리 목적 또는 사용자의 명시적 진입점 보존 지시는 우선한다.

---

### Task 1: Contract test

**Files:**
- Create: `tests/test_runnable_by_user_godot_validation.py`

**Interfaces:**
- Consumes: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Produces: 문서 계약의 필수 토큰과 reference 연결을 검증하는 회귀 테스트

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the focused test and verify it fails because `RUNNABLE_BY_USER` contract is absent**
- [ ] **Step 3: Keep the failing evidence before implementation**

### Task 2: Focused entrypoint reference and routing

**Files:**
- Create: `templates/project-operations/.agents/skills/godot-live-editor-operations/references/runnable-by-user-project-entrypoint.md`
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`

**Interfaces:**
- Consumes: existing L2/L3 write gates, `reviewing-and-validating-project-changes`
- Produces: `RUNNABLE_BY_USER` A/B decision rule, F5 acceptance criteria, rollback and reporting semantics

- [ ] **Step 1: Add the focused reference with A/B decision table and exceptions**
- [ ] **Step 2: Route from the live-editor Skill only when user-runnable validation is part of the approved goal**
- [ ] **Step 3: Require `F5 / Run Project`, expected Main Scene, full user flow, diff, parse/import/test, regression, and rollback evidence**
- [ ] **Step 4: Keep human validation separate from `USER_RUNNABLE_READY`**

### Task 3: Verify and adversarially review

**Files:**
- Test: `tests/test_runnable_by_user_godot_validation.py`
- Review: changed Skill/reference/plan

**Interfaces:**
- Consumes: Task 1-2 output
- Produces: regression evidence and PR-ready decision report

- [ ] **Step 1: Run the focused test and verify green**
- [ ] **Step 2: Run applicable Base validation in CI**
- [ ] **Step 3: Attack over-broad scope, unsafe `project.godot` mutation, false human-validation claims, and Prototype/Test Scene regressions**
- [ ] **Step 4: Recheck the exact PR diff and unresolved review threads**
