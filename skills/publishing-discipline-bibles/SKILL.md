---
name: publishing-discipline-bibles
description: Use when creating, synchronizing, or validating schema v3 project and discipline documents with Markdown or JSON sources, current PDFs, optional DOCX or Mermaid derivatives, and publication manifests.
---

# Publishing Hybrid Project and Discipline Documents

## Core principle

문서마다 단일 Markdown 또는 JSON 책임 원본을 선택한다. PDF는 원본 변경과 같은 작업에서 항상 동기화하고, DOCX와 다이어그램은 필요한 경우만 생성한다. 최신성과 사람 검수 상태를 혼동하지 않는다.

먼저 `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`와 대상 프로젝트의 `DESIGN_DOCUMENT_REGISTRY.json`을 읽는다.

## Trigger

- 프로젝트 종합 또는 분야별 책임 문서 신규 생성
- 책임 원본·승인 이미지·Mermaid·생성기 변경
- PDF·Manifest 최신성이나 전 페이지 품질 검수
- schema v2.2.0을 v3로 승인 후 마이그레이션
- 주요 제품 게이트·외부 배포·사용자 요청의 시각 검수

## Do not use

- 책임 원본과 입력 해시가 같고 Manifest가 `CURRENT`인 단순 조회
- 기존 프로젝트 본책을 감사·보존 대조·승인 없이 변환
- PDF·DOCX·자동 생성 Markdown을 수동 책임 원본으로 유지
- 구현 증거 없이 완료 상태를 만드는 작업

## Required inputs

```yaml
project_repository:
design_document_registry:
document_id:
source_path:
source_format: markdown/json
responsibility_coverage:
approved_visuals:
actual_captures:
implementation_and_validation_evidence:
output_pdf:
output_docx: optional
diagram_policy: none/mermaid/generated
publication_manifest:
source_commit:
human_visual_review_required:
```

## Procedure

1. Registry에서 schema v3, 문서 ID, 책임 범위, 단일 책임 원본과 출력 경로를 확인한다.
2. 기존 Markdown·JSON·DOCX·PDF에만 있는 고유 결정, 표, 링크, 이미지, 예외, 보류와 미검증을 대조한다.
3. 서술 중심이면 Markdown, 구조 검증·게임 데이터면 JSON을 선택한다. 같은 서술을 양쪽에 복제하지 않는다.
4. Markdown은 H1과 필수 섹션, 로컬 이미지, 선택 Mermaid를 검증한다. Raw HTML과 원격 이미지는 거부한다.
5. JSON은 `schemas/structured-design-document-v3.schema.json`으로 검증한다.
6. 환경을 사전 점검한다.

```powershell
python tools/check_publication_environment.py --require-mermaid
```

7. 임시 디렉터리에서 DOCX, PDF, 선택 자산을 생성하고 PDF 전 페이지를 렌더 검증한다.
8. 모든 검증이 성공한 뒤 출력과 Manifest를 원자적으로 교체한다. 실패하면 기존 정상 산출물을 보존한다.
9. 동일 입력으로 다시 실행해 추적 파일 diff 0을 확인한다.
10. Codex는 변경 PDF 전 페이지를 확인하고 PR 검수 증거를 남긴다. 사용자가 보지 않았다면 `human_visual_review: NOT_RUN`을 유지한다.

## Validation

- 제목·목차·페이지 번호·기준 커밋·책임 원본 경로와 해시
- 전체 과정·현재 상태·다음 단계·책임 범위
- 확정·구현·검증·미검증·보류 분리
- 표·코드·링크·한글·특수문자·이미지 잘림과 겹침
- 승인 이미지의 Asset ID·출처·승인 상태·캡션
- Mermaid SVG·PNG와 원본 해시
- PDF와 선택 DOCX·자산·Manifest 해시
- `CURRENT`, 자동 렌더, 사람 검수의 독립 상태

## Output contract

```md
## schema v3 기획서 발행 결과
- 문서 ID·책임 범위:
- 책임 원본·형식:
- 사람용 최신 PDF:
- 선택 DOCX·다이어그램:
- 승인 이미지·실제 캡처:
- 기준 커밋·입력 해시:
- Manifest 상태:
- 자동 렌더 페이지 수:
- Codex 전 페이지 검수:
- 사람 시각 검수:
- 결정성 재실행 diff:
- 미검증·불일치:
```

## Learning update

실패, 중요한 결정, 재사용 가능한 교훈 또는 실제 검증 결과가 있을 때 Learning Log에 기록한다. 사소한 재실행은 의무 기록하지 않는다. 한 번의 성공이나 미검증 추측을 공용 규칙으로 자동 승격하지 않는다.

## Failure conditions

- Markdown·JSON·PDF·DOCX를 각각 독립 책임 원본으로 수정
- 변경된 입력과 오래된 PDF·Manifest를 함께 커밋
- 실패한 생성이 기존 정상 산출물을 덮어씀
- `CURRENT`를 사람 검수 완료로 해석
- 전 페이지 렌더 없이 자동·Codex 시각 검수를 통과 처리
- 기존 프로젝트 고유 정보나 승인 상태를 무손실 대조 없이 제거
