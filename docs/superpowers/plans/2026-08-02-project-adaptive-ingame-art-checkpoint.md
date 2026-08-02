# Project-Adaptive In-Game Art Checkpoint Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one reusable Base prompt that studies each game project before selecting scenes, requires Grill Me approval before image generation, and delivers only adversarially reviewed in-game image boards to the user.

**Architecture:** Keep the existing `designing-art-prompts-and-technique-cards: intermediate-visual-checkpoint` owner and add a focused prompt template rather than a new Skill. A dedicated contract test reads the prompt as a public interface and checks the project-first, PR-check, scene-approval, evidence-state, two-board, adversarial-review, and image-only output gates.

**Tech Stack:** Markdown prompt contract, Python `unittest`, GitHub branch/PR workflow.

## Global Constraints

- Base main baseline: `896d2e6fd257084b6aa29b1703cd0bbfa3b18daa`.
- Do not change `skills/SKILL_REGISTRY.json` or add a broad Skill.
- Route through `designing-art-prompts-and-technique-cards: intermediate-visual-checkpoint`.
- Image generation is prohibited before user approval of the scene set through Grill Me.
- Inspect target-project canon, actual files, assets, open PRs, and recent merged PRs before scene selection.
- Do not force one universal screen set on every project.
- Treat generated images as `DRAFT_VISUAL`, not runtime or final-asset evidence.
- Default to two boards when scene density would make a single board unreadable; the project and user approval may override this.
- Final default user-facing delivery is the reviewed image board only; internal analysis remains available on request.

---

### Task 1: Add the prompt contract regression

**Files:**
- Create: `tests/test_project_adaptive_ingame_art_prompt.py`

**Interfaces:**
- Consumes: repository root resolved from `Path(__file__).resolve().parents[1]`.
- Produces: contract assertions for `templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md`.

- [ ] **Step 1: Write the failing test**

Create a `unittest.TestCase` that reads the prompt and asserts the following public contract tokens and Korean behavior statements:

```python
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md"


class ProjectAdaptiveInGameArtPromptTests(unittest.TestCase):
    def test_prompt_requires_project_first_scene_approval_and_review(self) -> None:
        text = PROMPT.read_text(encoding="utf-8")
        for token in (
            "PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT",
            "PROJECT_FIRST",
            "PR_CHECK_REQUIRED",
            "SCENE_SET_APPROVAL_REQUIRED",
            "GRILL_ME_REQUIRED",
            "IMAGE_GENERATION_PROHIBITED_BEFORE_APPROVAL",
            "FINAL_USER_OUTPUT_IMAGE_ONLY",
        ):
            self.assertIn(token, text)
        self.assertIn("모든 프로젝트에 고정 화면 세트를 강제하지 않는다", text)
        self.assertIn("열린 PR", text)
        self.assertIn("최근 병합 PR", text)

    def test_prompt_preserves_evidence_and_adversarial_gates(self) -> None:
        text = PROMPT.read_text(encoding="utf-8")
        for token in (
            "CURRENT",
            "INFERRED",
            "PROPOSED",
            "PLACEHOLDER",
            "MISSING_CANON",
            "CANON_CONFLICT",
            "VISUAL_CANONICAL_CONFLICT",
            "DRAFT_VISUAL",
            "attack",
            "validate-critique",
            "decision-report",
            "regression-recheck",
        ):
            self.assertIn(token, text)

    def test_prompt_supports_individual_scenes_and_readable_boards(self) -> None:
        text = PROMPT.read_text(encoding="utf-8")
        self.assertIn("개별 장면", text)
        self.assertIn("TWO_BOARD_DEFAULT_WHEN_DENSITY_RISK", text)
        self.assertIn("합", text)
        self.assertIn("절초", text)
        self.assertIn("사용자가 검토 기록을 요청", text)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_project_adaptive_ingame_art_prompt -v
```

Expected: `ERROR` or `FAIL` because `templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md` does not exist yet.

- [ ] **Step 3: Commit the failing contract**

```bash
git add tests/test_project_adaptive_ingame_art_prompt.py
git commit -m "test: define project-adaptive art prompt contract"
```

### Task 2: Implement the reusable prompt

**Files:**
- Create: `templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md`

**Interfaces:**
- Consumes: Base and target-project repository URLs, latest user instruction, project canon and actual implementation evidence.
- Produces: approved scene set, Screen Briefs, individual `DRAFT_VISUAL` images, one or more reviewed image boards, and internal review evidence.

- [ ] **Step 1: Add the prompt header and operating contract**

Create the prompt with exact contract identifiers:

```yaml
prompt_id: PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT
execution_profile: PROJECT_FIRST
pr_check: PR_CHECK_REQUIRED
scene_gate: SCENE_SET_APPROVAL_REQUIRED
interview_gate: GRILL_ME_REQUIRED
preapproval_image_generation: IMAGE_GENERATION_PROHIBITED_BEFORE_APPROVAL
board_policy: TWO_BOARD_DEFAULT_WHEN_DENSITY_RISK
user_delivery: FINAL_USER_OUTPUT_IMAGE_ONLY
```

- [ ] **Step 2: Add the project-understanding gate**

Require Base routing, project `AGENTS.md`/start/current context/document map, current Decisions, actual code/data/scenes/resources/assets/tests, open and recent merged PRs, approved images, current UI, and stale/superseded designs. Fail closed with `MISSING_CANON`, `CANON_CONFLICT`, or `BLOCKED_UNVERIFIED`.

