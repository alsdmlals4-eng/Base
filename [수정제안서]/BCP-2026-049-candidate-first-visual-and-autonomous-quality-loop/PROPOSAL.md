# BCP-2026-049 · 후보 선제작 이미지와 자율 품질·학습 루프

## 출처와 상태

```yaml
proposal_id: BCP-2026-049-candidate-first-visual-and-autonomous-quality-loop
submitted_at: 2026-08-29
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: 2026-08-29 current user instruction — 이미지 후보 선제작, 실제 구현 가능성 조사, 장기 품질 우선, 사용자 개입 최소 자동화·학습, 작업 후 실제 적대적 검토·교정
source_base_main: b384f4750b06287a0768dee5b2077807a41484e5
incremental_paid_cost: 0
```

이 제안은 단순 문구 추가가 아니다. Base의 오래된 이미지 사전승인·Notion 중심 맞춤형 지침과, 이미 최신 프로젝트에서 검증 중인 후보 선제작·repository-first·실현 가능성·적대적 검토 계약을 하나의 공용 실행 경계로 정렬한다.

## 사용자 승인 목표

1. 이미지가 실제로 필요하면 프로젝트의 기존 기획·승인 이미지·시안·실제 소비처를 먼저 읽고 일관된 후보를 제작한다.
2. 후보 제작 전 매번 멈추지 않고 결과를 먼저 제시한 뒤, 사용자가 최종 확정·수정·폐기를 결정한다.
3. 새 시스템·데이터·UI/UX·Godot 구조는 최신 공식 자료, 직접 관련 벤치마크와 현업 사례를 조사하고 실제 코드·Scene·Resource·asset·test·runtime 경계에서 구현 가능한지 확인한다.
4. 빠른 임시완료보다 장기 효율·유지보수성·재사용성·정본 명확성·완성도를 우선하되 근거 없는 과설계는 피한다.
5. 사용자는 핵심 제품 의미·취향·고위험·최종 visual lock에 집중하고, 조사·비교·후보 제작·기계검증·교정·readback·교훈 환류는 가능한 범위에서 연속 수행한다.
6. 작업 후 적대적 검토와 교정은 보고 문구가 아니라 실제 증거가 있어야 하며, 최소 5회 전체 루프와 CLEAN_REVIEW_EXIT를 적용한다.

## 현재 Base 문제

### P1. 이미지 후보 제작 전에 멈추는 구형 두 턴 Gate

`docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`와 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`는 assistant가 필요성을 발견한 이미지에 대해 `TEXT_BRIEF → STOP → NEXT_USER_EXPLICIT_APPROVAL → GENERATE`를 강제한다.

이 구조는 실제 consumer와 승인 visual direction이 이미 확인된 경우에도 같은 승인을 반복하게 해 사용자 개입과 Work↔사용자 왕복을 증가시킨다.

### P2. 맞춤형 지침 템플릿의 정본 drift

`templates/custom-instructions.gpt.md`는 아직 다음 구형 전제를 포함한다.

- Notion을 사람용 current canon으로 사용
- 프로젝트 작업마다 연결 Notion을 기본 확인
- GitHub/Notion 동시 동기화
- 이미지 생성은 사용자가 현재 메시지에서 명시 요청한 경우에만 수행

이는 Base latest repository-first workspace와 다수 프로젝트의 current policy에 충돌한다.

### P3. 프로젝트마다 같은 공용 원칙을 개별 보정

십보강호, Blacksmith, GRIMOIRE, Omenward, Switchy Express와 Tetris는 이미 다음을 프로젝트별로 구현했다.

- actual consumer와 current visual canon을 먼저 확인
- 후보는 별도 이미지별 재승인 없이 생성 가능
- 생성 성공·사용자 final lock·repository asset promotion·runtime evidence 분리
- current official/primary research와 실제 implementation feasibility 확인
- material change 뒤 최소 5회 full-scope adversarial loop 또는 Base post-change loop

반면 Ninja Survival은 여전히 `사용자가 명시 요청한 경우에만 생성`, MylittleBoat는 한 번의 clean review 표현, Coc-Fiction은 잔여 Notion 완료조건, urban-legend 하위 image workflow는 Notion/Sheet 이중 기록을 current gate처럼 남긴다.

### P4. 자동화 목표가 수동 승인 생략으로 오해될 위험

사용자 개입 최소화는 다음을 뜻하지 않는다.

- 핵심 게임 의미 자동 확정
- 대규모 이미지 batch 무제한 생성
- 후보의 자동 정본 승격·runtime 연결
- 위험한 삭제·배포·비용·보안 변경 자동 승인
- 실행하지 않은 테스트나 적대적 검토를 PASS로 보고

따라서 후보 제작 권한과 final lock/implementation authority를 명확히 분리해야 한다.

## 프로젝트 실증 근거

| 프로젝트 | 현재 증거 | 일반화 결과 |
|---|---|---|
| Ten-Paces-Hidden-Moves | 생성 전 재승인 없이 scoped candidate, 생성 후 final lock, 외부 조사·실현 가능성·5회 loop | 후보 선제작과 final lock 분리 가능 |
| Blacksmith | `USER_PREAUTHORIZED_AFTER_CONSUMER_REQUIREMENT`, final direction/runtime promotion은 사후 lock | actual consumer를 선행조건으로 사용 |
| GRIMOIRE | `USER_PREAUTHORIZED_GENERATE_CANDIDATE__FINAL_LOCK_ONLY`, runtime batch 확장은 사용자 확정 | 후보와 product promotion 분리 |
| Omenward | `USER_AUTHORIZED_AUTONOMOUS_REQUIRED_IMAGES`, post-change 5회 loop | project-authorized autonomous production 가능 |
| Switchy Express | concrete consumer가 있을 때 per-image approval 없이 생성, candidate는 runtime proof 아님 | repository provenance와 evidence ceiling 유지 |
| Tetris | planning visual은 auto-generate 후 user lock, runtime image는 exact Godot consumer 필요 | planning/runtime image의 서로 다른 gate 유지 |

프로젝트 고유 visual style, asset path, 캐릭터·세계관, 수치, 특정 Decision ID는 Base에 복사하지 않는다.

## 외부 공식·실무 조사

### Google SRE — 반복 작업 제거와 사람 fallback

- https://sre.google/workbook/eliminating-toil/
- https://sre.google/sre-book/postmortem-culture/

채택:

- 반복 수동작업은 계측하고 가능하면 증상 우회가 아니라 원인에서 제거한다.
- 복잡한 자동화는 한 번에 완전자동화하지 않고 human-backed interface에서 점진 개선한다.
- unsafe condition에서는 사람에게 되돌리고, feedback·오류율·재작업·사람 시간 절감을 측정한다.
- 실패 원인과 교훈을 구조화해 다른 작업에서 재사용한다.

### NIST AI RMF·SSDF — 전 수명주기 검증과 재발 방지

- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- https://airc.nist.gov/
- https://csrc.nist.gov/projects/ssdf

채택:

- 설계·개발·사용·평가 전 수명주기에서 testing, evaluation, verification, validation을 구분한다.
- 요구·위험·설계결정·provenance를 추적하고, 문제의 근본 원인을 반영해 재발을 막는다.

### Godot 4.7 공식 문서 — 실제 구조 가까이 검증

- https://docs.godotengine.org/en/4.7/tutorials/best_practices/index.html
- https://docs.godotengine.org/en/4.7/tutorials/best_practices/project_organization.html

채택:

- 일반론으로 “구현 가능”을 선언하지 않고 실제 project filesystem, Scene, Resource와 consumer 근처에서 구조를 검증한다.
- 프로젝트가 커질수록 asset과 consumer의 소유 경계를 유지보수 가능한 방식으로 조직한다.

### GitHub 공식 문서 — 최신 SHA의 검증 증거

- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request

채택:

- required check는 최신 commit SHA를 기준으로 확인한다.
- 자동 병합은 review/check 요구가 충족된 경우에만 사용하며 보호 규칙을 우회하지 않는다.

## 비교한 대안

| 대안 | 장점 | 실패 모드 | 판정 |
|---|---|---|---|
| 모든 이미지에 기존 두 턴 사전승인 유지 | 위험이 낮아 보임 | 승인된 방향·consumer에도 반복 개입, 자동화 목표 실패 | REJECT |
| 필요하다고 판단하면 무제한 batch 생성·자동 적용 | 사용자 개입 최소 | scope 폭증, 비용·drift·후보/정본/runtime 혼동 | REJECT |
| consumer·current visual 확인 후 bounded candidate 선제작, 사용자 final lock 뒤 승격 | 왕복 감소와 사람 통제 동시 유지 | precondition·상태·회귀 test 필요 | ADOPT |
| 빠른 최소패치 우선, 조사·검토는 선택 | 단기 속도 | 반복 부채·구현 불가능한 명세·완료 과장 | REJECT |
| 장기 가치/실현 가능성/검증 우선 + 과설계 방지 | 초기 작업량 증가 | 기준이 없으면 느려질 수 있음 | ADOPT, ROI·non-goal·minimum sufficient complexity 필수 |

## 채택 공용 계약

### 1. `CANDIDATE_FIRST_VISUAL_PRODUCTION`

```text
VISUAL_NEED_CONFIRMED
→ CURRENT_PROJECT_AND_VISUAL_CANON_READBACK
→ ACTUAL_OR_EXPLICITLY_PLANNED_CONSUMER_REQUIRED
→ EXISTING_APPROVED_ASSET_AND_CANDIDATE_REUSE_CHECK
→ BOUNDED_BRIEF_READY
→ IMAGE_MODEL_GENERATES_ONE_CANDIDATE
→ OBJECTIVE_QA_AND_BOUNDED_CORRECTION
→ PRESENT_FOR_USER_FINAL_LOCK
```

- current project identity·approved visual anchor·Keep/Avoid/Do Not Drift·consumer·규격이 확인되면 후보 제작은 standing preauthorization을 가진다.
- 방향 자체가 없거나 current anchors가 충돌하면 비교용 exploration 하나를 먼저 만들거나 `BLOCKED_UNVERIFIED`로 닫는다.
- host/system/tool이 명시적 이미지 요청을 별도로 요구하면 그 상위 제약을 따른다.
- 한 candidate 또는 명시된 bounded correction 뒤에는 결과를 사용자에게 보여주고 final lock을 받는다.

### 2. 상태 분리

```text
NEEDED
→ BRIEF_READY
→ GENERATED_CANDIDATE
→ OBJECTIVE_QA_PASSED | REVISION_REQUIRED | REJECTED
→ USER_FINAL_LOCKED
→ CANON_REGISTERED
→ IMPLEMENTED
→ RUNTIME_VERIFIED
```

```text
GENERATED_CANDIDATE
!= USER_FINAL_LOCKED
!= PROJECT_ASSET_APPROVED
!= CANON_REGISTERED
!= IMPLEMENTED
!= RUNTIME_VERIFIED
```

후보 제작은 Blueprint나 product implementation authority를 만들지 않는다. 신규 구현은 해당 프로젝트의 exact Blueprint/Decision/implementation approval gate를 별도로 통과한다.

### 3. `IMPLEMENTATION_FEASIBILITY_BEFORE_COMMITMENT`

material system·data·UI/UX·asset pipeline·automation 구조를 채택하기 전에 다음을 실제로 확인한다.

```yaml
current_owner_and_actual_implementation:
current_official_primary_sources:
directly_relevant_success_failure_or_mixed_cases:
material_alternatives:
project_fit_and_player_value:
actual_consumer_and_integration_boundary:
scene_node_resource_script_data_state_signal_save_structure:
test_debug_runtime_performance_platform_constraints:
rollback_migration_and_evidence_ceiling:
classification: FEASIBLE | PARTIAL | BLOCKED_UNVERIFIED
```

### 4. `LONG_TERM_QUALITY_OVER_LOCAL_SPEED`

- 반복 비용, 정본 drift와 기술 부채를 줄이는 장기 효율을 우선한다.
- root-cause fix, 재사용 가능한 owner/test/automation, 명확한 rollback을 선호한다.
- 현재 필요를 넘는 speculative abstraction·대규모 범용화는 거절한다.
- 시간 투입의 정당성은 player/user value, 재작업 감소, 검증 가능성과 유지비 절감으로 설명한다.

### 5. `MINIMIZE_USER_INTERVENTION_WITH_SAFE_FINAL_CONTROL`

AI가 연속 수행할 기본 범위:

- fresh-read와 authority reconstruction
- 조사·대안 비교·feasibility classification
- bounded visual candidate와 objective QA
- 안전한 문서·정본·test·readback 교정
- 실제 검증과 남은 작업 재계산
- 문제·원인·해결·회귀 방지·Base 승격 후보 환류

사용자에게 남기는 기본 gate:

- 핵심 제품 의미·서사·경제·Art Direction 변경
- 서로 우열이 객관적으로 결정되지 않는 취향 선택
- 후보 visual final lock과 runtime promotion
- 비용·외부 공개·배포·보안·권한·비가역 삭제
- 현재 정본과 직접 충돌하는 scope expansion

### 6. `ACTUAL_POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`

- 변경 후 Base `running-adversarial-review-and-refinement`의 최소 5회 full-scope loop를 실제 수행한다.
- 각 회차의 input/head, evidence delta, finding, validated finding, applied correction, verification, better alternative, long-term fit, unresolved를 기록한다.
- 실행 증거가 없으면 “적대적 검토 완료”라고 보고하지 않는다.
- 최소 5회 뒤 새 blocking finding·회귀·stale reference·evidence ceiling 위반이 0일 때만 `CLEAN_REVIEW_EXIT`다.

### 7. `INCIDENT_SOLUTION_LESSON_AUTOMATION_LOOP`

```text
problem
→ reproducible evidence
→ root cause
→ minimal correction
→ regression prevention
→ project owner/readback
→ reusable lesson candidate
→ Base BCP when cross-project evidence exists
```

학습은 대화 기억에 의존하지 않고 repository owner·test·checklist·automation·proposal로 남긴다.

## 구현 범위

Base 별도 구현 PR에서 다음을 수정한다.

1. `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
2. `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
3. `docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`
4. `templates/custom-instructions.gpt.md`
5. `templates/project-operations/CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9.md`
6. focused regression contract와 design/plan/review evidence

프로젝트 별도 PR에서 current top-level 또는 delegated owner가 직접 충돌하는 경우만 최소 교정한다.

- MylittleBoat `AGENTS.md`
- ninja-survival-godot `AGENTS.md`
- Coc-Fiction `AGENTS.md`
- urban-legend `docs/IMAGE_ASSET_WORKFLOW.md`

이미 같은 계약을 가진 프로젝트는 변경하지 않고 exact readback receipt로 닫는다.

## 보호·제외 범위

- 실제 이미지 생성·편집 없음
- 기존 이미지 binary·asset·runtime scene 변경 없음
- 새 paid service/provider/dependency 없음
- host/system image tool precedence 변경 없음
- 후보를 사용자 승인·정본·runtime으로 자동 승격하지 않음
- Blueprint 최종 승인과 Codex implementation gate 우회 없음
- open/draft/ready PR의 기존 소유 경로 수정 없음
- 프로젝트별 game rule·art style·story·numeric tuning 변경 없음
- `[수정제안서]/PROPOSAL_REGISTRY.json`은 진행 중 proposal workstream과 충돌하지 않도록 이번 PR에서 수정하지 않음

## 검증 계획

1. focused contract를 먼저 추가하고 기존 Base에서 실패를 관측한다.
2. owner·template을 수정해 focused contract를 GREEN으로 만든다.
3. 기존 image-model-only, visual-anchor, Blueprint, Work v4.9 계약을 회귀 검사한다.
4. canonical reference freshness로 old active semantics와 Notion current-canon drift를 검색한다.
5. exact-head GitHub Actions와 `ci-gate` 결과를 읽는다.
6. 최소 5회 full-scope adversarial loop를 실제 기록하고 finding을 같은 PR에서 교정한다.
7. merge가 허용되면 squash merge 후 새 main·same-goal PR·정본·테스트를 readback하고 post-merge review를 수행한다.

## 롤백

- proposal 기록은 결정·검토 이력으로 보존한다.
- 구현 PR은 한 squash commit 단위로 revert 가능해야 한다.
- 프로젝트별 PR도 독립 squash commit으로 분리해 Base 전체 롤백과 프로젝트 전용 rollback을 분리한다.
- 롤백 시 구형 두 턴 Gate를 암묵적으로 되살리지 않고 rollback 사유와 다음 안전 경계를 별도 Decision으로 기록한다.
