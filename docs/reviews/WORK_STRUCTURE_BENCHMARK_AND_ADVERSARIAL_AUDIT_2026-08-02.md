# Base 작업 구조 벤치마킹·적대적 검토

- Date: 2026-08-02
- Baseline main: `79cae496b89eb519d93b1430ceb0caa13ac77d8b`
- Review mode: `PLAN → REVIEW`
- Primary responsibility: `managing-project-intake-and-work-contract`
- Supporting review: `running-adversarial-review-and-refinement`, `reviewing-and-validating-project-changes`
- Scope: Base 작업 진입, Work Mode·Skill 라우팅, 기획 결정권, Grill Me, 검증·PR·릴리스·프로젝트 전파
- Product/runtime changes: none

## 1. 결론

현재 Base 작업 구조는 **고거버넌스·다중 프로젝트 게임 기획/개발 운영체계로서 적절하며 정적 계약 강도는 높다.** 특히 선택적 Skill 라우팅, 책임 원본 우선순위, `PLAN / BUILD / REVIEW` 권한 분리, exact-head 검증, Registry·release lock 보호, 미실행 증거를 `NOT_RUN`으로 남기는 방식은 일반적인 프롬프트 모음보다 훨씬 강하다.

다만 다음 세 경계가 상위 작업 순서에 충분히 명시되지 않았다.

1. `L1` 이상에서 기획이 구현보다 선행해야 한다는 불변 원칙
2. GPT가 결정할 가역적 상세 수치와 사용자가 승인할 기획 충돌의 경계
3. Grill Me 승인 Decision을 언제 PR로 묶고 검사·적대적 검토·병합할지에 대한 배치 규칙

이 감사에서는 새 광역 Skill을 추가하지 않고 `AGENTS.md`와 단일 상세 정책·Template·CI 회귀로 보완했다.

## 2. 벤치마킹

### 2.1 작은 자기완결 변경

Google Engineering Practices는 작은 변경이 더 빠르고 철저하게 검토되고, 버그 가능성·거절 시 낭비·병합 충돌을 줄이며 설계를 다듬기 쉽다고 설명한다.

적용:

- “정확히 승인 10건을 채워야 한다”는 고정 최소 배치를 채택하지 않는다.
- `MAX_APPROVED_DECISIONS_PER_BATCH: 10`을 **상한**으로 둔다.
- 고위험·정본 충돌·구현 차단·세션 종료·사용자 요청·diff 과대화에는 조기 체크포인트를 연다.

Source:

- `https://google.github.io/eng-practices/review/developer/small-cls.html`

### 2.2 기술 사실과 지속적 개선

Google의 코드 리뷰 표준은 의견보다 기술 사실과 데이터를 우선하고, 완벽함을 기다리기보다 전체 코드 건강을 분명히 개선하는 변경을 승인하는 균형을 권장한다.

적용:

- 적대적 검토를 무조건 반대하는 절차로 사용하지 않는다.
- `MUST_FIX / SHOULD_FIX / OPTIONAL / REJECTED_CRITIQUE / BLOCKED_UNVERIFIED`를 분리한다.
- 사용자안이 가장 강하면 근거와 함께 채택한다.
- L0 기계 수정까지 장문의 PLAN으로 막지 않는다.

Sources:

- `https://google.github.io/eng-practices/review/reviewer/standard.html`
- `https://google.github.io/eng-practices/review/reviewer/looking-for.html`

### 2.3 최신 HEAD의 필수 검사

GitHub 문서는 protected branch의 required check가 최신 Commit SHA에 대해 통과해야 한다고 설명한다.

적용:

- 이전 Commit의 성공 결과를 배치 PR 병합 근거로 재사용하지 않는다.
- 배치 PR의 `batch_exact_head`를 기록한다.
- required checks, unresolved thread, P0/P1, 미해결 사용자 결정을 병합 직전에 다시 확인한다.

Source:

- `https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks`

