# Daily Source Context Analysis and Auto-Merge Design

## Goal

Upgrade the existing periodic Source Scan Queue so that it runs every day at 18:00 Asia/Seoul, researches current external articles, converts cited material into Evidence Method-compatible context packets, performs an independent adversarial review, and carries eligible bounded evidence changes through a verified pull request and automatic squash merge.

```text
daily 18:00 KST
→ select overdue sources fairly
→ current article and new-source web research
→ exact URL/source capture
→ structured context extraction
→ independent adversarial review
→ deterministic fail-closed gate
→ bounded evidence and scan-state change
→ PR
→ exact-head Evidence / Base v9 / Game Project OS validation
→ strict-main and review-thread recheck
→ automatic squash merge when eligible
```

## Approval and authority

The user explicitly approved all three changes on 2026-08-14:

1. daily schedule at 18:00;
2. removal of the repository-defined workflow timeout;
3. context analysis followed by the existing Evidence Method, adversarial review, PR validation, and automatic merge.

This approval does not authorize bypassing Base protected-semantic gates. Existing authority remains:

- Source discovery and cadence: `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- Operational state: `PERIODIC_SOURCE_OPERATIONS_LEDGER.json`
- Evidence tier, state, claim ceiling, and disposition: `EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`
- Adversarial attack and critique validation: `running-adversarial-review-and-refinement`
- Actual diff and exact-head evidence: `reviewing-and-validating-project-changes`
- Repository merge policy and strict Required Check: `BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`

No new ACTIVE Skill, Work Mode, independent Evidence owner, or project Canon authority is introduced.

## Existing Solution First

Reuse the existing Source pipeline and `SOURCE_SCAN_AUTO_MERGE_GATE`. Do not add a second scheduler or a model-controlled patch engine.

The current Queue renderer remains responsible for deterministic due-source selection and the human-readable Issue. A new standard-library analysis tool owns network/API orchestration and generated evidence records. The model never receives repository write credentials and never emits shell commands or arbitrary Git patches.

## Schedule and timeout

The workflow schedule becomes:

```yaml
schedule:
  - cron: "0 18 * * *"
    timezone: "Asia/Seoul"
