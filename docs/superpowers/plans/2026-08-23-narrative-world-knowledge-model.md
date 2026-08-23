# Narrative & World Knowledge Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reusable narrative/world research and canon-organization layer that separates knowledge, events and evidence, supports summary-first Center Peek detail in Notion, and enforces text approval before visual production.

**Architecture:** Base adds one focused common Method and routes existing serial-fiction/knowledge documentation to it. Notion implements the five conceptual layers through three physical databases: Knowledge Master, Event Ledger and Evidence Ledger. COC-Fiction is a bounded pilot: infrastructure and views are created first, but unapproved Part 1 prose is not promoted.

**Tech Stack:** Markdown policy/method docs, Python contract tests, GitHub PR workflow, Notion databases/relations/views.

**Spec:** `docs/superpowers/specs/2026-08-23-narrative-world-knowledge-model-design.md`

## Global Constraints

- Open/draft/ready PRs are read-only; PR #620 must not be modified, merged or copied from.
- No direct push to `main`; use the current-task branch and PR.
- No new broad Skill; extend existing routing only.
- No character/world image generation before user-approved text.
- Asset Library remains visual-asset authority, not narrative-canon authority.
- Notion human views show short summaries first; detailed database pages open through native peek behavior.
- Candidate/legacy/source material never silently becomes confirmed canon.
- COC Part 1/Bridge/Part 2/Rift Accord boundaries remain explicit.

---

### Task 1: Add the Base knowledge model Method and routing

**Files:**
- Create: `docs/knowledge/methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md`
- Modify: `docs/knowledge/README.md`
- Modify: `skills/developing-and-revising-serial-fiction/SKILL.md`

**Interfaces:**
- Consumes: `NARRATIVE_AND_RELATIONSHIP_METHOD.md`, `CHARACTER_AND_NARRATIVE_ART_METHOD.md`, `NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`
- Produces: `NARRATIVE_WORLD_KNOWLEDGE_MODEL` contract and routing reference for canon/character/world extraction tasks.

- [ ] **Step 1: Write the common Method from the approved spec**

The Method must contain the exact conceptual chain:

```text
AUTHORITY_MAP
→ ENTITY_EXTRACTION
→ EVENT_EXTRACTION
→ RELATION_RULE_EXTRACTION
→ EVIDENCE_LINK
→ CONTRADICTION_AUDIT
→ HUMAN_PRIMER
→ USER_APPROVAL
→ VISUAL_GATE
```

It must define the three Notion physical stores and the status enums from the spec.

- [ ] **Step 2: Route the knowledge README**

Add this row under `docs/knowledge/README.md` routing:

```markdown
| 서사·세계관 정본 조사·구조화 | `methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md` |
```

- [ ] **Step 3: Route the serial-fiction Skill**

In `skills/developing-and-revising-serial-fiction/SKILL.md`, add the Method to `Read first` for canon/character/world extraction and make explicit that Character Bible prose must not be drafted directly from raw sources before structured extraction and conflict audit.

- [ ] **Step 4: Commit Task 1**

```bash
git add docs/knowledge/methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md docs/knowledge/README.md skills/developing-and-revising-serial-fiction/SKILL.md
git commit -m "docs: add narrative world knowledge model"
```

### Task 2: Add regression tests for the contract

**Files:**
- Create: `tests/test_narrative_world_knowledge_model.py`

**Interfaces:**
- Consumes: Method and routing files from Task 1
- Produces: fail-closed checks for the required layers, visual gate and routing.

- [ ] **Step 1: Write the failing contract test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
METHOD = ROOT / "docs/knowledge/methods/NARRATIVE_WORLD_KNOWLEDGE_MODEL.md"
README = ROOT / "docs/knowledge/README.md"
SKILL = ROOT / "skills/developing-and-revising-serial-fiction/SKILL.md"


def test_narrative_world_knowledge_model_contract():
    text = METHOD.read_text(encoding="utf-8")
    for token in [
        "AUTHORITY_MAP",
        "ENTITY_EXTRACTION",
        "EVENT_EXTRACTION",
        "RELATION_RULE_EXTRACTION",
        "EVIDENCE_LINK",
        "CONTRADICTION_AUDIT",
        "HUMAN_PRIMER",
        "USER_APPROVAL",
        "VISUAL_GATE",
        "NARRATIVE KNOWLEDGE · Master",
        "NARRATIVE EVENT · Ledger",
        "CANON EVIDENCE · Ledger",
        "BLOCKED_BY_TEXT",
        "READY_FOR_VISUAL",
        "CORE_CONFIRMED",
        "CURRENT_CANDIDATE",
        "CONFLICT",
    ]:
        assert token in text


def test_knowledge_model_is_routed():
    assert "NARRATIVE_WORLD_KNOWLEDGE_MODEL.md" in README.read_text(encoding="utf-8")
    assert "NARRATIVE_WORLD_KNOWLEDGE_MODEL.md" in SKILL.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run the focused test**

Run:

```bash
python -m pytest tests/test_narrative_world_knowledge_model.py -q
```

Expected before Task 1 completion: FAIL. Expected after Task 1 completion: PASS.

- [ ] **Step 3: Commit Task 2**

```bash
git add tests/test_narrative_world_knowledge_model.py
git commit -m "test: guard narrative world knowledge contract"
```

### Task 3: Build the common Notion storage layer

**Files/Surfaces:**
- Create Notion DB: `NARRATIVE KNOWLEDGE · Master`
- Create Notion DB: `NARRATIVE EVENT · Ledger`
- Create Notion DB: `CANON EVIDENCE · Ledger`
- Parent: `90 · SYSTEM MASTERS`

**Interfaces:**
- Consumes: PROJECT REGISTRY · Master relation
- Produces: shared structured stores for all projects.

