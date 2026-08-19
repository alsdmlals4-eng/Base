# P07 Optimization Audit — 2026-08-19

## Identity

- `PART_ID: P07`
- `PART_NAME: Platform, Release & Execution Validation`
- `BASELINE_SHA: df8ef644d30fc96456da23a5157e5efb61b620bb`
- `BRANCH: opt/base-part-P07-evidence-freshness`
- `PR: #542`
- Scope authority: `docs/operations/BASE_PARTITION_MANIFEST.json`
- Context pack: `docs/operations/base-partitions/P07_PLATFORM_RELEASE_VALIDATION.md`
- Core Skill: `reviewing-and-validating-project-changes`

This audit is a P07 maintenance/specialization record, not a new global authority. CP0 and other Part changes are requests only.

## What P07 is

P07 turns implementation, runtime, platform, store, rights, backend, entitlement, build and release facts into bounded delivery evidence. It does not author gameplay, own the Godot runtime, decide adversarial policy, or treat planning/Notion approval as execution proof.

### Inputs

- P04 acceptance criteria and player-facing requirements
- P05 asset-rights inputs
- P06 runtime/toolchain evidence
- P03 adversarial decisions
- CP0 release identity
- platform/store first-party rules
- actual diff, test, build, device and submission evidence when available

### Processing

- material-claim and evidence-locator verification
- latest-exact-head validation
- static/runtime/build/submission evidence separation
- platform/store/source freshness review
- build-size/release/backend/entitlement readiness evaluation
- explicit blocker and unverified-state preservation

### Outputs / consumers

- evidence-backed completion/release decisions
- project release evidence packs and issue packets
- platform/release guides
- runtime/build/release blockers for P01/P03/project operators
- tests that prevent evidence-state inflation or contract drift

### Removal impact

Removing P07 would collapse the boundary between planning approval and executable/release proof, leave platform policy freshness without an owner, and fragment backend/DRM/build/store evidence across unrelated skills.

## Important rules audit

### 1. Evidence ceiling

- Canonical source: `skills/reviewing-and-validating-project-changes/SKILL.md` and `references/claim-and-intent-verification.md`
- Purpose: never promote a claim above the strongest executed evidence.
- Consumers: completion review, release review, runtime/build/platform checks.
- Tests: platform/entitlement/backend/release evidence tests.
- Finding: **KEEP**. Specialized status vocabularies are compatible with the common ceiling and should not be flattened into one global enum.

### 2. `LATEST_EXACT_HEAD_ONLY`

- Canonical source: claim-and-intent verification reference.
- Purpose: old successful evidence cannot certify a newer head.
- Consumers: PR review, CI evidence, merge readiness.
- External recheck: current GitHub required-check guidance still binds required checks to the current PR/commit state.
- Finding: **KEEP**.

### 3. Runtime/build proof is separate from planning approval

- Purpose: documents, Notion approvals, screenshots or accepted plans do not imply a runtime/build PASS.
- Consumers: P06→P07 handoff, release decision, user completion reports.
- Finding: **KEEP**. All project/device/human/submission `NOT_RUN` states in the PC/Android guide remain unchanged.

### 4. Platform official-source-first

- Purpose: mutable store policies are not Base constants.
- Rechecked 2026-08-19:
  - Google Play target API requirements still change on 2026-08-31 to API 36 for normal Android new apps/updates, with API 35 discoverability for existing normal Android apps.
  - new personal Google Play accounts covered by the current rule still require 12 opted-in closed testers for 14 continuous days before production-access application.
  - Steam Content Survey still compares survey answers against build/store content and includes generative-AI disclosure.
- Finding: **KEEP**. Existing Base guidance remains semantically current; no policy-number rewrite is required in this PR.

### 5. Android deferred until the approved release stage where applicable

- Purpose: do not turn Android device/submission work into an early universal blocker when the project has deliberately deferred it.
- Finding: **KEEP**. `DEVICE_NOT_RUN` and submission `NOT_RUN` remain truthful until project-stage evidence exists.

## Skill / Mode audit

### `reviewing-and-validating-project-changes`

- Disposition: **IMPROVE, DO NOT SPLIT**
- Trigger: completion, execution, regression, platform/release or external-evidence review.
- Inputs: diff, acceptance criteria, execution evidence, current official sources, project constraints.
- Outputs: bounded verdict, evidence locators, blockers/unverified states, regression findings.
- Important modes retained:
  - contract-check
  - multi-lens-review
  - external-source-review
  - claim-and-intent-verification
  - reference-freshness
  - static/runtime validation
  - accessibility/performance/regression review
  - evidence-report
- Overlap result: no second broad compliance/release Skill is justified. P03 owns adversarial decision quality; P06 owns runtime/toolchain evidence production; P07 owns delivery-evidence interpretation.

## Module audit

