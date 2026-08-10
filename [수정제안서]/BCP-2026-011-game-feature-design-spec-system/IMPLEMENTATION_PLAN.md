# Game Feature Design Spec Hierarchy Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Work only on an isolated implementation branch created from the latest `main`. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable L2 `GAME_FEATURE_DESIGN_SPEC` layer that turns PoC-surviving game features into cross-discipline implementation-ready design contracts without creating a new ACTIVE Skill or duplicating the existing Traceability Packet.

**Architecture:** Keep concept validation owned by `analyzing-and-refining-game-concepts`, canonical document authoring owned by `managing-design-documents`, and implementation/verification mapping owned by `FEATURE_SPEC_TRACEABILITY_PACKET`. The new template sits between PoC/recalibration and approved traceability, and is linked through focused edits to the two existing owner Skills plus the existing document-system and traceability templates.

**Tech Stack:** Markdown contracts, Python/pytest repository contract tests, GitHub Actions Base validation.

## Global Constraints

- Add **no new ACTIVE Skill** and do not change `skills/SKILL_REGISTRY.json`.
- Do not create a monolithic MASTER_GDD.
- Do not require L2 detailed specs for L0/L1 or pre-PoC ideas.
- `GAME_FEATURE_DESIGN_SPEC` owns intended feature behavior; it must not own Task progress, implementation-file completion, PR state, or executed verification results.
- `FEATURE_SPEC_TRACEABILITY_PACKET` remains a noncanonical link layer after approval.
- Specialized domain contracts remain authoritative where they are more precise; the generic feature spec references or composes them rather than replacing them.
- Google Sheets remains a user-facing summary/workspace and must not receive a duplicated full detailed spec.
- Any `skills/**/SKILL.md` change must satisfy Base coupled-change rules by changing an accepted focused test and `skills/SKILL_LEARNING_LOG.md`.
- Human/project-pilot effectiveness remains `NOT_RUN` until a real project uses the contract.

---

## File Structure

### Create
- `templates/planning/GAME_FEATURE_DESIGN_SPEC.md` — L2 feature-detail canonical authoring template.
- `tests/test_game_feature_design_spec_contract.py` — focused routing, boundary, and non-duplication regression tests.

### Modify
- `skills/managing-design-documents/SKILL.md` — route eligible L2 feature-detail authoring to the new template and preserve canonical ownership boundaries.
- `skills/analyzing-and-refining-game-concepts/SKILL.md` — add the promotion gate from PoC/recalibration into detailed feature specification.
- `templates/planning/DESIGN_DOCUMENT_SYSTEM.md` — document L0 → L1 → L2 → L3 resolution hierarchy.
- `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md` — add upstream `design_spec_id` and `canonical_design_spec_path` linkage without copying detailed behavior.
- `skills/SKILL_LEARNING_LOG.md` — record the absorbed workflow lesson and why no new Skill was created.

### Explicitly Do Not Modify
- `skills/SKILL_REGISTRY.json`
- `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`
- `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`
- unrelated specialized design contracts

---

### Task 1: RED — lock the contract before production changes

**Files:**
- Create: `tests/test_game_feature_design_spec_contract.py`

**Interfaces:**
- Consumes: current `managing-design-documents`, `analyzing-and-refining-game-concepts`, `DESIGN_DOCUMENT_SYSTEM`, and `FEATURE_SPEC_TRACEABILITY_PACKET` behavior on latest `main`.
- Produces: failing assertions that define the new template, promotion gate, upstream traceability linkage, and non-Registry requirement.

- [ ] **Step 1: Write the focused failing test**

Create tests that assert:

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_game_feature_design_spec_template_declares_l2_behavior_contract() -> None:
    template = read("templates/planning/GAME_FEATURE_DESIGN_SPEC.md")
    for token in (
        "L2",
        "Player Problem",
        "Experience Intent",
        "Player Verbs",
        "Entry / Exit / Cancel / Re-entry",
        "State & Rules",
        "Success / Failure / Partial Success / Recovery",
        "Data & Balance",
        "Benchmark Decision",
        "Risk & Prototype",
        "Acceptance Criteria",
        "Telemetry / Playtest",
        "Cut-down / Rollback",
        "Open Decisions",
        "USER_DECISION_REQUIRED",
        "BLOCKED_UNVERIFIED",
    ):
        assert token in template


def test_feature_spec_is_progressive_and_does_not_take_traceability_ownership() -> None:
    template = read("templates/planning/GAME_FEATURE_DESIGN_SPEC.md")
    assert "PoC" in template
    assert "L0" in template and "L1" in template
    assert "Task progress" in template
    assert "executed verification" in template
    assert "소유하지" in template


