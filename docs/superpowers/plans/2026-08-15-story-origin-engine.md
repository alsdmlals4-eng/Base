# Multi-entry Story Origin Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 세계관·성격·가치관·관계·기관·직업·능력·질문·사건·전제·Reader Promise 중 어디서든 시작해 `SEED → PRESSURE → CHOICE → CHANGE → NEXT_PRESSURE`로 변환하는 `STORY_ORIGIN_ENGINE` 공용 작법 Method를 Base에 추가하고 기존 서사 consumer에 연결한다.

**Architecture:** 새 Skill·Skill Mode·Registry 항목을 만들지 않는다. `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`가 유일한 공용 owner이며, 기존 `NARRATIVE_AND_RELATIONSHIP_METHOD`, serial-fiction Guide/Skill, 게임 `NARRATIVE_CONTENT_PLAN`, Source Radar가 필요한 경우에만 이 owner를 소비한다. `RELATIONAL_APPEAL`은 조합 품질 검수, `STORY_ORIGIN_ENGINE`은 이야기 발생·확장을 소유해 책임을 분리한다.

**Tech Stack:** Markdown knowledge/Skill/template contracts, Python `unittest`, GitHub Actions existing Base validation workflows.

## Global Constraints

- Base branch for this work: `docs/story-origin-engine-20260815`.
- Approved design: `docs/superpowers/specs/2026-08-15-story-origin-engine-design.md`.
- Plan-time current main: `1e9a9ae4b2e480ba7cc1549e7627264889d51610`; re-read latest `main` before ready/merge.
- `primary_seed_count: 1`.
- `secondary_seed_count: 0..2`.
- `all_seed_completion_required: false`.
- Required engine chain: `SEED → AFFECTED_AGENT → PRESSURE → DESIRE / GOAL → RESISTANCE → CONSEQUENTIAL_CHOICE → CONSEQUENCE → STATE / VALUE / RELATIONSHIP_SHIFT → NEXT_PRESSURE`.
- `CONSEQUENTIAL_CHOICE` is not synonymous with `PLAYER_BRANCH_REQUIRED`.
- MICE, Snowflake, Story Genius, Want/Need/Lie/Truth, Truby, Save the Cat, Story Grid remain optional diagnostic/generation lenses, not universal Base formulas.
- No new ACTIVE Skill, Skill Mode, Registry entry, Work Mode, runtime code, project Canon, Save/Data Schema, or relationship-stat system.
- Do not modify or synchronize any other open/draft PR branch. Only reconcile this branch against completed `main` changes before merge.
- Do not claim project-specific story quality, human reader/player response, commercial effect, or universal superiority from Base contract tests.

---

## File Structure

### Create

- `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`
  - Sole common owner of story seed selection, seed-to-pressure conversion, the 11 seed families, story-origin packet, failure states, interactive boundary, and downstream handoff.

### Modify

- `tests/test_serial_fiction_discipline.py`
  - Extend the existing narrative craft contract suite with four focused `STORY_ORIGIN_ENGINE` tests. Do not create a separate standalone test island.
- `docs/knowledge/README.md`
  - Add the new Method to the knowledge routing table.
