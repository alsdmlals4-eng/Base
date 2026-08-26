# BCP-2026-038 — Work·Codex 최소 전환 버티컬 슬라이스 자동화

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base` 및 사용자의 다중 프로젝트 Work 운영 사례
- 기준 커밋: `43b3ffb2c5b026e3d4a38dab2338585894d36f61`
- 제출일: `2026-08-27`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `PATTERN`
- approval reference: `2026-08-27 current ChatGPT Work conversation — 사용자가 권장안 B와 추가 연속 실행·승인 위임·Hera/GUT 우선 QA·Work↔Codex 전환 최소화를 명시 승인`

## 1. 관찰과 증거

현재 Base `main`은 이미 다음 공용 능력을 가진다.

- Project GitHub·Notion·Base fresh-read
- Reuse-First, 시장·현업·성공/실패 사례 조사, 최소 3개 대안 비교
- Work의 기획·Notion·Visual 책임과 Codex의 실제 게임 제품 구현 책임 분리
- Playable Slice, Implementation Reality Gate, GUT/Hera 역할 경계
- recover first → local defer → independent continuation → global stop last
- current-task PR의 exact-head 검증·안전 병합·post-merge readback
- required work 재계산과 completion-candidate 적대적 재검토

그러나 실제 프로젝트 운영에서는 다음 형태의 중단이 반복된다.

1. Work가 기획·검수·이미지 준비를 각각의 작은 승인 checkpoint에서 멈춘다.
2. 실제 게임에 필요한 이미지·사운드·UI·데이터가 모두 준비되기 전에 Codex로 넘어가 Work↔Codex 전환이 반복된다.
3. Codex가 구현 중 발견한 누락을 한 건씩 Work에 반환해 context switch와 재수화 비용이 누적된다.
4. connector·CI·도구 경로가 지연되면 이미 존재하는 우회·대체 경로보다 동일 경로 재시도 또는 전역 중단이 먼저 발생한다.
5. 자동 test·runtime evidence와 인간 QA의 경계가 불명확하면 인간 QA를 실행하지 못한 상태에서 전체 작업이 멈추거나, 반대로 machine evidence를 human PASS로 과장할 위험이 있다.
6. 계획된 목록이 소진된 뒤 실제 상태에서 새 누락을 찾지 않고 종료하거나, 반대로 `남은 작업 0`을 프로젝트 전체 무한 확장으로 해석할 위험이 있다.

사용자가 원하는 기본 운영은 다음 세 단계다.

```text
1. Work
   기획 마무리
   → 검수 마무리
   → 실제 인게임에 필요한 이미지·사운드·UI·데이터·Flow·Acceptance 준비

2. Codex
   하나의 통합 구현 packet을 fresh-read
   → 실제 제품 구현
   → GUT·Hera·runtime/build 자동 QA

3. User validation
   자동 검증된 완성 버티컬 슬라이스를 사용자가 직접 플레이
   → 사용자 검증 뒤 다음 Slice 또는 교정 작업
```

## 2. 제안 목표

새 광역 Skill·새 executor·새 유료 서비스·두 번째 project canon을 만들지 않고, 기존 Work v4.9 bundle·continuous work·GPT–Codex handoff·Visual approval·Vertical Slice·HiGodot/GUT/Hera owner를 조합해 다음 계약을 추가한다.

```text
WORK_PREP_COMPLETION_BEFORE_CODEX
WORK_PRODUCTION_INPUT_BATCH
MINIMIZE_WORK_CODEX_TRANSITIONS
CODEX_SINGLE_IMPLEMENTATION_WINDOW
CONSOLIDATED_RETURN_PACKET

STALL_SIGNAL_ROUTE_SWITCH
BOUNDED_RETRY_THEN_FALLBACK
EVIDENCE_EQUIVALENT_FALLBACK_ONLY

DELEGATED_RECOMMENDED_DEFAULT_APPROVAL
HIGH_RISK_DECISIONS_DEFER_AND_BUNDLE
NO_ROUTINE_APPROVAL_STOPS

SCOPE_BOUNDED_REQUIRED_WORK_ZERO
AUTOMATION_PHASE_REMAINING_WORK_ZERO

