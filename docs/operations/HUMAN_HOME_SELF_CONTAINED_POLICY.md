# Human Home Self-Contained Policy

`HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`

`HUMAN_HOME_EXCLUDES_AI_SYSTEM_METADATA`

`PROJECT_REGISTRY_IS_SYSTEM_MASTER_NOT_HUMAN_HOME`

`HUMAN_HOME_PHYSICALLY_SEPARATE_FROM_REGISTRY_ROW`

Notion의 Base Home과 Project Home은 링크 허브가 아니라 사람이 **추가 이동 없이 핵심을 이해하는 첫 화면**이다. GitHub/Repository의 structured/runtime truth를 복제해 새 정본을 만드는 것이 아니라, latest merged facts와 사용자 확정 방향을 사람이 읽기 쉬운 형태로 투영한다.

## Human Home / AI-System 물리 분리

`PROJECT REGISTRY · Master`와 같은 Project Registry는 프로젝트 identity·자동화 연결·동기화 상태를 유지하는 **AI/System Master**이며 사람용 Project Home으로 사용하지 않는다. 프로젝트 허브에서 사용자가 프로젝트를 선택했을 때 열리는 기본 진입점은 Registry row와 물리적으로 분리된 **전용 Human Project Home**이어야 한다.

Human Home의 본문과 기본 노출 속성에는 사람이 프로젝트를 이해하거나 판단하는 데 직접 필요하지 않은 machine/automation metadata를 두지 않는다. 다음 정보는 `90 · SYSTEM MASTERS`, Project Registry, `AI / System` view 또는 repository evidence로 분리한다.

- `Codex Home`, `Project Local Path`, `Godot Port`/WS Port, 전용 executable 같은 로컬 실행 연결값
- `Repo Main SHA`, `Record Key`, `Revision`, raw source hash와 같은 machine identity/sync 값
- `Prompt`, `AI Note`, `Asset ID`, `Hash`, `Implementation Path` 같은 AI/asset processing metadata
- raw CI run ID, 전체 PR/commit 로그, 자동화 receipt, 내부 routing/debug 정보

Human Home은 구현·동기화·검증 상태를 **사람이 판단할 수 있는 수준으로 요약**할 수 있다. 예를 들어 `Runtime NOT_RUN`, `현재 main과 동기화됨`, `Human playtest 미실행`은 허용하지만, 이를 설명하기 위해 원시 SHA·포트·로컬 경로·전체 CI 로그를 기본 화면에 노출하지 않는다. 사용자가 명시적으로 기술 evidence를 요청하면 분리된 AI/System 또는 Production/Handoff drilldown에서 확인한다.

Project Home이 database row인 경우에도 해당 row 자체가 AI/System 속성을 보유하면 Human Home으로 간주하지 않는다. 단순히 database view에서 열을 숨기는 것은 `HUMAN_HOME_PHYSICALLY_SEPARATE_FROM_REGISTRY_ROW`를 충족하지 않는다.

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

## Base Home 필수 내용

- Base 목적과 Notion/GitHub authority split
- 전체 작업 lifecycle과 각 단계의 존재 이유
- 중요 규칙과 작동 조건
- active Skill별 **Skill 목적 / 호출 조건 / 입력 / 처리 / 출력 / 기대효과 / 연결 Module·consumer·Test**
- Module별 입력→판단/처리→출력→다음 consumer와 **없으면** 생기는 실패
- P01~P09 책임·대표 Skill/Module·진행 흐름·연결·기대효과·위험/revisit
- current main, 완료/미완료 workstream, 실제 검증과 `NOT_RUN`

## Project Home 필수 내용

1. 프로젝트 한 줄 정의
2. 핵심 플레이어/사용자 가치
3. 현재 확정 방향과 보호/금지 요소
4. Core Loop / 주요 Flow
5. 핵심 시스템별 목적·작동·상호작용
6. UX/UI/Visual 방향·승인 상태
7. 현재 구현상태와 Repository/runtime truth 연결
8. 검증상태와 static/runtime/device/human/accessibility/platform/store evidence ceiling
9. 현재 blocker / 다음 작업
10. 최근 중요한 결정과 이유
11. 주요 위험 / revisit condition

하위 페이지는 `drilldown`이다. 긴 표·전체 asset·reference·로그·세부 수치·evidence를 보관하되 Home의 핵심 설명을 '상세는 링크 참조'로 대체하지 않는다.
