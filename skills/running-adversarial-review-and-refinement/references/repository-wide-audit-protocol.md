# 저장소 전체 적대적 감사 프로토콜

이 reference는 `running-adversarial-review-and-refinement`의 `repository-wide-audit` mode를 실행할 때만 읽는다. 일반 단일 작업 공격이나 병합 후 최소 검토에서는 사용하지 않는다.

## 1. 책임 경계

이 프로토콜은 저장소 전체를 하나의 작업물로 보고 **권한·중복·누락·stale 계약·untouched 소비자·파생본 drift**를 공격하고 Finding을 라우팅한다.

- 실제 정적·런타임·접근성·성능 검증: `reviewing-and-validating-project-changes`
- 경로·ID·정본·Template·Test 전파: `auditing-canonical-reference-freshness`
- 구형본·Archive·Compatibility·삭제 Gate: `governing-legacy-retention-and-archives`
- 운영체계 설치·마이그레이션: `managing-game-project-operating-system`

이 mode가 위 책임을 복제하거나, 검색 결과만으로 파일을 삭제하지 않는다.

## 2. 필수 입력

```yaml
baseline_branch_and_commit:
current_branch_and_commit:
user_requirements_and_recent_decisions:
current_confirmed_decisions:
documentation_map_and_registries:
active_entrypoints:
canonical_sources:
repository_search_roots:
actual_code_data_scenes_resources_assets_tests:
open_recent_and_replacement_prs:
known_renames_replacements_and_legacy_aliases:
generated_derivatives_and_manifests:
project_google_sheet_state:
protected_paths_and_assets:
validation_environment:
change_authority:
```

Base 자체는 `project_google_sheet_state: BASE_EXCLUDED`다. 개별 프로젝트가 Sheet를 사용하지 않으면 `NOT_CONFIGURED`이며 일치 여부를 추정하지 않는다.

## 3. 권한 분류

모든 후보는 내용·활성 참조·Registry·생성 관계·실제 소비자를 근거로 다음 중 하나로 분류한다.

- `CURRENT_AUTHORITY`: 한 질문·책임의 현행 정본.
- `ACTIVE_CONSUMER`: 정본을 읽거나 구현·검증·발행에 사용하는 활성 파일.
- `ACTIVE_TEMPLATE`: 새 프로젝트·문서·작업에 설치되는 현행 Template.
- `GENERATED_DERIVATIVE`: 원본·생성기·해시·Manifest에 종속된 파생본.
- `COMPATIBILITY_ONLY`: 구형 ID·경로·용어의 소비자를 현행으로 연결하지만 독립 권한은 없음.
- `HISTORY_ONLY`: Changelog·완료 Plan·PR 설명처럼 과거 사실을 보존함.
- `ARCHIVE_HISTORY`: 활성 라우팅에서 격리되고 metadata·replacement·rollback이 있는 보관본.
- `TEST_FIXTURE`: 구형 표현·오류 상태를 의도적으로 재현하는 검사 입력.
- `PLACEHOLDER_INACTIVE`: 설치 전 예시이며 활성 상태로 오인되지 않음.
- `KEEP_UNRESOLVED`: 권한·고유 정보·소비자를 확인하지 못함.

파일명·날짜·버전 숫자만으로 분류하지 않는다. `CURRENT_AUTHORITY`가 둘 이상이면 `DUPLICATE_ACTIVE_SOURCE`다.

## 4. 실행 순서

```text
repository-scope-map
→ canonical-authority-map
→ full-file-inventory
→ stale-and-duplicate-attack
→ untouched-consumer-attack
→ derivative-and-prompt-drift-attack
→ validate-critique
→ legacy-classification
→ approved-minimal-fix
→ regression-and-freshness-recheck
→ repository-audit-report
```

### 4.1 `repository-scope-map`

- 최신 `main`, 현재 Branch, 동일 Goal의 열린·최근 병합·대체 PR을 고정한다.
- 사용자 최신 승인과 `CURRENT_CONFIRMED_DECISIONS`를 복원한다.
- 검색 root, 제외 root, generated root, archive root와 보호 경로를 기록한다.
- 도구·권한 때문에 전수 파일 목록을 얻지 못하면 `BLOCKED_UNVERIFIED` 범위를 명시한다.

