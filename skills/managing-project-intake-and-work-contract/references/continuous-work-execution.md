# Continuous Work Execution

## 목적

`CONTINUATION_INTENT_ALIASES`는 `[연속작업] 진행해`뿐 아니라 **이미 승인된 동일 작업 계약**에 대한 `진행해`, `계속해`, `남은 작업 진행` 같은 명확한 계속 실행 의도를 인식한다. 유효한 approval reference와 함께 있을 때만 `APPROVED_CONTRACT_CONTINUATION`으로 중간 routine approval 대기 없이 다음 미완료 작업까지 수행한다.

이 계약은 새로운 Skill이나 Work Mode가 아니다. `CONTINUOUS_WORK_ACTIVE` / `CONTINUOUS_WORK_INACTIVE`라는 실행 상태를 기존 intake 계약에 얹으며, `PLAN / BUILD / REVIEW` Work Mode를 대체하지 않는다.

핵심 원칙은 **recover first → defer locally second → continue independent work third → stop globally last**다. blocker 하나를 발견했다는 이유만으로 전체 루프를 즉시 종료하지 않는다.

## 활성화와 범위

```text
사용자 입력에 CONTINUATION_INTENT_ALIASES 존재
→ 현재 승인된 동일 작업 계약과 approval reference 확인
→ APPROVED_CONTRACT_CONTINUATION
→ CONTINUOUS_WORK_ACTIVE

유효한 승인 계약 또는 계속 실행 의도 트리거가 없는 일반 요청
→ CONTINUOUS_WORK_INACTIVE
→ 기존 승인·Grill Me 계약 유지
```

- 동일 메시지에 새 작업 범위가 함께 있으면 먼저 intake의 `route → first-prompt → contract → clarify`로 계약을 닫고, 승인된 범위에서만 활성화한다.
- 이미 진행 중인 작업에서 `[연속작업] 진행해`, `진행해`, `계속해`, `남은 작업 진행`이 입력되면 **현재 승인된 작업 계약**의 남은 범위에 적용한다.
- 별칭은 자연어를 넓게 추측하는 권한이 아니다. approval reference가 없거나 새 Goal·범위가 섞이면 `CONTINUOUS_WORK_INACTIVE`를 유지하고 intake 계약을 먼저 닫는다.
- 이 상태는 채팅 전체에 영구 권한을 부여하지 않는다. 계약 완료, 사용자 중지, 진짜 전역 차단 또는 범위 변경에서 종료한다.
- 다음 작업은 승인된 계약의 완료 기준에서 파생된 미완료 작업만 선택한다. 스스로 새 Goal을 만들거나 범위 확대를 하지 않는다.

## 예기치 않은 실행 중단 복구

메시지 timeout/network 오류, 응답 생성 실패, 실행 프로세스 종료, 장시간 `stalled`처럼 **작업 실행 자체가 끊긴 경우**에는 [`task-recovery-protocol.md`](task-recovery-protocol.md)의 `TASK_RECOVERY_PROTOCOL`을 먼저 적용한다. 이 프로토콜은 새로운 Skill이나 Work Mode가 아니다.

```text
interruption
→ RETRY 또는 RESUME 분류
→ trusted checkpoint + 현재 상태 readback
→ 완료된 단계 보호
→ 미완료 단계만 계속
→ 기존 recovery ladder / Global Progress Queue로 복귀
```

안전한 transient failure만 bounded `RETRY`하고, 파일 수정·commit·PR·merge·외부 전송처럼 일부 부작용이 이미 일어났을 수 있는 작업은 `RESUME`으로 현재 상태를 재확인한다. Git worktree 기반 Loop A2 실행은 별도 durable-resume owner의 exact ownership/HEAD 검증을 재사용하며 임의로 기존 workspace를 adopt하지 않는다.

## Global Progress Queue

연속작업은 현재 task 하나만 보지 않고 다음 세 집합을 유지한다.

```yaml
ready_tasks: []
deferred_tasks: []
completed_tasks: []
```

