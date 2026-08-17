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

## Considered Approaches

### A. Browser lease + heartbeat + grace period — selected

Each Tool Hub page instance owns a random per-tab lease ID. The page registers that lease with the Hub, renews it periodically, and attempts a best-effort release during `pagehide`. The server tracks live leases. When the final live lease disappears, the Hub starts a short shutdown grace period. A refresh/new tab that reconnects during the grace period cancels shutdown. If no lease returns, the Hub calls the existing child cleanup path and then requests its own Uvicorn shutdown.

Advantages:
- Uses the existing HTTP/session/CSRF boundary.
- Handles multiple tabs explicitly.
- Refresh-safe with a short grace period.
- Has a timeout fallback when browser unload delivery is lost.
- Easy to unit-test without introducing a new protocol.

Trade-off:
- If the browser crashes and the release request is lost, automatic shutdown waits for the heartbeat TTL instead of being instantaneous.

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
- heartbeat TTL: 6 seconds
- last-tab shutdown grace: 2 seconds

The manager does not directly kill arbitrary processes. Its expiry callback invokes the same reviewed shutdown path used by the explicit shutdown endpoint:

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
→ begin heartbeat every 2 seconds
```

On `pagehide`/`beforeunload`:
- stop the heartbeat timer;
- issue `fetch(..., {method: "POST", keepalive: true, headers: {X-Hub-CSRF: ...}})` to close the lease;
- do not call `/api/shutdown` directly.

This distinction is required for refresh safety and multiple-tab support.

### 4. Shutdown decision

The watchdog periodically removes leases whose last heartbeat is older than 6 seconds.

If the manager is armed and the live lease count becomes zero:
1. record the zero-lease timestamp;
2. wait 2 seconds;
3. if any lease reappears, cancel pending shutdown;
4. otherwise call the reviewed Hub shutdown callback exactly once.

Expected behavior:

| Situation | Result |
|---|---|
| Close only Tool Hub tab | Hub + Hub-owned Studios stop automatically |
| Close one of two Tool Hub tabs | Hub stays alive |
| Refresh current Tool Hub tab | temporary lease loss is recovered during grace period; Hub stays alive |
| Browser crashes | heartbeat expires, then Hub auto-shuts down |
| Studio tab remains open but Hub tab closes | Studio process is stopped with Hub |
| Manual `Tool Hub 종료` | immediate shutdown, unchanged |
| Figma desktop/plugin remains open | not killed by Hub lifecycle manager |

## Git Fetch/Pull Interaction

The feature reduces the stale-process overlap that produced the user-visible lag after closing the browser and immediately using GitHub Desktop. It does not run Git itself and does not alter repositories.

The shutdown path must not perform Fetch, Pull, Reset, Clean, Checkout, package installation, or project mutation. Its only responsibility is terminating the Hub and Hub-owned child processes.

A normal close request should usually stop the Hub after roughly the 2-second grace period. If the browser close request is lost, the heartbeat fallback may take up to roughly 8 seconds (6-second TTL + 2-second grace).

## Error Handling

- Lease API validation failure: reject the request; do not shut down.
- Browser heartbeat request failure: the browser retries on the next heartbeat; server timeout remains the fallback.
- Duplicate/open heartbeat: idempotent update.
- Duplicate/unknown close: idempotent success.
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
3. Single lease close starts shutdown grace.
4. New lease during grace cancels shutdown.
5. Two leases: closing one does not shut down.
6. Expired heartbeat removes stale lease and eventually shuts down.
7. Unknown/duplicate close remains idempotent.
8. Shutdown callback fires once only.
9. Explicit `/api/shutdown` still stops children immediately.

### Web contract tests

1. Page creates one lease after `/api/config` succeeds.
2. Heartbeat uses the existing CSRF header.
3. `pagehide` uses keepalive close rather than direct `/api/shutdown`.
4. Refresh/re-init can create a replacement lease.
5. No provider secrets or launcher credentials appear in browser lease code.

### Integration / Windows IRG

After merge on the user PC:

1. Pull latest Base main.
2. Launch Tool Hub only from the desktop shortcut.
3. Start Character Studio and confirm it is Hub-owned.
4. Close the Tool Hub browser tab without pressing `Tool Hub 종료`.
5. Verify Tool Hub port 8764 disappears automatically.
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
