# Human Home Self-Contained Policy

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

`HUMAN_HOME_EXCLUDES_AI_SYSTEM_METADATA`

`PROJECT_REGISTRY_IS_SYSTEM_MASTER_NOT_HUMAN_HOME`

`HUMAN_HOME_PHYSICALLY_SEPARATE_FROM_REGISTRY_ROW`

`PROJECT_HOME_INFORMATION_RICHNESS_ALLOWED`

`PROJECT_SPECIFIC_CORE_DATA`

`AI_INTERPRETATION_FOR_USER_CORRECTION`

`AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED`

`HUMAN_EDIT_GUIDE_REQUIRED`

`HUMAN_HOME_PROGRESSIVE_DISCLOSURE`

`HOME_PROJECTION_IS_NOT_DUPLICATE_CANON`

`FULL_GAME_FLOW_VISIBLE_ON_HOME`

`CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME`

`PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME`

`HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING`

Notion의 Base Home과 Project Home은 링크 허브가 아니라 사람이 **추가 이동 없이 핵심을 이해하는 첫 화면**이다. GitHub/Repository의 structured/runtime truth를 복제해 새 정본을 만드는 것이 아니라, latest merged facts와 사용자 확정 방향을 사람이 읽기 쉬운 형태로 투영한다.

`PROJECT_HOME_INFORMATION_RICHNESS_ALLOWED`: Human Home의 문제는 정보량이 아니라 **책임이 다른 정보의 혼재**다. 사람이 프로젝트 전체를 이해·학습·비교·수정하는 데 직접 필요한 Flow, 핵심 시스템, 핵심 데이터, 승인 Visual, 중요한 결정 이유, 현재 상태는 Home에 충분히 많이 들어갈 수 있다. 페이지를 짧게 만들기 위해 핵심 이해를 하위 링크로 밀어내지 않는다.

`HUMAN_HOME_PROGRESSIVE_DISCLOSURE`는 다음 세 층을 기본으로 한다.

```text
30초: 프로젝트/작업의 전체 약속과 핵심 흐름
→ 5분: Full Game/Story Flow / CORE_SYSTEMS / SETTING / PROJECT_SPECIFIC_CORE_DATA / VISUAL_ASSET_ANCHORS / 현재 상태
→ drilldown: 전체 raw table·asset·reference·history·원시 evidence·구현 상세
```

`FULL_GAME_FLOW_VISIBLE_ON_HOME`: Home은 Core Loop 한 줄만 보여주고 전체 플레이 흐름을 하위 페이지로 밀어내지 않는다. 프로젝트에 맞는 **전체 session/run/story flow**를 직접 보여준다. encounter/core loop와 meta/progression loop가 모두 있으면 두 흐름이 어떻게 연결되는지도 Home에서 설명한다. 서사 프로젝트는 Part·사건·장면·독자 경험의 상위 흐름을 같은 역할로 사용한다.

`CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME`: 핵심 시스템의 이름만 나열하지 않고 목적·작동·상호작용·플레이어 판단을 Home에서 직접 설명한다. 세계/설정이 시스템의 의미를 결정한다면 플레이어 역할, 세계 전제, 핵심 갈등·목표도 함께 보인다. 설정 비중이 낮은 프로젝트는 `NOT_APPLICABLE_WITH_REASON`으로 이유를 적을 수 있지만, 필요한 설정을 단순히 상세 페이지로 숨길 수는 없다.

`PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME`: 프로젝트의 핵심을 이해·비교·수정하는 데 필요한 대표 값과 관계는 Home의 표 또는 project-filtered linked view로 직접 보인다. 전체 raw dataset과 machine schema는 L3/Database/Repository owner에 남긴다. Home을 짧게 만들기 위해 핵심 데이터 표 전체를 drilldown으로 이동하지 않는다.

`HOME_DETAIL_LINKS_CANNOT_REPLACE_CORE_UNDERSTANDING`: 하위 링크는 **더 자세히 보기**다. 사용자가 프로젝트의 전체 Flow, 핵심 시스템·설정, 핵심 데이터 관계를 처음 이해하기 위해 반드시 하위 페이지를 열어야 한다면 Human Home 계약 실패다.

`HOME_PROJECTION_IS_NOT_DUPLICATE_CANON`: Home에 사람용 설명·표·필터 View·Visual anchor를 보여주는 것은 repository/Master의 구조화 원본을 독립 복제하는 것이 아니다. 긴 원시 데이터나 machine-consumed 규칙을 Home에 두 번째 정본으로 재구현하지 않는다.

## Human Home / AI-System 물리 분리

`PROJECT REGISTRY · Master`와 같은 Project Registry는 프로젝트 identity·자동화 연결·동기화 상태를 유지하는 **AI/System Master**이며 사람용 Project Home으로 사용하지 않는다. 프로젝트 허브에서 사용자가 프로젝트를 선택했을 때 열리는 기본 진입점은 Registry row와 물리적으로 분리된 **전용 Human Project Home**이어야 한다.

