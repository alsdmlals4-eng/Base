# Claim and Intent Verification Gate Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to execute this plan task by task. Preserve exact-head evidence and stop on concurrent overlap.

**Goal:** Absorb a fail-closed claim and approved-intent verification Mode into the existing project-change validation Skill without creating a new ACTIVE Skill or Work Mode.

**Architecture:** Extend one existing owner with a focused reference, Registry routing metadata, quality Template, REVIEW workflow connection, behavior fixture, Learning Log, and deterministic contract test. Reuse concurrent sync, traceability, Evidence ceiling, adversarial review, exact-head and post-merge contracts.

**Tech Stack:** Markdown, JSON, Python `unittest`, GitHub Actions, existing Base generators and validators.

---

## Task 0 — Concurrent-change preflight

1. Record:
   - `current_task_or_pr_identity: BCP-2026-027 implementation`
   - `source_main_sha`
   - `current_main_sha`
   - `write_parent_sha`
   - intended paths and semantic locks.
2. Inspect open/recent same-goal PRs and changed filenames.
3. Exclude this task/PR from duplicate comparison.
4. Classify `NO_OVERLAP | PATH_OVERLAP | SEMANTIC_OVERLAP | SAME_GOAL | UNKNOWN`.
5. Proceed only on `CLEAR`.
6. Repeat before PR creation, each write after a moved branch, and merge.

Current initial result:

```yaml
source_main_sha: a96864a84ac2513e488f20cba304c252dea3045d
current_main_sha: a96864a84ac2513e488f20cba304c252dea3045d
write_parent_sha: a96864a84ac2513e488f20cba304c252dea3045d
expected_head_sha: PENDING_FIRST_WRITE
open_prs:
  316: complementary invalidated-finding correction; path intersection 0
  312: visual tool work; path intersection 0
overlap_classification: NO_OVERLAP
disposition: CLEAR
```

## Task 1 — RED contract

Files:

- Create `tests/test_claim_and_intent_verification_contract.py`
- Create this plan and the companion design

The test must require, before production implementation:

- new reference and Skill Mode;
- material claim and intent status vocabulary;
- exact-ref readback negative case;
- Template sections;
- REVIEW workflow/operating integration;
- existing Registry owner metadata and active count `30`;
- `SBE-038` route and `NOT_RUN` honesty;
- Learning Log entry;
- BCP lifecycle transition.

Expected command:

```bash
python -m unittest tests.test_claim_and_intent_verification_contract -v
```

Expected RED: failures for absent reference/Mode/Template/Registry routing/behavior fixture/learning record. Capture exact HEAD and GitHub Actions job log. Do not add production contract before observing RED.

## Task 2 — Core reference

Create:

- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`

Required content:

- applicability and L0 exception;
- authority order;
- `MATERIAL_CLAIM_LEDGER` fields/statuses;
- `INTENT_IMPLEMENTATION_FIDELITY_MATRIX` fields/statuses;
- `COMPLETION_CLAIM_GATE` minimum Evidence;
- exact-ref repository-fact rule;
- deterministic-first and model-judge ceiling;
- independent VERIFIER/CRITIC;
- exact-head and post-merge main readback;
- fail-closed rationalization table.

Run focused test; remaining failures are expected until integration surfaces exist.

## Task 3 — Existing Skill integration

Modify:

- `skills/reviewing-and-validating-project-changes/SKILL.md`

Minimal changes:

1. Extend frontmatter description to completion claims and approved-intent fidelity.
2. Add `claim-and-intent-verification` to Skill Modes.
3. Add input requirements for approved intent, material claims, exact SHA, actual diff, executed evidence, producer report.
4. Add one focused workflow section linking the new reference.
5. Add output/DoD/failure rules:
   - producer/model/search explanation is a lead, not Evidence;
   - test definition is not execution;
   - merge requires merge SHA and main readback;
   - unmapped acceptance remains unverified.
6. Preserve all existing validation modes and ownership boundaries.

## Task 4 — Registry routing and generated summary

Modify:

- `skills/SKILL_REGISTRY.json`
- regenerate `docs/generated/BASE_ACTIVE_SKILLS.md`

Only the existing `reviewing-and-validating-project-changes` entry changes:

- trigger tags: `completion-claim`, `claim-evidence`, `intent-conformance`, `hallucination-audit`
- `use_when` and `review_triggers` for unsupported completion/intent claims.

Assertions:

- ACTIVE Skill ID set unchanged;
- active count remains `30`;
- no new responsibility ID;
- generated summary matches Registry.

Commands:

```bash
python tools/build_base_v9_artifacts.py --write
python tools/build_base_v9_artifacts.py --check
```

## Task 5 — Quality Template and workflow

Modify:

- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/OPERATING_MODEL.md`

