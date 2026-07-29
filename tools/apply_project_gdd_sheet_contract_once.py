from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    content = read(path)
    count = content.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one occurrence, found {count}: {old!r}")
    write(path, content.replace(old, new, 1))


def insert_after(path: str, marker: str, addition: str) -> None:
    content = read(path)
    if addition.strip() in content:
        return
    count = content.count(marker)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {marker!r}")
    write(path, content.replace(marker, marker + addition, 1))


def insert_before(path: str, marker: str, addition: str) -> None:
    content = read(path)
    if addition.strip() in content:
        return
    count = content.count(marker)
    if count != 1:
        raise RuntimeError(f"{path}: expected one marker, found {count}: {marker!r}")
    write(path, content.replace(marker, addition + marker, 1))


def replace_section(path: str, start: str, end: str, replacement: str) -> None:
    content = read(path)
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    matches = list(pattern.finditer(content))
    if len(matches) != 1:
        raise RuntimeError(f"{path}: section {start!r} -> {end!r} matched {len(matches)}")
    write(path, pattern.sub(replacement + end, content, count=1))


POLICY = """# 프로젝트 GDD Google Sheets 정책

이 문서는 Base를 적용한 개별 게임 프로젝트에서 Google Sheets를 어떻게 GDD로 사용하고, GitHub 정본·실제 구현·사용자 편집·AI 참조를 어떻게 연결할지 정의하는 공용 책임 원본이다.

Base 자체는 프로젝트 Sheet를 만들거나 동기화하지 않으며 `BASE_EXCLUDED`다. 정확한 URL·Spreadsheet ID·tab·권한을 확인한 개별 프로젝트만 이 정책을 적용한다.

## 1. 목적과 역할

프로젝트 Google Sheets의 역할은 `USER_FACING_GDD_WORKSPACE`다.

- 사용자가 프로젝트 전체 흐름, 방향성, 핵심 루프, 메인 시스템, 현재 승인·구현·검증 상태를 한곳에서 확인한다.
- 사용자가 기존 정보를 수정하거나 새 제안을 기록한다.
- AI는 GitHub와 Google Sheets를 함께 읽어 현재 방향과 변경 제안을 복원한다.
- 긴 기획 전문을 복제하기보다 시각 요약, 핵심 수치, 상태, GitHub 정본 경로를 연결한다.

Google Sheets는 사용자의 기본 GDD 작업면이지만 GitHub 정본을 대체하지 않는다. 등록된 Markdown·JSON이 상세 규칙을, 실제 코드·데이터·Scene·Resource·자산·테스트가 구현 상태를 책임진다.

## 2. 권한과 충돌 우선순위

```text
최신 사용자 지시·승인
→ 프로젝트 AGENTS·보안·엔진·데이터 규칙
→ CURRENT_CONFIRMED_DECISIONS.md
→ 등록된 분야 Markdown·JSON 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 프로젝트 GDD Google Sheets
→ Issue·PR·Commit 이력
→ 외부 근거·과거 대화·AI 추론
```

Sheet는 사용자에게 가장 읽기 쉽고 수정하기 쉬운 작업면이지만, Sheet 한 곳의 값만으로 승인·구현·검증 완료를 확정하지 않는다.

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

## 7. 시각화 우선

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

## 8. 지속적인 업데이트

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

승인 결정은 장기 작업 checkpoint까지 미루지 않고 즉시 GitHub 정본과 Sheet에 반영한 뒤 양쪽을 재조회한다.

## 9. 명확한 수치화

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

## 10. 설치·검증

설치와 갱신은 다음 순서를 따른다.

```text
정확한 Sheet URL·ID·권한 확인
→ 기존 tab·값·수식·이미지·검증 규칙 감사
→ 표준 GDD 영역과 프로젝트 고유 영역 매핑
→ 기존 정보 보존 계획
→ tab·열·시각 요약 설치
→ GitHub 정본 경로·Decision ID·Commit 연결
→ 실제 현재 상태 동기화
→ 사용자 편집 범위 확인
→ 재읽기·시각 검수·충돌 판정
```

완료는 파일이나 tab 존재가 아니라 GitHub 정본·실제 구현·Sheet의 책임과 동기화 상태를 복원할 수 있을 때다.

## 11. HTML 대시보드 경계

일반 프로젝트 기획·상태 확인은 GitHub 정본과 프로젝트 GDD Google Sheets를 우선한다. HTML 대시보드는 사용자가 명시적으로 요청하거나 기존 대시보드 유지보수가 필요한 경우에만 선택적으로 사용한다.

## 12. 실패 조건

- Sheet를 GitHub 상세 정본이나 실제 구현 상태의 단일 권한으로 사용함
- 사용자 Sheet 편집을 읽지 않고 자동 덮어씀
- Sheet-only 제안을 승인 결정처럼 구현함
- GitHub만 갱신하거나 Sheet만 갱신하고 `SYNCED`로 보고함
- 긴 자유 메모만 두고 핵심 흐름·이미지·수치·상태를 찾을 수 없음
- 단위·초기 시험값·조정 범위·검증 상태 없이 모호한 수치 표현만 유지함
- 이미지 안 임시 수치·문구를 공식 기획값으로 사용함
- 정확한 URL·권한을 확인하지 않고 새 Sheet를 추정 생성함
"""

