# Local Bootstrap Capability Discovery Resilience Design

- 날짜: 2026-08-15
- 상태: `APPROVED_USER_DIRECTION`
- Tracking Issue: `#415`
- 대상: Base 공용 local bootstrap, 특히 Loop A2 Local Executor 설치/복구 경계

## 1. 문제

Windows Loop A2 Local Executor 설치 과정에서 실제 환경은 이미 다음 capability를 증명했다.

```text
gh auth status --hostname github.com -> authenticated
codex login status -> Logged in using ChatGPT
docker version -> client/server ready
```

그런데 첫 설치기는 `codex.exe`라는 특정 파일명만 존재하는지 검사했다. Windows에서는 `codex` 명령이 PATHEXT 또는 package-manager shim을 통해 `codex.cmd` 같은 다른 실행 진입점으로 제공될 수 있으므로, 실제 capability가 정상인데도 설치기가 `BLOCKED`로 오판했다.

후속 설치기에서는 중간 오류 때 창이 닫혀 사용자에게 진단 증거가 남지 않는 문제도 확인됐다.

## 2. 근본 원인

### 2.1 Capability와 packaging literal의 혼동

`codex login status` 성공이 실제 요구사항인데 `codex.exe` 존재 여부를 그보다 높은 gate로 사용했다. 발견용 heuristic이 capability authority를 대체한 것이다.

### 2.2 엄격해야 할 것과 유연해야 할 것의 미분리

엄격해야 하는 것은 repository/project identity, exact SHA/immutable evidence, trusted author/authority, ChatGPT-authenticated Codex, paid API/API-key fallback 금지, protected paths와 destructive-operation 금지다.

반면 executable suffix (`.exe`, `.cmd`, `.bat`), 현재 shell PATH 갱신 여부, package-manager shim 위치, trusted standard install location, launcher wrapper 형태는 환경별로 달라질 수 있다.

### 2.3 실패 진단 보존 부족

bootstrap은 사용자 PC의 환경 경계에서 실행되므로 CI보다 변수가 많다. 실패 시 창과 로그가 사라지면 root-cause 분류가 어려워지고 guess-and-fix 반복으로 이어진다.

## 3. 결정

새 Skill을 만들지 않는다. 광역 GPT–Codex 정책을 불필요하게 확대하지 않고, 실제 consumer/owner인 `docs/LOOP_A2_LOCAL_EXECUTOR.md`에 다음 두 원칙을 흡수한다. 기존 one-shot bootstrap 계약 테스트가 이 owner와 Learning Log를 함께 감시한다.

### `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION`

환경 의존 도구는 특정 파일명 하나를 요구하기 전에 신뢰 가능한 여러 discovery route를 순서대로 시도한다.

```text
required capability
→ current command resolution / PATHEXT
→ explicitly configured trusted executable path when present
→ known trusted standard install location when appropriate
→ semantic readiness probe
→ capability READY | bounded BLOCKED
```

예:

```text
BAD:  require codex.exe
GOOD: resolve `codex` using trusted Windows command semantics
      → accept trusted .exe/.cmd/.bat entry form
      → run `codex login status`
      → require exact ChatGPT-authenticated readiness result
```

Path 존재만으로 readiness를 PASS로 올리지 않는다. 가능한 경우 최종 판정은 실제 semantic readiness probe로 한다.

### `DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`

사용자 PC bootstrap은 실패 지점이 사라지지 않도록 최소 하나를 보장한다.

- 사용자가 닫기 전까지 유지되는 terminal failure state, 또는
- durable bounded diagnostic log / blocker code.

가능하면 둘 다 제공한다. token, credential, raw private file contents는 기록하지 않는다.

## 4. 유연성의 경계

“유연하게 찾는다”는 보안 완화를 의미하지 않는다.

허용:

- Windows command resolver/PATHEXT가 찾은 trusted executable/shim
- 승인된 configuration에 명시된 path
- Base가 아는 trusted standard install location
- 여러 trusted 후보 중 semantic probe를 통과한 후보

