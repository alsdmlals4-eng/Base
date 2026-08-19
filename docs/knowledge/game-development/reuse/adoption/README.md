# Reuse Adoption Kit

이 디렉터리는 Base에 구현된 P0 재사용 모듈을 각 프로젝트에 **선택적으로 설치·검증**하기 위한 적용 규격을 설명한다.

## 원칙

```text
Base reference module
→ project adoption manifest
→ safe selected vendor sync
→ thin project adapter
→ project-owned CI/runtime evidence
```

- 모든 모듈을 모든 프로젝트에 넣지 않는다. `not_applicable`을 정상 상태로 사용한다.
- Base는 공용 helper를 제공하지만 프로젝트의 canon, save state, gameplay rules, art, UI composition을 소유하지 않는다.
- 설치 파일은 이전 Adoption Lock의 해시와 현재 파일 해시가 일치할 때만 갱신한다.
- 프로젝트가 vendored 파일을 수정했다면 자동 덮어쓰지 않고 `REFUSE_OVERWRITE_LOCAL_MODIFICATION`으로 중단한다.
- `check`는 읽기 전용이며 설치 상태, Base source drift, local modification, manifest/lock commit drift를 보고한다.
- 별도 package manager, network fetch, paid service, runtime dependency를 추가하지 않는다.

## 파일

- 실행 도구: `tools/reuse_modules/reuse_adoption.py`
- Manifest 예시: `templates/reuse-modules/PROJECT_REUSE_ADOPTION_MANIFEST.json`
- 전체 프로젝트 상태: `ACTIVE_PROJECT_ADOPTION_MATRIX.json`
- 설치 Lock: 프로젝트의 `.base-reuse/adoption-lock.json`

## Manifest 상태

- `enabled`: 실제 vendoring 대상. `source`와 `destination`을 명시한다.
- `planned`: 적합하지만 아직 프로젝트 gate/소비자가 준비되지 않음.
- `not_applicable`: 프로젝트에 실질적 가치가 없어 설치하지 않음.
- `deferred`: 가치가 있으나 명시적 blocker 때문에 보류.

현재 구현된 P0 module ID만 fail-closed allowlist에 포함된다.

- `RM-TOOL-001 DATA_SCHEMA_CROSSREF_VALIDATOR`
- `RM-SYS-001 GRID_PLACEMENT_RULE_ENGINE`
- `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE`
- `RM-VIS-001 SEMANTIC_UI_SKIN_KIT`
- `RM-VIS-002 GAMEPLAY_SYMBOL_ATLAS`

새 모듈을 추가할 때는 Base reference implementation, tests, rights/dependency boundary가 먼저 검증된 뒤 allowlist를 확장한다.

## 실행

프로젝트 manifest가 `docs/base-reuse-adoption.json`에 있다고 가정한다.

```bash
python tools/reuse_modules/reuse_adoption.py apply docs/base-reuse-adoption.json --base-root <BASE_ROOT> --project-root <PROJECT_ROOT>
python tools/reuse_modules/reuse_adoption.py check docs/base-reuse-adoption.json --base-root <BASE_ROOT> --project-root <PROJECT_ROOT>
```

`apply`는 모든 enabled module을 먼저 preflight한 뒤 문제가 하나라도 있으면 쓰기를 시작하지 않는다.

## 프로젝트 상태 어휘

- `ADOPTED_AND_VERIFIED`: 하나 이상의 adapter가 프로젝트 CI/main에서 검증됨.
- `READY_TO_ADOPT`: 현재 gate상 신규 sidecar PR을 만들 수 있음.
- `DEFERRED_OPEN_PR`: 기존 진행 중 PR을 보호하기 위해 보류.
- `DEFERRED_PHASE_GATE`: 프로젝트 자체 planning/build gate 때문에 보류.
- `DEFERRED_PRODUCT_GATE`: 현재 제품 구현 범위가 명시적으로 BLOCKED.
- `NOT_APPLICABLE`: 해당 모듈군이 프로젝트 문제를 해결하지 않음.

상태가 `DEFERRED_*`여도 Base에서 적용 가능한 manifest/profile을 유지해 blocker가 풀린 뒤 동일 검증 절차를 재사용한다.

## 권위 경계

```text
ADOPTION_KIT_INSTALLED != PROJECT_ADOPTION_APPROVED
PROJECT_ADAPTER_VERIFIED != HUMAN_PLAYER_EXPERIENCE_PASS
VENDORED_REFERENCE != PROJECT_CANON
SEMANTIC_UI_CONTRACT != PRODUCT_ART_APPROVAL
```

실제 프로젝트 적용은 해당 저장소의 최신 `AGENTS.md`, active decision, open PR isolation, required CI를 우선한다.