WORKBOOK = """# Project Google Sheets Workbook Contract

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
"""

TABS = """# 프로젝트 기획 작업순서·Google Sheets GDD tab Template

이 Template은 Base 자체가 아니라 Base를 적용한 개별 프로젝트에서 사용한다. 프로젝트 Google Sheets가 없거나 정확한 URL을 확인하지 못하면 `NOT_CONFIGURED`로 기록하고 새 Sheet나 임의 후보를 추정하지 않는다.

공용 정책: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`

## 1. 설치할 tab

```text
00_프로젝트_허브
01_작업순서
02_현재_확정결정
03_근거_라이브러리
04_누락_충돌_감사
05_GDD_요약
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
51_미니게임                    # 필요할 때만
52_글쓰기_서사                 # 필요할 때만
60_UX_UI_접근성
70_아트_오디오_에셋
71_이미지기획_생성목록
72_이미지검수_승인로그
80_데모_버티컬슬라이스_플레이테스트
90_본제작_출시_사업
98_Base_반영후보
99_변경이력
```

## 2. 표준 GDD 6영역 매핑

| 표준 GDD 영역 | 주요 tab | 필수 시각·요약 |
|---|---|---|
| 1. 문서 개요 | `00_프로젝트_허브`, `05_GDD_요약`, `10_제품방향` | 핵심 카피, 프로젝트 흐름, 현재 Stage |
| 2. 핵심 게임플레이 | `12_핵심루프`, `15_조작_게임규칙`, `20_코어경험_데모목표` | Core Loop 흐름도, 입력 매핑, 승패 흐름 |
| 3. 게임 시스템 | `40_핵심시스템_메인콘텐츠`, `41_성장_경제` | 시스템 관계도, 공식·수치, 입력·출력 |
| 4. 스토리 및 세계관 | `11_세계관`, `13_주요인물`, `14_조연_세력_관계`, `50_메인콘텐츠`, `52_글쓰기_서사` | 관계도, 월드·스테이지 구조, 정보 공개 흐름 |
| 5. 아트 및 사운드 | `60_UX_UI_접근성`, `70_아트_오디오_에셋`, `71_이미지기획_생성목록`, `72_이미지검수_승인로그` | 와이어프레임, 캡처, 레퍼런스, 오디오 역할 |
| 6. 기술 및 로드맵 | `01_작업순서`, `30_데모범위_품질기준_제작기반`, `80_데모_버티컬슬라이스_플레이테스트`, `90_본제작_출시_사업` | 마일스톤, 기술 의존성, 성능·검증 상태 |

## 3. `00_프로젝트_허브`

| 프로젝트 | 한 문장 핵심 카피 | 장르·플랫폼·엔진 | 타깃 유저·플레이 상황 | 현재 Stage | 현재 Work Mode | Base SHA | Sheet 상태 | GitHub | 다음 Approval Bundle | 차단 Finding |
|---|---|---|---|---|---|---|---|---|---|---|

## 4. `05_GDD_요약`

| GDD 영역 | 현재 한 문장 요약 | 대표 흐름도·관계도 | 와이어프레임·이미지·캡처 | 핵심 수치·상태 | 책임 정본 경로 | main Commit SHA | 마지막 수정 시각 | 수정 주체 | 동기화 상태 | 다음 확인 |
|---|---|---|---|---|---|---|---|---|---|---|

이 tab은 장문 본책이 아니라 사용자가 전체 게임을 빠르게 훑는 시작 화면이다.

## 5. `01_작업순서`

| 순서 | Approval Bundle | 분야 | 현재 단계 | 선행 조건 | `BLOCKS` | `INFORMS` | 승인 상태 | 정본 반영 | 소비처 반영 | 구현 | 검증 | 이미지 필요 | 다음 작업 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 6. 분야별 tab 공통 열

| 순서 | Decision ID | Approval Bundle | 현재 확정 내용 | 신규 제안 | 변경 이유 | Evidence ID | GPT 권장안 | 사용자 결정 | 선행·후속 | 책임 정본 경로 | main Commit SHA | 구현 상태 | 검증 상태 | 누락·충돌 | 마지막 수정 시각 | 수정 주체 | Sheet·GitHub 동기화 | 최종 상태 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

`최종 상태`: `CURRENT / SUPERSEDED / DEFERRED / REJECTED / BLOCKED_UNVERIFIED`.

Sheet에만 있는 수정은 `PROPOSED_SHEET_CHANGE`로 기록한다.

## 7. 의미 구조 tab

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

## 10. Approval Bundle 종료 조건

```text
APPROVED
→ CANON_UPDATED
→ CONSUMERS_UPDATED
→ PROJECT_SHEET_UPDATED | NOT_CONFIGURED
→ VISUALS_NOT_REQUIRED | VISUALS_REVIEWED
→ IMPLEMENTED | IMPLEMENTATION_PENDING
→ VALIDATED | BLOCKED_UNVERIFIED
→ SYNCED | PROPOSED_SHEET_CHANGE | SHEET_GITHUB_CONFLICT
→ NO_CONFLICT | CONFLICT_FIXED | USER_DECISION_REQUIRED | BLOCKED_UNVERIFIED
```
"""


