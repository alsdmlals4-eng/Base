# Prompt 캐싱·비용 측정 계약

## 목적

반복 Prompt의 안정된 부분만 cacheable prefix로 구성하고 현재 요청·프로젝트 상태·변동 수치는 dynamic suffix에 둔다. Cache hit 자체가 목표가 아니라 **요구 품질을 통과한 순비용 감소**가 목표다.

## Provider profile

가격·최소 token·TTL·할인율·context limit은 공급자와 시점에 따라 변한다.

```yaml
provider:
model_id:
verified_at:
official_source:
input_rate:
output_rate:
cache_write_rate:
cache_read_rate:
cache_minimum:
cache_ttl:
context_limit:
reasoning_options:
status: VERIFIED | STALE_RECHECK_REQUIRED | UNVERIFIED
```

- `verified_at`과 `official_source`가 없으면 `UNVERIFIED`다.
- 적용 시점이 달라졌거나 provider 정책이 바뀔 가능성이 있으면 `STALE_RECHECK_REQUIRED`다.
- 커뮤니티 절감률은 `ANECDOTAL_CASE`, 사용자 제공 수치는 확인 전 `USER_SUPPLIED_CLAIM`이다.

## Cacheable Prompt 구조

```yaml
stable_prefix:
  shared_rules:
  schemas:
  tool_contracts:
  invariant_examples:
dynamic_suffix:
  current_project_state:
  issue_and_goal:
  current_request:
  volatile_values:
excluded_sensitive_data:
refresh_trigger:
```

### `stable_prefix`

넣을 수 있는 후보:

- 반복되는 공용 역할·권한 경계
- 변하지 않는 출력 Schema와 도구 계약
- 안전 규칙과 승인된 불변조건
- 정상·실패·경계 Fixture 중 현재 계약에서 안정된 예시

넣지 않는 것:

- 현재 Branch·Commit·Issue 상태
- 자주 바뀌는 프로젝트 진행 정보
- 가격·가용 모델·날짜·실시간 데이터
- 사용자별 비밀·개인정보·token·cookie·API key
- 아직 승인되지 않은 기획과 임시 추정

### `dynamic_suffix`

- 현재 프로젝트 정본과 실제 파일 상태
- 이번 Issue·Goal·작업 계약
- 최신 사용자 요청과 변경 값
- 현재 날짜·버전·가격·가용성처럼 변동하는 정보
- 이번 실행의 실패·재시도·검증 결과

## 민감 정보 경계

다음은 cacheable 영역에 넣지 않는다.

```text
API key
access token
password
private key
cookie
recovery code
개인정보
프로젝트 비밀
변동 인증 정보
```

민감 정보를 제거하면 작업 자체가 불가능한 경우 캐싱을 포기하거나 안전한 참조 ID·권한 도구로 대체한다.

## 총비용 모델

```text
total_cost
= uncached_input
+ output
+ cache_write
+ cache_read
+ retries
+ higher_model_rework
+ validation
```

```yaml
estimated:
  input:
  output:
  cache_write:
  cache_read:
  retries:
  higher_model_rework:
  validation:
actual:
  provider_usage:
  billing_evidence:
  cache_hit:
  retry_count:
  rework:
  quality_result:
```

- cache read 비용이 낮아도 stale prefix 때문에 결과가 틀리면 순절감 실패다.
- 하위 모델 결과를 상위 모델이 전면 재작성하면 두 실행을 모두 비용에 포함한다.
- 실제 usage와 청구 근거가 없으면 절감률을 보장하지 않는다.

## Refresh trigger

다음 경우 stable prefix와 provider profile을 재검토한다.

- 공용 정책·Schema·도구 계약 변경
- Base 또는 프로젝트 정본 버전 변경
- 모델 ID·가격·context limit·cache 조건 변경
- 반복 실패·누락·재시도 증가
- 보안·개인정보·권한 경계 변경
- 예시가 현재 인터페이스와 불일치

Cache hit를 유지하려고 오래된 규칙을 보존하지 않는다.

## 검증

- stable_prefix와 dynamic_suffix의 변동성이 실제로 다른가
- 민감·변동 정보가 안정 접두부에 없는가
- provider profile이 공식 source와 확인일을 갖는가
- cache minimum·TTL·할인율이 영구 상수로 복제되지 않았는가
- 재시도·재작업·검증 비용이 순비용에 포함됐는가
- 결과가 품질·안전 Gate를 통과했는가
- 실제 billing을 실행하지 않았다면 `NOT_RUN`인가

## 실패 조건

- 민감 정보를 cache hit를 위해 반복 저장
- stale 규칙을 stable_prefix에 유지
- cache read 할인만 보고 총비용 절감을 주장
- provider 조건을 출처·확인일 없이 확정
- 재시도·상위 모델 재작업 비용 누락
- Fixture를 현재 계약보다 높은 권위로 사용