- [ ] **Step 3: Add adaptive scene selection and Grill Me approval**

Require a candidate list scored by core-experience fidelity, project specificity, visual value, evidence, user-flow coverage, duplication, and board readability. Present `필수 / 확장 / 통합 가능 / 제외` categories and ask one decision-focused Grill Me question. Prohibit image generation until explicit approval.

- [ ] **Step 4: Add Screen Brief and image-production contracts**

For every approved scene, require purpose, first attention, primary action, information hierarchy, platform/aspect/input, risk/cost/reward, success/failure/recovery, previous/next screen, visual anchors, and evidence state. Generate scenes individually before montage composition and lock shared cast, backgrounds, UI language, camera, color, material, lighting, and era.

- [ ] **Step 5: Add board composition and output rules**

Default to two boards when seven or more scenes or readability risk exists. Use `Board A: entry/preparation/journey` and `Board B: core play/decisive spectacle/review/result` only as an adaptable starting point. Ensure the final response prioritizes images without process diagrams or long explanatory text.

- [ ] **Step 6: Add evidence and adversarial review**

Include `CURRENT / INFERRED / PROPOSED / PLACEHOLDER`, `DRAFT_VISUAL`, `VISUAL_CANONICAL_CONFLICT`, and the full `attack → validate-critique → decision-report → refine → regression-recheck` loop. Explicitly test generic-RPG drift, unsupported implementation claims, superseded concepts, camera/input/UI distortion, cross-scene inconsistency, omitted project-specific decisive moments, and unreadable montage density.

- [ ] **Step 7: Run the focused test and verify GREEN**

Run:

```bash
python -m unittest tests.test_project_adaptive_ingame_art_prompt -v
```

Expected: `3 tests`, all `OK`.

- [ ] **Step 8: Commit the prompt**

```bash
git add templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md
git commit -m "feat: add project-adaptive in-game art checkpoint prompt"
```

### Task 3: Run Base regressions and adversarial review

**Files:**
- Verify: `templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md`
- Verify: `tests/test_project_adaptive_ingame_art_prompt.py`
- Verify: repository-wide validation outputs

**Interfaces:**
- Consumes: Task 1 contract and Task 2 implementation.
- Produces: fresh validation evidence and classified review findings.

- [ ] **Step 1: Run the focused test**

```bash
python -m unittest tests.test_project_adaptive_ingame_art_prompt -v
```

Expected: all three tests pass.

- [ ] **Step 2: Run the existing visual workflow regression**

```bash
python -m unittest tests.test_bca_visual_sheet_workflow -v
```

Expected: all tests pass without changing existing Skill or Registry behavior.

- [ ] **Step 3: Run canonical-reference freshness**

```bash
python tools/check_canonical_reference_freshness.py
```

Expected: exit code `0`.

- [ ] **Step 4: Run Base local validation**

```bash
python tools/run_local_validation.py --base-remote-url https://github.com/alsdmlals4-eng/Base.git --base-trusted-ref 896d2e6fd257084b6aa29b1703cd0bbfa3b18daa
```

Expected: all applicable checks pass; unavailable external runtimes remain explicitly `NOT_RUN` rather than inferred.

- [ ] **Step 5: Perform adversarial review**

Classify findings using:

```text
MUST_FIX
SHOULD_FIX
USER_DECISION_REQUIRED
DEFER
REJECTED_CRITIQUE
BLOCKED_UNVERIFIED
```

Attack the prompt for fixed-screen leakage, generic genre substitution, image generation before approval, missing PR checks, false implementation claims, absent evidence states, omitted decisive effects, and final responses that expose process reports instead of image boards.

- [ ] **Step 6: Commit only validated refinements**

```bash
git add templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md tests/test_project_adaptive_ingame_art_prompt.py
git commit -m "fix: harden project-adaptive art checkpoint gates"
```

Skip this commit when no refinement is required.

### Task 4: Open and review the Draft PR

**Files:**
- Review: all branch changes against `main`

**Interfaces:**
- Consumes: validated branch HEAD.
- Produces: Draft PR with scope, evidence, limitations, and merge gates.

- [ ] **Step 1: Confirm branch scope**

```bash
git diff --name-only 896d2e6fd257084b6aa29b1703cd0bbfa3b18daa...HEAD
```

Expected paths:

```text
docs/superpowers/specs/2026-08-02-project-adaptive-ingame-art-checkpoint-design.md
docs/superpowers/plans/2026-08-02-project-adaptive-ingame-art-checkpoint.md
templates/prompts/PROJECT_ADAPTIVE_INGAME_ART_CHECKPOINT_PROMPT.md
tests/test_project_adaptive_ingame_art_prompt.py
```

- [ ] **Step 2: Open a Draft PR**

Use title:

```text
feat: add project-adaptive in-game art checkpoint prompt
```

The PR body must record the Ten Paces failure that motivated the contract, the project-first and Grill Me gates, two-board density handling, no new Skill/Registry change, test evidence, and any `NOT_RUN` items.

- [ ] **Step 3: Review exact PR HEAD**

Check required workflows, unresolved threads, P0/P1 findings, branch freshness, and the exact changed-file set. Do not claim completion until fresh checks support it.
