# P02 · Skill Governance, Canon Freshness & Legacy — Partition Audit

- Part: `P02`
- Baseline main: `df8ef644d30fc96456da23a5157e5efb61b620bb`
- Branch: `opt/base-part-P02-skill-governance-freshness`
- Scope: Skill lifecycle, canonical-reference freshness, Base change proposals, skill-body simplification, stale pruning, legacy retention/retirement
- Protected concurrent work: PR #530 is read-only and is not copied, rebased, merged, closed, or absorbed by this Part.

## 1. What P02 is

P02 is the maintenance view that keeps Base knowledge-governance mechanisms trustworthy without creating a second runtime or a second control plane. Its responsibility chain is:

```text
Skill lifecycle / proposal intake
→ canonical owner and consumer map
→ reference freshness
→ simplify active instructions when justified
→ classify stale material
→ preserve UNIQUE material
→ archive/remove only after consumer and recovery gates
```

If P02 disappeared, Base would still have individual documents and Skills, but there would be no dedicated owner for duplicate Skill authority, stale canonical references, proposal lifecycle, safe pruning, or legacy absorption/removal.

## 2. Important rules audit

| Rule | Canonical source | Purpose / consumer | Tests / evidence | Finding |
|---|---|---|---|---|
| Existing Solution First | `AGENTS.md`, P02 context pack | Prevent duplicate Skills/Modes/tools | Registry/Skill audits | KEEP |
| canonical reference freshness | `skills/auditing-canonical-reference-freshness/SKILL.md`, checker/config | Propagate path/ID/schema/authority changes | `tests/test_reference_freshness.py` | IMPROVE: alias parser false-negative + content-drift remains partly manual |
| no duplicate active Skill authority | Registry + evolution Skill | Keep one active owner per responsibility | skill coverage/integrity tests | KEEP |
| `LEGACY_ABSORB_VERIFY_REMOVE` | legacy-retention Skill + Partition operating model | Preserve UNIQUE material before archive/delete | freshness + legacy/consumer gates | KEEP, but atomic companion ownership is inconsistent |
| `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL` | `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md` | Stop new Sheets authority; migrate UNIQUE legacy material | related contract tests | KEEP; several CP0/P01 consumers remain semantically stale on baseline and PR #530 is already changing them |
| current write authority is fail-closed | Partition Manifest/Operating Model | Prevent a Part from mutating CP0/other Part work | partition scope checker | KEEP; current coupled-change rules conflict with this rule for P02-owned files |

## 3. Skill / Mode audit

| Skill | Responsibility | Modes / key flow | Overlap judgment | Disposition |
|---|---|---|---|---|
| `evolving-project-discipline-skills` | create/consolidate/evolve Skill responsibility | inventory → boundary decision → integrate/create → register → eval → verify → learn | Owns Skill lifecycle; does not replace pruning/freshness | KEEP |
| `auditing-canonical-reference-freshness` | path/ID/schema/consumer propagation and stale-reference detection | impact-map / reference-scan / content-drift / derivative-freshness / propagation-gap / closure-report | Read/verify owner; distinct from destructive retirement | IMPROVE |
| `managing-base-change-proposals` | BCP extract/submit/review/implement/verify | extract → submit → review → implement → verify | Proposal lifecycle, not Skill lifecycle itself | IMPROVE via ownership reconciliation |
| `simplifying-skill-bodies` | progressive disclosure and context reduction without behavior loss | baseline → classify → extract → verify | Active-skill context optimization; not stale deletion | KEEP |
| `pruning-stale-and-nonfunctional-material` | classify dead/duplicate/nonfunctional material | KEEP/MERGE/MOVE/STUB/ARCHIVE/DELETE/UNVERIFIED | Determines stale disposition; legacy Skill owns retention/recovery lifecycle | KEEP |
| `governing-legacy-retention-and-archives` | absorb UNIQUE material, compatibility, archive/delete gates | inventory/classify/reconcile/archive/delete-approved/verify | Distinct from pruning because it owns recovery and destructive gates | IMPROVE via CP0 coupling reconciliation |

### Skill count decision

No new P02 Skill is justified. No pair should be merged at this baseline: the six responsibilities have materially different inputs, outputs, failure modes, or mutation gates. `simplifying` vs `pruning` and `pruning` vs `legacy retention` look adjacent but are not duplicate lifecycle owners.

## 4. Module audit

