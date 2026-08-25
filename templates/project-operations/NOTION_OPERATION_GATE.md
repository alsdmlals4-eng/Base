# Project Notion Operation Gate

이 문서는 Base를 채택한 프로젝트에서 **Notion을 실제로 읽고 수정할 때의 공용 실행 계약**이다. Notion 제품 기능의 전체 설명서가 아니며, 프로젝트 기획 정본·Human Home 정책·Visual workflow·repository runtime truth를 대체하지 않는다.

상위 제품 동작 참조는 `docs/knowledge/methods/NOTION_OFFICIAL_PRODUCT_OPERATING_REFERENCE.md`다. 이 문서는 그 공식 제품 동작을 프로젝트 실행 규칙으로 좁혀 적용하며, 제품 기능 자체의 의미·제약이 바뀌면 상위 참조를 먼저 확인한다.

```text
NOTION_OPERATION_GATE
!= NOTION_PRODUCT_REFERENCE
!= PROJECT_GAME_DESIGN_CANON
!= REPOSITORY_RUNTIME_TRUTH
```

## 1. Authority boundary

- 사람용 프로젝트 개요·기획·시각 자료·사람이 수정하는 표/Flow는 `NOTION_HUMAN_FACING_CANON`을 따른다.
- Markdown/JSON/game data/code/scene/resource/test와 실제 build/runtime evidence는 `REPOSITORY_STRUCTURED_CANON` / `REPOSITORY_RUNTIME_TRUTH`를 따른다.
- raw ID, schema, Record Key, revision, prompt, hash, automation metadata 같은 AI/System 정보는 사람용 Home 기본 콘텐츠로 복제하지 않는다.
- Notion 변경이 structured/runtime 의미를 바꾸면 repository owner에 동기화하기 전 구현·runtime 완료를 주장하지 않는다.

## 2. Object scope before write

지속 변경 전 다음 중 실제 영향 범위를 판정한다.

```text
PAGE_BLOCK
DATABASE_RECORD
VIEW_PRESENTATION
DATA_SOURCE_SCHEMA_OR_RECORD
DATABASE_GLOBAL_LAYOUT
FILE_UPLOAD
AUTOMATION_OR_WEBHOOK
```

핵심 구분:

```text
VIEW_PRESENTATION != SOURCE_MUTATION
SINGLE_RECORD_EDIT != DATABASE_GLOBAL_LAYOUT
UPLOAD_SUCCESS != DESTINATION_ATTACHMENT_SUCCESS
NOTION_READBACK != CLIENT_GEOMETRY_OR_RUNTIME_PASS
```

## 3. Bounded mutation protocol

```text
정확한 Project / destination 확인
→ current destination fetch/read
→ database/data source면 schema와 정확한 property 이름 확인
→ object scope와 Project relation 확인
→ smallest bounded edit
→ write
→ destination readback
→ source mutation이면 source readback
→ structured/runtime 의미 변경이면 repository owner 동기화
```

규칙:

- targeted update/insert가 가능하면 전체 page `replace_content`를 기본값으로 사용하지 않는다.
- child page/database 삭제 가능성이 있는 `allow_deleting_content=true`를 자동 사용하지 않는다. 영향을 받는 child 목록을 확인하고 사용자 확인을 받은 경우에만 의도적 삭제를 진행한다.
- linked view의 filter/sort/group/card 표현 변경과 source record/property/schema 변경을 구분한다.
- database-global layout은 단일 record polish 요청으로 변경하지 않는다. 실제 database family 전체 변경이 의도된 경우에만 영향 범위를 확인하고 진행한다.
- write invocation만으로 성공을 주장하지 않는다. 의도한 필드·Project relation·배치가 남았는지 destination readback을 요구한다.
- connector/API persistence는 desktop/mobile 화면 geometry, 첨부 렌더링, 게임 runtime PASS를 증명하지 않는다. 검증하지 못한 층은 `NOT_RUN`, `BLOCKED_UNVERIFIED` 또는 해당 evidence ceiling으로 남긴다.

