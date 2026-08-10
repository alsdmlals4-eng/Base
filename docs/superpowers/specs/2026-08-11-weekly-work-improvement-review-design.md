# Weekly Work Improvement Review — Design

## Problem

Base already owns periodic external-source discovery, game/player-experience evidence, serial-fiction craft, prompt/Skill placement, and adversarial review. BCP-2026-020 also extracted durable player-experience gates from the 2026-08-10 weekly report. What is still missing is a reusable, non-canonical synthesis surface that turns those existing owners into a consistent weekly A/B/C/D improvement review without copying the same rules into a new broad Skill.

## Existing Solution First

Disposition: `ABSORB_EXISTING_OWNER / LOW_RISK_BOUNDED_UPDATE`.

Keep current owners:

- source discovery and evidence authority: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
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

1. starts with current Base/project truth and previous-report delta, not news collection;
2. separates source facts, player/reader evidence, professional guidance, model inference, and project recommendation;
3. uses the Watchlist and original-source backtrace instead of treating newsletters/vendor benchmarks as canon;
4. preserves the requested four-part structure:
   - A. 메인게임
   - B. 미니게임
   - C. 글쓰기
   - D. 종합 반영안
5. requires direct competitor + adjacent genre + outside-genre reference only when they change a decision, and includes failure/mixed-response evidence when available;
6. prevents repeated works from reappearing unless there is new evidence or a new comparison dimension;
7. makes every recommendation choose `BASE_PROMOTION_CANDIDATE`, `PROJECT_ONLY`, `EVIDENCE_ONLY`, `TEST`, `AVOID`, or `NO_CHANGE` and names the concrete consumer/project;
8. turns small experiments into `research question → method → evidence type → success criterion`, because observation/interview/analytics/survey answer different questions;
9. emits copy-ready GitHub Issue / Codex Goal / test-checklist wording only for retained findings;
10. preserves `NO_CHANGE` when no real improvement survives PR check and adversarial review, while still looking for owner absorption, stale references, tests, counterexamples, and small validation-contract improvements first.

## Adversarial boundaries

- Do not turn the fixed 17-item report shape into 51 mandatory paragraphs when an item is not material; use concise `N/A — reason` entries.
- Do not require three benchmark works merely to fill quotas; comparison selection is decision-driven.
- Do not promote project-specific characters, numeric values, story canon, UI layout, or channel strategy to Base.
- Do not infer sales, retention, CTR, ratings, or review sentiment causally without method/context.
- Do not claim `HUMAN_USABILITY_EVIDENCE` or `PLAYER_EXPERIENCE_EVIDENCE` from AI analysis, CI, screenshots, or author self-review.
- Do not create a new Skill merely because the report spans multiple domains.
- Do not force repository churn every week.

## Discoverability and validation

- Link the template from the Watchlist completion-report section.
- Add the template to `docs/DOCUMENTATION_MAP.md` as a reusable research/report surface, not a new canon owner.
- Add a focused contract test and run it from the existing Evidence Knowledge workflow.
- No Registry, ACTIVE Skill identity, security permission, schema, or release-lock change.