MACHINE_QA_FIRST
HUMAN_QA_DEFERRED_BY_CURRENT_USER
GUT_DETERMINISTIC_TESTS_WHEN_ADOPTED
HERA_LIVE_QA_AND_SCREEN_EVIDENCE_WHEN_ADOPTED
HUMAN_USABILITY_EVIDENCE_NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE_NOT_RUN
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
```

## 3. 방법 비교

### 대안 A — 현행 checkpoint를 그대로 유지

- 장점: 각 결정의 사용자 통제가 가장 강하다.
- 단점: 이미지·사운드·기획·구현 사이의 정지와 재수화가 많고, 사용자가 이미 위임한 routine 판단도 반복 질문한다.
- 판정: 안전 fallback으로 보존하되 현재 사용자의 기본 자동화 경로로는 기각한다.

### 대안 B — 모든 Work·Codex·이미지·병합을 무조건 자동 승인

- 장점: 중단 횟수가 가장 적다.
- 단점: 파괴적 삭제, 계정·보안 권한, 유료 비용, 권리·법적 위험, 프로젝트 core identity 교체까지 자동화할 수 있다. host/system confirmation도 우회한다고 오해될 수 있다.
- 판정: 기각한다.

### 대안 C — 승인된 Slice 안의 권장 기본값을 위임하고 고위험 항목만 국소 보류

- 장점: routine 중단을 제거하면서도 되돌릴 수 없는 위험은 차단한다. Work 준비를 한 번에 닫고 Codex 구현을 한 번에 수행할 수 있다.
- 단점: Slice scope, production-input readiness, high-risk taxonomy, evidence ceiling을 명시해야 한다.
- 판정: **채택**한다.

## 4. Work Production Input Completion Gate

Codex 전환 전 Work는 현재 Slice가 실제 구현에 필요한 비제품 입력을 가능한 한 한 번에 닫는다.

```yaml
WORK_PRODUCTION_INPUT_PACKET:
  slice_identity:
  player_outcome:
  meaningful_choice:
  approved_scope: []
  explicit_non_scope: []
  protected_scope: []
  planning_and_rules:
  ui_ux_flow:
  data_and_state_contract:
  visual_requirements: []
  approved_visual_assets: []
  audio_requirements: []
  approved_audio_assets_or_procedural_specs: []
  vfx_feedback_requirements: []
  localization_and_accessibility_requirements: []
  provenance_and_rights_records: []
  acceptance_criteria: []
  deterministic_tests: []
  runtime_qa_scenarios: []
  build_or_export_checks: []
  rollback:
  unresolved_nonblocking: []
  blocking_missing_inputs: []
  readiness: READY_FOR_SINGLE_CODEX_WINDOW | BLOCKED_UNVERIFIED
```

규칙:

- 설명용 문서량이 아니라 actual game consumer가 있는 입력만 production packet에 넣는다.
- 이미지·사운드·UI·VFX는 실제 Scene/Screen/slot/cue consumer와 연결한다.
- Work에서 실제 binary 제작 capability가 없으면 생성됐다고 추측하지 않는다. 기존 승인 자산, 무료·허용된 source, 승인된 procedural specification, 별도 도구의 durable 결과 중 evidence가 있는 경로를 사용한다.
- 핵심 feedback에 필요한 asset이 없으면 shipping-intent readiness를 과장하지 않는다.
- 한 요소가 준비되지 않았더라도 독립적으로 닫을 수 있는 Work 준비는 계속하고 마지막에 blocking input을 한 묶음으로 판정한다.

## 5. Work↔Codex 최소 전환 계약

정상 경로는 계획된 전환 두 번 이내의 한 round trip이다.

```text
Work preparation
→ Codex single implementation window
→ Work final evidence review / canon / merge
→ user vertical-slice validation
```

`CODEX_SINGLE_IMPLEMENTATION_WINDOW`:

- Codex는 전달된 packet과 Project GitHub·Notion을 fresh-read해 승인된 Slice 구현을 연속 수행한다.
- 기술적 세부사항·승인 범위의 bug fix·reversible refactor는 권장 기본값으로 계속한다.
- 구현 중 비차단 누락·의문은 즉시 Work로 한 건씩 반환하지 않고 `CONSOLIDATED_RETURN_PACKET`에 모은다.
- 현재 packet으로 구현 가능한 독립 작업과 GUT·Hera·build QA를 계속한다.
- 한 번의 missing input 때문에 전체 구현을 즉시 중단하지 않는다.

```yaml
CONSOLIDATED_RETURN_PACKET:
  project:
  slice_id:
  exact_head:
  completed_implementation: []
  machine_qa_completed: []
  missing_input_batch: []
  change_proposal_batch: []
  high_risk_deferred_batch: []
  independent_work_remaining: []
  evidence:
  requested_work_reentry:
