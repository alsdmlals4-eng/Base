# Base Tool Hub 설계

## 1. 조건부 결정

권장 가설은 Base의 기존 `tools/tool-hub/` 하나를 유일한 Hub 진입점으로 유지하는 것이다. 이 허브는 여러 프로젝트와 공용 도구를 한 화면에서 선택하고, **검증된 기존 도구 프로세스를 프로젝트별로 분리 실행**하며, 준비·실행·차단 상태를 보여 주는 localhost 전용 런처다. PR #328/#329의 Tool Hub·QA·visual import baseline은 이 owner에 흡수됐고 별도 Tool Radar runtime·두 번째 Hub·marketplace·iframe은 만들지 않았다. 다만 실제 Windows 동시 실행 smoke가 통과하기 전에는 `HUB_LAUNCHER_ACCEPTED`로 판정하지 않는다. 실제 이미지 생성까지 포함한 `GENERATION_PRODUCT_READY`는 별도 승인된 production engine adapter, 실제 provider 샘플 smoke와 Figma placement evidence까지 통과해야 하며 현재 `BLOCKED_UNVERIFIED`다.

### 2026-08-13 Task 5 구현 readback

- 한 catalog가 선택한 프로젝트별 QA, Expression, Sprite child 상태를 독립 표시하고 server-returned authenticated loopback URL만 연다.
- Linux에서 공백 경로를 가진 두 임시 committed project fixture에 canonical Base Figma route와 committed project-owned anchor evidence를 구성했다. 두 Expression + 두 Sprite child는 네 고유 PID·port와 정확한 `(tool_id, project_id)` identity를 보고했다.
- Expression 2-candidate import/export, Sprite 4-frame `sprite_action` import/export, Sprite 4-frame `effect_stages` import/export가 project-local vault에서 통과했다. 모든 import/export public packet은 `subscription_handoff_import`, `INCLUDED_OR_LOCAL_HANDOFF`, `provider_call_made=false`였고 상대 프로젝트에 run/output path가 없었다.
- QA session/evidence packet vertical slice도 별도로 통과해 Android `DEFERRED_NOT_CONNECTED`를 보존했다.
- 이 증거는 Linux/import 자동 smoke다. Windows process tree, Android device, live Figma connector/upload/node, paid OpenAI/pinned provider 호출과 실제 AI 생성은 실행하지 않아 `BLOCKED_UNVERIFIED` 또는 `DEFERRED`다. Figma는 routing/placement surface일 뿐 Hub smoke 증거가 아니다.
- 다음 독립 vertical slice 후보는 `Balance & Scenario Lab`이다. 현재 catalog에 placeholder를 두거나 기존 Hub/Studio owner에 흡수하지 않는다.

허브는 이미지 생성 엔진, Sprite Animation Studio, Expression Studio, Figma 전달, Godot authoring 또는 프로젝트 자산 승인 책임을 다시 구현하지 않는다. 기존 owner와 실행 계약을 등록·호출하는 얇은 제어면만 소유한다.

```text
Base tracked code and manifests
  ├─ tools/tool-hub/                 # launcher and status UI
  ├─ tools/TOOL_REGISTRY.json        # reviewed tool definitions only
  ├─ tools/expression-studio/        # unchanged domain owner
  └─ tools/sprite-animation-studio/  # unchanged domain owner

machine-local configuration
  └─ local locator → absolute project root

selected project adapter
  └─ canonical project identity, Base pin, protected paths

selected project workspace
  ├─ approved source assets
  ├─ generated candidates and exports
  └─ project-local delivery packets

Figma
  └─ review, comparison, approval, and project-GPT placement surface
```

## 2. 승인 근거와 작업 계약

### Direction Anchor

공용 도구 코드는 Base에 한 벌만 유지하고, 각 프로젝트는 자신의 로컬 루트·출력·Figma 대상에만 결합한다. 한곳에서 실행할 수 있어야 하지만 도구의 실행 권위와 프로젝트 데이터는 합치지 않는다.

### Work Mode와 범위

- Work Mode: `BUILD_APPROVED / IMPLEMENTATION_IN_PROGRESS`
- 작업 수준: `L4`, 여러 프로젝트가 재사용하는 공용 실행 계층
- 현재 산출물: Phase 0/0.5 Studio·공용 계약 구현, production engine dependency 구현, Tool Hub Phase 1 설계·흡수 판정
- 현재 제외: 기존 Studio 대량 이동, 원격 호스팅, Figma 자동 mutation, 외부 도구 자동 설치
- 보호 대상: 기존 두 Studio의 프로젝트 격리, Figma registry, 프로젝트 로컬 자산 권위, API key 비기록, 기존 dirty worktree 변경

사용자는 2026-08-13 이 설계의 L4 BUILD와 Phase 0/0.5 진행을 명시적으로 승인했다. 승인은 구현 시작 권한이며 실제 production generation, Windows 동시 실행, Figma placement 또는 Hub acceptance 증거를 대신하지 않는다.

## 3. Base 현행 구조 분석

2026-08-12 로컬 tracked inventory 기준 Base에는 919개 파일이 있다.

| 영역 | tracked files | 현재 책임 |
|---|---:|---|
| `docs/` | 322 | 운영·정본·연구·설계·계획·증거 |
| `templates/` | 141 | 프로젝트 분화·조사·실행·검증 템플릿 |
| `tests/` | 128 | Base 계약·회귀 검증 |
| `skills/` | 102 | 32개 분야 Skill과 Registry·references |
| `tools/` | 91 | 검사기·생성기·로컬 Studio |
| `.github/` | 15 | CI·PR·운영 자동화 |

`tools/`에는 두 성격이 함께 있다.

1. 41개의 top-level Python checker/builder/adapter는 주로 문서·CI·운영 계약을 기계 검증한다.
2. `expression-studio`와 `sprite-animation-studio`는 독립 Python 패키지, FastAPI 서버, 브라우저 UI와 테스트를 가진 사용자용 localhost 애플리케이션이다.

따라서 모든 `tools/*.py`를 사용자 화면에 나열하거나 기존 파일을 새 폴더로 대량 이동하면 안 된다. Tool Hub의 기본 화면은 명시적으로 등록된 `HUMAN_INTERACTIVE` 도구만 보여 주고, checker/builder는 향후 실제 소비 요구가 생긴 경우에만 `INTERNAL_AUTOMATION`으로 별도 등록한다.

현행 정책과의 결합은 다음과 같다.

