# Universal Loop Capsule-to-SHADOW Adapter

## Purpose

This adapter is the deterministic bridge between the merged M2 Project Execution Capsule contracts and the merged M3 model-free SHADOW Kernel.

It does not add new project authority. It converts already-validated M2 Planning/Visual/Package/Coverage data into the closed `LOOP_SHADOW_REQUEST` shape expected by M3.

## Authority rule

Human-approved project meaning remains in the M2 documents. The adapter accepts only four runtime observations that M2 does not own:

```text
run_id
observed_main_sha
planning_drift
visual_drift
```

Callers cannot inject changed paths, allowed paths, Requirement IDs, Evidence, Resource Locks, Canon references, autonomy, A3 permissions, Scheduler configuration, or M3 transition budgets.

## Translation

```text
M2 Project Execution Capsule bundle
→ validate_bundle()
→ load Planning / Visual / Package / Coverage
→ verify observed main SHA
→ reject Planning/Visual conflict or unverified drift
→ derive Coverage-output changed paths
→ build closed LOOP_SHADOW_REQUEST
→ parse_shadow_request()
→ normalized read-only request
```

Authority-bearing field mapping:

- `project_id`, `source_main_sha`, autonomy, A3 allowlist, Scheduler ← Capsule
- Planning status and approved Requirement IDs ← Planning Lock
- Visual status ← Visual Lock
- package ID, Requirement IDs, allowed paths, visual impact, required Evidence, Resource Locks ← Implementation Package
- tasks, outputs, tests, Evidence and derived `changed_paths` ← Coverage Ledger
- Canon reference paths ← Planning authority sources
- M3-specific budgets ← fixed conservative adapter defaults (`16` transitions, `2` repeated failures)

`changed_paths` is the normalized, deterministic union of Coverage outputs. It is never accepted from the caller.

## Fail-closed gates

Translation stops when:

- M2 bundle validation has any finding;
- observed main differs from the Capsule source SHA;
- runtime identifiers or drift values violate M3's closed contract;
- Planning Drift is `PLANNING_CONFLICT` or `UNVERIFIED`;
- existing locked visual work is `VISUAL_CONFLICT` or `UNVERIFIED`;
- a package requires new visual design;
- M2 project/path/Coverage/authority integrity fails;
- M3 `parse_shadow_request` rejects the generated request.

## Read-only boundary

The adapter and CLI do not:

- write `.loop-engineering` state;
- invoke M3 `shadow` execution;
- invoke models;
- access the network;
- execute subprocesses from the adapter package;
- write project product, Planning, Visual, Figma, or asset files;
- create or merge PRs;
- enable A3;
- configure a Scheduler.

The CLI only prints the translated request or a blocked diagnostic.

## CLI

```bash
python tools/loop_capsule_to_shadow.py \
  docs/operations/loop/PROJECT_EXECUTION_CAPSULE.json \
  --run-id RUN_001 \
  --observed-main-sha <trusted-current-main-sha> \
  --planning-drift NO_DRIFT \
  --visual-drift NOT_APPLICABLE
```

The trusted current main SHA must come from the execution environment, not from model inference.

## Rollback

Revert the adapter PR. M2 and M3 remain independently usable and no project/product migration is involved.
