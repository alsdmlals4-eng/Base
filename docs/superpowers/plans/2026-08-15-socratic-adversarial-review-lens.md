# Socratic Adversarial Review Lens Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Socratic Review Lens to the existing adversarial review Skill without creating a new Skill ID, Registry entry, or user-interview gate.

**Architecture:** Keep `running-adversarial-review-and-refinement` as the single execution owner. Put the six Socratic question families and selection/escalation rules in one new reference, link that reference from `SKILL.md`, and lock the behavior with the existing neutral-adversarial contract test. Only update freshness/changelog/learning-log surfaces when the focused change actually requires them.

**Tech Stack:** Markdown Skill contracts, Python `unittest`, JSON reference-freshness configuration.

## Global Constraints

- Do not modify any currently open/draft/in-progress PR branch.
- Base branch starts from exact `main` SHA `1d57e75adc7401afffe7d908423b4876aeb00a64`.
- Do not create a new Skill ID or Registry entry.
- Do not change `base-v9.4.lock.json` or released identity pins.
- Do not turn Socratic questioning into a mandatory six-question checklist or a new user interview gate.
- Repository/canonical/tool evidence must be investigated before asking the user.
- Existing `MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED` meanings remain unchanged.
- Actual model behavior is not claimed from string-contract tests alone.

---

### Task 1: Lock the Socratic contract in a failing focused test

**Files:**
- Modify: `tests/test_neutral_adversarial_feature_lifecycle.py`
- Test: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Consumes: existing `read(relative: str) -> str` helper and current adversarial Skill path.
- Produces: a test contract that requires the new reference, all six lens identifiers, selective-use rules, internal-evidence-first rules, and meta-question validation.

- [ ] **Step 1: Add a failing test**

Add this method to `NeutralAdversarialFeatureLifecycleTests`:

```python
    def test_socratic_review_lens_is_selective_evidence_first_and_meta_validated(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        socratic = read(
            "skills/running-adversarial-review-and-refinement/references/"
            "socratic-questioning-lenses.md"
        )

        for term in (
            "Socratic Review Lens",
            "socratic-questioning-lenses.md",
            "저장소·정본·실제 구현·도구",
            "사용자에게 묻지 않는다",
        ):
            self.assertIn(term, adversarial)

        for term in (
            "Clarification",
            "Assumptions",
            "Reasons / Evidence",
            "Viewpoints",
            "Implications / Consequences",
            "Meta-question",
            "관련된 Lens만",
            "가짜 Finding",
            "BLOCKED_UNVERIFIED",
            "USER_DECISION_REQUIRED",
            "답이 달라지면 실제 결정도 달라지는가",
        ):
            self.assertIn(term, socratic)

        self.assertIn("사용자 질문은 마지막 수단", socratic)
        self.assertNotIn("skill_id: socratic-questioning", socratic)
```

- [ ] **Step 2: Run the focused test and observe RED**

Run:

```bash
python -m unittest tests.test_neutral_adversarial_feature_lifecycle.NeutralAdversarialFeatureLifecycleTests.test_socratic_review_lens_is_selective_evidence_first_and_meta_validated -v
```

Expected: FAIL because `socratic-questioning-lenses.md` does not exist yet.

- [ ] **Step 3: Commit the RED contract**

```bash
git add tests/test_neutral_adversarial_feature_lifecycle.py
git commit -m "test: require Socratic adversarial review lens"
```

---

### Task 2: Add the Socratic reference and wire it into the Skill

**Files:**
- Create: `skills/running-adversarial-review-and-refinement/references/socratic-questioning-lenses.md`
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`
- Test: `tests/test_neutral_adversarial_feature_lifecycle.py`

**Interfaces:**
- Consumes: existing `attack`, `validate-critique`, `regression-recheck`, finding decisions, and cross-discipline lens selection rules.
- Produces: one selectable Socratic reference with six lenses plus explicit escalation rules.

- [ ] **Step 1: Create the reference with the six lenses**

The file must contain these headings and rules:

```markdown
# Socratic Questioning Review Lenses

## 목적과 권한
Socratic Review Lens는 적대적 검토의 질문 구조를 강화하지만 Finding 판정·분야 작성·사용자 결정을 소유하지 않는다.

## 선택 규칙
- 현재 Requirement·주장·Finding·위험과 직접 관련된 Lens만 선택한다.
- 모든 Lens를 채우기 위해 가짜 Finding을 만들지 않는다.
- 저장소·정본·실제 구현·도구로 답할 수 있는 사실은 먼저 직접 조사한다.
- 사용자 질문은 마지막 수단이다.

