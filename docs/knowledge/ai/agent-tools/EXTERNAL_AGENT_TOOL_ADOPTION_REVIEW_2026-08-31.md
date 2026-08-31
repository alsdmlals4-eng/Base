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
- `TRIAL_OPTIONAL`: keep a candidate eligible for a separately scoped, reversible A/B trial with original evidence and an explicit kill switch; this disposition is not trial execution or installation approval.
- `REFERENCE_ONLY`: keep the pattern as research material; do not add runtime or workflow dependency.
- `REJECT_AS_REQUIRED_DEPENDENCY`: do not make the package or service mandatory for Base or projects.

Selected structure:

1. action- and reader-adaptive briefing is owned by `managing-project-intake-and-work-contract`;
2. correction-to-rule promotion remains owned by `evolving-project-discipline-skills`;
3. reuse-before-build remains owned by the existing reuse-first and plugin-evaluation contracts;
4. context compression and handoff remain owned by `maintaining-project-context-and-handoff`;
5. code review remains owned by `reviewing-and-validating-project-changes` plus deterministic project tests;
6. optional external executors use `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md` and remain advisory.

`EXISTING_OWNER_REUSE_NOT_NEW_HOOK_IMPLEMENTATION`: naming these owners reuses their existing responsibilities. This change adds briefing/adapter references, the two existing reference-loader links, document regression checks, and an entry in the existing evaluation learning log. It does not implement Ballast's keyword hook, Click's state machine, a new memory system, or an external reviewer/CLI integration.

`EXPLICIT_USER_DECISION_IS_NOT_LEARNED_HEURISTIC`: Record an explicit user-approved decision immediately in its current canonical owner, with scope, approval source, and supersession links when applicable. Do not wait for recurrence before honoring or recording it. Repeated evidence and counterexamples are required when generalizing an observed correction into a reusable heuristic across tasks/projects; that is a different operation owned by `skills/evolving-project-discipline-skills/SKILL.md`.

## 2. Alternatives compared

The viable alternatives are compared on user value, authority safety, total maintenance cost, evidence quality, reversibility, and long-term fit.

| Alternative | Useful result | Trade-off | Disposition |
|---|---|---|---|
| A — retain current Base mechanisms and make only local wording corrections | Lowest integration overhead; existing reuse, learning, and verification paths remain unchanged | Repeated external-tool evaluations still need to reconstruct common raw-output, billing, and rollback requirements | Viable fallback when no external adapter work is expected |
| B — selectively absorb the missing requirements into existing owner references | One briefing contract and one optional-adapter contract, reached through existing loaders; targeted regression checks | Adds a small shared documentation surface that must be maintained; does not provide source plugins' mechanical enforcement | Selected for the approved Base work |
| C — manually enable one isolated upstream package for a representative task after safety preflight | Can directly test hook enforcement or command compression with less custom implementation | Requires exact package/version, permissions, baseline, privacy, and rollback validation; benefit is unmeasured here | Retained as a later project-scoped trial option, not current activation |

Installing every package globally and rejecting all useful concepts are excluded extremes, not the three viable alternatives. Revisit B when a demonstrated recurring problem requires mechanical enforcement that existing Base tools cannot provide, or when measured upkeep outweighs its benefit.

## 3. Candidate dispositions

