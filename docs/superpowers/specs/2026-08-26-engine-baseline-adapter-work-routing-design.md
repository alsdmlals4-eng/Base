# Engine Baseline, Adapter, and ChatGPT Work Routing Design

## Status

`USER_APPROVED_FOR_IMPLEMENTATION · 2026-08-26`

## Goal

Keep the current Godot portfolio productive while removing unnecessary engine-update churn, separating reusable implementation/runtime rules from engine-specific tooling, and routing long noncoding project work through ChatGPT Work without replacing Notion or GitHub authority.

## Decision

1. Existing game projects remain on their current approved Godot baseline unless a project-specific migration Reality Gate is separately approved.
2. Base gains an `ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE` above engine adapters.
3. Godot remains `GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER`; current HiGodot/GUT/Hera and Godot-specific contracts remain valid adapter responsibilities.
4. Production projects use `STABLE_ENGINE_BASELINE`; new engine releases are not followed automatically.
5. Baseline promotion requires a bounded canary, compatibility/regression evidence, a concrete benefit or blocker, rollback, and a planned maintenance window.
6. Unity or another engine may be evaluated later as a canary for a new or low-implementation project. MCP quality alone is not enough to migrate the current portfolio.
7. P08 routes task shape as `Chat → Work → Codex`: quick discussion in Chat, long multi-step noncoding/project-governance work in Work, actual game product implementation in Codex.
8. Work is an execution surface, not a new source of truth. Notion stays the human-facing planning/visual canon; GitHub/repository stays structured implementation/runtime truth.

## Architecture

```text
User / Project
→ Chat: quick discussion, decision shaping, short questions
→ Work: long multi-step research, review, Base/Notion/document/analysis execution
→ approved implementation handoff
→ Codex: actual game product implementation
→ ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON
   └─ current default: Godot adapter
→ runtime/test/play evidence
→ GPT final review
→ Notion/GitHub canon sync
```

The engine-neutral core owns project identity, implementation handoff, execution freshness, evidence ceilings, runtime/test separation, rollback, and final review. Each engine adapter owns editor/runtime/build/test/package details.

## Compatibility

`CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER` remains an active compatibility vocabulary for existing Godot projects. It becomes the current Godot adapter specialization of `CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER`, not a deleted or superseded contract.

No existing Godot project, Scene, Resource, GDScript, test suite, HiGodot authority, GUT suite, Hera live-QA boundary, or project runtime is migrated by this change.

## Engine update gate

```text
new engine release
→ NO_AUTOMATIC_LATEST_FOLLOW
→ concrete blocker/security/platform/benefit?
   ├─ no → keep current STABLE_ENGINE_BASELINE
   └─ yes → isolated canary
              → plugin/addon compatibility
              → import/parse/test/runtime/export regression
              → rollback proof
              → benefit confirmed
              → planned maintenance window
              → CANARY_BEFORE_ENGINE_BASELINE_PROMOTION
```

## Work routing gate

Use Work by default when a task is long, multi-step, requires research/analysis across connected apps or files, modifies Notion/Base/documents, performs a broad audit, creates a finished deliverable, or must maintain a longer execution thread. Use Chat for short discussion and decision shaping. Use Codex for software/game implementation.

Work must fresh-read relevant Notion/GitHub sources just like other GPT-owned work; its conversation state does not become canon by itself.

## Non-goals

- no Unity migration;
- no second persistent engine writer;
- no forced MCP installation;
- no rewrite of every Godot-specific identifier in one change;
- no Notion replacement;
- no GitHub replacement;
- no new paid service requirement;
- no product/runtime PASS claim.

## Acceptance

- new engine policy records the neutral core, default Godot adapter, stable baseline, canary promotion, and migration Reality Gate;
- P06 points to the policy and treats Godot as the current adapter rather than the universal reusable core;
- P08 records Chat/Work/Codex routing and generic Codex product implementation ownership while retaining Godot compatibility vocabulary;
- existing open PR-owned paths remain untouched;
- focused regression test turns GREEN and existing P08/Godot contracts remain valid.