금지:

- 전체 디스크 arbitrary executable 탐색
- 이름만 같은 untrusted binary 자동 선택
- discovery 실패 후 임의 binary 자동 다운로드
- ChatGPT auth가 없을 때 API key/paid provider fallback
- reviewed Docker image가 없을 때 unpinned image 대체

즉 **discovery는 넓게, authority와 acceptance는 좁게** 유지한다.

## 5. 오류 처리

```text
candidate not found
→ try next trusted discovery route
→ routes exhausted
→ BLOCKED with stable reason

candidate found
→ semantic probe fails
→ do not pretend readiness
→ try another trusted candidate only when bounded ambiguity exists
→ otherwise BLOCKED with probe result class

bootstrap parser/process failure
→ keep diagnostic surface open and/or write bounded durable log
```

## 6. 사용자 경험 원칙

- 사용자가 이미 성공시킨 capability를 다시 설치하라고 요구하기 전에 현재 증거를 우선한다.
- 사용자가 폴더/실행파일 확장자를 알아야만 진행되는 설계를 피한다.
- 기본 Golden Path는 one-click/no-terminal 방향을 유지한다.
- failure는 재설치 지시보다 실제 실패 capability와 probe 결과를 먼저 제시한다.

## 7. 구현 범위

1. `docs/LOOP_A2_LOCAL_EXECUTOR.md`
   - 두 새 원칙, trusted multi-route discovery, strict acceptance, diagnostic preservation 경계.
2. `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`
   - 실제 실패 → 원인 → 해결 → 경계를 `OBSERVATION`으로 기록.
3. `tests/test_one_shot_local_executor_bootstrap_contract.py`
   - capability/diagnostic 규칙과 workflow coupling 회귀.
4. `.github/workflows/validate-one-shot-local-executor-bootstrap.yml`
   - owner/Learning Log/design/plan 변경도 focused contract를 trigger하도록 연결.
5. 이 spec과 대응 implementation plan/evidence.

새 Skill ID, Registry, A3, Scheduler, product scope, paid provider 변경은 없다.

## 8. TDD 검증

### RED 1 — 원칙 부재

- head: `a8ee9bcefb11baf03a5ec30393a6affc05b09267`
- workflow: `Validate One-Shot Local Executor Bootstrap`
- run: `31833180090`
- job: `94873467584`
- 결과: 기존 3개 contract PASS, 새 capability-discovery contract 1개만 FAIL.

### RED 2 — workflow consumer 누락

- head: `7655dbb8fd7f8f904233b6e1e3cb8def11a9fc6b`
- workflow run: `31833487469`
- job: `94874445902`
- 결과: capability/diagnostic 계약은 PASS, 새 workflow-coupling contract만 `docs/LOOP_A2_LOCAL_EXECUTOR.md` trigger 부재로 FAIL.

GREEN은 workflow coupling 구현 뒤 exact final head에서 요구한다.

## 9. 적대적 검토

- flexible discovery가 malicious executable 선택으로 확장되는가? → trusted routes만 허용하고 semantic probe를 요구한다.
- strict gate를 약화시키는가? → identity/SHA/auth/payment/protected-path gate는 유지한다.
- 모든 도구에 복잡한 resolver framework를 강제하는가? → 아니다. 실제 환경 변동성이 있는 local bootstrap에 최소 원칙만 둔다.
- 로그가 credential을 누출하는가? → bounded status/code 중심으로 제한한다.
- open/draft PR을 건드리는가? → 별도 branch의 독립 파일만 수정하며 진행 중 PR은 read-only다.

## 10. 기대 효과

```text
single literal assumption
→ false negative / 불필요한 재설치 / 반복 수정
```

을 다음으로 바꾼다.

```text
trusted multi-route discovery
→ real semantic capability probe
→ strict acceptance
→ preserved diagnostics
```

환경 차이를 흡수하면서 실제 권위·보안 조건은 더 명확하게 유지한다.
