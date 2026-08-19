---
name: optimizing-ai-model-and-prompt-costs
description: Use when AI work needs model and reasoning-effort routing, cache boundaries, cost estimates, usage measurement, or quality-aware recalibration.
---

# AI 모델·추론·Prompt 비용 최적화

## 목적과 권한 경계

이 Skill은 AI 작업의 **요구 품질을 만족하는 최저 총비용**을 찾는다. 가장 싼 모델을 기본값으로 강제하지 않으며, 모델 하향으로 누락·재시도·상위 모델 전면 재작업이 늘면 비용 최적화 실패로 판정한다.

- Luna / Terra / Sol은 사용자가 이해하기 쉬운 논리적 작업 등급 또는 provider equivalent다. 실제 제품 surface에 그 이름의 모델이 존재한다는 뜻이 아니다.
- 모델명·가격·context limit·cache minimum·TTL·할인율·reasoning option은 `verified_at`과 `official_source`가 있는 provider profile에서만 확정한다.
- 이 Skill은 **실제 모델 설정을 변경하지 않는다**. 현재 응답 중 모델이 자동 교체됐다고 주장하지 않고, 검증 가능한 checkpoint에서 사용자가 설정을 변경한 뒤 다음 작업부터 적용한다.
- 프로젝트 코어·중요 기획·Prompt 요구 확정은 `managing-project-intake-and-work-contract`, Prompt·Context 구조는 `AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`, 결과 검증은 `reviewing-and-validating-project-changes`가 책임진다.
- Base의 현재 기본 유료 경로는 `GPT_PRO`다. 별도 사용자 승인 없이 API, credits, 새 SaaS, 새 subscription, 종량제 compute/storage 같은 추가 비용 경로를 비용 최적화라는 이유로 활성화하지 않는다.

## COST_SURFACE_GATE

모델이나 cache 비용을 계산하기 전에 **어떤 결제 surface를 쓰는 작업인지** 먼저 분류한다.

```text
SUBSCRIPTION_INCLUDED
SEPARATELY_METERED
UNVERIFIED_COST_SURFACE
COST_GATE_BLOCKED
```

### `SUBSCRIPTION_INCLUDED`

- 현재 승인된 `GPT_PRO` 플랜에 포함된 사용량 안에서 ChatGPT/Codex 등 승인 surface를 사용하는 경우.
- 여기서는 먼저 Context 축소, sparse Skill/Tool routing, 작업 분할, 재시도 감소로 효율을 높인다.
- 포함 사용량을 쓴다는 이유만으로 provider API 가격표나 prompt cache billing을 강제 계산하지 않는다.

### `SEPARATELY_METERED`

예:

- 구매형 credits 또는 auto top-up
- OpenAI/기타 provider API 사용량 과금
- 별도 유료 SaaS·runner·hosted compute/storage
- 기존 구독과 별개로 청구되는 기능

현재 Base의 `ZERO_INCREMENTAL_COST_REQUIRED` 아래에서는 **사용자 승인 전 기본 경로가 아니다**. 사용자가 명시적으로 승인한 경우에만 provider profile과 비용 추정을 진행한다.

### `UNVERIFIED_COST_SURFACE`

현재 기능이 구독 포함인지, credits/API/별도 요금인지 공식 근거로 확인하지 못했다면 비용을 0으로 추정하지 않는다. 최신 공식 source를 확인할 수 없으면 `COST_GATE_BLOCKED`로 종료한다.

### `COST_GATE_BLOCKED`

- 새 비용 경로가 필요하지만 사용자 승인이 없다.
- 공식 가격/가용성 근거가 없어 무료·포함 사용량이라고 보장할 수 없다.
- auto top-up·credits·API key 등 별도 결제 가능 surface를 우회적으로 켜야만 작업이 진행된다.

이 상태에서는 더 싼 provider를 찾아 자동 전환하지 않고, 승인된 포함 surface 또는 로컬/정적 대안을 먼저 찾는다.

## Skill Modes

- `route-model-and-effort`: 작업 난도·품질 위험·권한·실패 비용·재시도·재작업을 분류해 모델 등급과 추론 단계를 추천한다.
- `design-cacheable-prefix`: 반복 가능한 안정 접두부와 현재 작업의 변동 접미부를 분리하고 민감·변동 정보를 캐시 경계에서 제외한다.
- `estimate-cost`: 입력·출력·cache write·cache read·재시도·상위 모델 재작업 비용을 분리해 사전 추정한다.
- `measure-actual-usage`: provider usage·청구 근거·cache hit/miss·재시도·품질 결과를 기록한다.
- `recalibrate`: 실제 순비용과 품질 실패를 바탕으로 분류·승격·캐시 기준을 재조정한다.

