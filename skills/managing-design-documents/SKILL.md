---
name: managing-design-documents
description: Use when authoring, restructuring, publishing, or validating registered design-document sources and their policy-driven derivatives.
---

# Managing Design Documents

## Core principle

기획 내용·책임 구조·사람용 표현·발행은 하나의 문서 생명주기다. 문서 작성 Skill과 PDF 발행 Skill이 같은 Registry·원본·상태를 다시 판정하지 않는다.

현재 프로젝트 권위 모델은 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`의 `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`다.

```text
REPOSITORY_PRIMARY_CANON
→ current Project Home content / decisions / Visual or Story Bible source / Flow or Storyboard source / Markdown / JSON / game data / code / scene / resource / test / runtime evidence

APPROVED_HUMAN_BLUEPRINT_PDF_CANON
→ 사람이 milestone에서 읽고 교정하는 exact-SHA PDF snapshot

NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE
→ existing unique material의 migration input 또는 명시적 V4 exception
```

승인된 기획 결정은 대화나 checkpoint 대기열에만 남기지 않는다. 결정 직후 GitHub 추적 근거와 `CURRENT_CONFIRMED_DECISIONS.md`, 영향받는 repository 책임 원본을 갱신하고 commit/readback한다. 사람이 실제로 이해·수정할 내용은 같은 source SHA의 PDF milestone view로 제공하며, PDF 교정은 repository source에 먼저 반영한 뒤 재발행한다. `V4_NOTION_EXCEPTION_ONLY` / `NO_NEW_NOTION_WRITE_BY_DEFAULT`: Notion은 V4 exception 또는 legacy migration scope에서만 사용하며 repository current decision을 대체하지 않는다.

공용 승인 동기화 계약은 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`, workspace 권위는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`, 사람용 PDF·시각 계약은 `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`를 따른다. V3 visual/Notion 자료는 compatibility/history 또는 V4 exception 경계에서만 읽는다.

Google Sheets는 `COMPATIBILITY_ONLY` migration source다. 기존 프로젝트에서 unique material이 남은 경우에만 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`를 사용한다.

## Modes

- `author`: 새 책임 원본을 설계하고 작성한다.
- `update`: 기존 책임 원본에 승인된 변경을 반영한다.
- `restructure`: 중복 책임과 경로를 감사하고 승인된 범위만 재배치한다.
- `publish`: 발행 정책에 따라 PDF·선택 DOCX·다이어그램·Manifest를 생성한다.
- `validate`: 내용·Schema·Notion readback·발행 최신성·전 페이지 렌더를 검수한다.

하나의 작업에서 필요한 mode를 순서대로 실행하되 같은 사실과 상태를 다시 판정하지 않는다.

## Required inputs

```yaml
project_repository:
notion_project_home: null-or-url
notion_human_surface: null-or-url
design_document_registry:
document_id:
source_path:
source_format: markdown/json
source_role:
responsibility_coverage:
publication_policy: source_only/milestone_sync/always_sync
approved_visuals:
actual_captures:
implementation_and_validation_evidence:
output_pdf: null-or-path
output_docx: null-or-path
diagram_policy: none/mermaid/generated
publication_manifest: null-or-path
generator: null-or-path
source_commit:
human_visual_review_required:
decision_tracking_surface: issue/pr/discussion/commit/null
current_confirmed_decisions:
notion_last_sync: null-or-date
google_sheet_compatibility_source: null-or-url
related_open_and_recent_prs:
subsystem_checkpoint: null-or-name
```

## Responsibility contract

