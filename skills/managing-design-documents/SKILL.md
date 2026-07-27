---
name: managing-design-documents
description: Use when creating, restructuring, updating, publishing, or validating registered project and discipline design documents with one Markdown or JSON source of truth and policy-driven human publications.
---

# Managing Design Documents

## Core principle

기획 내용·책임 구조·발행은 하나의 문서 생명주기다. 문서 작성 Skill과 PDF 발행 Skill이 같은 Registry·원본·상태를 다시 판정하지 않는다.

승인된 기획 결정은 대화나 checkpoint 대기열에만 남기지 않는다. 결정 직후 GitHub 추적 근거를 남기고, `CURRENT_CONFIRMED_DECISIONS.md`, 영향받는 책임 원본, 허용되는 경우 `main`, 프로젝트 Google Sheets까지 같은 승인 단위에서 동기화한다.

공용 승인 동기화 계약은 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다.

## Modes

- `author`: 새 책임 원본을 설계하고 작성한다.
- `update`: 기존 책임 원본에 승인된 변경을 반영한다.
- `restructure`: 중복 책임과 경로를 감사하고 승인된 범위만 재배치한다.
- `publish`: 발행 정책에 따라 PDF·선택 DOCX·다이어그램·Manifest를 생성한다.
- `validate`: 내용·Schema·발행 최신성·전 페이지 렌더를 검수한다.

하나의 작업에서 필요한 mode를 순서대로 실행하되 같은 사실과 상태를 다시 판정하지 않는다.

## Required inputs

```yaml
project_repository:
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
google_sheet:
related_open_and_recent_prs:
subsystem_checkpoint: null-or-name
```

## Responsibility contract

```text
AI·자동 검사 → DESIGN_DOCUMENT_REGISTRY.json·등록된 Markdown 또는 JSON 원본
승인 결정 복원 → CURRENT_CONFIRMED_DECISIONS.md
사람 기본 열람 → Registry 정책이 요구하는 PDF
Word 검토 → 선언한 경우의 선택 DOCX
시각 자료 → 선언한 asset dir
최신성 → Publication Manifest
현재 상태 → Active Context
작업 순서 → Roadmap·Issue·Plan
반복 절차 → Project Skill
질문·승인 원문 추적 → GitHub Issue·PR·Discussion·commit
사용자 작업면 → 프로젝트 Google Sheets
```

한 질문에는 현행 책임 원본 하나만 둔다. 같은 서술을 Markdown과 JSON 양쪽에 복제하지 않는다.

GitHub 댓글·Issue·PR·Discussion은 승인 결정의 추적 근거이지 최종 책임 원본의 대체물이 아니다. Google Sheets도 상세 책임 원본을 대체하지 않으며 GitHub 정본의 동기화 작업면으로 사용한다.

`CURRENT_CONFIRMED_DECISIONS.md`는 현재 승인 Decision의 핵심·대체 관계·상세 정본 경로·Commit·Sheet 위치를 책임지고, 시스템 상세 규칙은 등록된 분야 원본이 책임진다.

## Publication policy

- `source_only`: 내부 운영·라우팅 문서. `output_pdf`, `output_docx`, `publication_manifest`, `generator`는 `null`, `diagram_policy`는 `none`이다.
- `milestone_sync`: 주요 게이트·정기 검토·외부 공유 시 PDF와 Manifest를 동기화한다.
- `always_sync`: 원본·승인 이미지·생성기가 바뀐 같은 작업에서 PDF와 Manifest를 항상 재생성한다.

DOCX와 다이어그램은 Registry가 선언한 경우만 생성한다. `CURRENT`와 사람 시각 검수 완료는 독립 상태다.

승인 결정의 즉시 정본화와 PDF·DOCX 발행 주기는 별개다. `milestone_sync` 문서라도 승인 Decision은 즉시 Markdown·JSON 정본에 반영하고, 파생 발행본은 정책이 정한 시점에 생성한다.

## Workflow

### 1. Resolve responsibility before writing

