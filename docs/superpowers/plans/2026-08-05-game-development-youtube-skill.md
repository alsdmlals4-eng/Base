# Game Development YouTube Skill Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `superpowers:test-driven-development` task by task. Do not write the active Skill contract before the corresponding failing test exists. Use `superpowers:systematic-debugging` for every unexpected failure and `superpowers:verification-before-completion` before completion claims.

**Goal:** Implement the approved independent Base Skill `producing-game-development-youtube-videos` without absorbing game design, thumbnail image generation, platform review, asset-rights provenance, project-specific branding, or video-editor execution.

**Architecture:** Add one selective specialist Skill plus one reusable Episode Packet template. Register it as an active Base Skill, expose it through current entrypoints, add positive and non-selection behavior cases, and generate the implementation-evidence view. Do not add a Base shared route because no project adapter exists. Publication remains blocked until actual-build, promise-match, rights/rating, spoiler, privacy, security, and CTA gates are satisfied. Analytics conclusions remain sample-limited and must preserve `HUMAN_NOT_RUN`, `CONVERSION_UNVERIFIED`, or `INSUFFICIENT_SAMPLE` where evidence is absent.

**Tech Stack:** Markdown Skill contracts and templates, JSON registries/evaluation sets, Python `unittest`, Base reference-freshness checker, behavior-evaluation checker, deterministic evidence builder, GitHub Actions.

**Approved source:** `BCP-2026-006-game-youtube-devlog-marketing-workflow`

**Approval reference:** `https://github.com/alsdmlals4-eng/Base/pull/167#issuecomment-5192600204`

**Lifecycle boundary:** This plan is documentation only. Active Skill implementation belongs in a new branch and separate PR after this approval-plan PR is merged.

---

## Scope decision

### Add or update during implementation

- `skills/producing-game-development-youtube-videos/SKILL.md`
- `templates/game-development-youtube/EPISODE_PACKET.md`
- `skills/SKILL_REGISTRY.json`
- `skills/SKILL_LEARNING_LOG.md`
- `skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json`
- `skills/SKILL_IMPLEMENTATION_EVIDENCE.json`
- `docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md`
- `docs/generated/BASE_ACTIVE_SKILLS.md`
- `docs/OPERATING_MODEL.md`
- `.github/reference-freshness.json`
- `tests/test_game_development_youtube_skill.py`
- `tests/test_skill_package_integrity.py`
- `tests/test_base_v9_5_skill_operating_refinement.py`
- `tests/test_skill_behavior_evidence_hardening.py`
- `tests/test_skill_implementation_evidence.py`
- `tests/test_skill_behavior_governance_integration.py`
- `tests/test_skill_behavior_adversarial_boundaries.py`

### Explicitly do not change

- `skills/BASE_SHARED_SKILL_ROUTES.json`: no project adapter exists, so no shared route is valid.
- Project repositories or project Google Sheets: Base implementation only.
- `skills/SKILL_BEHAVIOR_EVALS.json`: external model-run evidence remains separate; static coverage cases belong in `SKILL_BEHAVIOR_COVERAGE_EVALS.json`.
- YouTube API upload automation or video-editor automation.
- Project-specific channel names, branding, upload cadence, CTA URLs, KPI thresholds, spoilers, or actual Episode Packets.
- Released Base v9.0.0 lock/snapshot/plugin artifacts.

---

## Task 1: Freeze the approved lifecycle and implementation branch

**Files:**

- Read: `[수정제안서]/BCP-2026-006-game-youtube-devlog-marketing-workflow/PROPOSAL.md`
- Read: `[수정제안서]/BCP-2026-006-game-youtube-devlog-marketing-workflow/DESIGN.md`
- Read: `[수정제안서]/PROPOSAL_REGISTRY.json`
- Read: `skills/managing-base-change-proposals/SKILL.md`

- [ ] **Step 1: Confirm current main and approval state**

Run:

```bash
git fetch origin main
git rev-parse origin/main
python tools/check_base_change_proposals.py
```

Expected:

- current `main` includes the merged BCP proposal;
- BCP-2026-006 is `APPROVED_FOR_IMPLEMENTATION` with the stable approval reference;
- proposal validation passes.

- [ ] **Step 2: Search for duplicate implementation work**

Run:

```bash
gh pr list --repo alsdmlals4-eng/Base --state all --search 'producing-game-development-youtube-videos OR YouTube devlog'
gh issue list --repo alsdmlals4-eng/Base --state all --search 'producing-game-development-youtube-videos OR YouTube devlog'
```

