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

- [x] **Step 1: Write failing tests** requiring:
  - `EVIDENCE_DERIVED`, `CONTEXT_SYNTHESIZED`, `HYBRID`
  - `SOURCE_NOT_REQUIRED_FOR_HYPOTHESIS`
  - `CONTEXT_SYNTHESIS_IS_NOT_VALIDATION`
  - `EVIDENCE_REQUIRED_FOR_PROMOTION`
  - context packet fields including `context_basis`, `planned_consumers`, `falsification_test`, `smallest_pilot`
  - Registry origin/maturity/validation vocabulary
  - `RM-WORK-003 HUMAN_FACING_ARTIFACT_SYNTHESIS`
  - presentation workflow markers `OUTLINE_BEFORE_LAYOUT`, `EDITABLE_BLOCK_ARTIFACT`, `CLAIM_GAP_REVIEW_AFTER_GENERATION`, `EXPORT_IS_DERIVATIVE_NOT_CANON`
  - no default provider/adoption claim for Gamma/Canva/Beautiful.ai/Pitch/SlidesAI.

- [x] **Step 2: Run repository CI on the test-only head.**
Observed RED: whole-core failed on the intended missing production contracts and stale Registry rows.

### Task 2: Add the context-synthesis companion contract

**Files:**
- Create: `docs/knowledge/research/CONTEXT_DRIVEN_REUSE_SYNTHESIS.md`

- [ ] Implement trigger taxonomy, three-axis state model, promotion ceilings, and fail-closed YAGNI/rollback rules.

### Task 3: Integrate dual-origin discovery into existing Reuse surfaces

**Files:**
- Modify: `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`
- Modify: `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`

- [ ] Add `CANDIDATE_ORIGIN_GATE` and context synthesis branch.
- [ ] Extend reusable contract with origin/context/evidence/falsification fields.
- [ ] Keep multi-source comparison required for external invariant claims, not for pure context hypotheses.

### Task 4: Absorb presentation-AI patterns as a provider-neutral HYBRID candidate

**Files:**
- Create: `docs/knowledge/game-development/reuse/HUMAN_FACING_ARTIFACT_SYNTHESIS.md`
- Modify: `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`

- [ ] Record official-source observations with claim ceilings.
- [ ] Define Generate / Structure Existing / Import inputs and outline-before-layout flow.
- [ ] Preserve editable artifact, post-generation claim-gap review, human visual review, and derivative export boundaries.

### Task 5: Reconcile stale completed-main P0 states

**Files:**
- Modify: `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`

- [ ] Set RM-TOOL-001, RM-SYS-001, RM-SYS-003, RM-VIS-001, RM-VIS-002, RM-TOOL-003 to `REFERENCE_IMPLEMENTATION_EXISTS` based on completed-main evidence only.
- [ ] Do not infer project adoption beyond dedicated evidence owners.

### Task 6: Verify, adversarially review, merge, and read back

- [ ] Run focused tests and whole-core regression.
- [ ] Run all applicable required workflows.
- [ ] Run five full adversarial loops: YAGNI, evidence ceilings, provider lock-in/cost, duplicate owner, concurrency/freshness/rollback.
- [ ] Re-read latest main, PR head, review threads, and required checks.
- [ ] Squash merge exact reviewed head only if all gates pass.
- [ ] Read back merged files and confirm same-goal open PRs are zero.
