# Base 공용 Skill 어댑터 계약

## Base v9.1 canonical authority

The canonical project integration file is `skills/PROJECT_BASE_ADAPTER.json`.

`RETIRED_HISTORY_ONLY`: 과거 Tool Hub·`base-tool-contracts` identity migration 설명은 Git 이력과 명시적 역사 문서에서만 감사할 수 있으며 현재 adapter 실행 권위·신규 설치 경로가 아니다. Free-form `validators` 문자열은 compatibility metadata일 뿐 실행하지 않으며, executable validation은 현재 저장소가 유지하는 고정·검토된 validator와 typed argument·`shell=False` 경계만 사용한다.
`skills/PROJECT_BASE_SKILL_ADAPTER.json`, `skills/BASE_V9_ADAPTER.json`, and
`skills/PROJECT_PATH_ADAPTER.json` remain for one compatibility cycle only as
deterministic `GENERATED_COMPATIBILITY_VIEW` outputs. Never hand-edit them.
They are also `HISTORY_ONLY`: they are omitted when no preserved file-specific
legacy input exists and can never become an active adapter authority. Any older
JSON examples below are historical consumer shapes, not editable v9.1 inputs.

The canonical schema separates release payload and evidence pins and owns
`base_release`, `project`, `routing`, `skill_registry`, `shared_overrides`,
`gdd_sheet`, `protected_baseline`, `protected_paths`, `validators`, and
`compatibility`. `protected_baseline` binds an approved commit to an external
authority kind/reference plus a confined policy source path, source type,
`/protected_paths` JSON Pointer, and policy SHA-256. First migration reads the
real legacy source at that commit; later waves may read the canonical adapter
at their baseline. Local standard validation resolves the recorded
`REMOTE_TRACKING_REF` (normally `refs/remotes/origin/main`) and requires exact
commit equality. Pull-request CI passes `github.event.pull_request.base.sha`
as `--protected-base`, which must exactly equal the adapter record and can
never replace it. This CLI value is trusted caller input, not cryptographic
attestation. Standard validation never silently skips or self-attests the
protected-path comparison.

## 목적

Base는 여러 프로젝트가 공유하는 판단 절차와 품질 기준을 단일 원본으로 유지한다. 각 프로젝트는 공용 Skill 본문을 복제하지 않고 **route Registry + 프로젝트 어댑터**로 연결하며, 프로젝트 고유 규칙만 로컬 Skill로 만든다.

## 소유권 원칙

```text
Base 공용 판단·절차·상태·품질 기준
→ Base Skill이 단일 소유

프로젝트 경로·정본·엔진·플랫폼·검증기·보호 대상
→ 프로젝트 어댑터가 소유

세계관·게임 규칙·프로젝트 고유 제작 절차
→ 프로젝트 전용 Skill이 소유
```

## 강제 규칙

1. Base 공용 Skill은 프로젝트에 `SKILL.md` 복사본을 만들지 않는다.
2. 프로젝트 Registry는 Base Skill ID, Base 경로, 고정 커밋, 프로젝트 어댑터를 route한다.
3. 프로젝트 어댑터는 공용 절차를 다시 설명하지 않고 실제 경로·정본·검증기·예외만 기록한다.
4. 프로젝트 전용 Skill은 세계관, 코어 규칙, 실제 데이터 구조, 플랫폼 차이처럼 다른 프로젝트에 직접 적용할 수 없는 책임에만 만든다.
5. 새 프로젝트 Skill을 만들기 전에 Base Registry와 `skills/BASE_SHARED_SKILL_ROUTES.json`에서 기존 공용 Skill을 검색한다.
6. 공용화 가능한 반복 절차가 없을 때만 프로젝트 전용 Skill을 생성한다.
7. 프로젝트에서 검증된 공용 개선은 `managing-base-change-proposals`를 통해 Base로 승격하고, 프로젝트 복사본을 영구 정본으로 유지하지 않는다.
8. Base 커밋 갱신은 자동 덮어쓰기가 아니다. 프로젝트 정본·route·adapter·validator를 같은 변경 묶음에서 검증한다.

## 프로젝트 route Registry 최소 계약

```json
{
  "schema_version": 1,
  "registry_role": "project-base-shared-skill-router",
  "base": {
    "repository": "alsdmlals4-eng/Base",
    "commit": "<40자 커밋 SHA>",
    "source_registry": "skills/BASE_SHARED_SKILL_ROUTES.json"
  },
  "project_adapter": "<프로젝트 어댑터 경로>",
  "routes": {
    "<route_name>": {
      "skill_id": "<Base Skill ID>",
      "base_path": "skills/<skill-id>/SKILL.md",
      "adapter": "<프로젝트 어댑터 경로>"
    }
  },
  "local_skill_policy": {
    "base_shared_skills": "adapter-only",
    "project_specific_skills": "local-only",
    "duplicate_base_skill_bodies": false
  }
}
```

## 프로젝트 어댑터 최소 계약

```json
{
  "schema_version": 1,
  "adapter_role": "base-shared-skill-project-adapter",
  "base": {
    "repository": "alsdmlals4-eng/Base",
    "commit": "<route와 같은 SHA>"
  },
  "project": {
    "repository": "<owner/repo>",
    "layout_policy": "preserve-existing-canonical-paths"
  },
  "role_bindings": {
    "project_agents": "...",
    "documentation_map": "...",
    "active_context": "...",
    "skill_registry": "..."
  },
  "canonical_sources": [],
  "protected_paths": [],
  "engine": {},
  "validators": [],
  "shared_skill_overrides": {}
}
```

## 허용되는 어댑터 차이

- 기존 저장소 경로와 파일 이름.
- Godot 버전·렌더러·목표 플랫폼.
- 정본 문서와 실제 데이터·Scene·Script 경로.
- 프로젝트 보호 경로와 저장 호환성 제약.
- 실제 존재하는 자동 검증 명령과 수동 검증 항목.
- 아카이브 위치와 제3자 라이선스 기록 위치.
- 공용 Skill 입력을 채우는 프로젝트별 역할 바인딩.

## 금지되는 어댑터 내용

- Base Skill의 절차 전체 복사.
- Base 정책을 프로젝트가 임의로 완화하는 재정의.
- 존재하지 않는 검증 명령.
- 프로젝트 고유 수치나 세계관을 Base 공용 규칙처럼 선언.
- Base 커밋과 route Registry의 서로 다른 버전 지정.

## 변경 절차

```text
Base Skill·route 변경
→ Base 검증
→ Base 커밋 고정
→ 각 프로젝트 route·adapter 갱신
→ 프로젝트 정본·경로·validator 검사
→ 기존 로컬 공용 Skill 복사본은 별도 승인 아래 호환·아카이브 판정
```

기존 프로젝트의 로컬 공용 Skill 복사본은 이번 계약을 채택했다는 이유만으로 즉시 삭제하지 않는다. `governing-legacy-retention-and-archives`로 고유 정보·활성 참조·복구 경로를 확인한 뒤 별도 작업에서 처리한다.

## 완료 기준

- 공용 Skill 본문이 Base에 하나만 존재한다.
- 프로젝트 route와 adapter가 같은 Base 커밋을 가리킨다.
- 프로젝트 로컬 Registry에는 프로젝트 고유 Skill만 활성 로컬 Skill로 등록한다.
- 기존 경로를 강제 개명하지 않는다.
- 검증 결과와 미실행 항목이 분리돼 있다.
- 새 작업자가 프로젝트 저장소만으로 Base route, adapter, 정본과 검증기를 찾을 수 있다.
