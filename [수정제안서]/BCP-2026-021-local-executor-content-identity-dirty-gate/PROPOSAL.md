# Base Change Proposal — Local Executor Content-Identity Dirty Gate

## 출처와 상태

```yaml
proposal_id: BCP-2026-021-local-executor-content-identity-dirty-gate
status: SUBMITTED
knowledge_state: PATTERN
source_project: alsdmlals4-eng/urban-legend
source_commit: f46258233246be04f0efbef637e95710af6f5af5
source_project_pr: https://github.com/alsdmlals4-eng/urban-legend/pull/199
source_project_exact_head: 59306138d100db72e815d18798322290c3f6bc94
source_project_owner: docs/CURRENT_HANDOFF.md
submitted_at: 2026-08-12
existing_solution_verdict: ABSORB
base_owner_candidate: ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP / PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
proposal_storage_merge_authority: GRANTED_BY_CURRENT_HANDOFF_INSTRUCTION
base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE
approval_ref: null
implementation_pr: null
```

이 제안은 `urban-legend`의 CASE-01 Phase C 전용 로컬 실행환경을 복구하는 과정에서 관찰된 Git false-dirty 진단 문제에서 추출했다. 프로젝트 적용 부분은 PR #199로 먼저 `docs/CURRENT_HANDOFF.md`에 반영·검증·병합되었고, 이 문서는 그중 재사용 가능한 공용 원리만 Base 제안으로 분리한다.

이 PR이 Base에 병합되더라도 구현 승인을 뜻하지 않는다. 활성 Base Skill/Docs/Template/Test/Tool/Workflow 변경은 별도 후속 단계다.

## 관찰과 증거

### 실제 프로젝트 증상

전용 Godot/HiGodot 실행환경을 구성하는 과정에서 tracked `.import` 파일 111개가 `git status`에서 working-tree modified로 표시되었다. 초기에는 EOL 변환, Godot importer rewrite, Godot AI self-update 등 여러 원인을 의심했고, destructive cleanup 없이 단계적으로 분리 진단했다.

대표 파일 `addons/gut/fonts/AnonymousPro-Bold.ttf.import`에서 최종 관찰값은 다음과 같았다.

```text
INDEX    : 23867ed44fa29a70a38d9a9dc8128d28059c437a
RAW      : 23867ed44fa29a70a38d9a9dc8128d28059c437a
FILTERED : 23867ed44fa29a70a38d9a9dc8128d28059c437a
INDEX == RAW      : YES
INDEX == FILTERED : YES

git diff --quiet       exit : 0
git diff-files --quiet exit : 1
porcelain v2            : .M
index mode              : 100644
working mode            : 100644
```

`git check-attr`은 해당 경로에 `text: auto`만 보고했고 global attributes file은 없었다. Git LFS filter 설정은 시스템/사용자 config에 존재했지만 이 파일의 path-filtered blob은 index/raw blob과 동일했다.

중요한 증거 상한:

- 대표 파일 1개에 대해서는 `INDEX == RAW == FILTERED`와 porcelain content diff 없음이 확인됐다.
- 앞선 진단에서 111개 `.import` 모두 `git diff --ignore-space-at-eol --quiet` 기준 semantic difference 0으로 관찰됐다.
- 그러나 **111개 전체에 대한 index/raw/path-filtered blob 동일성 검증은 아직 `NOT_RUN`**이다.
- 따라서 이 제안은 “111개 전부가 stat-only였다”를 사실로 승격하지 않는다. 실제 관찰에서 드러난 **content identity 판정 절차와 evidence classification gap**을 공용 후보로 제안한다.

### 실패하거나 오해를 만든 접근

1. `git status`의 `M`만으로 semantic user-content mutation이라고 간주.
2. `core.autocrlf=false` 또는 `core.eol=lf`만 적용하면 dirty 표시가 사라질 것으로 기대.
3. `git update-index --really-refresh`의 `needs update`를 실제 content 변경의 직접 증거로 해석.
4. readiness를 만들기 위해 `reset`, `restore`, `clean`, `assume-unchanged`, `skip-worktree` 같은 상태 변경을 고려.

프로젝트에서는 위 접근을 중단하고 staged diff, index blob, raw working blob, path-filtered working blob, mode, porcelain content diff, attribute/filter context를 분리해서 관찰했다.

### 현재 Base coverage

Base의 `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` 설계는 이미 다음을 요구한다.

- bootstrap이 user work를 reset/restore/clean/stage/rewrite하지 않을 것;
- broad Git diff/repository-wide noisy diagnostics를 Codex 진입의 기본 전제처럼 수행하지 않을 것;
- `KNOWN_LF_CRLF_OR_STAT_NOISE_FLOOD`를 adversarial launcher lens로 공격할 것;
- process/port 존재만 readiness로 간주하지 않을 것.