blocker가 생기면 현재 task의 blocker와 dependency를 기록한 뒤 `recovery ladder`를 실행한다. 바로 해결되지 않으면 그 task만 `deferred_tasks`로 옮기고, 실행 가능한 독립 task가 `ready_tasks`에 있으면 계속 수행한다. 새 증거·도구·선행 결과가 생길 때마다 deferred task를 다시 평가한다.

## `USER_DIRECTED_PARALLEL_PR`

사용자가 같은 승인 범위의 작업을 **명시적으로 계속 진행**하라고 지시했는데 `same-goal`의 `in-progress PR`이 이미 있으면, 그 PR의 존재만으로 interactive 작업 전체를 멈추지 않는다. 기존 PR은 overlap·risk 확인을 위한 read-only evidence로만 취급하고, 명시적으로 그 PR을 맡으라는 지시가 없는 한 **do not modify/rebase/update** 한다.

Base는 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`을 동시작업 조정의 standing authorization으로 사용한다. 단, `STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION`이 적용된다. 현재 작업의 더 구체적인 승인 계약이 다른 open/draft/ready PR 또는 다른 workstream을 `read-only / no absorption`으로 지정하면 그 계약이 standing authorization보다 우선한다. 그 경계를 넘어 material delta를 가져오려면 **explicit absorption authorization**이 별도로 있어야 하며, 기존 전역 표현으로는 `EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION`을 만족해야 한다. 승인이 없으면 다른 PR은 충돌·overlap 탐지에만 읽고 selective copy·재구현·흡수하지 않는다.

```text
explicit user-directed continue
→ same-goal open/recent PR read-only inspection
→ current completed main 확인
→ current completed main에서 새 branch 생성
→ separate branch/PR로 승인 범위 구현
→ synchronizing-local-and-github-state의 concurrent preflight
   ├─ NO_OVERLAP → 일반 separate PR 검증/병합 Gate
   └─ SAME_GOAL / PATH_OVERLAP / SEMANTIC_OVERLAP
      → stronger work contract 확인
      ├─ read-only / no absorption + explicit absorption authorization 없음
      │  → overlap만 기록하고 owner content는 흡수하지 않음
      └─ 흡수 허용 범위
         → PROVISIONAL_INTEGRATION
         → owner PR branches read-only
         → 필요한 material delta만 selective copy / 재구현
         → owner/main 이동마다 semantic reconciliation + exact-head 재검증
         → absorbed_owner_deltas / residual_owner_deltas 기록
→ merge 직전 current main + same-goal PR 상태 재확인
   ├─ 다른 PR이 먼저 병합됨 → main에 실제 landed 된 내용만 새 정본으로 재평가
   ├─ material delta 없음 → own PR을 superseded로 닫고 불필요한 churn 금지
   └─ 허용된 통합 범위가 정리됨 → exact-head Gate 통과 후 own PR 병합 가능
