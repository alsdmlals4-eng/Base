# Local Godot Reference Library

## Status

```yaml
scope: LOCAL_USER_ENVIRONMENT
role: LOCAL_TEMPLATE_AND_OFFICIAL_DEMO_REFERENCE_LIBRARY
production_authority: false
project_dependency: false
portable_required_path: false
```

이 문서는 현재 사용자 Windows 환경에서 Godot 템플릿·공식 데모·검토용 플러그인 원본을 모아두는 **로컬 참고 라이브러리의 위치와 사용 경계**를 기록한다.

Base나 개별 게임 프로젝트의 정본·의존성·설치 경로가 아니다. 이 폴더의 항목이 존재한다는 사실만으로 프로젝트 채택·승인·호환성 검증이 완료된 것으로 해석하지 않는다.

## Local path

```text
C:\Users\user\Documents\GitHub\Godot_Reference
```

이 절대 경로는 **현재 사용자 PC 전용 환경 정보**다. 다른 PC, CI, 원격 agent, 새 Windows 계정에서 동일 경로가 존재한다고 가정하지 않는다.

경로가 없거나 접근할 수 없으면:

```yaml
local_reference_state: UNAVAILABLE_LOCAL_REFERENCE
hard_failure: false
fallback: CONTINUE_NORMAL_EXISTING_SOLUTION_SEARCH
```

즉, 로컬 라이브러리는 검색을 빠르게 하는 참고 선반이지 Base와 프로젝트가 실행되기 위한 필수 의존성이 아니다.

## Intended contents

필요에 따라 다음처럼 정리할 수 있다.

```text
Godot_Reference\
├─ Templates\
├─ Official_Demos\
├─ Plugins_Reference\
└─ Archive\
```

- `Templates`: 게임 셸, 메뉴, 설정, 저장, UI 등 재사용 가능한 구조를 검토하는 템플릿.
- `Official_Demos`: Godot Foundation·공식 프로젝트의 기능별 데모와 예제.
- `Plugins_Reference`: 도입 전 소스·구조·사용법을 검토하기 위한 애드온 또는 플러그인 원본.
- `Archive`: 구버전 또는 현재 우선순위에서 제외된 참고 자료.

폴더 구조는 로컬 정리 규칙이며 프로젝트의 표준 디렉터리 계약이 아니다.

## Usage order

Godot 기능·템플릿·애드온·구현 예시를 찾을 때 관련성이 있으면 다음 순서를 사용한다.

```text
현재 프로젝트의 실제 코드·Scene·Resource·addon·dependency
→ Base의 현행 구현·정본·관련 PR
→ 현재 PC의 Local Godot Reference Library
→ Godot 기본 기능·공식 문서
→ Godot Asset Store / Asset Library
→ 제작자 공식 Release·GitHub·상용 원본
→ 필요한 경우에만 BUILD_NEW
```

로컬 라이브러리를 확인했다고 해서 외부 원본 재검증을 생략하지 않는다. 버전, 라이선스, Godot 호환성, 유지보수 상태처럼 변할 수 있는 정보는 채택 시점에 공식 원본에서 다시 확인한다.

## Adoption boundary

로컬 라이브러리의 항목은 기본적으로 다음 상태다.

```yaml
local_library_item_state: REFERENCE_ONLY
adopted_into_project: false
```

프로젝트에서 실제 사용하려면 `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`의 평가 절차를 따른다.

최소 확인 항목:

- 현재 요구와 실제 기능 적합성
- 정확한 Godot 버전 호환성
- 원본 source와 exact version/release
- 라이선스와 상업 사용·수정·재배포 조건
- 기존 프로젝트 구조·데이터 권위와의 중복 여부
- 실제 `consumption_path`
- 제거·rollback 가능성
- 필요한 테스트·runtime 검증

발견 또는 다운로드만으로 `REUSE`, `ADOPTED_ACTIVE`, production readiness를 선언하지 않는다.

## Selective reuse rule

템플릿과 데모는 **통째로 프로젝트 표준으로 복사하는 것보다 필요한 패턴·컴포넌트·설정만 선택적으로 검토하고 흡수하는 것을 기본값**으로 한다.

다음은 별도 검토 없이 수행하지 않는다.

- 템플릿 전체를 신규 프로젝트의 canonical architecture로 지정
- 템플릿의 Autoload·manager·input·save·UI 구조를 기존 프로젝트 위에 일괄 덮어쓰기
- 데모 프로젝트를 제품 코드로 직접 승격
- 참고 플러그인을 프로젝트 `addons/`에 자동 복사·활성화
- 라이브러리 전체를 Base 또는 게임 프로젝트 Git 저장소에 복제

기존 프로젝트와 충돌하지 않는 최소 부분만 `REUSE / ABSORB / REFACTOR / ARCHIVE / BUILD_NEW` 판정에 따라 처리한다.

## Repository boundary

```yaml
Base_repository:
  stores: path_and_usage_contract_only
  stores_reference_library_files: false

Game_project_repository:
  stores: only_explicitly_adopted_project_files_and_records
  stores_entire_reference_library: false

Local_Godot_Reference:
  stores: downloaded_reference_templates_demos_and_review_sources
  canonical_project_truth: false
```

GitHub의 `Base` 저장소와 실제 게임 프로젝트는 이 로컬 폴더의 존재 여부에 의존해서는 안 된다.

## Update rule

로컬 경로가 이동하거나 라이브러리 운영 방식이 바뀌면 이 문서와 이를 참조하는 Godot source catalog를 함께 갱신한다. 개별 템플릿의 버전 변동은 Base 전역 정본으로 매번 기록할 필요가 없으며, 실제 프로젝트 채택·재검증 시 exact version을 프로젝트 기록에 남긴다.
