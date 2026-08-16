# 프로젝트 로컬 이미지 보존소 정책

이 문서는 Base를 적용한 게임 프로젝트에서 **GPT 생성/다운로드·사용자 수동 추가 → 프로젝트별 로컬 보존소 → Godot 로컬 작업면 → 승인된 Repo 자산** 흐름을 운영하는 공용 책임 원본이다.

## 1. 핵심 원칙

- 프로젝트마다 보존소는 정확히 하나이며 기본 경로는 `<project-root>/.asset-vault/`다.
- 보존소 원본과 자동 동기화 상태는 **로컬 전용**이다. GitHub에 commit하지 않는다.
- `.asset-vault/library/`의 현재 파일시스템 상태가 활성 로컬 후보의 최우선 권위(`local-vault-filesystem`)다.
- 사용자가 `library/`에 이미지를 직접 추가하면 다음 동기화에서 Godot 로컬 작업면에 반영한다.
- 사용자가 `library/`에서 이미지를 삭제하거나 `.asset-vault/archive/`로 이동하면 다음 동기화에서 해당 로컬 작업 복사본을 제거한다.
- 삭제한 bytes는 SHA-256 tombstone으로 기록하여 파일명·mtime만 바뀐 과거 다운로드가 자동 부활시키지 못하게 한다.
- 사용자가 같은 bytes를 `library/`에 직접 다시 넣는 행위는 명시적 재도입으로 간주하고 tombstone을 해제한다.
- `GENERATED_EXPLORATION`, `IN_REVIEW`, `APPROVED_CANDIDATE`는 Repo 자산이 아니다. **`PROJECT_ASSET_APPROVED` 이후의 명시적 `promote`만 tracked 자산을 만든다.**
- 이미 승격된 tracked 자산은 로컬 후보를 삭제했다고 자동 삭제하지 않는다. 폐기·교체는 별도 승인/자산 원장 절차를 따른다.
- `.asset-vault/harvest.json`은 재사용 후보의 분류·방법·해시를 연결하는 **local-only metadata**이며 이미지 bytes·제품 승인·복원 원본이 아니다.

## 2. 권위와 저장 위치

```text
ChatGPT 브라우저 다운로드 / 사용자 직접 추가 / 로컬 생성기
                    ↓ ingest
.asset-vault/                         # LOCAL ONLY, gitignored
├─ library/                           # 활성 로컬 후보의 유일한 파일 권위
├─ archive/                           # 사용 중지 원본을 로컬 보관할 선택 영역
├─ inbox/                             # 브라우저/도구 입력 대기 영역
├─ state.json                         # 다운로드 event·tombstone·이전 투영 상태
├─ sync.json                          # 현재 로컬 투영 결과
└─ harvest.json                       # 재사용 후보 분류·방법·content hash 연결, LOCAL ONLY
                    ↓ sync
assets/_vault_local/                  # LOCAL ONLY, gitignored, Godot-visible/importable
                    ↓ PROJECT_ASSET_APPROVED + promote
assets/<approved-path>/               # TRACKED, 장기 사용 자산
ASSET_MANIFEST.yml                    # TRACKED, 승인·의미·권리·용도 원장
Scene/Resource                        # TRACKED 자산 경로만 참조
```

`sync.json`은 파일 존재·해시·로컬 작업 경로를 기록하는 **로컬 기계 동기화 원장**이다. `harvest.json`은 Primary Use Gate 뒤 선별된 재사용 후보가 어떤 source/member bytes에서 왔는지 상대 경로와 SHA-256으로 연결하는 **로컬 재사용 검토 메타데이터**다. `ASSET_MANIFEST.yml`은 승인 상태·용도·시각 DNA·권리·검증을 기록하는 **tracked 의미/승인 원장**이다. 셋을 합치지 않는다.

원격 AI/Codex가 사용자의 로컬 `.asset-vault/`를 볼 수 없는 경우 Repo 상태가 더 최신이라고 추정하지 않고 `VAULT_LOCAL_STATE_UNVERIFIED`로 표시한다.