```

- `USER_DIRECTED_PARALLEL_PR`은 다른 `in-progress PR`의 branch·commit·review 상태를 소유하거나 채택하는 권한이 아니다.
- unmerged PR의 구현은 canonical current state가 아니다. 새 작업 기준선은 항상 **current completed main**이다.
- approved same-goal/path/semantic overlap은 ordinary coordination 범위에서 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`을 재사용할 수 있지만, `STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION`과 다른 workstream의 `EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION`을 우회하지 않는다.
- `PROVISIONAL_INTEGRATION`이 실제 허용된 경우에도 **owner PR branches**를 계속 read-only로 유지하고, stale whole-file 복사 대신 필요한 material delta만 **selective copy**·재구현한다.
- owner PR이나 main이 움직이면 semantic reconciliation으로 더 최신·강한 canonical 구현을 보존하고 provisional duplicate를 제거한 뒤 exact-head 검증을 다시 수행한다.
- `absorbed_owner_deltas`는 명시적으로 허용된 통합 PR이 실제로 흡수·검증한 material delta를, `residual_owner_deltas`는 아직 고유하게 남아 owner PR에 보존할 material delta를 기록한다.
- **owner PR이 열려 있다는 사실만으로** own PR merge를 막지 않는다. 다만 다른 workstream content를 흡수하지 않는 계약이면 그 PR의 미병합 material delta를 own PR 완료 조건으로 삼지 않는다.
- 다른 PR이 먼저 병합된 뒤 현재 main과 비교해 material delta가 사라지면 own PR은 `superseded`로 닫는다. 이미 landed 된 내용을 다시 병합하기 위한 churn을 만들지 않는다.
- 명시적 흡수 권한이 없는 다른 workstream PR을 own PR이 `superseded` 처리하거나 close하는 것은 금지한다.
- scheduled/periodic repository-writing automation도 unrelated open PR 존재 자체를 전역 blocker로 사용하지 않는다. 실제 path/semantic overlap을 판정하고, deterministic coordination이 불가능한 conflicted write만 국소 defer한다.
- direct `main` push, force push, `--admin`, ruleset bypass는 이 규칙으로 허용되지 않는다.
- standing authorization은 새 제품 범위, 파괴적 migration, 결제, 계정·보안 권한 확대까지 승인하지 않는다.

## 실행 루프

```text
현재 승인된 작업 계약
→ ready_tasks에서 다음 미완료 작업 선택
→ BUILD에서 작업 수행
→ REVIEW: attack → validate-critique
→ finding/blocker 분류
   ├─ 범위 안의 기술적 단일 최소 안전안
   │  → 권장안 자동 승인 간주
   │  → BUILD에서 최소 반영
   │  → REVIEW: regression-recheck → decision-report
   │  → completed_tasks 기록
   ├─ RECOVERABLE_VERIFICATION_BLOCKER
   │  → exact evidence recovery
   │  → 해결되면 같은 task 계속
   │  → 당장 미해결이면 deferred_tasks
   ├─ RECOVERABLE_EXECUTION_ROUTE_BLOCKER
   │  → authorized alternate executor/tool 탐색
   │  → 해결되면 같은 task 계속
   │  → 당장 미해결이면 DEFERRED_EXTERNAL_EXECUTOR
   ├─ LOCAL_TASK_BLOCKER
   │  → 해당 task만 deferred_tasks
   ├─ USER_DECISION_REQUIRED
   │  → 해당 decision-dependent task 보류
   └─ HIGH_RISK_CONFIRMATION_REQUIRED
      → 해당 high-risk task 보류
→ ready_tasks가 남아 있으면 다음 독립 작업 계속
→ 상태 변화 뒤 deferred_tasks 재평가
→ REMAINING_WORK_RECALCULATION_REQUIRED
   ├─ required work > 0 → ready/deferred queue 재구성 후 계속
   └─ required work = 0 → COMPLETION_CANDIDATE
→ IMPLEMENTATION_CORRECTION_RESCAN
   ├─ valid omission/correction finding
   │  → NEW_FINDING_REOPENS_REMAINING_WORK
   │  → 기존 owner의 최소 BUILD/verify
   │  → REMAINING_WORK_RECALCULATION_REQUIRED로 복귀
   └─ no required finding
      → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
      → same final POST_CHANGE_MONITOR_LOOP
      → minimum-five full-scope loops, then until CLEAN_REVIEW_EXIT
      → FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
→ 최종 실행 보고
```

`POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`는 **두 번째 5회 검토가 아니다.** 마지막 구현·교정 뒤의 completion candidate를 입력으로 하는 기존 `POST_CHANGE_MONITOR_LOOP` 자체이며, 같은 final-state lineage가 최소 5회와 `CLEAN_REVIEW_EXIT`를 충족한다. `NO_MATERIAL_FOLLOWUP`이면 가짜 finding이나 불필요한 변경을 만들지 않는다.

진행 시간이 긴 경우 짧은 진행 업데이트를 제공할 수 있다. 다만 업데이트를 `진행할까요?`, `승인할까요?` 같은 승인 Gate로 바꾸지 않는다.