Expected: no separate active implementation PR for the same goal.

- [ ] **Step 3: Create the implementation branch from exact current main**

```bash
git switch -c agent/implement-game-youtube-devlog-skill origin/main
```

- [ ] **Step 4: Record baseline evidence before writes**

```bash
python -m unittest tests.test_skill_package_integrity -v
python tools/check_skill_behavior_evals.py
python tools/build_skill_implementation_evidence.py --check
```

Expected: all pass on baseline. Any pre-existing failure must be reported and separated before implementation.

---

## Task 2: Write failing contract tests first

**Files:**

- Create: `tests/test_game_development_youtube_skill.py`
- Modify: `tests/test_skill_package_integrity.py`
- Modify: `tests/test_base_v9_5_skill_operating_refinement.py`

- [ ] **Step 1: Add a dedicated test that describes the missing package**

Create tests that require:

- the Skill path and Episode Packet path to exist;
- frontmatter name `producing-game-development-youtube-videos`;
- all six approved modes;
- the contract tokens:
  - `PROJECT_CANON_AND_ACTUAL_BUILD_FIRST`
  - `ONE_VIEWER_JOB`
  - `ONE_EPISODE_PROMISE`
  - `ACTUAL_BUILD_EVIDENCE`
  - `TITLE_THUMBNAIL_PROMISE_MATCH`
  - `RIGHTS_RATING_SPOILER_SECURITY_REVIEW`
  - `ONE_PRIMARY_CTA`
  - `ANALYTICS_WITH_SAMPLE_LIMITS`;
- blocking states:
  - `BLOCKED_UNVERIFIED`
  - `PUBLICATION_BOUNDARY_UNVERIFIED`
  - `RIGHTS_OR_RATING_UNVERIFIED`
  - `CONVERSION_UNVERIFIED`
  - `HUMAN_NOT_RUN`;
- analytics decisions:
  - `KEEP`
  - `CHANGE`
  - `STOP`
  - `INSUFFICIENT_SAMPLE`;
- explicit non-ownership of game design, thumbnail generation, platform/asset-rights authority, project KPI thresholds, and editor automation;
- the template’s required evidence, hook, script, shot, packaging, pre-publish review, publish record, analytics, and next-experiment sections.

- [ ] **Step 2: Add package/registry integration assertions**

Extend `tests/test_skill_package_integrity.py` only where the generic checks cannot express the new boundary. Assert that the new Skill is selective, active, and discoverable, and that no project adapter route is required for an unadapted Base specialist.

- [ ] **Step 3: Add an operating-refinement regression**

Extend `tests/test_base_v9_5_skill_operating_refinement.py` to require the new Skill’s description/routing distinction from:

- `analyzing-and-refining-game-concepts`;
- `designing-vertical-slices`;
- `designing-art-prompts-and-technique-cards`;
- `reviewing-and-validating-project-changes`.

- [ ] **Step 4: Run the focused tests and observe RED**

```bash
python -m unittest \
  tests.test_game_development_youtube_skill \
  tests.test_skill_package_integrity \
  tests.test_base_v9_5_skill_operating_refinement -v
```

Expected: FAIL because the Skill, template, registry entry, entrypoint reference, and behavior evidence do not exist yet. Failure messages must name the missing contract rather than fail on malformed test setup.

- [ ] **Step 5: Commit RED tests**

```bash
git add tests/test_game_development_youtube_skill.py \
  tests/test_skill_package_integrity.py \
  tests/test_base_v9_5_skill_operating_refinement.py
git commit -m "test: define game development YouTube skill contract"
```

---

## Task 3: Implement the minimal Skill and Episode Packet

**Files:**

- Create: `skills/producing-game-development-youtube-videos/SKILL.md`
- Create: `templates/game-development-youtube/EPISODE_PACKET.md`

- [ ] **Step 1: Write the minimal Skill frontmatter and responsibility boundary**

Use:

```yaml
---
name: producing-game-development-youtube-videos
description: 게임 프로젝트의 실제 정본·빌드·공개 가능 범위를 바탕으로 개발일지·Shorts·기능 공개·출시 홍보 영상의 채널 구조, 에피소드 약속, 대본·샷, 제목·썸네일 패키지, 공개 전 검증, 게시 후 제한적 Analytics 학습을 설계할 때 사용한다.
---
```

The body must state:

- one independent specialist owner;
- approved six-mode lifecycle;
- required inputs and blocked states;
- outputs and handoffs;
- publication gates;
- sample-limited analytics decisions;
- explicit use/non-use conditions;
- references to the Episode Packet and existing owners;
- no claim that repository tests prove audience or conversion effectiveness.

