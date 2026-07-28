# Project Google Sheets Workbook Contract

이 파일은 개별 프로젝트 Google Sheets를 만들거나 기존 Sheet를 재구조화할 때 사용하는 설치 계약이다. Base에는 Sheet를 만들지 않는다.

## 상태 확인

```yaml
project_google_sheet_status: PROJECT_SHEET_CONFIGURED | NOT_CONFIGURED
spreadsheet_url:
spreadsheet_id:
verified_tabs:
last_verified_at:
```

정확한 URL·ID·권한을 확인하지 못하면 `NOT_CONFIGURED`로 유지한다. 비슷한 제목의 Sheet를 추정하거나 중복 생성하지 않는다.

## 필수 tab과 열

`templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`를 따른다. 최소 필수 의미 구조는 다음이다.

- 세계관
- 핵심루프
- 주요인물
- 조연·세력·관계
- 핵심시스템·메인콘텐츠
- 이미지 기획·생성 목록
- 이미지 검수·승인 로그

## 설치·갱신 순서

```text
정확한 Sheet 확인
→ metadata와 기존 tab 읽기
→ 중복·구형 tab 감사
→ 이름 변경·병합·신규 tab 계획
→ 기존 값·수식·검증·링크 보존
→ tab 생성·열 설치
→ 정본 경로와 Decision ID 연결
→ 샘플이 아닌 실제 현재 Decision 동기화
→ 재읽기·시각 검수
→ PROJECT_SHEET_CONFIGURED
```

## 금지

- Base용 Sheet 생성
- 기존 Sheet URL 없이 임의 신규 Sheet 생성
- 사용자 편집 범위를 읽지 않고 전면 덮어쓰기
- 세계관·핵심루프·인물·핵심시스템을 한 자유 메모 탭에 혼합
- 이미지 URL만 붙이고 생성 목적·검수·승인 상태를 기록하지 않음
