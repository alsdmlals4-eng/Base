# Five-Stage Work Vertical Slice — Design Specification

**Date:** 2026-08-27  
**Status:** user-approved design baseline  
**Proposal:** BCP-2026-040  
**Base baseline:** `9b45125d087521fa98696cbd1e857bf2ffbf816a`

## 1. Problem

Current Work automation minimizes Work↔Codex transitions but collapses three materially different Work responsibilities into one stage:

```text
planning
+ planning review
+ images/audio/UI/data/VFX production
```

It also treats consolidated machine review and user handoff as one broad closeout. This makes it difficult to answer:

- Has the user actually approved the core fun and Slice promise?
- Was the plan independently reviewed before expensive asset production?
- Are images/audio/data ready, or merely listed?
- Did Codex implementation and machine QA finish?
- Is the Slice merely ready for user validation, or actually validated and complete?

## 2. Design goal

Establish one project-neutral orchestration vocabulary:

```text
Stage 1 — Planning
Stage 2 — Review
Stage 3 — Asset & Input Production
Stage 4 — Codex Implementation & Machine Verification
Stage 5 — User Validation
```

The contract must preserve:

- current Base/Project authority and fresh-read;
- startup canon correction;
- Reuse First and benchmark/market/success/failure evidence;
- Grill Me for user-owned product decisions;
- minimum Work↔Codex transitions;
- project-local durable Visual/Audio inputs;
- TDD, runtime/build, CI and IRG evidence;
- Human/Player evidence ceiling;
- safe Git/PR/merge/readback;
- recovery ladder and required-work-zero rescan;
- project-specific state vocabulary without mass migration.

## 3. Architecture

### 3.1 New owner

Add:

```text
templates/project-operations/WORK_FIVE_STAGE_VERTICAL_SLICE_EXECUTION_CONTRACT.md
```

This owner controls only:

- stage names and order;
- stage entry/output/exit gates;
- allowed return transitions;
- machine-ready vs user-validated completion semantics;
- mapping of existing project state vocabularies.

It does not duplicate detailed Visual, Git, Godot, CI, Grill Me or vertical-slice methods.

### 3.2 Existing owner composition

```text
WORK_PROJECT_START_CANON_CHECKLIST.md
→ Stage 1 bootstrap and canon correction

PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md
+ managing-project-intake-and-work-contract/references/grill-me-protocol.md
→ Stage 1 collaborative core decisions

WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
→ detailed production packets, Codex window, machine QA and delivery

WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md
→ Stage 3 project-local Visual binary route

WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md
→ candidate/CI/product/runtime/remote identity

skills/designing-vertical-slices/SKILL.md
→ player value trace, quality bar, pipeline proof, playtest and decision gate
```

The new contract declares:

```text
FIVE_STAGE_CONTRACT_SUPERSEDES_THREE_STAGE_LABELS_ONLY
THREE_STAGE_PROFILE_REMAINS_DETAIL_OWNER
```

## 4. Stage model

### Stage 1 — Planning

Purpose: co-design the player promise and approved Slice meaning.

Entry:

- exact Project/Base fresh-read;
- startup canon checklist and bounded correction;
- current stage/accepted frontier restored;
- existing decisions identified so they are not reopened.

Core user-owned decisions:

- project/player fantasy;
- pointed fun;
- core loop;
- meaningful choice/tradeoff;
- reward and failure learning;
- first-session promise;
- differentiator/sales point;
- Slice boundary and explicit non-scope.

Method:

```text
current canon + implementation
→ reuse candidates
→ current benchmark / market / success-failure evidence
→ minimum three materially distinct alternatives
→ GPT recommendation
→ Grill Me one product decision at a time
→ user confirmation
→ early canon sync/readback
```

Routine technical details are not re-questioned. Standing auto-approval does not cover unresolved core product meaning.

Output:

```text
USER_AND_GPT_CO_DESIGN_DECISION_PACKET
```

