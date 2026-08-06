# HiGodot Single Authority and Reuse-First Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make HiGodot the sole Godot MCP/addon execution authority, preserve destructive authoring capabilities behind risk-tier safeguards, and require existing-solution research before any duplicate MCP/addon/Skill/framework construction.

**Architecture:** Add one canonical Godot policy and link it from existing owners rather than creating new broad Skills. The existing Godot evaluation Skill owns alternative research and disposition, intake blocks premature construction, project operating-system management owns adoption and upgrades, and the installed Godot live-editor Skill owns runtime routing and L0–L3 safeguards.

**Tech Stack:** Markdown policy and Skill contracts, Python 3.12 `unittest` static contract tests, existing Base v9 artifact and integrity validators, GitHub Actions.

## Global Constraints

- `hi-godot/godot-ai` is the only active Godot MCP/addon execution authority.
- Node deletion, file writes, file deletion, project settings, autoload, and structural operations remain allowed.
- Destructive operations use L2 safeguards; project-wide changes use L3 planning, approval, regression, and rollback safeguards.
- DeepSeek receives no HiGodot MCP registration or credential.
- HiGodot remains local loopback only; LAN, public URL, forwarding, and remote tunnel use are forbidden.
- Every adoption pins an exact release or commit and retains rollback evidence.
- No active project `.vscode/mcp.json`, new Base MCP server, Base network Bridge, Hera addon, or second mutation addon is introduced.
- PR #198, #201, and #202 are not merged or closed without a separate explicit decision.
- No new active broad Skill is created; current registered owners are extended.
- No completion or production-readiness claim is made from static files or a connection handshake alone.

---

### Task 1: Add RED contract tests

**Files:**
- Create: `tests/test_higodot_single_authority_policy.py`
- Modify: `.github/workflows/validate-base-v9-rc.yml`

**Interfaces:**
- Consumes: repository text files through `pathlib.Path`.
- Produces: `HiGodotSingleAuthorityPolicyTests`, executed by the existing Base v9 focused test workflow.

- [ ] **Step 1: Write the failing tests**

Create tests that require:

```python
POLICY = ROOT / "docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md"
GODOT_SKILL = ROOT / "templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md"

EXPECTED_OWNER_FILES = (
    ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md",
    ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md",
    ROOT / "skills/evolving-project-discipline-skills/SKILL.md",
    ROOT / "skills/managing-game-project-operating-system/SKILL.md",
)
```

Assertions must cover:

- `HiGodot` and `hi-godot/godot-ai` as sole authority;
- `Node deletion`, file writes, project settings, and autoload under L2/L3;
- `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` gate;
- DeepSeek profile exclusion;
- loopback-only and LAN/public/forwarding/tunnel prohibitions;
- exact pin, canary, regression, and rollback;
- all owner files linking to the canonical policy;
- Godot project Skill naming HiGodot and rejecting Base custom addon authority;
- no root `.vscode/mcp.json` or `.codex/config.toml`;
- AGENTS and START_HERE discoverability.

- [ ] **Step 2: Add the test module to the workflow**

Append `tests.test_higodot_single_authority_policy` to the focused `python -m unittest` command in `.github/workflows/validate-base-v9-rc.yml`.

- [ ] **Step 3: Commit RED**

```bash
git add tests/test_higodot_single_authority_policy.py .github/workflows/validate-base-v9-rc.yml
git commit -m "test: define HiGodot authority and reuse-first contracts"
```

- [ ] **Step 4: Verify RED**

Run the exact GitHub Actions workflow and confirm failures are caused by the missing canonical policy and missing links, while existing Base tests remain green.

---

### Task 2: Publish the canonical policy and global entry gate

**Files:**
- Create: `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`
- Modify: `AGENTS.md`
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: approved design spec.
- Produces: one canonical cross-cutting policy path used by all affected Skills.

- [ ] **Step 1: Create the canonical policy**

The policy must contain these stable sections:

```text
Authority and provider boundary
Existing Solution First Gate
Disposition states
L0–L3 operation classes
Tool/schema progressive discovery
Client and DeepSeek isolation
Local transport boundary
Adoption record
Upgrade, canary, regression, and rollback
Custom PR reference disposition
Failure conditions and evidence status
```