## 3. 왜 `.gdignore`가 아닌가

Godot 공식 Project organization 문서에 따르면 `.gdignore`가 있는 폴더는 FileSystem dock에서 숨겨지고 그 안의 리소스는 load/preload할 수 없다. 따라서 **사용자가 Godot 안에서 후보 이미지를 보고 씬 작업 참고자료로 쓸 수 있어야 하는 로컬 작업면에는 `.gdignore`를 사용하지 않는다.**

대신 `assets/_vault_local/`은 일반 Godot 프로젝트 폴더로 두어 import가 가능하게 하고 Git만 `.gitignore`로 제외한다. Godot import cache(`.godot/imported`)는 파생 상태이며 보존소 권위가 아니다.

공식 근거:

- https://docs.godotengine.org/en/latest/tutorials/best_practices/project_organization.html
- https://docs.godotengine.org/en/latest/tutorials/assets_pipeline/import_process.html

## 4. GPT 생성 → 로컬 보존 연결

### 4.1 ChatGPT 웹 사용

호스팅된 ChatGPT가 사용자의 임의 로컬 프로젝트 경로에 직접 파일을 쓸 수 있다고 가정하지 않는다. 기본 브리지는 프로젝트 로컬에서 실행되는 `tools/project_asset_vault.py watch`다.

```text
GPT 이미지 생성
→ 브라우저가 로컬 다운로드 폴더에 저장
→ local watch가 새 이미지 event만 감지
→ .asset-vault/library/gpt-imports/<date>/ 로 복사
→ 즉시 sync
→ assets/_vault_local/ 갱신
→ 사용자는 Godot/File Explorer에서 후보 확인
```

첫 감시는 기존 다운로드 파일을 **기준선으로만 기록**하고 기본적으로 가져오지 않는다. 감시 전에 있던 파일도 가져와야 할 때만 `--include-existing`을 사용한다. 전체 Downloads를 감시하면 작업과 무관한 새 이미지도 들어올 수 있으므로 가능하면 프로젝트 전용 다운로드 폴더를 사용한다.

### 4.2 완전 자동 보존이 필요한 경우

브라우저 다운로드 동작까지 없애려면 로컬 프로세스가 생성 API/파일 소스를 호출하여 `.asset-vault/inbox/` 또는 `library/`에 직접 저장하는 구조가 필요하다. 이 경우에도 Base의 권위는 동일하며 로컬 생성기가 `sync`를 호출한다.

API key·token·서비스 secret은 Repo, `PROJECT_ASSET_VAULT.json`, `ASSET_MANIFEST.yml`, prompt, 로그에 기록하지 않는다. 사용자의 로컬 secret store/environment만 사용한다. Base는 특정 이미지 생성 공급자를 기본 권위로 강제하지 않는다.

## 5. 동기화 계약

`tools/project_asset_vault.py sync`는 Manifest나 Harvest metadata를 복원 원본으로 사용하지 않고 매 실행마다 `library/`를 다시 스캔한다.

1. 지원 확장자의 현재 파일을 읽는다.
2. SHA-256과 `library/` 기준 상대 경로를 계산한다.
3. 같은 상대 경로로 `assets/_vault_local/`에 복사·갱신한다.
4. 이전 동기화에서 도구가 투영했던 경로 중 현재 `library/`에 없는 항목만 제거한다.
5. 제거/교체된 이전 bytes를 tombstone으로 기록한다.
6. 현재 `library/`에 다시 존재하는 bytes는 명시적 재도입으로 간주하여 tombstone을 해제한다.
7. 로컬 `.asset-vault/sync.json`을 재생성한다.
8. Manifest/state/Harvest metadata에는 사용자 PC 절대 경로를 프로젝트 공유 기록으로 노출하지 않는다.

보존소의 symlink는 활성 자산으로 허용하지 않는다. `.crdownload`, `.part`, `.tmp` 같은 미완료 다운로드와 지원하지 않는 확장자는 가져오지 않는다.

### 5.1 Reusable Visual Harvest metadata

