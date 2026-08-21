# Managing Project Intake and Work Contracts — Learning Log

## 2026-08-21 — Continue intent inherits only an already approved contract

- **상태:** `PATTERN_CANDIDATE`
- **호출 트리거:** 사용자가 이미 승인한 장기 교정 작업에서 `진행해`, `계속해`, `남은 작업 진행`이라고 자연스럽게 말했는데도 exact `[연속작업] 진행해` 문구가 없다는 이유로 실행이 끊길 수 있는 퇴행을 감사했다.
- **Finding:** exact magic phrase는 미승인 작업의 오작동을 막지만, 승인 상태와 계속 의도를 하나의 literal로 결합해 정상적인 후속 지시에도 재승인 대기와 조기 답변을 만들었다.
- **Decision:** `CONTINUATION_INTENT_ALIASES`를 `APPROVED_CONTRACT_CONTINUATION`으로 도입한다. 별칭은 유효한 approval reference와 함께 있을 때만 현재 계약의 남은 범위를 계속하며, 새 Goal·범위 확대·사용자 전용 결정·고위험 외부 행위는 승인하지 않는다.
- **TDD evidence:** `tests/test_postmerge_github_notion_long_term_contract.py`의 RED에서 `CONTINUATION_INTENT_ALIASES`와 `APPROVED_CONTRACT_CONTINUATION` 부재를 재현했다. 최종 증거는 전체 discovery와 Skill coverage에서 확정한다.
- **다음 검토 트리거:** 자연어 별칭이 미승인 요청을 자동 실행하거나, 반대로 승인된 동일 계약의 명확한 계속 지시를 다시 마법 문구 부족으로 차단할 때.

## 2026-08-16 — Copy integration replaces open-PR waiting as the Base coordination default

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 open/conflicting PR 때문에 대기시간이 길어지는 문제를 지적하고, 충돌되는 PR이나 파일은 원본을 건드리지 않은 채 복사해 별도 최신-main 작업으로 진행한 뒤 검증·병합하는 방식을 Base 공용 작업 방식으로 바꾸라고 지시했다.
- **Finding:** 기존 `USER_DIRECTED_PARALLEL_PR`은 새 PR 시작은 허용했지만 actual overlap은 per-case replacement approval과 owner-resolution-before-merge에 묶였고 scheduled automation은 any-open-PR guard로 전면 직렬화됐다. 두 규칙을 합치면 owner branch 안전은 높지만 unrelated 작업까지 idle하게 만드는 waiting tax가 생겼다.
- **Decision:** `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16`을 기존 intake/safe-sync owner에 흡수한다. approved same-goal/path/semantic overlap은 exact latest completed main의 separate integration branch에서 필요한 material delta만 selective copy·재구현하고 semantic reconciliation한다. owner PR branches는 read-only다. merge 전에는 `absorbed_owner_deltas`/`residual_owner_deltas`, exact-head checks, P0/P1 0, unresolved thread 0을 요구한다. fully absorbed owner는 post-merge superseded로 정리하고 residual unique work는 보존한다.
- **Scheduled boundary:** 예약·주기 작업도 foreign PR 존재만으로 분석 전체를 막지 않는다. 실제 changed-path/semantic overlap을 검사하고 안전하게 자동 reconcile할 수 없는 conflicted write만 국소 defer한다.
- **Safety boundary:** standing authorization은 새 제품 범위, 파괴적 migration, 결제, 계정·보안 권한 확대, direct main, force push, `--admin`, ruleset bypass를 승인하지 않는다.
- **TDD evidence:** PR #436 initial RED head `d2edf12d016e718808be87762fc9ae47a40b3bad`의 Evidence Knowledge run `31943137165`에서 기존 계약은 유지되고 새 scheduled overlap-aware assertions 두 건만 실패해 이전 all-open-PR 직렬화가 정확히 재현됐다.
- **다음 검토 트리거:** unrelated open PR 때문에 전체 작업이 다시 대기하거나, stale whole-file copy가 newer main을 덮어쓰거나, owner PR branch를 수정하거나, residual unique work를 잃고 superseded 처리하거나, standing authorization이 새 범위·고위험 권한으로 확대되는 사례가 나타날 때.