| Module | Input | Output | Main consumer/test | Disposition |
|---|---|---|---|---|
| Skill Lifecycle Governance | Registry, Skill packages, eval/learning evidence | KEEP/IMPROVE/MERGE/ABSORB/SPLIT/DEPRECATE decisions | Registry/coverage/integrity surfaces | KEEP |
| Canonical Reference Freshness | canonical changes + consumer graph | stale/orphan/propagation findings | checker + reference freshness tests | IMPROVE |
| Base Change Proposal | project lesson + approval evidence | BCP lifecycle state and implementation handoff | `[수정제안서]/PROPOSAL_REGISTRY.json` | IMPROVE ownership |
| Skill Simplification | active Skill body + fixtures/tests | smaller equivalent active contract | skill tests/evals | KEEP |
| Stale Pruning | inventory + consumers + history | disposition packet | freshness/legacy handoff | KEEP |
| Legacy Absorb/Verify/Remove | UNIQUE/DUPLICATE/OBSOLETE classification | migrated authority + archive/delete evidence | consumer/readback/rollback gates | KEEP, improve ownership coupling |

## 5. Confirmed findings

### P02-F01 — BCP canonical path is outside P02 declared write ownership

**Severity:** MUST_FIX at Integration/CP0.

- `skills/managing-base-change-proposals/SKILL.md` uses `[수정제안서]/PROPOSAL_REGISTRY.json` and `[수정제안서]/<proposal-id>/...`.
- The live registry itself declares `proposal_root: "[수정제안서]"` and contains implemented BCP records.
- The P02 Manifest instead grants `proposals/**`; that root does not exist on the baseline.

**Risk:** a literal Part worker either cannot perform its BCP responsibility or creates a second proposal authority.

**Mitigation in this PR:** do not create `proposals/`; preserve the live `[수정제안서]` authority and export CP0 ownership correction.

### P02-F02 — P02-owned freshness checker cannot be changed atomically inside P02

**Severity:** MUST_FIX at Integration/CP0.

`.github/reference-freshness.json` contains `reference-checker-test-and-config-sync`: any change to `tools/check_canonical_reference_freshness.py` requires both `.github/reference-freshness.json` and `tests/test_reference_freshness.py` to change. The checker and test are P02-owned, while `.github/**` is CP0.

**Risk:** every checker bugfix forces an out-of-partition write even when configuration semantics do not change.

**Preferred correction:** make test synchronization mandatory, but require config change only when config schema/keys/semantics actually change. Do not move the whole CP0 config into P02 and do not create a duplicate P02 config.

### P02-F03 — P02-owned legacy Skill is unconditionally coupled to a CP0 route

**Severity:** MUST_FIX at Integration/CP0.

`legacy-retention-shared-skill-sync` requires `skills/BASE_SHARED_SKILL_ROUTES.json` for any non-description-only body change to `governing-legacy-retention-and-archives/SKILL.md`. The Skill body belongs to P02; the shared route belongs to CP0.

**Risk:** internal procedure/evidence changes that do not alter routing still force forbidden CP0 writes.

**Preferred correction:** require package learning/test evidence for body changes; require shared-route mutation only when route identity/trigger/activation semantics actually change.

### P02-F04 — legacy alias parser misses multi-alias table cells

**Severity:** MUST_FIX after F02 is resolved; currently blocked by CP0 atomic-coupling rule.

`parse_legacy_aliases()` matches only a table row whose first cell is exactly one backticked token. The live alias table has first cells containing multiple backticked aliases, including the Grill Me aliases, 좋은 프롬프트 aliases, legacy-retention aliases, and Godot asset-search aliases.

**Risk:** stale legacy IDs from those rows are not loaded into the freshness scan and can survive in strict execution entrypoints without detection.

**TDD fix contract after ownership unblock:**
1. RED: add a test whose alias table first cell contains two or more backticked aliases and whose strict entrypoint uses a non-first alias; current checker must incorrectly PASS.
2. GREEN: parse all backticked tokens from the first table cell, not only a single-token row.
3. Regression: single-alias rows, historical allowed globs, and deleted-path detection remain unchanged.

### P02-F05 — baseline consumer semantics still contain active Google Sheets authority language

**Severity:** RECONCILE_AFTER_PR_530; do not duplicate current work.

The P02-owned Sheets policy is `MIGRATION_ONLY_UNTIL_REMOVAL`, while baseline P01/CP0 routing still contains required-input/read-first language that treats project Google Sheets as an active user-facing planning source. Draft PR #530 already changes the relevant policy/config/P01 files and is protected read-only by this Part.

**Action:** no copy or competing fix. Integration must read post-#530 `main` and only file residual changes if semantic active-authority drift remains.

## 6. Rejected findings / structures intentionally kept