def update_policy_and_templates() -> None:
    write("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md", POLICY)
    write("templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md", WORKBOOK)
    write("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md", TABS)


def update_sync_policy() -> None:
    path = "docs/CONFIRMED_DECISION_SYNC_POLICY.md"
    insert_after(
        path,
        "실제 변경 검증은 `skills/reviewing-and-validating-project-changes/SKILL.md`가 계속 책임진다.",
        " 프로젝트 GDD Google Sheets의 역할·편집·동기화 계약은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`가 책임진다.",
    )
    replace_once(
        path,
        "| 프로젝트 Google Sheets | 사용자가 확인·편집하는 동기화 작업면 | GitHub 정본의 운영 mirror |",
        "| 프로젝트 Google Sheets | `USER_FACING_GDD_WORKSPACE`: 사용자가 전체 흐름을 확인·수정하고 AI가 GitHub와 함께 읽는 GDD 작업면 | GitHub 정본·실제 구현을 대체하지 않는 제안·동기화 surface |",
    )
    insert_before(
        path,
        "## 10. 동기화 상태",
        """### 9.1 프로젝트 GDD Sheet 편집 처리

프로젝트 Sheet는 단순 읽기 전용 mirror가 아니다. 사용자가 방향성·메인 시스템·수치·설명을 수정하면 자동 덮어쓰지 않고 `PROPOSED_SHEET_CHANGE`로 보존한다.

```text
PROPOSED_SHEET_CHANGE
→ 최신 main·Decision·분야 정본·실제 구현과 비교
→ 기존 승인 복원 또는 신규 제안 분류
→ 승인된 변경만 GitHub 정본에 반영
→ main Commit SHA 기록
→ Sheet 재동기화·재조회
→ SYNCED
```

추가 상태:

```text
GITHUB_UPDATE_PENDING_SHEET
SHEET_UPDATE_PENDING_GITHUB
SHEET_GITHUB_CONFLICT
```

GitHub와 Sheet가 충돌하면 어느 한쪽을 자동으로 덮어쓰지 않는다. 최신 사용자 승인, Decision ID, Commit SHA, 수정 시각, 분야 정본과 실제 구현으로 누락 위치를 판정한다.

""",
    )


