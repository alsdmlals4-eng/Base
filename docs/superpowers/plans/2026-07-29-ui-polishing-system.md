# UI Polishing System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the existing shared game UX/UI skill with an evidence-based UI polishing pass while repairing stale machine routing and coupled-change coverage.

**Architecture:** Keep `auditing-and-refining-ui-art` as the single canonical UX/UI skill. Add one focused polishing reference and one `polishing-pass` mode, then propagate the contract through the project template, review checklist, registry, routers, learning log, tests, and dedicated CI path filters. Preserve all existing design, A~E runtime audit, approval, accessibility, and domain-state boundaries.

**Tech Stack:** Markdown, JSON, YAML, Python `unittest`, GitHub Actions.

## Global Constraints

- Do not add a new shared Skill ID.
- Do not modify game product code, Godot scenes, game data, or assets.
- Do not hard-code one universal animation duration, scale, spacing, contrast, sound, or haptic value for all projects.
- Do not treat external guidance as project authority or implementation fact.
- Preserve `ADOPT / ADAPT / AVOID / TEST / IGNORE`, the existing 12 UX pattern IDs, A~E runtime audit, user approval before UI edits, and UI/domain-state separation.
- Automated checks do not replace runtime, device, human, or accessibility-user evidence.
- Project-specific values, paths, captures, and results remain in project repositories.

---

### Task 1: Add failing polishing contract tests

**Files:**
- Modify: `tests/test_game_ux_ui_system.py`

**Interfaces:**
- Consumes: current Skill, references, templates, registry, coupled-change config, CI workflow, and router files.
- Produces: failing contract assertions for every new polishing consumer.

- [ ] **Step 1: Add tests for the new reference and Skill mode**

Add assertions that:

```python
REFERENCE_ROOT / "ui-polishing-method.md"
```

exists and `SKILL.md` contains:

```text
`polishing-pass`
P0 BLOCKER
P1 CLARITY
P2 CONSISTENCY
P3 DELIGHT
반복 사용
중단·재진입
```

- [ ] **Step 2: Add tests for Template and Checklist propagation**

Assert `GAME_UX_UI_SYSTEM.md` contains:

```text
폴리싱 준비도
피드백 예산
반복 사용·중단·재진입
전후 Artifact
```

Assert `GAME_UX_UI_REVIEW_CHECKLIST.md` contains:

```text
P0
P1
P2
P3
reduced motion
중복 입력
애니메이션 중단
반복 사용
```

- [ ] **Step 3: Add registry routing assertions**

Parse `skills/SKILL_REGISTRY.json`, find `skill_id == "auditing-and-refining-ui-art"`, and assert trigger tags contain:

```python
{"game-ux", "ui-design", "ui-polishing", "interaction-feedback", "godot-ui", "runtime-ui-audit"}
```

Assert `use_when` mentions design, polishing, and rendered audit rather than audit only.

- [ ] **Step 4: Add coupled-change and CI path assertions**

Parse `.github/reference-freshness.json` and assert `game-ux-ui-skill-sync.require_all_changed` contains:

```python
{
    "skills/SKILL_REGISTRY.json",
    "skills/SKILL_LEARNING_LOG.md",
    "skills/README.md",
    "tests/test_game_ux_ui_system.py",
    ".github/workflows/validate-game-ux-ui-system.yml",
}
```

Assert the dedicated workflow watches `skills/SKILL_REGISTRY.json`, `skills/SKILL_LEARNING_LOG.md`, `AGENTS.md`, `START_HERE.md`, `docs/OPERATING_MODEL.md`, and `docs/DOCUMENTATION_MAP.md`.

- [ ] **Step 5: Add router assertions**

Assert the router files describe the Skill as UX/UI design, polishing, and runtime audit:

```text
AGENTS.md
START_HERE.md
docs/OPERATING_MODEL.md
docs/DOCUMENTATION_MAP.md
skills/README.md
```

