# BCP-2026-007 — Cloud Run 게임 백엔드·플랫폼 권한·무결성 보호 계약

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 최초 제안 기준 커밋: `48273f79ab261a1f064adfc7431c99a74a22c33a`
- 제안 병합 커밋: `1b323b2e16cf1f1e27698a8e83496b767b6f06e3`
- 제출일: `2026-08-05`
- 상태: `IMPLEMENTED`
- 지식 상태: `패턴`
- 사용자 승인 근거: `https://github.com/alsdmlals4-eng/Base/pull/170#issuecomment-5192884554`
- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/179`, `https://github.com/alsdmlals4-eng/Base/pull/181`

이 문서와 `[수정제안서]/PROPOSAL_REGISTRY.json`이 BCP 생명주기 상태를 소유한다. 상세 설계는 같은 디렉터리의 `DESIGN.md`가 책임진다.

## 관찰과 증거

사용자는 여러 Godot 게임 프로젝트에서 서버 기능이 필요할 때 Cloud Run을 우선 검토 후보로 삼고, 게임 배포의 소유권·무결성·DRM 판단을 재사용 가능한 Base 구조로 관리하려 한다.

공식 문서에서 확인한 공용 경계는 다음과 같다.

- Cloud Run은 HTTPS·WebSocket·HTTP/2·gRPC를 지원하지만 인스턴스 메모리와 파일 시스템은 영구 상태의 정본이 아니다.
- WebSocket은 요청 제한 시간, 재연결, 여러 인스턴스 간 외부 상태 동기화와 연결 비용 검증이 필요하다.
- 서비스 간 호출은 IAM·서비스 계정·ID token과 최소 권한을 사용하고, 비밀은 Secret Manager 등 서버 측 경계에서 관리해야 한다.
- Steam DRM Wrapper는 완전한 불법 복제 방지 수단이 아니다.
- Google Play Integrity 신호는 백엔드에서 검증하고 중요한 요청에 결합해야 하며, 단일 verdict를 영구 제재의 단독 근거로 사용해서는 안 된다.

이 근거는 공용 설계 경계를 지원하지만 프로젝트별 지연·비용·부하·보안·플랫폼 승인·오탐률 또는 생산 준비도를 증명하지 않는다. Cloud Run 배포, 플랫폼 SDK 통합, 실제 부하·장애·비용·사람 복구 검증은 모두 `NOT_RUN`이다.

## 일반화 후보

새 활성 Skill을 추가하지 않고 두 개의 독립 Capability Pack을 기존 Base Skill 생명주기에 연결한다.

```text
A. GAME_BACKEND_CLOUD_RUN
B. GAME_ENTITLEMENT_INTEGRITY_AND_DRM
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

핵심 계약:

```text
SERVER_FEATURE_DETECTED
→ CLOUD_RUN_DEFAULT_CANDIDATE
→ FIT_AND_RISK_ASSESSMENT
→ PROJECT_OWNED_SERVICE_CONTRACT
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

실행 책임은 기존 요청 접수·게임 기획·프로젝트 운영·기술/출시·Vertical Slice·외부 의존성 평가·AI 비용·통합 검증·적대적 검토 Skill이 유지한다. 실제 프로젝트 데이터, 플랫폼 설정, 서비스와 SDK 코드는 프로젝트가 소유한다.

## 적용 조건과 비사용 조건

Cloud Run Capability Pack 사용 조건:

- 로그인·프로필·클라우드 저장·리더보드·업적·비동기 보상·턴제 결과 API
- webhook·관리 API·유한 비동기 작업·LLM 또는 외부 API 중계
- timeout·재연결·외부 상태·순서·비용 증거를 갖춘 조건부 WebSocket 또는 soft realtime

Cloud Run 기본 후보에서 제외하거나 별도 검토할 조건:

- 낮은 지연의 고주파 authoritative realtime, UDP, 고정 전용 서버 lifecycle
- 인스턴스 로컬 메모리나 임시 파일에 장기 세션·영구 상태 권위를 두는 구조
- 종료되지 않는 상시 worker를 요청 모델로 억지 구현하는 경우
- 서버가 필요하지 않은 오프라인 전용 기능

권한·무결성 Capability Pack 사용 조건:

- 유료 게임·DLC·후원 보상·온라인 저장·경쟁 점수·거래·재화·비동기 전투 결과 보호
- 플랫폼 소유권·서명·앱/빌드/요청 무결성 신호와 재전송 방지
- 오프라인 허용, grace period, 플랫폼·백엔드 장애, 계정·기기 복구, 환불·철회, 서비스 종료 정책

비사용 또는 제한 조건:

- DRM을 완전한 복제 방지로 홍보·보증
- 자체 라이선스 서버나 암호화를 플랫폼 기본 기능보다 먼저 개발
- 클라이언트 난독화나 단일 무결성 신호만으로 경쟁·결제 데이터를 보호
- 한 신호 실패를 영구 밴·구매 차단·저장 삭제로 직결
- 플랫폼별 의미를 확인하지 않고 Steam·Google Play·STOVE를 동일하게 취급

## 반례와 위험

- Cloud Run 지원 기능 목록만 보고 실시간 권위 서버 적합성을 과장할 수 있다.
- scale-to-zero, minimum instances, 동시 연결, DB connection, egress, 로그와 AI 호출이 비용 폭주를 만들 수 있다.
- retry와 중복 제출이 보상·점수·재화·거래를 중복 반영할 수 있다.
- 비밀 키·관리 route·판정 로직이 클라이언트나 로그에 노출될 수 있다.
- 하나의 공통 플랫폼 verdict로 정규화하면 플랫폼 고유 의미와 미지원 상태를 잃을 수 있다.
- DRM이 실제 위협보다 합법 구매자의 오프라인 플레이·세이브·접근성·모딩·지원 경험에 더 큰 피해를 줄 수 있다.
- 무결성·기기 신호의 과도한 수집과 보존이 개인정보 위험을 만들 수 있다.
- 서비스 종료 계획이 없으면 구매한 게임과 세이브 접근이 서버 수명에 종속될 수 있다.