## Blocker taxonomy와 recovery ladder

### `RECOVERABLE_VERIFICATION_BLOCKER`

검증 자체가 실패한 것이 아니라 결과 확인·전송·상태 확정이 일시적으로 막힌 경우다.

예:

- `tool-output truncation`
- API 응답 잘림 또는 일시 오류
- workflow가 `queued` / `in_progress`
- exact HEAD run을 첫 조회에서 찾지 못함

이때 상태는 `EVIDENCE_TRANSPORT_INCOMPLETE`로 기록한다. `EVIDENCE_TRANSPORT_INCOMPLETE`는 **FAIL이 아니다**.

```text
expected exact HEAD SHA 고정
→ workflow run 재조회
→ exact HEAD run 식별
→ run status/conclusion 재조회
→ job status/conclusion 재조회
→ 필요한 경우 좁은 job/log query
→ 다른 authoritative evidence surface 조회
→ 안전하고 의미가 있을 때 동일 SHA rerun
→ PASS/FAIL/terminal evidence 확보
```

재조회는 무한 반복하지 않는다. 새 증거가 생길 수 있는 유한한 evidence path를 순서대로 소진한다. 한 경로가 막혔다는 이유로 `BLOCKED_UNVERIFIED`를 전역 종료 상태로 승격하지 않는다.

### `RECOVERABLE_EXECUTION_ROUTE_BLOCKER`

필요한 실행 권위는 존재하지만 **현재 세션**에 그 도구가 직접 노출되지 않은 경우다.

예: 프로젝트가 persistent Godot authoring을 HiGodot 단일 권위로 고정했는데 현재 ChatGPT 세션에 HiGodot MCP가 노출되지 않은 경우.

```text
현재 세션 capability 확인
→ 같은 승인·권위에 맞는 연결 도구 확인
→ callable authorized alternate executor 확인
→ 가능하면 CONTINUOUS_WORK_EXECUTOR_HANDOFF
→ 불가능하면 executor-ready handoff/checkpoint 작성
→ blocked task만 DEFERRED_EXTERNAL_EXECUTOR
→ 독립 작업 계속
```

`현재 세션 도구 부재`와 `승인된 전체 실행 경로 부재`를 구분한다. 현재 세션에 HiGodot가 없다는 사실만으로 전체 실행 경로 부재라고 판정하지 않는다.

`alternate executor`는 해당 프로젝트의 권위·보안·파일 쓰기 계약을 그대로 지켜야 한다. HiGodot가 persistent Godot authoring의 유일한 권위라면 GitHub API나 일반 텍스트 편집으로 우회하지 않는다. 실제 executor를 호출할 수 없으면 호출했다고 주장하지 않고 `DEFERRED_EXTERNAL_EXECUTOR`와 준비된 handoff만 기록한다.

### `LOCAL_TASK_BLOCKER`

현재 task만 막혔고 승인 범위 안의 다른 독립 작업은 가능한 상태다. 이 경우 현재 task만 `deferred_tasks`로 이동한다. 다른 `ready_tasks`가 있으면 전체 루프를 즉시 종료하지 않는다.

### `USER_DECISION_REQUIRED`

다음처럼 승인된 **결과 자체**를 바꾸는 선택에만 사용한다.

- 프로젝트 코어·플레이어 경험·주요 UX·콘텐츠 의미를 바꾸는 복수의 유효한 선택지
- 비용·범위 우선순위를 새로 바꾸는 선택
- 기존 approval reference로 복원할 수 없는 새 사용자 의사결정

다음은 `USER_DECISION_REQUIRED가 아니다`.

- 같은 승인 목표를 더 강하게 증명하기 위한 테스트 규모 확대
- `dedicated execution package` 또는 test package 작성
- 실패한 검증의 재조회·재실행
- 동일 동작을 보존하는 기술적 최소 수정
- 승인 범위의 PR 생성·검증·병합
- 현재 세션 도구 부재 때문에 동일 승인 범위를 authorized alternate executor로 넘기는 것

