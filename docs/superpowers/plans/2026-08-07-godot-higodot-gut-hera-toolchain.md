# HiGodot + GUT + Hera Godot Toolchain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development when subagent dispatch is available, otherwise use superpowers:executing-plans and execute this plan task-by-task with review checkpoints.

**Goal:** Extend Base so adopted Godot product projects can use HiGodot for persistent authoring, GUT for deterministic GDScript tests, and Hera Agent Godot CLI for live runtime QA without creating duplicate mutation authority, duplicate test authority, blanket addon installation, or unverifiable readiness claims.

**Architecture:** Preserve `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` as the canonical Godot automation policy. Extend the existing addon evaluation and project-operating owners plus the installed `godot-live-editor-operations` thin Skill. HiGodot remains the only persistent editor/source mutation authority; GUT becomes the canonical deterministic GDScript suite only when adopted; Hera is adopted only with `LIVE_QA_AND_OBSERVABILITY_ONLY` role restriction. Project-specific pins and consumption remain project-owned records rather than a new Base-wide addon registry.

**Tech Stack:** Markdown policy and Skill contracts, JSON shared Skill routes, Python 3.12 `unittest`, existing Base reference-freshness/integrity validators, GitHub Actions, Godot/HiGodot/GUT/Hera runtime evidence only in later project adoption work.

## Global Constraints

- Implementation baseline is Base `main@4f98f968a377f7b6a11aafa4fc94d11bddbebedc`; before BUILD, re-read `main` and integrate newer non-conflicting changes if it has advanced.
- Approved design is `docs/superpowers/specs/2026-08-07-godot-higodot-gut-hera-toolchain-design.md` at `a0afc65d07de0f6f9f3c058f8cab9a53bc20d222`.
- Do not add a new ACTIVE Skill or a second central addon registry.
- Do not install HiGodot, GUT, or Hera into every project as part of this Base PR.
- HiGodot remains the sole persistent Godot authoring/editor mutation authority.
- GUT authority is limited to adopted deterministic GDScript project tests; C#/.NET, native SDK, platform sandbox, build, packaging, device, and human validation remain separate.
- Hera persistent Scene/Node/script/project/resource/filesystem mutation is forbidden on the active QA path.
- Hera runtime state mutation such as `game set` or state-changing `call` is `DIAGNOSTIC_ONLY`, cannot satisfy acceptance evidence, and requires restore or restart.
- Hera acceptance QA requires a pre/post tracked-source comparison whose Hera-phase delta is `NONE`.
- Hera Base adoption is localhost-only with shared-token use required; secrets are not committed or copied into evidence.
- GUT version compatibility and Hera CLI/addon pairing use exact pins; floating latest and automatic unreviewed updates remain forbidden.
- Existing HiGodot L0-L3 gates, DeepSeek isolation, rollback, import/parse, diff, regression, and truthful `NOT_RUN` evidence boundaries remain intact.
- No merge to `main` is authorized by this plan. Implementation may be placed in a Draft PR for review.

---

### Task 1: Establish RED contracts for the three-tool authority model

**Files:**
- Create: `tests/test_godot_higodot_gut_hera_toolchain.py`
- Modify: `tests/test_higodot_single_authority_policy.py`
- Modify: `.github/workflows/validate-base-v9-rc.yml`

**Interfaces:**
- Consumes current policy, evaluation Skill, operating-system Skill, installed project Skill, shared route JSON, `START_HERE.md`, and `docs/DOCUMENTATION_MAP.md`.
- Produces a focused static contract that fails until the approved HiGodot/GUT/Hera role separation is propagated.

- [ ] **Step 1: Add a new focused test module**

The test module must verify at minimum:

```text
HiGodot persistent authoring authority count == 1
GUT adopted deterministic GDScript test authority is declared
GUT does not replace C#/.NET/native/platform tests
GUT exact Godot-compatible pin is required
same GDScript case is not canonical in both GUT and McpTestSuite
Hera role restriction == LIVE_QA_AND_OBSERVABILITY_ONLY
Hera persistent source/editor mutation == forbidden
Hera game set/call diagnostic path cannot be acceptance evidence
Hera CLI/addon pair exact pin is required
Hera localhost/shared-token boundary is declared
Hera acceptance QA requires tracked source delta NONE
blanket three-addon installation is forbidden
INSTALLED_UNUSED remains removal/defer state
shared route exposes GUT/Hera triggers and project adapter roles
START_HERE exposes the HiGodot → GUT → Hera validation route
no new shared Skill ID is introduced
```

