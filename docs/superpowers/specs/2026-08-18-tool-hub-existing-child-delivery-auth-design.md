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

1. `ProcessSupervisor._start()` sets the requested key to `REGISTERED` before checking for an already-running child.
2. If that child is alive and its authenticated health payload is valid, `_start()` returns the existing identity immediately.
3. The existing-child return path does not restore the public state to `RUNNING`.
4. `delivery_supervisor.ProcessSupervisor.authorize_delivery_token()` accepts a child token only when the same key's public state is exactly `RUNNING` and the owned child process is alive.

Therefore an ordinary repeat `start()` / UI `다시 열기` can preserve the same healthy Studio process and token while making delivery authorization fail closed.

## Decision

Restore exact `RUNNING` state only after the existing child passes the same liveness and authenticated-health checks already required by the reuse path.

The fix belongs in the existing-child success path of the supervisor, not in delivery authorization.

## Alternatives Rejected

### Accept `REGISTERED` in delivery authorization

Rejected because it weakens a security boundary. `REGISTERED` is not proof that an authenticated child is currently healthy.

### Rotate/reissue the private delivery token when reusing a child

Rejected because a live Studio already holds the original token. Rotation would require a new secure synchronization mechanism and adds unnecessary state.

### Always spawn a replacement Studio

Rejected because repeat `다시 열기` is intended to reuse a healthy project-bound child. Spawning a replacement adds process churn and creates additional ownership/cleanup risk.

## Required Runtime Behavior

For one exact `(tool_id, project_id)` key:

- First successful start creates one owned child and ends at `RUNNING`.
- A second start against that healthy child performs the current authenticated health check.
- No second process is created.
- The same `ChildIdentity` is returned.
- The public supervisor state is restored/confirmed as `RUNNING` before return.
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
ProcessSupervisor.start()
        |
        v
_start(): existing child found
        |
        +--> process alive?
        |      no -> UNHEALTHY / reject
        |
        +--> authenticated /api/status matches exact expected identity?
               no -> UNHEALTHY / reject
               yes
                |
                v
          set public state RUNNING
                |
                v
          return existing identity
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

Expected production change: `tools/tool-hub/src/tool_hub/supervisor.py`, existing-child reuse success path only.

Expected regression coverage: existing Tool Hub supervisor/delivery tests. The test must exercise real supervisor state transitions rather than merely assert source text.

No change is planned for:

- `studio_delivery_api.py` authorization rules;
- Figma route/pairing/receipt contracts;
- Studio client token format or Authorization header;
- provider/API-key behavior;
- project repositories or Figma files;
- Windows Job Object ownership semantics.

## TDD Contract

### RED

Create a regression that represents an existing healthy child with an injected private delivery token and starts the same key again. On current main it must prove:

- existing child identity is reused;
- no replacement process is required;
- after the reuse call, delivery-token authorization fails because the public state was left as `REGISTERED` instead of `RUNNING`.

The test should fail specifically on the desired postcondition (`RUNNING` / token authorization), not because of an unrelated fixture error.

### GREEN

Make the smallest production change so the exact same test proves:

- reuse returns the same identity;
- public state is `RUNNING`;
- existing token authorizes;
- wrong token and non-running/dead child cases remain blocked.

Run focused Tool Hub contracts on Ubuntu and Windows plus the applicable Base/GPO/confirm-delivery integration gates before merge.

## Adversarial Checks

Before merge, verify:

1. The fix does not make `REGISTERED` an authorized delivery state.
2. `RUNNING` is set only after authenticated health succeeds.
3. Reuse does not spawn a second process or rotate the token.
4. Cross-project/cross-tool tokens cannot authorize.
5. A dead or stopping child remains unable to deliver.
6. No secret token appears in logs, API payloads, or diagnostics.
7. No Figma delivery claim is upgraded without an actual user-PC Bridge receipt/readback.

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
