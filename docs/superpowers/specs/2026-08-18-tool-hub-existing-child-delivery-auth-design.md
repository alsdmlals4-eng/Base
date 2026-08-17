# Tool Hub Existing-Child Delivery Authority Design

Date: 2026-08-18
Issue: #512
Base main at design start: `2227b03cfc1fecbd77e69823a3a91505f70da6a7`

## Problem

During the Windows user-PC IRG, the Tool Hub and Character Studio were proven to be in the same owned process tree:

```text
Tool Hub PID 6888 / port 8764
└─ Studio wrapper PID 19436
   └─ Character Studio runtime PID 21328 / port 64211
```

The Character Studio could prepare a ChatGPT Pro handoff, import four PNG candidates, and reach `확정 및 전달`, but the private Studio-to-Hub request failed with `STUDIO_DELIVERY_AUTH_REQUIRED` / `Tool Hub rejected confirmed delivery` before Figma Bridge pairing.

The current supervisor state transition contains a deterministic mismatch:

1. Base `ProcessSupervisor._start()` sets the requested key to `REGISTERED` before checking for an already-running child.
2. If that child is alive and its authenticated health payload is valid, `_start()` returns the existing identity immediately.
3. The existing-child return path does not restore the public state to `RUNNING`.
4. `delivery_supervisor.ProcessSupervisor.authorize_delivery_token()` accepts a child token only when the same key's public state is exactly `RUNNING` and the owned child process is alive.

Therefore an ordinary repeat `start()` / UI `다시 열기` can preserve the same healthy Studio process and token while making delivery authorization fail closed.

## Decision

Restore exact `RUNNING` state only after the existing child has already passed the existing liveness and authenticated-health checks. Keep delivery authorization unchanged.

Implementation review refined the safest location: the production Tool Hub uses the delivery-aware subclass in `tools/tool-hub/src/tool_hub/delivery_supervisor.py`. Its public `start()` delegates to the reviewed base `start()` first; only after that successful authenticated call does it reacquire the same project/tool key lock and repair the stale `REGISTERED` state to `RUNNING` when the exact child still exists and is alive.

This keeps the base process supervisor generic and localizes delivery-authority repair to the delivery-aware production owner.

## Alternatives Rejected

### Accept `REGISTERED` in delivery authorization

Rejected because it weakens a security boundary. `REGISTERED` is not proof that an authenticated child is currently healthy.

### Rotate/reissue the private delivery token when reusing a child

Rejected because a live Studio already holds the original token. Rotation would require a new secure synchronization mechanism and adds unnecessary state.

### Always spawn a replacement Studio

Rejected because repeat `다시 열기` is intended to reuse a healthy project-bound child. Spawning a replacement adds process churn and creates additional ownership/cleanup risk.

### Modify the generic base supervisor directly

Not required for the production fix. The stale state affects private delivery authority, and the actual Tool Hub production owner is the delivery-aware subclass. Keeping the repair there reduces blast radius while preserving the same approved behavior.

## Required Runtime Behavior

For one exact `(tool_id, project_id)` key:

- First successful start creates one owned child and ends at `RUNNING`.
- A second start against that healthy child performs the current authenticated health check in the base supervisor.
- No second process is created.
- The same `ChildIdentity` is returned.
- After successful base `start()`, the delivery-aware owner reacquires the exact key lock.
- If the exact child still exists, remains alive, and the stale public state is exactly `REGISTERED`, the public state is restored to `RUNNING`.
- If a concurrent stop already removed or transitioned the child, the repair does nothing.
- The existing private `BASE_TOOL_HUB_DELIVERY_TOKEN` remains valid for that exact child.

Fail-closed behavior remains unchanged:

- wrong token: reject;
- another project/tool token: reject;
- dead child process: reject;
- failed authenticated health: mark/reject as unhealthy;
- `STOPPING` or other non-running lifecycle state: reject;
- no expansion of Figma, provider, project, or browser authority.

## Data Flow