| 정본 | Tool Hub가 지킬 경계 |
|---|---|
| `AGENTS.md` | Existing Solution First, localhost, 미실행을 통과로 보고하지 않음 |
| `START_HERE.md` | 모든 Skill을 로드하지 않고 요청별 최소 owner로 라우팅 |
| `VISUAL_COLLABORATION_TOOL_POLICY.md` | Figma는 시각 작업면이며 실행·정본·Godot 증거가 아님 |
| `PROJECT_LOCAL_ASSET_VAULT_POLICY.md` | 후보와 출력은 프로젝트 로컬, 승격은 명시적 `promote` |
| `SPRITE_ANIMATION_STUDIO_ADOPTION_GUIDE.md` | Base는 도구 코드만, 프로젝트가 입력·출력·생성 실행·Figma 대상 소유 |
| `PROJECT_FIGMA_TARGET_REGISTRY.json` | project ID와 Figma target의 canonical routing, 로컬 경로 저장소가 아님 |
| BCP-026 (`SUBMITTED`, 미승인) | 비교 증거로만 사용. 허브는 프로젝트 제작 phase owner나 Godot/Codex/HiGodot 전용 실행환경 owner가 아님 |

## 4. Existing Solution First 판정

### 해결할 문제

- 사용자가 공용 도구의 위치와 실행 명령을 외우지 않아도 된다.
- 같은 기능 코드를 프로젝트마다 복사하지 않는다.
- 여러 프로젝트가 동시에 서로 다른 도구를 실행해도 입력·출력·Figma 대상이 섞이지 않는다.
- fake/simulated 엔진, 누락된 key, 포트 충돌, 죽은 프로세스를 실제 생성 성공으로 표시하지 않는다.
- 새 도구는 등록 한 건과 검증 계약으로 발견 가능해야 한다.

### 조사한 기존·외부 해법

| 사례 | 확인한 원리 | 적용 | 제외 |
|---|---|---|---|
| Unity Hub | 프로젝트와 Editor 설치를 한곳에서 관리하고 올바른 Editor로 연다 | 프로젝트 우선 탐색·실행기 분리 | 게임/자산 생성 책임을 Hub가 흡수하지 않음 |
| JetBrains Toolbox | 여러 도구 버전과 프로젝트를 한 화면에서 열고 rollback 가능성을 유지한다 | 하나의 진입점, 독립 도구 lifecycle | 모든 IDE 기능을 Toolbox 안에 재구현하지 않음 |
| Stability Matrix | 여러 생성 UI를 설치·실행하고 각 패키지 의존성을 분리하며 공용 자원만 선택적으로 공유한다 | launcher, health/status, package isolation | 모델 저장소까지 1차 범위에 통합하지 않음 |
| ComfyUI | 로컬 서버·API·재사용 가능한 workflow와 App Mode를 제공한다 | 미래 production engine adapter 후보, 검토 가능한 workflow | 현행 Studio를 node graph로 전면 재작성하지 않음 |
| ComfyUI-Manager | registry 기반 설치·활성화·비활성화와 hub 패턴 | 명시적 registry와 상태 | 외부 plugin 자동 설치는 1차 범위에서 제외 |
| Pinokio | 로컬 앱 launcher와 격리된 환경 | isolation과 provenance 교훈 | 임의 shell, 임의 URL 설치, 브라우저 입력 command 실행 금지 |

공식·1차 자료(2026-08-12 확인):

- Unity Hub: <https://docs.unity.com/en-us/hub>
- JetBrains Toolbox App: <https://www.jetbrains.com/toolbox-app/>
- Stability Matrix repository: <https://github.com/LykosAI/StabilityMatrix>
- ComfyUI documentation and repository: <https://docs.comfy.org/> · <https://github.com/Comfy-Org/ComfyUI>
- ComfyUI-Manager repository: <https://github.com/Comfy-Org/ComfyUI-Manager>
- Pinokio repository and script policy: <https://github.com/pinokiocomputer/pinokio>

공개 GitHub 페이지의 현재 채택 신호는 ComfyUI 127.0k stars/15.0k forks, ComfyUI-Manager 15.7k stars/2.4k forks, Stability Matrix 8.6k stars/588 forks, Pinokio 7.8k stars/789 forks다. 이는 다운로드 수나 제품 성공을 직접 증명하지 않지만, 로컬 생성 엔진·registry·launcher 패턴이 대규모 공개 사용자·기여자 집단에서 반복 채택되었다는 보조 지표다. Unity와 JetBrains 사례는 다운로드 수를 추정하지 않고 공식 제품 문서에 확인되는 현업 구조만 사용한다.

시장 비교에서 반복되는 성공 원리는 다음 세 가지다.

1. 사용자는 프로젝트와 도구를 한 화면에서 찾는다.
2. 실제 작업은 버전·패키지·프로젝트별로 분리된 실행기가 수행한다.
3. 확장성과 편의성이 커질수록 registry 신뢰, 설치 provenance, sandbox와 rollback이 제품 핵심이 된다.

Base는 첫 두 원리를 채택하고, 아직 필요하지 않은 제3자 설치 marketplace는 공급망 위험 때문에 보류한다.

### Disposition

```yaml
current_studios: REUSE
project_figma_registry_data: REUSE
duplicated_studio_figma_registry_loaders: REFACTOR_TO_ONE_OWNER
project_local_asset_vault: REUSE
hub_ui_and_process_supervision: BUILD_NEW_MINIMAL
shared_generation_engine_abstraction: DEFER
shared_model_or_asset_repository: DEFER
external_arbitrary_app_installer: ARCHIVE_AS_REFERENCE_ONLY
monolithic_studio_merge: REJECT
figma_native_execution_host: REJECT
remote_hosted_saas: DEFER
```

조건부 판정은 **`REUSE + REFACTOR + BUILD_NEW_MINIMAL`**이다. Base에 이미 사용자용 도구가 두 개 있지만 이를 안전하게 발견·동시 실행하는 owner는 없다. 외부 범용 launcher를 설치하면 임의 script 실행, 별도 패키지 관리, 프로젝트/Figma registry 이중화가 생긴다. 따라서 기존 Studio와 registry data는 재사용하고, 중복된 Figma parser·delivery contract를 먼저 단일 owner로 합친 뒤, Base registry에 고정된 도구만 실행하는 얇은 launcher만 신규 제작한다.

### 2026-08-13 중복 채팅 Tool Radar 후보 흡수 판정

