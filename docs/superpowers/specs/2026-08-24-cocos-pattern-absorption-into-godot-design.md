# Cocos Pattern Absorption into Godot Design

## Status

- date: 2026-08-24 KST
- user direction: `GODOT_ONLY_RUNTIME · ABSORB_COCOS_PATTERNS_ONLY`
- change class: Base architecture/knowledge refinement
- game engine authority: Godot remains the only default/runtime authoring engine
- Cocos runtime/project adoption: rejected
- active project engine migration: none
- project canon mutation: none
- Notion mutation: none
- new Skill/Agent: none
- new paid dependency: none
- new scheduler: none
- implementation evidence: not yet claimed by this design

## Decision

Base will **not** introduce Cocos Creator as a second supported production engine.

Cocos is treated as an external engineering benchmark whose useful, engine-independent patterns may be extracted and adapted into the existing Godot toolchain when Godot has an equivalent or safer implementation path.

```text
Cocos feature
→ identify underlying production problem
→ extract engine-independent contract
→ check existing Base/Godot owner first
→ map to verified Godot capability
→ ADOPT | ADAPT | TEST | REJECT
→ validate in Godot
```

The forbidden shortcut is:

```text
Cocos has feature X
→ add Cocos dependency / TypeScript runtime / second engine
```

## Problem

Cocos Creator has mature workflows around browser/mobile distribution, modular resource loading, build profiles, command-line publishing, and mini-game packaging. Those workflows contain useful production ideas, but adopting Cocos itself would create a second engine/toolchain, duplicate authoring authority, increase testing and maintenance surfaces, and conflict with the existing Godot-centered Base runtime/toolchain.

The useful question is therefore not "Should Base support Cocos?" but:

> Which Cocos production patterns solve recurring problems that can be expressed through existing Godot capabilities without importing Cocos-specific runtime or authoring dependencies?

## Existing Base owners to preserve

This change reuses rather than replaces:

- `AGENTS.md` — Existing Solution First, evidence, cost, and Godot authority invariants.
- `docs/operations/base-partitions/P06_GODOT_RUNTIME_TOOLCHAIN.md` — Godot authoring/runtime/toolchain owner.
- `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` — shared core and platform-adapter boundaries.
- `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` — package/download/asset optimization owner.
- `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md` — build/release technical owner.
- `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` — periodic source-discovery owner.
- `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md` — external pattern extraction and ADOPT/ADAPT/TEST/REJECT routing.
- `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md` — reusable module maturity/evidence owner.
- existing QA/runtime/Implementation Reality Gate contracts — actual build/run evidence before PASS.

No second engine registry, second runtime authority, Cocos-specific Skill, or Cocos-specific scheduler is introduced.

## Three-option comparison

### Option A — Dual-engine Base: Godot + Cocos

Support Cocos Creator as an equal production engine and maintain parallel runtime/build/QA paths.

**Reject.** It increases authoring, CI, dependency, documentation, debugging, and project-selection complexity without a current project requirement strong enough to pay that cost. It would also dilute the existing Godot single-authority/toolchain investment.

### Option B — Godot-only runtime + pattern absorption

Keep Godot as the only production engine. Treat Cocos as a benchmark and port only engine-independent patterns that map cleanly onto verified Godot features.

**Adopt.** This captures the useful operational ideas while preserving one runtime authority and zero incremental software cost.

### Option C — Ignore Cocos entirely

Keep the current Base unchanged and do not track Cocos patterns.

**Reject as incomplete.** Cocos provides concrete evidence around modular asset delivery, build configuration, browser/mobile publishing, and small-package workflows that can improve the existing Godot production model when adapted carefully.

## Source evidence and translation boundary

Primary Cocos reference surfaces used for this design:

- Cocos Creator 3.8 Asset Bundle overview: <https://docs.cocos.com/creator/3.8/manual/en/asset/bundle.html>
- Cocos Creator 3.8 Build Panel: <https://docs.cocos.com/creator/3.8/manual/en/editor/publish/build-panel.html>
- Cocos Creator 3.8 command-line publishing: <https://docs.cocos.com/creator/3.8/manual/en/editor/publish/publish-in-command-line.html>
- Cocos Creator 3.8 mini-game subpackage: <https://docs.cocos.com/creator/3.8/manual/en/editor/publish/subpackage.html>

Primary Godot translation surfaces:

- Godot stable project export/resource selection: <https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html>
- Godot stable PCK/ZIP packs and runtime loading: <https://docs.godotengine.org/en/stable/tutorials/export/exporting_pcks.html>
- Godot stable `PCKPacker`: <https://docs.godotengine.org/en/stable/classes/class_pckpacker.html>
- Godot command-line export contract: <https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html>
- Godot Web export constraints: <https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html>

Cocos documentation is evidence for **Cocos behavior and design ideas only**. Godot implementation claims must be independently supported by Godot documentation or actual Base/project runtime evidence.

## Pattern disposition matrix

