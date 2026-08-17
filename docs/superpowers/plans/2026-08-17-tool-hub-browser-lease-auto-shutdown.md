# Tool Hub Browser-Lease Auto Shutdown Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Tool Hub and every Hub-owned Studio child shut down automatically when the final Tool Hub browser tab closes, while keeping refresh, multiple tabs, browser background throttling, and existing security boundaries safe.

**Architecture:** Add a small `BrowserLeaseManager` that tracks per-tab lease IDs using monotonic time and one cancellable background timer. Wire three same-origin CSRF-protected lease endpoints into `create_app()`, centralize manual and lease-triggered shutdown through the existing `launcher.stop_all()` + Uvicorn shutdown callback path, and make `app.js` register/heartbeat/release one lease per Tool Hub page. Normal close uses `pagehide` plus a 2-second grace; heartbeat expiry is a conservative 300-second crash fallback.

**Tech Stack:** Python 3.12, FastAPI, Pydantic 2, `threading.Timer`, pytest, browser JavaScript (`crypto.randomUUID`, `fetch(..., keepalive: true)`), existing Tool Hub security middleware, GitHub Actions Ubuntu/Windows.

## Global Constraints

- Normal use must not require PowerShell or a terminal.
- Closing the final Tool Hub tab stops the Hub and every Studio child owned by that Hub.
- Closing one of several Tool Hub tabs must not stop the Hub.
- Refresh must be recoverable during the 2-second shutdown grace.
- Studio child tabs do not keep the Hub alive.
- Browser background throttling must not cause short false shutdowns; stale-lease TTL is exactly 300 seconds.
- Normal heartbeat interval is exactly 30 seconds.
- Explicit final-tab shutdown grace is exactly 2 seconds.
- Existing `/api/shutdown` remains an immediate fallback.
- Only Hub-owned children may be stopped; unrelated Python/Git/Figma processes remain untouched.
- Lease endpoints remain under existing same-origin/session/CSRF middleware.
- Lease IDs are bounded UUIDs and are not credentials.
- No Git Fetch/Pull/Reset/Clean/Checkout, package installation, provider call, Figma mutation, or project mutation is added to shutdown.
- No provider, Figma, Git, project path, or launcher credential may enter browser lease payloads/storage.
- CI cannot promote user-PC auto-shutdown to PASS; live Windows close/port/child/Fetch-Pull evidence is still required.

---

### Task 1: Deterministic browser lease manager

**Files:**
- Create: `tools/tool-hub/src/tool_hub/browser_lifecycle.py`
- Modify/Test: `tools/tool-hub/tests/test_web_launch_diagnostics.py`

**Interfaces:**
- Produces: `BrowserLeaseManager(shutdown_callback, *, clock=time.monotonic, timer_factory=threading.Timer, heartbeat_ttl=300.0, shutdown_grace=2.0)`
- Produces: `open(lease_id: str) -> None`, `heartbeat(lease_id: str) -> None`, `close(lease_id: str) -> None`, `stop() -> None`, `live_count -> int`, `armed -> bool`
- Timer handles must support `start()` and `cancel()`; real `threading.Timer` instances are daemonized before start.

- [ ] **Step 1: Add RED manager tests to the existing focused suite**

Extend `tools/tool-hub/tests/test_web_launch_diagnostics.py` with a manual clock/timer fixture and tests equivalent to:

```python
class ManualClock:
    def __init__(self) -> None:
        self.value = 0.0
    def __call__(self) -> float:
        return self.value
    def advance(self, seconds: float) -> None:
        self.value += seconds

class ManualTimer:
    def __init__(self, delay, callback):
        self.delay = delay
        self.callback = callback
        self.cancelled = False
        self.daemon = False
    def start(self):
        return None
    def cancel(self):
        self.cancelled = True
    def fire(self):
        if not self.cancelled:
            self.callback()
```

Required RED cases:

```python
def test_browser_lease_manager_waits_for_first_browser_owner(): ...
def test_final_explicit_close_shuts_down_after_two_second_grace(): ...
def test_replacement_lease_during_grace_cancels_shutdown(): ...
def test_one_of_two_tabs_closing_keeps_hub_alive(): ...
def test_recent_background_heartbeat_is_not_expired(): ...
def test_stale_lease_uses_300_second_crash_fallback_then_grace(): ...
def test_unknown_close_is_idempotent_and_shutdown_fires_once(): ...
```

- [ ] **Step 2: Run RED focused test**

Run:

```bash
python -m pytest -q tools/tool-hub/tests/test_web_launch_diagnostics.py
```

Expected: FAIL because `tool_hub.browser_lifecycle` / `BrowserLeaseManager` does not exist.

- [ ] **Step 3: Implement `BrowserLeaseManager` minimally**

Create `tools/tool-hub/src/tool_hub/browser_lifecycle.py` with:

