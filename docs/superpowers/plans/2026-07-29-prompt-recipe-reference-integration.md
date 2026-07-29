# PromptRecipe Reference Integration Implementation Plan

> **For agentic workers:** This plan records the approved implementation and the TDD evidence used to refine its boundary. The final architecture below supersedes the initial direct-Skill-edit hypothesis.

**Goal:** Integrate PromptRecipe and similar image/prompt examples into the existing Base art-technique workflow so an AI can forecast likely image results and explain why each prompt expression is expected to move the result toward the requested target.

**Final architecture:** Keep `designing-art-prompts-and-technique-cards` and its Registry entry unchanged. Add one Source Audit and one detailed Recipe Card, then connect both from the existing `templates/planning/ART_TECHNIQUE_CARD.md` used by `technique-card` mode. Validate the contract with a focused unittest in the existing Evidence Knowledge workflow.

**Tech stack:** Markdown, YAML examples, Python `unittest`, GitHub Actions.

## 1. Global constraints

- Do not add a new shared Skill ID, Skill mode, or Registry trigger.
- Do not copy PromptRecipe prompt bodies, protected images, identifiable characters, logos, signatures, named-artist instructions, or unique compositions into Base.
- Treat similar images and similar prompts as separate reference evidence.
- Treat pre-generation forecasts as `LOW / MEDIUM / HIGH` confidence hypotheses, never guarantees.
- Connect every important prompt phrase to a desired observable result, reasoning basis, expected model response, and risk/correction.
- Keep actual project prompts, generated images, approved assets, model/account settings, and runtime evidence in project repositories.
- Do not modify Godot code, Scene, Resource, game data, project Google Sheets, or approved project assets.
- Preserve the existing art-prompt Skill, Pinterest/FACS/poster contracts, lifecycle states, QA, Registry, and Learning Log.
- Use GitHub Actions as the execution environment because local GitHub DNS is unavailable.

## 2. Baseline and conflict audit

- Base fork point: `main@0fd95f4513343e77fd664af2763a01b02f52545b`.
- Same-goal open PR before work: none.
- Related open PR: #62, UX/UI polishing. Its final changed paths do not overlap this plan's final paths.
- Existing execution owner: `designing-art-prompts-and-technique-cards: technique-card`.
- Existing machine routing: `image-prompt` and `technique-card`; sufficient for this request.

## 3. Task 1 — Establish TDD RED

**Files**

- Create `tests/test_prompt_recipe_reference_contract.py`.
- Modify `.github/workflows/validate-evidence-knowledge.yml`.
- Modify `tests/test_evidence_knowledge_workflow_contract.py`.

**Required failing behaviors**

- Source Audit file is missing.
- Recipe Card file is missing.
- The existing Art Technique Card does not yet link the forecast/reasoning contract.

**Validation**

- Open Draft PR #63.
- Run `Validate Evidence-Based Game Development Knowledge` on the RED commit.
- Accept RED only when failure is caused by missing planned artifacts, not YAML/Python errors or unrelated regressions.

**Observed result**

- Run `30449161396`: failure.
- Missing Source Audit and Recipe Card were detected as intended.

## 4. Task 2 — Add Source Audit

**Create**

- `docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md`

**Contract**

- `source_status: PARTIALLY_VERIFIED`
- `source_decision: REFERENCE_ONLY`
- Separate homepage observations from unverified individual page content, rights, model settings, and reproducibility.
- Define similar-image analysis, similar-prompt analysis, pre-generation forecast limits, prompt reverse inference, rights/non-copying boundaries, Base/project responsibility, and revalidation conditions.
- Explicitly prohibit copying full prompt bodies and claiming `VERIFIED` without actual generation and QA.

## 5. Task 3 — Add detailed Recipe Card

**Create**

- `templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md`

**Required fields**

