# PromptRecipe Reference Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate PromptRecipe and similar image/prompt examples into the existing Base art-prompt workflow so agents can forecast likely image results and explain the reasoning used to derive prompts before generation.

**Architecture:** Keep `designing-art-prompts-and-technique-cards` as the single execution owner. Add a source audit and a reusable prompt-recipe card, connect them from the existing Skill, and validate discovery, prediction, reasoning, rights, and non-copying contracts through one focused unittest added to the existing evidence-knowledge workflow.

**Tech Stack:** Markdown, YAML examples, Python `unittest`, GitHub Actions, GitHub Contents API.

## Global Constraints

- Do not add a new shared Skill ID.
- Do not copy PromptRecipe prompt bodies, protected images, identifiable characters, logos, signatures, or named-artist style instructions into Base.
- Treat similar images and similar prompts as reference evidence, not project authority or guaranteed reproduction instructions.
- Pre-generation output forecasts are hypotheses with `LOW / MEDIUM / HIGH` confidence, not promises.
- Every important prompt phrase must connect a desired observable result to a reasoning basis, expected model response, and risk/correction.
- Actual project prompts, generated images, approved assets, model/account settings, and runtime evidence remain project-specific.
- Do not modify Godot code, scenes, resources, game data, project Sheets, or approved project assets.
- Preserve every existing mode, lifecycle state, QA rule, Template link, and Pinterest/FACS/poster contract in `designing-art-prompts-and-technique-cards`.
- PR #62 modifies other shared routing consumers. Before each shared-file write, re-fetch the current branch file and preserve unrelated content; do not overwrite PR #62 work if it reaches `main` during execution.
- Local GitHub DNS is unavailable. Use Draft PR Actions for mandatory RED and GREEN evidence; local tests remain `NOT_RUN`.

---

### Task 1: Add the failing PromptRecipe contract test and Draft PR

**Files:**
- Create: `tests/test_prompt_recipe_reference_contract.py`
- Modify: `.github/workflows/validate-evidence-knowledge.yml`
- Modify: `tests/test_evidence_knowledge_workflow_contract.py`

**Interfaces:**
- Consumes: the approved design at `docs/superpowers/specs/2026-07-29-prompt-recipe-reference-integration-design.md`.
- Produces: a failing contract that names every required Source Audit, Template, Skill link, forecast field, reasoning field, rights boundary, and workflow consumer.

- [ ] **Step 1: Create the focused failing unittest**

Create `tests/test_prompt_recipe_reference_contract.py` with these exact behaviors:

```python
from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_AUDIT = ROOT / "docs" / "knowledge" / "research" / "PROMPT_RECIPE_SOURCE_AUDIT.md"
RECIPE_CARD = ROOT / "templates" / "research" / "AI_IMAGE_PROMPT_RECIPE_CARD.md"
SKILL = ROOT / "skills" / "designing-art-prompts-and-technique-cards" / "SKILL.md"
DESIGN = ROOT / "docs" / "superpowers" / "specs" / "2026-07-29-prompt-recipe-reference-integration-design.md"


class PromptRecipeReferenceContractTests(unittest.TestCase):
    def test_required_files_exist(self) -> None:
        missing = [
            path.relative_to(ROOT).as_posix()
            for path in (SOURCE_AUDIT, RECIPE_CARD, SKILL, DESIGN)
            if not path.is_file()
        ]
        self.assertEqual([], missing)

    def test_source_audit_preserves_reference_and_rights_boundaries(self) -> None:
        text = SOURCE_AUDIT.read_text(encoding="utf-8")
        for required in (
            "https://promptrecipe.pages.dev/",
            "REFERENCE_ONLY",
            "UNVERIFIED",
            "원문 전문을 복제하지 않는다",
            "유사 이미지",
            "유사 프롬프트",
            "특정 작가",
            "재검증 조건",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_recipe_card_requires_forecast_reasoning_and_result_comparison(self) -> None:
        text = RECIPE_CARD.read_text(encoding="utf-8")
        for required in (
            "similar_image_references",
            "similar_prompt_references",
            "pre_generation_forecast",
            "prediction_confidence",
            "confidence_basis",
            "unverified_assumptions",
            "desired_observation_to_prompt",
            "reasoning_basis",
            "expected_model_response",
            "risk_and_correction",
            "actual_result_review",
            "PREDICTION_NOT_TESTED",
            "MODEL_OR_CONTEXT_CHANGED_RETEST_REQUIRED",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_skill_routes_reference_assisted_forecast_before_generation(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        for required in (
            "PROMPT_RECIPE_SOURCE_AUDIT.md",
            "AI_IMAGE_PROMPT_RECIPE_CARD.md",
            "생성 전 결과 예측",
            "프롬프트 추론 근거",
            "유사 이미지",
            "유사 프롬프트",
            "예측과 실제 결과",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_unrun_generation_cannot_be_verified(self) -> None:
        source = SOURCE_AUDIT.read_text(encoding="utf-8")
        card = RECIPE_CARD.read_text(encoding="utf-8")
        combined = source + "\n" + card
        self.assertIn("실제 생성 없이", combined)
        self.assertIn("VERIFIED", combined)
        self.assertIn("가설", combined)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Add the test and relevant paths to the dedicated workflow**

Update `.github/workflows/validate-evidence-knowledge.yml` so pull-request path filters include:

```yaml
      - "docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md"
      - "docs/superpowers/specs/*prompt-recipe-reference-integration*.md"
      - "docs/superpowers/plans/*prompt-recipe-reference-integration*.md"
      - "skills/designing-art-prompts-and-technique-cards/SKILL.md"
      - "tests/test_prompt_recipe_reference_contract.py"
