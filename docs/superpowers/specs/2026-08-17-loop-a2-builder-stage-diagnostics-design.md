# Loop A2 REAL Builder Stage Diagnostics Design

## Goal

Identify the exact adapter stage of the live `BUILDER_PROVIDER_EXCEPTION / AttributeError` without exposing raw traces or guessing a functional fix.

## Design

Keep the A2 public receipt contract unchanged. `A2Runtime` already publishes only `provider_error_type`; replace an unexpected raw exception escaping `GitWorktreeBuilderAdapter.invoke()` with a stable stage exception class before it reaches `A2Runtime`.

Stages:
- `BuilderWorkspacePreparationError`
- `BuilderWorkerInvocationError`
- `BuilderDiffCollectionError`
- `BuilderResultBindingError`

Intentional fail-closed domain results remain `WorkerResult` values and are not converted to exceptions. Existing `BuilderStageError` instances pass through unchanged. No traceback, exception message, path, prompt, stdout/stderr, or credential is added to public evidence.

## Data flow

`GitWorktreeBuilderAdapter.invoke()` stage-wraps unexpected exceptions around workspace preparation, worker invocation, diff collection, and result binding. `OpenAIWorkspaceBuilder` remains unchanged: its model/provider call, response parsing, and local-write failures already become bounded `BLOCKED WorkerResult` values. Therefore a live `BuilderWorkerInvocationError` further narrows the original `AttributeError` to the pre-provider Builder preparation path that currently sits outside that internal containment boundary.

`A2Runtime` remains unchanged and records only `type(error).__name__` in its existing provider-failure receipt.

## Diagnostic run

After merge, use a fresh non-counting run id so the confirmed missing `builder.close()` lifecycle does not let a stale `BS_A2_BURNIN_001` workspace mask the original failure. This diagnostic run is evidence only and never increments REAL burn-in count.

## Invariants

```yaml
raw_trace_publication: FORBIDDEN
paid_openai_api: FORBIDDEN
api_key_fallback: FORBIDDEN
blacksmith_authority: UNCHANGED
blacksmith_product_scope: UNCHANGED
a3_auto_merge: DISABLED
scheduler: NOT_CONFIGURED
real_a2_burnin_runs: 0
```