- [ ] **Step 2: Add the global construction gate to AGENTS**

Under `## 2. 작업 진입 게이트`, add a mandatory rule that no new MCP, addon, CLI, framework, Skill, Mode, or execution layer may enter design/build before inventory and disposition through the canonical policy and Godot evaluation Skill.

- [ ] **Step 3: Add one-hop discovery to START_HERE**

Add routes for:

```text
new MCP/addon/framework/Skill before custom construction
Godot live Editor/MCP/addon operation
HiGodot adoption or upgrade
```

All routes point to existing owner Skills and the canonical policy.

- [ ] **Step 4: Register the canonical document in DOCUMENTATION_MAP**

Add one responsibility-table row naming the policy as owner of HiGodot authority, operation tiers, client isolation, provider adoption, and upgrade controls.

- [ ] **Step 5: Run the focused test**

```bash
python -m unittest tests.test_higodot_single_authority_policy -v
```

Expected: owner-link tests may still fail; canonical policy and entrypoint tests pass.

- [ ] **Step 6: Commit**

```bash
git add AGENTS.md START_HERE.md docs/DOCUMENTATION_MAP.md docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md
git commit -m "docs: establish HiGodot authority and reuse-first gate"
```

---

### Task 3: Extend the existing solution-evaluation and intake owners

**Files:**
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/evolving-project-discipline-skills/SKILL.md`

**Interfaces:**
- Consumes: canonical policy path and current Skill routing.
- Produces: mandatory disposition evidence before custom construction without adding a new Skill ID.

- [ ] **Step 1: Extend the Godot evaluation Skill**

Add `inventory-current-environment` and `disposition` modes. Require installed addons, connected MCPs, package manifests, active profiles, Base/project implementations, and related PRs before external search. Replace the narrow decision vocabulary with the canonical disposition mapping while retaining existing adoption states as output compatibility:

```yaml
REUSE: ADOPT
ABSORB: ADAPT
REFACTOR: ADAPT_OR_TRIAL
ARCHIVE: REJECT_OR_DEFER
BUILD_NEW: BUILD_CUSTOM
```

- [ ] **Step 2: Block premature construction in intake**

For requests to create MCPs, addons, CLIs, frameworks, Skills, Modes, or duplicate integrations, route the evaluation Skill before design. Require `existing_solution_disposition`, evidence sources, comparison criteria, and user approval state in the work contract.

- [ ] **Step 3: Harden Skill evolution**

Require evaluation of installed/external equivalents in addition to consolidation-first checks. A new Skill or Mode fails the boundary gate when an existing tool or owner can be reused, absorbed, or refactored.

- [ ] **Step 4: Run focused tests**

```bash
python -m unittest tests.test_higodot_single_authority_policy -v
```

Expected: evaluation, intake, and Skill-evolution link tests pass; Godot operating-owner tests may remain red.

- [ ] **Step 5: Commit**

```bash
git add skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md skills/managing-project-intake-and-work-contract/SKILL.md skills/evolving-project-discipline-skills/SKILL.md
git commit -m "feat: enforce existing-solution disposition before construction"
```

---

### Task 4: Convert project Godot operations and provider adoption to HiGodot

**Files:**
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md`
- Create: `templates/project-operations/HIGODOT_ADOPTION_RECORD.json`

**Interfaces:**
- Consumes: canonical policy and project adapter facts.
- Produces: exact project adoption record and operational routing to HiGodot.

- [ ] **Step 1: Add provider adoption and upgrade responsibilities**

Extend `managing-game-project-operating-system` with provider inventory, exact pin, canary, staged upgrade, rollback, and project evidence requirements. Explicitly separate configuration, connection, runtime, regression, and production-readiness states.

- [ ] **Step 2: Rewrite the Godot live-editor project Skill authority boundary**

Keep the existing `bootstrap → observe → mutate → validate → resume → recover` lifecycle, but replace Base custom addon execution with HiGodot as sole provider. Add:

- progressive domain/schema discovery;
- active project/session verification;
- L0–L3 operation classification;
- L2 support for Node deletion, file writes/deletion, project settings, input map, autoload, Resource replacement, and structural Scene changes;
- L3 explicit approval and full regression;
- DeepSeek no-registration rule;
- loopback-only transport rule;
- no second addon or Base MCP fallback.

- [ ] **Step 3: Add the adoption record template**

Create valid JSON with fields for:

```json
{
  "schema_version": 1,
  "artifact_role": "HIGODOT_ADOPTION_RECORD",
  "provider": "hi-godot/godot-ai",
  "exact_release_or_commit": "NOT_CONFIGURED",
  "godot_version": "NOT_CONFIGURED",
  "host_clients": {"codex": "NOT_CONFIGURED", "gpt_vscode": "NOT_CONFIGURED", "deepseek": "FORBIDDEN"},
  "network_mode": "LOOPBACK_ONLY",
  "enabled_domains": [],
  "unverified_domains": [],
  "last_verified_at": null,
  "verification_evidence": [],
  "rollback_release_or_commit": "NOT_CONFIGURED",
  "connection_status": "NOT_RUN",
  "runtime_status": "NOT_RUN",
  "regression_status": "NOT_RUN",
  "production_readiness": false
}
```

- [ ] **Step 4: Run focused tests**

```bash
python -m unittest tests.test_higodot_single_authority_policy -v
```

Expected: all focused tests pass.

- [ ] **Step 5: Commit**

```bash
git add skills/managing-game-project-operating-system/SKILL.md templates/project-operations/.agents/skills/godot-live-editor-operations/SKILL.md templates/project-operations/HIGODOT_ADOPTION_RECORD.json
git commit -m "feat: route Godot authoring through HiGodot only"
```

---

### Task 5: Full validation and adversarial PR review

**Files:**
- Modify only files required by validated failures.
- Create no new authority document or Skill.

**Interfaces:**
- Consumes: Tasks 1–4 exact branch head.
- Produces: evidence-backed Draft PR with no unresolved P0/P1 findings.

- [ ] **Step 1: Run focused and Base contract tests**

```bash
python -m unittest tests.test_higodot_single_authority_policy -v
python tools/build_base_v9_artifacts.py --check
python tools/check_base_v9_integrity.py --trusted-history-commit <main-sha>
python -m unittest \
  tests.test_v9_machine_contracts \
  tests.test_v9_registry_generation \
  tests.test_v9_governance_documents \
  tests.test_v9_1_project_operating_contract \
  tests.test_v9_1_review_remediation \
  tests.test_v9_1_skill_pressure_contracts \
  tests.test_higodot_single_authority_policy \
  -v
```

- [ ] **Step 2: Create the Draft PR**

The PR body records:

- HiGodot sole authority;
- destructive features allowed with L2/L3 controls;
- existing-solution-first gate and current owner Skills;
- exact files and tests;
- no installation or active MCP config changes;
- PR #198/#201/#202 left unmerged;
- `production_readiness: false`.

- [ ] **Step 3: Run exact-head GitHub Actions**

Require:

```yaml
Validate Base v9 Operating Contracts: PASS
Validate Game Project Operating System: PASS
Dependency Review: PASS
```

- [ ] **Step 4: Run adversarial PR inspection**

Inspect the entire PR patch and attack:

- hidden second execution authority;
- accidental prohibition of requested destructive features;
- duplicated policy text that could drift;
- missing current-environment or PR inventory;
- DeepSeek access leakage;
- public/LAN transport allowance;
- auto-update or missing rollback;
- static evidence overstated as runtime readiness;
- stale references to Base custom addon authority;
- generated artifact or Registry drift.

Classify findings as `P0 / P1 / P2 / ACCEPTED_RISK`. Fix all validated P0/P1 findings, rerun exact-head checks, and ensure unresolved review threads are zero.

- [ ] **Step 5: Stop at merge gate**

Report exact head SHA, workflow results, changed paths, remaining NOT_RUN evidence, rollback path, and PR URL. Do not merge without fresh user authorization.
