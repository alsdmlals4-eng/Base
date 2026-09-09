# Aseprite Local Bridge

Aseprite Local Bridge는 **사용자가 별도로 설치·구매한 정식 Aseprite 실행 파일**을 Codex/PowerShell에서 안전하게 호출해 다음 작업을 반복 가능하게 만드는 로컬 도구다.

```text
.aseprite 후보 원본
→ layer/tag/slice 점검
→ PNG sprite sheet + Aseprite JSON export
→ SHA-256 readback receipt
→ Asset Vault sync
→ Godot에서 로컬 후보 확인
→ PROJECT_ASSET_APPROVED 뒤 명시적 promote
```

이 브리지는 Aseprite 자체를 포함하거나 재배포하지 않는다. Aseprite 라이선스는 사용자가 별도로 보유해야 한다. 브리지 코드는 Base 저장소의 MIT 라이선스를 따른다.

## 현재 채택 범위

```yaml
bridge_version: 0.1.0
adoption_state: CANDIDATE_FOR_PROJECT_TRIAL
transport: direct local process
network_listener: none
raw_lua: forbidden
generic_shell_command: forbidden
write_root: .asset-vault/library/aseprite-generated
runtime_dependency: none
```

지원 명령은 네 개뿐이다.

| 명령 | 역할 | 쓰기 여부 |
|---|---|---|
| `doctor` | 설정·Aseprite 경로·버전 확인 | 없음 |
| `inspect` | `.aseprite`의 layer/tag/slice 목록과 원본 해시 확인 | 없음 |
| `export-candidate` | 제한된 후보 경로에 PNG+JSON+receipt 생성 | 후보 경로만 |
| `validate-candidate` | 원본·출력·receipt 해시와 경로 재검증 | 없음 |

`ASEPRITE_RUNTIME_NOT_RUN`, `GODOT_RUNTIME_NOT_RUN`, `UX_HUMAN_NOT_RUN`은 서로 다른 상태다. `export-candidate` 성공만으로 실제 게임 적용이나 사용자 승인이 되지 않는다.

## 공식 링크

- Aseprite 공식 사이트: https://www.aseprite.org/
- 공식 다운로드: https://www.aseprite.org/download/
- Steam 상점: https://store.steampowered.com/app/431730/Aseprite/
- 공식 CLI 문서: https://www.aseprite.org/docs/cli/
- 공식 Lua scripting 문서: https://www.aseprite.org/docs/scripting/
- 공식 extension 문서: https://www.aseprite.org/docs/extensions/
- 편집 원본과 export 파일 안내: https://www.aseprite.org/docs/files/
- Aseprite 공식 GitHub: https://github.com/aseprite/aseprite
- Codex MCP 설정 문서: https://developers.openai.com/codex/mcp
- Python Windows 다운로드: https://www.python.org/downloads/windows/

이 브리지는 공식 CLI의 비스크립트 기능만 사용한다. 공식 Lua API는 참고 링크로만 남기며 `--script`, raw Lua, 임의 CLI 옵션을 노출하지 않는다.

## 요구 사항

- Windows 10/11 또는 Aseprite가 실행되는 macOS/Linux
- Python 3.11 이상
- Aseprite 1.3 이상 권장
- Aseprite 실행 파일에 대한 정상적인 사용자 라이선스
- 대상 프로젝트의 `.asset-vault/library/`와 `assets/_vault_local/` 운영 규칙

Aseprite 자체가 없으면 브리지를 설치해도 `doctor`는 `ASEPRITE_UNAVAILABLE`로 실패한다.

# Windows 설치 — 권장 경로

## 1. Aseprite.exe 위치 확인

### 공식 설치본의 일반 경로

```text
C:\Program Files\Aseprite\Aseprite.exe
C:\Program Files (x86)\Aseprite\Aseprite.exe
%LOCALAPPDATA%\Programs\Aseprite\Aseprite.exe
```

### Steam 기본 경로

```text
C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe
```

