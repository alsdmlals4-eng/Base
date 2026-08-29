# Candidate-First Visual · Autonomous Quality Loop Implementation Plan

> 설계 원본: `docs/superpowers/specs/2026-08-29-candidate-first-visual-autonomous-quality-loop-design.md`
> 승인 제안: `[수정제안서]/BCP-2026-049-candidate-first-visual-and-autonomous-quality-loop/PROPOSAL.md`
> 기준 main: `f80ae737619d300cedf906b544961066ed373312`

## 완료 목표

Base의 이미지 생성·검수 owner, 프로젝트 이미지 routing, 맞춤형 지침 템플릿과 Work v4.9를 다음 계약으로 정렬한다.

```text
CANDIDATE_FIRST_VISUAL_PRODUCTION
IMPLEMENTATION_FEASIBILITY_BEFORE_COMMITMENT
LONG_TERM_QUALITY_OVER_LOCAL_SPEED
MINIMIZE_USER_INTERVENTION_WITH_SAFE_FINAL_CONTROL
ACTUAL_POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
INCIDENT_SOLUTION_LESSON_AUTOMATION_LOOP
```

## 보호 범위

- 실제 이미지 binary·runtime asset·Godot Scene을 변경하지 않는다.
- Blueprint의 exact revision 사용자 최종 승인과 Codex 구현 Gate를 우회하지 않는다.
- open PR #660·#713·#748과 기타 workstream의 소유 파일을 수정하지 않는다.
- `PROPOSAL_REGISTRY.json`을 수정하지 않는다.
- Notion·Sheets history는 삭제하지 않고 active completion authority만 repository-first로 교정한다.
- 새 paid dependency·provider·runner를 추가하지 않는다.

## Task 1 — RED 계약

파일:

- 새 `tests/test_candidate_first_autonomous_quality_contract.py`

절차:

1. 새 공용 token과 stale custom-instruction 문구 제거를 assertion한다.
2. test만 있는 branch를 PR로 열어 canonical GitHub Actions에서 실패를 확인한다.
3. failing job·assertion·exact head SHA를 기록한다.

완료 증거:

```text
RED_EXACT_HEAD
CANONICAL_REMOTE_CI_FAILURE
FAILURE_CAUSED_BY_MISSING_NEW_CONTRACT
```

## Task 2 — 이미지 owner 교정

파일:

- `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`

구현:

1. assistant-discovered visual need의 active route를 candidate-first로 바꾼다.
2. project identity·approved anchor·actual/planned consumer·reuse·bounded brief를 precondition으로 둔다.
3. 한 bounded candidate와 objective correction 후 사용자 final lock을 받는다.
4. generation/lock/canon/implementation/runtime 상태를 분리한다.
5. old two-turn token은 active contract가 아닌 `RETIRED_COMPATIBILITY_ALIAS`로만 남긴다.
6. Notion/Sheet active current authority 표현을 repository-first/migration-only로 교정한다.
7. image-model-only와 host precedence를 유지한다.

## Task 3 — 맞춤형 지침·Work adapter 교정

파일:

- `templates/custom-instructions.gpt.md`
- `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md`

구현:

1. 맞춤형 지침을 repository-first bootstrap으로 전면 교체한다.
2. Notion·Sheets는 unique migration-only로 제한한다.
3. 후보 선제작·final lock·상태 분리를 반영한다.
4. current official/primary research·현업 사례·actual implementation feasibility를 명시한다.
5. 장기 품질·minimum sufficient complexity·anti-overengineering을 명시한다.
6. 사용자 개입 최소화와 고위험/제품 의미/final lock 경계를 분리한다.
7. 작업 후 실제 최소 5회 adversarial correction과 evidence requirement를 명시한다.
8. problem→root cause→regression prevention→Base learning loop를 명시한다.
9. Blueprint final approval 전 implementation 금지를 유지한다.

## Task 4 — GREEN과 회귀 검사

원격 exact-head에서 최소 다음을 확인한다.

```text
new focused contract
existing image-model-only contract
existing visual-anchor pipeline contract
existing Master GDD/Blueprint contract
existing Work v4.9/base operating contracts
canonical reference freshness
full repository CI selected by canonical workflow
```

실행하지 못한 로컬 검증은 PASS로 쓰지 않는다. canonical remote CI가 current head를 소유하면 local fallback으로 덮지 않는다.

## Task 5 — 최소 5회 전체 적대적 검토와 실제 교정

파일:

- 새 `docs/reviews/2026-08-29-candidate-first-autonomous-quality-adversarial-review.md`

각 loop:

```yaml
loop_index:
input_head:
evidence_delta: []
full_scope_findings: []
validated_findings: []
changes_applied: []
verification: []
better_alternative_result:
long_term_fit:
unresolved: []
output_head:
clean_exit_candidate:
```

전체 lens:

- 사용자 승인 의도와 authority.
- 후보 선제작과 final lock 경계.
- Blueprint 구현 권한 비침범.
- current consumer·rights·provenance.
- repository-first와 history/migration 보존.
- current primary research와 actual feasibility.
- 사용자 개입 최소화·unsafe fallback.
- long-term value·anti-overengineering·cost.
- stale reference·untouched test/template.
- evidence ceiling·rollback·same-goal PR.

유효 finding은 같은 PR에서 최소 수정하고 exact-head 검증 뒤 다음 whole loop를 수행한다. 다섯 회가 끝나도 finding이 남으면 계속한다.

## Task 6 — PR·병합·post-merge readback

1. PR diff와 changed paths를 baseline과 대조한다.
2. current head의 canonical CI, reviews, open thread, same-goal PR을 확인한다.
3. 승인 범위와 check가 닫히면 squash merge한다.
4. 새 `main`, merged file, test, CI와 proposal status를 readback한다.
5. post-merge whole-state review와 remaining-work recalculation을 수행한다.

## 프로젝트 교정 분리

Base implementation과 프로젝트 전용 드리프트는 독립 PR로 분리한다.

- `MylittleBoat/AGENTS.md`
- `ninja-survival-godot/AGENTS.md`
- `Coc-Fiction/AGENTS.md`
- `urban-legend/docs/IMAGE_ASSET_WORKFLOW.md`

십보강호·Blacksmith·GRIMOIRE·Omenward·Switchy Express·Tetris는 이미 같은 상위 계약이 있어 exact readback으로 닫고 불필요한 churn을 만들지 않는다.

## 완료 판정

```text
focused RED observed
→ owner/template correction
→ focused GREEN
→ existing contracts GREEN
→ canonical freshness closed
→ minimum 5 actual full-scope loops
→ validated findings corrected
→ exact-head CI success
→ squash merge
→ post-merge main readback
→ remaining actionable work recalculated
```

문서 PASS는 runtime·human PASS가 아니다. 이번 Base 변경은 운영 계약·문서·test 범위이며 실제 게임 runtime/human evidence는 `NOT_APPLICABLE` 또는 `NOT_RUN`으로 분리한다.
