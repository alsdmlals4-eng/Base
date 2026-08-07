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

- [x] **Step 1: Add a new focused test module**

The test module verifies HiGodot persistent authoring authority, GUT GDScript scope and version compatibility, Hera live-QA restriction/source-delta/security, shared-route propagation, discovery, and lifecycle state.

- [x] **Step 2: Update the pre-existing HiGodot test so RED represents the new approved boundary, not the obsolete Hera prohibition**

The prior blanket Hera benchmark-only assertion was removed while HiGodot L0-L3, DeepSeek, loopback, exact-pin, rollback, destructive-operation and historical-adapter protections were preserved.

- [x] **Step 3: Wire the focused module into Base v9 required contracts**

`tests.test_godot_higodot_gut_hera_toolchain` is included in `.github/workflows/validate-base-v9-rc.yml`.

- [x] **Step 4: Run the focused RED set**

GitHub Actions RED head: `1af2454ad2f0fcf367838c3fba11361d88348e85`.

Observed evidence:

```yaml
generated_artifacts_and_integrity: PASS
focused_contract_step: FAIL_EXIT_1
policy_implementation_at_red_head: ABSENT
```

The hosted connector did not expose the Python assertion body for that run, so RED evidence is bounded to the successful integrity step followed by focused-contract failure. No syntax/import/JSON failure is claimed.

- [x] **Step 5: Commit RED evidence**

Completed on the implementation branch and Draft PR #209.

---

### Task 2: Update the canonical Godot policy without weakening HiGodot authority

**Files:**
- Modify: `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`
- Test: `tests/test_godot_higodot_gut_hera_toolchain.py`
- Test: `tests/test_higodot_single_authority_policy.py`

- [x] Replace blanket Hera prohibition with `REUSE + LIVE_QA_AND_OBSERVABILITY_ONLY` while preserving one persistent authoring authority.
- [x] Add dated GUT compatibility candidates, exact-version requirement, GDScript scope, and McpTestSuite duplicate-case boundary.
- [x] Add Hera exact pair, localhost/shared-token, allowed live-QA categories, persistent-write prohibition, diagnostic-only runtime mutation, and source-delta `NONE` gate.
- [x] Add the standard HiGodot → import/parse → GUT → Hera → Git/adversarial chain.
- [ ] Exact-head GREEN verification remains pending GitHub Actions completion.

---

### Task 3: Extend the existing addon evaluation owner and shared route metadata

**Files:**
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md`
- Modify: `skills/BASE_SHARED_SKILL_ROUTES.json`
- Modify: `tests/test_base_shared_skill_routes.py`

- [x] Add GUT/Hera project adapter roles.
- [x] Add focused GUT/Hera selective-adoption rules without a new Skill.
- [x] Add `gut`, `gdscript-test-framework`, `hera-agent`, `live-runtime-qa`, and `source-delta-guard` trigger tags.
- [x] Preserve exactly two shared Skill IDs.
- [x] Record the 2026-08-07 learning decision and evidence ceiling.
- [ ] Exact-head GREEN verification remains pending.

---

### Task 4: Extend project operating-system adoption and verification

**Files:**
- Modify: `skills/managing-game-project-operating-system/SKILL.md`

- [x] Extend required inputs/read order for GUT/Hera project-owned adoption state.
- [x] Keep HiGodot in `HIGODOT_ADOPTION_RECORD.json`; keep GUT/Hera in existing third-party inventory.
- [x] Make GUT/Hera optional and consumption-backed; keep `INSTALLED_UNUSED`/`DEFERRED` states.
- [x] Correct legacy reconciliation so restricted Hera presence is not itself a conflict; unrestricted persistent mutation is.
- [x] Extend verify/output/failure conditions.
- [ ] Exact-head GREEN verification remains pending.

---

### Task 5: Make the installed Godot Skill execute the staged author-test-live-QA workflow

**Files:**
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`

- [x] Preserve HiGodot L0-L3 authoring and add `deterministic-test` and `live-qa` validation stages.
- [x] Add conditional GUT/Hera bootstrap checks without making optional tools block unrelated authoring.
- [x] Add Hera acceptance allowlist, persistent-write prohibition, and `DIAGNOSTIC_ONLY` runtime mutation exception.
- [x] Add pre/post tracked source `source-delta NONE` guard.
- [x] Extend output/failure contracts while preserving DeepSeek/loopback/rollback evidence boundaries.
- [ ] Exact-head GREEN verification remains pending.

---

### Task 6: Propagate one-step discovery without duplicating the canonical policy

**Files:**
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/superpowers/specs/2026-08-07-godot-higodot-gut-hera-toolchain-design.md`

- [x] Add one-step HiGodot → GUT → Hera route in `START_HERE.md` without duplicating version tables/allowlists.
- [x] Expand the Documentation Map row so the canonical policy owns GUT/Hera coexistence and source-delta handoff.
- [x] Advance the design to `APPROVED_FOR_IMPLEMENTATION`, `implementation: IN_PROGRESS`, while preserving `project_installation: NOT_STARTED` and `merge_authorization: NOT_GRANTED`.
- [ ] Exact-head discovery GREEN remains pending.

---

### Task 7: Reference-freshness, adversarial regression, and exact-head evidence

- [ ] Re-read current `main` and integrate any new non-conflicting changes before final evidence.
- [ ] Run the focused contract regression on exact head.
- [ ] Run Base-wide local/hosted contract suites and generated-artifact checks.
- [ ] Run canonical reference freshness against exact base/head SHAs.
- [ ] Run adversarial `attack → validate-critique → refine-approved-findings → regression-recheck → decision-report`.
- [ ] Update Draft PR #209 with exact-head evidence and remaining `NOT_RUN` ceilings.
- [ ] Do not merge without fresh explicit user merge authorization.

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
  adversarial_regression: pending_final_review
placeholder_scan: PASS_NO_TODO_TBD_PLACEHOLDERS
interface_consistency: PASS_STATIC_IMPLEMENTATION_PENDING_CI
project_installation: EXCLUDED
merge_authorization: NOT_GRANTED
```

## Implementation Handoff

Implementation is active on `agent/godot-higodot-gut-hera-toolchain-implementation` in Draft PR #209. Base static contracts are implemented; exact-head CI, reference-freshness, adversarial closure, and completion verification remain before the branch can be presented as ready for merge review. Actual project installation and real HiGodot→GUT→Hera runtime E2E remain separate later project-adoption work.