Steam 라이브러리를 다른 드라이브에 설치했다면 다음 순서로 정확한 경로를 찾는다.

```text
Steam
→ 라이브러리
→ Aseprite 우클릭
→ 관리(Manage)
→ 로컬 파일 보기(Browse local files)
→ 열린 폴더의 Aseprite.exe 확인
```

## 2. 프로젝트 Asset Vault 초기화

대상 게임 저장소에서 아직 Asset Vault를 초기화하지 않았다면 Base의 도구를 사용한다.

```powershell
Set-Location "C:\GitHub\내게임프로젝트"
python "C:\GitHub\Base\tools\project_asset_vault.py" init --project-root .
```

다음 경로가 만들어져야 한다.

```text
.asset-vault/library/       # 로컬 후보 원본과 생성 결과의 권위
assets/_vault_local/        # Godot이 볼 수 있는 로컬 파생 작업면
```

두 경로는 로컬 전용이며 기본적으로 Git에 커밋하지 않는다.

## 3. 설치 스크립트 실행

새 PowerShell 창을 열고 아래 경로를 실제 경로로 바꾼다.

```powershell
$ErrorActionPreference = "Stop"
Set-Location "C:\GitHub\Base"

& ".\tools\aseprite-local-bridge\windows\Install_Aseprite_Local_Bridge.ps1" `
  -ProjectRoot "C:\GitHub\내게임프로젝트" `
  -AsepritePath "C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe"
```

스크립트는 다음만 수행한다.

1. Python 3.11 이상 탐색
2. 사용 중인 Base 체크아웃의 `run_bridge.py` 경로를 확인
3. 기존 `.aseprite-bridge.json`이 없을 때만 예제 설정 복사
4. 프로젝트의 로컬 전용 `.asset-vault/tools/Aseprite_Local_Bridge.ps1` launcher 생성
5. 현재 PowerShell 프로세스에만 `ASEPRITE_PATH` 설정
6. launcher가 사용할 Python·Base runner·프로젝트·Aseprite 경로를 고정
7. 같은 runner로 `doctor` 실행

`pip`, 네트워크 다운로드, Python `PATH`, 사용자 site-packages 등록은 사용하지 않는다. 기존 프로젝트 설정은 덮어쓰지 않는다. Base 폴더나 Aseprite 설치 위치를 이동하면 설치 스크립트를 다시 실행해 launcher를 갱신한다.

### ASEPRITE_PATH를 Windows 사용자 환경 변수로 저장할 때만

```powershell
& ".\tools\aseprite-local-bridge\windows\Install_Aseprite_Local_Bridge.ps1" `
  -ProjectRoot "C:\GitHub\내게임프로젝트" `
  -AsepritePath "D:\SteamLibrary\steamapps\common\Aseprite\Aseprite.exe" `
  -PersistAsepritePath
```

`-PersistAsepritePath`를 생략하면 영구 환경 변수는 만들지 않는다. 경로가 바뀌거나 Steam 라이브러리를 이동했을 때는 다시 실행한다.

## 4. 설치 결과 확인

성공 시 마지막 줄 근처에 JSON 한 줄이 출력된다.

```json
{
  "status": "PASS",
  "operation": "doctor",
  "aseprite_version": "Aseprite 1.3.x",
  "evidence_ceiling": "ASEPRITE_CALLABLE_ONLY_NO_ASSET_EXPORT_NO_GODOT_RUNTIME"
}
```

이 상태가 증명하는 것은 **Aseprite CLI를 호출할 수 있음**뿐이다. 아직 실제 자산 export, Godot import, 인게임 표시를 증명하지 않는다.

# 수동 실행 — 설치 없이 사용

설치 스크립트를 쓰지 않아도 네트워크나 추가 Python 패키지는 필요하지 않다. Base에 포함된 `run_bridge.py`를 직접 실행한다.

```powershell
$ErrorActionPreference = "Stop"
$Bridge = "C:\GitHub\Base\tools\aseprite-local-bridge\run_bridge.py"
$Aseprite = "C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe"