Human Home의 본문과 기본 노출 속성에는 사람이 프로젝트를 이해하거나 판단하는 데 직접 필요하지 않은 machine/automation metadata를 두지 않는다. 다음 정보는 `90 · SYSTEM MASTERS`, Project Registry, `AI / System` view 또는 repository evidence로 분리한다.

- `Codex Home`, `Project Local Path`, `Godot Port`/WS Port, 전용 executable 같은 로컬 실행 연결값
- `Repo Main SHA`, `Record Key`, `Revision`, raw source hash와 같은 machine identity/sync 값
- `Prompt`, `AI Note`, `Asset ID`, `Hash`, `Implementation Path` 같은 AI/asset processing metadata
- raw CI run ID, 전체 PR/commit 로그, 자동화 receipt, 내부 routing/debug 정보
- raw PR/commit/CI history
- Prompt / AI Note / Asset ID / Hash / Implementation Path

`AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED`: 위 정보는 사용자에게 숨기는 비밀 데이터가 아니라 **기본 Human Home의 이해 목적과 책임이 다른 운영 데이터**다. 필요한 경우 AI/System·Production/Handoff drilldown에서 확인한다.

Human Home은 구현·동기화·검증 상태를 **사람이 판단할 수 있는 수준으로 요약**할 수 있다. 예를 들어 `Runtime NOT_RUN`, `현재 main과 동기화됨`, `Human playtest 미실행`은 허용하지만, 이를 설명하기 위해 원시 SHA·포트·로컬 경로·전체 CI 로그를 기본 화면에 노출하지 않는다. 사용자가 명시적으로 기술 evidence를 요청하면 분리된 AI/System 또는 Production/Handoff drilldown에서 확인한다.

Project Home이 database row인 경우에도 해당 row 자체가 AI/System 속성을 보유하면 Human Home으로 간주하지 않는다. 단순히 database view에서 열을 숨기는 것은 `HUMAN_HOME_PHYSICALLY_SEPARATE_FROM_REGISTRY_ROW`를 충족하지 않는다.

## AI가 이해한 설계 의도와 사용자 교정

`AI_INTERPRETATION_FOR_USER_CORRECTION`은 AI 작업 로그나 내부 chain-of-thought를 Home에 노출하는 규칙이 아니다. **현재 정본과 사용자 승인으로부터 AI가 이해한 프로젝트의 핵심 의도·우선순위·보호 요소를 사람이 검토 가능한 요약으로 표현**하는 계약이다.

예:

```text
AI가 이해한 핵심
→ 이 게임은 높은 수치보다 불완전한 정보를 이용한 의미 있는 선택이 중심이다.
→ 따라서 UI·밸런스·콘텐츠 변경에서 선택의 정보성·긴장감·결과 가독성을 먼저 보호한다.
```

사용자는 이 요약이 틀리면 바로 수정할 수 있어야 한다. AI는 교정된 내용을 새 사실로 독립 승격하지 않고 승인 Decision·repository/Notion owner에 동기화한다.

## 승인 시각자료 전달 Gate

`APPROVED_VISUAL_NOTION_DELIVERY_REQUIRED`

`APPROVAL_WITHOUT_NOTION_DELIVERY_IS_INCOMPLETE`

실제 이미지·목업·다이어그램·시각화가 생성 또는 편집되었고 사용자/프로젝트 authority가 프로젝트용으로 승인했다면, 승인 상태만 텍스트로 남기고 끝내지 않는다.

```text
actual visual exists
→ user/project approval
→ 해당 Project Visual Bible 또는 Project-filtered Asset record에 업로드/첨부
→ Approved 상태와 용도 기록
→ destination readback으로 파일/preview/Project/승인 상태 확인
→ 필요하면 Human Home에서 승인 visual anchor를 사람이 보기 쉽게 노출 또는 직접 연결
```

- `Visual Bible`은 사람이 보는 시각 방향·승인 reference의 기본 drilldown이다.
- `Asset`/Asset Library는 Preview·Approved·용도·재사용 상태를 구조적으로 추적한다.
- `Prompt`, `AI Note`, `Hash`, `Implementation Path` 등은 동일 자산의 `AI / System` 정보로 남기되 Human Home 기본 화면에는 노출하지 않는다.
- **텍스트로만 승인된 시각 방향**, 생성 전 image package, `READY_TO_GENERATE`, reference 후보는 실제 승인 이미지가 아니다. 사용자가 별도로 이미지 생성을 지시하지 않았다면 그림을 임의 생성하지 않으며, 존재하지 않는 이미지를 업로드 완료로 표시하지 않는다.
- 업로드 호출 성공만으로 완료하지 않는다. `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`의 attach + readback 계약을 따른다.

`VISUAL_ASSET_ANCHORS`: Home은 모든 승인 asset을 복사하는 archive가 아니다. 프로젝트/핵심 경험을 가장 빨리 이해시키는 HERO와 주요 시스템·캐릭터·세계·UI를 설명하는 PRIMARY 시각자료만 해당 설명 가까이에 배치한다. 나머지는 Visual Bible/Asset drilldown에서 보존한다.