| Module | Responsibility | Main input | Output | Coupling finding |
| --- | --- | --- | --- | --- |
| Change Validation | diff/claim/acceptance verification | PR/diff + criteria | completion verdict | cohesive; keep |
| Evidence Ledger | evidence locators and ceilings | machine/human/source evidence | bounded claim state | cohesive; keep |
| Platform/Store Review | store policy, questionnaire, rights | official sources + build/store facts | platform blocker/readiness | cohesive; P01 template dependency needs declaration |
| Build/Size/Release | package/patch/release evidence | build measurements | release readiness | cohesive; keep |
| Backend/Online Services | backend fit/load/failure evidence | service/runtime evidence | verified/unverified capability | distinct from P06 runtime ownership |
| Entitlement/DRM | entitlement/integrity evidence | platform/backend/player-harm constraints | bounded protection decision | distinct; keep |

`templates/evidence/**`, `templates/testing/**`, and `schemas/game-evidence-pack/**` are currently reserved P07 ownership surfaces. Their absence is not by itself a defect; creating empty or duplicate canon solely to occupy the paths is rejected.

## Findings

### F1 — stale merged-contract lifecycle marker — MUST_FIX — RESOLVED

Baseline `PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` said:

```yaml
base_contract: PROPOSED_IN_DRAFT_PR
```

although the guide is already on current `main`. This mixed publication lifecycle state with project/runtime evidence.

Resolution:

```yaml
base_contract: ACTIVE_IN_MAIN
```

All actual-project/device/human/build/store `NOT_RUN` states are preserved.

Regression protection is placed in the already-consumed P07 `tests/test_platform_review_asset_rights_reference_production.py` suite rather than introducing a new broad Skill or duplicate evidence schema.

### F2 — P07 test consumes P01-owned evidence templates without declared dependency — CROSS_PART — OPEN_NONBLOCKING

P07-owned `tests/test_platform_review_asset_rights_reference_production.py` reads and validates:

- `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`

