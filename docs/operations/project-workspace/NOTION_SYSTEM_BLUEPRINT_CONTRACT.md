# Notion System Blueprint Contract

## Purpose

`NOTION_SYSTEM_BLUEPRINT` is a human-readable node graph and implementation contract for complex project systems. It sits between approved design intent and repository implementation, but it is **not** a visual-scripting runtime and it is **not** an independent source of truth.

Use it to make the following chain explicit:

```text
player action / system event
→ trigger
→ condition
→ state or data change
→ output / next state
→ player feedback
→ implementation mapping
→ validation
```

## Authority boundary

- Human-facing Blueprint summaries belong in the Project Notion Home or the relevant human Detail Canon.
- Detailed mapping, edge cases and implementation traceability may live in the project Detail Canon / AI-System surface as appropriate.
- Repository Markdown, JSON/game data, Godot scenes/resources, GDScript, tests and runtime evidence remain structured/runtime canon.
- A Blueprint is a derived projection of approved design and current implementation ownership. It cannot silently override repository runtime truth or an approved project decision.
- If the Blueprint disagrees with current canon, reconcile the approved decision and correct the derived Blueprint rather than creating a third competing canon.

## Applicability gate

`SYSTEM_BLUEPRINT_REQUIRED_WHEN_COMPLEX`

### Selected two-artifact profile exception

`TWO_ARTIFACT_PROFILE_NO_NOTION_BLUEPRINT_OUTPUT_READBACK`

`DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`가 명시적으로 선택되면 `NO_SEPARATE_BLUEPRINT_ARTIFACT`가 이 계약의 일반 Notion presentation/lifecycle 규칙보다 우선한다. 사람용 Blueprint layer와 machine mapping은 정확히 두 산출물인 PDF + repository AI Markdown 안에 통합하며, 새 Notion Blueprint output/readback을 생성하거나 완료 조건으로 요구하지 않는다.

기존 Notion Blueprint에 repository로 이관되지 않은 고유 정보가 있으면 input-only source로 fresh-read하고 Source Registry에 provenance와 migration gap을 남긴다. 유효한 기존 Blueprint 구조는 두 산출물 안에서 reuse/adapt할 수 있지만 Notion에 write back하지 않는다. 이 예외는 선택된 profile의 출력 경계일 뿐이며 다른 프로젝트나 일반 `DOMAIN_SPLIT_CANON`의 Blueprint 적용성을 전역 폐기하지 않는다.

Create or maintain a System Blueprint when at least one of these is true:

- multiple states or branches interact;
- multiple systems exchange data or events;
- the player action → consequence chain is difficult to understand from prose alone;
- implementation requires explicit ownership or event/data boundaries;
- the system is reusable across scenes/content or projects;
- a wrong implementation interpretation would materially change player choice, feedback, pacing, reward or failure behavior.

Typical candidates:

- Core Loop / session flow
- combat
- AI / state machines
- progression / economy
- quest / stage / encounter transitions
- crafting / production chains
- complex UI/UX navigation or state flow
- reusable gameplay modules

`SYSTEM_BLUEPRINT_NOT_REQUIRED_FOR_TRIVIAL_WORK`

Do not require a Blueprint for:

- copy/text-only edits;
- isolated numeric tuning with unchanged logic;
- cosmetic-only style adjustments;
- one-off asset replacement with unchanged behavior;
- single-step implementation whose contract is already explicit and proven;
- repetitive content entry that does not change system topology.

## Node contract

Material nodes use a stable `Node ID`. A detailed node record contains the fields that are applicable to that node:

| Field | Meaning |
|---|---|
| `Node ID` | Stable identifier, e.g. `BP-COMBAT-012` |
| `Type` | `Trigger / Condition / Action / State / Data / Feedback / Output` |
| `Player Meaning / Intent` | Why the node matters to the player's experience or decision |
| `Trigger / Input` | Event, input, signal or incoming data that activates the node |
| `Condition` | Branch condition or prerequisite |
| `State / Data Change` | State transition or data mutation |
| `Output / Next` | Result and next node(s) |
| `Feedback` | UI, animation, audio, VFX, camera, text or other player-visible response |
| `Owner` | Human/system owner of the rule or data |
| `Godot Mapping` | Scene/Node/Resource/Signal/GDScript mapping when implementation-bound |
| `Validation` | Observable evidence that proves the intended behavior |

The Project Home does not need to expose every field. It should show the readable graph, node labels and the player-relevant meaning. Detailed fields remain in the linked/detail surface.

## Node graph rules

Use small, bounded graphs. Split the graph when one diagram begins mixing unrelated responsibility or becomes difficult to scan.

Recommended node semantics:

```text
[TRIGGER]     event or player action
[CONDITION]   branch / prerequisite
[ACTION]      behavior execution
[STATE]       state transition
[DATA]        meaningful data mutation
[FEEDBACK]    player-visible/audible response
[OUTPUT]      reward, failure, emitted event or handoff
```

A diagram alone is not an implementation contract. Stable Node IDs and the detailed text fields must allow an AI or developer to interpret the graph without guessing arrow meaning.

## Project Home presentation

`PROJECT_HOME_CORE_SYSTEM_BLUEPRINT_VISIBLE`

When System Blueprint is applicable, the Project Home places the most important Blueprint near the top-level Visual GDD material:

```text
Project definition / North Star
→ Core System Blueprint
→ Core Gameplay Loop / Full Flow
→ Major UI / Visual structure
→ Core data / tuning context
→ detail drilldown
```

