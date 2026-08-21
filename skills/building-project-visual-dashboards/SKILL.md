---
name: building-project-visual-dashboards
description: Use when a project needs a self-contained Notion Project Home or Visual Map that explains concepts, loops, systems, UX/visual state, evidence, risks, and next work without replacing repository truth.
---

# Building Project Visual Dashboards — Notion Project Home & Visual Map

`NOTION_PROJECT_HOME_AND_VISUAL_MAP`

## 목적

이 Skill은 사람이 프로젝트를 **추가 페이지 이동 없이 메인 Home 한 화면에서 이해**할 수 있도록 Notion의 human-facing Project Home과 Visual Map을 구성·갱신한다.

Repository Markdown/JSON/code/scene/resource/test/runtime evidence를 복제 정본으로 만들지 않는다. Notion은 사람이 이해·비교·학습하는 projection이고, structured/runtime truth는 Repository가 계속 소유한다.

## 핵심 계약

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

Project Home에는 최소 다음을 직접 설명한다.

- 프로젝트 한 줄 정의와 핵심 사용자/플레이어 가치
- 현재 확정 방향과 보호/금지 요소
- Core Loop / 주요 Flow
- 핵심 시스템별 목적·작동 방식·상호작용·기대효과
- UX/UI/Visual 방향과 승인 상태
- 현재 구현상태와 repository/runtime truth 연결
- 검증상태와 evidence ceiling
- blocker / 다음 작업
- 최근 중요한 결정과 선택 이유
- 주요 위험과 revisit condition

하위 페이지는 긴 표, 전체 asset 목록, 상세 evidence, history, Source를 위한 drilldown이다. Home 핵심 이해를 “링크 참조”로 대체하지 않는다.

## Skill Modes

- `frame-project-home`: exact Project identity, latest confirmed decisions, GitHub main, existing Notion Home과 현재 blocker를 읽어 이번 Home의 범위와 보호 대상을 고정한다.
- `map-canonical-sources`: core direction·loop·systems·UX/Visual·implementation·evidence의 repository/runtime owner와 human-facing projection을 연결한다.
- `build-project-home`: 핵심 이해가 자체 완결된 Notion Project Home을 구성·갱신하고 관계 설명에 실질적으로 필요할 때만 Visual Map/diagram을 추가한다.
- `bind-evidence-status`: 구현·검증·위험·다음 작업을 owner locator와 연결하고 `PASS / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED`를 분리한다.
- `verify-destination-readback`: write 뒤 exact Project destination을 다시 읽어 project 혼입, stale·duplicate 정보, evidence overclaim과 drilldown-only 핵심 누락을 검사한다.

## 진행 흐름

```text
Project identity / latest user decisions
→ latest GitHub main + Project Notion readback
→ core direction / loop / systems / UX / visual / implementation / evidence 복원
→ 사람이 알아야 할 정보 계층 설계
→ Home 본문에 자체 완결 설명 작성
→ 필요 시 Visual Map / image / diagram 배치
→ structured/runtime locator 연결
→ destination readback
→ stale/duplicate/overclaim 검토
```

## 입력

- exact Project identity
- latest confirmed decisions
- Project GitHub main / canonical owners
- actual implementation/runtime evidence
- Project Notion existing Home/detail pages
- approved visual/reference inputs
- current blockers / next work / revisit conditions

## 출력

- self-contained Notion Project Home
- 필요한 Visual Map/diagram
- 상세 하위 페이지로 가는 drilldown link
- repository/runtime evidence locator
- `PASS / PARTIAL / NOT_RUN / BLOCKED_UNVERIFIED`를 구분한 검증 상태

## 기대효과

- 사용자가 프로젝트를 다시 읽을 때 여러 하위 페이지를 찾아다니는 비용 감소
- Skill/Module/시스템의 목적과 연결관계를 빠르게 학습
- AI가 프로젝트를 재개할 때 human-facing 방향과 repository truth를 함께 복원하기 쉬움
- 링크 허브만 남아 핵심 방향이 숨는 문제 감소

## standalone HTML / local dashboard 금지

다음은 현행 기본 경로가 아니다.

- standalone HTML/CSS/JavaScript project dashboard 생성
- 별도 localhost project-management UI 생성
- HTML dashboard 상태를 current implementation truth로 사용
- Notion/Repository 정보를 HTML에 다시 복사해 제3의 정본 생성

과거 HTML dashboard의 UNIQUE 자료가 있으면 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`에 따라 현행 Notion/Repository owner로 흡수한다.

## 검증

- Home만 읽어도 핵심 방향·흐름·시스템·Visual·상태·다음 작업을 설명할 수 있는가
- Notion 주장과 repository/runtime evidence가 충돌하지 않는가
- 실제 미실행 검증이 PASS로 표시되지 않았는가
- 다른 프로젝트 정보가 섞이지 않았는가
- 핵심 정보를 하위 링크로만 밀어내지 않았는가
- write 뒤 exact Project destination을 readback했는가

## Reference

기존 human-facing 정보 계층 원리는 `skills/building-project-visual-dashboards/references/dashboard-information-architecture.md`를 참고하되, standalone HTML 탭 구현이 아니라 Notion Home/Visual Map에 맞게 적용한다.

## Output contract

최소 출력은 self-contained Project Home, 필요한 Visual Map/diagram, repository/runtime locator, 검증 상태, blocker·next work·revisit condition이다. 핵심 이해를 하위 링크로만 넘기지 않는다.

## Quality gate

Home만 읽어 프로젝트 핵심 가치·Core Loop·주요 시스템·UX/Visual·구현/검증 상태·다음 작업을 설명할 수 있어야 한다. Notion과 repository/runtime truth가 충돌하거나 미실행 검증을 PASS로 표시하거나 standalone HTML/local dashboard가 새 authority로 부활하면 실패다.

Learning Log: `skills/building-project-visual-dashboards/LEARNING_LOG.md`