- [ ] **Step 6: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests/test_game_ux_ui_system.py -v
```

Expected: failures for missing `ui-polishing-method.md`, `polishing-pass`, Template/Checklist sections, stale Registry routing, coupled-change requirements, and stale router wording.

- [ ] **Step 7: Commit the RED test**

```bash
git add tests/test_game_ux_ui_system.py
git commit -m "test: define UI polishing system contract"
```

---

### Task 2: Implement the polishing method and Skill contract

**Files:**
- Create: `skills/auditing-and-refining-ui-art/references/ui-polishing-method.md`
- Modify: `skills/auditing-and-refining-ui-art/SKILL.md`
- Modify: `skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md`
- Modify: `skills/auditing-and-refining-ui-art/references/ux-ui-reference-library.md`
- Modify: `skills/auditing-and-refining-ui-art/references/godot-ui-implementation-contract.md`
- Modify: `skills/auditing-and-refining-ui-art/agents/openai.yaml`

**Interfaces:**
- Consumes: existing UX patterns, Godot ownership contract, accessibility gate, runtime audit, official reference adoption model.
- Produces: `polishing-pass` workflow and the canonical polishing output fields used by templates and review.

- [ ] **Step 1: Create the polishing reference**

Write `ui-polishing-method.md` with these exact sections:

```text
1. 목적과 비목표
2. 진입 조건과 중단 조건
3. P0 BLOCKER / P1 CLARITY / P2 CONSISTENCY / P3 DELIGHT
4. 폴리싱 패스 순서
5. feedback tier: routine / confirming / warning / reward / critical
6. hierarchy·spacing·typography·numbers·copy
7. state·affordance·focus·error recovery
8. motion·audio·haptics·reduced motion·mute·haptic off
9. rapid repeat·duplicate input·interruption·reentry
10. resolution·localization·fallback·performance
11. before/after evidence and HUMAN_NOT_RUN
12. failure conditions and stop rules
```

Require `REMOVE → REDUCE → MERGE → CLARIFY → FEEDBACK → ADD` before visual ornament.

- [ ] **Step 2: Add `polishing-pass` to the Skill**

Place the mode between design and implementation-result audit. Define it as:

```text
기능·정보 구조·상태 소유권이 충분히 안정된 화면에서 P0→P3 순서로 명확성·일관성·피드백·모션·음향·햅틱·반복 피로·성능을 마감하고 전후 증거를 만든다.
```

Add `ui-polishing-method.md` to progressive-disclosure references and add the polishing output fields to the design output contract.

- [ ] **Step 3: Connect design readiness to polishing**

Update `ux-ui-design-system-method.md` so the lifecycle is:

```text
설계 계약
→ 구현 준비도
→ polishing-pass
→ runtime-ui-audit
→ approved refinement
→ reaudit
```

State that unresolved information architecture, state ownership, or blocked input returns to design instead of receiving decorative polish.

- [ ] **Step 4: Extend official reference decisions**

Add focused official links and Base decisions for:

```text
W3C focus appearance, target size, animation from interactions
Xbox focus, UI context, errors/destructive actions, motion, haptics
Apple feedback, motion, accessibility/reduce motion, haptics, game controls
Godot Theme, Container, GUI navigation
Material interaction states
```

Do not promote exact platform values into universal Base constants.

- [ ] **Step 5: Extend the Godot contract**

Add:

```text
semantic feedback tokens
feedback tier mapping
Tween/AnimationPlayer interruption and reentry behavior
duplicate input policy
reduced-motion alternate path
mute and haptic-off equivalent feedback
repeated-use and frame/memory risk checks
```

Keep animation completion non-authoritative for domain rules.

- [ ] **Step 6: Update the agent interface**

Change the display and default prompt to explicitly include design, polishing, and audit.

- [ ] **Step 7: Run the focused test**

```bash
python -m unittest tests/test_game_ux_ui_system.py -v
```

Expected: Skill/reference assertions pass; Template, Checklist, Registry, coupled-change, CI path, and router assertions still fail.

- [ ] **Step 8: Commit the focused implementation**

```bash
git add skills/auditing-and-refining-ui-art
git commit -m "feat: add evidence-based UI polishing pass"
```

---

### Task 3: Propagate polishing into project templates and quality gates

**Files:**
- Modify: `templates/planning/GAME_UX_UI_SYSTEM.md`
- Modify: `templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md`

**Interfaces:**
- Consumes: polishing output contract from Task 2.
- Produces: project-facing planning fields and review gates.

- [ ] **Step 1: Add the project polishing contract section**

Add a section after feedback/error recovery with:

```text
폴리싱 준비도
P0~P3 finding budget
routine/confirming/warning/reward/critical feedback mapping
motion/audio/haptic budget
reduced-motion/mute/haptic-off fallback
rapid-repeat/duplicate-input/interruption/reentry fixture
before/after Artifact
```

- [ ] **Step 2: Add review gates**

Add checklist items that verify:

```text
P0~P2 are resolved or explicitly blocked before P3 delight work
frequent actions use lower intensity than milestone rewards
motion, audio, and haptics map to the same cause and result
effects can be interrupted or completed instantly without duplicate domain results
repeated use does not create fatigue or input delay
before/after captures use the same build, state, resolution, and input context
```

- [ ] **Step 3: Run the focused test**

```bash
python -m unittest tests/test_game_ux_ui_system.py -v
```

Expected: Template and Checklist assertions pass; Registry, coupled-change, CI path, and router assertions still fail.

- [ ] **Step 4: Commit the propagation**

```bash
git add templates/planning/GAME_UX_UI_SYSTEM.md templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md
git commit -m "docs: add project UI polishing contract and gates"
```

---

### Task 4: Repair machine routing and coupled-change enforcement

**Files:**
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `.github/reference-freshness.json`
- Modify: `.github/workflows/validate-game-ux-ui-system.yml`

**Interfaces:**
- Consumes: `polishing-pass` and new reference from Task 2.
- Produces: correct automatic routing and drift prevention.

- [ ] **Step 1: Update the Registry entry**

For `auditing-and-refining-ui-art`, set trigger tags to include at least:

```json
[
  "game-ux",
  "ui-design",
  "ui-information-architecture",
  "interaction-pattern",
  "ui-polishing",
  "interaction-feedback",
  "microinteraction",
  "motion-feedback",
  "audio-haptic-feedback",
  "godot-ui",
  "web-ui",
  "runtime-ui-audit",
  "visual-refinement",
  "render-review"
]
```

Update `use_when` to cover planning, polishing, and rendered audit. Update review triggers with:

```text
폴리싱으로 구조 결함 은폐
효과 과잉
반복 피로 미검증
중단·재진입 중복 결과
Registry drift
```

Set `last_reviewed_at` to `2026-07-29` and leave the commit reference traceable to the implementation PR until merged.

- [ ] **Step 2: Record the reusable learning**

Prepend a Learning Log entry documenting:

```text
new Skill rejected as duplicate
existing Skill extended with polishing-pass
PR #57 Registry drift discovered
coupled-change rule repaired
project values and runtime results remain project-specific
knowledge state PATTERN candidate, cross-project effectiveness OBSERVATION
```

- [ ] **Step 3: Strengthen the coupled-change rule**

Update `game-ux-ui-skill-sync.require_all_changed` to require:

```json
[
  "skills/SKILL_REGISTRY.json",
  "skills/SKILL_LEARNING_LOG.md",
  "skills/README.md",
  "tests/test_game_ux_ui_system.py",
  ".github/workflows/validate-game-ux-ui-system.yml"
]
```

Keep one of agent/reference files as the content-specific change requirement.

- [ ] **Step 4: Extend dedicated CI path filters**

Add to pull request and main push paths:

```text
skills/SKILL_REGISTRY.json
skills/SKILL_LEARNING_LOG.md
AGENTS.md
START_HERE.md
docs/OPERATING_MODEL.md
docs/DOCUMENTATION_MAP.md
```

- [ ] **Step 5: Run the focused test**

```bash
python -m unittest tests/test_game_ux_ui_system.py -v
```

Expected: Registry, coupled-change, and CI path assertions pass; router wording assertions still fail.

- [ ] **Step 6: Commit the routing repair**

```bash
git add skills/SKILL_REGISTRY.json skills/SKILL_LEARNING_LOG.md .github/reference-freshness.json .github/workflows/validate-game-ux-ui-system.yml
git commit -m "fix: synchronize UX UI routing and change coupling"
```

---

### Task 5: Update top-level discovery routes

**Files:**
- Modify: `skills/README.md`
- Modify: `AGENTS.md`
- Modify: `START_HERE.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: machine routing from Task 4.
- Produces: one-step human discovery of design, polishing, and audit.