Use `Path.read_text`, `json.loads`, and exact marker assertions like the existing policy tests. Do not require a real Godot executable or network service in this static Base test.

- [ ] **Step 2: Update the pre-existing HiGodot test so RED represents the new approved boundary, not the obsolete Hera prohibition**

In `tests/test_higodot_single_authority_policy.py`:

- remove the assertion that `BENCHMARK_REFERENCE_ONLY` must remain the active Hera disposition;
- preserve assertions for HiGodot, `SOLE_GODOT_EXECUTION_AUTHORITY`, `authority_count: 1`, L0-L3 and destructive authoring capabilities;
- require the policy to distinguish `persistent authoring` from non-authoring live QA;
- require the project thin Skill to reject a second persistent mutation authority while allowing bounded GUT/Hera validation roles.

Do not weaken DeepSeek, loopback, exact-pin, rollback, or destructive-operation safety assertions.

- [ ] **Step 3: Wire the focused module into Base v9 required contracts**

Add `tests.test_godot_higodot_gut_hera_toolchain` to the `python -m unittest` list in `.github/workflows/validate-base-v9-rc.yml` immediately after the existing Godot addon/HiGodot policy tests.

- [ ] **Step 4: Run the focused RED set**

Run:

```bash
python -m unittest \
  tests.test_godot_higodot_gut_hera_toolchain \
  tests.test_higodot_single_authority_policy \
  tests.test_godot_addon_utilization_policy \
  tests.test_base_shared_skill_routes \
  -v
```

Expected before policy implementation: assertion failures limited to the newly approved GUT/Hera routing, obsolete `BENCHMARK_REFERENCE_ONLY`, and missing consumer propagation. Syntax, import, JSON parse, and file-not-found errors are not acceptable RED evidence.

- [ ] **Step 5: Commit RED evidence**

```bash
git add tests/test_godot_higodot_gut_hera_toolchain.py tests/test_higodot_single_authority_policy.py .github/workflows/validate-base-v9-rc.yml
git commit -m "test: define HiGodot GUT Hera toolchain contracts"
```

---

### Task 2: Update the canonical Godot policy without weakening HiGodot authority

**Files:**
- Modify: `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`
- Test: `tests/test_godot_higodot_gut_hera_toolchain.py`
- Test: `tests/test_higodot_single_authority_policy.py`

**Interfaces:**
- Consumes the approved design and existing HiGodot L0-L3 contract.
- Produces the canonical cross-tool authority, version, security, QA, and failure-boundary rules.

- [ ] **Step 1: Replace the blanket Hera prohibition with a role-restricted coexistence rule**

Keep the machine-stable HiGodot authority markers, but explicitly define them as persistent Godot authoring/editor mutation authority. Replace the active statement that Hera is `BENCHMARK_REFERENCE_ONLY` with:

```yaml
HiGodot:
  role: SOLE_PERSISTENT_GODOT_AUTHORING_AUTHORITY
  persistent_mutation: allowed_under_L0_L3

GUT:
  role: DETERMINISTIC_GDSCRIPT_TEST_AUTHORITY_WHEN_ADOPTED
  persistent_authoring: false

Hera_Agent_Godot:
  disposition: REUSE
  role_restriction: LIVE_QA_AND_OBSERVABILITY_ONLY
  persistent_source_mutation: forbidden
```

Preserve the prohibition on a second MCP/EditorPlugin/Bridge/CLI persistent mutation authority.

- [ ] **Step 2: Add the GUT compatibility and test-authority boundary**

Document the current verified compatibility candidates as of 2026-08-07:

```text
Godot 4.7.x -> GUT 9.7.1
Godot 4.6.x -> GUT 9.6.1
Godot 4.5.x -> GUT 9.5.0
Godot 4.3.x-4.4.x -> GUT 9.4.0
Godot 4.2.x -> GUT 9.3.0
```

State that the table is a dated benchmark and must be revalidated against the official compatibility matrix on engine/framework upgrade. Require exact version, actual test consumption, and no duplicate canonical GDScript case in HiGodot `McpTestSuite`.

- [ ] **Step 3: Add Hera live-QA security and evidence rules**

Require:

```yaml
hera_cli_addon_pair: EXACT_MATCH_REQUIRED
transport: LOCALHOST_ONLY
shared_token: REQUIRED_FOR_BASE_ADOPTION
secret_recording: FORBIDDEN
persistent_editor_write: FORBIDDEN
acceptance_source_delta: NONE
runtime_mutation_exception: DIAGNOSTIC_ONLY
runtime_mutation_acceptance_evidence: false
restore_or_restart_after_diagnostic_mutation: required
```

Explicitly list allowed live QA categories: status/read-only inspection, run/stop, runtime tree/UI inspect, input/click, assertions, output/diagnostics, screenshots/diff, smoke/QA diagnose, and bounded batches containing only allowed operations.

- [ ] **Step 4: Add the standard verification chain**

Record:

```text
HiGodot author
→ Godot import/parse
→ GUT focused tests
→ GUT regression at package gate
→ snapshot tracked source state
→ Hera live run/input/inspect/assert/diagnostics/screenshot
→ compare tracked source state
→ require Hera-phase delta NONE
→ Git diff
→ adversarial review
```

The chain is conditional: missing/unneeded GUT or Hera remains `DEFERRED`/`NOT_CONFIGURED`, not a reason for blanket installation.

- [ ] **Step 5: Run policy-focused GREEN subset**

Run the same Task 1 focused command. Expected: canonical-policy assertions pass; evaluation/route/operating/project-skill propagation may remain red until later tasks.

- [ ] **Step 6: Commit**

```bash
git add docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md
git commit -m "docs: define Godot author test and live QA authority"
```

---

### Task 3: Extend the existing addon evaluation owner and shared route metadata

**Files:**
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md`
- Modify: `skills/BASE_SHARED_SKILL_ROUTES.json`
- Modify: `tests/test_base_shared_skill_routes.py`

**Interfaces:**
- Consumes Existing Solution First and selective addon lifecycle.
- Produces reusable project adapter roles and trigger discovery for GUT/Hera without creating a new Skill.

- [ ] **Step 1: Extend required project adapter roles**

Add project-owned roles for:

```text
godot_test_framework
gut_exact_version
gut_test_consumption_path
hera_cli_addon_pair
hera_live_qa_consumption_path
hera_source_delta_guard
```

Do not make them globally configured values; they are adapter roles whose actual state remains in each project.

- [ ] **Step 2: Add a focused Godot test/live-QA subsection under selective addon utilization**

The Skill must define:

- GUT evaluation only when testable GDScript product code exists;
- exact Godot-compatible GUT version and real test/CI consumption;
- existing HiGodot `McpTestSuite` tests as migration input, not automatic deletion;
- Hera `REUSE` with `LIVE_QA_AND_OBSERVABILITY_ONLY` restriction;
- Hera CLI/addon exact pair, localhost/shared-token, live-QA consumption, source-delta guard;
- rejection of unrestricted Hera editor write as a second persistent mutation authority;
- no blanket installation.

- [ ] **Step 3: Extend shared route metadata**

In the existing `evaluating-godot-assets-and-plugins-before-creation` route, add trigger tags sufficient for discovery, including:

```text
gut
gdscript-test-framework
hera-agent
live-runtime-qa
source-delta-guard
```

Add the project adapter roles from Step 1. Do not add a third shared Skill entry.

- [ ] **Step 4: Extend shared route tests**

Update `tests/test_base_shared_skill_routes.py` to assert the new tags and roles while retaining the exact two shared Skill IDs already expected.

- [ ] **Step 5: Record the learning decision**

Append a dated 2026-08-07 Learning Log entry covering:

```text
Finding: authoring, deterministic test, and live QA were previously conflated or under-specified.
Decision: HiGodot authoring + GUT GDScript tests + Hera restricted live QA.
Boundary: no blanket install, no second persistent mutation authority, no GUT takeover of non-GDScript tests.
Evidence ceiling: Base static contracts only; actual project installation/runtime remains NOT_RUN.
```

- [ ] **Step 6: Run focused tests**

```bash
python -m unittest \
  tests.test_godot_higodot_gut_hera_toolchain \
  tests.test_godot_addon_utilization_policy \
  tests.test_base_shared_skill_routes \
  -v
