# Tool Hub Existing-Child Delivery Authority Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve exact `RUNNING` delivery authority when Tool Hub reuses an already-healthy Studio child, without weakening token, process, project, or Figma boundaries.

**Architecture:** Keep `authorize_delivery_token()` unchanged. Repair the existing-child success path in `ProcessSupervisor._start()` so authenticated reuse ends in `RUNNING`, then consume a regression in focused Ubuntu/Windows CI. The user-PC postmerge run reuses the existing four PNG candidates; if this final local-tool attempt still fails, stop investing in the full local Tool Hub path and fall back to Figma Bridge-only project image organization.

**Tech Stack:** Python 3.12, pytest, FastAPI-local Tool Hub, GitHub Actions Ubuntu/Windows matrices.

**Spec:** `docs/superpowers/specs/2026-08-18-tool-hub-existing-child-delivery-auth-design.md`

## Global Constraints

- Existing healthy child reuse must end in exact `RUNNING` state only after authenticated health succeeds.
- Do not authorize `REGISTERED`, `STOPPING`, `UNHEALTHY`, dead-process, wrong-token, wrong-project, or wrong-tool states.
- Do not rotate the existing child delivery token and do not spawn a second Studio process on reuse.
- Do not modify Figma routing, pairing, receipt, provider/API-key, project repository, or Windows Job Object authority.
- Preserve the user's existing four PNG candidates; do not regenerate them for the postmerge IRG.
- Final user rule: if this merged fix still fails in the real user-PC delivery flow, abandon the full local Tool Hub workflow and retain only Figma Bridge-based project image organization.

---

### Task 1: Add a consumed RED regression for existing-child reuse authority

**Files:**
- Modify: `tools/tool-hub/tests/test_studio_delivery_trust.py`
- Modify: `.github/workflows/validate-tool-hub-subscription-contracts.yml`

**Interfaces:**
- Consumes: `tool_hub.delivery_supervisor.ProcessSupervisor.start()`, `.view()`, `.authorize_delivery_token()`.
- Produces: regression `test_reusing_healthy_child_restores_running_state_and_delivery_authority` and focused CI consumption on Ubuntu/Windows.

- [ ] **Step 1: Add the regression before production changes**

Add a test that constructs one `ProcessSupervisor` with a reviewed `expression-studio` tool entry, seeds a live existing child with `_PRIVATE_TOKEN`, sets initial state `RUNNING`, stubs only `_fetch_status()` with the exact authenticated health payload, and calls `start()` again for the same `(tool_id, project_id)`.

The intended assertions are:

```python
reused = supervisor.start(*key)

assert reused is identity
assert supervisor.started_process_count == started_before
assert supervisor.view(*key).status == "RUNNING"
assert supervisor.authorize_delivery_token(token) == key
with pytest.raises(LaunchError, match="delivery credential"):
    supervisor.authorize_delivery_token("wrong-token")
```

The fake child must expose the same fields read by the production existing-child path: `process.pid`, `process.poll()`, `spec.expected_identity`, `spec.env`, `identity`, and `state`.

- [ ] **Step 2: Wire the focused workflow to the production and regression paths**

In both `pull_request.paths` and `push.paths`, add:

```yaml
- "tools/tool-hub/src/tool_hub/supervisor.py"
- "tools/tool-hub/src/tool_hub/delivery_supervisor.py"
- "tools/tool-hub/tests/test_studio_delivery_trust.py"
- "docs/superpowers/specs/2026-08-18-tool-hub-existing-child-delivery-auth-design.md"
- "docs/superpowers/plans/2026-08-18-tool-hub-existing-child-delivery-auth.md"
```

In `Run subscription, routing, and Windows preflight contracts`, add:

```text
tools/tool-hub/tests/test_studio_delivery_trust.py
```

- [ ] **Step 3: Commit the RED-only change**

Commit only the regression, workflow consumption wiring, and this plan/spec documentation. Production `supervisor.py` must remain unchanged on the RED head.

- [ ] **Step 4: Verify RED in GitHub Actions**

