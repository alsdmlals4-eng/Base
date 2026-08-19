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

## Repository design root

프로젝트가 Base 운영 템플릿을 채택할 때 설계 문서 폴더 `[기획서]`는 **저장소 루트**에 둔다. `templates/project-operations/` 자체나 중첩된 하위 폴더를 프로젝트의 활성 design root로 사용하지 않는다. Notion 사람용 workspace와 Repository `[기획서]` 구조화 문서는 서로 역할이 다르며, 어느 한쪽도 다른 쪽의 복사본으로 운영하지 않는다.

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

`COMPATIBILITY_ONLY` legacy Sheet의 존재·쓰기 권한·행 상태는 active Decision sync 완료 조건이 아니다.

## Legacy Sheet 관련 파일

`templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`와 이 디렉터리의 `PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md` 같은 과거 Sheet surface는 새 프로젝트 기본 설치 경로가 아니다. 아직 이관되지 않은 legacy 정보를 해석·보존하는 호환 자료로만 취급한다. 해당 외부 템플릿의 장기 분류/Archive는 소유 Part/CP0가 별도로 결정해야 한다.

## Definition of Done

- 정확한 프로젝트 Repository와 Project Notion workspace를 구분했다.
- 사람용 `NOTION_HUMAN_FACING_CANON`과 구조화 `REPOSITORY_STRUCTURED_CANON`의 owner가 명확하다.
- 저장소 루트의 `[기획서]` design root가 유지된다.
- 승인 Decision은 Branch/Commit과 적용 가능한 Notion record에 추적된다.
- Notion write는 정확한 Project relation으로 격리되고 destination readback을 가진다.
- Google Sheets는 `COMPATIBILITY_ONLY`이며 신규 입력·active sync·완료 판정에 필요하지 않다.
- legacy `UNIQUE` material은 현행 owner 이관·readback/Test·consumer 확인 없이 삭제하지 않는다.
- 실제로 수행하지 않은 runtime/사용자 검증은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 남긴다.
