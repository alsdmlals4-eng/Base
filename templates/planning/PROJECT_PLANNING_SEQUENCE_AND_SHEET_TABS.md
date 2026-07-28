# 프로젝트 기획 작업순서·Google Sheets tab Template

이 Template은 Base 자체가 아니라 Base를 적용한 **개별 프로젝트**에서 사용한다. 프로젝트 Google Sheets가 없으면 `NOT_CONFIGURED`로 기록하고 Sheet가 있는 것처럼 추정하지 않는다.

## 1. 설치할 tab

```text
00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
10_제품방향
20_코어경험_데모목표
30_데모범위_품질기준_제작기반
40_시스템_성장_경제
50_메인콘텐츠
51_미니게임                 # 필요할 때만
52_글쓰기_서사              # 필요할 때만
60_UX_UI_접근성
70_아트_오디오_에셋
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력
```

## 2. `01_작업순서` 공통 열

| 순서 | Approval Bundle | 분야 | 현재 단계 | 선행 조건 | `BLOCKS` | `INFORMS` | 승인 상태 | 정본 반영 | 소비처 반영 | 구현 | 검증 | 다음 작업 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 3. 분야별 tab 공통 열

| 순서 | Decision ID | Approval Bundle | 현재 확정 내용 | 신규 제안 | 변경 이유 | Evidence ID | GPT 권장안 | 사용자 결정 | 선행·후속 | 책임 정본 경로 | 소비처 | 구현 상태 | 검증 | 누락·충돌 | Sheet 동기화 | 최종 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

`최종 상태`는 `CURRENT / SUPERSEDED / DEFERRED / REJECTED / BLOCKED_UNVERIFIED`를 사용한다.

## 4. `03_근거_라이브러리`

| Evidence ID | 유형 | 출처 | 날짜·버전 | 비교 차원 | 대상 플레이어 | 관찰 사실 | 플레이어 반응 | 현업·공식 권장 | 적용 판정 | 신뢰도 | 후속 검증 |
|---|---|---|---|---|---|---|---|---|---|---|---|

유형:

- `BENCHMARK_EVIDENCE`
- `PLAYER_RESPONSE_EVIDENCE`
- `PROFESSIONAL_OFFICIAL_EVIDENCE`
- `BEHAVIORAL_EVIDENCE`
- `CONTROLLED_EXPERIMENT`

적용 판정은 `ADOPT / ADAPT / AVOID / TEST / IGNORE`를 사용한다.

## 5. `04_누락_충돌_감사`

| Audit ID | 날짜 | 작업·질문 | 비교한 main | 비교한 Decision | 비교한 PR | 비교한 정본 | 비교한 구현 | Sheet 상태 | 판정 | 영향 | 수정 위치 | 재검증 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

판정:

- `DUPLICATE_WORK`
- `DUPLICATE_QUESTION`
- `MISSING_CANON`
- `MISSING_CONSUMER`
- `CANON_CONFLICT`
- `IMPLEMENTATION_CONFLICT`
- `STALE_REFERENCE`
- `MISSING_SYNC`
- `NO_CONFLICT`
- `BLOCKED_UNVERIFIED`

## 6. Approval Bundle 종료 조건

```text
APPROVED
→ CANON_UPDATED
→ CONSUMERS_UPDATED
→ PROJECT_SHEET_UPDATED
→ IMPLEMENTED | IMPLEMENTATION_PENDING
→ VALIDATED | BLOCKED_UNVERIFIED
→ NO_CONFLICT | CONFLICT_FIXED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
```

다음 Bundle은 현재 Bundle의 차단 Finding과 미동기화가 정리된 뒤 진행한다.
