# Base 공용 Skill 프로젝트 라우팅 정책

## 목적

Base의 공용 Skill은 프로젝트 저장소에 본문을 복사하지 않는다. 모든 프로젝트는 공용 절차를 **Base Registry route → 프로젝트 어댑터**로 사용하고, 세계관·게임 규칙·실제 데이터 계약처럼 프로젝트에만 존재하는 책임만 로컬 Skill로 만든다.

## 2단계 라우팅

### 1. Base 메인 Registry route

프로젝트 route Registry는 Base의 `skills/SKILL_REGISTRY.json`을 자동 trigger 기반으로 선택하되 반드시 프로젝트 공용 어댑터를 거친다.

```json
{
  "base_registry_route": {
    "source_registry": "skills/SKILL_REGISTRY.json",
    "selection": "automatic-trigger-match",
    "adapter": "skills/PROJECT_BASE_SKILL_ADAPTER.json",
    "copy_skill_bodies_to_project": false
  }
}
```

이 route는 작업 계약, 기획서 관리, 프로젝트 코어, 검증, 정본 최신성, 런타임 진단 등 Base 메인 Registry의 공용 절차를 담당한다.

### 2. 전문 extension route

`skills/BASE_SHARED_SKILL_ROUTES.json`은 프로젝트별 추가 계약이나 전문 어댑터가 필요한 공용 Skill을 명시적으로 route한다.

현재 필수 extension route는 다음과 같다.

| route | Skill | adapter |
|---|---|---|
| `legacy_retention_and_archives` | `governing-legacy-retention-and-archives` | 프로젝트의 archive retention adapter |
| `godot_assets_before_creation` | `evaluating-godot-assets-and-plugins-before-creation` | 프로젝트 공용 adapter |

전문 extension은 Base 메인 Registry를 대체하지 않는다. 메인 Registry의 자동 선택을 보완한다.

## 프로젝트 어댑터 책임

프로젝트 공용 어댑터는 다음만 소유한다.

- 프로젝트 AGENTS, Documentation Map, Active Context, 로컬 Skill Registry 경로.
- 프로젝트 정본과 보호 경로.
- Godot 버전·렌더러·플랫폼·addon·asset 경로.
- 실제 존재하는 자동·수동 검증기.
- 제3자 자산·라이선스 기록 위치.
- 아카이브 루트·Manifest·증거·복구 기준.
- 프로젝트별 검색 초점과 외부화 금지 코어.

Base Skill 절차 전체를 어댑터에 복사하지 않는다.

## 프로젝트 전용 Skill 생성 조건

다음 조건을 모두 만족할 때만 프로젝트 로컬 Skill을 만든다.

1. Base 메인 Registry와 extension route에 같은 책임이 없다.
2. 책임이 특정 프로젝트의 세계관·코어 규칙·데이터 구조·제작 방식에 종속된다.
3. 다른 프로젝트에 그대로 적용하면 잘못된 판단을 만들 수 있다.
4. 입력·산출물·검증 기준이 독립적으로 정의된다.

공용화 가능한 반복 절차는 프로젝트에 새 Skill로 만들지 않고 `managing-base-change-proposals`를 통해 Base 승격 후보로 보낸다.

## 버전 고정

프로젝트는 다음 두 기준을 구분할 수 있다.

- **전체 운영체계 채택 기준:** 프로젝트가 전반적으로 검증해 채택한 Base commit.
- **공용 Skill route 기준:** 현재 route·adapter가 선택적으로 읽는 Base commit.

두 기준이 다를 때는 별도 사람용 문서에 범위와 이유를 명시한다. 공용 Skill route pin을 올렸다는 이유로 CI, 발행, Codex 인수 등 다른 Base 정책을 프로젝트에 자동 강제하지 않는다.

## 검증 계약

각 프로젝트는 최소한 다음을 정적으로 검사한다.

- route Registry, 프로젝트 어댑터, archive adapter가 같은 Base commit을 가리킨다.
- `base_registry_route`가 프로젝트 어댑터를 사용하고 Skill 본문 복사를 금지한다.
- 필수 extension route 2개가 존재한다.
- 프로젝트 로컬 정책이 `adapter-only / local-only / duplicate=false`다.
- 어댑터가 가리키는 정본·기록·아카이브 경로가 실제로 존재한다.
- 아카이브 기본 권한이 `active=false`, `implementation=NONE`이다.
- 실행하지 않은 Godot·플랫폼·사람 검증을 PASS로 보고하지 않는다.

## 변경 순서

```text
Base 공용 Skill 또는 route 변경
→ Base 테스트와 PR 검증
→ Base commit 고정
→ 프로젝트 branch에서 route·adapter·문서·검증기 동시 갱신
→ 프로젝트 PR 검증
→ 사용자 승인·Required Check 뒤 병합
```
