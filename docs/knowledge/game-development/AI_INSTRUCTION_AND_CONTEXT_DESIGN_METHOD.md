# AI 지시·Context 설계 Method

## 1. 목적과 권위

AI 지시문과 Context Pack을 무조건 길고 구체적으로 만드는 대신, **무엇을 강제하고 무엇을 기본값으로 두며 무엇을 판단에 맡길지** 구분한다. 현재 결정 질문에 필요한 정본·근거·실제 파일만 선별하고, 작업 유형에 맞는 검증 가능한 Artifact를 사용한다.

이 Method는 사용자 최신 지시, 프로젝트 `AGENTS.md`, 승인된 책임 원본, 실제 파일·검증을 덮어쓰지 않는다. AI Memory와 과거 대화는 편의 입력이며 GitHub 정본을 대체하지 않는다.

담당 실행:

- 요청·작업 계약·first-prompt·Grill Me 정합성: `managing-project-intake-and-work-contract`
- Skill 본문 점진적 공개: `simplifying-skill-bodies`
- 모델·추론·비용: `optimizing-ai-model-and-prompt-costs`
- UI 설계·모션: `auditing-and-refining-ui-art`
- 결과 검증: `reviewing-and-validating-project-changes`

## 2. 지시 권위 예산

모든 문장을 강한 규칙으로 만들지 않는다. 지시는 다음 세 등급 중 하나를 가진다.

### `HARD_CONSTRAINT`

위반하면 안전·권한·무결성·호환성·법적 문제가 생기는 규칙이다.

```text
보안·개인정보
권한·신뢰 경계
데이터 무결성
비가역 변경과 파괴적 작업
저장·Schema·호환성
법적·라이선스 경계
사용자 명시적 금지·보호 대상
```

`HARD_CONSTRAINT`는 모델 판단력 향상을 이유로 삭제하거나 `JUDGMENT_SPACE`로 완화하지 않는다. 강제 규칙을 새로 추가할 때는 실제 실패를 막는지, 더 낮은 권위의 기본값·검증으로 대체할 수 없는지 기록한다.

### `RECOMMENDED_DEFAULT`

프로젝트 방향을 바꾸지 않고 정본·기술 표준·테스트로 최소 안전안이 정해지는 항목이다.

```text
파일·폴더·식별자 명명
일반적인 오류 처리·로그·테스트
초기 UI 간격·시간·수치 Fixture
기존 인터페이스를 보존하는 내부 구조
되돌릴 수 있는 작은 기술 선택
```

기본값에는 이유·조정 조건·검증을 둔다. 플레이어 경험·코어·경제·난이도·저장 의미를 바꾸면 기본값이 아니라 사용자 결정이다.

### `JUDGMENT_SPACE`

정본·범위·불변조건 안에서 AI가 대안을 비교해 선택할 수 있는 영역이다.

```text
비파괴적 초안의 표현 방식
정보 배치와 설명 순서
동등한 내부 구현 대안
현재 목적에 맞는 Artifact 형식
근거 범위 안의 개선 후보
```

판단 공간은 권한 위임이 아니다. 결과는 출력 계약과 검증 Gate를 통과해야 한다.

### 기록 형식

```yaml
instruction:
authority: HARD_CONSTRAINT | RECOMMENDED_DEFAULT | JUDGMENT_SPACE
reason:
source:
adjustment_condition:
validation:
```

## 3. Interface-first Prompt

Prompt는 긴 예시보다 먼저 작업의 입력·출력·불변조건을 정의한다.

```yaml
problem:
player_or_user_value:
inputs:
required_fields:
optional_fields:
authority_and_source:
output_contract:
invariants:
failure_conditions:
validation:
```

좋은 인터페이스는 다음을 답한다.

- 무엇을 해결하는가
- 누구에게 어떤 가치가 생기는가
- 어떤 입력이 필수이고 어떤 입력이 선택인가
- 어느 자료가 정본이고 어느 자료가 참고인가
- 결과를 어떤 형식과 상태로 반환하는가
- 절대 바꾸면 안 되는 것은 무엇인가
- 실패·중단·미검증은 어떻게 표시하는가
- 무엇으로 결과를 검증하는가