- [ ] **Step 2: Write the reusable Episode Packet template**

The template must include:

```text
Project canon and actual build evidence
Target viewer and episode job
One-sentence promise
Conflict, change, and visible result
Marketing stage and one primary CTA
Spoiler, confidentiality, security, rights, and rating limits
Hook alternatives
Script
Shot list and capture evidence
Edit beat sheet
Title and thumbnail packages
Description, chapters, pinned comment, playlist, and end screen
Shorts derivatives
Pre-publish adversarial review
Publish record
Analytics precommit
Analytics result and sample limits
KEEP / CHANGE / STOP / INSUFFICIENT_SAMPLE
Learning and next experiment
```

- [ ] **Step 3: Run focused tests**

```bash
python -m unittest tests.test_game_development_youtube_skill -v
```

Expected: package-contract tests that do not depend on registry/evidence turn GREEN; registry/evidence-related assertions may remain RED until later tasks.

- [ ] **Step 4: Refactor only after GREEN**

Remove duplicated wording between the Skill and template. Keep responsibility, gates, status tokens, and output schema unchanged.

- [ ] **Step 5: Commit the package**

```bash
git add skills/producing-game-development-youtube-videos/SKILL.md \
  templates/game-development-youtube/EPISODE_PACKET.md
git commit -m "feat: add game development YouTube production skill"
```

---

## Task 4: Register and expose the Skill without inventing a project route

**Files:**

- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `docs/generated/BASE_ACTIVE_SKILLS.md`
- Modify: `.github/reference-freshness.json`

- [ ] **Step 1: Add one selective specialist Registry entry**

Use these boundaries:

```json
{
  "skill_id": "producing-game-development-youtube-videos",
  "layer": "specialist",
  "discipline": "game-marketing-content-production",
  "path": "skills/producing-game-development-youtube-videos/SKILL.md",
  "status": "ACTIVE",
  "load_by_default": false,
  "trigger_tags": [
    "game-devlog",
    "youtube-development-video",
    "game-development-shorts",
    "feature-reveal-video",
    "release-marketing-video",
    "channel-portfolio",
    "episode-concept",
    "script-shot-plan",
    "title-thumbnail-package",
    "youtube-analytics-review"
  ],
  "use_when": [
    "실제 게임 정본·빌드·공개 범위를 바탕으로 YouTube 개발일지·Shorts·기능 공개·출시 홍보 영상의 기획, 대본·샷, 패키징, 게시 Gate와 제한적 Analytics 학습을 설계한다."
  ],
  "do_not_use_when": [
    "게임 자체의 코어·시스템·밸런스 설계, 썸네일 이미지 한 장의 생성, 플랫폼 심사·에셋 권리 원장 작성, 단순 인코딩·업로드, 또는 프로젝트 정본·실제 빌드·공개 범위가 없는 작업이다."
  ],
  "learning_log": "skills/SKILL_LEARNING_LOG.md",
  "review_triggers": [
    "미구현 기능 과장",
    "제목·썸네일 약속 불일치",
    "실제 빌드 증거 누락",
    "권리·등급·스포일러·보안 검토 누락",
    "특정 창작자 표현 복제",
    "조회수·CTR 단독 성공 판정",
    "작은 표본 과잉 해석",
    "영상 제작의 핵심 개발 잠식",
    "프로젝트 Adapter 없는 shared route 추가"
  ],
  "last_reviewed_at": "2026-08-05",
  "last_reviewed_commit": "<implementation-head-sha-at-final-review>",
  "knowledge_state": "PATTERN"
}
```

Place it near other game-design/production specialist Skills while preserving the current registry’s intentional order.

- [ ] **Step 2: Add a learning-log entry**

Record:

- approved BCP and approval reference;
- why this is independent rather than absorbed;
- why no shared route is added;
- static tests versus real-audience evidence boundary;
- rollback owner and unresolved human validation.

- [ ] **Step 3: Add current-entrypoint discoverability**

Update `docs/OPERATING_MODEL.md` with a compact section that explains:

- when the Skill is selected;
- what existing owners it consumes;
- why actual project Episode Packets remain project-owned;
- why publication and Analytics claims are evidence-gated.

Update `docs/generated/BASE_ACTIVE_SKILLS.md` from the Registry-derived format. Do not alter released lock/snapshot/plugin files.

- [ ] **Step 4: Make the coupled-change configuration truthful**

