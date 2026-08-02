# 중립적 적대 검토와 기능 생명주기 설계

## 1. 결정

Base에 새 광역 Skill을 추가하지 않는다.

기능 구현 전반은 기존 `managing-project-intake-and-work-contract`가 상위 생명주기 라우터로 소유하고, 분야 Skill이 설계·구현 책임을 수행하며, `running-adversarial-review-and-refinement`와 `reviewing-and-validating-project-changes`가 비판 검증과 증거 판정을 맡는다.

사용자의 의견과 AI의 최초 제안은 모두 검토 가능한 가설로 취급한다. 근거 없이 동의하거나 반대하지 않고, 동일한 기준으로 대안·반증·위험을 비교한 뒤 가장 강한 결론을 권장한다.

## 2. 배경과 문제

Base에는 이미 다음 구조가 있다.

```text
요청
→ managing-project-intake-and-work-contract
→ PLAN / BUILD / REVIEW
→ 분야 Skill
→ running-adversarial-review-and-refinement
→ reviewing-and-validating-project-changes
→ 문서·상태·학습 동기화
```

새로운 “기능 구현 전반” 또는 “전체 제작 생명주기” Skill을 추가하면 다음 문제가 생긴다.

- 기존 intake Skill과 요청 수준·범위·라우팅 책임이 중복된다.
- 주 책임 분야 Skill 하나 원칙과 충돌할 수 있다.
- 단순 작업에도 불필요한 전체 검토 루프가 호출될 수 있다.
- 기술별 세부 지식이 Skill 본문에 고정되어 빠르게 오래될 수 있다.

따라서 기존 책임 경계를 유지하면서 중립성·동의 편향 방지와 기능 생명주기 연결을 강화한다.

## 3. 목표

1. 기능 구현 요청을 기획부터 구현·검증·문서화·학습까지 추적한다.
2. 사용자 주장과 AI 제안을 동일한 기준으로 검토한다.
3. 적대적 검토를 “반대를 위한 반대”로 오용하지 않는다.
4. 기술 판단과 사용자 결정의 경계를 유지한다.
5. 새 Skill과 Registry 중복 없이 행동을 테스트할 수 있게 한다.

## 4. 비목표

- 모든 L0 오탈자·기계 수정에 전체 적대 검토 Skill을 강제하지 않는다.
- 사용자 최신 지시의 권한을 약화하지 않는다.
- 검토를 이유로 승인된 범위를 임의 확장하지 않는다.
- PyTorch·머신러닝·API의 변동 가능한 기술 지식을 공용 Skill 본문에 복제하지 않는다.
- `skills/SKILL_REGISTRY.json`, v9.0~v9.4 released lock, evidence identity와 frozen snapshot을 변경하지 않는다.
- 프로젝트 코드·Google Sheets·Godot 자산을 변경하지 않는다.

## 5. 중립성 계약

### 5.1 항상 적용되는 경량 게이트

권장안·판정·설계 선택을 포함하는 응답은 다음을 확인한다.

1. 결론을 바꿀 평가 기준은 무엇인가.
2. 사용자안·AI 최초안 외에 유효한 대안이 있는가.
3. 현재 선호를 반증하는 사실·실패 조건은 무엇인가.
4. 각 선택의 이익·비용·위험·되돌리기 난이도는 무엇인가.
5. 증거가 부족한 항목은 무엇인가.
6. 동일 기준을 적용했을 때 어떤 결론이 가장 강한가.

검토 뒤 사용자안이 가장 강하면 동의한다. 다른 안이 더 강하면 근거와 함께 이견을 제시한다. 판정할 증거가 없으면 `BLOCKED_UNVERIFIED` 또는 확인 조건을 제시한다.

### 5.2 전체 적대 검토 루프

다음에는 `running-adversarial-review-and-refinement`를 실제 실행한다.

- L1 이상 기능·설계·아키텍처·정책·방향 결정
- “무조건 동의”, “반대하지 말라”처럼 비판을 차단하는 요청
- 완료·안전·정합성·프로젝트 코어에 영향을 주는 권장안
- 작업물·PR·저장소·병합 결정의 검수

```text
기준·범위 고정
→ attack
→ validate-critique
→ 대안 비교·권장
→ 승인된 BUILD
→ regression-recheck
→ decision-report
```

단순 사실 전달, 오탈자, 동일 입력의 검사 재실행은 전체 루프의 비사용 조건을 유지한다.

## 6. 기능 생명주기

```text
요청·현재 단계
→ 정본·실제 구현·최근 결정 복원
→ 문제·사용자 가치·완료 기준
→ 대안·반증·중립적 권장안
→ 사용자 결정 Gate
→ 실행 계약
→ 검증 가능한 기능 패키지·의존성·롤백
→ 분야 Skill BUILD
→ 계약·정적·런타임·접근성·성능·회귀 검증
→ 책임 원본·상태·발행·Handoff 동기화
→ 실행 증거·Learning Log
```