예를 들어 robustness outcome이 이미 승인되어 있고 `10,000-seed` 실제 실행이 그 acceptance criterion을 검증하는 실행 방법이라면, dedicated 10,000-seed robustness execution package 작성 → TDD → 실제 실행은 같은 승인 목표 안의 기술 실행 방법이다. 새로운 제품 결과·예산·권한을 만들지 않는 한 **별도 사용자 승인**을 묻지 않는다.

### `HIGH_RISK_CONFIRMATION_REQUIRED`

결제, 계정 삭제, 보안·권한 확대, 사용자 자격 확인, 승인된 예산을 넘는 외부 비용처럼 실제 사용자 확인이 필요한 행위다. 이 경우 해당 task는 보류하지만 독립 작업이 있으면 계속한다.

### `GLOBAL_TERMINAL_BLOCKER`

다음 조건을 **모두** 만족할 때만 전역 종료 blocker다.

1. 필수 완료 기준이 남아 있다.
2. 허용된 recovery ladder 경로를 모두 소진했다.
3. 실행 가능한 독립 `ready_tasks`가 없다.
4. 자동 승인, 기존 approval reference, `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`, authorized alternate executor로 해결할 수 없다.
5. 사용자 결정·실제 high-risk 확인·외부 실행환경/권한/필수 증거의 변화 중 하나가 생기기 전에는 더 진행할 수 없다.

`BLOCKED_UNVERIFIED`는 개별 task/evidence 상태일 수 있으며 자동으로 `GLOBAL_TERMINAL_BLOCKER`가 되지 않는다.

## 권장안 자동 승인 조건

연속작업에서 권장안을 자동 승인한 것으로 간주하려면 다음을 모두 만족해야 한다.

1. 현재 승인된 작업 계약 범위 안이다.
2. 정본·테스트·명시적 사용자 요구·표준으로 기술적으로 단일 최소 안전안이 결정된다.
3. 적대 검토에서 finding이 유효하다고 확인됐다.
4. 프로젝트 코어, 주요 UX, 콘텐츠 의미, 비용·범위 우선순위를 새로 바꾸지 않는다.
5. 되돌리기 어려운 외부 고위험 행위가 아니다.

`MUST_FIX`와 승인 범위의 기술적 `SHOULD_FIX`는 위 조건을 만족할 때 자동 승인할 수 있다. 단순한 선호나 AI 최초안이라는 이유만으로 자동 승인하지 않는다.

## 승인 상속과 병합

`CONTINUOUS_WORK_ACTIVE`는 기존 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 반드시 소비한다.

승인된 동일 범위의 PR은 **별도 병합 승인**을 묻지 않는다. 검토한 `exact HEAD`, `required checks`, 독립 검토, `unresolved thread 0`, `USER_REVIEW_REQUIRED`·`CHANGE_PROPOSAL`·P0/P1 없음이 확인되면 저장소가 허용한 방식으로 **즉시 병합**한다.

동시작업 overlap이 있고 현재 작업 계약이 흡수를 허용하면 `synchronizing-local-and-github-state`의 `PROVISIONAL_INTEGRATION`과 `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`을 적용한다. 이는 owner branch를 수정할 권한이 아니라 latest-main 통합 Branch에서 selective copy와 semantic reconciliation을 수행할 권한이다. 반대로 `STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION`이 다른 workstream을 no-absorption으로 보호하면 **explicit absorption authorization** 없이는 그 경계를 넘지 않는다. owner PR의 open 상태 자체는 merge blocker가 아니지만, 허용되지 않은 owner delta를 own PR에 복제해 해결해서도 안 된다.

연속작업은 merge safety gate를 제거하지 않는다. 승인 상속과 standing authorization은 재승인·불필요한 waiting을 제거하는 것이지 검증이나 더 구체적인 작업 계약의 보호 경계를 제거하는 것이 아니다.

## 자동 승인 금지와 전역 종료 조건

