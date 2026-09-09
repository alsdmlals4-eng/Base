# Aseprite Local Bridge 적용 가이드

## 상태

```yaml
owner: tools/aseprite-local-bridge/README.md
adoption: CANDIDATE_FOR_PROJECT_TRIAL
asset_candidate_owner: docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md
godot_persistent_authoring_owner: docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md
final_repository_truth: Git
```

이 문서는 새 자산 정본이나 두 번째 Godot 저작 권위를 만들지 않는다. 기본 실행은 Base의 `run_bridge.py`와 프로젝트 로컬 `.asset-vault/tools/Aseprite_Local_Bridge.ps1`이며 Python 전역 설치를 요구하지 않는다. 사용법·명령·문제 해결의 상세 owner는 `tools/aseprite-local-bridge/README.md`다.

## 역할 경계

```text
Aseprite Local Bridge
→ .aseprite inspect
→ .asset-vault/library/aseprite-generated 에 PNG+JSON+receipt 생성
→ CLI readback evidence

Asset Vault
→ tools/project_asset_vault.py sync
→ assets/_vault_local 로 로컬 투영
→ PROJECT_ASSET_APPROVED 뒤 explicit promote

HiGodot
→ tracked Godot Scene/Resource persistent authoring

Godot/GUT/Hera/manual
→ import/test/runtime/screenshot evidence
```

브리지는 `assets/_vault_local`에 직접 쓰지 않는다. 그 경로는 Asset Vault가 `.asset-vault/library`에서 생성하는 로컬 파생 작업면이다.

## 프로젝트 채택 전 확인

대상 프로젝트 최신 `AGENTS.md`와 지정 read order를 먼저 읽고 다음을 확인한다.

- exact Godot version/renderer/platform
- 기존 addon·importer·`SpriteFrames`·`AnimationPlayer` 소비 구조
- `.asset-vault/library`와 `assets/_vault_local` 실제 설정
- `PROJECT_ASSET_VAULT.json` 지원 확장자
- 픽셀 필터·프레임 duration·pivot·slice/tag 규칙
- 승인 자산과 `ASSET_MANIFEST.yml`
- runtime 실행·캡처·회귀검사 진입점

프로젝트별 채택 기록은 `tools/aseprite-local-bridge/project_profile.example.json`을 복사해 실제 경로·version·consumer·검증 결과만 채운다.

## 최소 채택 흐름

```powershell
$Bridge = ".\.asset-vault\tools\Aseprite_Local_Bridge.ps1"

# 1. 연결 확인
& $Bridge doctor

# 2. 원본 구조 확인
& $Bridge inspect `
  --source ".asset-vault/library/aseprite-sources/hero.aseprite"

# 3. 후보 생성
& $Bridge export-candidate `
  --source ".asset-vault/library/aseprite-sources/hero.aseprite" `
  --asset-id "HERO_IDLE_01"

# 4. 독립 readback
& $Bridge validate-candidate --asset-id "HERO_IDLE_01"

# 5. 기존 owner를 통한 Godot 로컬 투영
python tools/project_asset_vault.py sync --project-root .
```

여기까지는 `GENERATED_CANDIDATE / REVIEWED` 후보 단계다. `PROJECT_ASSET_APPROVED`, tracked promotion, Godot consumer 연결, `RUNTIME_VERIFIED`, 사용자 승인은 각각 별도 Gate다.

## 승인과 승격

PNG 승격 예시:

```powershell
python tools/project_asset_vault.py promote --project-root . `
  --source-key "aseprite-generated/HERO_IDLE_01/HERO_IDLE_01.png" `
  --target "approved/characters/hero/HERO_IDLE_01.png"
```

실제 프로젝트가 Aseprite JSON을 runtime/authoring consumer로 사용해야 한다면 기본 이미지 보존소 규칙을 임의로 확장하지 않는다. 프로젝트의 데이터 owner와 import 설계를 먼저 확정하고, 필요한 JSON 또는 파생 `SpriteFrames`/`.tres`의 tracked 경로와 검증을 프로젝트 정본에 기록한다. receipt는 evidence이며 제품 runtime 자산이 아니다.

## 증거 상한

```text
DOCUMENT/STATIC/AUTOMATED_TEST
!= ASEPRITE_RUNTIME
!= GODOT_RUNTIME
!= UX_HUMAN
!= USER_APPROVED
```

브리지 receipt의 상한은 다음이다.

```text
CLI_EXPORT_AND_READBACK_ONLY_NOT_GODOT_RUNTIME_NOT_HUMAN_APPROVAL
```
