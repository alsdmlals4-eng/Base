# Context-Driven Reuse Synthesis + Human-Facing Artifact Patterns Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fail-closed context-driven reuse synthesis path alongside evidence-derived reverse engineering, use presentation-AI patterns as the first HYBRID workflow candidate, and reconcile stale completed-main P0 implementation states.

**Architecture:** Keep the existing Reuse Pipeline and owners. Add one companion synthesis contract, extend existing pipeline/template/Registry semantics, and add one provider-neutral workflow candidate. No new active Skill, default SaaS, paid dependency, or project runtime authority is introduced.

**Tech Stack:** Markdown contracts, Python unittest regression suite, existing GitHub Actions validation.

**Spec:** `docs/superpowers/specs/2026-08-22-context-driven-reuse-synthesis-and-human-publication-patterns-design.md`

## Global Constraints

- Open/draft/ready foreign PRs remain read-only.
- `SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS`, but `EVIDENCE_REQUIRED_FOR_PROMOTION`.
- Existing Solution First remains mandatory before new module/Tool/Skill creation.
- TodayFreeAI is discovery-only unless its exact body is fetched; product claims must come from official sources.
- No new paid subscription/API/runtime dependency.
- Presentation providers remain optional references, not Base defaults.
- Player/fun/visual-quality claims require corresponding human/runtime evidence.

---

### Task 1: Lock the dual-origin contract with RED tests

**Files:**
- Create: `tests/test_context_driven_reuse_synthesis.py`

**Interfaces:**
- Consumes: existing Reuse Pipeline, Project Reuse Scan template, Registry.
- Produces: regression requirements for origin/maturity/validation separation and provider-neutral human-facing artifact synthesis.

- [ ] **Step 1: Write failing tests** requiring:
  - `EVIDENCE_DERIVED`, `CONTEXT_SYNTHESIZED`, `HYBRID`
  - `SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS`
  - `CONTEXT_SYNTHESIS_IS_NOT_VALIDATION`
  - `EVIDENCE_REQUIRED_FOR_PROMOTION`
  - context packet fields including `context_basis`, `planned_consumers`, `falsification_test`, `smallest_pilot`
  - Registry origin/maturity/validation vocabulary
  - `RM-WORK-003 HUMAN_FACING_ARTIFACT_SYNTHESIS`
  - presentation workflow markers `OUTLINE_BEFORE_LAYOUT`, `EDITABLE_BLOCK_ARTIFACT`, `CLAIM_GAP_REVIEW_AFTER_GENERATION`, `EXPORT_IS_DERIVATIVE_NOT_CANON`
  - no default provider/adoption claim for Gamma/Canva/Beautiful.ai/Pitch/SlidesAI.

- [ ] **Step 2: Run repository CI on the test-only head.**
Expected: focused/whole-core RED because production contracts are absent.

### Task 2: Add the context-synthesis companion contract

**Files:**
- Create: `docs/knowledge/research/CONTEXT_DRIVEN_REUSE_SYNTHESIS.md`

**Interfaces:**
- Consumes: project canon, roadmap, current module Registry, Existing Solution First.
- Produces: `context_synthesis_packet` with origin/maturity/validation and falsification/pilot boundaries.

- [ ] **Step 1: Implement trigger taxonomy** for planned multi-consumer, predicted repeat cost, one-input/multi-output, responsibility tangle, composition opportunity, cross-project plan pattern, user reuse intent.
- [ ] **Step 2: Implement three-axis state model** and promotion ceilings.
- [ ] **Step 3: Define fail-closed YAGNI/rollback rules** so vague future usefulness cannot create durable modules.

### Task 3: Integrate dual-origin discovery into existing Reuse surfaces

**Files:**
- Modify: `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`
- Modify: `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`

**Interfaces:**
- Consumes: Task 2 contract.
- Produces: one unified project scan that can route either evidence-derived or context-synthesized candidates.

- [ ] **Step 1: Add `CANDIDATE_ORIGIN_GATE` before candidate search/reverse engineering.**
- [ ] **Step 2: Add context synthesis branch and rejoin at Existing Solution First.**
- [ ] **Step 3: Extend reusable contract with origin/context/evidence/falsification fields.**
- [ ] **Step 4: Make three-source comparison optional for pure context hypothesis but mandatory before claiming repeated external invariant.**

### Task 4: Absorb presentation-AI patterns as a provider-neutral HYBRID candidate

**Files:**
- Create: `docs/knowledge/game-development/reuse/HUMAN_FACING_ARTIFACT_SYNTHESIS.md`
- Modify: `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`

**Interfaces:**
- Consumes: official-source observations from Gamma, Canva, Beautiful.ai, Pitch, SlidesAI plus current Base human-facing publication context.
- Produces: `RM-WORK-003 HUMAN_FACING_ARTIFACT_SYNTHESIS` as `HYBRID · MODULE_CONTRACT_DEFINED · NOT_RUN` unless later project evidence exists.

- [ ] **Step 1: Record source observations with claim ceilings.**
- [ ] **Step 2: Define input modes Generate / Structure Existing / Import.**
- [ ] **Step 3: Require source+audience packet, outline-before-layout, evidence check, visual/brand constraints, editable artifact, layout variants, claim-gap review, human visual review, derivative export.**
- [ ] **Step 4: Explicitly state import-content != imported visual canon and provider use remains optional.**

### Task 5: Reconcile stale completed-main P0 states

**Files:**
- Modify: `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`
- Test: `tests/test_context_driven_reuse_synthesis.py`

**Interfaces:**
- Consumes: `P0_IMPLEMENTATION_PILOT.md` and RM-TOOL-003 merged-main evidence.
- Produces: Registry rows that no longer claim `IMPLEMENTATION_NOT_BUILT` for completed Base reference implementations.

- [ ] **Step 1: Update RM-TOOL-001, RM-SYS-001, RM-SYS-003, RM-VIS-001, RM-VIS-002 to include `REFERENCE_IMPLEMENTATION_EXISTS`.**
- [ ] **Step 2: Update RM-TOOL-003 from merged-main direct evidence only.**
- [ ] **Step 3: Do not infer project adoption beyond the dedicated evidence owners.**

### Task 6: Verify, adversarially review, merge, and read back

**Files:** no new product files.

- [ ] **Step 1: Run focused tests and whole-core regression.**
- [ ] **Step 2: Run all applicable repository required workflows.**
- [ ] **Step 3: Perform five full adversarial loops:**
  1. context invention overreach / YAGNI;
  2. evidence overclaim / state collapse;
  3. provider lock-in / paid-cost creep;
  4. module duplication / existing-owner bypass;
  5. stale-main / concurrent PR overlap / rollback.
- [ ] **Step 4: Re-read latest main, PR head, review threads, and required checks.**
- [ ] **Step 5: Squash merge only at exact reviewed head if all gates pass.**
- [ ] **Step 6: Read back merged files from new main and confirm same-goal open PRs are zero.**
