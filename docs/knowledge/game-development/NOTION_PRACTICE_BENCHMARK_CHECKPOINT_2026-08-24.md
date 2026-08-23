# Notion Practice Benchmark Checkpoint · 2026-08-24

## Evidence ceiling

This checkpoint records a focused Notion optimization scan for the current Base/project operating model. Baseline: `alsdmlals4-eng/Base` main `dbc5d576c152d1a8bd9b2de25b25c02155a7e23c` after #630 (`7c6349719b6505a373cff7114b6be799b21a70d1`), which already adopted shallow Notion project information architecture.

The existing owners remain authoritative:

- `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`
- `docs/operations/NOTION_PROJECT_ISOLATION_AND_CORE_SYSTEM_CONTRACT.md`
- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`

External sources below are evidence, not project canon. Product facts use Notion official sources; practitioner/template sources are `PROFESSIONAL_PRACTICE` with commercial-interest notes; Reddit is `DISCOVERY_FEED / SELF_REPORT`; research papers are primary research for the population/method they studied. No external template or workflow is copied wholesale.

`FIGMA_USAGE: DISABLED_BY_USER` remains a higher-priority user decision. Figma/Huddling is not reintroduced as an active source, workspace, or recommended workflow.

## Current Base fit

Current Base already implements the strongest repeated pattern from this scan:

```text
L0 PROJECT_HUB
→ L1 HUMAN_PROJECT_HOME
→ L2 4~6 project-specific DOMAIN_WORKSPACE
→ L3 DETAIL_OR_RECORD

Notion = human-facing design/visual/comparison canon
Repository = Markdown/JSON/game data/code/scene/resource/test/runtime truth
```

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`, project-filtered linked views, Project namespace isolation, bounded record writes, optimistic conflict detection, source/status laundering guards, and `ZERO_INCREMENTAL_COST` are consistent with the external evidence reviewed here. This scan does not justify replacing that architecture.

## Source packets

### NOTION-OFFICIAL-20260824-RESPONSIBILITY-BOUNDARY — ADAPT / ALREADY_COVERED

Official sources:
- Skills: https://www.notion.com/help/create-and-manage-skills
- Instructions: https://www.notion.com/help/instructions-for-notion-agent
- Custom Agents: https://www.notion.com/help/custom-agents
- Custom Agent best practices: https://www.notion.com/help/best-practices-for-creating-and-optimizing-a-custom-agent
- MCP: https://www.notion.com/help/notion-mcp
- Releases: https://www.notion.com/releases

Checked: 2026-08-24.

Observed product boundaries:
- Instructions are persistent/default behavior.
- Skills are reusable task-specific procedures.
- Custom Agents are autonomous recurring/event-triggered workers.
- Notion recommends narrow context, explicit completion criteria, simple first versions, and lower-frequency starts before expanding automation.
- Notion MCP can connect ChatGPT Pro and other MCP clients, but acts with the user's Notion permissions.
- The 2026-08-19 release added the Developer Portal in the sidebar for Workers, connections, personal access tokens, and developer IDs/API objects.

Disposition:
- `ADAPT / ALREADY_COVERED` for responsibility separation and least-privilege/readback principles.
- Do not mirror Base Skills wholesale into Notion Skills.
- Keep automatic Skill invocation off until a candidate procedure is stable and its retrieval/routing behavior has been tested.
- Use the personal/interactive agent path for one-off work before considering autonomous agents.

### NOTION-OFFICIAL-20260824-COST-BOUNDARY — AVOID_DEFAULT / RECHECK_ON_DEMAND

Official sources:
- Custom Agent credit pricing: https://www.notion.com/help/buy-and-track-notion-credits-for-custom-agents
- Notion credits: https://www.notion.com/help/category/notion-credits
- Workers pricing: https://www.notion.com/help/understand-pricing-for-workers

Checked: 2026-08-24.

Observed:
- Custom Agents consume Notion credits and require the plan/features described in current official docs.
- Workers are for deterministic background code such as syncs, updates, and event handling.
- Workers began requiring Notion credits on 2026-08-11.
- Credit usage rises with content read, actions/steps, and execution frequency.

