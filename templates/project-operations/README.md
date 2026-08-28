# Project Operations Templates

이 디렉터리는 Base를 채택한 프로젝트가 **프로젝트 운영 상태·결정·handoff·설계 문서 연결**을 시작할 때 복사/적용하는 템플릿 묶음이다. 설치 템플릿 자체는 프로젝트의 활성 상태 정본이 아니며, 실제 프로젝트에서 생성·채택된 문서와 정확한 Project Notion workspace가 정본 역할을 가진다.

## Workspace authority

현재 기본 계약은 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json`의 `DOMAIN_SPLIT_CANON`이다.

```text
NOTION_DEFAULT_PROJECT_WORKSPACE
├─ NOTION_HUMAN_FACING_CANON: 사람이 읽고 판단하는 프로젝트 계획·결정·설명·시각 자료
└─ Project relation으로 프로젝트 간 격리

REPOSITORY_STRUCTURED_CANON
└─ 구조화 상태·Commit·실제 코드/데이터/씬/자산·runtime truth·검증 증거

Google Sheets
└─ COMPATIBILITY_ONLY: 기존 프로젝트의 UNIQUE legacy material 이관 입력
```

- 새 프로젝트의 기본 사람용 계획 workspace로 Google Sheets를 만들지 않는다.
- Figma, 외부 HTML workspace, 폐기된 custom local Tool/Hub를 신규 기본 surface로 부활시키지 않는다.
- legacy source는 `UNIQUE / DUPLICATE / OBSOLETE`로 판정하고, `UNIQUE`만 현행 owner로 이관 → destination readback/Test → consumer/reference 확인 뒤 원본 수명주기를 판정한다.

## 선택형 Desktop GPT 2파일 통합 제작 기획서 프로필

사용자가 프로젝트 정본을 **사람용 상세 PDF와 AI용 repository Markdown의 정확히 2개 산출물**로 정리하라고 명시적으로 선택한 경우 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD` profile을 사용한다.

- 정책 owner: `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`
- 붙여넣기용 실행 원본: `templates/project-operations/GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md`
- 결과: 사용자용 상세 제작 기획서 PDF 1개 + `docs/design/PROJECT_AI_PRODUCTION_SPEC.md` 1개
- 사용자 download surface: PDF만 제공하고 AI 문서는 repository path·branch·commit SHA·PR·검증 결과만 보고한다.
- Notion: 기존 고유 미이관 자료가 있을 때 입력 자료로만 읽으며 신규 출력·갱신·동기화·readback 대상에서 제외한다.
- 보호 경계: DOCX·ZIP·별도 appendix·이미지 묶음을 만들지 않고, 새 이미지 생성은 사용자의 별도 명시적 요청이 있을 때만 진행한다.

이 profile은 master-GDD 작업에 사용자가 명시적으로 선택한 경우에만 적용한다. 기존 `DOMAIN_SPLIT_CANON`, 일반 Notion 프로젝트 운영, 다른 publication profile을 전역 폐기하거나 자동 대체하지 않는다.

## Notion project operation gate

세부 실행 원본은 `templates/project-operations/NOTION_OPERATION_GATE.md`다. 아래 내용은 설치·콜드 스타트용 요약이며 충돌 시 세부 실행 원본을 우선한다.

프로젝트에서 Notion을 읽거나 수정하는 AI/자동화는 `NOTION_OPERATION_GATE`를 기본 안전 계약으로 사용한다. 이 규칙은 사람용 Home에 새 메타데이터를 추가하는 규칙이 아니라, AI/System 작업면에서 **무엇을 어떤 범위로 수정할지** 통제하는 규칙이다.

```text
Project / destination 확인
→ current page/database/data source fetch/read
→ PAGE_BLOCK | DATABASE_RECORD | VIEW_PRESENTATION | DATA_SOURCE_SCHEMA_OR_RECORD | DATABASE_GLOBAL_LAYOUT | FILE_UPLOAD 판정
→ schema/property/Project relation 확인
→ smallest bounded edit
→ write
→ destination readback
→ source mutation이면 source readback
→ structured/runtime 의미 변경이면 repository owner 동기화
```

운영 규칙:

- database page나 data source를 수정하기 전에는 현재 schema와 정확한 property 이름을 먼저 읽는다.
- `VIEW_PRESENTATION`과 source record/schema mutation을 구분한다. linked view의 filter/sort/card 표현만 바꿨다면 source 자체를 바꿨다고 보고하지 않는다.
- targeted update/insert가 가능하면 전체 page replace를 기본값으로 사용하지 않는다.
- child page/database 삭제가 필요한 변경은 자동으로 강행하지 않고 삭제 대상을 제시한 뒤 사용자 확인을 받는다.
- write 성공만으로 완료하지 않고 의도한 값과 Project relation을 `destination readback`으로 확인한다.
- connector/API readback은 실제 화면 geometry, 모바일 표현, 첨부 렌더링, 게임 runtime truth를 대신하지 않는다.
- Notion 조작용 raw ID, schema, Record Key, revision, prompt, automation metadata 같은 AI/System 정보는 사람용 Home의 기본 콘텐츠로 복제하지 않는다.

### Automation / webhook route

Notion의 자동화 관련 기능은 목적에 따라 구분한다.

- **Webhook action**: 사용자가 누른 Button 또는 Database automation이 외부 endpoint로 POST를 보내는 outbound 기능이다.
- **Integration webhook**: 외부 integration이 Notion page/database 변경 이벤트를 받아 처리하는 developer/event-listener 기능이다.
- **Database automation**: Notion 내부 조건/트리거에 따라 action을 실행하는 기능이다. automation이 만든 변경이 다른 Database automation을 계속 깨우는 **자동 연쇄 실행을 전제로 설계하지 않는다**. 사용자가 직접 누른 Button처럼 명시적 user action은 별도 trigger 가능성을 확인한다.
- webhook payload에 API key, password, access token 같은 `secret`을 직접 넣지 않는다. 외부 서비스 인증은 수신 측의 안전한 secret storage/header/verification 경로로 분리한다.
- paid-only 자동화나 Agent 기능은 Base/프로젝트 필수 dependency로 만들지 않는다. 무료·현재 연결 도구·repository-native 경로로 충분한 경우 그 경로를 우선한다.

자동화를 도입할 때는 UI에 기능이 존재한다는 사실과 현재 연결된 GPT/Notion 도구가 실제로 생성·수정·검증할 수 있다는 사실을 구분한다. 지원되지 않는 기능은 수동 설정이 필요한 것으로 남기고 구현 완료라고 주장하지 않는다.

## Repository design root

프로젝트가 Base 운영 템플릿을 채택할 때 설계 문서 폴더 `[기획서]`는 **저장소 루트**에 둔다. `templates/project-operations/` 자체나 중첩된 하위 폴더를 프로젝트의 활성 design root로 사용하지 않는다. Notion 사람용 workspace와 Repository `[기획서]` 구조화 문서는 서로 역할이 다르며, 어느 한쪽도 다른 쪽의 복사본으로 운영하지 않는다.

`DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`를 선택한 master-GDD 작업에서는 `docs/design/PROJECT_AI_PRODUCTION_SPEC.md`가 AI 기획·구현 계약 owner이고 PDF는 동일 SHA의 사람용 snapshot이다. 이 선택형 경로는 저장소의 실제 code/data/scene/resource/test/runtime truth를 대체하지 않는다.

## 핵심 템플릿

| 경로 | 역할 |
|---|---|
| `PROJECT_START_HERE.md` | 프로젝트 콜드 스타트 진입점 |
| `ACTIVE_CONTEXT.md` | 현재 작업 단계·blocker·다음 행동 |
| `CURRENT_CONFIRMED_DECISIONS.md` | 승인 Decision과 Repository/Notion readback 상태 |
| `DECISION_LOG.md` | 결정 이력 |
| `GRILL_ME_DECISION_RECORD.md` | 단일 Grill Me 질문·답변·승인·반영 증거 |
| `GRILL_ME_BATCH_CHECKPOINT.md` | 최대 10건 승인 Decision 배치 checkpoint |
| `HANDOFF.md` | 다른 세션/Executor가 이어받을 상태 |
| `ROADMAP.md` | milestone/단계 |
| `DEVELOPMENT_GATES.md` | 단계별 완료·검증 gate |
| `PROJECT_DOCUMENTATION_MAP.md` | 프로젝트 정본 지도 |
| `DESIGN_DOCUMENT_REGISTRY.json` | 구조화 설계 문서 registry |
| `SKILL_EXECUTION_REPORT.md` | 실제 Work Mode/Skill/Mode 사용 증거 |
| `LEGACY_ARTIFACT_RECONCILIATION.md` | 폐기·중복·고유 legacy 자료 이관 판정 |
| `PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md` | **COMPATIBILITY_ONLY legacy migration aid**; 신규 Sheet 설계 계약이 아님 |
| `GPT_WORK_PROJECT_MASTER_GDD_TWO_ARTIFACT_INSTRUCTION.md` | `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD` 선택 시 사용하는 붙여넣기용 전체 실행 지시문 |