```text
AI·자동 검사 → DESIGN_DOCUMENT_REGISTRY.json·등록된 Markdown 또는 JSON 원본
승인 결정 복원 → CURRENT_CONFIRMED_DECISIONS.md
현재 전체 그림·시각·예산·Tier·비교표 source → REPOSITORY_PRIMARY_CANON
사람용 milestone view → APPROVED_HUMAN_BLUEPRINT_PDF_CANON
실제 구현·runtime 상태 → REPOSITORY_RUNTIME_TRUTH
사람 기본 발행 열람 → Registry 정책이 요구하는 PDF
Word 검토 → 선언한 경우의 선택 DOCX
최신성 → Publication Manifest + repository SHA + PDF source SHA/readback
현재 상태 → Active Context
작업 순서 → Roadmap·Issue·Plan
반복 절차 → Project Skill
질문·승인 원문 추적 → GitHub Issue·PR·Discussion·commit
Google Sheets → COMPATIBILITY_ONLY migration source
```

repository의 등록된 Markdown·JSON structured source는 시스템 규칙·예외·수치의 **상세 책임 원본**이며, 사람용 PDF와 V4 exception/legacy migration 표현은 그 machine data를 독립적으로 재구현하지 않는다.

한 질문에는 **도메인별 active owner 하나**만 둔다. 같은 서술을 Markdown과 JSON 양쪽에 독립 원본으로 복제하지 않고, PDF와 V4 exception/legacy migration 표현도 machine data를 독립적으로 재구현하지 않는다.

GitHub 댓글·Issue·PR·Discussion은 승인 결정의 추적 근거이지 최종 책임 원본의 대체물이 아니다. repository는 현재 기획·구조화·구현 도메인의 정본이며 사람이 raw Markdown·JSON을 직접 읽어야만 프로젝트를 이해하도록 강제하지 않는다. PDF는 사람이 보는 파생본이고, Notion은 V4 exception 또는 legacy migration source일 뿐 runtime proof나 기본 정본이 아니다.

`CURRENT_CONFIRMED_DECISIONS.md`는 현재 승인 Decision의 핵심·대체 관계·상세 repository 정본 경로·Commit·PDF source SHA를 책임지고, 시스템 상세 규칙은 등록된 분야 원본이 책임진다. V4 exception/legacy migration 위치는 적용될 때만 보조 provenance로 기록한다.

## Legacy Notion and explicit exception responsibility

프로젝트 Notion은 기본 작업면이 아니다. `NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE`로서 이미 존재하는 고유 자료를 repository로 이관하거나, V4 exception gate가 explicit approval·owner·scope·measurable value·exit/revisit 조건을 기록한 경우에만 제한적으로 사용한다.

Project Home의 필수 구조는 `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`의 `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`을 따른다. 이 Skill은 Home을 짧은 상태·링크 허브로 재축약하지 않고, 프로젝트별 핵심 데이터와 AI 해석 교정면, 사용자 수정 경로까지 같은 사람용 projection 안에서 보존한다.

기본 책임은 다음과 같다.

```text
PROJECT HOME
→ HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN
→ PROJECT_SPECIFIC_CORE_DATA
→ AI_INTERPRETATION_FOR_USER_CORRECTION
→ HUMAN_EDIT_GUIDE_REQUIRED
→ 상태 / 핵심 재미 / 핵심 루프 / 핵심 시스템 / UX·Visual / 구현·검증 상태 / blocker·다음 작업 / 중요한 결정·위험

Visual or Story Bible
→ 승인된 시각·서사 North Star

Flow Map / Storyboard
→ 사람이 보는 화면·장면·관계 흐름

Asset / Reference / Benchmark
→ 승인 자산·재사용·근거·채택 판단

07+ project-specific confirmed tables
→ 예산 / Tier / 로스터 / 경제 / 성장 / 그 밖의 비교·학습 표
```

Notion V4 exception/legacy source에서 사람용 의미를 수정하면 먼저 `PROPOSED_LEGACY_CHANGE`로 해석한다. 새 기본 project planning과 사람용 Flow/Wireframe은 repository primary owner에서 관리한다. 예외 source의 수정이 spec/data/runtime 동작을 바꾸면 Decision ID와 영향 경로를 확인하고 repository를 `SYNC_BEFORE_IMPLEMENTATION`으로 동기화한 뒤 `SYNCED`로 올린다.

