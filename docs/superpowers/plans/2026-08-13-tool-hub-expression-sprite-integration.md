# Tool Hub Expression/Sprite Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend the already-merged PC-first Tool Hub so it can launch project-bound Expression Studio and Sprite Animation Studio concurrently in no-additional-cost import mode without duplicating QA Evidence Studio or creating a second Hub.

**Architecture:** Keep `tool_hub` from PR #328 as the only user entrypoint and keep all three Studios as independent process/domain owners. Replace the Hub's weak project inspection with one shared descriptor-bound identity preflight, add fixed typed launch specifications for the two visual Studios, give both Studios an environment-only authenticated port-0 startup contract, then generalize the existing QA supervisor to own multiple `(tool_id, project_id)` children. QA Evidence Studio remains unchanged except for shared lifecycle compatibility; Balance & Scenario Lab is a later independent vertical slice.

**Tech Stack:** Python 3.12, FastAPI, Uvicorn, Pydantic v2, JSON Schema 2020-12, browser-native HTML/CSS/JavaScript, pytest, Git.

## Global Constraints

- Exact starting point is `main@3e3f59b1b835f9675f0b8dbc4543a6c69a526c36`, which already contains merged PR #328/#329.
- Reuse `tools/tool-hub/src/tool_hub`; do not retain or recreate the obsolete `base_tool_hub` package, two-tool registry, or second Hub UI.
- Preserve QA Evidence Studio's developer-only PC evidence contract and Android state `DEFERRED_NOT_CONNECTED`.
- Hub launches Expression/Sprite only with `subscription_handoff_import`; paid OpenAI and pinned sprite generation remain explicit direct-operator modes.
- Browser requests select only reviewed `tool_id` and verified `project_id`; they cannot supply argv, interpreter, environment, paths, ports, output roots, or secrets.
- Project/Figma/anchor inputs are read component-by-component without following links and are bound to committed canonical records before child creation.
- Figma remains a review/placement workspace. Hub and Studio delivery packets are not Figma mutation or upload proof.
- POSIX lifecycle is implemented and tested. Windows process-tree ownership and four-process path-with-spaces operation remain `BLOCKED_UNVERIFIED` until a real Windows smoke is run.
- PR #322 changes only Loop Capsule design files and has no planned changed-path intersection.
- No production code is written before its intended test fails.
- Phase 1 trusts the same OS user account and machine administrator. Runtime hashes, no-follow path checks, descriptor binding, and clean environments protect reviewed launch inputs and detect drift through the final launch check. Concurrent Base/Studio runtime edits after that check are unsupported and surfaced in the UI. Separate-user/container/signed read-only runtime hardening is `HARDENED_RUNTIME_DEFERRED`.

---

### Task 1: Absorb Canonical Project and Registry Trust Into the Existing Hub

**Files:**
- Create: `tools/base-tool-contracts/src/base_tool_contracts/trusted_files.py`
- Create: `tools/base-tool-contracts/src/base_tool_contracts/project_identity.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/approved_anchor.py`
- Modify: `tools/base-tool-contracts/src/base_tool_contracts/figma_routing.py`
- Create: `tools/base-tool-contracts/tests/test_project_identity.py`
- Modify: `tools/base-tool-contracts/tests/test_figma_routing.py`
- Modify: `tools/check_project_operating_contract.py`
- Modify: `tools/project_operating_contract.py`
- Modify: `tools/tool-hub/src/tool_hub/projects.py`
- Modify: `tools/tool-hub/tests/test_projects.py`

**Interfaces:**
- Produces: `validate_project_identity(project_root: Path, expected_project_id: str, base_root: Path) -> ProjectIdentityEvidence`.
- Produces: `ProjectIdentityEvidence(project_id, root_fingerprint, adapter_sha256, protected_paths, validator_sha256)`.
- Produces: `ProjectFigmaRegistry.assert_canonical(base_root: Path) -> None`.
- Preserves: `ProjectLocator.register`, `ProjectLocator.resolve`, and public path redaction.

- [x] **Step 1: Add hostile RED tests** proving that untracked adapters, `core.fsmonitor` local config, fake caller `PATH`, untracked/ignored Python shadow modules, symlinked root components, root rename ABA, dirty fixed validator bytes, arbitrary Figma registries, archived routes, dirty/untracked anchor registries, and public absolute-path diagnostics are blocked.

```python
def test_identity_ignores_project_fsmonitor(tmp_path: Path) -> None:
    fixture = project_fixture(tmp_path)
    fixture.install_fsmonitor_marker()
    validate_project_identity(fixture.root, fixture.project_id, BASE_ROOT)
    assert not fixture.marker.exists()

def test_preflight_rejects_noncanonical_figma_registry(locator_fixture) -> None:
    with pytest.raises(ProjectBindingError, match="PROJECT_FIGMA_ROUTING_UNAVAILABLE"):
        locator_fixture.locator.preflight(locator_fixture.attacker_figma_registry)
```

