# Cross-Discipline Adversarial Review Lenses

## 목적과 권한

L2 이상 다분야 결정·저장소 감사·외부 조달에서 혼자 놓치기 쉬운 각도를 선택적으로 공격한다. Lens는 Finding을 만들지만 **결정을 소유하지 않는다**. 최종 판정과 수정은 주 책임 Skill, 중요 방향 선택은 사용자가 소유한다.

## 선택 규칙

- 현재 Requirement·변경·위험과 직접 연결된 Lens만 선택한다.
- 관련 없으면 `NOT_APPLICABLE`과 이유를 기록한다.
- 모든 Lens를 의식적으로 채우기 위해 가짜 Finding을 만들지 않는다.
- L0·L1 기계 수정에는 기본 사용하지 않는다.

## Lens

### 제품·플레이어 가치
- 해결할 문제와 사용자 가치가 구현 편의로 대체됐는가.
- 핵심 경험·완료 기준·비목표가 유지되는가.
- 기능 추가가 실제 행동·보상·학습에 연결되는가.

### UX·접근성
- 중심 질문·첫 시선·핵심 행동·복구 경로가 명확한가.
- 색·소리·모션 하나에만 중요한 의미가 의존하는가.
- 포인터·키보드·게임패드·터치·긴 한국어·Reduced Motion 경계가 검증됐는가.

### 아키텍처·상태 소유권
- 같은 질문의 권위 상태가 둘 이상인가.
- UI·애니메이션·외부 도구가 도메인 결과를 소유하는가.
- 경계·Schema·호환성·롤백이 명시됐는가.

### 구현·성능·플랫폼
- 실제 대상 플랫폼·엔진·의존성에 맞는가.
- 추측 최적화, 무제한 작업, 숨은 네트워크·파일 변경이 있는가.
- baseline·환경·측정 조건 없이 성능을 주장하는가.

### QA·회귀·출시
- 정상·실패·경계·복구·회귀 fixture가 있는가.
- 테스트 정의를 실행 성공으로 오인하는가.
- 출시·플랫폼·사람 검증의 증거 상한이 보존되는가.

### 문서·추적성·인수인계
- Decision→Requirement→Task→구현→검증 연결이 끊겼는가.
- 정본·파생본·Prompt·Template·Test 소비자 일부가 untouched인가.
- 다음 작업자가 기준 commit·미검증·rollback을 복원할 수 있는가.

## Finding contract

```yaml
finding_id:
lens:
evidence:
affected_requirement:
severity: MUST_FIX | SHOULD_FIX | USER_DECISION_REQUIRED | DEFER | BLOCKED_UNVERIFIED
owner_skill:
status: CANDIDATE | VALIDATED | REJECTED_CRITIQUE | APPROVED | RESOLVED | NOT_APPLICABLE
reason:
verification:
```

## 충돌 처리

Lens 간 결론이 다르면 사실성·발생 가능성·영향·비용·프로젝트 코어·호환성·되돌리기 난이도로 `validate-critique`한다. 기술적으로 단일 답이 없는 중요 방향은 `USER_DECISION_REQUIRED`로 분리한다. Named Agent별 별도 정본·PRD·Architecture 복제본을 만들지 않는다.