```

Expected: evaluation/route assertions GREEN.

- [ ] **Step 7: Commit**

```bash
git add skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md skills/BASE_SHARED_SKILL_ROUTES.json tests/test_base_shared_skill_routes.py
git commit -m "feat: route GUT and Hera through existing Godot evaluation"
```

---

### Task 4: Extend project operating-system adoption and verification

**Files:**
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Test: `tests/test_godot_higodot_gut_hera_toolchain.py`
- Test: `tests/test_game_project_operating_system_structure.py` only if an operating-system-specific assertion is needed by the final implementation.

**Interfaces:**
- Consumes project-owned third-party inventory and existing HiGodot adoption record.
- Produces install/audit/verify rules for optional GUT and Hera adoption without adding a second Base-wide record.

- [ ] **Step 1: Extend required inputs and read order**

Add the GUT/Hera adapter roles from Task 3 and require third-party inventory inspection alongside `HIGODOT_ADOPTION_RECORD.json` when the project has adopted those tools.

- [ ] **Step 2: Add the three-tool adoption contract**

Keep HiGodot in `HIGODOT_ADOPTION_RECORD.json`. Record GUT and Hera in the project's existing third-party/addon inventory with exact version, source, license, state, consumption, owner boundary, validation, and rollback/removal.

Install/verify rules:

```text
HiGodot required for AI persistent authoring tasks
GUT required only when adopted for deterministic GDScript tests
Hera required only when adopted for live runtime QA
missing optional tool -> DEFERRED/NOT_CONFIGURED
installed without consumption -> INSTALLED_UNUSED
Hera unrestricted editor mutation -> blocking duplicate authority
Hera restricted live QA -> allowed coexistence
```

- [ ] **Step 3: Correct legacy-reconciliation wording**

Replace any rule that treats mere Hera presence as a legacy conflict. The conflict is Hera acting as a persistent mutation authority, unrestricted writer, or duplicate authoring path. Restricted `LIVE_QA_AND_OBSERVABILITY_ONLY` adoption is not legacy by itself.

- [ ] **Step 4: Run focused operating tests**

```bash
python -m unittest \
  tests.test_godot_higodot_gut_hera_toolchain \
  tests.test_game_project_operating_system_structure \
  -v
