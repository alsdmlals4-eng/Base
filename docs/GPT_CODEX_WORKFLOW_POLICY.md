# Work 통합 실행·조건부 인계 정책

> Workspace: `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`
> Machine contract: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`
> Approval: 2026-09-16 사용자 승인 — Work에서 기획·코딩·구현을 통합하고 최적화 권장안을 Base에 반영.

## 1. 단일 책임과 실행 능력

`UNIFIED_WORK_EXECUTION` / `CAPABILITY_BASED_EXECUTOR_SELECTION`

현재 Work 세션이 승인 범위에 필요한 저장소 접근·수정·명령·엔진 도구를 실제로 사용할 수 있으면 기획, 상세 설계, 제품 코딩, 데이터·Scene·Resource·자산 연결, 테스트, 검수, PR와 정상 병합까지 같은 작업에서 이어간다. GPT/Work/Codex라는 제품명이나 파일 확장자는 구현 금지 또는 강제 인계 사유가 아니다. Base Python test, CI contract, Registry/generated checker도 같은 원칙을 따른다.

`CAPABILITY_IS_NOT_AUTHORIZATION`: 도구가 있다는 사실은 사용자 승인·보안·프로젝트 보호 경계·외부 행위 권한을 확대하지 않는다. 시스템/개발자 지시와 실제 도구 제약을 repository 정책으로 우회하지 않는다. Work는 실행 작업면이지 정본이 아니며 `REPOSITORY_PRIMARY_CANON`을 유지한다.

| 관측한 능력 | 현재 작업의 처리 |
|---|---|
| 승인 범위 + repository 수정 + 테스트/엔진 실행 가능 | 현재 세션에서 직접 구현·검증·교정 |
| 수정 가능, 일부 runtime/기기 검증 불가 | 독립 구현·가능한 검사 계속; 해당 증거만 `NOT_RUN` / `BLOCKED_UNVERIFIED` |
| 읽기만 가능 | 사실 확인·구체 blocker·재개 정보; 구현·write 완료 주장 금지 |
| 사용자 지정 executor 또는 실제 부족한 실행 능력 | 해당 범위만 조건부 인계; 도구 가용성·권한 확인 후 실행 |
| 새 비용·권한·핵심 의미·승인 범위 변경 필요 | `USER_DECISION_REQUIRED`; 독립된 승인 작업은 계속 |

runtime MCP가 없다고 엔진 실행 전체가 불가능하다고 가정하지 않는다. 허용된 기존 CLI·테스트·정확한 build 증거 경로를 확인한다. 반대로 connector로 파일을 수정할 수 있다는 사실만으로 Godot 실행도 가능하다고 주장하지 않는다.

## 2. 기획부터 사용자 실행 가능 결과까지

```text
current authority + actual implementation + related PR fresh-read
→ 기존 승인·재사용/벤치마크 근거 복원
→ 기획 + 기본 설계 → 검토·보완 → 승인 또는 기존 승인 재사용
→ 필요한 상세 설계
→ 현재 세션의 승인된 실행 능력으로 구현
→ 자동 검사 + 필요한 실제 엔진·화면·플레이 경로 검증
→ FIX | TUNE | REDESIGN 판정 및 범위 안 교정
→ 전체 승인 항목·consumer·미검증 재대조
→ 정확한 HEAD의 필수 CI·독립 검토·정상 병합
→ main readback + 실행 방법 + 필요한 Blueprint 갱신
```

`PLAY_MEANINGFUL_WORK_SLICE`는 플레이어 행동·의미 있는 선택·결과를 검증하는 내부 실행 단위다. 전체 승인 블루프린트를 한 Slice로 임의 축소하지 않는다. `explicit_non_scope` / 제외 범위는 미승인 미래 아이디어를 제외하는 경계이지 승인 항목을 버리는 수단이 아니다.

`GPT_MINIMUM_IMPLEMENTATION_READY_PLANNING`: 필요한 데이터, 상태·입출력, UI/UX flow, 필요한 이미지·사운드, 실제 consumer, 정상·실패·경계 Acceptance가 구현 가능한 만큼 준비되면 상세 설계와 구현으로 이동한다. 이미 승인된 결과를 다시 인터뷰하거나 계획 문서를 계속 늘리지 않는다.

`PLANNING_CANON_BEFORE_HANDOFF`의 안전 의미는 유지한다: 승인된 의미·범위·보호·Acceptance를 기존 repository owner에 기록한다. 같은 세션이면 별도 handoff 문서나 기획 전용 PR을 반드시 만들 필요는 없다. `PRE_HANDOFF_GPT_STOP`은 **기획 과잉을 멈추고 구현으로 넘어가는 과거 호환 이름**이며 Work 종료·Codex 전환 명령이 아니다.

`HANDOFF_IS_NOT_DELIVERY`: 인계 문서·코드 파일·이미지 생성은 사용자 실행 가능 결과와 다르다. 전체 완료 기준은 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`의 `APPROVED_BLUEPRINT_END_TO_END_DELIVERY` / `USER_TESTABLE_DELIVERY`가 소유한다.

