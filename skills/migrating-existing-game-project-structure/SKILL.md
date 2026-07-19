---
name: migrating-existing-game-project-structure
description: Use when applying Base governance to an operating game project while preserving approved decisions, implementation state, assets, references, history, hold items, and unverified evidence before selecting schema v3 Markdown or JSON sources and generating current PDFs with optional derivatives.
---

# Migrating an Existing Game Project Structure

## Core principle

기존 프로젝트 마이그레이션은 신규 폴더 복사가 아니라 **보존 증거를 가진 단계적 책임 재배치**다.

공용 Method: `EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md`

보고 템플릿: `EXISTING_PROJECT_MIGRATION_AUDIT.md`

## Trigger

- 운영 중인 프로젝트를 Base 기준으로 검수·재배치
- Markdown·DOCX·PDF·이미지 구조의 중복·누락 정리
- 승인된 경우 기존 기획 본책을 역할별 Markdown·JSON 단일 책임 원본 + 최신 PDF·선택 DOCX로 전환
- 책임 원본 재정의 또는 폴더 이동
- `[백업]`, `[보류]`, 제거 후보 정리
- 기존 프로젝트에 분야별 스킬·GitHub Governance 설치

신규 프로젝트에는 `installing-game-project-operating-system`을 사용한다.

## 절대 보존 대상

조사와 사용자 승인 없이 다음을 삭제·축약·변경하지 않는다.

- 사용자 승인 기획과 결정
- 프로젝트 고유 세계관·용어·수치
- 현재 구현 상태와 실제 경로
- 승인 이미지·UI·다이어그램·프롬프트
- 테스트 결과·실패 사례
- Roadmap·Issue·Goal·Plan 진행 기록
- Active Context·Handoff의 미완료 작업
- `[보류]`, `[확인 필요]`, `[미검증]`
- 외부에서 참조되는 파일
- 출처·승인 근거가 되는 과거 문서

## Phase 0 — Authority and scope

```yaml
target_repository:
base_reference_commit:
requested_level: audit/governance/migration/enforcement
protected_paths:
protected_decisions:
protected_assets:
explicitly_approved_changes:
target_design_document_contract: preserve-current-or-use-explicitly-approved-target
```

## Phase 1 — Audit only

첫 단계에서 대규모 삭제·이동·통합을 수행하지 않는다.

조사 대상:

- 루트·AGENTS·README·START_HERE
- Documentation Map·Active Context·Handoff·Roadmap
- Markdown·DOCX·PDF 기획서와 부록
- 기존 JSON·데이터·스키마
- Skill Registry·스킬·Learning Log
- Visual Source·Asset Manifest·승인 이미지·실제 캡처
- Issue·Goal·Plan·PR
- 코드·설정·테스트의 문서·자산 참조
- 최근 커밋과 과거 이동

파일별 기록:

| 현재 경로 | 역할 | 참조 | 고유 정보 | 중복 | 상태 | 목표 처리 | 위험 |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  | 현행/보조/백업/보류/제거 후보 |  |  |

탐지:

- 한 질문의 중복 책임 원본
- 서로 다른 최신 수치·용어·상태
- 실제 구현과 문서 차이
- Markdown·DOCX·PDF에만 남은 고유 정보
- 끊어진 경로와 외부 참조
- 승인 이미지·실제 캡처 누락
- 분야별 프로젝트 스킬·게이트·검증 누락
- 보류 항목의 활성 범위 혼입
- 완전히 흡수되지 않은 제거 후보

## Phase 2 — Proposal only

사용자 검토용 산출물:

1. 현재 구조 분석
2. 현행 책임 문서·스킬·자산 지도
3. 중복·충돌·누락 목록
4. `DESIGN_DOCUMENT_REGISTRY.json` 목표안
5. 프로젝트 전체·분야별 Markdown 또는 JSON 책임 원본 목표안
6. DOCX·PDF·다이어그램·승인 이미지 발행 계획
7. 이동·통합·재배치 제안
8. 제거 후보와 보존 근거
9. 변경 전후 예상 구조
10. 위험·검증·롤백·사용자 승인 항목

승인 전에는 명백한 오탈자·끊어진 내부 링크 외의 대규모 변경을 하지 않는다.

## Phase 3 — Approved content migration

승인된 처리표의 항목만 수행한다.