사용자가 제공한 `Game Development Tool Radar` 정적 ZIP과 채팅 기록을 현재 Base·PR 상태와 대조했다. 정적 파일의 JavaScript 문법과 localhost HTTP 제공은 재현됐지만, 채팅이 주장한 canonical `catalog.json`, generator, schema, tests와 browser-smoke evidence는 ZIP에 없었다. ZIP의 `data.js`에는 28개 unique tool entry가 있으나 Hub 자체를 `base.external_game_development_tool_hub`와 `base.game_development_tool_radar` 두 ID로 중복 등록한다. GitHub same-goal 검색에서는 현재 PR #312 외 별도 Tool Radar/External HTML PR은 확인되지 않았다.

| 후보 요소 | 판정 | 흡수 방식 |
|---|---|---|
| 검색·카테고리·상태 필터·즐겨찾기 UI | `ADAPT` | `tools/tool-hub/`의 catalog 탭으로 흡수 |
| sprite splitter, image resize, JSON/SHA/diff 등 browser-local utility | `ADAPT_AFTER_TEST` | network·shell 없이 작동하는 capability로 개별 등록·테스트 |
| 브라우저 `localStorage` 후보 저장 | `ADAPT` | `UNVERIFIED_LOCAL_DRAFT`만 허용하고 registry 자동 승격 금지 |
| 외부 도구·discovery source 카드 | `DERIVED_VIEW_ONLY` | 기존 periodic source owner의 읽기 전용 projection으로 표시 |
| `data.js`의 도구 상태·명령·evidence | `EVIDENCE_ONLY` | Base current owner와 실제 smoke로 다시 생성; 정본으로 import 금지 |
| 두 Hub ID와 별도 external HTML owner | `REJECT_DUPLICATE_OWNER` | Base Tool Hub 하나로 통합하고 두 candidate ID는 채택하지 않음 |
| static `python -m http.server` process owner | `REJECT_AS_RUNTIME_OWNER` | Hub FastAPI가 같은-origin 정적 UI와 typed launcher를 함께 제공 |
| ZIP의 `READY/PASS/ACTIVE` 주장 | `BLOCKED_UNVERIFIED` | bundled browser harness·source generator 부재로 재검증 전 승격 금지 |

통합 후 한 화면은 세 종류를 명확히 분리한다.

1. `RUNNABLE`: reviewed `tools/TOOL_REGISTRY.json` entry와 typed adapter·health contract가 있는 도구.
2. `REFERENCE`: 외부 도구 또는 discovery source의 읽기 전용 카드. 실행·설치·승격 권위가 없다.
3. `UNVERIFIED_LOCAL_DRAFT`: 현재 브라우저 프로필의 임시 후보. Base 또는 프로젝트 파일을 수정하지 않는다.

`file://` 페이지와 별도 포트의 두 번째 허브는 유지하지 않는다. Hub의 authenticated localhost origin에서 catalog와 launcher를 함께 제공하되, catalog UI는 process argv·environment·project path를 만들 수 없고 launcher는 고정 typed adapter만 소비한다.

## 5. 대안 비교

| 대안 | 프로젝트 격리 | 실제 로컬 파일 작업 | 유지보수 | 보안 경계 | 확장성 | 판정 |
|---|---|---|---|---|---|---|
| A. registry 기반 localhost launcher | 높음 후보 | 높음 후보 | 중간~높음 후보 | 높음 후보 | 높음 후보 | **조건부 권장** |
| B. 두 Studio를 한 모놀리식 앱으로 병합 | 중간 | 높음 | 낮음 | 중간 | 낮음 | 제외 |
| C. 외부 클라우드 SaaS portal | 중간 | 낮음 | 중간 | 낮음~중간 | 높음 | 보류 |
| D. Figma plugin/page 안에서 실행 | 낮음 | 낮음 | 중간 | 중간 | 낮음 | 제외 |
| E. 문서 링크 모음만 제공 | 높음 | 낮음 | 높음 | 높음 | 낮음 | 불충분 |

A가 현재 가장 강한 가설인 이유는 “한곳”을 하나의 프로세스·데이터 저장소로 오해하지 않기 때문이다. 사용자가 보는 진입점은 하나지만 실제 Studio는 project ID에 immutable하게 결합된 별도 child process다. Clean environment, atomic port allocation과 Linux 네-process import smoke는 구현·실행됐지만 Windows process-tree, production adapter/provider, live Figma placement는 아직 없으므로 전체 다중 플랫폼·생성 제품 판정은 `BLOCKED_UNVERIFIED`다.

## 6. 소유권과 데이터 경계

### Tracked registry

`tools/TOOL_REGISTRY.json`은 코드 리뷰를 받은 고정 manifest다. 브라우저 요청이 실행 명령을 만들지 못하게 한다.

필수 필드 예시:

```json
{
  "schema_version": 1,
  "tools": [
    {
      "tool_id": "sprite-animation-studio",
      "display_name": "Sprite Animation Studio",
      "audience": "HUMAN_INTERACTIVE",
      "owner_path": "tools/sprite-animation-studio",
      "launch_adapter": "sprite_animation_studio",
      "health_path": "/api/status",
      "project_scoped": true,
      "capabilities": ["sprite_action", "pose_sequence", "effect_stages"],
      "production_engine_required_for_delivery": true
    }
  ]
}
```

`launch_adapter`는 Hub 코드에 구현된 고정 adapter ID다. registry에 raw command, shell fragment, API key, 절대 project path를 넣지 않는다.

registry edit도 실행 신뢰 경계다. 구현은 다음을 모두 강제한다.

- `shell=False`와 argv array만 사용한다.
- browser/request가 flag, environment, interpreter, owner path를 추가·교체할 수 없다.
- `owner_path`와 interpreter는 reviewed Base/tool root 아래의 expected realpath·hash·environment identity와 일치해야 한다.
- `..`, symlink escape, registry path replacement, interpreter substitution을 시작 직전에 다시 차단한다.
- schema는 `schemas/base-tool-registry-v1.schema.json`이 단일 owner가 되고 `$id`, version, migration policy를 가진다.
- `README.md`, `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`, validator, active Hub consumer와 compatibility tests가 같은 변경에서 연결돼야 한다.

### Machine-local project locator

Figma target registry와 별도로 기기 로컬 설정이 사용자가 붙인 local locator를 절대 project root에 매핑한다. 이 파일은 canonical project identity를 만들거나 수정하지 않는다.

```json
{
  "coc-fiction": {"project_root": "D:/games/coc-fiction"},
  "ten-paces-hidden-moves": {"project_root": "D:/games/ten-paces"}
}
```