### 4.2 `canonical-authority-map`

```text
AGENTS·START_HERE·README
→ 운영 정책·Documentation Map
→ CURRENT_CONFIRMED_DECISIONS·분야 정본
→ Skill Registry·Legacy Alias·Shared Route
→ 프로젝트 설치 Template
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 생성기·파생본·Manifest
→ GitHub PR·Issue·Release·프로젝트 Sheet
```

각 책임에 `CURRENT_AUTHORITY` 하나와 필요한 `ACTIVE_CONSUMER`를 연결한다.

### 4.3 `full-file-inventory`

가능한 실제 tracked file 목록을 기준으로 다음을 수집한다.

- 경로·확장자·크기·hash·마지막 변경 Commit
- Registry·Documentation Map 등록 여부
- inbound/outbound reference
- source/generator/derivative 관계
- 현재 Decision·Schema·ID·Skill·제품 단계 토큰
- 동일·유사 내용과 대체 정본
- 실행·발행·테스트 소비 여부

검색 API 결과는 후보 목록일 뿐 전수 인벤토리 완료 증거가 아니다.

### 4.4 `stale-and-duplicate-attack`

다음을 공격한다.

- 승인된 최신 Decision이 빠졌거나 `SUPERSEDED / REJECTED / DEFERRED` 결정이 다시 활성화됨
- 같은 책임을 둘 이상의 활성 파일이 주장함
- 구형 경로·Skill ID·Schema·제품 단계·완료 기준이 현행처럼 사용됨
- 파일은 존재하지만 Registry·entrypoint·실제 실행 경로가 없음
- README·기획서·Template·Skill·Test가 서로 다른 정책을 설명함
- Base Template을 Base의 실제 프로젝트 상태로 오인함
- 별도 `CORE_POC` 같은 폐기된 Gate가 활성 흐름으로 부활함

역사·호환 문맥의 명시적 구형 표현은 `ALLOWED_LEGACY` 후보로 분리한다.

### 4.5 `untouched-consumer-attack`

정본 변경 시 변경된 파일만 보지 않고 **변경됐어야 하지만 untouched인 파일**을 찾는다.

```yaml
source_change:
expected_consumers:
changed_consumers:
UNTOUCHED_CONSUMER:
  - path:
    expected_reason:
    actual_state:
    finding: MISSING_CONSUMER | FALSE_POSITIVE | ALLOWED_UNCHANGED | BLOCKED_UNVERIFIED
```

확인 대상:

- README·START_HERE·AGENTS
- 운영 정책·Documentation Map
- Registry·Legacy Alias·Shared Route
- 프로젝트 설치·AI workflow·Handoff Template
- 분야 Skill·Reference·기획서·데이터 계약
- Workflow·회귀 Test·checker·fixture
- PDF·DOCX·Dashboard·Manifest·generated map
- GitHub Issue·PR·프로젝트 Sheet

### 4.6 `derivative-and-prompt-drift-attack`

- 파생본의 source·generator·input hash·source Commit이 현재 원본과 일치하는가?
- Prompt가 최신 Base·프로젝트 정본보다 오래된 Skill ID·Gate·경로를 현행 권한으로 주장하는가?
- 첨부 Prompt와 현행 정본이 다르면 `STALE_PROMPT_CONTRACT`를 기록했는가?
- 생성하지 않았거나 렌더하지 않은 파일을 `CURRENT`·`PASSED`로 표시했는가?

## 5. Finding 유형과 검증

후보 Finding:

- `MISSING_CANON`
- `MISSING_CONSUMER`
- `MISSING_SYNC`
- `STALE_REFERENCE`
- `ORPHANED_REFERENCE`
- `CONFLICTING_SOURCE`
- `DUPLICATE_ACTIVE_SOURCE`
- `DERIVATIVE_STALE`
- `STALE_PROMPT_CONTRACT`
- `SUPERSEDED_DECISION_REVIVED`
- `DUPLICATE_WORK`
- `DUPLICATE_QUESTION`
- `UNVERIFIED_DEPENDENCY`

