# CI 실행·비용 최적화 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 GitHub Actions 사용량을 변경 위험에 맞게 배분하고, 같은 변경에 전체 검증이 중복 실행되는 것을 막는 공용 정본이다.

## 1. 목표

- 문서만 바뀐 PR에서 다중 운영체제·다중 Python·엔진 전체 검증을 반복하지 않는다.
- 코드·도구·Schema·워크플로 변경에는 통합 신뢰도를 유지하는 충분한 검증을 실행한다.
- `main` 병합, nightly, release 후보에서는 지원 운영체제·런타임 전체 계약을 확인한다.
- 새 커밋이 올라온 PR의 오래된 실행을 자동 취소한다.
- GitHub Actions를 사용할 수 없는 동안 실행하지 못한 검증을 통과로 보고하지 않고, 재개 조건과 정확한 보류 작업을 남긴다.

## 2. 적용 범위

다음에 적용한다.

- Base 자체의 `.github/workflows/**`
- Base 템플릿에서 프로젝트에 설치하는 GitHub Actions
- Godot 프로젝트의 정적 검사·headless 실행·import·테스트·빌드 검증
- Python 기반 문서·Registry·Schema·생성기·governance 검사
- Windows·Linux 교차 플랫폼 발행·경로·인코딩 검증

프로젝트 고유 엔진 버전, Python 지원 버전, 브랜치 보호 Required Check 이름은 해당 프로젝트가 선언한다. Base는 변경 분류·실행 계층·증거 상태의 공용 계약을 제공한다.

## 3. 핵심 원칙

1. **변경 위험에 비례한 검증**: 모든 PR에 가장 비싼 검증을 실행하지 않는다.
2. **증거 손실 금지**: 비용 절감은 필요한 테스트 삭제가 아니라 실행 시점과 대상을 계층화하는 작업이다.
3. **한 SHA당 한 목적의 실행**: PR 검증과 모든 브랜치 push 검증이 같은 커밋에서 중복되지 않게 한다.
4. **안정된 통합 게이트**: Branch protection은 조건부 세부 Job 여러 개보다 항상 종료되는 단일 `ci-gate`를 우선 Required Check로 사용한다.
5. **보류와 통과 분리**: Actions 미사용·권한 제한·결제 제한·runner 장애는 `UNVERIFIED`이며 성공이 아니다.
6. **프로젝트 지원 범위가 정본**: 지원하지 않는 운영체제·Python 버전을 관성적으로 matrix에 추가하지 않는다.

## 4. 변경 분류

변경 파일을 먼저 분류하고 가장 높은 위험 등급을 해당 실행의 등급으로 사용한다.

### 4.1 `DOCS_ONLY`

사람이 읽는 Markdown·문구·주석·정적 설명만 변경되고 다음 항목은 바뀌지 않은 경우다.

- 실행 코드·도구·테스트
- `AGENTS.md`, `START_HERE.md`, Registry, Schema, 정책·계약 문서
- Skill 실행 계약·Template
- package·lockfile·requirements
- `.github/workflows/**`
- Godot script·scene·resource·project 설정
- 생성기 입력·출력·Manifest

권장 검증:

```text
Ubuntu 1개
× 프로젝트 기준 Python 1개
× whitespace·Markdown link·문서 validator
```

LibreOffice·Poppler·Node·브라우저·Godot·Windows가 결과에 영향을 주지 않으면 설치하지 않는다.

### 4.2 `CANONICAL_CONTRACT`

다음처럼 AI·자동화·프로젝트 운영 행동을 바꾸는 정본 변경이다.

- `AGENTS.md`, `START_HERE.md`, Documentation Map
- Skill·Registry·Coverage·Template
- Schema·정책·검증 명령
- 책임 원본 경로·ID·발행 정책

권장 검증:

```text
Ubuntu 1개
× 프로젝트 기준 Python 1개
× 전체 계약·Registry·Schema·reference-freshness 회귀
```

문서 형식이더라도 실행 계약을 바꾸므로 단순 `DOCS_ONLY`로 축소하지 않는다. 다만 Windows publication과 전체 Python matrix는 기본 PR 경로에서 제외한다.

### 4.3 `CODE_OR_ENGINE`

다음 변경이 하나라도 포함되는 경우다.

- Python·GDScript·JavaScript·TypeScript 등 실행 코드
- 검사기·생성기·테스트
- Godot scene·resource·autoload·plugin·project 설정
- package·lockfile·requirements
- 저장·불러오기·공개 Schema·호환성

권장 검증:

```text
Ubuntu 1개
× 프로젝트 기준 Python 1개
× 전체 계약·관련 테스트
× 적용 시 Godot headless·import·런타임 검증
```

모든 코드 PR에 Windows 전체 matrix를 강제하지 않는다. 플랫폼 경로·인코딩·발행 동작을 바꾼 경우에만 PR 단계 Windows smoke를 추가한다.

### 4.4 `CI_TOOLCHAIN_HIGH_RISK`

다음 변경은 CI 자체의 오판·미실행 가능성이 있으므로 별도 고위험으로 분류한다.

- `.github/workflows/**`
- 변경 분류기·통합 게이트
- runner·권한·cache·artifact·dependency 설치
- 지원 OS·Python·Godot matrix
- Branch protection Required Check 계약

권장 검증:

- YAML·정적 정책 테스트
- Ubuntu 전체 계약
- 영향받는 플랫폼의 선택적 smoke
- 사용 가능할 때 `workflow_dispatch` 실제 실행
- Required Check 이름과 `ci-gate` 종료 상태 확인

### 4.5 `FULL_MATRIX`

다음 이벤트에서 지원 범위 전체를 검증한다.

- `main` push 또는 병합 결과
- nightly schedule
- release·release candidate
- 사용자가 요청한 `workflow_dispatch` 전체 검증
- PR의 `ci:full` 같은 명시적 escalation

권장 검증:

```text
지원 Ubuntu·Windows
× 선언된 Python 전체 matrix
× 전체 계약·발행·플랫폼 smoke
× 적용 시 Godot 전체 검증
```

## 5. 이벤트 구조

권장 기본값:

- `pull_request`: 변경 분류 뒤 필요한 최소 계층만 실행한다.
- `push`: `main`과 release branch만 실행한다. 모든 feature branch push를 PR과 중복 실행하지 않는다.
- `schedule`: nightly 전체 matrix를 실행한다.
- `workflow_dispatch`: `auto / docs / contract / code / full` 입력을 제공할 수 있다.

`paths`만으로 복잡한 위험 분류를 완결하려 하지 않는다. 저비용 `classify-changes` Job이 diff를 읽고 다음 출력을 만든 뒤 각 Job의 `if`에서 사용한다.

```yaml
docs_only: true | false
canonical_contract: true | false
code_or_engine: true | false
ci_toolchain_high_risk: true | false
full_matrix: true | false
```

분류가 실패하거나 알 수 없는 파일이 있으면 더 높은 검증 계층으로 안전하게 승격한다.

## 6. 중복 실행 취소

모든 PR 중심 workflow는 최소 다음 계약을 둔다.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

PR 번호를 안정적으로 사용할 수 있는 workflow는 다음 형태를 사용할 수 있다.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true
```

새 커밋이 push되면 같은 PR·workflow의 이전 실행을 취소한다. nightly·release처럼 실행 이력을 보존해야 하는 이벤트는 별도 concurrency group을 사용하거나 취소 정책을 명시한다.

## 7. Job 계층

권장 Job 그래프:

```text
classify-changes
├─ docs-validation
├─ ubuntu-contract
├─ godot-validation
├─ platform-smoke
├─ full-matrix
└─ ci-gate
```

- `classify-changes`: checkout과 diff 판정만 수행한다.
- `docs-validation`: 저비용 문서 검사만 수행한다.
- `ubuntu-contract`: Registry·Schema·도구·회귀의 기준 Job이다.
- `godot-validation`: Godot 변경 또는 전체 검증에서만 실행한다.
- `platform-smoke`: Windows 경로·발행·인코딩 영향이 있을 때만 실행한다.
- `full-matrix`: main·nightly·release·명시적 escalation에서 실행한다.
- `ci-gate`: 선택된 Job의 성공·실패·취소·미실행을 판정하고 항상 종료한다.

Branch protection은 조건부 Job 이름을 모두 Required Check로 묶지 않는다. `ci-gate`가 필요한 Job이 누락·실패·취소됐는지 검사하고, Branch protection은 가능한 한 `ci-gate` 하나를 요구한다.

## 8. 설치·cache·artifact 절감

- 고비용 의존성은 실제 사용하는 Job에서만 설치한다.
- 문서 문구 변경에 LibreOffice·Poppler·브라우저·Godot를 설치하지 않는다.
- lockfile 기반 cache key를 사용하고, cache miss가 검증 실패를 숨기지 않게 한다.
- 생성물 자체를 cache로 오인하지 않는다. 정본과 재생성 검증은 유지한다.
- report artifact는 실패·진단 필요 시 우선 업로드하고 retention을 짧게 둔다.
- 동일 Job 안에서 같은 의존성 설치·같은 전체 테스트를 두 번 실행하지 않는다.
- matrix 각 축의 목적을 설명하지 못하면 축을 제거하거나 nightly로 이동한다.

## 9. GitHub Actions 사용 불가 계약

결제·사용량·권한·조직 정책·runner 장애로 Actions를 실행할 수 없으면 다음 상태를 사용한다.

```text
BLOCKED_BY_GITHUB_ACTIONS
판정: UNVERIFIED
```

작업 보고와 Issue·PR에는 다음을 남긴다.

```yaml
actions_availability: unavailable
completed_without_actions:
  - 실제 수행한 로컬·정적 검사
