---
name: publishing-discipline-bibles
description: Use when creating, refreshing, or validating project and discipline bibles whose AI source is structured JSON and whose human-readable outputs are DOCX, PDF, diagrams, approved images, and publication manifests.
---

# Publishing Structured Project and Discipline Bibles

## Core principle

기획서 본책은 **AI용 구조화 JSON 책임 원본**이고, 사람은 같은 JSON에서 생성한 **DOCX·PDF·다이어그램·승인 이미지 통합본**을 본다.

공용 방법: `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`

템플릿·도구:

- `templates/project-operations/DESIGN_DOCUMENT.json`
- `templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json`
- `tools/build_design_documents.py`
- `tools/design_document_diagrams.py`
- `templates/project-operations/github/check_design_document_publications.py`

## Trigger

- 프로젝트 종합 기획서 또는 분야별 본책 신규 생성
- JSON 기획 내용, 승인 이미지, 실제 캡처 또는 생성기가 변경됨
- DOCX·PDF가 현재 JSON보다 오래됐는지 검수
- 사람이 이미지와 다이어그램을 포함한 최신 통합본을 요청
- Markdown 본책을 구조화 JSON + DOCX/PDF로 안전하게 마이그레이션
- 주요 개발 게이트 전 사람용 기획서 패키지 검수

## Do not use

- 운영 라우터 Markdown 한 줄 수정
- JSON·승인 이미지·생성기에 변화가 없고 Manifest가 `CURRENT`
- 기존 프로젝트 본책을 감사·승인 없이 강제 변환
- 실제 구현 상태를 확인하지 않고 완료형 문서를 제작
- PDF 또는 DOCX를 독립 책임 원본으로 수동 유지하려는 작업

## Required inputs

```yaml
project_repository:
design_document_registry:
document_id:
source_json:
responsibility_coverage:
approved_visuals:
actual_captures:
asset_directory:
skill_registry:
development_gates:
implementation_and_validation_evidence:
output_docx:
output_pdf:
publication_manifest:
source_commit:
human_visual_review_required:
```

## Phase 1 — Responsibility audit

- `DESIGN_DOCUMENT_REGISTRY.json`에서 문서 ID·분야·책임 범위·경로를 확인한다.
- 기존 Markdown·DOCX·PDF에만 남은 고유 결정·표·이미지·보류를 조사한다.
- 사용자 승인 전 기존 본책을 삭제하거나 대규모 축약하지 않는다.
- 프로젝트 전체와 11개 분야 책임이 누락 없이 등록됐는지 확인한다.
- 통합 본책은 `responsibility_coverage`로 담당 범위를 명시한다.

원본이 불명확하면 발행보다 안전 마이그레이션·책임 원본 정리를 먼저 수행한다.

## Phase 2 — Structure the JSON source

`DESIGN_DOCUMENT.json` 계약에 따라 다음을 구조화한다.

```text
문서 메타데이터
→ 목적·플레이어 가치·현재 목표
→ Quality Bar·금지 방향
→ 책임·비책임·협업 계약
→ 분야 전체 작업 과정
→ 작업·제품 개발 게이트
→ Foundation·분야 스킬·Learning Log
→ 확정·구현·검증·확인 필요·보류
→ 결정·실제 경로·검증 증거
→ 상세 기획
→ 승인 이미지·실제 캡처
→ 위험·다음 작업·Ready·Done
→ 부록·변경·학습 이력
```

문장을 줄이는 과정에서 승인 상태, 예외, 실패 조건과 미검증을 제거하지 않는다.

## Phase 3 — Register the publication

Registry 활성 항목에 다음을 연결한다.

```yaml
document_id:
discipline:
responsibility_coverage:
status: ACTIVE
source_json:
output_docx:
output_pdf:
asset_dir:
publication_manifest:
generator: tools/build_design_documents.py
```

AI는 Registry와 JSON을 읽고, 사람은 PDF를 우선 열람한다.

## Phase 4 — Build diagrams and human documents

권장 명령:

```text
python tools/build_design_documents.py \
  --registry "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json" \
  --only <document-id> \
  --source-commit <commit>
```

생성 결과:

- `기획서.docx`
- `기획서.pdf`
- `기획서.assets/generated/workflow.png`
- `기획서.assets/generated/status-summary.png`
- `기획서.assets/generated/responsibility-map.png`
- `기획서_PUBLICATION_MANIFEST.json`

승인 이미지와 실제 캡처는 JSON 경로에서 읽어 DOCX·PDF에 포함한다.

## Phase 5 — Content validation

- 분야 목적과 플레이어 가치가 첫 페이지에서 이해되는가?
- 전체 과정이 입력 → 판단 → 산출물 → 검증 → 다음 게이트로 연결되는가?
- 승인·구현·검증·확인 필요·보류가 분리되는가?
- 관련 프로젝트 스킬과 실제 파일·테스트 경로가 있는가?
- 승인 이미지·실제 캡처가 빠짐없이 포함되는가?
- 이미지 캡션에 Asset ID·상태·채택·비채택 요소가 있는가?
- 폐기 이미지를 현행 기준처럼 보여주지 않는가?
- JSON의 수치·용어·상태와 DOCX·PDF가 일치하는가?

## Phase 6 — Render and visual validation

자동 검수:

- DOCX 생성과 ZIP 구조
- PDF 헤더
- PDF 전 페이지 PNG 렌더
- 빈 페이지·비정상 크기
- 한글 글꼴 설치 여부
- 다이어그램과 승인 이미지 존재

사람 검수:

- 모든 페이지를 100% 기준으로 확인
- 표·문장·이미지 잘림과 겹침
- 한글·특수문자 깨짐
- 이미지 비율·해상도·캡션
- 너무 작은 표 글자
- 첫 페이지부터 마지막 페이지까지 읽기 흐름

실제로 렌더링하지 않았다면 `human_visual_review`를 `PASSED`로 표시하지 않는다.

## Phase 7 — Freshness and governance

`check_design_document_publications.py`로 다음을 확인한다.

- JSON source SHA-256
- DOCX·PDF 파일 형식과 SHA-256
- 생성기·다이어그램 생성기 SHA-256
- 자동 다이어그램·승인 이미지 SHA-256
- 자동 렌더 페이지 수
- 사람 시각 검수 요구 상태
- 프로젝트 전체·분야 책임 범위
- 활성 Markdown 기획서 재생성 여부

JSON, 승인 이미지 또는 생성기가 바뀌면 이전 DOCX·PDF는 자동으로 오래된 것으로 판정한다.

## Phase 8 — Migration cleanup

기존 Markdown 본책에서 모든 고유 정보가 JSON으로 승계되고 참조·출력이 검증된 뒤에만 다음을 수행한다.

- Markdown 본책을 제거 후보로 분류
- `DOCUMENTATION_MAP`과 링크를 JSON·PDF 경로로 갱신
- Git 이력으로 복구 가능한지 확인
- 사용자 승인 후 활성 Markdown 본책 제거

운영 라우터 Markdown은 유지한다.

## Output contract

```md
## 구조화 기획서 발행 결과
- 문서 ID·분야:
- 책임 범위:
- AI 책임 원본 JSON:
- 사람용 DOCX:
- 사람용 PDF:
- 자동 다이어그램:
- 승인 이미지·실제 캡처:
- 기준 커밋:
- 생성 명령:
- Manifest 상태:
- 자동 렌더 페이지 수:
- 내용 검수:
- 사람 시각 검수:
- 미검증·불일치:
- 다음 재생성 트리거:
```

## Learning update

의미 있는 실행 후 해당 프로젝트 스킬 Learning Log에 기록한다.

- 생성 성공·실패
- 레이아웃 결함과 수정
- JSON 구조의 누락·과잉
- 승인 이미지 경로 문제
- 다이어그램 개선점
- 불필요하게 반복된 내용
- 생성기·검사기 갱신 필요 여부

## Failure conditions

- JSON·DOCX·PDF를 각각 독립 원본으로 수정
- 활성 Markdown 본책이 별도 책임 원본으로 남음
- 분야 전체 과정·현재 상태·다음 작업 누락
- 승인 이미지 누락 또는 폐기 이미지 혼입
- 수동 편집으로 재현 불가
- 생성 실패 후 이전 PDF를 `CURRENT`로 표시
- 렌더링 없이 시각 검수 통과 선언
- 문서 존재를 실제 구현·검증 완료로 해석