## 3. 현재 구조의 강점

### 3.1 권한 순서가 명확하다

`사용자 최신 지시 → 프로젝트 규칙 → Active Context·승인 계약 → 책임 원본·실제 구현 → 프로젝트가 채택한 Base → Base 원본 → 외부 근거` 순서가 명시돼 있다.

효과:

- 외부 벤치마크가 프로젝트 정본을 덮어쓰지 않는다.
- Base가 프로젝트 고유 결정과 구현 상태를 침범하지 않는다.
- Sheet·대시보드·과거 대화가 독립 정본으로 승격되지 않는다.

### 3.2 최소 Skill 자동 라우팅

`load_all_skills=false`, trigger 일치, 주 책임 분야 하나의 원칙은 컨텍스트 과적재와 책임 중복을 줄인다.

### 3.3 Work Mode와 Skill 책임이 분리된다

`PLAN / BUILD / REVIEW`는 권한 상태이며 Skill은 분야 책임이다. REVIEW finding을 즉시 수정하지 않고 승인된 범위만 BUILD로 전환한 뒤 REVIEW로 복귀하는 구조가 합리적이다.

### 3.4 검증과 적대적 검토가 분리된다

- `running-adversarial-review-and-refinement`: 실패 가정·반례·finding 분류
- `reviewing-and-validating-project-changes`: diff·정적·런타임·회귀 증거
- `auditing-canonical-reference-freshness`: 정본·경로·ID·Schema 전파

공격과 실제 증거 검사를 분리해 “비판했으니 검증했다”는 오류를 줄인다.

### 3.5 릴리스·Adapter 경계가 명확하다

Base release payload/evidence와 프로젝트 Adapter pin을 분리해 Base main의 미병합·미릴리스 변경이 프로젝트에 몰래 유입되지 않게 한다.

### 3.6 증거 과장을 차단한다

실제 모델·런타임·기기·사람 검증을 수행하지 않았으면 `NOT_RUN`으로 유지한다. 정적 계약 통과를 실제 행동·제품 품질 통과로 과장하지 않는다.

## 4. 적대적 검토 Finding

### MUST_FIX — 해결됨

#### F-01 기획 우선 원칙이 상위 불변 규칙으로 충분히 명시되지 않음

위험:

- 상세 요청을 구현 승인으로 오인할 수 있다.
- 정본 충돌·비목표·검증·롤백이 닫히기 전에 BUILD로 이동할 수 있다.

수정:

- `AGENTS.md`에 `기획 우선 원칙` 추가
- `L1` 이상 `PLAN → 승인된 실행 계약 → BUILD → REVIEW`
- L0 기계 수정 예외 보존

#### F-02 수치 결정권 경계가 모호함

위험:

- 모든 수치를 사용자에게 물어 작업이 정체된다.
- 반대로 GPT가 경제·세션 길이·난이도 곡선처럼 기획을 바꾸는 수치를 기술 기본값으로 확정할 수 있다.

수정:

- `DETAILED_NUMERIC_DEFAULT` / `RECOMMENDED_DEFAULT`
- `PLANNING_CONFLICT` / `USER_DECISION_REQUIRED` / `GRILL_ME_REQUIRED`
- 난이도·경제·성장·세션·빌드 우열·보상 의미·핵심 경험을 명시적 승격 조건으로 정의

#### F-03 승인 즉시 동기화와 10건 PR 배치가 충돌함

위험:

- 승인마다 main에 직접 반영하면 PR 검토를 우회한다.
- 정확히 10건까지 아무것도 기록하지 않으면 승인 유실·중단 복원 실패가 발생한다.

수정:

- 승인 즉시 활성 배치 Branch·GitHub 추적 surface·Decision별 논리 Commit에 기록
- Sheet는 `APPROVED_PENDING_MERGE`
- 최대 10건 또는 조기 체크포인트에서 하나의 PR
- 병합 후 main·Sheet 재조회 뒤 `SYNCED_TO_MAIN`