```

- [ ] **Step 5: Commit**

```bash
git add skills/managing-game-project-operating-system/SKILL.md tests/test_game_project_operating_system_structure.py
git commit -m "docs: govern GUT and Hera project adoption"
```

If `tests/test_game_project_operating_system_structure.py` does not require a semantic change after RED/GREEN evaluation, leave it untouched and commit only the Skill.

---

### Task 5: Make the installed Godot Skill execute the staged author-test-live-QA workflow

**Files:**
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Test: `tests/test_godot_higodot_gut_hera_toolchain.py`
- Test: `tests/test_higodot_single_authority_policy.py`

**Interfaces:**
- Consumes the canonical policy and project adoption state.
- Produces the operational sequence used by Codex/GPT in an installed project.

- [ ] **Step 1: Preserve HiGodot authoring modes and add validation stages**

Keep `bootstrap`, `observe`, `mutate`, `validate`, `resume`, and `recover`. Add explicit deterministic-test and live-QA stage routing without converting GUT or Hera into a second authoring mode.

The core sequence must be discoverable as:

```text
HiGodot author
→ GUT deterministic GDScript test when adopted/required
→ Hera live QA when adopted/required
→ source-delta guard
→ review
```

- [ ] **Step 2: Add conditional bootstrap checks**

For an adopted GUT, verify exact version and Godot compatibility. For an adopted Hera, verify exact CLI/addon pair, localhost/shared token, project/instance readiness, and live-QA consumption. Optional tools that are not needed for the current project stage must not block authoring.

- [ ] **Step 3: Add Hera allowed/forbidden operation boundary**

Allowed: read-only inspect, run/stop, runtime inspect, input/click, assertions, diagnostics/output, screenshot/diff, smoke/QA diagnose.

Forbidden in acceptance QA: persistent scene/node/script/project/resource/filesystem write, state-changing editor eval, or any other operation that duplicates HiGodot authoring.

Runtime mutation exception must be marked `DIAGNOSTIC_ONLY`, followed by restore/restart, and excluded from acceptance evidence.

- [ ] **Step 4: Add source-delta guard**

The Skill must require a tracked-source fingerprint/diff snapshot immediately before the Hera acceptance phase and compare it immediately after. Any newly introduced tracked source delta during Hera QA is a failure and routes back to investigation; it is never silently accepted as a Hera-authored product change.

- [ ] **Step 5: Update output contract**

Add fields for GUT status/version/test result and Hera status/version pair/live-QA/source-delta state while preserving HiGodot provider, operation level, rollback, import/parse, tests, runtime, human, unverified, and production readiness fields.

- [ ] **Step 6: Run focused tests**

```bash
python -m unittest \
  tests.test_godot_higodot_gut_hera_toolchain \
  tests.test_higodot_single_authority_policy \
  -v
```

Expected: all role and operational-boundary assertions GREEN.

- [ ] **Step 7: Commit**

```bash
git add templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md
git commit -m "feat: stage Godot author test and live QA operations"
```

---

### Task 6: Propagate one-step discovery without duplicating the canonical policy

**Files:**
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/superpowers/specs/2026-08-07-godot-higodot-gut-hera-toolchain-design.md`
- Test: `tests/test_godot_higodot_gut_hera_toolchain.py`

**Interfaces:**
- Consumes canonical policy path and thin project Skill path.
- Produces cold-start discovery and truthful lifecycle state.

- [ ] **Step 1: Update START_HERE Godot route**

Keep the canonical policy as the first Godot automation authority and summarize the staged route as:

```text
persistent authoring -> HiGodot
adopted deterministic GDScript tests -> GUT
adopted live runtime QA -> Hera CLI restricted role
```

Do not copy version tables or full command allowlists into `START_HERE.md`.

- [ ] **Step 2: Update Documentation Map responsibility wording**

Expand the HiGodot policy row so it owns authoring authority plus GUT/Hera coexistence boundaries, exact pins, live-QA source-delta guard, and validation handoff. Do not create a second canonical Godot toolchain document.

- [ ] **Step 3: Advance the approved design lifecycle**

Update the spec status from written-spec pending review to implementation-approved/implementation-in-progress state based on the user's 2026-08-07 approval. Preserve `merge_authorization: NOT_GRANTED` and `project_installation: NOT_STARTED`.

- [ ] **Step 4: Run discovery tests**

```bash
python -m unittest tests.test_godot_higodot_gut_hera_toolchain -v
```

- [ ] **Step 5: Commit**

```bash
git add START_HERE.md docs/DOCUMENTATION_MAP.md docs/superpowers/specs/2026-08-07-godot-higodot-gut-hera-toolchain-design.md
git commit -m "docs: expose Godot author test live QA workflow"
```

---

### Task 7: Reference-freshness, adversarial regression, and exact-head evidence

**Files:**
- Review all changed files from Tasks 1-6.
- Modify only files required by actual reference-freshness or regression findings.

**Interfaces:**
- Consumes exact implementation diff and current `main`.
- Produces evidence-backed readiness for a Draft PR, not production readiness and not project installation.

- [ ] **Step 1: Re-sync with current main before final validation**

Fetch current `main`. If it differs from `4f98f968a377f7b6a11aafa4fc94d11bddbebedc`, integrate it non-destructively and re-run affected tests before claiming exact-head evidence.

