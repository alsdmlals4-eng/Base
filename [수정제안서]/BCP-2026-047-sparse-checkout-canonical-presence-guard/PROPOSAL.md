# BCP-2026-047 — Sparse Checkout Canonical Presence Guard

## 출처와 상태

~~~yaml
proposal_id: BCP-2026-047-sparse-checkout-canonical-presence-guard
status: SUBMITTED
knowledge_state: OBSERVATION
source_project: alsdmlals4-eng/urban-legend
source_commit: 756e8469853059ab15d304e55409210126a17b6d
submitted_at: 2026-08-31
existing_solution_verdict: ADAPT_EXISTING_DIRTY_GATE_BOUNDARY
base_implementation_authority: NOT_GRANTED_IN_THIS_STAGE
approval_ref: "2026-08-31 current user instruction: Base promotion evaluation and proposal submission authorized; active implementation remains unapproved."
implementation_pr: null
~~~

Urban Legend 작업에서 current commit에 추적된 문서가 working tree에는 존재하지 않아 파일 누락처럼 보였던 사례를 출처로 한다. 확인 결과 그 경로는 삭제되거나 손상된 것이 아니라 sparse checkout으로 생략되어 있었다. 이 BCP는 그 관찰을 공용화 후보로 보존하는 proposal-only 자료다. Base 활성 계약, Skill, template, test, registry of active skills를 이번 단계에서 변경하지 않는다.

## 후보보고서 상태와 정본 경계

CANDIDATE_REPORT_IS_NOT_BASE_CANON

- 후보보고서·첨부물의 역할: Urban Legend checkout 관찰과 안전한 진단 순서.
- Base 정본 또는 구현 지시가 아닌 이유: 단일 프로젝트 관찰이며, 다른 repository·submodule·partial clone·filter 환경에 대한 반복 검증은 아직 없다.
- 제외한 프로젝트 고유 내용: Urban Legend worktree 경로, Godot 테스트 이름, Base adapter pin, case ID, 이미지·UI·게임 규칙, 해당 세션의 sparse path 목록.

## 관찰과 증거

### 실제로 확인한 작업·구현·검증

1. 필요한 current 문서를 working tree에서 읽지 못해 누락·삭제 가능성을 확인했다.
2. 같은 repository path의 HEAD blob 존재와 index 표시를 비교했고, sparse omission을 나타내는 skip-worktree 상태를 확인했다.
3. current source의 정확한 blob을 working tree에 복원한 뒤, 의도하지 않은 tracked diff가 만들어지지 않았음을 확인했다.
4. 절차는 reset, clean, force checkout, broad restore로 user work를 지우지 않았고 정확히 확인된 누락 경로에만 적용됐다.

### 추측·미실행 항목과 evidence ceiling

- sparse checkout이 언제나 문서 누락의 원인이라는 주장은 하지 않는다.
- 다른 Git client, partial clone, submodule, LFS, filter/EOL, unmerged state, 파일 권한 오류, 실제 삭제를 같은 현상으로 분류하지 않는다.
- 다른 프로젝트 반복성, 실제 Base owner, Base runtime/tooling 구현 검증은 NOT_RUN이다.

## 공통 교훈과 일반화 후보

COMMON_LESSON_AND_CORRECTION_REQUEST_REQUIRED

### 제안 원리

tracked file을 working tree에서 읽지 못했을 때, 파일을 삭제·정본 누락·0-byte 손상·stale source로 분류하거나 replacement를 만들기 전에 다음 질문을 순서대로 분리한다.

~~~text
1. current exact HEAD에 이 repository path blob이 있는가?
2. current index에서 sparse omission 또는 skip-worktree 상태인가?
3. working tree에 path가 이미 존재하거나 user-modified 상태인가?
4. remote baseline 비교가 이 판단에 실제로 필요한가?
5. 필요한 경우에만 exact HEAD blob을 missing clean path에 복원할 수 있는가?
~~~

이 순서는 복구 명령이 아니라 absence 원인을 구별하는 evidence gate다. sparse omission이면 과거 버전이나 외부 사본을 생성·복사하지 않고 current HEAD를 source로 삼는다.

### 적용 조건

- Git-tracked repository path가 current working tree에서 읽히지 않거나 테스트·도구가 파일 부재를 보고할 때.
- sparse checkout, skip-worktree, linked worktree, partial population이 가능한 checkout일 때.
- HEAD blob과 index 상태를 read-only로 확인할 수 있고, path가 truly missing이며 user edit·unmerged conflict·mode/type change가 없을 때.

### 비사용 조건

- working tree에 파일이 존재하고 user change, staged change, conflict, submodule, symlink, mode/type change가 있거나 그 여부를 모를 때.
- source HEAD에도 blob이 없는 실제 신규 파일 요구 또는 실제 삭제일 때.
- LFS pointer, filter conversion, case-only rename, filesystem permission/lock, antivirus block을 sparse omission으로 단정하려 할 때.
- 넓은 glob 또는 broad restore로 작업 공간을 정리하려는 상황일 때.

### 그대로 복사하면 안 되는 요소

- Urban Legend의 actual path, test command, Base pin, case ID, branch, saved evidence path.
- Windows-specific shell과 index flag 문자만을 hard-code한 규칙.
- 단일 프로젝트 관찰을 모든 sparse checkout이 안전하게 복원 가능하다는 결론으로 바꾸는 주장.

