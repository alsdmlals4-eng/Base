# 튜토리얼·온보딩 설계 Guide 설계

- 상태: `APPROVED_DESIGN`
- 사용자 승인: `2026-08-02`
- 기준 Base main: `896d2e6fd257084b6aa29b1703cd0bbfa3b18daa`
- Work Mode: `PLAN → BUILD → REVIEW`
- 주 Skill: `analyzing-and-refining-game-concepts: tutorial-and-onboarding-design`
- 지원 Skill: `managing-project-intake-and-work-contract`, `governing-game-user-research-coverage`, `running-adversarial-review-and-refinement`, `reviewing-and-validating-project-changes`
- 신규 광역 Skill: 추가하지 않음
- Base Google Sheets 동기화: `NOT_APPLICABLE` — Base 자체는 프로젝트 Sheet 동기화 대상이 아니며 대상 프로젝트가 지정되지 않음

## 1. 목적

게임 프로젝트의 튜토리얼을 조작 설명이나 긴 텍스트 안내가 아니라, 플레이어가 핵심 규칙을 실제로 수행하고 문제를 인식한 뒤 해결 방법과 성장 시스템을 발견하며 성장 전후 차이를 체감하고, 안내 없이 같은 원리를 다시 사용할 수 있게 만드는 검증 가능한 학습 흐름으로 설계한다.

사용자가 제시한 핵심 골격을 다음처럼 보존·확장한다.

```text
기본 룰 제공
→ 필요·결핍(문제 발생)
→ 성장 시스템(방법 발견)
→ 성장 체감(쾌감 제공)
→ 독립 수행
→ 다른 상황에서 재사용
```

이 Guide는 공용 방법론과 검증 계약만 소유한다. 프로젝트 고유 규칙·수치·성장 내용·첫 세션 구성·실제 구현 상태는 각 프로젝트 정본과 코드·데이터·자산·테스트가 소유한다.

## 2. 현행 Base 구조와 통합 판단

Base의 `analyzing-and-refining-game-concepts`는 핵심 컨셉, DDD, 벤치마크, 플레이테스트, 게임 시스템 경계와 성장·보상 설계를 이미 소유한다. 튜토리얼 설계는 별도 독립 권한이 아니라 이 책임을 첫 학습 경험에 적용하는 조건부 mode다.

`governing-game-user-research-coverage`는 튜토리얼 이해도 연구 영역의 설치·누락 감사를 담당한다. 튜토리얼 자체의 학습 흐름 설계는 `analyzing-and-refining-game-concepts`, 연구 Coverage와 증거 누락 감사는 `governing-game-user-research-coverage`가 담당해 경계를 분리한다.

따라서 다음 구조를 사용한다.

```text
프로젝트 정본·실제 구현·진행 상태 복원
→ tutorial-and-onboarding-design mode
→ 조건부 공용 Guide
→ 프로젝트용 설계 Contract
→ 플레이테스트·텔레메트리 계약
→ 적대적 검토
→ 실제 변경 검증
```

## 3. 프로젝트 선감사 Gate

프로젝트에 적용할 때는 튜토리얼 문구나 화면을 먼저 만들지 않는다. 다음을 확인한다.

1. 최신 사용자 지시와 승인 Decision
2. 프로젝트 `AGENTS.md`, `START_HERE`, Active Context, Documentation Map
3. 현재 핵심 컨셉·코어 루프·대상 플레이어·첫 세션 목표
4. 실제 코드·데이터·Scene·Resource·UI·입력·테스트
5. 프로젝트 Google Sheets가 구성된 경우 현재 진행도·계획·제안 변경
6. 동일 Goal의 열린 PR과 최근 병합 PR
7. 기존 튜토리얼·도움말·온보딩·첫 플레이 데이터
8. 보류·대체·폐기된 구형 기획
9. 벤치마크가 답해야 할 현재 결정 질문

정본·실제 구현·진행 상태를 확인하지 못하면 `BLOCKED_UNVERIFIED`로 표시한다. 프로젝트 고유 규칙이나 구현 상태를 외부 사례로 추정해 채우지 않는다.

## 4. 튜토리얼 학습 사다리

### 4.1 `RULE` — 기본 규칙 수행

- 플레이어가 현재 필요한 목표·행동·결과를 실제 플레이로 수행한다.
- 한 구간에서 한 개의 핵심 학습 목표를 우선한다.
- 정적 조작표나 설명만 읽은 상태를 학습 완료로 판정하지 않는다.
- 첫 의미 있는 행동과 피드백을 불필요한 메뉴·계정·메타 기능보다 먼저 제공한다.

### 4.2 `NEED` — 필요·결핍 인식

