# Project Operations Templates

이 디렉터리는 Base를 채택한 프로젝트가 **프로젝트 운영 상태·결정·handoff·기획 명세·에셋 전달·검증**을 시작할 때 필요한 최소 템플릿을 선택해 설치하는 묶음이다.

설치 템플릿 자체는 활성 프로젝트 정본이 아니다. 프로젝트에 복사·채택되고 해당 프로젝트 `AGENTS.md`, registry와 repository commit으로 연결된 파일만 현재 정본이 된다.

## 1. Current workspace authority

현재 기본 계약은 다음 두 owner다.

- `docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json`
- `docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md`

```text
REPOSITORY_PRIMARY_PROJECT_CANON
├─ Markdown / JSON / game data / code / scene / resource / config
├─ tracked implementation asset / ASSET_MANIFEST
├─ test / build / runtime evidence
└─ exact commit / PR / rollback history

AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN
└─ 프로젝트 의미·시스템·콘텐츠·UX·데이터·구현 계약의 AI 정본

HUMAN_GDD_PDF_DERIVED_VIEW
└─ exact repository commit에서 생성한 사람용 상세 기획서 PDF

CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON

Notion / Google Sheets
└─ LEGACY_READ_ONLY_MIGRATION_SOURCE when unique unmigrated material remains
```