예산표·Tier표에는 가능하면 `CONFIRMED / PROVISIONAL / DEFERRED / REJECTED`, Decision ID 또는 canonical path, source main SHA/freshness locator, derived PDF 또는 실제 V4 exception readback을 함께 남긴다.

## Google Sheets compatibility responsibility

Google Sheets는 새 프로젝트의 기본 GDD 작업면이 아니다. 기존 unique material이 남은 migration source만 `COMPATIBILITY_ONLY`로 읽는다.

- Sheet-only 수정은 자동 canon 승격하지 않는다.
- unique material은 repository 책임면으로 이관하고 destination readback한다. Notion destination은 실제 V4 exception일 때만 추가한다.
- duplicate/obsolete material은 현재 정본으로 승격하지 않는다.
- migration 완료 뒤 Sheet freshness를 일반 프로젝트 DoD에 강제하지 않는다.

## Publication policy

- `source_only`: 내부 운영·라우팅 문서. `output_pdf`, `output_docx`, `publication_manifest`, `generator`는 `null`, `diagram_policy`는 `none`이다.
- `milestone_sync`: 주요 게이트·정기 검토·외부 공유 시 PDF와 Manifest를 동기화한다.
- `always_sync`: 원본·승인 이미지·생성기가 바뀐 같은 작업에서 PDF와 Manifest를 항상 재생성한다.

DOCX와 다이어그램은 Registry가 선언한 경우만 생성한다. `CURRENT`, exact-SHA derived PDF, runtime 검증, 사람 시각 검수 완료는 서로 독립 상태다.

승인 결정의 즉시 정본화와 PDF·DOCX 발행 주기는 별개다. `milestone_sync` 문서라도 승인 Decision은 즉시 repository primary owner에 반영하고, 파생 발행본은 정책이 정한 시점에 생성한다. Notion write는 V4 exception/migration scope가 실제로 있을 때만 별도 수행한다.

## Workflow

### 1. Resolve responsibility before writing

1. 사용자 약속과 현재 문제를 한 문장으로 쓴다.
2. 최신 `main`, 동일 Goal의 열린 PR, 최근 병합 PR을 확인한다.
3. `CURRENT_CONFIRMED_DECISIONS.md`, Registry와 Documentation Map에서 같은 질문의 기존 Decision과 구조화 책임 원본을 찾는다.
4. 관련 repository 사람이 보는 문서·Flow/Wireframe·Asset catalog과 필요한 exact-SHA derived view를 읽는다. 실제 V4 exception/migration source가 있으면 그 scope만 추가로 읽는다.
5. Google Sheets는 `COMPATIBILITY_ONLY`이고 unique migration material이 실제로 남은 경우에만 추가로 확인한다.
6. 문서 ID·책임 범위·포함·제외와 repository primary owner, 필요한 derived view 또는 actual exception boundary를 확정한다.
7. 서술 중심 structured source는 Markdown, 구조 검증·상태·ID·game data는 JSON을 선택한다.
8. 구현 사실, 승인 계획, 진행 중, 가설, 보류를 분리한다.

기존 Decision이 유효하면 같은 질문을 다시 사용자에게 묻지 않는다. 기술 세부·초기 시험값은 `RECOMMENDED_DEFAULT`, 프로젝트 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분류한다.

### 2. Author or update the canonical source

```text
목적
→ 경험
→ 규칙
→ 흐름
→ 예외
→ 실제 경로
→ 사람용 표현
→ 검증
→ 다음 단계
```

- 세부 코드·데이터·자산·테스트는 경로로 연결하고 전문을 복제하지 않는다.
- 승인 이미지와 실제 캡처는 Asset ID·상태·채택 범위를 기록한다.
- 작은 기능은 새 본책을 만들지 않고 기존 책임 원본 Section과 작업 계약에 차이를 기록한다.
- 승인 문구가 없는 제안·가설은 승인 Decision과 분리한다.
- 사람이 비교·학습해야 하는 예산·Tier·로스터·경제·성장 정보는 repository-native 표와 필요한 derived PDF를 우선 고려한다.
- V4 exception Notion 표는 machine-consumed JSON/game data의 별도 복제 구현이 아니다.

