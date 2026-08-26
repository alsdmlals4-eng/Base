# Work-Codex Minimum-Transition Automation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans. This plan is being executed in the current session under the user-approved continuous-work contract.

**Goal:** Add an explicit opt-in Work profile that completes current-Slice in-game inputs before Codex, uses one consolidated Codex implementation and machine-QA window, performs Work final evidence review, and hands an automatically verified vertical slice to the user for actual play validation.

**Architecture:** Keep Work v4.9 and all current Base domain owners authoritative. Add one progressive-loaded project-operation adapter, route it append-only from the Compatibility Appendix, and protect its activation, phase ordering, approval boundaries, fallback behavior, QA ceiling, and remaining-work semantics with a focused Python contract.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub pull requests, repository `ci-gate`, squash merge.

**Spec:** Proposal PR #729 and the 2026-08-27 user approval in the current ChatGPT Work conversation.

## Global Constraints

- Completed-main baseline: `43b3ffb2c5b026e3d4a38dab2338585894d36f61`.
- All pre-existing open/draft/ready PRs remain read-only.
- No new Skill, provider, paid dependency, executor, Registry owner, second canon, engine migration, direct-main push, force push, or ruleset bypass.
- Default image approval remains active without explicit current-user delegation.
- Work remains non-product owner; Codex remains game-product implementation owner.
- HiGodot remains sole persistent authoring authority; GUT/Hera roles follow the current owner.
- Machine evidence never becomes Human/Player PASS.
- Remaining-work zero is bounded to the current approved Slice and automation phase.

---

### Task 1: Establish RED contract evidence

**Files:**
- Create: `tests/test_work_codex_minimum_transition_automation_contract.py`

**Produces:** A deterministic contract for profile discovery, three-stage order, delegated approvals, high-risk deferral, stall fallback, scope-bounded zero, GUT/Hera evidence, current-owner composition, completed Codex implementation, Work final review, and user validation separation.

- [x] **Initial RED before production implementation**

Exact corrected RED head:

```text
25195a44c420b73f4ef886a15d93008675224e63
```

Command and result:

```bash
python -m unittest tests.test_work_codex_minimum_transition_automation_contract -v
# Ran 6 tests; FAILED with 6 expected assertion failures and 0 errors.
# Cause: the opt-in profile did not exist.
```

- [x] **Completion-meaning RED**

Exact test-only head:

```text
cb83526920493f2f6298037104c3670d21fcb8f0
```

The added test rejected `Codex one-window implementation attempted` and required completed implementation before automated readiness.

- [x] **Current-owner composition RED**

Exact test-only head:

```text
d235e36ac5c1490ecba8bc1f6f6dc966dfba06f2
```

The added test required the adapter to name and defer to current continuous-work, GPT–Codex, Visual, Vertical Slice, and HiGodot/GUT/Hera owners.

- [x] **Final-review and equivalent-QA RED**

Exact test-only head:

```text
51cfdcb5a8854d6c9ba8e593f1f519ad9eabc588
```

The added tests required Work final evidence review before user validation, evidence-equivalent machine QA when GUT/Hera is not adopted, and blocking high-risk decisions to prevent phase advance.

---

### Task 2: Implement the current-owner composition adapter

**Files:**
- Create: `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`

**Consumes:**

```text
skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md
docs/GPT_CODEX_WORKFLOW_POLICY.md
docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md
docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md
skills/designing-vertical-slices/SKILL.md
docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md
```

- [x] **Activation and ownership**

The profile is explicit opt-in only, current-Slice only, host-confirmation preserving, and `COMPOSE_CURRENT_OWNERS_NOT_SECOND_CANON`.

- [x] **Minimum-transition phase order**

