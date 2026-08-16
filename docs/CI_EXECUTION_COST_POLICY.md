# CI 실행·비용 최적화 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 GitHub Actions 사용량을 변경 위험에 맞게 배분하고, 검증 신뢰도를 보존하면서 원격 CI와 제한적 로컬 fallback의 책임을 분리하는 공용 정본이다.

**상위 비용 Gate — `ZERO_INCREMENTAL_COST_REQUIRED`:** CI·자동화도 사용자의 추가 금전 지출을 만들지 않는 실행 경로만 기본 허용한다. 현재 저장소·계정에서 별도 과금이 없다고 확인된 standard runner·기존 로컬 환경은 사용할 수 있지만, `pay-as-you-go` API·유료 credit·larger/GPU runner·유료 storage·marketplace·기타 separately metered service는 사용자가 이 정책을 명시적으로 바꾸기 전에는 실행하지 않는다. 비용 상태를 확인할 수 없으면 실제 유료 가능 실행을 시작하지 않고 `COST_GATE_BLOCKED`로 둔다. 이 Gate는 필요한 검증을 삭제하는 권한이 아니라 **무료로 재현 가능한 검증 경로를 선택하거나 검증을 정직하게 보류하는 권한 경계**다.

## 1. 목표

- 문서만 바뀐 PR에서 다중 운영체제·다중 Python·엔진 전체 검증을 반복하지 않는다.
- 코드·도구·Schema·워크플로 변경에는 통합 신뢰도를 유지하는 충분한 검증을 실행한다.
- `main` 병합, nightly, release 후보에서는 지원 운영체제·런타임 전체 계약을 확인한다.
- 새 커밋이 올라온 PR의 오래된 실행을 자동 취소한다.
- 추가비용 0이 확인된 공개 저장소의 standard GitHub-hosted runner는 기본 `REMOTE_CI`로 사용한다.
- Actions 인프라가 실제로 검증 실행을 소유하지 못한 경우에만 엄격한 `LOCAL_FALLBACK`을 검토한다.
- 실행하지 못했거나 locally reproducible 하지 않은 검증을 통과로 보고하지 않는다.

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
4. **안정된 통합 게이트**: Branch protection은 항상 종료되는 단일 `ci-gate`를 우선 Required Check로 사용한다.
5. **두 실행 모드**: `REMOTE_CI`와 `LOCAL_FALLBACK`만 존재하며 기본은 `REMOTE_CI`다. 라우터는 세 번째 모드가 아니다.
6. **원격 소유권 우선**: 현재 PR head에 canonical `REMOTE_CI workflow run`이 하나라도 있으면 final `ci-gate` Check Run이 아직 생기지 않았더라도 원격 CI가 해당 SHA를 소유한다.
7. **실패 우회 금지**: `ci-gate` Check Run·commit status가 이미 있거나 테스트·workflow가 실패·취소·대기·실행 중이면 `LOCAL_FALLBACK`으로 덮지 않는다.
8. **등가 증거만 허용**: fallback은 현재 로컬 검증 계약으로 locally reproducible 한 변경만 성공 처리한다.
9. **보류와 통과 분리**: 필요한 증거가 로컬에서 동등하게 재현되지 않으면 `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`다.
10. **프로젝트 지원 범위가 정본**: 지원하지 않는 운영체제·Python 버전을 관성적으로 matrix에 추가하지 않는다.
11. **0원 Gate 우선**: 동일한 검증 목표에 separately metered 실행이 필요하면 자동 결제 경로로 우회하지 않고 무료 동등 경로를 찾거나 `COST_GATE_BLOCKED / UNVERIFIED`로 보류한다.

저장소 전체에서 `name: ci-gate`를 노출하는 Job은 하나뿐이어야 한다. 그 Job을 소유한 Workflow의 `pull_request` 이벤트에는 Workflow-level `paths`·`paths-ignore`를 두지 않고 내부 분류 Job에서 비용 계층을 선택한다. 집중 Workflow는 path filter를 사용할 수 있지만 `ci-gate` 이름을 재사용하지 않는다.

