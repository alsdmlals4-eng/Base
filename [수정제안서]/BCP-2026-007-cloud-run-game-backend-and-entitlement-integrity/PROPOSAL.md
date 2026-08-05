# BCP-2026-007 — Cloud Run 게임 백엔드·플랫폼 권한·무결성 보호 계약

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `48273f79ab261a1f064adfc7431c99a74a22c33a`
- 제출일: `2026-08-05`
- 상태: `SUBMITTED`
- 지식 상태: `패턴`
- 사용자 방향 승인: `2026-08-05 — 두 개의 Capability Pack을 기존 Skill에 흡수하는 권장안 승인`
- 안정적 승인 근거: `미확정 — 이 제안 PR의 사용자 검토 기록으로 확정 예정`
- 구현 PR: `없음`

## 관찰과 증거

사용자는 여러 Godot 게임 프로젝트에서 서버 기능이 필요해질 때 Cloud Run 구현 준비를 기본 검토 대상으로 삼고, 게임 배포 시 DRM·소유권·무결성 보호를 재사용 가능한 Base 구조로 관리하려 한다.

현재 Base는 다음 관련 책임을 이미 보유한다.

- `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`: 서버·저장·플랫폼·성능·출시 기술 기획
- `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`: 플랫폼 심사·권리·출시 증거
- `managing-game-project-operating-system`: 프로젝트 운영체계·Template 설치
- `designing-vertical-slices`: 대표 플레이·제작 파이프라인·목표 환경 검증
- `reviewing-and-validating-project-changes`: 계약·정적·런타임·성능·회귀 검증
- `running-adversarial-review-and-refinement`: 실패 가정·과잉 일반화·누락 공격
- `evolving-project-discipline-skills`: consolidation-first Skill 경계 판정

공식 기술 근거에서 확인된 핵심 사실:

### Cloud Run

- Cloud Run 서비스는 HTTPS·WebSocket·HTTP/2·gRPC를 지원한다.
- 인스턴스 파일 시스템은 일시적이며 영구 상태는 외부 데이터 저장소가 소유해야 한다.
- 기본 scale-to-zero는 비용을 줄이지만 첫 요청 지연을 만들 수 있다.
- WebSocket은 HTTP 요청으로 취급되어 요청 제한 시간의 영향을 받고, 클라이언트 재연결과 인스턴스 간 상태 동기화가 필요하다.
- session affinity는 best-effort이며 동일 인스턴스를 영구 보장하지 않는다.
- 서비스 간 호출은 IAM·서비스 계정·ID token과 최소 권한을 사용하고, 비밀은 Secret Manager를 사용한다.

공식 출처:

- https://docs.cloud.google.com/run/docs/overview/what-is-cloud-run
- https://docs.cloud.google.com/run/docs/triggering/websockets
- https://docs.cloud.google.com/run/docs/configuring/request-timeout
- https://docs.cloud.google.com/run/docs/configuring/session-affinity
- https://docs.cloud.google.com/run/docs/authenticating/service-to-service
- https://docs.cloud.google.com/run/docs/configuring/services/secrets

### 플랫폼 권한·무결성·DRM

- Steam DRM Wrapper는 소유권 확인과 Steamworks 기능 연결을 제공하지만 완전한 불법 복제 방지 수단이 아니다.
- Google Play Integrity는 앱·라이선스·기기·요청 무결성 신호를 제공하며, 백엔드가 결과를 검증하고 대응을 결정한다.
- Play Integrity 표준 요청은 `requestHash`로 중요한 요청 내용과 verdict를 결합할 수 있고 자동 replay 방지를 제공한다.
- 단일 무결성 신호를 절대적 진실로 취급하지 않고 복구 가능한 단계적 대응을 설계해야 한다.

공식 출처:

- https://partner.steamgames.com/doc/features/drm?l=koreana
- https://developer.android.com/google/play/integrity
- https://developer.android.com/google/play/integrity/overview
- https://developer.android.com/google/play/integrity/standard