`record-harvest`는 이미 존재하는 `library/` source와 선택된 member files를 **분류·연결**한다. 이미지 분할·mask 생성·inpainting·복원·Figma mutation·Godot authoring을 수행하지 않는다.

```text
Primary Use Gate accepted
→ Reusable Visual Harvest Gate
→ source/member가 .asset-vault/library에 실제 존재하는지 재검증
→ 상대 source_key + SHA-256 기록
→ .asset-vault/harvest.json
```

지원 분류:

```text
REUSE_AS_IS
VARIANT_SEED
STRUCTURE_PATTERN
STYLE_DNA
REBUILD_FOR_REUSE
ONE_OFF_KEEP
REJECT_REUSE
```

지원 분리·재구축 provenance:

```text
SOURCE_LAYER
MASK_CUTOUT
MANUAL_OR_SEMANTIC_REBUILD
DERIVED_GENERATIVE_RECOVERY
```

`DERIVED_GENERATIVE_RECOVERY`는 가려진 부분을 생성적으로 복원한 결과처럼 원본에서 직접 관측되지 않은 픽셀을 포함한다는 뜻이다. `contains_derived_generated_pixels=true`로 기록하며 원본 사실로 취급하지 않는다.

다음 세 경계는 동일하지 않다.

```text
record-harvest != image decomposition
record-harvest != PROJECT_ASSET_APPROVED
record-harvest != promote
```

`harvest.json` record의 기본 상태는 `review_status: IN_REVIEW`, `project_asset_approved: false`다. 이 metadata는 `asset_vault_harvest_record_id`로 Figma/이미지 검토 기록에서 참조할 수 있지만, 역으로 Figma나 계획 문서가 local bytes의 존재를 만들어내지 않는다.

사용자가 `library/`에서 source/member를 삭제하거나 archive로 이동해도 `harvest.json`이 파일을 복원하지 않는다. 현재 `library/` 파일시스템이 계속 최우선 권위이며, 해당 Harvest record는 과거 해시를 설명하는 stale/inert metadata가 될 수 있다. 같은 bytes의 명시적 재도입은 기존 tombstone 규칙을 그대로 따른다.

예시:

```powershell
python tools/project_asset_vault.py record-harvest --project-root . `
  --record-id "HARVEST-UI-001" `
  --source-key "gpt-imports/2026-08-16/ui-screen.png" `
  --classification "REBUILD_FOR_REUSE" `
  --method "MANUAL_OR_SEMANTIC_REBUILD"
```

member file이 실제로 있다면 `--member-key "<library-relative-path>"`를 반복해서 추가한다. 브라우저 파일명이나 사용자 PC 절대 경로를 authoritative path로 기록하지 않는다.

## 6. 승인과 Repo 승격

로컬 후보를 Repo/제품 자산으로 만드는 경계는 자동 `sync`나 `record-harvest`가 아니라 **명시적 `promote`**다.

```text
GENERATED_EXPLORATION / IN_REVIEW / APPROVED_CANDIDATE
→ .asset-vault/library + assets/_vault_local 에서 검토
→ 권리·유사성·규격·실제 화면 검수
→ PROJECT_ASSET_APPROVED
→ promote
→ assets/<approved-path>/
→ ASSET_MANIFEST.yml·provenance·관련 정본 갱신
→ Scene/Resource tracked 경로 연결
→ APPLIED_AND_RUNTIME_VERIFIED
```

예시:

```powershell
python tools/project_asset_vault.py promote --project-root . `
  --source-key "gpt-imports/2026-08-08/ui-button.png" `
  --target "approved/ui/ui-button.png"
```

`promotion_root` 기본값은 `assets`이므로 위 결과는 `assets/approved/ui/ui-button.png`다. 기존 target에 다른 bytes가 있으면 덮어쓰지 않고 fail closed한다.

tracked Godot Scene/Resource가 `res://assets/_vault_local/...`를 참조하면 로컬 PC가 아닌 환경에서 깨진다. PR/commit 전 다음을 실행한다.

```powershell
python tools/project_asset_vault.py check --project-root .
```