GitHub Actions의 정상 `ci-gate`는 Check Run이고, 제한적 로컬 fallback은 같은 Required Check 문맥의 commit status를 사용할 수 있다. 같은 이름의 Check와 status가 동시에 존재하면 병합 조건이 중첩될 수 있으므로 local fallback은 원격 workflow run, Check Run, 기존 commit status의 부재를 검증 전후 모두 확인한다.

## 4. 변경 분류

변경 파일을 먼저 분류하고 가장 높은 위험 등급을 해당 실행의 등급으로 사용한다.

### 4.1 `DOCS_ONLY`

사람이 읽는 Markdown·문구·정적 설명만 변경되고 실행 코드·도구·테스트·Schema·Skill 실행 계약·package·lockfile·workflow·Godot runtime 파일이 바뀌지 않은 경우다.

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

문서 형식이더라도 실행 계약을 바꾸므로 단순 `DOCS_ONLY`로 축소하지 않는다. 다만 Windows publication과 전체 Python matrix가 결과에 영향을 주지 않으면 기본 PR 경로에서 제외한다.

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

`CODE_OR_ENGINE`은 현재 Base의 일반 `LOCAL_FALLBACK`에서 기본적으로 locally reproducible 로 간주하지 않는다. 별도 프로젝트가 동등한 로컬 엔진·플랫폼 검증 계약을 명시적으로 추가하기 전에는 Actions 불가 시 `BLOCKED_BY_GITHUB_ACTIONS / UNVERIFIED`다.

### 4.4 `CI_TOOLCHAIN_HIGH_RISK`

다음 변경은 CI 자체의 오판·미실행 가능성이 있으므로 별도 고위험으로 분류한다.

- `.github/workflows/**`
- 변경 분류기·통합 게이트
- runner·권한·cache·artifact·dependency 설치
- 지원 OS·Python·Godot matrix
- Branch protection Required Check 계약
- `tools/run_local_ci_fallback.py`처럼 Required Check 증거를 발행하는 대체 검증 도구

권장 검증:

- YAML·정적 정책 테스트
- Ubuntu 전체 계약
- 영향받는 플랫폼의 선택적 smoke
- 사용 가능할 때 실제 Actions 실행
- Required Check 이름과 `ci-gate` 종료 상태 확인
- fallback 도구 변경 시 dirty/stale/SHA drift/workflow-run race/Check Run race/existing status/status target 회귀

`CI_TOOLCHAIN_HIGH_RISK` 역시 자신의 대체 검증기를 자기 자신만으로 승인할 수 없으므로 현재 일반 fallback 성공 대상이 아니다.

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

저비용 `classify-changes` Job이 diff를 읽고 다음 출력을 만든 뒤 각 Job의 `if`에서 사용한다.

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

## 9. `REMOTE_CI` / `LOCAL_FALLBACK` 계약

### 9.1 `REMOTE_CI` — 기본 모드

- 현재 저장소·계정에서 추가비용 0이 확인된 standard GitHub-hosted runner를 사용할 수 있으면 `REMOTE_CI`를 기본으로 사용한다.
- 기존 변경 분류, 조건부 publication/Windows smoke, evaluator, Required Check `ci-gate`를 그대로 사용한다.
- larger/GPU runner, 유료 storage, 미래의 private repository 등 과금 가능성이 있는 실행은 default authority 밖이며, 비용이 0임을 확인하지 못하면 `COST_GATE_BLOCKED`다.
- 현재 head에 canonical `REMOTE_CI workflow run`이 존재하면 final `ci-gate` Check Run이 아직 생성되지 않았더라도 해당 SHA는 `REMOTE_CI` 소유다.
- `ci-gate` Check Run 또는 commit status가 이미 존재하면 local fallback은 기존 증거를 덮지 않는다.
- `ci-gate`가 실패·취소·queued·in progress이면 원인을 수정하거나 원격 실행을 재개한다. 테스트 실패나 workflow 실패를 이유로 fallback으로 전환하지 않는다.

### 9.2 `LOCAL_FALLBACK` — 인프라 전용 대체 모드