## 4. First-prompt direction anchoring

`direction anchor`는 Prompt의 첫 지시 섹션에 놓는 1~2문장이다. 핵심 행동, 의도한 결과, 가장 중요한 판단 기준을 먼저 고정해 뒤의 Context와 세부 조건이 같은 방향으로 해석되도록 돕는다.

```text
DIRECTION_ANCHOR
→ TASK_AND_SUCCESS
→ CONTEXT_AND_SOURCES
→ CONSTRAINTS_AND_PROTECTED_SCOPE
→ OUTPUT_AND_VALIDATION
→ OPTIONAL_RESPONSE_DIVERSIFICATION
```

### 배치 원칙

- 핵심 문장은 장황한 역할 설명·배경·예시보다 먼저 둔다.
- 순서는 주목도를 높이지만 권위를 높이지 않는다. 시스템·사용자 최신 지시·프로젝트 정본·`HARD_CONSTRAINT`와 충돌하면 anchor를 수정한다.
- “항상”, “절대”, “오직”, “반드시”는 실제 권한 근거가 있을 때만 사용한다.
- 첫 문장만 강하고 뒤의 범위·출력·검증이 비어 있으면 좋은 Prompt가 아니다.
- 방향 문장을 뒤의 계약에서 재정의하지 말고 같은 용어·범위·성공 기준을 유지한다.

### instruction/context 분리

지시와 자료를 명시적인 delimiter 또는 heading으로 구분한다.

```text
### Direction anchor
[핵심 행동 + 결과 + 지배 기준]

### Instruction
[Task / success / permissions]

### Context and Source
[정본 / 실제 파일 / 참고 / 충돌]

### Constraints
[보호 대상 / 비목표 / HARD_CONSTRAINT]

### Output and Validation
[산출물 / 상태 / 테스트 / 미검증]
```

Task, Context, Source, Constraints, Output, Validation은 고정 문구를 채우는 양식이 아니라 누락을 검사하는 인터페이스다. 작업에 필요 없는 빈 섹션은 만들지 않되, 필요한 의미를 다른 이름으로 숨기지 않는다.

### 첫 답변 다변화

설계·전략·기획 결정에서 하나의 관성적 초안이 전체 방향을 고정할 위험이 있으면 다음을 조건부로 요청한다.

```text
정석안: 검증된 기본 구조
파격안: 핵심 가정을 바꾸는 차별화 구조
통합안: 장점을 결합하고 복잡성을 통제한 구조
```

세 안은 같은 평가 기준·제약·반증 자료로 비교하고 하나를 추천한다. 오탈자·번역·정형 변환·승인 구현처럼 기계적이거나 이미 결정된 작업에는 억지 선택지를 만들지 않는다.

### conflict scan

```yaml
anchor_matches_task:
anchor_matches_output:
source_authority_preserved:
hard_constraints_preserved:
later_instruction_conflict:
protected_scope_visible:
user_decisions_visible:
counterevidence_preserved:
unverified_claims_labeled:
```

첫 문장이 뒤의 범위보다 넓거나 좁거나, Context의 문장이 Instruction처럼 보이거나, 예시가 정본을 대체하면 Prompt를 실행하지 않고 다시 작성한다.

### Grill Me alignment gate

모든 L1 이상 지시문은 intake Skill에서 `first-prompt → contract`를 거친 뒤 실행 전 `Grill Me alignment gate`로 사용자 의도와 기획 정합성을 확인한다.

- 중대한 모호성이 있으면 가장 영향이 큰 질문 하나씩 닫는다.
- 계약이 완전하지만 승인되지 않았으면 direction anchor와 핵심 계약을 한 번 확인받는다.
- 동일한 exact contract의 유효한 승인 근거가 있으면 재질문하지 않고 재사용한다.
- 승인 또는 재사용 가능한 승인 근거가 없으면 `AWAITING_USER_CONFIRMATION`이며 구현·위임·제품 변경을 시작하지 않는다.
- L0 오탈자·명백한 형식 수정·동일 검사 재실행은 인터뷰 예외다.