| Candidate | Observed mechanism | Base overlap | Disposition | Adopted or bounded result |
|---|---|---|---|---|
| `i-have-adhd` | Action-first briefing, visible next action, compact numbered output, session hook | Intake/reporting and user-update rules | `ADAPT` | Adopt action/conclusion first, visible state, and matter-of-fact error reporting. Do not require a diagnosis, fixed universal list limit, mandatory time estimate, or always-on vendor hook. |
| `ballast` | Keyword-triggered rule delivery, correction pinning, compaction/session hooks, decision and goal traces | Discipline-skill promotion, context handoff, decision ledger | `ADAPT` | Record explicit approved decisions immediately; generalize learned rules only through evidence-backed promotion with owner, trigger, counterexample, revalidation, consumer, and regression test. No second decision canon, installed hook, or full-prompt log. |
| `ponytail` | Reuse/deletion-first pressure against speculative code | Existing-solution-first and reuse-first preflight | `ADAPT` | Reinforce reuse/standard-library/configuration options before new code. Removal remains subject to ownership, preservation, and user safety gates; shorter code is not sufficient evidence of a better result. |
| `open-code-review` | Deterministic pipeline plus LLM review, line-level findings, managed and delegated modes | Review and validation skill, CI, project tests | `TRIAL_OPTIONAL` | Advisory review only on bounded diffs. Confirm actual mode, applicable language/ruleset, model/data/cost path, and reviewer independence. A delegated host model is not automatically a separate reviewer. |
| `rtk` | Command-output compression proxy | Prompt/token cost optimization and evidence capture | `TRIAL_OPTIONAL` | Trial only on noisy output with safe original-invocation capture. Compare correctness, omissions, total tokens/cost, retries, and raw rereads. Preserve child status; never replay a side-effecting command merely because its output filter failed. |
| `eli5` | Audience-specific vocabulary, analogy, and explanation depth | User-specific Korean beginner-developer explanation rules | `ADAPT` | Explain in Korean with exact identifiers and verified path/command/reason/acceptance. Do not invent a project runner or replace technical identifiers with childish analogies. |
| `paperthin` | Low-level agentic patterns derived from engineering practices | Multiple existing Base skills and checks | `REFERENCE_ONLY` | Absorb a pattern only after a concrete recurring failure, named owner, bounded trigger, and regression test are present. No wholesale global pattern bundle or duplicate registry entry. |
| `click` | Approved compact contract, persistent stage hooks, bounded execution, revision-bound evidence reuse | Intake/work contract, scope lock, verification and handoff | `ADAPT` | Retain explicit inspect/mutate/verify boundaries, no implicit shell, bounded retries/output, and current-evidence reuse. Do not establish a second approval authority or claim to have installed its hook state machine. |
| `antigravity-cli` | Terminal-first external-agent product | Optional external executor and model-routing concerns | `TRIAL_OPTIONAL` | Evaluate only a named task class after current account/model/quota, permissions, telemetry, data, and billing documentation is verified. No claim that it universally replaces another CLI or outperforms a model. |
| `macro` | Unified communication, documents, tasks, agents, and shared memory | Repository workspace, connectors, task/PR lifecycle, derived memory | `REFERENCE_ONLY` plus `REJECT_AS_REQUIRED_DEPENDENCY` | Reuse observation and linked task→branch→PR UX ideas. Repository remains canon. A future separately approved running mate may use Macro as an optional adapter; no running-mate implementation or Macro deployment is authorized by this review. |

GDScript-specific review quality remains unverified. Open Code Review's availability and generic review architecture do not replace actual Godot parsing, GUT/project tests, runtime evidence, or the existing review owner at `skills/reviewing-and-validating-project-changes/SKILL.md`.

## 4. Primary-source and license observations

These are documentation observations at the evidence date, not pinned executable adoptions, complete security audits, or legal clearance. Exact source commits and effective licenses must be captured before a real package trial.

- `i-have-adhd`: <https://github.com/ayghri/i-have-adhd> — repository identifies MIT and describes action-first output plus a session hook. Base excludes its fixed-list/time-estimate conventions where they conflict with current task needs.
- `ballast`: <https://github.com/svy04/ballast> — repository identifies MIT. Its README distinguishes hook delivery from model obedience and code-enforced behavior from Markdown conventions. The original README was recovered through the GitHub connector when the web reader failed; a failed web fetch alone is not absence of source evidence.
- `ponytail`: <https://github.com/DietrichGebert/ponytail> — repository identifies MIT and describes a reuse-first decision ladder. Its benchmark outcomes are source-reported and do not establish our projects' results.
- `open-code-review`: <https://github.com/alibaba/open-code-review> — repository identifies Apache-2.0. Its README distinguishes managed inference from delegation to a coding agent's model. A no-separate-key mode still requires verification of the actual model, account limits, telemetry, and data path.
- `rtk`: <https://github.com/rtk-ai/rtk> — repository identifies Apache-2.0. Its README explicitly distinguishes bash-output reduction from bill reduction and documents bytes-based token estimates. Exact source reads and diffs are lossy command classes, so Base retains a raw path. Increased overhead or task cost is an evaluation hypothesis here, not an observed local A/B result or an uncited external incident.
- `eli5`: <https://github.com/DreambigOu/ELI5> — repository identifies MIT and describes audience adaptation. Published self-evaluation does not validate Korean explanations or current project tasks.
- `paperthin`: <https://github.com/LilMGenius/paperthin> — repository identifies MIT and describes its pattern library. Its global installation/update instructions are not executed or adopted as Base requirements.
- `click`: <https://github.com/grapefruit0205/click> — repository identifies MIT. Its README states that hooks constrain observable tool paths, not hidden reasoning or semantic correctness, and are not an operating-system sandbox. The original README was read through the GitHub connector.
- `antigravity-cli`: <https://antigravity.google/product/antigravity-cli> — official product surface confirms the terminal-first product. Account, model, quota, telemetry, permissions, and billing details remain activation-time checks; marketing copy is not proof that those checks passed.
- `macro`: <https://github.com/macro-inc/macro> and <https://macro.com/> — repository identifies AGPL-3.0 and describes a shared-backend workspace. Self-hosting suitability, required backend services, auth, backup, operating cost, and effective license obligations need project-specific review; no self-hosted instance was tested here.

