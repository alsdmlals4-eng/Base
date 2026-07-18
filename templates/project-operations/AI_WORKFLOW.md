# 프로젝트 AI·GitHub 작업 흐름

## 1. 목적

사용자는 만들고 싶은 결과와 중요한 방향을 설명한다. 저장소 운영체계가 분야 판정, 개발 게이트, 책임 문서·프로젝트 스킬·Manifest·PDF 갱신과 검증 경로를 기억한다.

```text
사용자 방향
→ GPT 문제·경험·영향도 구조화
→ Definition of Ready
→ 사용자 기획·구현 승인
→ Codex Plan Mode 저장소 조사
→ Implementation Gate
→ 자동·수동 Verification
→ Documentation Gate
→ QA·통합검수
→ PR Required Checks·리뷰
→ Completion·병합
→ Active Context·Handoff·스킬 학습 갱신
```

## 2. 공통 시작 순서

```text
최신 사용자 지시
→ 프로젝트 AGENTS.md
→ START_HERE.md
→ Active Context·Handoff
→ Documentation Map
→ DEVELOPMENT_GATES.md
→ 관련 분야 본책
→ PROJECT_SKILL_MAP의 foundation + 분야 스킬
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
→ 필요한 Base Method·Skill·Template
```

저장소 모든 파일을 무작정 읽지 않는다. `[백업]`, `[보류]`, `[제거 후보]`, archive·hold는 감사·재개 요청이 없는 한 기본 읽기에서 제외한다.

## 3. 요청 분류

```yaml
request:
work_level: L0/L1/L2/L3/L4
project_mode: new/existing/operational
primary_discipline:
affected_disciplines:
change_type:
foundation_skills:
discipline_skills:
```

- L0: 오탈자·명확한 형식
- L1: 범위가 명확한 작은 수정
- L2: 시스템 선택·여러 파일/분야 영향
- L3: 핵심 구조·장기 방향·대형 마이그레이션
- L4: 여러 프로젝트에서 재사용 가능한 방법

기존 운영 프로젝트의 구조 개편은 `migrating-existing-game-project-structure` 스킬로 시작하고 첫 단계에서는 감사·제안만 수행한다.

## 4. GPT 역할

- 사용자 의도와 플레이어 가치 구조화
- 전문 용어 최초 등장 시 짧은 주석 제공
- 주 책임 분야·영향 분야·변경 유형 판정
- 확정·권장·확인 필요·보류·제외·미검증 분리
- 기획서·Decision Record·Roadmap·게이트 초안
- Codex Work Order와 Acceptance Criteria 작성
- 벤치마킹·유저리서치·분석
- 문서·구현·이미지·사운드·PDF·검증 통합검수
- 프로젝트 스킬 학습·Base 환류 후보 정리

GPT가 하지 않는 것:

- 실제 파일을 확인하지 않고 구현 완료 추정
- 사용자 결정 없이 제품 방향 확장
- 기존 승인 이미지 확인 없이 새 시안 생성
- 대화를 최종 책임 원본으로 사용
- 문서 또는 PDF 존재를 검증 증거로 사용

## 5. Codex Plan Mode

L2 이상 코드·Scene·Resource·데이터·자산 파이프라인 작업은 Plan Mode를 우선한다.

```yaml
problem:
user_or_player_value:
primary_discipline:
affected_disciplines:
foundation_skills:
discipline_skills:
scope:
out_of_scope:
current_repository_findings:
protected_decisions_and_paths:
files_to_change:
data_and_state_ownership:
asset_ui_audio_impact:
migration_and_compatibility:
risks_and_fallbacks:
acceptance_criteria:
validation:
documentation_skill_manifest_pdf_updates:
rollback:
```

사용자의 명확한 구현 승인 전까지 대규모 제품 변경을 수행하지 않는다.

## 6. 작업 실행 게이트

### 6.1 Intake·Context Gate

- 최신 지시·책임 원본·실제 파일·관련 스킬 확인
- 문제·사용자 가치·보호 범위·미확정 기록

### 6.2 Definition of Ready

- 목적·경험·범위·제외 범위
- 책임 분야·선행 조건·의존성
- 저장·호환성·승인 자산 위험
- 관찰 가능한 완료 기준
- 자동·수동·사용자 검수
- 관련 foundation·분야 스킬

준비되지 않은 작업은 구현으로 넘기지 않고 조사·기획·결정으로 분리한다.

### 6.3 Planning·Approval Gate

- 실제 저장소 조사
- 변경·보호 파일
- 상태·데이터 소유
- 예외·폴백·롤백
- Acceptance Criteria
- 검증·문서·스킬·Manifest·PDF 갱신
- 사용자 구현 승인

### 6.4 Implementation Gate

- 승인 Plan 범위만 변경
- 가장 작은 검증 가능한 변경
- 기능 추가와 대규모 리팩터링 분리
- 저장·인터페이스·사용자 흐름 보호
- 보류 항목 승인 없는 구현 금지
- 승인 이미지 임의 대체 금지

### 6.5 Verification Gate

```text
포맷·문법·정적 검사
→ 자동 테스트
→ 핵심 정상 경로
→ 실패·취소·중복·누락
→ 저장·호환성
→ 실제 화면·플레이·오디오·성능
→ diff·승인 범위
→ 사용자 수동 검수
```

