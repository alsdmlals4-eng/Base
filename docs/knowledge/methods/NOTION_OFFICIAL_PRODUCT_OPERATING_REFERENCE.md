# Notion Official Product Operating Reference

- 상태: 공용 product-behavior reference
- 책임: Notion page/database/view/layout/media/permission/Agent 작업에서 제품 동작을 추측하지 않도록 하는 공식문서 기반 운영 참조
- 확인일: `2026-08-25`
- 출처 우선순위: `Notion Product / Help / Developer official docs > professional practice > community report`
- 비목표: Notion을 GitHub runtime truth 대신 제3 정본으로 만들기, 모든 프로젝트 Home을 동일한 template으로 강제하기, 유료 기능을 Base 필수 dependency로 만들기

이 문서는 **Notion 제품의 현재 동작 경계**를 설명한다. 프로젝트 구조·Human Home·Visual 승인·runtime handoff의 책임 원본을 대체하지 않는다.

```text
PRODUCT_BEHAVIOR_REFERENCE != PROJECT_CANON
PRODUCT_BEHAVIOR_REFERENCE != WORKFLOW_OWNER
NOTION_PRESENTATION_CANON != GITHUB_RUNTIME_TRUTH
```

관련 owner:

- Project/Notion 운영: `docs/operations/base-partitions/P01_PROJECT_PLANNING_OPERATIONS_NOTION.md`
- Human Home: `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`
- Visual placement/evidence: `docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md`
- Visual Asset lifecycle: `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
- System Blueprint: `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md`
- Notion query fallback: `docs/knowledge/methods/NOTION_KNOWLEDGE_QUERY_FALLBACK.md`

## 1. 기본 원칙

### `NOTION_OBJECT_SCOPE_BEFORE_WRITE`

의미 있는 Notion 변경 전에는 먼저 **무엇을 바꾸는지** 분류한다.

```text
PAGE_BLOCK
DATABASE_RECORD
VIEW_PRESENTATION
DATA_SOURCE_SCHEMA_OR_RECORD
DATABASE_GLOBAL_LAYOUT
FILE_UPLOAD
SHARING_PERMISSION
AGENT_CONFIGURATION
```

같은 화면에서 조작하더라도 영향 범위가 다르다.

- `PAGE_BLOCK`: 현재 page body의 text/image/callout/table/block.
- `DATABASE_RECORD`: database 안의 개별 page/record property 값.
- `VIEW_PRESENTATION`: filter/sort/group/visible property/card layout 등 view 표현.
- `DATA_SOURCE_SCHEMA_OR_RECORD`: source title/property/schema/page 자체.
- `DATABASE_GLOBAL_LAYOUT`: database page layout 전체.
- `FILE_UPLOAD`: binary upload object와 destination attachment.
- `SHARING_PERMISSION`: page/teamspace/source access.
- `AGENT_CONFIGURATION`: Personal Agent instruction 또는 Custom Agent access/trigger.

```text
VIEW_PRESENTATION != SOURCE_MUTATION
SINGLE_RECORD_EDIT != DATABASE_GLOBAL_LAYOUT
UPLOAD_OBJECT_CREATED != DESTINATION_ATTACHED
TARGET_PAGE_VISIBLE != LINKED_SOURCE_ACCESSIBLE
```

분류가 불명확하면 광역 변경보다 가장 좁은 bounded edit을 선택한다.

## 2. Database · Data Source · Linked Database

Notion database는 하나 이상의 data source로 구성된다. 기존 data source를 다른 database/page에서 link할 수 있다.

### Base 작업 규칙

1. 프로젝트 Home에는 가능한 경우 **기존 master의 project-filtered view**를 사용한다.
2. filter/sort/group/card layout을 바꾸는 작업과 source property/record를 바꾸는 작업을 별도로 판정한다.
3. linked data source는 원본 access level을 따른다. destination page 접근만으로 source 접근을 보장하지 않는다.
4. 프로젝트별 표현이 필요하다고 master record를 복제하지 않는다.
5. 실제 source mutation이면 Project relation, approval state, authority를 먼저 확인한다.

### 안전 순서

```text
read destination view
→ identify linked source
→ classify VIEW_PRESENTATION | SOURCE_MUTATION
→ verify Project relation / source authority
→ smallest write
→ destination readback
→ source readback when source mutation occurred
```

## 3. Database Page Layout

### `NOTION_DATABASE_GLOBAL_LAYOUT_IMPACT_GATE`

Notion의 database page layout은 **해당 database의 모든 page에 적용**된다. 특정 page 또는 특정 view에만 layout을 적용할 수 없다.

따라서:

```text
single record polish
→ database-global layout mutation 금지
→ page body / record property / local block edit 사용