Set-Location "C:\GitHub\내게임프로젝트"
if (-not (Test-Path ".\.aseprite-bridge.json")) {
  Copy-Item `
    "C:\GitHub\Base\tools\aseprite-local-bridge\bridge_config.example.json" `
    ".\.aseprite-bridge.json"
}

py -3.12 $Bridge doctor --project-root . --aseprite $Aseprite
```

`py -3.12`가 없지만 Python 3.11 이상이 설치되어 있다면 `py -3.11` 또는 `python`으로 바꾼다. `run_bridge.py`가 자신의 `src`만 로드하므로 Python 전역·사용자 환경을 변경하지 않는다.

설치 스크립트를 실행한 뒤에는 프로젝트 로컬 launcher를 사용한다.

```powershell
Set-Location "C:\GitHub\내게임프로젝트"
$Bridge = ".\.asset-vault\tools\Aseprite_Local_Bridge.ps1"
& $Bridge doctor
```

`pyproject.toml`과 console script는 개발자 패키징 호환성을 위해 제공하지만, 기본 Windows 경로는 `pip`나 네트워크 다운로드를 사용하지 않는다.

# 프로젝트 설정

프로젝트 루트의 `.aseprite-bridge.json` 기본값은 다음과 같다.

```json
{
  "schema_version": 1,
  "source_roots": [".asset-vault/library"],
  "candidate_output_root": ".asset-vault/library/aseprite-generated",
  "allowed_source_extensions": [".aseprite", ".ase"],
  "sheet_type": "rows",
  "border_padding": 0,
  "shape_padding": 1,
  "inner_padding": 0,
  "timeout_seconds": 60,
  "use_noinapp": true
}
```

## 설정 의미

| 키 | 의미 |
|---|---|
| `source_roots` | 읽을 수 있는 프로젝트 내부 원본 루트 |
| `candidate_output_root` | 쓸 수 있는 유일한 후보 출력 루트 |
| `allowed_source_extensions` | 입력으로 허용하는 Aseprite 원본 확장자 |
| `sheet_type` | `horizontal`, `vertical`, `rows`, `columns`, `packed` 중 하나 |
| `border_padding` | 시트 외곽 여백 |
| `shape_padding` | 프레임 사이 여백 |
| `inner_padding` | 각 프레임 내부 여백 |
| `timeout_seconds` | 한 번의 Aseprite 호출 제한 시간 |
| `use_noinapp` | Windows에서 기존 GUI 인스턴스 전달을 피하고 CLI 실행을 분리하는 옵션 |

안전 규칙:

- 모든 경로는 프로젝트 상대 경로여야 한다.
- `candidate_output_root`는 `source_roots` 중 하나의 **하위 폴더**여야 한다.
- `..` 또는 심볼릭 링크로 프로젝트 밖으로 나가면 실패한다.
- 자산 ID는 대문자 영문·숫자·`_`·`-`만 허용하며 1~64자다.
- 기존 후보는 `--replace-candidate`가 없으면 덮어쓰지 않는다.
- receipt에는 절대 사용자 경로를 기록하지 않는다.

# 실제 사용 순서

## 1. disposable 원본 배치

사용자 원본을 바로 덮어쓰지 말고 프로젝트 후보 폴더 아래에 복사본을 둔다.

```text
C:\GitHub\내게임프로젝트\.asset-vault\library\aseprite-sources\hero.aseprite
```

PowerShell 예시:

```powershell
Set-Location "C:\GitHub\내게임프로젝트"
New-Item -ItemType Directory -Force ".asset-vault\library\aseprite-sources" | Out-Null
Copy-Item "C:\작업원본\hero.aseprite" ".asset-vault\library\aseprite-sources\hero.aseprite"
```

## 2. Aseprite 호출 상태 확인

```powershell
$Bridge = ".\.asset-vault\tools\Aseprite_Local_Bridge.ps1"
& $Bridge doctor
```

설치 스크립트를 사용하지 않는 직접 실행은 다음과 같다.

```powershell
$BridgeRunner = "C:\GitHub\Base\tools\aseprite-local-bridge\run_bridge.py"
py -3.12 $BridgeRunner doctor `
  --project-root . `
  --aseprite "D:\SteamLibrary\steamapps\common\Aseprite\Aseprite.exe"