```yaml
source_audit:
purpose:
similar_image_references:
similar_prompt_references:
pre_generation_forecast:
  prediction_confidence: LOW | MEDIUM | HIGH
  confidence_basis:
  unverified_assumptions:
prompt_derivation:
  desired_observation_to_prompt:
    desired_observation:
    prompt_expression:
    reasoning_basis:
    expected_model_response:
    risk_and_correction:
prompt_modules:
generation_record:
actual_result_review:
  prediction_status: PREDICTION_NOT_TESTED | PREDICTION_PARTIALLY_MATCHED | PREDICTION_MATCHED | PREDICTION_FAILED | MODEL_OR_CONTEXT_CHANGED_RETEST_REQUIRED
knowledge_state_decision:
```

**QA**

- Project identity and approved visuals are protected.
- Target-size readability, anatomy, weapons, text, logo, perspective, lighting, production feasibility, rights, and actual-result comparison are reviewed.

## 6. Task 4 — Connect through the existing Technique Card

**Modify**

- `templates/planning/ART_TECHNIQUE_CARD.md`

**Architecture decision**

The first implementation changed `skills/designing-art-prompts-and-technique-cards/SKILL.md`. Reference freshness correctly required Registry, Learning Log, and existing companion-test changes. Because the request does not introduce a new trigger, mode, input authority, or approval boundary, that expansion was excessive.

The final implementation therefore:

- restores the Skill and existing BCA test to their baseline blobs;
- keeps Registry and Learning Log unchanged;
- adds a `레퍼런스 기반 생성 전 예측·프롬프트 추론` section to the existing Art Technique Card;
- links the Source Audit and detailed Recipe Card;
- keeps only summary fields in the Art Technique Card and detailed fields in the Recipe Card.

**Required output contract**

- Similar image observations.
- Similar prompt observations.
- `ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY` decision.
- Expected result, likely failures, confidence, confidence basis, unverified assumptions.
- Desired observation → prompt expression → reasoning → expected response → risk/correction table.
- Forecast-versus-result comparison and minimum module to change.

## 7. Task 5 — Validate workflow and regressions

**Focused suite**

```text
Validate Evidence-Based Game Development Knowledge
```

Must compile and run:

- existing Evidence Knowledge tests;
- human validation governance;
- synthetic tester governance;
- PromptRecipe focused contract.

**Repository suite**

```text
Validate Game Project Operating System
```

Must pass:

- changed-file classification;
- docs whitespace and lightweight contracts;
- Python syntax;
- Base proposal validation;
- canonical reference freshness;
- contract/governance regressions;
- publication validation;
- Windows publication smoke;
- stable `ci-gate`.

## 8. Final changed paths

```text
.github/workflows/validate-evidence-knowledge.yml
docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md
docs/superpowers/plans/2026-07-29-prompt-recipe-reference-integration.md
docs/superpowers/specs/2026-07-29-prompt-recipe-reference-integration-design.md
templates/planning/ART_TECHNIQUE_CARD.md
templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md
tests/test_evidence_knowledge_workflow_contract.py
tests/test_prompt_recipe_reference_contract.py
```

No final diff is allowed in Skill, Registry, Learning Log, BCA tests, project code, Scene, data, assets, or Sheets.

## 9. Adversarial review

Attack and classify:

- PromptRecipe copied instead of adapted.
- Similar-image and similar-prompt evidence conflated.
- Prediction written as guarantee.
- Named-artist or identifiable-IP imitation.
- Project-specific values leaked into Base.
- Actual generation/runtime/human validation overclaimed.
- Duplicate Skill/mode/trigger introduced.
- Existing art-prompt behavior removed.
- PR #62 changes overwritten.
- Design/plan still describe the reverted direct-Skill-edit approach.

## 10. Completion and publication state

- Keep PR #63 as Draft until final verification and user integration decision.
- Do not merge automatically.
- Local tests: `NOT_RUN` because GitHub DNS is unavailable in the local execution environment.
- Actual image generation: `NOT_RUN`.
- Project-specific application, runtime review, and human visual validation: `NOT_RUN`.
- Base-to-project propagation occurs only after Base merge and a separate project audit/approval change.
