# Claim and Intent Verification Gate — Design

- Date: 2026-08-13
- Source main: `a96864a84ac2513e488f20cba304c252dea3045d`
- Proposal: `BCP-2026-027-claim-and-intent-verification-gate`
- Existing owner: `reviewing-and-validating-project-changes`
- Disposition: `ABSORB`

## Goal

AI·Agent·작업자의 설명, 검색 snippet, 파일 존재, 모델 자신감을 완료 Evidence로 과승격하지 않고 다음을 독립적으로 판정한다.

1. 중요한 사실·구현·검증·병합 주장이 authority와 actual evidence를 갖는가.
2. 승인된 WHAT/WHY·Acceptance·Protected Scope가 실제 구현 경로와 관찰 동작에 연결되는가.
3. 테스트와 병합이 exact HEAD와 post-merge main에서 실제로 확인됐는가.

## Current Base fit

새 ACTIVE Skill을 만들지 않는다. 기존 검증 owner는 이미 외부 산출물 검수, 계약 대조, static/runtime/regression, Evidence ceiling, exact-head 판정을 소유한다. 이번 변경은 그 Skill에 `claim-and-intent-verification` Mode와 전용 reference를 추가하고, 기존 Registry 항목의 trigger/use_when만 좁게 확장한다.

보호 대상:

- ACTIVE Skill ID 집합과 수 `30`
- Work Mode `PLAN / BUILD / REVIEW`
- 기존 Evidence E0–E6 의미
- BCP-008 Traceability, BCP-020 Player Experience Evidence owner
- release lock·pin·immutable artifacts
- 프로젝트별 수치·세계관·구현 경로

## Evidence model

### Material Claim Ledger

```yaml
claim_id:
claim_type: REPOSITORY_FACT | EXTERNAL_FACT | INFERENCE | IMPLEMENTATION | VERIFICATION | INTEGRATION
claim_text:
authority_source:
evidence_locator:
freshness:
counterevidence:
status: CLAIM_VERIFIED | CLAIM_CONTRADICTED | CLAIM_UNVERIFIED | NOT_APPLICABLE
```

모든 문장이 아니라 결정·수정·완료 상태를 바꾸는 material claim만 기록한다.

Authority order:

```text
latest user instruction / approved contract
→ exact-SHA repository and registered canon
→ tool/test/runtime result executed at that SHA
→ dated/versioned official primary external source
→ explicit inference
→ search snippet / producer report / model explanation as an unverified lead
```

### Intent Implementation Fidelity Matrix

```yaml
intent_id:
approved_intent_or_acceptance:
protected_and_excluded_scope:
implementation_paths:
observed_behavior:
verification_evidence:
evidence_ceiling:
drift_status: INTENT_CONFORMANT | MINOR_TECHNICAL_DRIFT | PLANNING_CONFLICT | IMPLEMENTATION_UNVERIFIED
```

- `INTENT_CONFORMANT`: 승인 결과·보호 동작과 관찰 결과가 일치한다.
- `MINOR_TECHNICAL_DRIFT`: HOW만 달라지고 WHAT/WHY·제품 의미는 동일하다.
- `PLANNING_CONFLICT`: 플레이어 경험·주요 UX·콘텐츠 의미·범위가 승인과 충돌한다.
- `IMPLEMENTATION_UNVERIFIED`: 필요한 diff·runtime·test·render·사람 Evidence가 없다.

### Completion Claim Gate

| Claim | Minimum evidence |
|---|---|
| implemented | actual diff, requirement-specific implementation paths, no out-of-scope mutation |
| tested | command, environment, result, exact HEAD, failure/skip count |
| intended behavior achieved | acceptance-by-acceptance observation at the required Evidence level |
| merged | merged PR state, merge SHA, post-merge main readback, required push checks |

필요 Evidence가 없으면 `BLOCKED_UNVERIFIED` 또는 `IMPLEMENTATION_UNVERIFIED`다.

## Workflow integration

```text
CONCURRENT_CHANGE_PREFLIGHT
→ approved intent / acceptance / protected scope
→ material claim ledger
→ authority, freshness, counterevidence
→ exact-ref readback, actual diff, consumer and implementation-path mapping
→ deterministic static/test/runtime evidence
→ Evidence ceiling
→ independent VERIFIER / CRITIC
→ exact-head verdict
→ merge-time current-main preflight
→ post-merge main readback
→ claim / intent / verification report
```

`CONCURRENT_CHANGE_PREFLIGHT`는 `synchronizing-local-and-github-state` owner를 재사용하며 이번 Skill이 중복 소유하지 않는다.

## Base regression case

PR #313 감사의 README hardcoded-27 finding은 검색·요약에서 저장소 사실로 과승격됐으나, `README.md@453f7908…`와 `README.md@190511e3…` exact-ref readback은 동일한 generated Skill Map 위임을 확인했다. PR #316은 이를 `INVALIDATED_FINDING`으로 교정한다.

필수 negative case:

```text
search result or producer summary exists
AND exact-ref file readback is absent
→ REPOSITORY_FACT = CLAIM_UNVERIFIED
→ canonical/document mutation is forbidden
```

#316 경로는 수정하지 않고 read-only regression evidence로만 사용한다.

## Routing

기존 Registry owner에 다음 metadata만 추가한다.

- tags: `completion-claim`, `claim-evidence`, `intent-conformance`, `hallucination-audit`
- use_when: AI/Agent가 구현·테스트·병합 완료를 주장하거나 승인 의도와 실제 diff/evidence의 일치를 판정할 때
- review trigger: unsupported, contradictory, stale claim; missing exact-head/post-merge readback

`SBE-038`은 `REVIEW` → `reviewing-and-validating-project-changes` → `claim-and-intent-verification`을 요구한다. Live model execution은 실제로 실행하지 않으면 계속 `NOT_RUN`이다.

## Scope

Implementation paths:

- `skills/reviewing-and-validating-project-changes/SKILL.md`
- `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`
- `skills/SKILL_REGISTRY.json`
- `docs/generated/BASE_ACTIVE_SKILLS.md`
- `templates/quality/PROJECT_CHANGE_VALIDATION.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/OPERATING_MODEL.md`
- `skills/SKILL_BEHAVIOR_EVALS.json`
- `skills/SKILL_LEARNING_LOG.md`
- `tests/test_claim_and_intent_verification_contract.py`
- this design and implementation plan
- BCP-027 proposal/Registry lifecycle fields

The dedicated test file is a minor technical substitution for appending the contract to a large unrelated lifecycle test. It preserves the approved WHAT/WHY and improves isolated failure diagnostics.

## Adversarial boundaries

- This Gate reduces unsupported claims; it does not promise zero hallucinations.
- Deterministic evidence precedes semantic/model judges. A judge is advisory Evidence only.
- Test PASS cannot prove fun, usability, market fit, accessibility, or visual quality without the corresponding higher Evidence layer.
- A file or test definition existing does not prove execution.
- A merged label does not prove correct integration without merge SHA and main readback.
- Missing evidence is not repaired by confidence language.

## Rollback

Revert the implementation squash commit. Registry metadata, generated summary, Mode/reference, Template, behavior fixture, Learning Log, tests, and BCP lifecycle update must roll back together. Product code/data and #313/#316 correction paths are unaffected.
