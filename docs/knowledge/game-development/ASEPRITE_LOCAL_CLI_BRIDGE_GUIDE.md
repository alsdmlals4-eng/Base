# Aseprite 로컬 CLI 브리지 설치·운용 가이드

```yaml
status: BASE_SHARED_CANDIDATE
scope: INSPECT_EXPORT_VALIDATE_ONLY
live_editor_mutation: NOT_INCLUDED
arbitrary_lua: FORBIDDEN
network_listener: NONE
project_adoption: PROJECT_BY_PROJECT
additional_paid_service: NONE
runtime_evidence: REQUIRED_PER_PROJECT
```

이 가이드는 Codex나 로컬 작업자가 **사용자가 보유한 정식 Aseprite 실행 파일**을 공식 CLI로 호출하여 `.aseprite` 원본을 검사하고, PNG 스프라이트 시트·JSON 메타데이터·SHA-256 영수증을 프로젝트의 로컬 Asset Vault에 생성하는 절차다.

이 브리지는 다음을 하지 않는다.

- Aseprite를 다운로드하거나 재배포하지 않는다.
- Aseprite GUI를 실시간으로 그리거나 조작하지 않는다.
- 임의 Lua나 임의 CLI 인자를 실행하지 않는다.
- MCP 서버·WebSocket·HTTP 포트를 열지 않는다.
- `assets/_vault_local/` 또는 승인된 tracked asset 경로에 직접 쓰지 않는다.
- 후보 생성만으로 프로젝트 채택·사용자 승인·Godot runtime PASS를 주장하지 않는다.

## 1. 전체 흐름

```text
licensed Aseprite + .aseprite source
  -> tools/aseprite_cli_bridge.py doctor
  -> inspect
  -> export
     -> .asset-vault/library/aseprite-generated/<ASSET_ID>/
        - <ASSET_ID>.png
        - <ASSET_ID>.json
        - <ASSET_ID>.receipt.json
  -> tools/project_asset_vault.py sync
     -> assets/_vault_local/aseprite-generated/<ASSET_ID>/<ASSET_ID>.png
  -> Godot import / scene wiring / runtime capture
  -> user review
  -> PROJECT_ASSET_APPROVED
  -> existing Asset Vault promote flow
  -> tracked asset + ASSET_MANIFEST + actual consumer
```

`.asset-vault/library/`가 활성 로컬 후보의 파일 권위이고 `assets/_vault_local/`은 Godot에서 보기 위한 로컬 투영이다. 따라서 브리지는 `_vault_local`에 직접 쓰지 않는다.

## 2. 필요한 것

### 필수

- Windows 10/11 또는 Aseprite가 지원하는 데스크톱 OS
- Python 3.11 이상
- 사용자가 정식으로 보유한 Aseprite 1.3 이상
- 최신 프로젝트 `AGENTS.md`를 읽을 수 있는 프로젝트 저장소
- Base 저장소의 다음 파일
  - `tools/aseprite_cli_bridge.py`
  - `templates/project-operations/ASEPRITE_LOCAL_BRIDGE_PROFILE.json`
  - `tools/project_asset_vault.py`

### 추가 비용

브리지·Python·Codex의 로컬 CLI 호출에는 별도 서버나 API 비용이 없다. Aseprite 자체는 별도 소프트웨어이며 이미 보유한 정식 설치본을 사용한다. Base는 Aseprite 구매·라이선스를 대신 제공하지 않는다.

## 3. 공식 링크

| 목적 | 링크 |
|---|---|
| Aseprite 공식 사이트 | https://www.aseprite.org/ |
| Aseprite 공식 CLI 문서 | https://www.aseprite.org/docs/cli/ |
| Aseprite 공식 스크립팅 문서 | https://www.aseprite.org/docs/scripting/ |
| Aseprite 공식 Extension 문서 | https://www.aseprite.org/docs/extensions/ |
| Aseprite 공식 GitHub | https://github.com/aseprite/aseprite |
| Aseprite 공식 빌드 지침 | https://github.com/aseprite/aseprite/blob/main/INSTALL.md |
| Steam Aseprite | https://store.steampowered.com/app/431730/Aseprite/ |
| itch.io Aseprite | https://aseprite.itch.io/aseprite |
| Python Windows 다운로드 | https://www.python.org/downloads/windows/ |
| Codex MCP 공식 문서 | https://developers.openai.com/codex/mcp/ |

