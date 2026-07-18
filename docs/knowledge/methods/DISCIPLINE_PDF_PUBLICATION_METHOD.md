# 구조화 기획서·분야 본책 발행 방법

- 상태: 공용 방법
- 목적: 프로젝트 전체 기획과 분야별 본책을 **AI용 구조화 JSON 책임 원본**으로 관리하고, 사람이 한눈에 읽을 수 있는 DOCX·PDF와 다이어그램·승인 이미지 자산을 재현 가능하게 생성한다.
- 적용 대상: 프로젝트 종합 기획서, 설정·게임 디자인·UX·개발·아트·사운드·QA·프로덕션·분석·통합검수 본책, 프로젝트 스킬맵

## 1. 책임 원본과 사람용 열람본

```text
AI·자동 검사 책임 원본
→ 기획서 JSON
→ DESIGN_DOCUMENT_REGISTRY.json

사람용 열람
→ 기획서 DOCX
→ 기획서 PDF
→ 기획서.assets/generated/*.png
→ 기획서.assets/approved/*

최신성·검증
→ 기획서_PUBLICATION_MANIFEST.json
```

- 활성 기획 내용을 책임지는 본책은 JSON이다.
- DOCX·PDF는 JSON과 승인 이미지에서 생성되는 사람용 파생본이다.
- 다이어그램은 JSON의 작업 흐름·책임·현재 상태에서 자동 생성한다.
- 사람은 PDF를 기본 열람본으로 사용하고, 문서 형식 검토가 필요할 때 DOCX를 사용한다.
- DOCX를 직접 편집해도 JSON에 반영되지 않았다면 공식 변경이 아니다.
- 활성 `*_기획서.md`, `DISCIPLINE_BIBLE.md`, `PROJECT_MASTER_PLAN.md`는 만들지 않는다.
- `START_HERE`, `ACTIVE_CONTEXT`, `DOCUMENTATION_MAP`, 작업 절차처럼 빠른 라우팅이 필요한 운영 문서는 Markdown을 유지할 수 있다.

## 2. 기본 폴더 구조

```text
[기획서]/
├─ 00_프로젝트_허브/
│  ├─ DESIGN_DOCUMENT_REGISTRY.json
│  └─ 프로젝트_종합_기획서.*
└─ 02_게임_디자인/
   ├─ 게임_기획서.json
   ├─ 게임_기획서.docx
   ├─ 게임_기획서.pdf
   ├─ 게임_기획서.assets/
   │  ├─ generated/
   │  │  ├─ workflow.png
   │  │  ├─ status-summary.png
   │  │  └─ responsibility-map.png
   │  └─ approved/
   └─ 게임_기획서_PUBLICATION_MANIFEST.json
```

각 프로젝트는 같은 계약으로 11개 책임 분야와 프로젝트 전체 방향을 등록한다. 소규모 프로젝트가 여러 책임을 한 본책에 통합할 수는 있지만 `responsibility_coverage`에서 누락 없이 선언한다.

## 3. JSON 본책 필수 계약

각 활성 기획서 JSON은 최소한 다음을 가진다.

```text
문서 ID·종류·프로젝트·제목·분야·책임·상태
→ 마지막 편집·검토·기준 커밋·현재 게이트
→ 목적·플레이어 가치·현재 목표·요약·위험·다음 작업
→ 목표·Quality Bar·금지 방향
→ 책임·비책임·분야 간 입력·출력 계약
→ 분야 전체 작업 흐름
→ 작업 게이트·제품 게이트 기여
→ Foundation·분야 스킬·Learning Log
→ 확정·구현·검증·확인 필요·보류 상태
→ 결정·구현 경로·검증 증거
→ 상세 기획 장
→ 승인 이미지·UI·다이어그램·실제 캡처
→ 위험·다음 작업·Ready·Done·부록·변경 이력
```

상세 구조는 `templates/project-operations/DESIGN_DOCUMENT.json`을 따른다.

## 4. Design Document Registry

`DESIGN_DOCUMENT_REGISTRY.json`은 AI가 기획서 위치와 발행 상태를 찾는 지도다.

각 활성 문서 항목:

```json
{
  "document_id": "game-design-bible",
  "discipline": "게임 디자인",
  "responsibility_coverage": ["게임 디자인"],
  "status": "ACTIVE",
  "source_json": "../02_게임_디자인/게임_기획서.json",
  "output_docx": "../02_게임_디자인/게임_기획서.docx",
  "output_pdf": "../02_게임_디자인/게임_기획서.pdf",
  "asset_dir": "../02_게임_디자인/게임_기획서.assets",
  "publication_manifest": "../02_게임_디자인/게임_기획서_PUBLICATION_MANIFEST.json",
  "generator": "tools/build_design_documents.py"
}
```

Registry는 다음 책임을 가진다.

- 프로젝트 전체와 모든 분야의 책임 범위 보장
- 현행·보류·백업·제거 후보 구분
- JSON·DOCX·PDF·자산·Manifest 경로 제공
- 새 AI의 콜드 스타트 라우팅
- 통합 본책이 여러 분야를 담당할 때 책임 범위 기록

## 5. 사람용 DOCX·PDF 필수 내용

DOCX와 PDF는 단순 요약본이 아니다.

```text
표지·기준 커밋·JSON 해시
→ 한눈에 보기
→ 목표·Quality Bar·금지 방향
→ 책임·협업 경계 다이어그램
→ 분야 전체 작업 흐름 다이어그램
→ 단계별 입력·판단·산출물·검증
→ 개발 게이트·프로젝트 스킬
→ 확정·구현·검증·확인 필요·보류
→ 확정 결정·실제 구현 경로·검증 증거
→ 상세 기획
→ 승인 이미지·실제 캡처·상태 캡션
→ 위험·다음 작업·Ready·Done
→ 부록·변경·학습 이력
```

PDF가 기본 사람용 열람본이며 DOCX는 같은 내용의 문서 검토용 파생본이다.

## 6. 다이어그램 자산

기본 자동 생성 다이어그램:

- `workflow.png`: 입력부터 다음 게이트까지의 작업 과정
- `status-summary.png`: 확정·구현·검증·확인 필요·보류 분리
- `responsibility-map.png`: 소유·비소유·분야 간 계약

추가 다이어그램은 해당 분야 JSON의 상세 장과 `.assets/`에 등록한다. 사람이 만든 승인 다이어그램도 Asset ID·상태·채택 요소·비채택 요소를 기록한다.

## 7. 승인 이미지 포함 규칙

- 기존 승인 이미지가 있으면 별도 지시 없이 새 시안을 만들지 않는다.
- `REFERENCE`, `DIRECTION_APPROVED`, `PRODUCTION_READY`, `IMPLEMENTED`, `VISUALLY_VALIDATED`를 구분한다.
- 캐노니컬 경로와 Asset ID를 JSON에 기록한다.
- 이미지 전체가 승인된 것이 아니면 채택 요소와 비채택 요소를 기록한다.
- 이미지 안 임시 수치·문구를 공식 기획값으로 사용하지 않는다.
- 폐기·대체 이미지는 현행 PDF에서 제외하거나 상태를 명확히 표시한다.
- 실제 게임 캡처와 콘셉트 이미지를 구분한다.

## 8. 생성 파이프라인

공용 명령:

```text
python tools/build_design_documents.py \
  --registry "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json" \
  --source-commit "$GIT_COMMIT"
```

생성 순서:

```text
Registry에서 활성 문서 선택
→ 기획서 JSON 검증
→ 작업 흐름·상태·책임 다이어그램 생성
→ 승인 이미지 경로·형식 확인
→ DOCX 생성
→ LibreOffice로 PDF 변환
→ PDF 전 페이지 PNG 렌더
→ 빈 페이지·렌더 실패 검사
→ 입력·생성기·출력·이미지 해시 Manifest 작성
```

필수 도구:

- Python 3.12 이상
- `python-docx`
- Pillow
- LibreOffice Writer
- Poppler `pdftoppm`
- 한글 글꼴 `NanumGothic` 또는 Noto CJK

## 9. Publication Manifest

각 기획서 Manifest는 최소한 다음을 추적한다.

- source JSON 경로·SHA-256
- 기준 커밋
- DOCX·PDF 경로·SHA-256
- 생성기·다이어그램 생성기 SHA-256
- 자동 생성 다이어그램 경로·SHA-256
- 승인 이미지 경로·SHA-256
- 생성 시각
- `CURRENT / STALE / FAILED / NOT_BUILT`
- 자동 렌더 검수
- 렌더 페이지 수
- 사람 시각 검수 상태

