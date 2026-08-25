# P01 · Project Planning, Operations & Notion — Learning Log

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

## 2026-08-19 · P01 workspace-authority normalization

```yaml
date: 2026-08-19
work_ref: P01 / PR #534
baseline_and_result: "df8ef644d30fc96456da23a5157e5efb61b620bb -> PR head pending final validation/merge"
what_worked:
  - "최신 main exact SHA와 P01 Manifest/Context Pack/Notion 정본을 먼저 복원한 뒤 consumer drift를 수정했다."
  - "새 Skill이나 중복 정책을 만들지 않고 기존 DOMAIN_SPLIT_CANON을 P01 active consumer에 일관되게 적용했다."
  - "영구 Base v9 CI module에 먼저 실패 assertion을 넣어 실제 RED를 확인한 뒤 production 문서를 변경했다."
  - "기존 concurrent-work contract의 EXPLICIT_USER_ABSORPTION_AUTHORIZATION 경계를 재사용해 더 구체적인 no-absorption 작업 계약을 보호했다."
  - "canonical partition scope checker를 영구 P01 회귀 테스트에서 직접 실행해 scope PASS를 실행 증거로 만들었다."
what_failed_or_was_rejected:
  - "초기 tests/test_p01_notion_workflow_authority_contract.py는 영구 CI에서 자동 발견되지 않아 test 존재를 실행 증거로 사용할 수 없었다. assertion을 기존 permanent CI module에 흡수하고 중복 파일은 삭제했다."
  - "Manifest가 가리키는 누락된 PROJECT_WORKSPACE_AUTHORITY_POLICY.md를 새로 만드는 안은 JSON authority contract와 isolation policy의 중복 canonical owner를 만들기 때문에 기각했다."
  - "Google Sheets active dual-sync 유지안은 현행 Notion/Repository authority와 충돌해 기각했다."
  - "Project Workspace 전용 신규 Skill은 기존 intake/project-OS/design-document 책임과 계약을 중복하므로 기각했다."
reusable_lesson: "Authority migration이 이미 canonical contract에 완료되어 있다면 새 정책/Skill을 만들기보다 stale consumer와 실행되는 regression을 먼저 정리한다. 또한 generic standing integration authorization은 현재의 더 구체적인 read-only/no-absorption 작업 계약을 넓힐 수 없다."
anti_pattern:
  - "legacy compatibility surface를 active workspace처럼 계속 소비"
  - "테스트 파일 존재를 실제 RED/PASS 실행으로 오인"
  - "standing integration authorization을 current explicit no-absorption boundary보다 강하게 해석"
  - "누락된 경로를 발견했다는 이유만으로 중복 canonical policy 생성"
affected_rules_skills_modules:
  - "DOMAIN_SPLIT_CANON / NOTION_HUMAN_FACING_CANON / REPOSITORY_STRUCTURED_CANON / COMPATIBILITY_ONLY"
  - "managing-project-intake-and-work-contract"
  - "managing-game-project-operating-system"
  - "PLANNING_FIRST_GRILL_ME_BATCH_POLICY"
  - "Project Workspace Authority / Decision Batch / Continuous Work modules"
evidence:
  - "baseline main df8ef644d30fc96456da23a5157e5efb61b620bb"
  - "PR #534"
  - "TDD RED: Validate Base v9 Operating Contracts run 32222958528"
  - "GREEN before final scope hardening: Validate Base v9 Operating Contracts run 32223803242"
  - "canonical scope checker invocation: tests/test_notion_project_isolation_core_system_contract.py"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "Specific-work-contract precedence over generic standing integration authorization + executed-test evidence discipline"
source_followup_questions:
  - "legacy Sheet active references가 0이 된 뒤 CP0 Registry/global routing에서 compatibility trigger를 언제 완전히 제거할 것인가?"
  - "PROJECT_WORKSPACE_AUTHORITY_CONTRACT schema v2와 stale schema-v1 consumer test를 Integration에서 어떻게 단일화할 것인가?"
revisit_condition: "CP0 Registry/Manifest Integration 완료, stale schema-v1 test 교정, 또는 실제 프로젝트 Notion migration pilot에서 새로운 consumer gap이 발견될 때"
```

## 2026-08-25 · project instruction revision non-regression recovery