상위 흐름은 `managing-project-intake-and-work-contract`가 라우팅한다. 분야 Skill은 해당 기능의 설계·구현을 소유한다. 적대 검토와 변경 검증은 작성 책임을 빼앗지 않고 독립 Gate로 작동한다.

PyTorch·머신러닝·fine-tuning 같은 기술은 실제 기능 요청에서 trigger가 확인될 때 공식 문서·현재 프로젝트 환경·데이터 계약을 조건부로 읽는다. 반복 검증된 독립 입력·출력·검증 경계가 생기기 전에는 새 공용 Skill로 승격하지 않는다.

## 7. 변경 경계

### 항상 적용되는 정본

- `AGENTS.md`: 동의 편향 금지와 중립 결론 원칙
- `docs/OPERATING_MODEL.md`: 기능 생명주기와 책임 경계
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`: 경량 게이트와 전체 적대 검토 trigger

### 실행 Skill

- `skills/managing-project-intake-and-work-contract/SKILL.md`: 대안·반증·중립 권장안을 contract 이전 Gate로 추가
- `skills/running-adversarial-review-and-refinement/SKILL.md`: 사용자안·AI 최초안의 대칭 검토와 반대를 위한 반대 금지
- 필요 시 `skills/reviewing-and-validating-project-changes/SKILL.md`: 권장 근거와 실제 변경 증거 대조

### 행동 평가와 회귀

- `skills/SKILL_BEHAVIOR_EVALS.json`: 동의 유도·반대 유도·불완전 증거 경계 사례
- 기존 v9.5 행동 평가 검사와 문서·Skill package·reference freshness 회귀 사용
- 필요한 경우 집중 계약 테스트를 추가하되 문자열 존재만으로 모델 행동 통과를 주장하지 않는다.

Registry의 기존 `칭찬·균형 평가만 요청` 비사용 조건은 결정·권장안이 없는 설명형 요약에만 적용하고, 이 비사용 경계도 행동 Fixture로 고정한다. L1 이상 결정·중요 권장안의 PLAN 사전판정은 `attack → validate-critique → decision-report`를 실행한다. 승인 finding은 `refine-approved-findings`에서 분야 Skill BUILD가 한 번만 반영하고 `regression-recheck → decision-report`로 이동해 전체 루프를 닫는다.

### 기록

- `docs/CHANGELOG.md`: 완료된 변경만 기록
- `skills/SKILL_LEARNING_LOG.md`: 사용자 결정과 검증 결과를 상태에 맞게 기록

## 8. 상태와 권한

이 요청은 사용자의 직접 승인으로 Base 변경 계약이 될 수 있으므로 별도 BCP 제출은 요구하지 않는다. 구현은 별도 Branch와 Draft PR에서 수행한다.

- 설계 승인 전: 문서 설계만 허용
- 설계 승인 후: 테스트 우선 구현
- 필수 검사 실패·P0/P1·미해결 review thread·정본 충돌: 병합 차단
- 실제 모델 행동 평가를 실행하지 않은 경우: `MODEL_RUN_STATUS: NOT_RUN`
- 저장소 전체 tracked inventory가 없으면: 전수 감사 완료를 주장하지 않음

## 9. 검증

구현 단계에서 다음을 실행한다.

```text
집중 중립성·기능 생명주기 계약 테스트
→ Skill behavior contract 검사
→ Skill package integrity
→ documentation governance
→ canonical reference freshness
→ 전체 unittest
→ Base v9 integrity
→ diff check
→ 적대적 regression-recheck
```

GitHub Actions와 외부 모델 행동 평가는 실행 결과가 확인된 경우에만 통과로 기록한다.

## 10. 완료 기준

- 새 광역 Skill이나 Registry 중복 없이 1+3 구조가 기존 라우터에 연결된다.
- 사용자안과 AI 최초안을 같은 기준으로 검토하도록 항상 적용 규칙이 생긴다.
- 반대를 위한 반대와 근거 없는 동의를 모두 실패 조건으로 검출한다.
- L0 경량 작업과 L1 이상 전체 검토의 경계가 명확하다.
- 기술 판단·사용자 결정·미검증 상태가 분리된다.
- 관련 행동 평가와 회귀가 변경을 검출할 수 있다.
- released lock·Registry bytes·과거 증거·프로젝트 파일은 보존된다.

## 11. 롤백

변경이 과도한 Skill 호출, 사용자 결정권 약화, 기존 라우팅 회귀를 일으키면 해당 정책·Skill·평가 변경을 같은 PR 단위로 되돌린다. released lock과 Registry를 수정하지 않으므로 이전 v9.4 계약으로 복귀할 수 있다.
