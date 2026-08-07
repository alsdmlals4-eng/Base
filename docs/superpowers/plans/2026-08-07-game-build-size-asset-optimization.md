# Game Build Size and Asset Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable Base contract for minimizing Windows PC and Android game delivery size while preserving visual/audio quality, runtime performance, and patch/update efficiency.

**Architecture:** Add one focused knowledge Guide rather than a new broad Skill. Existing PC/Android delivery, art/asset, routing, evidence, and validation owners consume the Guide; project-specific numbers remain in `PC_ANDROID_DELIVERY_PROFILE.md`. Routing changes are minimal and only extend existing owners where tests prove discoverability gaps.

**Tech Stack:** Markdown contracts, JSON Skill Registry/behavior fixtures when required, Python unittest/Base validation tools, Git/GitHub PR workflow.

## Global Constraints

- Do not add a new broad optimization Skill.
- Preserve existing `package_and_download_size` as a compatibility field.
- Do not put project-specific fixed MB, texture resolution, bitrate, or font-count targets into Base common policy.
- Optimize delivered/installed/runtime/update bytes without accepting unverified visual, audio, loading, memory, CPU/GPU, thermal, battery, or patch regressions.
- Share source policy and quality classes, but permit platform-specific texture formats, resolutions, packaging, and delivery.
- Font policy minimizes duplicated families/weights/files without breaking CJK, emoji, localization, fallback metrics, or licensing.
- Android delivery must distinguish served download, installed size, first-launch/first-session download, typical content, and optional content.
- Windows delivery must distinguish compressed download, installed size, normal/worst patch size, temporary patch disk, and runtime memory.
- Steam patch locality and Android App Bundle/Play Asset Delivery are evidence-backed optional delivery mechanisms, not universal mandates.
- Base documentation changes must not claim real Godot build, Android-device, Steam upload, Google Play delivery, or human quality evidence that was not run.
- Baseline design spec: `docs/superpowers/specs/2026-08-07-game-build-size-asset-optimization-design.md`.

---

## File Structure

**Create**
- `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` — sole reusable knowledge authority for build-size/asset optimization method, measurements, asset policies, delivery trade-offs, and quality gates.

**Modify**
- `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` — consume the new Guide from quality/performance/release gates without duplicating its detailed rules.
- `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md` — hold project-specific size budgets, measured evidence, asset breakdown, accepted/rejected optimizations, and unresolved gaps.
- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` — extend Asset Specification with size/quality/import-profile fields and require actual in-game quality evidence.
- `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md` — register current official Godot, Android/Google Play, Steam evidence used by the Guide.
- `docs/knowledge/game-development/README.md` — add the new Guide to the game-development knowledge routing table/index.
- `START_HERE.md` — make game build/package/download/asset optimization discoverable in one routing step.
- `docs/DOCUMENTATION_MAP.md` — map the new Guide to its exact responsibility and consumers.

**Modify only if failing routing coverage proves a gap**
- `skills/SKILL_REGISTRY.json` — add only relevant trigger tags to existing owners; do not create a new Skill entry.
- `skills/SKILL_BEHAVIOR_EVALS.json` — add/adjust fixtures only when Registry routing changes are required.
- `docs/generated/BASE_ACTIVE_SKILLS.md` and coverage artifacts — regenerate only through the repository's existing generators when Registry changes require it; do not hand-edit generated files.

**Validation entrypoint**
- `tools/run_local_validation.py` — run unchanged using the trusted history baseline required by current Base policy.

---

### Task 1: Add the reusable build-size and asset-optimization Guide

**Files:**
- Create: `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`
- Reference: `docs/superpowers/specs/2026-08-07-game-build-size-asset-optimization-design.md`

**Interfaces:**
- Consumes: existing Base evidence hierarchy, PC/Android delivery boundaries, Art/Asset Specification conventions, adversarial/validation ownership.
- Produces: canonical sections/field names referenced by Tasks 2–4: `windows_size_budget`, `android_size_budget`, `asset_size_breakdown`, `quality_class`, `font_profile`, `texture_profile`, `audio_profile`, `optimization_change`.

- [ ] **Step 1: Write a failing contract check before creating the Guide**

Run from repository root:

```bash
python - <<'PY'
from pathlib import Path
p = Path('docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md')
assert p.exists(), 'missing optimization guide'
text = p.read_text(encoding='utf-8')
for token in [
    'download', 'installed', 'runtime', 'patch',
    'font_profile', 'texture_profile', 'audio_profile',
    'quality_class', 'optimization_change',
    'Steam', 'Play Asset Delivery', 'rollback'
]:
    assert token in text, token
