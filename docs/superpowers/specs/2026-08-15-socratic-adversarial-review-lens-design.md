# Socratic Adversarial Review Lens 설계

## 1. 결정

새 `socratic-questioning` 광역 Skill을 만들지 않는다.

기존 `running-adversarial-review-and-refinement`가 적대적 검토의 단일 실행 책임을 유지하고, Socratic questioning은 그 내부에서 사고의 명료성·가정·근거·관점·파급·질문 자체를 점검하는 선택형 `Socratic Review Lens`로 흡수한다.

상세 질문은 새 reference `skills/running-adversarial-review-and-refinement/references/socratic-questioning-lenses.md`가 소유한다. `SKILL.md`는 언제 이 reference를 읽고 어떻게 finding으로 연결하는지만 책임진다.

## 2. 배경

Base의 현행 적대적 검토는 다음 흐름을 사용한다.

```text
attack
→ validate-critique
→ refine-approved-findings
→ regression-recheck
→ decision-report
```

또한 사용자안과 AI 최초안을 같은 평가 기준으로 검토하고, 근거 없는 동의와 반대를 위한 반대를 모두 금지한다. `cross-discipline-review-lenses.md` 역시 관련 Lens만 선택하고 모든 Lens를 억지로 채우기 위한 가짜 Finding을 금지한다.

Socratic questioning의 대표적 분류는 다음 질문군을 반복적으로 사용한다.

1. clarification
2. probing assumptions
3. probing reasons/evidence
4. viewpoints/perspectives
5. implications/consequences
6. questions about the question

Foundation for Critical Thinking의 Richard Paul·Linda Elder 계열 자료는 Socratic questioning을 단순 질문 목록이 아니라 중요한 사고를 체계적이고 깊게 탐색하는 disciplined questioning으로 설명하며, 위 질문군을 reasoning의 assumptions, evidence, viewpoints, implications 등과 연결한다.

## 3. 목표

1. 애매한 주장이나 용어를 명료화하기 전에 결함으로 확정하지 않는다.
2. 사용자안과 AI 최초안의 숨은 가정을 대칭적으로 공격한다.
3. 주장과 정본·실제 구현·테스트·외부 근거 사이의 증거 사슬을 점검한다.
4. 현재 선호안 외의 실질적 대안과 이해관계자 관점을 찾는다.
5. 채택 시 정상 경로·실패 경로·회귀·유지·롤백 파급을 검토한다.
6. 제기된 비판 자체가 중요한지, 범위 안인지, 결론을 바꾸는지 재검증해 가짜 Finding과 질문 폭주를 줄인다.
7. 저장소·정본·도구로 답할 수 있는 사실을 사용자에게 되묻지 않는다.

## 4. 비목표

- 새 Skill ID 또는 Registry entry를 추가하지 않는다.
- 모든 L0·기계 수정에서 6개 질문군을 강제로 실행하지 않는다.
- 여섯 질문군마다 Finding을 하나씩 만들지 않는다.
- Socratic questioning을 사용자 인터뷰 또는 승인 Gate로 바꾸지 않는다.
- 저장소에서 확인할 수 있는 사실을 사용자 질문으로 대체하지 않는다.
- 사용자 최신 지시, 분야 정본, 기존 `USER_DECISION_REQUIRED` / `BLOCKED_UNVERIFIED` 경계를 약화하지 않는다.
- 진행 중인 기존 PR의 파일이나 branch를 수정하지 않는다.

## 5. 구조

```text
running-adversarial-review-and-refinement
│
├─ attack
│  ├─ clarification
│  ├─ assumptions
│  ├─ reasons/evidence
│  ├─ viewpoints
│  └─ implications/consequences
│
├─ validate-critique
│  ├─ evidence 재검증
│  ├─ assumption 재검증
│  └─ questions-about-the-question
│
├─ refine-approved-findings
│
├─ regression-recheck
│  └─ implications/consequences 재검사
│
└─ decision-report
   └─ 질문의 중요성·범위·미검증 기록
```