## 3. 경량 실행: 한 계약, 한 판단, 필요한 검증

새 변경의 사용자-visible 승인안과 `CONTEXT_FIT_RECHECK`의 단일 owner는 `skills/managing-project-intake-and-work-contract/SKILL.md`다. 의도·구현 개요는 승인 전에 보여주고, 상세 실행·범위 안 교정은 승인 후 연속 수행한다. 같은 계약의 승인을 단계마다 초기화하지 않는다.

`TARGETED_CONTEXT_RECOVERY_NOT_FULL_PROJECT_REAUDIT`

- 시작에는 최신 AGENTS·main·결정/Active Context·실제 대상/consumer·같은 Goal PR을 확인한다. 같은 작업 안에서는 바뀐 owner와 직접 의존성을 다시 읽고, cross-system 충돌·공용 schema·새 권한·사용자 전수감사 요청이 있을 때 범위를 넓힌다.
- `EXISTING_SOLUTION_FIRST`: 프로젝트 구현·승인 자산 → 관련 Base 축적 근거 → 필요한 외부 자료. 같은 승인 범위의 유효한 benchmark는 `REUSED_EVIDENCE`로 재사용한다. benchmark **확인**은 매 작업, 신규 인터넷 **재조사**는 판단에 필요한 근거가 부족하거나 바뀐 경우다.
- Base intake와 플러그인이 같은 요구 정리·승인·계획·검토를 중복 실행하지 않게 현재 owner와 승인 참조를 한 번 연결한다. 스킬 존재만으로 전체 본문·모든 reference를 읽지 않는다. 선택한 지침은 빠짐없이 읽되 관련 없는 지침은 선택하지 않는다.
- 현재 계획·검증 진입점으로 충분하면 새 Skill·프레임워크·대시보드·추적표를 만들지 않는다. 플러그인 설치 수를 실제 호출량·비용과 동일시하지 않는다.
- 필요한 module/Skill 생성은 허용한다. 기존 owner 흡수·조건부 module·독립 Skill을 비교하고, 독립 trigger·입출력·권한·검증 경계와 실제 consumer가 있는 최소안을 택한다. 생성/통합 후 연결·조건부 로드·반례를 확인하며 Skill 수 자체를 목표로 삼지 않는다.
- `IMPACT_BOUNDED_REVALIDATION`: 중간 변경은 영향 범위 테스트, 통합 경계에서는 관련 회귀검사, 병합 전에는 repository 필수 검사. 필수 CI·보안·저장 호환성·runtime Acceptance를 비용 명목으로 생략하지 않는다.
- 같은 승인 후보 계보의 전체 적대 검토는 정확히 2회다. 기획·구현·인계·병합 때마다 초기화하지 않는다. 2회 뒤 결함별 수정·표적 검증만 계속하고 미해결 blocker를 PASS로 바꾸지 않는다. 상세: `docs/operations/FULL_ADVERSARIAL_REVIEW_LOOP_POLICY.md`.
- `CANON_SYNC_AFTER_VALIDATION`: 구현 상태·결정·다음 작업은 같은 작업에서 갱신한다. 전체 PDF는 사용자 검토·의미 있는 마일스톤·최종 인도에 생성한다. 중간 코드 수정마다 재생성하지 않고 기존 PDF의 source SHA와 stale 상태를 정직하게 유지한다.
- 반복 실패에 새 증거가 없으면 맹목 재시도 대신 원인 분류·대안·복구 또는 국소 defer를 적용한다. 사용량 절감률은 실측 전 `NOT_RUN`이며 모델/플러그인 자동 변경·새 과금은 별도 승인 없이는 하지 않는다.

## 4. 조건부 인계

`HANDOFF_ONLY_FOR_CAPABILITY_GAP_OR_EXPLICIT_REQUEST`

실제로 필요한 권한/엔진/환경이 없거나 사용자가 다른 executor를 지정하거나 독립된 작업의 격리가 정당화될 때만 인계한다. 인계가 합리적이라는 판단만으로 새 작업 생성·외부 서비스 실행 권한을 얻지 않는다. 허용된 도구로만 수행한다.

기존 Template `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`와 Skill mode `codex-godot-implementation-handoff`는 경로 호환성을 유지한다. `CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF`는 Codex를 실제로 선택했을 때의 값이지 모든 게임 구현의 선행 Gate가 아니다.

