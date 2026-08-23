---
name: building-project-visual-dashboards
description: Use when a project needs a self-contained Notion Project Home or Visual Map that explains concepts, loops, systems, UX/visual state, evidence, risks, and next work without replacing repository truth.
---

# Building Project Visual Dashboards — Notion Project Home & Visual Map

`NOTION_PROJECT_HOME_AND_VISUAL_MAP`

`HUMAN_HOME_INFORMATION_RICHNESS_IS_ALLOWED`

`PROJECT_SPECIFIC_CORE_DATA_INVENTORY`

`AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW`

`HOW_TO_CORRECT_AI_UNDERSTANDING`

`DO_NOT_FORCE_UNIVERSAL_DATA_CATEGORIES`

## 목적

이 Skill은 사람이 프로젝트를 **추가 페이지 이동 없이 메인 Home 한 화면에서 이해**할 수 있도록 Notion의 human-facing Project Home과 Visual Map을 구성·갱신한다.

Repository Markdown/JSON/code/scene/resource/test/runtime evidence를 복제 정본으로 만들지 않는다. Notion은 사람이 이해·비교·학습하는 projection이고, structured/runtime truth는 Repository가 계속 소유한다.

Home은 짧을 필요가 없다. 사람이 프로젝트 전체 핵심을 이해하는 데 필요한 정보라면 Flow, 핵심 시스템, 대표 데이터, Visual/Asset, 현재 상태와 수정방법을 충분히 보여준다. 다만 상세 원시 표와 AI/System processing metadata를 복사해 competing canon을 만들지 않는다.

## 핵심 계약

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Project Home에는 최소 다음을 직접 설명한다.

- 프로젝트 한 줄 정의와 핵심 사용자/플레이어 가치
- 현재 확정 방향과 보호/금지 요소
- Core Loop / 주요 Flow
- 핵심 시스템별 목적·작동 방식·상호작용·기대효과
- `PROJECT_SPECIFIC_CORE_DATA_INVENTORY`에서 선정한 프로젝트 고유 대표 데이터/시각화
- UX/UI/Visual 방향과 승인 상태
- 실제 승인된 Visual/Asset anchor
- `AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW`: AI가 핵심 재미·플레이어 판단·보호 방향을 어떻게 이해했는지 사람용 설명
- `HOW_TO_CORRECT_AI_UNDERSTANDING`: 사용자가 설명·기획 규칙·이미지·구현을 어떤 순서로 수정 요청하면 되는지
- 현재 구현상태와 repository/runtime truth 연결
- 검증상태와 evidence ceiling
- blocker / 다음 작업
- 최근 중요한 결정과 선택 이유
- 주요 위험과 revisit condition

`DO_NOT_FORCE_UNIVERSAL_DATA_CATEGORIES`: 예산, 경제, 상대, 몬스터, 아이템, 성장, Route/Map, 로스터 같은 항목은 예시다. 모든 프로젝트에 같은 섹션을 강제하지 않고, 해당 프로젝트의 core와 실제 상세 owner를 먼저 읽은 뒤 플레이어 판단과 프로젝트 이해에 중요한 항목만 선택한다.

하위 페이지는 긴 표, 전체 asset 목록, 상세 evidence, history, Source를 위한 drilldown이다. Home 핵심 이해를 “링크 참조”로 대체하지 않는다. 반대로 Home을 rich하게 만든다는 이유로 하위 owner의 전체 내용을 그대로 복사하지 않는다.

## Skill Modes

- `frame-project-home`: exact Project identity, latest confirmed decisions, GitHub main, existing Notion Home과 현재 blocker를 읽어 이번 Home의 범위와 보호 대상을 고정하고 `PROJECT_SPECIFIC_CORE_DATA_INVENTORY`를 만든다.
- `map-canonical-sources`: core direction·loop·systems·project-specific data·UX/Visual·implementation·evidence의 repository/runtime owner와 human-facing projection을 연결한다.
- `build-project-home`: 핵심 이해가 자체 완결된 Notion Project Home을 구성·갱신한다. 대표 데이터/시각 자료와 `AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW`, `HOW_TO_CORRECT_AI_UNDERSTANDING`을 사람 수준으로 배치하고 관계 설명에 실질적으로 필요할 때만 Visual Map/diagram을 추가한다.
- `bind-evidence-status`: 구현·검증·위험·다음 작업을 owner locator와 연결하고 `PASS / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED`를 분리한다.
- `verify-destination-readback`: write 뒤 exact Project destination을 다시 읽어 project 혼입, stale·duplicate 정보, evidence overclaim, raw AI/System metadata 누출과 drilldown-only 핵심 누락을 검사한다.

## 진행 흐름

```text
Project identity / latest user decisions
→ latest GitHub main + same-goal PR read-only reconciliation + Project Notion readback
→ core direction / loop / systems / project-specific data / UX / visual / implementation / evidence 복원
→ PROJECT_SPECIFIC_CORE_DATA_INVENTORY
→ 사람이 알아야 할 정보 계층 설계
→ Home 본문에 자체 완결 설명 작성
→ 필요 시 Visual Map / image / diagram 배치
→ AI design interpretation + correction guide
→ structured/runtime locator 연결
→ destination readback
→ stale/duplicate/AI-metadata-leak/overclaim 검토
```