PY
```

Expected: FAIL with `missing optimization guide`.

- [ ] **Step 2: Create the Guide from the approved design**

The Guide must contain these top-level responsibilities in this order:

```text
Purpose and non-goals
Measurement model
Optimization order
Quality classes
Font policy
Texture/image policy
Audio policy
Video/mesh/animation policy
Duplicate/unused asset gate
Windows/Steam packaging and patch locality
Android/Google Play delivery partitioning
Quality/runtime/delivery regression gate
Optimization decision record
Project application boundary
Official evidence and revalidation conditions
```

Use the approved field names verbatim. Keep project-specific targets blank/by-profile rather than inventing values.

- [ ] **Step 3: Run the contract check again**

Expected: PASS.

- [ ] **Step 4: Run a prohibited-fixed-default scan**

```bash
python - <<'PY'
from pathlib import Path
text = Path('docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md').read_text(encoding='utf-8')
for prohibited in ['모든 텍스처는 1024', '무조건 500MB', '폰트는 반드시 1개', '모든 오디오는 동일 bitrate']:
    assert prohibited not in text, prohibited
PY
```

Expected: PASS.

- [ ] **Step 5: Commit Task 1**

```bash
git add docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md
git commit -m "docs: add game build size optimization guide"
```

---

### Task 2: Extend the project delivery profile and existing PC/Android consumer

**Files:**
- Modify: `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`
- Modify: `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`

**Interfaces:**
- Consumes: Task 1 field names and measurement semantics.
- Produces: project-specific `build_size_and_asset_optimization` record and PC/Android routing link to the Guide.

- [ ] **Step 1: Write a failing profile/consumer check**

```bash
python - <<'PY'
from pathlib import Path
profile = Path('templates/planning/PC_ANDROID_DELIVERY_PROFILE.md').read_text(encoding='utf-8')
guide = Path('docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md').read_text(encoding='utf-8')
assert 'build_size_and_asset_optimization:' in profile
for token in ['windows_size_budget:', 'android_size_budget:', 'asset_size_breakdown:', 'accepted_optimizations:', 'rejected_optimizations:', 'patch_evidence:']:
    assert token in profile, token
assert 'GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md' in guide
assert 'package_and_download_size:' in profile, 'compatibility field removed'
PY
```

Expected: FAIL before the edits.

- [ ] **Step 2: Extend `PC_ANDROID_DELIVERY_PROFILE.md`**

Keep the existing `performance_budget.package_and_download_size` field. Add this sibling project evidence block:

```yaml
build_size_and_asset_optimization:
  baseline_build:
  target_budget_status:
  windows_size_budget:
  android_size_budget:
  asset_size_breakdown:
  top_contributors:
  font_profile:
  texture_profiles:
  audio_profiles:
  delivery_partition:
  duplicate_unused_audit:
  accepted_optimizations:
  rejected_optimizations:
  visual_quality_evidence:
  audio_quality_evidence:
  runtime_evidence:
  patch_evidence:
  unresolved:
```

Add text stating that project-specific MB/quality targets live here and require measured-state labels rather than being inherited from Base.

- [ ] **Step 3: Update the cross-platform Guide as a consumer, not a duplicate authority**

Add a concise link from performance/quality and release-validation sections to `GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`. State that Windows and Android may use different import/delivery profiles while preserving the shared core and visual intent.

- [ ] **Step 4: Run the profile/consumer check again**

Expected: PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add templates/planning/PC_ANDROID_DELIVERY_PROFILE.md docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md
git commit -m "docs: add platform build size evidence profile"
```

---

### Task 3: Connect Art/Asset Specification and official evidence

**Files:**
- Modify: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- Modify: `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`

**Interfaces:**
- Consumes: Task 1 quality classes and platform import profiles.
- Produces: asset-level planning fields and T1 evidence records backing Godot/Android/Steam-specific statements.

- [ ] **Step 1: Write a failing asset/evidence check**

```bash
python - <<'PY'
from pathlib import Path
art = Path('docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md').read_text(encoding='utf-8')
src = Path('docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md').read_text(encoding='utf-8')
for token in ['size_quality_class:', 'platform_import_profile:', 'quality_validation:']:
    assert token in art, token
for token in [
    'importing_images.html',
    'importing_audio_samples.html',
    'gui_using_fonts.html',
    'developer.android.com/games/optimize/game-size',
    'asset-delivery/texture-compression',
    'asset-delivery',
    'partner.steamgames.com/doc/sdk/uploading'
]:
    assert token in src, token
PY
```