Update `.github/reference-freshness.json` so the dedicated test is an accepted companion for this Skill contract and Registry change. Do not weaken existing global rules or create a wildcard exemption.

- [ ] **Step 5: Run Registry and reference tests**

```bash
python -m unittest \
  tests.test_skill_package_integrity \
  tests.test_base_v9_5_skill_operating_refinement -v
python tools/check_canonical_reference_freshness.py --base origin/main --head HEAD
```

Expected: GREEN and no demand for `BASE_SHARED_SKILL_ROUTES.json`.

- [ ] **Step 6: Commit Registry and entrypoints**

```bash
git add skills/SKILL_REGISTRY.json \
  skills/SKILL_LEARNING_LOG.md \
  docs/OPERATING_MODEL.md \
  docs/generated/BASE_ACTIVE_SKILLS.md \
  .github/reference-freshness.json \
  tests/test_skill_package_integrity.py \
  tests/test_base_v9_5_skill_operating_refinement.py
git commit -m "feat: register YouTube production skill"
```

---

## Task 5: Add behavior activation and non-selection evidence

**Files:**

- Modify: `skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json`
- Modify: `skills/SKILL_IMPLEMENTATION_EVIDENCE.json`
- Modify: `tests/test_skill_behavior_evidence_hardening.py`
- Modify: `tests/test_skill_implementation_evidence.py`
- Modify: `tests/test_skill_behavior_governance_integration.py`
- Modify: `tests/test_skill_behavior_adversarial_boundaries.py`
- Regenerate: `docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md`

- [ ] **Step 1: Add failing behavior evidence tests**

Require at least these cases:

1. **Primary activation** — user asks for a game-development devlog episode from a verified build, including promise, script, shot list, packaging, publication gates, CTA, and analytics precommit. Expected primary Skill: `producing-game-development-youtube-videos`.
2. **Non-selection** — user asks to rebalance combat or define the game core without any video deliverable. The YouTube Skill must be forbidden; game-concept design remains primary.
3. **Boundary/non-selection** — user asks only for a thumbnail image. The art-prompt/image owner is primary and the YouTube Skill is not primary.
4. **Adversarial publication block** — user asks to advertise an unimplemented feature or publish with unresolved rights/secrets. Expected output contains the correct blocked status and no publication-ready claim.
5. **Analytics restraint** — tiny sample or CTR-only evidence yields `INSUFFICIENT_SAMPLE` or `CONVERSION_UNVERIFIED`, not universal success.

- [ ] **Step 2: Run behavior tests and observe RED**

```bash
python -m unittest \
  tests.test_skill_behavior_evidence_hardening \
  tests.test_skill_implementation_evidence \
  tests.test_skill_behavior_governance_integration \
  tests.test_skill_behavior_adversarial_boundaries -v
python tools/check_skill_behavior_evals.py
```

Expected: FAIL because new coverage and evidence-index entries are absent.

- [ ] **Step 3: Add coverage cases**

Append new unique IDs after the current highest `SBE-COV-*` ID. Preserve schema and status conventions. Use `expected_secondary_skills` only for real support owners and `forbidden_skills` for responsibility-boundary proof.

- [ ] **Step 4: Add implementation-evidence index entry**

Add an entry for the new Skill with executable evidence pointing to:

- `tests/test_game_development_youtube_skill.py`
- relevant behavior-governance/adversarial tests;
- optionally the contract path as `CONTRACT` evidence.

Do not mark model, runtime, audience, or conversion validation as run.

- [ ] **Step 5: Generate and check evidence Markdown**

```bash
python tools/build_skill_implementation_evidence.py
python tools/build_skill_implementation_evidence.py --check
python tools/check_skill_behavior_evals.py
```

Expected:

- evidence Markdown shows the new active Skill;
- primary and non-selection behavior are PASS;
- evidence class is executable repository evidence;
- external model behavior run remains its actual current state, not fabricated.

- [ ] **Step 6: Run all behavior governance tests**

```bash
python -m unittest \
  tests.test_skill_behavior_evidence_hardening \
  tests.test_skill_implementation_evidence \
  tests.test_skill_behavior_governance_integration \
  tests.test_skill_behavior_adversarial_boundaries -v
```

Expected: GREEN.

- [ ] **Step 7: Commit behavior evidence**

```bash
git add skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json \
  skills/SKILL_IMPLEMENTATION_EVIDENCE.json \
  docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md \
  tests/test_skill_behavior_evidence_hardening.py \
  tests/test_skill_implementation_evidence.py \
  tests/test_skill_behavior_governance_integration.py \
  tests/test_skill_behavior_adversarial_boundaries.py
git commit -m "test: cover YouTube skill routing boundaries"
```