## 2026-08-15 — Separate user-directed parallel PR work from scheduled active-PR guards

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 같은 목표의 open/draft/ready PR이 이미 있더라도 그 PR을 수정하지 말고, 현재 완료된 `main`에서 새 PR을 만들어 명시적으로 요청한 작업을 계속 진행하도록 Base 공용 규칙에 반영하라고 지시했다.
- **Finding:** 기존 Continuous Work는 blocker recovery와 병합 권한 상속을 소유했고, scheduled/periodic repository-writing automation은 active PR이 있으면 fail-closed하는 별도 안전장치를 갖게 됐다. 첫 구현 뒤 작업 중 PR #425가 병합되며 `synchronizing-local-and-github-state`가 explicitly authorized concurrent overlap을 `PROVISIONAL_INTEGRATION`으로 소유하고 **owner 해결 전 merge 금지**를 정본화했다. 따라서 “새 PR을 만들어 계속 작업한다”는 user-directed 실행 권한과 “겹치는 PR을 병합한다”는 ownership 권한을 분리하지 않으면 intake가 safe-sync보다 느슨한 merge Gate를 만들 수 있었다.
- **Decision:** 새 Skill/Mode를 만들지 않고 `managing-project-intake-and-work-contract`의 Continuous Work owner에 `USER_DIRECTED_PARALLEL_PR`을 흡수한다. 명시적 user-directed continue에서는 same-goal in-progress PR을 read-only overlap evidence로만 읽고 **do not modify/rebase/update** 하며, **current completed main**에서 **separate branch/PR**을 만든다. 이후 actual `SAME_GOAL / PATH_OVERLAP / SEMANTIC_OVERLAP`은 `synchronizing-local-and-github-state`의 concurrent preflight와 `PROVISIONAL_INTEGRATION` 계약에 위임한다. 겹치는 owner PR branch는 read-only이며 owner/main 이동 때 semantic reconciliation + exact-head 재검증을 수행하고, owner가 해결되기 전에는 merge하지 않는다. 다른 PR이 먼저 landing되어 material delta가 사라지면 own PR은 `superseded`로 닫는다. `scheduled/periodic` automation의 active-PR guard는 별도 더 엄격한 계약으로 유지한다.
- **Evidence:** focused test를 처음 standalone로 추가했을 때 기존 Game Project OS suite가 소비하지 않아 거짓 GREEN 위험을 발견했다. 전용 Durable Resume gate에 연결한 RED run `31852863100`에서는 기존 79개 계약이 통과하고 새 `USER_DIRECTED_PARALLEL_PR` 계약만 실패했다. production owner 반영 뒤 run `31853060506`은 Ubuntu/Windows 모두 GREEN이었다. canonical reference freshness는 `SKILL.md` 변경에 대해 승인된 companion test와 Learning Log 동기화를 추가로 요구해 `tests/test_claim_evidence_binding.py` binding test를 연결했다. 이후 #425 병합 후 reconciliation RED run `31853777847`, Ubuntu job `94934536818`은 81개 중 기존 계약은 모두 PASS이고 새 `PROVISIONAL_INTEGRATION` delegation assertion 하나만 FAIL해 상위 owner 정렬 필요성을 정확히 재현했다.
- **Boundary:** 이 정책은 다른 in-progress PR의 branch·commit·review authority를 채택하지 않으며 direct main push, force push, `--admin`, ruleset bypass를 허용하지 않는다. explicit user authorization은 새 isolated PR에서 작업을 계속할 수 있게 하지만 overlap을 `CLEAR`로 낮추지 않는다. actual provisional overlap의 owner-resolution / semantic-reconciliation Gate는 inherited merge authority보다 우선한다. 예약/주기 자동화에는 이 완화 규칙을 적용하지 않는다.
- **다음 검토 트리거:** 같은 목표 PR이 먼저 병합됐는데 중복을 제거하지 못하거나, `superseded`여야 할 PR이 churn을 만들거나, interactive와 scheduled execution 경계가 다시 혼동되거나, `PROVISIONAL_INTEGRATION`인데 owner 해결 전 병합되거나, 다른 PR branch를 암묵적으로 수정·rebase하는 사례가 나타날 때.

## 2026-08-15 — Discover real local capability before rejecting one executable literal