각 비판은 최신 사용자 승인, 실제 파일·diff, 발생 가능성, 영향, 범위, 수정 비용, 코어·호환성 위험을 다시 검증한다.

판정:

- `MUST_FIX`
- `SHOULD_FIX`
- `USER_DECISION_REQUIRED`
- `DEFER`
- `REJECTED_CRITIQUE`
- `BLOCKED_UNVERIFIED`
- `ALLOWED_LEGACY`

심각도가 높다는 이유만으로 자동 `MUST_FIX`가 되지 않는다. 역사 표현을 현재 표현으로 강제해 증거를 파괴하지 않는다.

## 6. 처리 라우팅

| 상황 | 처리 |
|---|---|
| 현행 정본·활성 소비자가 stale | 현재 범위의 최소 수정 후 reference freshness |
| 고유 정보가 있으나 현행 권한 없음 | legacy governance의 reconcile/archive |
| 외부·구형 소비자가 필요 | compatibility stub·alias |
| generated derivative가 stale | 원본·생성기 검증 후 재생성 |
| 둘 이상의 유효한 제품 방향 | `USER_DECISION_REQUIRED` |
| 도구·권한·환경 부족 | `BLOCKED_UNVERIFIED` |
| 역사·Migration·fixture 문맥 | `ALLOWED_LEGACY` |
| 삭제 후보 | deletion gate를 모두 통과한 경우만 승인 삭제 |

사용자 승인 범위 밖 대량 이동·삭제·정본 재선정은 수행하지 않는다.

## 7. 회귀 재검사

수정 뒤 다음을 다시 검사한다.

1. 원 Finding과 실패 사례가 사라졌는가?
2. 최신 Decision·프로젝트 코어·정상 경로가 유지되는가?
3. Registry·entrypoint·Template·Test·파생본 전파가 완료됐는가?
4. 역사·Compatibility·rollback 증거를 훼손하지 않았는가?
5. 실제 코드·데이터·저장·ID·Schema·자산 경로가 유지되는가?
6. 동일 Goal의 중복 PR·Branch·작업이 남지 않았는가?
7. 실행하지 않은 정적·런타임·렌더·Sheets·branch 삭제를 성공으로 표시하지 않았는가?

회귀 판정:

- `PASS`
- `PASS_WITH_FOLLOWUP`
- `REVISE_AGAIN`
- `REJECT_CHANGE`
- `BLOCKED_UNVERIFIED`

## 8. 출력 계약

```md
# 저장소 전체 적대적 감사

## 기준 Branch·Commit·Decision·PR·Sheet 상태
## 검색·인벤토리 범위와 미검증 범위
## 권한 지도와 CURRENT_AUTHORITY
## 중복·stale·고아·Decision 부활 Finding
## UNTOUCHED_CONSUMER와 변경 전파 누락
## Prompt·파생본·Manifest drift
## MUST_FIX / SHOULD_FIX / USER_DECISION_REQUIRED / DEFER
## REJECTED_CRITIQUE / BLOCKED_UNVERIFIED / ALLOWED_LEGACY
## 실제 반영한 최소 변경
## Archive·Compatibility·삭제 판정
## reference freshness·정적·런타임·회귀 결과
## 보호한 코어·고유 정보·정상 경로
## 열린·최근 PR와 Branch cleanup 상태
## 최종 판정·남은 위험·재개 조건
```

## 9. 완료 조건

- tracked 범위 또는 미검증 범위가 명확하다.
- 한 질문의 `CURRENT_AUTHORITY`가 하나다.
- 최신 Decision 누락과 이전 Decision 부활을 검사했다.
- 변경됐어야 할 `UNTOUCHED_CONSUMER`를 판정했다.
- 활성 stale와 `ALLOWED_LEGACY`를 구분했다.
- 파생본·Prompt·Manifest 최신성을 검사했다.
- 검증된 Finding만 수정하고 사용자 결정 영역을 침범하지 않았다.
- 가능한 자동 검사와 회귀를 실제 실행했다.
- 실행하지 못한 검사는 `BLOCKED_UNVERIFIED`다.
