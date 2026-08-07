# 프로젝트 자산 보존소 적용 계약

Base 공용 정책은 `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`다. 프로젝트에 이 기능을 채택할 때 이 템플릿을 `docs/PROJECT_ASSET_VAULT.md`로 설치하고, `PROJECT_ASSET_VAULT.json`과 `tools/project_asset_vault.py`를 함께 적용한다.

## 프로젝트 설치 결과

```text
<project-root>/
├─ PROJECT_ASSET_VAULT.json            # tracked, v2 설정
├─ .asset-vault/                       # LOCAL ONLY, gitignored
│  ├─ library/                         # 활성 후보 원본 권위
│  ├─ archive/                         # 로컬 보류/미사용 원본
│  ├─ inbox/                           # 선택 입력 대기
│  ├─ state.json                       # event/tombstone/local state
│  └─ sync.json                        # local sync manifest
├─ assets/
│  ├─ _vault_local/                    # LOCAL ONLY, gitignored, Godot-visible
│  └─ <approved-path>/                 # TRACKED, promote된 제품 자산
├─ ASSET_MANIFEST.yml                  # tracked 승인·의미·권리 원장
└─ tools/project_asset_vault.py
```

## 권위 규칙

- 로컬 접근 가능 시 `.asset-vault/library/`의 현재 상태가 활성 로컬 후보 집합의 최우선 권위다.
- 사용자의 직접 추가·삭제·archive 이동은 다음 `sync`에서 반드시 반영한다.
- `.asset-vault/sync.json`은 이전 상태를 복원하는 원본이 아니라 현재 로컬 투영 결과를 설명하는 파생 원장이다.
- `ASSET_MANIFEST.yml`은 `PROJECT_ASSET_APPROVED` 이후 tracked 자산의 승인·의미·권리·검증 원장이며 자동 파일 미러링 원장과 합치지 않는다.
- 원격 AI가 로컬 보존소를 볼 수 없으면 `VAULT_LOCAL_STATE_UNVERIFIED`로 취급하고 Repo 상태가 로컬 후보보다 최신이라고 추정하지 않는다.

## GPT 생성 연결

ChatGPT 웹에서 생성한 이미지를 프로젝트와 연결할 때 기본 브리지는 로컬 watcher다.

```powershell
python tools/project_asset_vault.py watch --project-root . --source "$env:USERPROFILE\Downloads"
```

첫 실행은 기존 파일을 기준선으로 기록하고 이후 새 이미지 event만 `library/gpt-imports/<date>/`로 복사한다. 프로젝트 전용 다운로드 폴더를 사용할 수 있으면 전체 Downloads보다 우선한다.

호스팅된 ChatGPT가 임의 로컬 경로에 직접 저장한다고 가정하지 않는다. 브라우저 다운로드 동작까지 없애려면 로컬 생성/API 프로세스가 `.asset-vault/inbox/` 또는 `library/`에 저장하고 `sync`를 호출하게 한다. API key/token은 Repo나 자산 원장에 저장하지 않는다.

## 사용자 직접 편집

- 사용 후보 추가: `.asset-vault/library/` 아래 원하는 분류 폴더에 파일을 추가한다.
- 사용 중지: `library/`에서 삭제하거나 `.asset-vault/archive/`로 이동한다.
- 삭제/이동된 bytes는 tombstone되어 이름·mtime만 바뀐 다운로드로 자동 부활하지 않는다.
- 다시 사용: `archive/`에서 `library/`로 되돌리거나 같은 bytes를 직접 `library/`에 재추가한다. 이 직접 재도입은 tombstone을 해제한다.
- 변경 후 `python tools/project_asset_vault.py sync --project-root .`를 실행한다.

## Godot 로컬 작업면

- Godot가 후보를 preview/import할 경로는 `assets/_vault_local/`이다.
- `_vault_local`에는 `.gdignore`를 두지 않는다. `.gdignore`는 Godot FileSystem에서 숨기고 resource load/import도 막기 때문이다.
- `_vault_local`은 `.gitignore`로만 제외한다.
- 로컬 후보는 참고자료·비교·임시 배치에 사용할 수 있지만 tracked Scene/Resource의 장기 참조가 되어서는 안 된다.

Godot 안에서 더 편하게 보고 싶다면 Base 공용 정책의 벤치마킹 결과에 따라 `Global Asset Manager`를 `REUSE/TRIAL` browse/preview UI로 시험할 수 있다. 애드온은 lifecycle authority가 아니며 기본 `Add to Project` 동작으로 승인 경계를 우회하지 않는다.

## 승인과 Repo 승격

`GENERATED_EXPLORATION`, `IN_REVIEW`, `APPROVED_CANDIDATE`는 로컬 후보 상태다. `PROJECT_ASSET_APPROVED` 이후에만 다음처럼 승격한다.

```powershell
python tools/project_asset_vault.py promote --project-root . `
  --source-key "<library-relative-path>" `
  --target "<assets-relative-target>"
```

승격 후:

1. `ASSET_MANIFEST.yml`에 `vault_source_key`, tracked path, 승인/권리/용도를 기록한다.
2. Scene/Resource는 promoted tracked path를 참조한다.
3. 다음 검사를 통과시킨다.

```powershell
python tools/project_asset_vault.py check --project-root .
```

로컬 후보 삭제는 이미 promote된 tracked 자산을 자동 삭제하지 않는다. 제품 자산 폐기·교체는 별도 승인과 원장 갱신으로 처리한다.

## 작업 시작 체크

자산 영향이 있는 작업은 다음 순서로 확인한다.

```text
최신 사용자 지시
→ 로컬 접근 가능 여부
→ .asset-vault/library/ 현재 상태 (가능한 경우)
→ .asset-vault/sync.json (로컬 접근 가능한 경우)
→ ASSET_MANIFEST.yml 승인·의미 상태
→ promoted assets 경로
→ Godot 실제 참조·import/runtime
→ Git diff·PR 범위
```

사용자가 보존소에서 제거한 파일을 stale 문맥이나 이전 Manifest만 근거로 복원하지 않는다.

## v1 프로젝트 주의

기존 `assets/_managed/`와 `assets/ASSET_VAULT_SYNC.json`이 tracked 상태라면 v2 설치만으로 자동 untrack되지 않는다. 현재 Scene/Resource 참조와 승인 자산을 inventory하고, 승인된 사용 자산만 durable tracked path로 이동한 뒤 참조를 바꾸고 `check`를 통과시킨 다음 구형 tracked 경로를 제거한다.
