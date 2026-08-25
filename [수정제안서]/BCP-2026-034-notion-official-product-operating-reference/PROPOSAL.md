# BCP-2026-034 — Notion 공식 제품 사용법·작업 정확도 Reference

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `1b996831ec6f726cf0394288a5686903902383db`
- 제출일: `2026-08-25`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `공식 제품 사실 = 검증`, `Base 일반화 = 검토 완료 / 구현 대기`
- 사용자 요청: `2026-08-25 현재 작업에서 https://www.notion.com/ko/product 및 연결된 Notion 공식 문서를 돌아다니며 정보를 모아 Base가 Notion에서 더 정확하게 작업하도록 교정 요청`
- Registry 상태: `DEFERRED_CONCURRENT_OWNER` — 열린 PR #678이 `[수정제안서]/PROPOSAL_REGISTRY.json`을 수정 중이므로 이번 PR은 해당 경로를 건드리지 않는다. BCP-034 식별자는 main과 열린 BCP-033을 확인한 뒤 충돌 없는 다음 번호로 선택했다.

## 관찰과 증거

### 1. 현재 Base 방향은 유지 가치가 높다

현재 Base는 이미 다음 방향을 사용한다.

```text
Notion = 사람이 읽고 비교·수정하는 프로젝트 기획/시각/데이터 presentation canon
GitHub = Markdown/JSON/code/scene/resource/test/runtime truth
Human Home != AI/System metadata dump
bounded write → destination readback
```

Notion 공식 제품 구조도 Docs, Wikis/Knowledge, Projects, databases/views, integrations, Agent를 서로 다른 책임 표면으로 제공한다. 따라서 Notion을 GitHub runtime truth의 복제본으로 만드는 것보다 현재 Domain Split Canon을 유지하면서 Notion 자체의 객체·보기·권한·레이아웃 동작을 더 정확하게 아는 편이 장기적으로 안전하다.

### 2. 데이터베이스·Data Source·Linked View의 변경 경계가 중요하다

공식 문서상 database는 하나 이상의 data source로 구성되며, 기존 data source를 다른 database/page에 연결할 수 있다. 연결된 data source는 원본 database의 접근 권한을 따른다.

Base에서 특히 구분해야 할 것은 다음 두 종류의 변경이다.

```text
VIEW_LOCAL_PRESENTATION
= filter / sort / group / view layout처럼 현재 view에서 표현을 바꾸는 작업

SOURCE_MUTATION
= page/property/title/data source 자체를 바꾸는 작업
```

프로젝트별 filtered linked view를 편집한다고 해서 항상 사본만 바꾸는 것이 아니다. view 표현 변경과 source record/property 변경을 혼동하면 다른 프로젝트 또는 master data를 의도치 않게 바꿀 수 있다.

### 3. database page layout은 한 레코드 전용 꾸미기가 아니다

Notion 공식 Layouts 문서는 database page layout이 해당 database의 **모든 페이지에 적용**되며 특정 페이지나 특정 view에만 적용할 수 없다고 명시한다. 따라서 GPT/Agent가 한 카드만 보기 좋게 만들 목적으로 `Customize layout`을 수정하는 것은 광역 변경이 될 수 있다.

Base에는 다음 선행 판정이 필요하다.

```text
single record presentation request
→ database-global layout mutation 금지
→ page body / property / bounded block change 사용

database family layout redesign
→ affected records 전수 영향 확인 뒤 layout change 가능
```

### 4. columns는 모바일에서 보존되지 않고 단일 열로 쌓인다

Notion 공식 Columns 문서와 모바일 도움말에 따르면 desktop/tablet column은 phone에서 지원되지 않으며 오른쪽 열 내용이 왼쪽 열 아래로 쌓인다.

따라서 Human Home의 2-column 구성은 desktop 미관만 맞추면 안 된다. 모바일 stack 순서에서도 다음이 성립해야 한다.

- 제목 → 핵심 설명 → 관련 이미지/표 → 다음 섹션 순서가 의미를 유지한다.
- 오른쪽 열에만 필수 전제·주의·결론을 숨기지 않는다.
- comparative pair도 mobile에서 `A → B`로 읽혀야 한다.

### 5. Gallery는 explicit preview source를 쓰는 편이 안정적이다

공식 Gallery 문서는 card preview를 `Page cover`, `Page content`, `Files & media property` 중에서 선택할 수 있다고 설명한다. `Page content`는 첫 블록 변화에 따라 preview가 바뀔 수 있다.