---

## Task 6: Run the full adversarial and regression gate

**Files:**

- Review all implementation-branch changes.
- Update only evidence timestamps/commit references that are part of the approved contract.

- [ ] **Step 1: Run focused contract tests**

```bash
python -m unittest \
  tests.test_game_development_youtube_skill \
  tests.test_skill_package_integrity \
  tests.test_base_v9_5_skill_operating_refinement -v
```

Expected: GREEN.

- [ ] **Step 2: Run behavior and generated-evidence checks**

```bash
python tools/check_skill_behavior_evals.py
python tools/build_skill_implementation_evidence.py --check
python -m unittest \
  tests.test_skill_behavior_evidence_hardening \
  tests.test_skill_implementation_evidence \
  tests.test_skill_behavior_governance_integration \
  tests.test_skill_behavior_adversarial_boundaries -v
```

Expected: GREEN.

- [ ] **Step 3: Run proposal and reference propagation checks**

```bash
python tools/check_base_change_proposals.py
python tools/check_canonical_reference_freshness.py --base origin/main --head HEAD
```

Expected: GREEN; no missing coupled consumer and no invalid active implementation against the approved BCP.

- [ ] **Step 4: Run full regression**

```bash
python -m unittest discover -s tests -v
```

Expected: all tests pass. Record the exact count; do not reuse a count from another commit.

- [ ] **Step 5: Run adversarial review attacks**

Check explicitly:

- Can the Skill be selected for pure game-system design? It must not.
- Can it claim a feature is implemented without build evidence? It must not.
- Can it publish with unresolved rights, rating, spoilers, private data, or secrets? It must not.
- Can it copy an identifiable creator package? It must not.
- Can it call high CTR or Shorts views proof of game demand? It must not.
- Can it impose universal KPI thresholds? It must not.
- Can it create a project shared route without an adapter? It must not.
- Can repository tests be described as human audience validation? They must not.
- Can video production consume the game-development schedule without a budget response? It must produce reduce/postpone/stop guidance.

Record unresolved real-world states:

```yaml
model_behavior_evaluation: NOT_RUN unless actually run
real_project_video_pilot: NOT_RUN
human_audience_validation: HUMAN_NOT_RUN
conversion_validation: CONVERSION_UNVERIFIED
production_marketing_effectiveness: NOT_PROVEN
```

- [ ] **Step 6: Review exact diff and scope**

```bash
git diff --check
git diff --stat origin/main...HEAD
git diff --name-only origin/main...HEAD
```

Expected: only approved implementation files; no project repository, Google Sheet, release lock, plugin, or unrelated Skill changes.

---

## Task 7: Open the implementation PR and preserve evidence

- [ ] **Step 1: Push the implementation branch**

```bash
git push -u origin agent/implement-game-youtube-devlog-skill
```

- [ ] **Step 2: Open a Draft PR**

The PR body must include:

- BCP ID and approval reference;
- independent Skill boundary;
- explicit no-shared-route decision;
- test-first commits and RED/GREEN evidence;
- exact changed-file inventory;
- exact focused and full regression results;
- generated evidence status;
- adversarial attacks and outcomes;
- unresolved human/model/runtime states;
- rollback unit.

- [ ] **Step 3: Verify exact-head CI and review threads**

Do not mark ready or merge until:

- all required workflows are successful on the current head SHA;
- no unresolved review thread remains;
- current `main` has not drifted or the branch has been resynchronized and reverified;
- changed-file scope still matches the approved plan.

- [ ] **Step 4: Merge only after verification**

Use the repository’s accepted merge method with expected-head protection. After merge, use a separate lifecycle update to set BCP-2026-006 to `IMPLEMENTED` and record the implementation PR URL. Do not combine the post-merge state claim with unmerged implementation work.

---

## Rollback unit

Revert the implementation PR as one unit. This removes:

- the active Skill package;
- the Episode Packet template;
- Registry/entrypoint/evaluation/evidence entries;
- dedicated tests and generated current views.

Do not delete project-owned Episode Packets or previously collected Analytics. Preserve those as project evidence with their original verification states.

## Completion claim boundary

Repository implementation may be reported as complete only when exact-head CI and required tests pass. The following remain separate and cannot be inferred from repository success:

- actual video quality;
- audience retention;
- click-through performance;
- demo, wishlist, funding, or purchase conversion;
- channel portfolio effectiveness;
- production-time return on investment.
