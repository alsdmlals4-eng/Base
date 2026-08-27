# BCP-2026-046 · Work Godot 기계검증과 작업 소유 프로세스 종료 계약

## 출처와 상태

- 출처: GPT Work 작업 중 Godot 직접 기계검증과 검증 종료 후 프로세스 정리를 요구한 사용자 운영 지시
- 기준 Base: `1117572df293b668271d473e7fcdca3794cd5aed`
- 제출일: `2026-08-27`
- 상태: `IMPLEMENTED`
- 상태 설명: Proposal PR #761과 구현 PR #762가 병합됐고, 누락됐던 최초 Registry `SUBMITTED` 기준점도 PR #766으로 복구했다. active owner 문서·focused regression·Registry가 구현 완료 상태로 일치한다.
- 지식 상태: `사용자 승인 운영 요구 + RED 재현 + exact-head GREEN + Registry lifecycle 완료`
- 승인 근거:
  - 사용자 메시지: `work 작업 중에 필요시 godot 켜서 기계검증하고 사용 종료시 해당 godot을 꺼달라고해줘`
  - 후속 사용자 메시지: `좋아 base에도 교정해줘`

## 관찰과 증거

기존 Base는 다음을 이미 요구했다.

- GPT가 현재 도구로 runtime/play를 직접 실행·관찰할 수 있으면 직접 증거를 확보한다.
- 실제 Godot/runtime을 실행하지 않았으면 runtime PASS가 아니다.
- stale PID/session/port를 current truth로 사용하지 않는다.
- 다른 프로젝트의 Editor·server·process를 임의 조작하지 않는다.
- 필요하지 않을 때 HiGodot addon과 MCP server를 종료하거나 비활성화한다.

그러나 GPT Work가 검수를 위해 Godot Editor, 게임 창, headless/debug runner 또는 관련 QA process를 직접 시작한 경우 다음이 명시되어 있지 않았다.

1. 어떤 process/session이 이번 작업이 시작한 것인지 식별·기록하는 규칙
2. 기계검증 종료 후 해당 작업 소유 process와 파생 child process를 종료하는 시점
3. 사용자가 원래 열어 둔 Godot 또는 다른 프로젝트 instance를 보호하는 판정
4. 소유권을 구분할 수 없을 때 강제 종료하지 않고 잔여 위험을 보고하는 실패 경계
5. 완료 보고에서 `Godot 실행 검증`과 `Godot 종료 확인`을 분리하는 증거 형식

이 누락은 불필요한 CPU·메모리 점유, project lock, stale debug session, 잘못된 대상 종료 또는 다음 작업의 wrong-target 오판을 만들 수 있다.

## 일반화 후보

### 1. `WORK_DIRECT_GODOT_VERIFICATION_WHEN_MATERIAL`

GPT Work는 승인된 구현을 변경하기 위한 저작 단계가 아니라 **검수·기계검증**에 Godot 실행이 materially 필요하고 현재 도구로 실행 가능할 때 기존 프로젝트를 직접 실행한다.

대표 대상:

- scene/project load와 parse/import
- runtime input·상태 전이·UI 상태·resource 연결
- 오류 로그·crash·startup smoke
- GUT/headless/runtime test
- Hera 등 채택된 read-only/live-QA 경로

문서·정적 diff·data schema 검사만으로 acceptance를 충족할 수 있으면 Godot을 불필요하게 실행하지 않는다. 이 규칙은 GPT가 실제 Godot 제품 코드를 직접 누적 구현하도록 권한을 넓히지 않는다.

### 2. `TASK_LAUNCHED_GODOT_PROCESS_OWNERSHIP`

실행 전 exact project/repository/worktree identity와 기존 process/session 상태를 확인하고, 이번 Work가 시작한 다음 항목을 작업 소유 대상으로 기록한다.

- Godot Editor instance
- 실행한 game window 또는 headless/runtime process
- debug/test runner와 이번 실행에서 파생된 child process
- 이번 검증을 위해 직접 시작한 addon/MCP/live-QA server

PID 하나만 영구 신뢰하지 않고 project path, launch time, parent-child relation, session/port 등 현재 환경에서 확인 가능한 식별자를 함께 사용한다.

### 3. `STOP_TASK_OWNED_GODOT_WHEN_NO_LONGER_NEEDED`

필요한 evidence를 확보했고 같은 작업에서 추가 Godot 검증이 남지 않았으면 완료 보고 전에 이번 Work가 시작한 Godot·게임·debug/test·관련 server process를 정상 종료한다.