프로젝트 Visual Bible/Asset catalog처럼 이미지 identity가 중요한 surface는 가능한 경우 승인 이미지용 `Files & media` property를 card preview로 명시하는 것이 더 안정적이다.

`Fit image`는 전체 이미지를 카드 안에 맞추는 옵션이다. 구도 전체 확인이 중요한 reference/mockup/flow는 기본적으로 전체가 보이게 하고, 의도된 crop이 필요한 hero/thumbnail만 예외로 둔다.

### 6. 이미지/파일 제한은 공식 문서 내부에도 현재 상충되는 안내가 있다

`Images, files & media` 도움말 상단 note는 다음처럼 안내한다.

- Free: 모든 업로드 파일 5MB 미만
- Paid: PDF 20MB 미만, PNG/JPG image 5MB 미만
- 너무 큰 image가 display되지 않으면 file로 업로드 시도

그러나 같은 문서의 FAQ는 다음처럼 안내한다.

- Free: 개별 파일 5MB
- Paid: 개별 파일 5GB

따라서 Base가 `유료면 이미지도 무조건 5GB까지 inline render 가능` 또는 `유료도 모든 파일이 5MB`처럼 하나의 숫자를 보편 규칙으로 고정하면 안 된다.

안전한 일반화 후보:

```text
INLINE_IMAGE_DISPLAY_SAFE_TARGET
→ PNG/JPG human-visible preview는 5MB 이하를 보수적 목표로 사용

SOURCE_MASTER_OR_LARGE_FILE
→ plan/API가 허용하는 file upload 경로 사용
→ upload success != inline image render success
→ destination readback
→ rendering claim이면 실제 client-visible 확인
```

고해상도 원본 자체를 버리지 않는다. 필요하면 `display preview`와 `source master file`의 역할을 분리한다.

### 7. API file upload는 upload와 attach가 별도 lifecycle이다

Notion Developer 문서에 따르면 File Upload는 `uploaded` 상태가 된 뒤 `type=file_upload` + ID로 page/block/database에 attach해야 한다. Direct Upload는 작은 파일용 단일 multipart 경로, 큰 파일은 multipart 경로가 존재한다.

따라서 Base의 기존 `upload → attach → readback` 원칙은 공식 API와 일치한다. 보강할 부분은 `upload object 생성 성공`과 `destination attachment 성공`을 명확히 분리하는 것이다.

### 8. Synced Block은 재사용 도구지만 프로젝트 정본 복제용으로 남용하면 위험하다

공식 Synced Blocks 문서상 어느 instance에서 수정해도 모든 synced instance가 함께 바뀐다. 원본 block에 접근 권한이 없으면 synced content도 볼 수 없다.

따라서 Base에서는 다음처럼 제한하는 편이 안전하다.

- 공용 용어 설명, 변하지 않는 안내, 공통 edit guide처럼 **정말 동일해야 하는 내용**만 sync.
- 프로젝트 고유 결정, project-specific core system, 승인 상태를 cross-project synced block으로 공유하지 않는다.
- 프로젝트 재사용은 source relation/link/derived view로 추적하고, shared synced block이 프로젝트별 canon처럼 보이지 않게 한다.

### 9. 권한은 page 공유만 보고 판단하면 불충분하다

공식 Sharing 문서는 workspace/teamspace/page 공유 방식과 permission level을 구분한다. linked data source는 원본 접근 권한을 따르고, synced block도 원본 접근 권한에 의존한다.

Base 작업에서 `페이지를 볼 수 있음 = 연결된 모든 source를 볼 수 있음`으로 가정하지 않는다. AI/connector 작업 전에는 target page뿐 아니라 linked source의 실제 접근 가능성까지 구분해야 한다.

### 10. Personal Notion Agent와 Custom Agent는 권한 모델이 다르다

공식 Notion Agent 문서:

- Personal Notion Agent는 현재 사용자와 같은 권한을 가진다.
- page/database 생성·편집, database query, views/properties/relations의 일부 작업을 수행할 수 있다.
- database automation/template/page layout/advanced property(rollup/button 등) 생성, sharing/permission 변경, workspace setting 변경 등은 제한된다.
- 선택한 모델에 따라 workspace/connected-app context 사용 가능성이 달라질 수 있다.

공식 Custom Agents 문서:

- 각 Agent에 사용할 page/database/external source를 명시적으로 부여한다.
- broad access보다 작은 `Tools and access` 범위를 권장한다.
- Agent output의 노출 경계와 underlying source 권한이 같다고 가정하면 안 된다.
- activity/log를 통해 실제 run surface를 확인할 수 있다.

