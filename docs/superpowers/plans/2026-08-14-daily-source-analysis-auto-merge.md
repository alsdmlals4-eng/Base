# Daily Source Context Analysis and Auto-Merge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run the Base Source Scan every day at 18:00 KST, analyze cited current external material through the existing Evidence and adversarial contracts, and automatically squash-merge only deterministic bounded evidence PRs after exact-head validation.

**Architecture:** Extend the current Queue instead of adding another scheduler. A standard-library Python pipeline uses the OpenAI Responses API for web-grounded research, strict context extraction, and an independent adversarial verdict; deterministic code validates URLs, classifications, and generated paths. GitHub Actions creates a bounded PR, explicitly dispatches canonical validations, synchronizes current `main`, and enables squash auto-merge only after all gates pass.

**Tech Stack:** Python 3.12 standard library, `unittest`, OpenAI Responses API, strict JSON Schema Structured Outputs, GitHub Actions, GitHub CLI, Markdown and JSON evidence records.

## Global Constraints

- Baseline `main`: `39936ff6a83410b4169878c1335de9eb3e4c25cf`.
- Work Branch: `feat/daily-source-analysis-auto-merge-20260814`.
- Schedule: `cron: "0 18 * * *"`, `timezone: "Asia/Seoul"`.
- Remove repository-defined `timeout-minutes`; GitHub platform limits remain external.
- Reuse the current Watchlist, operations Ledger, Evidence Method, adversarial review, project-change validation, and strict `ci-gate`.
- Add no ACTIVE Skill, Work Mode, independent Evidence owner, direct-main push, Ruleset bypass, force push, or project Canon write.
- Use repository secret `OPENAI_API_KEY`; model variable `SOURCE_ANALYSIS_MODEL` defaults to `gpt-5.6-terra`.
- Every API request uses `store: false`; external pages are untrusted data.
- Model output is never an arbitrary Git patch or shell command.
- Generated PR paths are limited to `source-scans/**`, `PERIODIC_SOURCE_CANDIDATE_LEDGER.json`, and truthful `PERIODIC_SOURCE_OPERATIONS_LEDGER.json` state.
- New sites stay `UNVERIFIED_DISCOVERY` until the existing promotion gate approves them.
- Protected policy, Skill, permission, security, Ruleset, runtime, data, or project-direction changes fail closed.
- Recheck exact changed-path overlap with open PRs #330 and #333 before merge.

---

### Task 1: Lock intentional RED contracts

**Files:**
- Modify: `tests/test_periodic_source_scan_queue.py`
- Create: `tests/test_periodic_source_analysis_auto_merge.py`
- Modify: `.github/workflows/validate-evidence-knowledge.yml`

**Interfaces:**
- Consumes: current Queue and source-governance contracts.
- Produces: failing tests for daily cadence, timeout removal, fair selection, strict model packets, deterministic evidence, bounded PR validation, and auto-merge.

- [ ] Update Queue tests to require daily 18:00 KST, no `timeout-minutes`, explicit `actions/contents/issues/pull-requests` write permissions, and no `pull_request_target`.
- [ ] Change `daily-or-weekly` expectations to one day and add a never-scanned/oldest-first ordering test.
- [ ] Create analysis tests importing `ANALYSIS_SCHEMA`, `REVIEW_SCHEMA`, `AnalysisBlocked`, request builders, URL/output extractors, packet validators, deterministic gate, renderers, and Ledger updaters from `tools.periodic_source_analysis`.
- [ ] Assert research requests use hosted `web_search`, complete sources, and `store: false`; context/review requests use strict JSON Schema and no tools.
- [ ] Add fail-closed fixtures for missing/refused output, empty or non-HTTPS sources, foreign URLs, unknown Source IDs, future dates, invalid enums, missing claim ceiling/counterevidence/validation/rollback, P0/P1, protected semantics, and incomplete reviewer coverage.
- [ ] Add deterministic tests for visible cited URLs, no article-body dump, candidate idempotency, pending unverified status, truthful operations timestamps, untouched contribution fields, `NO_CHANGE`, and generated path allowlisting.
- [ ] Require workflow tokens for branch/PR creation, three explicit workflow dispatches, exact-head run polling, current-main merge/revalidation, unresolved-thread query, `gh pr merge --auto --squash --match-head-commit`, and blocked-state Issue updates.
- [ ] Wire the new tool/test into Evidence Knowledge syntax, unit-test, path-filter, and artifact lists.
- [ ] Commit and open a draft RED PR; confirm only the approved missing implementation fails.

### Task 2: Implement daily Queue and fair source selection

