# Base v9.4 AI Operations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base v9.4에 모델·추론·Prompt 비용 운영 Skill과 판단 중심 지시·Context 큐레이션·게임 UI 모션 계약을 독립 책임으로 통합하고, 검증된 릴리스 후보를 만든다.

**Architecture:** BCP-2026-003은 신규 전문 Skill 하나로 구현하고, BCP-2026-004는 기존 intake·Skill 간소화·UI Skill의 mode/reference를 확장한다. 두 기능군은 같은 v9.4 후보 PR을 사용하되 Registry entry, 문서, 테스트와 적대적 검토를 분리하며 `base-v9.4.lock.json`이 현재 Registry raw bytes를 소유한다.

**Tech Stack:** Markdown, JSON/JSON Schema, Python 3.12 `unittest`, GitHub Actions, Base Skill Registry, Godot UI 계약.

## Global Constraints

- Base v9.3 release·evidence·pin 이력을 수정하지 않는다.
- BCP-2026-003과 BCP-2026-004의 입력·출력·검증 책임을 합치지 않는다.
- BCP-2026-004를 위한 새 활성 Skill이나 외부 `ui-skills` 의존성을 추가하지 않는다.
- 모델명·가격·cache 조건·context limit은 확인일이 없는 영구 상수로 고정하지 않는다.
- 보안·권한·데이터 무결성·비가역 변경·저장 호환성·법적 경계는 `HARD_CONSTRAINT`다.
- 예시는 삭제하지 않고 Fixture·Golden Set으로 보존한다.
- Base에서 provider billing·Godot 런타임·사람 이해 검증을 실행한 것으로 주장하지 않는다.
- 프로젝트 저장소·Google Sheets는 Base 후보 PR에서 수정하지 않는다.

---

### Task 1: RED 계약 테스트와 v9.4 후보 경계

**Files:**
- Create: `tests/test_base_v9_4_ai_operations_contract.py`
- Create: `base-v9.4.lock.json`
- Create: `schemas/base-v9-4-candidate-lock-v1.schema.json`
- Create: `schemas/base-v9-4-release-evidence-v1.schema.json`
- Create: `docs/operations/BASE_V9_4_RELEASE_CONTRACT.md`
- Modify: `tools/check_base_v9_integrity.py`

**Interfaces:**
- Consumes: released v9.3 lock and integrity patterns.
- Produces: `v94_release_lock_errors(repository, candidate_lock, trusted_history_commit)` and a candidate lock with null release pins.

- [ ] **Step 1: Write failing contract tests**

Create tests that require:

```python
REQUIRED_SKILL_ID = "optimizing-ai-model-and-prompt-costs"
REQUIRED_METHOD = ROOT / "docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md"
REQUIRED_MOTION = ROOT / "skills/auditing-and-refining-ui-art/references/ui-motion-and-interaction-principles.md"
```

Test cases:

```python
def test_v94_candidate_has_null_pins_and_current_registry_hash(): ...
def test_model_cost_skill_has_five_modes_and_model_recommendation_contract(): ...
def test_instruction_method_preserves_hard_constraints_and_examples_as_fixtures(): ...
def test_context_curation_requires_counterevidence_and_refresh_triggers(): ...
def test_ui_motion_contract_covers_interruption_repetition_and_reduced_motion(): ...
def test_required_consumers_link_to_new_contracts(): ...
def test_bcp_003_and_004_are_approved_and_linked_to_this_implementation(): ...
def test_v94_does_not_rewrite_v93_released_identity(): ...
```

- [ ] **Step 2: Run GitHub Actions and verify RED**

Expected failures:

```text
missing optimizing-ai-model-and-prompt-costs
missing AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md
missing ui-motion-and-interaction-principles.md
missing/invalid Base v9.4 candidate lock integration
BCP proposals not transitioned to APPROVED_FOR_IMPLEMENTATION
```

Do not fix tests to match missing implementation.

- [ ] **Step 3: Add minimal v9.4 candidate schema and lock**

Candidate lock fields:

```json
{
  "schema_version": 1,
  "artifact_role": "BASE_V9_4_RELEASE_CANDIDATE_LOCK",
  "release_line": "v9.4.0",
  "release_state": "RELEASE_CANDIDATE",
  "repository": "alsdmlals4-eng/Base",
  "github_issue": 113,
  "linked_issue": 115,
  "candidate_release_commit": null,
  "candidate_release_evidence_commit": null,
  "candidate_registry": {
    "path": "skills/SKILL_REGISTRY.json",
    "sha256": "generated after Registry update",
    "hash_definition": "RAW_FILE_BYTES_SHA256"
  }
}
```

- [ ] **Step 4: Extend integrity validation**

Add v9.4 constants and functions parallel to v9.3 while preserving v9.3 logic. Candidate state requires null pins and exact HEAD Registry hash. Released state requires payload/evidence ancestry and trusted-history evidence.

