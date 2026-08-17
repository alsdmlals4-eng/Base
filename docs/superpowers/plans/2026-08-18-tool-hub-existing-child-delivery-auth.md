# Tool Hub Existing-Child Delivery Authority Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve exact `RUNNING` delivery authority when Tool Hub reuses an already-healthy Studio child, without weakening token, process, project, or Figma boundaries.

**Architecture:** Keep `authorize_delivery_token()` unchanged. Let the existing base `ProcessSupervisor.start()` remain authoritative for liveness/authenticated-health validation, then have the production delivery-aware subclass reacquire the exact key lock and repair only a stale `REGISTERED` state to `RUNNING` when the same child still exists and is alive. Consume the regression in focused Ubuntu/Windows CI. The user-PC postmerge run reuses the existing four PNG candidates; if this final local-tool attempt still fails, stop investing in the full local Tool Hub path and fall back to Figma Bridge-only project image organization.

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
- Create: `tools/tool-hub/tests/test_existing_child_delivery_auth.py`
- Modify: `.github/workflows/validate-tool-hub-subscription-contracts.yml`

**Interfaces:**
- Consumes: `tool_hub.delivery_supervisor.ProcessSupervisor.start()`, `.view()`, `.authorize_delivery_token()`.
- Produces: regression `test_reusing_healthy_child_restores_running_state_and_delivery_authority` and focused CI consumption on Ubuntu/Windows.

- [x] **Step 1: Add the regression before production changes**

The regression constructs one delivery-aware `ProcessSupervisor`, seeds an existing live `expression-studio/coc-fiction` child with a private token and exact authenticated identity, stubs only the localhost health read, and calls `start()` again for the same key.

Assertions:

```python
reused = supervisor.start(*key)

assert reused is identity
assert supervisor.started_process_count == started_before
assert supervisor.view(*key).status == "RUNNING"
assert supervisor.authorize_delivery_token(token) == key
with pytest.raises(LaunchError, match="delivery credential"):
    supervisor.authorize_delivery_token("wrong-token")
```

- [x] **Step 2: Wire the focused workflow to production and regression paths**

Both pull/push path filters now include `supervisor.py`, `delivery_supervisor.py`, the new regression, existing delivery-auth tests, and this spec/plan. The focused Ubuntu/Windows command explicitly executes both delivery-auth test files.

- [x] **Step 3: Commit the RED-only change**

RED head: `cca705a4e650d5e4d4f13b82d6cf2dddcdff1e9f`. Production delivery-supervisor code was unchanged at this head.

- [x] **Step 4: Verify RED in GitHub Actions**

Focused run `32080418145`, Ubuntu:

```text
1 failed, 86 passed
assert 'REGISTERED' == 'RUNNING'
```

The new regression alone failed on the expected stale-state postcondition.

### Task 2: Implement localized state restoration

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/delivery_supervisor.py`
- Test: `tools/tool-hub/tests/test_existing_child_delivery_auth.py`
- Preserve unchanged: `authorize_delivery_token()` accepted states.

**Interfaces:**
- Consumes: successful `super().start(tool_id, project_id)`, which already performed existing-child liveness and authenticated-health validation.
- Produces: after success, reacquire `_locked_key(key)` and restore `REGISTERED -> RUNNING` only when the exact child still exists and `child.process.poll() is None`.

- [x] **Step 1: Make the minimal production change**

Implemented production wrapper:

```python
def start(self, tool_id: str, project_id: str):
    identity = super().start(tool_id, project_id)
    key = (tool_id, project_id)
    with self._locked_key(key):
        child = self._children.get(key)
        state = self._states.get(key)
        if (
            child is not None
            and state is not None
            and state.status == "REGISTERED"
            and child.process.poll() is None
        ):
            self._set_state(key, "RUNNING", url=identity.url)
    return identity
```

This refinement localizes the fix to the delivery-aware production owner rather than widening the generic base supervisor. If a concurrent stop removes or transitions the child before this lock is reacquired, the guard does not overwrite it.

- [x] **Step 2: Verify GREEN on the focused workflow**

Implementation head `63b63d9b610d7c776eb2d821c18c38683faf3ff8`, focused run `32080694518`:
- Ubuntu focused contracts: PASS.
- Windows focused contracts: PASS.
- production-boundary contract: PASS on both.
- new same-child authority regression: PASS.
- existing wrong-token / STOPPING / dead-process contracts remain consumed and PASS.

### Task 3: Run integration gates and adversarial review

**Files:** no additional production files expected.

**Interfaces:**
- Consumes: final exact PR head after documentation alignment.
- Produces: merge-ready evidence with zero unresolved Important/Critical findings.

- [ ] **Step 1: Verify Base and integration workflows on the final exact head**

Require:
- Base v9 `base-v9-contract`: PASS.
- Base v9 `adversarial-gate`: PASS.
- Game Project Operating System docs/Ubuntu/publication/Windows smoke/final `ci-gate`: PASS.
- Confirm Delivery Ubuntu/Windows contracts: PASS when triggered.
- Focused Tool Hub Ubuntu/Windows + production-boundary: PASS.
- Provisional Figma Integration is supplemental; if Windows hits the known 12-minute workflow budget after the relevant Tool Hub delivery tests have passed, record it as a CI budget ceiling rather than inventing a product PASS.

- [ ] **Step 2: Adversarially review the final exact diff**

Check:
1. `REGISTERED` remains unauthorized.
2. State repair occurs only after successful base `start()` authenticated-health validation.
3. The same key lock is reacquired before repair so a completed concurrent stop cannot be overwritten.
4. Existing child identity/token are reused unchanged.
5. No second process or token rotation path was introduced.
6. Wrong/dead/stopping/cross-scope authorization remains fail-closed.
7. No Figma/provider/project authority changed.

Resolve any Important/Critical finding with a new RED→GREEN cycle before merge.

### Task 4: Merge, postmerge, and one final user-PC IRG

**Files:** no additional production changes unless postmerge verification exposes a server-side regression.

- [ ] **Step 1: Mark ready and squash merge with exact-head protection**

Merge only after all required final exact-head gates and review are complete.

- [ ] **Step 2: Verify postmerge main**

Read back merged `delivery_supervisor.py` and focused workflow. Require fresh main push evidence for Base v9, focused Tool Hub Ubuntu/Windows, and GPO final gate.

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