기본 통합 기획서 프로필은 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`다.

```text
EXACTLY_TWO_DELIVERABLES
├─ HUMAN_MASTER_GDD_PDF
└─ AI_PRODUCTION_SPEC_MARKDOWN
```

- 사용자에게 기본 다운로드 링크로 제공하는 것은 PDF 하나다: `PDF_ONLY_USER_DOWNLOAD`.
- AI Markdown은 repository path·branch·exact commit SHA·PR·validation result로 보고한다.
- 두 산출물은 `SHARED_ID_AND_SOURCE_SHA_REQUIRED`를 따른다.
- 신규 Notion page/database/write/upload/sync/readback은 기본 작업이나 완료 조건이 아니다.
- 이미지 생성·편집은 사용자가 명시적으로 요청했을 때만 진행한다.

## 2. Recommended project canonical bundle

프로젝트 구조가 이미 있으면 기존 owner를 우선하고 동등 경로를 `AGENTS.md`와 registry에 기록한다.

```text
AGENTS.md
START_HERE.md
ACTIVE_CONTEXT.md
CURRENT_CONFIRMED_DECISIONS.md
docs/canon/AI_GAME_SPEC.md              # 또는 등록된 동등 owner
docs/handoffs/CURRENT_CODEX_HANDOFF.md
assets/ASSET_MANIFEST.json               # 또는 프로젝트 manifest owner
docs/exports/HUMAN_GDD_<gate>_<sha>.pdf  # 파생 검토본
actual code / data / scenes / resources / tests / evidence
```

한 질문에 두 활성 정본을 만들지 않는다. PDF·대화·memory·Library·legacy Notion은 repository current owner를 덮지 않는다.

## 3. Core templates

| 경로 | 역할 |
|---|---|
| `PROJECT_START_HERE.md` | 프로젝트 콜드 스타트 진입점 |
| `ACTIVE_CONTEXT.md` | 현재 목표·단계·blocker·다음 행동 |
| `CURRENT_CONFIRMED_DECISIONS.md` | 승인 Decision과 repository readback 상태 |
| `DECISION_LOG.md` | 결정 이력과 supersession |
| `HANDOFF.md` | 다른 세션/Executor가 이어받을 상태 |
| `ROADMAP.md` | milestone과 실행 순서 |
| `DEVELOPMENT_GATES.md` | 단계별 완료·검증 Gate |
| `PROJECT_DOCUMENTATION_MAP.md` | 프로젝트 정본 지도 |
| `DESIGN_DOCUMENT_REGISTRY.json` | 구조화 설계 문서 registry |
| `AI_PROJECT_CANON_SPEC.md` | AI용 상세 기획·구현 명세 기본 Template |
| `HUMAN_GDD_PDF_EXPORT_CHECKLIST.md` | 사람용 상세 PDF 생성·render/readback Gate |
| `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD_WORK_INSTRUCTION.md` | Desktop GPT에서 2파일 통합 기획서를 만드는 실행 지시문 |
| `NOTION_RETIREMENT_AND_REPOSITORY_MIGRATION_CHECKLIST.md` | legacy Notion/Sheet 고유 자료 이관·퇴역 Gate |
| `ASSET_MANIFEST.yml` | 실제 소비 asset identity·consumer·version·provenance·상태 |
| `CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md` | 실제 Godot 제품 구현 인계 기본 Template |
| `GRILL_ME_DECISION_RECORD.md` | 단일 Grill Me 질문·답변·승인·반영 증거 |
| `GRILL_ME_BATCH_CHECKPOINT.md` | 승인 Decision 배치 checkpoint |
| `SKILL_EXECUTION_REPORT.md` | 실제 Work Mode·Skill·Mode 사용 증거 |
| `LEGACY_ARTIFACT_RECONCILIATION.md` | legacy 자료 분류·이관 증거 |
| `PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md` | `COMPATIBILITY_ONLY` legacy migration aid |

모든 템플릿을 일괄 복사하지 않는다. 프로젝트의 현재 구조와 Goal에 필요한 최소 파일만 채택한다.

## 4. Installation sequence

```text
latest project repository and exact main commit
→ project AGENTS / START_HERE / ACTIVE_CONTEXT / confirmed decisions
→ registered design/data/asset/test/runtime owners
→ same-Goal open PR read-only reconciliation
→ legacy Notion/Sheet inventory only when unique material may remain
→ install only the missing required templates
→ route AI canon / handoff / asset manifest / evidence owners
→ repository readback and contract tests
→ exact commit identity
→ project work
```

### New project

- repository를 먼저 만든다.
- `REPOSITORY_PRIMARY_PROJECT_CANON`을 기본 workspace로 둔다.
- AI 기획 정본과 current handoff·asset manifest owner를 등록한다.
- 사용자가 프로젝트 통합 정리를 요청하면 두 산출물 프로필을 적용한다.
- 신규 Notion workspace나 Google Sheet를 설치 완료 조건으로 만들지 않는다.

### Existing project

- 기존 경로·이름을 무조건 표준명으로 바꾸지 않는다.
- project `AGENTS.md`와 registry가 선언한 동등 owner를 보존한다.
- legacy 자료는 `UNIQUE / DUPLICATE / OBSOLETE / BLOCKED_UNVERIFIED`로 분류한다.
- `UNIQUE`만 repository canon, tracked runtime asset 또는 비정본 Library reference로 이관한다.
- destination readback·consumer·provenance를 확인하기 전 원본을 삭제하지 않는다.

## 5. AI canon and human PDF

### AI canon

`AI_PROJECT_CANON_SPEC.md`는 다음을 포함한다.

- 플레이어 약속·핵심 감정·의미 있는 선택·차별점;
- Core / Session / Meta Loop와 full flow;
- 핵심·서브 시스템과 콘텐츠의 규칙·상태·예외·피드백;
- UX/UI, 데이터·저장, asset/audio/VFX 실제 소비처;
- Godot Scene/Node/Script/Resource 책임과 signal/event/state contract;
- Acceptance, automated/runtime/play/UX evidence ceiling;
- 보호 범위·명시적 제외 범위·위험·rollback.

### Human PDF

`HUMAN_GDD_PDF_DERIVED_VIEW`는 사람이 읽고 중간점검하는 상세 기획서다.

- exact source branch/SHA와 canon version을 표시한다.
- AI canon과 동일한 `SYS / CNT / UI / UX / AST / AUD / DAT / QA / DEC` ID를 사용한다.
- 구현되지 않은 내용을 구현 완료처럼 쓰지 않는다.
- 모든 페이지를 render/readback한다.
- PDF에서 승인된 수정은 repository canon으로 되돌린다.
- 작은 변경마다 재생성하지 않고 의미 있는 Gate에서 생성한다.

## 6. Asset delivery

```text
actual game consumer / screen / scene / action / state inventory
→ approved or explicitly missing asset requirement
→ repository implementation path
→ ASSET_MANIFEST identity / consumer / version / approval / provenance / rights
→ SHA-256 readback
→ Codex implementation
→ runtime consumption evidence
```

`REPOSITORY_PATH_MANIFEST_SHA256_READBACK`의 최소 필드:

```text
asset_id
repository_path
actual_consumer
approval_status
version
sha256
source_or_provenance
rights_or_license_state
implementation_status
supersedes_or_replaced_by
```

Notion preview나 attachment만으로 implementation-ready가 아니다. 반대로 Notion이 없어도 repository asset과 manifest readback이 있으면 current implementation input이 될 수 있다.

## 7. GPT–Codex handoff

세부 owner는 `docs/REPOSITORY_FIRST_GPT_CODEX_HANDOFF_POLICY.md`다.

```text
GPT planning / research / review / approved visual preparation
→ repository AI canon and asset readback
→ EXACT_REPOSITORY_COMMIT
→ Codex actual Godot product implementation
→ test / runtime / play evidence
→ GPT final review
→ CANON_SYNC_AFTER_VALIDATION
```

Codex는 일반 repository 문서 작업자나 이미지 생성자가 아니다. 실제 Godot 제품 구현이 필요한 `PLAY_MEANINGFUL_WORK_SLICE`에서만 사용한다.

## 8. Legacy Notion operation gate

Notion은 신규 기본 workspace가 아니지만, 고유 미이관 자료를 읽거나 보존해야 할 때는 `templates/project-operations/NOTION_OPERATION_GATE.md`를 계속 적용한다.

```text
LEGACY_READ_ONLY_MIGRATION_SOURCE
→ exact Project and destination identity
→ read/fetch current page, database, data source and attachment
→ classify object and material
→ smallest bounded migration edit only when required
→ destination repository/Library readback
→ provenance and consumer check
→ legacy source remains read-only
```

- `PROJECT_RELATION_REQUIRED`: 여러 프로젝트 자료를 섞지 않는다.
- database/schema/property를 수정하기 전 current schema를 읽는다.
- targeted update가 가능하면 전체 page replacement를 사용하지 않는다.
- 삭제·대량 이동은 별도 사용자 승인 없이 수행하지 않는다.
- webhook payload나 repository에 secret·token·개인정보를 넣지 않는다.
- paid-only Notion automation·Agent를 Base 필수 dependency로 만들지 않는다.
- connector/API readback은 화면 geometry, 첨부 원본, 게임 runtime truth를 대신하지 않는다.

과거 용어 `NOTION_DEFAULT_PROJECT_WORKSPACE`, `NOTION_HUMAN_FACING_CANON`, `DOMAIN_SPLIT_CANON`은 `LEGACY_DISCOVERY_ONLY` migration alias다. 이 문자열이 legacy 문서에 존재해도 현재 기본값으로 복원하지 않는다.

## 9. Legacy retirement exit

프로젝트가 Notion dependency 제거를 주장하려면 다음이 모두 0이어야 한다.

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

- 모든 `UNIQUE` 항목이 destination readback을 가져야 한다.
- `BLOCKED_UNVERIFIED`가 있으면 완료 claim의 영향을 명시한다.
- 사용자가 삭제를 요청하지 않았다면 기존 Notion page/database를 삭제하지 않는다.
- 이 세 count의 0은 runtime·UX·release PASS가 아니다.

## 10. Decision synchronization

```text
user approval
→ branch CURRENT_CONFIRMED_DECISIONS and domain canon
→ stable DEC ID and source commit
→ repository readback
→ logical commit
→ exact-head review and checks
→ squash merge
→ main readback
→ SYNCED_TO_MAIN
```

legacy Notion/Sheet write나 readback은 active Decision sync 완료 조건이 아니다. 다만 승인 근거가 legacy source에만 있으면 먼저 migration evidence를 남긴다.

## 11. Vertical Slice entry

통합 Vertical Slice 구현·검증이 승인되면 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md`를 사용한다. 이 README는 Prompt의 복사본을 소유하지 않는다.

프로젝트 기획·검수·asset 준비와 Codex 구현·사용자 검증의 단계 상태는 현재 adopted Base owner를 따른다. 오래된 Prompt의 Notion-first 문구가 current repository-first owner를 덮지 않는다.

## 12. Definition of Done

- [ ] 정확한 project repository와 exact commit을 확인했다.
- [ ] project-specific `AGENTS.md`와 current owners를 확인했다.
- [ ] `REPOSITORY_PRIMARY_PROJECT_CANON` 또는 명시된 동등 owner가 있다.
- [ ] AI canon·confirmed decisions·active context·handoff·asset manifest가 연결된다.
- [ ] 신규 Notion/Sheet를 기본 workspace나 완료 조건으로 만들지 않았다.
- [ ] legacy 고유 자료는 분류·이관·destination readback 없이 삭제하지 않았다.
- [ ] 사람용 PDF는 exact commit의 파생본이며 AI canon과 같은 ID/SHA를 사용한다.
- [ ] 실제 asset은 repository path·consumer·approval·SHA·provenance를 가진다.
- [ ] 실행하지 않은 test/runtime/render/play/UX는 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`다.
- [ ] 추가 유료 서비스나 별도 metered API를 승인 없이 도입하지 않았다.