```yaml
date: 2026-08-25
work_ref: "PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION v4.8 r2→r3→r4 recovery"
baseline_and_result: >-
  The approved r2 contract had 1,721 lines and a broad project lifecycle covering planning,
  benchmark/trade study, Notion delivery, IRG, TDD, recovery, PR/CI, and completion evidence.
  A condensed r3 rewrite fell to 1,319 lines and removed multiple material capabilities.
  The recovery rebuilt from r2 as the baseline instead of from the condensed rewrite; r4
  reached 2,036 lines, preserved the prior capability set, and added an explicit revision
  non-regression gate plus new local-execution/update requirements.
what_worked:
  - "Treat the last approved revision as the baseline and inventory machine keys, major sections, acceptance/evidence blocks, and required capabilities before rewriting."
  - "Use additive change by default; require an explicit replacement owner plus migration evidence for any removal or compression of an existing capability."
  - "Compare capability presence rather than trusting a shorter or cleaner-looking document to be semantically equivalent."
  - "Keep temporary scheduling facts such as project order or simultaneous-project count out of the durable project execution contract unless they are intentionally promoted to policy."
  - "After a regression is found, restart from the last known-good baseline rather than patching the already-regressed derivative."
what_failed_or_was_rejected:
  - "Rewriting the contract from a summary of the old document: r3 became easier to read but silently lost planning, evidence, recovery, and lifecycle capabilities."
  - "Using line count alone as quality evidence: the r3 size drop was a useful alarm but capability inventory/diff was required to prove the regression."
  - "Embedding short-lived workload choices into a long-lived common contract was rejected because user scheduling can change independently of project execution invariants."
  - "Assuming that latest Base owner delegation makes any deleted project-specific invariant safe; the replacement owner and behavior must be demonstrated, not inferred."
reusable_lesson: >-
  Long-lived project instructions, agent contracts, and operating adapters must be revised
  with a capability-level non-regression gate. Start from the last approved baseline,
  inventory executable semantics and evidence/recovery/completion contracts, then apply
  additions or explicit migrations. A rewrite is not an improvement if it is clearer or
  shorter but loses behavior that no current owner demonstrably replaces.
recurrence_response:
  trigger_signals:
    - "사용자가 이전 버전보다 퇴행했다고 지적"
    - "새 revision에서 major section, machine key, acceptance/evidence/recovery/completion block이 예상보다 감소"
    - "새 문서가 더 짧아졌는데 replacement owner/migration evidence가 없음"
    - "기존 프로젝트 작업에서 과거에 수행하던 필수 Gate가 새 지시문에서 라우팅되지 않음"
  immediate_actions:
    - "새 revision의 추가 수정/배포/정본 승격을 즉시 중단하고 REGRESSION_SUSPECTED로 분류한다."
    - "마지막 승인된 known-good baseline의 exact file/hash를 다시 확보한다."
    - "문제 revision을 복구 기준으로 사용하지 않고 baseline과 직접 비교한다."
    - "machine keys → major sections → lifecycle → acceptance/evidence → recovery → completion → reporting capability 순으로 diff한다."
    - "삭제·축약된 각 capability를 INTENTIONAL_MIGRATION / ACCIDENTAL_LOSS / DUPLICATE_OWNER_REMOVAL / TEMPORARY_FACT_REMOVAL로 분류한다."
    - "ACCIDENTAL_LOSS는 known-good baseline에서 복원하고 신규 요구는 additive patch로 다시 적용한다."
    - "INTENTIONAL_MIGRATION은 exact replacement owner, consumer path, evidence, rollback이 확인될 때만 유지한다."
    - "복구 후 대표 프로젝트 시나리오와 전체 capability inventory를 다시 검증하고 최소 5회 적대적 검토를 수행한다."
    - "퇴행 derivative는 active instruction으로 재사용하지 않고 superseded/rejected 상태를 명확히 남긴다."
  completion_condition: >-
    Baseline required capability 100% accounted for, every intentional removal has a
    demonstrated replacement/migration, new requirements are present, representative
    scenarios retain their gates, and adversarial review finds no unexplained loss.
prevention:
  before_revision:
    - "항상 last approved revision의 exact hash와 capability inventory를 먼저 고정한다."
    - "Task를 ADD / REPLACE / REMOVE / MOVE_OWNER로 분해하고 기본값은 ADD로 둔다."
    - "일시적 프로젝트 순서·동시작업 수·현재 queue 같은 운영값은 durable contract와 분리한다."
  during_revision:
    - "요약문을 새 본문으로 사용하지 않고 known-good baseline을 직접 편집한다."
    - "section 삭제나 대폭 축약 시 replacement owner와 migration evidence를 같은 diff에서 요구한다."
    - "문서 길이보다 capability/evidence/recovery/completion semantics를 비교한다."
    - "새 기능 추가 후에도 기존 owner routing, Notion/GitHub authority, PR/CI, IRG, failure recovery, completion gate를 다시 샘플링한다."
  before_publish:
    - "machine-key inventory diff PASS"
    - "major-section/lifecycle inventory diff PASS"
    - "acceptance/evidence/recovery/completion capability diff PASS"
    - "대표 프로젝트 cold-start/plan/build/review/merge/completion 시나리오 PASS 또는 NOT_RUN 명시"
    - "최소 5회 전체 적대적 검토 후 unexplained capability loss 0"
    - "이전 revision보다 개선된 점과 trade-off를 사용자에게 기능 단위로 보고"
anti_pattern:
  - "summary-first rewrite of a mature operational contract"
  - "shorter document = better prompt without representative capability comparison"
  - "delete a rule because a shared owner probably covers it"
  - "mix temporary queue/order/capacity decisions into durable execution canon"
  - "repair a regressed derivative instead of rebasing the revision on the last known-good contract"
affected_rules_skills_modules:
  - "managing-project-intake-and-work-contract"
  - "managing-game-project-operating-system"
  - "maintaining-project-context-and-handoff"
  - "LONG_HORIZON_WORK_EXECUTION_POLICY / BEST_LONG_TERM_EFFICIENT_METHOD"
  - "Base owner progressive-load / thin project adapter"
  - "Implementation Reality Gate and completion evidence"
evidence:
  - "Conversation artifact r2 total_file_lines=1721"
  - "Conversation artifact r3 total_file_lines=1319"
  - "Conversation artifact r4 total_file_lines=2036"
  - "r4 REVISION_NON_REGRESSION_GATE explicitly inventories baseline keys, sections, capabilities, additions/replacements/removals, replacement owner/evidence, and blocks unexplained capability loss"
  - "User review identified r3 as materially regressed before the r4 recovery"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: >-
  Generalize a capability-preserving revision/eval gate inside the existing project-intake,
  project-OS, or long-horizon owner. Do not create a separate broad Skill solely for this
  lesson; prefer a focused reference/eval that can compare mature instructions and adapters.
source_followup_questions:
  - "Which existing Base owner should own a reusable capability inventory/eval for long-lived project instructions without duplicating CP0 validation?"
  - "Which representative project adapters should become regression fixtures if this lesson is promoted?"
  - "Can machine-key/section inventory be combined with behavior evals so semantic loss is detected even when wording changes?"
revisit_condition: >-
  Revisit on the next material project-instruction revision, on any simplification that
  removes or delegates an existing invariant, or if another project adapter becomes shorter
  while its acceptance/recovery/completion behavior is not demonstrably preserved.
```