```python
from __future__ import annotations

import threading
import time
from collections.abc import Callable


class BrowserLeaseManager:
    def __init__(
        self,
        shutdown_callback: Callable[[], None],
        *,
        clock: Callable[[], float] = time.monotonic,
        timer_factory: Callable[[float, Callable[[], None]], object] = threading.Timer,
        heartbeat_ttl: float = 300.0,
        shutdown_grace: float = 2.0,
    ) -> None:
        if heartbeat_ttl <= shutdown_grace or shutdown_grace <= 0:
            raise ValueError("browser lease timing is invalid")
        self._shutdown_callback = shutdown_callback
        self._clock = clock
        self._timer_factory = timer_factory
        self._heartbeat_ttl = heartbeat_ttl
        self._shutdown_grace = shutdown_grace
        self._leases: dict[str, float] = {}
        self._armed = False
        self._zero_since: float | None = None
        self._shutdown_requested = False
        self._timer = None
        self._lock = threading.RLock()

    @property
    def armed(self) -> bool: ...

    @property
    def live_count(self) -> int: ...

    def open(self, lease_id: str) -> None:
        self._touch(lease_id)

    def heartbeat(self, lease_id: str) -> None:
        self._touch(lease_id)

    def close(self, lease_id: str) -> None: ...

    def stop(self) -> None: ...
```

Implementation rules:
- `open`/`heartbeat` set `armed=True`, update `last_seen`, clear `_zero_since`, cancel the pending timer, then schedule the earliest stale deadline.
- `close` removes only that lease. If others remain, reschedule their earliest stale deadline. If the final lease disappears after arming, set `_zero_since=clock()` and schedule exactly `shutdown_grace`.
- Timer callback removes leases with `now - last_seen >= heartbeat_ttl`. If leases remain, reschedule the earliest expiry. If none remain, start/continue the grace window. Once grace elapses, set `_shutdown_requested=True` under the lock and invoke `shutdown_callback()` once outside the lock.
- `stop()` cancels the timer and makes later timer callbacks harmless; it does not call the shutdown callback.
- Any new `open`/`heartbeat` during grace cancels pending shutdown as long as `_shutdown_requested` has not already fired.

- [ ] **Step 4: Run manager tests GREEN**

```bash
python -m pytest -q tools/tool-hub/tests/test_web_launch_diagnostics.py
```

Expected: all manager tests and the existing launch-diagnostic test PASS.

- [ ] **Step 5: Commit Task 1**

Commit message:

```text
feat(tool-hub): add browser lease lifecycle manager
```

---

### Task 2: Bind leases to the reviewed FastAPI shutdown path

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Modify/Test: `tools/tool-hub/tests/test_web_launch_diagnostics.py`

**Interfaces:**
- Consumes: `BrowserLeaseManager` from Task 1.
- Produces API payload model `BrowserLeasePayload` with exact lowercase UUID pattern.
- Produces endpoints `POST /api/browser-lease/open`, `/heartbeat`, `/close`.
- Produces one internal `request_hub_shutdown()` closure shared by manual and lease-triggered shutdown.

- [ ] **Step 1: Add RED API/security tests**

Add focused tests that construct `create_app(..., test_mode=True, shutdown_callback=...)`, bootstrap `/api/config`, and verify:

```python
def test_browser_lease_mutations_require_existing_origin_session_and_csrf(): ...
def test_browser_lease_payload_rejects_non_uuid_and_extra_fields(): ...
def test_browser_lease_open_heartbeat_and_close_are_idempotent(): ...
def test_explicit_shutdown_still_uses_immediate_reviewed_shutdown_path(): ...
```

Assertions:
- POST before config/session or without exact Origin/CSRF returns 403.
- `lease_id="not-a-uuid"` and extra fields return 422.
- `open` returns `{"state": "OPEN"}`; `heartbeat` returns `{"state": "ALIVE"}`; duplicate/unknown `close` returns `{"state": "CLOSED"}`.
- `app.state.browser_leases.live_count` reflects open/close.
- explicit `/api/shutdown` calls the injected shutdown callback immediately and does not wait for lease grace.

- [ ] **Step 2: Run API RED**

```bash
python -m pytest -q tools/tool-hub/tests/test_web_launch_diagnostics.py
```

Expected: FAIL because lease routes/state are not wired.

- [ ] **Step 3: Wire manager and endpoints in `app.py`**

Add:

```python
from .browser_lifecycle import BrowserLeaseManager

class BrowserLeasePayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    lease_id: str = Field(pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$")
```

After `launcher` exists, centralize shutdown:

```python
def request_hub_shutdown() -> None:
    launcher.stop_all()
    if shutdown_callback is not None:
        shutdown_callback()

browser_leases = BrowserLeaseManager(request_hub_shutdown)
```

