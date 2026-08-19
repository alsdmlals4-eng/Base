# P06 · Godot, Runtime & Technical Toolchain — Optimization Audit

```yaml
part_id: P06
baseline_sha: df8ef644d30fc96456da23a5157e5efb61b620bb
branch: opt/base-part-P06-runtime-authority-clarity
pr: 536
scope: P06_OWNED_ONLY
review_date: 2026-08-19
```

## 1. P06 responsibility map

P06 owns the Base specialization view for Godot authoring/runtime/debugging, Godot-specific addon and tool evaluation, retained Godot runtime-adapter evidence, QA technical tooling, and local execution-environment boundaries. It does not own gameplay acceptance, visual-quality authority, release/platform verdicts, Skill Registry/control-plane policy, or another Part's project canon.

```text
inputs
  current project Godot code/scenes/resources/addons
  P04 gameplay acceptance criteria
  P05 visual/UX acceptance inputs
  P07 release/device validation requirements
  CP0 authority/routing policy
  approved external Godot tools and official sources

P06 processing
  authoring-authority selection and risk gates
  runtime failure diagnosis
  addon/plugin/tool evaluation
  retained adapter/security/evidence review
  Godot-focused regression and runtime evidence classification
  QA/local technical-tool boundary checks

outputs
  safe Godot authoring/tool route
  runtime diagnosis and bounded remediation evidence
  addon/tool adoption disposition
  Godot-focused tests and evidence ceilings
  reusable Godot operational lessons

consumers
  project implementation workflow
  project validation/review workflow
  P07 release validation
  project-specific adoption/third-party records
```

If P06 disappears, Godot writer authority becomes ambiguous, runtime PASS can be overclaimed from static/process evidence, addon/tool duplication pressure returns, and Godot-specific runtime/evidence safeguards lose a dedicated owner.

## 2. Important rule audit

| Rule | Canonical source | Purpose / consumer | Tests | Finding / disposition |
|---|---|---|---|---|
| Single persistent Godot authoring authority | `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md` | Prevent two MCP/Editor/CLI writers from mutating the same project; consumed by project Godot operating route | `test_higodot_single_authority_policy.py`, `test_godot_higodot_gut_hera_toolchain.py` | KEEP. HiGodot remains the current writer authority when adopted. |
| Existing Solution First | P06 evaluation Skill + HiGodot policy | Search current project/Base/local refs/official upstream before building new Godot tooling | Godot addon/toolchain tests | KEEP. No new Skill or writer was justified. |
| Actual runtime evidence before runtime PASS | HiGodot policy + retained adapter evidence contracts | Prevent static schema, process existence, connection, or one pilot from becoming runtime/release proof | Godot runtime/adapter tests | KEEP. Historical adapter docs now explicitly preserve evidence ceilings without claiming current authority. |
| GUT is deterministic GDScript test authority only when adopted | HiGodot policy | Avoid duplicate canonical GDScript suites and floating incompatible versions | `test_godot_higodot_gut_hera_toolchain.py` | KEEP. Official upstream still supports the recorded 4.7.x → GUT 9.7.1 mapping as of this review. |
| Hera is bounded live QA/observability, not a second persistent writer | HiGodot policy | Allow runtime QA while protecting single-writer authority and source-delta acceptance | `test_godot_higodot_gut_hera_toolchain.py` | KEEP. Upstream has broader write abilities; Base intentionally restricts its role. |
| Local Godot reference library is reference-only | `docs/knowledge/godot/LOCAL_GODOT_REFERENCE_LIBRARY.md` | Speed discovery without making one Windows path a project dependency or canon | `test_local_godot_reference_library.py` | KEEP. No portability authority inversion found. |
| Retained Base live-editor v1/v2 material is historical/audit evidence only | HiGodot policy + historical adapter docs | Preserve security/rollback/evidence learning without reviving a second writer | `test_godot_live_editor_contract_v2_docs.py`, historical adapter tests | IMPROVE. Baseline legacy docs still used active/current language; fixed in PR #536. |

### Rule conflict found

Baseline `GODOT_LIVE_EDITOR_AUTOMATION_CONTRACT.md` called the v2 surface `활성 v2 권위` while the newer HiGodot policy explicitly classified the old Base adapter/schema/pilot as historical evidence and not the current persistent execution path. Security/readiness/pilot documents also lacked an explicit supersession banner. A reader could therefore choose a stale writer route even though the actual project adapter tests already forbid direct active adoption.

The fix is semantic authority normalization, not evidence deletion:

```text
retained security / identity / stale-state / rollback / evidence knowledge
  KEEP

current active-writer implication in historical docs
  REMOVE

current writer/tool-role authority
  HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md
```

## 3. Skill / Mode audit

### `diagnosing-game-engine-runtime-failures`