- 성장이나 새 시스템을 소개하기 전에 현재 능력으로 해결하기 어렵거나 비효율적인 실제 문제를 제시한다.
- 플레이어가 실패·지연·비용·위험의 원인을 설명할 수 있어야 한다.
- 강제 패배나 숨은 규칙으로 결핍을 조작하지 않는다.
- 문제 전 예고, 대응 기회, 실패 후 복구와 재시도를 제공한다.

### 4.3 `DISCOVER` — 해결 방법 발견

- 플레이어가 문제를 인식한 뒤 필요한 성장·도구·규칙·정보를 공개한다.
- 플레이어가 직접 획득·선택·장착·적용하거나 사용한다.
- `무엇을 누르는가`뿐 아니라 `왜 지금 필요한가`, `언제 다시 쓰는가`를 연결한다.
- 해결 방법이 여러 개라면 첫 학습에서는 최소 대표 방법을 가르치고 이후 선택 공간을 확장한다.

### 4.4 `FEEL` — 성장 전후 차이 체감

```text
성장 전 기준 행동
↔ 성장 후 동일하거나 비교 가능한 행동
```

성장 체감은 숫자·이펙트·팝업 크기만이 아니라 다음 중 하나 이상의 행동 변화로 증명한다.

- 시간·자원·위험 감소
- 새로운 선택·경로·조합 발생
- 이전 장벽 돌파
- 실패 원인과 개선 원인의 명료한 연결
- 핵심 재미의 강화

### 4.5 `PROVE` — 안내 없는 독립 수행

- 하이라이트·강제 입력·정답 고정을 줄인 상태에서 같은 원리를 다시 사용한다.
- 성공·실패 원인을 플레이어가 이해할 수 있어야 한다.
- 한 번의 우연한 성공만으로 숙련을 확정하지 않는다.
- 핵심 조작·판단은 실제 플레이 환경과 일치하는 조건에서 검증한다.

### 4.6 `TRANSFER` — 재사용·복귀

- 다른 적·상황·조합·레벨에서 배운 원리를 재사용한다.
- 튜토리얼·도움말·목표를 필요할 때 다시 확인할 수 있다.
- 숙련자 Skip과 신규·복귀 플레이어의 재학습 경로를 함께 제공한다.
- 음성·색·시간 제한 하나에만 정보를 의존하지 않고 접근성 대체 채널을 둔다.

## 5. 점진 공개와 안내 감소

튜토리얼은 `설명량`이 아니라 `플레이어 자율성`의 변화로 설계한다.

```text
시범·명확한 안내
→ 제한된 선택 안에서 수행
→ 힌트가 있는 유사 문제
→ 안내 없는 독립 수행
→ 다른 상황으로 전이
```

각 단계는 다음 진입 조건을 가진다.

- 필요한 선수 지식이 확인됨
- 현재 행동을 성공 또는 실패 원인까지 이해함
- 다음 개념이 이전 개념 위에 자연스럽게 쌓임
- 안내를 줄여도 막힘이 과도하게 증가하지 않음
- 실패 시 이전 학습을 다시 볼 경로가 있음

## 6. 벤치마크 원칙

외부 튜토리얼과 온보딩은 기능 목록이 아니라 작동 원리와 실패 조건을 비교한다.

주요 근거:

- Apple `Onboarding for Games`: 핵심 루프를 실제 행동으로 가르치고, 기본 요소부터 시작해 숙련 확인 후 복잡도를 높이며, 짧은 단계·필요한 순간의 여러 튜토리얼·안내 없는 플레이·Skip을 권장한다.
- Microsoft Xbox Accessibility Guideline 109: 정적 조작 화면은 충분한 튜토리얼이 아니며, 핵심 메커니즘을 실제로 수행하거나 시연하고 필요할 때 다시 접근할 수 있어야 한다.
- Microsoft Xbox Accessibility Guideline 116: 비핵심 UI 안내의 시간 제한은 플레이어가 읽고 해석하고 수행할 충분한 시간을 보장해야 한다.

벤치마크 결과는 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 판정하고, 출처·날짜·버전·적용 조건·표본 한계를 기록한다. 프로젝트 정본보다 높은 권한을 갖지 않는다.

## 7. 프로젝트 산출물 Contract

```md
## 프로젝트·첫 세션 현황 감사
## 대상 플레이어·플레이 상황·선수 지식
## 핵심 학습 목표와 본편 규칙 연결
## RULE–NEED–DISCOVER–FEEL–PROVE–TRANSFER 단계표
## 안내 감소·힌트·실패·복구·재시도
## Skip·복습·복귀·접근성 대체 채널
## 성장 전후 비교와 핵심 재미 강화 근거
## 벤치마크 질문·근거·판정
## 플레이테스트 과제·관찰·인터뷰·텔레메트리
## 적대적 Finding과 판정
## KEEP / CHANGE / REMOVE / TEST / HOLD
## 미검증·롤백·다음 Gate
```