```text
Hub UI: start/reopen exact Studio
        |
        v
delivery_supervisor.ProcessSupervisor.start()
        |
        v
base ProcessSupervisor.start()
        |
        +--> existing child alive?
        |      no -> UNHEALTHY / reject
        |
        +--> authenticated /api/status matches exact identity?
               no -> UNHEALTHY / reject
               yes -> existing identity returned
                         |
                         v
              reacquire exact key lock
                         |
                         +--> child still exists + alive
                         |    and public state == REGISTERED?
                         |          yes -> set RUNNING
                         |          no  -> leave state unchanged
                         v
                  return same identity
                         |
                         v
Later confirmed-delivery request
                         |
                         v
authorize_delivery_token()
  exact RUNNING state + live child + constant-time token match
                         |
                         v
                  delivery accepted
```

## Implementation Scope

Production change:
- `tools/tool-hub/src/tool_hub/delivery_supervisor.py::ProcessSupervisor.start`

Regression:
- `tools/tool-hub/tests/test_existing_child_delivery_auth.py`

Focused CI consumption:
- `.github/workflows/validate-tool-hub-subscription-contracts.yml`

The regression exercises real supervisor state transitions rather than merely asserting source text. The focused workflow explicitly triggers on the production and regression paths and consumes the regression on Ubuntu and Windows.

No change is planned for:

- `studio_delivery_api.py` authorization rules;
- `authorize_delivery_token()` accepted states;
- Figma route/pairing/receipt contracts;
- Studio client token format or Authorization header;
- provider/API-key behavior;
- project repositories or Figma files;
- Windows Job Object ownership semantics.

## TDD Evidence Contract

### RED

On RED head `cca705a4e650d5e4d4f13b82d6cf2dddcdff1e9f`, focused run `32080418145` consumed the new regression with production delivery-supervisor code unchanged. Ubuntu produced exactly:

```text
1 failed, 86 passed
assert 'REGISTERED' == 'RUNNING'
```

This proves the failure is the stale public state after healthy same-child reuse rather than an unrelated fixture failure.

### GREEN

The minimal production repair is a localized `start()` wrapper that runs only after `super().start()` succeeds and changes no delivery-auth acceptance rule. Exact-head focused validation must prove:

- reuse returns the same identity;
- public state is `RUNNING`;
- existing token authorizes;
- wrong token and non-running/dead child cases remain blocked;
- Ubuntu and Windows focused contracts and production-boundary contract pass.

## Adversarial Checks

Before merge, verify:

1. The fix does not make `REGISTERED` an authorized delivery state.
2. State repair occurs only after `super().start()` succeeds, which includes the existing authenticated-health check.
3. The exact key lock is reacquired before state repair so a concurrent stop cannot be overwritten after it has removed/transitioned the child.
4. Reuse does not spawn a second process or rotate the token.
5. Cross-project/cross-tool tokens cannot authorize.
6. A dead or stopping child remains unable to deliver.
7. No secret token appears in logs, API payloads, or diagnostics.
8. No Figma delivery claim is upgraded without an actual user-PC Bridge receipt/readback.

## User-PC Postmerge IRG

After postmerge server validation:

1. update Base to the merged main;
2. terminate the old Hub/Studio tree through the reviewed Hub shutdown path where possible;
3. start one fresh Tool Hub instance and one Urban Legend Character Studio child;
4. reuse the previously generated four PNG candidates; do not regenerate them;
5. create/import a fresh Studio run if the prior in-memory run did not survive restart;
6. select one candidate and confirm delivery;
7. require a real pairing code or paired Bridge state rather than `STUDIO_DELIVERY_AUTH_REQUIRED`;
8. continue Figma Bridge pairing, exact-byte receipt/readback, then later Asset Vault/Godot consumption gates.

CI is not evidence that the user-PC delivery path passed. `STUDIO_DELIVERY_AUTH_USER_PC` remains `NOT_RUN` until the live sequence succeeds.

## Stop-Loss Rule

If this merged fix still fails in the real user-PC delivery flow, do not open another full Tool Hub repair cycle. Preserve the generated images and reviewed Figma routes and switch the operating path to **Figma Bridge-only project image organization** as explicitly requested by the user.