- **상태:** `OBSERVATION`
- **호출 트리거:** Windows Loop A2 Local Executor 설치 중 사용자 PC에서 `gh auth status --hostname github.com`, `codex login status`, `docker version`이 실제로 성공했고 Codex는 `Logged in using ChatGPT`를 반환했지만, 첫 설치기가 `codex.exe`라는 특정 파일명만 찾도록 작성되어 `codex.exe was not found in PATH`로 잘못 차단했다. 뒤이은 설치기는 중간 실패 때 창이 닫혀 blocker의 diagnostic evidence가 사라지는 문제도 노출했다.
- **Finding:** 실제 요구사항은 “ChatGPT-authenticated Codex CLI가 실행 가능한가”인데 packaging literal인 `codex.exe` 존재 여부를 capability보다 높은 gate로 사용했다. Windows command는 PATHEXT와 package-manager shim 때문에 `.exe`, `.cmd`, `.bat` 등으로 노출될 수 있으므로 단일 suffix 강제는 정상 환경을 false negative로 만들 수 있다. 동시에 보안·권위 조건과 환경 discovery heuristic을 같은 수준의 엄격성으로 처리해, 유연해야 할 탐색과 엄격해야 할 acceptance가 분리되지 않았다. 실패 창/로그 보존도 bootstrap 계약으로 명시하지 않아 수정 반복 시 근거가 쉽게 사라졌다.
- **Decision:** local bootstrap은 `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION`을 따른다. 현재 command resolution/PATHEXT, 명시된 trusted executable path, 필요한 경우 known trusted standard install location을 순서대로 탐색하고, 후보를 찾은 뒤 `codex login status` 같은 semantic readiness probe로 실제 capability를 검증한다. **discovery는 넓게, authority와 acceptance는 좁게** 유지한다. 또한 `DIAGNOSTIC_PRESERVATION_ON_BOOTSTRAP_FAILURE`로 실패 terminal을 사용자가 닫기 전까지 유지하거나 durable bounded diagnostic log를 남기고, 가능하면 둘 다 제공한다.
- **Evidence:** 사용자 터미널에서 GitHub auth와 Codex ChatGPT auth가 성공했고 Docker Desktop client/server도 정상 응답했다. 고정 Docker image pull도 exact digest `sha256:dd29372629eeba2dd003fd9e9d35a5b8236c44727875a0364254b5127af88e65`로 완료됐다. 그럼에도 installer v1은 `codex.exe` literal만 검사해 BLOCKED를 냈다. Base 회귀 TDD RED는 PR #416 head `a8ee9bcefb11baf03a5ec30393a6affc05b09267`, workflow `Validate One-Shot Local Executor Bootstrap` run `31833180090`, job `94873467584`에서 기존 3개 bootstrap contract는 PASS이고 새 capability-discovery contract만 `CAPABILITY_DISCOVERY_BEFORE_LITERAL_REJECTION` 부재로 1 failure를 냈다.
- **Boundary:** 유연한 discovery는 arbitrary disk search나 이름만 같은 untrusted binary 선택을 허용하지 않는다. repository/project identity, exact SHA, trusted author/label, ChatGPT authentication, reviewed Docker image, protected path는 계속 strict gate다. ChatGPT auth 실패 시 API key 또는 separately billed OpenAI API로 fallback하지 않으며, reviewed image 부재를 unpinned image로 우회하지 않는다. path 존재만으로 readiness를 PASS로 올리지 않는다.
- **다음 검토 트리거:** 로컬 설치기/launcher가 실제 실행 가능한 도구를 특정 suffix·고정 path 때문에 다시 차단하거나, 사용자가 이미 성공시킨 capability를 재설치하라고 먼저 요구하거나, 실패 창·로그가 사라져 원인 증거를 잃거나, 반대로 multi-route discovery가 untrusted executable 선택으로 과도하게 넓어질 때.

