# PowerShell Fresh-Shell Execution Contract

사용자에게 PowerShell 실행을 요청할 때의 Base 공용 사용자 실행 계약이다. 목표는 사용자가 이전 터미널 상태를 기억하거나 여러 블록을 순서대로 조립하지 않아도, **새 PowerShell 창 하나에서 한 블록을 붙여넣어** 위치 확인부터 실행·오류 위치 확인까지 진행할 수 있게 하는 것이다.

## Machine contract

```text
FRESH_SHELL_ASSUMPTION
ONE_COPY_PASTE_BLOCK
LOCATION_FIRST
NO_PRIOR_SHELL_STATE_DEPENDENCY
FAIL_FAST
EXPECTED_PATH_MARKER
COMMAND_PREFLIGHT
NATIVE_EXIT_CODE_REQUIRED
ERROR_STAGE_MARKER
BEGINNER_SAFE_USER_ACTION
TOOL_HUB_RETIRED_FROM_DEFAULT_ROUTE
LOOP_ENGINEERING_DIRECT_WHEN_RELEVANT
```

## 1. `FRESH_SHELL_ASSUMPTION`

사용자에게 제공하는 블록은 **매 작업마다 새 PowerShell을 연 상태**를 기본 전제로 한다.

- 이전 창에서 만든 `$변수`, 함수, alias, `Set-Location`, 임시 환경 변수에 의존하지 않는다.
- 필요한 위치·변수·도구 검사는 같은 블록 안에서 다시 정의한다.
- 이미 열려 있는 특정 터미널 상태를 알아야만 성공하는 명령을 기본 경로로 제공하지 않는다.

## 2. `ONE_COPY_PASTE_BLOCK`

사용자 행동이 필요한 PowerShell 절차는 가능한 한 **한 코드 블록 전체를 한 번 복사 → 한 번 붙여넣기 → Enter**로 끝나야 한다.

여러 단계가 필요해도 한 블록 내부에서 stage로 순차 실행한다.

```text
[0/N LOCATION]
→ [1/N PREFLIGHT]
→ [2/N ACTION]
→ [3/N VERIFY]
→ [N/N RESULT]
```

보안상 별도 입력이 필요한 비밀값, OS 재부팅, 브라우저 인증처럼 한 블록으로 안전하게 자동화할 수 없는 행위는 예외다. 예외를 이유로 나머지 자동화 가능한 단계를 여러 블록으로 쪼개지 않는다.

## 3. `LOCATION_FIRST`

첫 실행 단계에서 작업 위치를 명시적으로 세팅하고 검증한다.

권장 골격:

```powershell
$ErrorActionPreference = 'Stop'
$Stage = '0/N LOCATION'
$Repo = 'C:\expected\project'
Write-Host "[$Stage] $Repo"
Set-Location -LiteralPath $Repo

if (-not (Test-Path -LiteralPath '.git')) {
    throw "EXPECTED_PATH_MARKER missing: .git"
}
```

프로젝트 성격에 따라 `.git`, `project.godot`, 특정 manifest 등 **현재 작업이 실제로 요구하는 최소 marker**를 사용한다. 존재하지 않는 경로를 임의 생성해 위치 오류를 숨기지 않는다.

경로를 자동 탐색할 수 있고 후보가 하나로 결정되면 같은 블록 안에서 탐색해도 된다. 후보가 여러 개라면 임의 선택하지 말고 발견된 후보를 보여주고 정확한 선택이 필요한 지점만 사용자에게 요청한다.

## 4. `NO_PRIOR_SHELL_STATE_DEPENDENCY`

블록은 다음을 이전 세션에서 이미 존재한다고 가정하지 않는다.

- 현재 디렉터리
- 사용자 정의 변수·함수·alias
- 특정 venv 활성화 상태
- 임시 PATH 수정
- 이전 명령 성공 결과

설치가 영속적으로 끝난 도구는 사용할 수 있지만 `COMMAND_PREFLIGHT`로 현재 새 창에서도 해석되는지 먼저 확인한다.

## 5. `FAIL_FAST`와 `COMMAND_PREFLIGHT`

PowerShell cmdlet 오류는 `$ErrorActionPreference = 'Stop'` 또는 동등한 명시적 처리로 조기에 멈춘다.

외부 명령을 호출하기 전:

```powershell
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'git command not found'
}
```

처럼 현재 shell에서 실제 해석 가능한지 확인한다. 설치됐을 것이라는 추측만으로 다음 단계를 실행하지 않는다.

## 6. `NATIVE_EXIT_CODE_REQUIRED`

`git`, `gh`, `python`, `godot`, `docker` 같은 native executable은 PowerShell 예외만으로 성공 여부를 판단하지 않는다. 필요한 경우 실행 직후 `$LASTEXITCODE`를 검사하고 non-zero를 실패로 승격한다.

```powershell
& git status --short
if ($LASTEXITCODE -ne 0) {
    throw "git status failed with exit code $LASTEXITCODE"
}
```

명령 자체가 다른 성공 규약을 가진 경우 그 실제 계약을 따른다.

## 7. `ERROR_STAGE_MARKER`

오류가 나면 사용자가 **어디에서 멈췄는지 한 줄만 보내도** 진단할 수 있어야 한다.

권장 패턴:

```powershell
$Stage = '0/N LOCATION'
try {
    # ...
}
catch {
    Write-Host "[BLOCKED][$Stage] $($_.Exception.Message)"
    Write-Host "[CWD] $(Get-Location)"
    throw
}
```

- stage 이름은 `LOCATION`, `PREFLIGHT`, `ACTION`, `VERIFY`, `RESULT`처럼 행동을 설명한다.
- secret/token/password 전체를 오류 메시지로 출력하지 않는다.
- 자동 복구가 안전하면 같은 블록에서 bounded recovery를 시도할 수 있다. 새로운 증거 없이 무한 retry하지 않는다.

## 8. `BEGINNER_SAFE_USER_ACTION`

실제 사용자 행동이 필요할 때는 이미 알고 있을 것이라 가정하지 않는다.

최소 설명 순서:

1. **어디를 클릭하는지** — 예: 시작 메뉴 → PowerShell.
2. **무엇을 복사하는지** — 제공된 코드 블록 전체.
3. **어디에 붙여넣는지** — 새 PowerShell 창.
4. **무엇을 누르는지** — Enter.
5. **성공하면 무엇이 보이는지** — `[N/N RESULT] ...`.
6. **실패하면 무엇을 보내는지** — `[BLOCKED][...]` 줄과 필요 시 바로 아래 최소 로그.

사용자에게 `cd ...`, `git ...`, `python ...`을 각각 따로 입력하게 하는 방식은 자동화할 수 없는 이유가 없으면 기본안으로 사용하지 않는다.

## 9. Direct execution·Loop Engineering 관계

`TOOL_HUB_RETIRED_FROM_DEFAULT_ROUTE`: Tool Hub는 신규 프로젝트의 기본 launcher나 PowerShell 대체면이 아니다. 과거 Hub code/history가 남아 있어도 이 계약에서 우선 실행 경로로 라우팅하지 않는다.

기본 로컬 구현 경로는 다음과 같다.

```text
fresh PowerShell
→ LOCATION_FIRST
→ project identity / worktree preflight
→ project-dedicated Godot / HiGodot / CODEX_HOME 확인·복구
→ adopted GUT / Hera가 현재 acceptance에 필요할 때만 해당 profile 확인
→ Codex를 exact project/worktree에서 실행
→ Codex 내부에서 fresh repository/runtime evidence 확인
→ implementation / test / runtime verification
```

`LOOP_ENGINEERING_DIRECT_WHEN_RELEVANT`: 승인된 Implementation Package와 current operational evidence가 Loop Engineering 사용을 정당화하면 Tool Hub를 경유하지 않고 해당 Loop contract/runtime을 직접 사용한다. 현재 지원 범위는 `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`과 실제 code/test에서 다시 읽는다.

- PowerShell 블록을 제공했다는 사실은 Codex/Godot/Loop Engineering 실제 readiness 증거가 아니다.
- editor process 존재나 port listen만으로 project-authorized readiness를 PASS 처리하지 않는다.
- 다른 프로젝트의 CODEX_HOME, HiGodot profile/port, Hera token/profile을 재사용하지 않는다.
- 이미 안전한 current project runtime이 정확히 확인되면 불필요한 중복 process를 만들지 않는다.

## 10. Security and rollback

- 비밀값을 코드 블록에 하드코딩하지 않는다.
- `Remove-Item -Recurse -Force`, registry 변경, 서비스/프로세스 강제 종료, 디스크·계정 변경처럼 파괴 가능성이 큰 명령은 일반 편의 자동화에 섞지 않는다.
- side effect가 있는 단계가 실패하면 현재 상태를 먼저 readback하고 이미 끝난 작업을 무조건 재실행하지 않는다.
- 되돌리기 가능한 설정 변경은 원래 값이나 backup/replacement pointer를 보존한다.

## Example skeleton

다음은 **형식 예시**이며 실제 프로젝트 경로·marker·명령은 현재 저장소에서 확인해 채운다.

```powershell
$ErrorActionPreference = 'Stop'
$Stage = '0/4 LOCATION'

try {
    $Repo = 'C:\REPLACE_WITH_VERIFIED_REPO_PATH'
    Write-Host "[$Stage] $Repo"
    Set-Location -LiteralPath $Repo
    if (-not (Test-Path -LiteralPath '.git')) { throw 'EXPECTED_PATH_MARKER missing: .git' }

    $Stage = '1/4 PREFLIGHT'
    Write-Host "[$Stage]"
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'git command not found' }

    $Stage = '2/4 ACTION'
    Write-Host "[$Stage]"
    & git status --short
    if ($LASTEXITCODE -ne 0) { throw "git failed with exit code $LASTEXITCODE" }

    $Stage = '3/4 VERIFY'
    Write-Host "[$Stage]"
    # current task-specific verification

    $Stage = '4/4 RESULT'
    Write-Host "[$Stage] COMPLETE"
}
catch {
    Write-Host "[BLOCKED][$Stage] $($_.Exception.Message)"
    Write-Host "[CWD] $(Get-Location)"
    throw
}
```

`C:\REPLACE_WITH_VERIFIED_REPO_PATH` 같은 placeholder를 사용자에게 그대로 실행시키지 않는다. 실제 작업에서는 저장소 사실로 경로를 확정하거나 같은 블록 안에서 안전하게 탐색한다.