### 5.1 Socratic Lens 계약

각 Lens는 질문을 생성하기 위한 목적이 아니라 **검토 finding의 품질을 높이는 검사 관점**이다.

| Lens | Base 역할 | 대표 검사 |
|---|---|---|
| Clarification | 주장·용어·Requirement·완료 기준 명확화 | "정확히 무엇을 주장하고 있는가?" |
| Assumptions | 숨은 전제·의존성·당연시한 조건 공격 | "무엇이 사실이라고 가정해야 이 결론이 성립하는가?" |
| Reasons / Evidence | 주장과 실제 증거의 연결 검증 | "어떤 정본·코드·테스트·자료가 이 결론을 지지하거나 반증하는가?" |
| Viewpoints | 유효한 대안·이해관계자 관점 탐색 | "다른 선택·플레이어·개발·QA·운영 관점에서 무엇이 달라지는가?" |
| Implications / Consequences | 채택 결과·회귀·장기 영향 탐색 | "이 결론을 적용하면 정상·실패·복구·롤백 경로에 어떤 변화가 생기는가?" |
| Meta-question | 질문·비판 자체의 중요성·범위 검증 | "답이 달라지면 실제 결정도 달라지는가?" |

### 5.2 질문 처리 우선순위

```text
Socratic question candidate
→ 저장소·정본·실제 구현·도구로 답할 수 있는가?
  → YES: AI가 직접 조사하고 evidence로 기록
  → NO
→ 답이 결론·완료·코어에 영향을 주는가?
  → NO: NOT_APPLICABLE / DEFER / REJECTED_CRITIQUE
  → YES
→ 기술 증거가 부족한가?
  → BLOCKED_UNVERIFIED + 확인 조건
→ 둘 이상의 유효한 선택이 프로젝트 코어·중요 방향을 다르게 만드는가?
  → USER_DECISION_REQUIRED + 사용자 질문 1개
```

사용자 질문은 마지막 수단이다. Socratic Lens를 이유로 인터뷰를 늘리지 않는다.

## 6. 기존 적대적 검토와의 중복 제거

- 기존 `attack`의 실패·모순·악용·누락 탐색은 그대로 유지한다.
- Socratic Lens는 attack 대상의 **사고 구조**를 명료화하고 빠진 전제·증거·관점·파급을 찾는다.
- 기존 `validate-critique`의 사실성·발생 가능성·영향·비용 재판정은 유지한다.
- `Meta-question`은 `validate-critique` 안에서 "이 비판이 진짜 결론을 바꾸는가"를 재검증해 반대를 위한 반대를 제거한다.
- `cross-discipline-review-lenses`는 제품·UX·아키텍처 등 **분야 관점**을 제공하고, Socratic Lens는 그 관점을 심문하는 **질문 구조**를 제공한다. 둘은 대체 관계가 아니다.

## 7. 파일 변경

### 신규

- `skills/running-adversarial-review-and-refinement/references/socratic-questioning-lenses.md`
  - 6개 Lens
  - 선택 규칙
  - 내부 조사 우선 규칙
  - 사용자 질문 승격 조건
  - finding 연결 예시

### 수정

- `skills/running-adversarial-review-and-refinement/SKILL.md`
  - Socratic Review Lens 선택 규칙과 reference 링크
  - attack / validate-critique / regression-recheck 연결
  - 저장소로 답할 사실 재질문 금지
- `tests/test_neutral_adversarial_feature_lifecycle.py`
  - 6개 Lens 계약
  - 새 reference 연결
  - 질문 폭주 방지·내부 조사 우선·Meta-question 계약 회귀

### 필요 시 최소 동기화

- `.github/reference-freshness.json`
  - 기존 coupled rule이 새 reference와 집중 테스트의 동시 변경을 놓치는 경우에만 수정한다.