### 2A. Preserve approved decisions immediately

승인·수정된 Decision이 발생하면 다음 순서로 운영한다.

```text
사용자 승인·수정
→ 현재 GitHub 추적 surface에 답변 원문·Decision 상태 즉시 기록
→ Decision ID·날짜·영향 분야·대체 범위 연결
→ CURRENT_CONFIRMED_DECISIONS.md 갱신
→ 영향받는 repository 분야 책임 원본 / structured data / Flow·Wireframe 갱신
→ 필요한 Active Context·작업 계약 갱신
→ branch PR exact-head review·checks·squash merge
→ 새 main HEAD·Commit SHA 재조회
→ 필요한 exact-SHA derived PDF 또는 repository-native 사람용 view 갱신
→ 실제 V4 exception/migration write가 있었다면 destination readback
→ Decision·Commit·derived view/exception 표현·대체 관계 대조
→ SYNCED / PROPOSED_LEGACY_CHANGE / SYNC_FAILED / BLOCKED_UNVERIFIED 판정
```

- 기록에는 규칙, 공식, 예시, 예외, 대체되는 이전 Decision, 미결정 항목을 포함한다.
- 최신 승인 Decision이 이전 기록과 충돌하면 최신 결정을 반영하고 대체 범위를 명시한다.
- 승인 Decision을 하위 시스템 checkpoint까지 임시 누적하지 않는다.
- 댓글 기록만 존재하는 상태를 책임 원본 갱신 완료로 보고하지 않는다.
- repository primary owner만 갱신했는데 필요한 derived view가 오래됐거나, 반대로 exception source만 의미 변경했는데 repository 반영이 필요한 상태를 `SYNCED`로 보고하지 않는다.
- 실제로 수행하지 않은 검수·플레이테스트·CI·derived view/exception readback은 `UNVERIFIED`를 유지한다.
- 동기화가 실패하면 `SYNC_FAILED` 또는 `BLOCKED_UNVERIFIED`와 재개 조건을 남긴다.
- `SYNCED`가 아닌 승인 건이 있으면 비차단 질문을 계속 늘리지 않는다.

직접 `main` 반영 허용 범위와 반드시 구현 PR을 사용하는 범위는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다.

### 2B. Use subsystem checkpoints as audit, not delayed promotion

전투·성장·경제·진행·콘텐츠 등 하나의 하위 시스템 기획이 마무리되면 checkpoint를 실행한다. checkpoint는 이미 즉시 정본화된 Decision을 다시 승격하는 단계가 아니라 다음을 감사하는 단계다.

- 누적 Decision ID와 구조화 책임 원본 반영 위치 일치
- 필요한 derived PDF/repository-native 표·Flow·Wireframe·Visual 또는 실제 exception record가 해당 도메인의 현재 Decision과 일치
- 누락·충돌·중복·대체 누락 0건
- GitHub `main`과 필요한 derived view/exception readback 일치
- 미결정·보류·기각 항목 보존
- 관련 구현·테스트·발행 상태 구분

장기 작업에서는 checkpoint를 주기적으로 실행하되 기획 완료나 구현 승인을 의미하지 않는다.

### 2C. Use the L2 feature-detail contract only after cheaper uncertainty is reduced

PoC·benchmark·적대적 검토 뒤 `KEEP / CHANGE / RETEST`로 살아남고 production handoff가 필요한 **주요 L2 기능**은 `templates/planning/GAME_FEATURE_DESIGN_SPEC.md`를 사용해 상세 구조화 책임 원본을 작성하거나 기존 분야 원본에 같은 구조를 적용한다.

```text
L0 Project Direction
→ L1 Feature Brief
→ benchmark / PoC / adversarial review
→ L2 GAME_FEATURE_DESIGN_SPEC
→ approval
→ L3 FEATURE_SPEC_TRACEABILITY_PACKET
```

