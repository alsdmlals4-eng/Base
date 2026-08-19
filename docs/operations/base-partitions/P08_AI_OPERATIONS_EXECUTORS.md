# P08 · AI Operations & External Executors — Context Pack

## 역할
AI instruction/context, model/cost routing, source/research, DeepSeek/worktree와 선택적 외부 executor 운영을 책임진다.

## 핵심 Skill
`orchestrating-deepseek-worktrees`, `optimizing-ai-model-and-prompt-costs`.

## 중요 규칙
GPT primary, OPTIONAL_CODEX_EXECUTOR, minimal Skill routing, ZERO_INCREMENTAL_COST_REQUIRED, CURRENT_PAID_PLANS: GPT_PRO.

## 핵심 Module
Instruction/Context → Model/Cost → Source Research → DeepSeek Worktree → Optional Executor Handoff.

## 경계
GPT/Codex 역할 정본은 P01을 읽고, workstream isolation은 P03, evidence는 P07. Partition 공통 Prompt는 CP0이므로 P08의 `templates/prompts/**`보다 CP0 보호가 우선한다.

## 우선 공격 대상
도구/Skill 과다 호출, 불필요 유료 API/SaaS, executor가 GitHub/Notion 실제 상태를 재확인하지 않음, 다른 프로젝트/worktree 혼입.

## 검증/완료
AI/model/source 관련 focused tests와 scope 검사. 최소 5회 전체 적대적 개선 후 clean까지.
## 학습 루프
- 작업마다 `docs/operations/base-partitions/learning/P08_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: PROMPT_AND_AGENT_WORKFLOW, SKILL_AUTHORING_AND_EVOLUTION, CODE_ENGINEERING.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.