```text
WORK_PREP_COMPLETION_BEFORE_CODEX
→ CODEX_SINGLE_IMPLEMENTATION_WINDOW
→ WORK_FINAL_EVIDENCE_REVIEW_BEFORE_USER_VALIDATION
→ AUTOMATED_VERTICAL_SLICE_READY
→ READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

- [x] **Work production input packet**

The packet includes exact Project/Slice identity, scope/non-scope/protected scope, planning/rules, UI/UX Flow, data/state, actual-consumer Visual/Audio/VFX inputs, provenance/rights, acceptance, deterministic tests, runtime QA, build/export, canon updates, rollback, blockers, and evidence ceiling.

- [x] **Delegated routine approval and high-risk deferral**

Routine reversible decisions inside the approved Slice proceed without repeated questions. Irreversible data loss, account/security expansion, new paid cost, legal/rights uncertainty, external publication, force/direct-main/admin bypass, project-core replacement, and broad engine/save-breaking migration are deferred and bundled.

- [x] **Stall fallback**

The adapter uses current-state readback, root-cause classification, bounded retry, authorized fallback A/B, evidence-equivalent local/manual route, local defer, independent continuation, deferred re-evaluation, and global stop last.

- [x] **Codex consolidated return**

The return packet records exact baseline/head, implementation, files/reasons, deterministic/runtime/build evidence, Visual/Audio consumption, missing inputs, change proposals, high-risk items, independent remaining work, failed/not-run tests, evidence locations, and one bounded Work re-entry classification.

- [x] **Machine QA and evidence ceiling**

GUT/Hera are used only when adopted. Non-adopted projects require an evidence-equivalent deterministic/runtime QA route. Hera persistent mutation is forbidden and source delta must remain `NONE`. Human Usability and Player Experience stay `NOT_RUN` until the user plays.

- [x] **Scope-bounded zero and clean exit**

The adapter requires completed Codex implementation, current-Slice machine-executable remaining work zero, completion-candidate rescan, at least five full adversarial loops, safe merge/readback when applicable, and user validation as the next explicit milestone.

Final profile blob:

```text
97bc7d39cb580284657ba5925312524ee97ec909
```

---

### Task 3: Route the profile without changing default Work behavior

**Files:**
- Modify: `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md`

- [x] **Append explicit delegated profile routing**

The added section contains:

```text
EXPLICIT_USER_DELEGATION_REQUIRED
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
```

- [x] **Preserve the original appendix**

The original appendix blob is:

```text
1cf2cc79db3fed8ccea00e975a0070d69419b05a
```

The current appendix contains that exact original byte sequence followed by one blank separator and the new section. Existing v4.9 behavior is unchanged when delegation evidence is absent.

Final appendix blob:

```text
55ac4a7cd5993ce65fe048adae9345b2b0f1e9c5
```

---

### Task 4: Focused and static verification

**Files:**
- Test: `tests/test_work_codex_minimum_transition_automation_contract.py`
- Verify: profile and Compatibility Appendix

- [x] **Match local reconstructed files to remote Git blobs**

```text
profile: 97bc7d39cb580284657ba5925312524ee97ec909
test: a1269bcde5f6788af11b58d6408998cdbf192338
appendix: 55ac4a7cd5993ce65fe048adae9345b2b0f1e9c5
```

- [x] **Run final focused GREEN contract**

```bash
python -m unittest tests.test_work_codex_minimum_transition_automation_contract -v
# Ran 10 tests; OK.
```

- [x] **Run static profile checks**

```text
Markdown fence parity: PASS
placeholder scan: PASS
forbidden attempted-completion wording: absent
current-owner routes: present
```

- [x] **Establish static v4.9 non-regression**

The main Work instruction and P08 are absent from the implementation diff. The Compatibility Appendix change is append-only, so existing positive token checks cannot lose their prior inputs. Fresh repository execution remains required before merge.

- [ ] **Run exact-head repository CI**

Required evidence:

```text
ci-gate: PASS on the final exact PR head
core regression: PASS or current required equivalent
canonical freshness: PASS
whitespace: PASS
```

A missing workflow run is `NOT_RUN`, not PASS.

---

### Task 5: Final adversarial review, safe merge, and post-merge readback

- [ ] **Complete at least five full-scope loops on the final candidate**

Each loop rechecks user intent, opt-in/default boundary, current-owner composition, Work/Codex transition count, Visual/Audio actual consumers, approval safety, high-risk phase blocking, fallback equivalence, GUT/Hera authority, Human/Player ceiling, scope-bounded zero, open-PR concurrency, CI/ruleset, rollback, and context cost.

- [ ] **Reconcile latest completed main**

The implementation head must remain based on the current completed main or be safely reconciled before checks and merge.

- [ ] **Verify merge gates**

Require exact head, current `ci-gate`, unresolved threads 0, review blockers 0, conflict 0, protected-scope drift 0, and high-risk blockers 0.

- [ ] **Enable or execute squash merge using exact head**

No direct main, force push, admin, or ruleset bypass.

- [ ] **Read back new main and proposal lifecycle**

Fetch the merged files from new main, verify the merge SHA is current, recheck same-goal/open PRs, and report proposal PR #729 status without falsely claiming its merge if proposal-only CI remains unavailable.

- [ ] **Recalculate remaining work**

Only exact-head CI, safe merge, new-main readback, and proposal lifecycle reconciliation may remain after content review. Any blocker is reported with its exact resume condition.