Add:

- `원자 주장 원장`
- `의도-구현 충실도`
- `완료 주장 Gate`
- exact HEAD, post-merge readback, independent reviewer and Evidence ceiling fields
- REVIEW route from approved intent → evidence → counterevidence → verdict
- Builder report = lead, not Evidence
- L0 lightweight exception
- reuse of `CONCURRENT_CHANGE_PREFLIGHT`

## Task 6 — Behavior fixture and learning record

Modify:

- `skills/SKILL_BEHAVIOR_EVALS.json`
- `skills/SKILL_LEARNING_LOG.md`

Add `SBE-038`:

- expected mode: `REVIEW`
- primary owner: `reviewing-and-validating-project-changes`
- expected Skill Mode: `claim-and-intent-verification`
- required evidence includes claim/intent IDs, exact-ref readback, exact head, post-merge readback, fail-closed status
- negative case: search snippet/producer report without exact-ref readback
- keep `model_run_status: NOT_RUN` unless a real independent live run is performed.

Learning Log records trigger, finding, decision, evidence, boundary, next trigger.

## Task 7 — BCP lifecycle

Modify:

- `[수정제안서]/BCP-2026-027-claim-and-intent-verification-gate/PROPOSAL.md`
- `[수정제안서]/PROPOSAL_REGISTRY.json`

Before implementation PR merge:

- update source/current baseline and implementation PR URL;
- record #313 preflight reuse and #316 invalidated-finding regression;
- transition to the repository-supported implementation state;
- transition to `IMPLEMENTED` only when exact-head checks and merge evidence satisfy repository policy.

Do not claim post-merge evidence inside the pre-merge commit. Final merge state may require a follow-up lifecycle-only commit if the Registry contract cannot truthfully name its own future merge SHA.

## Task 8 — GREEN verification

Run:

```bash
python -m unittest tests.test_claim_and_intent_verification_contract -v
python -m unittest tests.test_neutral_adversarial_feature_lifecycle -v
python tools/check_skill_behavior_evals.py
python tools/check_canonical_reference_freshness.py
python tools/build_base_v9_artifacts.py --check
python tools/check_base_change_proposals.py
python -m unittest discover -s tests -p 'test_*.py'
```

GitHub Actions on exact HEAD are authoritative in connector-only execution. Record skips separately; do not report skipped runtime/human/render checks as PASS.

## Task 9 — Independent review and adversarial loop

Request independent review. Classify findings P0/P1/P2. For each:

```text
attack
→ verify criticism against exact source
→ accept/reject with evidence
→ apply minimal fix
→ rerun focused and broad regressions
```

Required counterexamples:

1. search result without exact-ref readback;
2. test file without execution result;
3. PASS on another SHA;
4. unmapped acceptance;
5. working implementation with changed approved UX meaning;
6. merged PR without post-merge readback;
7. moved main/open PR overlap after review.

## Task 10 — Merge and post-merge readback

Immediately before merge:

- reread current main, PR head, open/recent same-goal PRs and changed paths;
- ensure reviewed HEAD equals expected HEAD;
- required checks Green on exact HEAD;
- unresolved threads 0;
- no active path/semantic owner overlap.

Use squash merge with `expected_head_sha`.

After merge:

- read new main SHA;
- read back Skill Mode, reference, Registry owner, generated summary, Template, behavior fixture, Learning Log and BCP lifecycle;
- inspect post-merge push CI;
- report exact verified and unverified evidence.

## Rollback

Revert the implementation squash commit. Revert Registry metadata, generated summary, reference/Mode, Template/workflow, behavior fixture, Learning Log, tests and BCP lifecycle together. No product migration is required.