`UPSTREAM_BENCHMARK_NOT_LOCAL_A_B_RESULT`: source descriptions and vendor benchmarks are learning inputs. No token-saving percentage, human comprehension gain, model superiority, or runtime performance improvement is claimed for Base/projects by this change.

A repository license does not automatically approve its hosted service, network behavior, model endpoint, telemetry, generated-output license, or project data flow. Those are separate gates.

## 5. Required A/B gate for optional tools

A `TRIAL_OPTIONAL` disposition is only candidate eligibility. The existing adoption owner must first authorize a bounded isolated trial after safety, cost, data, and rollback preflight. The trial then produces the A/B evidence required for activation; completed measurements are not required before the trial that obtains them.

Record:

- exact repository/project revision and bounded task class;
- tool version, configuration, applicable source/model/endpoint, account tier, and telemetry state;
- baseline and candidate paths receiving equivalent isolated starting states, one intentional treatment difference, declared cache/order conditions, and predeclared acceptance criteria;
- task success, expected coverage, and deterministic verification result;
- input/output tokens where observable, measurement kind, elapsed time, retries, failure rate, and total marginal cost;
- omitted or altered evidence, false positives, false negatives, and original-output rereads;
- secrets/data classes exposed and retention/logging behavior;
- kill switch, original-output recovery, and provider-independent rollback result.

Promotion requires repeated benefit on representative project tasks, no authority drift, no hidden charge, and no material information loss. A successful installation, single demo, or documentation test is insufficient.

## 6. Review lenses and full-loop evidence

`REVIEW_LENSES_ARE_NOT_FULL_LOOPS`: the five items below are review perspectives, not evidence that five iterations were executed. Each counted full loop must examine the whole current result with the applicable perspectives, validate criticism against sources/counterevidence, apply any warranted correction, check regression evidence, and reread the resulting state.

1. **Authority collision:** no candidate may become a second canon, decision ledger, approval gate, review owner, or context owner.
2. **Cost and privacy:** reject hidden billing, automatic paid-credit use, plaintext secret/prompt logs, unclear retention, and unbounded telemetry.
3. **Evidence loss:** transformed or generated output is advisory until preserved original evidence and owned checks agree.
4. **Execution safety:** separate inspection, mutation, and verification; preserve child status, avoid duplicate side effects, and bound permissions/retries/cleanup.
5. **Lock-in and recovery:** keep replaceable optional integrations, exportable receipts, repository-owned state, explicit revalidation, and provider-independent rollback without authorizing a new framework.

`FULL_LOOP_RECEIPT_REQUIRED`: actual execution records belong to this workstream's PR review/comments and must identify the reviewed revision/content set, whole-scope findings, counterevidence, correction/no-change rationale, executed or explicitly reused regression evidence, and remaining gates. Do not count one lens as one loop or relabel a single CI run as five executions.

`SAME_AUTHOR_REVIEW_IS_NOT_INDEPENDENT_REVIEW`: repeated self-review and deterministic CI do not supply an independent reviewer. The current repository's independent-review, exact-head checks, unresolved-thread, and ruleset requirements still apply before merge. An empty review list is not review approval.

`EXTERNAL_TOOL_RUNTIME_NOT_RUN`: no external package installation, hook enforcement, model A/B trial, Godot runtime, human UX trial, or service deployment is established by this reference. Test and PR lifecycle claims require current evidence rather than this static document's existence.

## 7. Promotion and rollback

Concepts marked `ADAPT` are policy/reference adaptations reached through existing Base owners. Repository absorption is complete only after the authorized PR is merged and its resulting main state is read back; branch files or a green PR alone are not merged-main adoption. Project adoption and behavior improvement remain separate states.

Optional adapters remain disabled until a project records the appropriate trial and activation gates. Disable an adapter when:

- task success or deterministic verification is worse than baseline;
- evidence needed for diagnosis is omitted or transformed without a valid original capture;
- marginal cost, retry rate, or latency materially regresses;
- applicable source/model/version cannot be identified;
- permissions, telemetry, retention, or billing are ambiguous;
- repository authority or approved project meaning drifts.

Rollback removes only the affected optional configuration and preserves repository facts, tests, decisions, and approved assets. Recover original-invocation evidence before deciding whether a new raw command is safe; do not blindly replay a potentially successful mutation. A Base policy rollback uses the normal reviewed PR route, not force push, broad cleanup, or source-history removal.

## 8. Corrections and reusable learning

Observed baseline: PR #788 at `91fbcc0a89f3c1b3ce1eb5a68a9a619074fabdf6` contained the six-file reference/test change but remained Draft and unmerged. Its body still described the initial RED stage. The prior prose report therefore overstated merged adoption and review evidence.

