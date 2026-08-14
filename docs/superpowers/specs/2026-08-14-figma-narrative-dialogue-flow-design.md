# Figma Narrative Dialogue Flow Contract Design

## Goal

Add a reusable Base rule for visually planning branching game dialogue in Figma so a solo developer can understand scene continuity, choices, location changes, and edit individual scenes/dialogue lines without turning Figma into a second narrative canon.

Issue: #381

## Evidence and current-state inspection

### Base reuse decision

Existing owners already cover the needed authority boundary:

- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`: Figma is a `VISUAL_WORKSPACE`, not game-rule/runtime canon.
- `templates/project-operations/FIGMA_WORKSPACE_STRUCTURE_PROFILE.md`: `SCREENS`, `SCREEN_STATES`, `USER_FLOWS`, `GAMEPLAY_FLOWS`, `PROTOTYPES`, `DEV_HANDOFF` and AI edit boundaries.
- `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`: approved/WIP/rejected/final visual lifecycle.
- `tests/test_visual_collaboration_capability_contract.py`: current Figma authority and workflow regression contract.

Existing Solution First verdict: **ABSORB**. Add a focused project-operation profile that extends these owners; do not create a new broad Figma Skill, narrative engine, Figma bridge, or duplicate Tool Hub implementation.

Open PR boundary checked on 2026-08-14:

- #373 owns Tool Hub / Character Studio expansion.
- #376 owns local-to-Figma delivery bridge.

This change must not modify files owned by those PRs.

### Supplied Figma Make inspection

Source: `https://www.figma.com/make/HwZcPcvuNzHf6BRKiDg04O/...`

The connected Figma MCP exposed the generated Make source files and screenshots. The current prototype is React-based and models:

```text
Scene
├─ location
├─ title
├─ background
├─ dialogues[]
└─ choices[] -> next scene id
```

It also keeps a separate manually-authored branch map (`MNODES` + `MEDGES`).

Observed strengths:

- Playable dialogue preview and branch selection are easy to understand.
- Current/visited/unvisited branch state gives useful visual feedback.
- Location/background and dialogue panel are shown together.

Observed scale/edit risks:

1. `s1` and `s1a` are separate `Scene` objects even though they intentionally keep the same school-corridor background. This conflates narrative branch state with visual scene continuity.
2. Dialogue lines have no stable `dialogue_id`; individual line selection/edit references cannot survive insert/reorder reliably.
3. Choices contain only `text` + `next`; same-scene continuation and location/scene movement are not explicit transition semantics.
4. The visible branch map duplicates story links in a separate `MNODES/MEDGES` list, creating drift risk.
5. There is no edit-mode selection contract for scene, branch beat, dialogue line, or choice.

The Figma connector does **not** expose the Figma Make prompt/chat history as a readable transcript. Therefore `MAKE_CHAT_HISTORY = BLOCKED_UNVERIFIED`; only the current generated source/screenshots are treated as inspected evidence.

## External benchmark

Primary/official sources were checked on 2026-08-14.

### Figma

- Prototype flows are collections of connected frames and can have independent flow starting points: `https://help.figma.com/hc/en-us/articles/360039823894-Create-and-manage-prototype-flows`
- Sections can group frames belonging to the same flow and can themselves be prototype destinations: `https://help.figma.com/hc/en-us/articles/16194160540567-Use-sections-in-prototyping`

Adopt: group visual continuity and flow explicitly instead of treating every branch stop as an unrelated screen.

Do not adopt: using prototype wiring as narrative/runtime canon.

### Yarn Spinner

- Yarn scripts use named nodes to divide/manage longer branching stories; node bodies contain lines, commands, and options. Node headers can carry metadata such as location: `https://docs.yarnspinner.dev/3.0/write-yarn-scripts/scripting-fundamentals/lines-nodes-and-options`
- Godot integration emits node/dialogue lifecycle and presents lines/options separately: `https://docs.yarnspinner.dev/2.4/using-yarnspinner-with-godot/components/dialogue-runner`

