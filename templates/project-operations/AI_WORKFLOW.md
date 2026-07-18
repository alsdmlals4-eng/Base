# 프로젝트 AI·GitHub 작업 흐름

## 1. 목적

사용자는 만들고 싶은 결과와 중요한 방향을 설명하고, 저장소 운영체계가 분야 판정·문서 갱신·검증 경로를 기억하게 한다.

```text
사용자 방향
→ GPT 기획·영향도 분석
→ 사용자 결정
→ 분야별 책임 원본 갱신
→ Codex Plan Mode 저장소 조사
→ 사용자 구현 승인
→ Codex 구현·테스트·문서 갱신
→ GitHub PR 자동 검사
→ QA
→ 통합검수
→ 병합·Active Context 갱신
```

## 2. 공통 시작 순서

```text
최신 사용자 지시
→ 프로젝트 AGENTS.md
→ 프로젝트 START_HERE.md
→ Active Context
→ Documentation Map
→ 관련 분야 본책
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
→ 필요한 Base method·skill·template
```

저장소의 모든 파일을 무작정 읽지 않는다. Documentation Map과 영향 관계로 현재 작업에 필요한 활성 원본을 빠짐없이 선택한다.

## 3. GPT 역할

GPT는 다음을 책임진다.

- 사용자 의도와 플레이어 가치 구조화
- 전문 용어를 사용하되 최초 등장 시 짧은 주석 제공
- 주 책임 분야·영향 분야·변경 유형 판정
- 대안·위험·미확정 분리
- 기획서·Decision Record·Roadmap 초안
- Codex Work Order·Acceptance Criteria 작성
- 벤치마킹·유저리서치·분석
- 문서·구현·자산·검증 통합검수

**Acceptance Criteria(인수 기준)**: 사용자가 결과를 승인할 수 있도록 관찰 가능한 조건으로 작성한 기준이다.

GPT가 하지 않는 것:

- 실제 파일을 확인하지 않고 구현 완료 추정
- 사용자 결정 없이 제품 방향 확장
- 기존 승인 이미지 확인 없이 새 시안 생성
- 대화를 최종 책임 원본으로 사용

## 4. Codex Plan Mode 역할

코드·Scene·Resource·데이터·엔진 설정을 바꾸는 L2 이상 작업은 Plan Mode를 우선한다.

Plan에는 다음이 있어야 한다.

```yaml
problem:
player_or_user_value:
primary_discipline:
affected_disciplines:
scope:
out_of_scope:
current_repository_findings:
files_to_change:
data_and_state_ownership:
asset_and_ui_impact:
migration_and_compatibility:
risks:
acceptance_criteria:
validation:
documentation_updates:
```

Plan Mode 중에는 사용자의 명확한 구현 승인 전까지 실제 제품 파일을 수정하지 않는다.

## 5. Codex 구현 역할

- 승인된 Plan과 Issue 범위만 변경한다.
- 가장 작은 안전한 변경 단위를 사용한다.
- 기존 저장·인터페이스·사용자 흐름을 승인 없이 변경하지 않는다.
- 관련 자동·수동 검증을 실행한다.
- 실제 결과에 맞게 본책·Active Context·검증 기록을 갱신한다.
- 미검증과 남은 위험을 명시한다.
- 범위 밖 개선은 별도 제안으로 분리한다.

## 6. GitHub 역할

GitHub는 다음의 책임 원본이다.

- 활성 문서·코드·데이터·자산 이력
- Issue와 PR 작업 계약
- 리뷰와 결정 흔적
- GitHub Actions 검증
- 릴리스와 빌드 증거

권장 운영:

- 기본 브랜치 직접 수정 대신 작업 브랜치·PR
- Issue Form으로 Ready 조건 확인
- PR Template으로 문서·자산·검증 확인
- CODEOWNERS로 분야별 리뷰 요청
- Required Status Check로 자동 검사 강제
- 해결되지 않은 리뷰 대화가 있으면 병합 차단

브랜치 보호가 실제 설정됐는지 확인하지 않았다면 `권장` 또는 `미검증`으로 기록한다.

## 7. 작업 단계

### 7.1 Intake

```yaml
request:
primary_discipline:
affected_disciplines:
change_type:
work_level: L0/L1/L2/L3/L4
```

- L0: 오탈자·명확한 형식
- L1: 범위가 명확한 작은 수정
- L2: 시스템 선택과 여러 파일 영향
- L3: 핵심 구조·여러 분야·장기 방향
- L4: 여러 프로젝트에서 재사용할 공용 방법

### 7.2 Definition of Ready

- 목적과 플레이어 가치
- 포함·제외 범위
- 책임 원본과 영향 분야
- 보호 경로와 기존 동작
- 완료 기준과 검증 방법
- 필요한 사용자 결정

준비되지 않은 작업은 구현으로 넘기지 않고 기획·조사·질문으로 분리한다.

### 7.3 Execution

```text
현재 상태 확인
→ 작은 변경
→ 자동 검증
→ 실제 화면·플레이 검증
→ 문서·Manifest 갱신
→ diff 검수
```

### 7.4 Definition of Done

- 승인 범위가 실제 파일에 반영됨
- 테스트·검증 결과 존재
- 본책·Active Context 최신
- 이미지·사운드·데이터 Manifest 최신
- 미검증·위험 분리
- 다음 작업·선행 조건 기록
- PR 자동 검사 통과

## 8. 이미지 작업 흐름

```text
기존 Visual Source·Manifest 확인
→ 기존 승인 자료 검색
→ 사용자 요청이 생성/편집/교체인지 판정
→ 참고·비참고 요소 정의
→ 새 작업 수행
→ 캐노니컬 경로·상태 갱신
→ 실제 게임 캡처 비교
→ 시각 QA·통합검수
```

기존 이미지가 있는 경우 별도 지시 없이 같은 항목의 새 시안을 만들지 않는다.

## 9. 채팅 결정 처리

```text
대화에서 결정 후보
→ 확정·권장·미확정·보류 분류
→ 사용자 승인
→ Decision Log
→ 관련 본책
→ Active Context·Roadmap
→ 필요 시 Issue·Plan
```

단순 대화라도 방향·수치·용어·범위·완료 기준이 확정되면 저장소 갱신 대상이다.

## 10. 완료 보고

```md
## 결과
- 주 책임 분야:
- 영향 분야:
- 변경 파일:
- 변경 이유:
- 유지한 기존 동작:
- 실행한 검증:
- 검증 결과:
- 미검증 항목:
- 갱신한 본책·상태·Manifest:
- 남은 위험:
- 다음 작업:
- Base 환류 후보:
```

실행하지 않은 테스트나 확인하지 않은 구현을 완료로 보고하지 않는다.