- `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
  - Link upstream to the new owner only when story seed/pressure is not yet fixed; preserve `RELATIONAL_APPEAL` as downstream combination audit.
- `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`
  - Add optional story-origin use for new story/arc/episode generation between Reader Promise and scene dramatization; do not force it on proofreading or already-fixed canon revision.
- `skills/developing-and-revising-serial-fiction/SKILL.md`
  - Connect existing `arc-and-episode-design` work to the new Method without adding a Skill Mode or changing front-matter identity.
- `skills/developing-and-revising-serial-fiction/LEARNING_LOG.md`
  - Record the multi-entry story-origin learning, framework-Lens boundary, and evidence ceiling required by skill freshness governance.
- `templates/planning/NARRATIVE_CONTENT_PLAN.md`
  - Add an optional `0. 이야기 발생` section for new narrative/event ideation; preserve all existing scene/content fields.
- `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`
  - Record the reviewed craft sources and claim ceilings under existing `STORY_ARCHITECTURE_GENRE_AND_SERIALIZATION`; the Radar remains discovery/evidence routing, not craft authority.

No changes to `skills/SKILL_REGISTRY.json`, `skills/SKILL_BEHAVIOR_EVALS.json`, `START_HERE.md`, Work Mode definitions, runtime code, or project schemas are planned.

---

### Task 1: Add the RED contract surface

**Files:**
- Modify: `tests/test_serial_fiction_discipline.py` — constants near the existing `ROOT/SKILL_PATH/GUIDE_ROOT` declarations and four tests beside `test_relational_appeal_has_common_owner_and_serial_fiction_consumers`.

**Interfaces:**
- Consumes: existing `ROOT`, `SKILL_PATH`, `GUIDE_ROOT`, `REFERENCE_ROOT` test constants.
- Produces: focused contracts that later tasks make Green; no production file is modified in this task.

- [ ] **Step 1: Add shared paths for the new owner and consumers**

Insert:

```python
METHOD_ROOT = ROOT / "docs" / "knowledge" / "methods"
STORY_ORIGIN_METHOD_PATH = METHOD_ROOT / "STORY_ORIGIN_AND_GENERATION_METHOD.md"
NARRATIVE_METHOD_PATH = METHOD_ROOT / "NARRATIVE_AND_RELATIONSHIP_METHOD.md"
KNOWLEDGE_README_PATH = ROOT / "docs" / "knowledge" / "README.md"
NARRATIVE_TEMPLATE_PATH = ROOT / "templates" / "planning" / "NARRATIVE_CONTENT_PLAN.md"
SOURCE_RADAR_PATH = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md"
)
```

- [ ] **Step 2: Add the common-owner contract test**

Add:

```python
def test_story_origin_engine_common_owner_is_multi_entry_and_bounded(self) -> None:
    self.assertTrue(STORY_ORIGIN_METHOD_PATH.is_file())
    method = STORY_ORIGIN_METHOD_PATH.read_text(encoding="utf-8")

    for token in (
        "STORY_ORIGIN_ENGINE",
        "AFFECTED_AGENT",
        "PRESSURE",
        "DESIRE / GOAL",
        "RESISTANCE",
        "CONSEQUENTIAL_CHOICE",
        "CONSEQUENCE",
        "STATE / VALUE / RELATIONSHIP_SHIFT",
        "NEXT_PRESSURE",
        "primary_seed_count: 1",
        "secondary_seed_count: 0..2",
        "all_seed_completion_required: false",
        "CHARACTER",
        "VALUE_BELIEF",
        "RELATIONSHIP",
        "WORLD_MILIEU",
        "INSTITUTION",
        "OCCUPATION_ROLE",
        "ABILITY_RESOURCE_RULE",
        "INQUIRY",
        "EVENT",
        "PREMISE",
        "GENRE_READER_PROMISE",
        "LORE_WITHOUT_AGENT",
        "TRAIT_WITHOUT_TEST",
        "VALUE_AS_SLOGAN",
        "INSTITUTION_AS_LABEL",
        "JOB_AS_COSTUME",
        "EVENT_WITHOUT_DECISION",
        "MYSTERY_WITHOUT_STAKES",
        "FRAMEWORK_CHECKLIST_OVERFIT",
        "PLAYER_BRANCH_REQUIRED",
        "RELATIONAL_APPEAL",
    ):
        self.assertIn(token, method)

    registry = (ROOT / "skills" / "SKILL_REGISTRY.json").read_text(encoding="utf-8").lower()
    self.assertNotIn('"skill_id": "story-origin', registry)
    self.assertNotIn('"skill_id": "story_origin', registry)
```

- [ ] **Step 3: Add the common routing/boundary contract test**

Add:

```python
def test_story_origin_engine_is_discoverable_and_hands_off_to_scene_craft(self) -> None:
    knowledge = KNOWLEDGE_README_PATH.read_text(encoding="utf-8")
    narrative = NARRATIVE_METHOD_PATH.read_text(encoding="utf-8")
    method_path = "methods/STORY_ORIGIN_AND_GENERATION_METHOD.md"

    self.assertIn(method_path, knowledge)
    self.assertIn("STORY_ORIGIN_AND_GENERATION_METHOD.md", narrative)
    self.assertIn("STORY_ORIGIN_ENGINE", narrative)
    self.assertIn("RELATIONAL_APPEAL", narrative)