2026-09-09 조사 시 Aseprite 공식 GitHub의 latest release tag는 `v1.3.18.4`였다. GitHub release에는 소스 패키지가 중심이며, 일반 사용자는 본인이 구매한 공식/Steam/itch.io 바이너리를 사용한다. 설치 후에는 `doctor`가 실제 로컬 버전을 읽으므로 문서의 조사 시점 버전을 고정값으로 가정하지 않는다.

## 4. Windows에서 Aseprite 실행 파일 찾기

### 가장 확실한 방법: Steam에서 직접 열기

1. Steam 라이브러리에서 **Aseprite**를 선택한다.
2. 톱니바퀴 → **관리(Manage)** → **로컬 파일 탐색(Browse local files)**을 누른다.
3. 열린 폴더의 `Aseprite.exe` 경로를 복사한다.

Steam 라이브러리를 다른 드라이브에 설치했다면 자동 검색보다 이 방법이 정확하다.

### 일반 경로 자동 확인

새 PowerShell 창을 열고 아래 한 블록을 실행한다.

```powershell
$Candidates = @(
    "$env:ProgramFiles\Aseprite\Aseprite.exe",
    "$env:ProgramFiles\Steam\steamapps\common\Aseprite\Aseprite.exe",
    "${env:ProgramFiles(x86)}\Aseprite\Aseprite.exe",
    "${env:ProgramFiles(x86)}\Steam\steamapps\common\Aseprite\Aseprite.exe",
    "$env:LOCALAPPDATA\Programs\Aseprite\Aseprite.exe"
) | Where-Object { $_ -and (Test-Path -LiteralPath $_) }

if (-not $Candidates) {
    throw "Aseprite.exe를 일반 설치 경로에서 찾지 못했습니다. Steam의 '로컬 파일 탐색'으로 경로를 확인하세요."
}

$Candidates | ForEach-Object { Resolve-Path -LiteralPath $_ }
```

### 현재 PowerShell 세션에 경로 지정

아래 경로는 실제 설치 경로로 바꾼다.

```powershell
$AsepritePath = "C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe"

if (-not (Test-Path -LiteralPath $AsepritePath -PathType Leaf)) {
    throw "Aseprite 실행 파일이 없습니다: $AsepritePath"
}

$env:ASEPRITE_PATH = (Resolve-Path -LiteralPath $AsepritePath).Path
& $env:ASEPRITE_PATH --version
```

이 설정은 현재 PowerShell 창에만 적용된다.

### 사용자 환경 변수로 영구 저장

```powershell
$AsepritePath = "C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe"

if (-not (Test-Path -LiteralPath $AsepritePath -PathType Leaf)) {
    throw "Aseprite 실행 파일이 없습니다: $AsepritePath"
}

$ResolvedAsepritePath = (Resolve-Path -LiteralPath $AsepritePath).Path
[Environment]::SetEnvironmentVariable("ASEPRITE_PATH", $ResolvedAsepritePath, "User")
$env:ASEPRITE_PATH = $ResolvedAsepritePath

Write-Host "ASEPRITE_PATH=$env:ASEPRITE_PATH"
& $env:ASEPRITE_PATH --version
```

Codex·VS Code·터미널이 이미 열려 있었다면 완전히 닫았다가 다시 열어 새 환경 변수를 읽게 한다.

## 5. 최초 연결 진단

아래 두 경로를 실제 Base와 대상 프로젝트 경로로 바꾼다. **새 PowerShell에서 위치와 파일을 먼저 확인한 뒤** 실행한다.