증거 한계:

- 공식 문서는 현재 제품 기능과 권장 경계를 설명하지만 개별 프로젝트의 트래픽·비용·지연·보안·플랫폼 승인 결과를 증명하지 않는다.
- Cloud Run 실제 배포, 부하 테스트, 장애 복구, 플랫폼 SDK 통합과 합법 구매자 오탐 검증은 아직 실행하지 않았다.
- STOVE의 구체적인 권한·무결성 API는 구현 직전 공식 개발자 문서와 계약 화면에서 별도 재검증해야 한다.
- 이 제안은 법률 자문이나 완전한 불법 복제 방지 보증이 아니다.

## 일반화 후보

새 활성 Skill을 만들지 않고 두 개의 독립 Capability Pack을 기존 책임에 연결한다.

```text
Capability Pack A
GAME_BACKEND_CLOUD_RUN

Capability Pack B
GAME_ENTITLEMENT_INTEGRITY_AND_DRM
```

예정 공용 산출물:

```text
docs/knowledge/game-development/
├─ GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md
└─ GAME_ENTITLEMENT_INTEGRITY_AND_DRM_GUIDE.md

templates/project-operations/
├─ GAME_BACKEND_SERVICE_CONTRACT.md
└─ GAME_ENTITLEMENT_AND_INTEGRITY_RECORD.md
```

핵심 원칙:

```text
SERVER_FEATURE_DETECTED
→ CLOUD_RUN_DEFAULT_CANDIDATE
→ FIT_AND_RISK_ASSESSMENT
→ PROJECT_OWNED_SERVICE_CONTRACT
→ IMPLEMENTATION
→ STATIC / RUNTIME / LOAD / FAILURE / COST VALIDATION
```

```text
PLATFORM_NATIVE_FIRST
→ ENTITLEMENT_AND_INTEGRITY_SIGNALS
→ SERVER_AUTHORITY_FOR_HIGH_VALUE_STATE
→ REQUEST_BINDING_AND_REPLAY_CONTROL
→ TIERED_REMEDIATION
→ OFFLINE_AND_OUTAGE_POLICY
→ PLAYER_HARM_REVIEW
```

## Skill 경계 판정

### 새 활성 Skill을 만들지 않는 이유

Cloud Run과 DRM은 반복 가능한 전문 계약이지만 현재 실행 단계의 입력·산출물은 기존 기술 기획·프로젝트 운영·Vertical Slice·통합 검증 생명주기 안에서 처리할 수 있다.

- 요청·범위·완료 기준: `managing-project-intake-and-work-contract`
- 게임 시스템·서버 필요성·플레이어 가치: `analyzing-and-refining-game-concepts`
- 프로젝트 설치·책임 원본·운영체계: `managing-game-project-operating-system`
- 문서 정본·결정 추적: `managing-design-documents`
- 서버·플랫폼 SDK·외부 의존성 선택: `evaluating-godot-assets-and-plugins-before-creation`
- 대표 흐름·실제 배포·목표 환경: `designing-vertical-slices`
- 계약·보안·런타임·성능·비용·회귀: `reviewing-and-validating-project-changes`
- 실패 가정·오탐·비용 폭주·권위 위조 공격: `running-adversarial-review-and-refinement`
- 경로·Template·Guide 소비자 전파: `auditing-canonical-reference-freshness`

새 활성 Skill은 실제 프로젝트 Pilot에서 기존 라우팅이 반복적으로 실패하거나 독립 도구·승인·검증 경계가 입증될 때만 재검토한다.

## 적용 조건과 비사용 조건

### Cloud Run Capability Pack 사용

