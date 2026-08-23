# Human Home + AI/System Separation Design

## Goal

Base와 모든 프로젝트의 Notion 진입면을 `사람이 프로젝트를 배우고 이해하고 수정 방향을 판단하는 Human Home`과 `AI/자동화가 작업·검증·동기화를 수행하는 AI/System surface`로 명확히 분리한다. Home은 정보량을 줄이는 요약 페이지가 아니라 프로젝트 전체 핵심을 시각자료·Flow·시스템·사람용 데이터와 함께 자체 완결적으로 설명하는 학습형 페이지다.

## Authority

- 최신 사용자 지시와 승인된 프로젝트 결정이 최우선이다.
- `NOTION_HUMAN_FACING_CANON`은 사람이 읽고 비교·학습·수정하는 전체 그림, Visual, Flow, 예산/Tier/로스터/경제/성장 등 사람용 표현을 소유한다.
- `REPOSITORY_STRUCTURED_CANON`은 Markdown, JSON, game data, code, Scene, Resource, Test를 소유한다.
- `REPOSITORY_RUNTIME_TRUTH`은 실제 build/test/runtime evidence를 소유한다.
- `90 · SYSTEM MASTERS`, Project Registry, raw PR/SHA/CI/Prompt/Hash/Implementation Path는 AI/System surface다.

## Core decision

선택안은 `풍부한 Human Home + 기존 AI/System 상세 원본 재사용`이다.

### REJECT — Home 축소 + AI metadata만 제거

혼재는 줄지만 핵심 시스템·데이터·Visual이 계속 하위 페이지에 숨어 사용자가 전체 게임을 배우기 어렵다.

### REJECT — 모든 하위 내용을 Home에 복제

처음 읽기는 풍부하지만 동일 수치·시스템·상태의 중복 정본이 생겨 drift와 재동기화 비용이 커진다.

### ADOPT — Rich Human Home + single-owner drilldown/projection

Home에는 사람이 이해해야 할 핵심을 직접 설명하고, 긴 표/전체 목록/원시 evidence는 기존 drilldown·Master·repository owner에 유지한다. Home은 원본을 무차별 복사하지 않고 사람이 판단할 수 있는 설명·표·필터 view·시각 anchor로 투영한다.

### DEFER — 별도 자동 Home generator

현재 Notion MCP/linked view/readback으로 목표를 달성할 수 있으므로 추가 자동화·서비스·대시보드는 실제 반복 병목이 증명되기 전 도입하지 않는다.

## Human Home information architecture

### Base Home

Base Home은 다음 질문에 추가 이동 없이 답해야 한다.

1. Base는 무엇이며 왜 필요한가?
2. 게임/프로젝트 작업은 어떤 순서로 진행되는가?
3. 각 단계에서 사용자는 무엇을 결정하고 AI는 무엇을 처리하는가?
4. 핵심 Skill/Module은 언제 호출되고 입력→처리→출력이 어떻게 이어지는가?
5. 사용자가 AI의 해석이 틀렸다고 판단했을 때 어떻게 수정 요청하는가?
6. 현재 어떤 작업면이 active이고 어떤 작업면이 retired인가?
7. 현재 구현/검증 상태에서 무엇이 실제 PASS이고 무엇이 NOT_RUN인가?

Base Home에는 raw PR 번호 나열, exact SHA 이력, CI run ID, closure receipt, connector 내부 transport, debug routing을 기본 노출하지 않는다. 이런 정보는 P01~P09/AI/System drilldown에서 보존한다.

### Project Home

Project Home은 프로젝트 성격에 맞춰 다음 층을 직접 보여준다.