## Base Home 필수 내용

- Base 목적과 Notion/GitHub authority split
- 전체 작업 lifecycle과 각 단계의 존재 이유
- 중요 규칙과 작동 조건
- active Skill별 **Skill 목적 / 호출 조건 / 입력 / 처리 / 출력 / 기대효과 / 연결 Module·consumer·Test**
- Module별 입력→판단/처리→출력→다음 consumer와 **없으면** 생기는 실패
- P01~P09 책임·대표 Skill/Module·진행 흐름·연결·기대효과·위험/revisit
- 사용자가 AI의 이해·설명·기획을 어떻게 교정하는지
- active surface와 retired/migration-only surface의 차이
- 현재 상태의 사람이 읽을 수 있는 PASS/PARTIAL/NOT_RUN/BLOCKED 구분

Base Home은 raw PR/SHA/CI/receipt history를 학습 흐름보다 먼저 보여주지 않는다. 완료된 사건의 **교훈과 현재 규칙**은 Home에 남길 수 있지만, exact SHA·run ID·closure receipt 전문은 관련 P01~P09/AI-System drilldown에 둔다.

## Project Home 필수 내용

`FLOW_MAP`

`CORE_SYSTEMS`

1. 프로젝트 한 줄 정의
2. 핵심 플레이어/사용자 가치
3. 현재 확정 방향과 보호/금지 요소
4. `FULL_GAME_FLOW_VISIBLE_ON_HOME`: 전체 session/run/story Flow와 Core Loop/주요 FLOW_MAP의 관계
5. `CORE_SYSTEMS_AND_SETTING_VISIBLE_ON_HOME`: CORE_SYSTEMS별 목적·작동·상호작용·플레이어 의미·기대효과 + 필요한 설정/플레이어 역할/핵심 갈등
6. `PROJECT_SPECIFIC_CORE_DATA_TABLES_VISIBLE_ON_HOME`: 사람이 비교·학습·수정해야 하는 프로젝트 고유 핵심 데이터의 대표 표/관계
7. UX/UI/Visual 방향·승인 상태와 `VISUAL_ASSET_ANCHORS`
8. `AI_INTERPRETATION_FOR_USER_CORRECTION`
9. `HUMAN_EDIT_GUIDE_REQUIRED`
10. 현재 구현상태와 Repository/runtime truth 연결
11. 검증상태와 static/runtime/device/human/accessibility/platform/store evidence ceiling
12. 현재 blocker / 다음 작업
13. 최근 중요한 결정과 이유
14. 주요 위험 / revisit condition
15. L2/L3 drilldown은 위 핵심 이해를 대체하지 않고 전체 raw detail/evidence를 제공

### PROJECT_SPECIFIC_CORE_DATA

프로젝트마다 실제 핵심 데이터가 다르므로 공통 필드 강제를 금지한다. 예:

- 제작/경영: 예산·경제·강화·내구·고객·생산 흐름
- 전투/전략: 상대·몬스터·병종·건물·확률·전선·기술·자원
- 퍼즐: 보드 규칙·목표·자원·콤보·스테이지 구조
- 힐링/탐험: 환경·발견·수집·기록·관계·세션 흐름
- 서사: 인물·세력·관계·장면·단서·타임라인·연속성

Home에는 사람이 이해하는 대표 값·관계·요약표를 보여주고, 전체 원시 데이터와 machine schema는 기존 owner를 유지한다.

## 사람이 수정하는 방법

`HUMAN_EDIT_GUIDE_REQUIRED`에 따라 Home은 최소 다음 세 종류를 쉽게 구분한다.

### 1. 설명/배치만 고치기

```text
사용자: "이 설명을 더 쉽게 바꿔줘"
→ human-facing 표현만 수정
→ Notion destination readback
```

구조화 규칙이나 runtime 동작이 바뀌지 않으면 repository 변경을 억지로 만들지 않는다.

### 2. 게임/프로젝트 규칙 바꾸기

```text
사용자 제안
→ 현재 정본·영향·PR·Notion 조사
→ 변경 전 / 변경 후 / 기대효과 / 위험 / 롤백 보고
→ 사용자 승인
→ repository structured canon 동기화
→ 필요한 Notion human surface 동기화 + readback
→ 구현/검증
```

### 3. 이미지 생성/수정하기

이미지 생성·편집은 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`가 존재하면 그 hard conversation barrier를 따른다. 해당 계약이 아직 활성 consumer에 연결되지 않은 상태에서는 기존 명시적 사용자 이미지 요청 Gate를 유지하고 자동 생성하지 않는다.

하위 페이지는 `drilldown`이다. 긴 표·전체 asset·reference·로그·세부 수치·evidence를 보관하되 Home의 핵심 설명을 '상세는 링크 참조'로 대체하지 않는다.