## Clarification
## Assumptions
## Reasons / Evidence
## Viewpoints
## Implications / Consequences
## Meta-question
```

Each section must define its Base-specific purpose, attack prompts, validation rule, and non-escalation condition. `Meta-question` must include the literal check `답이 달라지면 실제 결정도 달라지는가`.

- [ ] **Step 2: Wire the reference into `SKILL.md`**

Add a compact `Socratic Review Lens` subsection that:

```text
- reads references/socratic-questioning-lenses.md only when ambiguity, hidden assumptions, evidence gaps, viewpoint blind spots, consequence risk, or critique-quality uncertainty is material;
- uses clarification/assumptions/evidence/viewpoints/consequences mainly during attack;
- uses evidence/assumptions/meta-question during validate-critique;
- rechecks consequences during regression-recheck;
- investigates repository/canonical/actual implementation/tool evidence before user escalation;
- does not ask the user when those sources can answer the question.
```

- [ ] **Step 3: Run the focused Socratic test**

Run:

```bash
python -m unittest tests.test_neutral_adversarial_feature_lifecycle.NeutralAdversarialFeatureLifecycleTests.test_socratic_review_lens_is_selective_evidence_first_and_meta_validated -v
```

Expected: PASS.

- [ ] **Step 4: Run the full neutral-adversarial focused suite**

Run:

```bash
python -m unittest tests.test_neutral_adversarial_feature_lifecycle -v
```

Expected: PASS, with existing symmetry, no-manufactured-opposition, post-change-monitor, and Registry identity tests still green.

- [ ] **Step 5: Commit the implementation**

```bash
git add skills/running-adversarial-review-and-refinement/SKILL.md \
  skills/running-adversarial-review-and-refinement/references/socratic-questioning-lenses.md
git commit -m "feat: add Socratic adversarial review lens"
```

---

### Task 3: Verify coupled references and record only completed learning

**Files:**
- Inspect: `.github/reference-freshness.json`
- Modify only if required: `.github/reference-freshness.json`
- Modify after tests pass: `docs/CHANGELOG.md`
- Modify after tests pass: `skills/SKILL_LEARNING_LOG.md`
- Test: repository governance tests selected by the changed-file coupling rules.

**Interfaces:**
- Consumes: the exact changed path set from Tasks 1-2.
- Produces: canonical freshness coverage and completion/learning records without changing Registry or released locks.

- [ ] **Step 1: Inspect reference-freshness coupling**

Check whether `local-skill-contract-learning-test-sync` or another existing rule already couples changes under `skills/running-adversarial-review-and-refinement/` to `tests/test_neutral_adversarial_feature_lifecycle.py` and learning records.

If the existing rule already catches the new reference path, do not modify the JSON. If it only names files narrowly and misses the new reference, minimally extend that existing rule rather than creating a duplicate rule.

- [ ] **Step 2: Add completion records after focused GREEN**

Add one concise changelog entry describing `Socratic Review Lens` as an internal extension of the existing adversarial Skill, and one learning-log entry recording:

```text
- six Socratic lenses are useful as selective review lenses, not a mandatory questionnaire;
- repository/canonical/tool evidence precedes user questioning;
- meta-question validation prevents critique-for-critique and question inflation;
- no new Skill ID or Registry entry was needed.
```

Do not record model-run success unless an actual model behavior evaluation was executed.

- [ ] **Step 3: Run governance/freshness tests**

Run the focused test(s) that own the changed coupled rule plus:

```bash
python -m unittest tests.test_neutral_adversarial_feature_lifecycle -v
```

If `.github/reference-freshness.json` changes, also run the repository's canonical reference-freshness validation command identified by the existing rule/tests before claiming PASS.

- [ ] **Step 4: Confirm protected identities are unchanged**

Verify:

```text
skills/SKILL_REGISTRY.json: unchanged
base-v9.4.lock.json: unchanged
open/draft PR branches: untouched
```

- [ ] **Step 5: Commit governance records**

```bash
git add docs/CHANGELOG.md skills/SKILL_LEARNING_LOG.md .github/reference-freshness.json
git commit -m "docs: record Socratic review lens adoption"
```

Omit `.github/reference-freshness.json` from `git add` when it did not require a change.

---

### Task 4: Adversarial regression review and PR handoff

**Files:**
- Review only: all files changed by Tasks 1-3.
- No new production files unless a validated in-scope finding requires a minimal fix.

**Interfaces:**
- Consumes: final branch diff and focused test evidence.
- Produces: attack → validate-critique → regression-recheck → decision-report closure and a PR against `main`.

- [ ] **Step 1: Attack the final diff**

Explicitly test these failure hypotheses:

```text
- Did the new lens accidentally become a mandatory six-question checklist?
- Can it manufacture findings simply to satisfy categories?
- Does it ask the user for facts available in the repository/canonical/tool evidence?
- Does it duplicate cross-discipline-review-lenses responsibilities?
- Does it alter existing finding severities or user decision authority?
- Did it create or mutate a Registry Skill ID?
- Did it touch unrelated/open PR-owned work?
```

- [ ] **Step 2: Validate each critique**

Classify each as `MUST_FIX`, `SHOULD_FIX`, `REJECTED_CRITIQUE`, `DEFER`, or `BLOCKED_UNVERIFIED` using actual diff and test evidence. Apply only validated in-scope fixes.

- [ ] **Step 3: Regression-recheck**

Rerun the focused suite and any governance test changed by Task 3. Confirm no new ambiguity, duplicate authority, or user-question inflation remains.

- [ ] **Step 4: Compare exact branch head to current main**

Re-read `main`, same-goal open/recent PRs, and changed-file diff. If `main` advanced, re-evaluate conflicts before PR creation and do not force-update unrelated work.

- [ ] **Step 5: Open a PR**

Create a PR whose body records:

```text
Goal: add Socratic Review Lens inside existing adversarial review Skill.
Architecture: new reference + narrow Skill wiring + focused regression.
No new Skill ID/Registry/released-lock change.
Open/draft existing PRs untouched.
Tests actually executed and their results.
MODEL_RUN_STATUS: NOT_RUN unless an actual behavior model run was executed.
Rollback: revert this PR as one unit.
```

Do not merge unless required checks, exact-head review, unresolved-thread gate, and post-change monitor requirements are actually satisfied.