def update_planning_policy() -> None:
    path = "docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md"
    insert_after(
        path,
        "프로젝트 Sheet와 GPT 이미지 생성·검수는 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`가 책임진다.",
        " 프로젝트 GDD Google Sheets의 사용자 작업면·편집·동기화·시각화·수치화 계약은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`가 책임진다.",
    )
    replacement = """### Google Sheets

- Base 저장소 자체: `BASE_EXCLUDED`. 프로젝트 Google Sheets를 만들거나 동기화하지 않는다.
- 개별 프로젝트의 정확한 Sheet URL·ID·tab·권한이 확인됨: `PROJECT_SHEET_CONFIGURED`이며 역할은 `USER_FACING_GDD_WORKSPACE`다.
- 개별 프로젝트에 Sheet가 없거나 아직 연결하지 않음: `NOT_CONFIGURED`.
- Base 작업을 Sheet 미동기화로 실패 처리하지 않는다.
- 사용자는 Sheet에서 전체 GDD 흐름·방향성·메인 시스템·이미지·수치·상태를 확인하고 수정한다.
- AI는 GitHub 정본·실제 파일과 Sheet를 함께 읽고 `PROPOSED_SHEET_CHANGE`·누락·충돌을 판정한다.
- Sheet는 시각화 우선, 지속 갱신, 명확한 수치화를 따르며 GitHub 정본이나 실제 구현을 대체하지 않는다.
- 승인된 변경만 GitHub 정본·Commit·Sheet에 반영하고 재조회해 `SYNCED`를 증명한다.

"""
    replace_section(path, "### Google Sheets\n", "### 내용 보존", replacement)
    insert_after(path, "04_누락_충돌_감사\n", "05_GDD_요약\n")
    insert_after(path, "14_조연_세력_관계\n", "15_조작_게임규칙\n")


