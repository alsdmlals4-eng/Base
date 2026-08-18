# 프로젝트 GDD Google Sheets 정책

이 문서는 Base를 적용한 개별 게임 프로젝트에서 Google Sheets를 어떻게 GDD migration source로 보존하고, GitHub 정본·실제 구현·사용자 편집·AI 참조를 어떻게 연결할지 정의하는 공용 책임 원본이다.

Base 자체는 프로젝트 Sheet를 만들거나 동기화하지 않으며 `BASE_EXCLUDED`다. 정확한 URL·Spreadsheet ID·tab·권한을 확인한 기존 프로젝트만 이 정책의 Sheet migration 계약을 적용한다.

## 1. 목적과 역할

현재 Base의 workspace authority는 다음과 같다.

```text
FIGMA_DEFAULT_VISUAL_WORKSPACE
REPO_NATIVE_STRUCTURED_DATA
GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE
USER_FACING_GDD_WORKSPACE_COMPATIBILITY_ALIAS
```

새 프로젝트와 새 시각 작업의 기본 협업면은 Figma이며, 승인 Decision·상세 규칙은 GitHub 정본, 밸런스·경제·Schema·runtime config 같은 구조화 데이터는 repo-native source가 소유한다.

이미 구성된 프로젝트 Google Sheets는 검증된 이관이 끝날 때까지 `GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE`이며 `MIGRATION_COMPATIBILITY_SURFACE`로 취급한다.

- 사용자가 기존 Sheet에서 프로젝트 전체 흐름, 방향성, 핵심 루프, 메인 시스템, 현재 승인·구현·검증 상태를 확인한다.
- 사용자가 기존 정보를 수정하거나 새 제안을 기록한다.
- AI는 GitHub와 구성된 Google Sheets를 함께 읽어 현재 방향과 변경 제안을 복원한다.
- 긴 기획 전문을 복제하기보다 시각 요약, 핵심 수치, 상태, GitHub 정본 경로를 연결한다.

Google Sheets는 migration 동안 사용자의 기존 GDD 검토·제안 surface를 보존하지만 GitHub 정본을 대체하지 않는다. 등록된 Markdown·JSON이 상세 규칙을, 실제 코드·데이터·Scene·Resource·자산·테스트가 구현 상태를 책임진다.

`USER_FACING_GDD_WORKSPACE_COMPATIBILITY_ALIAS`는 기존 문서·Skill·Adapter·과거 기록에 남아 있는 `USER_FACING_GDD_WORKSPACE`를 **기존 Sheet의 읽기·제안·동기화 호환 의미**로 해석하기 위한 migration alias다. 이 별칭은 새 프로젝트에 Sheet를 만들거나 새 작업의 기본 workspace 권위를 되살리지 않는다.

### 1.1 현업 GDD 템플릿 비교와 채택

