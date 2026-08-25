# P08 · AI Operations & External Executors — Context Pack

## 현재 실행 계약
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS` · `PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER`

이 Part는 semantic responsibility / learning / validation checkpoint다. 현재 coordinator가 다른 Part/CP0의 검증된 오류·충돌·누락을 발견하면 다른 Part라는 이유만으로 보류하지 않고 `CROSS_PART_CHANGE`로 owner를 기록해 직접 수정할 수 있다. 단, 다른 독립 open/draft/ready PR·branch·worktree는 `ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`에 따라 read-only다.

## 2026-08-25 역할 분리 정본

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING
```

과거 `GPT_PRIMARY_REVIEWER + OPTIONAL_CODEX_EXECUTOR`는 **구현 단계에서도 Codex가 선택적이라는 뜻으로 사용하지 않는다.** 현재 의미는 다음과 같다.

- 기획·조사·검수·Notion 정리·이미지 제작만 있으면 Codex 실행이 필요 없다.
- 코드·데이터·Scene·Resource·test·build·runtime 구현이 존재하면 Codex가 기본 implementation executor다.
- GPT는 PowerShell/local Codex를 직접 구동하는 기본 경로를 사용하지 않는다.
- Codex는 구현 전에 현재 GitHub와 관련 Notion 정본을 다시 읽는다.
- Codex는 이미지를 생성·편집하지 않고 Notion에 현재 용도로 승인·업로드·readback된 이미지와 자산만 사용한다.
- 이미지가 부족하면 `GPT_VISUAL_REQUEST`를 반환하고 독립 구현은 계속할 수 있다.

Canonical owner: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

## 역할

P08은 AI instruction/context, model/cost routing, source/research, 구현 executor handoff, 외부 worktree 격리와 실행 재수화를 책임진다.

### GPT

- 기획·조사·벤치마킹·적대적 검수
- 구현 전 acceptance/보호 계약
- 이미지 생성·편집·검수와 Notion 승인 전달
- Codex handoff 및 구현 결과 최종 검수

### Codex

- current GitHub + Notion rehydration
- 승인 범위 repository 구현·코딩·테스트·runtime 검증
- 실제 변경·테스트·런타임 evidence 반환
- 기획 변경이 필요하면 `CHANGE_PROPOSAL`
- 이미지가 필요하면 `GPT_VISUAL_REQUEST`

## 핵심 Skill
`orchestrating-deepseek-worktrees`, `optimizing-ai-model-and-prompt-costs`, `maintaining-project-context-and-handoff`.

## 핵심 Module

```text
GPT Planning / Review / Visual
→ Implementation Ready?
   ├─ No → GPT canon/readback/final review
   └─ Yes → Codex Handoff
             → GitHub + Notion Rehydration
             → Optional Technical Preflight
             → Repository Implementation / Test / Runtime
             → Missing Visual?
                ├─ No → Evidence
                └─ Yes → GPT_VISUAL_REQUEST
                          → GPT create/review
                          → Notion approved upload/readback
                          → Codex resume
             → GPT Final Review
```

## 중요 규칙

- `ZERO_INCREMENTAL_COST_REQUIRED`, `CURRENT_PAID_PLANS: GPT_PRO` 유지.
- 별도 Codex Plan은 `CODEX_PREFLIGHT_OPTIONAL`; Codex 구현 책임 자체는 optional이 아니다.
- 외부 executor 결과는 GPT/정본/테스트 검토 전까지 `EXTERNAL_AI_RESULT_REVIEW_PENDING`다.
- 구현자는 실행 직전 current `AGENTS.md`, GitHub canon, relevant Notion canon, exact branch/commit, protected paths, tests를 읽는다.
- 다른 프로젝트/worktree 혼입 금지.
- 다른 독립 open/draft/ready PR은 read-only.
- 이미지 생성은 Codex executor capability가 아니라 GPT visual pipeline으로 라우팅한다.

## 비용·Tool 경계

- 기본 supporting Skill 수를 성과로 취급하지 않는다. 현재 단계에 필요한 최소 Tool/Skill만 사용한다.
- 구독 포함 사용량과 API/credits/새 SaaS/hosted compute/storage를 구분한다.
- 별도 결제는 사용자 승인 없이 기본 경로로 만들지 않는다.
- 로컬 PowerShell/Codex launcher를 GPT 작업의 상시 중간 계층으로 유지하지 않는다.

## 검증/완료

P08 변경은 최소 다음을 공격한다.

1. GPT가 구현·코딩 책임을 다시 가져가고 있지 않은가.
2. 구현 작업인데 Codex가 단순 optional로 빠지고 있지 않은가.
3. Codex가 GitHub만 읽고 Notion 기획·Visual을 놓치지 않는가.
4. Codex가 이미지 생성·편집 또는 임의 placeholder 제작을 하고 있지 않은가.
5. `GPT_VISUAL_REQUEST → GPT 제작/검수 → Notion 승인 업로드/readback → Codex 재개`가 닫히는가.
6. 다른 open PR/worktree·프로젝트가 보호되는가.
7. 비용·권한·evidence Gate가 약화되지 않았는가.

최소 5회 전체 적대적 개선 후 clean까지 반복한다.

## 학습 루프

- 작업마다 `docs/operations/base-partitions/learning/P08_LEARNING_LOG.md`에 Learning Checkpoint를 남긴다.
- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.
- 주기 Source domains: PROMPT_AND_AGENT_WORKFLOW, SKILL_AUTHORING_AND_EVOLUTION, CODE_ENGINEERING.
- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.