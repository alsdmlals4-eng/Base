# 프로젝트 GDD Google Sheets 공용 계약 설계

## 승인 근거

사용자는 2026-07-29 다음 변경을 명시적으로 승인했다.

- Base 구조상 주의점을 권장안대로 수정한다.
- 각 프로젝트 Google Sheets를 GDD 파일로 사용한다.
- 사용자는 Sheet에서 전체 흐름, 정보 갱신 상태를 확인하고 직접 수정한다.
- AI는 GitHub와 Google Sheets를 함께 확인해 방향성·메인 시스템·현재 결정을 참조한다.
- GDD는 시각화 우선, 지속 갱신, 명확한 수치화를 기본 원칙으로 한다.

## 목표

각 프로젝트 Google Sheets를 장문의 기획서 복제본이 아니라 **사용자가 한 화면에서 이해하고 수정할 수 있는 시각형 GDD 작업면**으로 정의한다. AI는 GitHub 정본·실제 파일과 함께 Sheet를 읽어 현재 방향과 변경 제안을 복원하고, 승인된 변경만 양쪽에 동기화한다.

## 책임 경계

### GitHub

- `CURRENT_CONFIRMED_DECISIONS.md`: 현재 승인 결정 복원 정본
- 등록된 Markdown·JSON: 분야별 상세 책임 원본
- 코드·데이터·Scene·Resource·자산·테스트: 실제 구현 상태
- Issue·PR·Commit: 질문·승인·변경 이력

### 프로젝트 Google Sheets

- 상태명: `USER_FACING_GDD_WORKSPACE`
- 사용자가 전체 기획 흐름과 최신 상태를 확인하는 기본 작업면
- 방향성·핵심 루프·주요 시스템·세계관·인물·UX·아트·로드맵을 시각적으로 탐색하는 GDD
- 사용자가 직접 수정하거나 새 제안을 남기는 입력면
- GitHub 상세 정본과 실제 구현을 대체하지 않음

### Base

- 프로젝트 Sheet의 구조·동기화·검증 계약만 제공
- Base 자체 Sheet는 `BASE_EXCLUDED`
- 프로젝트 고유 세계관·수치·경로·자산·구현 상태를 저장하지 않음

## Sheet 편집 권한 모델

사용자 Sheet 편집은 무시하거나 자동 덮어쓰지 않는다. 다만 GitHub 정본을 즉시 암묵 변경하지도 않는다.

```text
사용자 Sheet 수정
→ PROPOSED_SHEET_CHANGE
→ AI가 GitHub main·Decision·분야 정본·실제 구현과 비교
→ 기술 기본값이면 RECOMMENDED_DEFAULT 제안
→ 중요 기획이면 USER_DECISION_REQUIRED 또는 기존 승인 확인
→ 승인된 변경을 GitHub 정본에 반영
→ Commit SHA 기록
→ Sheet 재동기화
→ SYNCED
```

충돌 상태는 다음으로 구분한다.

- `SYNCED`: GitHub 정본과 Sheet가 같은 승인 내용을 가짐
- `PROPOSED_SHEET_CHANGE`: Sheet에만 있는 사용자 제안
- `GITHUB_UPDATE_PENDING_SHEET`: GitHub가 최신이고 Sheet 갱신 필요
- `SHEET_UPDATE_PENDING_GITHUB`: 승인된 Sheet 변경의 GitHub 반영 필요
- `SHEET_GITHUB_CONFLICT`: 양쪽의 현재 내용이 충돌
- `NOT_CONFIGURED`: 정확한 Sheet URL·권한이 없음
- `BASE_EXCLUDED`: Base 저장소 자체
- `BLOCKED_UNVERIFIED`: 읽기·쓰기·재조회 증거가 없음

## AI 읽기 순서

```text
최신 사용자 지시
→ 프로젝트 AGENTS
→ CURRENT_CONFIRMED_DECISIONS
→ 등록된 분야 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 프로젝트 GDD Google Sheets
→ 동일 Goal의 Issue·PR·Commit
→ 차이·제안·동기화 상태 판정
```