```yaml
mode: skill
trigger: engine/runtime behavior does not match expected behavior
responsibility: reproduce exact runtime conditions, isolate smallest failing system, apply minimal fix, revalidate and prevent regression
inputs: exact runtime symptom, relevant logs/scene/node/component/signal/data/state
outputs: bounded root-cause diagnosis, minimal remediation, runtime/regression evidence
status: KEEP
```

Why it stays separate: runtime fault isolation is a different responsibility from deciding whether an addon/tool should exist. It delegates broad refactor/general review rather than duplicating them.

### `evaluating-godot-assets-and-plugins-before-creation`

```yaml
mode: skill
trigger: proposed Godot MCP/addon/plugin/CLI/framework/tool or capability acquisition
responsibility: inventory current solutions, compare upstream options, require consumption/rollback evidence, then decide reuse/absorb/refactor/archive/build-new
inputs: requirement, current project/Base/tool inventory, official/upstream sources
outputs: adoption disposition and validation contract
status: KEEP
```

Why it stays separate: it is a pre-creation/procurement and lifecycle gate, not runtime fault diagnosis.

### Mode conclusion

No new P06 Mode is required. The existing two Skills have materially distinct triggers and outputs. A new `legacy-adapter-history` Skill would add routing/context cost for a responsibility that is adequately represented by historical documents plus focused tests.

## 4. Module audit

| Module | Responsibility | Inputs | Outputs | Main consumers / tests | Disposition |
|---|---|---|---|---|---|
| Godot Authoring Authority | One persistent writer, risk levels, client/network/update boundaries | project need + current tool state | authorized writer route + evidence gates | project Godot route; HiGodot tests | KEEP |
| Runtime Diagnostics | Reproduce/isolate runtime failures without unsupported PASS | runtime symptom/evidence | root cause + minimal remediation + regression | project implementation/review | KEEP |
| Addon / Plugin Evaluation | Existing Solution First, lifecycle/consumer/rollback decision | candidate + current inventory + official source | REUSE/ABSORB/REFACTOR/ARCHIVE/BUILD_NEW disposition | project third-party/addon records | KEEP |
| Editor / Runtime Adapter Evidence | Preserve historical Base adapter security, stale-state, rollback and execution evidence | retained v1/v2 docs/tests/pilots | audit/regression knowledge only | historical tests; current policy extraction | IMPROVE authority labeling; do not reactivate |
| QA Technical Tooling | Capture technical QA/evidence without turning automation into human/release authority | project UX/runtime acceptance inputs | bounded evidence | QA Evidence Studio / project review | PROTECTED_CURRENT_WORK: PR #530 owns active changes |
| Local Execution Environment | Keep PC-specific Godot tools/refs noncanonical and project-isolated | local paths/executables | bounded local availability state | local validation/reference consumers | KEEP |

No split/merge improves cohesion enough to justify new interfaces. The main defect was authority labeling inside the historical adapter-evidence module.

## 5. Material alternatives

### A. Keep baseline unchanged

Rejected. Known authority ambiguity remains and conflicts with the newer single-writer canon.

### B. Minimal historical-status normalization + regression guard — CHOSEN

- mark four retained legacy documents `HISTORICAL_BASE_ADAPTER_REFERENCE_ONLY`
- route current writer/tool roles to `HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`
- rename stale active-authority headings/statements
- preserve unique security, stale-state, approval, rollback, runtime-evidence and Pilot details
- enforce the boundary in `test_godot_live_editor_contract_v2_docs.py`

This has the smallest blast radius, direct rollback, and high audit value.

### C. Delete/archive the legacy docs, schemas, tools and tests now

Rejected. Historical surfaces still have audit/regression consumers and contain unique evidence rules. Destructive retirement before proving consumer 0 would violate the Base legacy-retention and evidence rules.

### D. Rebuild all Godot routing/templates/schemas around a new unified provider-neutral abstraction

Rejected. It would touch CP0/global/template surfaces, recreate infrastructure that current HiGodot/GUT/Hera roles already cover, increase context/interface cost, and create a second abstraction without a measured blocker.

### BETTER_ALTERNATIVE_SEARCH

A fifth option was considered: keep historical files byte-identical and only add a new index/router document. Rejected because direct links/search hits can still land on the stale `활성 v2 권위` text. The authority status must be visible inside each retained document itself.

### LONG_TERM_PLAN_FIT_REQUIRED

B fits the long-term plan because Base retains reusable evidence knowledge while presenting exactly one current persistent writer route. It also avoids forcing all historical implementation detail into the active policy.

Trade-off: the repository continues to carry legacy implementation/test surface, so maintenance cost is not zero. This is intentional until actual consumers reach zero or a future migration proves the knowledge has been safely absorbed elsewhere.

## 6. Current source / benchmark review

Primary-source checks on 2026-08-19:

- Godot Foundation release material: Godot 4.7.1 remains the stable 4.7 maintenance release; 4.7.2 is still represented as a release candidate in the checked official material. `ADOPT`: continue exact project-version verification rather than floating latest.
- `bitwes/Gut`: current upstream still exposes GUT 9.7.1 for the Godot 4.7 line. `ADOPT`: keep the existing compatibility gate and exact-pin requirement.
- `hi-godot/godot-ai`: current upstream remains an active Godot MCP/editor integration with broad inspect/create/modify/test/runtime capabilities. `ADAPT`: keep using it as the single persistent writer when adopted, but preserve Base-specific risk, client-isolation, local-transport and rollback gates.
- `NotNull92/hera-agent-godot`: upstream provides live editor/runtime QA and also broader mutation surfaces. `ADAPT`: Base keeps the intentionally narrower `LIVE_QA_AND_OBSERVABILITY_ONLY` role and source-delta `NONE` acceptance gate.

No source justified a new P06 Skill, second writer, or broad provider migration.

## 7. Protected concurrent work

Open PR #530 changes `tools/qa-evidence-studio/**`. Those files are read-only in this P06 branch. This audit does not copy, modify, rebase, merge, close, or absorb PR #530.

Other P01/P02/P03/P04/P05/P08/P09 partition PRs are also concurrent read-only work. This branch modifies only P06-owned/allowed paths.

## 8. Adversarial full-loop record

### Loop 1 — authority and canon attack

Found a valid MUST_FIX: historical Base adapter docs still presented v2 as active/current while current HiGodot canon said historical only. Added a failing regression contract first, observed exact-head RED, then normalized the four docs.

### Loop 2 — destructive cleanup / duplicate-surface attack

Attacked the choice to retain legacy docs/tools. Deletion did not survive evidence review because unique stale-state/approval/rollback/evidence logic and regression consumers remain. No destructive cleanup performed.

### Loop 3 — tool/Skill/context-cost attack

Checked whether P06 has duplicate Skills/Modes or needs a new history/toolchain Skill. The two owned Skills have distinct responsibilities; a new Skill would add routing pressure. QA Evidence Studio changes are protected by PR #530 and were not absorbed.

### Loop 4 — source freshness and alternative-provider attack

Rechecked current Godot, GUT, HiGodot and Hera primary/upstream sources. No evidence justified replacing the current author→test→live-QA division. Current stable/compatibility signals remain consistent with the Base policy's bounded claims.

### Loop 5 — ownership, consumer, evidence and regression attack

Rechecked P06 write paths, direct consumers/tests, local-reference portability, unrun runtime evidence, and the chosen patch. No new P06-owned MUST_FIX was found after the authority fix. Current GitHub CI must remain green on the final exact head; actual user-PC Godot execution remains separate evidence and is not inferred from repository CI.

```yaml
full_loops_performed: 5
new_valid_must_fix_after_loop_5: 0
blocking_p06_owned_finding: 0
canonical_conflict: 0_after_patch
ownership_conflict: 0_for_changed_paths
unsupported_pass_claim: 0
clean_review_exit: CONDITIONAL_ON_FINAL_HEAD_VALIDATION_AND_READBACK
```

## 9. Validation contract

Required before merge:

```text
python tools/check_base_partition_scope.py --part P06 --base df8ef644d30fc96456da23a5157e5efb61b620bb --head HEAD
python -m unittest discover -s tests -p 'test_godot_*.py' -v
exact-head required GitHub Actions GREEN
unresolved review threads = 0
changed paths remain P06-owned/allowed
Notion P06 readback complete
```

TDD evidence:

```yaml
red_commit: 6481375f2d75223e25d84533955f3fdac24df44e
red_result: EXPECTED_FAIL
red_failures: 5
red_skipped: 1
red_reason: four documents lacked historical marker/current-authority route and automation contract retained active-v2 heading
green_contract_run: 32223186130
green_contract_result: PASS
```

The skipped actual Godot editor transaction pilot requires an exact `GODOT_BIN`; it remains `SKIPPED_NOT_CONFIGURED` in repository CI and is not converted to runtime PASS by this audit.

## 10. Cross-Part / CP0 boundary

No blocking CP0 edit is required for the chosen fix. Global schema/template retention is already guarded by tests that forbid direct historical-adapter adoption. A future full retirement of those surfaces must be coordinated only after consumer/reference count reaches zero and unique security/evidence knowledge has an approved destination.

No `CROSS_PART_CHANGE_REQUEST` is emitted for a speculative cleanup.

## 11. Rollback and revisit

Rollback: revert PR #536. The change is documentation/test/learning-only and does not migrate product data, project scenes, addons, or runtime configuration.

Revisit when:

- Godot major/minor support baseline changes;
- HiGodot authoring-authority policy changes or upstream becomes unsuitable;
- GUT compatibility mapping changes;
- Hera's accepted role/security boundary changes;
- PR #530 resolves QA Evidence Studio retirement/absorption and P06 can re-evaluate the remaining QA technical-tooling surface;
- historical Base adapter consumers reach zero and CP0/P06 can prove safe retirement.