```

- [ ] **Step 4: Add the serial-fiction consumer contract test**

Add:

```python
def test_story_origin_engine_serial_fiction_consumers_are_optional(self) -> None:
    skill = SKILL_PATH.read_text(encoding="utf-8")
    guide = (GUIDE_ROOT / "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md").read_text(
        encoding="utf-8"
    )
    learning = (ROOT / "skills" / SKILL_ID / "LEARNING_LOG.md").read_text(
        encoding="utf-8"
    )

    for consumer in (skill, guide):
        self.assertIn("STORY_ORIGIN_AND_GENERATION_METHOD.md", consumer)
        self.assertIn("STORY_ORIGIN_ENGINE", consumer)

    self.assertIn("arc-and-episode-design", skill)
    self.assertIn("다중 진입", learning)
    self.assertIn("STORY_ORIGIN_ENGINE", learning)
```

- [ ] **Step 5: Add the game-template/source-evidence contract test**

Add:

```python
def test_story_origin_engine_game_template_and_source_evidence_are_linked(self) -> None:
    template = NARRATIVE_TEMPLATE_PATH.read_text(encoding="utf-8")
    radar = SOURCE_RADAR_PATH.read_text(encoding="utf-8")

    for token in (
        "STORY_ORIGIN_AND_GENERATION_METHOD.md",
        "primary_seed",
        "affected_agent",
        "pressure",
        "consequential_choice",
        "next_pressure",
    ):
        self.assertIn(token, template)

    for token in (
        "STORY_ORIGIN_AND_GENERATION_METHOD.md",
        "MICE",
        "Snowflake",
        "Story Genius",
        "Truby",
        "Institutionalized",
        "Story Grid",
    ):
        self.assertIn(token, radar)
```

- [ ] **Step 6: Run RED before creating the owner**

Local command when a checkout is available:

```bash
python -m unittest \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_common_owner_is_multi_entry_and_bounded \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_is_discoverable_and_hands_off_to_scene_craft \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_serial_fiction_consumers_are_optional \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_game_template_and_source_evidence_are_linked \
  -v
```

Expected: FAIL because `STORY_ORIGIN_AND_GENERATION_METHOD.md` and the new consumer links do not exist yet. Existing unrelated serial-fiction contracts must not fail.

If execution is GitHub-connector-only, commit this RED test state and open/update a draft PR so the existing `Validate Game Project Operating System` workflow runs the same test file. Record the exact RED head/run/job and verify the failures are limited to these new expectations.

- [ ] **Step 7: Commit the RED contract**

```bash
git add tests/test_serial_fiction_discipline.py
git commit -m "test: add RED story origin engine contract"
```

---

### Task 2: Implement the common `STORY_ORIGIN_ENGINE` owner

**Files:**
- Create: `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`

**Interfaces:**
- Consumes: approved Spec sections 3–11 and existing `NARRATIVE_AND_RELATIONSHIP_METHOD.md` downstream boundary.
- Produces: `STORY_ORIGIN_ENGINE`, 11 seed families, `story_origin_packet`, failure states, interactive boundary, and handoff contract consumed by later tasks.

- [ ] **Step 1: Create the Method header and authority boundary**

The file must start with:

```markdown
# 이야기 기원·생성 방법

- 상태: 공용 방법
- 목적: 세계·인물·가치·관계·기관·직업·능력·질문·사건·전제·Reader Promise 중 하나의 seed를 실제 이야기 압력·선택·변화로 발전시킨다.
- 외부 Source 발견: `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`의 `STORY_ARCHITECTURE_GENRE_AND_SERIALIZATION`