AI는 Sheet만 읽고 프로젝트 방향이나 구현 상태를 확정하지 않는다. 반대로 GitHub만 읽고 사용자의 최신 Sheet 제안을 무시하지 않는다.

## GDD 구성

기존 Base의 의미별 tab 구조를 유지하면서 표준 GDD 여섯 영역을 연결한다.

1. 문서 개요: 프로젝트 허브, 제품 방향, 한 문장 핵심 카피, 타깃·플랫폼·장르·엔진
2. 핵심 게임플레이: 핵심 루프, 조작, 승패·점수·페널티 규칙
3. 게임 시스템: 캐릭터·전투·성장·경제·보상·메인 시스템
4. 스토리 및 세계관: 시놉시스, 세계관, 주요·조연 인물, 세력, 스테이지·콘텐츠
5. 아트 및 사운드: Visual Pillar, UI·UX 와이어프레임, BGM·SFX 방향, 이미지 계획·검수
6. 기술 및 로드맵: 목표 플랫폼·사양·저장·네트워크·성능·마일스톤·Vertical Slice·출시

## 시각화 우선 계약

각 주요 tab은 긴 설명보다 다음 순서로 구성한다.

1. 한 화면 요약
2. 흐름도·관계도·다이어그램 링크 또는 삽입 이미지
3. 와이어프레임·실제 캡처·레퍼런스 이미지
4. 핵심 수치·상태 표
5. 상세 GitHub 정본 경로

이미지가 없으면 빈 장식 이미지를 만들지 않고 `VISUAL_NOT_PREPARED`로 둔다. 시각 자료는 Asset ID·원출처·승인 상태·GitHub 경로와 연결한다.

## 지속 갱신 계약

모든 주요 행은 최소한 다음 메타데이터를 가진다.

- Decision ID
- GitHub 정본 경로
- main Commit SHA
- 마지막 수정 시각
- 수정 주체
- 승인 상태
- 구현 상태
- 검증 상태
- Sheet·GitHub 동기화 상태
- 다음 확인 조건

장시간 작업의 승인 결정을 checkpoint까지 미루지 않는다. 승인 직후 GitHub 정본과 Sheet에 반영하고 양쪽을 재조회한다.

## 수치화 계약

모호한 표현만 기록하지 않는다. 수치가 적용되는 항목은 다음 필드를 사용한다.

- 지표·파라미터 이름
- 단위
- 초기 시험값
- 조정 범위
- 공식·계산 규칙
- 적용 대상·조건
- 플레이어 영향
- 검증 방법
- 검증 상태
- 재조정 조건

예: `점프를 높게`가 아니라 `점프 높이 3.5 m / 체공 0.8 s / 초기 시험값 / 플레이테스트 조정 필요`로 기록한다.

## HTML 대시보드 경계

`building-project-visual-dashboards`는 공용 선택 기능으로 보존한다. 프로젝트 GDD Sheet와 GitHub 문서로 충분한 일반 작업에서는 사용하지 않는다. 사용자가 HTML 대시보드를 명시적으로 요청하거나 기존 대시보드 유지보수가 필요할 때만 호출한다.

## 활성 Skill 수 표기

사람용 진입 문서에서는 다음 표현을 사용한다.

- 핵심 통합 실행 Skill: 13개
- 구조·운영·지원 Skill: 14개
- 전체 ACTIVE Skill: 27개

기계적 권한은 `skills/SKILL_REGISTRY.json`이 가진다.

## 검증

- 전용 Python 계약 테스트가 새 정책·템플릿·진입점·Skill 연결을 검사한다.
- BCA Sheet Workflow가 변경 파일에서 실제 실행되도록 path filter를 확장한다.
- Reference Freshness가 새 정책 소비처 누락을 검사한다.
- 로컬 실행이 불가능하면 GitHub Actions 결과를 기다리고 `UNVERIFIED`를 유지한다.

## 제외 범위

- 개별 프로젝트 Sheet 실제 생성·수정
- 제품 코드·Godot Scene·Resource·게임 데이터 변경
- 프로젝트별 수치·세계관·캐릭터 내용 작성
- HTML 대시보드 생성·복구
- GitHub 정본을 Sheet로 대체