```

Add `tests/test_prompt_recipe_reference_contract.py` to `py_compile`, `unittest`, and uploaded evidence paths.

- [ ] **Step 3: Extend the workflow self-contract**

Update `tests/test_evidence_knowledge_workflow_contract.py` to require:

```python
"tests/test_prompt_recipe_reference_contract.py",
"docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md",
"skills/designing-art-prompts-and-technique-cards/SKILL.md",
```

- [ ] **Step 4: Commit the RED contract**

Commit message:

```text
test: define PromptRecipe reference contract
```

- [ ] **Step 5: Open a Draft PR**

PR title:

```text
PromptRecipe 이미지·프롬프트 예측 레퍼런스 통합
```

The PR body must state that RED is expected because the Source Audit and Recipe Card do not exist and the Skill is not connected yet.

- [ ] **Step 6: Verify RED in GitHub Actions**

Inspect the PR-head workflow run for the RED commit.

Expected result:

```text
Validate Evidence-Based Game Development Knowledge: FAILURE
```

The focused failure must name missing `PROMPT_RECIPE_SOURCE_AUDIT.md`, missing `AI_IMAGE_PROMPT_RECIPE_CARD.md`, or missing Skill contract phrases. A YAML parse failure or unrelated existing failure is not valid RED evidence.

---

### Task 2: Implement the Source Audit and Prompt Recipe Card

**Files:**
- Create: `docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md`
- Create: `templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md`

**Interfaces:**
- Consumes: design principles and the failing test from Task 1.
- Produces: the source/rights contract and project-facing record schema consumed by the Skill in Task 3.

- [ ] **Step 1: Create the Source Audit**

The Source Audit must contain:

```text
source_status: PARTIALLY_VERIFIED
source_decision: REFERENCE_ONLY
checked_at: 2026-07-29
```

Required sections:

```text
1. 목적
2. 확인된 범위
3. 미검증 범위
4. 유사 이미지 참고 원칙
5. 유사 프롬프트 참고 원칙
6. 생성 전 결과 예측의 증거 한계
7. 원하는 결과에서 프롬프트를 역추론하는 방법
8. 권리·복제·유사성 경계
9. Base와 프로젝트 책임 경계
10. 재검증 조건
```

The document must explicitly prohibit copying full prompt bodies and must classify observed homepage structure separately from unverified individual pages, model versions, rights, and reproducibility.

- [ ] **Step 2: Create the reusable Recipe Card**

The card must provide editable Markdown/YAML fields for:

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
actual_result_review:
  generation_status: NOT_RUN | RUN
  prediction_status: PREDICTION_NOT_TESTED | PREDICTION_PARTIALLY_MATCHED | PREDICTION_MATCHED | PREDICTION_FAILED | MODEL_OR_CONTEXT_CHANGED_RETEST_REQUIRED
```

Add checklist gates for project identity protection, target-size readability, anatomy/text/logo/perspective risks, production feasibility, rights review, and actual result comparison.

- [ ] **Step 3: Commit the knowledge artifacts**

Commit message:

```text
docs: add PromptRecipe source audit and recipe card
```

- [ ] **Step 4: Verify partial GREEN**

Expected focused results after this commit:

- file-existence test passes;
- Source Audit and Recipe Card field tests pass;
- Skill routing test still fails because the existing Skill has not been connected.

---

### Task 3: Connect the existing art-prompt Skill

**Files:**
- Modify: `skills/designing-art-prompts-and-technique-cards/SKILL.md`

**Interfaces:**
- Consumes: Source Audit and Recipe Card from Task 2.
- Produces: an explicit pre-generation `similar references → forecast → prompt derivation → generation → comparison` workflow without adding a new Skill or mode.

- [ ] **Step 1: Extend required inputs without removing existing inputs**

Add:

```text
- 유사 이미지·유사 프롬프트 사례와 각 출처·확인일·권리 상태.
- 원하는 결과를 관찰 가능한 문장으로 표현한 목표와 허용 오차.
- 생성 전 예상 결과·실패 가능성·확신도와 추론 근거.
```