실행하지 못한 항목은 `[미검증]`으로 기록한다.

### 6.6 Documentation Gate

같은 작업에서 확인한다.

- 관련 분야 본책
- Roadmap·Development Gates
- Documentation Map·Active Context·Handoff
- Decision Log·Changelog
- Project Skill Map·분야 스킬·Learning Log
- Visual Source·Asset Manifest
- 테스트·QA·통합검수
- PDF·Publication Manifest
- README·Issue·Goal·Plan
- Base version·후속 동기화

### 6.7 Integration·Completion Gate

- Acceptance Criteria 증거 판정
- 구현·검증·사용자 확인 상태 분리
- 본책·스킬·Manifest·PDF 최신
- 미검증·불일치·위험 분리
- 이동·제거 잔여 참조 없음
- PR Required Checks·리뷰 통과
- 다음 작업·선행 조건·Handoff 존재
- 프로젝트 전용 교훈·Base 환류 후보 분리

## 7. 제품 마일스톤

```text
Concept
→ Prototype
→ Graybox
→ First Playable
→ Vertical Slice
→ Production
→ Alpha
→ Feature Complete
→ Content Complete
→ Beta
→ Release Candidate
```

작업 하나의 완료를 프로젝트 전체 게이트 통과로 해석하지 않는다. 세부 기준은 `DEVELOPMENT_GATES.md`를 따른다.

## 8. 기존 프로젝트 구조 마이그레이션

```text
Audit only
→ 책임·참조·고유 정보 지도
→ 중복·충돌·누락
→ 변경 전후 보존 대조가 포함된 제안
→ 사용자 승인
→ 승인 범위만 이동·통합
→ 링크·스킬·PDF·콜드 스타트 검증
→ 제거 후보 별도 승인
```

승인 전 금지:

- 대량 삭제·이동·통합
- 책임 문서 대규모 축약
- 승인 자산 제거·교체
- 보류 폐기
- Base 구조에 맞춘 강제 개명

## 9. 분야별 프로젝트 스킬

- 공용 절차는 foundation에서 한 번만 책임진다.
- 분야 스킬은 해당 분야의 실제 본책·경로·산출물·Quality Bar·검증·실패 조건을 책임진다.
- 새 작업은 `PROJECT_SKILL_MAP.md`에서 foundation + 분야 스킬만 선택한다.
- 작업 종료 후 Learning Log에 성공·실패·예외·사용자 피드백과 스킬 변경을 기록한다.
- 지식 상태는 관찰·가설·패턴·검증·승격 후보로 구분한다.

## 10. 이미지 작업 흐름

```text
기존 Visual Source·Asset Manifest 확인
→ 승인 자료 검색
→ 생성/편집/교체 요청 판정
→ 채택·비채택 요소 정의
→ 작업 수행
→ 캐노니컬 경로·상태 갱신
→ 실제 게임 캡처 비교
→ 시각 QA·통합검수
→ 관련 분야 PDF 갱신
```

기존 승인 이미지가 있는 경우 별도 지시 없이 같은 항목의 새 시안을 만들지 않는다.

## 11. PDF 발행 흐름

```text
분야 본책·활성 부록·승인 이미지 확인
→ 전체 과정 구성
→ 재현 가능한 명령으로 생성
→ Publication Manifest 입력 해시 갱신
→ 내용·링크·시각·접근성 검수
→ governance 최신성 검사
```

PDF는 읽기 전용 파생본이다. 생성 파이프라인이나 렌더링을 확인하지 못했으면 `NOT_BUILT`, `STALE` 또는 `[미검증]`으로 기록한다.

## 12. 채팅 결정 처리

```text
대화의 결정 후보
→ 확정·권장·확인 필요·보류·제외 분류
→ 사용자 승인
→ Decision Log
→ 관련 본책·게이트·스킬
→ Active Context·Roadmap
→ 필요 시 Issue·Plan·PDF
```

단순 대화라도 방향·수치·용어·범위·완료 기준이 확정되면 저장소 갱신 대상이다.

## 13. GitHub 역할

- 활성 문서·코드·데이터·자산·PDF 이력
- Issue와 PR 작업 계약
- CODEOWNERS 리뷰
- Governance·엔진·테스트 Actions
- Required Status Checks
- 릴리스·빌드·검증 증거

Workflow 파일 존재, 실제 실행 확인, Required Check 강제를 별도 상태로 기록한다.

## 14. 완료 보고

```md
## 결과
- 주 책임 분야:
- 영향 분야:
- 적용한 foundation·분야 스킬:
- 통과한 작업 게이트:
- 변경 파일:
- 변경 이유:
- 유지한 기존 결정·동작·자산:
- 실행한 검증:
- 검증 결과:
- 미검증·불일치:
- 갱신한 본책·게이트·스킬·Manifest·PDF:
- 백업·보류·제거 후보:
- 콜드 스타트 결과:
- 남은 위험:
- 다음 작업:
- Base 환류 후보·지식 상태:
```

실행하지 않은 테스트, 렌더링, PDF 최신성 검사, 브랜치 보호나 사용자 확인을 완료로 보고하지 않는다.
