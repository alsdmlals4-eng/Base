# Periodic Source Scan Checkpoint · 2026-08-22

## Evidence ceiling

This checkpoint records a user-directed ChatGPT review of the due sources from Base Issue #334. Search snippets and secondary summaries were not treated as canon. Material changes were backtraced to original/official sources where they affected a decision. `NO_CHANGE` means no Base owner change was justified by this scan; it does not mean the source contains nothing new.

## Material candidate packets

### YOUTUBE-20260822-METRIC-BOUNDARY — ADOPT
- source: YouTube / TeamYouTube official announcement
- original: https://support.google.com/youtube/thread/433409976
- published: 2026-08-17; effective: 2026-08-24
- claim: public views for non-Short formats move to a first-frame play definition; the older continuity metric remains as `Engaged views` in Advanced Mode. Monetization/YPP continues to use engaged/qualified metrics.
- owner/consumer: YouTube analytics and publication evidence consumers.
- decision: comparisons spanning 2026-08-24 must record the metric-definition boundary. Use Engaged/qualified metrics for continuity rather than treating old/new public view counts as one unchanged series.
- rollback/revisit: revisit if YouTube changes the definition or exposes a replacement continuity metric.

### ANDROID-20260822-API36 — ADOPT / FRESHNESS_REFRESH
- source: Android Developers / Google Play target API requirement
- original: https://developer.android.com/google/play/requirements/target-sdk
- effective: 2026-08-31
- claim: new apps/updates must target Android 16/API 36+ for standard mobile submissions; existing-app discoverability requires API 35+ for newer devices, with platform exceptions documented by Google.
- owner: `PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- decision: existing Base owner already contains this rule; refresh evidence only, no duplicate policy.
- rollback/revisit: recheck at Play policy deadline/version changes.

### GITHUB-20260822-AGENT-PLUGINS — ADAPT / TEST
- source: GitHub Changelog
- original: https://github.blog/changelog/2026-08-12-agent-plugins-1-0-in-vs-code-copilot-cli-and-the-copilot-app/
- claim: Agent Plugins 1.0 is an open package format for reusable skills plus MCP configuration across compatible clients; vendor-specific behavior remains namespaced.
- owner/consumer: Base skill/MCP packaging only when duplicated cross-client packaging is actually present.
- decision: do not migrate existing Base packaging wholesale. TEST only where one skill+MCP pair is maintained for multiple compatible clients.
- rollback/revisit: discard if no real duplicated consumer emerges.

### DOORDASH-20260822-AGENT-GATEWAY — ADAPT / PROMOTION_CANDIDATE
- source: DoorDash Engineering
- original: https://careersatdoordash.com/blog/how-doordash-built-a-centralized-gateway-for-ai-agent-tool-access/
- published: 2026-07-30
- claim: MCP standardizes tool invocation but does not itself solve identity, credential choice, authorization, tool visibility, policy or observability.
- owner/consumer: connector/MCP governance and Implementation Reality Gate.
- decision: preserve task-scoped tool exposure, credential separation, explicit policy/evidence layers. Do not introduce a new gateway product for the solo workflow unless fragmentation becomes a demonstrated recurring cost.
- rollback/revisit: revisit only if tool count/credential routing becomes a repeated operational failure.

### STEAM-20260822-NEXTFEST-OCT — PROJECT_ONLY
- source: Steamworks official documentation
- original: https://partner.steamgames.com/doc/marketing/upcoming_events/nextfest/2026october
- event: 2026-10-19 through 2026-10-26 PT
- claim: eligible games need a public store page and playable public demo; each game can participate in Next Fest once, so timing must match release strategy.
- decision: release-planning candidate only; no Base-wide rule beyond checking the current Steamworks event page near a project's launch window.
- revisit: project-specific release planning.

### GODOT-20260822-472 — REFERENCE_ONLY / VERSION_REVISIT
- source: Godot Engine official release post
- original: https://godotengine.org/article/maintenance-release-godot-4-7-2/
- published: 2026-08-18
- claim: 4.7.2 is a maintenance release; Godot still recommends backups/version control around upgrades.
- decision: do not auto-upgrade active projects solely because a maintenance release exists. Upgrade only after project compatibility/regression evidence.

## Due-source disposition table

| source_id | disposition | scan result |
|---|---|---|
| hada-geeknews | REFERENCE_ONLY | discovery feed only; backtrace material items to originals |
| adobe-premiere | NO_CHANGE | current release-note surface produced no Base-owner change |
| blackmagic-davinci | REFERENCE_ONLY | current training/release workflow remains useful reference, no new owner change |
| frameio | NO_CHANGE | recent workflow updates did not justify a Base rule change |
| gamediscoverco | REFERENCE_ONLY | market/discovery observations remain project/release context |
| godot-proposals | NO_CHANGE | proposals are not implementation canon until accepted/landed |
| reedsy | NO_CHANGE | no material craft/editing change requiring Base owner update |
| steamdb | REFERENCE_ONLY | observational data; official Steamworks preferred for policy/event facts |
| vidiq | REFERENCE_ONLY | secondary creator guidance; official YouTube definitions take priority |
| 80-level | REFERENCE_ONLY | technical-art discovery/reference only |
| deconstructor-of-fun | REFERENCE_ONLY | operator/commercial analysis; no Base-wide rule promotion |
| gameanalytics | REFERENCE_ONLY | vendor analytics guidance; general evidence principles already owned |
| git-scm | NO_CHANGE | current Git reference did not require workflow policy change |
| godot-demo-projects | NO_CHANGE | useful examples, no current reusable-module promotion |
| gpuopen | REFERENCE_ONLY | optimization/tool reference, no current project consumer |
| igda-game-writing | NO_CHANGE | no material update requiring narrative-owner change |
| emily-short | REFERENCE_ONLY | durable interactive-fiction craft reference; no current change |
| game-accessibility-guidelines | NO_CHANGE | existing accessibility owner remains sufficient |
| google-engineering-practices | NO_CHANGE | review/change-author guidance remains stable relative to Base governance |
| level-design-book | REFERENCE_ONLY | durable design reference; no current owner update |
| xbox-accessibility | NO_CHANGE | current guidance remains compatible with existing accessibility rules |
| microsoft-learn | REFERENCE_ONLY | Agent Skills portability supports existing direction; no immediate migration |
| youtube-official | ADOPT | metric-definition boundary candidate above |
| game-developer | REFERENCE_ONLY | recent professional-practice material did not justify Base-wide change |
| how-to-market-a-game | PROJECT_ONLY | marketing cases belong to project/release decisions |
| android-games | ADOPT / FRESHNESS_REFRESH | API 36 deadline corroborates existing Android delivery owner |
| anthropic | REFERENCE_ONLY | recent agent/research material did not justify current Base consumer change |
| github-copilot | ADAPT / TEST | Agent Plugins 1.0 candidate above |
| github-platform-engineering | NO_CHANGE | current Actions/security/ruleset practice already covered by Base governance |
| godot | REFERENCE_ONLY / VERSION_REVISIT | 4.7.2 candidate above |
| google-ai-adk | NO_CHANGE | no material change requiring current Base owner update |
| google-play-policy | ADOPT / FRESHNESS_REFRESH | same API 36 deadline; no duplicate owner |
| openai | REFERENCE_ONLY | current agent/eval updates do not justify an immediate Base architecture change |
| steamworks | PROJECT_ONLY | October Next Fest candidate above |

## Existing Solution First result

- No new broad skill was created.
- Android deadline stays in the existing cross-platform delivery owner.
- Agent Plugins and DoorDash gateway patterns remain bounded candidates, not mandatory architecture.
- YouTube metric-definition boundaries are evidence semantics, not a new analytics product.
- Steam Next Fest remains project release planning, not global canon.

## Completion

All due sources in Issue #334 received a disposition. Only sources actually reviewed in this checkpoint are eligible for `last_successful_scan_at=2026-08-22`. Material-candidate counters are updated conservatively only for watchlist sources with a material candidate (`youtube-official`, `github-copilot`, `godot`, `steamworks`).