- **Do not merge pruning and legacy retention.** Pruning decides whether material is stale/duplicate/behaviorless; legacy retention owns UNIQUE migration, compatibility, recovery, archive, and destructive gates.
- **Do not merge simplifying and pruning.** Simplifying preserves active behavior while reducing context; pruning can retire material.
- **Do not create a P02-local Registry or freshness config.** That would solve write isolation by creating duplicate authority, which is worse than the current coupling defect.
- **Do not create `proposals/`.** The live BCP registry already declares `[수정제안서]` as proposal root.
- **Do not absorb PR #530.** It is an independent draft workstream and remains read-only.

## 7. Alternatives

| Alternative | Accuracy | Context/maintenance | Ownership safety | Rollback | Long-term fit | Decision |
|---|---|---|---|---|---|---|
| A. Keep current state | Low: confirmed false-negative and ownership contradictions remain | Low immediate cost, growing hidden debt | Superficially safe | Easy | Poor | REJECT |
| B. Let P02 write CP0 companions directly | High short-term | Medium | Violates partition contract | Medium | Poor; erodes control plane | REJECT |
| C. Merge P02-owned audit/learning, export exact CP0 requests, then fix atomic coupling at Integration | High and evidence-preserving | Low duplication | Strong | Strong | Best | ADOPT |
| D. Split a P02 Registry/config/control plane out of CP0 | Potentially high | High duplicate authority/context | Creates new boundary conflicts | Hard | Poor for one-person Base | REJECT |

### BETTER_ALTERNATIVE_SEARCH

After choosing C, two variants were rechecked:

- transferring the entire shared route/config files to P02 would reduce one class of scope failures but make global routing/freshness control compete with other Parts;
- creating generated per-Part fragments would improve machine ownership precision but adds a generator/schema/integration layer before current scale justifies it.

Neither beats the minimal semantic-coupling correction in C.

### LONG_TERM_PLAN_FIT_REQUIRED

The selected path keeps ONE BASE, keeps CP0 singular, and makes Part ownership describe the smallest independently changeable semantic unit. Revisit if P02 repeatedly needs CP0 companions in more than a small minority of maintenance changes; at that point generated owner fragments may become justified.

## 8. External source learning

| Source | Disposition | Applied lesson |
|---|---|---|
| Agent Skills specification (`agentskills.io/specification`) | ADOPT | Skill directory + optional references/scripts/assets and progressive disclosure support existing P02 simplification direction. |
| Agent Skills creator best practices | ADAPT | Coherent Skill units; overly narrow Skills increase multi-skill overhead; overly broad Skills activate imprecisely; keep active bodies focused. |
| Agent Skills evaluation guidance | TEST | Future Skill changes should compare previous/current behavior with isolated evals where cost is justified; do not add a new eval platform just for this audit. |
| OpenAI Academy · Skills | REFERENCE_ONLY | Confirms reusable workflow/SKILL.md model and Agent Skills portability; no new Base-specific rule needed. |
| GitHub CODEOWNERS docs | ADAPT | Path ownership/review separation is a sound model, while Base Manifest remains necessary for logical GPT-Part ownership because one human owns the repository. |

No paid API/SaaS or new broad Skill is introduced.

## 9. Adversarial review — full loops

### Loop 1 — authority / ownership / write scope

Re-attacked the whole P02 responsibility map. Found F01, F02, F03. Rejected direct CP0 edits and duplicate authorities.

### Loop 2 — canonical / consumer / freshness semantics

Re-attacked canon→consumer→test propagation. Confirmed F04 parser false-negative and F05 semantic Sheets drift. F05 is protected by the independent #530 workstream, so no competing write was made.

### Loop 3 — Skill / Mode overlap and context cost

Re-attacked all six P02 Skills as responsibility units. No justified merge/new Skill found. `simplify`, `prune`, and `legacy` remain distinct by output and destructive authority.

### Loop 4 — destructive legacy / recovery / history

Re-attacked archive/delete behavior and live BCP history. Confirmed `[수정제안서]` is active canonical proposal storage; `proposals/` must not be created merely to satisfy the Manifest typo. No destructive deletion is justified in this Part.

### Loop 5 — regression / external practice / long-horizon fit

Rechecked findings against current Agent Skills progressive-disclosure/coherent-unit/eval guidance and GitHub ownership practice. No evidence supports more Skills or another control plane. C remains preferred.

### Loop 6 — post-mitigation whole-Part re-attack

Re-ran the full ownership→Skill→module→consumer→test→legacy chain after converting non-owned fixes into explicit cross-part requests. New P02-owned MUST_FIX findings: **0**. Remaining MUST_FIX items all require CP0 atomic-boundary changes and are exported below; protected #530 remains untouched.

`FULL_LOOPS_PERFORMED: 6`

