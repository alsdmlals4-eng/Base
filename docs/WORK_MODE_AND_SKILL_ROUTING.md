# Work Mode·Skill·Skill Mode 라우팅 계약

## 1. 작업 종류와 실행자를 분리한다

단일 역할 정본: `docs/GPT_CODEX_WORKFLOW_POLICY.md`.
Workspace: `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`.
Machine contract: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`.

| Work Mode | 책임 | 목적 |
|---|---|---|
| `PLAN` | 현재 승인된 작업 owner | 의도·기획·기본 설계·Acceptance |
| `NONCODING_BUILD` | 현재 세션의 허용된 도구 | 문서·데이터·시각 자료·Base 교정 |
| `GODOT_PRODUCT_BUILD` | 현재 세션의 허용된 구현 도구 | 제품 코드·Scene·Resource·runtime 연결 |
| `REVIEW` | 현재 검토 owner 및 필요한 독립 reviewer | 구현·증거·회귀·기획 일치 |

Mode는 앱 전환 명령이 아니다. `UNIFIED_WORK_EXECUTION` / `CAPABILITY_BASED_EXECUTOR_SELECTION`에 따라 Work가 가능한 구현까지 계속한다. 역할 통합은 작성자 자체 검토를 독립 검토로 바꾸지 않는다.

## 2. 기본 라우팅

```text
사용자 요청
→ 프로젝트 current authority / 실제 consumer / 같은 Goal PR
→ 승인 범위와 결과·검증 복원
→ 주 책임 Skill과 필요한 mode 선택
→ 현재 세션의 실제 권한·도구 확인
→ PLAN → NONCODING_BUILD 또는 GODOT_PRODUCT_BUILD → REVIEW
→ 교정·허용 병합·main readback·사용자 실행 가능 인도
```

`CAPABILITY_IS_NOT_AUTHORIZATION`: read/write/test/engine 권한과 검증 능력을 각각 확인한다. Work라는 이름만으로 권한을 만들거나, Codex가 없다는 이유만으로 가능한 제품 구현을 보류하지 않는다.

`HANDOFF_ONLY_FOR_CAPABILITY_GAP_OR_EXPLICIT_REQUEST`: 사용자 지정·실제 능력 부족·정당한 격리 필요가 있을 때만 허용된 인계 경로를 선택한다. runtime 도구가 없으면 가능한 구현과 검사는 계속하되 해당 runtime evidence는 `NOT_RUN`이다. 새 작업/외부 executor 호출은 도구별 허용 조건을 따른다.

## 2A. Owner classification

분야 owner는 제품 의미와 계약을 소유한다. 실행자는 실제 능력으로 선택한다. Base Python contract test·Registry/generated·CI나 GDScript라는 확장자 자체로 앱을 선택하지 않는다.

## 2B. Skill / Skill Mode 자동 선택

- 사용자는 Skill 이름을 고를 필요가 없다. Registry trigger로 주 책임 하나와 실제 필요한 companion만 선택한다.
- `load_by_default=false`는 trigger 기반 선택을 막지 않는다.
- 선택한 Skill과 필요한 reference는 읽되 전체 registry 본문·전 분야 playbook을 매번 로드하지 않는다.
- 같은 승인·요구 분류·계획·검토는 Base와 플러그인 사이에서 중복 실행하지 않는다. 기존 owner와 approval reference를 재사용한다.
- 새로운 증거·실패·범위 변화가 없으면 동등한 조사·설계·승인을 반복하지 않는다.
- 설치 여부, 세션 노출, 실제 호출, 실행 결과, 사용량은 서로 다른 관측이다.

## 2C. CLAIM_AND_INTENT_VERIFICATION_GATE

완료 주장과 요청 의도를 current repository·PR·actual evidence로 대조한다.
Reference: `skills/reviewing-and-validating-project-changes/references/claim-and-intent-verification.md`.
연속 작업: `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`.
과거 보고·PDF·memory를 current truth로 삼지 않는다.
필수 근거가 없으면 `BLOCKED_UNVERIFIED`, 승인 의도와 구현이 다르면 해당 conflict를 유지한다. 테스트 PASS만으로 runtime·Human·출시 주장을 해제하지 않는다.

## 3. 구현·인계·Visual

제품 구현은 GDScript/product code, Scene/Resource/Autoload, runtime data, save/load, UI wiring, shader/VFX, build/export, test/runtime/play를 포함한다. 승인된 capability가 있는 Work가 직접 수행한다.

인계가 필요한 경우만 기존 `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`를 사용한다. exact repository SHA·project.godot·현재 결정·approved_scope·explicit_non_scope·보호 범위·실제 command·Acceptance를 전달하고 받는 실행자가 다시 읽는다.

Visual은 이미지 도구로 후보 제작 → 검수·사용자 승인 → repository binary/SHA-256/consumer/provenance/manifest → runtime 적용 순서를 따른다. 실행자 이름에 따른 이미지 생성 금지는 폐기한다. 도구 부재·미승인 후보는 `GPT_VISUAL_REQUEST` / `WAITING_GPT_VISUAL` 같은 호환 상태로 표현할 수 있으나 그것이 앱 전환 의무는 아니다.

## 4. 판단과 검토

평가 기준 → 유효 대안 → 반증 → 이익/비용/위험 → 되돌리기 난이도 → 미검증 → 권장 결론.
기계적 변경에 허수 대안을 만들지 않는다. 기획 방향이 바뀌면 `USER_DECISION_REQUIRED`.
`경량 중립성 Gate`는 사용자안과 AI안의 동의 편향·반대를 위한 반대를 모두 피한다. L0와 결정·권장안이 없는 설명형 칭찬·균형 요약에는 전체 review를 추가하지 않는다. L1 이상 실질적 선택은 기존 `PLAN 사전판정`과 아래 공유 검토 예산을 적용한다.
승인 범위 안의 기술적 단일 최소 안전 finding이면 자동 승인해 교정한다는 기존 규칙은 재승인을 생략하는 의미다. 새 권한·비용·핵심 의미·범위 변경을 자동 승인한다는 뜻이 아니다.

- L0는 전체 적대 검토 생략 가능. 기존 L1+ 적용 범위는 유지하되 같은 승인 후보 계보에서 정확히 2회만 계수한다.
- `running-adversarial-review-and-refinement`의 `attack → validate-critique → decision-report`로 유효 finding을 구분한다.
- `refine-approved-findings`에서 분야 Skill BUILD로 한 번만 구현·수정하고 `regression-recheck → decision-report`로 돌아온다.
- 같은 Work가 검토 단계로 바뀌어도 두 번째 구현이나 routine 재승인을 하지 않는다.
- CI·독립 승인·exact-head·병합 후 readback은 유지한다. 세션/단계/커밋이 바뀌었다는 이유로 두 회를 다시 시작하지 않는다.

## 5. 연속작업과 실행 안전

`CONTINUOUS_WORK_ACTIVE`는 승인된 작업을 계속하는 flag다. `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`는 정상 repository gate를 통과할 권한이지 bypass가 아니다.
`[연속작업] 진행해`, `진행해`, `계속해`는 유효한 동일 작업 승인 참조와 함께 있을 때만 연속 실행을 활성화한다. 새 Goal·비용·권한·영구 백그라운드 실행 승인이 아니다.
실행 가능한 작업 → 영향 범위 검사 → 교정 → 다음 작업. 국소 blocker는 복구·defer 후 독립 작업 계속; 진짜 새 결정·권한은 사용자에게 올린다.

Godot은 필요한 경우 실제 실행한다. 실행 전 existing/task-owned 구분, 필요한 evidence 후 task-owned 정상 종료, child/lock/session 잔여 확인. 사용자 기존·타 프로젝트 instance는 보존한다. `PROCESS_OWNERSHIP_UNVERIFIED`이면 broad kill하지 않는다.

`WORK_DIRECT_GODOT_VERIFICATION_WHEN_MATERIAL`, `TASK_LAUNCHED_GODOT_PROCESS_OWNERSHIP`, `STOP_TASK_OWNED_GODOT_WHEN_NO_LONGER_NEEDED`, `PRESERVE_PREEXISTING_AND_UNRELATED_GODOT_INSTANCES`, `GODOT_VERIFICATION_AND_SHUTDOWN_REPORT`의 상세 owner는 통합 실행 정책이다.

완료 증거 owner: `docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md` §5.1. 실행 작업에만 아래 항목을 기존 결과 기록에 포함한다. 별도 빈 보고서를 만들지 않는다.

```yaml
godot_verification: <PASS | FAIL | NOT_RUN | BLOCKED_UNVERIFIED; exact build/run evidence>
godot_process_cleanup:
  task_owned_processes_started: []
  task_owned_processes_stopped: []
  preexisting_or_unrelated_preserved: []
  residual_check: <PASS | PARTIAL | NOT_APPLICABLE>
  residual_risk: <없음 또는 확인하지 못한 범위>
```

## 6. 완료와 호환

repository source/HEAD, 변경·유지 범위, 검사 결과, runtime_or_play_evidence, asset 소비, 실행 방법, 미구현·미검증·rollback을 설명한다. 검증·cleanup·Human·출시는 독립 상태다. `READY_FOR_GPT_REVIEW`는 legacy 인계 상태명이며 PASS가 아니다.

`BASE_GOVERNANCE_BUILD_IS_GPT`, `NOTION_BUILD_IS_GPT`, `GODOT_PRODUCT_BUILD_IS_CODEX`, `CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR`, `BASE / NOTION / PLANNING / DOC / VISUAL → GPT`, `ACTUAL GODOT PRODUCT IMPLEMENTATION → Codex`는 RETIRED_ROLE_SPLIT_COMPATIBILITY다. Notion은 V4 exception/migration에만 사용하며 새 정본이 아니다.

별도 프로젝트의 adopted contract는 자동 교체하지 않는다. 사용자 승인 운영 동기화에서 구형 역할/5회 검토/중복 인계 문구의 consumer를 교정하고 프로젝트 validator와 변경 readback으로 실제 채택을 증명한다.