| Cocos pattern | Underlying problem | Godot/Base disposition | Target owner |
|---|---|---|---|
| Asset Bundle | startup/download cost and coarse asset loading | `ADAPT` to resource-pack/content-boundary pattern | build-size/asset optimization + Godot runtime |
| Remote/local/subpackage bundle distinction | content should not all be mandatory at first boot | `ADAPT/TEST` as first-load budget + deferred content contract | build-size/asset optimization |
| Build-task configuration | builds need explicit reproducible profiles | `ADOPT` as provider-neutral build-profile principle | technical production/release |
| JSON build config + CLI | machine-repeatable builds | `ADAPT` to Godot export presets + headless CLI evidence | technical production/release + QA |
| build selected bundle | avoid rebuilding unrelated heavy content | `TEST` against Godot selective export/PCK workflows | Godot runtime/tooling |
| mini-game subpackages | strict initial package budget and deferred loading | `ADAPT` the package-budget principle only | build-size/asset optimization |
| multi-platform publish adapters | platform API/build differences should stay outside game rules | `ADOPT` through existing platform-adapter boundary | PC/Android delivery |
| Cocos TypeScript/Component model | component composition | `REFERENCE_ONLY`; Godot already has Node/Scene/script composition | no new owner |
| Cocos Store/package ecosystem | reuse third-party modules | `REJECT` as a default dependency source; evaluate case-by-case | Existing Solution First |
| Cocos runtime/engine | second production engine | `REJECT` | n/a |

## Absorbed contracts

### 1. `FIRST_LOAD_BUDGET_AND_DEFERRED_CONTENT`

This is a cross-engine production contract, not a Cocos module.

```text
player-required-at-start content
→ main package / first-load set
→ optional or later-session content
→ deferred pack/content set
→ explicit load trigger
→ loading/error/retry UX
→ memory/cache lifecycle
→ package-size + startup-time evidence
```

Godot translation candidates include selective export plus PCK/ZIP resource packs loaded with `ProjectSettings.load_resource_pack()`. This remains `TEST` until a project proves download/load/error/recovery behavior; the existence of the API is not runtime proof.

### 2. `REPRODUCIBLE_BUILD_PROFILE`

```text
named target profile
→ versioned build/export configuration
→ deterministic command invocation
→ explicit output path
→ captured exit code/log
→ artifact identity
→ smoke/runtime verification
```

Cocos demonstrates the value through Build Panel configuration, JSON config import/export, and command-line publishing. Base should express the same principle through Godot's own export preset/CLI path, without copying Cocos config formats.

A successful command is not a release PASS. The built artifact must still be checked under existing QA/IRG rules.

### 3. `PLATFORM_ADAPTER_STAYS_OUTSIDE_GAME_RULES`

This is already present in the PC/Android delivery guide and should be strengthened rather than duplicated.

```text
platform SDK / browser API / store API / lifecycle
→ adapter
→ semantic game action/service
→ shared game rules/state
```

No platform SDK becomes authoritative game state.

### 4. `PACKAGE_BUDGET_DRIVES_CONTENT_BOUNDARIES`

Cocos mini-game subpackages provide a strong example of designing content boundaries around strict initial-package limits. Base should absorb the general principle, not Cocos/WeChat-specific constants as universal Godot rules.

```text
platform/package constraint
→ first-session player promise
→ mandatory content set
→ deferrable content set
→ loading transition
→ failure fallback
→ measured package/startup budget
```

Any current platform-specific size limit must be verified from that platform's official documentation at release time.

### 5. `PARTIAL_REBUILD_CANDIDATE`

Cocos 3.8 can build a selected Asset Bundle. The transferable goal is to avoid unnecessary rebuilds of unrelated heavy content.

For Base/Godot this stays `TEST`, because a safe implementation depends on Godot import dependencies, export presets, resource pack boundaries, cache behavior, and project structure. Do not add a generic partial-build tool until at least one real project demonstrates repeatable time savings without stale-artifact risk.

## What is explicitly not absorbed

```text
NO_COCOS_RUNTIME
NO_COCOS_CREATOR_PROJECT_TEMPLATE
NO_TYPESCRIPT_REQUIREMENT
NO_SECOND_ENGINE_SELECTION_GATE
NO_COCOS_CLI_DEPENDENCY
NO_COCOS_STORE_DEFAULT
NO_WECHAT_OR_DOUYIN_PLATFORM_SUPPORT_CLAIM
NO_COPY_OF_COCOS_INTERNAL_ARCHITECTURE
NO_COCOS_SPECIFIC_MODULE_IDS_WITHOUT_MULTI_CONTEXT_EVIDENCE
```

Web/H5 or mini-game business opportunities may still be researched, but they do not change the engine authority automatically. A Godot Web target must pass Godot-specific browser/performance/input/storage/hosting checks.

## Godot Web boundary

Cocos's Web-first strengths should increase our attention to Web delivery, but not create a false equivalence.

Godot Web has its own constraints, including browser/WASM/WebGL requirements and platform-specific limitations. Therefore:

```text
WEB_TARGET_REQUESTED
→ read current Godot Web export constraints
→ confirm renderer/language/plugin compatibility
→ measure startup/download/memory
→ verify persistence and browser lifecycle
→ verify representative browsers/devices
→ only then approve Web delivery
```

`Cocos works well on Web` is never evidence that a Godot build is ready for Web.

## Reusable Module Registry policy

This change does **not** immediately allocate new `RM-*` IDs for every extracted pattern.

Reason:

- `PLATFORM_ADAPTER_STAYS_OUTSIDE_GAME_RULES` already has an existing owner.
- package-size and first-load optimization already have an existing owner.
- build reproducibility already overlaps with technical production/QA evidence.
- PCK/deferred-content and partial-rebuild patterns need real Godot project evidence before promotion.

Promotion rule:

```text
external pattern
+ existing owner cannot express the reusable interface cleanly
+ >= 2 materially distinct Godot project consumers OR one strong Base reference implementation plus second consumer
+ focused regression evidence
+ no duplicate state/build authority
→ consider new RM-TOOL / RM-WORK module ID
```

Until then the patterns are `EXISTING_OWNER_REUSE` or `TEST` candidates.

## Periodic source routing

Cocos should be added as a **GAME_DEVELOPMENT discovery/authority source for its own engine behavior**, not as a Base runtime authority.

Candidate scan surfaces:

```text
Cocos Creator official docs
Cocos Creator release/change notes
cocos/cocos-engine repository releases when relevant
Web/mobile publishing changes
Asset Bundle/build-pipeline changes
startup/package-size optimization changes
editor/automation changes
```

Material discoveries flow through the existing periodic source/evidence/reverse-engineering pipeline. No Cocos-specific scheduler is created.

A source scan can produce:

```text
NO_CHANGE
REFERENCE_ONLY
ADAPT_TO_EXISTING_OWNER
TEST_IN_GODOT
BASE_PROMOTION_CANDIDATE
REJECT
```

## Validation design

### Static contract checks

Implementation should add regression coverage proving at minimum:

1. Godot remains the production/runtime engine authority.
2. Cocos is referenced as benchmark/source, not runtime dependency.
3. no Cocos/TypeScript dependency is introduced.
4. extracted patterns route to existing owners first.
5. PCK/deferred-content and partial-build claims remain `TEST` until runtime evidence exists.
6. Web readiness cannot be inferred from Cocos evidence.
7. periodic Cocos scanning uses the existing source pipeline rather than a new scheduler.

### Implementation Reality Gate

Documentation-level completion may claim only:

```text
Cocos pattern research complete
translation contract documented
owner routing installed
static regressions passing
```

It may not claim:

```text
Godot deferred-content production ready
Godot Web release ready
partial rebuild speedup proven
mobile/browser performance proven
project adoption complete
```

Those require an actual Godot project pilot and artifact/runtime evidence.

## Adversarial review targets

Implementation and review must attack these failure modes for at least the repository-required full review loop:

1. **Second-engine creep** — did any wording silently turn Cocos into a supported runtime?
2. **Renaming duplication** — did a new module duplicate build-size, release, platform-adapter, or QA owners?
3. **False portability** — was a Cocos feature assumed to exist in Godot without independent evidence?
4. **API-exists-equals-ready** — was PCK/Web/CLI capability confused with project-level readiness?
5. **Premature abstraction** — was a reusable runtime/tool built before a real Godot consumer existed?
6. **Package-limit staleness** — were current mini-game/platform numeric limits frozen into Base as universal constants?
7. **Cost/toolchain expansion** — was any new paid service or unnecessary dependency added?
8. **Project migration drift** — did any existing project get migrated or altered without a project-specific decision?

## Planned implementation surfaces

Prefer the smallest changes that preserve current owners:

1. add a dated Cocos pattern/evidence note under the existing game-development/reuse knowledge surface;
2. update the build-size/asset optimization owner with first-load/deferred-content and package-boundary principles;
3. update technical production/release guidance with the reproducible-build-profile translation where not already present;
4. update the PC/Android/platform adapter owner only if the current wording lacks the extracted boundary;
5. add Cocos official source surfaces to the existing periodic source discovery pool with an explicit Cocos-only authority ceiling;
6. update module registry only if a genuinely distinct reusable candidate remains after overlap analysis;
7. add focused regression tests for the invariant that Godot remains sole engine authority and Cocos is pattern-source-only;
8. record P06 learning checkpoint only if a new reusable lesson survives implementation review.

Do not modify active project repositories or Notion as part of this Base-only change.

## Acceptance criteria

The design is successful when:

- Godot remains the only production engine in Base's default game-development path.
- useful Cocos ideas are expressed as engine-independent contracts and mapped to Godot capabilities.
- no duplicate Skill, scheduler, engine layer, or paid dependency is introduced.
- existing owners remain canonical.
- unsupported Godot runtime claims are marked `TEST`/`NOT_RUN` rather than PASS.
- future Cocos changes can be periodically scanned through the existing external-source system.
- a future project can benefit from first-load budgeting, deferred content, reproducible builds, and platform isolation without installing Cocos.