따라서 새 broad Skill은 필요하지 않다. gap은 **known stat-noise를 발견했을 때 semantic dirty와 metadata/stat-only candidate를 안전하게 구분하는 최소 evidence gate**다. Existing Solution verdict는 `ABSORB`다.

### 공식 Git benchmark

Git 공식 문서는 이 관찰과 같은 계층 차이를 명시한다.

- `git diff`의 `diff.autoRefreshIndex`는 working-tree 내용이 index와 같으면 stat-only 차이를 changed로 취급하지 않으며, 이 동작은 porcelain `git diff`에만 적용되고 lower-level `git diff-files`에는 적용되지 않는다.
- `git hash-object --no-filters`는 attributes/EOL 변환을 포함한 input filter를 무시하고 raw file content를 해시한다.
- `git hash-object --path=<path>`는 해당 repository path에 적용될 filter를 고려한 object ID를 계산한다.

공식 출처:

- https://git-scm.com/docs/git-diff
- https://git-scm.com/docs/git-hash-object
- https://git-scm.com/docs/git-diff-index

## 일반화 후보

### 제안 원리

로컬 executor/bootstrap readiness에서 Git working-tree dirtiness를 검사할 때 **`git status` 또는 lower-level `git diff-files` 신호만으로 semantic user-content mutation을 확정하지 않는다.** 동시에 이 신호를 무시하거나 숨기지도 않는다.

known stat/EOL noise가 bounded candidate set으로 식별된 경우에만 다음 최소 증거 순서로 분류한다.

```text
staged diff 확인
→ index mode / working mode 확인
→ index blob ID
→ raw working blob ID (--no-filters)
→ path-filtered working blob ID (--path)
→ porcelain content diff
→ attributes / relevant filter context
→ classification
```

고신뢰 `CONTENT_IDENTICAL_STAT_ONLY_CANDIDATE` 분류 조건:

```text
staged change 없음
AND mode identity 유지
AND index_blob == raw_working_blob
AND index_blob == path_filtered_working_blob
AND porcelain git diff reports no content difference
```

조건 하나라도 불충족하면 `DIRTY_UNVERIFIED` 또는 실제 semantic dirty로 유지한다. 이 분류는 파일을 clean으로 만드는 명령이 아니라 **증거 분류**다.

### 실행 원칙

- 기본 preflight는 계속 작고 빠르게 유지한다.
- repository-wide hash scan을 새 기본 절차로 만들지 않는다.
- known-noise가 readiness를 가로막고 실제 원인 구분이 필요한 bounded candidate set에서만 deep classification을 수행한다.
- 분류 결과를 receipt/handoff에 남길 수는 있지만, `git status clean`이라는 거짓 주장은 하지 않는다.
- genuine dirty가 한 파일이라도 섞이면 해당 파일은 별도로 보존하고 blocker/risk로 처리한다.
- classification을 만들기 위해 `reset`, `restore`, `clean`, `git add`, `assume-unchanged`, `skip-worktree`를 사용하지 않는다.

## 적용 조건과 비사용 조건

### Use When

- editor/importer/tool 실행 뒤 많은 tracked 파일이 modified로 보이지만 실제 source mutation 여부가 불명확할 때;
- `git diff`와 `git diff-files`/status가 서로 다른 신호를 보일 때;
- EOL/filter/index metadata가 false-dirty 원인 후보일 때;
- destructive cleanup 없이 기존 user/tool work를 보존하면서 readiness를 판정해야 할 때;
- candidate path 집합이 bounded되어 있고 deep classification 비용이 합리적일 때.

### Do Not Use When

- staged diff가 실제로 존재할 때;
- index/raw/path-filtered blob 중 하나라도 다를 때;
- file mode/type이 바뀌었을 때;
- unmerged/conflict/submodule/symlink 상태를 일반 파일 stat-noise로 축약하려 할 때;
- candidate set 자체가 불명확해 repository-wide hashing이 필요해지는 상황에서 bootstrap latency를 숨기려 할 때;
- 단순히 dirty worktree를 무시하고 작업을 강행하기 위한 면책 장치로 사용할 때.

### Project-Specific Boundary

다음 값은 `urban-legend`에 남고 Base 공용 구현 후보에 하드코딩하지 않는다.

- Godot 4.7.1 exact executable path;
- HiGodot HTTP 8004 / WS 9504;
- Godot AI 3.1.2 dev-mode override;
- Hera v1.0.0 exact local setup;
- `pr198-exec` worktree/path/branch;
- CASE-01 테스트 파일명과 `.import` 111개 관찰 수;
- PR #198 product authority/Decision IDs.