`CLEAN_REVIEW_EXIT: P02_OWNED_SCOPE_CLEAN_WITH_EXPORTED_CROSS_PART_REQUESTS`

## 10. Cross-part change requests

```yaml
CROSS_PART_CHANGE_REQUEST:
  id: P02-CP0-001
  from_part: P02
  target_owner: CP0
  target_paths:
    - docs/operations/BASE_PARTITION_MANIFEST.json
  reason: P02 BCP ownership points at non-existent proposals/** while live BCP canonical root is [수정제안서]/**.
  evidence:
    - skills/managing-base-change-proposals/SKILL.md
    - [수정제안서]/PROPOSAL_REGISTRY.json
  required_semantic_change: Make the live [수정제안서] proposal root writable by the BCP owner without creating a second proposal authority.
  acceptance_criteria:
    - P02 scope validation accepts intended BCP lifecycle changes at the live canonical path.
    - proposals/** is not introduced as a second active proposal root.
    - PROPOSAL_REGISTRY.json continues to declare exactly one proposal_root.
  blocking: true
```

```yaml
CROSS_PART_CHANGE_REQUEST:
  id: P02-CP0-002
  from_part: P02
  target_owner: CP0
  target_paths:
    - .github/reference-freshness.json
    - skills/BASE_SHARED_SKILL_ROUTES.json
  reason: Unconditional coupled-change rules make P02-owned checker/legacy Skill non-independently writable.
  evidence:
    - reference-checker-test-and-config-sync
    - legacy-retention-shared-skill-sync
  required_semantic_change: Couple only semantic companions that must actually change; keep tests/learning mandatory without forcing unrelated CP0 mutations.
  acceptance_criteria:
    - A parser-only checker bugfix can change checker + owned tests without a no-op config edit.
    - A legacy Skill internal procedure change can update owner-local learning/tests without a no-op shared-route edit.
    - Route/config semantic changes still require their canonical CP0 files and regression tests.
  blocking: true
```

```yaml
CROSS_PART_CHANGE_REQUEST:
  id: P02-CP0-003
  from_part: P02
  target_owner: CP0
  target_paths:
    - tools/check_canonical_reference_freshness.py
    - tests/test_reference_freshness.py
  reason: Multi-alias first cells in LEGACY_SKILL_ALIASES.md are skipped by parse_legacy_aliases().
  evidence:
    - skills/LEGACY_SKILL_ALIASES.md
    - tools/check_canonical_reference_freshness.py
  required_semantic_change: After P02-CP0-002 unblocks atomic ownership, land the RED→GREEN parser fix described in F04.
  acceptance_criteria:
    - Every backticked alias in the first table cell is scanned.
    - A stale non-first alias in a strict execution entrypoint fails freshness.
    - Existing single-alias and allowed-history behavior remains green.
  blocking: true
```

```yaml
CROSS_PART_CHANGE_REQUEST:
  id: P02-CP0-004
  from_part: P02
  target_owner: CP0
  target_paths:
    - skills/SKILL_REGISTRY.json
    - .github/reference-freshness.json
    - P01-owned project operating/intake consumers as applicable
  reason: Baseline still contains active Google Sheets authority semantics while the P02 policy is migration-only; draft PR #530 already overlaps this cleanup.
  evidence:
    - docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md
    - protected draft PR #530 changed-file inventory
  required_semantic_change: Re-read post-#530 main and remove only residual active-authority semantics; preserve migration-only access for UNIQUE unmigrated legacy material.
  acceptance_criteria:
    - No new project workflow requires Google Sheets as a default planning authority.
    - Migration-only consumers remain available until UNIQUE material is read back and moved.
    - No #530 branch content is copied or treated as current before merge.
  blocking: false
```

## 11. Validation contract for this P02 PR

Because confirmed executable fixes are blocked by CP0 ownership, this Part PR intentionally changes only P02-owned audit/learning surfaces. It must still satisfy:

- partition scope checker for P02;
- Base required CI applicable to the exact head;
- no changed path from PR #530;
- no CP0/direct Registry/generated/.github write;
- Notion P02 page readback after update;
- post-merge `main` readback before completion claim.

## 12. Revisit conditions

Re-open P02 architecture if any of the following occurs:

- active Skills exceed 40;
- repeated P02 changes still require CP0 no-op companion edits after P02-CP0-002;
- freshness false-positive/false-negative recurs after the alias parser correction;
- duplicate active proposal roots appear;
- legacy-retirement backlog becomes large enough to justify a separately scheduled maintenance campaign;
- post-#530 main still treats Sheets/HTML/local deprecated surfaces as default authority.