- pre-PoC 아이디어, L0·L1 단순 변경, `REMOVE / DEFER` 항목에는 L2 Spec을 강제하지 않는다.
- Feature Spec은 플레이어 문제·경험 의도·Player Verbs·Entry/Exit/Cancel/Re-entry·State & Rules·피드백·실패/복구·edge case·Data & Balance·Acceptance Criteria·Cut-down을 책임진다.
- Feature Spec은 **Task progress, 구현 파일 완료 여부, PR 상태, executed verification 결과를 소유하지 않는다.** 이 상태는 승인 뒤 Traceability Packet과 실제 구현·테스트가 책임진다.
- 전투 AI·UX/UI·아트·오디오·서사 등 전문 분야 정본이 같은 질문을 더 정확하게 소유하면 Feature Spec은 해당 정본의 ID·경로·Section을 reference/compose하고 전문을 복제하지 않는다.
- Notion에는 Feature ID·Decision ID·핵심 상태·사람이 이해해야 하는 수치·canonical path를 요약/시각화하고 상세 machine 전문을 복제하지 않는다.

### 3. Restructure safely when needed

기존 문서·DOCX·PDF·이미지·Notion·legacy Sheet에만 남은 고유 Decision·표·예외·보류를 대조한다. 감사와 사용자 승인 전에는 책임 원본 형식·경로를 강제 변경하거나 기존 본책을 제거하지 않는다.

구조 변경 전 동일 Goal의 열린 PR과 최근 병합 PR을 확인한다. 같은 변경이 진행 중이면 새 PR을 만들지 않고 기존 PR을 재사용한다.

### 4. Publish by policy

정책 선택기는 `tools/build_policy_driven_design_documents.py`다.

```text
기본 실행
→ always_sync만 생성

--include-milestone
→ always_sync + milestone_sync 생성

--only <document-id>
→ 지정한 milestone_sync 또는 always_sync 생성

source_only
→ 생성 대상이 아니며 요청 시 오류
```

1. Markdown은 H1·필수 Section·로컬 이미지·선택 Mermaid를 검증한다.
2. JSON은 등록된 Schema로 검증한다.
3. 환경과 생성기 의존성을 사전 점검한다.
4. 정책 선택기가 발행 대상만 임시 Registry로 분리한다.
5. 기존 `build_design_documents.py`가 임시 디렉터리에서 선택 DOCX·PDF·자산을 생성한다.
6. PDF 전 페이지를 렌더하고 빈 페이지·한글·표·이미지 잘림을 확인한다.
7. 모든 검증 성공 뒤 출력과 Manifest를 원자적으로 교체한다.
8. 동일 입력 정상 재실행에서 추적 파일 diff 0을 확인한다.
9. 사용자가 직접 확인하지 않았다면 `human_visual_review: NOT_RUN`을 유지한다.

### 5. Validate by policy

- `source_only`: 원본·Schema·등록·링크를 검증하며 Manifest를 요구하지 않는다.
- `milestone_sync`: 일반 작업에서는 Manifest 부재·STALE를 허용하고, 주요 게이트 설정에서는 `CURRENT`와 전 페이지 렌더를 요구한다.
- `always_sync`: 항상 `CURRENT`, 자동 렌더 `PASSED`, 현재 입력·생성기·출력 해시를 요구한다.

승인 Decision 변경에서는 발행 정책과 별개로 다음을 검증한다.

- `CURRENT_CONFIRMED_DECISIONS.md`와 repository 분야 원본 일치
- Decision ID·대체 관계·Commit SHA 일치
- GitHub 댓글의 승인 원문·반영 위치 존재
- 필요한 derived view/exception readback과 current Decision 일치
- exception/legacy 의미 변경이 repository structured/runtime 변경을 요구할 경우 `SYNC_BEFORE_IMPLEMENTATION` 충족
- Google Sheets가 migration source로 실제 사용된 경우에만 이관 destination readback
- 동일 Goal의 중복 PR·중복 질문 부재