## 반례와 위험

### Counterexamples

1. **실제 source edit**: raw/path-filtered hash가 index와 다르면 stat-only가 아니다.
2. **filter transformation**: raw hash는 다르더라도 path-filtered hash가 index와 같을 수 있다. 이 경우 raw equality를 무조건 요구하면 false negative가 될 수 있으므로 향후 구현 설계에서 filter-aware 정책을 별도 검증해야 한다. 현재 제안은 높은 보수성 때문에 raw equality까지 요구한다.
3. **mode-only semantic change**: content hash가 같아도 executable bit/type이 달라지면 동일 상태가 아니다.
4. **staged user work**: working content가 같아 보여도 index가 HEAD와 다르면 bootstrap이 이를 숨겨서는 안 된다.
5. **partial population/sparse checkout**: 일반 working file의 stat-noise gate를 기계적으로 적용하면 안 된다.

### Risks

- 해시 검증을 과도하게 일반화하면 대형 저장소 bootstrap이 느려질 수 있다.
- “content-identical”이라는 분류를 “worktree clean”으로 잘못 표현하면 이후 staging에서 원치 않는 파일이 섞일 수 있다.
- filter semantics를 충분히 이해하지 않고 raw/path-filtered hash를 사용하면 false positive/negative가 생길 수 있다.
- Windows filesystem timestamp granularity, antivirus/indexer, editor import 동작 등 trigger는 환경별로 달라질 수 있다.

### Adversarial findings

- `MUST_FIX`: full-repository deep scan을 기본 preflight로 요구하지 않는다 — 제안에 반영됨.
- `MUST_FIX`: 대표 파일 1개의 증거를 111개 전체 사실로 승격하지 않는다 — evidence ceiling에 반영됨.
- `MUST_FIX`: stat-only classification이 genuine content/mode/staged change를 숨기지 못하도록 fail-closed 조건을 둔다 — 반영됨.
- `SHOULD_FIX`: filter-aware raw-vs-clean semantics는 future implementation design에서 fixture로 검증 필요.
- `REJECTED_CRITIQUE`: 새 broad Skill이 필요하다는 주장 — existing Base owner가 이미 dedicated local bootstrap/stat-noise lens를 소유하므로 `ABSORB`가 우선.

## 영향 범위와 검증

### Potential Affected Consumers — future implementation only

이 proposal 자체는 아래 활성 파일을 수정하지 않는다. 별도 구현 승인이 생길 경우 최소 후보는 기존 owner에 흡수한다.

- `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` contract/reference
- project-dedicated local execution environment guidance
- Godot live-editor project-operations template의 generic preflight diagnostics
- existing bootstrap contract tests
- project handoff/receipt guidance where a generic classification locator is useful

새 broad Skill/Registry entry를 기본 해법으로 만들지 않는다.

### Validation Plan — future implementation stage

1. clean worktree fixture remains fast and avoids deep hash scan.
2. same-content timestamp/stat mutation fixture is not rejected as semantic dirty after bounded classification.
3. real content edit fails classification.
4. staged change fails classification.
5. mode/type change fails classification.
6. filter-aware fixture verifies `--no-filters` vs `--path` semantics and conservative policy.
7. no destructive Git state mutation occurs.
8. no project-specific paths/ports/tool versions leak into Base generic contract.
9. existing one-shot bootstrap and project operating-contract regressions remain green.

### Regression Plan

- preserve `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`;
- preserve minimal preflight/no noisy repository-wide dump;
- preserve no reset/restore/clean/stage/rewrite boundary;
- preserve exact project/worktree/session readiness receipts;
- preserve project-specific tool authority downstream.

### Rollback

Proposal stage rollback is deletion/rejection of this BCP and its Registry entry before implementation. Future implementation, if separately approved, should be an additive classification branch in the existing bootstrap owner and must be removable without changing project-specific runtime authority.

## 승인과 구현

```yaml
proposal_status: SUBMITTED
user_implementation_approval: NOT_GRANTED_IN_THIS_STAGE
approval_ref: null
implementation_status: NOT_STARTED_IN_THIS_STAGE
implementation_pr: null
implementation_boundary: SEPARATE_FOLLOWUP_STAGE
```

현재 실행의 권한은 이 proposal을 `[수정제안서]/**`에 저장·검증·proposal-only PR로 병합하는 데까지다. 이 문서의 병합을 `APPROVED_FOR_IMPLEMENTATION`으로 승격하지 않는다.