| Problem and cause | Bounded correction | Reusable verification |
|---|---|---|
| Five perspectives were headed as five completed loops | Separate the lens checklist from revision-bound full-loop receipts and independent review | Reject the old loop heading; require explicit evidence limits |
| Raw fallback could be read as rerunning a command after filter failure | Capture before transform, preserve child status, and prohibit automatic replay | Assert the capture/exit-status/no-replay contract |
| Every tool appeared to require a model identity | Mark model/endpoint/account not applicable when genuinely unused; keep unknown applicable identities blocked | Check deterministic-tool applicability and evidence-freshness clauses |
| Activation requirements were called implementation readiness, creating a circular A/B prerequisite | Separate safety readiness, authorized trial, measured evidence, and project activation | Require existing trial/adoption states and stage ordering |
| A generic Godot runner path and zero exit were offered without a target project | Discover the real validator and check expected executed coverage and revision | Reject the invented runner and require coverage-aware examples |
| Future running-mate advice was phrased as an implementation instruction | Keep it conditional, reference-only, and outside current scope | Reject the imperative build instruction |
| Source metrics and static contracts could be mistaken for local effectiveness | Remove the unsourced cost-regression assertion and label source/runtime boundaries | Require explicit local-A/B and behavior-evaluation limits |
| Equivalent prompts alone could hide different starting state, cache, or prior mutations | Isolate/reset both trial arms and declare the single treatment and acceptance criteria | Check starting-state identity and measurement-kind requirements |
| A repeated-learning threshold could delay an explicit user decision | Record approved decisions immediately; require recurrence only for generalizing heuristics | Check the separate explicit-decision rule |
| A new Base reference could overwrite an adopted project pin or demand duplicate approval | Preserve project authority and reuse valid scoped approval; recheck before writes/merge | Check no-silent-rollout and approval freshness |

`CONTRACT_TESTS_ARE_NOT_BEHAVIOR_EVALUATIONS`: `tests/test_external_agent_tool_adoption_contract.py` checks document content, reference locations, and guardrail presence. It does not execute source hooks, measure reader comprehension, run RTK, or prove an adapter's process semantics. Those require the separate trial gate.

Historical RED receipts:

- The new seven regression cases were committed before corrections at `32232d523c52bc02f963bc64652f711988f5e6cb`. GitHub Actions run `33345247103` executed 2,360 tests and reported exactly seven intended failures with 37 skips. Diagnostic artifact `9741787788` matched its published SHA-256 `7fa047b9e68b395e2f30e0f574bf37bd26c8b9e6a906416a50fd6f110d7b6d43`.
- A compatible concurrent test-only change `52eafa58a3e25af068d366f1778c996947987395` added five cases and was preserved. At `2cb76ba164d3dd0bd847d82c4bdea1ebc7725d26`, run `33345827640` executed 2,365 tests with exactly those five failures and 37 skips; the prior twelve cases passed. Artifact `9741970546` matched SHA-256 `eea9039124570347cf184bf1c5f902eb65548339ddc6420170fc2a75f00946cb`.

These are historical failure/correction receipts, not final validation or independent-review claims. Final exact-head CI, full-loop records, independent-review disposition, and merge/readback state belong to the current PR record: <https://github.com/alsdmlals4-eng/Base/pull/788>.

The existing owner learning entry is `skills/evaluating-godot-assets-and-plugins-before-creation/LEARNING_LOG.md`; this case supplies bounded evidence rather than creating a parallel learning registry. Other owners are referenced only for their already defined responsibilities.

## 9. Absorption state and actual consumers

| State | Applied scope | Evidence limit |
|---|---|---|
| `NEW_REFERENCE_ROUTING` | Evaluation `references/source-catalog.md` reaches this review and the adapter contract; intake `references/first-prompt-direction-anchoring.md` reaches the reader briefing | Loader/document checks prove discoverability, not that every future model obeys |
| `REUSED_EXISTING_CONTRACT` | Existing learning, reuse-first, context/handoff, and review owners retain decision/verification authority | No new hook, duplicate decision ledger, or project rollout is implied |
| `CONTRACT_ONLY_NO_HOOK_ENFORCEMENT` | This PR specifies boundaries and regression checks on their text | Ballast/Click execution mechanisms and external adapters are not implemented here |
| `OPTIONAL_TOOL_NOT_ACTIVATED` | Open Code Review, RTK, Antigravity CLI, and Macro remain outside active project execution | No actual A/B, quota saving, Godot/runtime, human UX, or deployment PASS |

No extra automatic loader, global hook, registry entry, paid integration, or project-local installation is claimed. Further shared rule promotion follows the existing learning owner; this bounded case is not a new source of project truth.
