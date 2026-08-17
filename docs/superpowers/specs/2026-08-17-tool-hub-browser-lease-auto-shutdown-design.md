# Tool Hub Browser-Lease Auto Shutdown Design

## Status

Approved interaction direction: when the last Tool Hub browser tab/window is closed, the Tool Hub parent and every Studio child started by that Hub should shut down automatically. Manual `Tool Hub 종료` remains available as an immediate fallback but is no longer required for normal use.

## Problem

The current Tool Hub lifetime is process-owned rather than browser-owned. Closing the browser UI does not stop the localhost Hub or its child Studio processes. A later GitHub Desktop Fetch/Pull can therefore overlap with still-running Tool Hub validation and child processes, causing unnecessary CPU/disk contention and user-visible lag.

The desired normal operation is:

```text
open desktop shortcut
→ Tool Hub runs
→ use Tool Hub / Studios
→ close the last Tool Hub tab
→ Hub stops all Hub-owned Studio children
→ Hub process exits
→ Git Fetch/Pull can proceed without a stale Tool Hub process
```

## Constraints

- Do not require PowerShell or a terminal for normal shutdown.
- Do not kill unrelated Python/Git/Figma processes.
- Only processes owned by the exact Tool Hub supervisor may be stopped.
- Refreshing the Tool Hub page must not shut down the Hub.
- Closing one of several Tool Hub tabs must not shut down the Hub while another Tool Hub tab is still active.
- Studio child tabs do not keep the Hub alive. The selected policy is: closing the final Tool Hub tab shuts down the Hub and all Hub-owned children even if Studio tabs remain open.
- Existing explicit `/api/shutdown` behavior and lifecycle cleanup remain fail-safe fallbacks.
- Existing browser/session/CSRF boundaries must not be weakened.
- Figma Bridge or external provider processes that are not owned by the Tool Hub process supervisor must not be killed by this feature.
- Browser background-timer throttling or memory-saving must not cause a normally open Tool Hub tab to be treated as closed after only a few seconds.

## Considered Approaches

### A. Browser lease + close signal + conservative heartbeat fallback — selected

Each Tool Hub page instance owns a random per-tab lease ID. The page registers that lease, renews it periodically, and sends a best-effort release during `pagehide`. The server tracks live leases. When the final lease is explicitly released, the Hub starts a short shutdown grace period. A refresh/new tab that reconnects during the grace period cancels shutdown.

Heartbeat expiry exists only as a slow crash-recovery fallback; it is not the normal close detector. This avoids treating a background-throttled browser tab as dead.

Advantages:
- Uses the existing HTTP/session/CSRF boundary.
- Handles multiple tabs explicitly.
- Normal tab close is fast.
- Refresh-safe with a short grace period.
- Browser crash still has a bounded cleanup fallback.
- Easy to unit-test without introducing a new protocol.

Trade-off:
- Browser/OS crash cleanup is intentionally slower than normal tab-close cleanup to avoid false shutdown during browser timer throttling.

### B. WebSocket connection lifetime

Each Tool Hub tab keeps a WebSocket open; last socket disconnect starts shutdown.

Advantages: fast disconnect detection.

Rejected because it adds a new authenticated protocol path and extra security/testing surface solely for lifecycle control.

### C. Browser unload request only

Send one shutdown/release request when the tab closes.

Advantages: minimal code.

Rejected because browser unload requests are best-effort and may be dropped during browser crash, OS shutdown, navigation, or process termination.

## Selected Architecture

### 1. Server-side `BrowserLeaseManager`

Add a small lifecycle component with one responsibility: track Tool Hub browser-page leases and determine when the Hub has no remaining UI owner.

State:
- lease ID → last-seen monotonic timestamp
- `armed`: false until at least one valid browser lease has registered
- normal heartbeat interval: 30 seconds
- conservative stale-lease TTL: 5 minutes
- explicit last-tab shutdown grace: 2 seconds

The manager does not directly kill arbitrary processes. Its shutdown callback invokes the same reviewed shutdown path used by the explicit shutdown endpoint:

```text
launcher.stop_all()
→ shutdown_callback()
→ Uvicorn server exits
→ FastAPI lifespan finally calls launcher.stop_all() again idempotently
```

The `armed` state prevents a freshly started Hub from terminating before the launcher has opened its first browser page.

### 2. HTTP lease API

Add same-origin endpoints under the existing Hub security middleware:

```text
POST /api/browser-lease/open
POST /api/browser-lease/heartbeat
POST /api/browser-lease/close
```

Payload:

```json
{ "lease_id": "<browser-generated UUID>" }
```

Rules:
- non-GET endpoints keep the current CSRF requirement;
- lease IDs must match a bounded UUID-like format and are not authentication credentials;
- unknown `close` is idempotent;
- `heartbeat` for an unknown lease registers/re-registers the current page, which makes refresh recovery straightforward;
- no lease endpoint can launch or identify Studio/Figma resources.

### 3. Browser client lifecycle

On Tool Hub page startup:

```text
crypto.randomUUID()
→ load /api/config and CSRF
→ POST browser-lease/open
→ begin heartbeat every 30 seconds
```

On `pagehide`:
- stop the heartbeat timer;
- issue `fetch(..., {method: "POST", keepalive: true, headers: {X-Hub-CSRF: ...}})` to close the lease;
- do not call `/api/shutdown` directly.

