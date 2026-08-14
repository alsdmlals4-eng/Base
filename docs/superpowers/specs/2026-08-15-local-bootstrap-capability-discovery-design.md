# Local Bootstrap Capability Discovery Resilience Design

- 날짜: 2026-08-15
- 상태: `APPROVED_USER_DIRECTION`
- Tracking Issue: `#415`
- 대상: Base 공용 local bootstrap / GPT–Codex handoff policy

## 1. 문제

Windows Loop A2 Local Executor 설치 과정에서 실제 환경은 이미 다음 capability를 증명했다.

```text
gh auth status --hostname github.com -> authenticated
codex login status -> Logged in using ChatGPT
docker version -> client/server ready
```

그런데 첫 설치기는 `codex.exe`라는 특정 파일명만 존재하는지 검사했다. Windows에서는 `codex` 명령이 PATHEXT 또는 package-manager shim을 통해 `codex.cmd` 같은 다른 실행 진입점으로 제공될 수 있으므로, 실제 capability가 정상인데도 설치기가 `BLOCKED`로 오판했다.

다음 설치기에서는 중간 오류 때 창이 닫혀 사용자에게 진단 증거가 남지 않는 문제가 추가로 확인됐다.

## 2. 근본 원인

### 2.1 Capability와 packaging literal의 혼동

`codex login status` 성공이 실제 요구사항인데 `codex.exe` 존재 여부를 그보다 높은 gate로 사용했다. 발견용 heuristic이 capability authority를 대체한 것이다.

### 2.2 엄격해야 할 것과 유연해야 할 것의 미분리

다음은 엄격해야 한다.

- 승인된 repository / project identity
- exact SHA / immutable evidence
- trusted author / label / authority
- ChatGPT-authenticated Codex 요구
- paid OpenAI API / API-key fallback 금지
- protected paths / destructive operation 금지

반면 다음은 환경마다 달라질 수 있으므로 단일 literal을 강제하면 안 된다.

- executable suffix (`.exe`, `.cmd`, `.bat`)
- PATH가 갱신된 현재 shell 여부
- package-manager shim 위치
- trusted standard installation location
- launcher wrapper 형태

### 2.3 실패 진단 보존 부족

bootstrap은 사용자 PC의 환경 경계에서 실행되므로 CI보다 변수가 많다. 실패 시 창이 사라지거나 로그가 남지 않으면 원인 분류가 어려워지고 guess-and-fix 반복으로 이어진다.

## 3. 결정

새 Skill을 만들지 않는다. 기존 `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` / `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` 정책에 다음 두 원칙을 흡수한다.

### `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION`

환경 의존 도구는 특정 파일명 하나를 요구하기 전에 신뢰 가능한 여러 discovery route를 순서대로 시도한다.

```text
required capability
→ current command resolution / PATHEXT
→ configured trusted executable path if present
→ known trusted standard install locations when appropriate
→ semantic readiness probe
→ capability PASS | bounded BLOCKED
```

예:

```text
BAD:  require codex.exe
GOOD: resolve `codex` using current Windows command semantics
      → accept .exe/.cmd/.bat shim only from trusted resolution paths
      → run `codex login status`
      → require exact ChatGPT-authenticated readiness result
```

Path 존재만으로 readiness를 PASS로 올리지 않는다. 최종 판정은 가능한 경우 실제 semantic probe로 한다.

### `DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`

사용자 PC bootstrap은 실패 지점이 사라지지 않도록 최소 하나를 보장한다.

- 창을 사용자가 닫기 전까지 유지하는 failure mode, 또는
- durable bounded log / blocker code.

가능하면 둘 다 제공한다. token, credential, private file contents는 로그에 기록하지 않는다.

## 4. 유연성의 경계

“유연하게 찾는다”는 보안 완화를 의미하지 않는다.

허용:

- Windows command resolver가 찾은 executable/shim
- 승인된 configuration에 명시된 path
- Base가 아는 trusted standard install location
- 여러 후보 중 semantic probe를 통과한 후보

금지:

- 전체 디스크 arbitrary executable 탐색
- 이름만 같은 untrusted binary 자동 선택
- PATH 결과가 실패했다고 인터넷에서 임의 binary 다운로드
- ChatGPT auth가 없을 때 API key fallback
- Docker reviewed image가 없을 때 job execution 중 unpinned image 사용

즉 **discovery는 넓게, authority와 acceptance는 좁게** 유지한다.

## 5. 오류 처리

```text
candidate not found
→ try next trusted discovery route
→ all routes exhausted
→ BLOCKED with stable reason

candidate found
→ semantic probe fails
→ do not pretend readiness
→ try another trusted candidate only when ambiguity exists
→ otherwise BLOCKED with probe result class

bootstrap parser/process failure
→ keep diagnostic surface open and/or write bounded durable log
```

## 6. 사용자 경험 원칙

- 사용자가 이미 성공시킨 capability를 다시 설치하라고 요구하기 전에 현재 증거를 우선한다.
- 사용자가 폴더/실행파일 확장자를 알아야만 진행되는 설계를 피한다.
- 기본 Golden Path는 one-click/no-terminal 방향을 유지한다.
- failure는 “무엇을 다시 설치하세요”보다 “어떤 capability가 실제로 실패했는지”를 먼저 말한다.

## 7. 구현 범위

1. `docs/GPT_CODEX_WORKFLOW_POLICY.md`
   - 두 새 원칙과 discovery/diagnostic 경계 추가.
2. `skills/managing-project-intake-and-work-contract/LEARNING_LOG.md`
   - 이번 실제 실패 → 원인 → 해결 → 경계를 Observation으로 기록.
3. `tests/test_one_shot_local_executor_bootstrap_contract.py`
   - 기존 bootstrap contract에 회귀 요구 추가.
4. 이 spec과 대응 implementation plan.

새 Skill ID, Registry, A3, Scheduler, product scope, paid provider 변경은 없다.

## 8. 검증 기준

다음 문자열/의미가 공용 정책에 존재해야 한다.

```text
CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION
DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE
PATHEXT
semantic readiness probe
discovery는 넓게, authority와 acceptance는 좁게
```

계약 테스트는 `.exe` 한 종류만 고정하는 방식이 권장 규칙으로 추가되지 않았음을 확인하고, local bootstrap의 기존 destructive-operation 금지와 project-neutral 경계를 보존한다.

## 9. 적대적 검토

- 유연한 discovery가 malicious executable 선택으로 확장되는가? → trusted routes만 허용하고 semantic probe를 요구한다.
- strict gate를 약화시키는가? → identity/SHA/auth/payment/protected-path gate는 그대로 유지한다.
- 모든 도구마다 복잡한 resolver 프레임워크를 강제하는가? → 아니다. 환경 차이가 실제로 존재하는 도구에만 최소 다중 경로 discovery를 적용한다.
- 로그가 credential을 누출하는가? → bounded status/code 중심으로 제한한다.
- open/draft PR을 건드리는가? → 별도 branch에서 독립 파일만 수정한다.

## 10. 기대 효과

```text
single literal assumption
→ false negative / 재설치 요구 / 반복 수정
```

을 다음으로 바꾼다.

```text
trusted multi-route discovery
→ real capability probe
→ strict acceptance
→ preserved diagnostics
```

환경 차이를 흡수하면서도 실제 권위·보안 조건은 더 명확하게 유지한다.
