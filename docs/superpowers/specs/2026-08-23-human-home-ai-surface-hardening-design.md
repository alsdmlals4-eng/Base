# Human Home / AI Surface Hardening Design

## Goal

Base와 모든 프로젝트의 Notion 첫 화면을 사람이 프로젝트 전체를 학습·이해·수정할 수 있는 풍부한 Human Home으로 고정하면서, PR·SHA·Prompt·Hash·CI 원시 로그·구현 경로 같은 AI/System 운영 메타데이터는 별도 System surface에만 유지한다.

## Problem

현행 Base는 이미 `DOMAIN_SPLIT_CANON`, `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`, `HUMAN_HOME_EXCLUDES_AI_SYSTEM_METADATA`, Project Registry/System Master 분리를 갖고 있다. 그러나 실제 Notion에서는 다음 drift가 남아 있다.

1. Base Home에 PR closure, exact SHA, CI gate, connector 내부 처리 같은 AI/운영 정보가 학습형 설명과 섞여 있다.
2. Project Home은 사람용으로 분리되어 있지만 핵심 시스템·예산·상대·Route·Flow·Visual 같은 이미 존재하는 프로젝트별 핵심 자료가 하위 drilldown에만 머물러 Home이 지나치게 얇다.
3. `AI가 이해한 설계 의도`와 `AI 작업 메타데이터`의 경계가 계약상 명확하지 않아 재혼재 가능성이 있다.
4. 이미지 정책은 Visual Requirement/approval/readback을 갖고 있지만, 사용자가 요구한 `전체 프로젝트 검토 → 텍스트 brief → 반드시 한 응답 종료 → 다음 사용자 승인 → 이미지 1장 생성 → 다시 종료`의 hard two-turn barrier가 테스트 가능한 계약으로 고정되지 않았다.
5. 중요 Base/프로젝트 작업의 사전 조사·대안·IRG·5회 full-loop 검토·사전 before/after/effect 보고가 여러 owner에 분산되어 있어 Project Home/Notion 작업에서 일부 단계가 쉽게 약화될 수 있다.

## Decision

`풍부한 Human Home + 기존 AI/System 상세 원본 재사용`을 채택한다.

- Human Home은 정보량을 임의로 줄이지 않는다. 사람이 프로젝트를 이해·비교·학습·수정하는 데 필요한 핵심 정보라면 Home에 직접 요약·시각화·대표 데이터로 노출한다.
- 하위 페이지와 Master DB는 상세 원본/drilldown을 유지한다. Home은 핵심 의미를 설명하되 긴 원시 로그나 전체 표를 복제해 제2 정본을 만들지 않는다.
- AI/System metadata는 `90 · SYSTEM MASTERS`, Project Registry, AI/System view, Production/Handoff, repository evidence에 유지한다.
- 새 광역 Skill이나 별도 dashboard/automation tool을 만들지 않는다. 기존 `building-project-visual-dashboards`, `managing-design-documents`, `managing-project-intake-and-work-contract`, `running-adversarial-review-and-refinement`, `reviewing-and-validating-project-changes`를 강화한다.

## Human Home contract

### Base Home

Base Home은 다음을 사람이 개발 지식이 적어도 순서대로 이해할 수 있게 직접 설명한다.

1. Base가 무엇인지와 Notion/GitHub 역할 분리
2. `조사 → 기획 → 독립 상세 검수 → Visual/Component 준비 → 구현 → release-near demo → 검증 → merge/readback` 전체 lifecycle
3. 단계별 `왜 필요한가 / 무엇을 입력으로 보는가 / 무엇을 출력하는가 / 실패하면 무엇이 생기는가`
4. 주요 Skill/Module의 호출 조건·입력·처리·출력·기대효과
5. `AI가 이해한 현재 운영 원리`를 사람이 검토할 수 있는 요약
6. 사용자가 잘못된 AI 이해를 어떻게 수정 요청하는지
7. 현재 검증 상태를 사람 수준으로 요약한 상태/NOT_RUN

PR 번호, raw SHA, CI run ID, exact closure receipt, connector transport detail은 Base Home의 기본 학습 본문에서 제외하고 AI/System/운영 drilldown으로 이동한다.

### Project Home

Project Home은 프로젝트별로 필요한 다음 정보를 직접 보여준다.

1. 프로젝트 한 줄 정의·장르·핵심 판타지·핵심 재미
2. 대표 승인 Visual이 실제로 있을 때만 Hero
3. 전체 Core Loop / 주요 Flow Map
4. 핵심 시스템별 `목적 → 플레이어 행동/질문 → 작동 → 결과/피드백 → 다른 시스템과 연결 → 기대되는 경험`
5. 프로젝트별 핵심 데이터 요약/시각화: 예산·경제·상대/몬스터·아이템·성장·Route/Map·로스터 등 해당 프로젝트에 실제로 중요한 것만 선택
6. Visual Bible / Asset / 주요 UI·화면·캐릭터·배경 등 승인 자료의 대표 anchor
7. `AI가 이해한 설계 의도`: 플레이어 경험과 선택 의미를 사람이 검토할 수 있는 자연어 요약
8. `사용자가 수정하는 방법`: 설명 수정 / 기획 규칙 수정 / 이미지 수정 / 구현 수정의 영향·승인·동기화 흐름
9. 현재 제작 상태: 완료 / 현재 / 다음 / NOT_RUN

모든 프로젝트에 동일 데이터 카테고리를 강제하지 않는다. 각 프로젝트를 먼저 읽고 해당 core/system/data/visual inventory를 만든 뒤 Home section을 선택한다.

