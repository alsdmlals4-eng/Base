# 프로젝트 자산 보존소 적용 계약

Base 공용 정책은 `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`다. 프로젝트에 이 기능을 채택할 때 이 템플릿을 `docs/PROJECT_ASSET_VAULT.md`로 설치하고, `PROJECT_ASSET_VAULT.json`과 `tools/project_asset_vault.py`를 함께 적용한다.

## 프로젝트 설치 결과

```text
<project-root>/
├─ PROJECT_ASSET_VAULT.json            # tracked
├─ .asset-vault/                       # local only, gitignored
│  ├─ library/                         # 활성 원본 기준
│  ├─ archive/                         # 로컬 보류/미사용 원본
│  ├─ inbox/                           # 선택 입력 대기
│  └─ state.json                       # local only
├─ assets/
│  ├─ _managed/                        # Godot/Repo 반영 자산
│  └─ ASSET_VAULT_SYNC.json            # repo-safe 자동 원장
└─ tools/project_asset_vault.py
```

## 권위 규칙

- 로컬 접근 가능 시 `.asset-vault/library/`의 현재 상태가 활성 이미지 집합의 최우선 권위다.
- 사용자의 직접 추가·삭제·archive 이동은 다음 `sync`에서 반드시 반영한다.
- `ASSET_VAULT_SYNC.json`은 이전 상태를 복원하는 원본이 아니라 현재 동기화 결과를 설명하는 파생 원장이다.
- `ASSET_MANIFEST.yml`은 승인·의미·검증 원장이며 자동 파일 미러링 원장과 합치지 않는다.
- 원격 AI가 로컬 보존소를 볼 수 없으면 `VAULT_LOCAL_STATE_UNVERIFIED`로 취급하고 repo 상태가 더 최신이라고 추정하지 않는다.

## GPT 생성 연결

프로젝트 작업 세션에서 자동 다운로드 브리지를 사용하려면 이미지 생성 전에 로컬 watcher를 실행한다.

```powershell
python tools/project_asset_vault.py watch --project-root . --source "$env:USERPROFILE\Downloads"
```

첫 실행은 기존 파일을 기준선으로 기록하고 이후 새 이미지 이벤트만 `library/gpt-imports/<date>/`로 복사한다. 프로젝트 전용 다운로드 폴더나 `.asset-vault/inbox/`를 사용할 수 있으면 전체 Downloads보다 우선한다.

## 사용자 직접 편집

- 사용 이미지 추가: `.asset-vault/library/` 아래 원하는 분류 폴더에 파일을 추가한다.
- 사용 중지: `library/`에서 삭제하거나 `.asset-vault/archive/`로 이동한다.
- 다시 사용: `archive/`에서 `library/`로 되돌리거나 새 파일/새 다운로드로 재도입한다.
- 변경 후 `python tools/project_asset_vault.py sync --project-root .`를 실행한다.

## Godot/Repo 규칙

- Godot 씬·리소스는 `.asset-vault/`를 직접 참조하지 않는다.
- Godot가 읽는 경로는 `assets/_managed/`다.
- 동기화 도구는 이전에 자신이 관리했다고 기록한 파일만 삭제하며, 다른 사용자 파일을 임의 삭제하지 않는다.
- Repo에는 `.asset-vault/`를 포함하지 않는다.
- 자동 다운로드만으로 commit/push/merge하지 않는다. 기존 프로젝트 PR·검증 게이트를 거친다.

## 작업 시작 체크

자산 영향이 있는 작업은 다음 순서로 확인한다.

```text
최신 사용자 지시
→ 로컬 접근 가능 여부
→ .asset-vault/library/ 현재 상태 (가능한 경우)
→ assets/ASSET_VAULT_SYNC.json
→ ASSET_MANIFEST.yml 승인·의미 상태
→ Godot 실제 참조·import/runtime
→ Git diff·PR 범위
```

사용자가 보존소에서 제거한 파일을 stale 문맥이나 이전 Manifest만 근거로 복원하지 않는다.