- [x] **Step 2: Run focused tests and verify RED**.

Run:

```bash
PYTHONPATH=tools/base-tool-contracts/src:tools/tool-hub/src .venv/bin/python -m pytest -q \
  tools/base-tool-contracts/tests/test_project_identity.py \
  tools/base-tool-contracts/tests/test_figma_routing.py \
  tools/tool-hub/tests/test_projects.py
```

- [x] **Step 3: Implement descriptor-bound identity validation** by holding the project root directory descriptor for the full check, passing `/proc/self/fd/<fd>` with `pass_fds` to the fixed validator on supported POSIX systems, rejecting unsupported Hub launch platforms before execution, comparing exact adapter SHA before/inside/after validation, and returning only reason codes publicly.

- [x] **Step 4: Isolate the fixed validator runtime** by copying only verified committed checker/module/schema/release-index bytes into an unlinked fd-backed archive, executing Python with `-I -S`, using an absolute trusted Git executable with `core.fsmonitor=false`, `core.hooksPath=/dev/null`, inert filter settings, and rejecting untracked/ignored importable validator modules under the Base validator source roots.

- [x] **Step 5: Make Figma/anchor ownership canonical** using component-safe bounded reads, line-ending-only equality for clean LF/CRLF checkouts, committed-path proof, `ARCHIVED -> ROUTING_ARCHIVED`, and exact Base/project registry path verification.

- [x] **Step 6: Run the focused and operating-contract suites**.

Run:

```bash
PYTHONPATH=tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/base-tool-contracts/tests
PYTHONPATH=tools/base-tool-contracts/src:tools/tool-hub/src .venv/bin/python -m pytest -q tools/tool-hub/tests/test_projects.py
.venv/bin/python -m pytest -q tests/test_v9_1_project_operating_contract.py tests/test_project_base_adapter_v2.py tests/test_project_base_adapter_v2_docs.py
```

- [x] **Step 7: Commit Task 1**.

```bash
git add tools/base-tool-contracts tools/check_project_operating_contract.py tools/project_operating_contract.py tools/tool-hub/src/tool_hub/projects.py tools/tool-hub/tests/test_projects.py
git commit -m "feat: harden Tool Hub project identity"
```

### Task 2: Give Both Visual Studios an Authenticated Port-0 Startup Contract

**Files:**
- Modify: `tools/expression-studio/src/expression_studio/app.py`
- Modify: `tools/expression-studio/src/expression_studio/security.py`
- Modify: `tools/expression-studio/tests/test_app.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/app.py`
- Modify: `tools/sprite-animation-studio/src/sprite_animation_studio/security.py`
- Modify: `tools/sprite-animation-studio/tests/test_app.py`

**Interfaces:**
- Produces: direct operator `--port 1..65535` and Hub-only `--port 0 --startup-file <private-file>`.
- Consumes: `BASE_TOOL_HUB_LAUNCH_NONCE`, `BASE_TOOL_HUB_ADAPTER_SHA256`, and `BASE_TOOL_HUB_ROOT_FINGERPRINT` only from the child environment.
- Produces startup JSON: `{tool_id, project_id, process_id, port, launch_nonce, adapter_sha256, root_fingerprint}`.
- Produces `/api/status` with the same immutable identity plus engine/Figma/anchor hashes.

- [x] **Step 1: Add parser and startup RED tests** for port zero without a private file, startup-file symlink/existing-file rejection, environment-only nonce, exact bound origin from the actual socket port, and direct-port compatibility.

```python
def test_port_zero_requires_private_startup_file() -> None:
    with pytest.raises(SystemExit):
        build_parser().parse_args(required_args() + ["--port", "0"])

def test_hub_identity_is_environment_only(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BASE_TOOL_HUB_LAUNCH_NONCE", "n" * 43)
    assert hub_identity_from_environment().launch_nonce == "n" * 43
```

- [x] **Step 2: Run both Studio app suites independently and verify RED**.

- [x] **Step 3: Implement a shared bounded startup helper consumed by each Studio** that binds `127.0.0.1:0`, computes exact `bind_origin`, writes the report with exclusive no-follow creation, and starts Uvicorn on that already-bound socket descriptor. Direct nonzero ports retain the existing operator path.

- [x] **Step 4: Extend health identity** with environment-provided adapter/root evidence and ensure nonce is never accepted from argv in Hub mode.

- [x] **Step 5: Run both full Studio suites and JavaScript syntax checks**.

```bash
cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest -q
cd tools/sprite-animation-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest -q
node --check tools/expression-studio/web/app.js
node --check tools/sprite-animation-studio/web/app.js
```