Disposition:
- `AVOID_DEFAULT` for Custom Agents and Workers in the current zero-incremental-cost workflow.
- Revisit only after a measured recurring manual burden exists and a free/currently-connected route is demonstrably worse.
- Agent SDK/preview surfaces remain `REFERENCE_ONLY` until stability, access, and project need are proven.

### NOTION-PRACTICE-20260824-CONTEXTUAL-VIEWS — ADAPT

Professional-practice sources:
- Thomas Frank Ultimate Tasks database reference: https://thomasjfrank.com/docs/ultimate-tasks/databases/
- Thomas Frank project/task relations: https://thomasjfrank.com/docs/ultimate-tasks/databases/projects/
- Notion VIP project management: https://www.notion.vip/insights/streamline-project-management-with-notion
- Bulletproof Notion upper-bound example: https://bulletproof.notion.vip/

Commercial-interest note:
- These authors publish/sell Notion templates and training. Their patterns are workflow examples, not neutral authority.

Observed:
- Thomas Frank's core task system is centered on a small number of master databases and linked views.
- Notion VIP emphasizes relational master databases with filtered/contextual views.
- The Bulletproof system's nine content-type databases show how quickly a generalized workspace can become expansive.

Disposition:
- `ADAPT` the principle: centralize only genuinely shared records; expose them through project-filtered contextual views.
- `AVOID` copying nine-database/second-brain complexity into a solo-game workspace.
- Current Base's Project Registry + Work/Asset/Core System masters + project-filtered human views are closer to the desirable side of this trade-off.

### GAMEDEV-PRACTICE-20260824-LIGHTWEIGHT-WIP — TEST

Community discovery/self-report:
- Recent solo-dev organization discussion (2026-06-17): https://www.reddit.com/r/gamedev/comments/1u8pky9/
- Solo process/overhead discussion: https://www.reddit.com/r/gamedev/comments/1703cya/
- Solo PM tool discussion: https://www.reddit.com/r/gamedev/comments/1eey9sc/

Observed:
- A 2026 solo developer using Notion/Trello/Miro reported frustration when trying to centralize project databases.
- Another solo developer reported better focus after separating a 1–3 day immediate shortlist from the longer MVP/backlog view and planning once per week.
- Repeated community counterexamples describe enterprise-style PM tooling as excessive overhead for solo work.

Disposition:
- `TEST`, not a Base hard rule: each project should have a low-noise current-work view derived from `WORK_MASTER`, while long-horizon ideas remain outside the immediate execution surface.
- Do not duplicate the task state into a second independent Notion/GitHub tracker.
- Exact WIP counts are project/person dependent; no universal numeric limit is adopted from Reddit.

### GAME-DOC-20260824-LIVING-MODULAR — ADOPT_CURRENT_DIRECTION

Professional-practice sources:
- Game Developer, modern GDD discussion: https://www.gamedeveloper.com/design/how-to-write-a-game-design-document
- Game Developer, game-development wiki discussion: https://www.gamedeveloper.com/design/learning-the-ways-of-the-game-development-wiki
- Game Design Documentation reference: https://gdad.wiki/wiki/production/game-design-documentation

Observed:
- Modern documentation guidance favors searchable, readable, concise, living/modular references over a single monolithic design bible.
- Documentation should have a specific audience and purpose; stale documents become liabilities.
- Technical implementation and production tracking can be separate from design intent while remaining linked.

Disposition:
- `ADOPT_CURRENT_DIRECTION`: #630's self-contained Human Home plus shallow domain drilldown is compatible with living/wiki-style documentation without turning the Home into a thin link hub.
- Keep implementation/runtime truth in the repository rather than stuffing technical execution detail into the human-facing GDD.

### GAMEDEV-RESEARCH-20260824-OVERHEAD-RISK — ADAPT

Primary research:
- Video Game Project Management Anti-patterns: https://arxiv.org/abs/2202.06183
- Dataset of Video Game Development Problems: https://arxiv.org/abs/2001.00491
- Learning from the past: process recommendations: https://arxiv.org/abs/2009.02445

