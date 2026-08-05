# Godot Live Editor Contract v2 — Main Reconciliation Note

## Status

- Date: `2026-08-05`
- Approved written spec: `docs/superpowers/specs/2026-08-05-godot-live-editor-contract-v2-reconciliation-design.md`
- Approved spec commit: `ea0442ddb7fb9286d093cc96e523fdd74a841c22`
- Approval reference: `https://github.com/alsdmlals4-eng/Base/pull/154#issuecomment-5187157323`
- Current main baseline: `83683eecaaeaf415bf629fe5a1231fc6cef575f3`
- Main transition: PR #152 was squash-merged after the written spec was approved.
- Base proposal: `BCP-2026-005-godot-live-editor-contract-v2`, Draft PR #156
- Implementation: `NOT_STARTED`
- Merge authorization: `NOT_GRANTED`

## Why this note exists

The approved specification was written while PR #152 was still an open Draft parent. PR #152 subsequently merged to main and made the v1 contract, schemas, templates, tests, and isolated Godot 4.7.1 Pilot part of the current Base worktree.

The approved architecture and security conclusions remain valid. One migration assumption changed:

```text
approved-spec assumption:
v1 existed only in open Draft work

current fact:
v1 is present on main, but is not part of the locked Base v9.4.3 release identity
```

This note reconciles that fact without rewriting the approved specification or weakening its gates.

## Preserved approved decisions

- Keep Base protocol-neutral and project-owned at the execution layer.
- Do not add a broad active Base Skill or universal MCP server.
- Split effect, idempotency, approval, execution lifetime, and rollback into independent policy axes.
- Bind approvals, ledgers, tasks, and results to exact project/instance/session identity and contract snapshot.
- Require closed input/output schemas, stale-state preconditions, evidence hashes, transport-specific security, and recovery-mode handling.
- Keep Registry identity and released Base locks unchanged.
- Require TDD RED, semantic validation, adversarial review, current merge-ref CI, and zero unresolved MUST_FIX findings.

## Reconciled migration sequence

### Stage A — Static v2 authority

The first implementation PR will:

1. Add active v2 manifest and operation schemas.
2. Migrate the canonical contract, security/readiness documents, project template manifest, adapter, and AGENTS fragment to v2.
3. Add the semantic validator and v2 adversarial tests.
4. Mark v1 schemas and the existing runtime Pilot as `LEGACY_PILOT_COMPAT_ONLY`.
5. Prohibit new project templates, adapters, or canonical documents from selecting v1.
6. Keep the current v1 Pilot executable and its historical runtime evidence intact so static v2 work does not fabricate new Godot execution evidence.

At the end of Stage A there is one active authority for new adoption: v2. The retained v1 files are compatibility artifacts for the already-merged Pilot only, not a second active contract.

### Stage B — Runtime Pilot migration

A separate follow-up PR will:

1. Migrate the isolated Godot 4.7.1 Pilot manifest, CLI envelopes, approval binding, task records, and evidence to v2.
2. Execute the actual Godot binary and regenerate runtime evidence.
3. Prove stale precondition rejection, snapshot/instance binding, output validation, task lifecycle, and recovery-mode behavior.
4. Remove the v1 compatibility schemas and all remaining v1 runtime references only after v2 runtime GREEN.

Stage B must not be reported as complete from static tests or edited evidence files.

## Branch and PR rules

- The static implementation branch must start from exact main `83683eecaaeaf415bf629fe5a1231fc6cef575f3` or a later freshly verified main.
- The BCP proposal remains separate in PR #156 and contains only `[수정제안서]/**`.
- The implementation-plan PR contains only approved design/plan documentation.
- The later implementation PR is separate from both proposal and plan PRs.
- PR #153 remains historical hardening evidence until Stage A reaches current-main GREEN; it is not merged or force-rebased.
- PR #154 is superseded by the main-based planning PR after that PR is created.

## Protected boundaries

The following remain outside both plan phases unless a new approval explicitly changes scope:

- `skills/SKILL_REGISTRY.json`
- Base v9.4.3 and predecessor release locks
- frozen release derivatives
- user game repositories and Google Sheets
- production network MCP server
- production EditorPlugin mutation bridge
- runtime debugger bridge
- project-specific test framework integration
- physical-input and human-usability claims

## Evidence truth table

```yaml
approved_written_spec: PASS
current_main_rechecked: PASS
bcp_proposal_created: PASS
static_v2_plan: WRITING
runtime_pilot_migration_plan: WRITING
static_v2_implementation: NOT_STARTED
v2_godot_runtime: NOT_RUN
production_adapter_ready: false
merge_authorized: false
```
