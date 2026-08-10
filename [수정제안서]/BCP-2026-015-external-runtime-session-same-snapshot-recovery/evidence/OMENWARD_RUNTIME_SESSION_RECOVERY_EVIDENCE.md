# OMENWARD Runtime Session Recovery Evidence

## 역할

이 파일은 `BCP - OMENWARD`의 project-specific evidence다.

Canonical proposal:

`[수정제안서]/BCP-2026-015-external-runtime-session-same-snapshot-recovery/PROPOSAL.md`

Base 공용 규칙은 proposal이 소유하고, 아래 PID·port·PR·Issue·Godot 버전 등 OMENWARD 전용 값은 evidence에만 남긴다.

## 출처

```yaml
project: alsdmlals4-eng/omenward
decision: OMW-DEC-20260809-PLANNING-BARRACKS-ROLE-OUTPUT-RUNTIME-IMPLEMENTATION-PACKAGE-V1
runtime_pr: 175
followup_issue: 176
runtime_head_at_proposal: bde85549560fca90f7aa25fc4842bc0a3afb92e7
godot_version: 4.7.1.stable.official.a13da4feb
observation_date: 2026-08-10
```

## 관찰 lineage

OMENWARD runtime package를 재개하기 위해 exact Godot 4.7.1 process와 Godot-AI session을 확인했다.

확인된 한 시점의 process/transport evidence:

```text
OMENWARD console PID = 10512
OMENWARD GUI PID = 29616
project root = C:\Users\user\Documents\GitHub\Ninza\omenward
GUI PID29616 = alive during bounded observation
GUI PID29616 -> WS9500 = ESTABLISHED
Godot stdout = Godot AI / GUT / OMENWARD loaded
Godot stderr = empty during observed window
```

그 뒤 별도의 `session_manage(op=list)` 관측에서는 다음 하나만 반환됐다.

```text
registered session = task7-circuit-placement-screen@63aa
project = GRIMOIRE
editor PID = 16652
Godot = 4.7.1
OMENWARD session = absent
```

중요한 점은 두 증거가 **같은 snapshot이 아니었다**는 것이다. process/WS 증거와 registry list 사이에 시간이 있었으므로 다음은 증명되지 않았다.

```text
PID29616 alive now
AND PID29616 owns WS9500 now
AND same Godot-AI server registry omits OMENWARD now
```

따라서 당시 안전한 판정은 다음이었다.

```text
RECOVERABLE_HIGODOT_REGISTRY_OMISSION_AFTER_RECENT_LIVE_WS
SAME_SERVER_HANDSHAKE_REGISTRATION_FAILURE = UNVERIFIED
```

## 다음 진단으로 좁힌 절차

전체 Issue #176 executor를 다시 실행하기 전에 하나의 짧은 관측창에서 다음을 묶도록 했다.

1. current exact OMENWARD Godot process + command line
2. 해당 current process의 ESTABLISHED WS9500
3. 최근 Godot-AI connection / handshake / auth / 4003 / reconnect / session log
4. 즉시 `session_manage(op=list)`

판정:

```text
LIVE_EXACT_OMENWARD + WS9500 + REGISTRY_OMISSION
=> RECOVERABLE_HIGODOT_SAME_SERVER_HANDSHAKE_REGISTRATION_BLOCKER

PROCESS_OR_WS_MISSING
=> current process/transport blocker
=> reason remains UNVERIFIED until evidence exists

EXACT_OMENWARD_SESSION_PRESENT
=> blocker self-recovered
=> fresh-read PR175 truth
=> resume Issue176 executor
```

## Shared server 보호가 필요했던 이유

Godot-AI server에는 OMENWARD 외 프로젝트가 연결되어 있었다. 따라서 OMENWARD session omission 하나만으로 shared server나 unrelated Editor를 종료하면 다른 프로젝트 작업을 손상할 수 있었다.

보호 규칙:

```text
DO NOT kill shared Godot-AI server for one missing target session
DO NOT kill unrelated GRIMOIRE/other project editors
DO NOT send OMENWARD mutation to a different registered project session
DO NOT patch executor/session matching before root-cause evidence
```

## Process 종료 표현 경계

이후 특정 과거 PID가 보이지 않는 상황이 생기더라도 다음처럼만 기록한다.

```text
process exited or is no longer running
reason = UNVERIFIED
```

증거 없이 `crashed`, `was killed`, `timed out` 같은 원인을 확정하지 않는다.

## Runtime package와 분리되는 증거 ceiling

이 recovery evidence는 OMENWARD 제품 기능 완료 증거가 아니다.

PR #175의 non-Godot transition CI는 exact head `bde85549...`에서 11 SUCCESS / 0 FAILURE까지 정리됐지만, Issue #176의 일곱 runtime/fixture gap은 그대로 남아 있다.

```text
1. Priest encouragement timing/events/support uptime
2. deterministic support-role fallback
3. flying priority != universal target permission
4. cluster density tie-break lane order/unit-id
5. Giant FRONTLINE_SURVIVAL_TIME + STRUCTURE_DAMAGE collectors
6. deterministic FV-PRIEST/MAGE/FLIER/GIANT/COMMON fixtures
7. true TARGETS_HIT_PER_CAST multi-cast semantics
```

따라서:

```text
SESSION_RECOVERY_GREEN != RUNTIME_PACKAGE_GREEN
```

세션 복구 뒤에도 GUT, Godot import, regression, deterministic fixtures, Hera source-delta, exact-head CI, review gate를 별도로 통과해야 한다.

## Base에 일반화하지 않을 값

- OMENWARD PR #175 / Issue #176 번호
- PID 10512 / 29616 / 16652
- WS9500 자체
- `task7-circuit-placement-screen@63aa`
- OMENWARD local Windows path
- barracks role-output 기능 내용
- FV metric 이름과 provisional numerics

Base에 일반화할 대상은 **같은 시점의 process/transport/log/registry 증거, fail-closed 분류, shared-session 보호, stale identity 방지**뿐이다.
