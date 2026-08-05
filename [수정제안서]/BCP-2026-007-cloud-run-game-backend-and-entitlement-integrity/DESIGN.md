# Cloud Run 게임 백엔드·플랫폼 권한·무결성 보호 설계

- 상태: `PROPOSED_DESIGN`
- 사용자 방향 승인: `2026-08-05 — Capability Pack A+B를 기존 Skill에 흡수`
- 기준 Base main: `48273f79ab261a1f064adfc7431c99a74a22c33a`
- Work Mode: `PLAN`
- BCP: `BCP-2026-007-cloud-run-game-backend-and-entitlement-integrity`
- 활성 Skill 추가: `NO`
- 활성 구현: `NOT_STARTED`
- Cloud Run 실제 배포: `NOT_RUN`
- 플랫폼 SDK 실제 통합: `NOT_RUN`
- 보안·부하·비용 Pilot: `NOT_RUN`
- 사람 오탐·복구 검증: `HUMAN_NOT_RUN`

## 1. 목적

게임 프로젝트가 온라인 기능이나 콘텐츠 보호가 필요해졌을 때 특정 공급자·DRM 제품부터 선택하지 않고 다음 순서로 판단하고 검증하게 한다.

```text
플레이어 가치와 보호 대상
→ 서버 또는 플랫폼 권한 필요성
→ 상태·지연·연결·보안·비용·오프라인 요구
→ Cloud Run 및 플랫폼 기본 기능 적합성
→ 프로젝트 책임 원본과 구현 계약
→ 최소 권한 구현
→ 정상·실패·경계·부하·비용·오탐 검증
→ 운영·복구·종료 계획
```

이 설계는 공용 서버나 공용 DRM 제품을 제공하지 않는다. Base는 판단·계약·증거 구조를 제공하고 실제 서비스·데이터·플랫폼 연동은 각 프로젝트가 소유한다.

## 2. 아키텍처 결정

### 선택한 구조

```text
기존 Base Skill owners
→ 선택형 Capability Pack Guide
→ 프로젝트 운영 Template
→ 프로젝트별 Adapter·정본·코드
→ 실제 Cloud Run·플랫폼 SDK
→ 검증 증거
```

Capability Pack:

```text
A. GAME_BACKEND_CLOUD_RUN
B. GAME_ENTITLEMENT_INTEGRITY_AND_DRM
```

### 선택 이유

- Cloud Run 서버 설계와 권한·무결성은 서로 다른 질문과 증거를 가진다.
- 그러나 현재 Base의 기술·운영·검증 Skill이 실행 생명주기를 이미 소유한다.
- 새 활성 Skill 두 개를 추가하면 라우팅·행동 평가·Learning Log·Registry 유지비가 증거보다 먼저 증가한다.
- 한 광역 Skill로 합치면 배포·비용·상태 경계와 플랫폼 소유권·오탐 경계가 섞인다.
- Guide+Template는 독립 계약을 유지하면서 기존 Skill의 권한을 보존한다.

## 3. 책임 배치

| 책임 | 소유자 |
|---|---|
| 서버 필요성·플레이어 가치·게임 규칙 영향 | `analyzing-and-refining-game-concepts` |
| 요청·범위·완료 기준·승인 | `managing-project-intake-and-work-contract` |
| 프로젝트 설치·정본·Adapter·상태 | `managing-game-project-operating-system` |
| 기획 정본·결정 기록 | `managing-design-documents` |
| SDK·서비스·라이브러리 채택 평가 | `evaluating-godot-assets-and-plugins-before-creation` |
| 대표 플레이·배포·목표 환경 | `designing-vertical-slices` |
| LLM 모델·Prompt·비용 | `optimizing-ai-model-and-prompt-costs` |
| 계약·정적·런타임·성능·비용·회귀 | `reviewing-and-validating-project-changes` |
| 위협·오탐·과잉 일반화·비용 폭주 | `running-adversarial-review-and-refinement` |
| 경로·ID·Template 소비자 전파 | `auditing-canonical-reference-freshness` |
| Base 제안 생명주기 | `managing-base-change-proposals` |

## 4. Capability Pack A — Cloud Run 게임 백엔드

### 4.1 적합성 분류