- [ ] **Step 5: Commit RED boundary**

Commit message:

```text
test: define Base v9.4 AI operations contract
```

### Task 2: 모델·추론·Prompt 비용 Skill

**Files:**
- Create: `skills/optimizing-ai-model-and-prompt-costs/SKILL.md`
- Create: `skills/optimizing-ai-model-and-prompt-costs/references/model-stack-routing.md`
- Create: `skills/optimizing-ai-model-and-prompt-costs/references/prompt-caching.md`
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `docs/generated/BASE_ACTIVE_SKILLS.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`

**Interfaces:**
- Produces Skill modes: `route-model-and-effort`, `design-cacheable-prefix`, `estimate-cost`, `measure-actual-usage`, `recalibrate`.
- Output: model recommendation YAML contract from the design spec.

- [ ] **Step 1: Implement minimal Skill body**

The body must contain purpose, positive/negative use conditions, authority boundary, five modes, required inputs, process, output, validation and failure conditions. It must state that it cannot change the active ChatGPT model itself.

- [ ] **Step 2: Add model-stack routing reference**

Define `SIMPLE_BULK / ROUTINE_BALANCED / HIGH_RISK_REASONING`, hidden-risk escalation, quality-first total cost and checkpoint behavior. Luna/Terra/Sol are logical tiers or user-facing aliases, not proof of provider availability.

- [ ] **Step 3: Add prompt-caching reference**

Define stable prefix, dynamic suffix, sensitive-data exclusions, provider profile, stale-value recheck and net-cost equation including retries/rework.

- [ ] **Step 4: Update Registry through deterministic migration**

Append one ACTIVE specialist entry with unique responsibility and triggers including:

```text
model-recommendation
model-effort-routing
luna-terra-sol
prompt-caching
cacheable-prefix
ai-cost-estimation
usage-measurement
provider-profile
```

Do not add dependencies that create cycles.

- [ ] **Step 5: Regenerate human view and learning record**

Active count increases by one. Registry SHA in generated view must match raw bytes.

- [ ] **Step 6: Run focused tests**

Expected: model-cost tests pass; BCP-2026-004 tests remain RED.

- [ ] **Step 7: Commit**

```text
feat: add AI model and prompt cost optimization skill
```

### Task 3: 지시 권위·Interface-first·Context 큐레이션 Method

**Files:**
- Create: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/simplifying-skill-bodies/SKILL.md`
- Modify: `skills/simplifying-skill-bodies/references/progressive-disclosure-rules.md`
- Modify: `docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- Modify: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- Modify: `skills/SKILL_REGISTRY.json`

**Interfaces:**
- Produces authority and context-curation YAML contracts.
- Consumed by intake, Skill simplification and AI work packages.

- [ ] **Step 1: Write the Method**

Required sections:

```text
목적·권위
HARD_CONSTRAINT / RECOMMENDED_DEFAULT / JUDGMENT_SPACE
Interface-first Prompt
Example as Fixture/Golden Set
Context curation
Representation by data type
Artifact-first delivery and claim limits
Memory vs canonical source
Refresh and stop conditions
Validation matrix
Failure conditions
```

- [ ] **Step 2: Extend intake Skill**

Add a conditional reference path and require authority classification before adding strong instructions. Context curation happens after the current decision question and canonical inputs are known.

- [ ] **Step 3: Extend simplification Skill**

Classification must distinguish:

```text
Always hard constraint
Conditional default
Judgment space
Fixture/example
Historical
Duplicate
```

Removing examples without preserving their tested behavior is a regression.

- [ ] **Step 4: Connect Guide and planning policy**

The AI Guide must use the Method for Prompt/Context design. The planning policy must require counterevidence, exclusion rationale, and refresh triggers where curation changes evidence inputs.

- [ ] **Step 5: Update existing Registry entries**

Add focused trigger/review metadata without changing their responsibility IDs.

- [ ] **Step 6: Run focused tests**

Expected: authority, interface and context tests pass.

- [ ] **Step 7: Commit**

```text
feat: add judgment-centered AI instruction and context method
```

### Task 4: 게임 UI 모션·상호작용 계약

**Files:**
- Create: `skills/auditing-and-refining-ui-art/references/ui-motion-and-interaction-principles.md`
- Modify: `skills/auditing-and-refining-ui-art/SKILL.md`
- Modify: `skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md`
- Modify: `templates/planning/GAME_UX_UI_SYSTEM.md`
- Modify: `templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md`
- Modify: `skills/SKILL_REGISTRY.json`

**Interfaces:**
- Consumes screen question, state source, input paths, feedback budget and polish readiness.
- Produces motion purpose, state transition, interruption/repetition fixtures, fallbacks and validation evidence.

- [ ] **Step 1: Add UI motion reference**

Required sections:

```text
목적·비목표
상태 변화와 staging
anticipation 판정
motion duration/easing as project values
spatial continuity and follow-through
input accepted / processing / result separation
interrupt / instant complete / rapid repeat / modal reentry
Reduced Motion / mute / haptic-off
performance and localization
Godot AnimationPlayer/Tween authority boundary
validation fixtures and failure conditions
```

- [ ] **Step 2: Route from UI Skill and Method**

The reference is loaded only for motion/interaction work. It does not replace information architecture or polishing readiness.

- [ ] **Step 3: Extend Template and Checklist**

Add fields for motion purpose, interruption, repetition, fallbacks, domain authority and before/after evidence. Do not add fixed duration constants.

- [ ] **Step 4: Update Registry metadata**

Add focused triggers such as `ui-motion-design`, `animation-interruption`, `reduced-motion`, while preserving the UI Skill responsibility.

- [ ] **Step 5: Run focused tests**

Expected: UI motion tests pass.

- [ ] **Step 6: Commit**

```text
feat: add game UI motion and interaction contract
```

### Task 5: 발견성·승인 상태·릴리스 후보 통합

**Files:**
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/BASE_RULES_VERSION.md`
- Modify: `templates/project-operations/AI_WORKFLOW.md`
- Modify: `docs/CHANGELOG.md`
- Modify: `[수정제안서]/PROPOSAL_REGISTRY.json`
- Modify: both BCP `PROPOSAL.md`
- Modify: `base-v9.4.lock.json`
- Modify: `docs/generated/BASE_ACTIVE_SKILLS.md`

**Interfaces:**
- Consumes completed Skill/Method/Reference and current Registry bytes.
- Produces discoverable v9.4 candidate identity and approved proposal linkage.

- [ ] **Step 1: Update proposal lifecycle in implementation PR**

Set BCP-2026-003 and BCP-2026-004 to `APPROVED_FOR_IMPLEMENTATION`, populate approval refs #113/#115 and the implementation PR number when known.

- [ ] **Step 2: Update Documentation Map and AI Workflow**

A new worker must find the model-cost Skill, instruction/context Method and UI motion reference in one step.

- [ ] **Step 3: Update Base version boundary**

Describe v9.4 as a compatible candidate; do not rewrite the immutable v9.0 or released v9.3 records.

- [ ] **Step 4: Recompute raw Registry hash**

Write the exact SHA-256 to `base-v9.4.lock.json` and generated active Skill view.

- [ ] **Step 5: Run focused contract tests**

Expected: all v9.4 focused tests pass.

- [ ] **Step 6: Commit**

```text
release: establish Base v9.4 AI operations candidate
```

### Task 6: 적대적 검토·전체 회귀·후속 릴리스

**Files:**
- Modify only validated findings within approved scope.
- Create later in separate PR: `docs/operations/BASE_V9_4_RELEASE_EVIDENCE.json`

**Interfaces:**
- Consumes exact PR HEAD, all tests, Registry, BCPs and release lock.
- Produces candidate verdict, then trusted evidence and final pins.

- [ ] **Step 1: Run repository-wide adversarial review**

Attack responsibility overlap, stale provider constants, hidden safety relaxation, example deletion, counterevidence removal, Artifact overclaim, UI domain-authority bugs, untouched consumers and v9.3 history changes.

- [ ] **Step 2: Validate critiques**

Classify each as `MUST_FIX / SHOULD_FIX / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED` and fix only validated approved findings.

- [ ] **Step 3: Run required GitHub Actions**

Required:

```text
proposal validation
reference freshness
skill coverage/package integrity
Base v9 integrity
focused v9.4 tests
full Python regression
publication/generation validation
git diff --check
ci-gate
```

- [ ] **Step 4: Record limitations**

```text
provider billing/cache hit: NOT_RUN
Godot runtime UI motion: NOT_RUN
human UI comprehension: NOT_RUN
Windows smoke: report actual status
```

- [ ] **Step 5: Merge candidate only with exact HEAD evidence**

Unresolved thread 0, P0/P1 0, required checks passed, no open user decision.

- [ ] **Step 6: Create trusted-main evidence PR**

Evidence must point to the merged candidate payload and exact Registry identity. It must not set final pins itself.

- [ ] **Step 7: Create pin-finalization PR**

Set `BASE_RELEASED`, payload and evidence SHAs after both exist in trusted main history.

- [ ] **Step 8: Start six project adoption audits**

Each project gets an independent Issue/Branch/PR, project-local Decision and validation. Base and project-specific content remain separated.

## Self-review

- Spec coverage: both BCPs, responsibility boundaries, release sequence, project follow-up and limitations are assigned to tasks.
- Placeholder scan: the candidate Registry hash is intentionally produced in Task 5 from actual bytes; no implementation behavior is left undefined.
- Type consistency: mode names, file paths and status values match the approved design.