- 로그인·권한 확인 API
- 유저 프로필·클라우드 저장
- 리더보드·업적·비동기 보상
- 비동기 턴·매치 결과 제출
- 매치메이킹·로비·초대·상태 조회
- webhook·관리 API·예약 작업
- LLM·외부 AI API 중계와 비밀 키 보호
- WebSocket 기반 presence·soft realtime을 조건부 평가할 때

### Cloud Run Capability Pack 비사용 또는 별도 검토

- 낮은 지연의 고주파 authoritative tick server
- UDP 또는 고정 연결을 요구하는 실시간 액션 대전
- 인스턴스 로컬 상태에 의존하는 장기 세션
- 종료되지 않는 상시 worker를 서비스 요청 모델로 억지 구현
- 오프라인 전용 게임에 서버를 불필요하게 추가
- 트래픽·비용·데이터 책임·장애 정책을 정의하지 않은 상태

### 권한·무결성 Capability Pack 사용

- 유료 게임·DLC·후원 보상·계정 권한 확인
- 온라인 저장·리더보드·경쟁 보상·거래·재화 보호
- 플랫폼 서명·라이선스·앱 무결성 신호 연동
- 변조·재전송·중복 요청·클라이언트 위조 대응
- 오프라인 허용·grace period·복구·서비스 장애 정책 설계

### 권한·무결성 Capability Pack 비사용 또는 제한

- DRM을 완전한 복제 방지로 홍보하거나 보증
- 클라이언트 난독화만으로 서버 데이터 무결성을 보장
- 단일 신호만으로 영구 밴·저장 삭제·구매 차단
- 자체 암호화·라이선스 서버를 플랫폼 기본 기능보다 먼저 개발
- 비밀 키·판정 로직·권위 데이터가 게임 클라이언트에만 존재
- 플랫폼 정책·개인정보·오탐 복구를 확인하지 않은 구현

## 제안 설계

### 1. Cloud Run 기본 후보 Gate

프로젝트에서 서버 필요가 발견되면 즉시 구현하지 않고 다음 질문을 기록한다.

```yaml
player_value:
server_feature:
authoritative_state:
latency_and_tick_requirement:
connection_model:
expected_traffic_and_burst:
persistent_state_store:
identity_and_authentication:
idempotency_and_replay:
offline_behavior:
failure_and_retry:
cost_budget_and_alerts:
data_region_retention_privacy:
rollback_and_provider_exit:
```

판정:

- `CLOUD_RUN_RECOMMENDED`
- `CLOUD_RUN_CONDITIONAL`
- `ALTERNATIVE_ARCHITECTURE_REQUIRED`
- `SERVER_NOT_REQUIRED`
- `BLOCKED_UNVERIFIED`

### 2. Cloud Run 서비스 계약

Cloud Run을 선택한 프로젝트는 최소 다음 경계를 가진다.

```text
game client
→ authenticated API boundary
→ request validation and idempotency
→ domain service
→ external persistent datastore
→ event/task boundary
→ response and durable evidence
```

필수 규칙:

- 컨테이너 파일 시스템을 영구 저장소로 사용하지 않는다.
- 모든 고가치 mutation은 사용자·세션·요청·버전·idempotency key에 결합한다.
- 재시도 가능한 작업과 한 번만 실행해야 하는 작업을 분리한다.
- public endpoint와 private service-to-service endpoint를 분리한다.
- 서비스별 user-managed service account와 최소 권한을 사용한다.
- API key·LLM key·DB credential은 Secret Manager로 관리한다.
- max instances·concurrency·database connection·rate limit·quota·budget alert를 함께 설계한다.
- scale-to-zero·cold start·minimum instances의 비용과 지연을 측정한다.
- 로그에 토큰·개인정보·원문 AI 입력을 무분별하게 남기지 않는다.

### 3. 멀티플레이 분류

```text
ASYNC_OR_TURN_BASED
→ 기본 적합 후보

LOBBY_MATCHMAKING_PRESENCE
→ 일반 API 또는 조건부 WebSocket

SOFT_REALTIME
→ reconnect + external state + timeout + cost proof가 있을 때 조건부

AUTHORITATIVE_HIGH_FREQUENCY_REALTIME
→ Cloud Run 기본 후보에서 제외하고 별도 아키텍처 검토
```

