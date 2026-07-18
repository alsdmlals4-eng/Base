---
name: publishing-discipline-bibles
description: Use when building, refreshing, or validating user-readable discipline PDF bibles from current Markdown responsibility sources, approved images, actual captures, appendices, and publication manifests.
---

# Publishing Discipline Bibles

## Core principle

분야 PDF는 요약본이 아니라 책임 원본과 승인 자료를 읽기 좋은 순서로 조합한 **최신 읽기 전용 통합본**이다.

공용 방법: `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`

템플릿:

- `templates/project-operations/DISCIPLINE_PDF_PUBLICATION.md`
- `templates/project-operations/PUBLICATION_MANIFEST.json`

## Trigger

- 분야별 기획서를 PDF로 발행
- 기존 PDF가 원본보다 오래됐는지 검수
- 승인 이미지를 포함한 사용자용 통합 문서 생성
- PDF 생성 파이프라인과 CI 최신성 검사 설치
- Markdown·PDF·DOCX 간 책임 충돌 정리

## Do not use

- Markdown 책임 원본이 정리되지 않은 상태에서 PDF만 최신화
- 폐기 이미지와 승인 이미지를 구분할 자료가 없음
- 실제 구현 상태를 확인하지 않고 완료형 포트폴리오 제작
- 사용자가 독립 편집 원본으로 PDF 또는 DOCX를 명시한 특수 계약을 임의로 변경

## Required inputs

```yaml
discipline:
source_bible:
appendices:
visual_source_of_truth:
asset_manifest:
approved_images:
actual_captures:
project_skill_map:
development_gates:
roadmap_and_status:
output_pdf:
generator_command:
publication_manifest:
```

## Phase 1 — Source audit

- 분야 본책의 상태·기준 커밋·목차 확인
- 부록의 활성·보조·백업·보류 상태 확인
- 승인 이미지의 Asset ID·캐노니컬 경로·채택 범위 확인
- 실제 캡처와 콘셉트 이미지 구분
- 구현·검증·미검증 상태 대조
- PDF에 포함할 전체 작업 흐름과 관련 프로젝트 스킬 확인
- 기존 PDF·DOCX가 독립 원본처럼 수정됐는지 확인

원본이 불명확하면 PDF 발행보다 책임 원본 정리를 먼저 수행한다.

## Phase 2 — Publication plan

`templates/project-operations/DISCIPLINE_PDF_PUBLICATION.md`를 분화한다.

필수 구성:

1. 표지·기준 커밋
2. 한눈에 보기
3. 분야 목적·Quality Bar·금지 방향
4. 전체 작업 과정
5. 단계별 입력·산출물·게이트
6. 분야 책임 문서·프로젝트 스킬
7. 승인 결정과 협업 경계
8. 승인 이미지·실제 캡처
9. 구현·검증 상태
10. 위험·보류·다음 작업
11. 부록·출처·변경 이력

공통 운영 원칙은 링크와 짧은 적용 요약만 넣고 분야 PDF마다 전문을 복사하지 않는다.

## Phase 3 — Build

- Markdown과 구조화된 Manifest를 입력으로 사용한다.
- 승인 이미지와 실제 캡처를 캐노니컬 경로에서 읽는다.
- PDF를 수동 편집하지 않는다.
- 재현 가능한 한 개의 명령으로 생성한다.
- 생성 실패 시 기존 PDF를 `CURRENT`로 유지하지 않는다.
- Publication Manifest에 입력 경로, 출력, 생성기, 기준 커밋과 해시를 기록한다.

권장 명령 예:

```text
python tools/build_discipline_publications.py --discipline art
```

실제 도구는 프로젝트 환경에 맞게 선택한다.

## Phase 4 — Content validation

- 분야의 전체 흐름이 처음부터 다음 작업까지 연결되는가?
- 승인·구현·검증·미검증이 구분되는가?
- 승인 이미지가 빠짐없이 포함되는가?
- 폐기·부분 참고 이미지가 현행 기준처럼 보이지 않는가?
- 이미지 캡션에 상태·채택 범위·경로가 있는가?
- 관련 실제 파일·스킬·게이트로 이동할 경로가 있는가?
- `[보류]`가 현재 구현처럼 설명되지 않는가?
- 원본 본책과 수치·용어·상태가 일치하는가?

## Phase 5 — Visual and accessibility validation

- 표지와 한눈에 보기
- 목차·북마크
- 한글 글꼴과 특수문자
- 표·코드·이미지 페이지 잘림
- 이미지 해상도와 캡션
- 색 외 상태 라벨
- 링크 작동
- 페이지 번호와 기준 커밋
- 마지막 페이지와 부록

렌더링을 직접 확인하지 못했다면 `[미검증]`으로 남긴다.

## Phase 6 — Freshness validation

- Manifest의 source files·approved images·output PDF가 존재
- PDF 헤더와 파일 형식 확인
- 입력 해시와 Manifest 해시 일치
- 원본·승인 이미지 변경 PR에서 PDF·Manifest도 갱신
- 본책과 PDF의 기준 커밋·상태 일치

파일 수정 시간만으로 최신성을 판단하지 않는다.

## Output contract

```md
## PDF 발행 결과
- 분야:
- 책임 원본:
- 포함한 부록:
- 승인 이미지·Asset ID:
- 실제 캡처:
- 전체 과정 포함 여부:
- 기준 커밋·빌드:
- 생성 명령:
- 출력 PDF:
- Publication Manifest:
- 내용 검수:
- 시각·접근성 검수:
- 최신성 검수:
- 미검증:
- 다음 재생성 트리거:
```

## Failure conditions

- PDF만 수정하고 Markdown 원본 방치
- 요약만 있고 전체 과정·현재 상태·다음 작업 누락
- 승인 이미지 누락 또는 폐기 이미지 혼입
- 수동 편집으로 재현 불가
- 생성 실패 후 이전 PDF를 최신으로 표시
- PDF 존재를 구현·검증 완료로 해석
- 렌더링을 확인하지 않고 시각 검수 통과 선언