1. **게임/작품 한눈에 보기** — 한 줄 정의, 장르/톤, 플레이어 판타지, 핵심 재미, 현재 단계.
2. **전체 Flow Map** — 플레이어/독자가 무엇을 보고 선택하고 어떤 결과와 보상을 거쳐 다음 상태로 가는지.
3. **핵심 시스템** — 목적, 플레이어 의미, 작동, 상호작용, 왜 재미/가치를 만드는지.
4. **프로젝트 핵심 데이터** — 프로젝트에 실제 필요한 예산/경제/몬스터/상대/아이템/기술/로스터/성장/Route/Map 등. 모든 게임에 같은 항목을 강제하지 않는다.
5. **Visual / Asset** — 승인된 HERO/PRIMARY 시각자료와 설명. 지원 자료는 Visual Bible/Asset drilldown에 둔다.
6. **AI가 이해한 설계 의도** — 사용자가 교정할 수 있도록 핵심 경험·우선순위·보호 요소를 사람말로 요약한다.
7. **사용자가 수정하는 방법** — 설명 수정, 기획/규칙 수정, 이미지 수정 요청의 차이를 중학생 수준으로 설명한다.
8. **현재 제작 상태** — 완료/진행/예정과 `PASS / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED`를 과장 없이 표시한다.

Home의 정보량 자체는 제한하지 않는다. 판단 기준은 `사람이 프로젝트를 이해·학습·비교·수정하는 데 직접 필요한가`다.

## Human content vs AI/System metadata

### Human Home allowed

- 플레이어/사용자 가치
- 핵심 재미/감정/판타지
- Core Loop/Flow
- 핵심 시스템과 상호작용
- 사람용 예산·경제·Tier·Roster·Monster/Opponent·Item·Skill·Growth 표
- 승인 Visual과 현재 시각 방향
- `AI가 이해한 설계 의도`
- 사람이 이해할 수준의 구현/검증 상태와 다음 작업
- 중요한 결정의 이유와 revisit condition

### AI/System only by default

- Project Local Path / Codex Home / Godot Port
- raw Repo Main SHA / source hash / Revision / Record Key
- raw PR/commit/CI run history
- Prompt / AI Note / Asset ID / Hash / Implementation Path
- automation receipt / routing / debug data
- 내부 evidence ledger 전문

`AI가 이해한 설계 의도`는 AI 작업 로그가 아니다. 설계 해석을 사용자가 교정하기 위한 human-facing 설명이다.

## Human edit guide

Home은 최소 다음 수정 경로를 설명한다.

### 설명/표현만 수정

`사용자 요청 → Notion human expression update → readback`으로 끝날 수 있다.

### 게임 규칙/구조화 의미 수정

`사용자 제안 → 영향 분석 → 변경 전/후/기대효과 보고 → 사용자 승인 → repository structured canon sync → Notion human surface sync/readback → implementation` 순서를 따른다.

### 이미지 수정/생성

`프로젝트 전체/관련 Visual canon 검토 → Visual Need → 텍스트 Brief → STOP_REQUIRED`가 첫 대화 턴이다. 다음 사용자 메시지에서 명시적 이미지 생성/편집 승인이 있어야 `GENERATE_EXACTLY_ONE → STOP_REQUIRED`로 진행한다. 생성 직후 자동으로 다음 이미지 생성으로 연속 진입하지 않는다.

## Project work lifecycle

모든 L1 이상 중요 Base/프로젝트 작업은 다음 순서를 선행한다.

```text
CURRENT STATE / CANON / PR / SKILL / NOTION / ACTUAL IMPLEMENTATION AUDIT
→ BENCHMARK + PROFESSIONAL PRACTICE + SUCCESS/FAILURE CASES
→ >= 3 MATERIAL ALTERNATIVES
→ IMPLEMENTATION REALITY GATE
→ EXPECTED BEFORE / AFTER / EFFECTS / RISKS / ROLLBACK
→ >= 5 FULL ADVERSARIAL LOOPS UNTIL CLEAN
→ USER APPROVAL
→ BUILD
→ GitHub + Notion sync/readback during approved work
→ post-build >= 5 full adversarial loops until clean
→ exact-head PR/CI/merge
→ postmerge GitHub + Notion readback
```