- 저장 위치는 사용자 지정 `--project-config`를 우선하고 저장소 밖 OS user config 경로를 기본으로 한다.
- Base 또는 프로젝트 Git에 commit하지 않는다.
- UI와 API 응답에는 기본적으로 전체 절대 경로를 노출하지 않고 display name과 검증 상태만 보여 준다.
- 프로젝트 등록은 사용자가 선택한 exact root에서만 수행하고 resolved root와 locator metadata만 저장한다.
- Hub는 root 안의 canonical `skills/PROJECT_BASE_ADAPTER.json`을 읽고 `project.project_id`, repository, Base exact pin과 protected paths를 검증한다. adapter의 `validators` 문자열은 구조·표시 metadata일 뿐 Hub가 shell-parse하거나 실행하지 않는다. identity preflight는 Hub에 고정 등록된 reviewed Base validator adapter ID에 typed project root와 Base pin만 전달하고 `shell=False` argv로 실행한다. 프로젝트가 선언한 validator를 실행하는 기능은 별도 allowlisted adapter ID·schema·review 전에는 Phase 1 범위 밖이다.
- 현행 `project-base-adapter-v1`을 제자리에서 확장하지 않는다. Phase 0.5는 `project-base-adapter-v2`를 만들고 `project.project_id`를 `^[a-z0-9]+(?:-[a-z0-9]+)*$` 패턴의 필수 필드로 정의한다. builder, checker, template, adapter contract, README/Documentation Map, compatibility views와 tests를 같은 coordinated release에서 갱신한다.
- v1 adopter는 directory name, repository name, local locator 또는 Figma entry에서 ID를 추론하지 않는다. 프로젝트별 v2 migration과 exact-ID 검증 전 상태는 `IDENTITY_MIGRATION_REQUIRED`이며 production 실행·delivery를 차단한다. rollout은 프로젝트별 명시적 adapter 재생성·검증으로 하고, rollback은 v1 파일을 보존한 채 해당 프로젝트의 Hub production 경로만 다시 비활성화한다.
- adapter의 exact `project.project_id`를 Base Figma target registry의 exact entry와 교차 검사한다. local locator name은 identity 증거가 아니다.
- 프로젝트 root는 시작 시 `resolve()`, directory 존재, adapter identity와 Base pin, 저장된 locator fingerprint를 재검사한다. 독립 owner의 identity proof가 없거나 drift하면 `PROJECT_IDENTITY_UNVERIFIED`이며 production 실행·delivery를 차단한다.

### Canonical Figma routing contract

`PROJECT_FIGMA_TARGET_REGISTRY.json` data와 validator/loader는 각각 하나의 owner만 둔다.

- `schemas/project-figma-target-registry-v1.schema.json`: URL, file key, node ID, status와 version의 canonical schema.
- `tools/base-tool-contracts/`: schema를 읽고 typed target을 반환하는 단일 loader/consumer contract.
- Expression Studio, Sprite Studio와 Tool Hub는 이 contract를 dependency로 사용하고 자체 `_RegistryDocument` parser를 보유하지 않는다.
- Hub는 Figma registry를 다시 해석하지 않고 single owner가 반환한 target과 routing state만 소비한다.
- 현재 두 Studio parser의 차이와 `purpose` 호환 수정은 추출 필요성을 증명하는 drift evidence다. 공통 추출은 generation engine 추상화가 아니라 이미 세 소비자가 공유해야 하는 routing/security contract이므로 Phase 0.5 선행 작업이다.

### Secrets and logs

- child environment는 Hub 환경 상속으로 만들지 않는다. adapter별 clean allowlist에 OS 필수값과 해당 project/tool의 명시적 secret source만 주입한다.
- `OPENAI_API_KEY`, provider token, `CODEX_HOME`, profile/config path는 해당 adapter가 선언하지 않으면 child에서 제거한다. 서로 다른 프로젝트·provider의 secret을 전달하지 않는다.
- Hub registry, local project config, URL, 브라우저 storage, run manifest, log, delivery packet에 저장하지 않는다.
- UI는 secret 값 대신 `PRESENT / MISSING / NOT_REQUIRED`만 표시한다.
- 기본 log는 structured event schema, bounded field와 bounded tail만 보존하고 argv/env/raw provider response를 기록하지 않는다. provider exception에 secret이나 Windows/POSIX path가 포함된 경우도 테스트한다.
- raw stdout/stderr 보존은 기본 금지다. 사용자가 별도로 opt-in한 국소 진단에서도 저장 위치·기간·redaction 한계를 먼저 표시한다.

### Outputs

- 모든 생성 입력·후보·export·lineage·delivery packet은 기본적으로 `<project-root>/.asset-vault/library/generated/<tool-id>/<run-id>/` 아래의 local-only staging에만 존재한다.
- 프로젝트 adapter의 protected paths, Git tracked path, symlink와 `.git/`을 검사한다. vault가 초기화·gitignore되지 않았거나 output target이 tracked/protected/symlink이면 생성 전에 차단한다.
- Base에는 샘플 fixture와 code/test만 남고 실제 프로젝트 이미지와 결과를 commit하지 않는다.
- 다른 local-only staging을 쓰려면 프로젝트 adapter가 허용 relative root와 validator를 명시해야 한다. browser request의 자유로운 `output_root`는 사용하지 않는다.
- 프로젝트 자산 승격은 현행 vault/promotion 계약이 계속 소유하며 명시적 `promote` 전에는 tracked asset이나 runtime 완료가 아니다.

## 7. 런타임 아키텍처

### Hub server

- `127.0.0.1`에만 bind한다.
- 기본 browser UI와 JSON API를 제공한다.
- `Host`를 실제 loopback host/port로 제한하고 mutating API는 exact `Origin`, same-site session cookie와 custom CSRF token을 모두 요구한다.
- Hub 시작마다 고엔트로피 session/child identity secret을 만들고 저장소·URL·command line에 기록하지 않는다. child에는 최소 environment로만 전달한다.
- 외부 origin, remote bind, file URL, arbitrary path browsing을 허용하지 않는다.
- 한 browser action은 `registered tool ID + registered project ID`만 받는다.
- launch 전 preflight 결과가 `READY`가 아니면 child를 만들지 않는다.

### Child process identity

child key는 `(tool_id, project_id)`다. 한 project가 여러 도구를 동시에 실행할 수 있고, 여러 project가 같은 도구를 동시에 실행할 수 있다.

