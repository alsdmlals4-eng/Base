---
name: building-project-visual-dashboards
description: Use when a project needs a self-contained Notion Project Home or Visual Map that explains concepts, loops, systems, project-specific core data, UX/visual state, evidence, risks, next work, and user correction paths without replacing repository truth.
---

# Building Project Visual Dashboards — Notion Project Home & Visual Map

`NOTION_PROJECT_HOME_AND_VISUAL_MAP`

`PROJECT_SPECIFIC_CORE_DATA`

`AI_INTERPRETATION_FOR_USER_CORRECTION`

`HUMAN_EDIT_GUIDE_REQUIRED`

`NO_UNIVERSAL_GAME_DATA_TEMPLATE`

## 목적

이 Skill은 사람이 프로젝트를 **추가 페이지 이동 없이 메인 Home 한 화면에서 이해**할 수 있도록 Notion의 human-facing Project Home과 Visual Map을 구성·갱신한다.

Repository Markdown/JSON/code/scene/resource/test/runtime evidence를 복제 정본으로 만들지 않는다. Notion은 사람이 이해·비교·학습하는 projection이고, structured/runtime truth는 Repository가 계속 소유한다.

Home은 짧은 요약 페이지가 아니다. 사람에게 필요한 정보라면 Flow·핵심 시스템·프로젝트 고유 핵심 데이터·승인 Visual·중요 결정 이유·AI가 이해한 설계 의도·수정 방법까지 충분히 포함한다. 정보량이 아니라 **사람용 이해 정보와 AI/System 운영 정보의 책임 분리**를 품질 기준으로 사용한다.

## 핵심 계약

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Project Home에는 최소 다음을 직접 설명한다.

- 프로젝트 한 줄 정의와 핵심 사용자/플레이어 가치
- 현재 확정 방향과 보호/금지 요소
- Core Loop / 주요 Flow
- 핵심 시스템별 목적·작동 방식·상호작용·플레이어 의미·기대효과
- `PROJECT_SPECIFIC_CORE_DATA`
- UX/UI/Visual 방향과 승인 상태
- 사람이 이해하는 핵심 Visual anchor
- `AI_INTERPRETATION_FOR_USER_CORRECTION`
- `HUMAN_EDIT_GUIDE_REQUIRED`
- 현재 구현상태와 repository/runtime truth 연결
- 검증상태와 evidence ceiling
- blocker / 다음 작업
- 최근 중요한 결정과 선택 이유
- 주요 위험과 revisit condition

하위 페이지는 긴 표, 전체 asset 목록, 상세 evidence, history, Source를 위한 drilldown이다. Home 핵심 이해를 “링크 참조”로 대체하지 않는다.

### PROJECT_SPECIFIC_CORE_DATA

Home을 만들기 전에 해당 프로젝트의 사람이 실제로 비교·학습·수정해야 하는 핵심 데이터를 먼저 찾는다.

예:

```text
Blacksmith
→ 강화 / 내구 / 파괴 / 경제 / 고객 / 작품 생애

Ten Paces
→ 3/3/4 / 상대 / 무공 / 기술 예산 / Route / 전장

Omenward
→ 전선 / Forecast / 징조륜 / 확률 / 병력 / Stage

Ninja Survival
→ 백팩 / 아이템 / 회전 / 인접 / 유파 / 조합

COC-Fiction
→ 인물 / 세력 / 관계 / 장면 / 단서 / 연속성
```

`NO_UNIVERSAL_GAME_DATA_TEMPLATE`: 모든 게임에 몬스터·경제·아이템·성장 같은 동일 섹션을 강제하지 않는다. 핵심이 아닌 항목은 Home completeness를 위해 만들지 않는다.

### AI_INTERPRETATION_FOR_USER_CORRECTION

AI가 현재 정본과 승인 Decision에서 이해한 **설계 의도·우선순위·보호 요소**를 사람이 확인할 수 있는 짧은 설명으로 보여준다.

허용:

```text
AI가 이해한 핵심
→ 플레이어는 공격력보다 불완전한 정보를 읽고 의미 있는 선택을 하는 재미를 느껴야 한다.
```

금지:

```text
Prompt / AI Note / Hash / Implementation Path / raw PR / raw CI / internal routing
```

이 섹션은 작업 로그가 아니라 사용자가 “AI가 내 의도를 잘 이해했는가?”를 빠르게 교정하기 위한 human-facing projection이다.

### HUMAN_EDIT_GUIDE_REQUIRED

Home에는 중학생도 따라갈 수 있는 수정 경로를 둔다.

```text
설명/배치만 수정
→ Notion human expression update + readback

게임 규칙/기획 수정
→ 영향 조사 → 변경 전/후/기대효과 → 사용자 승인
→ repository structured canon sync
→ Notion human surface sync/readback → 구현/검증

이미지 수정/생성
→ 현재 프로젝트 Visual canon과 사용자 이미지 Gate를 먼저 확인
```

## Skill Modes