프로젝트 제작은 두 단계로 본다.

1. `기획 → 독립 상세 검수 → 필요한 Flow/Component/Visual 요소 준비 → 승인 결과 즉시 GitHub+Notion 동기화`
2. `검수 완료 범위 Codex/Loop Engineering 구현 → release-near playable demo → 검증 → PR/merge/postmerge`

## Visual delivery rules

- 승인된 실제 이미지/목업/다이어그램은 해당 프로젝트 Visual Bible 또는 Asset lifecycle에 durable attachment + readback한다.
- Home에는 HERO/PRIMARY만 의미적으로 배치하고 모든 승인 asset을 복사하지 않는다.
- 이미지가 없으면 빈 공간을 채우기 위해 임의 생성하지 않는다.
- 이미지 블록 존재와 실제 픽셀 이해를 구분한다.
- Notion 배치 성공과 Godot/runtime 적용을 구분한다.

## Skill architecture

새 광역 Skill을 만들지 않는다. 기존 owner를 강화한다.

- intake/work contract: `managing-project-intake-and-work-contract`
- human design document lifecycle: `managing-design-documents`
- Project Home/Visual Map: `building-project-visual-dashboards`
- benchmark/SWOT/originality/player value: `analyzing-and-refining-game-concepts`
- adversarial loops: `running-adversarial-review-and-refinement`
- diff/runtime evidence: `reviewing-and-validating-project-changes`

## Migration strategy

- 기존 System Masters/Registry/Master DB를 삭제하지 않는다.
- 현재 Human Home을 별도 일반 페이지로 유지한다.
- AI metadata는 System surface에서 보존하고 Home에서 제거한다.
- 하위 사람용 페이지의 고유 기획/Visual/Flow/예산/핵심 데이터는 삭제하지 않고 Home 핵심 설명/anchor/view에 승격한다.
- 동일 데이터의 경쟁 정본을 만들지 않는다.
- 프로젝트별 고유 핵심을 먼저 읽고 Home을 맞춤 구성한다.

## Acceptance criteria

1. Base Home만 읽고 Base 작업 lifecycle·Skill 역할·사용자 수정 방법을 설명할 수 있다.
2. 각 Project Home만 읽고 핵심 가치·Flow·주요 시스템·핵심 데이터·Visual 방향·AI의 설계 이해·수정 방법·현재 상태를 설명할 수 있다.
3. raw PR/SHA/CI/Prompt/Hash/Implementation Path가 Human Home 기본 surface를 오염하지 않는다.
4. `AI가 이해한 설계 의도`와 `AI/System metadata`가 구분된다.
5. 실제 승인 Visual은 Notion에 전달/readback되고, 미존재 이미지를 승인 자산으로 가장하지 않는다.
6. 이미지 생성은 `TEXT_BRIEF_STOP_REQUIRED → NEXT_USER_EXPLICIT_APPROVAL → GENERATE_EXACTLY_ONE → STOP_REQUIRED` 계약을 따른다.
7. 프로젝트별 핵심 데이터가 Home에서 발견 가능하지만 repository/Master의 상세 owner와 경쟁하는 복제 정본을 만들지 않는다.
8. 기존 open/draft/ready PR은 read-only이며 current completed main에서 별도 변경을 수행한다.
9. 구현 후 전체 적대적 개선 루프 최소 5회와 exact-head/postmerge readback을 통과한다.
10. 추가 유료 서비스나 새 broad Skill 없이 현재 연결된 GitHub/Notion 경로로 동작한다.

## Rollback

- Base 변경은 squash merge revert로 되돌릴 수 있어야 한다.
- Notion은 기존 child page/Master/Registry를 삭제하지 않고 bounded edit만 수행한다.
- Notion 구조 교정 전 current content를 fetch하고, 실패 시 affected Home만 이전 문구로 복원할 수 있는 rollback note를 남긴다.
- Project structured/runtime canon은 이 정보구조 작업만으로 변경하지 않는다.