WebSocket을 사용할 때:

- 최대 연결 지속 시간과 재연결 정책
- best-effort session affinity
- 여러 인스턴스 간 상태 동기화
- disconnect·duplicate·out-of-order 처리
- 연결 유지 비용과 minimum/maximum instance
- 장애 시 안전한 degraded mode

를 실제 테스트한다.

### 4. AI API 중계

Cloud Run이 LLM·외부 AI 호출을 중계할 때:

- 클라이언트에 provider key를 배포하지 않는다.
- 사용자 입력·저장 데이터·시스템 Prompt의 공개 범위를 분리한다.
- rate limit·quota·모델·추론 effort·비용 상한을 둔다.
- Prompt injection과 도구 권한을 별도 검증한다.
- 생성 결과를 게임 정본·보상·결제·징계의 단독 권위로 사용하지 않는다.
- provider 장애·timeout·안전 필터·비용 초과 fallback을 둔다.

모델·Prompt 비용 최적화는 `optimizing-ai-model-and-prompt-costs`의 기존 책임을 재사용한다.

### 5. 게임 DRM 재정의

Base에서 DRM은 다음 다층 보호를 포괄하는 약어로만 사용한다.

```text
platform entitlement
+ app/build integrity
+ request binding and replay control
+ server authority
+ optional tamper resistance
+ offline/outage/remediation policy
```

게임 보호 축:

```yaml
platform:
product_and_package_identity:
entitlement_source:
app_or_build_integrity_source:
request_binding:
replay_protection:
server_authoritative_state:
local_tamper_resistance:
offline_entitlement_cache:
grace_period:
revocation_and_recovery:
false_positive_remediation:
privacy_and_data_minimization:
service_sunset_and_save_access:
```

### 6. 플랫폼 우선 전략

```text
Steam
→ ownership + Steamworks value + optional wrapper
→ wrapper를 완전한 anti-piracy로 간주하지 않음

Google Play
→ app signing + licensing/integrity verdict
→ 중요한 요청을 requestHash/nonce와 결합
→ backend에서 검증·단계적 대응

STOVE
→ 공식 SDK·소유권·실행·정책 기능을 구현 직전 재검증
→ 확인되지 않은 기능을 Base 공통 사실로 가정하지 않음
```

자체 DRM은 다음 조건을 모두 만족해야 검토한다.

- 플랫폼 기본 보호로 해결되지 않는 구체적 위협이 있음
- 보호할 플레이어 가치와 운영 비용이 명확함
- 키 회전·장애·오프라인·고객 지원·서비스 종료를 운영할 수 있음
- 독립 보안 검토와 우회 가정을 포함함
- 합법 구매자 피해가 이익보다 크지 않음

기본 판정은 `NO_CUSTOM_DRM_DEFAULT`다.

### 7. 서버 권위

다음은 클라이언트 단독 판정을 금지한다.

- 경쟁 리더보드 점수
- 거래·유료 재화·후원 보상
- 온라인 인벤토리·소유권
- 업적 중 보상과 연계된 판정
- 비동기 대전 결과
- 계정 제재·영구 상태 변경

서버도 자동으로 신뢰할 수 있는 것은 아니다. 요청 바인딩, 데이터 제약, 중복 방지, 감사 기록과 rollback이 필요하다.

### 8. 단계적 대응

무결성 또는 권한 이상 신호에 대한 기본 대응:

```text
OBSERVE
→ LIMIT_NONCRITICAL_FEATURE
→ REQUEST_RETRY_OR_REAUTH
→ OFFER_PLATFORM_REMEDIATION
→ TEMPORARY_BLOCK_HIGH_VALUE_ACTION
→ MANUAL_OR_MULTI_SIGNAL_REVIEW
```