외부 작법 프레임워크는 프로젝트 정본보다 높은 권한을 갖지 않는다. 이 Method는 MICE, Snowflake, Story Genius, Want/Need/Lie/Truth, Truby, Save the Cat, Story Grid를 선택적 Lens로만 사용하며 어느 하나를 모든 작품의 필수 구조로 만들지 않는다.
```

- [ ] **Step 2: Add the exact engine contract and seed budget**

Include:

```text
SEED
→ AFFECTED_AGENT
→ PRESSURE
→ DESIRE / GOAL
→ RESISTANCE
→ CONSEQUENTIAL_CHOICE
→ CONSEQUENCE
→ STATE / VALUE / RELATIONSHIP_SHIFT
→ NEXT_PRESSURE
```

and:

```yaml
primary_seed_count: 1
secondary_seed_count: 0..2
all_seed_completion_required: false
```

Define `PRESSURE` broadly enough to include responsibility, opportunity, curiosity, social expectation, relationship asymmetry, time/resource limits, value contradiction, and quiet routine disruption. Define `AFFECTED_AGENT` as individual, relationship, team, family, institution/community, or multiple player-controlled characters rather than only a single protagonist.

- [ ] **Step 3: Add all 11 seed families with the approved generation questions**

Use these headings exactly and copy the approved questions/limits from Spec §5 without adding mandatory fields:

```markdown
### `CHARACTER`
### `VALUE_BELIEF`
### `RELATIONSHIP`
### `WORLD_MILIEU`
### `INSTITUTION`
### `OCCUPATION_ROLE`
### `ABILITY_RESOURCE_RULE`
### `INQUIRY`
### `EVENT`
### `PREMISE`
### `GENRE_READER_PROMISE`
```

Preserve the explicit rule under `ABILITY_RESOURCE_RULE`: existing costs/limits may matter, but do not invent a cost or side effect for every ability.

- [ ] **Step 4: Add the optional story-origin packet and minimum executable condition**

Include:

```yaml
story_origin_packet:
  primary_seed:
  secondary_seeds: []
  seed_statement:
  affected_agent:
  pressure:
  desire_or_goal:
  resistance:
  consequential_choice:
  consequence:
  shift:
  next_pressure:
  reader_or_player_value:
  canon_constraints:
```

and:

```text
SEED
+ AFFECTED_AGENT
+ PRESSURE
+ CHOICE_OR_COMMITMENT
+ OBSERVABLE_CHANGE
```

State explicitly that `CHOICE_OR_COMMITMENT` can be a character commitment or executed approach, not only a menu branch.

- [ ] **Step 5: Add the seven-step generation procedure**

Use the approved sequence from Spec §7:

```text
A. Seed를 한 문장으로 제한
B. 가장 큰 압력을 받는 Agent 탐색
C. 압력을 행동 목표로 번역
D. Resistance 생성
E. Consequential Choice 생성
F. Shift 확인
G. Next Pressure 생성
```

Keep `Resistance` broader than a villain and keep `Shift` focused on observable state/value/relationship change rather than event spectacle.

- [ ] **Step 6: Add downstream boundaries and failure states**

Include the exact responsibility split:

```text
STORY_ORIGIN_ENGINE
= 무엇에서 이야기를 시작하고 어떻게 압력·선택·변화로 변환할지 생성한다.

RELATIONAL_APPEAL
= 선택된 요소들의 조합이 실제로 더 흥미로운 선택·갈등·대사·행동·결과를 만드는지 검수한다.
```

Include the downstream handoff to `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md` and these failure codes:

```text
LORE_WITHOUT_AGENT
TRAIT_WITHOUT_TEST
VALUE_AS_SLOGAN
INSTITUTION_AS_LABEL
JOB_AS_COSTUME
ABILITY_AS_PREMISE_DECORATION
EVENT_WITHOUT_DECISION
MYSTERY_WITHOUT_STAKES
SEED_ACCUMULATION_WITHOUT_PRESSURE
FRAMEWORK_CHECKLIST_OVERFIT
```

Also state that `CONSEQUENTIAL_CHOICE` is not `PLAYER_BRANCH_REQUIRED` and the Method does not create Save/Data Schema fields.

- [ ] **Step 7: Run the common-owner focused test**

```bash
python -m unittest \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_common_owner_is_multi_entry_and_bounded \
  -v
```

Expected: PASS. The other three new tests may still be RED until their consumers are wired.

- [ ] **Step 8: Commit the common owner**

```bash
git add docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md
git commit -m "docs: add multi-entry story origin method"
```

---

### Task 3: Make the owner discoverable and connect scene craft

**Files:**
- Modify: `docs/knowledge/README.md` — routing table in `## 6. 라우팅`.
- Modify: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md` — header/intro before `## 1. 장면의 최소 단위`.

