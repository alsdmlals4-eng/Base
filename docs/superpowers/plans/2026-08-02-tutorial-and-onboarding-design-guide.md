# Tutorial and Onboarding Design Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable Base tutorial and onboarding design contract that turns `basic rule → need/deficit → method discovery → felt growth → independent performance → transfer` into a project-first, evidence-backed, adversarially reviewed workflow.

**Architecture:** Keep `analyzing-and-refining-game-concepts` as the single game-design owner and add a conditional `tutorial-and-onboarding-design` mode in its Skill body. Put detailed method and evidence in the game-development knowledge hub, provide a project-facing planning template, and connect human discoverability through `START_HERE` and the hub index. Preserve `skills/SKILL_REGISTRY.json` bytes because it is a protected v9.4 release surface and the existing owner already exposes `game-system-design`, `playtest-design`, `digital-dopamine-design`, and `instant-feedback` trigger coverage.

**Tech Stack:** Markdown contracts, Python 3 `unittest`/`pytest` contract tests, existing Base GitHub Actions validation topology.

## Global Constraints

- Base main baseline is exactly `896d2e6fd257084b6aa29b1703cd0bbfa3b18daa`.
- Preserve existing Skill IDs, `skills/SKILL_REGISTRY.json`, release locks, frozen snapshots, project-specific data, and open PR #134/#136 prompt files.
- Base itself is not a project Google Sheets synchronization target.
- External references are evidence inputs, never project canon or implementation truth.
- No Guide, Template, or Skill integration is written before the focused test has been observed failing for the missing behavior.
- Human playtest, engine runtime, and real-project onboarding validation remain `NOT_RUN` unless actually executed.

---

### Task 1: Add the failing tutorial contract test

**Files:**
- Create: `tests/test_tutorial_and_onboarding_design_contract.py`

**Interfaces:**
- Consumes: repository root paths and the existing Skill Registry.
- Produces: assertions for the Guide, Template, existing Skill ownership, protected Registry preservation, discoverability, evidence, and failure boundaries.

- [ ] **Step 1: Write the failing test**

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md"
TEMPLATE = ROOT / "templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md"
SKILL = ROOT / "skills/analyzing-and-refining-game-concepts/SKILL.md"
START = ROOT / "START_HERE.md"
INDEX = ROOT / "docs/knowledge/game-development/README.md"
REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"


class TutorialAndOnboardingDesignContractTests(unittest.TestCase):
    def test_learning_ladder_and_failure_boundaries_exist(self) -> None:
        guide = GUIDE.read_text(encoding="utf-8")
        for token in ("RULE", "NEED", "DISCOVER", "FEEL", "PROVE", "TRANSFER"):
            self.assertIn(token, guide)
        for phrase in ("강제 패배", "정적 조작표", "가짜 성장", "안내 없는 독립 수행", "다른 상황에서 재사용"):
            self.assertIn(phrase, guide)

    def test_project_first_evidence_and_accessibility_contract(self) -> None:
        combined = GUIDE.read_text(encoding="utf-8") + TEMPLATE.read_text(encoding="utf-8")
        for phrase in ("프로젝트 정본", "실제 코드", "Google Sheets", "벤치마크", "플레이테스트", "텔레메트리", "Skip", "복습", "접근성 대체 채널", "BLOCKED_UNVERIFIED"):
            self.assertIn(phrase, combined)

    def test_existing_skill_owns_tutorial_design_without_new_broad_skill(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("tutorial-and-onboarding-design", skill)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md", skill)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md", skill)
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        skill_ids = {item["skill_id"] for item in registry["skills"]}
        self.assertNotIn("tutorial-and-onboarding-design", skill_ids)
        owner = next(item for item in registry["skills"] if item["skill_id"] == "analyzing-and-refining-game-concepts")
        for existing_trigger in ("game-system-design", "playtest-design", "digital-dopamine-design", "instant-feedback"):
            self.assertIn(existing_trigger, owner["trigger_tags"])

    def test_human_discoverability_routes_to_existing_owner(self) -> None:
        start = START.read_text(encoding="utf-8")
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn("튜토리얼·온보딩·첫 세션 학습", start)
        self.assertIn("analyzing-and-refining-game-concepts", start)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md", index)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m pytest tests/test_tutorial_and_onboarding_design_contract.py -q
