---
name: managing-design-documents
description: Use when creating, restructuring, updating, publishing, or validating registered project and discipline design documents with one Markdown or JSON source of truth and policy-driven human publications.
---

# Managing Design Documents

## Core principle

기획 내용·책임 구조·발행은 하나의 문서 생명주기다. 문서 작성 Skill과 PDF 발행 Skill이 같은 Registry·원본·상태를 다시 판정하지 않는다.

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
```

## Responsibility contract

```text
AI·자동 검사 → DESIGN_DOCUMENT_REGISTRY.json·등록된 Markdown 또는 JSON 원본
사람 기본 열람 → Registry 정책이 요구하는 PDF
Word 검토 → 선언한 경우의 선택 DOCX
시각 자료 → 선언한 asset dir
최신성 → Publication Manifest
현재 상태 → Active Context
작업 순서 → Roadmap·Issue·Plan
반복 절차 → Project Skill
```

한 질문에는 현행 책임 원본 하나만 둔다. 같은 서술을 Markdown과 JSON 양쪽에 복제하지 않는다.

## Publication policy

- `source_only`: 내부 운영·라우팅 문서. `output_pdf`, `output_docx`, `publication_manifest`, `generator`는 `null`, `diagram_policy`는 `none`이다.
- `milestone_sync`: 주요 게이트·정기 검토·외부 공유 시 PDF와 Manifest를 동기화한다.
- `always_sync`: 원본·승인 이미지·생성기가 바뀐 같은 작업에서 PDF와 Manifest를 항상 재생성한다.

DOCX와 다이어그램은 Registry가 선언한 경우만 생성한다. `CURRENT`와 사람 시각 검수 완료는 독립 상태다.

## Workflow

### 1. Resolve responsibility before writing

1. 사용자 약속과 현재 문제를 한 문장으로 쓴다.
2. Registry와 Documentation Map에서 같은 질문의 기존 책임 원본을 찾는다.
3. 문서 ID·책임 범위·포함·제외를 확정한다.
4. 서술 중심이면 Markdown, 구조 검증·상태·ID·게임 데이터면 JSON을 선택한다.
5. 구현 사실, 승인 계획, 진행 중, 가설, 보류를 분리한다.

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

### 3. Restructure safely when needed

기존 문서·DOCX·PDF·이미지에만 남은 고유 결정·표·예외·보류를 대조한다. 감사와 사용자 승인 전에는 책임 원본 형식·경로를 강제 변경하거나 기존 본책을 제거하지 않는다.

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

### 6. Close the documentation loop

같은 작업에서 Registry, 관련 책임 원본, Roadmap, Project Skill, Active Context, Documentation Map과 발행 상태를 맞춘다.

## Output contract

```md
## 기획서 생명주기 결과
- 실행 mode:
- 문서 ID·책임 범위:
- 책임 원본·형식·경로:
- 발행 정책:
- 실제 변경:
- PDF·선택 DOCX·다이어그램:
- 승인 이미지·실제 캡처:
- Manifest·입력 해시:
- 자동 렌더·Codex·사람 검수:
- Roadmap·Skill·Context 연결:
- 미검증·불일치·제거 후보:
```

## Definition of Done

- Registry가 한 문서의 단일 책임 원본과 발행 정책을 선언한다.
- 같은 서술을 여러 형식의 독립 원본으로 유지하지 않는다.
- 문서 변경이 실제 파일·테스트·상태와 연결된다.
- 정책이 요구하는 발행본과 Manifest가 최신이다.
- 생성 실패가 기존 정상 산출물을 덮어쓰지 않는다.
- 새 작업자가 책임 원본과 사람용 출력·다음 작업을 찾는다.

## Failure conditions

- 같은 규칙을 여러 책임 원본에 장문 복사함
- `final`, `latest`, `v2` 활성 복제본을 만듦
- Registry에 등록되지 않은 새 본책을 만듦
- DOCX·PDF를 독립 책임 원본으로 수정함
- 문서 존재를 구현·검증 완료로 판단함
- 감사·보존 대조 없이 기존 프로젝트 문서를 변환함
- `CURRENT`를 사람 검수 완료로 해석함
- 전 페이지 렌더 없이 시각 검수를 통과 처리함
- `source_only` 문서에 불필요한 PDF·DOCX를 강제함
- `milestone_sync`를 일반 변경마다 `always_sync`처럼 강제함

## Legacy aliases

- `writing-game-design-documents` → `author`, `update`, `restructure`
- `publishing-discipline-bibles` → `publish`, `validate`

Tools:

- `tools/build_policy_driven_design_documents.py`
- `tools/build_design_documents.py`
- `tools/design_document_diagrams.py`
- `tools/check_publication_environment.py`
- `templates/project-operations/github/check_design_document_publications.py`