Adopt: stable addressable narrative units; explicit separation of dialogue lines and options; location as metadata rather than identity.

Do not adopt: requiring Yarn Spinner for every Base project. Engine/tool choice remains project-specific.

### ink / Inky

- ink is designed for highly branching narrative and keeps narrative flow in a declarative source: `https://github.com/inkle/ink`
- Inky provides play-as-you-write, jump-to-definition, and issue navigation over the same source: `https://github.com/inkle/inky`
- Inky/ink are used by inkle productions including `80 Days`; ink release notes also document features developed for `Heaven's Vault`.

Adopt: editing and navigation should resolve back to stable source identity; preview/graph should derive from one data model rather than duplicate it.

Do not adopt: building a full custom narrative IDE in Figma.

## Design-space comparison

| Option | Description | Strength | Failure mode | Verdict |
|---|---|---|---|---|
| A. Branch node = Scene | Keep current Make model: every branch stop is a new Scene | simplest prototype | duplicate backgrounds; scene/branch semantics blur; per-line edit weak | REJECT |
| B. Scene container + Beat + Line + typed Choice | Scene owns background continuity; Beat owns branch point; Line owns editable text; Choice owns transition | best balance of visual clarity, editability, data stability | needs stable IDs and a small hierarchy | **SELECT** |
| C. Full Figma narrative editor / round-trip canon | Make Figma the primary story DB and editor | rich visual authoring | second canon, sync complexity, runtime divergence, high maintenance | REJECT |
| D. Mandate external narrative engine | Require Yarn/ink for all projects | strong authoring tools | violates project/tool neutrality and Godot/project-specific needs | REJECT |

## Selected model

### 1. Scene continuity container

A `SCENE_GROUP` represents visual/spatial continuity, not every branch stop.

Minimum identity:

```yaml
scene_id:
location_id:
background_ref:
title:
entry_beat_id:
```

If a choice continues with the same visual scene/background, it remains inside the same `SCENE_GROUP`. A location/background change crosses into another `SCENE_GROUP`.

### 2. Dialogue beat

A `DIALOGUE_BEAT` is an addressable narrative stop inside a scene: a short sequence of dialogue followed by zero or more choices.

```yaml
beat_id:
scene_id:
title:
dialogue_ids: []
choice_ids: []
```

A beat is useful for branch-map readability; it must not replace individual dialogue identity.

### 3. Dialogue line

Every editable dialogue row gets a stable ID.

```yaml
dialogue_id:
beat_id:
speaker_id:
text:
```

Do not use array index as durable identity. Reordering a list must not silently change the identity used by Figma annotations, implementation handoff, localization, review, or test evidence.

### 4. Choice and transition

Every choice gets a stable ID and explicit transition kind.

```yaml
choice_id:
source_beat_id:
text:
target_beat_id:
transition_kind: STAY_IN_SCENE | MOVE_SCENE | END
```

Rules:

- `STAY_IN_SCENE`: target beat has the same `scene_id`; background continuity is preserved.
- `MOVE_SCENE`: target beat belongs to another `scene_id`; scene/location/background transition is explicit.
- `END`: no playable target beat is required.
- Conditions, variables, skill checks, costs, and side effects are project data and are added only when the project actually needs them; Base does not prebuild them into this minimal visual contract.

## Figma visual layout contract

Recommended placement under project `20_<PROJECT>_UI_UX / 60_GAMEPLAY_FLOWS`:

```text
NARRATIVE_DIALOGUE
├─ 00_FLOW_INDEX
├─ SCENE_<scene_id>  (Section or containing frame)
│  ├─ SCENE_HEADER / background preview / metadata
│  ├─ BEAT_<beat_id>
│  │  ├─ DIALOGUE_<dialogue_id>
│  │  └─ CHOICE_<choice_id>
│  └─ ...
├─ SCENE_<scene_id>
└─ ...
```

Visual semantics:

- Same-scene branch connections stay within the Scene section.
- Location/scene movement crosses a Scene section boundary and must show `MOVE_SCENE` in connector/annotation metadata.
- Endings terminate at an `END` target/card.
- Branch-map geometry is derived from the same IDs/relationships whenever generated tooling exists. Do not maintain an unrelated second list of edges as canon.
- Prototype links may mirror important choices for click testing, but the prototype is still visual review evidence, not runtime proof.

## Edit-mode selection contract

The minimum edit surface has four independently selectable targets:

| Selection | Editable fields | Protected/derived |
|---|---|---|
| Scene | title, location/background reference | stable `scene_id`; approved visual source unless duplicated to WIP |
| Beat | title/order/contained line-choice references | stable `beat_id`, owning `scene_id` |
| Dialogue line | speaker, text | stable `dialogue_id`, owning `beat_id` |
| Choice | text, target, transition kind | stable `choice_id`, source identity |

Required behavior for an implementation or generated Figma editing surface:

1. Selecting a Scene shows only that scene's metadata and its contained beats.
2. Selecting a Beat shows the ordered dialogue list and outgoing choices for that beat.
3. Selecting a Dialogue Line allows that line to be inspected/edited without requiring edits to neighboring lines.
4. Selecting a Choice makes its target and `transition_kind` visible together; changing target cannot silently preserve an invalid transition kind.
5. A change to canonical project story data must regenerate/reconcile the visual map instead of requiring a second manual branch graph update.

## Authority and handoff

```text
project narrative data / confirmed planning = canonical story rules
Figma dialogue flow = editable visual mirror / review workspace
Godot runtime + tests = implementation reality
```

Stable IDs are bridges, not authority transfer. Figma edits are `DRAFT_VISUAL` / proposal state until accepted into the project's responsible narrative/data canon. A Figma prototype or Make preview cannot by itself claim `IMPLEMENTED`, `VERIFIED`, save/load correctness, localization correctness, or runtime branch correctness.

## Implementation Reality Gate

`Implementation Reality Gate` is the Base-local alias defined in `docs/CONTROLLED_VOCABULARY.md`; detailed claim verification remains owned by the existing validation skill/reference.

Evidence ceiling for this Base change:

```yaml
figma_make_source_inspected: YES
figma_make_current_screenshots_inspected: YES
figma_make_chat_history: BLOCKED_UNVERIFIED
base_policy_contract_authored: TARGET
focused_contract_test: TARGET
figma_make_edit_mode_implemented: NO
project_story_data_migrated: NO
godot_dialogue_runtime_implemented: NO
human_playtest: NOT_RUN
```

Therefore this change may claim **RULE_CONTRACT_ADDED** after exact-head tests pass. It must not claim the supplied Figma Make has been upgraded with the edit mode or that any game runtime implements this model.

## Adversarial pre-review

### Attack

- Risk: `Scene` terminology may still collide with Godot scene files or narrative screenplay scenes.
- Risk: forcing one dialogue line per visual graph node would make large conversations unreadable.
- Risk: Figma edits may be mistaken for canonical dialogue edits.
- Risk: adding condition/effect schemas now would overdesign projects that only need simple choices.
- Risk: visual graph and project data can drift if both author edges independently.

### Validate critique

- `Scene` collision is real; use `SCENE_GROUP` in Figma contract and require project translation if `scene` already has another canonical meaning.
- One line per graph node is unnecessary. Keep line rows inside a `DIALOGUE_BEAT`; line remains individually selectable but graph complexity stays bounded.
- Canon risk is already covered by Visual Collaboration Policy and is repeated explicitly here.
- Conditions/effects are valid future needs but not required by the user's current goal; defer them.
- Graph drift is the highest implementation risk; require one relationship model and derived visual edges when tooling exists.

### Approved minimal refinement

Selected model remains Scene Group → Dialogue Beat → Dialogue Line → Choice, with typed transitions and explicit authority boundary. No new Skill, runtime system, Figma bridge, or external narrative dependency is added.

## Rollback

This is an additive common rule. Roll back by reverting the eventual squash merge. It does not migrate project data, rename existing Figma pages, or modify the supplied Figma Make file.