Base는 두 Agent 유형을 같은 `Notion AI` 권한 모델로 뭉뚱그리지 않아야 한다.

### 11. Dashboard view는 좋은 기능이지만 Base 기본 구조로 강제하면 안 된다

공식 Dashboard view는 Business/Enterprise에서 제공되며 database views를 widget으로 묶는 안정적인 control-center surface다. 반면 inline database views in columns는 텍스트/이미지/callout과 자유롭게 섞는 데 더 적합하다.

현재 `ZERO_INCREMENTAL_COST_REQUIRED` 및 프로젝트별 Human Home 요구와 맞춰 다음처럼 판정한다.

- Dashboard view: `ADAPT_IF_INCLUDED_AND_USEFUL`
- Base 공용 필수 구조: `REJECT`
- 기존 Human Home + filtered inline views: 계속 기본

### 12. GitHub integration은 presentation/traceability 도구이지 runtime authority 이전 근거가 아니다

Notion 공식 Product/Docs/Connections는 GitHub PR, issues, repositories를 Notion으로 가져오고 동기화하는 사용 사례를 제공한다. 이는 Notion에서 실행 정보를 참고하기에 유용하지만 GitHub code/test/runtime truth를 Notion 쪽 독립 canon으로 복제해야 한다는 뜻은 아니다.

현재 Domain Split Canon을 유지한다.

## 공식 출처 목록 · 2026-08-25 확인

제품 허브와 해당 제품 사용법을 중심으로 다음 공식 문서를 확인했다.

- https://www.notion.com/ko/product
- https://www.notion.com/product/docs
- https://www.notion.com/product/wikis
- https://www.notion.com/product/projects
- https://www.notion.com/product/connections
- https://www.notion.com/help/data-sources-and-linked-databases
- https://www.notion.com/help/layouts
- https://www.notion.com/help/columns-headings-and-dividers
- https://www.notion.com/ko/help/notion-for-mobile
- https://www.notion.com/help/galleries
- https://www.notion.com/ko/help/images-files-and-media
- https://developers.notion.com/reference/file-upload
- https://developers.notion.com/guides/data-apis/working-with-files-and-media
- https://www.notion.com/help/synced-blocks
- https://www.notion.com/ko/help/share-your-work
- https://www.notion.com/help/notion-agent
- https://www.notion.com/help/custom-agents
- https://www.notion.com/help/custom-agents-sharing-and-permissions
- https://www.notion.com/ko/help/dashboards

제품/요금/Agent capability는 빠르게 변하는 영역이므로 Base에 영구 숫자·plan claim을 박을 때는 `checked_at`과 재검증 조건을 둔다.

## 일반화 후보

### A. `NOTION_OBJECT_SCOPE_BEFORE_WRITE`

모든 의미 있는 Notion mutation 전에 대상이 무엇인지 분류한다.

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

`VIEW_PRESENTATION` 작업과 `DATA_SOURCE_SCHEMA_OR_RECORD` mutation을 혼동하지 않는다.

### B. `NOTION_DATABASE_GLOBAL_LAYOUT_IMPACT_GATE`

`Customize layout`은 database 전체 page에 영향을 주므로 single-record polish에 사용하지 않는다.

### C. `NOTION_MOBILE_STACK_SEMANTIC_ORDER_REQUIRED`

Desktop columns를 사용해도 mobile 1-column stacking 순서에서 핵심 이해가 깨지지 않아야 한다.

### D. `NOTION_GALLERY_EXPLICIT_MEDIA_PREVIEW`

승인 Visual/Asset catalog는 가능한 경우 `Files & media` property를 explicit card preview source로 사용한다. `Page content` preview는 첫 block 변경에 따른 drift 가능성을 인지한다.

### E. `NOTION_PREVIEW_MASTER_SEPARATION`

고해상도 asset은 `human-visible optimized preview`와 `source master file` 역할을 분리할 수 있다. preview 압축/resize가 master quality를 대체하지 않는다.

### F. `NOTION_FILE_LIMIT_CLAIM_CONFLICT_GUARD`

공식 문서가 plan/file-type별 안내를 상충되게 제공하면 하나를 보편 hard limit으로 승격하지 않는다. 현재 inline PNG/JPG는 5MB 이하를 보수적 display target으로 사용하고, 더 큰 master/file은 실제 capability probe + attach + readback으로 판정한다.

### G. `NOTION_SYNCED_CONTENT_SHARED_IDENTITY_ONLY`

