# 자율 품질·선제 후보 제작·증거 기반 교정 실행 계획

> 기준: `Base@b384f4750b06287a0768dee5b2077807a41484e5`
> 설계: `docs/superpowers/specs/2026-08-29-autonomous-quality-generate-then-lock-design.md`
> 작업 브랜치: `docs/autonomous-quality-generate-then-lock-20260829`

## 목표

사용자 승인 네 항목과 증거 기반 적대적 검토를 Base active owner와 실제 drift 프로젝트에 반영한다. 기존 open/draft/ready PR은 read-only로 유지한다.

## Task 1 — 회귀 계약을 먼저 만든다

대상:

- `tests/test_project_image_request_visual_anchor_pipeline.py`
- `tests/test_autonomous_quality_generate_then_lock_contract.py` 신규

검증할 항목:

- concrete need는 사전 생성 승인 없이 후보 1건 제작 가능
- 기존 visual canon/anchor/consumer readback 필수
- 생성 후 `LOCK / REVISE / REJECT`
- 후보/승인/정본/구현/runtime 상태 분리
- current research + 최소 3안 + actual implementation feasibility
- long-term efficiency + no unsupported overengineering
- safe automation + fail-closed human escalation
- claim-only adversarial review 무효와 loop evidence receipt
- old two-turn token은 `SUPERSEDED`로만 존재

## Task 2 — Base active owner를 교정한다

대상:

- `templates/custom-instructions.gpt.md`
- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`
- `docs/AUTONOMOUS_QUALITY_OPTIMIZATION_AND_LEARNING_POLICY.md` 신규
- `templates/project-operations/ADVERSARIAL_REVIEW_EVIDENCE_RECEIPT.yml` 신규

보호 조건:

- `IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md` 유지
- actual consumer / Visual Requirement / provenance / rights 유지
- `GENERATE_EXACTLY_ONE`, `STOP_REQUIRED_AFTER_GENERATION`, `NO_AUTOMATIC_IMAGE_CHAIN` 유지
- Blueprint final approval before implementation 유지
- open PR #713/#748/#660 및 기타 pre-existing PR 경로를 수정하지 않음

## Task 3 — Base exact-head 검증과 1차 교정

- changed-file diff 확인
- 관련 Python tests와 repository CI 실행
- 실패는 실제 log를 읽고 root cause를 분류
- exact head에서 테스트 PASS 확인
- 문서-only 결과를 runtime PASS로 확대하지 않음

로컬 clone은 현재 실행 환경의 DNS 차단으로 `BLOCKED_NO_LOCAL_NETWORK`다. GitHub Actions exact-head 결과를 remote machine evidence로 사용하고 로컬 실행은 `NOT_RUN`으로 구분한다.

## Task 4 — 프로젝트 전수 drift를 교정한다

Fresh-read 대상:

- MylittleBoat
- urban-legend
- ninja-survival-godot
- omenward
- Ten-Paces-Hidden-Moves
- Blacksmith
- Coc-Fiction
- GRIMOIRE-
- Switchy-Express-Cargo-Puzzle
- Tetris

판정:

- `CHANGE_REQUIRED`: Base 새 계약과 직접 충돌하는 active owner를 project-specific 의미를 보존하며 수정
- `ALREADY_ALIGNED`: user-preauthorized candidate generation, current research/feasibility, long-term review와 five-loop evidence가 이미 active owner에 있으면 불필요한 diff를 만들지 않음

현재 preflight finding:

| repository | preliminary result | target |
|---|---|---|
| MylittleBoat | CHANGE_REQUIRED | root `AGENTS.md`의 one-clean-pass·quick-small-change 표현 보강 |
| urban-legend | CHANGE_REQUIRED | `docs/IMAGE_ASSET_WORKFLOW.md`의 stale Notion/Sheet와 no-auto-candidate 교정 |
| ninja-survival-godot | CHANGE_REQUIRED | root `AGENTS.md`의 explicit-request-only 문구를 DEC-034와 일치시킴 |
| Coc-Fiction | CHANGE_REQUIRED | root `AGENTS.md`의 조건부 Notion 완료 Gate를 repository-only로 교정하고 비게임 research/review 계약 추가 |
| Ten-Paces-Hidden-Moves | ALREADY_ALIGNED | no mutation unless review finds drift |
| omenward | ALREADY_ALIGNED | no mutation unless review finds drift |
| Blacksmith | ALREADY_ALIGNED | no mutation unless review finds drift |
| GRIMOIRE- | ALREADY_ALIGNED | no mutation unless review finds drift |
| Switchy-Express-Cargo-Puzzle | ALREADY_ALIGNED | no mutation unless review finds drift |
| Tetris | ALREADY_ALIGNED | no mutation unless review finds drift |

각 변경 저장소는 latest main에서 별도 branch/PR을 만들고 open PR을 침범하지 않는다.

## Task 5 — 실제 적대적 검토·교정

Base와 각 retained project PR에 다음 전체 loop를 최소 5회 수행한다.

```text
FULL_SCOPE_READ
→ ATTACK
→ VALIDATE_FINDING
→ APPLY_CORRECTION_OR_RECORD_BLOCKER
→ EXACT_HEAD VERIFY
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_FIT_RECHECK
→ RE-ATTACK RESULTING STATE
```

각 loop는 `templates/project-operations/ADVERSARIAL_REVIEW_EVIDENCE_RECEIPT.yml` 필드를 실제 값으로 채운다. 관점 이름만 바꾼 검토는 loop로 계수하지 않는다.

공격 범위:

- user intent / product value
- authority / current owner / supersession
- exact diff / untouched consumers / tests
- image state and asset promotion
- external research relevance / implementation feasibility
- automation safety / user-intervention boundary
- long-term maintainability / overengineering
- cost / paid dependency
- evidence ceiling / rollback / readback

## Task 6 — PR·병합·post-merge readback

- current-task PR 생성
- exact head, check suites, mergeability, review/thread 상태 확인
- required check가 없더라도 실행된 relevant checks를 확인
- 사용자 승인 continuation 범위에서 안전한 PR만 squash merge
- 새 main SHA와 target files를 다시 읽음
- same-goal open/recent PR, canon, tests와 충돌 재검사
- `REMAINING_WORK_RECALCULATION_REQUIRED`

## 완료 기준

- Base active owner와 맞춤형 지침 템플릿 교정 완료
- 4개 drift project active owner 교정 또는 실제 review에 따른 조정 완료
- aligned 6개 project에 불필요한 변경 없음
- 최소 5회 evidence-backed full-scope loop 실제 기록
- validated finding 전부 교정 또는 명시적 blocker
- exact-head remote tests/checks 결과 확인
- 병합한 경우 post-merge main readback 완료
- 미실행 로컬/Godot/Human evidence는 `NOT_RUN` 유지