- [ ] **Step 1: Replace audit-only descriptions**

Use the shared wording:

```text
게임 UX/UI 경험·흐름·정보 구조·패턴·상태·접근성·Godot 계약을 설계하고, 준비된 UI를 증거 기반으로 폴리싱하며, 구현 결과를 실제 렌더·입력·폴백으로 감사·재검수한다.
```

Keep the concise version where table width requires it.

- [ ] **Step 2: Add the reference/template discovery row**

In `docs/DOCUMENTATION_MAP.md`, add a detailed reference row:

```text
UI 폴리싱을 어떤 순서와 증거로 진행하는가?
→ ui-polishing-method.md
→ GAME_UX_UI_SYSTEM.md + GAME_UX_UI_REVIEW_CHECKLIST.md
```

- [ ] **Step 3: Run the focused test**

```bash
python -m unittest tests/test_game_ux_ui_system.py -v
```

Expected: all focused tests pass.

- [ ] **Step 4: Commit the discovery update**

```bash
git add skills/README.md AGENTS.md START_HERE.md docs/OPERATING_MODEL.md docs/DOCUMENTATION_MAP.md
git commit -m "docs: route UI design polishing and audit"
```

---

### Task 6: Run regression, reference freshness, and adversarial review

**Files:**
- Review: all changed files
- Update only if a verified defect is found.

