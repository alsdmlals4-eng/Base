# Approval Brief and Context Routing Implementation Plan

> Execution: approved inline implementation; reuse the current contract across stages. Two full-scope review rounds total, not per Skill.

**Goal:** Make new-change intent, implementation outline and acceptance visible before approval, while preserving approved continuation and reducing unnecessary Skill context.

**Architecture:** Keep the existing intake owner and Registry identity. Move conditional contract detail to directly linked modules; validation reads declared contract modules, while execution selects only applicable references. No new approval service or parallel owner to open PR #844.

**Spec / approval:** Current conversation, 2026-09-16: user approved the preceding proposal with `좋아 진행해줘`; permits justified module/Skill creation, consolidation and a final context/link check. All new modifications require a visible brief then approval; approved same-scope work continues without repeated approval. Read-only questions/research are not mutation requests.

## Constraints and baseline

- Source main: `09f3e45e6e35cd61ab4d71541d47938b1f66a6fe`.
- Current task only; existing PR #844 and all other workstreams read-only. No absorption, direct main push, force push, ruleset bypass, plugin uninstall, model setting changes or fleet project migration.
- Protect original checkout untracked `output/`, unrelated worktrees, released artifacts, Registry and project data/assets.
- Preserve security, authority, approval, evidence ceilings, examples and applicable required checks. No token/line cap used as a quality gate.
- Benchmark: current intake/first-prompt/workflow owners; OpenAI Build Skills progressive disclosure and Anthropic Effective Context Engineering. ADOPT precise triggers/conditional detail, ADAPT existing owner, REJECT broad deletion or another universal prompt Skill.
- Baseline: 16 existing prompt/modularity/reuse tests pass. Independent application probe A/B/C preserves approval/continuation/L0 user override; it found stale unconditional Sheets instructions in the conditional Grill Me reference. Do not invent a failed behavior or cost saving.
- Decision: use small reference modules and a bounded validation/context reader rather than a new Skill. Reconsider only for an independent trigger/input/output/authority/evaluation boundary.

## Approved addition: file-based continuation

The user additionally requested GitHub/local/Blueprint synchronization, short linked entrypoints instead of long chat context, and removal of replaced files, also during project work. Apply this through the existing handoff owner/template and pruning Skill. Inspect real replacement/reference/history boundaries before deletion; no fleet-wide project mutation or blanket cleanup. Correct reached legacy Notion/Sheets mandatory routes to current repository-first authority. Existing session tokens cannot be retroactively removed by a repository patch.

## Work and acceptance

- [ ] T1: Write tests for context selection, declared-module reachability, invalid/missing paths and non-recursive loading; observe RED. Add a small `tools/skill_context.py` helper used by contract validation/tests, not an approval or runtime execution service.
- [ ] T2: Refactor `skills/managing-project-intake-and-work-contract/SKILL.md` into essential entry rules and directly linked conditional modules; preserve original contract detail and downstream validators. Update first-prompt, executable template, AGENTS and workflow/entry links to show intent/current facts/scope/implementation order/acceptance before approval. Distinguish preliminary implementation outline from post-approval detailed execution.
- [ ] T3: Correct directly reached stale consumer instructions, verify selected-reference routing and representative new/continuation/L0/scope-change cases. Reuse valid evidence, reselect on actual context change; never automatically load all Skills after consolidation.
- [ ] T4: Run affected tests, Skill coverage, generated/readback checks and required validation. Complete two independent full-scope reviews; correct valid findings and rerun impacted checks. Publish current-task PR, await exact-head required CI, normal squash merge when permitted, read back main and report evidence ceilings.

## Validation and recovery

Use `python -m unittest tests.test_skill_context -v` for real file selection/side-effect-free rejection fixtures; existing contract suites must still detect missing declarations/content. After integration run `python tools/run_local_validation.py --trusted-history-commit 09f3e45e6e35cd61ab4d71541d47938b1f66a6fe` with process-local `PYTHONUTF8=1` on this Windows host. Agent application probes test interpretation, not game runtime or universal model compliance. Recovery is a normal revert of this PR, not destructive history rewriting. Measure entry-file and selected-reference bytes separately from real token billing, latency or fleet adoption (not measured).

## Evidence / closeout

- Bounded reader: 8 RED failures before implementation, then 8 PASS; redirected reference-directory and stale external handoff regressions additionally reproduced 2 failures and corrected to 20 focused tests PASS.
- Contract migration initially exposed root-only readers. They now read only explicitly declared contract modules for validation. Restored the required root receipt/CLI entry and tested the moved reuse-order owner: 49 focused tests PASS. No contract assertion was removed to make the extraction pass.
- Cleanup: obsolete unconditional Sheets/Notion instructions removed from live owners/consumers. Four conditional modules retain moved content. No old whole file is proven disposable in this bounded path audit: compatibility alias, frozen release history and unrelated/untracked material are retained, not claimed deleted.
- Final test/review/CI/merge evidence and exact SHA are recorded on the current-task PR to avoid self-referential commit hashes. Runtime/Human/game-project adoption and measured token/latency savings are not part of this policy change.
- Expanded focused suite: 69 PASS; coverage and generated artifact check PASS. First full local run: 2,679 tests, 15 errors, 55 skips. All errors came from existing PM subprocess output decoded using Windows cp949 while the renderer emits UTF-8; no product/contract failure was inferred. The same affected suites pass 48/48 with process-local `PYTHONUTF8=1`. A final full run/CI remains required; failed and successful receipts stay separate.