다음 항목은 자동 승인하지 않는다. 다만 blocker가 국소적이고 독립 작업이 남아 있으면 해당 task만 보류하고 계속한다.

- 진짜 `USER_DECISION_REQUIRED`
- recovery ladder를 소진한 필수 증거의 `BLOCKED_UNVERIFIED`
- 기존 승인 범위를 넓히는 새 목표 또는 범위 확대
- 서로 유효한 복수 선택지가 프로젝트 코어·주요 UX·콘텐츠 의미·비용 우선순위를 다르게 만드는 결정
- `HIGH_RISK_CONFIRMATION_REQUIRED`
- 사용자가 중지 또는 범위 변경을 지시한 경우

전체 루프는 다음에서만 끝난다.

- 현재 승인된 작업 계약의 `REMAINING_WORK_COMPLETION_GATE`가 `CLEAN_REVIEW_EXIT`까지 닫히고 `FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK`를 만족: `COMPLETE`
- 사용자가 중지: `STOPPED_BY_USER`
- 실행 가능한 독립 작업이 없고 진짜 사용자 결정만 남음: `STOPPED_USER_DECISION`
- recovery ladder를 모두 소진했고 실행 가능한 독립 작업이 없는 필수 blocker: `GLOBAL_TERMINAL_BLOCKER`

## Work Mode 관계

`CONTINUOUS_WORK_ACTIVE`는 Work Mode를 대체하지 않는다. 각 작업은 여전히 한 시점에 `PLAN / BUILD / REVIEW` 중 하나를 주 Work Mode로 사용한다.

일반적인 반복은 다음과 같다.

```text
BUILD
→ REVIEW attack → validate-critique
→ 기술적 권장안 자동 승인 가능 여부 판정
→ BUILD 최소 수정
→ REVIEW regression-recheck
→ recovery/dependency 재평가
→ 다음 ready task
```

기획 충돌이나 새 범위가 생기면 `PLAN`으로 돌아간다. 사용자만 결정 가능한 항목이 생겨도 다른 독립 작업을 먼저 소진하고, 그 결정 없이는 더 진행할 수 없을 때만 사용자에게 묻는다.

## 비동기·백그라운드 경계

연속작업은 **현재 응답 또는 현재 에이전트 실행 세션 안에서** 다음 작업으로 계속 진행하는 orchestration 계약이다.

다음을 의미하지 않는다.

- 별도 `scheduler` 실행
- `webhook` 이벤트 수신
- 브라우저가 닫힌 뒤의 백그라운드 작업
- 다른 ChatGPT 채팅으로의 자동 메시지 전달
- 미래 시점에 임의로 작업을 재개하는 기능

executor handoff는 실제로 연결·호출 가능한 실행 환경이 있을 때만 수행한다. 호출 불가능하면 handoff package를 준비하고 해당 task를 defer할 뿐, 백그라운드 실행을 약속하지 않는다.

## `POSTMERGE_REMAINING_WORK_RECALC`

연속작업에서 merge는 종료 신호가 아니다. 현재 승인된 계약이 PR/merge 이후 readback·후속 검증·교훈 정리까지 포함하면 다음을 수행한다.

이 단계는 `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`를 소비한다. 새 main의 exact SHA에서 전체 범위를 다시 공격하고, 유효 finding은 `POSTMERGE_CORRECTION_REQUIRED`로 새 Branch/PR에 교정한다. 적용 가능한 Notion 사람용 정본은 GitHub 증거 뒤에만 갱신하며, 두 목적지를 다시 읽은 `PROGRESS_READBACK_REQUIRED` 없이는 완료율을 확정하지 않는다.