database family layout redesign
→ affected record family 확인
→ global impact를 의도한 경우에만 Customize layout
→ Apply to all pages 영향 확인
```

Database page layout builder의 full experience는 desktop/web 기준으로 판단한다. 모바일에서 layout을 볼 수 있다고 해서 desktop builder geometry까지 검증된 것으로 보지 않는다.

## 4. Columns와 Mobile Stacking

### `NOTION_MOBILE_STACK_SEMANTIC_ORDER_REQUIRED`

Notion의 desktop/tablet columns는 phone에서 여러 열로 유지되지 않고 **오른쪽 열 내용이 왼쪽 열 아래로 쌓인다**.

Columns 자체를 금지하지 않는다. 대신 mobile 1-column reading order가 의미를 유지해야 한다.

좋은 구조:

```text
[핵심 설명] | [관련 이미지]
→ mobile: 핵심 설명 → 관련 이미지
```

위험한 구조:

```text
[결론만 있음] | [전제/주의/필수 조건]
→ mobile에서 전제보다 결론이 먼저 보이거나 의미가 분리됨
```

규칙:

- 오른쪽 열에만 핵심 전제·경고·결론을 숨기지 않는다.
- 비교형 2열은 mobile에서 `A → B` 순서로 읽어도 이해 가능해야 한다.
- Human Home acceptance에 mobile 이해가 포함되면 실제 mobile/client-visible evidence가 필요하다.
- connector/server readback만으로 phone geometry PASS를 주장하지 않는다.

## 5. Gallery · Visual Bible · Card Preview

### `NOTION_GALLERY_EXPLICIT_MEDIA_PREVIEW`

Notion Gallery card preview는 대표적으로 다음 source를 사용할 수 있다.

- `Page cover`
- `Page content`
- `Files & media` property

`Page content` preview는 첫 block이 바뀌면 card preview도 드리프트할 수 있다.

따라서 승인 Visual/Asset catalog에서는 가능한 경우 **승인 이미지가 들어 있는 `Files & media` property를 explicit card preview source로 사용**한다.

예외:

- Project Home hero처럼 page cover 자체가 의도된 visual authority일 때는 `Page cover` 사용 가능.
- 임시 note/reference처럼 preview identity가 중요하지 않으면 `Page content`도 허용.

### `Fit image`

- reference/mockup/flow처럼 전체 구도가 중요하면 전체 이미지가 보이도록 `Fit image`를 우선한다.
- hero/thumbnail에서 의도된 crop이 필요할 때만 crop/reposition을 사용한다.
- crop된 card preview가 source master의 전체 내용을 대체하지 않는다.

## 6. 이미지 · 파일 · 고해상도 원본

### 공식문서 충돌을 숨기지 않는다

2026-08-25 현재 `Images, files & media` 공식 도움말에는 서로 다른 제한 안내가 함께 존재한다.

상단 note:

- Free: 모든 업로드 파일 5MB 미만
- Paid: PDF 20MB 미만, PNG/JPG image 5MB 미만
- image가 너무 커 display되지 않으면 file upload 시도

같은 문서 FAQ:

- Free: 개별 file 5MB
- Paid: 개별 file 5GB

따라서 Base는 단일 숫자를 모든 upload/render 경로의 hard cap으로 일반화하지 않는다.

### `NOTION_FILE_LIMIT_CLAIM_CONFLICT_GUARD`

```text
INLINE_IMAGE_DISPLAY_SAFE_TARGET
→ human-visible PNG/JPG preview는 5MB 이하를 보수적 목표로 사용