## 2026-08-15 — Separate blind retry from state-aware resume after execution interruption

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 ChatGPT의 `메시지 전송 시간이 초과되었습니다. 다시 시도해 주세요`와 `연결이 끊어졌습니다. 전체 답변을 기다리는 중입니다` 때문에 승인된 연속작업이 중단되는 문제를 자동 감지·복구하도록 요청했다.
- **Finding:** 기존 continuous-work blocker recovery는 blocker를 어떻게 복구할지 소유했지만, **실행 자체가 끊긴 직후 같은 요청을 다시 보내도 되는지**를 별도로 분류하지 않았다. 특히 파일 수정·commit·PR·merge·메일·외부 write처럼 일부 부작용이 이미 일어났을 수 있는 작업에서 마지막 프롬프트를 그대로 재전송하면 중복 실행 위험이 있다. 또한 `연결이 끊어졌습니다. 전체 답변을 기다리는 중입니다`는 서버가 이미 요청을 처리 중일 수 있어 일반 timeout과 동일한 blind retry로 취급하면 안 된다.
- **Decision:** 새 Skill/Mode를 만들지 않고 intake owner에 `TASK_RECOVERY_PROTOCOL` reference를 흡수했다. 안전한 일시 오류는 `RETRY`, 실행 여부가 불명확하거나 부작용 가능성이 있으면 `RESUME`으로 분리한다. 기본 웹 retry는 3초→10초→30초 최대 3회이며, `stalled`와 안전한 retry control이 없는 연결 단절은 자동 프롬프트 재전송을 금지한다. Resume은 authoritative readback·checkpoint·idempotency를 사용해 완료된 단계를 건너뛰고 pending 단계만 계속한다. Git worktree 재연결은 새 구현을 만들지 않고 기존 Loop A2 durable-resume의 exact identity/ownership receipt 계약을 재사용한다.
- **Evidence:** dedicated `Validate Loop A2 Durable Resume`에 `tests/test_task_recovery_protocol.py`를 연결해 독립 테스트 false-GREEN을 제거했다. RED run `31827735602`에서 기존 durable-resume 계약은 통과하고 새 task-recovery 계약만 reference 부재로 실패했다. 이후 Skill package integrity가 새 reference의 owner 연결 누락을 잡았고, canonical reference freshness가 Skill 본문 변경에 대해 companion regression과 Learning Log 동기화를 다시 요구해 이 기록과 `tests/test_neutral_adversarial_feature_lifecycle.py`를 추가했다.
- **Boundary:** Watchdog·트레이·브라우저 확장은 관찰 신호를 제공할 뿐 새로운 repository write·승인·결제·계정·보안 권위를 만들지 않는다. `USER_DECISION_REQUIRED`, `HIGH_RISK_CONFIRMATION_REQUIRED`, 권위 우회, 범위 확대는 자동 승인하지 않는다. 결과가 불명확한 POST/외부 write는 상태를 확인하기 전 재전송하지 않는다.
- **다음 검토 트리거:** 동일 오류가 UI 변경으로 감지되지 않거나, retry/reload가 중복 실행을 만들거나, checkpoint가 완료 상태를 잘못 복원하거나, `RECOVERY_REQUIRED`가 무한 반복되거나, 실제 프로젝트에서 interruption 후 이미 완료된 단계가 다시 실행되는 사례가 발생할 때.

## 2026-08-09 — Recover local and transient blockers before global stop

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 `[연속작업]`이 중간에 멈춘 실제 4사례를 제시했다. (1) 승인된 robustness 목표의 dedicated 10,000-seed package를 새 사용자 승인으로 올림, (2) exact-head Actions 결과의 tool-output truncation에서 전체 작업을 중지함, (3) 현재 ChatGPT 세션에 HiGodot가 없다는 이유로 다른 executor/독립 작업을 탐색하지 않고 중지함, (4) 승인 범위 PR에도 별도 병합 승인이 필요하다고 보고함.
- **Finding:** BCP-2026-010의 첫 구현은 `USER_DECISION_REQUIRED`와 `BLOCKED_UNVERIFIED`를 너무 넓게 전역 종료 조건으로 사용했다. 이 때문에 결과 자체를 바꾸는 진짜 사용자 결정과, 동일 승인 결과를 수행·검증하는 HOW, 일시적인 evidence transport failure, current-session capability absence, 한 task만 막힌 local blocker를 구분하지 못했다. 또한 새 standalone 회귀 테스트를 추가했을 때 일부 명시적 CI 목록이 그 파일을 소비하지 않아 처음에는 거짓 GREEN이 재현됐다.
- **Decision:** `CONTINUOUS_WORK_ACTIVE`에 `recover first → defer locally → continue independent work → stop globally last` 원칙을 추가했다. `RECOVERABLE_VERIFICATION_BLOCKER`, `RECOVERABLE_EXECUTION_ROUTE_BLOCKER`, `LOCAL_TASK_BLOCKER`, `USER_DECISION_REQUIRED`, `HIGH_RISK_CONFIRMATION_REQUIRED`, `GLOBAL_TERMINAL_BLOCKER`를 분리하고 `ready_tasks / deferred_tasks / completed_tasks` Global Progress Queue를 사용한다. `EVIDENCE_TRANSPORT_INCOMPLETE`는 FAIL이 아니며 exact-head workflow/run/job/log를 재조회한다. 현재 세션에 권위 도구가 없으면 전체 실행 경로 부재로 간주하지 않고 callable authorized executor를 탐색하며, `[연속작업] 진행해`는 동일 승인 범위의 `CONTINUOUS_WORK_EXECUTOR_HANDOFF` 요청으로 재사용할 수 있다. 실제 executor가 없으면 거짓 실행 대신 해당 task만 `DEFERRED_EXTERNAL_EXECUTOR`로 두고 handoff/checkpoint를 남긴다. HiGodot 단일 persistent-authoring 권위는 우회하지 않는다. 승인된 동일 범위의 PR은 `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`를 소비해 merge gate 통과 뒤 별도 승인 없이 병합한다.
- **Evidence:** CI가 소비하지 않는 standalone test 문제를 확인한 뒤 `tests/test_deep_interview_contract.py`에 recovery 계약을 연결했다. exact HEAD `6b7144ce471514d133c0a12ff7c942ada57be578`, Actions run `31279523253`, job `93158494112`에서 381개 계약 중 새 `RECOVERABLE_VERIFICATION_BLOCKER` 요구만 1 failure로 재현되고 나머지는 통과해 RED가 정확히 확인됐다. 이후 canonical reference, AGENTS, routing, GPT–Codex handoff policy, intake Skill을 같은 recovery semantics로 정렬했다.
- **Boundary:** 연속작업은 새 제품 목표·범위·예산·권한을 자동 승인하지 않는다. 결제·계정 삭제·보안/권한 확대·사용자 자격 확인과 같은 true high-risk 행위, 프로젝트 결과 자체를 바꾸는 진짜 사용자 결정은 유지한다. 무한 retry를 허용하지 않으며 유한한 evidence/executor recovery path를 소진한 뒤 실행 가능한 독립 task도 없을 때만 `GLOBAL_TERMINAL_BLOCKER`다. 다른 채팅 자동 메시지·scheduler·webhook·브라우저 종료 뒤 백그라운드 실행을 의미하지 않는다.
- **다음 검토 트리거:** recoverable blocker가 무한 반복되거나, executor handoff가 비용/권한을 암묵 확대하거나, 독립 task 판정이 dependency를 무시하거나, 승인 상속이 새 `CHANGE_PROPOSAL`/P0/P1을 덮거나, 실제 프로젝트에서 여전히 `[연속작업]`이 복구 가능한 상황에 중단될 때.