실행 reference: `skills/managing-project-intake-and-work-contract/references/first-prompt-direction-anchoring.md`.

## 5. Example as Fixture / Golden Set

예시는 삭제 대상이 아니라 검증 자산이다. 다만 인터페이스와 정본보다 높은 권위를 갖지 않는다.

```text
정상 Fixture
실패 Fixture
경계 Fixture
과거 회귀 Fixture
상충·불완전 입력 Fixture
고위험 권한 Fixture
```

- 예시는 “이 범위 안에서만 답하라”는 정답 틀이 아니다.
- Example을 줄일 때는 그 예시가 검출하던 실패를 다른 Fixture·Test·검증이 보존하는지 확인한다.
- Fixture가 현재 인터페이스와 충돌하면 인터페이스를 기준으로 갱신한다.
- Golden Set은 대표 입력과 기대 판정을 기록하되 실제 프로젝트 비밀·개인정보·권리 침해 자료를 넣지 않는다.

예시를 제거해 정상·실패·경계 행동을 검증할 수 없게 되면 간소화가 아니라 회귀다.

## 6. 결정 질문 중심 Context 큐레이션

Context는 자료량이 아니라 현재 바꿀 결정과 권위로 선별한다.

```yaml
decision_question:
include_criteria:
exclude_criteria:
authority_level:
freshness:
representation:
deduplication:
known_conflicts:
context_budget:
progressive_load_trigger:
refresh_trigger:
```

### 순서

```text
현재 결정 질문
→ 사용자 최신 지시
→ 프로젝트 규칙·승인 Decision
→ 분야 책임 원본
→ 실제 파일·테스트·렌더
→ 현재 Issue·Plan·PR
→ 필요한 외부 근거와 반대 근거
→ 중복·충돌·오래된 입력 정리
→ 자료 유형에 맞는 표현
→ 필요할 때만 추가 로드
```

### Include 기준

- 결과·범위·검증을 실제로 바꾸는 정본
- 현재 결정을 반증할 수 있는 반대 근거와 실패 사례
- 보호 대상·권한·호환성 규칙
- 실제 구현·테스트·사용자 체감 증거
- 현재 작업이 소비하는 Schema·인터페이스

### Exclude 기준

- 현재 결정과 연결되지 않은 대화 전문
- 같은 책임의 중복 복제본
- 대체된 구형본이 현행처럼 보이는 자료
- 출처·날짜·버전이 없고 결과를 바꾸지 않는 참고
- 다른 장르·플랫폼의 표면 기능만 유사한 사례

제외에는 이유와 재조회 조건을 기록한다. 관련 없다는 이유로 반대 근거·실패 사례·소수 사용자 장벽을 지우지 않는다.

### Freshness와 progressive load

- `progressive_load_trigger`: 특정 mode·도메인·실패가 발생할 때 추가 Reference를 읽는 조건
- `refresh_trigger`: 정본·Schema·가격·버전·Issue·실제 구현이 변해 자료를 다시 읽어야 하는 조건

Context budget은 임의 token 상한이 아니라 결정에 필요한 최소 권위와 검증 가능성을 유지하는 경계다.

## 7. 자료 유형별 표현

같은 내용을 무조건 장문 글로 변환하지 않는다.

| 자료 | 우선 표현 |
|---|---|
| 수치·비교·상태 | Schema·표·JSON·Fixture |
| 절차·의존성 | 단계·상태 머신·Plan |
| 화면·배치 | 화면 계약·와이어프레임·렌더 |
| 서술·근거 | 짧은 요약 + 원출처·한계 |
| 실제 동작 | 코드·데이터·테스트·캡처 |
| 결정 | Decision ID·선택·대체 관계·Commit |

표를 산문으로 풀어 쓰거나 산문을 억지로 표로 만들지 않는다. 표현 방식은 정보의 관계와 검증 방법에 맞춘다.

## 8. Artifact-first 전달과 주장 상한