필요한 인계에는 project/repository/worktree, exact source SHA, current owners, work_slice_id, player outcome, approved_scope / explicit_non_scope / protected_scope, required_data_and_inputs, ui_ux_flow, asset_audio_dependencies, acceptance_criteria, review_evidence_expected, actual commands, remaining work를 기존 owner 참조로 전달한다. 받는 실행자는 current main과 drift를 재확인한다. 새 source에 오래된 승인·검증을 자동 승격하지 않는다.
기존 Template의 `exact_source_sha`와 `asset_manifest`는 실제 경로·검증한 revision으로 채우며, 인계하지 않는 작업에 빈 양식을 추가하지 않는다.

`CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA` / `CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED`의 안전 의미는 **모든 실행자**에게 적용된다. exact project/repository/worktree, source SHA, dirty/diverged, project.godot, 채택 engine/authoring authority, actual tool/session을 확인한다. stale PID/session/port를 신뢰하지 않는다.

## 5. 제품 의미·이미지·권리

`CHANGE_PROPOSAL`: 코어·주요 UX·경제/성장 의미·서사·Art Direction·저장 호환성·비용·범위가 달라지면 사용자 결정으로 올린다. 같은 세션의 역할 전환은 새 승인의 이유가 아니다.

`FIX | TUNE | REDESIGN`은 다음 경계를 유지한다.

- `FIX`: 승인 의미는 유지되지만 구현 결함·회귀가 있으면 같은 실행자가 교정한다.
- `TUNE`: **기존 승인 tuning envelope 안에서만** 수치·타이밍·배치·가독성·피드백을 조정한다. 허용 범위를 확인할 수 없거나 경제·성장·난이도 의미/선택 구조를 바꾸면 `REDESIGN` 또는 `USER_DECISION_REQUIRED`이지 임의의 소규모 조정이 아니다.
- `REDESIGN`: 실제 증거가 기획 가설·선택·보상·UX 의미를 부정하면 영향받는 Slice와 의존성의 기본 설계로 돌아간다. 핵심 의미·범위 변경은 사용자 결정이며 프로젝트 전체 재기획을 자동 시작하지 않는다.

이미지 제작은 실행자 이름이 아니라 **실제 이미지 도구·현재 소비처·프로젝트 승인**으로 결정한다. 기존 승인 자산을 우선 재사용하고, 필요한 후보는 이미지 도구로 제작·검수한다. 승인 전 후보를 정식 자산으로 자동 승격하지 않는다. 생성할 도구가 없으면 `GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING` / `GPT_VISUAL_REQUEST` / `WAITING_GPT_VISUAL`은 호환 상태명으로 사용 가능하지만 같은 Work에 이미지 도구가 있으면 강제 담당 전환 없이 후보 제작을 수행한다.

`APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST`: runtime 자산은 project-controlled binary, SHA-256, consumer, provenance, approval/implementation status가 확인되어야 한다. Library·PDF·Notion preview는 runtime binary가 아니다. `CODEX_IMAGE_GENERATION_FORBIDDEN`이라는 일괄 역할 금지는 폐기하고 미승인 이미지 사용 금지와 이미지 도구 사용 요건을 유지한다.
`CODEX_VISUAL_INPUT_REPOSITORY_MANIFEST_ONLY`는 이 runtime 자산 입력 계약의 호환 이름이며, 실제 이미지 도구를 가진 실행자의 후보 생성까지 금지하지 않는다.