| 참조 | 관찰한 구조 | 이 계약의 적용 |
|---|---|---|
| [Nuclino GDD](https://www.nuclino.com/templates/game-design-document) | 범위와 공통 방향을 잡는 살아있는 GDD, 시각 자료와 지속 갱신을 권장 | 허브에서 플레이어 약속·루프·현재 Stage를 먼저 읽고 긴 전문은 정본에 둔다. |
| [CrocoApps GDD](https://crocoapps.com/game-design-document-template/) | 개요·대상·플랫폼·Core Loop를 기능·제작 입력·QA·출시 요구와 연결 | GDD 본문과 근거·감사·제작·검증을 분리하되 Decision ID로 연결한다. |
| [StraySpark 2026 GDD](https://www.strayspark.studio/blog/game-design-document-template-indie-developers-2026) | 짧고 매주 갱신 가능한 living brief, pillar·loop·scope·risk·milestone 연결 | 다섯 분야 묶음과 `02_현재_확정결정`의 단일 원장을 사용한다. |
| [Allo living GDD](https://allo.io/blog/en/game-design-document-template/) | 정적 문서 대신 결정 로그, feature brief, scope matrix를 연결한 living hub | `00`·`05` 요약은 링크와 상태만, 상세은 분야 tab만 책임진다. |

**채택:** 한 화면 요약, Design Pillar·Core Loop·범위·위험·마일스톤 연결, 시스템별 상세, 결정 로그, 주기적 갱신.

**적응:** 기존 Google Sheets에서는 장문 페이지 대신 카드형 요약·Decision ID·정본 경로·상태를 사용하고, migration 뒤 책임 surface는 GitHub/Figma/repo-native로 분리한다.

**제외:** 고정된 대형 GDD 본문 복제, GitHub/실제 구현과 분리된 상태표, 프로젝트 상태를 소유하는 외부 템플릿.

## 2. 권한과 충돌 우선순위

```text
최신 사용자 지시·승인
→ 프로젝트 AGENTS·보안·엔진·데이터 규칙
→ CURRENT_CONFIRMED_DECISIONS.md
→ 등록된 분야 Markdown·JSON 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 구성된 프로젝트 GDD Google Sheets migration source
→ Issue·PR·Commit 이력
→ 외부 근거·과거 대화·AI 추론
```

Sheet는 migration 동안 사용자에게 읽기 쉽고 수정하기 쉬운 호환 surface지만, Sheet 한 곳의 값만으로 승인·구현·검증 완료를 확정하지 않는다.

## 3. AI 공동 읽기 계약

모든 L1 이상 기획·검수·작업 계획에서 프로젝트가 `PROJECT_SHEET_CONFIGURED`이면 다음을 비교한다.

```text
GitHub main HEAD
→ 현재 승인 Decision
→ 분야 책임 원본
→ 실제 구현·자산·테스트
→ 프로젝트 GDD Google Sheets 최신 tab·행·이미지·수치
→ 동일 Goal의 열린·최근 병합 PR
→ Decision ID·Commit SHA·수정 시각·대체 관계 비교
```

AI는 GitHub만 읽고 사용자의 최신 Sheet 제안을 무시하지 않으며, Sheet만 읽고 방향성·메인 시스템·구현 상태를 확정하지 않는다.

## 4. 사용자 Sheet 편집 처리

사용자의 Sheet 수정은 자동 삭제하거나 GitHub 값으로 즉시 덮어쓰지 않는다. GitHub 정본에 아직 없는 수정은 `PROPOSED_SHEET_CHANGE`로 보존한다.

```text
사용자 Sheet 수정
→ PROPOSED_SHEET_CHANGE
→ GitHub 정본·실제 구현과 차이 분석
→ 기존 승인 Decision인지 신규 제안인지 분류
→ 기술 기본값은 RECOMMENDED_DEFAULT
→ 코어·중요 기획·주요 UX·콘텐츠 의미는 USER_DECISION_REQUIRED
→ 승인된 변경을 GitHub 정본에 반영
→ main Commit SHA 기록
→ Sheet 재동기화·재조회
→ SYNCED
```

## 5. 동기화 상태

- `SYNCED`: 승인 내용·Decision ID·Commit SHA·대체 관계가 양쪽에서 일치
- `PROPOSED_SHEET_CHANGE`: Sheet에만 존재하는 사용자 제안
- `GITHUB_UPDATE_PENDING_SHEET`: GitHub 정본이 최신이며 Sheet 반영 필요
- `SHEET_UPDATE_PENDING_GITHUB`: 승인된 Sheet 변경의 GitHub 반영 필요
- `SHEET_GITHUB_CONFLICT`: 양쪽이 서로 다른 현재 결정을 주장
- `NOT_CONFIGURED`: 정확한 Sheet URL·권한·tab을 확인하지 못함
- `BASE_EXCLUDED`: Base 저장소 자체
- `BLOCKED_UNVERIFIED`: 읽기·쓰기·재조회 증거 부족

자동으로 어느 한쪽을 덮어쓰지 않는다. 최신 사용자 승인, Decision ID, Commit SHA, 수정 시각, 분야 정본과 실제 구현으로 누락 위치를 판정한다.

## 6. 표준 GDD 6영역

### 1. 문서 개요

- 게임 제목·가제
- 타깃 플랫폼
- 장르·엔진
- 타깃 유저와 플레이 상황
- 핵심 카피·한 문장 플레이어 약속
- 현재 Stage·Work Mode·Vertical Slice 상태

### 2. 핵심 게임플레이

- 핵심 루프 흐름도
- 조작법과 입력 장치 매핑
- 승리·패배 조건
- 점수·판정·페널티·실패 후 복구
- 플레이어 선택·고민·즉시 피드백·보상

### 3. 게임 시스템

- 캐릭터·클래스·능력치·스킬
- 전투·상태 이상·데미지 공식
- 성장·경제·재화·획득처·소모처
- 메인 시스템 간 입력·출력·의존 관계
- 저장·불러오기·데이터 책임

### 4. 스토리 및 세계관

- 시놉시스·세계 규칙
- 주요인물·조연·세력·관계도
- 정보 공개 시점·복선·금기·모순 방지
- 스테이지·월드맵·레벨·콘텐츠 구조

### 5. 아트 및 사운드

- Visual Pillar·Shape Language·Color·Value
- 캐릭터·환경·UI·VFX·애니메이션 방향
- 메인 화면·HUD·팝업 와이어프레임
- BGM·SFX·오디오 정보 전달
- 이미지 계획·생성·검수·승인 상태

### 6. 기술 및 로드맵

- 목표 플랫폼·최소/권장 사양
- 싱글·멀티·네트워크·온라인 의존성
- Godot 버전·렌더러·해상도·입력·성능 예산
- 마일스톤·Demo-First Vertical Slice·본제작·출시
- 위험·선행 조건·검증·롤백

## 7. 사람이 읽는 정보 구조와 중복 방지

GDD는 탭 수를 늘려 같은 내용을 여러 번 적는 문서가 아니라, **한 번 기록하고 여러 화면에서 참조하는 살아있는 작업면**이다. 다음 세 층을 분리한다.

```text
00_프로젝트_허브 · 05_GDD_요약
  = 사람이 1~2분 안에 현재 방향·핵심 흐름·다음 결정을 파악하는 읽기 층

02_현재_확정결정
  = 단일 현재 결정 원장: 현재 유효한 Decision ID, 한 문장 결정, 근거, 정본, 상태의 유일한 목록

06_시각_작업면 (선택적 색인)
  = GDD·외부 협업 시각 Artifact를 같은 ID로 연결하는 링크 층

10_경험 · 20_시스템_콘텐츠 · 30_세계_서사 · 40_표현 · 50_제작_검증
  = 결정의 의미·흐름·수치·시각·검증을 설명하는 분야 층
```

- **단일 현재 결정 원장:** `02_현재_확정결정`만 `CURRENT` 결정을 보유한다. `SUPERSEDED` 결정과 전체 변경 이력은 `99_변경이력`으로 보낸다.
- **Decision ID 참조:** 분야 층은 결정의 전문이나 상태를 복사하지 않고 `Decision ID`를 참조한다. 분야별 행에는 해당 분야에 필요한 규칙·흐름·수치·시각·검증만 둔다.
- **중복 금지:** `00_프로젝트_허브`와 `05_GDD_요약`은 카드형 요약·링크·상태만 제공한다. 시스템, 인물, 세계관, UX, 로드맵의 상세 내용을 다시 적지 않는다.
- **시각 작업면 색인:** `06_시각_작업면`은 실제 Figma·Whimsical·기타 Artifact가 있을 때만 쓴다. 각 행은 `Artifact ID`, `usage_context`(`GDD|EXTERNAL_COLLABORATION|BOTH`), 목적, Decision ID, 책임 정본, 링크·Snapshot, 상태와 다음 Gate만 가진다. 보드·Frame 전문을 Sheet에 복사하지 않는다. GDD 안·밖 어느 용도도 이 색인을 통해 연결할 수 있으며, 사용하지 않는 프로젝트에 tab을 강제하지 않는다.
- **다섯 묶음:** 경험(플레이어 약속·루프·조작), 시스템·콘텐츠(규칙·성장·경제·콘텐츠), 세계·서사(세계 규칙·인물·관계·정보 공개), 표현(UX/UI·접근성·아트·오디오·시각 자산), 제작·검증(범위·기술·위험·마일스톤·플레이테스트)으로 유사 책임을 묶는다.
- 기존 세부 tab은 삭제를 전제하지 않는다. 소비자와 이력이 있으면 위 다섯 묶음의 **상세 보기**로 남기고, 그 외에는 병합 후보·보존 계획·사용자 승인 없이는 변경하지 않는다.

## 8. 시각화 우선

각 주요 tab은 다음 순서를 기본으로 한다.

```text
한 화면 핵심 요약
→ 흐름도·관계도·상태 다이어그램
→ 와이어프레임·실제 캡처·레퍼런스 이미지
→ 핵심 수치·상태 표
→ 상세 GitHub 정본 경로
```

- 긴 텍스트보다 비교 가능한 표, 다이어그램, 이미지, 실제 화면을 우선한다.
- 시각 자료에는 Asset ID·원출처·승인 상태·GitHub 경로를 기록한다.
- 준비되지 않은 시각 자료는 가짜 이미지로 채우지 않고 `VISUAL_NOT_PREPARED`로 둔다.
- 이미지는 기획·정보 전달을 보조하며 실제 수치·규칙의 정본이 아니다.

## 9. 지속적인 업데이트

GDD는 살아있는 문서다. 모든 주요 행은 다음 메타데이터를 가진다.

- Decision ID
- 책임 정본 경로
- main Commit SHA
- 마지막 수정 시각
- 수정 주체
- 승인 상태
- 구현 상태
- 검증 상태
- Sheet·GitHub 동기화 상태
- 다음 확인·재검증 조건

승인 결정은 장기 작업 checkpoint까지 미루지 않고 즉시 GitHub 정본에 반영한다. 구성된 legacy Sheet가 있으면 같은 승인 단위에서 Sheet에도 반영한 뒤 양쪽을 재조회한다.

## 10. 명확한 수치화

`높게`, `빠르게`, `강하게`, `많이` 같은 표현만으로 완료하지 않는다. 수치가 적용되는 항목은 다음 필드를 가진다.

- 파라미터·지표 이름
- 단위
- 초기 시험값
- 조정 범위
- 공식·계산 규칙
- 적용 조건·대상
- 플레이어 영향
- 검증 방법
- 검증 상태
- 재조정 조건

예: `점프를 높게`가 아니라 `점프 높이 3.5 m, 체공 시간 0.8 s, 초기 시험값, 플레이테스트 조정 필요`로 기록한다.

## 11. 설치·검증

아래 설치·갱신 순서는 이미 `PROJECT_SHEET_CONFIGURED`인 기존 Sheet의 migration compatibility 유지·이관에만 적용한다.

```text
정확한 기존 Sheet URL·ID·권한 확인
→ 기존 tab·값·수식·이미지·검증 규칙 감사
→ 단일 현재 결정 원장과 기존 분야 tab의 Decision ID 매핑
→ 표준 GDD 영역과 프로젝트 고유 영역 매핑
→ 기존 정보 보존 계획
→ 필요한 호환 tab·열·시각 요약 갱신
→ GitHub 정본 경로·Decision ID·Commit 연결
→ 실제 현재 상태 동기화
→ 사용자 편집 범위 확인
→ GitHub/Figma/repo-native replacement pointer·readback 확인
→ 재읽기·시각 검수·충돌 판정
```

완료는 파일이나 tab 존재가 아니라 기존 Sheet의 고유 정보·제안·대체 관계를 GitHub/Figma/repo-native 책임 surface에서 복원할 수 있고, 필요한 readback과 replacement pointer가 검증됐을 때다.

## 12. HTML 대시보드 경계

일반 프로젝트 기획·상태 확인은 GitHub 정본을 우선하고, 새 시각 협업은 Figma, 구조화 데이터는 repo-native source를 사용한다. 기존 프로젝트 GDD Google Sheets는 migration·proposal·readback이 필요한 경우에만 사용한다. HTML 대시보드는 사용자가 명시적으로 요청하거나 기존 대시보드 유지보수가 필요한 경우에만 선택적으로 사용한다.

## 13. 실패 조건

- Sheet를 GitHub 상세 정본이나 실제 구현 상태의 단일 권한으로 사용함
- 새 프로젝트에 기본 GDD Sheet를 강제 생성함
- 사용자 Sheet 편집을 읽지 않고 자동 덮어씀
- Sheet-only 제안을 승인 결정처럼 구현함
- replacement pointer와 readback 없이 기존 Sheet를 폐기·삭제함
- GitHub만 갱신하거나 구성된 Sheet만 갱신하고 `SYNCED`로 보고함
- 같은 현재 결정·상태·정본 경로를 허브·요약·분야 tab에 복사해 서로 다른 값을 만들 수 있게 둠
- 긴 자유 메모만 두고 핵심 흐름·이미지·수치·상태를 찾을 수 없음
- 단위·초기 시험값·조정 범위·검증 상태 없이 모호한 수치 표현만 유지함
- 이미지 안 임시 수치·문구를 공식 기획값으로 사용함
- 정확한 URL·권한을 확인하지 않고 새 Sheet를 추정 생성함