**Files:**
- Modify: `tools/periodic_source_scan_queue.py`
- Modify: `.github/workflows/periodic-source-scan-queue.yml`

**Interfaces:**
- Consumes: Ledger schema version 1.
- Produces: daily due threshold, fair due order, daily schedule, and no repository-defined timeout.

- [ ] Set `CADENCE_DAYS["daily-or-weekly"] = 1`; keep weekly/monthly/quarterly at 7/30/90.
- [ ] Sort due Sources by never-scanned first, oldest successful scan, cadence priority, then Source ID.
- [ ] Change the schedule to `0 18 * * *` with `Asia/Seoul` and remove the whole `timeout-minutes` key.
- [ ] Add a narrow `push` trigger on `main` for this workflow/tool/test/design contract so the merged automation can be exercised once without evidence-PR recursion.
- [ ] Run focused Queue tests and commit the minimal GREEN behavior.

### Task 3: Implement the context-analysis engine

**Files:**
- Create: `tools/periodic_source_analysis.py`
- Create: `docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json`
- Create: `docs/knowledge/game-development/source-scans/README.md`

**Interfaces:**
- Consumes: due Source batch, operations/candidate Ledgers, run date/ID, model, API key, and injectable HTTP transport.
- Produces: verified Stage-A URL set, strict context packet, strict adversarial verdict, deterministic daily evidence, updated pending candidates and operational state, and a status file.

- [ ] Define `DEFAULT_MODEL = "gpt-5.6-terra"`, default batch size 4, low-risk work dispositions, `AnalysisBlocked`, and closed `ANALYSIS_SCHEMA`/`REVIEW_SCHEMA` objects with `additionalProperties: false`.
- [ ] Build three Responses API payloads: web-grounded research with `include: ["web_search_call.action.sources"]`; strict context extraction without tools; strict independent adversarial review without tools. All use `store: false` and explicitly ignore instructions inside external content.
- [ ] Implement a `urllib.request` JSON client for `https://api.openai.com/v1/responses`; never log the API key. Convert non-2xx, malformed JSON, refusals, and absent output into named blocked states.
- [ ] Recursively collect HTTPS URLs from web-search sources and URL citations; strip fragments only and preserve query strings.
- [ ] Validate exact run dates, selected Source IDs, Stage-A URL membership, enums, required Evidence fields, claim ceilings, counterevidence, validation artifacts, and rollback conditions.
- [ ] Validate the independent review and deterministically retain candidates only when all URLs/claims pass, no P0/P1 exists, protected semantics are false, candidate coverage is complete, and the work disposition is low risk.
- [ ] Render immutable JSON/Markdown evidence containing short paraphrases, visible URLs, Evidence tier/state, conditions, counterevidence, owner route, disposition, validation, review result, and rollback; omit raw research digests and article bodies.
- [ ] Update operations timestamps only for verified scanned Source IDs, increment material counts only for retained candidates, and never change contribution fields before an observed merge.
- [ ] Deduplicate pending new-site candidates by normalized name+URL and keep them `UNVERIFIED_DISCOVERY`.
- [ ] Implement a CLI with paths, date, run ID, model, batch size, and status-output arguments. Blocked runs write diagnostics/status only; `NO_CHANGE` creates no repository diff.
- [ ] Run mocked unit tests with no live network and commit GREEN.

### Task 4: Implement trusted PR validation and auto-merge orchestration

**Files:**
- Modify: `.github/workflows/periodic-source-scan-queue.yml`

**Interfaces:**
- Consumes: analysis status/generated files, GitHub token, API secret, current `main`, canonical validation workflows, and repository Ruleset.
- Produces: one Queue update, evidence artifact, bounded PR, exact-head validation, strict-main synchronization, and squash auto-merge.