```text
hub
  ├─ sprite-animation-studio @ coc-fiction
  ├─ expression-studio @ coc-fiction
  ├─ sprite-animation-studio @ omenward
  └─ expression-studio @ ten-paces-hidden-moves
```

각 child에는 다음을 고정 전달한다.

- canonical `--project-id`
- verified `--project-root`
- exact Base Figma target registry
- selected production/fake engine policy
- Hub가 할당한 loopback port
- 최소 환경 변수 allowlist
- Hub가 생성한 per-launch nonce와 adapter/config fingerprint

child가 실행 중 request body의 다른 `project_id`를 받더라도 Studio service가 이를 거부해야 한다. Hub의 process binding과 Studio의 service binding을 둘 다 유지한다.

### Port allocation

- 한 machine에서 활성 Hub는 하나만 소유권을 갖도록 OS-level Hub lock을 사용한다. stale lock은 process identity를 확인한 뒤에만 복구한다.
- `(tool_id, project_id)` start에는 transactional lock과 idempotency key를 적용해 동시 click/request가 child 두 개를 만들지 못하게 한다.
- 단순 “free port 검사 후 기록”은 OS port를 예약하지 못하므로 금지한다. 우선안은 child가 loopback port `0`에 bind하고 실제 port와 nonce를 authenticated startup channel로 보고하는 것이다.
- 사용 framework가 port 0 report를 지원하지 않으면 Hub가 socket을 실제 bind해 보유한 뒤 child에 descriptor/handle을 넘기는 방식을 사용하고 Windows/POSIX 전략을 각각 검증한다. 불가능한 플랫폼에서는 범위가 제한된 bind retry를 사용하되 경쟁 상대가 자신의 실패라는 identity 증거가 있어야 한다.
- Studio CLI는 모두 `--port`를 받아야 한다. 현재 Sprite Studio의 고정 8765는 구현 전에 수정한다.
- 검증된 bind failure만 제한 횟수만큼 재시도하고, 실패를 `PORT_CONFLICT`로 표시한다.
- 실제 선택된 URL을 health check가 통과한 뒤에만 `RUNNING`으로 공개한다.

### Process lifecycle

```text
REGISTERED
→ PREFLIGHT
├─ BLOCKED_CONFIGURATION
├─ BLOCKED_ENGINE
├─ BLOCKED_PROJECT
└─ READY
   → STARTING
   ├─ START_FAILED
   └─ RUNNING
      ├─ UNHEALTHY
      └─ STOPPING → STOPPED
```

- PID 존재만으로 `RUNNING`이라 하지 않고 authenticated health endpoint와 immutable child identity를 확인한다. 같은 port의 다른 localhost 앱은 health payload와 secret이 일치하지 않으므로 열지 않는다.
- open/stop 전 per-launch nonce, `(tool_id, project_id)`, process handle/PID, adapter/config hash와 Base/Figma registry hash를 모두 다시 대조한다.
- Hub 재시작 뒤 기존 process를 무조건 소유했다고 추정하지 않는다. identity token 없는 process는 `EXTERNAL_OR_STALE`로 표시하고 자동 종료하지 않는다.
- Stop은 Hub가 현재 세션에서 시작하고 identity가 일치하는 child만 대상으로 한다.
- Windows는 Job Object로 child process tree를 소유·종료하고, POSIX는 process group과 제한된 signal escalation을 사용한다. path-with-spaces와 quoting은 argv array로 검증한다.
- config/process state는 OS user config에 secure permission, atomic replace, lock을 사용한다. crash 뒤 stale record를 process/nonce 검증 없이 재사용하지 않는다.
- 비정상 종료는 exit code와 sanitized structured tail만 보존하고 성공으로 대체하지 않는다.

### Studio status contract

두 Studio에 공통 최소 read-only endpoint를 추가한다.

```json
{
  "tool_id": "expression-studio",
  "project_id": "coc-fiction",
  "engine_kind": "production",
  "delivery_eligible": true,
  "status": "ready",
  "launch_nonce": "<unpredictable per-launch value>",
  "adapter_config_sha256": "<64 hex>",
  "figma_registry_sha256": "<64 hex>"
}
```

fake/simulated/unmodified fixture는 `engine_kind: simulated`, `delivery_eligible: false`여야 한다. 이 상태는 Hub UI가 아니라 두 Studio service, export manifest와 delivery packet에서 fail closed한다. Hub는 이를 큰 경고로 표시하고 production 또는 Figma-ready 결과로 분류하지 않는다.

## 8. 사용자 흐름

### 기본 화면

1. 좌측에서 프로젝트를 선택한다.
2. 프로젝트 identity, Figma `ROUTING_CONFIGURED`, live-placement evidence 여부와 provider readiness를 각각 확인한다.
3. 중앙에서 사용 가능한 Tool Card를 본다.
4. `실행`을 누르면 preflight 후 child가 시작된다.
5. `열기`를 누르면 해당 Studio를 새 탭에서 연다.
6. Studio 안에서 원본 입력, 생성, 비교, export, delivery packet 준비를 수행한다.
7. Hub에는 현재 process readiness만 표시한다. 최근 run은 durable signed/validated run manifest가 도입된 이후에만 표시한다.
8. 프로젝트 GPT가 delivery packet을 검증해 자신의 Figma 파일에 배치한다.

허브 자체가 Studio 화면을 iframe으로 감싸는 것은 1차 범위에서 제외한다. 두 Studio가 현재 `/api`와 `/`를 자체 소유하고 있으므로 새 탭 실행이 route 충돌, cookie/origin 혼동, accessibility 문제를 줄인다.

### 도구 추가 흐름

```text
need and owner identified
→ Existing Solution First disposition
→ isolated tool implementation or approved adapter
→ health/status contract
→ sample golden path and failure tests
→ registry entry
→ Hub discovery
```

폴더 존재만으로 자동 노출하지 않는다. registry entry, adapter, health contract, 최소 실제 smoke test가 모두 있어야 `READY`다.

## 9. Figma 경계

Figma Plugin API는 iframe에서 browser API·network request·사용자 선택 local file을 사용할 수 있고 PNG/JPG/GIF bytes를 Figma image로 만들 수 있다. 따라서 “Figma는 이미지를 넣을 수 없다”는 주장은 틀리다. 그러나 공식 문서상 plugin action은 사용자가 시작하는 short-lived 작업이고 한 번에 plugin/action 하나만 실행할 수 있으며 background plugin은 만들 수 없다. 이 제약과 provider secret·project filesystem·여러 child process supervision 요구 때문에 Figma를 Tool Hub 실행 host로 선택하지 않는다.

