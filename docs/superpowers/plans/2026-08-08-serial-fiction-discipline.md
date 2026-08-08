# Serial Fiction Writing Discipline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one Base specialist Skill for serial-fiction planning, drafting, revision, pacing/payoff, continuity, and reader-feedback diagnosis without copying successful works or turning platform-specific length conventions into universal rules.

**Architecture:** `developing-and-revising-serial-fiction` owns fiction-specific quality decisions while existing intake, design-document, adversarial-review, reference-freshness, Skill-evolution, and BCP owners keep their current authority. A four-file `docs/knowledge/serial-fiction/` hub stores reusable craft guidance; Registry and behavior-eval metadata make the Skill discoverable, while focused contract tests prevent over-routing, fixed-count rules, style-copy guidance, comment-as-canon, and framework overfit.

**Tech Stack:** Markdown Skill/Knowledge contracts, JSON Skill Registry/evals/evidence, Python `unittest`, GitHub Actions current Base validation.

## Global Constraints

- Keep exactly one new ACTIVE Skill identity: `developing-and-revising-serial-fiction`.
- Do not change frozen Base v9.0 release lock, snapshot, or plugin payload.
- Base must not contain 《폭풍의 눈》 character names, plot events, fixed POV count, genre ratio, or TRPG-specific canon as reusable rules.
- Do not encode `5,000`, `5,500`, `6,000`, or `공백 제외 2,000자` as a universal completion rule.
- Do not copy or recommend copying a living/current writer's wording, voice, dialogue, metaphors, or scene text.
- Reader comments and reviews are external evidence: `RAW_REACTION → SYMPTOM_CLUSTER → REVISION_HYPOTHESIS`; they are never canon or direct commands.
- Frameworks such as Story Grid, Save the Cat, Story Circle, Hero's Journey, dialogue/action ratios, binary-choice crises, and fixed sentence lengths are optional diagnostic lenses, not mandatory scene formulas.
- Mystery may hide answers, but current POV, immediate goal, obstacle/risk, and changed state must remain trackable.
- Slow scenes are valid when state changes; reject stagnation, not slowness.
- Implementation must include a positive route and a non-selection boundary for generic proofreading/game design/marketing writing.
- Existing `running-adversarial-review-and-refinement` remains the adversarial-review authority.

---

### Task 1: Add RED contract tests for the missing serial-fiction discipline

**Files:**
- Create: `tests/test_serial_fiction_discipline.py`
- Modify: `.github/workflows/validate-game-project-operating-system.yml`

**Interfaces:**
- Consumes: current Base filesystem contracts.
- Produces: `SerialFictionDisciplineContractTests`, permanently executed by the `ubuntu-contract` test list.

- [ ] **Step 1: Write the failing contract test**

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_ID = "developing-and-revising-serial-fiction"
SKILL_PATH = ROOT / "skills" / SKILL_ID / "SKILL.md"
GUIDE_ROOT = ROOT / "docs" / "knowledge" / "serial-fiction"