def update_entrypoints() -> None:
    insert_after(
        "README.md",
        "- [프로젝트 Google Sheets Workbook 계약](templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md)",
        "\n- [프로젝트 GDD Google Sheets 정책](docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md)",
    )
    replace_once(
        "README.md",
        "활성 Registry 스킬은 책임 경계 재검토와 최적화 뒤 **27개**입니다.",
        "활성 Registry는 **핵심 통합 실행 Skill 13개 + 구조·운영·지원 Skill 14개 = 전체 ACTIVE Skill 27개**를 관리합니다. 기계적 권한은 `skills/SKILL_REGISTRY.json`이 가집니다.",
    )
    insert_before(
        "README.md",
        "## 프로젝트 책임 원본",
        """## 프로젝트 GDD와 선택형 대시보드

일반 프로젝트 기획·상태 확인은 GitHub 정본과 **프로젝트 GDD Google Sheets**를 우선합니다. HTML 대시보드는 사용자가 명시적으로 요청하거나 기존 대시보드 유지보수가 필요한 경우에만 선택적으로 사용합니다.

""",
    )

    replace_once(
        "AGENTS.md",
        "활성 Skill은 13개이며 모두 `load_by_default=false`다. 통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 새 Skill과 Skill Mode로 변환한다. 새 Registry·문서·작업 계약에는 새 ID만 사용한다.",
        "핵심 통합 실행 Skill은 13개이며, 구조·운영·지원 Skill 14개를 포함한 **전체 ACTIVE Skill은 27개**다. 모두 `load_by_default=false`이며 기계적 권한은 `skills/SKILL_REGISTRY.json`이 가진다. 통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 새 Skill과 Skill Mode로 변환한다. 새 Registry·문서·작업 계약에는 새 ID만 사용한다.",
    )
    insert_after(
        "AGENTS.md",
        "- Base 저장소 자체는 프로젝트 Google Sheets 동기화 대상이 아니다. 개별 프로젝트만 Sheet가 구성됐을 때 동기화한다.",
        "\n- 구성된 프로젝트 Sheet는 `USER_FACING_GDD_WORKSPACE`이며 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`를 따른다. 사용자의 Sheet 수정은 `PROPOSED_SHEET_CHANGE`로 보존하고 GitHub 정본·실제 파일과 비교한다.\n- 일반 기획·상태 확인은 GitHub 정본과 프로젝트 GDD Google Sheets를 우선하며 HTML 대시보드는 사용자 명시 요청 또는 기존 유지보수에만 사용한다.",
    )

    insert_after(
        "START_HERE.md",
        "→ Base Documentation Map",\n        "\n→ 프로젝트가 Sheet를 사용하면 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`",
    )
    insert_after(
        "START_HERE.md",
        "공용 구조와 상태·발행 정책의 단일 설명 원본은 `docs/OPERATING_MODEL.md`다. 이 문서는 요청을 해당 실행 Skill로 라우팅하는 역할만 가진다.",
        " 프로젝트 GDD Google Sheets 작업은 GitHub 정본과 함께 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`를 읽는다.",
    )

    insert_after(
        "docs/OPERATING_MODEL.md",
        "Base에는 여러 프로젝트에서 재사용 가능한 판단·절차·검증만 둔다. 프로젝트 고유 세계관·수치·경로·자산·구현 상태는 대상 프로젝트가 책임진다.",
        " 구성된 프로젝트 Google Sheets는 `USER_FACING_GDD_WORKSPACE`로 사용하며 상세 계약은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`가 책임진다.",
    )
    insert_before(
        "docs/OPERATING_MODEL.md",
        "Registry 정책:",
        "핵심 통합 실행 Skill은 13개이며 구조·운영·지원 Skill 14개를 포함한 **전체 ACTIVE Skill은 27개**다. 기계적 목록과 상태는 Registry를 따른다.\n\n",
    )
    insert_after(
        "docs/OPERATING_MODEL.md",
        "실제 상태 → 코드·데이터·자산·테스트·캡처·프로파일",
        "\n사용자 GDD 작업면 → 프로젝트 Google Sheets(`USER_FACING_GDD_WORKSPACE`), 제안 편집은 `PROPOSED_SHEET_CHANGE`",
    )
    insert_before(
        "docs/OPERATING_MODEL.md",
        "## 구조 최적화·작업 지원 Skill",
        """## 프로젝트 GDD와 HTML 대시보드 경계

일반 프로젝트의 전체 흐름 확인·정보 수정은 GitHub 정본과 프로젝트 GDD Google Sheets를 우선한다. HTML 대시보드는 사용자 명시 요청 또는 기존 대시보드 유지보수에서만 선택적으로 사용한다.

""",
    )

    row = "| 기획 작업순서·근거·데모 우선 | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` | 누락·충돌 선감사, 3층 근거 묶음, 분야별 Approval Bundle, 소비처 전파, 개별 프로젝트 Sheet tab, Demo-First Vertical Slice |"
    insert_after(
        "docs/DOCUMENTATION_MAP.md",
        row,
        "\n| 프로젝트 GDD Google Sheets | `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md` | 사용자 중심 시각형 GDD 작업면, Sheet 편집 제안, GitHub·Sheet 공동 읽기, 지속 갱신·수치화·동기화 |",
    )
    insert_after(
        "docs/DOCUMENTATION_MAP.md",
        "## 4. 활성 실행 스킬",
        "\n\n핵심 통합 실행 Skill 13개와 구조·운영·지원 Skill 14개를 합쳐 **전체 ACTIVE Skill은 27개**다. 기계적 권한은 `skills/SKILL_REGISTRY.json`이 가진다.",
    )
    insert_before(
        "docs/DOCUMENTATION_MAP.md",
        "## 5. 자동 호출 정책",
        """### 프로젝트 GDD·대시보드 선택 기준

일반 프로젝트 기획·상태 확인은 GitHub 정본과 **프로젝트 GDD Google Sheets**를 우선한다. HTML 대시보드는 사용자가 명시적으로 요청하거나 기존 대시보드 유지보수가 필요한 경우에만 호출한다.

""",
    )


