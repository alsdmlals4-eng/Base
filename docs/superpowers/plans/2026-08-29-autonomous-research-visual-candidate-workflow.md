# Autonomous research and candidate-first visual policy implementation plan

**Date:** 2026-08-29  
**Approved design:** `docs/superpowers/specs/2026-08-29-autonomous-research-visual-candidate-workflow-design.md`

## Task 1. Base current-state and conflict audit

- Read Base latest completed `main`, `START_HERE.md`, `AGENTS.md`, long-horizon policy, image policies, custom-instructions template, related tests and open PR paths.
- Read active project `AGENTS.md` files and classify each repository as aligned, conflicting, or not applicable.
- Preserve all pre-existing open/draft PRs as read-only.

Acceptance:

- Audit names every checked project and the exact conflicting rule.
- No broad project churn when Base adoption is sufficient.

## Task 2. Add autonomous research/implementation/learning owner

Create:

- `docs/AUTONOMOUS_RESEARCH_IMPLEMENTATION_AND_LEARNING_POLICY.md`

The owner must define:

- current official/primary research and industry comparison
- at least three viable alternatives when material
- actual implementation feasibility packet
- long-term total cost over local speed
- minimum complexity and no speculative overengineering
- minimized user intervention
- durable project learning and Base promotion candidate loop

Acceptance:

- Contract test asserts all machine tokens and required ordering.

## Task 3. Replace image candidate approval semantics

Update:

- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`

Required behavior:

```text
consumer + project canon + existing visual readback
→ bounded candidate may be generated before user lock
→ result review
→ user LOCK / REVISE / REJECT / REFERENCE_ONLY
→ lock required for canon/runtime promotion
```

Preserve:

- image-model-only creation
- actual/planned consumer gate
- text-native production information
- rights/provenance
- no unbounded image chain
- Blueprint final approval before new implementation

## Task 4. Replace GPT custom-instructions bootstrap

Update:

- `templates/custom-instructions.gpt.md`

Remove active Notion-first and explicit-image-request-only behavior. Add repository-first, research-to-feasibility, long-term quality, candidate-first image production, automation/learning and evidence separation.

Acceptance:

- Copy blocks remain within current custom-instruction size budget.
- Variable project state is not embedded.

## Task 5. Update regression tests

Update/add:

- `tests/test_project_image_request_visual_anchor_pipeline.py`
- `tests/test_autonomous_research_implementation_learning_policy.py`

Preserve old search tokens only as explicitly inactive legacy compatibility markers so unrelated existing tests do not silently restore the old behavior.

## Task 6. Correct project-local conflicts

Only change projects with an explicit current conflict after fresh-read.

Expected:

- `ninja-survival-godot`: replace explicit-request-only image rule with candidate-first + post-lock promotion.
- `Coc-Fiction`: remove stale Notion completion requirement and adopt repository-only readback plus research/automation/learning language suitable for a narrative project.
- Other checked projects: no-change audit receipt when already aligned.

Each repository uses a new latest-main branch and PR. Existing PRs remain read-only.

## Task 7. Verification and merge gate

Base:

- exact branch diff/readback
- focused contract tests through CI
- full applicable repository checks
- conflict-marker and whitespace inspection
- five full adversarial review loops
- PR exact-head status/review/thread/ruleset check

Projects:

- exact destination readback
- repository-appropriate documentation/tests
- PR status and changed-file scope
- no runtime/human PASS claims for documentation-only changes

Merge only when current-task continuation authority and all applicable checks permit it. Otherwise leave a verified PR with the exact blocker.