공식 근거:

- Plugin API introduction and user-action limits: <https://developers.figma.com/docs/plugins/>
- How plugins run and sandbox/UI split: <https://developers.figma.com/docs/plugins/how-plugins-run/>
- Working with images: <https://developers.figma.com/docs/plugins/working-with-images/>

Figma는 다음을 담당한다.

- 승인 원본과 생성 후보의 시각 비교
- 프로젝트별 Generated Assets 영역
- 사람 검토와 pinned handoff
- 프로젝트 GPT가 검증된 결과를 정확한 file/page/node에 배치

Figma는 다음을 담당하지 않는다.

- 로컬 Python process 시작
- `OPENAI_API_KEY` 보관
- 임의 프로젝트 filesystem 읽기·쓰기
- 이미지 생성 job supervision
- 실제 Godot 구현·런타임 검증

Tool Hub나 Studio가 `ready_for_project_gpt`를 반환해도 “Figma 업로드 완료”가 아니다. 실제 connector 배치 후 정확한 Figma section URL과 업로드 목록이 있어야 배치 완료다.

registry의 `READY_FOR_DELIVERY`는 local routing configuration 이름이지 live Figma node 존재 증거가 아니다. Hub는 이를 `ROUTING_CONFIGURED`로 표시한다. anchor `figma_node_url`은 HTTPS `www.figma.com/design/<bound-file-key>/...`의 host·file key가 bound project와 일치하고 `node-id`가 canonical syntax여야 한다. anchor node는 source-character/effect node이므로 delivery page나 Generated Assets destination node와 같을 필요가 없고, 같다고 승인 증거가 되지도 않는다. exact source node의 존재·승인은 별도 pinned anchor record에 URL, source SHA-256, approval state, snapshot 또는 connector evidence와 checked-at을 기록해 검증한다. 이 record는 project-owned visual approval artifact를 Hub가 참조·검증하는 것이며 Hub가 새 승인 원장이나 정본을 소유하지 않는다. syntax만 통과한 상태는 `ANCHOR_ROUTE_SYNTAX_VALID`일 뿐이다. 다른 host/file의 URL은 `EXTERNAL_REFERENCE`로 분류하고 production lineage·delivery에서 제외한다.

## 10. 보안·실패 가정

| 공격/실패 | 통제 |
|---|---|
| 브라우저가 임의 command 실행 | fixed adapter ID와 typed args만 허용, shell 사용 금지 |
| 악성 웹페이지가 localhost API 호출 | Host/Origin 검사, same-site session, custom CSRF token, JSON-only mutation |
| project A가 B의 Figma target 사용 | Hub와 Studio 양쪽에서 immutable project ID binding |
| local config에 잘못된 root 등록 | local file은 locator만 소유, canonical project adapter identity/Base pin/Figma entry 교차검증 |
| path traversal·symlink escape | resolved containment, protected/tracked/vault validation, launch-time realpath/hash recheck |
| fake output이 실제 생성으로 전달 | 두 Studio service에서 provenance 필수, `delivery_eligible=false`, export/delivery 차단 |
| API key 유출 | clean per-adapter env allowlist, 값 미반환, structured bounded logs |
| 포트 충돌로 다른 앱에 연결 | atomic bind/port 0, per-launch nonce와 process/adapter/registry identity health check |
| Hub 종료 시 child orphan | machine lock, Windows Job Object/POSIX process group, 다음 시작에서 stale 판정 |
| Hub가 외부 앱까지 종료 | 현재 세션에서 시작한 matching identity만 stop |
| 도구 dependency 충돌 | 각 Studio의 독립 venv/package 유지 |
| Hub가 새 정본이 됨 | tool metadata와 runtime state만 소유, 프로젝트·Figma·자산 승인 정본은 기존 owner 유지 |
| 자동 설치 supply-chain 위험 | 1차 범위에서는 install/update 기능 없음 |

## 11. 구현 단계

### Phase 0 — 기존 Studio 차단 결함 선행 해결

- Expression과 Sprite fake/simulated engine 결과의 export/Figma delivery를 각 service·manifest·packet에서 차단
- Expression configured project ID를 UI에 bootstrap하고 편집 불가 처리
- Sprite Studio `--port` 지원
- 두 Studio의 `/api/status`와 production/simulated provenance
- 두 Studio의 loopback Host/Origin/session/CSRF와 Hub child identity 계약
- anchor Figma URL의 host/file key와 canonical node syntax를 검증하고, 별도 pinned anchor record/connector evidence 없이는 승인·존재를 주장하지 않음
- output을 verified local vault staging으로 제한하고 protected/tracked/symlink target 차단
- 현재 uncommitted project binding/registry compatibility 변경 검증·커밋

이 단계가 통과하지 않으면 Hub가 안전하지 않은 경로를 더 쉽게 노출하므로 Hub 구현을 시작하지 않는다.

### Phase 0.5 — 단일 identity·routing owner

- 기존 v1을 제자리 수정하지 않고 `project-base-adapter-v2`에 canonical `project.project_id`를 필수화하며 builder/checker/template/docs/compat views/tests를 coordinated migration
- v1 adopter는 `IDENTITY_MIGRATION_REQUIRED`로 fail closed하고 프로젝트별 rollout/rollback을 검증
- local project config를 identity registry가 아닌 locator로 제한
- `PROJECT_FIGMA_TARGET_REGISTRY.json` 단일 schema와 `tools/base-tool-contracts/` loader를 만들고 두 Studio의 중복 parser 제거
- registry `READY_FOR_DELIVERY`와 live connector evidence를 분리해 Hub에는 `ROUTING_CONFIGURED`로 표시
- BCP-026은 승인될 때까지 scope authority가 아니라 비교 evidence로만 유지

### 별도 production dependency — Hub 범위와 독립

- `docs/superpowers/specs/2026-08-13-openai-visual-generation-engine-design.md`의 별도 승인·구현 계약에 따라 Expression과 Sprite production adapters를 채택한다.
- Expression CLI에는 explicit `simulated|openai` 선택과 reviewed snapshot adapter가 구현됐다. 단위·service 계약은 통과했으나 2026-08-13 실제 샘플 호출은 provider의 `credit_balance_exhausted / insufficient_quota`로 후보 0개·blocked였으므로 실제 표정 생성 제품은 아직 합격할 수 없다. Sprite의 OpenAI production adapter도 별도 미구현 상태다.
- Hub는 production adapter를 구현하거나 provider request를 소유하지 않는다. adapter가 없으면 `BLOCKED_ENGINE`, simulated이면 `DELIVERY_BLOCKED`를 표시한다.
- production provenance, anchor와 byte-different output, exact count/containment/readability, provider 비용·오류 처리와 실제 샘플 검증을 해당 Studio owner가 통과해야 `GENERATION_PRODUCT_READY` 후보가 된다.