pending_actions_validation:
  - workflow 파일
  - event 또는 workflow_dispatch 입력
  - 실행해야 할 Job
  - 기대하는 Required Check
  - 확인할 artifact·log·결과
resume_condition: 사용자가 GitHub Actions 사용 가능 상태를 알림
risk_until_resumed:
rollback_path:
```

금지:

- workflow 파일이 존재한다는 이유로 실행 통과를 주장한다.
- Actions 사용량이 복구되지 않았는데 반복 재실행한다.
- 보류된 전체 matrix를 `ACCEPT` 근거로 사용한다.
- 사용 가능해졌다는 사용자 알림 뒤 기준 branch·SHA를 갱신하지 않고 오래된 결과를 실행한다.

재개 절차:

```text
사용 가능 알림
→ 대상 branch·최신 SHA·workflow diff 재확인
→ 보류 목록에서 아직 필요한 검증만 선택
→ workflow_dispatch 또는 해당 이벤트 실행
→ Job·log·artifact·Required Check 확인
→ UNVERIFIED 판정 갱신
```

## 10. 공용 기본 실행 표

| 변경·이벤트 | 기본 OS | Python | 문서·계약 | Godot | 전체 matrix |
|---|---|---|---|---|---|
| 일반 문서만 변경 | Ubuntu | 기준 1개 | 문서 validator | 제외 | 제외 |
| 정본·Skill·Registry 변경 | Ubuntu | 기준 1개 | 전체 계약·reference freshness | 영향 시 | 제외 |
| 코드·도구·테스트 변경 | Ubuntu | 기준 1개 | 전체 계약 | 영향 시 실행 | 제외 |
| 플랫폼 발행·경로 변경 | Ubuntu + 영향 OS smoke | 기준 1개 | 전체 계약 | 영향 시 실행 | 제외 |
| CI·matrix·게이트 변경 | Ubuntu + 영향 OS smoke | 기준 1개 | 정책·전체 계약 | 영향 시 실행 | 실제 workflow 검증 필요 |
| main·nightly·release·수동 full | 지원 OS 전체 | 지원 버전 전체 | 전체 | 적용 시 전체 | 실행 |

프로젝트가 이 표보다 강한 규제·보안·플랫폼 계약을 가지면 프로젝트 규칙을 우선한다.

## 11. 완료 기준

CI 최적화는 다음을 모두 만족해야 완료다.

- 변경 분류 규칙과 안전한 fallback이 있다.
- 문서 전용 PR에서 고비용 전체 검증이 실행되지 않는다.
- 코드·계약 변경은 Ubuntu 기준 전체 검증을 건너뛰지 않는다.
- main·nightly·release에서 선언된 전체 matrix가 실행된다.
- `concurrency.cancel-in-progress`가 PR의 오래된 실행을 취소한다.
- PR과 feature branch push가 같은 SHA에서 전체 검증을 중복하지 않는다.
- 조건부 Job이 있어도 `ci-gate`가 Required Check 계약을 안정적으로 종료한다.
- Actions 미사용 상태의 보류 Job·재개 조건·위험이 명시된다.
- 실행한 정적 검사와 실제 Actions 결과가 분리되어 보고된다.
- 기존 검증 증거를 단순 삭제해 비용을 줄이지 않았다.

## 12. 관련 Skill

주 실행 Skill은 `skills/reviewing-and-validating-project-changes/SKILL.md`의 `ci-cost-optimization` Mode다.

연결 책임:

- 구조 중복 제거: `refactoring-with-contract-preservation`
- 정본·Workflow 참조 전파: `auditing-canonical-reference-freshness`
- 로컬·원격 SHA와 실행 상태 확인: `synchronizing-local-and-github-state`
- 작업 계약·Codex 실행 순서: `managing-project-intake-and-work-contract`