Expected: FAIL before edits.

- [ ] **Step 2: Extend Asset Specification minimally**

Add fields without replacing existing dimensions/export/import/performance fields:

```yaml
size_quality_class:
platform_import_profile:
quality_validation:
```

State that the optimization Guide owns byte/performance trade-offs while Art Direction continues to own visual intent and readability.

- [ ] **Step 3: Add official evidence records to the source catalog**

Register current official sources as `T1_PRIMARY_OFFICIAL`, with `checked_at: 2026-08-07`, topic/use/limits/revalidation fields:

```text
Godot stable: importing images
Godot stable: importing audio samples
Godot stable: using fonts
Android Developers: Reduce game size
Android Developers: Target texture compression formats in Android App Bundles
Android Developers: Play Asset Delivery
Steamworks: Uploading to Steam / SteamPipe Content System
```

Do not promote Unity/Unreal cross-engine comparison sources to mandatory project rules; keep them reference-only if included.

- [ ] **Step 4: Run the asset/evidence check again**

Expected: PASS.

- [ ] **Step 5: Commit Task 3**

```bash
git add docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md
git commit -m "docs: connect asset specifications to size quality gates"
```

---

### Task 4: Make the Guide discoverable without adding a new Skill

**Files:**
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/knowledge/game-development/README.md`
- Conditional modify: `skills/SKILL_REGISTRY.json`
- Conditional modify: `skills/SKILL_BEHAVIOR_EVALS.json`
- Conditional regenerate: `docs/generated/BASE_ACTIVE_SKILLS.md` and existing registry-derived artifacts

**Interfaces:**
- Consumes: Task 1 canonical Guide path.
- Produces: cold-start one-hop discovery and, only if necessary, automatic routing coverage through existing owners.

- [ ] **Step 1: Write a failing discoverability check**

```bash
python - <<'PY'
from pathlib import Path
path = 'docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md'
start = Path('START_HERE.md').read_text(encoding='utf-8')
docmap = Path('docs/DOCUMENTATION_MAP.md').read_text(encoding='utf-8')
knowledge = Path('docs/knowledge/game-development/README.md').read_text(encoding='utf-8')
assert path in start
assert path in docmap
assert path in knowledge
PY
```

Expected: FAIL before routing edits.

- [ ] **Step 2: Add one-hop routing references**

Add one concise route for requests such as game build size/package size/download size/asset optimization. Do not copy detailed optimization rules into routing files.

- [ ] **Step 3: Audit existing Registry coverage before editing it**

Run:

```bash
python tools/check_skill_system_coverage.py
```

Then inspect existing owner triggers for performance/platform/art/validation. If current triggers already route a representative `game package/download size optimization` request to an existing owner, leave Registry untouched.

- [ ] **Step 4: If and only if routing is not discoverable, add minimal existing-owner trigger tags**

Permitted additions are trigger-only, for example:

```text
build-size
package-size
download-size
asset-optimization
texture-compression
font-size-optimization
audio-size-optimization
steam-patch-size
play-asset-delivery
```

Do not add a new Skill ID. If Registry changes, add/update a behavior fixture proving the representative request routes to the intended existing owner and does not create a broad optimization owner.

- [ ] **Step 5: Regenerate derived Skill views only when Registry changed**

Use the repository's existing generator/check command; never hand-edit generated files. Confirm `tools/build_base_v9_artifacts.py --check` reports no stale generated contract after regeneration.

- [ ] **Step 6: Run discoverability and routing checks**

```bash
python - <<'PY'
from pathlib import Path
path = 'docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md'
for f in ['START_HERE.md', 'docs/DOCUMENTATION_MAP.md', 'docs/knowledge/game-development/README.md']:
    assert path in Path(f).read_text(encoding='utf-8'), f
