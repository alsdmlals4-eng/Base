# P08 · AI Operations & External Executors

## 목적

P08은 AI instruction/context, model/cost routing, 외부 executor, Codex handoff, worktree 격리와 실행 재수화의 semantic owner다.

## 현재 역할 계약

```text
GPT_NONCODING_PROJECT_OWNER
GPT_BASE_NOTION_GOVERNANCE_OWNER
CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
CHAT_QUICK_DISCUSSION_DEFAULT
WORK_LONG_MULTISTEP_NONCODING_DEFAULT
ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON
```

`CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER`는 엔진 중립 상위 역할이다. 현재 기존 게임 프로젝트에서는 `ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON → GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER`이므로 `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER`가 compatibility vocabulary이자 실제 Godot adapter specialization으로 계속 유효하다.

### GPT

- 기획·조사·벤치마킹·대안 비교
- 적대적 검토·IRG
- Base 정책·Skill·Guide·Template·Learning
- Base Registry/generated/CI/test contract
- Notion Home/Domain/AI System
- 문서·표·Flow·Storyboard
- 이미지 생성·편집·검수
- 프로젝트별 Codex 제품 구현지시문
- Codex 구현 결과 최종 검수

### Codex

- 실제 게임 프로젝트의 제품 구현만 담당
- project canon이 선택한 engine adapter의 product code / Scene / Resource / runtime wiring
- runtime game data integration
- save/load product implementation
- UI runtime wiring
- shader/VFX/code-driven feedback
- build/export
- implementation/runtime/headless/play tests

현재 Godot 프로젝트에서는 위 항목이 기존과 동일하게 다음 compatibility surface를 뜻한다.

- `GDScript/product code`
- `Scene/Resource/Autoload/runtime wiring`
- Godot build/export
- Godot implementation/runtime/headless/play tests

Codex는 Base repository의 일반 maintenance executor가 아니다. Base Python test·CI contract·Registry/generated checker처럼 코드 형식인 운영 인프라도 GPT 작업이다.

## Chat / Work / Codex 기본 라우팅

2026-08-26 current product guidance 기준으로 ChatGPT의 작업면은 작업의 길이와 산출물 성격에 따라 나눈다.

### `CHAT_QUICK_DISCUSSION_DEFAULT`

다음은 Chat을 기본으로 한다.

- 빠른 질문과 설명;
- 짧은 브레인스토밍·선택지 비교;
- 사용자 결정이 필요한 단일 쟁점 정리;
- 긴 실행 전에 방향을 잡는 대화.

### `WORK_LONG_MULTISTEP_NONCODING_DEFAULT`

다음은 Work를 기본으로 한다.

- 여러 단계의 프로젝트 기획·조사·분석·감사;
- GitHub/Notion/파일 등 연결된 자료를 넘나드는 GPT-owned 작업;
- Base·Notion·문서·표·보고서·검수·인수인계;
- 완료까지 긴 실행 흐름과 readback이 필요한 작업;
- 반복 또는 예약 작업이 실제로 유용한 프로젝트 운영 작업.

Work는 GPT-owned 작업을 더 오래 수행하는 **실행 작업면**이며 새 정본 저장소가 아니다. Work의 대화/중간 산출물만으로 canon을 만들지 않고, 승인된 결과는 기존 Notion/GitHub owner에 기록하고 readback한다.

### `CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER`

실제 software/game product implementation boundary에 들어가면 Codex가 담당한다. Codex는 해당 프로젝트의 GitHub + Notion을 fresh-read하고 `ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON`에 따라 현재 엔진 adapter를 사용한다.

```text
Chat · quick discussion / decision shaping
→ Work · long multi-step GPT-owned planning/review/Base/Notion execution
→ approved implementation handoff
→ Codex · actual game product implementation
→ selected engine adapter
→ runtime/play evidence
→ GPT final review
```

Work를 사용하더라도 `GPT_NONCODING_PROJECT_OWNER`, `GPT_BASE_NOTION_GOVERNANCE_OWNER`, `CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR` 경계는 바뀌지 않는다.

## Shared Work project instruction

