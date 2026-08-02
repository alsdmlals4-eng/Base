# Tutorial and Onboarding Design Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable Base tutorial and onboarding design contract that turns `basic rule → need/deficit → method discovery → felt growth → independent performance → transfer` into a project-first, evidence-backed, adversarially reviewed workflow.

**Architecture:** Keep `analyzing-and-refining-game-concepts` as the single game-design owner and add a conditional `tutorial-and-onboarding-design` mode. Put detailed method and evidence in the game-development knowledge hub, provide a project-facing planning template, and connect discoverability through `START_HERE`, the knowledge hub index, Skill Registry triggers, and focused regression tests. Do not add a new broad Skill or change release locks.

**Tech Stack:** Markdown contracts, minified JSON registries, Python 3 `unittest`/`pytest` contract tests, GitHub Actions via existing Base validation topology.

## Global Constraints

- Base main baseline is exactly `896d2e6fd257084b6aa29b1703cd0bbfa3b18daa`.
- Preserve existing Skill IDs, release locks, frozen snapshots, project-specific data, and open PR #134/#136 prompt files.
- Base itself is not a project Google Sheets synchronization target.
- External references are evidence inputs, never project canon or implementation truth.
- No production contract file is written before the focused test has been observed failing for the missing behavior.
- Human playtest, engine runtime, and real-project onboarding validation remain `NOT_RUN` unless actually executed.

---

### Task 1: Add the failing tutorial contract test

**Files:**
- Create: `tests/test_tutorial_and_onboarding_design_contract.py`

**Interfaces:**
- Consumes: repository root paths and existing `skills/SKILL_REGISTRY.json` schema.
- Produces: focused assertions for the Guide, Template, Skill mode, routing, evidence, and failure boundaries.

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
        for phrase in (
            "강제 패배",
            "정적 조작표",
            "가짜 성장",
            "안내 없는 독립 수행",
            "다른 상황에서 재사용",
        ):
            self.assertIn(phrase, guide)

    def test_project_first_evidence_and_accessibility_contract(self) -> None:
        combined = GUIDE.read_text(encoding="utf-8") + TEMPLATE.read_text(encoding="utf-8")
        for phrase in (
            "프로젝트 정본",
            "실제 코드",
            "Google Sheets",
            "벤치마크",
            "플레이테스트",
            "텔레메트리",
            "Skip",
            "복습",
            "접근성 대체 채널",
            "BLOCKED_UNVERIFIED",
        ):
            self.assertIn(phrase, combined)

    def test_existing_skill_owns_tutorial_design(self) -> None:
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("tutorial-and-onboarding-design", skill)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md", skill)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md", skill)
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        owner = next(item for item in registry["skills"] if item["skill_id"] == "analyzing-and-refining-game-concepts")
        for trigger in ("tutorial-design", "game-onboarding", "first-session-learning"):
            self.assertIn(trigger, owner["trigger_tags"])

    def test_human_discoverability_routes_to_existing_owner(self) -> None:
        start = START.read_text(encoding="utf-8")
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn("튜토리얼·온보딩·첫 세션 학습", start)
        self.assertIn("analyzing-and-refining-game-concepts", start)
        self.assertIn("TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md", index)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m pytest tests/test_tutorial_and_onboarding_design_contract.py -q
