# Producing Game Development YouTube Videos — Learning Log

## 2026-08-10 — External source watchlist bootstrap

### Trigger

Base-wide periodic external-source review expanded into YouTube/video editing and compared current YouTube official Analytics guidance, Blackmagic DaVinci Resolve training, Frame.io review workflow material, vendor creator research, and the existing `producing-game-development-youtube-videos` contract.

### What changed

- Added `STORY_EVIDENCE_EDIT_FIRST` and `VERSIONED_REVIEW` to the workflow.
- Added an edit pass order that keeps story/build evidence and dialogue clarity before graphics, motion, color, and VFX polish.
- Added versioned review findings with `KEEP / CHANGE / REJECT / QUESTION` resolution.
- Expanded Analytics interpretation to preserve traffic source, impressions/CTR, unique viewers, watch time/average view duration, retention key moments, audience segments, external conversion, production cost, and sample limits.
- Clarified that retention drops/spikes/rewatches are observations, not automatic causal explanations.
- Clarified that YouTube official metric definitions outrank third-party creator/vendor benchmark interpretation.
- Updated `templates/game-development-youtube/EPISODE_PACKET.md` and `tests/test_game_development_youtube_skill.py` as synchronized consumers/evidence.

### Adversarial findings

- More editing effects do not imply a better episode; polish can hide a weak viewer promise or missing build evidence.
- CTR, views, retention, and Shorts exposure do not independently prove game quality, purchase intent, or marketing return.
- Vendor benchmark numbers are context-limited unless niche, format, sample, duration, and observation window are preserved.
- Reviewer feedback is evidence, not authority; it must be resolved against project canon, actual build, rights, spoiler, and security boundaries.
- NLE-specific shortcuts, codec settings, and features are tool-specific and must not become Base-wide editing laws.

### Knowledge state

```yaml
repository_contract: EXECUTABLE_EVIDENCE
real_project_video_pilot: NOT_RUN
human_audience_validation: HUMAN_NOT_RUN
conversion_validation: CONVERSION_UNVERIFIED
production_marketing_effectiveness: NOT_PROVEN
```

### Revisit triggers

- YouTube changes metric definitions, Analytics surfaces, or title/thumbnail experiment behavior.
- A real project pilot exposes repeatable edit/review failures not covered by the current packet.
- Multiple real episodes provide enough evidence to refine review categories or production-cost gates.
- A new editing tool is adopted and needs tool-specific implementation guidance without changing the Base-wide storytelling contract.

## 2026-08-11 — Native title/thumbnail package experiment evidence

### Trigger

The 2026-05-11..2026-08-11 source refresh rechecked current YouTube official Help against the existing `title-thumbnail-package` mode. The Skill already generated three truthful package candidates and warned against CTR-only causal claims, but it did not preserve the setup/result of YouTube's native title-and-thumbnail experiment when that feature is actually available.

### What changed

- Kept the existing `title-thumbnail-package` mode and added an optional `youtube_package_experiment` evidence record rather than a new mode or Skill.
- Added current feature-support/eligibility verification before use.
- Preserved tested packages, experiment dates, platform result, watch-time result, CTR context, confounders, and `KEEP | CHANGE | INSUFFICIENT_SAMPLE | NOT_RUN`.
- Synchronized the reusable `EPISODE_PACKET.md` and contract test.

### Adversarial findings

- Native experiment availability can vary by current YouTube surface, account, and video format, so the feature is not mandatory.
- The platform's watch-time-based result must not be rewritten as a CTR-only optimization law.
- A winning title/thumbnail package is evidence about package performance on that experiment; it does not prove game demand, purchase intent, or overall marketing return.
- `UNAVAILABLE`, `BLOCKED_UNVERIFIED`, and `NOT_RUN` are valid outcomes when support, eligibility, or sample evidence is insufficient.

### Knowledge state

```yaml
repository_contract: EXECUTABLE_EVIDENCE
native_platform_experiment_pilot: NOT_RUN
real_project_video_pilot: NOT_RUN
human_audience_validation: HUMAN_NOT_RUN
conversion_validation: CONVERSION_UNVERIFIED
production_marketing_effectiveness: NOT_PROVEN
```

### Revisit triggers

- YouTube changes title/thumbnail experiment eligibility, tested elements, winner criteria, or result semantics.
- A real project runs the native experiment and exposes repeatable fields or confounders missing from the current packet.
- Multiple episodes show that the package experiment should be simplified, expanded, or removed.

## 2026-08-18 — Shorts metric-definition context

### Trigger

Merged PR #520 rechecked first-party YouTube Help and found a bounded comparability risk: from 2025-03-31, Shorts public `views` count starts/replays without the previous minimum-watch-time basis, while the earlier basis remains available in Analytics as `Engaged views`.

### What changed

- Kept the existing YouTube Skill and Analytics mode; no new Skill, mode, KPI or platform policy was created.
- The active `EPISODE_PACKET.md` records content type and the date on which the YouTube metric definition was checked.
- Shorts public views and Engaged views are preserved as separate fields with an explicit `shorts_views_basis`.
- A metric-definition change is treated as a longitudinal-comparison confounder rather than silently joining differently defined values into one time series.
- `tests/test_youtube_metric_definition_context.py` locks the reusable recording contract.

### Reusable lesson

A platform metric label is not sufficient provenance for longitudinal analysis. When the platform changes a definition, record **content format + definition basis + checked/effective date** and keep incompatible historical/current values separate unless an explicit bridge is justified.

This is measurement integrity, not evidence that game demand, audience quality, conversion or marketing effectiveness changed.

### Knowledge state

```yaml
source_authority: YOUTUBE_FIRST_PARTY_HELP
repository_contract: EXECUTABLE_EVIDENCE
real_episode_longitudinal_pilot: NOT_RUN
human_audience_validation: HUMAN_NOT_RUN
conversion_validation: CONVERSION_UNVERIFIED
production_marketing_effectiveness: NOT_PROVEN
```

### Revisit triggers

- YouTube changes Shorts public-view or Engaged-view definitions again.
- Analytics removes, renames or changes the availability of Engaged views.
- A real project must bridge historical Shorts series across definition changes.
- Another publication platform shows the same metric-label/definition drift often enough to justify Base-wide promotion.