## 2026-08-08 — Explicit bounded continuous-work execution

- **상태:** `OBSERVATION`
- **호출 트리거:** 사용자가 현재 채팅에서 `[연속작업] 진행해`라고 명시하면 `작업 → 적대적 검토 → 권장안 결정 → 자동 승인 처리 → 다음 작업 → … → 최종 보고`를 중간 승인 대기 없이 수행하라는 요청.
- **Finding:** Base에는 이미 승인된 계약, `PLAN / BUILD / REVIEW`, 적대 검토, 기술 finding 반영, 회귀 재검증, 승인 범위의 병합 권한 상속이 있었지만 이를 하나의 명시적 opt-in 연속 실행 상태로 묶는 계약은 없었다. 또한 새 standalone 테스트 파일만 추가하면 일부 명시적 CI 목록에서 소비되지 않아 거짓 GREEN이 될 수 있음을 RED 단계에서 다시 확인했다.
- **Decision:** 새 Skill이나 Work Mode를 만들지 않고 Existing Solution First를 `ABSORB`로 판정했다. intake에 `CONTINUOUS_WORK_ACTIVE / CONTINUOUS_WORK_INACTIVE` 실행 flag와 `references/continuous-work-execution.md`를 추가하고, `[연속작업] 진행해`가 있을 때만 현재 승인된 작업 계약의 남은 범위에서 다음 미완료 작업을 자동 선택한다. 기술적 단일 최소 안전 권장안은 적대 검토 뒤 자동 승인으로 간주할 수 있지만 `USER_DECISION_REQUIRED`, `BLOCKED_UNVERIFIED`, 범위 확대, 고위험 외부 행위, 사용자 중지는 자동 승인하지 않는다.
- **Evidence:** PR #228의 TDD RED에서 GitHub Actions `Validate Game Project Operating System` run `31256943151`, job `93101653170`가 새 reference 부재를 정확히 실패시켰고 나머지 기존 계약 테스트는 통과했다. 구현 뒤에는 기존 CI의 reference-freshness가 변경된 intake Skill에 대해 인정된 회귀 테스트와 Learning Log 동반 변경을 요구해 추가 소비자 누락도 탐지했다.
- **Boundary:** 연속작업은 현재 응답·에이전트 실행 세션 안의 orchestration이다. scheduler, webhook, 브라우저가 닫힌 뒤의 백그라운드 처리, 다른 ChatGPT 채팅 자동 메시지 전송을 의미하지 않는다. 트리거가 없는 일반 요청의 승인·Grill Me 흐름은 바꾸지 않는다.
- **다음 검토 트리거:** 실제 프로젝트에서 연속작업이 승인 범위를 넘어 새 Goal을 생성하거나, 사용자 전용 결정을 자동 확정하거나, 고위험 외부 행위를 우회하거나, 지나친 중간 보고/무한 반복으로 작업 연속성을 해칠 때 이 계약을 재검토한다.