This ordering is project-specific rather than a rigid universal template. A project may put the Core Loop before the Blueprint when that explains the game faster.

The Home should answer, without forcing a drilldown:

- What does the player do?
- What triggers the system?
- What meaningful choice or condition changes the path?
- What state/data changes?
- What feedback or reward/failure does the player receive?
- Which other major system does this connect to?

Do not expose raw SHA, PR/CI receipt, local path, raw implementation IDs or other AI/System operational metadata merely because they are linked to a Blueprint node.

## Detail / implementation mapping

A detailed Blueprint surface may add:

- node table;
- branch/edge conditions;
- state transition table;
- data owner and source mapping;
- error/edge cases;
- Godot scene / Node / Resource / Signal / GDScript mapping;
- deterministic scenario or manual-play validation criteria;
- links to repository owners/evidence.

Godot mapping is descriptive rather than generative. It does not create a new visual-scripting layer.

Typical mapping vocabulary:

```text
data ownership → Resource / structured project data owner
state          → state machine / explicit state owner
event          → Signal / callback / explicit message path
behavior       → Node / GDScript component
composition    → Scene / Node hierarchy
validation     → automated test / deterministic scenario / manual play evidence
```

Do not invent a mapping when the repository owner or implementation decision is not yet approved. Mark it as unresolved in the appropriate planning/AI surface instead.

## Lifecycle

```text
approved design or changed system decision
→ update human System Blueprint in the same approval unit
→ map material nodes to owners / implementation boundaries
→ implementation changes repository canon
→ run available tests / runtime / play verification
→ compare observed behavior with Blueprint intent
→ reconcile design + repository owner + derived Blueprint
```

An approved Blueprint proves design clarity, not runtime correctness. Runtime or play behavior remains `NOT_RUN` until actually executed.

## Project work entry and gradual rollout

`SYSTEM_BLUEPRINT_ENTRY_CHECK_REQUIRED`

`NO_MASS_BLUEPRINT_BACKFILL`

`REUSE_EXISTING_BLUEPRINT_BEFORE_CREATING_NEW`

Project work does **not** begin by converting every existing project or every system into Blueprint form. When a project task may materially change player-facing system logic or a connected flow, evaluate this contract after the existing reuse-first/current-state preflight and before implementation readiness.

```text
project task starts
→ restore current Project Home + repository owner + approved decisions
→ reuse-first preflight
→ SYSTEM_BLUEPRINT applicability check
   ├─ not applicable → NOT_APPLICABLE_WITH_REASON; continue lightweight workflow
   └─ applicable
       → existing approved Blueprint?
          ├─ yes → REUSE / ADAPT only the touched graph
          └─ no  → create the smallest bounded Blueprint needed for the touched system
       → update Home human projection when it changes human understanding
       → keep detailed Node ID / owner / mapping / validation in Detail or AI-System
       → implementation readiness / handoff
```

Operational rules:

- Untouched projects and unrelated systems are **not** incomplete merely because they have not been backfilled with Blueprint views.
- Do not run a repository-wide or Notion-wide Blueprint migration unless the user explicitly requests an audit/migration or a specific project needs it for current work.
- If a valid Blueprint already exists, update/reuse it instead of redrawing the same system from scratch.
- If the current task touches only one bounded subsystem, Blueprint only that subsystem; do not expand the graph to adjacent systems without decision-relevant need.
- `NOT_APPLICABLE_WITH_REASON` is a valid outcome for trivial or already-explicit work and must not become process debt.
- A stale or missing Blueprint blocks implementation readiness only when the current change passes `SYSTEM_BLUEPRINT_REQUIRED_WHEN_COMPLEX` and the missing representation would leave material behavior ambiguous.
- Handoff may reference the applicable Blueprint location, but the Blueprint does not replace repository canon, acceptance criteria, tests, or runtime evidence.
- The rollout unit is **project work as it is touched**, not the number of projects in the portfolio.

This gradual rollout preserves the existing project state while making Blueprint coverage grow naturally where it reduces planning-to-implementation interpretation loss.

## Review gates

Adversarial review checks at minimum:

1. **Third-canon drift** — Is the Blueprint duplicating data/rules that have a real owner elsewhere?
2. **Graph bloat** — Can unrelated responsibility be split into smaller bounded graphs?
3. **Arrow ambiguity** — Can each meaningful edge be interpreted without guessing?
4. **Home clutter** — Is the Project Home showing the human summary rather than raw implementation metadata?
5. **Process overhead** — Is the applicability gate preventing trivial work from requiring a Blueprint?
6. **Player meaning loss** — Does the graph show choices, consequences and feedback rather than only technical plumbing?
7. **Implementation reality** — Are unexecuted runtime claims still explicitly unverified?
8. **Rollout overreach** — Did the current task trigger unnecessary backfill or redraw of untouched projects/systems?

## Reuse and cross-project use

A Blueprint pattern may be `REUSE`, `ADAPT`, `REFERENCE_ONLY` or `NO_REUSE` according to the existing reuse system. Reusing a graph structure does not import another project's canon, values, visuals or player experience assumptions.

When a Blueprint reveals a reusable implementation module, record that module through the existing reuse handoff/registry flow after project proof. Do not create a parallel Blueprint-only module registry.

## Rollback

Removing a System Blueprint view or this workflow layer must not change repository code/data/runtime behavior. The rollback target is the derived Notion/contract representation; approved project decisions and repository canon remain intact.