Expected focused result on current code: the new regression fails because `ProcessSupervisor._start()` leaves the public state `REGISTERED` after a healthy existing-child reuse. Existing delivery-token fail-closed tests must remain green.

### Task 2: Implement the one-line state restoration

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/supervisor.py` in the existing-child success path of `_start()`.
- Test: `tools/tool-hub/tests/test_studio_delivery_trust.py`

**Interfaces:**
- Consumes: existing authenticated health result already validated by `_matches(...)` and `status.get("status") == "ready"`.
- Produces: `_set_state(key, "RUNNING", url=existing.identity.url)` immediately before returning `existing.identity`.

- [ ] **Step 1: Make the minimal production change**

After the existing child passes liveness and authenticated health checks, insert exactly:

```python
self._set_state(key, "RUNNING", url=existing.identity.url)
return existing.identity
```

Do not change `authorize_delivery_token()`.

- [ ] **Step 2: Verify GREEN on the focused workflow**

Required exact-head evidence:
- Ubuntu focused Tool Hub contracts: PASS.
- Windows focused Tool Hub contracts: PASS.
- `test_reusing_healthy_child_restores_running_state_and_delivery_authority`: PASS.
- Existing wrong-token / STOPPING / dead-process authorization tests: PASS.
- production-boundary contract: PASS.

### Task 3: Run integration gates and adversarial review

**Files:** no new production files expected.

**Interfaces:**
- Consumes: exact PR head from Task 2.
- Produces: merge-ready evidence with zero unresolved important findings.

- [ ] **Step 1: Verify Base and integration workflows on the exact head**

Require:
- Base v9 `base-v9-contract`: PASS.
- Base v9 `adversarial-gate`: PASS.
- Game Project Operating System docs/Ubuntu/publication/Windows smoke/final `ci-gate`: PASS.
- Confirm Delivery Ubuntu/Windows contracts: PASS when triggered.
- Provisional Figma Integration is supplemental; if Windows hits the known 12-minute workflow budget after the relevant Tool Hub delivery tests have passed, record it as a CI budget ceiling rather than inventing a product PASS.

- [ ] **Step 2: Adversarially review the exact diff**

Check:
1. `REGISTERED` remains unauthorized.
2. `RUNNING` is restored only after authenticated health passes.
3. Existing child identity/token are reused unchanged.
4. No second process or token rotation path was introduced.
5. Wrong/dead/stopping/cross-scope authorization remains fail-closed.
6. No Figma/provider/project authority changed.

Resolve any Important/Critical finding with a new RED→GREEN cycle before merge.

### Task 4: Merge, postmerge, and one final user-PC IRG

**Files:** no additional production changes unless postmerge verification exposes a server-side regression.

- [ ] **Step 1: Mark ready and squash merge with exact-head protection**

Merge only after all required exact-head gates and review are complete.

- [ ] **Step 2: Verify postmerge main**

Read back the merged `supervisor.py` and focused workflow. Require fresh main push evidence for Base v9, focused Tool Hub Ubuntu/Windows, and GPO final gate.

- [ ] **Step 3: Run the real user-PC sequence using the four existing PNGs**

1. Update Base to the merged main.
2. Shut down the old Hub/Studio ownership tree using the reviewed Hub shutdown path when possible.
3. Start exactly one fresh Tool Hub instance and one Urban Legend Character Studio child.
4. Recreate only the in-memory Studio run if needed; reuse the existing four PNG files.
5. Import those four PNGs into the fresh same-run handoff, select one, and press `확정 및 전달`.
6. PASS requires advancing beyond `STUDIO_DELIVERY_AUTH_REQUIRED` into a real `PAIRING_REQUIRED`/`BRIDGE_PAIRED` delivery state.
7. Continue Figma Bridge pairing and exact-byte receipt/readback only after that PASS.

- [ ] **Step 4: Apply the user's stop-loss rule**

If the real user-PC delivery path still fails after this merged fix, stop further full Tool Hub repair work in this workflow. Record the failure evidence, preserve the reusable image assets and Figma routing, and switch the operating recommendation to **Figma Bridge-only project image organization** rather than attempting another local-tool repair cycle.