파일 수정 시간만으로 최신성을 판정하지 않는다.

## 10. 자동 검수

`check_design_document_publications.py`는 다음을 검사한다.

- Registry와 활성 문서 ID 중복·누락
- 프로젝트 전체와 11개 분야 책임 범위
- JSON source와 Registry ID·상태 일치
- DOCX·PDF 실제 파일 헤더와 해시
- 생성기 변경 후 미재생성
- 다이어그램·승인 이미지 누락·해시 불일치
- 자동 렌더 검수와 페이지 수
- 필요 시 사람 시각 검수
- 활성 Markdown 기획서 재생성

JSON, 승인 이미지 또는 생성기가 변경됐는데 Manifest·DOCX·PDF·다이어그램이 이전 해시라면 PR을 실패시킨다.

## 11. 사람 시각 검수

자동 렌더 검수는 빈 페이지·파일 손상·기본 렌더 실패를 확인한다. 최종 품질 검수는 모든 페이지를 PNG로 렌더해 사람이 직접 확인한다.

확인 항목:

- 한글·특수문자 깨짐
- 표와 문장의 잘림·겹침
- 이미지 해상도·비율·캡션
- 페이지 순서와 제목 계층
- 너무 작은 표 글자
- 승인 이미지와 설명의 일치
- 첫 페이지·마지막 페이지·모든 중간 페이지

주요 개발 게이트와 외부 배포에서는 `human_visual_review: PASSED`를 요구한다.

## 12. 분야별 강조점

| 분야 | 특히 보여줄 전체 과정 |
|---|---|
| 설정·내러티브 | 정사 원칙 → 시나리오 → 캐릭터·대사 → 구현·현지화 → 검수 |
| 게임 디자인 | 게임 약속 → 핵심 루프 → 시스템·밸런스 → 데이터·UI 계약 → 플레이 검증 |
| UX·UI·접근성 | 사용자 과업 → 정보 구조 → 와이어프레임 → 시각 적용 → 사용성·접근성 QA |
| 개발 | 요구 → 아키텍처 → Scene·데이터 → 구현 → 테스트·성능·빌드 |
| 테크니컬 아트 | 원본 제작 → 규격 → Import → 엔진 적용 → 성능·시각 QA |
| 아트 | 방향 → 자산 계열 → 제작 규격 → 승인 이미지 → 실제 캡처 비교 |
| 사운드 | 감정·정보 목적 → 음원 제작 → 이벤트 연결 → 믹싱 → 반복·접근성 QA |
| QA | 위험 → 테스트 설계 → 실행 → 결함 등급 → 회귀·릴리스 판정 |
| 프로덕션 | 범위 → 일정·의존성 → 마일스톤 → 위험·예산 → Greenlight |
| 분석·유저리서치 | 질문 → 근거 → 조사·계측 → 해석 → 채택·제외 결정 |
| 통합검수 | 요구 → JSON 책임 원본 → 구현·자산 → 검증 → 불일치 → 게이트 판정 |

## 13. 실패 조건

- JSON과 DOCX/PDF를 각각 독립 원본으로 수정함
- 활성 Markdown 본책이 별도 책임 원본으로 남음
- DOCX/PDF에 분야의 전체 과정·현재 상태·다음 작업이 없음
- 승인 이미지·실제 캡처가 누락되거나 상태가 없음
- 생성기·JSON·이미지가 바뀌었지만 Manifest가 `CURRENT`임
- 렌더링하지 않고 시각 검수를 완료로 표시함
- 실제 구현·검증하지 않은 내용을 완료처럼 표현함
- 모든 분야의 내용을 하나의 거대한 문서에 복제해 책임 경계와 토큰 효율을 잃음

## 14. 운영 문서와의 경계

다음은 기획 본책이 아니므로 Markdown을 유지할 수 있다.

- `START_HERE.md`
- `ACTIVE_CONTEXT.md`
- `DOCUMENTATION_MAP.md`
- `DEVELOPMENT_GATES.md`
- `DOCUMENT_UPDATE_MATRIX.md`
- `AI_WORKFLOW.md`
- Skill의 `SKILL.md`와 Learning Log

이 문서들은 JSON 본책의 내용을 장문 복사하지 않고 경로·현재 상태·작업 순서만 연결한다.