```powershell
$BaseRoot = "C:\Repos\Base"
$ProjectRoot = "C:\Repos\YOUR_GAME_PROJECT"
$Bridge = Join-Path $BaseRoot "tools\aseprite_cli_bridge.py"
$Profile = Join-Path $BaseRoot "templates\project-operations\ASEPRITE_LOCAL_BRIDGE_PROFILE.json"

foreach ($RequiredPath in @($BaseRoot, $ProjectRoot, $Bridge, $Profile, $env:ASEPRITE_PATH)) {
    if (-not $RequiredPath -or -not (Test-Path -LiteralPath $RequiredPath)) {
        throw "필수 경로를 찾지 못했습니다: $RequiredPath"
    }
}

Set-Location -LiteralPath $ProjectRoot
python --version
python $Bridge doctor `
    --project-root $ProjectRoot `
    --config $Profile

if ($LASTEXITCODE -ne 0) {
    throw "Aseprite doctor가 실패했습니다. 위 ASEPRITE_BRIDGE_ERROR를 확인하세요."
}
```

정상 결과의 핵심 필드는 다음과 같다.

```json
{
  "status": "PASS",
  "operation": "doctor",
  "aseprite_version": "Aseprite 1.3.x",
  "discovery_source": "environment",
  "candidate_output_root": ".asset-vault/library/aseprite-generated",
  "allow_overwrite": false
}
```

`doctor PASS`는 Aseprite 실행 파일 발견과 버전 호출만 증명한다. 프로젝트 자산 내보내기나 Godot 적용을 증명하지 않는다.

이 1차 경로는 Codex의 일반 로컬 명령 실행을 사용하므로 `codex mcp add`나 `~/.codex/config.toml` 편집이 필요 없다. ChatGPT 웹 대화가 사용자의 Windows 실행 파일을 직접 여는 구조도 아니다. GPT Work가 브리프·검수 기준을 준비하고, 로컬 저장소를 여는 Codex가 아래 명령을 실행하는 역할 분리가 기본이다.

### Codex에 그대로 전달할 실행 지시문

```text
대상 프로젝트의 최신 AGENTS.md와 지정된 bootstrap/read order를 먼저 읽어라.
Base의 tools/aseprite_cli_bridge.py와 프로젝트의 Aseprite profile을 사용한다.
임의 Lua, 임의 CLI 인자, community Aseprite MCP, 네트워크 listener를 사용하지 않는다.

1. doctor로 실제 Aseprite 실행 파일과 버전을 확인한다.
2. 지정된 .aseprite 원본에 inspect를 실행하고 source SHA-256, layer hierarchy, tags, slices를 보고한다.
3. export는 .asset-vault/library/aseprite-generated/<ASSET_ID>/ 후보에만 수행한다.
4. validate를 실행해 원본/PNG/JSON hash와 command/evidence contract를 재검증한다.
5. 기존 tools/project_asset_vault.py sync로 PNG를 assets/_vault_local에 투영한다.
6. 후보 단계에서는 tracked asset, ASSET_MANIFEST, Scene/Resource를 수정하지 않는다.
7. 실제 Godot import와 화면 검증을 실행하지 못했으면 NOT_RUN으로 남긴다.
8. 출력 파일, receipt, git status, remaining blocker를 readback해서 보고한다.
```

## 6. 프로젝트별 profile 적용

Base template를 그대로 읽어 canary를 할 수 있지만, 실제 프로젝트에서 채택할 때는 프로젝트 `AGENTS.md`가 지정한 config/operations owner에 profile을 복사하고 프로젝트 경로에 맞게 검토한다.

예시:

```powershell
$BaseRoot = "C:\Repos\Base"
$ProjectRoot = "C:\Repos\YOUR_GAME_PROJECT"
$SourceProfile = Join-Path $BaseRoot "templates\project-operations\ASEPRITE_LOCAL_BRIDGE_PROFILE.json"
$TargetDirectory = Join-Path $ProjectRoot "config\tools"
$TargetProfile = Join-Path $TargetDirectory "aseprite-local-bridge.json"

New-Item -ItemType Directory -Force -Path $TargetDirectory | Out-Null
Copy-Item -LiteralPath $SourceProfile -Destination $TargetProfile
Get-Content -LiteralPath $TargetProfile -Raw
```