registry = Path('skills/SKILL_REGISTRY.json').read_text(encoding='utf-8')
assert '"skill_id":"game-build-size-optimization"' not in registry
assert '"skill_id": "game-build-size-optimization"' not in registry
PY
python tools/check_skill_system_coverage.py
```

Expected: PASS.

- [ ] **Step 7: Commit Task 4**

```bash
git add START_HERE.md docs/DOCUMENTATION_MAP.md docs/knowledge/game-development/README.md skills/SKILL_REGISTRY.json skills/SKILL_BEHAVIOR_EVALS.json docs/generated/BASE_ACTIVE_SKILLS.md
git commit -m "docs: route build size optimization through existing owners"
```

Before committing, remove unchanged conditional files from the index so the commit contains only actual changes.

---

### Task 5: Adversarial review, full Base validation, and PR-ready evidence

**Files:**
- Review all changed files from Tasks 1–4.
- No new production file is required unless a validated finding demands a minimal correction.

**Interfaces:**
- Consumes: complete branch diff.
- Produces: regression-checked, PR-ready branch with explicit unverified runtime/store boundaries.

- [ ] **Step 1: Attack the completed change against the approved design**

Check explicitly for these failure modes:

```text
new broad Skill accidentally added
fixed project MB/resolution/bitrate defaults leaked into Base
font-one-file rule breaks CJK/fallback
PC and Android forced to identical texture format/profile
mipmaps globally disabled
maximum compression accepted without CPU/thermal checks
initial download optimized by hiding mandatory first-session downloads
Steam install size treated as equivalent to patch size
unused assets deleted without dynamic-reference uncertainty state
quality evidence claimed without actual captures/listening/device runs
existing package_and_download_size compatibility field removed
routing docs duplicate the full Guide and create a second authority
```

Classify findings using Base adversarial states and fix only validated in-scope `MUST_FIX`/approved `SHOULD_FIX` items.

- [ ] **Step 2: Run focused contract checks from Tasks 1–4**

Expected: all PASS.

- [ ] **Step 3: Run full unit and static validation**

Use the branch's trusted history baseline from the approved design (`4f98f968a377f7b6a11aafa4fc94d11bddbebedc`) unless current Base policy requires a newer trusted-history commit after rebasing:

```bash
python tools/run_local_validation.py --trusted-history-commit 4f98f968a377f7b6a11aafa4fc94d11bddbebedc
```

This executes the repository's unittest discovery, CI topology check, Base v9 artifact check, integrity check, Skill coverage check, `git diff --check`, and `git fsck --strict`.

Expected: exit code 0.

- [ ] **Step 4: Verify exact branch scope**

```bash
git diff --name-status 4f98f968a377f7b6a11aafa4fc94d11bddbebedc...HEAD
git diff --check 4f98f968a377f7b6a11aafa4fc94d11bddbebedc...HEAD
```

Expected: only the approved design/plan plus implementation consumer/evidence files; no project-specific Godot assets or unrelated Base refactors.

- [ ] **Step 5: Record unverified boundaries in final review**

Explicitly state:

```text
Base contract/static validation: verified only if commands passed
real Godot project asset recompression: NOT_RUN
Windows packaged build size: NOT_RUN at Base level
Android physical-device size/performance: DEVICE_NOT_RUN at Base level
Steam upload/patch preview: NOT_RUN at Base level
Google Play served-size/PAD behavior: NOT_RUN at Base level
human visual/audio quality comparison: HUMAN_NOT_RUN at Base level
```

- [ ] **Step 6: Commit any review fixes separately**

```bash
git add <only validated review-fix files>
git commit -m "fix: harden build size optimization contracts"
```

Skip this commit when adversarial review finds no change-worthy defect.

- [ ] **Step 7: Prepare PR**

PR title:

```text
feat: add game build size and asset optimization contracts
```

PR body must summarize:

```text
approved design and scope
new Guide authority
existing-owner integration; no new broad Skill
font/texture/audio/delivery/patch quality gates
official evidence sources
validation commands and exact result
runtime/device/store/human evidence not run at Base level
rollback boundary
```

Do not merge until required checks and Base PR review policy pass.

---

## Plan Self-Review

- Spec coverage: measurement model, optimization order, quality classes, fonts, textures, audio, video/mesh/animation, duplicate/unused gate, Steam patching, Android delivery, project profile, routing, official evidence, quality/runtime/delivery regression, and rollback all map to Tasks 1–5.
- Placeholder scan: no TBD/TODO/“implement later” instructions remain; all conditional Registry work has an explicit failing-evidence gate.
- Naming consistency: `build_size_and_asset_optimization`, `windows_size_budget`, `android_size_budget`, `asset_size_breakdown`, `font_profile`, `texture_profile(s)`, `audio_profile(s)`, and `optimization_change` match the approved design.
- Scope check: one cohesive cross-cutting documentation/contract feature; no independent product subsystem is being implemented here.
