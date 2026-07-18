# 프로젝트 AI·GitHub 작업 흐름

## 1. 목적

사용자는 만들고 싶은 결과와 중요한 방향을 설명한다. 저장소 운영체계가 분야 판정, JSON 기획서, 선택적 스킬, 개발 게이트, 사람용 DOCX/PDF, 검증과 인수인계를 기억한다.

```text
사용자 방향
→ Registry 기반 분야·최소 스킬 라우팅
→ GPT 문제·경험·영향도 구조화
→ Definition of Ready
→ 사용자 승인
→ Codex 실제 저장소 조사·Plan
→ Implementation
→ 자동·수동 Verification
→ 관련 기획서 JSON·실제 상태 갱신
→ DOCX/PDF·다이어그램·Manifest 재생성
→ QA·통합검수
→ PR Required Checks·리뷰
→ 병합
→ Active Context·Handoff·Learning Log
```

## 2. 공통 시작 순서

```text
최신 사용자 지시
→ 프로젝트 AGENTS.md
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ Active Context·Handoff·Documentation Map
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 분야 기획서 JSON
→ SKILL_REGISTRY.json
→ 필요한 Foundation·분야 스킬
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
→ 사람 검토 시 DOCX/PDF·다이어그램·승인 이미지
```

백업·보류·제거 후보와 전체 skills 폴더는 기본 읽기에서 제외한다.

## 3. 요청·스킬 라우팅

```yaml
request:
work_level: L0/L1/L2/L3/L4
project_mode: new/existing/operational
primary_discipline:
affected_disciplines:
change_type:
required_design_document_ids:
foundation_skills:
discipline_skills:
deferred_skills:
asset_impact:
publication_impact:
routing_reason:
```

- 전체 스킬 로드 금지
- 주 책임 분야 스킬 최대 하나
- Foundation 스킬은 필요한 최소 개수
- Trigger·비사용 조건 확인
- 발행·검증·Handoff 스킬은 해당 단계에서만 호출

기존 프로젝트 구조 개편은 안전 마이그레이션의 `Audit only`부터 시작한다.

## 4. GPT 역할

- 사용자 의도·플레이어 가치·전문 용어 구조화
- 주 책임·영향 분야·변경 유형 판정
- Design Document Registry에서 관련 JSON 선택
- Skill Registry에서 최소 스킬 선택
- 확정·권장·확인 필요·보류·미검증 분리
- JSON 기획 초안·Decision·Roadmap·Gate·Work Order 작성
- 구현·이미지·사운드·DOCX/PDF·검증 통합검수
- 스킬 실행 결과와 Base 환류 후보 정리

하지 않는 것:

- 실제 파일 없이 구현 완료 추정
- 사용자 결정 없이 제품 방향 확장
- 승인 이미지 확인 없이 새 시안 생성
- 대화를 최종 책임 원본으로 사용
- DOCX/PDF 존재를 구현·검증 증거로 사용
- 관련 없는 스킬 호출

## 5. Codex Plan Mode

```yaml
problem:
user_or_player_value:
primary_discipline:
affected_disciplines:
required_design_document_ids:
foundation_skills:
discipline_skills:
scope:
out_of_scope:
repository_findings:
protected_decisions_paths_assets:
files_to_change:
data_and_state_ownership:
asset_ui_audio_impact:
migration_and_compatibility:
risks_and_fallbacks:
acceptance_criteria:
validation:
json_skill_learning_publication_updates:
rollback:
```

L2 이상은 실제 저장소 조사에 기반한 Plan과 사용자 승인을 우선한다.

## 6. 작업 실행 게이트

### Intake·Context

- 최신 지시·두 Registry·관련 JSON·실제 파일 확인
- 호출할 최소 스킬과 후속 스킬 판정
- 사용자 가치·보호 범위·미확정 기록

### Definition of Ready

- 목적·범위·제외 범위
- 책임 분야·의존성
- 저장·호환성·승인 자산 위험
- 관찰 가능한 완료 기준
- 자동·수동·사용자 검수
- 관련 JSON·스킬·발행 영향

### Planning·Approval

- 변경·보호 파일
- 상태·데이터 소유
- 실패·폴백·롤백
- Acceptance Criteria
- JSON·Registry·Skill·Learning Log·DOCX/PDF 갱신 계획
- 사용자 승인

### Implementation

- 승인 Plan 범위만 변경
- 가장 작은 검증 가능한 변경
- 기능 추가와 대규모 리팩터링 분리
- 저장·인터페이스·사용자 흐름 보호
- 보류 항목·승인 이미지 임의 변경 금지

### Verification

```text
포맷·문법·정적 검사
→ 자동 테스트
→ 핵심 정상 경로
→ 실패·취소·중복·누락
→ 저장·호환성
→ 실제 화면·플레이·오디오·성능
→ diff·승인 범위
→ 사용자 검수
```

### Documentation·Publication

같은 작업에서 확인:

- 관련 기획서 JSON
- Design Document Registry
- Roadmap·Development Gates
- Documentation Map·Active Context·Handoff
- Decision Log·Changelog
- Skill Registry·Skill·Learning Log
- Visual Source·Asset Manifest
- DOCX·PDF·다이어그램·승인 이미지
- 각 Publication Manifest
- Issue·Goal·Plan·README

### Integration·Completion

- Acceptance Criteria 증거
- 승인·구현·검증·사용자 확인 상태 분리
- JSON·Registry·Skill·발행본 최신
- 미검증·불일치·위험 분리
- 이동·제거 잔여 참조 없음
- PR Required Checks·리뷰 통과
- 다음 작업·Handoff 존재

## 7. 기획서 발행 흐름

```text
기획서 JSON 갱신
→ Design Document Registry 확인
→ 자동 다이어그램 생성
→ 승인 이미지·실제 캡처 포함
→ DOCX 생성
→ PDF 변환
→ 전 페이지 렌더 검수
→ Manifest 해시 갱신
→ check_design_document_publications.py
```

DOCX·PDF는 파생본이다. 렌더링하지 않았으면 사람 시각 검수를 통과로 표시하지 않는다.

## 8. 스킬맵 발행 흐름

```text
Skill Registry 갱신
→ PROJECT_SKILL_MAP.docx/.pdf/.assets 생성
→ SKILL_MAP_PUBLICATION_MANIFEST.json
→ check_skill_routing_governance.py
```

`PROJECT_SKILL_MAP.md`는 사용하지 않는다.

## 9. 기존 프로젝트 마이그레이션

```text
Audit only
→ 기존 문서·이미지·참조·고유 정보 지도
→ JSON 책임 구조와 사람용 발행 구조 제안
→ 변경 전후 보존 대조
→ 사용자 승인
→ 승인 범위만 승계
→ DOCX/PDF·링크·콜드 스타트 검증
→ 기존 본책 제거 후보 별도 승인
```

## 10. GitHub 역할

- JSON·코드·데이터·자산·DOCX/PDF 이력
- Issue·PR 작업 계약
- CODEOWNERS 리뷰
- 세 Governance Checker와 엔진 테스트
- Required Status Checks
- 릴리스·빌드·검증 증거

파일 존재, Workflow 실행, Required Check 강제를 별도 상태로 기록한다.

## 11. 완료 보고

```md
## 결과
- 주 책임·영향 분야:
- 변경한 JSON·실제 파일·스킬:
- 생성한 DOCX·PDF·다이어그램·Manifest:
- 보호한 결정·동작·자산:
- 실행한 검증:
- 사람 시각 검수:
- 미검증·불일치·위험:
- Learning Log·Base 환류:
- 다음 작업·Handoff:
```