이 경로는 예시다. 대상 프로젝트의 최신 `AGENTS.md`가 다른 owner 경로를 지정하면 그 경로가 우선한다. 실제 채택 profile에는 사용자 PC의 `C:\...\Aseprite.exe` 절대 경로를 기록하지 않는다.

### profile 항목

| 항목 | 의미 |
|---|---|
| `source_roots` | `.aseprite` 원본을 읽을 수 있는 프로젝트 내부 루트 |
| `candidate_output_root` | PNG/JSON/영수증을 쓸 수 있는 유일한 로컬 후보 루트 |
| `allowed_source_extensions` | 허용되는 Aseprite 원본 확장자 |
| `allow_overwrite` | 기존 후보 교체 기능 자체의 허용 여부 |
| `timeout_seconds` | 한 Aseprite CLI 프로세스의 최대 실행 시간 |
| `sheet_type` | Aseprite sprite-sheet 배열 방식 |
| `adoption_state` | `CANDIDATE` 등 Base 외부 도구 채택 수명주기 상태 |

기본값은 `allow_overwrite: false`다. 기존 후보를 바꾸려면 profile을 `true`로 바꾸는 것과 명령에 `--overwrite`를 넣는 것, 두 조건이 모두 필요하다. 승인된 tracked asset은 이 옵션으로 바뀌지 않는다.

## 7. `.aseprite` 원본 준비

예시 원본 위치:

```text
<project-root>/.asset-vault/library/aseprite-source/HERO_IDLE_01.aseprite
```

Aseprite에서 다음을 먼저 정리한다.

- 파일 캔버스 크기
- 프레임별 duration
- 애니메이션 tag 이름
- 필요한 layer 이름과 hierarchy
- slice·pivot 사용 시 이름과 위치
- 프로젝트 팔레트와 color mode

파일명은 사람이 읽는 이름이어도 되지만 export의 `asset-id`는 다음 정규식만 허용한다.

```text
[A-Z0-9][A-Z0-9_-]{0,63}
```

예: `HERO_IDLE_01`, `DOGYEOM_ATTACK_A`, `UI_CURSOR_SELECT`.

## 8. 원본 검사: `inspect`

```powershell
$BaseRoot = "C:\Repos\Base"
$ProjectRoot = "C:\Repos\YOUR_GAME_PROJECT"
$Bridge = Join-Path $BaseRoot "tools\aseprite_cli_bridge.py"
$Profile = Join-Path $ProjectRoot "config\tools\aseprite-local-bridge.json"
$Source = ".asset-vault\library\aseprite-source\HERO_IDLE_01.aseprite"

Set-Location -LiteralPath $ProjectRoot
python $Bridge inspect `
    --project-root $ProjectRoot `
    --config $Profile `
    --source $Source

if ($LASTEXITCODE -ne 0) {
    throw "Aseprite inspect가 실패했습니다."
}
```

`inspect`는 Aseprite의 고정된 batch/list 명령만 사용한다.

```text
-b
--list-layer-hierarchy
--list-tags
--list-slices
--data=
```

결과에는 프로젝트 상대 원본 경로, 원본 SHA-256, 실제 Aseprite 버전, Aseprite가 반환한 metadata가 포함된다. 파일을 쓰지 않는다.

## 9. 후보 내보내기: `export`

```powershell
$BaseRoot = "C:\Repos\Base"
$ProjectRoot = "C:\Repos\YOUR_GAME_PROJECT"
$Bridge = Join-Path $BaseRoot "tools\aseprite_cli_bridge.py"
$Profile = Join-Path $ProjectRoot "config\tools\aseprite-local-bridge.json"
$Source = ".asset-vault\library\aseprite-source\HERO_IDLE_01.aseprite"
$AssetId = "HERO_IDLE_01"

Set-Location -LiteralPath $ProjectRoot
python $Bridge export `
    --project-root $ProjectRoot `
    --config $Profile `
    --source $Source `
    --asset-id $AssetId