- `frame-project-home`: exact Project identity, latest confirmed decisions, GitHub main, existing Notion Home, 관련 Flow/System/Visual/사람용 표와 현재 blocker를 읽어 이번 Home의 범위와 보호 대상을 고정한다.
- `map-canonical-sources`: core direction·loop·systems·project-specific core data·UX/Visual·implementation·evidence의 repository/Master owner와 human-facing projection을 연결한다.
- `build-project-home`: 핵심 이해가 자체 완결된 Notion Project Home을 구성·갱신한다. `30초 전체 그림 → 5분 핵심 Flow/System/Data/Visual → drilldown` 순서로 배치하고 관계 설명에 실질적으로 필요할 때만 Visual Map/diagram을 추가한다.
- `bind-evidence-status`: 구현·검증·위험·다음 작업을 owner locator와 연결하고 `PASS / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED`를 분리한다.
- `verify-destination-readback`: write 뒤 exact Project destination을 다시 읽어 project 혼입, stale·duplicate 정보, evidence overclaim, AI/System metadata 노출과 drilldown-only 핵심 누락을 검사한다.

## 진행 흐름

```text
Project identity / latest user decisions
→ latest GitHub main + Project Notion readback
→ Home + core Flow/System/Visual/data drilldown 복원
→ PROJECT_SPECIFIC_CORE_DATA inventory
→ 사람이 알아야 할 정보 계층 설계
→ Home 본문에 자체 완결 설명 작성
→ 필요한 Visual Map / approved visual anchor 배치
→ AI_INTERPRETATION_FOR_USER_CORRECTION
→ HUMAN_EDIT_GUIDE_REQUIRED
→ structured/runtime owner locator 연결
→ destination readback
→ stale/duplicate/overclaim/AI-metadata 검토
```

## 입력

- exact Project identity
- latest confirmed decisions
- Project GitHub main / canonical owners
- actual implementation/runtime evidence
- Project Notion existing Home/detail pages
- relevant Flow/System/core-data human surfaces
- approved visual/reference inputs
- current blockers / next work / revisit conditions

## 출력

- self-contained, information-rich Notion Project Home
- 필요한 Visual Map/diagram과 승인 Visual anchor
- 프로젝트 고유 핵심 데이터의 사람용 설명/표/view
- AI가 이해한 설계 의도의 교정 가능한 요약
- 사용자 수정 방법
- 상세 하위 페이지로 가는 drilldown link
- repository/runtime evidence locator
- `PASS / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED`를 구분한 검증 상태

## 기대효과

- 사용자가 프로젝트를 다시 읽을 때 여러 하위 페이지를 찾아다니는 비용 감소
- Home만으로 “무슨 프로젝트인지 → 어떻게 진행되는지 → 어떤 시스템/데이터로 움직이는지” 학습 가능
- AI가 프로젝트 의도를 잘못 이해했을 때 사용자가 즉시 교정 가능
- Skill/Module/시스템의 목적과 연결관계를 빠르게 학습
- AI가 프로젝트를 재개할 때 human-facing 방향과 repository truth를 함께 복원하기 쉬움
- 링크 허브만 남아 핵심 방향·데이터가 숨는 문제 감소

## standalone HTML / local dashboard 금지

다음은 현행 기본 경로가 아니다.

- standalone HTML/CSS/JavaScript project dashboard 생성
- 별도 localhost project-management UI 생성
- HTML dashboard 상태를 current implementation truth로 사용
- Notion/Repository 정보를 HTML에 다시 복사해 제3의 정본 생성

과거 HTML dashboard의 UNIQUE 자료가 있으면 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`에 따라 현행 Notion/Repository owner로 흡수한다.

## 검증

- Home만 읽어도 핵심 방향·흐름·시스템·프로젝트 고유 핵심 데이터·Visual·상태·다음 작업을 설명할 수 있는가
- Home이 짧아 보이기 위해 핵심 표/Flow/System 이해를 링크로만 밀어내지 않았는가
- AI interpretation이 human-facing 설계 의도이며 raw 운영 metadata가 아닌가
- 사용자가 설명/기획/이미지 수정 경로의 차이를 이해할 수 있는가
- Notion 주장과 repository/runtime evidence가 충돌하지 않는가
- 실제 미실행 검증이 PASS로 표시되지 않았는가
- 다른 프로젝트 정보가 섞이지 않았는가
- 프로젝트에 없는 시스템/데이터 섹션을 템플릿 때문에 발명하지 않았는가
- write 뒤 exact Project destination을 readback했는가

## Reference

기존 human-facing 정보 계층 원리는 `skills/building-project-visual-dashboards/references/dashboard-information-architecture.md`를 참고하되, standalone HTML 탭 구현이 아니라 Notion Home/Visual Map에 맞게 적용한다.

상위 Human Home 내용/AI-System 분리 계약은 `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`가 소유한다.

## Output contract

최소 출력은 self-contained Project Home, 프로젝트 고유 core-data 설명, 필요한 Visual Map/diagram, AI interpretation, 사용자 edit guide, repository/runtime locator, 검증 상태, blocker·next work·revisit condition이다. 핵심 이해를 하위 링크로만 넘기지 않는다.

## Quality gate

Home만 읽어 프로젝트 핵심 가치·Core Loop·주요 시스템·프로젝트 고유 핵심 데이터·UX/Visual·AI가 이해한 설계 의도·수정 방법·구현/검증 상태·다음 작업을 설명할 수 있어야 한다. Notion과 repository/runtime truth가 충돌하거나 미실행 검증을 PASS로 표시하거나 raw AI/System metadata가 Home을 오염하거나 standalone HTML/local dashboard가 새 authority로 부활하면 실패다.

Learning Log: `skills/building-project-visual-dashboards/LEARNING_LOG.md`