`check` 실패는 해당 후보를 먼저 승인·승격하고 씬 참조를 tracked 경로로 바꾸라는 뜻이다.

## 7. 사용자 수동 편집 우선순위

```text
사용자가 library에 추가
→ sync에서 신규 로컬 Godot 후보 생성

사용자가 library에서 삭제
→ sync에서 기존 로컬 작업 복사본 제거
→ 해당 bytes tombstone
→ rename/mtime 변경만으로 자동 부활 금지
→ harvest.json은 해당 파일을 복원하지 않음

사용자가 library → archive 이동
→ 활성 후보에서는 제거 + tombstone
→ 원본은 로컬 archive에 유지

사용자가 archive → library 이동 또는 같은 bytes를 직접 library에 재추가
→ 사용자의 명시적 재도입으로 tombstone 해제

이미 PROJECT_ASSET_APPROVED 후 promote된 tracked 자산
→ 로컬 후보 삭제와 독립적으로 유지
→ 폐기/교체는 ASSET_MANIFEST와 프로젝트 승인 절차로 수행
```

AI는 자산 작업을 시작할 때 로컬 접근 권한이 있으면 `library/` 현재 상태를 먼저 확인하고, 없으면 `VAULT_LOCAL_STATE_UNVERIFIED`를 유지한다. stale 대화 문맥·과거 `sync.json`·`harvest.json`·다운로드 폴더만 근거로 사용자가 삭제한 후보를 복원하지 않는다.

## 8. Godot 안에서 보존소를 보는 방법 — 기존 솔루션 우선

2026-08-08 벤치마킹에서 새 Asset Browser를 Base가 처음부터 만드는 것보다 기존 Godot 도구를 **표현/탐색 UI로 재사용하고 Base는 권위·수명주기만 소유**하는 편이 낫다고 판단했다.

### Global Asset Manager — `REUSE/TRIAL`

- Godot Asset Store의 MIT 애드온.
- 임의 로컬 폴더를 스캔하고 이미지·오디오 등 preview, tag, search를 제공한다.
- 선택 자산을 프로젝트 `res://assets/...`로 복사하는 기능도 제공한다.
- https://store.godotengine.org/asset/sn1ks0h/global-asset-manager/

권장 사용:

- `.asset-vault/library/`를 **browse/preview source**로 등록하는 것은 허용한다.
- 이 애드온은 Base의 승인 상태·tombstone·`ASSET_MANIFEST.yml`을 알지 못하므로 lifecycle authority가 아니다.
- 기본 운영에서는 애드온의 `Add to Project`를 승인 우회 경로로 사용하지 않는다. 제품 반영은 Base `promote`를 사용한다.
- 팀이 Add to Project를 쓰려면 그 동작을 `PROJECT_ASSET_APPROVED + promote`와 동등하게 묶는 별도 adapter 검증이 먼저 필요하다.

### 비교 후보 — `DEFER`

- Local Assets Browser: 로컬 폴더 탐색 기능은 적합하지만 GPLv3, Rust/SQLite 의존, unstable 표기로 기본 채택하지 않는다. https://store.godotengine.org/asset/kaifungamedev/asset-browser/
- AssetPlus: MIT이며 global library/package 관리에 유용하지만 프로젝트별 local authority·삭제 tombstone·승인 승격 책임과는 중심 목적이 다르므로 기본 채택하지 않는다. https://store.godotengine.org/asset/moongdev/assetplus/

결론은 **Base 도구 `ABSORB/REFACTOR` + Global Asset Manager `REUSE/TRIAL`**이다. 이 기능만을 위한 새 broad Skill은 추가하지 않는다. 기존 Godot 자산 평가·이미지 생성·적대적 검토 Skill이 소비한다.

## 9. v1 → v2 마이그레이션

v1은 `library → assets/_managed/`를 tracked 자동 미러로 사용했다. v2는 승인 전 후보를 Repo에서 분리하므로 기존 프로젝트를 기계적으로 삭제하지 않는다.

마이그레이션 순서:

1. 현재 `assets/_managed/`와 `assets/ASSET_VAULT_SYNC.json`의 Git 추적 여부를 확인한다.
2. Scene/Resource가 `_managed`를 참조하는지 inventory한다.
3. 실제 사용 중이며 승인된 자산만 durable `assets/<approved-path>/`로 옮기고 `ASSET_MANIFEST.yml`에 연결한다.
4. Scene/Resource 참조를 durable path로 변경한다.
5. v2 `PROJECT_ASSET_VAULT.json` 설치 후 `init`, `sync`, `check`를 실행한다.
6. 참조가 모두 제거된 뒤에만 구형 tracked `_managed`와 `assets/ASSET_VAULT_SYNC.json`을 제거한다.

`.gitignore`는 이미 Git이 추적 중인 파일을 자동 untrack하지 않는다. 따라서 migration audit 없이 구형 tracked 자산을 일괄 삭제하지 않는다.

## 10. 기본 명령

```powershell
# 프로젝트 최초 1회
python tools/project_asset_vault.py init --project-root .

# 사용자가 library를 직접 추가/삭제한 뒤
python tools/project_asset_vault.py sync --project-root .

# 현재 세션부터 새로 내려받는 이미지를 자동 연결
python tools/project_asset_vault.py watch --project-root . --source "$env:USERPROFILE\Downloads"

# 감시 시작 전 이미 존재한 이미지까지 포함해야 할 때만
python tools/project_asset_vault.py pull-downloads --project-root . --source "$env:USERPROFILE\Downloads" --include-existing

# Primary Use 뒤 재사용 후보의 local-only 분류/provenance 기록
python tools/project_asset_vault.py record-harvest --project-root . --record-id "<harvest-id>" --source-key "<library-relative-path>" --classification "<classification>" --method "<method>"

# 승인된 후보만 tracked 자산으로 승격
python tools/project_asset_vault.py promote --project-root . --source-key "<library-relative-path>" --target "<assets-relative-target>"

# tracked/project Godot 파일이 local-only 후보를 참조하는지 검사
python tools/project_asset_vault.py check --project-root .
```

## 11. 검증 기준

- [ ] 프로젝트마다 로컬 보존소가 하나만 존재한다.
- [ ] `.asset-vault/`와 `assets/_vault_local/`이 Git에서 제외된다.
- [ ] `.gdignore`로 후보를 숨기지 않아 Godot가 로컬 작업면을 import/preview할 수 있다.
- [ ] 수동 추가가 `assets/_vault_local/`에 반영된다.
- [ ] 수동 삭제/archive 이동이 다음 sync에서 로컬 복사본 제거와 tombstone으로 반영된다.
- [ ] 삭제 bytes가 rename/mtime 변경·stale download event 때문에 자동 부활하지 않는다.
- [ ] `harvest.json`이 삭제된 source/member를 복원하거나 active library 권위를 대체하지 않는다.
- [ ] `harvest.json`에는 source/member의 library-relative key와 SHA-256만 기록하며 사용자 PC 절대 경로를 저장하지 않는다.
- [ ] `DERIVED_GENERATIVE_RECOVERY`는 generated/derived pixel provenance로 명시된다.
- [ ] 도구가 관리하지 않은 workspace 파일은 임의 삭제하지 않는다.
- [ ] 승인 전 후보가 tracked Repo 자산으로 자동 생성되지 않는다.
- [ ] `record-harvest`가 `sync`, `promote`, provider/Figma mutation을 암묵적으로 수행하지 않는다.
- [ ] `PROJECT_ASSET_APPROVED` 이후에만 `promote`로 tracked 자산을 만든다.
- [ ] tracked Godot Scene/Resource가 `assets/_vault_local/`를 참조하지 않는다.
- [ ] `ASSET_MANIFEST.yml`이 승격된 자산의 의미·권리·승인 상태를 소유한다.
- [ ] 로컬 vault를 볼 수 없는 원격 작업자는 `VAULT_LOCAL_STATE_UNVERIFIED`를 유지한다.
- [ ] 실제 Godot import/runtime 검증은 구성된 Godot 환경에서 별도로 수행한다.