## 입력

- exact Project identity
- latest confirmed decisions
- Project GitHub main / canonical owners
- same-goal open/recent PR read-only state
- actual implementation/runtime evidence
- Project Notion existing Home/detail pages
- project-specific budget/economy/enemy/monster/item/growth/Route/roster/system data when applicable
- approved visual/reference inputs
- current blockers / next work / revisit conditions

## 출력

- information-rich, self-contained Notion Project Home
- project-specific core data/visual inventory and representative human projection
- 필요한 Visual Map/diagram
- `AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW`
- `HOW_TO_CORRECT_AI_UNDERSTANDING`
- 상세 하위 페이지로 가는 drilldown link
- repository/runtime evidence locator
- `PASS / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED`를 구분한 검증 상태

## Human / AI boundary

Human Home에서 허용:

- "이 시스템의 핵심 재미를 AI가 무엇으로 이해했는가"
- "플레이어가 어떤 결정을 하도록 설계됐다고 이해했는가"
- "현재 보호해야 할 방향은 무엇인가"
- "틀렸다면 무엇을 어떻게 수정 요청하면 되는가"

Human Home 기본 화면에서 금지:

- PR/commit/raw SHA/CI run ID
- Prompt/AI Note/Hash/Asset ID/Record Key/Revision
- local path/port/executable/implementation path
- raw receipt/internal routing/debug

기술 evidence가 필요하면 AI/System 또는 Production/Handoff drilldown으로 연결한다.

## 기대효과

- 사용자가 프로젝트를 다시 읽을 때 여러 하위 페이지를 찾아다니는 비용 감소
- Core Loop뿐 아니라 실제 핵심 시스템·대표 데이터·Visual까지 Home에서 함께 이해
- AI가 프로젝트를 재개할 때 human-facing 방향과 repository truth를 함께 복원하기 쉬움
- 사용자가 AI의 잘못된 이해를 Home에서 발견하고 정확한 수정 경로로 교정 가능
- 링크 허브만 남아 핵심 방향이 숨는 문제 감소

## standalone HTML / local dashboard 금지

다음은 현행 기본 경로가 아니다.

- standalone HTML/CSS/JavaScript project dashboard 생성
- 별도 localhost project-management UI 생성
- HTML dashboard 상태를 current implementation truth로 사용
- Notion/Repository 정보를 HTML에 다시 복사해 제3의 정본 생성

과거 HTML dashboard의 UNIQUE 자료가 있으면 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`에 따라 현행 Notion/Repository owner로 흡수한다.

## 검증

- Home만 읽어도 핵심 방향·흐름·시스템·프로젝트 고유 대표 데이터·Visual·상태·다음 작업을 설명할 수 있는가
- 프로젝트에 실제로 없는 범용 카테고리를 억지로 추가하지 않았는가
- `AI_DESIGN_INTERPRETATION_FOR_HUMAN_REVIEW`가 작업 로그가 아니라 사람이 검토 가능한 설계 해석인가
- `HOW_TO_CORRECT_AI_UNDERSTANDING`이 설명/기획/시각/구현 변경 경로를 구분하는가
- Notion 주장과 repository/runtime evidence가 충돌하지 않는가
- 실제 미실행 검증이 PASS로 표시되지 않았는가
- 다른 프로젝트 정보가 섞이지 않았는가
- 핵심 정보를 하위 링크로만 밀어내지 않았는가
- raw AI/System metadata가 Human Home에 유출되지 않았는가
- write 뒤 exact Project destination을 readback했는가

## Reference

기존 human-facing 정보 계층 원리는 `skills/building-project-visual-dashboards/references/dashboard-information-architecture.md`를 참고하되, standalone HTML 탭 구현이 아니라 Notion Home/Visual Map에 맞게 적용한다.

## Output contract

최소 출력은 information-rich self-contained Project Home, 프로젝트 고유 핵심 데이터/Visual의 대표 projection, 필요한 Visual Map/diagram, AI design interpretation, correction guide, repository/runtime locator, 검증 상태, blocker·next work·revisit condition이다. 핵심 이해를 하위 링크로만 넘기지 않는다.

## Quality gate

Home만 읽어 프로젝트 핵심 가치·Core Loop·주요 시스템·프로젝트 고유 대표 데이터·UX/Visual·AI가 이해한 설계 의도·수정 경로·구현/검증 상태·다음 작업을 설명할 수 있어야 한다. Notion과 repository/runtime truth가 충돌하거나 미실행 검증을 PASS로 표시하거나 AI/System metadata가 Home에 섞이거나 standalone HTML/local dashboard가 새 authority로 부활하면 실패다.

Learning Log: `skills/building-project-visual-dashboards/LEARNING_LOG.md`
