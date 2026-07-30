# Project Google Sheets Workbook Contract

이 파일은 개별 프로젝트 Google Sheets를 **사용자 중심 GDD 작업면**으로 만들거나 기존 Sheet를 재구조화할 때 사용하는 설치 계약이다. Base에는 Sheet를 만들지 않는다.

공용 정책: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`

## 역할·상태 확인

```yaml
project_google_sheet_status: PROJECT_SHEET_CONFIGURED | NOT_CONFIGURED
workspace_role: USER_FACING_GDD_WORKSPACE
canonical_authority: GITHUB_CANONICAL_AND_ACTUAL_FILES
user_edit_policy: PROPOSED_SHEET_CHANGE
ai_read_policy: GITHUB_AND_SHEET_COMPARE
spreadsheet_url:
spreadsheet_id:
verified_tabs:
last_verified_at:
last_verified_commit:
```

정확한 URL·ID·권한을 확인하지 못하면 `NOT_CONFIGURED`로 유지한다. 비슷한 제목의 Sheet를 추정하거나 중복 생성하지 않는다.

## 책임 경계

- 사용자는 Sheet에서 전체 흐름·현재 정보·이미지·수치를 확인하고 수정한다.
- AI는 GitHub 정본·실제 파일과 Sheet를 함께 읽는다.
- Sheet에만 있는 수정은 `PROPOSED_SHEET_CHANGE`다.
- 승인된 변경만 GitHub 정본과 Sheet 양쪽에 반영하고 재조회한다.
- Sheet는 GitHub 정본과 실제 구현을 대체하지 않는다.

## 표준 GDD 영역

`templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`를 따른다.

1. 문서 개요
2. 핵심 게임플레이
3. 게임 시스템
4. 스토리 및 세계관
5. 아트 및 사운드
6. 기술 및 로드맵

최소 필수 의미 구조:

- GDD 요약·제품 방향
- 세계관·핵심 루프·조작·게임 규칙
- 주요인물·조연·세력·관계
- 핵심시스템·메인콘텐츠·성장·경제
- UX·UI·접근성·아트·오디오
- 이미지 기획·생성 목록과 이미지 검수·승인 로그
- Demo-First Vertical Slice·플레이테스트·기술·로드맵

## GDD 읽기 순서와 결정 원장

사람은 먼저 `00_프로젝트_허브`와 `05_GDD_요약`에서 게임의 현재 모습을 읽고, 변경 이유와 현재 상태는 `02_현재_확정결정`의 **결정 원장**에서 확인한다. 상세 tab은 다시 같은 결정을 쓰지 않고 `Decision ID`를 참조한다.

```text
00_프로젝트_허브 → 05_GDD_요약 → 02_현재_확정결정
→ 10_경험 | 20_시스템_콘텐츠 | 30_세계_서사 | 40_표현 | 50_제작_검증
→ 03_근거_라이브러리 | 04_누락_충돌_감사 | 99_변경이력
```

- 결정 원장은 `CURRENT`의 단일 목록이며, 분야 tab에는 전문·승인 상태·정본 경로를 복사하지 않는다.
- `00`과 `05`는 카드형 요약과 링크만 제공한다. 상세 규칙·수치·서사는 분야 tab에만 둔다.
- 기존 세부 tab은 이력·소비자가 있는 경우 다섯 분야 묶음 아래 상세 보기로 보존한다. 사용자 승인 없이 삭제·강제 병합하지 않는다.

## 시각·수치 계약

각 주요 tab은 한 화면 요약, 흐름도·관계도·다이어그램, 와이어프레임·실제 캡처·레퍼런스, 핵심 수치 표, GitHub 정본 경로 순으로 구성한다.

수치 열은 최소한 다음을 포함한다.

```text
파라미터·지표
단위
초기 시험값
조정 범위
공식·규칙
적용 조건
플레이어 영향
검증 방법
검증 상태
재조정 조건
```

## 설치·갱신 순서

```text
정확한 Sheet 확인
→ metadata와 기존 tab 읽기
→ 중복·구형 tab·사용자 편집 범위 감사
→ 표준 GDD 6영역과 기존 정보 매핑
→ 이름 변경·병합·신규 tab 계획
→ 기존 값·수식·검증·링크·이미지 보존
→ tab·열·시각 요약 설치
→ 정본 경로·Decision ID·Commit SHA 연결
→ 샘플이 아닌 실제 현재 Decision·구현 상태 동기화
→ PROPOSED_SHEET_CHANGE 분리
→ 재읽기·시각 검수·충돌 판정
→ PROJECT_SHEET_CONFIGURED
```

## 동기화 상태

```text
SYNCED
PROPOSED_SHEET_CHANGE
GITHUB_UPDATE_PENDING_SHEET
SHEET_UPDATE_PENDING_GITHUB
SHEET_GITHUB_CONFLICT
NOT_CONFIGURED
BLOCKED_UNVERIFIED
```

## 금지

- Base용 Sheet 생성
- 기존 Sheet URL 없이 임의 신규 Sheet 생성
- 사용자 편집 범위를 읽지 않고 전면 덮어쓰기
- Sheet-only 제안을 승인 정본으로 간주
- 세계관·핵심루프·인물·핵심시스템을 한 자유 메모 탭에 혼합
- 긴 텍스트만 두고 흐름도·관계도·와이어프레임·이미지·수치 요약을 생략
- 이미지 URL만 붙이고 생성 목적·원출처·검수·승인 상태를 기록하지 않음
- GitHub 또는 Sheet 한쪽만 갱신하고 `SYNCED`로 보고