`templates/project-operations/**` is owned by P01, but P07 `read_only_dependencies` currently omits P01.

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: P07
  target_owner: CP0
  target_paths:
    - docs/operations/BASE_PARTITION_MANIFEST.json
  reason: P07-owned release/platform tests consume P01-owned project-operation evidence templates, but the P07 dependency list omits P01.
  evidence:
    - tests/test_platform_review_asset_rights_reference_production.py
    - P01 owned_write_paths: templates/project-operations/**
  required_semantic_change: declare the P01 project-operation evidence artifacts as a P07 read-only dependency without transferring write ownership.
  acceptance_criteria:
    - P07 read_only_dependencies explicitly names the P01 project-operation evidence dependency or an equivalent precise dependency
    - P01 remains the single write owner of templates/project-operations/**
    - no duplicate P07 template canon is introduced
  blocking: false
```

### F3 — P07 local validation pattern and current Required CI are not the same surface — CROSS_PART — OPEN_NONBLOCKING

Manifest P07 validation explicitly calls:

```text
python -m unittest discover -s tests -p 'test_*release*.py' -v
```

The current Required CI also runs important P07 platform/backend/entitlement tests, but its fixed suite does not automatically discover arbitrary future `tests/test_p07_*.py` or every Manifest-local command. During TDD this was observed when a temporary P07 release-freshness test existed but was not consumed by the active Required CI list.

The final regression was therefore moved into an already-consumed P07 platform test. The temporary unconsumed test was removed.

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: P07
  target_owner: CP0
  target_paths:
    - .github/workflows/**
    - docs/operations/BASE_PARTITION_MANIFEST.json
  reason: P07's declared local validation surface and Required CI consumption can diverge for newly added P07 tests.
  evidence:
    - P07 manifest validation command
    - PR #542 TDD observation
    - Required CI fixed test lists
  required_semantic_change: Integration should decide whether P07 local validation remains intentionally local or whether Required CI needs a stable P07 suite entrypoint/discovery contract.
  acceptance_criteria:
    - the intended relationship between Part validation and Required CI is explicit
    - a new P07 regression cannot be silently treated as CI-covered when it is not executed
    - CI cost remains bounded
  blocking: false
```

## Alternatives

### A. Keep current main unchanged

- Benefit: zero change cost.
- Rejected: leaves a merged active guide self-describing as draft and keeps an unsupported publication-state claim.

### B. Minimal lifecycle repair + regression in an existing consumed P07 test + cross-Part requests

- Accuracy: high
- Context/maintenance cost: low
- Collision risk: low
- Rollback: simple
- Verification: strong static/CI path
- Long-term fit: high
- **Selected.**

### C. Create a new central `schemas/game-evidence-pack/**` status schema and migrate all P07 state vocabularies

- Benefit: superficially uniform vocabulary.
- Rejected: specialized platform/backend/runtime states carry different meanings; migration creates a second authority and high consumer cost for one stale lifecycle marker.

### D. Split platform/release validation into new Skills

- Benefit: smaller individual documents.
- Rejected: current single validation Skill already has explicit modes and P03/P06 boundaries. A new broad compliance/release Skill increases routing/context pressure without a demonstrated independent consumer.

### Better-alternative search

No materially better alternative was found after source freshness, consumer tracing, CI tracing and ownership review. Option B solves the proven defect without expanding authority.

## External source dispositions — 2026-08-19

| Source | Disposition | Result |
| --- | --- | --- |
| Google Play target API requirement | ADOPT | current Base API 36/API 35 gate remains current; recheck at submission |
| Google Play new personal-account testing requirement | ADOPT | 12 testers / 14 continuous days remains current for affected accounts |
| Steamworks Content Survey | ADOPT | build/store/survey consistency and AI disclosure remain relevant |
| GitHub status-check / required-check guidance | ADOPT | exact current head evidence remains the correct Base direction |
| Godot export/runtime docs | REFERENCE_ONLY in P07 | runtime/toolchain execution remains P06 authority |

Source collection is evidence input, not canon promotion. Mutable platform policy remains revalidation-gated.

## Full adversarial review loops

### Loop 1 — rules + source freshness

Attack: current policy text, lifecycle state, evidence ceiling and official-source freshness.

Finding: stale `PROPOSED_IN_DRAFT_PR` on merged guide.

Action: change only publication state to `ACTIVE_IN_MAIN`; preserve every unexecuted project/runtime/submission state.

Regression result: no evidence inflation introduced.

### Loop 2 — ownership + consumers

Attack: trace P07 tests/templates/guides to actual owners and consumers.

Finding: P07 platform test consumes P01-owned project-operation templates while P07 Manifest omits P01 dependency.

Action: no cross-Part write; emit CP0 request F2.

Regression result: P01 remains canonical template owner.

### Loop 3 — Skill/Mode duplication + module boundaries

Attack: try to justify a new Skill, schema or unified status vocabulary.

Finding: no valid need. Existing Skill modes and six modules remain coherent; specialized status semantics are intentionally different.

Action: reject new Skill/schema/enum migration.

Regression result: routing/context cost does not grow.

### Loop 4 — test consumption + evidence claims

Attack: verify that a new regression is really consumed rather than merely existing in the repository.

Finding: temporary `tests/test_p07_release_evidence_freshness.py` was not part of current Required CI fixed test list.

Action: move the assertion into existing CI-consumed P07 platform test; delete temporary duplicate; emit CP0 request F3 for long-term Part-validation/CI relationship.

Regression result: final protection is on a proven active CI surface.

### Loop 5 — long-term fit + release evidence ceiling

Attack: re-check changed files, current platform sources, remaining `NOT_RUN`, ownership, rollback, and the case for broader refactoring.

Finding: no new P07-owned MUST_FIX. Current Google Play and Steam official rules support the existing policy direction. Runtime/device/human/submission evidence correctly remains unverified.

Action: keep minimal solution; no broader P07 refactor.

Regression result: `new valid MUST_FIX = 0` inside P07-owned scope; cross-Part requests remain nonblocking integration work.

`FULL_LOOPS_PERFORMED: 5`

`CLEAN_REVIEW_EXIT: true` for the P07-owned change set, conditional on exact-head tests/CI, scope validation and Notion readback remaining clean.

## Long-term fit

The selected change keeps P07 focused on evidence truth rather than accumulating more routing surfaces. It also makes a useful distinction explicit: **a Base contract can be active in main while project runtime, device, human and store-submission evidence remain NOT_RUN.**

## Trade-offs

- The regression lives in the established platform/rights test rather than a new dedicated test file; this favors actual CI consumption over file-level purity.
- P01 dependency and Part-validation/CI topology cannot be fixed in this P07 PR because both require CP0/other-owner changes.
- Mutable platform policy still requires periodic/source-at-release revalidation; no static guide can remove that operational cost.

## Revisit conditions

Revisit P07 architecture when any of the following becomes true:

- another platform/store is added;
- backend/provider strategy materially changes;
- P07 validation repeatedly requires P03 to the point the boundary is no longer independent;
- P01/P07 evidence-template coupling grows beyond a read-only dependency;
- newly added P07 tests repeatedly miss Required CI consumption;
- a platform policy update invalidates recorded API/test/store assumptions.

## Rollback

If the publication-state correction proves semantically wrong, revert the guide marker and the paired regression assertion together. Do not roll back any project/runtime `NOT_RUN` evidence because this PR does not promote those states.

## Unverified / not claimed

- actual project pilot: not run here
- physical Android device: not run here
- human usability: not run here
- Windows/Android project builds: not run here
- STOVE/Google Play/Steam submission: not run here
- legal review: not performed here
- platform approval: not claimed
