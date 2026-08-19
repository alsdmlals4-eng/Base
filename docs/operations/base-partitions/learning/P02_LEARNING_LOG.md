# P02 · Skill Governance, Canon Freshness & Legacy — Learning Log

> 이 로그는 해당 Part 작업에서 실제로 확인된 교훈만 축적한다. 추정·외부 snippet·미검증 Source는 학습 사실로 승격하지 않는다.

## 작업별 Learning Checkpoint

각 완료 작업마다 아래 형식으로 하나의 checkpoint를 추가한다. 새 재사용 교훈이 없으면 `reusable_lesson: NO_NEW_REUSABLE_LESSON`로 명시하고 억지 교훈을 만들지 않는다.

```yaml
date:
work_ref:
baseline_and_result:
what_worked: []
what_failed_or_was_rejected: []
reusable_lesson:
anti_pattern: []
affected_rules_skills_modules: []
evidence: []
reuse_scope: PART_ONLY | BASE_PROMOTION_CANDIDATE | PROJECT_ONLY | NO_NEW_REUSABLE_LESSON
promotion_candidate:
source_followup_questions: []
revisit_condition:
```

### 2026-08-19 · P02 independent partition audit

```yaml
date: 2026-08-19
work_ref: docs/operations/legacy-retirement/2026-08-19-P02-skill-governance-canon-legacy-audit.md
baseline_and_result: "main df8ef644d30fc96456da23a5157e5efb61b620bb -> P02-owned audit + cross-part correction packet; no CP0 or protected PR #530 writes"
what_worked:
  - "Pin latest completed main before auditing Skill/consumer state."
  - "Compare the declared Part owner paths against the live canonical path instead of trusting either one alone."
  - "Treat coupled-change rules as part of effective write ownership, not only as CI details."
  - "Keep the independent draft PR #530 read-only and separate baseline defects from work already in progress there."
what_failed_or_was_rejected:
  - "Direct alias-parser fix was rejected in this Part because checker changes unconditionally require CP0 .github/reference-freshness.json."
  - "Direct legacy Skill procedure change was rejected because the current coupled rule unconditionally requires CP0 BASE_SHARED_SKILL_ROUTES.json."
  - "Creating proposals/** to match the Manifest was rejected because the live BCP registry declares [수정제안서] as the single proposal root."
  - "Creating a P02-local Registry/config control plane was rejected as duplicate authority."
reusable_lesson: "Atomic change-set ownership must match Part write ownership. A file is not independently Part-owned when its mandatory no-op companion is owned by CP0; coupled-change contracts must follow semantic coupling, not unconditional file pairing."
anti_pattern:
  - "Claiming ownership from Manifest paths without checking mandatory companions."
  - "Satisfying freshness by touching a control-plane file that has no semantic change."
  - "Resolving a path typo by creating a second canonical root."
affected_rules_skills_modules:
  - "P02 partition ownership"
  - "canonical reference freshness"
  - "Base Change Proposal"
  - "Legacy Absorb/Verify/Remove"
  - "check_canonical_reference_freshness.py"
evidence:
  - "docs/operations/BASE_PARTITION_MANIFEST.json"
  - ".github/reference-freshness.json#reference-checker-test-and-config-sync"
  - ".github/reference-freshness.json#legacy-retention-shared-skill-sync"
  - "[수정제안서]/PROPOSAL_REGISTRY.json"
  - "skills/LEGACY_SKILL_ALIASES.md"
  - "tools/check_canonical_reference_freshness.py"
  - "draft PR #530 changed-file inventory (read-only)"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "Integration should align mandatory semantic companion sets with Part ownership before expanding Partition use."
source_followup_questions:
  - "After CP0 coupling is corrected, does a multi-alias RED test catch every backticked alias in the first legacy-alias table cell?"
  - "After PR #530 completes, do any active P01/CP0 consumers still describe Google Sheets as a default project authority?"
  - "Do repeated Part changes justify generated ownership fragments, or is semantic coupled-rule refinement sufficient?"
revisit_condition: "Re-audit when P02-CP0-001/002/003 are integrated, after PR #530 completes, or if another P02-owned change requires a no-op CP0 companion edit."
```

## Source Learning

- Source domains: SKILL_AUTHORING_AND_EVOLUTION, CODE_ENGINEERING, PROMPT_AND_AGENT_WORKFLOW
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.