## Vertical Slice 실행 진입점

프로젝트가 통합 Vertical Slice 구현·검증 단계에 들어가면 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md`를 canonical 실행 프롬프트 진입점으로 사용한다. 이 README는 해당 Prompt의 복사본을 소유하지 않으며, 프로젝트 운영 템플릿과 실제 Vertical Slice 실행 계약 사이의 링크만 유지한다.

## 설치 순서

```text
프로젝트 Repository 확인
→ 프로젝트 AGENTS / START_HERE / 실제 파일 확인
→ 저장소 루트의 [기획서] design root 확인
→ 정확한 Project Notion workspace와 Project relation 확인
→ templates/project-operations에서 필요한 최소 템플릿만 프로젝트에 적용
→ CURRENT_CONFIRMED_DECISIONS / ACTIVE_CONTEXT / Documentation Map 연결
→ 기존 legacy Sheet·HTML·Figma·custom Tool 자료가 있으면 UNIQUE/DUPLICATE/OBSOLETE 판정
→ UNIQUE만 현재 Notion/Repository owner로 이관
→ destination readback/Test + consumer/reference 확인
→ 프로젝트 작업 시작
```

`DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`를 명시적으로 선택한 master-GDD 작업에서는 기존 Notion의 `UNIQUE` 자료 유무만 확인하고, Notion 신규 출력·동기화 없이 policy의 2파일 순서로 진행한다.

Base 저장소 자체를 콜드 스타트할 때 이 디렉터리의 예시/빈 템플릿을 활성 프로젝트 상태로 오인하지 않는다.

## 승인 Decision 동기화

활성 Decision은 다음 순서를 기본으로 한다.

```text
사용자 승인
→ GitHub 추적
→ 활성 Branch의 CURRENT_CONFIRMED_DECISIONS + 분야 정본
→ 적용 가능한 NOTION_HUMAN_FACING_CANON record
→ destination readback
→ 논리 Commit
→ APPROVED_PENDING_MERGE
→ exact-head review / checks
→ merge
→ main readback + 적용 가능한 Notion readback
→ SYNCED_TO_MAIN
```

`DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD` profile의 master-GDD 산출 작업에서는 승인 Decision과 현재 구현 사실을 AI spec/repository owner에 추적하며 Notion 동기화는 완료 조건에서 제외한다.

`COMPATIBILITY_ONLY` legacy Sheet의 존재·쓰기 권한·행 상태는 active Decision sync 완료 조건이 아니다.

## Legacy Sheet 관련 파일

`templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`와 이 디렉터리의 `PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md` 같은 과거 Sheet surface는 새 프로젝트 기본 설치 경로가 아니다. 아직 이관되지 않은 legacy 정보를 해석·보존하는 호환 자료로만 취급한다. 해당 외부 템플릿의 장기 분류/Archive는 소유 Part/CP0가 별도로 결정해야 한다.

## Definition of Done

- 정확한 프로젝트 Repository와 Project Notion workspace를 구분했다.
- 사람용 `NOTION_HUMAN_FACING_CANON`과 구조화 `REPOSITORY_STRUCTURED_CANON`의 owner가 명확하다.
- 저장소 루트의 `[기획서]` design root가 유지된다.
- 승인 Decision은 Branch/Commit과 적용 가능한 Notion record에 추적된다.
- Notion write는 정확한 Project relation으로 격리되고 destination readback을 가진다.
- `NOTION_OPERATION_GATE`가 적용되어 object scope, bounded edit, readback, automation/webhook 역할이 구분된다.
- 사람용 Home과 AI/System 작업면이 섞이지 않으며 repository `runtime truth` 경계를 유지한다.
- Google Sheets는 `COMPATIBILITY_ONLY`이며 신규 입력·active sync·완료 판정에 필요하지 않다.
- legacy `UNIQUE` material은 현행 owner 이관·readback/Test·consumer 확인 없이 삭제하지 않는다.
- 실제로 수행하지 않은 runtime/사용자 검증은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 남긴다.
- 선택형 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`를 사용한 경우 두 파일·동일 ID/SHA·PDF-only download·Notion input-only 경계를 검증했다.