Synced Block은 모든 소비처에서 동일해야 하는 내용에만 사용한다. 프로젝트 고유 canon 공유/복제 수단으로 쓰지 않는다.

### H. `NOTION_PERMISSION_TRANSITIVE_SOURCE_CHECK`

Target page 권한만이 아니라 linked data source / synced original / Agent resource access까지 필요한 실제 source 권한을 확인한다.

### I. `NOTION_AGENT_TYPE_PERMISSION_DISTINCTION`

Personal Agent의 user-inherited permission과 Custom Agent의 explicitly granted resource access를 구분한다. unsupported operation을 Agent에게 반복 지시하지 않는다.

### J. `NOTION_PAID_SURFACE_NOT_BASE_DEPENDENCY`

Dashboard/Custom Agent/Worker 등 plan·credit 종속 기능은 현재 Base 필수 구조로 만들지 않는다. 이미 포함된 기능이고 실제 반복 이득이 있을 때만 optional adoption한다.

## 프로젝트 전용으로 남길 내용

- 각 프로젝트 Home의 정확한 섹션 이름/순서
- 어떤 database view가 Gallery/Table/Board인지
- 프로젝트별 visible properties
- project-specific Asset ID, Visual category, core system name
- 특정 프로젝트의 column 개수/desktop 미관
- 특정 프로젝트의 WIP 수와 filtered view 이름

공용 Base에는 Notion의 동작 경계와 안전한 선택 규칙만 남긴다.

## 3안 비교

| 대안 | 내용 | 장점 | 위험 | 판정 |
|---|---|---|---|---|
| A | Notion 제품 사용법을 새 거대 매뉴얼 하나로 복제 | 한 문서에서 다 볼 수 있음 | 공식 문서 업데이트와 빠르게 drift, 기존 P01/Visual 계약과 중복 | `REJECT` |
| B | 공식제품 operating reference 1개 + 기존 책임 원본에 최소 link/guard 추가 | 정본 책임 유지, 공식 fact와 Base rule 분리, 수정 범위 작음 | 새 reference의 freshness 관리 필요 | `ADOPT` |
| C | 날짜형 조사 checkpoint만 추가하고 active owner는 그대로 둠 | 충돌 최소 | 실제 작업자가 새 규칙을 progressive-load하지 않을 수 있음 | `ADAPT_AS_EVIDENCE_ONLY`, 단독으로는 부족 |

권장안은 **B**다. 날짜형 evidence를 별도 대량 축적하기보다 durable reference 안에 `checked_at/source`를 두고, 빠르게 변하는 plan/capability claim만 재검증한다.

## 적용 조건과 비사용 조건

### 적용

- Notion page/database/view/layout/media/permission/Agent 관련 L1+ 작업
- Project Home/Visual Bible/Asset catalog 구조 수정
- linked database/data source 기반 project-filtered view 작업
- 이미지/file delivery와 client-visible claim

### 비사용

- 단순 텍스트 오탈자 교정
- Notion과 무관한 GitHub/runtime 작업
- 특정 프로젝트가 명시적으로 Notion을 사용하지 않는 경우
- 제품 동작과 무관한 순수 게임 디자인 판단

## 반례와 위험

1. **제품 drift** — Agent/dashboard/file-upload capability는 바뀔 수 있다. 해결: `checked_at` + 필요 시 official recheck.
2. **과도한 보수성** — 5MB를 모든 유료 파일의 hard cap으로 오해할 수 있다. 해결: `display-safe target`과 `general file/API capability` 분리.
3. **Notion 제3 정본화** — GitHub integration/linked views가 runtime authority로 오해될 수 있다. 해결: Domain Split Canon 유지.
4. **모바일 과최적화** — desktop 2-column 자체를 금지할 필요는 없다. 해결: column 금지가 아니라 stack semantic-order gate.
5. **Gallery 고정화** — 모든 visual을 Files & media로 강제하면 page cover가 더 적합한 hero use case를 해칠 수 있다. 해결: approved asset catalog 기본값으로만 적용, 명시 예외 허용.
6. **Agent capability 과장** — Notion Agent 기능이 업데이트될 수 있다. 해결: unsupported list를 permanent truth가 아니라 current capability reference로 취급.
7. **동시 PR 충돌** — #689가 `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`를 수정 중이다. 해결: 이번 구현에서 해당 파일 제외.
8. **Registry 충돌** — #678이 `PROPOSAL_REGISTRY.json` 수정 중이다. 해결: 이번 proposal/implementation에서 Registry write defer.