#### 기본 적합 후보

- REST/HTTPS API
- 로그인 토큰 검증과 권한 부여
- 프로필·설정·클라우드 저장
- 리더보드·업적·보상 기록
- 비동기 턴·매치 결과
- webhook·운영 도구·관리 API
- LLM·외부 AI API 중계
- 짧거나 명시적으로 종료되는 작업

#### 조건부 후보

- WebSocket presence
- lobby·invite·채팅
- soft realtime 상태
- 장기 스트리밍 응답
- 주기적 작업·비동기 pipeline

조건부 요구:

```yaml
request_timeout:
client_reconnect:
external_state_sync:
duplicate_and_ordering:
session_affinity_assumption: BEST_EFFORT_ONLY
minimum_instances:
maximum_instances:
connection_cost:
failure_degradation:
```

#### 기본 부적합 또는 별도 아키텍처

- 고주파 authoritative simulation
- 낮은 지연의 실시간 액션 전투
- UDP
- 로컬 메모리에 세션 권위를 유지해야 하는 구조
- 무기한 상시 process
- scale-to-zero와 충돌하는 polling worker
- 고정 서버 주소·전용 서버 lifecycle을 요구하는 기능

### 4.2 서비스 단위

각 서비스는 한 명확한 도메인 책임을 가진다.

예:

```text
identity-gateway
player-profile
cloud-save
leaderboard
achievement
async-match
ai-proxy
admin-webhook
```

소규모 프로젝트는 처음부터 microservice로 분할하지 않는다. 배포·권한·확장·장애 경계가 실제로 다를 때만 분리한다.

기본 권장:

```text
modular monolith service
+ external datastore
+ clear internal modules
+ future split seams
```

### 4.3 상태 소유

```text
static definitions
→ project canonical data

request-scoped state
→ Cloud Run request memory

durable player state
→ external database/storage

event/task state
→ task/event system + durable ledger

cache
→ replaceable external or in-memory optimization
```

인스턴스의 writable filesystem과 메모리는 정본이 아니다.

### 4.4 API 계약

모든 endpoint:

```yaml
operation_id:
actor_identity:
authorization_scope:
request_schema:
request_version:
resource_version_or_precondition:
idempotency_key:
rate_limit_class:
timeout_budget:
domain_result:
error_codes:
retry_policy:
audit_fields:
sensitive_log_redaction:
```

Mutation:

```text
authenticate
→ authorize
→ validate
→ bind request identity/version
→ check idempotency/replay
→ apply transaction
→ write durable result
→ return stable response
```

### 4.5 인증·권한

Cloud Run IAM은 서비스 호출 권한을 관리하지만 게임 최종 사용자 계정 모델을 자동 제공하지 않는다.

분리:

```text
service identity
→ Cloud Run IAM and service account

end-user identity
→ chosen identity provider and project account model

domain authorization
→ project-owned rules
```

- private service는 IAM invoker를 사용한다.
- service-to-service는 user-managed service account와 ID token을 사용한다.
- end-user token은 issuer·audience·expiry·revocation·account link를 검증한다.
- 관리자 route는 일반 게임 client route와 분리한다.

### 4.6 비밀

- API key·DB password·certificate를 저장소·Godot export·client에 넣지 않는다.
- Secret Manager를 사용한다.
- 환경 변수로 주입할 때는 버전 pin과 rotation 동작을 정의한다.
- 로그·exception·trace에 비밀이 노출되지 않도록 redaction한다.
- 개발·staging·production secret을 분리한다.

### 4.7 비동기 작업

선택:

```text
one-to-one delayed/retry
→ Cloud Tasks candidate

fan-out/event
→ Pub/Sub candidate

schedule
→ Cloud Scheduler candidate

long-running finite batch
→ Cloud Run Job candidate
```

각 작업은 durable identity, idempotency, retry limit, dead-letter 또는 manual recovery를 가진다.

### 4.8 WebSocket

Cloud Run 지원을 사용 가능 판정으로만 해석하지 않는다.

필수 시나리오:

1. 정상 연결과 종료
2. 요청 timeout 직전 재연결
3. 다른 인스턴스로 재연결
4. 중복 message
5. 순서 역전
6. 인스턴스 종료
7. 외부 state store 지연
8. 대량 동시 연결
9. quota·max instance 도달
10. 비용 예산 초과