금지:

- 한 번의 네트워크 오류로 구매한 게임 전체 차단
- 단일 신호로 저장 삭제·영구 밴
- 복구 경로 없는 오프라인 금지
- 사용자에게 원인을 알리지 않는 무한 실패
- 로컬 세이브 접근을 DRM 장애와 함께 영구 상실

## 프로젝트 전용으로 남길 내용

Base에 고정하지 않는다.

- 프로젝트명·세계관·게임 모드·챔피언·전투 규칙
- 실제 API route·database schema·service name·region
- 로그인 공급자와 계정 연결 정책
- 리더보드 점수식·보상·업적 수치
- 트래픽·지연·가용성·비용 절대 목표
- 오프라인 허용 기간과 entitlement cache TTL
- 플랫폼별 SDK 버전·상품 ID·App ID·package name
- 비밀·서비스 계정·프로젝트 ID
- 특정 프로젝트의 Cloud Run 채택 여부
- 특정 프로젝트의 DRM 강도·오탐 허용도
- 실제 배포·부하·침투·플랫폼 제출 상태

## 반례와 위험

### MUST_FIX 후보

1. **Cloud Run 강제 편향**
   - 서버 기능이 있다는 이유만으로 Cloud Run을 고정하면 실시간 권위 서버·UDP·상시 worker 요구와 충돌한다.
   - 해결: `CLOUD_RUN_DEFAULT_CANDIDATE`, not mandatory.

2. **인스턴스 로컬 상태 오용**
   - scale-in·재시작·다중 인스턴스에서 세션과 저장이 소실될 수 있다.
   - 해결: 외부 영구 저장과 요청 단위 재구성.

3. **WebSocket 과장**
   - 지원 사실만으로 안정적인 실시간 권위 서버가 되지 않는다.
   - 해결: timeout·reconnect·external synchronization·비용 증거.

4. **비용 폭주와 연결 폭풍**
   - 재시도·WebSocket·AI 호출·DB 연결·악성 트래픽이 예상 비용을 초과할 수 있다.
   - 해결: quota·rate limit·backpressure·max instances·budget alert·load test.

5. **클라이언트 신뢰**
   - 점수·보상·소유권을 클라이언트가 결정하면 변조에 취약하다.
   - 해결: 서버 권위와 요청 바인딩.

6. **DRM 만능론**
   - 암호화·wrapper·난독화는 완전한 방지가 아니다.
   - 해결: 보호 목표·공격 비용·합법 사용자 가치와 다층 방어.

7. **오탐과 합법 구매자 피해**
   - 무결성 신호 오류·네트워크 장애·플랫폼 장애가 정상 사용자를 차단할 수 있다.
   - 해결: 다중 신호·단계적 대응·grace·remediation·support.

8. **비밀 유출**
   - 클라이언트, 로그, repository, 환경 변수에 장기 키를 노출할 수 있다.
   - 해결: Secret Manager·service identity·rotation·redaction.

9. **AI 중계 남용**
   - Prompt injection·PII·무제한 토큰·provider 장애가 게임 기능과 비용을 위협한다.
   - 해결: 최소 권한·입력 경계·quota·fallback·비권위 생성.

10. **플랫폼 차이 은폐**
    - Steam·Google Play·STOVE를 하나의 동일 DRM API로 추상화하면 권한·오프라인·복구 의미가 왜곡된다.
    - 해결: 공통 Record + 플랫폼 Adapter.

11. **서비스 종료와 소유권 손실**
    - 서버 종료가 싱글플레이·세이브 접근까지 파괴할 수 있다.
    - 해결: sunset·export·offline fallback·데이터 보존 계약.

12. **개인정보·지역 규정**
    - 로그인·기기 신호·로그·AI 입력·IP 주소가 불필요하게 수집될 수 있다.
    - 해결: 목적 제한·최소 수집·보존 기간·삭제·동의·공식 정책 재검증.