if ($LASTEXITCODE -ne 0) {
    throw "Aseprite export가 실패했습니다."
}
```

생성 위치:

```text
.asset-vault/library/aseprite-generated/HERO_IDLE_01/
├─ HERO_IDLE_01.png
├─ HERO_IDLE_01.json
└─ HERO_IDLE_01.receipt.json
```

영수증은 다음을 기록한다.

- 원본 프로젝트 상대 경로와 SHA-256
- Aseprite 실제 버전
- PNG/JSON 프로젝트 상대 경로, SHA-256, 크기
- sheet type과 metadata 포함 범위
- arbitrary Lua/CLI가 사용되지 않았다는 command contract
- 생성 UTC 시각
- 프로젝트 채택·Godot runtime·사용자 승인을 증명하지 않는 evidence ceiling

사용자 PC의 Base 경로, 프로젝트 절대 경로, Aseprite 절대 경로는 영수증에 기록하지 않는다.

## 10. 결과 재검증: `validate`

```powershell
$BaseRoot = "C:\Repos\Base"
$ProjectRoot = "C:\Repos\YOUR_GAME_PROJECT"
$Bridge = Join-Path $BaseRoot "tools\aseprite_cli_bridge.py"
$Profile = Join-Path $ProjectRoot "config\tools\aseprite-local-bridge.json"

Set-Location -LiteralPath $ProjectRoot
python $Bridge validate `
    --project-root $ProjectRoot `
    --config $Profile `
    --asset-id "HERO_IDLE_01"

if ($LASTEXITCODE -ne 0) {
    throw "후보 파일 또는 영수증이 변경됐습니다. 재내보내기 전에 diff와 원인을 확인하세요."
}
```

검증 항목:

- PNG signature와 비어 있지 않은 파일 크기
- JSON의 `frames`와 `meta` 구조
- 원본 SHA-256
- PNG·JSON SHA-256과 크기
- 영수증의 asset ID와 상대 경로
- 고정 command contract와 evidence ceiling의 변조 여부
- candidate root 밖 경로와 모든 source/candidate symlink 여부

### 최초 카나리 명령을 한 번에 실행

아래 블록은 `doctor → inspect → export → validate`까지만 연속 실행한다. 기존 후보가 있으면 기본적으로 중단하며, Asset Vault sync와 Godot 검증은 결과를 읽은 뒤 별도로 수행한다.

```powershell
$ErrorActionPreference = "Stop"
$BaseRoot = "C:\Repos\Base"
$ProjectRoot = "C:\Repos\YOUR_GAME_PROJECT"
$Bridge = Join-Path $BaseRoot "tools\aseprite_cli_bridge.py"
$Profile = Join-Path $ProjectRoot "config\tools\aseprite-local-bridge.json"
$Source = ".asset-vault\library\aseprite-source\HERO_IDLE_01.aseprite"
$AssetId = "HERO_IDLE_01"

foreach ($RequiredPath in @($BaseRoot, $ProjectRoot, $Bridge, $Profile, $env:ASEPRITE_PATH)) {
    if (-not $RequiredPath -or -not (Test-Path -LiteralPath $RequiredPath)) {
        throw "필수 경로를 찾지 못했습니다: $RequiredPath"
    }
}

function Invoke-CheckedPython {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    & python @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python 명령 실패(exit=$LASTEXITCODE): $($Arguments -join ' ')"
    }
}

Set-Location -LiteralPath $ProjectRoot
Invoke-CheckedPython @($Bridge, "doctor", "--project-root", $ProjectRoot, "--config", $Profile)
Invoke-CheckedPython @($Bridge, "inspect", "--project-root", $ProjectRoot, "--config", $Profile, "--source", $Source)
Invoke-CheckedPython @($Bridge, "export", "--project-root", $ProjectRoot, "--config", $Profile, "--source", $Source, "--asset-id", $AssetId)
Invoke-CheckedPython @($Bridge, "validate", "--project-root", $ProjectRoot, "--config", $Profile, "--asset-id", $AssetId)

Get-ChildItem -LiteralPath (Join-Path $ProjectRoot ".asset-vault\library\aseprite-generated\$AssetId")
```

## 11. Asset Vault 동기화 후 Godot에서 확인

내보내기가 끝나면 Base의 기존 Asset Vault 도구로 로컬 후보를 Godot 작업면에 투영한다.

