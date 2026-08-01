# Base P2 Entrypoint Ownership and Compaction Design

## Status and authority

- Status: approved recommended implementation after P1 PR #126.
- Baseline: `main@dfcca68f3b0c654b5b75e6772b014e8fc8ef63af`.
- Work branch: `codex/base-p2-entrypoint-compaction`.
- Work Mode sequence: `PLAN → BUILD → REVIEW`.
- This work changes Base entrypoint presentation only. It does not change Registry bytes, Skill bodies, released locks, generated release artifacts, project repositories, Google Sheets, or product code and assets.

## Problem

`AGENTS.md` is an always-loaded repository instruction file, while `START_HERE.md` is the human and agent cold-start router. Both currently repeat lifecycle definitions, route procedures, publication policy, legacy handling, review sequences, completion criteria, and long Skill descriptions already owned by `docs/OPERATING_MODEL.md`, `docs/WORK_MODE_AND_SKILL_ROUTING.md`, individual Skill packages, and the generated active-Skill view.

The contracts are mostly correct, but the duplicated presentation has three costs:

1. every task pays for conditional detail before its trigger is known;
2. the same rule can drift between two entrypoints and its canonical document;
3. a cold-start reader must distinguish routing from policy while reading hundreds of lines in both files.

The existing Base rule that content preservation and one-step discoverability outrank line or character limits remains authoritative. This design therefore does not introduce a numerical size gate.

## External benchmark

Checked on 2026-08-01 against primary documentation:

- OpenAI Codex describes `AGENTS.md` as durable guidance applied before work and explicitly says to keep it small: <https://developers.openai.com/codex/customization/overview>.
- OpenAI documents layered `AGENTS.md` guidance and project-specific overrides: <https://developers.openai.com/codex/agent-configuration/agents-md>.
- OpenAI's Skill documentation uses progressive disclosure so full instructions load only after selection: <https://developers.openai.com/codex/build-skills>.
- OpenAI recommends linking dedicated review guidance from `AGENTS.md` instead of embedding the whole review manual: <https://developers.openai.com/codex/learn/best-practices>.
- GitHub distinguishes repository-wide instructions from path-specific instructions to avoid overloading the global layer: <https://docs.github.com/copilot/customizing-copilot/about-customizing-github-copilot-chat-responses>.
- GitHub's documentation guidance prioritizes audience, core task, readability, and scannability: <https://docs.github.com/en/contributing/writing-for-github-docs/best-practices-for-github-docs>.

These sources inform presentation and context-loading boundaries only. Base's user authority, approval, evidence, release, and project-adapter contracts remain the controlling requirements.

## Approaches considered

### A. Separate invariant rules from progressive routing — selected

Keep `AGENTS.md` limited to repository-wide authority, safety, approval, canonical-source, evidence, and completion-reporting rules that apply to every task. Keep `START_HERE.md` as a one-step route index from request type to the canonical Skill, mode, policy, or template. Delegate definitions and procedures to existing canonical documents.

This follows the external guidance, removes duplicate ownership, and preserves one-step discovery.

### B. Shorten both files independently

Delete prose from each file until they look shorter while retaining their current mixed responsibilities. This is easy to review visually but does not prevent future duplication or establish which file owns which class of instruction.

### C. Replace both files with a single link list

Make both files extremely small and delegate every rule. This minimizes initial context but weakens the always-on safety boundary and makes routine routing require multiple hops.

## Ownership contract

### `AGENTS.md`: always-on invariant layer

It owns only rules that must constrain every Base task:

- authority and source precedence;
- repository access, environment, permission, and truthful-evidence gates;
- safe handling of user changes, legacy material, approved assets, and protected release surfaces;
- selective Skill routing and user-decision boundaries;
- canonical-source, proposal, publication, and project/Sheet boundaries;
- exact-head validation, review, merge, and completion-reporting requirements.

It links to canonical operating and routing documents instead of reproducing their detailed lifecycle, state-axis, publication-mode, adversarial-loop, or Skill-mode procedures.

### `START_HERE.md`: one-step discovery layer

It owns:

- the minimum Base invocation;
- Base-versus-project cold-start distinction;
- the shortest canonical reading order;
- a request-to-owner route table;
- project reading order, integrated Vertical Slice prompt, and legacy alias discovery.

Each route names the owner and the next file in one step. It does not restate the owner's full procedure.

### Existing canonical detail owners

| Detail | Canonical owner |
|---|---|
| lifecycle, responsibility sources, publication, state axes, completion | `docs/OPERATING_MODEL.md` |
| Work Mode, Skill selection, review flow, GPT→Codex, merge gate | `docs/WORK_MODE_AND_SKILL_ROUTING.md` |
| repository map and secondary routes | `docs/DOCUMENTATION_MAP.md` |
| active Skill inventory and triggers | `skills/SKILL_REGISTRY.json`, generated `docs/generated/BASE_ACTIVE_SKILLS.md` |
| request-specific procedure | selected `skills/<skill-id>/SKILL.md` and its references |
| project installation and cold start | `templates/project-operations/` |

## Semantic regression contract

Tests verify responsibilities and discoverability rather than file length:

- both entrypoints identify their distinct role;
- both link the operating model, routing contract, documentation map, Registry, and generated active-Skill view where applicable;
- every high-risk or commonly used request has a one-step route;
- high-risk routes are selected from Registry trigger metadata, enter the owning `SKILL.md` before optional references or templates, and cannot be hidden by a hand-curated test list;
- always-on approval, environment, evidence, proposal, release, and project boundaries remain in `AGENTS.md`;
- a user-directly-approved Base change may use that explicit request as its work contract without a redundant proposal, while project-derived promotion still follows the proposal boundary;
- active local-validation examples require an exact trusted commit SHA and do not pass a moving ref name into the exact-commit boundary;
- detailed publication states and lifecycle status axes remain absent from both entrypoints because the operating model owns them;
- detailed review algorithms remain absent from both entrypoints because the routing and Skill documents own them;
- existing consolidated-Skill, UI, difficulty/AI, Vertical Slice, Google Sheets, cold-start, and reference-freshness tests continue to pass.

## Adversarial review questions

- Can a new agent still find every required owner without loading all Skills?
- Did compaction remove a safety rule instead of delegating it?
- Can `START_HERE.md` be mistaken for a second operating model?
- Can `AGENTS.md` be mistaken for a request catalog?
- Does a pointer resolve to a current file and active Skill ID?
- Are project-only status files still excluded from Base's active state?
- Are Registry, released locks, frozen/generated artifacts, and project files untouched?

## Completion criteria

- The two entrypoints have non-overlapping declared responsibilities.
- Conditional procedures are delegated to a canonical owner and remain one step discoverable.
- No numerical line or character threshold is introduced.
- RED semantic ownership tests turn GREEN after the compaction.
- Existing focused and full regressions, generated-artifact checks, integrity, Skill coverage, reference freshness, exact-head Actions, and adversarial review pass.
