# Recent Three-Month Source Refresh Implementation Plan

> **For Base maintainers:** Execute with TDD, Existing Solution First, repository-wide adversarial review, and exact-head CI. Do not create a new ACTIVE Skill.

**Goal:** Convert material 2026-05-11..2026-08-11 external-source changes into reusable Base contracts while preserving source authority and avoiding trend/news overreach.

**Architecture:** Keep `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` as the source/context owner. Add lifecycle/actionability fields there and propagate them only to the weekly evidence consumer. Apply two bounded owner updates: Google Play target-API readiness in the PC/Android delivery owner, and YouTube title/thumbnail A/B experiment evidence in the existing video Skill/Packet.

**Tech:** Markdown/YAML contract text, Python `unittest` repository contracts, GitHub Actions validation.

---

## Task 1: Lock source lifecycle/actionability behavior with RED tests

**Files:**
- Modify: `tests/test_periodic_external_source_watchlist.py`
- Modify: `tests/test_weekly_work_improvement_review.py`

**RED contract:** require `change_signal_type`, `availability_or_policy_state`, `effective_or_deadline_at`, `affected_versions_or_surfaces`, and `action_window` in the Watchlist context packet and weekly evidence card. Require explicit guardrails that preview/RC/proposal does not become stable evidence and deadline-bearing sources preserve action timing.

Run the affected tests and confirm failure is due only to the missing contract.

## Task 2: Implement source lifecycle/actionability fields

**Files:**
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- Modify: `templates/research/WEEKLY_WORK_IMPROVEMENT_REVIEW.md`

Add the minimal fields from the design spec, keep evidence tier/disposition/owner/auto-merge authority unchanged, and add adversarial questions for preview laundering and deadline omission.

Run the Task 1 tests to GREEN.

## Task 3: Lock Google Play target-API readiness with RED test

**Files:**
- Modify: `tests/test_pc_android_cross_platform_delivery.py`

Require the Guide/Profile to preserve:
- current official check date,
- 2026-08-31 effective deadline,
- Android 16 / API 36 for new apps/updates,
- Android 15 / API 35 discoverability floor for existing apps,
- extension path as conditional/current-source verified,
- project `target_sdk` status field,
- reverify-before-submission guardrail.

Run the focused test and confirm expected RED.

## Task 4: Implement Google Play volatile policy gate

**Files:**
- Modify: `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- Modify: `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`

Add a dated `google_play_target_api` readiness section, official source links, and adversarial stale-policy warning. Keep values explicitly volatile and tied to 2026-08-11 verification, not evergreen Base constants.

Run focused PC/Android tests to GREEN.

## Task 5: Lock YouTube packaging experiment evidence with RED tests

**Files:**
- Modify: `tests/test_game_development_youtube_skill.py`

Require optional `youtube_package_experiment` support in both Skill and Episode Packet, including feature-support check, eligibility, tested packages, dates, platform result, watch-time result, CTR context, confounders, and `KEEP | CHANGE | INSUFFICIENT_SAMPLE | NOT_RUN`. Require no interpretation as game demand/purchase intent and no mandatory experiment when unavailable.

Run the focused test and confirm expected RED.

## Task 6: Implement YouTube A/B package evidence

**Files:**
- Modify: `skills/producing-game-development-youtube-videos/SKILL.md`
- Modify: `templates/game-development-youtube/EPISODE_PACKET.md`

Add the optional experiment record under the existing title-thumbnail package mode. Preserve the existing actual-build promise, rights, sample-limit, and causal guardrails. Record that the current official experiment optimizes by watch-time result, not CTR alone, and reverify feature eligibility/support before use.

Run YouTube Skill tests to GREEN.

## Task 7: Full affected validation and adversarial audit

Run:
- focused source tests
- focused PC/Android tests
- focused YouTube tests
- evidence knowledge workflow contract tests
- canonical/reference freshness tests as selected by repository CI

Adversarially inspect:
- changed files
- owner sources
- weekly/template consumers
- untouched expected consumers
- generated/registry drift
- same-goal PRs
- current `main`

Reject any new Skill/owner/permission/schema expansion that is not needed by the three bounded changes.

## Task 8: Draft PR, exact-head CI, and merge gate

Create a draft PR with:
- 3-month research window and material sources
- RED→GREEN evidence
- Existing Solution First disposition
- retained `REFERENCE_ONLY/NO_CHANGE` findings
- adversarial attack results

Before merge require:
- no same-goal open PR conflict
- reviewed head equals current head
- branch includes latest `main`
- required workflows succeed and final `ci-gate` succeeds
- unresolved review threads = 0
- no protected semantic change / BCP state

If all remain true, mark ready and use repository-approved squash merge with expected head SHA. Re-read `main` after merge and do not report unrun validation as PASS.
