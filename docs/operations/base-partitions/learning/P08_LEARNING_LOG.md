# P08 · AI Operations & External Executors — Learning Log

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

## 2026-08-19 · P08 partition optimization

```yaml
date: 2026-08-19
work_ref: PR #535 / P08 AI Operations & External Executors optimization
baseline_and_result: >-
  Base main df8ef644d30fc96456da23a5157e5efb61b620bb에서 시작해 기존 두 ACTIVE Skill을 유지하면서
  external-executor reviewer authority, current-canon rehydration, included-vs-metered cost surface,
  just-in-time Tool shortlist를 강화했다. 새 Skill/Mode/runtime/paid dependency는 추가하지 않았다.
what_worked:
  - P01 GPT/Codex authority를 read-only dependency로 재확인한 뒤 P08 consumer만 정렬
  - Skill overload 연구를 새 router 구축이 아니라 기존 sparse routing Guide의 Tool-side 원칙으로 흡수
  - OpenAI current plan/credits 문서를 이용해 GPT_PRO 포함 사용량과 credits/API 별도 비용을 분리
  - 외부 AI provider 이름을 바꾸는 대개편보다 현재 실행 semantics를 먼저 수정
  - P08 범위를 넘는 Template/generated-plugin/workflow ownership 문제를 직접 수정하지 않고 CROSS_PART_CHANGE_REQUEST로 격리
what_failed_or_was_rejected:
  - initial tests/test_p08_ai_operations_contract.py RED commit은 기존 selected CI가 자동 실행하지 않아 TDD_RED_CI를 관찰하지 못함
  - provider-neutral external-executor subsystem 전면 rename/migration은 현재 가치 대비 cross-Part blast radius가 커서 기각
  - dynamic Skill/Tool router runtime은 실측 model-run bottleneck 증거가 없어 기각
  - .codex-plugin/plugin.json 직접 수정은 released/generated derivative ownership과 충돌할 수 있어 기각
reusable_lesson: >-
  AI orchestration 최적화는 executor/model/tool을 더 추가하기 전에 실행 권위와 비용 surface를 먼저 분리하고,
  외부 executor가 실행 직전 current canon과 exact branch/commit을 다시 읽게 해야 한다. sparse Skill routing은
  Tool에도 just-in-time 원칙을 적용할 수 있지만 Skill/Tool을 하나의 고정 숫자 budget으로 합치면 안 된다.
anti_pattern:
  - GPT 다음 단계라는 이유만으로 Codex를 의무 호출
  - GPT_PRO 구독을 credits/API/auto-top-up의 포괄 승인으로 해석
  - handoff summary를 current canon보다 우선
  - Tool 수를 줄이는 것 자체를 정확도 개선으로 주장
  - generated/control-plane artifact를 Part worker가 직접 수정
  - CI가 선택하지 않은 신규 test를 실행됐다고 보고
affected_rules_skills_modules:
  - GPT_FIRST_PLANNING_AND_REVIEW
  - OPTIONAL_CODEX_EXECUTOR
  - ZERO_INCREMENTAL_COST_REQUIRED
  - DEFAULT_SUPPORTING_SKILL_BUDGET: 1
  - orchestrating-deepseek-worktrees
  - optimizing-ai-model-and-prompt-costs
  - AI Instruction / Context
  - Model / Cost Routing
  - External AI Worktree Orchestration
  - Optional Executor Handoff
evidence:
  - docs/operations/ai-executors/P08_OPTIMIZATION_REPORT_2026-08-19.md
  - skills/orchestrating-deepseek-worktrees/SKILL.md
  - skills/optimizing-ai-model-and-prompt-costs/SKILL.md
  - docs/knowledge/ai/SKILL_ROUTING_PRECISION_GUIDE.md
  - docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md
  - tests/test_p08_ai_operations_contract.py
  - OpenAI Harness engineering / Unrolling the Codex agent loop / Codex plan and credits official documentation
  - Anthropic Writing effective tools for agents / Effective context engineering for AI agents
  - Git git-worktree official documentation
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: >-
  CP0 Integration에서 external-AI companion Template/checker/schema/test ownership, generated .codex-plugin ownership,
  tests/test_p08_*.py CI discoverability를 명시적으로 정리할 가치가 있다.
source_followup_questions:
  - 실제 Base model-run eval에서 Tool/Skill shortlist가 오선택과 총 context 비용을 얼마나 줄이는가?
  - 외부 executor가 늘어날 때 DeepSeek-specific naming이 실제 routing 오류를 만들기 시작하는 임계점은 무엇인가?
  - GPT/Codex plan의 included usage와 flexible credits 경계가 변경되면 COST_SURFACE_GATE provider profile을 어떻게 갱신할 것인가?
revisit_condition: >-
  provider/plan 정책 변경, 2개 이상 외부 executor의 상시 운영, measured routing regression,
  CP0 ownership 재분류, 또는 optional executor semantics가 실제 프로젝트 실행을 막는 경우.
```

## Source Learning

- Source domains: PROMPT_AND_AGENT_WORKFLOW, SKILL_AUTHORING_AND_EVOLUTION, CODE_ENGINEERING
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.