## 적대적 검토 5회

### Loop 1 — Authority / duplication
- 공격: 새 문서가 기존 `NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md`, `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`, P01을 대체하는 제3 정본이 되는가?
- 결과: 거대 매뉴얼 A를 기각. 새 문서는 **제품 동작 reference**, 기존 파일은 **workflow/owner**로 책임 분리.

### Loop 2 — Source conflict / false certainty
- 공격: 공식 help의 file size 안내가 서로 다른데 하나를 사실처럼 고정하는가?
- 결과: `FILE_LIMIT_CLAIM_CONFLICT_GUARD`, display-safe target과 file/API capability 분리.

### Loop 3 — Cross-project / linked-source mutation
- 공격: project-filtered view 편집이 master source mutation으로 번질 수 있는가?
- 결과: `OBJECT_SCOPE_BEFORE_WRITE`, view presentation vs data source mutation을 별도 class로 판정.

### Loop 4 — Rendering / mobile / visual evidence
- 공격: desktop readback만으로 mobile Home 품질을 PASS 처리하는가?
- 결과: mobile stack semantic order와 existing `HUMAN_VISIBLE_PASS` evidence ceiling 결합.

### Loop 5 — Cost / permissions / concurrent work
- 공격: Business dashboard/Custom Agent를 새로운 필수 운영 surface로 만들거나 열린 PR을 침범하는가?
- 결과: paid surface는 optional, #689/#678 owned path는 제외/보류. 새 blocking finding 0.

`CLEAN_REVIEW_EXIT = true` for proposal scope.

## 영향 범위와 검증

승인 구현은 다음 **최소 범위**만 대상으로 한다.

1. 신규 durable product reference
   - `docs/knowledge/methods/NOTION_OFFICIAL_PRODUCT_OPERATING_REFERENCE.md`
2. P01 progressive-load route 추가
   - `docs/operations/base-partitions/P01_PROJECT_PLANNING_OPERATIONS_NOTION.md`
3. Visual/Layout 계약에 모바일 stacking, explicit gallery preview, DB-global layout, file-limit conflict guard 연결
   - `docs/knowledge/game-development/NOTION_GPT_VISUAL_LAYOUT_CONTRACT.md`
4. focused regression test 추가
   - `tests/test_notion_official_product_operating_reference.py`

명시적 제외:

- `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md` — PR #689 owner 보호
- `[수정제안서]/PROPOSAL_REGISTRY.json` — PR #678 owner 보호
- Notion 실제 workspace mass rewrite
- Dashboard/Custom Agent/Worker 신규 구축
- paid service/tool 도입
- GitHub runtime authority 변경

검증:

- current main과 open PR changed-path 재확인
- 새 reference 필수 token/공식 source URL test
- P01 → reference routing test
- Visual/Layout에서 mobile/gallery/layout/file conflict guard 존재 확인
- 기존 Notion visual/MCP focused tests가 실행 가능한 범위에서 회귀 확인
- exact-head CI/readback

## 필요한 도구·파일·권한

- 필요 항목: Notion 공식 Product/Help/Developer docs, GitHub Base repository read/write
- 필요한 이유: fast-changing product facts를 1차 자료로 검증하고 BCP/implementation을 분리하기 위해 필요
- 설치·적용 방법: 새 유료 도구 없음. 현재 Web + GitHub connector 사용
- 설치 후 확인 명령: 신규 설치 없음
- 최소 권한: Base branch/PR 생성·파일 수정 권한. open independent PR mutation 권한 불필요

## 승인과 구현

- 사용자 승인 근거: `2026-08-25 현재 작업 사용자 직접 지시 — Notion product 링크와 연결 문서를 조사해 Base에서 더 정확하게 작업할 수 있도록 반영 요청`
- 승인 범위: 위 `영향 범위와 검증`의 4개 경로 중 충돌 없는 최소 변경
- 상태 전이: `SUBMITTED → UNDER_REVIEW → APPROVED_FOR_IMPLEMENTATION` (현재 작업 사용자 지시 + 3안 비교 + 5회 적대적 검토)
- 구현 PR: `별도 PR로 생성 예정`
- Registry: `DEFERRED_CONCURRENT_OWNER`; #678 owner 종료 뒤 lifecycle reconciliation 필요
- 롤백: 새 reference와 routing/guard/test 변경만 revert. 기존 Domain Split Canon, 기존 Notion Visual workflow, Notion workspace data에는 migration이 없으므로 데이터 롤백 불필요.
