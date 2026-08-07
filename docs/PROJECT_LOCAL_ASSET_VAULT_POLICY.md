# 프로젝트 로컬 이미지 보존소 정책

이 문서는 Base를 적용한 게임 프로젝트에서 **GPT 생성/다운로드 → 프로젝트별 로컬 보존소 → Godot 관리 자산 → GitHub Repo** 흐름을 운영하는 공용 책임 원본이다.

## 1. 핵심 원칙

- 프로젝트마다 보존소는 정확히 하나이며 기본 경로는 `<project-root>/.asset-vault/`다.
- 보존소는 **로컬 전용**이다. 원본 이미지, 다운로드 처리 기록, 로컬 경로는 GitHub에 commit하지 않는다.
- `.asset-vault/library/`의 현재 파일시스템 상태가 활성 이미지 집합의 최우선 권위(`local-vault-filesystem`)다.
- 사용자가 `library/`에 이미지를 직접 추가하면 다음 동기화에서 Godot 관리 영역에 반영한다.
- 사용자가 `library/`에서 이미지를 삭제하거나 `.asset-vault/archive/`로 이동하면 다음 동기화에서 해당 **관리 복사본만** 제거한다.
- 오래된 Manifest, GPT 대화 문맥, 다운로드 폴더의 이미 처리된 파일이 사용자가 제거한 이미지를 자동 복원해서는 안 된다.
- 사용자가 새 다운로드·새 파일 추가로 명시적으로 다시 들여온 자산은 새 입력으로 처리할 수 있다.

## 2. 권위와 저장 위치

```text
.asset-vault/                         # LOCAL ONLY, gitignored
├─ library/                           # 활성 자산의 유일한 로컬 기준
├─ archive/                           # 사용 중지 원본을 로컬 보관할 선택 영역
├─ inbox/                             # 브라우저/도구 입력 대기 영역
└─ state.json                         # 다운로드 처리·이전 관리 경로 로컬 상태

PROJECT_ASSET_VAULT.json              # TRACKED, repo-safe 설정
assets/_managed/                      # TRACKED, Godot가 읽는 관리 복사본
assets/ASSET_VAULT_SYNC.json          # TRACKED, repo-safe 자동 동기화 Manifest
ASSET_MANIFEST.yml                    # TRACKED, 승인·의미·용도 기록
```

`ASSET_VAULT_SYNC.json`은 파일 존재·해시·관리 경로를 기록하는 **기계 동기화 원장**이다. `ASSET_MANIFEST.yml`은 승인 상태·용도·시각 DNA·권리·검증을 기록하는 **의미/승인 원장**이다. 두 책임을 합치지 않는다.

## 3. GPT 생성 → 자동 다운로드 브리지

ChatGPT 웹 UI의 파일을 원격 GPT가 사용자의 로컬 디스크로 직접 저장할 수 있다고 가정하지 않는다. 자동 연결은 프로젝트 로컬에서 실행되는 `tools/project_asset_vault.py watch`가 담당한다.

```text
GPT 이미지 생성
→ 브라우저가 로컬 다운로드 폴더에 저장
→ local watch가 새 이미지 이벤트만 감지
→ .asset-vault/library/gpt-imports/<date>/ 로 복사
→ 즉시 sync
→ assets/_managed/ + ASSET_VAULT_SYNC.json 갱신
→ Godot import/runtime 확인
→ 승인된 변경만 GitHub PR에 포함
```

첫 감시는 기존 다운로드 파일을 **기준선으로만 기록**하고 기본적으로 가져오지 않는다. 따라서 감시 시작 전에 있던 무관한 이미지가 한꺼번에 보존소로 들어가지 않는다. 이미 존재하는 파일도 가져와야 할 때만 `--include-existing`을 사용한다.

이미 처리한 다운로드 이벤트는 `.asset-vault/state.json`에 로컬 기록한다. 사용자가 보존소에서 해당 이미지를 제거해도 같은 다운로드 이벤트를 다시 스캔하는 것만으로는 복원하지 않는다.

## 4. 동기화 계약

`tools/project_asset_vault.py sync`는 매 실행마다 Manifest가 아니라 `library/`를 다시 스캔한다.

1. 지원 확장자의 현재 파일을 읽는다.
2. SHA-256과 `library/` 기준 상대 경로를 계산한다.
3. 같은 상대 경로로 `assets/_managed/`에 복사·갱신한다.
4. 이전 동기화에서 관리했던 경로 중 현재 `library/`에 없는 항목만 제거한다.
5. 관리 영역에 사용자가 별도로 만든 미등록 파일은 임의 삭제하지 않는다.
6. repo-safe `assets/ASSET_VAULT_SYNC.json`을 재생성한다.
7. Manifest에는 사용자 PC 절대 경로를 기록하지 않는다.