### 6. Close the documentation loop

같은 작업에서 Registry, 관련 repository 책임 원본, `CURRENT_CONFIRMED_DECISIONS.md`, 필요한 PDF milestone view 또는 적용 가능한 V4 exception/legacy migration source, Roadmap, Project Skill, Active Context, Documentation Map과 발행 상태를 맞춘다.

하위 시스템 checkpoint에서는 누적 GitHub Decision ID와 책임 원본 반영 위치, PDF source SHA 또는 적용 가능한 V4 exception/legacy migration provenance를 대조하고 미반영·충돌·중복·대체 누락을 0으로 만든다. 미결정 항목은 삭제하지 않고 명시적으로 보류한다.

PR 또는 직접 `main` Decision Commit 뒤에는 `running-adversarial-review-and-refinement`로 최근 승인 누락·repository/PDF source drift·적용 가능한 V4 exception/legacy migration drift·회귀를 검사한다.

## Output contract

```md
## 기획서 생명주기 결과
- 실행 mode:
- 문서 ID·책임 범위:
- authority domain: REPOSITORY_PRIMARY_CANON | APPROVED_HUMAN_BLUEPRINT_PDF_CANON | LEGACY_NOTION_MIGRATION | V4_NOTION_EXCEPTION
- 책임 원본·형식·경로:
- CURRENT_CONFIRMED_DECISIONS 반영:
- PDF milestone view / V4 exception·legacy migration surface:
- PDF source SHA / applicable migration readback:
- 발행 정책:
- 실제 변경:
- 승인 Decision 추적 surface·ID:
- 기존 Decision·PR·repository/PDF source·applicable migration 비교:
- main Commit SHA:
- Google Sheets compatibility migration: NOT_USED | USED + source/destination
- 동기화 상태:
- 하위 시스템 checkpoint·감사 범위:
- 누락·충돌·중복·대체 검수:
- PDF·선택 DOCX·다이어그램:
- 승인 이미지·실제 캡처:
- Manifest·입력 해시:
- 자동 렌더·Codex·사람 검수:
- Roadmap·Skill·Context 연결:
- 병합 후 적대적 검토:
- 미검증·불일치·제거 후보:
```

## Definition of Done

- Registry가 한 structured 문서의 단일 책임 원본과 발행 정책을 선언한다.
- 같은 서술을 여러 structured 형식의 독립 원본으로 유지하지 않는다.
- 사람용 전체 그림·Visual·예산·Tier·비교표는 repository-native 문서와 exact-SHA PDF derived view에서 찾을 수 있으며, V4 exception Notion은 실제 승인된 scope에서만 보조한다.
- 문서 변경이 실제 파일·테스트·상태와 연결된다.
- 질문 전에 기존 Decision·repository 정본·열린 PR·최근 병합 PR·필요한 derived view/exception source를 대조했다.
- 승인 Decision이 GitHub 추적 근거에 기록됐다.
- 승인 Decision이 즉시 `CURRENT_CONFIRMED_DECISIONS.md`와 분야 책임 원본에 반영됐다.
- 승인 구조화 문서가 PR을 거쳐 `main`에 반영되고 Commit SHA가 기록됐다.
- 필요한 derived PDF/repository-native view를 갱신하고, 실제 exception write만 destination readback 결과가 일치한다.
- exception/legacy 변경이 structured/runtime 변경을 요구하면 구현 전 repository 동기화를 완료했다.
- Google Sheets는 compatibility migration이 필요한 경우에만 사용했다.
- checkpoint 대조 결과 미반영·충돌·중복·대체 누락이 없다.
- 정책이 요구하는 발행본과 Manifest가 최신이다.
- 생성 실패가 기존 정상 산출물을 덮어쓰지 않는다.
- 병합 뒤 적대적 검토와 회귀 재검사를 실행했다.
- 새 작업자가 repository primary 책임 원본과 필요한 derived view/exception source·다음 작업을 모두 찾는다.