Observed:
- The anti-pattern study mapped 440 postmortem problems and identified game-specific candidates including Feature Creep, Feature Cuts, Working on Multiple Projects, and Absent/Inadequate Tools.
- The broader postmortem dataset extracted 1,035 software-engineering problems from 200+ postmortems.
- Process recommendation research argues for context-sensitive process selection rather than one universal workflow.

Disposition:
- `ADAPT`: prefer a small, inspectable system that protects project focus and can vary by project context.
- Do not interpret one popular Notion template as a universal production process.
- New database/property/automation layers need an explicit recurring decision or handoff problem to solve.

## Architecture trade study

| Alternative | Setup / maintenance | GitHub conflict risk | Multi-project fit | AI fit | Cost / lock-in | Verdict |
|---|---|---:|---:|---:|---:|---|
| A. Notion all-in-one canon: GDD + tasks + bugs + implementation status + automation | High and grows with schema | High: execution truth can diverge from repo/CI | Medium; global DBs become noisy | High surface, but broad permissions/context | Higher lock-in; paid automation temptation | `REJECT` as default |
| B. Notion human control plane + repository execution/runtime canon | Moderate, bounded by project-filtered views | Low when sync boundary is explicit | High with Project namespace isolation | High: human context in Notion, execution evidence in repo | Compatible with zero-incremental-cost baseline | `ADOPT` — current Base direction |
| C. Notion GDD/reference only + GitHub owns all work/execution tracking | Low | Very low | High | Medium; weaker human project-at-a-glance surface | Lowest Notion dependence | `ADAPT` fallback for tiny prototypes/jams |
| D. GitHub-only documentation/execution | Low-to-medium | Lowest | High technically | High for code, weaker for human visual/editable planning | Low vendor spread | `REJECT` as Base default because it violates the current human-facing Notion canon; valid only if a project explicitly exits Notion |

Better-alternative search result: B remains strongest for the current user because it preserves the already-approved Domain Split Canon, human-readable/visual planning, and repository implementation truth without introducing a second execution canon.

## Recommended responsibility boundary

| Surface | Use now | Boundary |
|---|---|---|
| Notion Instructions | `REFERENCE_ONLY / TEST_IF_AVAILABLE` | Short always-on preferences only; never copy all Base governance into one instructions page. |
| Notion Skills | `TEST_IF_AVAILABLE` | Repeated page-local procedures only. Begin manual invocation; auto-use only after routing quality is verified. |
| Personal Notion Agent | `ADAPT` | One-off research/editing and bounded human-facing updates with destination readback. |
| Notion MCP | `ADAPT_WITH_GUARDS` | Useful for ChatGPT↔Notion; project-scoped reads, bounded writes, readback, and current permission awareness are mandatory. |
| Custom Agents | `AVOID_DEFAULT` | Paid/autonomous background work; revisit only for a measured recurring workload with clear evaluation. |
| Workers | `AVOID_DEFAULT` | Deterministic background code only when current free/local/connector routes fail a real need; credits apply. |
| Notion CLI/API | `REFERENCE_ONLY` | Use only for a concrete deterministic integration that existing connected tooling cannot do safely. |
| Agent SDK / preview developer surfaces | `REFERENCE_ONLY` | No production dependency until stability/access/cost are verified. |

## Minimal structure recommendation for solo game projects

Do not add another universal database set now. Reuse current Base owners:

```text
PROJECT_HUB
→ HUMAN_PROJECT_HOME
   → full game/story flow
   → core systems + setting/player role
   → representative project-specific tables
   → approved visual/UX anchors
   → current implementation/validation ceiling
   → blocker + next work

→ 4~6 project-specific L2 domains
   → project-filtered Work / Asset / Core System / Reference / Benchmark views
   → L3 detail records only when responsibility really differs

Repository
→ code / JSON / scenes / resources / tests / CI / runtime evidence
```

### Database-escalation test

A new Master DB or materially new property family is a candidate only when at least one of these is true:

- the record type repeats across projects and needs a stable identity;
- relation/filter/rollup/query is required for a real recurring decision;
- the same manual handoff is recurring and measurable;
- the information needs a separate human owner that cannot remain a page section/table or existing record type.