**Interfaces:**
- Consumes: `STORY_ORIGIN_AND_GENERATION_METHOD.md` from Task 2.
- Produces: knowledge-hub discovery and the upstream→downstream handoff into scene/relationship craft.

- [ ] **Step 1: Add a dedicated knowledge routing row**

In `docs/knowledge/README.md`, insert before the existing `서사·관계` row:

```markdown
| 이야기 발상·생성 | `methods/STORY_ORIGIN_AND_GENERATION_METHOD.md` |
```

Do not replace the existing `서사·관계` row.

- [ ] **Step 2: Add the upstream link to the narrative/relationship Method**

After the authority paragraph and before `## 1. 장면의 최소 단위`, add:

```markdown
새 이야기·사건·퀘스트의 seed, affected agent, pressure, consequential choice가 아직 정해지지 않았다면 먼저 `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`의 `STORY_ORIGIN_ENGINE`을 사용한다. 이미 무엇이 발생하고 누가 무엇을 선택하는지가 정해졌다면 이 단계를 반복하지 않는다.

`STORY_ORIGIN_ENGINE`은 이야기 발생을, 아래 `RELATIONAL_APPEAL`은 선택된 요소 조합의 장면 가치를, 이 Method는 장면·대사·선택·기억의 실행을 각각 소유한다.
```

- [ ] **Step 3: Run the routing/boundary test**

```bash
python -m unittest \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_is_discoverable_and_hands_off_to_scene_craft \
  -v
```

Expected: PASS.

- [ ] **Step 4: Commit the discovery/boundary wiring**

```bash
git add \
  docs/knowledge/README.md \
  docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md
git commit -m "docs: route story origin into narrative craft"
```

---

### Task 4: Connect serial-fiction planning without creating a mode

**Files:**
- Modify: `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md` — after `## 3. Reader Promise` and before current scene-experience section.
- Modify: `skills/developing-and-revising-serial-fiction/SKILL.md` — existing `arc-and-episode-design` description and `Read first` block; do not add a Skill Mode bullet.
- Modify: `skills/developing-and-revising-serial-fiction/LEARNING_LOG.md` — append one dated learning record.

**Interfaces:**
- Consumes: common `STORY_ORIGIN_ENGINE` owner and existing Reader Promise/arc planning.
- Produces: optional serial-fiction consumer link plus governance-required learning evidence.

- [ ] **Step 1: Add an optional origin section to the serial-fiction Guide**

Between Reader Promise and scene dramatization, add a subsection with this contract:

```markdown
### 새 이야기·아크·에피소드 기원이 비어 있을 때 — `STORY_ORIGIN_ENGINE`

새 이야기·아크·에피소드를 발상하거나 기존 Reader Promise에서 다음 사건을 생성해야 할 때 `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`를 선택적으로 사용한다.

```text
Reader Promise 또는 현재 seed
→ AFFECTED_AGENT
→ PRESSURE
→ DESIRE / GOAL
→ RESISTANCE
→ CONSEQUENTIAL_CHOICE
→ CONSEQUENCE / SHIFT
→ 다음 회차가 소비할 NEXT_PRESSURE
```

이미 정본 사건·인과·회차 목표가 확정된 단순 퇴고에서는 story origin을 다시 만들지 않는다. 정본을 더 흥미롭게 만들기 위해 보호된 사건 결과를 바꾸지 않는다.
```

Keep the existing Reader Promise and scene-experience text intact; renumber later numeric headings only if necessary for readability, without semantic edits.

- [ ] **Step 2: Link the existing `arc-and-episode-design` mode without adding a new mode**

Extend the existing `arc-and-episode-design` description so it states that, when a new arc/episode story seed is not yet fixed, it may consume `STORY_ORIGIN_ENGINE` to generate pressure/choice/shift before applying Episode Value and pacing.

In `## Read first`, add after the serial-fiction writing guide entry:

```markdown
새 이야기·아크·에피소드의 발생 원인이 아직 비어 있으면 `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`의 `STORY_ORIGIN_ENGINE`을 선택적으로 읽는다.
```