SOURCE_MASTER_OR_LARGE_FILE
→ 현재 plan/API가 실제로 허용하는 file path 사용
→ upload invocation
→ attach
→ destination readback
→ rendering claim이면 actual client observation
```

### `NOTION_PREVIEW_MASTER_SEPARATION`

고해상도 원본을 낮은 용량 preview 때문에 폐기하거나 overwrite하지 않는다.

권장 역할 분리:

```text
DISPLAY_PREVIEW
- Human Home / Gallery / inline viewing 최적화
- 빠른 로딩과 안정적 render 우선
- 필요하면 5MB 이하 PNG/JPG

SOURCE_MASTER
- 승인 원본 / 고해상도 보존
- Files & media / file block / verified typed file upload
- version / provenance / rights 유지
```

`DISPLAY_PREVIEW`가 존재한다고 `SOURCE_MASTER` 품질이나 runtime asset이 검증된 것은 아니다.

Notion에서 `원본 보기`는 브라우저 새 탭에서 원본 size를 열 수 있지만, 이 UI 기능 자체가 source-master provenance/version 관리의 대체물은 아니다.

## 7. File Upload API Lifecycle

Notion Developer API에서 File Upload는 upload object 생성, content 전송, destination attach가 분리된다.

### `NOTION_UPLOAD_ATTACH_READBACK_LIFECYCLE`

```text
create file upload
→ send/import bytes
→ wait until status=uploaded
→ attach with type=file_upload + id
→ fetch destination
→ verify expected file/image property or block
→ client-visible claim이면 actual client observation
```

`uploaded` 상태만으로 원하는 page/database에 배치됐다고 주장하지 않는다.

현재 공식 developer guide는:

- small/direct upload 경로
- large/multi-part upload 경로
- external URL import
- uploaded ID의 재사용/attachment

을 구분한다. exact size/capability는 API version과 plan에 따라 바뀔 수 있으므로 구현 직전 최신 official developer docs를 재확인한다.

## 8. Synced Blocks

### `NOTION_SYNCED_CONTENT_SHARED_IDENTITY_ONLY`

Synced Block은 어느 instance에서 편집해도 연결된 다른 instance에 반영된다.

적합:

- 공용 용어 설명
- 공통 edit guide
- 실제로 모든 소비처에서 동일해야 하는 evergreen 안내

부적합:

- 프로젝트 고유 core system 결정
- 프로젝트별 승인 상태
- 서로 독립적으로 진화해야 하는 GDD section
- cross-project canon을 하나의 shared block로 묶는 방식

원본 synced block에 access가 없으면 소비처에서도 content를 볼 수 없을 수 있다. permission/readback을 별도로 확인한다.

## 9. Sharing · Permission · Source Access

### `NOTION_PERMISSION_TRANSITIVE_SOURCE_CHECK`

Page 공유 상태만 보고 실제 작업 권한을 추측하지 않는다.

확인 대상:

```text
target page
+ parent/teamspace inheritance when relevant
+ linked data source original
+ synced block original
+ Agent Tools and access
+ connector/integration granted resources
```

권한이 필요한 mutation에서 `PAGE_READABLE`을 `SOURCE_WRITABLE`로 승격하지 않는다.

공개/외부 공유는 별도 사용자 결정·보안 검토 없이 자동 확대하지 않는다.

## 10. Personal Notion Agent

### `PERSONAL_NOTION_AGENT_USER_PERMISSION_INHERITANCE`

2026-08-25 공식 도움말 기준 Personal Notion Agent는 현재 사용자와 같은 Notion permission을 사용한다.

현재 가능한 대표 작업:

- workspace/connected-app context를 사용한 검색·질의
- page 생성/편집
- database 생성/편집
- database query
- view/property/relation의 일부 생성/편집
- PDF/CSV ingest 및 구조화

현재 제한되는 대표 작업:

- 새 database automation
- database template
- database page layout
- 일부 advanced property(공식 도움말의 formula/rollup/button 관련 제한은 기능 변화 가능성이 있으므로 사용 직전 재확인)
- sharing/permission 변경
- workspace-level settings

### 모델/context 주의

선택한 모델에 따라 workspace/connected-app 정보를 보지 못하고 web만 사용할 수 있는 경우가 있다.

```text
AGENT_SELECTED_MODEL != WORKSPACE_CONTEXT_GUARANTEED
```

workspace canon에 의존하는 작업은 실제 source selection/context를 확인한다.

## 11. Custom Agents

### `CUSTOM_AGENT_EXPLICIT_RESOURCE_ACCESS`

Custom Agent는 Personal Agent의 단순 복사본이 아니다. 각 Agent의 `Tools and access`에서 사용할 page/database/external source를 명시적으로 부여한다.

기본 규칙:

- smallest useful resource set부터 시작한다.
- broad `Pages shared with everyone` access를 기본값으로 두지 않는다.
- Instruction에서 page를 언급했다고 Agent resource access가 자동 부여되는 것으로 가정하지 않는다.
- Trigger/Access/Activity를 함께 확인한다.
- Agent output을 볼 수 있는 사람과 underlying source를 직접 볼 수 있는 사람이 항상 같다고 가정하지 않는다.

Custom Agent/Worker처럼 credit/plan에 종속되는 자동화는 현재 Base 기본 경로가 아니다.

## 12. Paid Surface와 비용 경계

### `NOTION_PAID_SURFACE_NOT_BASE_DEPENDENCY`

2026-08-25 공식 도움말 기준 Dashboard view는 Business/Enterprise plan surface다.

따라서:

```text
Dashboard view
→ ADAPT_IF_INCLUDED_AND_USEFUL
→ Base universal requirement 아님