## 2026-08-25 · Blacksmith cold-start handoff and Notion binary-evidence boundary

```yaml
date: 2026-08-25
work_ref: "Blacksmith PR #207 / BS-OPS-20260825-08 session handoff"
baseline_and_result: "Blacksmith planning state was spread across current successor canon, legacy Active Context, Human Notion surfaces, AI System Record, Sheet compatibility mirror, and Asset Library/Drive records; handoff now uses a current locator that requires fresh discovery and records explicit evidence ceilings."
what_worked:
  - "Treat the handoff as a cold-start locator, not a frozen source of truth: next session must re-read Base, repository main/open PRs, Sheet, Notion Human/AI surfaces before mutation."
  - "Separate Human Home from AI/System evidence while keeping both linked to repository authority."
  - "Demote a frozen legacy Active Context snapshot explicitly instead of rewriting historical evidence or allowing it to outrank the successor owner."
  - "Verify Notion asset storage with actual record readback rather than inferring image upload from Approved=true or a Drive Source URL."
what_failed_or_was_rejected:
  - "Asset Library row + Approved=true + hash + durable Drive PNG was previously described too broadly as 'uploaded to Notion'; representative readback showed no Preview FILES evidence and one page was blank."
  - "A handoff that copies current values without a fresh-read instruction was rejected because it would become the next predecessor ceiling."
reusable_lesson: "A durable project handoff should store current owners, superseded semantics, protected PR boundaries, unresolved gates, and evidence ceilings, while explicitly requiring fresh discovery on resume. For Notion visual delivery, metadata/source-link evidence must be separated from native Preview/page-binary evidence."
anti_pattern:
  - "handoff as immutable replacement for fresh repository/workspace discovery"
  - "Approved asset record or Drive URL treated as proof of native Notion image embedding"
  - "legacy router retaining higher current authority after a successor owner is verified"
affected_rules_skills_modules:
  - "maintaining-project-context-and-handoff"
  - "managing-project-intake-and-work-contract"
  - "Notion human/AI workspace authority"
  - "canonical reference freshness"
evidence:
  - "Blacksmith docs/operations/BS-OPS-20260825-08_SESSION_HANDOFF_CORE_SIMPLIFICATION.md"
  - "Fresh Notion Asset readback: BS-VIS-20260820-01 page blank; BS-VIS-20260820-04/08 page bodies contain durable Drive links but no Preview FILES evidence"
  - "Fresh Drive readback: BS-VIS-20260820-01 PNG exists, image/png, 2,165,251 bytes"
  - "Base evidence packet: docs/evidence/2026-08-25-blacksmith-canon-visual-handoff-learning.md"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "Handoff-as-locator + explicit destination evidence ceilings; native Notion image claim requires Preview/page-file readback"
source_followup_questions:
  - "Does the available Notion native file-upload path differ by connector/product surface, and can a cross-project test prove the same Preview evidence rule?"
  - "Should the handoff owner expose a standard destination-evidence matrix for Notion/Drive/GitHub/Sheet?"
revisit_condition: "Revisit after another project exercises native Notion image upload/readback or a second project handoff exposes the same stale-router failure."
```

## Source Learning

- Source domains: PROMPT_AND_AGENT_WORKFLOW, SKILL_AUTHORING_AND_EVOLUTION
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.