Do not alter front-matter `name`, do not create `story-origin-design` or any other Skill Mode, and do not change `skills/SKILL_REGISTRY.json`.

- [ ] **Step 3: Append the learning record**

Append a dated section containing all of these points:

```markdown
## 2026-08-15 — 다중 진입 이야기 기원 엔진 흡수

- 세계관·성격·가치관·관계·기관·직업·능력·질문·사건·전제·Reader Promise 중 어느 하나도 보편적 유일 출발점으로 두지 않는다.
- `STORY_ORIGIN_ENGINE`은 seed를 `AFFECTED_AGENT → PRESSURE → CHOICE → SHIFT → NEXT_PRESSURE`로 변환하고, `RELATIONAL_APPEAL`은 이후 조합의 장면 가치를 검수한다.
- MICE, Snowflake, Story Genius, Want/Need/Lie/Truth, Truby, Save the Cat, Story Grid는 `Lens`이며 필수 공식이 아니다.
- Base 계약 Green은 프로젝트별 이야기 품질·독자 반응·상업 효과를 증명하지 않는다.
```

- [ ] **Step 4: Run the serial-fiction consumer test**

```bash
python -m unittest \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_serial_fiction_consumers_are_optional \
  -v
```

Expected: PASS.

- [ ] **Step 5: Run the full serial-fiction discipline suite**

```bash
python -m unittest tests/test_serial_fiction_discipline.py -v
```

Expected: all existing and new tests implemented through Task 4 pass except the game-template/source-evidence test, which remains RED until Task 5.

- [ ] **Step 6: Commit the serial-fiction consumer**

```bash
git add \
  docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md \
  skills/developing-and-revising-serial-fiction/SKILL.md \
  skills/developing-and-revising-serial-fiction/LEARNING_LOG.md
git commit -m "docs: connect serial fiction to story origin engine"
```

---

### Task 5: Connect game narrative planning and record source evidence

**Files:**
- Modify: `templates/planning/NARRATIVE_CONTENT_PLAN.md` — header plus a new optional `## 0. 이야기 발생` section before existing `## 1. 콘텐츠 목표`.
- Modify: `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md` — existing `## 5. STORY_ARCHITECTURE_GENRE_AND_SERIALIZATION` section.

**Interfaces:**
- Consumes: common story-origin owner and reviewed external craft sources from the approved Spec.
- Produces: a reusable game-planning input surface and durable evidence-routing record.

- [ ] **Step 1: Update the template ownership header**

Replace the single-method header with:

```markdown
> 문서 위치: `templates/planning/NARRATIVE_CONTENT_PLAN.md` | 이야기 발생: `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md` | 장면·대화·관계 실행: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
```

- [ ] **Step 2: Add the optional story-origin section**

Before `## 1. 콘텐츠 목표`, add:

```markdown
## 0. 이야기 발생 — 새 이야기·사건을 만들 때만

이미 사건·목표·정본이 확정된 장면의 단순 작성·퇴고라면 이 절을 다시 만들지 않는다.

```yaml
story_origin_packet:
  primary_seed:
  secondary_seeds: []
  seed_statement:
  affected_agent:
  pressure:
  desire_or_goal:
  resistance:
  consequential_choice:
  consequence:
  shift:
  next_pressure:
  reader_or_player_value:
  canon_constraints:
```

기본은 Primary Seed 1개와 필요한 Secondary Seed 0~2개다. 모든 seed 유형을 채우지 않는다. `consequential_choice`는 플레이어 분기를 자동 요구하지 않는다.
```

Keep existing sections 1–12 unchanged except for downstream references that must point back to this packet.

- [ ] **Step 3: Record benchmark sources in the existing Source Radar section**

Under `## 5. STORY_ARCHITECTURE_GENRE_AND_SERIALIZATION`, add a small table titled `### Story Origin / Generation craft lenses` with these rows and claim ceilings:

```markdown
| Source | role | use | claim ceiling |
|---|---|---|---|
| **Writing Excuses — MICE Quotient** | `PROFESSIONAL_PRACTICE` | Milieu·Inquiry·Character·Event처럼 서로 다른 story thread 출발점과 conflict/closure 질문을 비교 | 네 분류를 모든 작품의 완전한 taxonomy나 필수 구조로 만들지 않음 |
| **Advanced Fiction Writing — Snowflake Method** | `PROFESSIONAL_PRACTICE` | 작은 seed에서 character·conflict·scene으로 점진 확장하는 방법 참고 | 전체 단계 수와 순서를 Base 필수 workflow로 복제하지 않음 |
| **Lisa Cron — Story Genius** | `PROFESSIONAL_PRACTICE` | 외부 사건을 인물의 판단·내적 논리와 연결하는 character-first Lens | 모든 이야기를 과거 상처·오해에서 시작한다고 일반화하지 않음 |
| **K. M. Weiland — Want/Need/Lie/Truth** | `PROFESSIONAL_PRACTICE` | 가치관·욕망·변화 방향을 진단하는 선택적 character-arc Lens | 모든 인물에게 네 칸이나 Positive Change Arc를 강제하지 않음 |
| **John Truby — The Anatomy of Story** | `PROFESSIONAL_PRACTICE` | premise·character·theme·world·plot·scene 상호작용 참고 | 22-step이나 moral argument 형식을 Base 필수 구조로 만들지 않음 |
| **Save the Cat — Institutionalized** | `PROFESSIONAL_PRACTICE` | 조직·집단 규칙과 개인 위치에서 story pressure를 찾는 Lens | 특정 세 결말·희생 구조를 모든 기관 이야기의 결말로 강제하지 않음 |
| **Story Grid** | `PROFESSIONAL_PRACTICE` | 사건 전후 value/state shift가 실제인지 확인하는 downstream Lens | 모든 scene을 하나의 polarity table이나 beat formula에 맞추지 않음 |
```

Immediately below the table, add:

```markdown
공용 craft owner는 `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`다. 이 Radar는 Source 발견·claim ceiling만 기록하며 실제 이야기 생성 규칙의 권위를 소유하지 않는다.
```

- [ ] **Step 4: Run the game-template/source-evidence test**

```bash
python -m unittest \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_game_template_and_source_evidence_are_linked \
  -v
```

Expected: PASS.

- [ ] **Step 5: Run all four new story-origin tests together**

```bash
python -m unittest \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_common_owner_is_multi_entry_and_bounded \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_is_discoverable_and_hands_off_to_scene_craft \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_serial_fiction_consumers_are_optional \
  tests.test_serial_fiction_discipline.SerialFictionDisciplineContractTests.test_story_origin_engine_game_template_and_source_evidence_are_linked \
  -v
```

Expected: PASS 4/4.

- [ ] **Step 6: Commit the game planning and evidence wiring**

```bash
git add \
  templates/planning/NARRATIVE_CONTENT_PLAN.md \
  docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
git commit -m "docs: connect story origin to game narrative planning"
```

---

### Task 6: Regression, adversarial review, and exact-main reconciliation

**Files:**
- Modify only if a valid in-scope defect is found: the files listed in Tasks 1–5.
- Do not add a new Skill, Mode, Registry entry, schema, or unrelated refactor during review.

**Interfaces:**
- Consumes: complete implementation from Tasks 1–5.
- Produces: verified branch state suitable for ready-for-review/merge.

- [ ] **Step 1: Run the complete serial-fiction discipline regression**

```bash
python -m unittest tests/test_serial_fiction_discipline.py -v
```

Expected: PASS.

- [ ] **Step 2: Run repository governance tests that cover this change type**

```bash
python -m unittest \
  tests/test_reference_freshness.py \
  tests/test_skill_routing_governance.py \
  tests/test_skill_package_integrity.py \
  tests/test_documentation_governance.py \
  -v
```

Expected: PASS. If the current CI topology executes a broader required suite, use that required suite as the higher evidence source.

- [ ] **Step 3: Run adversarial review against the approved attack list**

Record one `attack → validate-critique → minimal refinement → regression recheck → decision` pass covering exactly:

```text
1. 11 seed families accidentally became an 11-field checklist.
2. CHARACTER became a hidden default or superior seed.
3. WORLD/INSTITUTION/OCCUPATION lost their own pressure-generation logic.
4. Quiet stories are forced into violence/crisis/sacrifice.
5. Games are forced into player branches, relationship stats, or new Save/Data state.
6. STORY_ORIGIN_ENGINE duplicates RELATIONAL_APPEAL instead of handing off to it.
7. MICE/Snowflake/Story Genius/Truby/Save the Cat/Story Grid became universal rules.
8. The new Method is orphaned with no real consumer.
```