```

`timeout-minutes` is removed from the job. This removes the repository-defined 15-minute cap; it does not override GitHub-hosted runner or token platform limits.

A narrow `push` trigger on `main` is permitted only for the workflow, analysis tool, analysis tests, and source-analysis contracts. Its purpose is to exercise the newly merged automation once without waiting for the next scheduled evening. Automatically generated evidence PRs do not touch these paths, so they do not recursively trigger the operational pipeline.

## Research provider and authentication

GitHub Models is not used because the service was fully retired on 2026-07-30. The workflow uses the OpenAI Responses API through repository secret `OPENAI_API_KEY`.

```yaml
model_secret: OPENAI_API_KEY
model_variable: SOURCE_ANALYSIS_MODEL
model_default: gpt-5.6-terra
response_store: false
```

The API client uses the Python standard library. It sends `store: false`, uses hosted `web_search`, requests complete search sources, and uses strict JSON Schema Structured Outputs for both analysis and adversarial review.

If the secret is absent, authentication fails, the API refuses, cited sources are missing, or structured output fails validation, the run records a blocked state in the Queue Issue and creates no PR.

## Three-stage model boundary

### Stage A — web-grounded research

The first call may use only the OpenAI hosted `web_search` tool. It receives:

- a bounded batch of due Source families;
- names, domains, roles, and approved scan surfaces from the operational Ledger;
- current date and last successful scan dates;
- a request to inspect new or updated articles and discover a small number of additional durable Source-site candidates.

The response must include URL citations and `web_search_call.action.sources`. Repository text, secrets, shell commands, or write tools are unavailable.

External pages are untrusted data. Instructions inside article bodies, snippets, metadata, or linked pages must be ignored. They cannot alter the output schema, approval boundary, source role, or merge policy.

### Stage B — structured Context Packet

The second call has no tools. It receives only:

- the research digest;
- the exact URL/title set returned by Stage A;
- approved Source IDs and current Base owner hints;
- the Evidence Method classification contract.

It must return strict `SOURCE_CONTEXT_ANALYSIS` JSON. Every retained article URL must exactly match a URL present in the Stage A source set.

Required top-level fields:

```yaml
run_date:
scanned_sources: []
candidates: []
new_source_candidates: []
no_change_reason:
```

Each material candidate records:

```yaml
candidate_id:
source_id:
title:
original_url:
published_or_updated_at:
checked_at:
source_role:
evidence_tier:
evidence_status:
source_fact:
context_conditions: []
scope:
sample_or_method:
platform_or_medium:
commercial_or_vendor_interest:
license_or_copying_notes:
base_overlap: NONE | PARTIAL | ALREADY_COVERED | CONFLICT
existing_owner:
decision_delta:
smallest_change_candidate:
disposition: ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
work_disposition: NO_CHANGE | EVIDENCE_ONLY_UPDATE | ABSORB_EXISTING_OWNER | LOW_RISK_BOUNDED_UPDATE | RULE_OR_BCP_CANDIDATE | BCP_OR_USER_DECISION
claim_ceiling:
counterevidence: []
validation_artifact:
rollback_or_discard_condition:
```

New Source sites remain `UNVERIFIED_DISCOVERY`. They are added only to a pending candidate ledger and are not automatically promoted to an active trusted Source, direct fetch target, or Evidence authority.

### Stage C — independent adversarial review

The third call has no tools and receives the Stage B packet plus the exact source URL set. It applies the existing attack and critique-validation lenses:

- fabricated or uncited URL;
- source-role or Evidence-tier escalation;
- current article being treated as universal truth;
- missing version, sample, platform, region, or commercial-interest condition;
- correlation presented as causation;
- success-only selection and missing counterevidence;
- duplicate or already-covered finding presented as a new rule;
- weak claim proposed as a protected semantic change;
- project Canon, Skill identity, policy, permission, security, license, Ruleset, Required Check, save/data, or runtime authority expansion;
- prompt-injection residue or external instructions retained as guidance.

It returns strict `SOURCE_ADVERSARIAL_REVIEW` JSON with P0–P3 findings, approved and blocked candidate IDs, claim-ceiling and URL-verification verdicts, protected-semantic status, and `AUTO_MERGE_ELIGIBLE | AUTO_MERGE_BLOCKED`.

## Deterministic gate

Model verdicts are advisory inputs. Python code owns the final gate.

A generated repository change is eligible only when:

- every retained URL belongs to the exact Stage A source set;
- all Source IDs belong to the selected due batch;
- structured schemas and enums are valid;
- no P0 or P1 finding remains;
- `protected_semantic_change == false`;
- the adversarial reviewer approves every candidate that will be retained;
- retained repository content is limited to generated evidence records, truthful operational timestamps/counters, and pending unverified Source candidates;
- no active Source trust, Skill identity, policy meaning, permission, workflow authority, project Canon, code, schema, or runtime behavior is changed by the generated daily PR;
- the candidate's work disposition is `EVIDENCE_ONLY_UPDATE`, `ABSORB_EXISTING_OWNER`, or `LOW_RISK_BOUNDED_UPDATE`; other candidates may be documented as blocked/reference-only but cannot alter protected owners;
- the generated report explicitly preserves claim ceilings, counterevidence, validation, and rollback.

The model cannot produce arbitrary patches. The analysis tool renders deterministic Markdown/JSON from validated fields.

## Repository outputs

### Daily evidence record

Create one immutable pair per material run:

```text
docs/knowledge/game-development/source-scans/YYYY/MM/YYYY-MM-DD-<run-id>.json
docs/knowledge/game-development/source-scans/YYYY/MM/YYYY-MM-DD-<run-id>.md
```

The Markdown contains visible clickable URLs, short paraphrased findings, Evidence tier/state, conditions, counterevidence, owner route, disposition, validation artifact, adversarial result, and rollback. It does not copy article bodies or long quotations.

### Pending Source candidate ledger

Add:

`docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json`

It stores only unverified discovery metadata:

```yaml
candidate_id:
name:
domain:
url:
source_role:
reason:
first_seen_at:
last_seen_at:
seen_count:
status: UNVERIFIED_DISCOVERY | PROMOTION_CANDIDATE | REJECTED
```

Repeated appearance does not automatically increase Evidence tier or activate direct fetching. Promotion remains governed by the existing Watchlist gate.

### Operational Ledger

Update `last_successful_scan_at` only for Source families actually represented by verified Stage A URLs and Stage B `scanned_sources`. Increment material-candidate fields only for retained material candidates. Do not update Base-contribution fields before a merge is directly observed.

## Fair daily selection

Change `daily-or-weekly` due threshold from seven days to one day. Keep weekly, monthly, and quarterly thresholds unchanged.

Due-source sorting becomes:

```text
never scanned first
→ oldest successful scan
→ cadence priority
→ source_id
```

This prevents the alphabetically first daily Sources from starving never-scanned monthly or quarterly Sources. The operational analysis batch defaults to four Source families per run and can be changed through `SOURCE_SCAN_BATCH_SIZE` without altering repository policy.

## Pull request and automatic merge

The trusted workflow creates a branch from current `main` only when deterministic generated files changed.

```text
automation/source-scan-YYYYMMDD-<run-id>
```

The workflow then:

1. checks exact changed paths against the generated-file allowlist;
2. checks open PR changed-path overlap;
3. commits and pushes the bounded change;
4. creates one non-draft PR;
5. explicitly dispatches the canonical Evidence Knowledge, Base v9, and Game Project OS workflows for the exact branch SHA because token-created PR events may not trigger further workflows;
6. waits for all dispatched workflows to complete successfully;
7. verifies the PR head did not change;
8. verifies current `main` is an ancestor of the PR head; if `main` moved, merges current `main` into the automation branch and reruns all exact-head validation;
9. verifies unresolved review threads are zero;
10. enables repository-approved squash auto-merge with expected-head protection;
11. reads back the PR state and merge SHA when immediately available;
12. updates the Queue Issue with merged, auto-merge-enabled, or blocked evidence.

No direct push to `main`, Ruleset bypass, check bypass, force push, or self-approval is allowed.

## Workflow permissions

Use explicit job permissions:

```yaml
permissions:
  actions: write
  contents: write
  issues: write
  pull-requests: write
