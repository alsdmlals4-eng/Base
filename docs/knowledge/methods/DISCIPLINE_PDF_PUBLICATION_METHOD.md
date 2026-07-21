# Markdown·JSON 혼용 기획서 발행 방법

- 상태: 공용 원칙·호환 경로
- 실행 Skill: `skills/managing-design-documents/SKILL.md`
- 실행 mode: `publish`, `validate`

이 문서는 형식별 책임과 안전한 발행의 불변 원칙만 책임진다. 문서 작성·구조 변경·발행·검수를 분리된 Skill로 다시 나누지 않는다.

## 형식별 책임

| 형식 | 책임 |
|---|---|
| Markdown | 방향·의도·경험·규칙·흐름처럼 서술 중심인 책임 원본 |
| JSON | Registry·Manifest·상태·ID·경로·관계·게임 데이터처럼 구조 검증이 필요한 책임 원본 |
| PDF | Registry 발행 정책이 요구하는 사람용 열람 파생본 |
| DOCX | Word 검토가 필요한 경우의 선택 파생본 |
| Mermaid | 필요한 Markdown 안의 선택 편집 원본 |
| SVG·PNG | Mermaid 또는 생성기에서 만든 삽입·검수 자산 |

같은 서술을 Markdown과 JSON에 중복 저장하지 않는다. Registry의 각 문서는 정확히 하나의 `source_path`와 `source_format`을 가진다.

## 발행 정책

```text
source_only
→ 원본과 직접 검증만 유지

milestone_sync
→ 주요 게이트·정기 검토·외부 공유 시 PDF·Manifest 동기화

always_sync
→ 원본·승인 이미지·생성기 변경과 같은 작업에서 PDF·Manifest 동기화
```

DOCX와 다이어그램은 Registry가 선언한 경우만 생성한다.

## 독립 상태

```text
sync_status: CURRENT | STALE | FAILED | NOT_BUILT
automated_render_review: PASSED | FAILED
codex_visual_review: NOT_RUN | PASSED | FAILED
human_visual_review: NOT_RUN | PASSED | FAILED
```

`CURRENT`는 입력과 발행본이 동기화됐다는 뜻이지 사람이 읽었다는 뜻이 아니다. PDF 재생성 후 과거 사람 검수 해시를 승계하지 않는다.

## 안전한 생성

1. Markdown H1·필수 Section·로컬 이미지·선택 Mermaid를 검증한다.
2. JSON은 등록된 Schema로 검증한다.
3. 환경과 LibreOffice·Poppler·Mermaid·브라우저 경로를 실제 실행으로 사전 점검한다.
4. 모든 출력은 임시 디렉터리에서 생성·렌더·검증한다.
5. 모든 검증이 성공한 뒤 원자적으로 교체한다.
6. 실패하면 기존 정상 PDF·Manifest·자산을 보존한다.
7. 동일 입력 정상 재실행은 추적 파일 diff 0을 유지한다.

## 시각 검수

PDF 전 페이지를 렌더해 빈 페이지, 한글·특수문자, 표·코드·링크, 이미지 잘림·겹침, 다이어그램 가독성을 확인한다. 자동 렌더 성공만으로 사람 검수를 통과 처리하지 않는다.

## 승인 이미지

승인 이미지·실제 캡처·참고 이미지를 같은 상태로 취급하지 않는다. Asset ID, 출처, 승인 상태, 캡션, 채택·비채택 요소와 해시를 기록한다.

## 실패 조건

- 같은 내용을 Markdown과 JSON의 독립 책임 원본으로 유지함
- 발행 정책과 무관하게 모든 문서에 PDF·DOCX를 강제함
- 변경된 입력과 오래된 PDF·Manifest를 함께 커밋함
- 실패한 생성이 기존 정상 산출물을 덮어씀
- `CURRENT`와 사람 검수 완료를 혼동함
- 전 페이지 렌더 없이 시각 검수를 통과 처리함
- 실제 구현·검증하지 않은 내용을 완료처럼 표현함