- [ ] **Step 2: Run focused contract regression**

```bash
python -m unittest \
  tests.test_godot_higodot_gut_hera_toolchain \
  tests.test_higodot_single_authority_policy \
  tests.test_godot_addon_utilization_policy \
  tests.test_base_shared_skill_routes \
  tests.test_game_project_operating_system_structure \
  -v
```

- [ ] **Step 3: Run Base-wide local contracts**

```bash
python -m unittest discover -s tests -v
python tools/build_base_v9_artifacts.py --check
python tools/check_skill_system_coverage.py
git diff --check
git fsck --strict
```

Run `python tools/run_local_validation.py --trusted-history-commit 4f98f968a377f7b6a11aafa4fc94d11bddbebedc` only while that commit is still the current trusted main baseline. If main advanced, first integrate the new main and invoke the command with that newly observed immutable main SHA; never pass an invented or floating ref as the trusted-history commit.

- [ ] **Step 4: Run canonical reference freshness with exact branch SHAs**

Use `tools/check_canonical_reference_freshness.py` against `.github/reference-freshness.json` with the actual immutable PR base/head SHAs obtained immediately before the run. The result must show no missing coupled consumer caused by the evaluation Skill, shared routes, operating Skill, project template, or canonical policy changes.

- [ ] **Step 5: Run adversarial review**

Use `running-adversarial-review-and-refinement`:

```text
attack
→ validate-critique
→ refine-approved-findings only for verified MUST_FIX/approved SHOULD_FIX
→ regression-recheck
→ decision-report
```

Mandatory attack lenses:

```text
second persistent authoring authority accidentally reintroduced
Hera read/write surface too broad for live-QA role
Hera diagnostic mutation accidentally accepted as product evidence
source-delta guard absent or placed after an untracked mutation window
GUT version matrix treated as permanent instead of dated/revalidated
GUT duplicates McpTestSuite canonical GDScript cases
GUT overwrites C#/.NET/native/platform test authority
blanket install implied by Base documentation
INSTALLED_UNUSED no longer enforced
secret/shared token copied into repository guidance
DeepSeek or non-loopback HiGodot boundary weakened
new ACTIVE Skill or shared Skill entry accidentally added
untouched START_HERE/Documentation Map/route/test consumer drift
runtime/project-installation claims made without execution evidence
```

- [ ] **Step 6: Create a Draft PR after exact-head static validation**

The PR body must report:

```yaml
approved_design: yes
implementation: complete_or_partial_truthfully
new_active_skill: false
base_policy_static_contracts: PASS_or_actual_failure
reference_freshness: PASS_or_actual_failure
project_addon_installation: NOT_PERFORMED
real_higodot_gut_hera_e2e: NOT_RUN
hera_runtime_qa_on_real_project: NOT_RUN
human_validation: HUMAN_NOT_RUN
production_readiness: false
merge_authorization: NOT_GRANTED
```

Do not merge or auto-merge from this plan.

## Plan Self-Review

```yaml
spec_coverage:
  hiGodot_single_persistent_authoring: covered
  GUT_GDScript_boundary: covered
  non_GDScript_test_preservation: covered
  Hera_live_QA_role_restriction: covered
  Hera_source_delta_guard: covered
  Hera_diagnostic_only_runtime_mutation: covered
  exact_pin_and_upgrade_rules: covered
  localhost_shared_token_boundary: covered
  selective_adoption_and_INSTALLED_UNUSED: covered
  existing_owner_reuse_no_new_skill: covered
  discovery_and_reference_freshness: covered
  adversarial_regression: covered
placeholder_scan: PASS_NO_TODO_TBD_PLACEHOLDERS
interface_consistency: PASS
project_installation: EXCLUDED
merge_authorization: NOT_GRANTED
```

## Implementation Handoff

The written plan is intended for inline execution in this session because no independent subagent dispatcher is available here. Before BUILD, invoke `superpowers:executing-plans`, `superpowers:test-driven-development`, and later `superpowers:verification-before-completion`. Use a fresh implementation branch from the exact plan commit rather than mutating `main` or conflating the documentation branch with the implementation evidence chain.
