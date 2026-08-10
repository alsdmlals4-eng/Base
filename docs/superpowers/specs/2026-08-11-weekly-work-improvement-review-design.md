# Weekly Work Improvement Review — Design

## Problem

Base already owns periodic external-source discovery, game/player-experience evidence, serial-fiction craft, prompt/Skill placement, and adversarial review. BCP-2026-020 also extracted durable player-experience gates from the 2026-08-10 weekly report. The remaining gap is a reusable, non-canonical synthesis surface that turns those existing owners into a consistent weekly A/B/C/D improvement review without copying the same rules into a new broad Skill.

## Existing Solution First

Disposition: `ABSORB_EXISTING_OWNER / LOW_RISK_BOUNDED_UPDATE`.

Keep current owners:

- source discovery/evidence: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- game benchmark/player evidence: `analyzing-and-refining-game-concepts`
- fiction/serial revision: `developing-and-revising-serial-fiction`
- prompt/Skill placement: `docs/AI_SKILL_ADOPTION_GUIDE.md` + `evolving-project-discipline-skills`
- player-experience claim ceilings: `docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md`
- independent attack/critique validation: `running-adversarial-review-and-refinement`
- Base promotion: `managing-base-change-proposals`

Do not create a new ACTIVE Skill. The weekly review is an orchestration/template surface; it has no independent tool, permission, or authority boundary.

## Design

Create `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md` as a reusable report contract.

The template:

1. starts with current Base/project truth, connected GitHub/Drive context when available, same-goal PRs, and previous-report delta rather than a news dump;
2. separates source facts, player/reader evidence, professional guidance, model inference, and project recommendation;
3. uses the Watchlist and original-source backtrace instead of treating newsletters/vendor benchmarks as canon;
4. maps `PROMPT_AND_AGENT_WORKFLOW`, `SKILL_AUTHORING_AND_EVOLUTION`, and material AI-tool changes into A/B/C/D impact rather than adding a separate AI-news list;
5. preserves the requested four-part structure: A. 메인게임, B. 미니게임, C. 글쓰기, D. 종합 반영안;
6. uses direct competitor, adjacent genre, outside-genre, and failure/mixed-response evidence only when it changes a decision;
7. prevents repeated works from reappearing unless there is new evidence or a new comparison dimension;
8. routes retained findings to Base promotion, existing-owner absorption, project-only action, evidence-only update, test, avoid, or no-change with a concrete target;
9. turns small experiments into `research question → method → evidence type → success criterion`;
10. emits copy-ready GitHub Issue, Codex Goal, and test-checklist wording for retained findings;
11. preserves `NO_CHANGE` when no real improvement survives PR check and adversarial review, after checking smaller owner/test/reference/freshness improvements first.

## External benchmark implications

Current official and practitioner material supports this shape rather than a new broad Skill: customization systems separate always-on instructions, reusable prompts, task Skills and specialist agents; agent-first engineering benefits from repository-visible rules, tests, PR feedback and small continuous cleanup; game-user research chooses observation/interview/analytics/survey from the research question; professional editing separates developmental structure work from later copy/proof work. These are architecture inputs, not universal product rules.

## Adversarial boundaries

- Do not turn the fixed 17-item report shape into 51 mandatory paragraphs when an item is not material; use concise `N/A — reason` entries.
- Do not require benchmark works merely to fill quotas.
- Do not promote project-specific characters, numeric values, story canon, UI layout, or channel strategy to Base.
- Do not infer sales, retention, CTR, ratings, or review sentiment causally without method/context.
- Do not claim human-usability or player-experience evidence from AI analysis, CI, screenshots, or author self-review.
- Do not create a new Skill merely because the report spans multiple domains.
- Do not force repository churn every week.
- Do not duplicate BCP-2026-020’s durable player-experience rules inside the report Template.

## Discoverability and validation

- Link the Template from the Watchlist completion-report section as the single one-hop discovery route.
- Do not add a second high-level Documentation Map entry merely for an output template; the Template itself lists the existing owners it orchestrates.
- Add a focused contract test and run it from the existing Evidence Knowledge workflow.
- No Registry or ACTIVE Skill identity change.