`pagehide` is the primary normal-close signal. A duplicate close is harmless because the server close operation is idempotent.

This distinction is required for refresh safety and multiple-tab support.

### 4. Shutdown decision

The server maintains two paths:

**Normal close path**
1. final active lease receives `close`;
2. record zero-live-lease timestamp;
3. wait 2 seconds;
4. if a new/replacement lease appears, cancel pending shutdown;
5. otherwise call the reviewed Hub shutdown callback exactly once.

**Crash fallback path**
1. watchdog periodically removes leases whose heartbeat is older than 5 minutes;
2. if this leaves zero live leases and the manager is armed, use the same 2-second grace;
3. any new lease cancels the pending shutdown.

The long stale TTL is intentional: browser background tabs can throttle timers heavily, and normal close does not depend on this timeout.

Expected behavior:

| Situation | Result |
|---|---|
| Close only Tool Hub tab | Hub + Hub-owned Studios stop automatically after ~2 s grace |
| Close one of two Tool Hub tabs | Hub stays alive |
| Refresh current Tool Hub tab | replacement lease appears during grace; Hub stays alive |
| Switch to another browser tab / leave Hub in background | Hub stays alive; heartbeat timeout is intentionally conservative |
| Browser/renderer crashes | stale lease eventually expires and Hub shuts down |
| Studio tab remains open but Hub tab closes | Studio process is stopped with Hub |
| Manual `Tool Hub 종료` | immediate shutdown, unchanged |
| Figma desktop/plugin remains open | not killed by Hub lifecycle manager |

## Git Fetch/Pull Interaction

The feature reduces the stale-process overlap that produced the user-visible lag after closing the browser and immediately using GitHub Desktop. It does not run Git itself and does not alter repositories.

The shutdown path must not perform Fetch, Pull, Reset, Clean, Checkout, package installation, or project mutation. Its only responsibility is terminating the Hub and Hub-owned child processes.

A normal browser close should usually stop the Hub after roughly the 2-second grace period because `pagehide` is the primary signal. If the browser/renderer crashes and no close request arrives, the conservative fallback can take about 5 minutes plus grace; this is preferable to false shutdown of a legitimate background tab.

## Error Handling

- Lease API validation failure: reject the request; do not shut down.
- Browser heartbeat request failure: retry on the next heartbeat; server stale timeout remains the fallback.
- Duplicate/open heartbeat: idempotent update.
- Duplicate/unknown close: idempotent success.
- Pending shutdown is cancelled by any valid new/open/heartbeat lease.
- Shutdown callback exception: log through the existing bounded runtime log; lifecycle `finally` still calls `launcher.stop_all()`.
- A lease manager must never terminate the process before its first valid browser lease has armed it.

## Security Boundary

The selected design does not add a new cross-origin channel. It reuses existing loopback-only HTTP, same-origin browser access, session cookie, and CSRF controls.

Only a bounded random tab lease identifier crosses the new endpoints. No provider token, Figma credential, Git credential, project path, or launcher token is added to browser storage or lease payloads.

The feature cannot terminate unrelated processes because shutdown continues to route through the existing Tool Hub `ProcessSupervisor.stop_all()` ownership boundary.

## Testing Strategy

### Server contract tests

1. First valid lease arms the manager.
2. Zero leases before first registration does not shut down the Hub.
3. Single explicit lease close starts 2-second shutdown grace.
4. New lease during grace cancels shutdown.
5. Two leases: closing one does not shut down.
6. A recently heartbeating/background lease is not expired prematurely.
7. Stale lease older than 5 minutes is removed and eventually shuts down.
8. Unknown/duplicate close remains idempotent.
9. Shutdown callback fires once only.
10. Explicit `/api/shutdown` still stops children immediately.

### Web contract tests

1. Page creates one lease after `/api/config` succeeds.
2. Heartbeat uses the existing CSRF header.
3. `pagehide` uses keepalive close rather than direct `/api/shutdown`.
4. Refresh/re-init can create a replacement lease during grace.
5. No provider secrets or launcher credentials appear in browser lease code.

### Integration / Windows IRG

After merge on the user PC:

1. Pull latest Base main.
2. Launch Tool Hub only from the desktop shortcut.
3. Start Character Studio and confirm it is Hub-owned.
4. Close the Tool Hub browser tab without pressing `Tool Hub 종료`.
5. Verify Tool Hub port 8764 disappears automatically after the short grace.
6. Verify Character Studio child also exits.
7. Verify no PowerShell/console window appears.
8. Immediately run GitHub Desktop Fetch/Pull and confirm the previous stale-Hub lag is no longer reproduced.
9. Reopen Tool Hub from the desktop icon and continue the Character Studio → Figma live IRG.

CI alone must not promote this feature to user-PC PASS; steps 4–8 are required live evidence.

## Scope Exclusions

Not part of this change:
- Tool Hub startup-time optimization or Git validation caching;
- Figma Bridge process ownership changes;
- browser-specific extension installation;
- automatic Git operations;
- keeping the Hub alive from Studio tabs;
- changing project identity, anchor, Sprite, Expression, or Figma routing contracts.

Those remain separate work items.