## 기존 Base owner gap과 최소 수정 요청

MINIMUM_OWNER_CORRECTION_REQUEST

- 현재 owner·경로: BCP-2026-022 Local executor content-identity vs stat-only dirty gate는 sparse checkout을 stat-noise 분류에 섞지 말아야 할 반례로 기록한다.
- 확인한 gap: BCP-2026-022는 false-dirty 분류의 안전 경계다. current HEAD에 있지만 sparse working tree에서 생략된 path를 삭제·손상과 구분하거나 exact current source로 안전하게 복원하는 절차는 소유하지 않는다.
- 최소 수정 요청: 별도 Base Skill을 만들지 않는다. 미래 구현에서 existing checkout/working-tree diagnostic owner에 missing tracked path presence guard 한 절과 focused fixture만 추가한다.
- 새 Skill이 필요 없는 이유: Existing Solution First에 따라 BCP-2026-022의 no-destructive boundary와 existing Git/worktree diagnostic contract를 재사용한다. 새 범용 recovery framework는 중복과 오용 위험을 키운다.
- 보호 범위: project-specific paths, game-engine settings, asset policy, active user work, open/draft PR, 기존 false-dirty semantics 밖의 broad recovery.

## 프로젝트 전용으로 남길 내용

- Urban Legend의 exact source and branch details.
- M04, 루메, 괴이 매뉴얼, 회수 시계, Godot runtime 및 사람 검증 내용.
- Base root의 다른 user worktree와 prunable metadata 상태.
- 사용자 제공 이미지와 approved 또는 rejected art candidate 상태.

## 반례와 위험

EVIDENCE_CEILING_AND_NONUSE_CONDITIONS

1. **실제 삭제**: HEAD에 blob이 없으면 sparse checkout 문제가 아니다.
2. **현재 dirty file**: path가 존재하거나 user modification이 있으면 exact restore가 user work를 덮을 수 있다.
3. **Conflict / staged work**: index state가 단일 clean tracked file이 아니면 guard를 적용하지 않는다.
4. **LFS/filter/permission issue**: path가 보이지 않는 원인이 sparse가 아닐 수 있다.
5. **다른 source가 더 최신으로 보이는 상황**: origin/main 또는 external copy를 quiet replacement source로 쓰지 않는다. current task owner가 지정한 exact source를 먼저 판정한다.

위험은 skip-worktree 표시만으로 root cause를 확정하는 것, broad restore로 unreviewed user work를 유실하는 것, remote comparison을 기계적으로 강제하거나 생략하는 것이다.

승인 전 구현 금지 범위:

- existing Base active skill/template/test/validator mutation.
- index flag 변경 또는 restore를 new default automation으로 만드는 일.
- broad worktree clean/reset/checkout, automatic remote replacement, project-specific exception registry.

## 영향 범위와 검증

### Future implementation targets only

- 미래 owner review가 선택한 existing Git/worktree diagnostic guidance.
- actual consumer인 경우에만 existing local executor/bootstrap documentation.
- focused fixtures: HEAD blob absent, sparse-omitted missing path, present dirty path, staged path, conflict/type change, remote comparison-required branch.

### Future validation plan

1. HEAD에 없는 file은 sparse-omitted로 분류하지 않는다.
2. sparse-omitted clean path는 file overwrite 없이 식별한다.
3. present dirty path는 fail closed로 남고 restore를 받지 않는다.
4. staged, conflict, type-change, LFS/filter, partial-clone ambiguity는 unverified로 남긴다.
5. remote baseline은 current decision policy가 요구할 때만 확인한다.
6. BCP-2026-022 false-dirty/stat-noise 동작은 변경하지 않는다.
7. paid tool, external service, global Git config, project-specific hard-coding을 새로 만들지 않는다.

### Rollback

Proposal stage rollback은 이 proposal의 rejection 또는 archival뿐이다. 미래 구현은 additive, bounded, independently approved, regression-tested이어야 하며 project runtime 또는 user content를 변경하지 않고 제거 가능해야 한다.

## 필요한 도구·파일·권한

- 필요 항목: current local environment에 이미 있는 Git CLI.
- 필요한 이유: exact source blob과 index flag 검사는 새 product dependency가 아닌 repository-local evidence다.
- 설치·적용 방법: 설치 없음. 미래 구현은 narrow restore 이전에 read-only inspection만 문서화한다.
- 설치 후 확인 명령: future fixture에서 HEAD blob, index sparse flag, no-overwrite guard, exact-diff readback을 확인한다.
- 최소 권한: 진단은 read access. single missing clean path restore는 existing project recovery authorization이 있어야 하며 broad cleanup에 사용할 수 없다.

## 승인과 구현

~~~yaml
proposal_status: SUBMITTED
proposal_submission_authority: USER_AUTHORIZED_2026_08_31
user_implementation_approval: NOT_GRANTED
approval_ref: "2026-08-31 current user instruction: Base promotion evaluation and proposal submission authorized; active implementation remains unapproved."
implementation_status: NOT_STARTED
implementation_pr: null
implementation_boundary: SEPARATE_FOLLOWUP_PR_AFTER_APPROVED_FOR_IMPLEMENTATION
~~~

현재 권한은 proposal storage, validation, proposal-only commit/push까지다. 이 BCP가 병합되더라도 APPROVED_FOR_IMPLEMENTATION 또는 active Base promotion을 뜻하지 않는다.