authoritative game state가 한 연결·한 인스턴스 메모리에만 있으면 실패다.

### 4.9 비용·용량

```yaml
traffic_assumptions:
peak_rps:
concurrent_connections:
request_duration:
cpu_memory:
min_instances:
max_instances:
concurrency:
egress:
datastore_calls:
ai_provider_calls:
logging_volume:
budget_alert:
load_test_result:
cost_per_active_user_or_match:
```

예상치와 실제 관찰을 분리한다. 무료 구간을 제품 영구 비용 보장으로 취급하지 않는다.

### 4.10 AI proxy

```text
game client
→ bounded game intent
→ Cloud Run policy and quota
→ provider request
→ output validation
→ safe game response
```

금지:

- provider key를 client에 포함
- 무제한 자유 Prompt를 곧바로 고권한 tool에 연결
- LLM 출력으로 결제·보상·밴·영구 저장을 단독 결정
- 개인정보를 목적·보존 정책 없이 provider에 전송
- provider 실패 시 게임 진행 전체가 영구 차단

## 5. Capability Pack B — 권한·무결성·DRM

### 5.1 용어

```text
entitlement
= 사용자가 제품·DLC·기능을 사용할 권리

integrity
= 앱·빌드·기기·요청이 기대한 상태인지에 대한 신호

DRM
= entitlement, integrity, 실행 제어, optional tamper resistance의 포괄적 실무 용어
```

DRM은 완전한 복제 방지 보장이 아니다.

### 5.2 신뢰 계층

```text
Tier 0: client claim
Tier 1: platform entitlement signal
Tier 2: app/build integrity signal
Tier 3: request-bound integrity/replay protection
Tier 4: server-authoritative domain validation
Tier 5: audit, anomaly, human/multi-signal review
```

고가치 행동은 가능한 높은 계층을 사용하되 플레이어 피해와 비용을 함께 평가한다.

### 5.3 플랫폼 Adapter

공통 interface 예:

```yaml
platform:
account_identity:
product_identity:
package_or_app_identity:
entitlement_verdict:
app_integrity_verdict:
device_or_environment_verdict:
request_binding:
issued_at:
expiry:
replay_status:
raw_signal_storage_policy:
normalized_decision:
remediation_options:
```

공통 interface는 원본 신호를 평준화해 잃지 않는다. 플랫폼별 의미와 미지원 상태를 보존한다.

### 5.4 Steam

- Steam ownership과 실행 환경을 확인한다.
- DRM Wrapper는 선택적 얕은 보호와 Steam 실행 연결이다.
- Wrapper 제거 가능성을 전제로 한다.
- Steamworks의 온라인 기능·업적·리더보드 등 합법 사용자 가치를 강화한다.
- 오프라인 모드·가족 공유·환불·계정 전환 등 실제 정책은 출시 직전 재검증한다.
- 제3자 DRM 추가는 사용자 피해·지원·호환성·비용 검토를 통과해야 한다.

### 5.5 Google Play

- Play App Signing과 Play Integrity 적용 가능성을 검토한다.
- 중요한 요청은 `requestHash` 또는 해당 공식 binding 방식에 결합한다.
- encrypted token은 backend에서 공식 절차로 decode·verify한다.
- `accountDetails`, app integrity, device/environment 신호를 용도에 맞게 사용한다.
- standard request의 replay 보호와 quota·오류·remediation을 검증한다.
- 한 verdict 실패를 영구 제재로 직결하지 않는다.

### 5.6 STOVE와 기타 플랫폼

- 공식 SDK·소유권·실행·오프라인·복구 기능을 구현 직전 확인한다.
- 확인하지 않은 기능을 Steam·Google Play와 동일하다고 가정하지 않는다.
- Base는 `PLATFORM_CAPABILITY_UNVERIFIED` 상태를 허용한다.
- 플랫폼 Adapter가 없으면 custom fallback 전에 보호할 실제 위협과 사용자 피해를 비교한다.

### 5.7 서버 권위

서버 권위 대상:

```text
purchase-linked entitlement
currency and trade
competitive score and rank
reward-bearing achievement
async battle result
online inventory
account sanction
limited event claim
```

검증 요소:

```yaml
authoritative_input:
server_recomputation:
allowed_ranges:
resource_version:
transaction:
double_spend_guard:
idempotency:
replay_guard:
audit_record:
rollback:
appeal_or_support:
```

### 5.8 로컬 보호

가능한 보조 수단:

- binary signing
- export/package encryption where supported
- obfuscation
- integrity check
- save checksum or signature
- debugger/tamper detection

원칙:

- client-side secret는 추출 가능하다고 가정한다.
- 로컬 보호는 공격 비용을 높이는 보조 수단이다.
- 싱글플레이 modding·접근성·성능·crash·지원 비용과 충돌을 평가한다.
- 로컬 세이브 변조가 타인·경제·경쟁에 영향을 주지 않으면 과도한 DRM을 피한다.

### 5.9 오프라인·장애·서비스 종료

필수 결정:

```yaml
offline_play_allowed:
first_launch_online_required:
cached_entitlement:
cache_ttl:
clock_tamper_handling:
grace_period:
platform_outage:
backend_outage:
account_recovery:
device_change:
refund_or_revocation:
save_export:
sunset_mode:
support_and_appeal:
```

기본 원칙:

- 이미 합법적으로 사용 중인 싱글플레이를 일시적 서버 장애로 즉시 영구 차단하지 않는다.
- 오프라인 grace는 프로젝트 위험에 맞춰 정의한다.
- 서비스 종료 시 가능한 범위에서 offline fallback 또는 데이터 export를 계획한다.
- 고가치 온라인 mutation은 outage 중 queue·read-only·temporary block 중 하나로 명시한다.

### 5.10 단계적 대응

```text
signal unavailable
→ retry/backoff or degraded mode

weak anomaly
→ telemetry + low-risk limits

entitlement mismatch
→ reauth/platform remediation

request binding mismatch
→ reject high-value mutation, preserve account/save

repeated multi-signal abuse
→ temporary restriction + review

confirmed severe abuse
→ project policy action + appeal/support evidence
```

## 6. 프로젝트 Template 계약

### GAME_BACKEND_SERVICE_CONTRACT

```md
## Player value and server feature
## Fit decision and rejected alternatives
## Authority and persistent state
## API and request lifecycle
## Identity and authorization
## Data model and migration
## Idempotency, replay, transaction, and retry
## Realtime and connection model
## Async tasks and events
## AI proxy and provider limits
## Secrets and service identity
## Privacy, retention, and region
## Capacity, cost, quota, and alerts
## Failure, degradation, backup, and rollback
## Runtime, load, failure, and cost evidence
## Current readiness and remaining gates
```

### GAME_ENTITLEMENT_AND_INTEGRITY_RECORD

```md
## Platform and product identity
## Protected player value
## Threat and abuse model
## Entitlement source
## App/build integrity source
## Request binding and replay protection
## Server-authoritative state
## Local tamper resistance
## Offline, outage, and grace policy
## False-positive remediation
## Privacy and signal retention
## Service sunset and save access
## Platform-specific evidence
## Adversarial findings
## Current readiness and remaining gates
```

## 7. 상태 모델

```text
NOT_REQUIRED
→ CANDIDATE
→ SELECTED
→ CONFIGURED
→ STATIC_VERIFIED
→ RUNTIME_VERIFIED
→ LOAD_AND_FAILURE_VERIFIED
→ HUMAN_RECOVERY_VERIFIED
→ PRODUCTION_READY
```

규칙:

- 단계 건너뛰기 금지.
- 문서 존재는 `CONFIGURED` 또는 Runtime 통과를 뜻하지 않는다.
- CI는 실제 플랫폼 entitlement·Cloud Run 부하·사람 오탐 복구를 대신하지 않는다.
- `PRODUCTION_READY`는 프로젝트별 실제 증거만 선언한다.

## 8. 오류·복구 계약

공통 machine-readable 분류 후보:

```text
AUTHENTICATION_REQUIRED
AUTHORIZATION_DENIED
ENTITLEMENT_UNVERIFIED
PLATFORM_SIGNAL_UNAVAILABLE
APP_INTEGRITY_MISMATCH
REQUEST_BINDING_MISMATCH
REPLAY_DETECTED
VERSION_CONFLICT
RATE_LIMITED
DEPENDENCY_UNAVAILABLE
TIMEOUT
DURABLE_WRITE_FAILED
IDEMPOTENT_REPLAY
COST_GUARD_TRIGGERED
DEGRADED_READ_ONLY
BLOCKED_UNVERIFIED
```

사용자 메시지는 내부 보안 세부를 노출하지 않으면서 복구 행동을 제공한다.

## 9. 검증 설계

### 정적

- Guide와 Template 필수 섹션
- 기존 Skill route와 ownership
- 활성 Skill Registry byte 보존
- 공식 출처·확인일
- 금지된 절대 보장 문구
- project-specific secret·ID 부재

### 계약 fixture

1. 비동기 리더보드 API — Cloud Run recommended
2. 턴제 비동기 전투 — Cloud Run recommended
3. WebSocket lobby — conditional
4. 60Hz authoritative action battle — alternative required
5. LLM quest proxy — bounded conditional
6. Steam single-player entitlement — platform-native, graceful offline
7. Google Play score submit — request-bound backend verification
8. single-signal false positive — permanent ban prohibited
9. provider outage — degraded/read-only recovery
10. service sunset — save/export/offline decision required

### Runtime Pilot

별도 승인된 실제 프로젝트에서:

- local emulator or staging
- Cloud Run deploy
- auth and least privilege
- datastore persistence across instance restart
- idempotent retry and double-submit
- WebSocket reconnect where applicable
- load and connection storm
- dependency outage
- cost observation
- platform sandbox entitlement/integrity
- offline and remediation
- logs and secret leakage
- rollback and uninstall

## 10. 적대적 검토

### 공격 질문

- 서버가 정말 필요한가?
- Cloud Run이 아니라 더 단순한 플랫폼 기능·로컬 저장으로 충분한가?
- Cloud Run의 scale-to-zero와 session model이 플레이 요구를 깨뜨리는가?
- 한 인스턴스 장애가 게임 상태를 잃게 하는가?
- 재시도가 중복 보상·재화·점수를 만드는가?
- AI 호출이 비용·개인정보·Prompt injection 위험을 만드는가?
- DRM이 실제 위협보다 합법 사용자에게 더 큰 피해를 주는가?
- 플랫폼 신호가 unavailable일 때 안전하고 공정하게 복구되는가?
- 서버 종료 뒤 구매한 게임과 세이브에 접근할 수 있는가?
- 한 공급자에 묶여 migration이 불가능한가?
- 로그·분석·무결성 신호가 과도한 개인정보 수집이 되는가?

### 승인 전 MUST_FIX

- `CLOUD_RUN_REQUIRED` 같은 무조건 강제 문구
- client-only authoritative competitive state
- permanent secret in client/repository
- single integrity verdict → permanent ban
- no offline/outage policy
- no idempotency/replay policy for reward mutation
- no cost/maximum instance/rate limit guard
- no service sunset/save access decision
- platform capability asserted without official evidence

## 11. 구현 분해

제안 승인 뒤 계획은 최소 다음 Task로 분해한다.

1. test-only RED for Guide·Template·route.
2. Cloud Run Guide.
3. Backend Service Contract Template.
4. Entitlement/Integrity Guide.
5. Entitlement/Integrity Record Template.
6. Existing entrypoint·Documentation Map·technical/release Guide routes.
7. Static and adversarial fixtures.
8. Learning Log·Changelog·reference freshness.
9. Exact-head CI and protected-boundary review.
10. Optional real-project Pilot as separate approval scope.

## 12. 완료 기준

제안 단계 완료:

- BCP Registry와 Proposal·Design이 연결됨
- 기존 책임과 새 Capability Pack 경계가 명확함
- 공식 근거·반례·비사용·위험·롤백이 기록됨
- placeholder·모순·범위 확대 없음
- 활성 Skill·Registry·Template·Test·project가 변경되지 않음
- 사용자 written-spec review 대기 상태

구현 단계 완료는 이 설계의 승인이 아니라 별도 계획과 TDD 증거로 판정한다.