Otherwise prefer an existing owner, an L2/L3 page section, a simple table, or a filtered view. This is a `TEST` candidate from this scan, not a new Base invariant yet.

### Current-work view test

For solo execution, test a project-filtered `NOW / NEXT / LATER` or equivalent view derived from `WORK_MASTER`.

- `NOW`: only work that can realistically be acted on immediately.
- `NEXT`: short-horizon queued work.
- `LATER`: ideas, deferred work, and non-current scope.
- Do not copy these states into a second GitHub task canon.
- Do not adopt a universal WIP number until actual project evidence shows a useful limit.

## Candidate Notion Skills — no activation in this checkpoint

Only procedures that recur and stay page-local should become Notion Skill candidates. First candidates to test if the current plan exposes Skills without extra cost:

1. `Decision Delta Review` — compare a proposed human-facing change against confirmed direction, protected elements, source status, and repository-sync requirement.
2. `Benchmark Packet Normalize` — convert research notes into source / context / ADOPT-ADAPT-AVOID-TEST / player-value / production-fit fields.
3. `Playtest Evidence Synthesis` — summarize player observations separately from AI inference and produce next test questions.
4. `Human Home Consistency Check` — check that full flow, core systems, representative data, visual anchors, implementation ceiling, blocker, and next work remain understandable before drilldown.

Do not create these merely because Notion supports Skills. Promote only after the same prompt/procedure is actually repeated and the existing Base owner cannot supply the behavior more cheaply.

## Immediate decisions

### Our environment can use now
- Keep current #630 shallow IA and Domain Split Canon.
- Keep Human Home rich enough for core understanding; use linked filtered views for details.
- Keep one execution/runtime truth in GitHub.
- Use project namespace isolation and bounded Notion writes/readback for AI collaboration.
- Use official Notion docs to verify fast-changing product/permission/price claims immediately before adoption.

### Add when evidence justifies it
- One low-noise current-work view per project from the existing Work Master.
- Small Notion Skills for truly repeated page-local transformations, only if available within the current cost boundary.
- A practitioner/solo-game-dev/academic evidence lane in future Notion scans, with commercial/self-report bias recorded.

### Remove / avoid
- 40-page monolithic GDD as a universal template.
- Copying a large “second brain” workspace or nine-database template.
- Mirroring GitHub Issue/PR/test status as a second independent Notion execution truth.
- Property/formula/rollup growth without an active decision consumer.
- Custom Agents, Workers, paid connectors, or paid templates by default.
- Broad autonomous write permissions or “always allow” without a bounded target and readback.

### Experiments
- `TEST`: project-filtered current-work view; measure time-to-resume after a break, stale-task rate, and whether it reduces context switching.
- `TEST_IF_AVAILABLE`: one manual Notion Skill for `Decision Delta Review`; compare correction count and time versus the current GPT workflow.
- `TEST`: database-escalation gate on one project before making it Base-wide.
- `REFERENCE_ONLY`: Notion Developer Portal / CLI / Workers until a concrete integration need exists.

### Base promotion candidates
- `BASE_PROMOTION_CANDIDATE`: future Notion source scans should deliberately include three evidence lanes beyond official product facts: professional Notion practice, solo/indie game-development workflow self-reports, and game-development project-management/postmortem research.
- `BASE_PROMOTION_CANDIDATE`: database-escalation gate, only after at least one project trial demonstrates lower maintenance without discoverability loss.
- No new ACTIVE Skill is justified by this scan.

### Project-only candidates
- Current-work view naming, WIP shape, and visible fields.
- Which L2 domains are present and how they are named.
- Whether a specific project benefits from a dedicated Bugs/Builds/Experiments view versus repository-native tracking.
- Which Notion Skill candidates are actually repeated in that project.

## Adversarial review · 5 full loops

### Loop 1 — authority, current state, and duplication
Full-scope attack checked user intent, latest Base main, #630, current Notion owners, same-goal PRs, cost, external evidence, and project/repository authority.
- Finding: an all-in-one Notion recommendation would conflict with Domain Split Canon and duplicate GitHub execution truth.
- Validation: current Base explicitly separates human-facing Notion canon from repository runtime/structured truth.
- Refinement: keep alternative B; reject all-in-one as default.
- Regression recheck: no existing current Base owner is displaced.
- Better alternative / long-term: B remains stronger than A/C/D for multi-project human comprehension plus implementation fidelity.