### Phase 1 — 최소 Tool Hub

- `tools/TOOL_REGISTRY.json` schema와 validator
- `tools/tool-hub/` FastAPI UI/API
- machine-local project config loader
- typed launch adapters for the two Studios
- clean environment builder와 confined `shell=False` argv launcher
- machine/child locks, atomic port allocation, authenticated identity health check, OS별 process-tree start/open/stop
- project/tool readiness and simulated/production 표시
- Tool Radar 후보의 별도 runtime, marketplace, reference projection, browser-local draft/utilities는 이번 vertical slice에 구현하지 않고 후속 독립 범위로 유지
- candidate ZIP의 `data.js`, self-declared `PASS/ACTIVE`, raw command와 duplicate Hub ID는 import하지 않음
- 두 프로젝트 동시 실행 smoke test
- README·START_HERE·Documentation Map·schema migration·active consumer·compatibility test route

### Phase 2 — durable run identity 후에만 검토

- signed/validated durable run manifest가 먼저 존재할 때만 최근 run metadata와 delivery packet 링크
- path disclosure, schema migration, locking, secret exclusion이 검증된 뒤에만 project config import/export
- CLI와 Windows process-tree/atomic port smoke 뒤에만 Windows launcher shortcut 또는 packaged executable
- generation engine/run interface는 반복 계약이 안정된 경우에만 별도 공통 package로 추출

### 명시적 보류

- remote/cloud Hub
- team account/authentication
- arbitrary third-party tool installation
- shared model repository
- automatic Figma mutation
- automatic project commit/push
- embedded Studio iframe

## 12. 테스트와 Acceptance Criteria

### 정적·계약

- registry schema가 unknown field, raw command, absolute tool path, duplicate ID를 거부한다.
- local project locator는 canonical identity를 만들지 않으며 duplicate locator, 없는 root, non-directory, adapter/Figma registry mismatch, stale Base pin을 거부한다.
- v1 project adapter, 잘못된 v2 `project_id`, directory/repository/Figma entry에서 추론한 ID를 `IDENTITY_MIGRATION_REQUIRED` 또는 `PROJECT_IDENTITY_UNVERIFIED`로 차단한다.
- adapter `validators`의 raw command 문자열을 실행하지 않으며 fixed reviewed validator adapter 외의 실행 요청을 거부한다.
- 두 Studio와 Hub가 같은 canonical Figma routing loader를 사용하고 자체 parser가 남지 않는다.
- Studio status identity와 launched nonce, `(tool_id, project_id)`, process handle/PID, adapter/config hash, Figma registry hash 중 하나라도 다르면 Hub가 process를 열거나 종료 대상으로 소유하지 않는다.
- secrets와 project absolute path가 API 응답·structured log에 나타나지 않는다. provider exception/argv/env에 secret과 Windows/POSIX path를 심은 반례도 통과한다.
- shell metacharacter, caller flag/env/path, symlink swap, registry owner-path replacement, interpreter substitution을 모두 차단한다.
- output root가 `.git`, tracked/protected path, symlink 또는 초기화되지 않은 vault면 생성 전에 차단한다.
- anchor Figma URL의 host/file key가 bound project와 다르거나 node ID syntax가 canonical하지 않으면 approved lineage/delivery를 차단한다. anchor source node와 destination page/area node의 동일성은 요구하지 않는다.
- pinned anchor record나 connector evidence가 없으면 syntax-valid URL도 승인·live-node proof로 승격하지 않는다.

### 동시 실행

- 서로 다른 두 프로젝트에서 같은 Studio를 동시에 시작한다.
- 같은 프로젝트에서 Sprite와 Expression Studio를 동시에 시작한다.
- 네 process의 port, project ID, output root, Figma file key가 서로 다름을 확인한다.
- project A request로 B의 delivery packet을 얻으려 하면 API와 service 모두 차단한다.
- 같은 `(tool, project)` start를 동시에 요청해도 child가 정확히 하나만 생긴다.
- 같은 machine에서 두 번째 Hub가 ownership lock을 얻지 못하며, port 0/OS reservation 뒤 다른 process가 port를 선점할 수 없다.

### 실제 사용자 경로

- Hub 시작 → 프로젝트 선택 → Tool ready 확인 → Studio 시작 → 브라우저 open.
- production engine 미설정이면 `BLOCKED_ENGINE`; fake 선택은 `SIMULATED / DELIVERY_BLOCKED`.
- Expression과 Sprite 모두 fake/simulated 결과의 export/Figma delivery가 Hub 우회 direct API/service 호출에서도 차단된다.
- 별도 production dependency가 승인·구현된 뒤 샘플 원본으로 Expression 생성·선택·export가 production adapter에서 byte-different result를 만들고 lineage를 보존한다.
- 샘플 캐릭터로 Sprite `sprite_action`, 샘플 effect로 `effect_stages`를 각각 생성·curate·GIF/atlas export한다.
- 실제 provider 호출이 불가능한 테스트 환경에서는 위 세 생성 항목을 `NOT_RUN`으로 남기고 fake fixture 통과와 혼동하지 않는다.
- 준비된 packet을 프로젝트 GPT가 정확한 Figma file/page/area에 배치한 뒤에만 Figma placement를 별도 통과로 기록한다.
- Windows에서 path-with-spaces를 가진 두 실제 project locator로 Hub, 네 child process, open/stop/process-tree cleanup을 실제 PowerShell smoke한다. 실행 환경이 없으면 Windows 지원은 `BLOCKED_UNVERIFIED`이며 Hub 전체를 다중 프로젝트 production-ready로 판정하지 않는다.

### 회귀

- 각 독립 package에서 별도 pytest를 실행하고 각각의 JS syntax를 검사한다. root에서 두 suite를 한 pytest process로 합치지 않는다.
- Tool Hub tests와 process failure tests.
- catalog 화면에서 `RUNNABLE`, `REFERENCE`, `UNVERIFIED_LOCAL_DRAFT`가 혼합·자동 승격되지 않는 회귀 테스트.
- Tool Radar 후보의 두 Hub ID, raw command, self-declared status를 canonical registry로 import하려 하면 차단하는 테스트.
- `git diff --check`.
- 정확한 trusted main SHA에 대한 Base local validation.
- Windows PowerShell 실제 launcher/process-tree/path-with-spaces smoke.