보존소의 symlink는 활성 자산으로 허용하지 않는다. `.crdownload`, `.part`, `.tmp` 같은 미완료 다운로드와 지원하지 않는 확장자는 가져오지 않는다.

## 5. Godot 반영

- Godot 프로젝트는 보존소 원본을 직접 참조하지 않고 `assets/_managed/`만 참조한다.
- Godot의 import cache는 파생 상태이며 보존소 권위가 아니다.
- 씬·리소스가 제거된 관리 자산을 참조하면 동기화 후 runtime 검증에서 실패로 드러나야 하며, 삭제된 이미지를 몰래 복구하는 방식으로 해결하지 않는다.
- 원본 변환·리사이즈·압축이 필요하면 보존소 원본을 수정하지 않고 관리 파생 단계에서 수행한다.

## 6. GitHub 반영

GitHub에는 다음만 포함할 수 있다.

- `PROJECT_ASSET_VAULT.json`
- `tools/project_asset_vault.py`
- `docs/PROJECT_ASSET_VAULT.md` 또는 프로젝트별 동등 계약
- `assets/_managed/`의 현재 사용 자산
- `assets/ASSET_VAULT_SYNC.json`
- 승인/의미 원장과 관련 코드·씬·리소스

다음은 commit 금지다.

- `.asset-vault/` 전체
- 다운로드 폴더 절대 경로
- `.asset-vault/state.json`
- 브라우저 임시 다운로드

기본 운영은 **로컬 자동 가져오기·동기화까지만 자동화**하고 GitHub push/merge는 기존 프로젝트 PR·검증 규칙을 따른다. 단순 다운로드만으로 자동 commit/push하지 않는다.

## 7. 사용자 수동 편집 우선순위

```text
사용자가 library에 추가
→ sync에서 신규 관리 자산 생성

사용자가 library에서 삭제
→ sync에서 기존 관리 복사본 제거
→ 같은 과거 다운로드 이벤트로는 자동 부활 금지

사용자가 library → archive 이동
→ 활성 집합에서는 제거
→ 원본은 로컬 archive에 유지

사용자가 archive → library 이동 또는 새 다운로드
→ 명시적 재도입으로 처리
```

AI는 자산 작업을 시작할 때 `ASSET_VAULT_SYNC.json`과 실제 프로젝트 관리 경로를 확인하고, 로컬 접근 권한이 있는 경우에는 `library/` 현재 상태를 우선한다. 로컬 보존소에 접근할 수 없는 원격 작업자는 Manifest보다 더 최신이라고 추정하지 말고 `VAULT_LOCAL_STATE_UNVERIFIED`로 표시한다.

## 8. 기본 명령

```powershell
# 프로젝트 최초 1회
python tools/project_asset_vault.py init --project-root .

# 사용자가 library를 직접 추가/삭제한 뒤
python tools/project_asset_vault.py sync --project-root .

# 현재 세션부터 새로 내려받는 이미지를 자동 연결
python tools/project_asset_vault.py watch --project-root . --source "$env:USERPROFILE\Downloads"

# 감시 시작 전 이미 존재한 이미지까지 한 번에 포함해야 할 때만
python tools/project_asset_vault.py pull-downloads --project-root . --source "$env:USERPROFILE\Downloads" --include-existing
```

다운로드 폴더 전체를 감시하는 동안 다른 이미지도 새로 다운로드하면 함께 들어올 수 있다. 프로젝트 전용 다운로드 폴더 또는 `.asset-vault/inbox/`를 사용할 수 있으면 그 경로를 우선한다.

## 9. 검증 기준

- [ ] 프로젝트마다 로컬 보존소가 하나만 존재한다.
- [ ] `.asset-vault/`가 Git에서 제외된다.
- [ ] 수동 추가가 `assets/_managed/`에 반영된다.
- [ ] 수동 삭제/archive 이동이 다음 sync에서 관리 복사본 제거로 반영된다.
- [ ] 삭제된 자산이 stale Manifest나 이미 처리한 다운로드 때문에 부활하지 않는다.
- [ ] 관리되지 않은 파일은 삭제하지 않는다.
- [ ] `ASSET_VAULT_SYNC.json`에 절대 로컬 경로가 없다.
- [ ] Godot 실제 import/runtime가 현재 관리 자산과 일치한다.
- [ ] GitHub에는 보존소 원본이 아니라 현재 관리 자산과 repo-safe 기록만 들어간다.