MUST_FIX:

- `CLOUD_RUN_REQUIRED` 같은 무조건 강제 문구
- client-only authoritative paid/competitive state
- 비밀을 클라이언트·저장소·로그에 포함
- 보상 mutation의 idempotency·replay·transaction 누락
- max instances·rate limit·quota·budget·failure·rollback 누락
- 단일 integrity verdict를 영구 제재로 연결
- offline/outage·오탐 복구·지원/이의제기·서비스 종료·세이브 접근 결정 누락
- 공식 근거 없는 플랫폼 기능 주장

## 영향 범위와 검증

승인된 구현 범위:

- Cloud Run Guide 1개와 Backend Service Contract Template 1개
- Entitlement/Integrity/DRM Guide 1개와 프로젝트 Record Template 1개
- 기존 기술·출시·운영·Vertical Slice·외부 의존성·통합 검증·적대적 검토 경로 연결
- 전용 정적·계약·반례·reference freshness 테스트
- Learning Log·Changelog·Documentation Map·Knowledge Hub 동기화

보호 범위:

- `skills/SKILL_REGISTRY.json`과 활성 Skill 수
- `skills/BASE_SHARED_SKILL_ROUTES.json`
- released lock·snapshot·plugin·frozen derivative
- 사용자 프로젝트·Google Sheets·Cloud Run 리소스·플랫폼 계정·Secret
- 실제 플랫폼 SDK·프로젝트 API·DB Schema·트래픽·비용·플랫폼 ID

검증 순서:

1. Cloud Run Capability Pack을 별도 RED→GREEN 구현 PR로 완료·병합한다.
2. 최신 main과 공유 소비자를 재조회한다.
3. Entitlement/Integrity Capability Pack을 별도 RED→GREEN 구현 PR로 완료·병합한다.
4. 두 구현이 병합된 뒤에만 작은 생명주기 PR에서 `IMPLEMENTED` 전환 여부를 판정한다.
5. 실제 배포·플랫폼 sandbox·부하·비용·오탐 복구는 별도 프로젝트 Pilot 증거로 남긴다.

## 필요한 도구·파일·권한

### Base 정적 구현

- 필요 항목: Base 저장소 쓰기 권한, Python 3.12, 현재 publication 의존성, GitHub Actions
- 필요한 이유: Guide·Template·테스트·경로·reference freshness 구현과 검증
- 적용: 각 구현 계획의 TDD Task 순서
- 확인: focused tests, proposal checker, reference freshness, publication/generation, Base integrity, Required `ci-gate`
- 최소 권한: Base 브랜치와 PR 작성 권한

### 실제 프로젝트 Pilot

- 필요 항목: 대상 프로젝트 승인, Google Cloud 프로젝트·billing/budget alert, 최소 권한 서비스 계정, Secret Manager, staging 저장소, 플랫폼 sandbox 계정
- 필요한 이유: 실제 배포·권한·부하·장애·비용·플랫폼 무결성·복구 검증
- 적용: Base 구현과 분리된 프로젝트 계획·PR
- 확인: 배포 SHA, IAM policy, secret version, runtime/load/failure/cost evidence, 플랫폼 sandbox verdict, rollback·uninstall
- 최소 권한: 프로젝트별 필요한 서비스와 읽기/배포 권한만 허용

## 승인과 구현

- 사용자 승인 근거: `https://github.com/alsdmlals4-eng/Base/pull/170#issuecomment-5192884554`
- 제안 병합 PR: `https://github.com/alsdmlals4-eng/Base/pull/173`
- 제안 병합 커밋: `1b323b2e16cf1f1e27698a8e83496b767b6f06e3`
- 상태: `IMPLEMENTED`
- Cloud Run 구현 계획: `docs/superpowers/plans/2026-08-05-cloud-run-game-backend-capability-pack.md`
- 권한·무결성 구현 계획: `docs/superpowers/plans/2026-08-05-game-entitlement-integrity-drm-capability-pack.md`
- Cloud Run 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/179`
- Cloud Run 구현 병합 커밋: `dcc1a1bfa5f97a93351e2949e5aad04f06e9003d`
- 권한·무결성 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/181`
- 권한·무결성 구현 병합 커밋: `6ce0e5375f9ad1a0a56a337b7e4813f0296e3e0c`
- Base 정적 구현 완료 범위: Guide·Template·기존 owner route·전용 계약/반례 test·reference freshness·Learning Log·Changelog
- 생명주기 판정: `IMPLEMENTED`
- 활성 구현: `IMPLEMENTED_IN_BASE_STATIC_CONTRACTS`
- 실제 Cloud Run 배포: `NOT_RUN`
- Steam·Google Play·STOVE 실제 통합: `NOT_RUN`
- 부하·장애·비용·보안 검토: `NOT_RUN`
- 사람 오탐·복구 검증: `HUMAN_NOT_RUN`
- 법률 검토·플랫폼 승인: `NOT_PERFORMED`
- 롤백: 승인 상태와 두 계획 문서를 함께 되돌리면 활성 Base 동작은 바뀌지 않는다. 실제 구현은 각 별도 PR에서 독립적으로 되돌릴 수 있어야 한다.