```text
merge
→ merged main SHA / changed canon / generated consumer readback
→ full-scope adversarial review
→ required correction on new latest-main branch/PR when findings exist
→ applicable Notion current-state update after GitHub evidence
→ GitHub + Notion destination readback
→ postmerge regression evidence
→ acceptance criteria를 현재 main 기준으로 다시 대조
→ REMAINING_WORK_RECALCULATION_REQUIRED
→ REQUIRED_WORK_REMAINING 계산
→ REQUIRED_WORK_REMAINING == 0
   ├─ no  → REQUEUE_IN_SCOPE_WHEN_NONZERO
   │        → 승인 범위 안의 미완료 항목만 ready_tasks / deferred_tasks로 재분류
   │        → 실행 가능한 ready task 계속
   └─ yes → COMPLETION_CANDIDATE
            → IMPLEMENTATION_CORRECTION_RESCAN
            ├─ finding → NEW_FINDING_REOPENS_REMAINING_WORK → REQUEUE_IN_SCOPE_WHEN_NONZERO
            └─ clean → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
                       → same final POST_CHANGE_MONITOR_LOOP
                       → minimum-five full loops, then until CLEAN_REVIEW_EXIT
                       → FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
                       → COMPLETE
```

### `REQUEUE_IN_SCOPE_WHEN_NONZERO`

- `REQUIRED_WORK_REMAINING > 0`이면 merge했다는 이유로 완료 보고를 하지 않는다.
- 남은 작업은 **현재 승인된 acceptance criteria에서 파생되는 항목만** 재큐잉한다. 새 Goal이나 optional idea를 required work로 몰래 승격하지 않는다.
- external blocker와 optional backlog는 required work와 분리한다.
- postmerge에서 새 회귀·stale consumer·대체 표시 누락·검증 실패가 발견되면 범위 안의 수정/재검증 task를 다시 queue에 넣는다.
- 전역 종료는 `REMAINING_WORK_COMPLETION_GATE`의 clean exit 또는 앞에서 정의한 진짜 `GLOBAL_TERMINAL_BLOCKER` / 사용자 중지·결정 경계에서만 가능하다.

사용자 행동이 필수인 blocker라면 현재 상태와 막힌 stage를 먼저 특정하고, 사용자가 그대로 따라 할 수 있는 처음부터의 간단한 단계로 안내한다. PowerShell이 필요한 경우 `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`를 사용해 새 창·위치 세팅·한 블록 실행을 기본으로 한다.

## 최종 보고

정상 완료 시 중간 승인 질문을 반복 나열하지 않는다. 최종 보고에는 최소 다음을 포함한다.

```yaml
continuous_work_state: COMPLETE | STOPPED_USER_DECISION | GLOBAL_TERMINAL_BLOCKER | STOPPED_BY_USER
approved_scope:
ready_tasks: []
deferred_tasks: []
completed_tasks: []
required_work_remaining: 0 | N
remaining_work_recalculation_status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
implementation_correction_rescan_status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
completion_adversarial_review_status: NOT_RUN | IN_PROGRESS | PASS | FAIL | BLOCKED_UNVERIFIED
clean_review_exit_status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
external_blockers: []
optional_backlog: []
adversarial_findings: []
auto_approved_recommendations: []
recovery_actions: []
validation_evidence: []
remaining_risks: []
next_state:
```

`CONTINUOUS_WORK_ACTIVE`였다는 사실과 자동 승인해 반영한 권장안, blocker recovery, 적대 검토·회귀 검증 증거를 명확히 남긴다.

## Failure conditions

- `STRONGER_WORK_CONTRACT_OVERRIDES_COPY_INTEGRATION`을 무시하고 더 구체적인 read-only/no-absorption 작업 계약보다 standing authorization을 우선함
- 다른 workstream PR을 `explicit absorption authorization` 없이 selective copy·재구현·흡수·close·supersede 처리함
- 다른 PR을 읽는 것과 그 내용을 own PR에 흡수하는 것을 같은 권한으로 취급함
- `REQUIRED_WORK_REMAINING == 0`을 `COMPLETION_CANDIDATE`가 아니라 즉시 `COMPLETE`로 승격함
- `IMPLEMENTATION_CORRECTION_RESCAN`에서 새 유효 finding이 나왔는데 `NEW_FINDING_REOPENS_REMAINING_WORK`로 재큐잉하지 않음
