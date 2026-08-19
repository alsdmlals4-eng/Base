# 프로젝트 기획 작업순서·Google Sheets GDD tab Migration Reference

> `STATUS: MIGRATION_ONLY_UNTIL_REMOVAL`
> `NEW_PROJECT_USE: FORBIDDEN`
> `DEFAULT_WORKSPACE: NOTION_DEFAULT_PROJECT_WORKSPACE`

이 문서는 새 프로젝트에 Google Sheet나 tab을 만드는 Template이 아니다. **기존 legacy Sheet에 아직 고유 정보가 남아 있을 때 그 위치와 의미를 한 번 식별하여 올바른 Project의 Notion 사람용 owner 또는 repository structured/runtime owner로 이관하기 위한 migration reference**다. 신규 계획·수정·승인 데이터는 Sheet에 입력하지 않는다.

공용 정책: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`

## 1. 기존 legacy tab 식별 목록

아래 이름은 과거 Sheet에서 unique material을 찾기 위한 호환 식별자다. 새 Sheet나 새 tab을 생성하는 설치 목록으로 사용하지 않는다.

```text
00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
05_GDD_요약
06_시각_작업면 (Artifact가 있을 때만)
10_경험
20_시스템_콘텐츠
30_세계_서사
40_표현
50_제작_검증
```

위 11개는 **기존 legacy Sheet에서만 식별·이관할 수 있는 과거 핵심 tab**이다. 다음 상세 tab도 기존 Sheet에 남아 있는 unique material의 위치를 찾기 위한 참조일 뿐이며, 새 Sheet에 자동 생성하거나 사용자 승인 없이 이름을 바꾸지 않는다.

```text
10_제품방향
11_세계관
12_핵심루프
13_주요인물
14_조연_세력_관계
15_조작_게임규칙
20_코어경험_데모목표
30_데모범위_품질기준_제작기반
40_핵심시스템_메인콘텐츠
41_성장_경제
50_메인콘텐츠
51_미니게임
52_글쓰기_서사
60_UX_UI_접근성
70_아트_오디오_에셋
71_이미지기획_생성목록
72_이미지검수_승인로그
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력
```

기존 상세 tab은 실제 소비자·이력·사용자 편집을 감사한 뒤 각각 `10_경험`, `20_시스템_콘텐츠`, `30_세계_서사`, `40_표현`, `50_제작_검증`에 담긴 **의미**를 현재 Notion/repository owner로 이관하기 위한 판독 보조로만 사용한다. destination readback이 끝난 duplicate/obsolete 구조는 활성 작업면으로 유지하지 않는다.

## 2. 표준 GDD 6영역 migration 매핑

| 표준 GDD 영역 | legacy 주요 tab | 이관할 의미·시각 |
|---|---|---|
| 1. 문서 개요 | `00_프로젝트_허브`, `05_GDD_요약`, `02_현재_확정결정` | 핵심 카피, 프로젝트 흐름, 현재 Stage, 유효 Decision |
| 2. 핵심 게임플레이 | `10_경험` | Core Loop 흐름도, 입력 매핑, 승패 흐름 |
| 3. 게임 시스템 | `20_시스템_콘텐츠` | 시스템 관계도, 공식·수치, 입력·출력 |
| 4. 스토리 및 세계관 | `30_세계_서사` | 관계도, 월드·스테이지 구조, 정보 공개 흐름 |
| 5. 아트 및 사운드 | `40_표현` | 와이어프레임, 캡처, 레퍼런스, 오디오 역할 |
| 6. 기술 및 로드맵 | `50_제작_검증`, `01_작업순서` | 마일스톤, 기술 의존성, 성능·검증 상태 |

## 3. `00_프로젝트_허브`

| 프로젝트 | 한 문장 핵심 카피 | 장르·플랫폼·엔진 | 타깃 유저·플레이 상황 | 현재 Stage | 현재 Work Mode | Base SHA | Sheet 상태 | GitHub | 다음 Approval Bundle | 차단 Finding |
|---|---|---|---|---|---|---|---|---|---|---|

## 4. `05_GDD_요약`

| GDD Module ID | GDD 영역·사용자 질문 | 현재 한 문장 요약 | Decision ID | 대표 흐름도·관계도 | Artifact ID·와이어프레임·이미지·캡처 | 핵심 수치·상태 | 책임 정본 경로 | main Commit SHA | 마지막 수정 시각 | 수정 주체 | 동기화 상태 | 다음 확인 |
|---|---|---|---|---|---|---|---|---|---|---|

이 tab은 legacy Sheet에 고유 정보가 남아 있는 경우에만 사용자가 과거 전체 게임 구조를 빠르게 판독하는 migration input이다. 현재 GDD의 새 시작 화면이나 정본이 아니다.

`05_GDD_요약`에 있던 상세 전문이나 별도 상태값을 통째로 복사하지 않는다. 여섯 영역 카드가 가리키는 현재 의미와 Decision을 확인해 올바른 Notion/repository destination으로 이관한다.

`GDD Module ID`는 같은 주제의 결정·정본·시각 참조·검증을 대응시키는 legacy 식별 단서다. 이 ID 자체를 새 정본으로 만들지 않는다.

## 4A. `06_시각_작업면` — legacy Artifact 색인

기존 Sheet에 이 tab이 실제로 존재할 때만 migration input으로 읽는다. 과거 Figma·Whimsical·기타 외부 시각 Artifact 링크가 남아 있어도 **새 Figma/외부 visual workspace를 만들거나 활성 권위로 복구하지 않는다**. unique visual/reference 정보만 정확한 Project의 Notion Asset & Knowledge / Visual Map 또는 repository owner로 이관하고 readback한다.

| Artifact ID | 도구 | 사용 맥락 `GDD|EXTERNAL_COLLABORATION|BOTH` | 목적·Artifact 유형 | GDD Module ID·Decision ID | 책임 정본 경로 | 링크·Board/Page/Frame | Snapshot | 시각 상태 | 대상 플랫폼·해상도·입력 | 구현·제외 범위 | 검증·다음 Gate |
|---|---|---|---|---|---|---|---|---|---|---|---|

보드·Frame 전문, 게임 규칙, 구현 완료 주장을 새 작업면으로 복제하지 않는다. 과거 `VISUAL_ARTIFACT_REGISTRY.json`·`docs/VISUAL_COLLABORATION_TOOL_POLICY.md` 식별자는 provenance 확인에 필요한 경우에만 migration evidence로 취급한다.

## 5. `01_작업순서`

| 순서 | Approval Bundle | 분야 | 현재 단계 | 선행 조건 | `BLOCKS` | `INFORMS` | 승인 상태 | 정본 반영 | 소비처 반영 | 구현 | 검증 | 이미지 필요 | 다음 작업 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 6. `02_현재_확정결정` — legacy 결정 원장 판독

| Decision ID | 분야 묶음 | 현재 한 문장 결정 | 결정 이유·플레이어 가치 | Evidence ID | 사용자 승인 | 책임 정본 경로 | main Commit SHA | 구현 상태 | 검증 상태 | Sheet·GitHub 동기화 | 다음 확인 |
|---|---|---|---|---|---|---|---|---|---|---|---|

Sheet의 `CURRENT` 표시는 현재 사용자 결정이나 Notion/repository 정본보다 높은 권한이 아니다. 기존 Decision ID와 고유 근거를 대조하고, 현재 권위와 충돌하면 그대로 승격하지 말고 reconciliation 대상으로 둔다.

## 7. 다섯 분야 tab 공통 열

| 순서 | Decision ID | Approval Bundle | 현재 확정 내용 | 신규 제안 | 변경 이유 | Evidence ID | GPT 권장안 | 사용자 결정 | 선행·후속 | 책임 정본 경로 | main Commit SHA | 구현 상태 | 검증 상태 | 누락·충돌 | 마지막 수정 시각 | 수정 주체 | Sheet·GitHub 동기화 | 최종 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

`최종 상태`: `CURRENT / SUPERSEDED / DEFERRED / REJECTED / BLOCKED_UNVERIFIED`.

Sheet에만 남은 수정은 현재 정본이 아니라 `PROPOSED_SHEET_CHANGE` migration evidence로 기록하고 사용자 결정·현재 정본과 대조한다.

## 8. 의미 구조 상세 보기

아래 표는 기존 Sheet의 unique material을 의미 단위로 판독하기 위한 예시다. 같은 현재 결정·정본·상태를 새 표로 복제하지 않고 올바른 destination에 한 번만 이관한다.

### `11_세계관`

| World ID | 범주 | 현재 규칙·설정 | 플레이어가 아는 시점 | 관련 세력·장소·인물 | 게임플레이 영향 | 금기·모순 방지 | 책임 정본 | 관계도·이미지 | 상태 |
|---|---|---|---|---|---|---|---|---|---|

### `12_핵심루프`

| Loop ID | 단계 | 플레이어 행동 | 선택·고민 | 즉시 피드백 | 보상·손실 | 다음 단계 연결 | 실패·복구 | 관찰 지표 | 흐름도 | 책임 정본 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|

### `13_주요인물`

| Character ID | 이름 | 역할 | 목표 | 성격·가치 | 플레이어 관계 | 핵심 장면·기능 | 시각 키워드 | 표정·포즈·상태 | 관계도·이미지 | 책임 정본 | 이미지 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|

### `14_조연_세력_관계`

| Entity ID | 이름 | 유형 | 소속·세력 | 주요인물 관계 | 기능 | 갈등·비밀 | 등장·정보 공개 시점 | 관련 콘텐츠 | 관계도·이미지 | 책임 정본 | 이미지 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|

### `15_조작_게임규칙`

| Rule ID | 범주 | 입력 장치·키·제스처 | 플레이어 행동 | 발동·성공 조건 | 승리·패배·점수·페널티 | 파라미터·지표 | 단위 | 초기 시험값 | 조정 범위 | 공식·규칙 | 실패·복구 | 플레이어 영향 | 검증 방법 | 검증 상태 | 책임 정본 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### `40_핵심시스템_메인콘텐츠`

| System ID | 시스템·메인콘텐츠 | 해결하는 플레이어 문제 | 핵심 입력 | 규칙·상태 | 출력·보상 | 다른 시스템 연결 | 실패·복구 | 핵심 수치·공식 | 시스템 관계도 | Demo 범위 | 책임 정본 | 검증 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 8. 근거·감사 tab

### `03_근거_라이브러리`

| Evidence ID | 유형 | 출처 | 날짜·버전 | 비교 차원 | 대상 플레이어 | 관찰 사실 | 플레이어 반응 | 현업·공식 권장 | 적용 판정 | 신뢰도 | 후속 검증 |
|---|---|---|---|---|---|---|---|---|---|---|---|

### `04_누락_충돌_감사`

| Audit ID | 날짜 | 작업·질문 | 비교한 main | 비교한 Decision | 비교한 PR | 비교한 정본 | 비교한 구현 | Sheet 상태 | 판정 | 영향 | 수정 위치 | 재검증 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 9. 이미지 tab

### `71_이미지기획_생성목록`

| Image ID | 단계 | 분류 | 목적·사용처 | 관련 Decision·정본 | 브리프 | 비율·해상도 | 유지 요소 | 변경 축 | 레퍼런스·원출처 | 모델·버전 | 우선순위 | 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

단계: `PLANNING_VISUALIZATION / FINAL_VISUAL_CANDIDATE`.

### `72_이미지검수_승인로그`

| Review ID | Image ID | 버전 | 기획 일치 | 실제 화면 가독성 | 구현 가능성 | 일관성 | 재사용·편집 | 권리·유사성 | 오류 | 수정 요청 | 승인자·일시 | 승인 상태 | GitHub·자산 경로 | 런타임 검증 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

승인 상태: `IN_REVIEW / REVISION_REQUIRED / REJECTED / APPROVED_CANDIDATE / PROJECT_ASSET_APPROVED / APPLIED_AND_RUNTIME_VERIFIED`.

## 10. Migration 종료 조건

```text
LEGACY_SHEET_CLASSIFIED
→ UNIQUE_MATERIAL_MAPPED
→ NOTION_OR_REPOSITORY_DESTINATION_UPDATED
→ DESTINATION_READBACK_VERIFIED
→ DUPLICATE_OR_OBSOLETE_NOT_PROMOTED
→ REMAINING_UNMIGRATED_MATERIAL_LISTED | NONE
→ ACTIVE_CONSUMER_REFERENCE_REVIEWED
→ MIGRATED_READBACK_VERIFIED | MIGRATION_PENDING | BLOCKED_UNVERIFIED
```

이 파일의 존재 자체는 Google Sheets를 활성 작업면으로 만들지 않는다. 모든 unique material이 이관·readback되고 외부 active consumer/reference가 0이 되면 P02/CP0의 legacy-retirement 절차에 따라 Sheet 전용 template·routing 참조를 제거한다.