Actions 서비스·권한·조직 정책·runner 가용성 등으로 현재 PR head에 canonical `REMOTE_CI workflow run` 자체가 만들어지지 않았고, 같은 head/test-merge에 `ci-gate` Check Run 또는 기존 `ci-gate` commit status도 없는 경우에만 검토한다.

```text
python tools/run_local_ci_fallback.py \
  --repo <owner/repo> \
  --pr <number> \
  --trusted-history-commit <current-origin-base-sha> \
  --base main
```

도구는 다음을 모두 fail-closed로 확인한다.

1. `gh auth status`와 GitHub API 접근이 성공한다.
2. PR이 열려 있고 기대 base branch와 일치한다.
3. local `HEAD`가 PR `head.sha`와 정확히 같다.
4. worktree가 검증 전 깨끗하다.
5. `git fetch origin <base>` 후 최신 `origin/<base>`가 `HEAD`의 ancestor다.
6. 사용자가 전달한 `--trusted-history-commit`이 방금 fetch한 정확한 `origin/<base>` SHA와 같다.
7. 변경 파일이 현재 fallback 계약으로 locally reproducible 하다.
8. current head에 canonical `REMOTE_CI workflow run`이 없다.
9. PR head와 current test merge SHA에 `ci-gate` Check Run이 없다.
10. PR head와 current test merge SHA에 기존 `ci-gate` commit status가 없다.
11. 기존 `tools/run_local_validation.py --trusted-history-commit <current-origin-base-sha>`가 성공한다.
12. 검증 후 local HEAD·worktree·PR head가 변하지 않았다.
13. 재-fetch한 `origin/<base>` SHA가 검증 시작 때와 같다.
14. locally reproducible 변경 경계가 그대로 유지된다.
15. status 발행 직전에 canonical `REMOTE_CI workflow run`, head/test-merge의 `ci-gate` Check Run·commit status 부재를 다시 확인한다.
16. 위 조건이 모두 통과한 exact head SHA에만 commit status `context=ci-gate`, `state=success`를 발행한다.

### 9.3 Locally reproducible 기본 경계

Base의 공용 fallback은 의도적으로 보수적이다.

기본 허용:

- `.md`, `.txt` 문서
- `docs/`, `skills/`, `templates/`, `schemas/`, `references/` 아래의 검증 가능한 `.json`, `.yaml`, `.yml` 정본/템플릿
- 위 파일들만으로 구성되고 `run_local_validation.py`가 필요한 계약 검사를 재현할 수 있는 `DOCS_ONLY` 또는 제한적 `CANONICAL_CONTRACT`

기본 차단:

- `.github/workflows/**`
- `tools/**`, `tests/**`, `scripts/**`, `addons/**`
- Python/GDScript/JS/TS/shell/binary/native library
- Godot scene/resource/project 설정
- package/requirements/lockfile
- `CODE_OR_ENGINE`
- `CI_TOOLCHAIN_HIGH_RISK`
- 기타 명시적으로 locally reproducible 하다고 증명되지 않은 파일

프로젝트가 실제 Godot headless, Windows, publication 등 원격 CI 증거와 동등한 로컬 계약을 별도로 구현·테스트한 뒤에는 프로젝트 정본에서 범위를 확대할 수 있다. 그 계약이 없으면 차단을 유지한다.

### 9.4 fallback이 불가능한 경우

다음 중 하나라도 해당하면 기존 blocked 상태를 유지한다.

```text
BLOCKED_BY_GITHUB_ACTIONS
판정: UNVERIFIED
```

- canonical `REMOTE_CI workflow run` 또는 기존 `ci-gate` Check Run/status가 존재한다.
- 테스트·evaluator·workflow 자체가 실패했다.
- 로컬 환경에서 Required Check의 필수 증거를 재현할 수 없다.
- 변경이 locally reproducible 기본 경계를 벗어난다.
- exact head, clean worktree, current base ancestry를 증명할 수 없다.
- GitHub API 또는 인증 상태를 검증할 수 없다.
- 필요한 platform/runtime/Godot/publication 증거가 로컬에서 실행 불가능하다.

