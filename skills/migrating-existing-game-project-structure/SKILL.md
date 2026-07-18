---
name: migrating-existing-game-project-structure
description: Use when applying Base governance to an already-operating game project that must preserve approved decisions, implementation state, assets, references, history, hold items, and unverified evidence before any restructuring or cleanup.
---

# Migrating an Existing Game Project Structure

## Core principle

기존 프로젝트 마이그레이션은 신규 폴더 생성 작업이 아니라 **보존 증거를 가진 단계적 책임 재배치**다.

공용 방법: `docs/knowledge/methods/EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md`

보고 템플릿: `templates/project-operations/EXISTING_PROJECT_MIGRATION_AUDIT.md`

## Trigger

- 이미 운영 중인 프로젝트를 Base 기준으로 검수·재배치
- 문서·스킬·PDF·이미지 구조의 중복과 누락 정리
- 책임 원본 재정의 또는 폴더 이동
- `[백업]`, `[보류]`, 제거 후보 정리
- 기존 프로젝트에 분야별 본책·프로젝트 스킬·GitHub 검사를 설치

신규 프로젝트에는 `skills/installing-game-project-operating-system/SKILL.md`를 우선 사용한다.

## Non-negotiable preservation

사용자 승인 기획, 프로젝트 고유 정보, 현재 구현, 승인 자산, 테스트·실패 사례, Roadmap·Issue·Plan 기록, Active Context 미완료 작업, `[보류]`·`[확인 필요]`·`[미검증]`, 외부 참조와 출처 기록을 조사 없이 삭제·축약·변경하지 않는다.

## Phase 0 — Establish authority and scope

```yaml
target_repository:
base_reference_commit:
project_rules_version:
requested_level: audit/governance/migration/enforcement
protected_paths:
protected_decisions:
explicitly_approved_changes:
```

우선순위:

```text
최신 사용자 지시
→ 프로젝트 AGENTS.md
→ Active Context·Handoff
→ 승인 프로젝트 책임 원본과 실제 구현
→ 프로젝트에 동기화된 Base 기준
→ Base 원격 원본
→ 과거 대화·초안·추정
```

## Phase 1 — Audit only

첫 단계에서 대규모 삭제·이동·통합을 수행하지 않는다.

### Read

- 루트·AGENTS·README·START_HERE
- Base version·Documentation Map
- Active Context·Handoff·Roadmap
- 분야별 본책·부록·스킬
- PDF·Publication Manifest
- Visual Source·Asset Manifest·승인 이미지
- Issue·Goal·Plan·PR
- 코드·데이터·설정·테스트의 참조
- 최근 커밋과 과거 이동

### Inventory

| 현재 경로 | 역할 | 참조 위치 | 고유 내용 | 중복 | 상태 | 제안 | 위험 |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  | 현행/보조/백업/보류/제거 후보 |  |  |

### Detect

- 중복 책임 원본
- 서로 다른 최신 수치·용어·상태
- 실제 구현과 문서 차이
- 끊어진 경로와 외부 참조
- 승인 이미지·실제 캡처·PDF 누락
- 분야별 프로젝트 스킬 누락
- 개발 게이트·검증 절차 누락
- 보류 항목의 활성 범위 혼입
- 완전히 흡수되지 않은 제거 후보

## Phase 2 — Produce proposal only

다음 산출물을 사용자에게 검토 가능하게 작성한다.

1. 현재 구조 분석
2. 현행 책임 문서 지도
3. 중복·충돌·누락 목록
4. 이동·통합·재배치 제안
5. 제거 후보와 보존 근거
6. 변경 전후 예상 구조
7. 위험·검증·롤백
8. 사용자 승인 필요 항목

명백한 오탈자·끊어진 내부 링크 외에는 승인 전 대규모 변경을 하지 않는다.

## Phase 3 — Approved migration

승인된 처리표에 있는 항목만 수행한다.

### Integrate

```text
고유 정보 추출
→ 충돌 표시
→ 최신 결정·실제 구현으로 현행 판정
→ 불확실성은 [확인 필요]
→ 새 원본에 전체 승계
→ 표·이미지·예외·상태 대조
→ 참조 갱신
→ 검증
→ 원본 수명주기 판정
```

### Move or rename

이동 전후 다음 참조를 검색한다.

- Markdown·README·Documentation Map·AGENTS
- 코드 주석·설정·스크립트·테스트
- 스킬·템플릿·Manifest·Actions
- Issue·PR·Goal·Plan
- PDF 링크·캡션·Publication Manifest
- 외부 링크

수정할 수 없는 참조가 있으면 이동하지 않고 위험으로 보고한다.

### Classify

- `[현행]`: 현재 책임 원본과 실행 스킬
- `[백업]`: 외부 원본·감사·승인 기록처럼 Git 이력만으로 부족한 자료
- `[보류]`: 재개 조건과 선행 작업을 가진 미래 항목
- `[제거 후보]`: 보존·참조 검증과 사용자 승인을 기다리는 완전 중복 후보

단순 이전 버전은 별도 백업 파일 대신 Git 이력으로 보존한다.

## Phase 4 — Preservation validation

변경 전후 대조:

- 파일 수와 처리 유형
- 문서 제목·주요 섹션
- 승인 결정과 고유 수치
- 이미지·자산·프롬프트
- `[보류]`·`[확인 필요]`·`[미검증]`
- Roadmap 미완료 작업
- 분야별 스킬
- 링크·코드·Issue 참조
- PDF 원본·승인 이미지·Manifest

| 기존 내용 | 기존 위치 | 변경 후 위치 | 보존 | 검증 |
|---|---|---|---|---|
|  |  |  |  |  |

기존에 있었지만 변경 후 찾을 수 없는 내용이 있으면 실패다.

## Phase 5 — Cold-start validation

새 AI가 저장소만으로 다음을 찾는다.

- 프로젝트 목적·핵심 경험
- 현재 구현·검증 상태
- 다음 작업과 선행 조건
- 금지·보호 범위
- 분야별 책임 문서와 스킬
- 개발 게이트와 검증
- 보류·확인 필요·미검증
- 승인 이미지와 최신 PDF
- Base 공용 기준과 프로젝트 전용 확장

찾지 못한 항목은 Documentation Map·START_HERE·본책·스킬을 보완한다.

## Output contract

`templates/project-operations/EXISTING_PROJECT_MIGRATION_AUDIT.md` 형식을 사용한다.

완료 보고에는 다음을 분리한다.

- 실제 변경
- 제안만 한 변경
- 사용자 승인 대기
- 실행한 검증
- 미검증
- 제거 후보
- 다음 마이그레이션 단계

## Failure conditions

- 실제 파일·참조를 읽지 않고 추정
- 사용자 승인 전 대량 삭제·이동·통합
- Base 폴더명을 강제 적용
- 고유 정보·보류·실패 기록 축약
- 승인 이미지 임의 교체
- 삭제 조건을 만족하지 않은 파일 제거
- 파일 수 감소를 성공으로 판단
- 문서 정리만으로 구현·런타임 검증 완료 선언