```

Work 재진입은 다음 중 하나일 때만 수행한다.

- missing input batch가 실제 acceptance를 차단하고 Codex 내부의 승인된 대체 경로가 없음
- 프로젝트 core identity를 대체하는 변경이 필요함
- 파괴적·보안·비용·권리 위험이 있음
- Codex 구현과 machine QA가 끝나 GPT final review가 필요함

## 6. 지연·실패 우회 경로

임의의 시간 숫자를 영구 상수로 두지 않고 **stall signal**로 판단한다.

```text
STALL_SIGNAL:
- 동일 경로의 bounded retry 뒤 새 evidence가 없음
- 외부 service가 non-terminal 상태에서 진전 evidence를 제공하지 않음
- connector output이 반복 잘림·전송 실패
- executor/tool이 현재 세션에서 callable하지 않음
- 같은 원인으로 같은 command가 반복 실패
- required artifact/readback을 현재 경로가 구조적으로 만들 수 없음
```

```text
primary route
→ bounded retry with state readback
→ authorized fallback A
→ authorized fallback B
→ evidence-equivalent manual/local route when available
→ blocked task만 deferred
→ independent ready work 계속
→ 새 evidence 발생 시 deferred 재평가
→ global stop last
```

- fallback은 evidence·보안·권한·비용 수준을 낮추는 편법이 아니다.
- 같은 실패를 무한 반복하지 않는다.
- current session에 대체 connector/tool이 있으면 단순히 첫 도구가 실패했다는 이유로 사용자에게 수동 작업을 떠넘기지 않는다.
- 필수 source를 읽을 수 없는 상태는 추측으로 우회하지 않는다.

## 7. 승인 위임과 고위험 보류

현재 사용자가 명시적으로 이 모드를 승인한 프로젝트에서는 다음 flag를 활성화할 수 있다.

```text
DELEGATED_RECOMMENDED_DEFAULT_APPROVAL: ACTIVE
NO_ROUTINE_APPROVAL_STOPS
```

자동 승인 범위:

- 기존 승인된 project identity와 Slice scope 안의 권장안
- 기획 세부안·UI/UX 세부안·tunable default
- actual consumer가 있는 bounded 이미지·사운드 production candidate
- 기술 구현 방식·bug fix·reversible refactor
- 누락 test·consumer·reference·small canon sync
- current-task branch·PR·exact-head 안전 병합
- 검증된 문제의 최소 교정

자동 승인은 새 scope를 발명하는 권한이 아니다. 다음은 `HIGH_RISK_DEFERRED`로 묶고, 독립 작업을 모두 진행한 뒤 한 번에 보고·질문한다.

- project core identity 또는 핵심 player promise의 교체
- 대규모 engine migration 또는 저장 호환성 파괴
- irreversible data loss, destructive migration, broad delete
- 계정·credential·보안·네트워크 권한 확대
- 새 유료 비용·구매·결제
- 라이선스·저작권·법적 상태가 불명확한 배포
- 외부 공개·출시·게시·실제 사용자 대상 전송
- ruleset/admin bypass, force push, direct main push

host/system/tool이 confirmation을 강제하면 Base 위임 계약은 이를 우회하지 않는다.

## 8. Delegated Visual·Audio Production

기존 default image conversation approval gate는 보존한다. 다만 현재 사용자가 명시적으로 위임한 Slice에는 opt-in exception을 둔다.

```text
DELEGATED_VISUAL_PRODUCTION_ACTIVE
DELEGATED_AUDIO_PRODUCTION_ACTIVE
BOUNDED_PRODUCTION_PACKET_REQUIRED
CURRENT_SLICE_USE_ONLY
NO_AUTOMATIC_SCOPE_EXPANSION
```

필수 조건:

- exact Project와 current Slice
- actual consumer와 asset/cue slot
- current Art/Audio Direction 또는 approved reference
- required count와 independent brief
- format·dimensions·alpha/crop/import 또는 audio format·loop/loudness 요구
- protected identity·canon
- excluded scope
- objective acceptance
- provenance·rights
- Notion/repository destination
- runtime validation route

조건이 충족되면 current Slice 범위의 생성·선정·revision·Notion delivery는 per-result 사용자 메시지를 기다리지 않고 수행할 수 있다. 생성 성공은 runtime PASS가 아니며, 실제 consumer 적용과 machine QA가 별도 필요하다.

Art Direction master, 대표 캐릭터 identity master, store key art, 라이선스 위험, scope 확대는 위임 대상이 아니다.

## 9. Machine QA 우선·Human QA 보류

현재 사용자 결정:

```text
HUMAN_QA_DEFERRED_BY_CURRENT_USER
MACHINE_QA_FIRST
```

Codex 구현 구간에서 프로젝트가 채택한 도구를 사용한다.

```text
GUT
→ deterministic GDScript/domain regression