Custom Agents / Workers / paid automation
→ measured recurring burden + cost review + user decision 전에는 default 아님
```

Human Home + filtered inline views는 plan-independent 기본 구조로 유지한다.

## 13. Dashboard View vs Inline Views

Dashboard view가 available한 경우:

- 여러 database view를 stable widget surface로 묶고 싶을 때 유리.
- Edit/View mode 분리가 필요할 때 유리.
- global filter를 여러 widget에 적용할 수 있음.

Inline views in columns가 적합한 경우:

- rich text, image, callout과 database를 한 page에서 혼합.
- 프로젝트별 설명형 Home.
- 빠른 실험과 개별 page 맞춤 배치.

Base default는 Dashboard가 아니라 **project-specific Human Home + filtered views**다.

## 14. GitHub Integration Boundary

Notion Product/Connections는 GitHub PR/issues/repositories를 Notion에 가져오고 연결하는 기능을 제공한다.

Base 해석:

```text
GitHub integration in Notion
= human-facing traceability / context / derivative view
!= second runtime authority
```

- code/JSON/scene/resource/test/runtime evidence는 GitHub/repository authority 유지.
- Notion에서 GitHub 상태를 보여준다고 independent duplicated execution state를 새로 만들지 않는다.
- stale synced status보다 live link/derived integration을 우선한다.

## 15. Notion 작업 실행 순서

L1+ Notion mutation의 공용 순서:

```text
1. read current project authority + target page/database/view
2. classify Notion object scope
3. identify source / linked source / project relation
4. check reuse and existing canonical instance
5. check permission/capability/plan boundary
6. choose smallest bounded mutation
7. write
8. destination readback
9. source readback if source mutation occurred
10. human/device-visible observation when rendering matters
11. keep repository runtime truth separate
```

### Object-specific 추가 gate

```text
DATABASE_GLOBAL_LAYOUT
→ affected database family 확인

COLUMN_LAYOUT
→ mobile stacking semantic order 확인