- [ ] Set explicit workflow permissions: `actions: write`, `contents: write`, `issues: write`, `pull-requests: write`; pass `OPENAI_API_KEY` only to the analysis step.
- [ ] Render/upsert the single Queue Issue before analysis with run URL, selected batch, and `ANALYSIS_PENDING`.
- [ ] Run the analysis CLI and always upload status/evidence diagnostics. Stop Git mutation on `BLOCKED_*` or `NO_CHANGE` and update the Issue truthfully.
- [ ] Reject any changed path outside the three approved generated-state surfaces.
- [ ] List open PR files and block exact generated-path intersections.
- [ ] Create `automation/source-scan-YYYYMMDD-<run-id>`, commit allowlisted files, push the branch, and create one non-draft PR. On token-setting failure, record `BLOCKED_ACTIONS_PR_CREATION_SETTING`; never fall back to direct `main`.
- [ ] Explicitly dispatch `validate-evidence-knowledge.yml`, `validate-base-v9-rc.yml`, and `validate-game-project-operating-system.yml` for the branch because token-created PR events may be suppressed.
- [ ] Poll and require successful runs whose `headSha` equals current branch HEAD. Use no custom polling timeout.
- [ ] Fetch `origin/main`; if it is not an ancestor, merge current main into the automation branch, push, and rerun all exact-head validation.
- [ ] Require zero unresolved review threads and unchanged PR head.
- [ ] Enable repository-approved squash auto-merge with `--match-head-commit`; never use `--admin`.
- [ ] Read back merged/auto-merge state, exact SHAs, run IDs, and update the Queue Issue.

### Task 5: Connect Evidence and operational documentation

**Files:**
- Modify: `docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`
- Modify: `docs/knowledge/game-development/PERIODIC_SOURCE_SCAN_QUEUE.md`
- Create: `docs/knowledge/game-development/source-scans/README.md`
- Create: `docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json`

**Interfaces:**
- Consumes: approved implementation design.
- Produces: discoverable Evidence ceilings, daily operation, authentication/setup, blocked states, generated records, and rollback.

- [ ] State that generated scan records are T6-assisted records; cited original Sources may receive T1/T2 only after source/date/context verification, and auto-merging a record does not make its claim project Canon.
- [ ] Update Queue documentation from weekly 10:17 to daily 18:00 and document no repository timeout, three-stage analysis, secret/model variables, pending candidate Ledger, generated-path allowlist, explicit validation dispatch, strict-main retry, and squash auto-merge.
- [ ] Define immutable scan naming, required fields, citation/copyright boundary, and rollback in `source-scans/README.md`.
- [ ] Initialize the candidate Ledger with schema version 1, authority `UNVERIFIED_DISCOVERY_ONLY`, and an empty candidates list.

### Task 6: GREEN, adversarial review, and regression

**Files:** all changed files.

**Interfaces:**
- Consumes: exact PR head.
- Produces: fresh CI evidence, validated adversarial findings, no overlap/thread blockers, and merge-ready status.

- [ ] Run focused syntax and unit tests for both Queue and analysis modules.
- [ ] Run the full Evidence Knowledge command from its workflow and require zero failures.
- [ ] Attack secret leakage, prompt injection, uncited URLs, model authority escalation, copyright copying, arbitrary patches, protected semantic merge, token-event suppression, main-moving races, stale heads, unresolved threads, path escape, `NO_CHANGE` churn, Source starvation, and candidate auto-promotion.
- [ ] Validate critiques; fix confirmed P0/P1 and approved in-scope P2 only, then rerun regression.
- [ ] Recheck exact paths against all open PRs, especially #330 and #333.
- [ ] Require exact-head success for Evidence Knowledge, Base v9 including adversarial gate, Game Project OS including Windows smoke/final `ci-gate`, and Dependency Review.
- [ ] Verify ACTIVE Skill count remains 30, Work Modes remain PLAN/BUILD/REVIEW, no Registry/project Canon/runtime path changed, and unresolved threads are zero.

### Task 7: Synchronize, merge, and inspect the first operational run

**Files:** PR and GitHub operational state.

**Interfaces:**
- Consumes: GREEN exact head and current `main`.
- Produces: squash merge, post-merge CI, and a truthful first-run result.

- [ ] Re-read current main. If advanced, non-destructively merge it into the branch and rerun all exact-head checks.
- [ ] Squash-merge the implementation PR with expected-head protection only after every required gate passes.
- [ ] Read back new `main` and verify all intended files at the merge SHA.
- [ ] Require post-merge Base v9 and Game Project OS success including Windows smoke and final `ci-gate`.
- [ ] Inspect the narrow push-triggered operational run and report its exact result: `MERGED`, `AUTO_MERGE_ENABLED`, `NO_CHANGE`, `BLOCKED_MODEL_AUTH`, or another recorded blocked state.
- [ ] Verify exactly one open `[Periodic Source Scan Queue]` Issue with daily schedule, run URL, selected batch, analysis/adversarial status, PR/check/merge evidence, and recovery instructions.

## Self-Review

- Every requested behavior is assigned to implementation and verification tasks.
- Public test imports match Task 3 production interfaces.
- No placeholders, undefined error handling, or silent protected-semantic path remains.
- Generated daily PRs cannot modify workflow, tools, tests, policy, Skills, schemas, project Canon, or runtime code.