설명만으로 원하는 결과를 전달하기 어렵다면 작업에 맞는 Artifact를 우선한다.

```text
UI → 화면 계약·와이어프레임·대표 상태·전후 렌더
데이터 → Schema·표·정상/실패 Fixture
작업 순서 → 의존성·Gate·롤백 Plan
Prompt → 입출력 계약·Eval Fixture
게임 기획 → 대표 상황·Vertical Slice·플레이테스트 계약
```

각 Artifact에는 증명하는 것과 증명하지 못하는 **주장 상한**을 둔다.

- 화면 이미지: 배치·계층 후보를 보여 주지만 입력 완결성·피로·성능을 증명하지 못한다.
- Schema: 구조를 검증하지만 실제 데이터 품질과 플레이 감각을 증명하지 못한다.
- 자동 Test: 계약 회귀를 검출하지만 사람 이해·실기기 접근성을 증명하지 못한다.
- AI 보고서: 가설과 분류를 제공하지만 공식 사실·구현 완료의 독립 권위가 아니다.

실행하지 않은 렌더·런타임·사람 검증·billing은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 남긴다.

## 9. Memory와 정본

AI Memory·대화 기억·요약은 다음을 돕는다.

- 반복 질문 방지
- 사용자 선호·작업 맥락 복원
- 다음 읽기 경로 압축

그러나 다음을 소유하지 않는다.

- 승인 Decision의 최종 상태
- 실제 구현·테스트 결과
- 프로젝트 기획 책임 원본
- 최신 Branch·Commit·PR 상태
- 가격·법·플랫폼 정책 같은 변동 사실

새 작업은 저장소 정본과 실제 상태를 다시 확인한다. 기억과 정본이 다르면 `CANON_CONFLICT`로 보고하고 자동으로 기억을 진실로 가정하지 않는다.

## 10. 검증 매트릭스

```yaml
authority_check:
first_prompt_anchor_alignment:
instruction_context_separation:
interface_completeness:
grill_me_alignment:
fixture_coverage:
context_relevance:
counterevidence_preserved:
deduplication:
freshness_and_refresh:
artifact_claim_limit:
actual_validation:
result: PASS | PARTIAL | FAIL | NOT_RUN | BLOCKED
```

검사한다.

- 강제 안전 규칙이 판단 공간으로 이동하지 않았는가
- direction anchor가 전체 Task·범위·출력과 일치하는가
- 앞 배치를 권한 상승으로 오해하지 않았는가
- Instruction과 Context가 구분되는가
- 사용자 결정이 기술 기본값으로 숨겨지지 않았는가
- 실행 전 Grill Me 확인 또는 유효한 승인 재사용이 있는가
- Example·Golden Set이 삭제되어 회귀 검출력이 사라지지 않았는가
- Context 큐레이션이 반대 근거를 제거하지 않았는가
- 중복 정본·과거 대화가 현재 권위를 차지하지 않는가
- Artifact가 실제 검증 범위를 과장하지 않는가
- 새로운 사실·버전·실패가 생겼을 때 refresh trigger가 있는가

## 11. 실패 조건

- 강한 규칙을 줄인다는 이유로 보안·권한·무결성 경계를 삭제함
- 프로젝트 코어·중요 UX를 `JUDGMENT_SPACE`로 위임함
- direction anchor가 뒤의 범위·제약·출력과 충돌함
- 앞 배치를 이유로 상위 권한을 무시함
- L1 이상 지시문을 Grill Me 확인 또는 유효한 승인 없이 실행함
- 기계적 작업에 불필요한 정석안·파격안·통합안을 강제함
- 입력·출력 계약 없이 예시만 늘림
- Example을 삭제하고 Fixture 검증을 대체하지 않음
- 관련 자료를 많이 넣는 것을 Context 품질로 오해함
- 반대 근거·실패 사례를 편향적으로 제외함
- AI Memory를 GitHub 정본보다 우선함
- 이미지·문서·자동 Test만으로 런타임·사람 이해를 완료 처리함
- 실행하지 않은 항목을 `PASSED`로 표시함