def test_existing_owner_skills_route_feature_detail_without_new_skill() -> None:
    docs = read("skills/managing-design-documents/SKILL.md")
    concepts = read("skills/analyzing-and-refining-game-concepts/SKILL.md")
    registry = read("skills/SKILL_REGISTRY.json")
    assert "GAME_FEATURE_DESIGN_SPEC.md" in docs
    assert "GAME_FEATURE_DESIGN_SPEC.md" in concepts
    assert "PoC" in concepts and "승격" in concepts
    assert "game-feature-design" not in registry


def test_document_hierarchy_and_traceability_link_upstream_spec() -> None:
    system = read("templates/planning/DESIGN_DOCUMENT_SYSTEM.md")
    packet = read("templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md")
    assert "L0" in system and "L1" in system and "L2" in system and "L3" in system
    assert "GAME_FEATURE_DESIGN_SPEC" in system
    assert "design_spec_id" in packet
    assert "canonical_design_spec_path" in packet
    assert "별도 책임 원본이 아니다" in packet
```

- [ ] **Step 2: Commit the test-only RED state and open a Draft implementation PR**

Commit message:

```text
test: define game feature design spec contract
```

- [ ] **Step 3: Run repository CI against the exact test-only HEAD**

Required evidence:

```text
Validate Game Project Operating System = failure
```

Expected failure cause: missing `templates/planning/GAME_FEATURE_DESIGN_SPEC.md` and missing owner/template linkage. If failure is caused by syntax, unrelated CI breakage, or proposal governance, fix the test harness first and re-run until the expected contract failure is observed.

---

### Task 2: GREEN — add the minimal L2 feature-detail contract

**Files:**
- Create: `templates/planning/GAME_FEATURE_DESIGN_SPEC.md`
- Modify: `skills/managing-design-documents/SKILL.md`
- Modify: `skills/analyzing-and-refining-game-concepts/SKILL.md`
- Modify: `templates/planning/DESIGN_DOCUMENT_SYSTEM.md`
- Modify: `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: Task 1 test tokens and Base owner boundaries.
- Produces: one reusable L2 template plus routing and hierarchy references; no new Registry identity.

- [ ] **Step 1: Create `GAME_FEATURE_DESIGN_SPEC.md` with explicit authority boundaries**

Required top contract:

```text
적용: PoC/benchmark/adversarial review를 거쳐 KEEP·CHANGE·RETEST 대상으로 남은 주요 L2 기능
권한: 기능이 플레이어에게 어떻게 동작해야 하는지에 대한 canonical detailed design source
비사용: L0/L1, pre-PoC idea, specialized source가 이미 같은 질문을 더 정확히 소유하는 경우
비소유: Task progress, implementation completion, PR state, executed verification evidence
```

Required sections:

```text
0. Identity & authority
1. Player Problem
2. Experience Intent & Core Alignment
3. Scope / Non-goals
4. Player Verbs & Decisions
5. Entry / Exit / Cancel / Re-entry
6. Player Flow
7. State & Rules
8. Input → Processing → Output
9. Feedback — UI / VFX / Animation / Audio / Haptics
10. Success / Failure / Partial Success / Recovery
11. Edge Cases
12. Data & Balance
13. UX/UI & Accessibility
14. Art / Audio / Narrative Dependencies
15. Technical / Platform / Save / Online Constraints
16. Content Production Pipeline
17. Benchmark Decision — ADOPT / ADAPT / TEST / AVOID / IGNORE
18. Risk & Prototype
19. Acceptance Criteria
20. Telemetry / Playtest Observation Plan
21. Cut-down / Rollback
22. Open Decisions
23. Handoff to Traceability
```

`Open Decisions` must distinguish `CONFIRMED`, `RECOMMENDED_DEFAULT`, `USER_DECISION_REQUIRED`, `HYPOTHESIS`, and `BLOCKED_UNVERIFIED`.

- [ ] **Step 2: Route authoring through `managing-design-documents`**

Add a focused conditional rule after the canonical-authoring structure:

```text
PoC 이후 여러 직군이 구현 의미를 공유해야 하는 L2 주요 기능은
`templates/planning/GAME_FEATURE_DESIGN_SPEC.md`를 사용한다.
이 Template은 Task/implementation/test execution 상태를 소유하지 않으며,
전문 분야 정본이 더 정확하면 해당 정본을 reference/compose한다.
```

Do not add a new mode or rename the Skill.

- [ ] **Step 3: Add the PoC promotion gate to `analyzing-and-refining-game-concepts`**

Add after recalibration/PoC logic:

```text
KEEP / CHANGE / RETEST로 살아남고 production handoff가 필요한 주요 기능만
L2 detailed-spec 후보로 승격한다.
pre-PoC idea, REMOVE/DEFER, 단일 L0/L1 수정은 승격하지 않는다.
승격 시 `managing-design-documents`에 넘겨 `GAME_FEATURE_DESIGN_SPEC.md`를 작성한다.
```

Do not move canonical document ownership into the concept Skill.

- [ ] **Step 4: Add the resolution hierarchy to `DESIGN_DOCUMENT_SYSTEM.md`**

Add a compact section:

```text
L0 Project Direction
→ L1 Feature Brief
→ benchmark / PoC / adversarial review
→ L2 Game Feature Design Spec
→ approval
→ L3 Feature Spec Traceability Packet
```

State explicitly that detail increases only when uncertainty has survived cheaper validation.

- [ ] **Step 5: Link the existing Traceability Packet upstream**

Extend Packet identity or canonical authority with:

```yaml
design_spec_id:
canonical_design_spec_path:
```

State that these fields point to the detailed canonical source and do not copy its rules, flows, values, or edge cases into the Packet.

- [ ] **Step 6: Add Learning Log evidence**

Record:

```text
Observation: concept/PoC and traceability had a reusable detailed-design gap.
Decision: absorb into existing concept + design-document owners with one L2 template.
Rejected: new broad Skill, MASTER_GDD, full-Sheets duplication, traceability ownership expansion.
Validation: focused contract test + Base CI; real-project pilot remains NOT_RUN.
```

- [ ] **Step 7: Commit minimal GREEN implementation**

Commit message:

```text
feat: add game feature design spec hierarchy
```

---

### Task 3: Verify GREEN and attack the boundaries

**Files:**
- Test: `tests/test_game_feature_design_spec_contract.py`
- Review all Task 2 changed files.

**Interfaces:**
- Consumes: exact Task 2 implementation HEAD.
- Produces: CI evidence plus adversarial findings classification.

- [ ] **Step 1: Run exact-head GitHub Actions**

Required result before any completion claim:

```text
Validate Game Project Operating System = success
ci-gate = success
```

- [ ] **Step 2: Run adversarial ownership review**

Attack these failure modes and classify each as `MUST_FIX`, `SHOULD_FIX`, `REJECTED_CRITIQUE`, or `BLOCKED_UNVERIFIED`:

```text
new ACTIVE Skill accidentally introduced
Feature Spec duplicates Task/PR/test-result tracking
Feature Spec replaces specialized design contracts
pre-PoC/L0/L1 work gets forced into L2
Traceability Packet becomes a second detailed canonical source
Google Sheets becomes a second full detailed canonical source
acceptance criteria are vague instead of observable
prototype/benchmark evidence is presented as human validation
```

Fix every surviving `MUST_FIX` before continuing.

- [ ] **Step 3: Compare implementation branch to latest main**

Required checks:

```text
behind main = 0 before final review, or rebase/refresh before conclusion
skills/SKILL_REGISTRY.json = unchanged
no unrelated specialized template = changed
no release lock/frozen snapshot = changed
```

---

### Task 4: Finalize BCP implementation state

**Files:**
- Modify after implementation validation: `[수정제안서]/BCP-2026-011-game-feature-design-spec-system/PROPOSAL.md`
- Modify after implementation validation: `[수정제안서]/PROPOSAL_REGISTRY.json`

**Interfaces:**
- Consumes: merged proposal approval reference, implementation PR URL, exact validated implementation HEAD.
- Produces: auditable BCP lifecycle state.

- [ ] **Step 1: Record `IMPLEMENTING` when the implementation PR opens**

Set `implementation_pr` to the Draft PR URL and retain the approval reference.

- [ ] **Step 2: After verified merge, record `IMPLEMENTED`**

Only after the implementation PR is merged and the merged main state is verified:

```text
status = IMPLEMENTED
implementation_pr = exact merged PR URL
validation = exact-head CI evidence
project_pilot = NOT_RUN
human_usability = HUMAN_NOT_RUN
```

- [ ] **Step 3: Do not repair historical BCP-008 in this implementation**

Keep `BCP-2026-008` Registry-history repair as an independent pre-existing governance finding.

---

## Self-Review

- Spec coverage: all BCP-011 ownership, progressive-detail, benchmark/PoC, detailed behavior, traceability boundary, specialized-contract boundary, and validation requirements are mapped to Tasks 1–4.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation steps remain.
- Identity consistency: `GAME_FEATURE_DESIGN_SPEC.md`, `design_spec_id`, `canonical_design_spec_path`, and `tests/test_game_feature_design_spec_contract.py` use the same names throughout.
- Scope control: no new ACTIVE Skill, Registry mutation, Sheets duplication, or unrelated specialized-contract edit is planned.