## 13. 적대적 사전 검토

### MUST_FIX before implementation

1. local project file을 identity authority로 쓰지 않고 versioned canonical project adapter의 `project_id`·Base pin·protected paths와 exact Figma entry를 교차검증하며 v1을 제자리 수정하지 않는다.
2. 두 Studio의 Figma parser를 단일 schema/loader owner로 통합하고 Hub가 세 번째 parser를 만들지 않는다.
3. Hub environment 상속을 금지하고 adapter/project별 clean allowlist와 structured bounded logs를 사용한다.
4. health에 per-launch nonce, process/PID, adapter/config/registry hash를 포함해 stale/same-port process를 차단한다.
5. machine-wide Hub lock, `(tool,project)` transactional start와 OS-level atomic port allocation으로 TOCTOU를 제거한다.
6. Expression과 Sprite 모두 fake/simulated 결과를 service·manifest·packet에서 export/Figma delivery 불가로 만든다.
7. 두 Studio output을 vault local staging 또는 adapter가 허용한 local-only root로 제한하고 protected/tracked/symlink path를 차단한다.
8. anchor Figma URL은 bound host/file key와 canonical source-node syntax를 검증하되 destination node와 동일시하지 않고, 별도 pinned evidence 없이 승인·live Figma proof로 표시하지 않는다.
9. typed adapter 외에도 `shell=False`, argv array, reviewed realpath/interpreter/hash와 launch-time symlink/path recheck를 강제한다.
10. 미승인 BCP-026을 authority로 사용하지 않고 Hub scope를 두 art Studio launcher로 한정한다.
11. 대안 점수는 가설로 유지하고 실제 Windows 네-process smoke·production adapter/provider·live Figma evidence 전에는 다중 플랫폼 또는 generation product-ready를 주장하지 않는다.
12. project adapter의 raw `validators` 문자열은 절대 실행하지 않고 fixed reviewed validator adapter만 typed args와 `shell=False`로 호출한다.
13. `HUB_LAUNCHER_ACCEPTED`와 `GENERATION_PRODUCT_READY`를 분리해 production adapter 부재를 launcher 합격으로 숨기지 않는다.

### SHOULD_FIX in Phase 1

1. Hub process restart와 orphan/stale process 판정을 OS별 process-tree 계약으로 제공한다.
2. production/simulated, credential presence, routing configuration, live Figma evidence와 delivery eligibility를 한 화면에서 분리한다.
3. tool onboarding test template로 registry-only dead entry를 막는다.
4. schema `$id`, version/migration, README·START_HERE·Documentation Map·consumer·compatibility test route를 함께 추가한다.
5. OS user config permission, atomic write/lock, Windows/POSIX path·signal·crash recovery를 명시한다.

### DEFER

1. ComfyUI를 즉시 공용 backend로 채택하지 않는다. OpenAI production adapter 실측 뒤 quality/cost/control 요구가 생길 때 별도 disposition한다.
2. 외부 cloud Hub는 원격 파일·인증·비용·개인 자산 업로드 요구가 생기기 전까지 보류한다.
3. 전체 `tools/*.py`를 UI에 노출하지 않는다. 사용자 소비 경로가 확인된 항목만 이후 등록한다.
4. durable validated run manifest 전에는 최근 run metadata와 delivery link를 복원하지 않는다.
5. path disclosure·schema migration·locking·secret exclusion 전에는 project locator import/export를 제공하지 않는다.
6. CLI와 실제 Windows process ownership·atomic port smoke 전에는 packaged launcher를 만들지 않는다.

### Rejected critiques

- “한곳에 모으려면 모든 코드를 한 앱으로 합쳐야 한다”: 사용자 진입점과 실행 권위를 혼동한다.
- “Figma에 페이지가 있으니 Figma plugin이 생성도 해야 한다”: Figma visual workspace 계약과 로컬 filesystem/provider 실행 경계를 위반한다.
- “유명한 launcher를 설치하면 더 빠르다”: Base의 project/Figma/approval schema를 그대로 검증하지 못하고 새로운 arbitrary execution owner를 만든다.
- “subprocess launcher는 모두 arbitrary execution이다”: confined typed adapter, clean env, authenticated identity와 reviewed paths가 실제로 검증되면 기각 가능하다.
- “local absolute path를 Git/Figma에 넣어야 한다”: local locator는 저장소 밖에 두되 canonical adapter identity를 별도로 검증하는 편이 권위와 개인정보 경계에 맞다.

## 14. 성공 판정과 롤백

`HUB_LAUNCHER_ACCEPTED`는 화면이 열리는 것으로 판정하지 않는다. 두 실제 프로젝트 동시 실행, production/simulated 구분, 프로젝트별 output/Figma isolation과 실제 Windows process lifecycle이 증거로 확인되어야 한다. 샘플의 실제 생성·export와 정확한 Figma placement는 별도 production dependency가 닫힌 뒤 `GENERATION_PRODUCT_READY`에서만 판정한다. 한 상태의 합격을 다른 상태의 합격으로 표현하지 않는다.

롤백은 다음처럼 작다.

1. Hub process를 종료한다.
2. Hub가 시작한 child만 identity를 확인해 종료한다.
3. 기존 Studio 직접 실행 명령으로 돌아간다.
4. `tools/tool-hub/`와 registry entry를 revert한다.
5. 프로젝트 출력과 기존 Studio 코드는 그대로 보존한다.

이 구조는 모놀리식 병합이나 프로젝트별 코드 복사보다 되돌리기 쉽다.

## 15. 최종 결론

현재 비교에서 공용 도구 코드의 위치는 **Base repository의 `tools/` 아래**이고, 실행 형태는 **단일 localhost Tool Hub + tracked allowlist registry + machine-local locator + canonical project adapter identity + project-bound child processes**로 구현됐다.

이를 “모든 도구를 한 앱으로 재작성”하거나 “Figma 안에서 생성”으로 확장하지 않는다. 현행 두 visual Studio와 QA Studio를 독립 owner로 재사용하고 단일 Hub의 최소 UI·typed supervisor만 연결했다. Linux 네-process import 격리 증거는 확보했지만 실제 Windows 네-process smoke, provider 생성, Android device, live Figma placement 전 최종 상한은 `IMPLEMENTED_LINUX_IMPORT_SLICE / BLOCKED_UNVERIFIED`다.