```

Expected: FAIL because the Guide and Template do not exist and the existing Skill/Registry do not expose the tutorial mode and triggers.

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

- [ ] **Step 1: Write the Guide with the approved six-stage ladder**

The Guide must contain:

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

It must distinguish interactive learning from static control screens, prohibit forced-loss monetization and fake growth, require guidance fading, replay/skip/returning-player support, and cite Apple and Microsoft primary guidance with checked dates.

- [ ] **Step 2: Write the project-facing template**

The template must include exact fillable sections for:

```markdown
## 1. 프로젝트·첫 세션 현황 감사
## 2. 학습 대상·선수 지식·핵심 규칙
## 3. RULE–NEED–DISCOVER–FEEL–PROVE–TRANSFER 단계표
## 4. 안내 감소·실패·복구·재시도
## 5. 성장 전후 비교
## 6. Skip·복습·복귀·접근성
## 7. 벤치마크 Evidence
## 8. 플레이테스트·텔레메트리
## 9. 적대적 Finding
## 10. 결정·미검증·롤백·다음 Gate
```

- [ ] **Step 3: Run the focused test**

Run:

```bash
python -m pytest tests/test_tutorial_and_onboarding_design_contract.py -q
```

Expected: still FAIL only on missing Skill, Registry, and discovery routing.

- [ ] **Step 4: Commit the Guide and Template**

```bash
git add docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md
git commit -m "docs: add tutorial onboarding design guide"
```

### Task 3: Integrate the existing Skill and discovery routes

**Files:**
- Modify: `skills/analyzing-and-refining-game-concepts/SKILL.md`
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `START_HERE.md`
- Modify: `docs/knowledge/game-development/README.md`

**Interfaces:**
- Consumes: tutorial design requests and project-first evidence.
- Produces: automatic and human-readable routing to the existing game-design owner.

- [ ] **Step 1: Extend the existing Skill**

Add `tutorial-and-onboarding-design` to the mode sequence and add a conditional reference paragraph that routes to the new Guide and Template. The Skill workflow must require project audit before tutorial content, and its quality gate must mention forced loss, fake deficit, fake growth, static control screens, and ungated complexity.

- [ ] **Step 2: Add Registry trigger coverage**

For `analyzing-and-refining-game-concepts`, add these exact tags:

```json
["tutorial-design", "game-onboarding", "first-session-learning", "guidance-fading", "growth-comprehension"]
```

Add these review triggers:

```json
["forced-loss-tutorial", "fake-deficit", "fake-growth-feedback", "static-controls-mistaken-for-tutorial", "independent-performance-missing", "transfer-test-missing"]
```

Do not add a new Skill entry or alter unrelated entries.

- [ ] **Step 3: Add one-step human discovery**

Add a `START_HERE.md` route:

```markdown
| 튜토리얼·온보딩·첫 세션 학습·성장 체감 | `analyzing-and-refining-game-concepts: tutorial-and-onboarding-design` | `skills/analyzing-and-refining-game-concepts/SKILL.md` |
```

Add the Guide to the game-development knowledge hub table and state that it does not own execution authority.

- [ ] **Step 4: Run the focused test and verify GREEN**

Run:

```bash
python -m pytest tests/test_tutorial_and_onboarding_design_contract.py -q
```

Expected: `4 passed`.

- [ ] **Step 5: Commit the routing integration**

```bash
git add skills/analyzing-and-refining-game-concepts/SKILL.md skills/SKILL_REGISTRY.json START_HERE.md docs/knowledge/game-development/README.md
git commit -m "feat: route tutorial onboarding design"
```

### Task 4: Validate references, scope, and adversarial boundaries

**Files:**
- Test: `tests/test_tutorial_and_onboarding_design_contract.py`
- Review: all changed files relative to `896d2e6fd257084b6aa29b1703cd0bbfa3b18daa`

**Interfaces:**
- Consumes: exact changed-file inventory and focused test output.
- Produces: review verdict, evidence limits, and PR-ready state.

- [ ] **Step 1: Run syntax and focused contract validation**

```bash
python -m json.tool skills/SKILL_REGISTRY.json > /dev/null
python -m pytest tests/test_tutorial_and_onboarding_design_contract.py -q
```

Expected: valid JSON and `4 passed`.

- [ ] **Step 2: Run existing related knowledge and operating tests when present**

```bash
python -m pytest \
  tests/test_evidence_based_game_development_knowledge.py \
  tests/test_evidence_knowledge_workflow_contract.py \
  tests/test_skill_registry.py \
  tests/test_tutorial_and_onboarding_design_contract.py -q
```

If an exact named legacy test is absent, record `NOT_PRESENT` rather than inventing a pass.

- [ ] **Step 3: Run repository validation if the full checkout and dependencies are available**

```bash
python tools/run_local_validation.py --trusted-history-commit 896d2e6fd257084b6aa29b1703cd0bbfa3b18daa
```

If DNS or repository materialization prevents a full checkout, record `BLOCKED_ENVIRONMENT` and rely only on actually executed focused tests plus GitHub Actions.

- [ ] **Step 4: Perform adversarial review**

Check for:

- a new broad Skill accidentally introduced
- tutorial research governance confused with tutorial design ownership
- forced loss or monetization disguised as need creation
- growth feedback that changes only presentation
- static control screens accepted as learning
- missing independent performance or transfer test
- external benchmark treated as canon
- Base incorrectly treated as a project Sheet sync target
- changes to release locks, snapshots, or PR #134/#136 files

Classify findings and fix only validated `MUST_FIX` / `SHOULD_FIX` items, then rerun focused tests.

- [ ] **Step 5: Verify changed-file inventory and commit final corrections**

Expected allowed files:

```text
docs/superpowers/specs/2026-08-02-tutorial-and-onboarding-design-guide-design.md
docs/superpowers/plans/2026-08-02-tutorial-and-onboarding-design-guide.md
docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md
templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md
tests/test_tutorial_and_onboarding_design_contract.py
skills/analyzing-and-refining-game-concepts/SKILL.md
skills/SKILL_REGISTRY.json
START_HERE.md
docs/knowledge/game-development/README.md
```

```bash
git diff --name-only 896d2e6fd257084b6aa29b1703cd0bbfa3b18daa...HEAD
git status --short
git commit -am "test: validate tutorial onboarding contracts"
```

### Task 5: Publish the Draft PR and verify exact HEAD

**Files:**
- No additional repository files unless review finds a validated issue.

**Interfaces:**
- Consumes: pushed feature branch and exact HEAD.
- Produces: Draft PR with scope, evidence, limitations, rollback, and exact-HEAD check status.

- [ ] **Step 1: Push branch and open Draft PR**

PR title:

```text
feat: add tutorial and onboarding design guide
```

PR body must include the six-stage ladder, existing-Skill ownership, changed-file list, RED/GREEN evidence, `NOT_RUN` human/runtime limits, and rollback by reverting the PR.

- [ ] **Step 2: Verify exact PR HEAD**

Confirm:

```text
base SHA = 896d2e6fd257084b6aa29b1703cd0bbfa3b18daa
head SHA = current branch HEAD
unresolved review threads = 0 before merge decision
P0/P1 adversarial findings = 0 before merge decision
```

- [ ] **Step 3: Check GitHub Actions without overstating status**

Report each required check as `SUCCESS`, `FAILURE`, `PENDING`, or `NOT_RUN`. Do not claim workflow-file presence as an executed pass.