```text
verification complete
→ evidence/readback capture
→ graceful game/debug stop
→ task-launched Editor/server stop when no longer needed
→ child-process and project-lock residual check
→ completion report
```

검증 중 재실행이 예정된 경우 매 assertion 뒤 Editor를 반복 재시작하도록 강제하지 않는다. 작업 종료 또는 해당 도구가 더 이상 필요하지 않은 시점에 한 번 정확히 정리한다.

### 4. `PRESERVE_PREEXISTING_AND_UNRELATED_GODOT_INSTANCES`

다음 대상은 종료하지 않는다.

- 사용자가 Work 시작 전에 별도로 열어 둔 Godot instance
- 다른 프로젝트·repository·worktree의 Editor/game/server
- 다른 승인 workstream 또는 사용자가 직접 소유한 debug session
- 이번 작업이 시작했다는 증거가 없는 process

소유권을 안전하게 구분할 수 없으면 broad kill, process-name 전체 종료, port-wide destructive cleanup을 하지 않는다. `PROCESS_OWNERSHIP_UNVERIFIED`로 남기고 잔여 process와 수동 확인 필요성을 보고한다.

### 5. `GODOT_VERIFICATION_AND_SHUTDOWN_REPORT`

Work 완료 보고는 필요 시 다음을 분리한다.

```yaml
godot_verification:
  status: PASS | FAIL | PARTIAL | NOT_RUN
  project_identity:
  scenes_or_behaviors_checked: []
  evidence: []
  unverified: []

godot_process_cleanup:
  status: PASS | PARTIAL | NOT_RUN | NOT_APPLICABLE
  task_owned_processes_started: []
  task_owned_processes_stopped: []
  preexisting_or_unrelated_preserved: []
  residual_check: PASS | PARTIAL | NOT_RUN | NOT_APPLICABLE
  residual_risk: []
```

Godot을 실행하지 않은 작업은 verification `NOT_RUN`, cleanup `NOT_APPLICABLE`로 기록할 수 있다. 실행했지만 종료 확인이 없으면 완료 자체를 과장하지 않고 cleanup evidence를 `PARTIAL` 또는 `NOT_RUN`으로 남긴다.

## 적용 조건과 비사용 조건

적용:

- GPT Work가 프로젝트 runtime·scene·input·UI·로그·import·test를 직접 검증할 때
- Work가 Godot Editor, game, headless runner, debug/test process 또는 관련 local server를 직접 시작할 때
- 검증 완료 후 불필요한 자원 점유와 stale session을 남길 가능성이 있을 때

비사용 또는 축소:

- Godot을 실행하지 않는 Base/Notion/문서/정적 분석 작업
- 사용자가 명시적으로 Editor를 계속 열어 두라고 요청한 경우
- 외부 executor가 이미 정확한 build/commit의 검증 증거를 제공하고 Work가 직접 실행하지 않은 경우
- 현재 도구로 process ownership을 식별하거나 종료할 수 없는 환경. 이 경우 강제 종료 대신 `BLOCKED_UNVERIFIED` 또는 cleanup `PARTIAL`을 보고한다.

프로젝트 전용으로 남기는 항목:

- 각 프로젝트의 Godot executable path와 version
- exact repository/worktree/project path
- project별 addon, GUT, Hera, HiGodot 채택 상태
- OS별 process name, PID, port, session ID와 종료 명령
- 사용자가 열어 둔 instance 여부와 프로젝트별 예외
- 실제 scene/test/runtime acceptance와 evidence path

## 반례와 위험

- process name만 보고 `godot*` 전체를 종료하면 사용자 작업을 잃을 수 있다. task-owned 식별이 우선이다.
- 매 test마다 Editor를 닫으면 import cache와 반복 검증 비용이 증가한다. 같은 bounded verification group 안에서는 재사용하고 마지막에 정리한다.
- 강제 kill을 기본값으로 사용하면 저장 중 Scene·Resource나 로그 flush가 손상될 수 있다. graceful stop을 우선하고 강제 종료는 hung task-owned process에 한정해 이유와 결과를 남긴다.
- cleanup PASS가 runtime PASS를 대체하지 않는다. 실행 검증과 프로세스 정리는 별도 claim surface다.
- GPT Work 검증 권한이 persistent product authoring 권한으로 확대되어서는 안 된다.
- 구현이 이미 병합됐다는 이유로 Registry 최초 등록의 `SUBMITTED` Gate를 우회하면 Proposal lifecycle contract가 깨진다. PR #766으로 최초 기준점을 복구한 뒤 별도 상태 전이로 닫았다.