- [x] **Step 6: Commit Task 2**.

```bash
git add tools/expression-studio tools/sprite-animation-studio
git commit -m "feat: add Hub startup contract to visual Studios"
```

### Task 3: Add Fixed Expression and Sprite Launch Specifications

**Files:**
- Create: `tools/tool-hub/src/tool_hub/adapters.py`
- Create: `tools/tool-hub/src/tool_hub/environment.py`
- Create: `tools/tool-hub/tests/test_adapters.py`
- Create: `tools/tool-hub/tests/test_environment.py`
- Modify: `tools/TOOL_REGISTRY.json`
- Modify: `tools/validate_tool_registry.py`
- Modify: `tests/test_tool_registry_contract.py`

**Interfaces:**
- Produces: `build_launch_spec(tool: dict[str, object], project: ProjectBinding, context: LaunchContext) -> LaunchSpec`.
- Produces: `LaunchSpec(argv, cwd, env, startup_file, expected_identity)` with immutable tuples/mappings.
- Consumes only reviewed adapters `qa_evidence_studio`, `expression_studio`, `sprite_animation_studio`.

- [x] **Step 1: Add RED tests** proving each tool ID maps to exactly one owner/adapter/capability tuple, visual Studios always receive `--run-mode subscription_handoff_import`, the canonical Figma/anchor paths, and no API key, `CODEX_HOME`, caller flag, output root, or shell fragment.

- [x] **Step 2: Add hostile RED tests** for interpreter outside the Studio environment, owner symlink replacement, registry cross-wire, malicious checkout bytecode, project path with spaces/metacharacters, and startup path replacement.

- [x] **Step 3: Implement clean per-child environments** with only reviewed OS essentials, a private empty mode-0700 `PYTHONPYCACHEPREFIX`, `PYTHONDONTWRITEBYTECODE=1`, Hub identity values, and no provider credentials for import mode.

- [x] **Step 4: Implement fixed launch specs** using only each Studio's reviewed virtual-environment interpreter and module owner, `shell=False` argv arrays, fixed project evidence, canonical registries, and port zero. Runtime hash and descriptor checks are defense-in-depth within the approved local threat model, not a same-account process sandbox.

- [x] **Step 5: Run registry, adapter, and environment suites**.

```bash
PYTHONPATH=tools/tool-hub/src:tools/base-tool-contracts/src .venv/bin/python -m pytest -q \
  tools/tool-hub/tests/test_adapters.py tools/tool-hub/tests/test_environment.py \
  tests/test_tool_registry_contract.py
```

- [x] **Step 6: Commit Task 3**.

```bash
git add tools/tool-hub/src/tool_hub/adapters.py tools/tool-hub/src/tool_hub/environment.py tools/tool-hub/tests tools/TOOL_REGISTRY.json tools/validate_tool_registry.py tests/test_tool_registry_contract.py
git commit -m "feat: add typed visual Studio launch adapters"
```

### Task 4: Generalize the Existing QA Launcher Into a Multi-Tool Supervisor

**Files:**
- Modify: `tools/tool-hub/src/tool_hub/launcher.py`
- Create: `tools/tool-hub/src/tool_hub/supervisor.py`
- Modify: `tools/tool-hub/src/tool_hub/app.py`
- Modify: `tools/tool-hub/tests/test_launcher.py`
- Create: `tools/tool-hub/tests/test_supervisor.py`
- Modify: `tools/tool-hub/tests/test_api.py`

**Interfaces:**
- Produces: `ProcessSupervisor.start(tool_id: str, project_id: str) -> ChildIdentity`.
- Produces: `ProcessSupervisor.stop(tool_id: str, project_id: str) -> ChildPublicView`.
- Produces exact public states `REGISTERED|PREFLIGHT|STARTING|RUNNING|UNHEALTHY|STOPPING|STOPPED|START_FAILED|BLOCKED_*`.
- Preserves: QA launch semantics and existing `/api/tools`, `/api/projects`, `/api/launch` clients.

- [x] **Step 1: Add RED lifecycle tests** for idempotent same-key start, four different `(tool, project)` keys, wrong nonce/PID/hash, stale startup file, child crash, bounded timeout, and stop ownership.

- [x] **Step 2: Add API RED tests** proving Expression/Sprite can launch only when registered and verified, and a blocked visual child cannot affect a running QA child or another project.

- [x] **Step 3: Extract the existing QA lifecycle into `ProcessSupervisor`** with per-key locks, a machine lock, private launch directories, process groups on POSIX, bounded sanitized log tails, exact startup/status identity comparison, and TERM-then-KILL group stop.

- [x] **Step 4: Preserve fail-closed Windows behavior** before child creation until secure Job Object ownership is implemented and proven on a real Windows runner.