### 거절한 접근

- Cloud Run을 모든 서버 기능의 필수 구현으로 강제
- `cloud-run-game-backends`와 `game-drm`을 즉시 새 활성 Skill 두 개로 추가
- Cloud Run과 DRM을 하나의 광역 활성 Skill로 합침
- Base가 실제 공용 인증 서버·라이선스 서버·DRM 바이너리를 운영
- 클라이언트 난독화 또는 암호화만으로 서버 권위를 대체
- 특정 플랫폼 SDK 기능을 공식 확인 없이 공통 계약으로 확정

## 영향 범위와 검증

승인 후 별도 구현 PR의 예상 영향:

```text
docs/knowledge/game-development/
templates/project-operations/
README.md
START_HERE.md
docs/DOCUMENTATION_MAP.md
docs/OPERATING_MODEL.md
관련 기존 Skill reference/route
tests/
.github/workflows/validate-evidence-knowledge.yml
skills Learning Log
docs/CHANGELOG.md
```

보호 범위:

- `skills/SKILL_REGISTRY.json`의 활성 Skill 수·ID는 기본적으로 변경하지 않는다.
- released Base locks와 frozen derivatives를 변경하지 않는다.
- 실제 Google Cloud project·service·credential을 만들지 않는다.
- 실제 Steam·STOVE·Google Play App ID·키·상품을 만들지 않는다.
- 사용자 게임 프로젝트와 Google Sheets를 수정하지 않는다.

구현 검증 후보:

1. Guide·Template·라우팅 계약의 test-only RED.
2. Cloud Run 적합·조건부·부적합 fixture.
3. stateless storage·idempotency·retry·WebSocket·AI proxy 경계 fixture.
4. Steam ownership/DRM 한계와 Google Play Integrity backend verification fixture.
5. offline·outage·false-positive·service-sunset adversarial fixture.
6. 기존 Skill route와 Active Registry byte 보존 검사.
7. canonical reference freshness.
8. GitHub Actions exact-head 검증.
9. 실제 프로젝트 Pilot은 별도 승인 후 `NOT_RUN`에서 전환.

## 필요한 도구·파일·권한

- 필요 항목: Base 저장소 쓰기 권한
- 필요한 이유: 제안·설계·추후 승인된 공용 Guide·Template·Test 반영
- 설치·적용 방법: 별도 branch와 Draft PR 사용
- 설치 후 확인 명령: Base proposal validation, reference freshness, focused tests
- 최소 권한: 해당 branch push와 PR 생성 권한

추후 실제 프로젝트 Pilot에서만 필요:

- Google Cloud project와 billing account
- `gcloud` 인증과 최소 IAM
- Cloud Run·Artifact Registry·Secret Manager·선택 datastore 권한
- 목표 플랫폼 개발자 계정과 공식 SDK 접근
- 테스트용 App ID·package identity
- 실제 배포·부하·장애·비용 관찰 권한

이 제안 PR에는 위 클라우드·플랫폼 권한이 필요하지 않다.

## 승인과 구현

- 사용자 방향 승인: `권장안 A — 두 Capability Pack, 새 활성 Skill 없음`
- 안정적 구현 승인 근거: `미승인`
- 제안 PR: `이 문서를 포함하는 Draft PR`
- 구현 PR: `없음`
- 구현 시작 조건:
  1. 이 제안과 설계 문서 사용자 검토
  2. 제안 PR 병합
  3. 별도 상태 전환에서 `APPROVED_FOR_IMPLEMENTATION`
  4. 비어 있지 않은 GitHub `approval_ref`
  5. `writing-plans` 기반 구현 계획 승인
  6. 별도 TDD 구현 PR
- 롤백: 제안 전용 경로와 Registry 항목을 함께 되돌리며 활성 Base 동작은 변경되지 않는다.