## 영향 범위와 검증

### 구현된 영향 범위

1. `docs/GPT_CODEX_WORKFLOW_POLICY.md`에 Work 직접 Godot 검증과 작업 소유 process lifecycle 추가
2. `docs/WORK_MODE_AND_SKILL_ROUTING.md`에 실행·종료·보고 routing 노출
3. `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`에 task-owned cleanup과 pre-existing instance 보호 경계 추가
4. `docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md`의 기존 완료 증거 owner 재사용
5. `tests/test_work_godot_process_lifecycle_contract.py`에 focused RED→GREEN regression contract 추가

### 제외·보호 범위

- 실제 게임 프로젝트의 GDScript·Scene·Resource·runtime code 수정 없음
- GPT의 persistent Godot product authoring 권한 확대 없음
- Codex 역할·이미지 승인·사용자 결정 Gate 변경 없음
- broad process kill, 다른 프로젝트 instance 종료, stale PID 신뢰 금지
- 새 provider, addon, dependency, paid service, remote tunnel 추가 없음
- 열린 다른 PR·branch는 read-only

### 검증

1. Work 직접 실행은 materially 필요한 검수에만 허용되고 product implementation과 구분되는지 검사했다.
2. exact project identity와 task-launched process ownership 기록을 요구하는지 검사했다.
3. evidence 확보 뒤 task-owned Editor/game/debug/test/server 종료와 residual check를 요구하는지 검사했다.
4. pre-existing/unrelated instance 보호와 ownership-unverified fail-safe가 유지되는지 검사했다.
5. 완료 보고가 runtime verification과 cleanup evidence를 분리하는지 검사했다.
6. 기존 `DIRECT_RUN_OR_VERIFIED_EVIDENCE`, stale PID/session 불신, 다른 프로젝트 process 비조작, HiGodot/GUT/Hera authority 경계를 회귀검사했다.
7. 구현 PR exact HEAD에서 focused regression, whole core regression, Ubuntu contract, docs validation, publication validation, Base v9 contract, integrated Vertical Slice, required `ci-gate`를 통과했다.
8. Registry 등록 PR #766 exact HEAD에서 proposal validator, docs, Ubuntu contract, whole core regression, publication validation, required `ci-gate`를 통과했다.

## 승인과 구현

- 사용자 승인: 2026-08-27 현재 대화의 Godot 실행 검증·작업 소유 프로세스 종료 지시와 Base 교정 승인
- 제안 PR: [#761](https://github.com/alsdmlals4-eng/Base/pull/761), squash merge `c0e5d08f4f1068f736a510beb209995df0c4d06d`
- 구현 PR: [#762](https://github.com/alsdmlals4-eng/Base/pull/762), exact reviewed head `7afb0fea3c8268074d4ddcae40faf5e33ad55cf1`, squash merge `dd50abbbc64077ad6860b9c2ee7ed63719b3b471`
- Registry 등록 PR: [#766](https://github.com/alsdmlals4-eng/Base/pull/766), exact reviewed head `f12f0753f4e24429a9a29b61d0eab8450eb10be6`, squash merge `ecbeba7fa70348e5fb01317dce3f01299f8477dd`
- 구현 검증: focused RED 재현 후 GREEN, whole core regression, Ubuntu contract, docs validation, publication validation, Base v9 contract, integrated Vertical Slice, required `ci-gate`, 5회 whole-state 적대적 검토, post-merge main readback PASS
- lifecycle 결과: Proposal과 Registry가 `IMPLEMENTED`로 일치하며 active owner 문서와 focused regression이 `main`에 존재한다.
- 상태 한계: 이번 Base 문서·계약 작업에서는 게임 프로젝트 Godot runtime을 실행하지 않았으므로 `godot_verification: NOT_RUN`, `godot_process_cleanup: NOT_APPLICABLE`

## 롤백

구현 자체를 되돌릴 때는 구현 PR #762에서 추가한 Work Godot process lifecycle 문구, routing/report fields, Godot 안전 경계, evidence-owner 연결과 focused regression test를 한 단위로 revert한다. Registry lifecycle만 되돌릴 때는 등록 PR #766과 구현 상태 closeout 변경을 순서에 맞게 revert한다.