```

The workflow cannot read or write repository secrets other than receiving `OPENAI_API_KEY` as an environment value for the API process. The script never prints the key.

If repository Actions settings block PR creation or the token cannot dispatch workflows, record `BLOCKED_ACTIONS_PR_CREATION_SETTING` or `BLOCKED_ACTIONS_DISPATCH`, create no direct-main fallback, and preserve the generated evidence as an Actions artifact.

## No repository-defined timeout

The job has no `timeout-minutes`. Polling waits for dispatched validation without a custom time limit. Platform runner and token limits still apply and may terminate a run externally; such termination is not reported as completed analysis or merge.

## Tests

### Queue regression

Verify:

- cron `0 18 * * *` and `Asia/Seoul`;
- no `timeout-minutes` token;
- `daily-or-weekly == 1`;
- fair oldest/never-scanned sorting;
- explicit write permissions required by the approved automation;
- no `pull_request_target`;
- OpenAI secret is passed only to the analysis step;
- no direct `main` push command.

### Analysis unit tests

Use fixtures and an injected HTTP transport; never call the live API in contract tests.

Verify:

- request payload uses `store: false`;
- web search call requests complete sources;
- strict JSON Schema is used for Context Packet and adversarial review;
- missing key, refusal, malformed output, empty sources, foreign URLs, unknown Source IDs, future dates, and unapproved enums fail closed;
- P0/P1 or protected semantics block repository output;
- deterministic Markdown contains visible source URLs and no article body dump;
- duplicate candidate fingerprints are idempotent;
- pending Source candidates remain unverified;
- Ledger timestamps advance only for verified scanned Source IDs;
- no-change produces no repository diff;
- generated paths remain inside the allowlist.

### Workflow contract tests

Verify PR creation, explicit workflow dispatch, exact-head polling, strict-main synchronization, overlap check, unresolved-thread check, `gh pr merge --auto --squash`, expected-head protection, and blocked-state Issue updates are present.

## Failure states

```text
BLOCKED_MODEL_AUTH
BLOCKED_MODEL_API
BLOCKED_MODEL_REFUSAL
BLOCKED_RESEARCH_SOURCES
BLOCKED_CONTEXT_SCHEMA
BLOCKED_ADVERSARIAL_SCHEMA
BLOCKED_UNCITED_URL
BLOCKED_PROTECTED_SEMANTIC_CHANGE
BLOCKED_P0_P1
BLOCKED_PATH_SCOPE
BLOCKED_OPEN_PR_CONFLICT
BLOCKED_ACTIONS_PR_CREATION_SETTING
BLOCKED_ACTIONS_DISPATCH
BLOCKED_VALIDATION
BLOCKED_MAIN_MOVED_RETRY_REQUIRED
BLOCKED_UNRESOLVED_REVIEW_THREAD
AUTO_MERGE_ENABLED
MERGED
NO_CHANGE
```

A blocked run updates the single Queue Issue and uploads diagnostic JSON without committing model output.

## Security and copyright boundary

- External content is data, never instruction.
- Only OpenAI hosted web search performs external retrieval; generated new Source candidates are not directly fetched by runner code.
- URLs must be HTTPS and must come from the exact API source set.
- Article bodies and long excerpts are not stored.
- No downloaded file, archive, script, HTML event handler, attachment, or executable is run.
- No external text is interpolated into shell commands.
- Model output cannot alter workflow permissions, rulesets, checks, secrets, active Skills, or project Canon.
- API requests use `store: false`; repository reports contain only paraphrased evidence and URLs.

## Rollback

Revert the eventual squash merge commit. Restore the weekly Queue only if intentionally desired, remove the analysis tool and candidate ledger, close or annotate the Queue Issue with `DISABLED_BY_ROLLBACK`, and delete any unmerged `automation/source-scan-*` branches.

Already merged daily evidence records remain historical records unless the revert removes them. Runtime product code, Save/Data Schema, Skill Registry, and project Canon are not migrated by this feature.