```powershell
$BaseRoot = "C:\Repos\Base"
$ProjectRoot = "C:\Repos\YOUR_GAME_PROJECT"
$VaultTool = Join-Path $BaseRoot "tools\project_asset_vault.py"

Set-Location -LiteralPath $ProjectRoot
python $VaultTool sync --project-root $ProjectRoot

if ($LASTEXITCODE -ne 0) {
    throw "Asset Vault sync가 실패했습니다. 프로젝트의 PROJECT_ASSET_VAULT 설정과 Base 정책을 확인하세요."
}
```

Godot에서 예상되는 로컬 PNG 경로:

```text
res://assets/_vault_local/aseprite-generated/HERO_IDLE_01/HERO_IDLE_01.png
```

Asset Vault가 지원하지 않는 비이미지 파일은 local vault에만 남을 수 있다. JSON metadata를 runtime consumer가 필요로 한다면 프로젝트별 구현 명세에서 tracked data path와 importer를 별도로 정의하고 승인·검증한다. `sync` 결과를 근거 없이 추측하지 말고 실제 `sync.json`과 Godot FileSystem을 readback한다.

### Godot 기본 기능으로 확인

1. Godot 프로젝트를 연다.
2. FileSystem dock에서 위 PNG가 import됐는지 확인한다.
3. `AnimatedSprite2D`의 `SpriteFrames`에서 **Add frames from a Sprite Sheet**를 사용한다.
4. 원본의 프레임 셀 크기와 행·열을 맞춘다.
5. 프레임 순서와 duration을 실제 Aseprite tag/metadata와 비교한다.
6. 테스트 Scene을 실행하여 idle/attack 등 실제 상태를 캡처한다.

이 수동 절차는 canary용이다. 프로젝트가 tag·duration·pivot 자동 변환을 반복적으로 필요로 하면, 그때 프로젝트별 importer 또는 검증된 Godot addon을 별도 평가한다.

## 12. 기존 후보 교체

기본 profile은 교체를 막는다. 같은 `asset-id`로 다시 쓰려면 먼저 기존 결과를 검토하고, local candidate에 한해 다음 두 조치를 모두 수행한다.

1. 프로젝트 profile의 `allow_overwrite`를 `true`로 변경한다.
2. 명령에 `--overwrite`를 명시한다.

```powershell
python $Bridge export `
    --project-root $ProjectRoot `
    --config $Profile `
    --source $Source `
    --asset-id "HERO_IDLE_01" `
    --overwrite
```

브리지는 새 PNG/JSON/영수증을 임시 디렉터리에서 먼저 검사한 뒤 candidate bundle을 교체한다. 승인된 tracked asset이나 Scene/Resource는 변경하지 않는다. 교체 후 `validate`, Asset Vault `sync`, Godot runtime 검증을 다시 수행한다.

검증이 끝나면 profile을 다시 fail-closed 상태로 되돌린다.

```powershell
$Profile = Join-Path $ProjectRoot "config\tools\aseprite-local-bridge.json"
$Config = Get-Content -LiteralPath $Profile -Raw | ConvertFrom-Json
$Config.allow_overwrite = $false
$Config | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $Profile -Encoding utf8
```

## 13. Git에 후보가 들어가지 않는지 확인

```powershell
$ProjectRoot = "C:\Repos\YOUR_GAME_PROJECT"
Set-Location -LiteralPath $ProjectRoot

