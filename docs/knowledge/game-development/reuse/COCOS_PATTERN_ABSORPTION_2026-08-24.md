# Cocos Production Pattern Absorption into Godot — 2026-08-24

```yaml
status: BASE_PATTERN_TRANSLATION_ACTIVE
date: 2026-08-24 KST
engine_authority: GODOT_ONLY_RUNTIME
absorption_mode: ABSORB_COCOS_PATTERNS_ONLY
runtime_dependency_added: false
typescript_dependency_added: false
paid_dependency_added: false
new_scheduler_added: false
active_project_migration: none
project_adoption: NOT_RUN
```

## 1. Decision and evidence ceiling

Base keeps **Godot as the only production/runtime game engine**. Cocos Creator is an external benchmark for production patterns only.

```text
GODOT_ONLY_RUNTIME
ABSORB_COCOS_PATTERNS_ONLY

Cocos feature or workflow
→ identify the production problem it solves
→ extract a provider/engine-independent contract
→ check existing Base/Godot owner first
→ map only to independently verified Godot capability
→ ADOPT | ADAPT | TEST | REJECT
→ validate in a real Godot consumer before runtime-readiness claims
```

The evidence boundary is explicit:

```text
Cocos evidence != Godot runtime evidence
API_EXISTS_IS_NOT_PROJECT_READY
```

Cocos documentation can establish what Cocos does. It cannot establish that a Godot translation works in a project, on a target device/browser, or at production quality.

Current Godot claim ceiling:

```text
PCK_DEFERRED_CONTENT: TEST
PARTIAL_REBUILD: TEST
GODOT_WEB_RELEASE_READY: NOT_RUN
```

These states may be promoted only by the applicable Godot project build/run/runtime evidence and existing Implementation Reality Gate.

## 2. Primary evidence surfaces

### Cocos Creator 3.8

- Asset Bundle: <https://docs.cocos.com/creator/3.8/manual/en/asset/bundle.html>
- Build Panel: <https://docs.cocos.com/creator/3.8/manual/en/editor/publish/build-panel.html>
- command-line publishing: <https://docs.cocos.com/creator/3.8/manual/en/editor/publish/publish-in-command-line.html>
- mini-game subpackage: <https://docs.cocos.com/creator/3.8/manual/en/editor/publish/subpackage.html>

### Godot translation surfaces

- project export/resource selection: <https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html>
- PCK/ZIP resource packs and runtime loading: <https://docs.godotengine.org/en/stable/tutorials/export/exporting_pcks.html>
- `PCKPacker`: <https://docs.godotengine.org/en/stable/classes/class_pckpacker.html>
- command-line export: <https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html>
- Web export constraints: <https://docs.godotengine.org/en/latest/tutorials/export/exporting_for_web.html>

These URLs are reference evidence, not a statement that the corresponding Base/project implementation has been run.

## 3. Pattern disposition matrix

| Cocos-observed pattern | Underlying problem | Godot/Base translation | Disposition | Existing owner |
|---|---|---|---|---|
| Asset Bundle | startup/download cost and coarse loading boundaries | first-load set + deferred content; selective export/PCK/ZIP only as a candidate implementation | `ADAPT / TEST` | `GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md` |
| local/remote/subpackage bundle separation | not all content belongs in first boot | package budget drives mandatory vs deferrable content | `ADAPT` | build-size/asset optimization |
| Build Panel/config | builds need repeatable target profiles | named/versioned Godot export profile + evidence-bound CLI invocation | `ADOPT / ADAPT` | `TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md` |
| command-line publish | machine-repeatable builds | Godot export preset/CLI path; command success still requires artifact/runtime verification | `ADAPT` | technical production/release + QA |
| selected bundle build | avoid rebuilding unrelated heavy content | selective/partial rebuild hypothesis | `TEST` | technical production/release + Godot runtime |
| mini-game subpackage | strict first-package budget | generic first-session package-budget principle; no frozen Cocos/platform constants | `ADAPT` | build-size/asset optimization |
| multi-platform adapters | platform APIs should not own game rules | existing platform-adapter boundary | `ADOPT EXISTING OWNER` | `PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md` |
| TypeScript Component model | composition | Godot already has Node/Scene/script composition; no new abstraction | `REFERENCE_ONLY` | none |
| Cocos Store/package ecosystem | third-party reuse | case-by-case Existing Solution First only | `REJECT AS DEFAULT` | existing asset/tool evaluation owners |
| Cocos runtime/Creator | second production engine | no translation | `REJECT` | n/a |

## 4. Absorbed production contracts

### 4.1 `FIRST_LOAD_BUDGET_AND_DEFERRED_CONTENT`

```text
first-session player promise
→ content required before that promise is playable
→ main / first-load content set
→ optional or later-session content
→ deferred content set
→ explicit load trigger
→ loading + error + retry/fallback UX
→ cache/memory lifecycle
→ package size + startup/load evidence
```

