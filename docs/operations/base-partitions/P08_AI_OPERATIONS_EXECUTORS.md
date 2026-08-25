# P08 · AI Operations & External Executors

## 목적

P08은 AI instruction/context, model/cost routing, 외부 executor, Codex handoff, worktree 격리와 실행 재수화의 semantic owner다.

## 현재 역할 계약

```text
GPT_NONCODING_PROJECT_OWNER
GPT_BASE_NOTION_GOVERNANCE_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
```

### GPT

- 기획·조사·벤치마킹·대안 비교
- 적대적 검토·IRG
- Base 정책·Skill·Guide·Template·Learning
- Base Registry/generated/CI/test contract
- Notion Home/Domain/AI System
- 문서·표·Flow·Storyboard
- 이미지 생성·편집·검수
- 프로젝트별 Codex Godot 구현지시문
- Codex 구현 결과 최종 검수

### Codex

- 실제 게임 프로젝트의 Godot 제품 구현만 담당
- GDScript/product code
- Scene/Resource/Autoload/runtime wiring
- runtime game data integration
- save/load product implementation
- UI runtime wiring
- shader/VFX/code-driven feedback
- build/export
- Godot implementation/runtime/headless/play tests

Codex는 Base repository의 일반 maintenance executor가 아니다. Base Python test·CI contract·Registry/generated checker처럼 코드 형식인 운영 인프라도 GPT 작업이다.

## Handoff

```text
GPT 기획·검수·비코딩 작업 완료
→ 실제 Godot 제품 구현 필요 여부 판정
→ 필요하면 프로젝트별 Codex Work Instruction
→ Codex가 해당 프로젝트 GitHub + Notion 재수화
→ Godot 구현 방향 결정
→ 구현·코딩·runtime/play test
→ READY_FOR_GPT_REVIEW
→ GPT 최종 검수
```

Base Template:

`templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`

## 외부 AI

DeepSeek 등 외부 AI는 대량 초안·분류·비교·독립 반례에 선택적으로 사용할 수 있다. 외부 AI 결과는 항상 `REVIEW_PENDING`이며 GPT가 검수한다.

외부 AI optionality와 Codex 제품 구현 ownership을 혼동하지 않는다.

- 외부 AI: optional assistant
- Codex: 실제 Godot 제품 구현이 있을 때 product implementation owner

## Rehydration

Codex는 Godot 구현 전에:

1. exact project/repository/worktree
2. project AGENTS/Active Context
3. current GitHub product paths
4. relevant Notion Project Home/Domain/AI System
5. approved Visual
6. current open workstream
7. actual runtime/test evidence

를 fresh-read한다.

## 이미지

```text
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
```

Codex는 이미지를 만들거나 생성형 편집하지 않는다. 필요한 자산이 없으면 `GPT_VISUAL_REQUEST`로 GPT에 반환한다.

## 비용

```text
ZERO_INCREMENTAL_COST_REQUIRED
CURRENT_PAID_PLANS: GPT_PRO
```

별도 API/SaaS/compute 비용은 사용자 승인 없이 기본 경로로 만들지 않는다.

## Open PR 보호

다른 open/draft/ready PR은 기본 read-only다. exact branch/head를 fresh-read하고 force push/history rewrite/destructive reset을 하지 않는다.

## 실패 조건

- Base/Notion 작업을 Codex로 넘김
- Python/JSON이라는 이유로 Base 운영 인프라를 Codex에 넘김
- 실제 Godot 제품 구현을 GPT가 누적 수행
- Codex가 이미지 생성
- stale GitHub/Notion만 보고 구현
- external AI 결과를 current canon으로 승격

## 완료 기준

P08 역할이 다음 한 줄과 일치해야 한다.

> **GPT는 기획·검수·Base·Notion·문서·Visual을 담당하고, Codex는 실제 게임 프로젝트의 Godot 제품 구현·코딩을 담당한다.**
