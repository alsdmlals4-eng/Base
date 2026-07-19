# Markdown·JSON 혼용 기획서 발행 방법

- 상태: 공용 방법
- schema: v3
- 목적: 문서 성격에 맞는 단일 책임 원본에서 사람이 읽기 좋은 최신 PDF를 안전하고 재현 가능하게 발행한다.

## 1. 형식별 책임

| 형식 | 책임 |
|---|---|
| Markdown | 방향, 의도, 경험, 규칙, 흐름처럼 서술 중심인 기획의 기본 책임 원본 |
| JSON | Registry, Manifest, 상태, ID, 경로, 관계, 게임 데이터처럼 구조 검증이 필요한 책임 원본 |
| PDF | 책임 원본 변경과 같은 작업에서 항상 동기화하는 사람용 열람 파생본 |
| DOCX | PDF 생성 중 임시 파일 또는 Word 검토가 필요한 경우의 선택 파생본 |
| Mermaid | 필요한 Markdown 문서 안의 선택적 편집 원본 |
| SVG·PNG | Mermaid 또는 생성기에서 만든 삽입·검수 자산 |

같은 서술을 Markdown과 JSON에 중복 저장하지 않는다. Registry의 각 문서는 정확히 하나의 `source_path`와 `source_format`을 가진다.

## 2. Registry schema v3

```json
{
  "document_id": "game-design-bible",
  "title": "게임 기획서",
  "discipline": "게임 디자인",
  "responsibility_coverage": ["게임 디자인"],
  "status": "ACTIVE",
  "source_path": "../02_게임_디자인/게임_기획서.md",
  "source_format": "markdown",
  "source_role": "narrative_spec",
  "publication_policy": "always_sync",
  "output_pdf": "../02_게임_디자인/게임_기획서.pdf",
  "output_docx": null,
  "asset_dir": "../02_게임_디자인/게임_기획서.assets",
  "diagram_policy": "mermaid",
  "publication_manifest": "../02_게임_디자인/게임_기획서_PUBLICATION_MANIFEST.json",
  "generator": "tools/build_design_documents.py"
}
```

Markdown 기본 필수 제목은 `목표`, `배경과 의도`, `범위`, `규칙과 제약`, `검증과 완료 기준`이다. H1은 Registry `title`과 같아야 한다. JSON 문서는 정식 Schema로 필드와 타입을 검증한다.

Raw HTML과 원격 이미지는 재현성 때문에 거부한다. 로컬 이미지는 책임 원본 기준 상대 경로로 참조하고 SHA-256 해시를 Manifest에 기록한다.

## 3. 상시 동기화와 독립된 검수 상태

원본·로컬 이미지·Mermaid·생성기·잠금 파일이 변경된 작업에서는 PDF와 Manifest를 함께 재생성한다. PDF가 오래된 상태로 커밋되면 Governance가 실패한다.

```text
sync_status: CURRENT | STALE | FAILED | NOT_BUILT
automated_render_review: PASSED | FAILED
human_visual_review: NOT_RUN | PASSED | FAILED
human_visual_review_pdf_sha256: null | 검수한 PDF 해시
```

`CURRENT`는 입력과 PDF가 동기화됐다는 뜻이지 사람이 읽었다는 뜻이 아니다. 일반 변경은 `NOT_RUN`일 수 있다. 주요 제품 게이트·외부 배포·사용자 요청에서만 사람 `PASSED`를 요구한다. PDF 재생성 후 과거 사람 검수 해시는 승계하지 않는다.

Codex의 전 페이지 시각 검수는 PR 검증 증거로 별도 기록한다. 사용자가 직접 확인하지 않았다면 사람 검수 완료로 표시하지 않는다.

## 4. 내용과 시각 품질

PDF에는 문서 성격에 맞게 다음을 포함한다.

- 제목·목차·제목 계층·페이지 번호
- 기준 커밋·생성 기준 시각·책임 원본 경로와 해시
- 전체 과정·현재 상태·다음 단계·책임 범위
- 확정·구현·검증·미검증·보류 상태
- 승인 이미지의 Asset ID·출처·승인 상태·캡션
- 표·목록·코드·링크·한글·특수문자
- Mermaid가 있을 때 SVG·PNG 다이어그램

자동 검수는 PDF 파일 형식, 전 페이지 렌더, 빈 페이지, 최소 해상도를 확인한다. 최종 Codex 검수는 첫 페이지부터 마지막 페이지까지 글자·표·이미지 잘림, 겹침, 비율, 한글 폰트와 다이어그램 가독성을 확인한다.

## 5. 결정적·원자적 생성

- 입력 해시가 같으면 생성 시각만 바꾸기 위한 재작성을 하지 않는다.
- `SOURCE_DATE_EPOCH` 또는 기준 커밋 시각을 사용한다.
- DOCX ZIP 시각과 PDF 메타데이터를 정규화한다.
- 모든 출력은 임시 디렉터리에서 생성·렌더·검증한다.
- 모든 검증이 성공한 뒤 `os.replace`로 교체하고 Manifest를 마지막에 교체한다.
- 실패하면 기존 정상 PDF·Manifest·자산을 보존하고 부분 파일을 제거한다.

LibreOffice 자체의 강제 재빌드는 환경별 바이너리 차이가 생길 수 있다. 공식 결정성 계약은 동일 입력의 정상 재실행이 입력 해시를 인식해 추적 파일을 다시 쓰지 않고 diff 0을 유지하는 것이다.

## 6. 생성과 사전 점검

```powershell
python -m pip install -r requirements-publication.txt
pnpm install --frozen-lockfile
python tools/check_publication_environment.py --require-mermaid
python tools/build_design_documents.py --registry "[기획서]/00_프로젝트_허브/DESIGN_DOCUMENT_REGISTRY.json" --source-commit HEAD
```

지원 환경:

- Linux: LibreOffice Writer, Poppler, Nanum 또는 Noto CJK
- Windows: `soffice.exe`, Poppler, 맑은 고딕·Nanum·Noto CJK
- Mermaid 문서: 고정된 Mermaid CLI, Node.js, Chrome/Chromium

환경 재정의는 `BASE_LIBREOFFICE`, `BASE_PDFTOPPM`, `BASE_MERMAID_CLI`, `BASE_FONT_REGULAR`, `BASE_FONT_BOLD`, `PUPPETEER_EXECUTABLE_PATH`를 사용한다. 의존성이 없으면 탐색한 경로, 필요한 설치 항목과 재실행 명령을 알리고 기존 산출물을 변경하지 않는다.

## 7. 승인 이미지와 보존 상태

- 승인 이미지·실제 캡처·참고 이미지를 같은 상태로 취급하지 않는다.
- Asset ID, 출처, 승인 상태, 캡션과 채택·비채택 요소를 기록한다.
- 보류·확인 필요·미검증 항목을 완료처럼 표현하지 않는다.
- 기존 프로젝트는 감사와 보존 대조, 사용자 승인 전에는 책임 원본 형식이나 경로를 강제 변경하지 않는다.

## 8. 실패 조건

- 같은 내용을 Markdown과 JSON 양쪽의 독립 책임 원본으로 유지함
- 원본·이미지·생성기가 바뀌었지만 PDF·Manifest가 이전 해시임
- 파생 PDF·DOCX·Skill Map Markdown을 수동 책임 원본처럼 수정함
- `CURRENT`와 사람 검수 완료를 혼동함
- 실패한 생성이 기존 정상 산출물을 덮어씀
- 렌더하지 않고 자동 또는 Codex 시각 검수를 통과 처리함
- 실제 구현·검증하지 않은 내용을 완료처럼 표현함