```text
기존 원본별 고유 문장·표·결정·예외·이미지·보류 추출
→ 충돌 표시
→ 최신 사용자 결정과 실제 구현으로 현행 판정
→ 불확실성은 [확인 필요]
→ 선택한 Markdown 또는 JSON 책임 원본에 전체 승계
→ Design Document Registry 등록
→ 승인 이미지 경로·상태·채택 범위 연결
→ DOCX·PDF·다이어그램 생성
→ 전 페이지 렌더 검수
→ 참조 갱신
→ 변경 전후 보존 대조
→ 기존 원본 수명주기 판정
```

문장을 짧게 만드는 과정에서 의미, 제약, 예외, 승인 상태와 구현 상태를 제거하지 않는다.

## Phase 4 — Reference-safe movement

이동·이름 변경 전후 검색:

- Markdown 링크·README·Documentation Map·AGENTS
- Design Document Registry·Skill Registry
- 코드 주석·설정·스크립트·테스트
- Skill·Template·Manifest·Actions
- Issue·PR·Goal·Plan
- DOCX/PDF의 링크·캡션
- 외부 링크

수정할 수 없는 참조가 있으면 이동하지 않고 위험으로 보고한다.

## Phase 5 — Lifecycle classification

- `[현행]`: 활성 JSON·스킬·실제 파일
- `[백업]`: Git 이력만으로 부족한 외부 원본·감사·승인 근거
- `[보류]`: 재개 조건과 선행 작업을 가진 미래 항목
- `[제거 후보]`: 고유 정보·참조·복구·사용자 승인을 검증한 완전 중복 후보

단순 이전 버전은 별도 백업 복제본 대신 Git 이력으로 보존한다.

기존 Markdown·DOCX·PDF 본책은 다음을 모두 만족하기 전 삭제하지 않는다.

- 모든 고유 정보가 선택한 Markdown 또는 JSON 책임 원본에 승계됨
- 이미지·표·예외·보류가 보존됨
- 다른 파일·코드·Issue 참조가 새 경로로 갱신됨
- DOCX·PDF 출력과 Manifest가 검증됨
- Git 이력 또는 별도 백업으로 복구 가능
- 사용자 삭제 승인

## Phase 6 — Preservation validation

변경 전후 비교:

- 파일 수와 처리 유형
- 문서 제목·주요 섹션
- 승인 결정·고유 수치·용어
- 이미지·자산·프롬프트
- `[보류]`, `[확인 필요]`, `[미검증]`
- Roadmap 미완료 작업
- 분야별 스킬·Learning Log
- 링크·코드·Issue 참조
- JSON·DOCX·PDF·다이어그램·Manifest

| 기존 내용 | 기존 위치 | 새 책임 원본 위치 | 사람용 출력 | 보존 | 검증 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

변경 전 존재했지만 변경 후 찾을 수 없는 내용이 있으면 실패다.

## Phase 7 — Cold-start validation

새 AI가 저장소만으로 다음을 찾는다.

- 프로젝트 목적·핵심 경험
- 현재 구현·검증 상태
- 다음 작업과 선행 조건
- 금지·보호 범위
- Design Document Registry
- 프로젝트 전체·분야별 Markdown 또는 JSON 책임 원본
- 사람용 최신 DOCX/PDF·승인 이미지
- 분야별 스킬·검증 방법
- 보류·확인 필요·미검증
- Base 공용 기준과 프로젝트 전용 확장

찾지 못한 항목은 START_HERE·Documentation Map·Registry·JSON·스킬을 보완한다.

## Output contract

`EXISTING_PROJECT_MIGRATION_AUDIT.md` 형식을 사용한다.

완료 보고에서 분리:

- 실제 변경
- 제안만 한 변경
- 사용자 승인 대기
- 보존 대조 결과
- 생성한 JSON·DOCX·PDF·다이어그램·Manifest
- 실행한 검증과 사람 시각 검수
- 미검증·불일치
- 제거 후보
- 다음 마이그레이션 단계

## Failure conditions

- 실제 파일·참조를 읽지 않고 추정
- 사용자 승인 전 대량 삭제·이동·통합
- Base 폴더명을 강제 적용
- 고유 정보·보류·실패 기록 축약
- 승인 이미지 임의 교체
- 책임 원본 승계·발행 검증 전 기존 본책 제거
- DOCX·PDF를 독립 원본으로 유지
- 파일 수 감소를 성공으로 판단
- 문서 정리만으로 구현·런타임 검증 완료 선언