- `docs/CHANGELOG.md`, `skills/SKILL_LEARNING_LOG.md`
  - 변경이 구현·검증된 뒤 완료 상태만 기록한다.

## 8. 행동 규칙

1. 모든 Lens를 의식적으로 채우지 않는다. 현재 Requirement·Finding·위험과 직접 연결된 Lens만 사용한다.
2. Clarification이 필요한 애매한 문장을 곧바로 결함으로 확정하지 않는다.
3. Assumption은 증거 없는 추측을 새 사실로 만들지 않는다.
4. Evidence Lens는 정본·실제 구현·테스트·공식/1차 자료를 우선한다.
5. Viewpoints는 사용자안과 AI안 외 최소 하나의 실질적 대안을 찾되, 존재하지 않는 대안을 억지로 만들지 않는다.
6. Consequences는 기능 추가 수가 아니라 사용자/플레이어 가치, 정상·실패·복구·회귀·롤백 영향을 검토한다.
7. Meta-question은 finding이 중요한지, 현재 범위인지, 답이 결론을 바꾸는지 재판정한다.
8. 저장소·정본·도구로 해결 가능한 질문은 사용자에게 묻지 않는다.
9. 사용자 결정이 필요한 경우 기존 정책대로 가장 중요한 질문 하나만 올린다.
10. `BLOCKED_UNVERIFIED`, `REJECTED_CRITIQUE`, `DEFER`, `USER_DECISION_REQUIRED`의 기존 의미를 재정의하지 않는다.

## 9. 테스트 전략

집중 회귀는 최소 다음을 검출한다.

- 새 reference가 6개 Lens를 모두 정의한다.
- `SKILL.md`가 새 reference를 실제 실행 경로에 연결한다.
- 모든 Lens 강제 사용과 가짜 Finding 생성을 금지한다.
- 저장소·정본으로 답할 수 있는 사실은 직접 조사하도록 한다.
- Meta-question이 중요성·범위·결론 변화 여부를 검증한다.
- Socratic Lens가 사용자 인터뷰 Gate를 새로 만들지 않는다.
- Registry Skill ID 집합은 변경되지 않는다.

문자열 존재만으로 실제 모델 행동을 증명하지 않는다. 이번 변경의 증거 상한은 문서/Skill 계약과 저장소 회귀 테스트이며, 실제 모델 행동 평가는 별도 실행했을 때만 통과로 기록한다.

## 10. 외부 근거

- Foundation for Critical Thinking, Richard Paul & Linda Elder, *The Thinker's Guide to the Art of Socratic Questioning*: https://www.criticalthinking.org/TGS_files/SocraticQuestioning2006.pdf
- Foundation for Critical Thinking, *The Role of Socratic Questioning in Thinking, Teaching, and Learning*: https://www.criticalthinking.org/pages/the-role-of-socratic-questioning-in-thinking-teaching-learning/522

채택하는 것은 질문 분류와 disciplined questioning 원칙이며, 교육용 대화 절차 전체를 Base 운영 절차로 복제하지 않는다.

## 11. 완료 기준

- 기존 `running-adversarial-review-and-refinement` 안에서 Socratic Review Lens가 발견 가능하다.
- 6개 Lens가 reference에 명확히 정의된다.
- attack / validate-critique / regression-recheck에 역할이 연결된다.
- 가짜 Finding·질문 폭주·사용자 재질문을 방지하는 경계가 있다.
- 새 Skill ID와 Registry 중복이 없다.
- 집중 회귀 테스트가 통과한다.
- 진행 중인 기존 PR은 변경되지 않는다.

## 12. 롤백

회귀로 인해 적대적 검토가 과도하게 장황해지거나 사용자 질문을 늘리거나 기존 finding 판정과 충돌하면, 이번 PR에서 추가한 reference·SKILL 연결·집중 테스트를 함께 되돌린다. 새 Skill ID·Registry·released lock을 만들지 않으므로 기존 적대적 검토 구조로 바로 복귀할 수 있다.