필요한 mode만 순서대로 사용한다. 공급자 profile이나 실제 usage가 없으면 추정과 측정을 혼동하지 않는다. `SUBSCRIPTION_INCLUDED` 작업에는 별도 billing이 실제 결정에 필요하지 않으면 `estimate-cost`/`measure-actual-usage`를 억지로 호출하지 않는다.

## 사용 조건

- 사용자가 `[모델 추천]`이라고 말한다.
- 여러 모델·추론 단계 중 현재 작업에 맞는 조합을 선택해야 한다.
- 단순·대량, 일상·균형, 고난도 판단 작업을 서로 다른 모델 등급으로 라우팅한다.
- 반복되는 공용 규칙·Schema·도구 계약을 stable prefix로 구성하려 한다.
- 사용자 승인된 API·agent 작업의 비용을 품질 저하 없이 줄일 수 있는지 추정·측정·재보정한다.
- 현재 기능이 포함 사용량인지 별도 종량제인지 구분해야 안전한 실행 경로를 정할 수 있다.

## 비사용 조건

- 모델·추론 단계 선택권이 없는 단일 실행 환경이다.
- 한 번뿐인 짧은 요청으로 cache 설계 비용이 기대 이득보다 크다.
- 의료·법률·보안·릴리스처럼 검증 책임이 비용보다 우선하고 하향 모델 사용이 허용되지 않는다.
- provider의 공식 조건·usage·청구 근거를 확인할 수 없는데 특정 금액이나 절감률을 확정하려 한다.
- 비밀·개인정보·token·cookie·변동 인증 정보를 stable prefix에 넣어야만 cache hit가 가능한 구조다.
- 현재 `SUBSCRIPTION_INCLUDED` surface만으로 충분한데 API/credits 사용을 정당화하기 위해 비용 계산을 추가하려 한다.

## Required inputs

```yaml
work_package:
  goal:
  expected_artifacts:
  acceptance_criteria:
  quality_and_safety_risk:
  permission_and_tool_risk:
  retry_policy:
  current_checkpoint:
cost_surface: SUBSCRIPTION_INCLUDED | SEPARATELY_METERED | UNVERIFIED_COST_SURFACE
paid_path_approval:
available_model_profiles:
provider_profile_status:
reasoning_options:
prompt_structure:
actual_usage_and_billing:
quality_failures_and_rework:
```

## Read first

1. 승인된 작업 계약과 현재 checkpoint
2. 프로젝트 보안·품질·비용 경계
3. 현재 비용 surface와 사용자 승인 상태
4. `references/model-stack-routing.md`
5. cache 작업이면 `references/prompt-caching.md`
6. 변동 수치가 필요하면 해당 provider 공식 source와 확인일
7. 실제 측정이면 provider usage·청구 근거와 결과 품질

## Process

### 0. `COST_SURFACE_GATE`를 통과한다

```text
현재 승인된 구독 포함 사용량인가?
→ YES: SUBSCRIPTION_INCLUDED, 별도 과금 최적화 없이 품질/Context/재시도 효율부터 개선
→ NO/별도 결제 가능: SEPARATELY_METERED 여부와 사용자 승인 확인
→ 비용 상태 불명: UNVERIFIED_COST_SURFACE → 공식 source 확인
→ 승인/근거 없음: COST_GATE_BLOCKED
```

`GPT_PRO`가 존재한다는 사실은 credits, API, auto top-up 또는 다른 별도 과금 기능까지 승인한다는 뜻이 아니다.

### 1. 품질·위험을 먼저 분류한다

```text
작업 결과가 틀렸을 때 영향
→ 숨은 판단·권한·보안·호환성 위험
→ 독립 검증 가능성
→ 재시도와 상위 모델 재작업 비용
→ SIMPLE_BULK / ROUTINE_BALANCED / HIGH_RISK_REASONING
```

파일 수나 길이만으로 낮은 등급을 선택하지 않는다. 대량 작업 안에 구조·보안·데이터 의미 판단이 섞이면 분리하거나 상향한다.

### 2. `[모델 추천]` checkpoint

사용자가 `[모델 추천]`을 호출하면 다음 작업을 시작하기 전에 모델과 추론 단계를 제안한다. 사용자가 변경한 뒤 진행해야 하는 경우 현재 단계에서 중단한다.

```yaml
recommended_model: Luna | Terra | Sol | PROVIDER_EQUIVALENT
recommended_reasoning: LOW | MEDIUM | HIGH | PROVIDER_SUPPORTED_VALUE
classification: SIMPLE_BULK | ROUTINE_BALANCED | HIGH_RISK_REASONING
reason:
quality_risk:
retry_and_rework_risk:
next_checkpoint:
provider_profile_status: VERIFIED | STALE_RECHECK_REQUIRED | UNVERIFIED
cost_surface:
paid_path_approval:
continue_without_change_risk:
```

`recommended_model`과 `recommended_reasoning`은 사용 가능한 제품 옵션을 확인한 경우에만 구체 provider 값으로 변환한다.