Set `app.state.browser_leases = browser_leases`. In lifespan `finally`, call `browser_leases.stop()` before `launcher.stop_all()`.

Add routes before the static mount:

```python
@app.post("/api/browser-lease/open")
def open_browser_lease(payload: BrowserLeasePayload) -> dict[str, str]:
    browser_leases.open(payload.lease_id)
    return {"state": "OPEN"}

@app.post("/api/browser-lease/heartbeat")
def heartbeat_browser_lease(payload: BrowserLeasePayload) -> dict[str, str]:
    browser_leases.heartbeat(payload.lease_id)
    return {"state": "ALIVE"}

@app.post("/api/browser-lease/close")
def close_browser_lease(payload: BrowserLeasePayload) -> dict[str, str]:
    browser_leases.close(payload.lease_id)
    return {"state": "CLOSED"}
```

Change explicit `/api/shutdown` to:

```python
browser_leases.stop()
request_hub_shutdown()
return {"state": "SHUTTING_DOWN"}
```

Do not change `security.py`; existing `/api/*` POST middleware must protect the lease endpoints automatically.

- [ ] **Step 4: Run focused API/manager tests GREEN**

```bash
python -m pytest -q tools/tool-hub/tests/test_web_launch_diagnostics.py
python -m pytest -q tools/tool-hub/tests/test_api.py::test_launcher_status_is_token_bound_and_shutdown_is_csrf_protected
```

Expected: PASS.

- [ ] **Step 5: Commit Task 2**

Commit message:

```text
feat(tool-hub): bind browser leases to reviewed shutdown
```

---

### Task 3: Make the browser tab own the Hub lease

**Files:**
- Modify: `tools/tool-hub/web/app.js`
- Modify/Test: `tools/tool-hub/tests/test_web_launch_diagnostics.py`
- Modify: `tools/tool-hub/README.md`

**Interfaces:**
- Consumes the three Task 2 endpoints and current `state.csrf`.
- Produces `openBrowserLease()`, `closeBrowserLease()`, 30-second heartbeat, `pagehide` release, and `pageshow` bfcache recovery.

- [ ] **Step 1: Add RED browser source-contract tests**

Add assertions equivalent to:

```python
def test_web_registers_uuid_lease_and_30_second_heartbeat():
    source = APP_JS.read_text(encoding="utf-8")
    assert "crypto.randomUUID()" in source
    assert 'api("/api/browser-lease/open"' in source
    assert 'api("/api/browser-lease/heartbeat"' in source
    assert "30000" in source


def test_pagehide_releases_with_keepalive_not_direct_shutdown():
    source = APP_JS.read_text(encoding="utf-8")
    assert 'addEventListener("pagehide"' in source
    assert '"/api/browser-lease/close"' in source
    assert "keepalive: true" in source
    assert '"X-Hub-CSRF": state.csrf' in source
    pagehide_block = source[source.index('addEventListener("pagehide"'):]
    assert 'api("/api/shutdown"' not in pagehide_block


def test_browser_lease_code_does_not_store_sensitive_credentials():
    source = APP_JS.read_text(encoding="utf-8")
    assert "OPENAI_API_KEY" not in source
    assert "BASE_TOOL_HUB_LAUNCHER_TOKEN" not in source
    assert "git_executable" not in source
```

Also assert `pageshow` with `event.persisted` reopens a lease for bfcache recovery.

- [ ] **Step 2: Run web RED**

```bash
python -m pytest -q tools/tool-hub/tests/test_web_launch_diagnostics.py
```

Expected: web lifecycle tests FAIL while server tests remain PASS.

- [ ] **Step 3: Implement browser lease lifecycle in `app.js`**

Extend state:

```javascript
const state = {
  csrf: "",
  catalog: null,
  projectId: null,
  windowsLauncherState: "UNKNOWN",
  browserLeaseId: null,
  browserLeaseTimer: null,
};
```

Implement:

```javascript
async function openBrowserLease() {
  if (state.browserLeaseId) return;
  if (!globalThis.crypto?.randomUUID) throw new Error("BROWSER_LEASE_UUID_UNAVAILABLE");
  const leaseId = crypto.randomUUID();
  await api("/api/browser-lease/open", {
    method: "POST",
    body: JSON.stringify({ lease_id: leaseId }),
  });
  state.browserLeaseId = leaseId;
  state.browserLeaseTimer = window.setInterval(() => {
    if (!state.browserLeaseId) return;
    api("/api/browser-lease/heartbeat", {
      method: "POST",
      body: JSON.stringify({ lease_id: state.browserLeaseId }),
    }).catch(() => {});
  }, 30000);
}

function closeBrowserLease() {
  const leaseId = state.browserLeaseId;
  if (!leaseId) return;
  if (state.browserLeaseTimer !== null) window.clearInterval(state.browserLeaseTimer);
  state.browserLeaseTimer = null;
  state.browserLeaseId = null;
  fetch("/api/browser-lease/close", {
    method: "POST",
    keepalive: true,
    headers: { "Content-Type": "application/json", "X-Hub-CSRF": state.csrf },
    body: JSON.stringify({ lease_id: leaseId }),
  }).catch(() => {});
}
```