git status --short
git check-ignore -v -- ".asset-vault" "assets/_vault_local"
```

기대 결과:

- `.asset-vault/`와 `assets/_vault_local/`이 ignored다.
- 후보 생성만으로 tracked diff가 생기지 않는다.

`git check-ignore`가 아무것도 출력하지 않으면 자동으로 `.gitignore`를 덧붙이지 않는다. 먼저 프로젝트 최신 `AGENTS.md`, 기존 `.gitignore`, Asset Vault profile을 읽고 프로젝트 변경 PR에서 교정한다.

## 14. 승인과 tracked asset 승격

다음 상태를 구분한다.

```text
BRIDGE_EXPORT_PASS
!= ASSET_VAULT_SYNC_PASS
!= GODOT_IMPORT_PASS
!= RUNTIME_VERIFIED
!= USER_APPROVED
!= CANON_REGISTERED
!= RELEASE_PASS
```

사용자 승인 전에는 `.asset-vault/library/`와 `assets/_vault_local/` 후보로 유지한다. 승인 후 기존 Asset Vault `promote` 경계와 프로젝트 `ASSET_MANIFEST` 규칙을 사용한다.

PNG 예시 source key:

```text
aseprite-generated/HERO_IDLE_01/HERO_IDLE_01.png
```

프로젝트마다 승인 target, provenance, SHA-256, consumer, 상태군, runtime evidence가 다르므로 대상 프로젝트의 최신 `AGENTS.md`와 manifest owner를 먼저 읽는다. 영수증이나 JSON이 제품 consumer에 필요하면 별도의 tracked data 승인 경로를 명세한다.

## 15. 흔한 오류와 해결

### `Aseprite executable was not found`

- `$env:ASEPRITE_PATH`를 확인한다.
- Steam의 **로컬 파일 탐색**으로 실제 위치를 찾는다.
- Codex/VS Code를 환경 변수 설정 후 다시 연다.
- 일회성으로 `--aseprite "C:\...\Aseprite.exe"`를 전달한다.

### `Aseprite source is outside every declared source root`

- 원본을 `.asset-vault/library/` 또는 project profile에 승인된 source root 아래로 옮긴다.
- `..`로 프로젝트 밖 파일을 참조하지 않는다.
- 브리지는 허용 루트 안을 가리키는 경우에도 source/candidate symlink를 거부하므로 실제 파일·디렉터리를 사용한다.

### `Candidate output already exists`

- 다른 `asset-id`를 사용하여 새 후보로 비교한다.
- 교체가 정말 필요하면 project profile과 `--overwrite`를 함께 사용한다.
- 승인된 tracked asset을 이 명령으로 바꾸려 하지 않는다.

### `Aseprite inspection did not return valid JSON`

- `doctor`로 실제 버전을 확인한다.
- Aseprite CLI를 PowerShell에서 직접 호출해 오류를 확인한다.
- 사용 중인 Aseprite 버전의 공식 CLI 문서에서 list/data 지원을 확인한다.
- 원본 파일을 Aseprite GUI에서 열어 손상 여부를 확인한다.

### `Aseprite did not create both PNG and JSON outputs`

- source가 정상적으로 열리는지 확인한다.
- output 경로에 쓰기 권한이 있는지 확인한다.
- tag/layer 이름과 export 설정을 확인한다.
- bridge가 출력한 Aseprite error를 보존하고 임의 Lua 우회로 전환하지 않는다.

### `output hash does not match the receipt`

- 내보낸 뒤 파일이 수동 수정됐거나 sync/외부 도구가 candidate authority를 바꿨다.
- 원본·PNG·JSON·receipt의 변경 시각과 SHA-256을 비교한다.
- 의도된 수정이면 새 export로 영수증을 다시 만든다.
- 원인 불명 상태에서 기존 receipt를 손으로 고치지 않는다.

## 16. 제거·롤백

이 1차 브리지는 설치형 서버가 아니므로 제거가 단순하다.

1. Codex/터미널에서 실행 중인 bridge 프로세스가 있으면 해당 명령 종료와 함께 이미 끝난 상태다.
2. 필요하면 사용자 환경 변수 `ASEPRITE_PATH`만 제거한다.
3. 프로젝트의 local candidate를 archive 또는 삭제한다.
4. Asset Vault `sync`를 다시 실행한다.
5. 프로젝트에 복사한 profile이 미채택이면 제거한다.
6. tracked asset은 local candidate 삭제로 자동 삭제하지 않는다.

사용자 환경 변수 제거:

```powershell
[Environment]::SetEnvironmentVariable("ASEPRITE_PATH", $null, "User")
Remove-Item Env:ASEPRITE_PATH -ErrorAction SilentlyContinue
```

## 17. 2단계: Codex MCP로 실시간 Aseprite 조작

### 현재 판정

Base 기본 경로에는 아직 설치하지 않는다.

| 후보 | 장점 | 현재 차단점 | 판정 |
|---|---|---|---|
| `diivi/aseprite-mcp` | 광범위한 draw/animation/palette/tilemap/export 도구 | 100개가 넘는 도구와 raw Lua escape hatch로 기본 권한·컨텍스트가 큼 | `REFERENCE_ONLY` |
| `mattt/aseprite-mcp` | stdio, 작은 도구 수, workspace 제한 | `execute_lua`가 sandbox되지 않고 파일시스템 전체에 접근 가능 | `REFERENCE_ONLY` |
| `giangdvdotdev/aseprite-mcp` | `uvx` 기반 설치가 쉽고 Aseprite GUI 실시간 조작 | localhost WebSocket에 인증이 없고 save/export가 임의 절대 경로를 덮어쓸 수 있음 | `ISOLATED_TRIAL_ONLY` |
| `bachhoang0606/aseprite-mcp` | live preflight, 시각 readback, raw Lua/CLI 기본 비활성 | Rust build·bridge·plugin의 구성 요소가 많고 실제 Windows canary 필요 | `PREFERRED_LIVE_TRIAL_CANDIDATE` |

링크:

- https://github.com/diivi/aseprite-mcp
- https://github.com/mattt/aseprite-mcp
- https://github.com/giangdvdotdev/aseprite-mcp
- https://github.com/bachhoang0606/aseprite-mcp

### MCP trial 진입 조건

다음이 모두 충족된 프로젝트에서만 별도 승인된 trial을 연다.

1. CLI bridge canary를 실제로 2회 이상 사용했다.
2. 사람이 Aseprite GUI에서 즉시 보아야 하는 live mutation이 명확한 병목이다.
3. 대상 프로젝트와 source/output roots가 확정됐다.
4. 임의 Lua/CLI가 기본 비활성이다.
5. localhost only이며 port forwarding·LAN 공개·remote tunnel이 없다.
6. 별도 이름 `aseprite-live`로 등록해 다른 MCP와 충돌하지 않는다.
7. disposable source copy에서 먼저 검증한다.
8. tracked source diff와 candidate output diff를 전후 비교한다.
9. 서버·bridge·Aseprite plugin 종료·제거 절차를 검증한다.
10. 사용자 승인 전 정본 자산을 overwrite하지 않는다.

Codex는 공식적으로 로컬 stdio MCP를 `~/.codex/config.toml`에 등록하거나 `codex mcp add`로 관리할 수 있다. 실제 community server 명령은 선택한 release의 README와 exact version을 다시 읽고 구성한다. floating `latest`를 장기 profile에 고정하지 않는다.

### 예시 형태만 제시하는 Codex config

아래는 설치 완료 명령이 아니라 **최종 구조 예시**다. `<PINNED_SERVER_PATH>`는 검증한 exact build로 바꾼다.

```toml
[mcp_servers.aseprite-live]
command = "<PINNED_SERVER_PATH>"
args = []
startup_timeout_sec = 20
tool_timeout_sec = 60

[mcp_servers.aseprite-live.env]
ASEPRITE_PATH = "<LOCAL_ASEPRITE_EXECUTABLE>"
ASEPRITE_MCP_ALLOW_LUA = "0"
```

경로가 개인 설정에 저장되는 것은 허용되지만 repository·prompt·receipt·로그에 복제하지 않는다.

## 18. 프로젝트 채택 완료 증거

```yaml
bridge_doctor: PASS
source_inspect: PASS
candidate_export: PASS
receipt_validate: PASS
asset_vault_sync: PASS
tracked_source_delta_during_candidate_trial: NONE
Godot_import: PASS
actual_consumer_wired: PASS
Godot_runtime_capture: PASS
human_visual_review: PASS
user_asset_approval: PASS
manifest_provenance_sha256_consumer: PASS
release_validation: SEPARATE
```

Base 도구의 단위 테스트 PASS만으로 위 프로젝트 항목을 채우지 않는다.