### 3. Cache 경계를 설계한다

```text
stable_prefix
- 반복되는 공용 규칙
- 변하지 않는 Schema·출력 계약
- 안전한 도구 계약
- 안정된 Fixture

dynamic_suffix
- 현재 프로젝트 상태
- 현재 Issue·Goal
- 현재 요청과 변경 값
- 날짜·가격·가용 모델 같은 변동 정보
```

민감 정보와 변경 가능성이 높은 값을 stable prefix에 넣지 않는다. 오래된 접두부를 유지해 cache hit를 높이는 것은 최적화가 아니다. `SUBSCRIPTION_INCLUDED` surface에서 제품이 cache billing을 노출하지 않으면 가상의 cache 절감액을 계산하지 않는다.

### 4. 총비용을 추정·측정한다

```text
total_cost
= input
+ output
+ cache_write
+ cache_read
+ retries
+ higher_model_rework
+ validation
```

절감률은 `SEPARATELY_METERED`로 승인된 provider profile과 실제 usage가 있을 때만 계산한다. 커뮤니티 사례는 `ANECDOTAL_CASE`, 사용자 제공 수치는 확인 전 `USER_SUPPLIED_CLAIM`으로 둔다. 포함 구독 surface는 금액 환산보다 실패·재시도·컨텍스트 낭비 감소를 운영 지표로 사용할 수 있다.

### 5. 재보정한다

- 품질 통과·재시도 감소·순비용 감소: 유지 또는 확대
- 비용 감소지만 재작업 증가: 실패 또는 상향
- provider 조건 변경: `STALE_RECHECK_REQUIRED`
- 작업 경계가 불명확: 분할 후 다시 라우팅
- 고위험 조건 발견: 즉시 상향하고 기존 결과를 독립 검수
- 별도 비용 surface가 새로 필요해짐: `COST_SURFACE_GATE`로 되돌아가 승인 상태를 재확인

## Output contract

```yaml
mode:
cost_surface:
paid_path_approval:
model_recommendation:
provider_profile:
prompt_cache_boundary:
cost_estimate:
actual_usage:
quality_result:
retry_and_rework:
net_cost_result:
recalibration:
next_checkpoint:
verification_status: PASSED | PARTIAL | FAILED | NOT_RUN | BLOCKED
```

## Validation

- `COST_SURFACE_GATE`가 모델/가격 계산보다 먼저 실행됐는가
- `GPT_PRO` 포함 사용량과 credits/API/새 SaaS 같은 `SEPARATELY_METERED` 비용을 구분했는가
- 사용자 승인 없는 새 비용 경로를 자동 활성화하지 않았는가
- 추천 모델 등급이 작업 난도뿐 아니라 품질·안전·재작업 비용을 반영하는가
- 제품 surface에 없는 모델·추론 옵션을 단정하지 않았는가
- provider profile에 `verified_at`·`official_source`·상태가 있는가
- stable prefix와 dynamic suffix가 실제 변동성 기준으로 분리됐는가
- 비밀·개인정보·인증정보가 cacheable 영역에 없는가
- 절감률이 실제 usage와 품질 통과 뒤 계산됐는가
- 모델 하향으로 생긴 재작업이 총비용에 포함됐는가
- 실행하지 않은 billing·cache hit·절감 검증을 `NOT_RUN`으로 남겼는가

## Failure conditions

- 가장 싼 모델을 품질과 무관하게 선택함
- Luna / Terra / Sol을 실제 provider 모델 존재 증거로 사용함
- 고위험 작업을 분량이 많다는 이유로 단순 작업으로 분류함
- stale 가격·TTL·할인율을 공용 상수로 고정함
- 민감 정보를 stable prefix에 포함함
- cache hit를 위해 오래된 규칙을 유지함
- 실제 사용량 없이 절감률을 보장함
- 상위 모델 재작업과 검증 비용을 숨김
- 현재 응답의 모델을 이 Skill이 직접 변경했다고 주장함
- `GPT_PRO` 구독을 credits/API/auto top-up의 포괄 승인으로 해석함
- 사용자 승인 없는 `SEPARATELY_METERED` 경로를 비용 최적화 명목으로 호출함

References:

- `references/model-stack-routing.md`
- `references/prompt-caching.md`

Learning Log: `skills/SKILL_LEARNING_LOG.md`

## Cloud Run bounded AI proxy handoff

`docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`의 `bounded AI proxy`가 선택되면 모델·Prompt·cache·quota·rate limit·provider cost·budget fallback을 이 Skill이 검토한다. 이 경로가 실제 provider API 과금을 사용하면 `SEPARATELY_METERED`이며 현재 비용 정책상 별도 사용자 승인이 필요하다. LLM 출력은 결제·보상·제재·영구 저장의 단독 권위가 아니다.