Register:

```javascript
window.addEventListener("pagehide", closeBrowserLease);
window.addEventListener("pageshow", event => {
  if (event.persisted && state.csrf) openBrowserLease().catch(error => show(error.message, true));
});
```

In the existing `/api/config` initialization, set CSRF first, then `await openBrowserLease()`, then `await refresh()`.

- [ ] **Step 4: Update operator documentation**

In `tools/tool-hub/README.md`, replace the normal-use instruction that requires `Tool Hub 종료` with the new behavior:
- closing the final Tool Hub browser tab normally stops Hub-owned Studio children and the Hub after a short grace;
- refresh/multiple tabs are protected by leases;
- explicit `Tool Hub 종료` remains immediate fallback;
- browser crash may wait for conservative stale timeout;
- shutdown never runs Git operations or kills Figma/unrelated processes.

- [ ] **Step 5: Run full focused and existing Tool Hub tests**

```bash
python -m pytest -q tools/tool-hub/tests/test_web_launch_diagnostics.py
python -m pytest -q tools/tool-hub/tests/test_api.py
python -m pytest -q tools/tool-hub/tests/test_windows_launcher_self_repair.py
```

Expected: PASS.

- [ ] **Step 6: Commit Task 3**

Commit message:

```text
feat(tool-hub): auto stop Hub when final browser tab closes
```

---

### Task 4: PR gates, merge, and live Windows IRG

**Files:**
- No additional production files unless verification exposes a defect.
- Update the PR body/evidence only.

**Interfaces:**
- Consumes Tasks 1-3 exact head.
- Produces merged Base `main` plus user-PC lifecycle evidence.

- [ ] **Step 1: Open one dedicated draft PR from the implementation branch**

PR body must record:
- approved design path;
- RED head and exact failing assertions;
- GREEN head;
- changed-file list;
- evidence ceiling: user-PC close/child/port/Fetch-Pull still `NOT_RUN` until observed.

- [ ] **Step 2: Verify exact-head CI**

Required observations before Ready:
- `Validate Tool Hub Subscription Contracts`: Ubuntu + Windows focused PASS. This workflow already executes `tools/tool-hub/tests/test_web_launch_diagnostics.py`; do not modify the workflow.
- `Validate Base v9 Operating Contracts`: base-v9 + adversarial PASS.
- `Validate Game Project Operating System`: docs, Ubuntu contract, publication, Windows publication smoke, Windows Tool Hub import/catalog smoke, final `ci-gate` PASS.
- Figma exhaustive workflow failures/timeouts, if any, must be classified separately and must not be misreported as lifecycle PASS.

- [ ] **Step 3: Static adversarial diff review**

Confirm:
- only browser lifecycle, app wiring, web lifecycle tests/UI, README, design/plan files changed;
- no project/Figma route/Studio behavior changed;
- no arbitrary process enumeration/kill code;
- no Git mutation code;
- no provider/launcher credentials in browser payloads;
- unresolved review threads = 0;
- PR base still equals current completed `main`; if `main` advanced, rebase only this PR onto the new completed main and rerun exact-head gates.

- [ ] **Step 4: Ready and squash merge with expected head SHA**

Only merge the exact fully verified head. Then confirm the merge SHA is the new Base `main` and observe postmerge Tool Hub Subscription + Windows GPO smoke before claiming cloud completion.

- [ ] **Step 5: User-PC lifecycle IRG**

After the user pulls the merged Base main:

```text
desktop Base Tool Hub
→ open Urban Legend
→ launch Character Studio
→ close only the Tool Hub browser tab (do not press Tool Hub 종료)
→ wait ~3 seconds
→ verify 127.0.0.1:8764 is gone / desktop shortcut starts a fresh Hub
→ verify Character Studio child is no longer running/healthy
→ verify no console window appeared
→ immediately GitHub Desktop Fetch/Pull
→ verify prior stale-Hub lag is not reproduced
```

If any live step fails, keep `AUTO_SHUTDOWN_USER_PC = FAIL/NOT_RUN` and debug from that exact layer; do not promote CI to live PASS.

- [ ] **Step 6: Resume the original live IRG**

Once auto-shutdown passes, reopen Tool Hub and continue:

```text
Character Studio live launch
→ approved anchor
→ Figma Bridge pairing
→ real delivery
→ FIGMA_DELIVERED_VERIFIED
→ Figma node readback
```
