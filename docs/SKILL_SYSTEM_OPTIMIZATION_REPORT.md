# Base Skill System Optimization Report

## Scope

사용자가 제공한 1,201줄 학습 텍스트와 기존 활성 Skill 16개의 책임을 대조했다. 새 책임은 9개로 제한하고, 이미 존재하는 요청 명세화·벤치마킹·MVP·Issue/Goal·문서 기억·검증 책임은 중복 신설하지 않았다.

## Applied pruning

- 프로젝트 코어·적대적 검토·Skill 진화·게임 컨셉 Skill의 반복 설명과 상세 판정표를 본문에서 제거했다.
- 고유 규칙은 각 패키지의 `references/`로 이동하고 본문에서 읽는 조건을 연결했다.
- 임시 동기화 Workflow와 적용 스크립트는 결과 커밋에서 자체 제거한다.

## Applied simplification

수정한 SKILL.md는 목적·경계·mode·필수 입력·핵심 흐름·출력·품질 게이트 중심의 라우터로 재작성했다. 상세 예시·판정표·체크리스트는 조건부 reference로 분리했다.

## Applied refactoring

- 코어 판정, 코어 확정, 적대적 검토의 권한 경계를 보존했다.
- 분석 Skill의 컨셉·벤치마크·플레이테스트·DDD·PoC 기능을 유지하며 세부 계약을 모듈화했다.
- Skill 진화는 생성·통합 오케스트레이션만 남기고 가지치기·간소화·리팩토링을 독립 Skill로 위임했다.

## No-loss controls

- `skills/SKILL_COVERAGE.json`으로 원문 책임 18개를 활성 Skill에 매핑한다.
- 전용 checker가 coverage 대상, Registry, 파일, front matter, 최소 계약, compact target을 검증한다.
- 기존 구조·Registry·reference·정본 최신성 회귀 테스트와 PR Actions를 함께 실행한다.

## Expected result

활성 Skill은 16개에서 25개로 증가하지만, 각 새 Skill은 독립 계약이 있는 책임만 담당한다. 기본 컨텍스트는 전체 로드하지 않으며 `load_by_default=false`와 trigger 기반 선택을 유지한다.
