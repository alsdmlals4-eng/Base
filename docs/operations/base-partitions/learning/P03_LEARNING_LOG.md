# P03 · Adversarial Quality, Refactoring & Git Integrity — Learning Log

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

### 2026-08-19 — Evidence-bounded finding validation and Git execution surfaces

```yaml
date: 2026-08-19
work_ref: "P03 independent optimization / PR #537 / opt/base-part-P03-evidence-bounded-integrity"
baseline_and_result: "Base main df8ef644d30fc96456da23a5157e5efb61b620bb -> PR #537 exact-head validation candidate; merge result is recorded by the completion packet after main readback"
what_worked:
  - "A test-only first commit reproduced the missing configured-workspace contract before production edits."
  - "Existing adversarial and Git-sync Skills absorbed the improvement without creating another active Skill."
  - "Repository-native canonical-reference freshness caught the missing focused-test and Skill Learning Log companions after the first production candidate."
  - "Exact-head CI then verified the focused adversarial lifecycle and broader Base contracts after the companion fixes."
what_failed_or_was_rejected:
  - "Active P03 review references still treated Google Sheets as a default synchronization surface even though current operations require workspace-specific authority."
  - "Connector fallback existed, but the Git preflight schema did not distinguish connector-only execution from a real local worktree."
  - "The first production candidate omitted required focused-test and Skill Learning Log companions; canonical-reference freshness rejected it."
  - "A new quality Skill/checker was rejected because it would duplicate P02 freshness and P07 execution-evidence ownership."
  - "Direct CP0 Registry/Manifest edits were rejected because P03 does not own those paths."
reusable_lesson: "Executable critiques are more reliable when the proposed fix must demonstrate counterfactual improvement under the same acceptance/evidence ceiling; evidence providers must also identify their execution surface so unavailable local state is never inferred from remote evidence."
anti_pattern:
  - "Treating one retired or migration-only external workspace as a universal authority surface."
  - "Inventing a local worktree, dirty state, or local test result during connector-only Git execution."
  - "Treating focused GREEN as proof of broader compatibility or ignoring coupled-change freshness requirements."
  - "Adding a new Skill when an existing owner can absorb the responsibility with a narrower reference/test contract."
affected_rules_skills_modules:
  - "running-adversarial-review-and-refinement / Finding Validation / Post-change Monitor"
  - "synchronizing-local-and-github-state / Git Sync/Isolation"
  - "FULL_LOOP_COUNT_MINIMUM + CLEAN_REVIEW_EXIT evidence ceiling"
  - "INDEPENDENT_WORKSTREAM_ISOLATION"
evidence:
  - "test-only RED commit 6fa6dcae9d8952c53b68d506c6d4655fa6e4e5ff"
  - "canonical-reference freshness failure on production candidate abe0ec3a900d8cd28cfffb82ec3c1b258ff62f1f"
  - "Validate Integrated Vertical Slice Prompt success on corrected head 66438a9ec6c9d4ddb285fd2f95e7dd86e1ac544d"
  - "Validate Base v9 Operating Contracts success on corrected head 66438a9ec6c9d4ddb285fd2f95e7dd86e1ac544d"
  - "P03 Manifest-owned changed paths only; scope classification replayed with the checker --files contract"
  - "Git worktree/branch isolation, GitHub exact-head/status-check rules, disciplined refactoring guidance, and external-feedback/self-correction research reviewed as supporting sources"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "General evidence-surface identity and fix-guided counterfactual verification may be reusable beyond P03, but CP0 Integration must decide any shared-policy promotion."
source_followup_questions:
  - "Does fix-guided verification materially reduce false-positive MUST_FIX findings across several real Base audits without increasing review cost excessively?"
  - "Do repeated connector/local mixed workflows justify a machine-readable execution_surface field in a future shared evidence schema?"
revisit_condition: "Revisit when adversarial review creates measurable overcorrection/churn, connector/local evidence is confused again, or P03/P07 evidence ownership becomes ambiguous in repeated incidents."
```

## Source Learning

- Source domains: CODE_ENGINEERING, PROMPT_AND_AGENT_WORKFLOW
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.