### Loop 2 — solo-developer overhead and feature creep
Full-scope attack repeated current-state/owner/cost/security/maintenance review using practitioner, community, and postmortem evidence.
- Finding: generic productivity templates can add databases/properties faster than a solo developer gains decision value.
- Validation: professional systems themselves range from 3 core DBs to 9 content types; solo-dev reports explicitly describe database/tool overhead; game postmortems identify inadequate tools/multiple-project problems.
- Refinement: add database-escalation as `TEST`, not hard rule; use contextual filtered views.
- Regression recheck: current Project Registry/Work/Asset/Core System masters remain sufficient.
- Better alternative / long-term: no new Master DB set is justified.

### Loop 3 — AI permission, automation, and cost
Full-scope attack repeated authority, data flow, permission blast radius, cost, rollback, and current paid-plan constraints.
- Finding: Skills/Agents/Workers can look like workflow improvements while adding plan dependence, credits, and autonomous write risk.
- Validation: official docs distinguish responsibilities; MCP acts with user permissions; Custom Agents/Workers consume credits under current product terms.
- Refinement: personal/bounded interaction first; Skills manual-first; Custom Agents/Workers `AVOID_DEFAULT`.
- Regression recheck: zero-incremental-cost and bounded-write contracts remain intact.
- Better alternative / long-term: existing ChatGPT/Notion connection + current Base guards beats new paid automation for current workload.

### Loop 4 — documentation usability and canon drift
Full-scope attack repeated human-home UX, GDD freshness, GitHub sync, context switching, and re-entry after pauses.
- Finding: making Home too thin would force navigation; making it monolithic would bury details and become stale.
- Validation: modern GDD guidance favors living/searchable/modular docs; #630 explicitly requires full flow/core understanding on Home plus shallow drilldown.
- Refinement: preserve rich Home + contextual L2/L3, not “short Home at all costs.”
- Regression recheck: no conflict with Human Home self-contained policy.
- Better alternative / long-term: current #630 structure balances fast orientation and detail ownership better than monolith or link-only dashboard.

### Loop 5 — measurable value, project fit, and overgeneralization
Full-scope attack repeated all prior lenses and asked whether any recommendation is being promoted from popularity, a single anecdote, or vendor marketing.
- Finding: exact WIP numbers, mandatory Skills, and new database counts are not sufficiently generalizable.
- Validation: community evidence is self-report; practitioner sources have commercial/template interests; research supports context-sensitive process choice.
- Refinement: exact WIP/Skill/database changes stay `TEST` or project-only; only responsibility boundaries and current Base direction are retained.
- Regression recheck: no unsupported universal rule, no paid dependency, no new ACTIVE Skill, no Figma revival, no project canon/runtime mutation.
- Better alternative / long-term: evidence-lane expansion is the only Base-level promotion candidate; operational details remain project-specific.

`CLEAN_REVIEW_EXIT`: five full-scope loops completed with no remaining blocking conflict. The retained change is evidence-only; no implementation/runtime claim is made.

## Implementation Reality Gate

Verified:
- latest Base main and current Notion authority contracts were read;
- current #630 shallow IA is present on main;
- no open same-goal PR was found at scan time;
- current Notion official product/cost/permission claims were checked against official sources;
- practitioner, solo-dev, modern GDD, and academic/postmortem evidence were cross-compared.

Not verified / not claimed:
- no live project Notion pages were mutated in this checkpoint;
- no Notion Skill, Custom Agent, Worker, CLI, or SDK was enabled;
- no paid Notion feature was purchased;
- no project-specific current-work view experiment has yet produced measured results.

## Completion disposition

`EVIDENCE_ONLY_UPDATE`

The main material result is not a new Notion architecture. The strongest outcome is that current Base #630 is already aligned with the external evidence, while future scans should broaden beyond official Notion product facts and test lightweight, project-specific workflow refinements before promoting them to Base invariants.