- [ ] **Step 1: Create Knowledge Master**

Create exactly the properties defined in the spec, including `Text Approval`, `Visual Gate`, `Canon Status`, self-relations and Project relation.

- [ ] **Step 2: Create Event Ledger**

Create the event properties from the spec and relate `Participants` to Knowledge Master.

- [ ] **Step 3: Create Evidence Ledger**

Create evidence properties and relations to Knowledge Master and Event Ledger.

- [ ] **Step 4: Read back all three schemas**

Acceptance:
- Project relation targets `PROJECT REGISTRY · Master`.
- Evidence has separate Knowledge/Event targets.
- Knowledge has a text approval gate separate from visual gate.
- No visual file/prompt fields are used as canon authority.

### Task 4: Build summary-first Notion views and Base human guide

**Files/Surfaces:**
- Create Notion page under `P09 · Content, Narrative & Publication`: `Narrative & World Knowledge Model · 요약 → 상세`
- Create linked Gallery/Table views.

**Interfaces:**
- Consumes: three master DBs from Task 3
- Produces: human-readable primer and reusable filtered view pattern.

- [ ] **Step 1: Create the P09 guide page**

The page must explain:

```text
요약 카드
→ 카드 클릭
→ Center Peek 상세
→ 필요한 섹션만 펼치기
```

It must include the common conceptual model, authority order, text-first visual gate and conflict rules.

- [ ] **Step 2: Create Knowledge gallery views**

Create at minimum:
- `인물 · 요약 → 상세`
- `세력 · 요약 → 상세`
- `세계/규칙 · 요약 → 상세`
- `장소 · 요약 → 상세`

Each Gallery shows only:
- Name
- Summary
- Core Function
- Scope
- Canon Status
- Text Approval

Gallery is chosen because Notion opens Gallery cards in Center Peek by default.

- [ ] **Step 3: Create Event and Evidence audit views**

Create:
- `사건 · 요약 → 상세`
- `정본 충돌 / 미검증`

The evidence view filters `CONFLICTS` and `UNVERIFIED` first.

- [ ] **Step 4: Fetch/readback the guide and views**

Acceptance: overview content remains short and detailed fields are not duplicated onto the human overview page.

### Task 5: Apply the infrastructure to COC-Fiction without promoting unapproved prose

**Files/Surfaces:**
- Modify Notion page: `04 · Character Bible · 인물`
- Modify Notion page: `02 · Story Bible · Canon`
- Modify Notion page: `Visual · COC-Fiction Composition Board`

**Interfaces:**
- Consumes: new common DBs and existing COC canon pages
- Produces: filtered COC views and explicit legacy/visual separation.

- [ ] **Step 1: Fix Character Bible ownership**

Add a filtered linked Gallery from `NARRATIVE KNOWLEDGE · Master`:

```text
Project = Coc소설
Type = Character
Text Approval = APPROVED
```

Label it as the narrative character index.

Move the meaning of the current Asset Library inline view to `Visual Assets / Reference`; do not treat it as character canon.

- [ ] **Step 2: Add Story/World filtered views**

On Story Bible add filtered views for:
- Type = Faction / Location / World Rule / Setting / Relationship
- Project = Coc소설

Do not create detailed COC rows from the unapproved Part 1 draft in this task.

- [ ] **Step 3: Keep visual pipeline downstream of text approval**

Update COC Composition Board so `Text Approval = APPROVED` is required before `Visual Gate = READY_FOR_VISUAL`.

- [ ] **Step 4: Read back COC pages**

Acceptance:
- Character Bible no longer presents Asset Library as the narrative source of truth.
- New narrative views can remain empty until the user approves the text.
- Existing generated images remain candidates/replaced references only.

### Task 6: Run repository validation and adversarial review

**Files:** no new required files unless a verified finding requires a bounded fix.

**Interfaces:**
- Consumes: exact branch head from Tasks 1–5
- Produces: evidence for PR readiness.

- [ ] **Step 1: Run focused tests**

```bash
python -m pytest tests/test_narrative_world_knowledge_model.py -q
```

- [ ] **Step 2: Run relevant repository checks discovered from AGENTS/workflows**

At minimum run the documentation/skill routing tests that cover modified files. Do not use PR #620 branch/check results as evidence.

- [ ] **Step 3: Complete five full adversarial loops**

Each loop attacks the full approved scope for:

1. duplicate responsibility / owner conflict
2. canon/candidate contamination
3. Notion usability / summary-detail overload
4. cross-project reuse / schema overfit
5. visual gate bypass / evidence ceiling

Any valid finding is fixed, revalidated, then the next loop re-attacks the improved whole.

- [ ] **Step 4: Implementation Reality Gate**

Report separately:
- method implemented
- tests passed
- Notion schemas created/read back
- COC views connected
- COC content migration not yet claimed until user-approved text exists
- mobile Center Peek geometry not claimed without device observation

### Task 7: Open and complete the current-task PR

**Files:** current branch only.

**Interfaces:**
- Consumes: validated exact branch head
- Produces: current-task PR; merge only under Base current-task continuation rules and repository checks.

- [ ] **Step 1: Open a new PR against `main`**

PR body must state:
- benchmark sources and three alternatives
- PR #620 remained read-only
- COC pilot does not promote unapproved prose
- Notion readback evidence
- test commands/results

- [ ] **Step 2: Run exact-head checks/review gates**

Do not merge if repository-required checks, review, ruleset or unresolved-thread gates fail.

- [ ] **Step 3: Merge only if current-task continuation authorization and repository gates both allow it**

No admin bypass, force push or direct `main` push.

- [ ] **Step 4: Postmerge readback**

Confirm new Method/routing on merged `main` and re-fetch Notion P09/COC pages.