GALLERY_VISUAL
→ explicit preview source / approval / fit-image intent 확인

FILE_UPLOAD
→ upload → status → attach → readback

SYNCED_BLOCK
→ shared identity가 정말 동일해야 하는지 확인

AGENT_CONFIGURATION
→ Personal vs Custom permission model 구분
```

## 16. 실패 패턴

다음을 거부한다.

- linked view에서 source record를 바꾸면서 local view edit이라고 보고하는 것
- 한 database record만 꾸미려다 global page layout을 바꾸는 것
- desktop columns가 phone에서도 같은 geometry라고 가정하는 것
- Visual Bible에서 `Page content` 첫 block drift를 모른 채 canonical preview로 의존하는 것
- 5MB와 5GB 중 하나를 모든 Notion image/file 경로의 universal limit으로 고정하는 것
- low-size preview를 high-resolution master로 overwrite하는 것
- upload object 생성만으로 destination delivery 완료를 주장하는 것
- target page access만으로 linked source/synced original 권한을 추측하는 것
- Personal Agent와 Custom Agent permission model을 같은 것으로 보는 것
- paid Dashboard/Custom Agent/Worker를 Base 필수 운영 경로로 만드는 것
- Notion GitHub integration을 repository runtime authority 이전으로 해석하는 것

## 17. Freshness Gate

아래 사항은 fast-changing product fact이므로 사용 직전 official source를 재확인한다.

- plan별 upload/file size
- Agent가 할 수 있는/없는 operation
- Custom Agent credit/pricing/access model
- Dashboard/verified-page plan availability
- API upload size/multipart/version
- Developer Portal/CLI capability

고정 원칙은 제품 세부 수치가 아니라 다음과 같은 **검증 방식**이다.

```text
CHECK_CURRENT_OFFICIAL_SOURCE
→ classify scope/capability
→ minimum real operation when needed
→ readback
→ no overclaim
```

## 18. 공식 출처 · 2026-08-25

### Product

- https://www.notion.com/ko/product
- https://www.notion.com/product/docs
- https://www.notion.com/product/wikis
- https://www.notion.com/product/projects
- https://www.notion.com/product/connections

### Database / layout / media

- https://www.notion.com/help/data-sources-and-linked-databases
- https://www.notion.com/help/layouts
- https://www.notion.com/help/columns-headings-and-dividers
- https://www.notion.com/ko/help/notion-for-mobile
- https://www.notion.com/help/galleries
- https://www.notion.com/ko/help/images-files-and-media
- https://www.notion.com/help/synced-blocks
- https://www.notion.com/ko/help/share-your-work
- https://www.notion.com/ko/help/dashboards

### Agent

- https://www.notion.com/help/notion-agent
- https://www.notion.com/help/custom-agents
- https://www.notion.com/help/custom-agents-sharing-and-permissions

### Developer file upload

- https://developers.notion.com/reference/file-upload
- https://developers.notion.com/guides/data-apis/working-with-files-and-media
- https://developers.notion.com/guides/data-apis/uploading-small-files

## 19. Acceptance

이 reference를 올바르게 사용했다면:

- Notion object scope와 영향 범위를 write 전에 구분한다.
- project-filtered linked view를 source copy로 오해하지 않는다.
- single-record 요청이 database-global layout mutation으로 번지지 않는다.
- desktop Home이 mobile stack에서도 의미를 유지한다.
- Visual Gallery의 preview source가 의도적으로 선택된다.
- preview와 high-resolution master의 역할이 분리된다.
- file-size 공식문서 충돌을 숨기거나 universal hard cap으로 오해하지 않는다.
- upload/attach/readback을 별도 lifecycle로 검증한다.
- synced content와 project-specific canon의 경계를 유지한다.
- Personal Agent와 Custom Agent permission model을 구분한다.
- paid surface를 Base 필수 dependency로 만들지 않는다.
- GitHub runtime truth와 Notion human-facing canon 분리가 유지된다.