## AI interpretation boundary

Human Home에 허용:

- `이 시스템의 핵심 재미는 무엇으로 이해했는가`
- `플레이어가 어떤 결정을 하도록 설계되었는가`
- `현재 AI가 보호해야 한다고 이해한 방향은 무엇인가`
- `사용자가 이 이해가 틀렸을 때 어떻게 수정하면 되는가`

Human Home에서 금지:

- PR/commit/raw SHA/CI run ID
- Prompt/AI Note/Hash/Asset ID/Record Key/Revision
- local path/port/executable
- implementation path/raw receipt/internal routing/debug

## Project work lifecycle

모든 L1 이상 Base/프로젝트 중요 작업에서 다음 사전 순서를 명시적으로 적용한다.

```text
CURRENT STATE RECOVERY
→ Base/project GitHub + exact Notion + decisions + Skill + PR + actual implementation/assets/tests
→ benchmark / professional practice / success-failure cases
→ >= 3 materially distinct viable alternatives
→ Implementation Reality Gate
→ expected BEFORE / AFTER / EFFECT / risk / rollback plan
→ at least 5 full adversarial improvement loops until clean
→ user approval
→ implementation in bounded slices
→ GitHub + Notion synchronization of approved results during work
→ validation + post-change 5+ full loops until clean
→ exact-head PR / merge
→ postmerge GitHub + Notion readback
```

작은 가역적 세부·밸런스 초기값은 승인된 방향 안에서 recommended default로 연속 실행하되, core/플레이어 경험/비용/범위/정본 충돌은 사용자 결정으로 올린다.

## Two-stage project production flow

### Phase 1 — planning / independent review / visual-component preparation

- 프로젝트 전체 GitHub·Notion·정본·실제 구현을 먼저 읽는다.
- 기획은 core/player promise를 고정한 뒤 진행한다.
- 검수는 독창성, 창의성, 일관성, SWOT, benchmark, 추가요소, 복잡도, 장기 제작성, Implementation Reality를 전체적으로 본다.
- 필요한 Flow/Component/Visual Need를 정한다.
- 승인된 결정/시각 결과는 작업 중 GitHub·Notion에 즉시 동기화하고 readback한다.

### Phase 2 — implementation / Loop Engineering / demo validation

- 검수 완료 범위만 구현한다.
- 가능하면 playable, shipping-intent에 가까운 release-near Vertical Slice까지 연결한다.
- 실제 runtime/player evidence와 문서/Notion 상태를 분리한다.

## Image hard barrier

프로젝트용 이미지 생성/편집은 다음 상태 머신을 따른다.

```text
PROJECT_REVIEW_COMPLETE
→ VISUAL_NEED_DEFINED
→ TEXT_BRIEF_COMPLETE
→ STOP_REQUIRED

[next user message]
→ EXPLICIT_IMAGE_APPROVAL
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED

[next user message]
→ APPROVE | REVISE | REJECT
```

- 동일 assistant 응답에서 `brief → generation`으로 넘어가지 않는다.
- 한 이미지 생성 응답에서 자동으로 후속 이미지 생성으로 이어가지 않는다.
- 실제 승인 후에만 Notion Visual Bible/Asset에 attach + readback하고, runtime 적용은 별도 repository evidence를 요구한다.

## Alternatives

### A. AI metadata만 이동

안전하지만 Human Home이 계속 핵심 자료를 drilldown에 숨겨 학습/복원 비용이 남는다. REJECT.

### B. 모든 상세 데이터를 Home으로 복사

정보량은 늘지만 중복·drift·정본 충돌이 커진다. REJECT.

### C. 풍부한 Human Home + 기존 상세 원본 재사용

Home은 핵심 의미·대표 데이터·시각 anchor를 직접 보여주고, 상세 원본은 기존 drilldown/Master/repository가 소유한다. ADOPT.

### D. 자동 Home generator / 별도 dashboard

현재 Notion MCP와 기존 정책으로 목적을 달성할 수 있어 추가 도구·비용·실패면이 불필요하다. DEFER.

## Acceptance criteria

1. Base policy/test가 Human Home의 풍부한 핵심 시스템·데이터·Visual·AI interpretation·수정방법을 요구한다.
2. Base Home의 기본 본문에서 AI/System metadata를 제외하도록 owner/Skill이 명시한다.
3. Project Home은 프로젝트별 core data/visual inventory를 요구하고 모든 게임에 같은 카테고리를 강제하지 않는다.
4. `AI가 이해한 설계 의도`와 operational metadata가 테스트 가능한 문구로 분리된다.
5. 이미지 two-turn hard barrier가 policy + test로 고정된다.
6. 기존 Master DB와 repository authority를 복제하지 않는다.
7. 새 광역 Skill/유료 자동화/제2 dashboard를 만들지 않는다.
8. 현재 open PR #618과 경로 충돌 없이 별도 branch/PR에서 변경한다.
9. 변경 후 exact-head CI, 최소 5회 full adversarial loop, merge, new-main readback을 수행한다.
10. GitHub merge 증거 뒤 Notion Base Home과 Project Homes를 bounded edit로 갱신하고 destination readback한다.

## Rollback

- Base: 해당 squash merge를 revert한다.
- Notion: 기존 child/detail/System Master는 삭제하지 않으며, Home 본문 변경만 previous fetched content를 기준으로 되돌릴 수 있게 bounded edit/readback한다.
- 이미지: 새 이미지 생성은 이 작업 범위에 포함하지 않는다.