1. 사용자 약속과 현재 문제를 한 문장으로 쓴다.
2. 최신 `main`, 동일 Goal의 열린 PR, 최근 병합 PR을 확인한다.
3. `CURRENT_CONFIRMED_DECISIONS.md`, Registry와 Documentation Map에서 같은 질문의 기존 Decision과 책임 원본을 찾는다.
4. 프로젝트가 Google Sheets를 사용하면 마지막 Decision ID·Commit·행을 확인한다.
5. 문서 ID·책임 범위·포함·제외를 확정한다.
6. 서술 중심이면 Markdown, 구조 검증·상태·ID·게임 데이터면 JSON을 선택한다.
7. 구현 사실, 승인 계획, 진행 중, 가설, 보류를 분리한다.

기존 Decision이 유효하면 같은 질문을 다시 사용자에게 묻지 않는다. 기술 세부·초기 시험값은 `RECOMMENDED_DEFAULT`, 프로젝트 코어·중요 기획·방향성·정본 충돌은 `USER_DECISION_REQUIRED`로 분류한다.

### 2. Author or update the canonical source

```text
목적
→ 경험
→ 규칙
→ 흐름
→ 예외
→ 실제 경로
→ 검증
→ 다음 단계
```

- 세부 코드·데이터·자산·테스트는 경로로 연결하고 전문을 복제하지 않는다.
- 승인 이미지와 실제 캡처는 Asset ID·상태·채택 범위를 기록한다.
- 작은 기능은 새 본책을 만들지 않고 기존 책임 원본 Section과 작업 계약에 차이를 기록한다.
- 승인 문구가 없는 제안·가설은 승인 Decision과 분리한다.

### 2A. Preserve approved decisions immediately

승인·수정된 Decision이 발생하면 다음 순서로 운영한다.

```text
사용자 승인·수정
→ 현재 GitHub 추적 surface에 답변 원문·Decision 상태 즉시 기록
→ Decision ID·날짜·영향 분야·대체 범위 연결
→ CURRENT_CONFIRMED_DECISIONS.md 갱신
→ 영향받는 분야 책임 원본 갱신
→ 필요한 Active Context·작업 계약 갱신
→ 직접 main 허용 범위면 논리 Commit 하나로 반영
→ 새 main HEAD·Commit SHA 재조회
→ 프로젝트 Google Sheets 행 추가·수정
→ Sheet 행 재조회
→ Decision·Commit·대체 관계 대조
→ GitHub 댓글에 반영 위치와 SYNCED 판정 기록
```

- 기록에는 규칙, 공식, 예시, 예외, 대체되는 이전 Decision, 미결정 항목을 포함한다.
- 최신 승인 Decision이 이전 기록과 충돌하면 최신 결정을 반영하고 대체 범위를 명시한다.
- 승인 Decision을 하위 시스템 checkpoint까지 임시 누적하지 않는다.
- 댓글 기록만 존재하는 상태를 책임 원본 갱신 완료로 보고하지 않는다.
- GitHub만 또는 Sheets만 갱신한 상태를 `SYNCED`로 보고하지 않는다.
- 실제로 수행하지 않은 검수·플레이테스트·CI·Sheets 재조회는 `UNVERIFIED`를 유지한다.
- 동기화가 실패하면 `SYNC_FAILED` 또는 `BLOCKED_UNVERIFIED`와 재개 조건을 남긴다.
- `SYNCED`가 아닌 승인 건이 있으면 비차단 질문을 계속 늘리지 않는다.

직접 `main` 반영 허용 범위와 반드시 구현 PR을 사용하는 범위는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다.

### 2B. Use subsystem checkpoints as audit, not delayed promotion

전투·성장·경제·진행·콘텐츠 등 하나의 하위 시스템 기획이 마무리되면 checkpoint를 실행한다. checkpoint는 이미 즉시 정본화된 Decision을 다시 승격하는 단계가 아니라 다음을 감사하는 단계다.

- 누적 Decision ID와 책임 원본 반영 위치 일치
- 누락·충돌·중복·대체 누락 0건
- GitHub `main`과 Google Sheets 일치
- 미결정·보류·기각 항목 보존
- 관련 구현·테스트·발행 상태 구분

장기 작업에서는 checkpoint를 주기적으로 실행하되 기획 완료나 구현 승인을 의미하지 않는다.

### 3. Restructure safely when needed

기존 문서·DOCX·PDF·이미지에만 남은 고유 Decision·표·예외·보류를 대조한다. 감사와 사용자 승인 전에는 책임 원본 형식·경로를 강제 변경하거나 기존 본책을 제거하지 않는다.

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