class SerialFictionDisciplineContractTests(unittest.TestCase):
    def test_skill_and_knowledge_hub_exist(self) -> None:
        self.assertTrue(SKILL_PATH.is_file())
        for name in (
            "README.md",
            "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md",
            "SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md",
            "READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md",
        ):
            self.assertTrue((GUIDE_ROOT / name).is_file(), name)

    def test_registry_routes_serial_fiction_without_overrouting(self) -> None:
        registry = json.loads((ROOT / "skills" / "SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        matches = [entry for entry in registry["skills"] if entry["skill_id"] == SKILL_ID]
        self.assertEqual(len(matches), 1)
        entry = matches[0]
        self.assertEqual(entry["status"], "ACTIVE")
        joined = "\n".join(entry["trigger_tags"] + entry["use_when"] + entry["do_not_use_when"])
        for token in ("webnovel", "serial-fiction", "pov", "reader-feedback", "proofreading", "game"):
            self.assertIn(token, joined.lower())

    def test_craft_contract_prefers_episode_value_over_fixed_character_counts(self) -> None:
        text = (GUIDE_ROOT / "SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md").read_text(encoding="utf-8")
        pacing = (GUIDE_ROOT / "SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md").read_text(encoding="utf-8")
        combined = text + "\n" + pacing
        for token in (
            "Reader Promise",
            "Episode Value",
            "Local Payoff",
            "Open Loop",
            "Information Legibility",
            "Pattern Variation",
            "Consequence Memory",
            "Setup–Payoff",
            "FRAMEWORK_OVERFIT",
            "PLATFORM_REVERIFY_REQUIRED",
        ):
            self.assertIn(token, combined)
        self.assertIn("universal", combined.lower())
        self.assertIn("production target", combined.lower())

    def test_reader_feedback_is_evidence_not_canon(self) -> None:
        text = (GUIDE_ROOT / "READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md").read_text(encoding="utf-8")
        for token in ("RAW_REACTION", "SYMPTOM_CLUSTER", "REVISION_HYPOTHESIS", "PRODUCT_FACT", "READER_RESPONSE", "CRAFT_HYPOTHESIS", "TRANSFER_DECISION"):
            self.assertIn(token, text)
        self.assertIn("not canon", text.lower())
        self.assertIn("REJECT_COPY", text)

    def test_cold_start_routes_to_serial_fiction_owner(self) -> None:
        start = (ROOT / "START_HERE.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs" / "DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        operating = (ROOT / "docs" / "OPERATING_MODEL.md").read_text(encoding="utf-8")
        for text in (start, docs, operating):
            self.assertIn(SKILL_ID, text)

    def test_behavior_evals_cover_primary_and_non_selection(self) -> None:
        primary = json.loads((ROOT / "skills" / "SKILL_BEHAVIOR_EVALS.json").read_text(encoding="utf-8"))
        coverage = json.loads((ROOT / "skills" / "SKILL_BEHAVIOR_COVERAGE_EVALS.json").read_text(encoding="utf-8"))
        self.assertTrue(any(case.get("expected_primary_skill") == SKILL_ID for case in primary["cases"]))
        self.assertTrue(any(case.get("target_skill") == SKILL_ID and case.get("expected_selected") is False for case in coverage["cases"]))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Add the new test to CI syntax and contract lists**

Add `tests/test_serial_fiction_discipline.py` to both the `python -m py_compile` list and the `python -m unittest` list in `ubuntu-contract`.

- [ ] **Step 3: Run remote CI and verify RED**

Expected: `ubuntu-contract` fails in `test_serial_fiction_discipline.py` because the Skill/Knowledge/Registry routes do not exist yet. Preserve the failing run/head as RED evidence.

- [ ] **Step 4: Commit**

```bash
git add tests/test_serial_fiction_discipline.py .github/workflows/validate-game-project-operating-system.yml
git commit -m "test: define serial fiction discipline contracts"
```

### Task 2: Implement the Skill and reusable craft guides

**Files:**
- Create: `skills/developing-and-revising-serial-fiction/SKILL.md`
- Create: `skills/developing-and-revising-serial-fiction/references/episode-quality-gates.md`
- Create: `skills/developing-and-revising-serial-fiction/references/benchmark-and-reader-feedback.md`
- Create: `skills/developing-and-revising-serial-fiction/LEARNING_LOG.md`
- Create: `docs/knowledge/serial-fiction/README.md`
- Create: `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`
- Create: `docs/knowledge/serial-fiction/SERIAL_EPISODE_PACING_AND_PAYOFF_GUIDE.md`
- Create: `docs/knowledge/serial-fiction/READER_FEEDBACK_AND_BENCHMARK_EVIDENCE_GUIDE.md`

**Interfaces:**
- Consumes: project canon priorities, source/adaptation boundary, work identity, current arc/episode/scene, draft, POV/voice state, setup/payoff state, reader-feedback evidence, current platform constraints.
- Produces: bounded fiction plan/draft/revision result with explicit mode, protected canon, quality gates, evidence, unresolved items, and `NOT_RUN` ceilings.

- [ ] **Step 1: Implement Skill frontmatter and six modes**

Frontmatter:

```yaml
---
name: developing-and-revising-serial-fiction
description: Use when planning, drafting, adapting, revising, or diagnosing a serial novel/webnovel where arc/episode structure, POV/voice, scene prose, continuity, pacing/payoff, setup-payoff debt, or reader-feedback evidence materially affects quality. Do not use for game-system design, generic marketing copy, simple proofreading-only edits, or imitation of another writer's style.
---
```

The body must define exactly these modes:
`canon-and-continuity`, `arc-and-episode-design`, `pov-and-character-voice`, `draft-and-prose`, `serial-pacing-and-payoff`, `reader-feedback-and-revision`.

- [ ] **Step 2: Implement shared gates and failure markers**

Include:
`READER_PROMISE_MISSING`, `EPISODE_VALUE_MISSING`, `LOCAL_PAYOFF_MISSING`, `INFORMATION_LEGIBILITY_FAILURE`, `PATTERN_REPETITION_UNVARIED`, `CONSEQUENCE_MEMORY_MISSING`, `SETUP_PAYOFF_DEBT_UNTRACKED`, `COMMENT_AS_CANON`, `STYLE_COPY_RISK`, `FRAMEWORK_OVERFIT`, `PLATFORM_REVERIFY_REQUIRED`.

- [ ] **Step 3: Write the main writing/revision guide**

Required sections: canon before adaptation; reader promise; scene experience versus event summary; POV as information/attention/value filter; dialogue/subtext/action; concrete materiality; slow versus stagnant; consequence memory; revision pass order; optional framework lenses; originality boundary.

- [ ] **Step 4: Write the episode/pacing/payoff guide**

Required policy order:

```text
Episode Value
→ scene/episode completeness
→ rhythm
→ platform contract
→ production target character count
```

Required setup-payoff states:
`SETUP`, `RECALL`, `PARTIAL_PAYOFF`, `PAYOFF`, `RETIRED`, `DEFERRED`.

- [ ] **Step 5: Write benchmark/reader-feedback evidence guide**

Required evidence pipeline:

```text
PRODUCT_FACT
READER_RESPONSE
CRAFT_HYPOTHESIS
TRANSFER_DECISION
```

Required transfer decisions:
`ADOPT_INVARIANT`, `ADAPT_AS_LENS`, `PROJECT_ONLY`, `REJECT_COPY`, `INSUFFICIENT_EVIDENCE`.

Reader pipeline:
`RAW_REACTION → SYMPTOM_CLUSTER → REVISION_HYPOTHESIS`.

- [ ] **Step 6: Run the focused test**

Run: `python -m unittest tests/test_serial_fiction_discipline.py -v`
Expected: routing/eval portions still fail; file/gate portions pass.

- [ ] **Step 7: Commit**

```bash
git add skills/developing-and-revising-serial-fiction docs/knowledge/serial-fiction
git commit -m "feat: add serial fiction writing discipline"
```

### Task 3: Wire cold-start routing and current operating documentation

**Files:**
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: Skill ID and Knowledge Hub from Task 2.
- Produces: one-hop discovery from Base cold start without redefining the Skill contract in multiple documents.

- [ ] **Step 1: Add one-hop routing**

Route prompts about `소설 / 웹소설 / 연재소설 / 각색 / 원고 퇴고 / POV / 회차 pacing / 독자 댓글 진단` to `developing-and-revising-serial-fiction`, while pointing detailed procedure to its `SKILL.md` and Knowledge Hub.

- [ ] **Step 2: Add responsibility row in Operating Model**

State only the responsibility summary; do not duplicate the full gate list.

- [ ] **Step 3: Register the Knowledge Hub in Documentation Map**

Register its authority as reusable serial-fiction craft, explicitly excluding project-specific canon and platform-stale fixed numbers.

- [ ] **Step 4: Record Changelog entry**

Record BCP-2026-009 implementation and frozen-v9.0 non-change boundary.

- [ ] **Step 5: Run focused test**

Expected: cold-start assertions pass; Registry/eval assertions remain RED.

- [ ] **Step 6: Commit**

```bash
git add START_HERE.md docs/DOCUMENTATION_MAP.md docs/OPERATING_MODEL.md docs/CHANGELOG.md
git commit -m "docs: route serial fiction work"
```

### Task 4: Register the Skill and behavior/evidence contracts

**Files:**
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `docs/generated/BASE_ACTIVE_SKILLS.md`
- Modify: `skills/SKILL_BEHAVIOR_EVALS.json`
- Modify: `skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json`
- Modify: `skills/SKILL_IMPLEMENTATION_EVIDENCE.json`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Consumes: exact Skill identity and modes from Task 2.
- Produces: machine-routable ACTIVE Skill and positive/non-selection behavior evidence.

- [ ] **Step 1: Add Registry entry**

Use `layer: discipline`, `discipline: serial-fiction-writing-and-revision`, `status: ACTIVE`, and trigger tags including:
`serial-fiction`, `webnovel`, `novel-writing`, `fiction-revision`, `adaptation`, `pov`, `character-voice`, `episode-pacing`, `setup-payoff`, `reader-feedback`.

`do_not_use_when` must explicitly cover `proofreading-only`, `game-system-design`, `marketing-copy`, and `style-imitation`.

- [ ] **Step 2: Add positive behavior eval**

Example prompt:
`원본 TRPG 사건 결과는 보존하면서 이 웹소설 회차를 2차 퇴고해줘. POV 목소리, 회차 보상, 복선 회수와 다음 화 흡입력도 같이 점검해줘.`

Expected primary: `developing-and-revising-serial-fiction`.
Supporting: `managing-project-intake-and-work-contract` only when scope/canon ambiguity requires it.

- [ ] **Step 3: Add non-selection coverage**

At minimum:
- `이 전투 시스템의 DPS와 적 AI 난이도를 설계해줘.` → target Skill not selected.
- `이 한 문장 맞춤법만 고쳐줘.` → target Skill not selected.
- `게임 개발 유튜브 대본을 써줘.` → target Skill not selected.

- [ ] **Step 4: Add implementation evidence and learning entry**

Evidence must identify BCP-2026-009, approved lifecycle, focused test, behavior coverage, external benchmark evidence path, and `HUMAN_NOT_RUN`/`PROJECT_PILOT_NOT_RUN` ceilings.

- [ ] **Step 5: Rebuild current human-readable Skill view without touching frozen v9.0 artifacts**

Ensure `docs/generated/BASE_ACTIVE_SKILLS.md` shows the new ACTIVE Skill and correct current count. Do not modify `.codex-plugin/plugin.json`, `base.lock.json`, or `skills/BASE_V9_SKILL_SNAPSHOT.json`.

- [ ] **Step 6: Run focused and Registry/behavior tests**

Run:

```bash
python -m unittest tests/test_serial_fiction_discipline.py tests/test_skill_package_integrity.py tests/test_skill_system_coverage.py -v
python tools/check_skill_system_coverage.py
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add skills/SKILL_REGISTRY.json docs/generated/BASE_ACTIVE_SKILLS.md skills/SKILL_BEHAVIOR_EVALS.json skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json skills/SKILL_IMPLEMENTATION_EVIDENCE.json skills/SKILL_LEARNING_LOG.md
git commit -m "feat: register serial fiction skill routing"
```

### Task 5: Integrate contract test into canonical CI and finish TDD GREEN

**Files:**
- Modify: `.github/workflows/validate-game-project-operating-system.yml`
- Test: `tests/test_serial_fiction_discipline.py`

**Interfaces:**
- Consumes: all Task 2–4 artifacts.
- Produces: mandatory CI consumption of the new contract.

- [ ] **Step 1: Confirm test remains in ubuntu-contract syntax and regression lists**

No separate duplicate workflow is introduced.

- [ ] **Step 2: Run the full applicable remote validation**

Expected required jobs: `docs-validation`, `ubuntu-contract`, `publication-validation` when classified, and final `ci-gate`; any additional Base v9/skill behavior workflows triggered by changed files must also pass.

- [ ] **Step 3: Record RED/GREEN evidence in the Skill learning log or PR body**

Record exact RED head/run and exact GREEN head/run. Do not report human reader quality as verified.

- [ ] **Step 4: Commit any minimal CI-consumption correction**

```bash
git add .github/workflows/validate-game-project-operating-system.yml tests/test_serial_fiction_discipline.py skills/developing-and-revising-serial-fiction/LEARNING_LOG.md
git commit -m "test: enforce serial fiction discipline contract"
```

### Task 6: Run adversarial review and regression recheck

**Files:**
- Modify only files implicated by validated findings.
- Review: whole implementation diff against BCP-2026-009.

**Interfaces:**
- Consumes: implementation diff and CI evidence.
- Produces: finding dispositions with no unresolved P0/P1 before merge.

- [ ] **Step 1: Attack the implementation**

Test these failure hypotheses:
- generic proofreading is over-routed to the new Skill;
- game-concept benchmark responsibility was duplicated;
- design-document canon authority was duplicated;
- project-specific 《폭풍의 눈》 facts leaked into Base reusable guidance;
- a fixed character count is still implied as universal;
- `slow` was accidentally treated as failure;
- every scene is still forced into one framework;
- comments can still become direct requirements;
- living-author style imitation is encouraged;
- setup/payoff tracking became bureaucracy for tiny one-shot scenes;
- frozen v9.0 artifacts changed;
- generated active Skill view or behavior coverage is stale.

- [ ] **Step 2: Validate each critique against actual files and tests**

Classify `MUST_FIX`, `SHOULD_FIX`, `USER_DECISION_REQUIRED`, `ACCEPTED_RISK`, or `REJECTED_CRITIQUE`.

- [ ] **Step 3: Apply only approved/within-scope corrections**

Do not add a second fiction Skill or new broad policy unless an independent responsibility is demonstrated.

- [ ] **Step 4: Re-run focused and full regression**

Expected: all required CI success on the same exact head used for merge.

### Task 7: Finalize BCP implementation state and merge

**Files:**
- Modify: `[수정제안서]/BCP-2026-009-serial-fiction-writing-and-revision-discipline/PROPOSAL.md`
- Modify: `[수정제안서]/PROPOSAL_REGISTRY.json`

**Interfaces:**
- Consumes: implementation PR URL/number and exact verified head.
- Produces: `IMPLEMENTED` BCP state with implementation PR reference.

- [ ] **Step 1: Set BCP to IMPLEMENTED only after implementation PR exists**

Set `implementation_pr` to the actual GitHub PR URL in both proposal and Registry as required by the Base BCP checker.

- [ ] **Step 2: Re-run proposal validation**

Run: `python tools/check_base_change_proposals.py --base-ref <current-main-sha>`
Expected: PASS.

- [ ] **Step 3: Verify exact-head diff, CI, and review threads**

Required:
- branch behind main = 0;
- no unintended paths;
- required workflows success;
- unresolved review threads = 0;
- P0/P1 = 0.

- [ ] **Step 4: Merge using the repository-allowed method with expected head SHA**

Do not request a second approval for this already-approved scope.

- [ ] **Step 5: Post-merge verify main**

Confirm merged commit on `main`, read back BCP state and Skill route, and record any residual `HUMAN_NOT_RUN` / project-pilot limitations.
