# P09 · Content, Narrative & Publication — Optimization Audit

```yaml
part_id: P09
baseline_sha: df8ef644d30fc96456da23a5157e5efb61b620bb
branch: opt/base-part-P09-content-integrity
audit_date: 2026-08-19
scope: P09_OWNED_AND_READ_ONLY_DEPENDENCIES
runtime_fragmentation: false
```

## 1. Part responsibility reconstruction

P09 owns reusable content-production craft and evidence for two distinct outward-facing workflows:

1. **Serial Fiction** — canon/adaptation boundary, arc/episode design, POV/voice, character/opponent integrity, scene prose, pacing/payoff, reader-feedback revision.
2. **Game-development YouTube** — project/build evidence, viewer/episode promise, script/shot/edit/package/publish evidence, sample-limited analytics learning.

Game-specific world/story fit remains a P04 dependency, visual production remains P05, platform/release/rights authority remains P07, and global Skill routing/Manifest remains CP0.

The Part is removed incorrectly if either of these fails:

- content can silently drift from project canon/actual build;
- voice/character/continuity craft loses a reusable owner;
- YouTube packaging can overclaim unimplemented features or infer causality from weak analytics;
- publication evidence loses provenance, rights/rating/spoiler/security boundaries.

## 2. Current canonical surfaces

### Active Skills

| Skill | Registry state | Primary responsibility | Disposition |
|---|---|---|---|
| `developing-and-revising-serial-fiction` | ACTIVE, specialist, load-by-default=false | serial-fiction planning/drafting/revision | **KEEP** |
| `producing-game-development-youtube-videos` | ACTIVE, specialist, load-by-default=false | game-development YouTube production/publication evidence | **KEEP** |

The two Skills are materially distinct. Merging them would combine fiction craft with marketing/publication analytics and increase routing/context ambiguity.

### Important guides/templates/tests actually consumed

- `docs/knowledge/serial-fiction/**`
- `templates/game-development-youtube/EPISODE_PACKET.md`
- `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`
- `tests/test_serial_fiction_discipline.py`
- `tests/test_game_development_youtube_skill.py`
- `tests/test_youtube_metric_definition_context.py`

## 3. MUST_FIX finding — Manifest ownership path drift

The P09 Manifest currently declares these write paths:

```text
docs/knowledge/writing/**
templates/writing/**
templates/game-dev-youtube/**
```

Repository readback shows:

- `docs/knowledge/writing/**` does not exist; the active serial-fiction knowledge owner is `docs/knowledge/serial-fiction/**`.
- `templates/game-dev-youtube/**` does not exist; the active YouTube packet is `templates/game-development-youtube/EPISODE_PACKET.md`.
- `templates/writing/**` does not exist and repository search finds that path only in the Manifest.
- `START_HERE.md`, both P09 Skills and P09 tests consume the actual canonical paths, not the declared aliases.

This is an **ownership/control-plane drift**, not evidence that the active content contracts are broken. P09 must not repair the Manifest directly because it is CP0.