```

## 3. layer/tag/slice 점검

```powershell
& $Bridge inspect `
  --source ".asset-vault/library/aseprite-sources/hero.aseprite"
```

예상 결과에는 다음이 포함된다.

- 원본 상대 경로
- 원본 SHA-256
- 파일 크기
- layer hierarchy
- animation tags
- slices

원하는 애니메이션이 태그로 분리되지 않았거나 layer 이름이 프로젝트 규칙과 다르면 Aseprite에서 먼저 교정한다.

## 4. 후보 export

```powershell
& $Bridge export-candidate `
  --source ".asset-vault/library/aseprite-sources/hero.aseprite" `
  --asset-id "HERO_IDLE_01"
```

생성 위치:

```text
.asset-vault/library/aseprite-generated/HERO_IDLE_01/
├ HERO_IDLE_01.png
├ HERO_IDLE_01.json
└ HERO_IDLE_01.receipt.json
```

기존 후보를 명시적으로 교체할 때만 다음 플래그를 추가한다.

```powershell
& $Bridge export-candidate `
  --source ".asset-vault/library/aseprite-sources/hero.aseprite" `
  --asset-id "HERO_IDLE_01" `
  --replace-candidate
```

교체는 새 결과를 임시 폴더에서 먼저 검증한 뒤 후보 폴더 단위로 수행된다.

## 5. 독립 readback 검증

```powershell
& $Bridge validate-candidate --asset-id "HERO_IDLE_01"
```

다음 중 하나라도 바뀌면 실패한다.

- `.aseprite` 원본 해시/크기
- PNG 해시/크기 또는 PNG signature
- JSON 해시/크기 또는 `frames`
- receipt의 자산 ID·경로·evidence ceiling

## 6. Asset Vault를 Godot 로컬 작업면으로 동기화

브리지는 Asset Vault의 두 번째 writer가 되지 않으므로 `assets/_vault_local`에 직접 쓰지 않는다. 기존 owner를 호출한다.

```powershell
python "C:\GitHub\Base\tools\project_asset_vault.py" sync --project-root .
```

기본 Asset Vault 설정에서는 이미지 확장자만 동기화하므로 다음 PNG가 Godot에 보인다.

```text
assets/_vault_local/aseprite-generated/HERO_IDLE_01/HERO_IDLE_01.png
```

`HERO_IDLE_01.json`과 receipt는 `.asset-vault/library`에 남아 검토·증거 입력으로 사용된다. JSON을 실제 런타임 consumer가 필요로 한다면 대상 프로젝트의 최신 `AGENTS.md`, 기존 importer, `PROJECT_ASSET_VAULT.json` 지원 확장자, 데이터 owner를 먼저 확인한 뒤 별도 승인된 경로로 추적한다. receipt 자체를 런타임 자산으로 승격하지 않는다.

## 7. Godot에서 후보 확인

이 단계에서는 아직 로컬 후보다.

- FileSystem dock에서 `res://assets/_vault_local/aseprite-generated/...png`가 import되는지 확인
- 픽셀아트 texture filter 설정 확인
- 기존 `SpriteFrames`, `AnimatedSprite2D`, `AnimationPlayer` 또는 프로젝트 importer와 연결 가능성 확인
- 실제 씬에서 프레임 순서·pivot·속도·투명 배경·스케일 확인

HiGodot이 해당 프로젝트의 persistent Godot authoring authority라면 Scene/Resource 연결은 HiGodot 경로로 수행한다. Aseprite 브리지는 Godot 파일을 수정하지 않는다.

## 8. 사용자 승인 뒤 PNG 승격

사용자가 후보를 `PROJECT_ASSET_APPROVED`로 확정한 뒤에만 실행한다.