기능 원리·일반적 UI 관습·이용 허락된 템플릿은 재사용할 수 있다. 상용 성공작의 아트·문구·레벨·특징적 표현 조합을 그대로 복제한 뒤 reskin하면 안전하다는 가정은 금지한다. 권리 owner는 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`다.

## 6. 실제 검증과 프로세스 안전

실행·fresh artifact·정리·완료 증거의 단일 owner: `docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md` §5.1. 프로세스 조작 안전은 `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`를 따른다.

`DIRECT_RUN_OR_VERIFIED_EVIDENCE` / `WORK_DIRECT_GODOT_VERIFICATION_WHEN_MATERIAL`

필요한 runtime·입력·UI·리소스 연결은 실제 Godot 실행 또는 현재 변경에 유효한 exact-build 증거로 판정한다. 문서 변경에 불필요한 엔진 실행은 하지 않는다. 자동 검사·runtime·화면·기기·Human·출시 증거는 분리하고 `NOT_RUN`, `SKIPPED`, `BLOCKED_UNVERIFIED`를 PASS로 바꾸지 않는다. Human 검증은 사용자 선언·요청 시 수행하며 machine PASS로 대신하지 않는다.

`TASK_LAUNCHED_GODOT_PROCESS_OWNERSHIP`: 실행 전 project path, 실행 대상, 기존 Editor/game/server, launch time과 parent-child/PID/session 식별자를 확인한다.

- stale PID/session을 current truth로 쓰지 않음: 실행 직전 실제 대상·project path를 다시 확인한다.
- 다른 프로젝트 editor/server/process를 임의 조작하지 않음: 승인 범위와 task ownership을 함께 확인한다.
- 실제 Godot/runtime을 실행하지 않았으면 runtime PASS 아님: 파일 수정·정적 검사와 별도 판정한다.

`STOP_TASK_OWNED_GODOT_WHEN_NO_LONGER_NEEDED`: 필요한 evidence/readback 확보 → 이번 작업이 시작한 불필요한 game/debug/Editor/server 정상 종료 → child-process·project-lock·session 잔여 확인. 같은 검증 묶음 안에서 매 assertion마다 재시작하지 않는다.

`PRESERVE_PREEXISTING_AND_UNRELATED_GODOT_INSTANCES`: 사용자 기존 instance·다른 프로젝트/worktree·소유권 불명 프로세스는 보존한다. broad kill 금지. 안전하게 구분할 수 없으면 `PROCESS_OWNERSHIP_UNVERIFIED`로 남긴다.

`GODOT_VERIFICATION_AND_SHUTDOWN_REPORT`: 실행 PASS와 cleanup PASS는 별도다. 실행하지 않았으면 verification `NOT_RUN`, cleanup `NOT_APPLICABLE`; 종료·잔여 확인을 못 했으면 cleanup `PARTIAL`이다.

## 7. Git와 완료 보고

- `CURRENT_TASK_CONTINUATION_AUTHORIZES_READY_MERGE` / `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 동일 승인 current-task PR은 required checks·독립 검토·unresolved thread 0·ruleset 통과 후 정상 병합할 수 있다. `AUTO_MERGE_AFTER_REQUIRED_CHECKS` / `AGENT_MERGE_REQUIRED`는 우회 권한이 아니다.
- 다른 open/draft/ready PR은 read-only. force push/history rewrite/destructive reset, direct main push, admin/ruleset bypass 금지.
- merge 뒤 exact main과 변경 owner·consumer readback. 실제 필요한 publication만 source SHA에 연결한다. 새 Notion write/readback은 기본 요구가 아니다.
- 결과에는 changed files/reasons, tests_passed/failed/not_run, runtime_or_play_evidence, approved_repository_visuals_consumed, current revision, remaining scope/blocker, rollback, 실행 방법을 적는다. `READY_FOR_GPT_REVIEW`는 옛 인계 상태이며 독립 검토나 runtime PASS를 뜻하지 않는다.
- 사용자 학습 설명은 무엇이 바뀌었는가 / 어떤 연결로 작동하는가 / 어떻게 확인하는가. 상세 정책 토큰·전체 스킬 목록을 매번 재출력하지 않는다.

## 8. 프로젝트 채택과 폐기된 역할명

Base 병합은 모든 프로젝트에 자동 적용된 증거가 아니다. 프로젝트 최신 AGENTS·adopted contract·결정·실제 consumer를 먼저 읽고 명시적으로 승인된 운영 규칙 범위만 adapter와 관련 owner에 동기화·검증한다. engine/version·제품 의미·자산 승인·보안·저장 계약은 교체하지 않는다. 적용된 프로젝트와 미적용 프로젝트를 구분한다.

`GPT_NONCODING_PROJECT_OWNER`, `GPT_BASE_NOTION_GOVERNANCE_OWNER`, `GPT_BASE_REPOSITORY_GOVERNANCE_OWNER`, `CODEX_GAME_PRODUCT_IMPLEMENTATION_OWNER`, `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER`, `CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR`, `PRODUCT_IMPLEMENTATION_HANDOFF_ONLY`, `GODOT_PRODUCT_BUILD_IS_CODEX`, `WORK_LONG_MULTISTEP_NONCODING_DEFAULT`는 **RETIRED_ROLE_SPLIT_COMPATIBILITY**다. 과거 이름·파일 경로를 보존하는 것이 현재 역할 제한을 부활시키지 않는다.

`CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION_RETIRED`, `CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY_RETIRED`, `NOTION_HUMAN_FACING_CANON_RETIRED`: V3 historical contract는 유지하지만 현재 기본 경로는 V4 repository-only다. `NO_NEW_NOTION_WRITE_BY_DEFAULT`.

`GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED`는 유지한다. Work 통합을 이유로 폐기한 local one-shot launcher를 되살리지 않는다. `CODEX_PREFLIGHT_OPTIONAL`, `PLAN_REVIEW_ONLY`, `CONTINUOUS_WORK_EXECUTOR_HANDOFF`, `DEFERRED_EXTERNAL_EXECUTOR`는 실제 필요와 사용자 범위에 따른 조건부 상태이며 강제 앱 전환이 아니다.