## Failure conditions

- 같은 규칙을 여러 structured 책임 원본에 장문 복사함
- `final`, `latest`, `v2` 활성 복제본을 만듦
- Registry에 등록되지 않은 새 본책을 만듦
- DOCX·PDF를 독립 structured 책임 원본으로 수정함
- 문서·Notion 페이지 존재를 구현·검증 완료로 판단함
- 기존 Decision·PR·Notion을 확인하지 않고 같은 질문을 반복함
- 기술 세부·초기 시험값을 사용자 결정으로 전가함
- 승인 Decision을 대화나 댓글에만 남기고 정본을 갱신하지 않음
- 승인 Decision을 checkpoint까지 임시 누적함
- `CURRENT_CONFIRMED_DECISIONS.md`만 갱신하고 분야 책임 원본을 누락함
- 사람이 보는 예산·Tier·Flow/Wireframe의 의미가 바뀌었는데 repository-native view 또는 필요한 derived PDF를 갱신하지 않음
- exception/legacy source에서 structured/runtime 의미를 바꾸고 repository 동기화 없이 구현함
- repository 또는 필요한 derived view/exception source 한쪽만 갱신하고 `SYNCED`로 주장함
- Google Sheets를 새 기본 GDD workspace로 복원함
- checkpoint에서 누적 Decision의 누락·충돌·중복·대체 범위를 대조하지 않음
- 감사·보존 대조 없이 기존 프로젝트 문서를 변환함
- `CURRENT`를 사람 검수 완료로 해석함
- 전 페이지 렌더 없이 시각 검수를 통과 처리함
- `source_only` 문서에 불필요한 PDF·DOCX를 강제함
- `milestone_sync`를 일반 변경마다 `always_sync`처럼 강제함
- 병합 뒤 정본·최근 승인·Notion·회귀 비교를 생략함

## Legacy aliases

- `writing-game-design-documents` → `author`, `update`, `restructure`
- `publishing-discipline-bibles` → `publish`, `validate`

Tools:

- `tools/build_policy_driven_design_documents.py`
- `tools/build_design_documents.py`
- `tools/design_document_diagrams.py`
- `tools/check_publication_environment.py`
- `templates/project-operations/github/check_design_document_publications.py`

## BCP-008 명세 추적성 문서 경계

`templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`은 L2 이상 작업의 Decision·Requirement·Acceptance·Task·구현·검증 연결을 표시하는 비정본 파생 Packet이다. **상세 구조화 책임 원본**의 규칙·예외·수치·상태를 복제하지 않고 `canonical_source`와 정확한 Section·ID만 연결한다.

- 승인 Decision은 `CURRENT_CONFIRMED_DECISIONS.md`와 repository primary 분야 owner에 즉시 반영하고, 사람이 봐야 하는 변화는 필요한 exact-SHA derived PDF 또는 repository-native view에 동기화한다.
- Packet의 `coverage_status=CONVERGED`는 문서가 많다는 뜻이 아니라 모든 승인 Requirement가 실제 경로와 검증 증거에 연결됐다는 뜻이다.
- 상세 정본과 Packet이 충돌하면 상세 정본을 기준으로 Packet을 `GAP` 또는 `BLOCKED_UNVERIFIED`로 낮춘다.
- 작은 L0·L1 문서 수정에는 Packet을 만들지 않는다.

<!-- FEDERATED_DUAL_CANON_ROUTE -->

> V4 authority route: `FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER`. `REPOSITORY_EXECUTION_DATA_CANON` owns editable structured, execution, runtime, work-status, and evidence facts. Only a `USER_APPROVED_AND_MANIFEST_REGISTERED` `APPROVED_HUMAN_BLUEPRINT_PDF_CANON` owns the immutable human visual/review baseline. `ONE_EDITABLE_OWNER_PER_ATOMIC_FACT`; `CANDIDATE_PDF_NOT_CANON` and PDF annotations do not mutate repository-owned facts. See `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` and `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`.