Exit:

```text
PLANNING_CONFIRMED_BY_USER
```

### Stage 2 — Review

Purpose: prevent flawed planning from flowing into expensive production.

Review scope:

- player-value trace;
- core/system consistency;
- benchmark interpretation and originality;
- requirement→owner→consumer trace;
- feasibility and current architecture fit;
- Slice scope and content cost;
- quality bar and first-session flow;
- Visual/Audio/Data/VFX requirement coverage;
- rights/provenance plan;
- acceptance, tests, runtime/build and user-validation contract;
- IRG preflight;
- minimum five whole-scope adversarial loops when material.

Stage 2 may return to Stage 1 when the plan’s product meaning changes. It does not silently expand scope or manufacture final assets.

Output:

```text
REVIEWED_SLICE_SPEC
```

Exit:

```text
REVIEW_GATE_PASSED
```

### Stage 3 — Asset & Input Production

Purpose: finish all Work-owned implementation inputs before Codex.

Includes when required:

- UI/UX flow and screen/state specification;
- project-local images, animation frames and VFX inputs;
- music/SFX/UI cue assets or implementation-ready procedural specifications;
- data/content tables and schemas;
- localization-ready strings and accessibility requirements;
- Art Style Lock and asset manifest;
- provenance/rights/hash/path/consumer records;
- acceptance and QA scenarios;
- Codex handoff packet.

Every player-facing element must have an actual consumer. Stage 3 does not implement product code, Scene/Resource wiring or runtime logic.

Output:

```text
WORK_PRODUCTION_INPUT_PACKET
```

Exit:

```text
READY_FOR_SINGLE_CODEX_WINDOW
```

### Stage 4 — Codex Implementation & Machine Verification

Purpose: build the representative end-to-end product Slice from approved inputs.

Owner split:

```text
Codex
→ product code / Scene / Resource / data / runtime wiring / tests / build

Work
→ returned diff/evidence audit / valid-finding correction routing / canon and merge closeout
```

Required evidence where applicable:

- actual implementation diff;
- deterministic tests and relevant regression;
- import/parse/headless smoke;
- representative runtime flow;
- adopted GUT/Hera or evidence-equivalent machine QA;
- UI/Visual/Audio/VFX actual consumer evidence;
- build/export and clean launch smoke;
- downloadable artifact with exact identity/hash;
- current-task exact-head CI/review/merge;
- new-main and required GitHub/Notion readback;
- machine-executable remaining work = 0;
- Human/Player evidence remains NOT_RUN.

Output:

```text
AUTOMATED_VERTICAL_SLICE_PACKAGE
```

Exit:

```text
AUTOMATED_VERTICAL_SLICE_READY_FOR_USER_VALIDATION
```

This is not Vertical Slice completion.

### Stage 5 — User Validation

Purpose: collect actual user evidence from the exact build.

The user receives:

- downloadable artifact;
- one-click or one-block launch route where possible;
- representative play window;
- expected action/choice/result and feedback;
- focused feedback questions;
- evidence capture route;
- known NOT_RUN boundaries.

The user actually plays the build. Results are classified:

```text
ACCEPT
FIX_IMPLEMENTATION
TUNE
FIX_ASSET_OR_FEEDBACK
REVIEW_SPEC
REDESIGN_CORE
HOLD
STOP
```

Return routing:

- core design finding → Stage 1;
- specification/acceptance finding → Stage 2;
- image/audio/UI feedback asset finding → Stage 3;
- implementation/bug/tuning finding → Stage 4.

Output:

```text
USER_VALIDATION_DECISION_PACKET
```

Exit:

```text
USER_VALIDATED_VERTICAL_SLICE_COMPLETE
```

## 5. Vertical Slice completion definition

### Machine-ready state

```text
AUTOMATED_VERTICAL_SLICE_READY_FOR_USER_VALIDATION
```

Requires:

- representative end-to-end flow implemented;
- production-candidate player-facing inputs for the approved Slice;
- actual runtime/build evidence;
- downloadable artifact;
- required machine tests and current-task closeout;
- no remaining machine-executable blocker;
- Human/Player remains NOT_RUN.

### Complete state

```text
USER_VALIDATED_VERTICAL_SLICE_COMPLETE
```

Requires all machine-ready conditions plus:

- the user actually played the exact build;
- the player promise, meaningful choice, observable result, reward/failure learning and first-session comprehension were observed or explicitly assessed;
- blocking user findings were corrected and revalidated, or explicitly accepted/deferred by the user;
- final decision is recorded;
- canonical reflection updates current repository/Notion owners and readback;
- current Slice remaining work is 0 after rescan.

This does not mean full game, all content, all platforms, release, performance certification or market success.

## 6. Stage transition rules

Normal:

```text
1 → 2 → 3 → 4 → 5
```

Allowed return paths:

```text
2 → 1
3 → 1 or 2 when source planning/spec conflict is discovered
4 → 1/2/3 through a consolidated change-proposal batch
5 → 1/2/3/4 based on finding class
```

Forbidden:

- Stage 1 directly to Stage 4 while required Stage 2/3 inputs are missing;
- Stage 3 creating product code;
- Stage 4 reinterpreting Core meaning without returning to Stage 1;
- Stage 4 being reported as completed Vertical Slice;
- Stage 5 expanding into the next Slice without a user decision.

## 7. Existing project state mapping

Do not mass-rename project canons. At startup record:

```yaml
FIVE_STAGE_PROJECT_STATE_MAPPING:
  canonical_project_state:
  mapped_five_stage:
  mapping_evidence:
  unresolved_conflict:
```

Examples of generic mapping:

- `PLAN`, incomplete core decisions → Stage 1
- planning complete but review/readiness unresolved → Stage 2
- `IMPLEMENTATION_READY` inputs being produced → Stage 3
- Codex/build/machine QA in progress → Stage 4
- `AUTOMATED_VERTICAL_SLICE_READY`, `USER_VALIDATION_PENDING` → Stage 5
- actual user acceptance with required corrections closed → complete

## 8. Project and Notion strategy

No portfolio-wide rename or IA migration is required.

At the next material Work entry for a project:

1. fresh-read the exact Project GitHub/Notion;
2. map current local status to one five-stage phase;
3. correct only stale/contradictory stage summary fields;
4. preserve project-specific Decision IDs, product terms and specialized gates;
5. update the human-facing current stage only when a current status surface already exists.

## 9. Failure modes and protections

- **Five-stage waterfall:** prevented by explicit return paths.
- **Repeated user questions:** existing approved decisions are reused; Grill Me targets unresolved core choices only.
- **Auto-approval overriding core design:** explicitly forbidden.
- **Asset generation before review:** Stage 3 requires Stage 2 pass.
- **Codex starts with missing inputs:** Stage 3 exit gate blocks it.
- **Machine QA called user validation:** Stage 4/5 states and evidence ceilings separate them.
- **Mass project canon churn:** mapping receipt replaces bulk rename.
- **Second canon:** new owner controls orchestration only and delegates detail.

## 10. Validation strategy

- RED-first focused contract.
- Verify Starter and Router routing.
- Verify exact five-stage order and one output/exit gate per stage.
- Verify Grill Me + benchmark + three alternatives + user confirmation in Stage 1.
- Verify boundary prohibitions.
- Verify Stage 4 machine-ready is not complete and Stage 5 is completion.
- Verify return paths.
- Verify representative live Project GitHub/Notion observations in evidence-only audit.
- Verify project-specific names do not enter active policy.
- Run current Base full required workflows on exact head.
- Perform at least five full-scope adversarial loops and continue until clean.

## 11. Rollback

Revert the implementation squash commit and remove the new owner from Starter/Router. Existing detailed profiles and project canons remain usable because no project-wide migration is required.