```powershell
python "C:\GitHub\Base\tools\project_asset_vault.py" promote `
  --project-root . `
  --source-key "aseprite-generated/HERO_IDLE_01/HERO_IDLE_01.png" `
  --target "approved/characters/hero/HERO_IDLE_01.png"
```

이 명령은 기본 설정에서 다음 tracked 경로를 만든다.

```text
assets/approved/characters/hero/HERO_IDLE_01.png
```

그 다음에만 다음을 수행한다.

1. `ASSET_MANIFEST.yml`에 provenance·SHA-256·consumer·승인 상태 기록
2. Godot Scene/Resource 참조를 tracked 경로로 변경
3. 로컬 후보 경로 참조 검사
4. 자동 테스트
5. 실제 게임 실행과 캡처
6. `RUNTIME_VERIFIED`와 사용자 승인을 별도 기록

```powershell
python "C:\GitHub\Base\tools\project_asset_vault.py" check --project-root .
```

# Codex에 맡길 때 사용할 지시 예시

```text
대상 저장소 최신 AGENTS.md와 bootstrap/read order를 먼저 fresh-read해.
Aseprite 자산 후보는 .asset-vault/library의 현재 파일을 source of truth로 사용해.

1. aseprite-local-bridge doctor를 실행하고 exact Aseprite version을 기록해.
2. 지정된 .aseprite 원본을 inspect하여 layer/tag/slice와 SHA-256을 보고해.
3. 기존 후보를 임의로 덮어쓰지 말고 ASSET_ID로 export-candidate를 실행해.
4. validate-candidate readback을 실행해.
5. project_asset_vault.py sync로 Godot 로컬 작업면에 투영해.
6. 사용자 승인 전에는 promote, ASSET_MANIFEST 등록, tracked Scene/Resource 연결을 하지 마.
7. Aseprite runtime, Godot runtime, UX/Human, USER_APPROVED를 각각 분리해서 보고해.
```

# Codex MCP와의 관계

현재 권장 경로는 **Codex 로컬 shell → 이 CLI**다. Codex는 로컬 MCP 서버도 등록할 수 있지만, phase 1에서는 별도 서버를 추가하지 않는다.

향후 실제 프로젝트에서 반복 사용이 확인되면 다음 네 도구만 노출하는 bounded STDIO MCP를 검토한다.

```text
doctor
inspect
export_candidate
validate_candidate
```

프로젝트별 `.codex/config.toml`, `enabled_tools`, write approval, exact version pin이 필수이며 raw Lua나 generic command 도구는 추가하지 않는다. 공식 Codex MCP 문서: https://developers.openai.com/codex/mcp

# 검토한 커뮤니티 MCP

다음은 자동 설치 대상이 아니라 `REFERENCE_ONLY / TRIAL_CANDIDATE`다.

| 후보 | 장점 | 기본 채택하지 않는 이유 |
|---|---|---|
| https://github.com/giangdvdotdev/aseprite-mcp | Python+Lua extension, 실행 중 Aseprite 직접 조작, 약 30개 도구 | localhost WebSocket 무인증, 로컬의 다른 프로세스가 연결 가능, 절대 경로 export/overwrite 범위 |
| https://github.com/bachhoang0606/aseprite-mcp | live-first, preview/ascii/filmstrip, raw Lua/CLI 기본 off | Rust build+별도 bridge+extension, 장기 실행 구성과 공급망 검증 필요 |
| https://github.com/diivi/aseprite-mcp | 광범위한 drawing/animation/palette/analysis 기능 | 100개 이상 도구와 raw Lua escape hatch로 권한·컨텍스트 표면이 큼 |
| https://github.com/mattt/aseprite-mcp | 두 도구만 사용하는 단순 STDIO 구조, workspace 제한 | `execute_lua`가 샌드박스되지 않아 파일 시스템 전체 접근 가능 |

실시간 편집이 실제로 필요한 프로젝트에서만 별도 branch/canary로 exact release를 pin하고, source review·license·localhost threat model·output boundary·uninstall·Windows runtime을 검증한다.

# 문제 해결

## `ASEPRITE_UNAVAILABLE`

```text
원인: 실행 파일을 찾지 못함
조치: --aseprite 또는 ASEPRITE_PATH에 Aseprite.exe 전체 경로 지정
```

```powershell
& ".\.asset-vault\tools\Aseprite_Local_Bridge.ps1" doctor
```

## `CONFIG_NOT_FOUND`

```text
원인: 대상 프로젝트 루트에 .aseprite-bridge.json 없음
조치: bridge_config.example.json을 프로젝트 루트로 복사
```

## `SOURCE_OUTSIDE_ALLOWED_ROOTS`

```text
원인: 원본이 .asset-vault/library 밖에 있음
조치: 작업 복사본을 library 아래로 옮기거나, 프로젝트 승인 후 source_roots를 프로젝트 내부의 적절한 후보 경로로 수정
```

## `CANDIDATE_EXISTS`

기존 후보 보호 동작이다. 먼저 비교하고 실제 교체가 맞을 때만 `--replace-candidate`를 사용한다.

## `ASEPRITE_COMMAND_FAILED`

Aseprite 자체 stderr/stdout 일부가 `detail`로 나온다. 원본이 손상됐는지, 해당 버전에서 열리는지, output 경로 권한이 있는지 확인한다.

## `RECEIPT_MISMATCH`

원본 또는 출력이 export 뒤 바뀌었다. 기존 receipt를 수동으로 고치지 말고 원인을 확인한 뒤 새 asset ID로 다시 export하거나 명시적 교체를 수행한다.

## PowerShell에서 `py -3.12`를 찾지 못함

```powershell
python --version
py -0p
```

Python 3.11 이상이 보이면 명령의 `py -3.12`를 해당 launcher로 바꾼다. 설치가 없다면 https://www.python.org/downloads/windows/ 에서 설치한다.

# 제거와 롤백

프로젝트 로컬 launcher 제거:

```powershell
Remove-Item ".\.asset-vault\tools\Aseprite_Local_Bridge.ps1" -ErrorAction SilentlyContinue
```

개발자가 별도로 `pip` 설치 경로를 선택했던 경우에만 추가 제거한다.

```powershell
python -m pip uninstall aseprite-local-bridge
```

영구 `ASEPRITE_PATH`를 저장했던 경우 제거:

```powershell
[Environment]::SetEnvironmentVariable("ASEPRITE_PATH", $null, "User")
```

프로젝트 연결 제거:

```powershell
Remove-Item ".\.aseprite-bridge.json"
Remove-Item ".\.asset-vault\library\aseprite-generated" -Recurse
python "C:\GitHub\Base\tools\project_asset_vault.py" sync --project-root .
```

삭제 전 확인 사항:

- `.aseprite` 원본을 삭제하지 않는다.
- `assets/approved/...`의 tracked 승인 자산은 자동 삭제하지 않는다.
- `ASSET_MANIFEST.yml`과 실제 Scene/Resource consumer를 먼저 확인한다.
- 제거 뒤 `project_asset_vault.py check`와 Godot import/runtime 회귀를 별도로 수행한다.

# 검증 상태표

| 상태 | 의미 |
|---|---|
| `DOCUMENT_PASS` | 설계·가이드·경계가 정적 검토됨 |
| `AUTOMATED_TEST_PASS` | fake Aseprite 기반 path/export/receipt 테스트 통과 |
| `ASEPRITE_RUNTIME_PASS` | 사용자 PC의 licensed Aseprite로 실제 명령 통과 |
| `GODOT_RUNTIME_PASS` | exact project revision에서 실제 import·씬 실행·캡처 통과 |
| `UX_HUMAN_PASS` | 사람이 프레임·가독성·동작을 검수함 |
| `USER_APPROVED` | 후보 자산을 정본으로 쓰기로 명시 승인함 |

증거 상한:

```text
CLI_EXPORT_AND_READBACK_ONLY_NOT_GODOT_RUNTIME_NOT_HUMAN_APPROVAL
```