- `CURRENT_CONFIRMED_DECISIONS.md`와 분야 원본 일치
- Decision ID·대체 관계·Commit SHA 일치
- GitHub 댓글의 승인 원문·반영 위치 존재
- Google Sheets 재조회 결과 일치
- 동일 Goal의 중복 PR·중복 질문 부재

### 6. Close the documentation loop

같은 작업에서 Registry, 관련 책임 원본, `CURRENT_CONFIRMED_DECISIONS.md`, Roadmap, Project Skill, Active Context, Documentation Map과 발행 상태를 맞춘다.

하위 시스템 checkpoint에서는 누적 GitHub Decision ID와 책임 원본 반영 위치를 대조하고, 미반영·충돌·중복·대체 누락을 0으로 만든다. 미결정 항목은 삭제하지 않고 명시적으로 보류한다.

PR 또는 직접 `main` Decision Commit 뒤에는 `running-adversarial-review-and-refinement`로 최근 승인 누락·정본 충돌·Sheets 불일치·회귀를 검사한다.

## Output contract

```md
## 기획서 생명주기 결과
- 실행 mode:
- 문서 ID·책임 범위:
- 책임 원본·형식·경로:
- CURRENT_CONFIRMED_DECISIONS 반영:
- 발행 정책:
- 실제 변경:
- 승인 Decision 추적 surface·ID:
- 기존 Decision·PR·Sheet 비교:
- main Commit SHA:
- Google Sheets tab·row·재조회:
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

- Registry가 한 문서의 단일 책임 원본과 발행 정책을 선언한다.
- 같은 서술을 여러 형식의 독립 원본으로 유지하지 않는다.
- 문서 변경이 실제 파일·테스트·상태와 연결된다.
- 질문 전에 기존 Decision·정본·열린 PR·최근 병합 PR·Sheets를 대조했다.
- 승인 Decision이 GitHub 추적 근거에 기록됐다.
- 승인 Decision이 즉시 `CURRENT_CONFIRMED_DECISIONS.md`와 분야 책임 원본에 반영됐다.
- 승인 문서가 `main`에 반영되고 Commit SHA가 기록됐다.
- Google Sheets를 갱신하고 재조회 결과가 일치한다.
- checkpoint 대조 결과 미반영·충돌·중복·대체 누락이 없다.
- 정책이 요구하는 발행본과 Manifest가 최신이다.
- 생성 실패가 기존 정상 산출물을 덮어쓰지 않는다.
- 병합 뒤 적대적 검토와 회귀 재검사를 실행했다.
- 새 작업자가 책임 원본과 사람용 출력·다음 작업을 찾는다.

## Failure conditions

- 같은 규칙을 여러 책임 원본에 장문 복사함
- `final`, `latest`, `v2` 활성 복제본을 만듦
- Registry에 등록되지 않은 새 본책을 만듦
- DOCX·PDF를 독립 책임 원본으로 수정함
- 문서 존재를 구현·검증 완료로 판단함
- 기존 Decision·PR·Sheets를 확인하지 않고 같은 질문을 반복함
- 기술 세부·초기 시험값을 사용자 결정으로 전가함
- 승인 Decision을 대화나 댓글에만 남기고 정본을 갱신하지 않음
- 승인 Decision을 checkpoint까지 임시 누적함
- `CURRENT_CONFIRMED_DECISIONS.md`만 갱신하고 분야 책임 원본을 누락함
- GitHub 또는 Sheets 한쪽만 갱신하고 `SYNCED`로 주장함
- checkpoint에서 누적 Decision의 누락·충돌·중복·대체 범위를 대조하지 않음
- 감사·보존 대조 없이 기존 프로젝트 문서를 변환함
- `CURRENT`를 사람 검수 완료로 해석함
- 전 페이지 렌더 없이 시각 검수를 통과 처리함
- `source_only` 문서에 불필요한 PDF·DOCX를 강제함
- `milestone_sync`를 일반 변경마다 `always_sync`처럼 강제함
- 병합 뒤 정본·최근 승인·Sheets·회귀 비교를 생략함

## Legacy aliases

- `writing-game-design-documents` → `author`, `update`, `restructure`
- `publishing-discipline-bibles` → `publish`, `validate`

Tools:

- `tools/build_policy_driven_design_documents.py`
- `tools/build_design_documents.py`
- `tools/design_document_diagrams.py`
- `tools/check_publication_environment.py`
- `templates/project-operations/github/check_design_document_publications.py`