- [ ] **Step 2: Insert the reference-assisted forecast steps before prompt composition**

The process order must become:

```text
사용 목적·화면·프로젝트 정체성 확인
→ 유사 이미지와 유사 프롬프트를 별도 조사
→ ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY 분류
→ 생성 전 결과 예측과 확신도 기록
→ 원하는 관찰 결과에서 프롬프트 표현과 추론 근거 역산
→ 기존 프롬프트 모듈 작성
→ 생성
→ 예측과 실제 결과 비교
→ 최소 수정 모듈 결정
→ visual-qa-and-approval
```

Reference the exact paths:

```text
docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md
templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md
```

- [ ] **Step 3: Extend Technique Card and Output contracts**

Add fields for:

```text
유사 이미지 관찰
유사 프롬프트 구조
생성 전 결과 예측
프롬프트 추론 근거
예측 확신도와 미검증 가정
예측과 실제 결과 비교
수정 프롬프트의 변경 모듈
```

- [ ] **Step 4: Extend failure and validation contracts**

Failure conditions must include:

```text
유사 사례를 복제 대상으로 사용함
예측을 보장으로 표현함
근거 없이 형용사를 나열함
실제 생성 없이 VERIFIED로 승격함
```

Validation scenarios must include one pre-generation forecast and one forecast-versus-result comparison scenario.

- [ ] **Step 5: Add the Recipe Card to Templates**

Append:

```text
- `templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md`
```

- [ ] **Step 6: Commit the Skill integration**

Commit message:

```text
feat: add reference-assisted image prompt forecasting
```

- [ ] **Step 7: Verify focused GREEN in Actions**

Expected:

```text
python -m unittest tests/test_prompt_recipe_reference_contract.py -v
PASS
```

The full Evidence Knowledge workflow may still fail only if the workflow self-contract or another coupled consumer needs a verified correction.

---

### Task 4: Final regression, conflict audit, and PR reporting

**Files:**
- Review: all branch changes.
- Modify only when a verified regression or shared-file conflict is found.

**Interfaces:**
- Consumes: all prior tasks and the current open-PR state.
- Produces: a reviewable Draft PR with actual RED/GREEN evidence and no unverified completion claim.

- [ ] **Step 1: Re-check `main` and PR #62**

Confirm whether `main` moved from `0fd95f4513343e77fd664af2763a01b02f52545b` and whether PR #62 merged or changed shared files.

If `main` moved, compare the branch to new `main`. Preserve newer unrelated changes. Do not force-update or rewrite PR #62.

- [ ] **Step 2: Run all PR-head Actions checks**

Required evidence:

```text
Validate Evidence-Based Game Development Knowledge
Validate Game Project Operating System or stable ci-gate when triggered
```

Record success, failure, cancellation, and skipped jobs separately.

- [ ] **Step 3: Review the diff scope**

Expected changed paths are limited to:

```text
docs/superpowers/specs/2026-07-29-prompt-recipe-reference-integration-design.md
docs/superpowers/plans/2026-07-29-prompt-recipe-reference-integration.md
docs/knowledge/research/PROMPT_RECIPE_SOURCE_AUDIT.md
templates/research/AI_IMAGE_PROMPT_RECIPE_CARD.md
skills/designing-art-prompts-and-technique-cards/SKILL.md
tests/test_prompt_recipe_reference_contract.py
tests/test_evidence_knowledge_workflow_contract.py
.github/workflows/validate-evidence-knowledge.yml
```

No Registry change is required because current triggers `image-prompt` and `technique-card` already route this work. A Registry change is allowed only if the focused test proves actual routing failure.

- [ ] **Step 4: Perform adversarial review**

Attack:

```text
PromptRecipe copied rather than adapted
similar image and similar prompt evidence conflated
prediction written as guarantee
named-artist or identifiable-IP imitation
project-specific prompt or asset values leaking into Base
actual generation and runtime validation overclaimed
new duplicate Skill or mode added
existing Pinterest/FACS/poster/QA behavior removed
PR #62 changes overwritten
```

Classify findings as `MUST_FIX`, `SHOULD_FIX`, `REJECTED_CRITIQUE`, `WAIVED`, or `USER_DECISION_REQUIRED`.

- [ ] **Step 5: Update the Draft PR body**

Include:

```text
approved purpose
Base structure decision
similar image and similar prompt usage
pre-generation forecast contract
prompt reasoning contract
rights/non-copying boundary
RED run evidence
GREEN run evidence
changed files
open PR #62 conflict result
local tests NOT_RUN because GitHub DNS unavailable
actual image generation NOT_RUN
project propagation NOT_RUN
```

Do not mark the PR ready or merge without a final review decision.