**Interfaces:**
- Consumes: all previous tasks.
- Produces: final evidence report and a reviewable Draft PR.

- [ ] **Step 1: Run focused regressions**

```bash
python -m unittest \
  tests/test_game_ux_ui_system.py \
  tests/test_ui_art_audit.py \
  -v
```

Expected: PASS.

- [ ] **Step 2: Run reference freshness**

```bash
python tools/check_canonical_reference_freshness.py --root .
```

Expected: PASS with no missing coupled consumers.

- [ ] **Step 3: Run broader structure tests affected by Registry/router changes**

```bash
python -m unittest \
  tests/test_game_project_operating_system_structure.py \
  tests/test_consolidated_skill_references.py \
  tests/test_reference_freshness.py \
  tests/test_skill_system_coverage.py \
  -v
```

Expected: PASS.

- [ ] **Step 4: Check formatting and scope**

```bash
git diff --check
git diff --name-only main...HEAD
```

Expected: no whitespace errors; no game product code, Scene, data, image, or asset files.

- [ ] **Step 5: Perform adversarial review**

Attack these risks:

```text
new Skill duplication
polish hiding unresolved IA or domain ownership
universal magic-number timing rules
motion/audio/haptics as sole channels
animation completion becoming domain authority
repeated-use fatigue missing
human evidence overclaim
Registry/router drift
project-specific values leaking into Base
```

Classify findings as `MUST_FIX`, `SHOULD_FIX`, `WAIVED`, `REJECTED_CRITIQUE`, or `USER_DECISION_REQUIRED`.

- [ ] **Step 6: Re-run tests after verified fixes**

Run the commands from Steps 1–4 again. Expected: PASS.

- [ ] **Step 7: Open a Draft PR**

PR title:

```text
UX/UI 폴리싱 패스와 라우팅 동기화 추가
```

PR body must include:

```text
목표
현행 구조 분석
외부 근거와 채택 판정
변경 파일과 책임
Registry/coupled-rule drift repair
검증 evidence
HUMAN_NOT_RUN and project runtime NOT_RUN
project propagation notes
```

Do not merge automatically. Base main and the target project adapters are separate gates.