- [x] **Step 5: Run all Tool Hub suites**.

```bash
cd tools/tool-hub && PYTHONPATH=src:../base-tool-contracts/src ../../.venv/bin/python -m pytest -q
```

- [x] **Step 6: Commit Task 4**.

```bash
git add tools/tool-hub/src/tool_hub tools/tool-hub/tests
git commit -m "feat: supervise project-bound Studio processes"
```

### Task 5: Update the Single Hub UI and Prove Concurrent Import Workflows

**Files:**
- Modify: `tools/tool-hub/web/index.html`
- Modify: `tools/tool-hub/web/app.js`
- Modify: `tools/tool-hub/web/styles.css`
- Modify: `tools/tool-hub/tests/test_web_contract.py`
- Create: `tools/tool-hub/tests/test_multi_studio_smoke.py`
- Modify: `tools/tool-hub/README.md`
- Modify: `README.md`
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/superpowers/specs/2026-08-12-base-tool-hub-design.md`

**Interfaces:**
- Shows one catalog with QA, Expression, and Sprite status per selected project.
- Opens only server-returned authenticated loopback child URLs.
- Shows `ROUTING_REGISTERED`, `ANCHOR_EVIDENCE_MISSING`, `BLOCKED_UNVERIFIED`, and import-mode cost state without claiming Figma upload or AI generation.

- [x] **Step 1: Add RED web-contract tests** for three reviewed tools, no absolute paths/secrets/raw command controls, textContent-only project labels, independent child states, and truthful blocked status.

- [x] **Step 2: Implement the minimal UI changes** by extending the existing Hub cards; do not add a second page, Tool Radar runtime, marketplace, Balance Lab placeholder, or embedded Studio iframe.

- [x] **Step 3: Add a Linux four-process smoke** using two temporary project fixtures and both visual Studios in import mode. Assert four unique loopback ports, exact project/tool identities, successful Expression candidate import/export packet, successful Sprite action import/export packet, successful Sprite effect-stage import/export packet, zero provider calls, and no cross-project output paths.

- [x] **Step 4: Re-run the existing QA vertical slice** to prove the generalized supervisor did not regress its session/evidence packet flow.

- [x] **Step 5: Update documentation** with the absorbed PR #328/#329 baseline, single-Hub authority, actual Linux evidence, Windows/Android/Figma/provider ceilings, and next independent project `Balance & Scenario Lab`.

- [x] **Step 6: Run full relevant validation**.

```bash
PYTHONPATH=tools/base-tool-contracts/src .venv/bin/python -m pytest -q tools/base-tool-contracts/tests
cd tools/qa-evidence-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest -q
cd tools/expression-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest -q
cd tools/sprite-animation-studio && PYTHONPATH=src ../../.venv/bin/python -m pytest -q
cd tools/tool-hub && PYTHONPATH=src:../base-tool-contracts/src ../../.venv/bin/python -m pytest -q
.venv/bin/python -m pytest -q tests/test_tool_registry_contract.py tests/test_project_base_adapter_v2.py tests/test_v9_1_project_operating_contract.py
node --check tools/tool-hub/web/app.js
git diff --check
```

- [x] **Step 7: Run exact-head adversarial and independent review**. Required result before publish: `P0=0`, `P1=0`, no unresolved review thread, and no claim above the executed Linux/import evidence.

- [x] **Step 8: Commit Task 5**.

```bash
git add tools/tool-hub README.md START_HERE.md docs/DOCUMENTATION_MAP.md docs/superpowers/specs/2026-08-12-base-tool-hub-design.md
git commit -m "docs: complete visual Studio Hub integration"
```

### Task 6: Publish, Check, Merge, and Read Back Exact Main

**Files:**
- Modify only if required by actionable review feedback discovered after push.

- [ ] **Step 1: Rebase onto the exact current `origin/main`** and rerun every Task 5 validation command.
- [ ] **Step 2: Push the feature branch and open a draft PR** describing PR #328/#329 reuse, obsolete duplicate-Hub rejection, actual samples, blocked Windows/Android/Figma/provider states, rollback, and PR #322 path intersection.
- [ ] **Step 3: Inspect every required GitHub check and unresolved review thread**; address only evidence-backed findings on the exact PR head.
- [ ] **Step 4: Run final adversarial review on the exact reviewed head** and require `P0=0 / P1=0`.
- [ ] **Step 5: Merge using the repository-approved method**, fetch the resulting `main`, and verify the merge commit contains the single `tool_hub` package, QA Studio, both typed visual adapters, tests, and documentation.
- [ ] **Step 6: Report exact merge SHA, checks, before/after behavior, sample workflows, deferred Balance Lab, and every unverified platform/provider/Figma claim.**