#### F-04 10번째 승인 뒤 계속 질문할 수 있음

수정:

- 병합·재동기화 전 11번째 질문 금지
- 10건 미만에서 세션 종료 시 잔여 배치도 동일 Gate로 종료

#### F-05 존재하지만 Required CI가 실행하지 않는 중복 테스트 위험

수정:

- standalone 테스트를 제거
- 기존 Required CI가 실행하는 `tests/test_deep_interview_contract.py`에 계약 통합

### SHOULD_FIX — 후속 검증 필요

#### F-06 실제 프로젝트 Grill Me 배치 Pilot 부재

상태: `NOT_RUN`

측정 제안:

- 배치별 승인 수
- 조기 체크포인트 비율
- PR changed files/lines
- 리뷰 시간
- 재작업·되돌림 수
- 사용자 질문 피로
- 병합 전후 Sheet 불일치

#### F-07 실제 모델 라우팅 행동평가 미실행

상태: `NOT_RUN`

Base v9.4.1은 행동평가 Schema·coverage·결과 신원 검증을 제공하지만 실제 외부 모델 결과는 별도 실행이 필요하다.

#### F-08 독립 검토의 운영적 독립성

자동 adversarial gate와 계약 회귀는 존재하지만, 동일 모델·동일 컨텍스트가 작성과 검토를 모두 수행하면 인지적 독립성이 약해질 수 있다. 고위험 배치에서는 별도 검토 Context 또는 다른 리뷰어 증거를 권장한다.

#### F-09 프로젝트 채택 전파

새 정책이 Base main에만 병합되면 현재 v9.4.1 pin 프로젝트는 정식 채택 상태가 아니다. Base compatibility release와 프로젝트 Adapter pin 갱신 Wave가 필요하다.

## 5. 기각한 과잉 개선

### R-01 새 광역 Skill 추가

기각 이유:

- Intake·Grill Me·Work Mode·검증·적대적 검토 책임이 이미 존재한다.
- 새 Skill은 라우팅 경쟁과 책임 중복을 늘린다.

### R-02 모든 상세 수치를 Grill Me로 질문

기각 이유:

- 가역적 초기값까지 사용자에게 전가해 결정 피로와 구현 지연을 만든다.
- GPT 권장 기본값 + 검증·조정 조건이 더 적절하다.

### R-03 정확히 10건을 채운 뒤만 PR 생성

기각 이유:

- 중요한 결정 지연
- 큰 PR과 리뷰 품질 저하
- 세션 중단 시 미통합 승인 누적

### R-04 승인마다 main 직접 Commit

기각 이유:

- batch PR exact-head 검토와 적대적 Gate를 우회한다.
- rollback과 Decision 묶음 검토가 어려워진다.

### R-05 같은 상세 절차를 모든 상위 문서에 복제

기각 이유:

- 문서 drift와 수정 비용을 높인다.
- `AGENTS.md`의 불변 요약 + 단일 상세 정책이 더 명확하다.

## 6. 최종 판정

```yaml
work_structure_overall: STRONG
planning_first_authority: STRENGTHENED
numeric_decision_boundary: STRENGTHENED
grill_me_batch_governance: ADDED
small_change_and_early_checkpoint_alignment: PASS
latest_exact_head_gate: PASS_BY_CONTRACT
adversarial_review_balance: PASS_BY_CONTRACT
registry_and_release_lock_preservation: REQUIRED
actual_project_batch_pilot: NOT_RUN
actual_external_model_behavior: NOT_RUN
independent_human_or_external_review: NOT_RUN
project_adapter_adoption: PENDING_BASE_RELEASE
```

현재 구조는 적절하다. 단, 정책 병합만으로 실제 프로젝트 운영 효과까지 증명됐다고 보아서는 안 된다. 다음 검증 단위는 새 Base compatibility release, 프로젝트 Adapter 채택, 한 프로젝트 Pilot, 결과 기반 재조정이다.