The transferable lesson from Asset Bundles is **content-boundary discipline**, not Cocos's bundle implementation. In Godot, selective export and PCK/ZIP resource packs are implementation candidates. They remain `PCK_DEFERRED_CONTENT: TEST` until a real project proves download/load/version/error/retry/cache behavior.

### 4.2 `REPRODUCIBLE_BUILD_PROFILE`

```text
named target profile
→ versioned export/build configuration
→ deterministic non-interactive invocation where appropriate
→ explicit output path
→ exit code + log
→ artifact identity
→ smoke/runtime verification
```

Cocos Build Panel/CLI illustrates the production value. Base translates the principle through Godot's own export-preset/CLI surfaces rather than importing Cocos JSON formats or Cocos CLI. A successful command is build-process evidence, not release PASS.

### 4.3 `PLATFORM_ADAPTER_STAYS_OUTSIDE_GAME_RULES`

```text
platform SDK / browser API / store API / lifecycle event
→ platform adapter
→ semantic game action/service
→ shared game rules/state
```

This reinforces the existing PC/Android delivery owner. Platform services do not become authoritative gameplay state, and Cocos platform adapters are not imported.

### 4.4 `PACKAGE_BUDGET_DRIVES_CONTENT_BOUNDARIES`

```text
current target-platform/package constraint
→ first-session player promise
→ mandatory content set
→ deferrable content set
→ loading transition
→ failure fallback
→ measured first-package/startup budget
```

Mini-game subpackages are evidence that strict package constraints can shape content boundaries usefully. Platform-specific numeric limits are **not** frozen into Base; they must be rechecked from current official platform documentation when that platform is actually targeted.

### 4.5 `PARTIAL_REBUILD_CANDIDATE`

The transferable goal is to avoid rebuilding unrelated heavy content when safe. Cocos can build selected bundles, but that does not prove a generic Godot partial-build solution.

For Godot:

```text
PARTIAL_REBUILD: TEST
```

Promotion requires a real project showing repeatable build-time savings without stale imports, dependency omissions, mismatched packs, cache corruption, or release-artifact ambiguity. Until then Base does not create a generic partial-build tool or new `RM-*` module.

## 5. Godot Web boundary

Cocos's Web-first production strengths are useful as a benchmark, but they do not transfer readiness.

```text
Godot Web requested
→ read current Godot Web constraints
→ verify renderer / language / plugin compatibility
→ measure download + startup + memory
→ verify persistence + browser lifecycle
→ verify representative browsers/devices
→ only then promote delivery readiness
```

Therefore:

```text
GODOT_WEB_RELEASE_READY: NOT_RUN
```

A Cocos Web success, a Godot export option, or a successful CLI export is not browser/runtime evidence for the current project.

## 6. Explicit non-adoption boundary

```text
NO_COCOS_RUNTIME
NO_COCOS_CREATOR_PROJECT_TEMPLATE
NO_TYPESCRIPT_REQUIREMENT
NO_SECOND_ENGINE_SELECTION_GATE
NO_COCOS_CLI_DEPENDENCY
NO_COCOS_STORE_DEFAULT
NO_COPY_OF_COCOS_INTERNAL_ARCHITECTURE
NO_COCOS_SPECIFIC_MODULE_ID_WITHOUT_PROMOTION_EVIDENCE
```

This work also does not claim WeChat, Douyin, or any other mini-game platform support for Godot projects.

## 7. Existing Solution First / module policy

No new `RM-*` ID is allocated by this absorption pass.

- first-load/package boundaries already belong to build-size/asset optimization;
- reproducible builds already belong to technical production/release and QA evidence;
- platform isolation already belongs to the cross-platform adapter owner;
- PCK/deferred-content and partial rebuild still lack real Godot consumer evidence.

A later new module requires all of the following:

```text
existing owners cannot express the reusable interface cleanly
+ materially distinct Godot consumers provide repeated evidence
+ focused regression/runtime evidence exists
+ no duplicate build/state/authoring authority
→ consider module promotion
```

## 8. Periodic source routing

Cocos Creator official docs/releases can be scanned through the existing `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` pipeline as an authority for **Cocos behavior only**. Material findings can become:

```text
NO_CHANGE
REFERENCE_ONLY
ADAPT_TO_EXISTING_OWNER
TEST_IN_GODOT
BASE_PROMOTION_CANDIDATE
REJECT
```

They do not become Godot runtime authority, and no new scheduler is created.

## 9. Implementation Reality Gate

This Base change may claim, once its repository checks pass:

```text
Cocos production patterns captured
engine-independent translation contracts documented
existing Base owner routing installed
Godot remains sole production/runtime engine
static regression/CI evidence recorded
```

It may not claim without later project pilots:

```text
Godot deferred-content production ready
Godot Web release ready
partial rebuild speedup proven
browser/mobile performance proven
project adoption complete
```

The next promotion point is a **real Godot project consumer**, not more Cocos documentation.
