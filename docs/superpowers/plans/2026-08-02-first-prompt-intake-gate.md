# First-Prompt Intake Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a direction-anchor-first prompt mode to the existing intake Skill and require an approval-aware Grill Me alignment gate before every L1+ generated instruction is executed.

**Architecture:** Keep `managing-project-intake-and-work-contract` as the single owner. Put always-needed routing and gate rules in the Skill body, detailed ordering and examples in one reference, and reusable prompt-method rationale in the existing AI instruction Method. Preserve Registry bytes and test the cross-file contract with one focused regression.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions repository validation.

## Global Constraints

- Do not add a new broad Skill.
- Do not modify `skills/SKILL_REGISTRY.json`, released locks, or frozen/generated release artifacts.
- Every L1+ instruction-writing flow runs intake → first-prompt → contract → Grill Me alignment → confirmed execution.
- Do not repeat a Grill Me question when the exact contract already has a valid approval reference.
- Preserve L0 typo/formatting and identical-rerun exceptions.
- Front placement increases salience but never overrides higher-authority instructions or canonical constraints.

---

### Task 1: Lock the missing behavior with a focused regression

**Files:**
- Create: `tests/test_first_prompt_intake_contract.py`

**Interfaces:**
- Consumes: current `AGENTS.md`, intake Skill, AI instruction Method, Legacy aliases.
- Produces: executable assertions for the first-prompt and Grill Me alignment contract.

- [ ] **Step 1: Write the failing test**

Create tests that require:

```python
FIRST_PROMPT_REFERENCE = ROOT / "skills" / "managing-project-intake-and-work-contract" / "references" / "first-prompt-direction-anchoring.md"
```

Assertions must cover:

```text
`first-prompt`
DIRECTION_ANCHOR
TASK_AND_SUCCESS
CONTEXT_AND_SOURCES
CONSTRAINTS_AND_PROTECTED_SCOPE
OUTPUT_AND_VALIDATION
정석안
파격안
통합안
Grill Me alignment gate
AWAITING_USER_CONFIRMATION
exact contract already approved
L0
앞에 배치했다고 상위 권한이 되지 않는다
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python -m unittest tests.test_first_prompt_intake_contract -v
```

Expected: FAIL because the reference, Skill mode, and mandatory gate do not yet exist.

- [ ] **Step 3: Commit the RED contract**

```bash
git add tests/test_first_prompt_intake_contract.py
git commit -m "test: define first-prompt intake contract"
```

### Task 2: Add the direction-anchor reference and Skill mode

**Files:**
- Create: `skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`

**Interfaces:**
- Consumes: intake routing, neutral recommendation gate, Grill Me protocol, Interface-first Method.
- Produces: `first-prompt` mode and a single detailed reference.

- [ ] **Step 1: Add the reference**

Define:

```yaml
direction_anchor:
task_and_success:
context_and_sources:
constraints_and_protected_scope:
output_and_validation:
optional_response_diversification:
conflict_scan:
approval_state:
```

Include the sequence:

```text
DIRECTION_ANCHOR
→ TASK_AND_SUCCESS
→ CONTEXT_AND_SOURCES
→ CONSTRAINTS_AND_PROTECTED_SCOPE
→ OUTPUT_AND_VALIDATION
→ OPTIONAL_RESPONSE_DIVERSIFICATION
```

Require conventional, bold, and integrated alternatives only for real design/decision exploration.

- [ ] **Step 2: Extend the intake Skill**

Add `first-prompt` to Skill Modes and route every L1+ instruction-writing request through:

```text
route → inspect facts → first-prompt → contract → clarify/Grill Me alignment → confirmation → execution
```

Add the reference to `Read first`, the state model, Definition of Done, failure conditions, and legacy alias section.

- [ ] **Step 3: Run the focused test**

```bash
python -m unittest tests.test_first_prompt_intake_contract -v
```

Expected: remaining failures only for global rule, Method, and aliases.

- [ ] **Step 4: Commit the Skill change**

```bash
git add skills/managing-project-intake-and-work-contract
git commit -m "feat: add first-prompt intake mode"
```

### Task 3: Propagate the mandatory alignment gate

**Files:**
- Modify: `AGENTS.md`
- Modify: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- Modify: `skills/LEGACY_SKILL_ALIASES.md`

**Interfaces:**
- Consumes: `first-prompt` mode and Grill Me protocol.
- Produces: always-on L1+ instruction rule, reusable method, and human-compatible routing names.

- [ ] **Step 1: Update the always-on rule**

State that every L1+ generated work instruction uses intake and cannot proceed to execution without the Grill Me alignment gate or a valid exact-contract approval reference.

- [ ] **Step 2: Extend the Method**

Add a “First-prompt direction anchoring” section explaining salience, authority limits, ordering, delimiters, optional three-way alternatives, and conflict scanning.

- [ ] **Step 3: Add compatibility names**

Map:

```text
[좋은 프롬프트]
좋은 프롬프트
퍼스트 프롬프트
first prompt
```

To `managing-project-intake-and-work-contract` with `first-prompt` + `contract` + `clarify`.

- [ ] **Step 4: Run focused and related tests**

```bash
python -m unittest tests.test_first_prompt_intake_contract -v
python -m unittest tests.test_base_v9_4_ai_operations_contract -v
```

Expected: PASS.

- [ ] **Step 5: Commit propagation**

```bash
git add AGENTS.md docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md skills/LEGACY_SKILL_ALIASES.md
git commit -m "docs: require prompt alignment before execution"
```

### Task 4: Adversarial and repository verification

**Files:**
- Review all changed paths.

**Interfaces:**
- Consumes: complete branch diff.
- Produces: exact-head evidence and explicit evidence limits.

- [ ] **Step 1: Attack the design**

Check for:

```text
new broad Skill duplication
interview on L0 work
repeated questions despite prior approval
front-loaded sentence overriding authority
artificial three-option output on mechanical work
missing conflict scan
execution before confirmation
Registry or release-lock mutation
```

- [ ] **Step 2: Run repository checks**

```bash
python -m unittest tests.test_first_prompt_intake_contract -v
python -m unittest tests.test_base_v9_4_ai_operations_contract -v
python tools/check_canonical_reference_freshness.py
python tools/check_skill_system_coverage.py
python tools/check_base_v9_integrity.py
git diff --check
```

- [ ] **Step 3: Record evidence limits**

Keep cross-model behavior, actual prompt quality improvement, and human comprehension as `NOT_RUN` unless separately executed.

- [ ] **Step 4: Commit any validated review fixes**

```bash
git add <reviewed-paths>
git commit -m "fix: close first-prompt review findings"
```

- [ ] **Step 5: Open a Draft PR**

The PR body must report the exact base/head, changed-file inventory, focused test results, repository gates, protected surfaces, adversarial findings, and evidence limits.