## 4. Database and data source

- database를 수정하기 전에 현재 database와 연결된 data source를 식별한다.
- database record property 수정/생성 시 현재 data source schema에서 정확한 property 이름과 type을 확인한다.
- source를 공유하는 linked view를 프로젝트별 presentation 용도로 사용할 수 있지만, 표현 차이를 만들기 위해 canonical record를 복제하지 않는다.
- source mutation이면 정확한 Project relation과 해당 source의 authority를 먼저 확인한다.

## 5. Automation and webhook routing

기능명보다 **데이터 흐름 방향**으로 구분한다.

- **Webhook action**: Notion Button 또는 Database automation에서 외부 endpoint로 요청을 보내는 outbound action.
- **Integration webhook**: 외부 integration이 Notion content change event를 받아 처리하는 developer/event-listener route.
- **Database automation**: Notion 내부 trigger/condition에 따라 action을 실행하는 route.

안전 규칙:

- Database automation이 만든 변경이 다른 Database automation을 계속 실행시키는 자동 연쇄를 전제로 workflow를 설계하지 않는다.
- 사용자가 직접 누른 Button처럼 explicit user action이 별도 automation trigger가 될 수 있는지는 현재 제품 동작을 확인한다.
- webhook payload에 API key, password, access token 같은 `secret`을 직접 넣지 않는다. 인증 secret은 수신 측의 안전한 secret storage/verification 경로로 분리한다.
- Notion UI에 기능이 있다는 사실과 현재 GPT/Notion 연결 도구가 그 기능을 실제 생성·수정·검증할 수 있다는 사실을 구분한다.
- 현재 도구가 지원하지 않는 UI-only 설정은 `MANUAL_CONFIGURATION_REQUIRED` 또는 동등한 미검증 상태로 남기며 자동화 완료라고 주장하지 않는다.

## 6. Cost and dependency boundary

- Base/프로젝트 기본 workflow는 `ZERO_INCREMENTAL_COST`를 유지한다.
- paid-only Database automation, Dashboard, Agent 또는 기타 Notion 기능을 기본 필수 dependency로 만들지 않는다.
- 무료·현재 연결 도구·repository-native 경로가 요구를 충족하면 그 경로를 우선한다.
- 유료 기능은 명시적 필요와 비용 대비 장기 가치가 확인된 경우에만 별도 결정 대상으로 올린다.

## 7. Human Home boundary

사람용 Home에는 다음 결과를 우선한다.

- 프로젝트 정의와 플레이어 가치
- 핵심 Flow / Core Loop / 핵심 시스템
- 사람이 판단해야 하는 핵심 데이터 표
- 승인된 시각 자료와 설명
- 현재 구현 상태의 사람이 이해할 수 있는 요약
- blocker / 다음 작업 / 중요한 결정

다음은 기본적으로 AI/System 작업면이나 repository evidence에 둔다.

- raw page/data-source IDs
- schema mapping / Record Key / revision
- prompt / automation payload / webhook debugging data
- raw SHA / CI receipt / local path / port
- 구현 세부와 runtime 증거 원본

## 8. Definition of Done

Notion 변경 완료를 주장하려면 최소 다음을 확인한다.

- [ ] 정확한 Project와 destination을 식별했다.
- [ ] object scope를 분류했다.
- [ ] database/data source 변경이면 current schema를 읽었다.
- [ ] smallest bounded edit을 사용했다.
- [ ] 의도하지 않은 child 삭제나 global layout 변경이 없다.
- [ ] destination readback을 수행했다.
- [ ] source mutation이면 source readback을 수행했다.
- [ ] structured/runtime 의미가 바뀌면 repository owner와 동기화했다.
- [ ] Human Home에 AI/System 메타데이터를 새로 노출하지 않았다.
- [ ] connector/API evidence보다 높은 UI/runtime PASS를 과장하지 않았다.
- [ ] 자동화/webhook을 사용했다면 역할·secret·capability 경계를 확인했다.