```

Expected: `4 failed` because the Guide and Template are absent and the Skill/entrypoint do not yet expose the mode.

- [ ] **Step 3: Commit the RED test**

```bash
git add tests/test_tutorial_and_onboarding_design_contract.py
git commit -m "test: define tutorial onboarding design contract"
```

### Task 2: Add the Guide and project contract

**Files:**
- Create: `docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md`
- Create: `templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md`

**Interfaces:**
- Consumes: project canon, actual implementation, current progress, benchmark evidence, playtest and telemetry evidence.
- Produces: one staged learning ladder, measurement plan, adversarial findings, and `KEEP / CHANGE / REMOVE / TEST / HOLD` decisions.

- [ ] **Step 1: Write the Guide**

The Guide must implement:

```text
PROJECT AUDIT
→ RULE
→ NEED
→ DISCOVER
→ FEEL
→ PROVE
→ TRANSFER
→ PLAYTEST / TELEMETRY
→ ADVERSARIAL REVIEW
→ DECISION
```

It must distinguish interactive learning from static control screens, prohibit forced-loss monetization and fake growth, require guidance fading, replay/skip/returning-player support, and record Apple/Microsoft primary guidance with checked dates and limits.

- [ ] **Step 2: Write the project-facing Template**

The Template must contain exact sections for project audit, learner context, stage table, guidance fading, need/growth causality, before/after comparison, skip/review/returning/accessibility, benchmark evidence, playtest/telemetry, adversarial findings, decisions, unverified work, rollback, and next gate.

- [ ] **Step 3: Run the focused test**

```bash
python -m pytest tests/test_tutorial_and_onboarding_design_contract.py -q
```

Expected: Guide/Template assertions pass; Skill and discovery assertions remain failing.

- [ ] **Step 4: Commit the Guide and Template**

```bash
git add docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md
git commit -m "docs: add tutorial onboarding design guide"
```

### Task 3: Integrate the existing Skill and discovery routes

**Files:**
- Modify: `skills/analyzing-and-refining-game-concepts/SKILL.md`
- Modify: `START_HERE.md`
- Modify: `docs/knowledge/game-development/README.md`
- Preserve: `skills/SKILL_REGISTRY.json`

**Interfaces:**
- Consumes: tutorial design requests plus project-first evidence.
- Produces: one conditional mode and one-step human discovery without a new broad Skill or Registry mutation.

- [ ] **Step 1: Extend the existing Skill**

Add `tutorial-and-onboarding-design` to the mode sequence, required inputs, analysis lens, conditional Guide/Template reference, workflow, output contract, and quality gate. Explicitly separate tutorial design ownership from GUR coverage auditing.

- [ ] **Step 2: Add one-step discovery**

Add this `START_HERE.md` route:

```markdown
| 튜토리얼·온보딩·첫 세션 학습·성장 체감 | `analyzing-and-refining-game-concepts: tutorial-and-onboarding-design` | `skills/analyzing-and-refining-game-concepts/SKILL.md` |
```

Add the Guide and Template to the knowledge hub and state that the hub does not own execution authority.

- [ ] **Step 3: Verify the Registry remains unchanged**

```bash
git diff --exit-code 896d2e6fd257084b6aa29b1703cd0bbfa3b18daa -- skills/SKILL_REGISTRY.json
```

Expected: no diff.

- [ ] **Step 4: Run the focused test and verify GREEN**

```bash
python -m pytest tests/test_tutorial_and_onboarding_design_contract.py -q
```

Expected: `4 passed`.

- [ ] **Step 5: Commit the integration**

```bash
git add skills/analyzing-and-refining-game-concepts/SKILL.md START_HERE.md docs/knowledge/game-development/README.md
git commit -m "feat: route tutorial onboarding design"
```

### Task 4: Validate references, scope, and adversarial boundaries

**Files:**
- Test: `tests/test_tutorial_and_onboarding_design_contract.py`
- Review: all changed files relative to baseline main.

**Interfaces:**
- Consumes: exact changed-file inventory and focused test output.
- Produces: review verdict, evidence limits, and PR-ready state.

- [ ] **Step 1: Run focused validation**

```bash
python -m json.tool skills/SKILL_REGISTRY.json > /dev/null
python -m pytest tests/test_tutorial_and_onboarding_design_contract.py -q
```

Expected: valid protected Registry and `4 passed`.

- [ ] **Step 2: Run related repository tests when present**

```bash
python -m pytest \
  tests/test_evidence_based_game_development_knowledge.py \
  tests/test_evidence_knowledge_workflow_contract.py \
  tests/test_tutorial_and_onboarding_design_contract.py -q
```

If an exact file is absent, record `NOT_PRESENT` rather than inventing a pass.

- [ ] **Step 3: Run full local validation when the complete checkout is available**

```bash
python tools/run_local_validation.py --trusted-history-commit 896d2e6fd257084b6aa29b1703cd0bbfa3b18daa
```

If DNS or repository materialization blocks the checkout, record `BLOCKED_ENVIRONMENT`; do not convert it to a pass.

- [ ] **Step 4: Perform adversarial review**

Attack:

- new broad Skill accidentally introduced
- tutorial research governance confused with tutorial design ownership
- Registry or release lock changed without a release contract
- forced loss or monetization disguised as need creation
- growth feedback that changes only presentation
- static control screens accepted as learning
- missing independent performance or transfer test
- external benchmark treated as canon
- Base incorrectly treated as a project Sheet sync target
- changes to PR #134/#136 prompt files

Fix only validated findings, then rerun focused tests.

- [ ] **Step 5: Verify changed-file inventory**

Allowed files:

```text
docs/superpowers/specs/2026-08-02-tutorial-and-onboarding-design-guide-design.md
docs/superpowers/plans/2026-08-02-tutorial-and-onboarding-design-guide.md
docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md
templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md
tests/test_tutorial_and_onboarding_design_contract.py
skills/analyzing-and-refining-game-concepts/SKILL.md
START_HERE.md
docs/knowledge/game-development/README.md
```

### Task 5: Publish the Draft PR and verify exact HEAD

**Files:**
- No additional files unless review finds a validated defect.

**Interfaces:**
- Consumes: feature branch and exact HEAD.
- Produces: Draft PR with scope, evidence, limitations, rollback, and exact-HEAD check status.

- [ ] **Step 1: Open Draft PR**

Title:

```text
feat: add tutorial and onboarding design guide
```

Body includes the six-stage ladder, existing-Skill ownership, protected Registry decision, changed-file list, RED/GREEN evidence, `NOT_RUN` human/runtime limits, and rollback by reverting the PR.

- [ ] **Step 2: Verify exact PR HEAD**

Confirm base SHA, current head SHA, changed-file scope, unresolved review threads, and adversarial P0/P1 findings before any merge decision.

- [ ] **Step 3: Check GitHub Actions truthfully**

Report each required check as `SUCCESS`, `FAILURE`, `PENDING`, or `NOT_RUN`; workflow-file presence is not an executed pass.