작업 보고와 Issue·PR에는 다음을 남긴다.

```yaml
validation_mode: REMOTE_CI | LOCAL_FALLBACK
actions_availability: available | infrastructure_unavailable
head_sha:
base_sha:
completed_validation:
pending_validation:
required_check: ci-gate
resume_condition:
risk_until_resumed:
rollback_path:
```

금지:

- workflow 파일이 존재한다는 이유로 실행 통과를 주장한다.
- 테스트 실패·evaluator 실패·workflow 오류를 `LOCAL_FALLBACK`으로 덮는다.
- canonical `REMOTE_CI workflow run`이 있는데 final `ci-gate` Check Run이 아직 없다는 이유로 fallback을 시작한다.
- 기존 `ci-gate` Check Run 또는 commit status를 local status로 덮는다.
- 검증한 SHA와 다른 commit에 success status를 발행한다.
- stale base나 dirty worktree에서 success status를 발행한다.
- locally reproducible 하지 않은 변경을 local validator만으로 승인한다.
- 보류된 전체 matrix를 `ACCEPT` 근거로 사용한다.

재개 절차:

```text
Actions 사용 가능 상태 확인
→ 대상 branch·최신 SHA·workflow diff 재확인
→ REMOTE_CI 실행 또는 기존 실행 재개
→ Job·log·artifact·Required Check 확인
→ LOCAL_FALLBACK status가 있었더라도 새 Check Run 결과를 우선 확인
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

- `ZERO_INCREMENTAL_COST_REQUIRED`와 `COST_GATE_BLOCKED`가 CI 선택보다 우선한다.
- 변경 분류 규칙과 안전한 fallback이 있다.
- 실행 모드는 `REMOTE_CI`와 `LOCAL_FALLBACK` 두 개이며, 추가비용 0이 확인된 원격 CI가 기본이다.
- 무료로 사용할 수 있는 standard GitHub-hosted runner를 단지 로컬이 더 싸 보인다는 이유로 우회하지 않는다.
- 비용 상태가 불명확한 separately metered runner·storage·service를 자동 실행하지 않는다.
- 문서 전용 PR에서 고비용 전체 검증이 실행되지 않는다.
- 코드·계약 변경은 필요한 Ubuntu 기준 검증을 건너뛰지 않는다.
- main·nightly·release에서 선언된 전체 matrix가 실행된다.
- `concurrency.cancel-in-progress`가 PR의 오래된 실행을 취소한다.
- PR과 feature branch push가 같은 SHA에서 전체 검증을 중복하지 않는다.
- 조건부 Job이 있어도 `ci-gate`가 Required Check 계약을 안정적으로 종료한다.
- canonical `REMOTE_CI workflow run`, `ci-gate` Check Run 또는 기존 status가 존재하면 `LOCAL_FALLBACK`이 성공 status를 발행하지 못한다.
- fallback은 locally reproducible 변경에서만 exact head/current base/clean tree를 검증하고 성공 status를 발행한다.
- `CODE_OR_ENGINE`·`CI_TOOLCHAIN_HIGH_RISK`는 별도 동등 로컬 계약이 없으면 fallback 성공 대상이 아니다.
- fallback을 실행할 수 없는 상태의 보류 Job·재개 조건·위험이 명시된다.
- 실행한 정적 검사와 실제 Actions 결과가 분리되어 보고된다.
- 기존 검증 증거를 단순 삭제해 비용을 줄이지 않았다.

## 12. 관련 Skill

주 실행 Skill은 `skills/reviewing-and-validating-project-changes/SKILL.md`의 `ci-cost-optimization` Mode다.

연결 책임:

- 구조 중복 제거: `refactoring-with-contract-preservation`
- 정본·Workflow 참조 전파: `auditing-canonical-reference-freshness`
- 로컬·원격 SHA와 실행 상태 확인: `synchronizing-local-and-github-state`
- 작업 계약·Codex 실행 순서: `managing-project-intake-and-work-contract`