# External Agent Tool Adoption Review — 2026-08-31

- `STATUS: ACTIVE_REFERENCE`
- `EVIDENCE_AS_OF: 2026-08-31`
- `AUTHORITATIVE_OWNER: skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- `NO_NEW_SKILL_REGISTRATION`
- `ROLLBACK_BOUNDARY: remove the affected optional adapter or reference rule without changing repository canon, project data, or approved implementation state`
- `REVALIDATION_TRIGGER: upstream license, ownership, release, pricing, telemetry, auth, storage, model, hook, or output-semantics change; Base authority change; repeated false-positive, false-negative, information-loss, or cost-regression evidence`

## 1. Decision

Do **not** install ten parallel always-on skills or make any external workspace the Base authority.

Use the existing Base owners and apply this vocabulary:

- `ADOPT`: keep a demonstrated concept as a Base rule under an existing owner.
- `ADAPT`: retain the useful mechanism after removing diagnosis assumptions, vendor lock-in, duplicate authority, unsafe hooks, unsupported promises, or hidden cost paths.
- `TRIAL_OPTIONAL`: permit only a bounded, reversible A/B trial with raw evidence and an explicit kill switch.
- `REFERENCE_ONLY`: keep the pattern as research material; do not add runtime or workflow dependency.
- `REJECT_AS_REQUIRED_DEPENDENCY`: do not make the package or service mandatory for Base or projects.

Selected structure:

1. action- and reader-adaptive briefing is owned by `managing-project-intake-and-work-contract`;
2. correction-to-rule promotion remains owned by `evolving-project-discipline-skills`;
3. reuse-before-build remains owned by the existing reuse-first and plugin-evaluation contracts;
4. context compression and handoff remain owned by `maintaining-project-context-and-handoff`;
5. code review remains owned by `reviewing-and-validating-project-changes` plus deterministic project tests;
6. optional external executors use `external-agent-adapter-contract.md` and remain advisory.

## 2. Alternatives compared

### Alternative A — install every package as published

Rejected. It creates overlapping always-on instructions, hook-order ambiguity, duplicated decision stores, provider lock-in, extra auth and telemetry surfaces, and several new failure modes without proving project-level value.

### Alternative B — selectively absorb mechanisms under current Base owners

Chosen. It preserves one authority per concern, allows measured trials, and keeps rollback local.

### Alternative C — reject the entire set

Rejected. Several mechanisms improve briefing, evidence reuse, bounded execution, and correction promotion when adapted to current Base constraints.

## 3. Candidate dispositions

| Candidate | Observed mechanism | Base overlap | Disposition | Adopted or bounded result |
|---|---|---|---|---|
| `i-have-adhd` | Action-first briefing, visible next action, compact numbered output, session hook | Intake/reporting and user-update rules | `ADAPT` | Adopt action/conclusion first, visible state, and matter-of-fact error reporting. Do not require a diagnosis, fixed universal list limit, mandatory time estimate, or always-on vendor hook. |
| `ballast` | Keyword-triggered knowledge, correction pinning, pre-compaction/session hooks, decision and goal traces | Discipline-skill promotion, context handoff, decision ledger | `ADAPT` | Promote only repeated evidence-backed corrections with owner, trigger, counterexample, expiry/revalidation, consumer, and regression test. Do not create a second decision canon or log full prompts. |
| `ponytail` | Reuse/deletion-first pressure against speculative code | Existing-solution-first and reuse-first preflight | `ADAPT` | Reinforce deletion/reuse/standard-library/configuration options before new code. Keep exceptions evidence-based; do not add another always-on authority. |
| `open-code-review` | Deterministic pipeline plus LLM review, line-level findings, CLI/agent modes | Review and validation skill, CI, project tests | `TRIAL_OPTIONAL` | Advisory review only on bounded diffs. Require existing endpoint or explicit no-extra-cost route, machine-readable output, secret-safe configuration, and Base-owned validation. |
| `rtk` | Command-output compression proxy | Prompt/token cost optimization and evidence capture | `TRIAL_OPTIONAL` | Trial only on noisy, reconstructable output. Measure total tokens, task correctness, omissions, latency, retries, and total cost against raw commands. Never hide exact failures, source reads, security logs, or required diffs; raw fallback is mandatory. |
| `eli5` | Audience-specific vocabulary, analogy, and explanation depth | User-specific Korean beginner-developer explanation rules | `ADAPT` | Default to Korean beginner-developer explanations with exact identifiers, path, command, reason, and verification. Define jargon once without replacing technical identifiers or becoming childish. |
| `paperthin` | Low-level agentic patterns derived from established engineering practices | Multiple existing Base skills and checks | `REFERENCE_ONLY` | Absorb a pattern only after a concrete recurring failure, named owner, bounded trigger, and regression test are present. No wholesale pattern bundle or duplicate registry entry. |
| `click` | Approved compact contract, stage hooks, bounded runner, evidence reuse | Intake/work contract, scope lock, verification and handoff | `ADAPT` | Adopt argument-array execution, no implicit shell, bounded retry/output, inspect–mutate–verify separation, and evidence reuse. Do not establish a second approval or work-contract authority. |
| `antigravity-cli` | Terminal/headless external agent, permissions, skills/hooks, MCP and model routing | Optional external executor and model-routing concerns | `TRIAL_OPTIONAL` | Use only for a measurable task class with workspace-scoped permissions, exact model/account/quota receipt, telemetry choice, no automatic paid-credit path, and untrusted-output validation. It is not the default executor. |
| `macro` | Unified communication, docs, tasks, code, agents, shared memory; hosted and self-hostable paths | Repository workspace, connectors, task/PR lifecycle, derived memory | `REFERENCE_ONLY` plus `REJECT_AS_REQUIRED_DEPENDENCY` | Reuse UX ideas such as linked task→branch→PR state and unified observation. Repository remains canon; shared memory is derived/untrusted. Any future running-mate core must be provider-neutral with Macro as an optional adapter, not the only viable backend. |

## 4. Evidence and license notes

Sources reviewed at the evidence date:

- `i-have-adhd`: <https://github.com/ayghri/i-have-adhd> — MIT repository and published skill/hook behavior.
- `ballast`: <https://github.com/svy04/ballast> — MIT repository, hook/decision/correction behavior, and documented compliance limits.
- `ponytail`: <https://github.com/DietrichGebert/ponytail> — MIT repository and reuse/deletion-first guidance.
- `open-code-review`: <https://github.com/alibaba/open-code-review> — Apache-2.0 repository, CLI/agent architecture, endpoint and telemetry controls.
- `rtk`: <https://github.com/rtk-ai/rtk> — Apache-2.0 repository. Vendor savings claims are not accepted as project evidence; public counter-evidence includes low-output overhead and low-reasoning cost regression reports.
- `eli5`: <https://github.com/DreambigOu/ELI5> — MIT repository and audience-adaptation guidance. Self-reported evaluation is not Korean-project validation.
- `paperthin`: <https://github.com/LilMGenius/paperthin> — MIT repository and pattern library.
- `click`: <https://github.com/grapefruit0205/click> — MIT repository and bounded contract/runner patterns.
- `antigravity-cli`: <https://antigravity.google/product/antigravity-cli> — official product/documentation surface; account, model, quota, telemetry, permission, and billing behavior must be re-read before each adoption decision.
- `macro`: <https://github.com/macro-inc/macro> and <https://macro.com/> — AGPL-3.0 source plus hosted service. Self-hosting introduces a substantial service/auth/storage/search/event-stream dependency surface; deployment and license obligations require project-specific review.

A repository license does not automatically approve its hosted service, network behavior, model endpoint, telemetry, generated-output license, or project data flow. Those are separate gates.

## 5. Required A/B gate for optional tools

A `TRIAL_OPTIONAL` candidate may run only when all fields are recorded:

- exact repository/project revision and bounded task class;
- tool version, configuration, source/model/endpoint, account tier, and telemetry state;
- baseline path and candidate path receiving equivalent inputs;
- task success and deterministic verification result;
- input/output tokens where observable, elapsed time, retries, failure rate, and total marginal cost;
- omitted or altered evidence, false positives, false negatives, and required raw-output rereads;
- secrets/data classes exposed and retention/logging behavior;
- kill switch, raw fallback, and rollback result.

Promotion requires repeated benefit on representative project tasks, no authority drift, no hidden charge, and no material information loss. A single successful demo is insufficient.

## 6. Five adversarial review loops

1. **Authority collision:** no candidate may become a second canon, decision ledger, approval gate, review owner, or context owner.
2. **Cost and privacy:** reject hidden billing, automatic paid-credit use, plaintext secret/prompt logs, unclear retention, and unbounded telemetry.
3. **Evidence loss:** compressed or generated output is advisory until raw evidence and deterministic checks agree.
4. **Execution safety:** separate inspection, mutation, and verification; use bounded retries, explicit permissions, reversible changes, and a kill switch.
5. **Lock-in and recovery:** keep a provider-neutral core, exportable receipts, repository-owned state, explicit revalidation triggers, and local rollback.

## 7. Promotion and rollback

Concepts marked `ADAPT` are active only through the owner references and tests introduced by this change. They do not grant automatic installation approval.

Optional adapters remain disabled until a project records the A/B gate. Disable the adapter immediately when any of these occurs:

- task success or deterministic verification is worse than baseline;
- evidence needed for diagnosis is omitted or transformed;
- marginal cost, retry rate, or latency materially regresses;
- source/model/version cannot be identified;
- permissions, telemetry, retention, or billing are ambiguous;
- repository authority or approved project meaning drifts.

Rollback removes the optional adapter/configuration and re-runs the same task through the raw Base-owned path. Repository facts, tests, decisions, and approved project assets must remain recoverable without the external tool.