Hera
→ live run/stop
→ normal gameplay input path
→ runtime tree/state assertion
→ UI inspection
→ screenshot capture and bounded visual diff
→ diagnostics
→ tracked source pre/post snapshot
→ Hera-phase source delta NONE

repository/engine route
→ import/parse
→ headless/runtime smoke
→ build/export when applicable
```

- GUT/Hera가 프로젝트에 채택되지 않았으면 무조건 설치하지 않고 Existing Solution First와 project adoption authority를 따른다.
- Hera는 persistent authoring에 사용하지 않는다.
- diagnostic state mutation은 normal gameplay acceptance가 아니다.
- screenshot diff는 디자인 품질·가독성·재미·human approval PASS가 아니다.
- `HUMAN_USABILITY_EVIDENCE`와 `PLAYER_EXPERIENCE_EVIDENCE`는 사용자가 실제 플레이하기 전까지 `NOT_RUN`이다.

Machine-executable acceptance를 모두 닫고 explicit human QA만 남으면 상태는 전체 제품 완료가 아니라 다음으로 둔다.

```text
AUTOMATED_VERTICAL_SLICE_READY
READY_FOR_USER_VERTICAL_SLICE_VALIDATION
HUMAN_QA: DEFERRED_BY_USER
```

사용자는 이 빌드를 실제 플레이한 뒤 `EXPAND / FIX / TUNE / REDESIGN / HOLD` 방향을 결정한다.

## 10. 남은 작업 0 계약

`남은 작업 0`은 프로젝트 전체 future roadmap을 자동 실행한다는 뜻이 아니다.

```text
SCOPE_BOUNDED_REQUIRED_WORK_ZERO
```

현재 승인된 Slice와 automation phase의 required work만 계산한다.

```text
ready tasks 실행
→ blocked task recovery/fallback
→ local defer + independent continuation
→ remaining-work recalculation
→ remaining machine-executable required work > 0이면 계속
→ 0이면 completion candidate
→ actual implementation/canon/asset/consumer/test/PR/readback rescan
→ 새 valid finding이면 remaining work reopen
→ 최소 5회 final-state adversarial loop
→ blocking finding 0
→ AUTOMATED_VERTICAL_SLICE_READY
→ user validation은 명시된 다음 milestone
```

다음은 remaining work를 숨기지 않는다.

- 필수 asset/input의 실제 부재
- required machine QA `NOT_RUN`
- merge/readback 미완료
- high-risk deferred가 현재 Slice acceptance를 차단함

다음은 automation phase의 0을 막지 않는 명시적 다음 단계다.

- 사용자가 현재 결정으로 보류한 Human QA
- 현재 Slice 밖 future enhancement
- user validation 결과에 따라 열릴 다음 Slice

## 11. Implementation Reality Gate

```text
plan exists
!= production inputs ready
!= Codex handoff ready
!= implemented
!= GUT pass
!= Hera runtime pass
!= screenshot captured
!= human understands
!= player enjoys
!= user accepted vertical slice
```

각 단계의 evidence identity·SHA·tool version·result·NOT_RUN을 보존한다.

## 12. 영향 범위와 구현 계획

기존 owner에 최소 변경한다.

예상 owner:

- `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_COMPATIBILITY_APPENDIX.md`
- `skills/managing-project-intake-and-work-contract/references/continuous-work-execution.md`
- `docs/GPT_CODEX_WORKFLOW_POLICY.md`
- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- `skills/designing-vertical-slices/SKILL.md`
- focused regression test
- Superpowers implementation plan

구현은 다음을 보존한다.

- default per-image approval gate는 explicit delegation이 없으면 그대로 유지
- open/draft/ready PR read-only
- Work/GPT와 Codex 제품 구현 owner 경계
- HiGodot sole persistent authoring, GUT deterministic tests, Hera live QA only
- Human/Player evidence ceiling
- Base proposal/implementation PR 분리
- squash-only·required check·exact-head·post-merge readback
- zero incremental cost

## 13. 반례와 위험

### 무한 작업 확대

`remaining work 0`이 전체 roadmap을 먹을 수 있다.

- 완화: current approved Slice + automation phase로 계산 범위를 고정한다.

### 위임 승인에 의한 제품 drift

권장안 자동 승인이 project identity를 바꿀 수 있다.

- 완화: current identity·protected scope 안의 선택만 자동 승인하고 core replacement는 high-risk defer한다.

### Work packet 비대화

Codex 전환을 줄이려다 Work가 전체 게임을 미리 기획할 수 있다.

- 완화: 현재 Slice actual consumer와 acceptance에 필요한 정보·asset만 준비한다.

### machine QA 과장

GUT·Hera·screenshot을 human/player proof로 오인할 수 있다.

- 완화: `AUTOMATED_VERTICAL_SLICE_READY`와 `READY_FOR_USER_VERTICAL_SLICE_VALIDATION`을 분리한다.

### fallback 품질 저하

우회 경로가 검증 수준을 낮출 수 있다.

- 완화: evidence-equivalent fallback만 허용하고 필수 source unreadable은 blocked로 유지한다.

### Codex 반환 누적

모든 issue를 batch로 모으면 blocker 발견이 늦을 수 있다.

- 완화: destructive/security/data-loss처럼 즉시 중단해야 하는 high-risk는 즉시 국소 보류하되, routine 질문만 batch한다.

## 14. 검증 계약

TDD로 다음을 검증한다.

- Work v4.9 bundle이 3-stage minimum-transition 계약을 발견한다.
- continuous work가 stall signal → fallback → local defer → independent continuation을 보존한다.
- delegated approval은 explicit opt-in이며 high-risk boundary를 삭제하지 않는다.
- Visual gate가 default explicit approval과 delegated bounded exception을 동시에 보존한다.
- GPT–Codex workflow가 Work input completion → single Codex window → consolidated return → final review를 가진다.
- Vertical Slice가 machine QA ready와 user validation을 구분한다.
- GUT/Hera owner와 evidence ceiling을 재정의하거나 중복하지 않는다.
- 기존 Work v4.9 non-regression test가 계속 통과한다.
- full Base regression과 canonical freshness가 통과한다.

## 15. 프로젝트 전용으로 남길 내용

- 각 프로젝트의 actual Slice, 이미지·사운드 목록, 수치, Art Direction, 캐릭터, scene path
- GUT/Hera exact adopted version과 실제 scenario
- project-specific dangerous decision
- 실제 user play 결과와 다음 개발 결정

## 16. 적용 조건과 비사용 조건

적용:

- 사용자가 current 프로젝트에 연속 실행·권장안 위임을 명시 승인했다.
- Work 준비와 Codex 구현의 전환 비용이 material하다.
- 현재 Slice가 bounded되어 있다.
- 실제 product implementation과 machine QA가 필요하다.

비사용:

- 사용자가 검토만·제안만·병합 금지·이미지별 승인 유지처럼 범위를 제한했다.
- exact Project 또는 current Slice가 불명확하다.
- 외부 공개, 결제, 계정·보안 권한, 파괴적 migration처럼 high-risk confirmation이 필요하다.
- Human/Player validation을 machine QA로 대체하려는 경우다.

## 17. 필요한 도구·파일·권한

- 필요 항목: 기존 GitHub connector, current Work, 프로젝트별 Codex, 프로젝트가 이미 채택한 HiGodot/GUT/Hera
- 필요한 이유: 정본 수정·제품 구현·자동 test/runtime QA·readback
- 설치·적용 방법: 새 공용 provider는 설치하지 않는다. 프로젝트 채택 상태를 fresh-read한다.
- 설치 후 확인 명령: owner별 기존 exact-version·test·runtime·source-delta Gate를 사용한다.
- 최소 권한: current-task branch/PR write와 안전 merge; direct main/force/admin bypass 없음
- 추가 비용: `ZERO_INCREMENTAL_COST`

## 18. 승인과 구현

- 사용자 승인 근거: `2026-08-27 current ChatGPT Work conversation — "권장안 B 승인" 및 지연 우회, 남은 작업 0, routine 승인 위임, Human QA 보류, Hera/GUT 화면 확인, Work 준비→Codex 구현→사용자 Slice 검증을 명시`
- 구현 상태: `APPROVED_FOR_IMPLEMENTATION`
- 구현 PR: `별도 PR 예정`
- 보호 중인 기존 PR: 모든 pre-existing open/draft/ready PR은 read-only
- 롤백: 구현 PR 전체를 하나의 squash commit으로 revert하고 default approval·Work/Codex·Visual·QA 기존 경계로 복귀