### CROSS_PART_CHANGE_REQUEST

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: P09
  target_owner: CP0
  target_paths:
    - docs/operations/BASE_PARTITION_MANIFEST.json
  reason: >
    P09 owned_write_paths contain three non-existent aliases while active serial-fiction
    knowledge and the YouTube episode packet live at different canonical paths.
  evidence:
    - docs/knowledge/writing/** => missing
    - docs/knowledge/serial-fiction/** => active and consumed
    - templates/game-dev-youtube/** => missing
    - templates/game-development-youtube/EPISODE_PACKET.md => active and tested
    - templates/writing/** => missing and Manifest-only reference
  required_semantic_change: >
    Align P09 owned_write_paths with the existing active canonical paths instead of
    creating duplicate compatibility directories. Replace the stale serial-fiction and
    YouTube aliases with docs/knowledge/serial-fiction/** and
    templates/game-development-youtube/**. Remove templates/writing/** unless Integration
    can identify an active unique consumer that intentionally requires it.
  acceptance_criteria:
    - P09 scope checker accepts edits to the current serial-fiction knowledge owner.
    - P09 scope checker accepts edits to the current game-development YouTube template owner.
    - No duplicate writing/YouTube canonical directory is created.
    - START_HERE, Skill and test consumers retain one active canonical path.
    - Any retained templates/writing/** declaration has a real consumer and purpose.
  blocking: false
```

`blocking: false` means current P09 runtime/content contracts remain usable and this P09-owned audit can complete. The request should be resolved by Integration before a future P09 task needs to modify those currently read-only canonical paths.

## 4. Important rule audit

| Rule | Canonical owner | Purpose / consumer | Test/evidence | Finding |
|---|---|---|---|---|
| Project canon and actual evidence first | P09 Skills + project canon dependency | prevents invented story/build claims | fiction/YouTube contract tests | KEEP |
| Voice/style consistency without identifiable imitation | serial-fiction Skill | preserves project voice while avoiding expression copying | fiction contract + learning evidence | KEEP |
| Reader feedback is evidence, not canon | serial-fiction Skill/guides | prevents comments from becoming authority | `test_serial_fiction_discipline.py` | KEEP |
| Local payoff + open loop + consequence memory | serial-fiction Skill/guides | protects episode value and continuity | fiction contract | KEEP |
| Character/opponent integrity | serial-fiction Skill/reference | prevents off-screen strength and opponent deflation | fiction contract | KEEP |
| Actual build evidence before YouTube promise | YouTube Skill | prevents feature/release overclaim | `test_game_development_youtube_skill.py` | KEEP |
| Rights/rating/spoiler/security review | YouTube Skill with P07 dependency | prevents unsafe publication claim | YouTube contract | KEEP; P07 remains authority |
| Analytics with sample limits | YouTube Skill/template | prevents CTR/views/retention causal overclaim | YouTube contract | KEEP |
| Platform metric definition context | YouTube packet/test | preserves comparability across metric changes | `test_youtube_metric_definition_context.py` | KEEP |
| Content output != runtime proof | P09 Context/Skill boundaries | prevents a script/story/publication artifact from proving implementation | owner boundaries | KEEP |

No consumer-less critical rule or duplicate active content Skill was found.

## 5. Skill / Mode audit

### `developing-and-revising-serial-fiction`

```yaml
status: ACTIVE
disposition: KEEP
modes:
  - canon-and-continuity
  - arc-and-episode-design
  - pov-and-character-voice
  - character-and-opponent-integrity
  - draft-and-prose
  - serial-pacing-and-payoff
  - reader-feedback-and-revision
important_boundary:
  - project-specific canon remains project-owned
  - game-system design remains P04-owned
  - proofreading-only does not select this Skill
  - identifiable living-author/work style imitation is rejected
```

The Skill body is substantial, but size alone is not a defect. Registry routing is lazy (`load_by_default: false`), detailed references already exist, and focused tests lock several rare but safety-critical contracts. A broad compression now would create more regression risk than demonstrated context savings. Revisit progressive disclosure only with representative routing/context measurements or repeated maintenance failures.

### `producing-game-development-youtube-videos`

```yaml
status: ACTIVE
disposition: KEEP
modes:
  - channel-portfolio
  - episode-concept
  - script-and-shot-plan
  - title-thumbnail-package
  - production-and-publish
  - analytics-review
important_boundary:
  - game design and runtime validation are dependencies, not owned
  - thumbnail image generation remains P05
  - platform/release/rights authority remains P07
  - analytics observation does not prove game demand or causal marketing effect
```

The current mode set already contains the native title/thumbnail experiment as optional evidence rather than creating a new mode/Skill. No split or merge is justified.

## 6. Module audit

| Module | Responsibility | Inputs | Outputs | Consumers / validation | Disposition |
|---|---|---|---|---|---|
| Serial Fiction | story/episode/prose revision | project canon, draft, continuity, reader evidence | revised story/episode evidence | fiction tests, projects | KEEP |
| Narrative / Character / Voice | reusable narrative research/craft lens | project question, source evidence | bounded method/source guidance | serial fiction + game-design consumers | KEEP |
| Game-dev YouTube | truthful production/publication | actual build, audience job, captured evidence | episode/package/publish/analytics packet | YouTube tests, project marketing | KEEP |
| Publication Evidence | provenance/rights/sample limits | platform state, rights/rating/security status | verified or blocked publication status | P07 + projects | KEEP |
| Reusable Writing Lessons | proven reusable learning | merged work/source evidence | Learning Log checkpoint | future P09 work | IMPROVE: add latest Shorts metric lesson |

The modules are cohesive enough for the current one-person workflow. Splitting game narrative into another active Skill would duplicate existing methods and P04/P09 boundaries without a demonstrated routing failure.

## 7. Alternatives

### A. Keep everything unchanged

- advantage: zero churn
- failure: leaves known Manifest ownership drift and misses a learning checkpoint
- disposition: REJECT

### B. Create the missing Manifest-declared directories and copy active content into them

- advantage: makes the literal Manifest paths exist
- failure: creates duplicate canon, active-reference drift and future reconciliation cost
- disposition: REJECT

### C. Keep active canonical paths; hand the Manifest correction to CP0; make only P09-owned evidence/log changes now

- advantage: minimal blast radius, no duplicate canon, respects ownership, easy rollback
- trade-off: Integration must later change one CP0 file
- disposition: **ADOPT**

### D. Rename/migrate all active canonical directories to the Manifest spellings

- advantage: normalizes names around the current Manifest
- failure: high consumer churn across START_HERE, Skills, tests, generated/reference surfaces for no user/player value
- disposition: REJECT

### BETTER_ALTERNATIVE_SEARCH

A broader Skill merge/split and aggressive Skill-body compression were also tested as alternatives. Neither addresses the actual observed failure. Both increase semantic risk and context migration cost. No better alternative than C was found.

### LONG_TERM_PLAN_FIT_REQUIRED

C preserves ONE BASE and stable P09 responsibilities while making the ownership model describe the paths already used by Skills/tests. It also leaves future progressive-disclosure refactoring evidence-driven rather than size-driven.

Revisit if:

- P09 Skill routing repeatedly selects both Skills for one task;
- representative model/context measurements show material Skill-body overhead;
- a third independent publication/content workflow repeats across multiple projects;
- CP0 path drift recurs after Integration correction;
- real human audience/project pilots expose a missing evidence category.

## 8. Current external-source check

| Source | Check | Decision | Why |
|---|---|---|---|
| YouTube Help — A/B test titles & thumbnails | current 2026-08-19 | ADOPT/KEEP | up to 3 title/thumbnail variants; watch-time-based result; not available for Shorts; current P09 contract already matches the bounded principle |
| YouTube Help — Shorts views | current 2026-08-19 | ADOPT/KEEP | public views changed 2025-03-31; previous basis retained as Engaged views; current packet/test already separate definitions |
| inkle/ink | current release observed 1.2.1, 2026-05-05 | REFERENCE_ONLY | useful interactive-narrative implementation reference; no P09 rule delta found |
| Yarn Spinner / Godot | current official docs/release surfaces checked | REFERENCE_ONLY | active Godot narrative tooling remains relevant; no Base-wide workflow change justified |
| GDC narrative talks on choice/consequence | professional-practice reference | ADAPT/KEEP | meaningful consequence, self-expression and bounded branching support current narrative principles; do not universalize one talk |
| Writers Guild Foundation Library | current institutional source | REFERENCE_ONLY | useful produced-script/development-material research surface; no new rule required |
| Reedsy / Writing Excuses current craft material | professional-practice reference | REFERENCE_ONLY | supports POV/voice/revision lenses already present; not authority for one universal prose style |

No source is promoted merely because it is recent. Source truth, project canon and human/project outcomes remain separate evidence levels.

## 9. Adversarial review loops

### Loop 1 — authority / ownership attack

Finding: Manifest write paths do not describe two active canonical P09 content surfaces.  
Validation: actual directories, START_HERE/Skill/test consumers and Manifest-only searches were compared.  
Decision: valid MUST_FIX, but CP0-owned; create a nonblocking cross-part request. Do not duplicate directories.

### Loop 2 — duplicate Skill / responsibility attack

Attack: serial fiction and YouTube might be an unnecessary content umbrella split, or game narrative might need a third Skill.  
Validation: Registry triggers, do-not-use boundaries, modes, tests and consumers were compared.  
Decision: no duplicate active Skill; merging increases ambiguity, third Skill lacks a distinct repeated workflow. No change.

### Loop 3 — context-cost / overengineering attack

Attack: both Skill bodies are large and could be aggressively compressed.  
Validation: lazy Registry routing, existing conditional references, rare safety contracts and tests were checked.  
Decision: file size alone is insufficient evidence. Preserve behavior; defer compression until measured routing/context pressure exists.

### Loop 4 — source freshness attack

Attack: YouTube metrics/experiments or interactive-narrative tooling may have invalidated P09 rules.  
Validation: current first-party YouTube Help plus current ink/Yarn official surfaces were rechecked.  
Decision: current P09 contracts already bound the relevant platform changes; add no new Skill/mode/KPI law.

### Loop 5 — evidence overclaim / publication attack

Attack: repository checks may be silently treated as audience, conversion, rights or runtime proof.  
Validation: YouTube tests explicitly retain HUMAN_NOT_RUN/CONVERSION_UNVERIFIED and owner boundaries; fiction tests separate reader feedback from canon.  
Decision: no semantic gap found.

### Loop 6 — regression / better-alternative reattack

Attack: the minimal solution may merely document the problem rather than improve P09.  
Validation: direct P09 value is preserved by recording the merged Shorts metric lesson in the YouTube Skill Learning Log and this bounded Part checkpoint, while the only structural defect is handed to its actual CP0 owner.  
Decision: no additional valid P09-owned MUST_FIX remains. No speculative Skill rewrite.

```yaml
full_loops_performed: 6
new_valid_p09_owned_must_fix_after_loop_6: 0
blocking_p09_owned_finding: 0
canonical_conflict_in_changed_scope: 0
ownership_conflict_in_changed_scope: 0
unsupported_pass_claim: 0
clean_review_exit: true
cross_part_debt_pending:
  - CP0 Manifest path alignment request
```

## 10. Verification and claim ceiling

Planned/required after branch changes:

```text
python tools/check_base_partition_scope.py --part P09 --base df8ef644d30fc96456da23a5157e5efb61b620bb --head HEAD
python -m unittest discover -s tests -p 'test_*fiction*.py' -v
python -m unittest discover -s tests -p 'test_*youtube*.py' -v
```

The chat environment did not obtain a working local repository clone, so these commands are **NOT_RUN locally**. PR/Actions exact-head evidence must be read before merge. Static repository readback is not a substitute for human reader quality, real audience response, conversion, rights review or runtime implementation proof.

## 11. Rollback

P09 changes are documentation/learning evidence only and can be reverted without altering runtime/game content. The CP0 request proposes no destructive migration: if rejected, existing canonical paths stay unchanged and P09 remains read-only for those mismatched paths until Integration chooses another ownership solution.