Only a validated issue may produce `ACCEPTED_MINIMAL_REFINEMENT`. Re-run the focused test affected by any refinement immediately.

- [ ] **Step 4: Re-read latest `main` and same-goal PRs**

Before ready/merge, fetch current `main` SHA and search open/recent PRs for `story origin`, `story engine`, `narrative generation`, and the exact changed paths.

Rules:

```text
open/draft/ready PR belonging to another goal → inspect only, do not modify
same-goal duplicate → stop and reconcile ownership before merge
completed main change → reconcile this branch to latest main
path overlap with unrelated completed main change → compare exact content before carrying this patch forward
```

- [ ] **Step 5: Reconcile to latest main without losing this branch's scoped changes**

Use a normal merge/rebase/current-main reconciliation supported by the active GitHub tooling. Preserve only the approved changed paths plus Spec/Plan. Do not force-update another branch.

- [ ] **Step 6: Run exact-head GitHub Actions**

Required evidence before merge:

```text
Validate Game Project Operating System: SUCCESS
Validate Base v9 Operating Contracts: SUCCESS
Validate Evidence-Based Game Development Knowledge: SUCCESS when triggered for the changed Source Radar/knowledge paths
unresolved review threads: 0
P0/P1 blockers: 0
```

Record exact branch head, reconciled base SHA, workflow run IDs, and any skipped platform job accurately. A skipped job is not a passed execution claim.

- [ ] **Step 7: Update PR body from RED state to final evidence**

The final PR body must state:

```text
Summary: multi-entry story origin owner + bounded consumers
TDD RED: exact head/run/job and expected missing-owner/consumer failures
GREEN: exact reconciled head/base and required workflow results
Adversarial review: accepted/refuted findings
No new Skill/Mode/Registry/schema/runtime authority
Evidence ceiling: PROJECT_PILOT_NOT_RUN / HUMAN_NOT_RUN / commercial NOT_RUN
Rollback: revert this PR as one unit
```

- [ ] **Step 8: Merge only after current Base merge authority is satisfied**

Use exact expected head SHA. Do not merge while required checks are pending, branch is stale against completed `main`, review blockers exist, or another same-goal change has superseded this implementation.

- [ ] **Step 9: Post-merge readback and validation**

After merge, verify on `main` that:

```text
STORY_ORIGIN_AND_GENERATION_METHOD.md exists
STORY_ORIGIN_ENGINE core chain is present
11 seed families remain optional, not mandatory
NARRATIVE_AND_RELATIONSHIP_METHOD links upstream and retains RELATIONAL_APPEAL
serial-fiction Guide/Skill links exist
NARRATIVE_CONTENT_PLAN story_origin_packet exists
Source Radar contains the bounded craft-source table
SKILL_REGISTRY has no new story-origin Skill
post-merge required workflow is Green
```

Do not claim project-specific narrative quality until a later project pilot produces story packets and human/player evidence.

---

## Plan Self-Review

### Spec coverage

- Common bounded owner: Task 2.
- 11 seed catalog + optional budget: Task 2.
- seed→pressure→choice→shift→next-pressure conversion: Task 2.
- `RELATIONAL_APPEAL` responsibility boundary: Tasks 2–3.
- interactive/player-branch boundary: Tasks 2 and 5.
- serial-fiction consumer: Task 4.
- game narrative planning consumer: Task 5.
- source evidence/claim ceilings: Task 5.
- learning record: Task 4.
- focused RED/GREEN contract: Tasks 1–5.
- no Skill/Mode/Registry growth: global constraints + Tasks 1/4/6.
- adversarial review, latest-main reconciliation, exact-head CI, rollback/readback: Task 6.

### Placeholder scan

No `TBD`, `TODO`, deferred implementation, unnamed test, or unspecified consumer remains in this plan.

### Interface consistency

All tasks use the same owner path `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`, the same marker `STORY_ORIGIN_ENGINE`, the same 11 seed names, and the same conversion-chain field names defined by the approved Spec.