def update_skills_and_registry() -> None:
    intake = "skills/managing-project-intake-and-work-contract/SKILL.md"
    insert_after(
        intake,
        "승인 결정 복원·중복 질문 방지·GitHub·Google Sheets 동기화: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`",
        "\n\n프로젝트 GDD Google Sheets 역할·편집·시각화·수치화: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`",
    )
    insert_before(
        intake,
        "## State model",
        """## Project GDD Google Sheets handling

프로젝트가 구성된 Sheet를 사용하면 이를 `USER_FACING_GDD_WORKSPACE`로 읽는다. 최신 GitHub 정본·실제 파일과 Sheet를 비교하고, Sheet에만 있는 사용자 수정은 `PROPOSED_SHEET_CHANGE`로 보존한다. 기술 기본값과 중요 기획 결정을 분리하고 승인된 변경만 GitHub 정본·Commit·Sheet에 반영한 뒤 재조회한다.

""",
    )

    ops = "skills/managing-game-project-operating-system/SKILL.md"
    insert_after(
        ops,
        "신규 설치, 기존 구조 감사, 구형 파일 정리, 승인된 마이그레이션과 운영체계 검수는 같은 책임 원본·참조·복구 계약을 공유한다. `Work Mode`와 `Skill Mode`를 구분하며, 읽기 전용 조사와 승인된 쓰기 작업을 혼동하지 않는다.",
        " 프로젝트 GDD Google Sheets 설치·감사·검증은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`를 따른다.",
    )
    insert_before(
        ops,
        "## Skill Mode: install",
        """## Project GDD Google Sheets contract

정확한 Sheet URL·권한이 확인된 프로젝트는 `USER_FACING_GDD_WORKSPACE`로 설치한다. 기존 값·수식·이미지·사용자 편집을 먼저 감사하고, Sheet-only 수정은 `PROPOSED_SHEET_CHANGE`로 보존한다. `install / audit / verify`는 GitHub 정본·실제 구현·Sheet의 Decision ID·Commit·수정 시각·동기화 상태를 비교한다.

""",
    )

    design = "skills/managing-design-documents/SKILL.md"
    insert_after(
        design,
        "공용 승인 동기화 계약은 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 따른다.",
        "\n\n프로젝트 GDD Google Sheets의 사용자 작업면·제안 편집·시각화·수치화 계약은 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`를 따른다.",
    )
    insert_before(
        design,
        "## Publication policy",
        """## Project GDD Google Sheets responsibility

프로젝트 Sheet는 `USER_FACING_GDD_WORKSPACE`이며 사용자의 전체 흐름 확인과 직접 수정에 사용한다. Sheet에만 있는 수정은 `PROPOSED_SHEET_CHANGE`로 기록하고, 등록된 분야 정본과 실제 구현을 비교해 승인된 변경만 GitHub 정본·Commit·Sheet에 동기화한다. Sheet의 시각 요약과 수치 표는 상세 Markdown·JSON 정본을 대체하지 않는다.

""",
    )

    registry_path = ROOT / "skills/SKILL_REGISTRY.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    for entry in registry["skills"]:
        skill_id = entry["skill_id"]
        if skill_id in {
            "managing-project-intake-and-work-contract",
            "managing-game-project-operating-system",
            "managing-design-documents",
        }:
            for tag in ("project-gdd-sheet", "gdd-workspace", "proposed-sheet-change"):
                if tag not in entry["trigger_tags"]:
                    entry["trigger_tags"].append(tag)
            clause = " 프로젝트 GDD Google Sheets를 USER_FACING_GDD_WORKSPACE로 읽고 PROPOSED_SHEET_CHANGE를 GitHub 정본·실제 구현과 비교한다."
            if clause.strip() not in entry["use_when"][0]:
                entry["use_when"][0] += clause
            entry["last_reviewed_at"] = "2026-07-29"
        if skill_id == "building-project-visual-dashboards":
            entry["use_when"] = [
                "사용자가 HTML 대시보드를 명시적으로 요청했거나 기존 프로젝트 대시보드 유지보수·시각 상태판이 필요한 경우에만 정본 연결형 대시보드를 만든다."
            ]
            entry["do_not_use_when"] = [
                "GitHub 정본과 프로젝트 GDD Google Sheets로 전체 흐름·상태 확인·수정이 충분하거나 사용자가 HTML 대시보드를 사용하지 않는 경우다."
            ]
            entry["last_reviewed_at"] = "2026-07-29"
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def update_reference_freshness() -> None:
    path = ROOT / ".github/reference-freshness.json"
    config = json.loads(path.read_text(encoding="utf-8"))
    rule_name = "project-gdd-google-sheets-entrypoints"
    if not any(rule.get("name") == rule_name for rule in config["canonical_reference_rules"]):
        config["canonical_reference_rules"].append(
            {
                "name": rule_name,
                "canonical_path": "docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md",
                "reference_tokens": [
                    "docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md",
                    "PROJECT_GDD_GOOGLE_SHEETS_POLICY.md",
                ],
                "required_consumers": [
                    "README.md",
                    "START_HERE.md",
                    "AGENTS.md",
                    "docs/OPERATING_MODEL.md",
                    "docs/DOCUMENTATION_MAP.md",
                    "docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md",
                    "skills/managing-project-intake-and-work-contract/SKILL.md",
                    "skills/managing-game-project-operating-system/SKILL.md",
                    "skills/managing-design-documents/SKILL.md",
                    "templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md",
                    "templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md",
                ],
            }
        )
    for rule in config["coupled_change_rules"]:
        if rule["name"] == "local-skill-contract-registry-learning-sync":
            if "tests/test_project_gdd_google_sheets_contract.py" not in rule["require_any_changed"]:
                rule["require_any_changed"].append(
                    "tests/test_project_gdd_google_sheets_contract.py"
                )
        if rule["name"] == "registry-structure-test-sync":
            if "tests/test_project_gdd_google_sheets_contract.py" not in rule["require_any_changed"]:
                rule["require_any_changed"].append(
                    "tests/test_project_gdd_google_sheets_contract.py"
                )
        if rule["name"] == "bca-visual-sheet-policy-sync":
            for changed in (
                "docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md",
                "templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md",
            ):
                if changed not in rule["when_changed"]:
                    rule["when_changed"].append(changed)
            if "tests/test_project_gdd_google_sheets_contract.py" not in rule["require_any_changed"]:
                rule["require_any_changed"].append(
                    "tests/test_project_gdd_google_sheets_contract.py"
                )
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_learning_and_changelog() -> None:
    learning_path = "skills/SKILL_LEARNING_LOG.md"
    learning = read(learning_path)
    heading = "# Base Skill Learning Log\n"
    section = """
## 2026-07-29 — 프로젝트 Google Sheets의 시각형 GDD 역할

- **Trigger:** 각 프로젝트 Google Sheets를 사용자의 전체 흐름 확인·정보 갱신 확인·직접 수정용 GDD로 사용하고, AI도 GitHub와 함께 방향성·메인 시스템을 참조하라는 요청.
- **Finding:** Sheet를 단순 운영 mirror로만 두면 사용자 편집의 의미가 약하고, 반대로 Sheet를 단일 정본으로 승격하면 GitHub 상세 정본·실제 구현과 충돌한다. 기존 Intake·운영체계·문서 Skill이 이미 Sheet 비교·동기화를 책임지므로 새 광역 Skill은 중복이다.
- **Decision:** **새 Skill을 추가하지 않음**. Sheet를 `USER_FACING_GDD_WORKSPACE`로 정의하고, 사용자 편집은 `PROPOSED_SHEET_CHANGE`로 보존한 뒤 GitHub 정본·실제 구현과 비교한다. 시각화 우선·지속 갱신·단위·초기 시험값·조정 범위·검증 상태를 공용 계약으로 추가한다.
- **Boundary:** GitHub 등록 정본과 실제 파일의 권한을 유지한다. HTML 대시보드는 사용자 명시 요청 또는 기존 유지보수에만 선택적으로 사용한다.
- **Learning state:** 정책·Template·회귀 계약은 `PATTERN` 후보이며, 여러 프로젝트에서 사용자 수정 누락 감소·AI 방향 복원·운영 비용을 확인하기 전까지 실제 효과는 `OBSERVATION`이다.
- **Next trigger:** 서로 다른 두 프로젝트 이상에서 Sheet 편집→승인→GitHub 정본→Sheet 재동기화 흐름과 시각 GDD 사용성을 검증할 때 재검토한다.
"""
    if "프로젝트 Google Sheets의 시각형 GDD 역할" not in learning:
        write(learning_path, learning.replace(heading, heading + section, 1))

    changelog_path = "docs/CHANGELOG.md"
    changelog = read(changelog_path)
    marker = "## Unreleased - Base audit and operating-contract consistency\n"
    bullet = """
- 프로젝트 Google Sheets를 `USER_FACING_GDD_WORKSPACE`로 정의해 사용자의 전체 GDD 흐름 확인·직접 수정과 AI의 GitHub·Sheet 공동 참조를 연결했다. Sheet-only 수정은 `PROPOSED_SHEET_CHANGE`로 보존하고 승인 후 GitHub 정본·Commit·Sheet 재조회로 동기화한다.
- 표준 GDD 6영역, 흐름도·관계도·와이어프레임·이미지 중심 시각화, 지속 갱신 메타데이터, 단위·초기 시험값·조정 범위·검증 상태 수치화 계약을 추가했다.
- 활성 Skill 표기를 핵심 통합 13개와 구조·운영·지원 14개, 전체 ACTIVE 27개로 명확히 하고 HTML 대시보드를 사용자 명시 요청 또는 기존 유지보수에만 사용하는 선택 기능으로 고정했다.
"""
    if "USER_FACING_GDD_WORKSPACE" not in changelog:
        write(changelog_path, changelog.replace(marker, marker + bullet, 1))


def main() -> None:
    update_policy_and_templates()
    update_sync_policy()
    update_planning_policy()
    update_entrypoints()
    update_skills_and_registry()
    update_reference_freshness()
    update_learning_and_changelog()


if __name__ == "__main__":
    main()
