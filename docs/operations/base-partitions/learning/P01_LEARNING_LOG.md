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

## Source Learning

- Source domains: PROMPT_AND_AGENT_WORKFLOW, SKILL_AUTHORING_AND_EVOLUTION
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.
