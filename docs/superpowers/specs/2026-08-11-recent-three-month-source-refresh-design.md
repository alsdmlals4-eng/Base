# Recent Three-Month Source Refresh — Design

**Date:** 2026-08-11  
**Research window:** 2026-05-11..2026-08-11  
**Base baseline:** `8e7d85b1b1272002a8086c502a41073888cb3318`

## Goal

Use the current periodic Source system and existing owners to convert recent external changes into bounded Base improvements without creating a broad news/research Skill.

## Existing Solution First

Disposition: `ABSORB_EXISTING_OWNER / LOW_RISK_BOUNDED_UPDATE`.

Reuse:

- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` for source discovery, context extraction, evidence boundaries, and scan/merge gates.
- `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md` as the recurring synthesis consumer.
- `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` + `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md` for Android store readiness.
- `skills/producing-game-development-youtube-videos/SKILL.md` + `templates/game-development-youtube/EPISODE_PACKET.md` for packaging experiments.
- Existing adversarial review and validation Skills; no new ACTIVE Skill, owner, permission, workflow, or repository setting.

Rejected approaches:

1. **One-off news report only** — useful facts would not persist in the execution contract.
2. **New recent-news Skill/agent** — duplicates Watchlist/domain owners and increases routing surface without an independent permission/output/validation boundary.
3. **Copy every recent product feature into Base rules** — overgeneralizes previews, product-specific functions, vendor data, and transient releases.

## Cross-source finding: lifecycle/action state is missing

Recent sources repeatedly require a distinction between publication date and operational state:

- Godot: stable 4.7/4.7.1 alongside 4.8 development builds and release-policy support states.
- Python: 3.15 beta/RC milestones before the planned final release.
- Microsoft/agent products: Skill or agent capabilities may be preview/rolling availability rather than stable cross-surface behavior.
- Adobe Premiere: stable releases and beta-only AI features are documented on separate surfaces.
- Google Play: policy requirements have explicit effective/deadline dates.
- Steam events: participation and submission deadlines create an action window separate from the page publication date.
- GitHub Actions/security: platform protections or approval holds can change workflow execution state without representing a test failure.

The current `SOURCE_CONTEXT_PACKET` records `freshness`, `scope`, and `published_or_updated_at`, but does not explicitly preserve release/policy lifecycle or action timing. This can cause a current-looking source to be treated as stable or immediately actionable when it is preview/proposal/RC, and can also hide deadlines.

### Minimal contract addition

Add these fields to the existing packet and weekly evidence consumer:

```yaml
change_signal_type: RELEASE | MAINTENANCE | PREVIEW | PROPOSAL | DEPRECATION | POLICY_DEADLINE | SECURITY_ADVISORY | PRACTICE_GUIDANCE | OBSERVATIONAL_BENCHMARK | OTHER
availability_or_policy_state: STABLE | GA | PREVIEW | BETA | RC | DEV | PROPOSED | DEPRECATED | RETIRED | POLICY_EFFECTIVE | UNKNOWN
effective_or_deadline_at:
affected_versions_or_surfaces: []
action_window: NOW | BEFORE_DEADLINE | WHEN_ADOPTING | MONITOR_ONLY | REVERIFY_BEFORE_USE
```

These fields classify evidence; they do not grant authority or change the existing T1–T6 tier, disposition, owner, approval, or auto-merge rules.

## Concrete owner absorption 1 — Google Play target API deadline

Official Android/Google Play guidance for 2026 states that starting **2026-08-31**, new apps and app updates submitted to Google Play must target Android 16 / API level 36 or higher, while existing apps need Android 15 / API 35 or higher to remain discoverable to new users on newer Android versions; an extension path to 2026-11-01 may be available for the update deadline.

The current PC/Android Guide was checked on 2026-08-05 but its store readiness section does not capture the target API deadline. Add a volatile policy gate rather than an evergreen universal constant:

```yaml
google_play_target_api:
  checked_at:
  new_app_or_update_required_target_api:
  existing_app_discoverability_target_api:
  effective_at:
  extension_if_available:
  project_target_sdk:
  status: VERIFIED_CURRENT | UPDATE_REQUIRED | EXTENSION_REQUIRED | BLOCKED_UNVERIFIED
```

Official sources:

- https://developer.android.com/google/play/requirements/target-sdk
- https://support.google.com/googleplay/android-developer/answer/11926878

## Concrete owner absorption 2 — YouTube packaging experiment evidence

Current YouTube Help allows eligible creators to A/B test up to three titles/thumbnails or combinations in Studio; the winner is selected using watch-time performance rather than CTR alone. The current Base Skill already supports three packaging candidates and warns against CTR-only causal claims, but it does not preserve the platform experiment setup/result.

Add an optional experiment record to the existing `title-thumbnail-package` mode and Episode Packet:

```yaml
youtube_package_experiment:
  feature_support_checked_at:
  eligibility_status: AVAILABLE | UNAVAILABLE | BLOCKED_UNVERIFIED
  tested_packages: []
  test_started_at:
  test_ended_at:
  platform_result:
  watch_time_result:
  ctr_context:
  confounders:
  decision: KEEP | CHANGE | INSUFFICIENT_SAMPLE | NOT_RUN
```

This does not make A/B testing mandatory and does not let YouTube metrics prove game demand or purchase intent.

Official source:

- https://support.google.com/youtube/answer/16391400

## Evidence retained but not promoted to new rules

- Godot 4.7/4.7.1 and 4.8 dev cadence: validates lifecycle-state fields; no Base engine-version hardcode.
- GitHub Actions/security platform changes: validate execution-state/actionability metadata; current Required Check and fail-closed rules remain stronger and are not weakened.
- Python 3.15 beta/RC milestones: validates RC/beta distinction; no Base Python support-version migration without repository need.
- Yarn Spinner Godot work approaching beta: tool-specific preview evidence only; no new narrative dependency recommendation.
- Deconstructor of Fun, GameDiscoverCo, How To Market A Game, vidIQ: professional/observational context only; no universal KPI or business formula.
- Premiere beta AI Assistant: preview/tool-specific; no required editing workflow change.
- Xbox Accessibility Guidelines: no material three-month change found in the inspected current page; retain as durable static authority.

## Adversarial attack

1. **Freshness bias:** newer does not mean higher evidence authority.
2. **Preview laundering:** beta/RC/proposal/experimental features cannot become stable facts.
3. **Deadline omission:** policy dates must not disappear into generic `freshness` text.
4. **Vendor KPI laundering:** vendor samples cannot become project targets.
5. **Tool-specific overreach:** NLE/agent/engine product features do not define universal Base workflow.
6. **Skill inflation:** current owners already exist; a new recent-news Skill is rejected.
7. **Security overclaim:** platform/AI security checks do not prove runtime security/compliance.
8. **Analytics causality:** A/B package result is a platform observation, not proof of game quality/demand.
9. **Policy staleness:** target API values must keep `checked_at` and reverify-before-release behavior.
10. **Consumer omission:** new packet fields must appear in the weekly synthesis consumer and tests, not only the Watchlist definition.

## Expected changed surfaces

- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md`
- `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`
- `skills/producing-game-development-youtube-videos/SKILL.md`
- `templates/game-development-youtube/EPISODE_PACKET.md`
- existing contract tests only; no new broad Skill or workflow permission.

## Validation

TDD RED first, then minimal implementation. Required validation includes affected contract tests, evidence-knowledge workflow, broader repository `ci-gate`, exact-head comparison, unresolved review-thread check, latest-main check, and post-merge readback if merge gate remains eligible.