프로젝트별 ChatGPT Work의 공용 실행 adapter는 다음 두 파일을 하나의 bundle로 사용한다.

```text
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md
templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md
```

정상적인 기본 입력은 **`프로젝트명 + 공용 작업지시문`만**이다. 별도 Goal은 사용자가 특정 작업을 우선하고 싶을 때만 선택적으로 줄 수 있다. Goal이 없으면 Work가 current Project GitHub/Notion canon에서 `current stage → active/approved current work → blockers/dependencies → roadmap/accepted frontier → next safe playable slice → current work contract`를 복원한다. 단순히 Goal 문장이 없다는 이유로 사용자의 작업 목표를 다시 묻지 않는다.

본체와 Compatibility appendix는 r5.4의 planning/reuse/verification 기능 및 execution-scope, external process, toolchain freshness, local Godot/Fresh Shell, retired-surface, prompt-efficiency 경계를 함께 보존한다. 두 파일은 서로 다른 정본이 아니라 하나의 실행 bundle이다.

사용자에게 전달하는 단일 다운로드 파일은 본체와 appendix를 결합할 수 있다.

Work 대화를 정본으로 만들지 않고 current Project GitHub/Notion과 Base current owner를 다시 읽으며 Default memory는 discovery-only 후보로만 사용한다. 이 bundle은 P08·Base 상세 절차의 두 번째 정본이 아니다. 현재 `skills/SKILL_REGISTRY.json`을 inventory하고 복원된 current work contract 또는 사용자가 명시한 특정 작업에 맞는 Skill만 progressive-load하며, 실제 세부 owner가 최신 Base에서 바뀌면 current Base owner가 우선한다.

## Handoff

```text
GPT 기획·검수·비코딩 작업 완료
→ 실제 게임 제품 구현 필요 여부 판정
→ 필요하면 프로젝트별 Codex Work Instruction
→ Codex가 해당 프로젝트 GitHub + Notion 재수화
→ project canon의 engine adapter 확인
→ 구현 방향 결정
→ 구현·코딩·runtime/play test
→ READY_FOR_GPT_REVIEW
→ GPT 최종 검수
```

현재 Godot 프로젝트의 handoff는 기존 `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER`와 Godot-specific implementation contract를 그대로 사용한다.

Base Template:

`templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`

Engine baseline/adapter owner:

`docs/knowledge/game-development/ENGINE_BASELINE_AND_ADAPTER_POLICY.md`

## 외부 AI

DeepSeek 등 외부 AI는 대량 초안·분류·비교·독립 반례에 선택적으로 사용할 수 있다. 외부 AI 결과는 항상 `REVIEW_PENDING`이며 GPT가 검수한다.

외부 AI optionality와 Codex 제품 구현 ownership을 혼동하지 않는다.

- 외부 AI: optional assistant
- Codex: 실제 게임 제품 구현이 있을 때 product implementation owner

## Rehydration

Codex는 제품 구현 전에:

1. exact project/repository/worktree
2. project AGENTS/Active Context
3. current GitHub product paths
4. relevant Notion Project Home/Domain/AI System
5. approved Visual
6. current open workstream
7. actual runtime/test evidence
8. selected engine adapter / stable engine baseline

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
- 실제 게임 제품 구현을 GPT/Work가 누적 수행
- Work 대화 상태를 Notion/GitHub 정본 대신 사용
- project canon을 무시하고 engine adapter를 임의 변경
- Codex가 이미지 생성
- stale GitHub/Notion만 보고 구현
- external AI 결과를 current canon으로 승격
- 별도 Goal이 없다는 이유만으로 current canon 조회 전에 사용자의 목표를 다시 질문

## 완료 기준

P08 역할이 다음 한 줄과 일치해야 한다.

> **Chat은 빠른 논의, Work는 프로젝트명+공용 지시문만으로도 current canon에서 작업 계약을 복원해 긴 multi-step GPT-owned 기획·검수·Base·Notion 작업을 수행하고, Codex는 실제 게임 프로젝트의 제품 구현을 담당하며 현재 기존 게임은 Godot adapter를 사용한다.**