## 8. 플레이테스트와 측정

완료율 하나로 학습을 판정하지 않는다. 최소한 다음을 분리한다.

- 첫 의미 있는 행동까지의 시간
- 단계별 진입·성공·실패·재시도·이탈
- 힌트 요청·도움말 재열람·Skip
- 독립 수행 성공률과 실패 원인
- 성장 전후 행동 시간·자원·위험·선택 변화
- 다른 상황에서의 전이 성공
- 플레이어 자기보고와 실제 행동의 불일치
- 접근성 옵션·대체 채널 사용과 막힘

지표와 성공·중단 기준은 결과를 보기 전에 선언한다. 실제 빌드·대상 집단·과제·관찰 없이 재미·이해·체감을 검증했다고 주장하지 않는다.

## 9. 적대적 검토

### 필수 공격 질문

- 튜토리얼 전용 규칙이 본편과 다른가
- 조작 설명을 이해·판단 학습으로 오인했는가
- 플레이어가 문제를 인식하기 전에 해결책을 광고하는가
- 강제 패배·숨은 규칙·회복 불가능 손실로 결핍을 조작하는가
- 성장 후 숫자만 커지고 행동·선택은 그대로인가
- 핵심 재미보다 메타·상점·과금·알림을 먼저 노출하는가
- 여러 개념을 동시에 가르쳐 실패 원인을 알 수 없게 만드는가
- 한 번의 성공·완료율만으로 숙련을 확정하는가
- 안내를 제거하면 수행할 수 없는가
- Skip·복습·복귀·접근성 대안이 없는가
- 벤치마크 기능을 프로젝트 맥락 없이 복제하는가

Finding은 `MUST_FIX`, `SHOULD_FIX`, `USER_DECISION_REQUIRED`, `DEFER`, `REJECTED_CRITIQUE`, `BLOCKED_UNVERIFIED`로 분류한다. 검증된 Finding만 최소 수정하고 회귀 재검사를 수행한다.

## 10. 파일 구조

### 생성

- `docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md`: 공용 방법론·근거·실패 경계
- `templates/planning/TUTORIAL_AND_ONBOARDING_DESIGN_CONTRACT.md`: 프로젝트 적용용 산출물 틀
- `tests/test_tutorial_and_onboarding_design_contract.py`: Guide·Template·Skill·라우팅 계약 회귀
- `docs/superpowers/plans/2026-08-02-tutorial-and-onboarding-design-guide.md`: 테스트 우선 구현 계획

### 수정

- `skills/analyzing-and-refining-game-concepts/SKILL.md`: 조건부 mode·reference·산출물 연결
- `docs/knowledge/game-development/README.md`: Guide 발견 경로
- `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`: 공식 근거와 적용 범위
- `START_HERE.md`: 튜토리얼·첫 세션 요청의 한 단계 라우트

### 보호

- 새 광역 Skill을 추가하지 않는다.
- 기존 Skill ID를 변경하지 않는다.
- Base release lock과 frozen snapshot을 변경하지 않는다.
- 프로젝트별 세계관·수치·기획·Google Sheets를 Base에 복제하지 않는다.
- 열린 PR #134·#136의 Prompt 파일 범위를 수정하지 않는다.

## 11. 비목표

- 모든 게임에 같은 튜토리얼 순서·화면·대사 강제
- 성장 시스템이 없는 게임에 인위적인 수치 성장 추가
- 강제 패배를 통한 상점·과금 전환 설계
- 튜토리얼을 실제 플레이테스트 없이 완료 판정
- 접근성 옵션 존재만으로 접근성 검증 완료 주장
- Base 자체를 프로젝트 Google Sheets에 동기화
- 특정 엔진 구현 코드 작성

## 12. 완료 조건

- 기존 `analyzing-and-refining-game-concepts`가 튜토리얼 설계 주 책임을 유지한다.
- 공용 Guide와 프로젝트 Contract가 `RULE → NEED → DISCOVER → FEEL → PROVE → TRANSFER`를 구현한다.
- 프로젝트 선감사, 벤치마크, 적대적 검토, 측정·플레이테스트가 연결된다.
- 강제 패배·가짜 결핍·가짜 성장·정적 조작표·완료율 단독 판정이 실패 경계로 명시된다.
- Skip·복습·복귀·접근성 대체 채널이 포함된다.
- 관련 테스트가 RED에서 의도대로 실패하고 구현 후 GREEN으로 통과한다.
- 정확한 PR HEAD에서 Required Check와 변경 파일 범위를 확인하며, 실행하지 않은 사람 플레이테스트·엔진 런타임은 `NOT_RUN`으로 보고한다.
