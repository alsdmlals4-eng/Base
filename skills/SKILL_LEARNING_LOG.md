# Base Skill Learning Log

## 2026-09-01 — 기능별 코드·계약 경계의 소형 기능 라우팅

- **상태:** `OBSERVATION`
- **Trigger:** 기능별 코드·계약 모듈화가 작업 분해 reference에는 필요했지만, 승인된 작은 작업은 intake Registry의 비사용 조건에 걸리고 실행계획에는 contract owner·공개 경계·consumer 입력란이 없었다.
- **Finding:** 파일 또는 작업 단계가 작다는 이유만으로 새 공개 계약·상태 소유권·consumer 연결을 intake 없이 처리하면, 정본·구현·테스트·롤백 연결이 누락될 수 있다. 반대로 이미 승인된 내부 경계를 그대로 구현하는 continuation까지 L1로 승격하면 불필요한 절차와 정본 복제가 생긴다.
- **Decision:** 새 기능 또는 기능 계약·공개 경계·상태 소유권·consumer 연결의 의미 변경만 작업 크기와 무관하게 `managing-project-intake-and-work-contract`로 라우팅한다. 이미 승인·정의된 경계를 그대로 구현하는 작은 continuation은 기존 approval reference를 재사용한다. `EXECUTION_SEQUENCE_PLAN.md`에는 기존 owner와 구현·데이터·테스트 위치, 공개·통합 경계, 실제 consumer·의존 방향, 검증·롤백을 연결하며 별도 Registry나 중복 정본을 만들지 않는다.
- **Evidence ceiling:** 이 Base 변경은 작성·라우팅·양식 계약의 기계 검증만 다룬다. 기존 프로젝트 코드가 이미 모듈화됐거나 Godot runtime·UX·사용자 검수가 완료됐다는 뜻은 아니다.
- **Recheck trigger:** 작은 기능이 다시 intake를 우회하거나, 실행계획에서 contract owner·public boundary·consumer path가 누락되거나, 단순 내부 구현까지 과도하게 L1 계약 작업으로 분류될 때 경계를 재검토한다.

## 2026-08-27 — Screen inventory is a subordinate input, not a second visual coverage owner

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** 화면-first audit를 추가하면서 별도 companion 문서가 기존 Visual Asset Coverage와 같은 완료·READBACK 책임을 갖도록 구현됐다.
- **Finding:** 화면 누락을 먼저 찾는 계약은 필요하지만, screen inventory와 asset coverage가 각각 완료 상태를 소유하면 공용 소비자가 둘 중 하나만 읽거나 서로 다른 PASS를 만들 수 있다.
- **Decision:** `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`를 `CANONICAL_VISUAL_COVERAGE_OWNER`로 유지하고, screen inventory는 `SUBORDINATE_TO_GAME_VISUAL_ASSET_COVERAGE_OWNER` preflight와 handoff만 소유한다. 이미지 정책·Art Skill·생성 계획·Work 지시문은 screen inventory 뒤 canonical coverage owner를 호출한다.
- **Evidence:** `tests/test_game_visual_asset_coverage_contract.py`, `tests/test_bca_visual_sheet_workflow.py`, PR #763.
- **Boundary:** gap 발견은 이미지 생성 승인, runtime PASS, human visual approval이 아니다.
- **Next trigger:** 새 화면·UI·asset checklist가 독립 완료 status 또는 READBACK owner를 추가할 때 single-owner reconciliation을 다시 수행한다.


## 2026-08-25 — Product responsibility, not code shape, determines Codex ownership

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** GPT↔Codex 역할 분리 중 Base Python test·Registry/generated·CI를 코드라는 이유로 Codex 영역에 잘못 포함했다.
- **Finding:** Base governance code와 game product code는 모두 코드 형식일 수 있지만 책임 owner가 다르다.
- **Decision:** `GPT_BASE_NOTION_GOVERNANCE_OWNER`가 Base·Notion·문서·표·이미지·Registry/generated·CI/test contract를 소유하고, `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER`는 실제 게임 프로젝트의 GDScript·Scene·Resource·runtime wiring·build/export·Godot implementation/runtime/play test에만 진입한다.
- **Evidence:** `docs/GPT_CODEX_WORKFLOW_POLICY.md`, `docs/WORK_MODE_AND_SKILL_ROUTING.md`, `skills/maintaining-project-context-and-handoff/SKILL.md`, `templates/project-operations/CODEX_IMPLEMENTATION_WORK_INSTRUCTION.md`, PR #674.
- **Boundary:** 실제 Godot runtime PASS는 별도 project evidence가 필요하다.
- **Next trigger:** Base 작업이 다시 Codex에 라우팅되거나 GPT가 실제 Godot 제품 구현을 직접 누적하려 할 때 재검토한다.

## 2026-08-21 — Behavior fixtures must move with active Skill contracts

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** behavior contract 검사가 Git 동기화의 구형 `publish-remote / verify-sync`와 폐기된 standalone HTML dashboard mode를 current Skill package에서 찾지 못했다.
- **Finding:** 2일 전 기준에도 Git 동기화 fixture 3개가 이미 stale했고, HTML → Notion Home 재분류 뒤 3개가 추가됐다. 본문 전체 단어 검색은 우연히 남은 `inspect`, `frame`, `build` 토큰을 mode로 오인해 일부 drift를 숨겼다.
- **Decision:** current Git sync의 `preflight / reconcile / publish / verify`, current Notion Home의 명시적 5단계 mode로 fixture를 갱신한다. 조기 최종답변 회귀를 직접 압박하는 `SBE-040`은 2일 전 비교, 인터넷 원출처, 최소 3개 대안, 실제 Tool 실행, 5회 전체 적대적 개선 루프, `NOT_RUN` 완료 차단과 중간보고 축소≠작업 축소를 요구한다.
- **Evidence ceiling:** schema·coverage·discoverability 검사는 정적 계약만 증명한다. 외부 모델 결과 파일이 없으므로 `MODEL_RUN_STATUS: NOT_RUN`이며 실제 ChatGPT 행동 개선은 별도 fresh-conversation benchmark 전까지 미검증이다.
- **Next trigger:** mode 토큰이 선언부가 아닌 본문 우연 일치로 통과하거나, active Skill 변경 시 behavior fixture drift가 다시 발생하면 machine-readable mode ownership과 freshness check를 별도 승인 범위에서 검토한다.

## 2026-08-19 — Visual dashboard responsibility moved to self-contained Notion Home

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** 프로젝트 관리용 standalone HTML/local visual surface를 폐기하면서도 사람이 시스템 관계·상태·UX flow를 한 화면에서 읽을 책임은 계속 필요했다.
- **Finding:** `building-project-visual-dashboards`를 통째로 삭제하면 기존 유효한 human-facing visualization 책임까지 잃고, 새 Notion 전용 Skill을 만들면 같은 목적의 owner가 중복된다.
- **Decision:** 기존 Skill을 `NOTION_PROJECT_HOME_AND_VISUAL_MAP` 책임으로 재분류한다. Project Home은 `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`을 만족하고, standalone HTML/dashboard 생성은 금지한다. GitHub/repository runtime truth와 Notion human-facing projection의 authority는 계속 분리한다.
- **Evidence:** `tests/test_bca_visual_sheet_workflow.py`와 PR #548 selective-integration regression이 Skill body·Registry route·Notion Home·HTML 금지·Sheet migration-only 경계를 검증한다. QA Evidence Studio는 프로젝트 관리 surface가 아니라 specialist validation utility이므로 유지한다.
- **Boundary:** Notion Home 재분류가 실제 사람 이해도를 향상시켰다는 human usability evidence는 아직 `NOT_RUN`이다.
- **Next trigger:** Notion Home이 반복적으로 너무 커져 탐색성이 악화되거나, 별도 visual workspace에 고유 편집 기능이 실제 blocker로 입증될 때 재검토한다.


## 2026-08-13 — BCP-2026-027 Claim and Intent Verification Gate

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** AI·Agent·작업자의 사실·완료 주장과 승인한 의도가 실제 저장소·실행·병합 결과에 연결됐는지 fail-closed로 확인할 공용 절차가 필요했다.
- **Observed regression:** PR #313 감사에서 `README.md` drift 가설이 검색 결과만으로 저장소 사실에 과승격됐고, PR #316의 exact-SHA readback이 이를 `INVALIDATED_FINDING`으로 교정했다.
- **Decision:** 새 ACTIVE Skill을 만들지 않고 `reviewing-and-validating-project-changes`에 `claim-and-intent-verification` Mode와 전용 reference를 흡수한다. 기존 Registry owner에 좁은 trigger를 추가하고 Material Claim Ledger, Intent–Implementation Fidelity Matrix, Completion Claim Gate를 validation Template·REVIEW 운영 문서·`SBE-038`에 연결한다.
- **Fail-closed boundary:** 검색 결과·snippet·생산자 설명·모델 자신감은 lead일 뿐 Evidence가 아니다. exact-ref file readback, 실제 diff, exact HEAD 실행 결과, merge SHA와 post-merge main readback이 없으면 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED` 또는 `BLOCKED_UNVERIFIED`를 유지한다.
- **TDD evidence:** PR #319 exact RED head `bf0890439cbef96777171cc00a0229c65e852af8`의 required workflow에서 기존 계약 뒤 신규 Gate 계약 6개가 예상대로 실패했다. 별도 whitespace 3건도 함께 검출돼 구현 변경에서 제거한다.
- **Evidence ceiling:** 정적·테스트 PASS를 runtime·render·사용성·재미·시장성 PASS로 승격하지 않는다. model behavior run은 실제 실행 전 `NOT_RUN`이다.
- **Next trigger:** 서로 다른 프로젝트에서 완료 오판·의도 drift·검색 사실 과승격이 재발하거나, 새 trigger가 과도하게 route할 때 경계를 재검토한다.

## 2026-08-10 — Handoff consumer inventory before compression

- Sources: BCP-013, BCP-014, BCP-016, BCP-019, and the approved continuity design.
- Finding: a compact handoff can accidentally break a machine consumer, while preserving every literal can fossilize an incidental representation.
- Decision: `auditing-canonical-reference-freshness` inventories `CURRENT_MUTABLE`, `CANONICAL_LOCATOR`, `HISTORICAL_DISCOVERY`, `COMPATIBILITY_ANCHOR`, and `SAFE_TO_DROP`; semantic migration requires a canonical-owner check and cannot weaken a real `literal protocol`.
- Boundary: this is review guidance, not an automatic document rewrite or a claim that all literal consumers are accidental.
- Validation: `tests/test_gpt_codex_workflow_contract.py` and exact-head canonical-reference freshness audit.

## 2026-08-10 — staged Canon migration의 debt set·frontier 전파 감사

- **Finding:** 새 Canon Decision의 즉시 권위와 과거 활성 DRAFT의 이관 완료를 같은
  상태로 취급하면, 의미를 잃는 blind rewrite와 무제한 legacy 확산 사이에서 선택하게
  된다. candidate frontier를 검증 전 verified prefix로 부르거나, derived consumer가
  미검증 경계를 normal continuity로 연결하면 거짓 상태 전파가 생긴다.
- **Decision:** 소설의 lifecycle과 narrative 판단은
  `developing-and-revising-serial-fiction: canon-and-continuity`이 소유한다.
  `auditing-canonical-reference-freshness`는 active/archive consumer inventory,
  exact debt set, declared validation gate, derived-consumer propagation,
  duplicate current authority를 감사만 하며 project field·chapter·사건 truth는 정하지
  않는다.
- **Evidence:** focused serial-fiction contract의 RED→GREEN, exact-head reference
  freshness, protected-surface diff audit. 실제 두 번째 프로젝트 적용과 human usability는
  `NOT_RUN`이다.
- **Boundary:** Base는 특정 작품의 Canon ID, bundle 크기, chapter 번호, source 파일명,
  index/reverse-outline schema를 강제하지 않는다. `PASS_WITH_KNOWN_DEBT`는
  `CANON_MIGRATION_COMPLETE`가 아니다.
- **Next trigger:** 다른 작품 적용, debt set 확산, candidate frontier 조기 승격,
  derived consumer의 false continuity 또는 duplicate current authority 발견.

## 2026-08-10 — 튜토리얼은 설명이 아니라 재사용 가능한 행동 학습

- **상태:** `OBSERVATION`
- **Trigger:** 구형 튜토리얼·온보딩 제안의 재검토에서, 기본 규칙 → 필요·결핍 → 해결 방법 발견 → 성장 체감 → 독립 수행 → 다른 상황 전이의 학습 사다리를 기존 게임 기획 책임자에 재포팅했다.
- **Decision:** 새 광역 Skill을 만들지 않고 `analyzing-and-refining-game-concepts`의 조건부 `tutorial-and-onboarding-design` mode와 공용 Guide·프로젝트 Contract로 흡수한다. 튜토리얼 이해도 연구 coverage는 계속 `governing-game-user-research-coverage`가 소유한다.
- **Evidence:** 새 계약은 정적 조작표, 상점·과금을 위한 강제 패배, 가짜 결핍·가짜 성장, 완료율·한 번의 성공만으로 숙련 확정하는 실패 경계를 명시한다. RED/GREEN 계약 테스트와 기존 게임 기획 통합 회귀, 보호된 Registry 무변경 검사를 연결했다.
- **Boundary:** 실제 프로젝트 빌드·사람 플레이테스트·접근성·성능·전이 성공률은 아직 검증하지 않았다. 특정 게임의 수치, 성장 내용, Scene, UI, 튜토리얼 대사와 순서는 Base 공용 규칙으로 승격하지 않는다.
- **다음 검토 트리거:** 둘 이상의 실제 프로젝트에서 독립 수행·전이·복귀 경로가 관찰될 때, 강제 패배나 가짜 성장 경계가 지나치게 넓거나 좁을 때, 또는 공용 Contract가 프로젝트별 실제 의사결정을 막을 때.

## 2026-08-02 — First-prompt 방향 고정과 intake 승인 게이트

- **상태:** `OBSERVATION`
- **호출 트리거:** 프롬프트 전체 방향에 큰 영향을 주는 핵심 문장을 가장 앞에 배치하고, 모든 지시문을 intake Skill의 좋은 프롬프트 변환과 Grill Me 확인 뒤 실행하라는 사용자 결정.
- **Finding:** 기존 `Interface-first Prompt`는 입력·출력·권위·검증을 정의했지만, 핵심 방향 문장의 초두 배치와 지시문 작성 후 의도·기획 정합성 승인 게이트를 하나의 실행 흐름으로 고정하지 않았다. 또한 새 독립 테스트만 추가하면 현재 명시적 CI 목록에서 실행되지 않아 거짓 GREEN이 될 수 있었다.
- **Decision:** 새 광역 Skill을 만들지 않고 `managing-project-intake-and-work-contract`에 `first-prompt` Mode와 전용 reference를 추가한다. 모든 L1 이상 지시문 작성은 `route → first-prompt → contract → clarify/Grill Me alignment gate → CONFIRMED 또는 REUSED_APPROVAL → execution` 순서를 사용한다. Direction anchor는 핵심 행동·의도한 결과·지배 기준을 앞에 두지만 순서만으로 상위 권한이 되지 않는다. Task·Context·Source·Constraints·Output·Validation을 연결하고, 정석안·파격안·통합안은 실제 설계 탐색 가치가 있을 때만 같은 기준으로 비교한다.
- **Evidence:** Draft PR #143에서 먼저 standalone 회귀를 작성했으나 기존 Workflow가 이를 실행하지 않는 누락을 발견했다. 기존 `test_base_v9_4_ai_operations_contract.py`에 계약을 연결한 exact RED `be5be21a57442934d06df358b249be1c7a9a1240`에서 105개 중 새 reference 누락만 1 failure·1 error로 재현됐고, 구현 뒤 집중 v9 회귀는 통과했다. Canonical reference freshness가 Learning Log와 기존 통합 회귀 동기화를 추가로 요구해 소비자 누락을 차단했다.
- **Boundary:** 프롬프트 초두 배치가 모든 모델에서 품질을 높인다는 보장은 하지 않는다. 실제 모델별 방향 유지율, 재작업 감소, 사용자 이해도와 반복 질문 감소는 `NOT_RUN`이며, L0 오탈자·명백한 형식 수정·동일 검사 재실행은 인터뷰 예외다. 기존 exact contract의 유효한 approval reference가 있으면 중복 Grill Me 질문을 하지 않는다.
- **다음 검토 트리거:** 서로 다른 프로젝트와 모델에서 direction anchor 전후 결과를 비교할 때, Grill Me가 단순 작업을 과도하게 막을 때, 앞 문장이 뒤 제약을 왜곡할 때, 승인 재사용이 stale 계약을 통과시킬 때, 또는 새 테스트가 필수 CI에서 다시 누락될 때.

## 2026-08-01 — Repository governance files are not repository-setting evidence

- **Trigger:** the public Base repository had reusable operating materials and dependency-review CI but no License, Security policy, CODEOWNERS, or Dependabot configuration.
- **Finding:** adding placeholder community files could falsely imply reuse permission, a private contact channel, valid team ownership, or enabled security settings. A Dependabot file disconnected from actual manifests could also be accepted while monitoring the wrong surface.
- **Decision:** use one MIT license for Base-owned material, support only current `main`, route sensitive reports to GitHub private reporting without claiming it is enabled, derive CODEOWNERS from the mutable current repository governance profile, and enable only currently documented Dependabot combinations. Frozen release locks remain historical identities. `pip` and `github-actions` are active; pnpm 11 is visibly deferred because GitHub currently documents pnpm v7-v10.
- **Evidence:** repository inventory, public visibility and owner write/admin metadata, official GitHub file-location and ecosystem/version contracts, plus semantic RED/GREEN tests for unique precedence locations, mutable current identity, scope, manifest mapping, supported-versus-deferred updates, grouping, and docs-only as well as contract CI consumption.
- **Boundary:** license selection is not legal advice. Private reporting availability, CODEOWNERS review requests, Ruleset enforcement, Dependabot parsing, and its first scheduled update remain `UNVERIFIED_REPOSITORY_SETTING` or `NOT_RUN` until GitHub supplies direct evidence.
- **Next trigger:** repository rename/transfer, new package ecosystem or manifest directory, license exception, maintainer/team change, private-reporting setting verification, or first Dependabot PR.

## 2026-08-01 — Entrypoint ownership before size reduction

- **Trigger:** `AGENTS.md` and `START_HERE.md` repeated lifecycle, publication, review, legacy, and completion procedures already owned by the operating model, routing contract, and Skill packages.
- **Finding:** shortening both files independently would preserve mixed ownership and allow drift. A numerical line or character gate could also reward deleting necessary exceptions instead of delegating them.
- **Decision:** keep `AGENTS.md` as the always-on invariant layer and `START_HERE.md` as the request-by-request one-step router. Delegate conditional detail to `docs/OPERATING_MODEL.md`, `docs/WORK_MODE_AND_SKILL_ROUTING.md`, `docs/DOCUMENTATION_MAP.md`, the Registry-derived view, and selected Skill packages.
- **Benchmark:** OpenAI's Codex guidance says durable `AGENTS.md` guidance should stay small and supports linked/layered instructions; OpenAI Skills and GitHub path-specific instructions use progressive disclosure. These sources inform presentation only and do not override Base authority.
- **Evidence:** semantic RED tests reproduced the mixed-role contract and duplicate publication/review detail; the compact entrypoints then passed focused cold-start, consolidated-Skill, UI, difficulty/AI, Vertical Slice, and GDD Sheet regressions. The first canonical local-validation run also proved that the active `origin/main` example violated the checker's exact-commit boundary, so active examples and a regression now require a 40-character trusted main SHA. Independent review then caught a deleted direct-approval exception, a template route that bypassed its owning Skill, and missing archive/plugin/model-cost high-risk routes; Registry-trigger-derived regressions now preserve those boundaries. Re-review found that the game-system table was corrected while the top banner still bypassed the owner, so the regression now enumerates every first-hop representation of that route instead of sampling one table row.
- **Boundary:** this is structural and automated evidence. Live model behavior, project installation, project runtime, Google Sheets, accessibility, performance, and human comprehension remain `NOT_RUN` until separately exercised.
- **Next trigger:** if a new policy adds detailed procedure to either entrypoint, require an explicit reason it is always-on or one-step routing; otherwise link its canonical owner and extend semantic discovery tests.

## 2026-07-31 — Canonical-bound intermediate visual checkpoint

- Status: `PATTERN`.
- Decision: extend the existing art-prompt Skill instead of creating a Figma-, Whimsical-, or checkpoint-only duplicate Skill. Trigger the checkpoint from a mid-review request or P1 interpretation risk and use only the current project canon.
- Boundary: require one Screen Brief and a Screen Interpretation Review; output remains `DRAFT_VISUAL` or a text/Mermaid/Figma fallback. It is never an automatic canon change, final asset, license approval, implementation handoff, or runtime/human evidence.
- Verification trigger: Registry tags, the shared v9 contract, visual-workspace policy, project application template, and v9 contract tests must remain connected.

## 2026-07-30 — Verified agent merge execution

- Status: `PATTERN`.
- Decision: a non-Draft PR at its reviewed SHA must be merged by the responsible agent after required checks, independent review, unresolved-thread, and decision gates pass. A separate user click is not a normal merge gate.
- Boundary: `USER_REVIEW_REQUIRED` and `CHANGE_PROPOSAL` remain pre-implementation decision gates; P0/P1 findings, failed or missing checks, unresolved threads, conflicts, or unsupported merge methods block execution.
- Verification trigger: the policy, implementation handoff Skill, active prompt, Registry, learning log, and contract tests must change together. Repository auto-merge availability may vary, so direct merge is used only when its allowed method and every gate are confirmed.

## 2026-07-30 — External authority for protected baselines

- Status: `PATTERN`.
- Decision: a mutable project adapter cannot attest its own comparison base. Record an authority kind/ref and require its resolved commit to equal the adapter commit.
- Local boundary: resolve an explicit remote-tracking ref; do not infer the baseline from `HEAD`.
- Pull-request boundary: pass the event base SHA as trusted caller input and require equality; this is not cryptographic attestation.
- Verification trigger: missing refs, mismatched CLI values, or a protected product change combined with a feature-branch adapter baseline update must fail closed.

## 2026-07-30 — Base project router baseline hardening

- 상태: `PATTERN`
- 결정: 프로젝트 라우터는 스냅샷을 읽기 전에 표준 `--check`를 실행하며, 첫 마이그레이션에서는 commit-qualified legacy 정책 소스, 후속 wave에서는 canonical adapter 정책 소스를 사용한다.
- 실패 조건: adapter와 CLI 양쪽에 기준선이 없거나, 기준선 이후 보호 경로가 변경되었으면 route 실행을 중단한다.
- 검증: 기준선 없는 검사, `project.godot` 변경, 마이그레이터 기준선 누락을 실행형 임시 Git 저장소 테스트로 확인한다.

## 2026-07-30 — Base v9.1 review remediation

- Replaced string-only pressure evidence with four executable temporary-repository fixtures.
- Historical Base Registry authority now comes from the pinned Git blob; current Registry evolution is separate.
- Added ACTIVE-only route/alias resolution, evidence-derived health verdicts, protected/path fail-closed rules, and source-backed compatibility projections.
- Declared near-duplicate Skill similarity below normalized hash equality as a manual-review gap.

## 2026-07-30 Base v9.1: fail-closed project routing

- **Trigger:** pressure scenarios encouraged body copying, stale-pin execution, shared-route shadowing, and mismatch ignoring.
- **Finding:** route prose without machine validation allowed deadline, sunk cost, and authority pressure to bypass ownership.
- **Decision:** one canonical adapter drives deterministic views; project-local routes win; shared bodies remain in Base; every pin/hash mismatch refuses execution.
- **Evidence:** four recorded `BASELINE_FAIL` scenarios, four `GUIDED_PASS` decisions, focused Skill tests, and cross-repository validator tests.
- **Boundary:** no project runtime, device, accessibility, human, or product-code validation was performed.

## 2026-07-30 Base v9: generated authority instead of fixed Skill count

- **Trigger:** Base needed a final release operating contract without treating
  the current active Skill count as an architecture target.
- **Finding:** Human-maintained count summaries can drift from the Registry and
  hide whether a Skill has a complete routing and verification boundary.
- **Decision:** Keep the Registry and Skill frontmatter authoritative; generate
  the plugin manifest, Base lock, active-Skill view, and snapshot from them.
  Re-evaluate open Skill proposals through the migration map instead of merging
  their file sets directly.
- **Evidence:** Focused v9 RED→GREEN tests, deterministic second-generator run,
  Base v9 integrity check, existing skill coverage check, and full local suite.
- **Boundary:** No project repository or Google Sheet was read or written. Project
  adoption is a `POST_RELEASE_PROJECT_ADOPTION_WAVE` and does not block Base v9.0.0.
- **Learning state:** `PATTERN` for Base governance; project-level outcomes remain
  `UNVERIFIED` until separately authorized adoption work produces evidence.
- **Next trigger:** Re-run the migration and responsibility-boundary review when a
  project adoption supplies new evidence or a proposed Skill has a distinct
  input/output/authority/verification boundary.

## 2026-07-29 — UX/UI 폴리싱 패스와 Registry 전파 교훈

- **Trigger:** UI 폴리싱 실무 방법을 외부 공식 근거와 함께 조사해 Base Skill·작업 구조에 반영하라는 요청.
- **Finding:** 2026-07-29 PR #57에서 `auditing-and-refining-ui-art`가 UX/UI 설계까지 확장됐지만 기계 권한인 `skills/SKILL_REGISTRY.json`은 구현 후 감사 중심의 이전 trigger와 설명을 유지했다. UX/UI 전용 coupled-change rule도 Registry·Learning Log 동기화를 요구하지 않아 consumer drift를 차단하지 못했다.
- **Decision:** **새 Skill을 추가하지 않음**. 기존 Skill에 `polishing-pass`를 추가하고 `ui-polishing-method.md`, 프로젝트 Template, Review Checklist, Godot 중단·재진입·반복 사용 계약을 연결한다. Skill 변경 시 Registry·Learning Log·전용 Test·CI·상위 라우터를 함께 갱신하도록 coupled-change를 강화한다.
- **Evidence:** TDD RED에서 새 Reference·Mode·Template·Registry·라우터 누락이 실제 실패했고 기존 A~E 감사 회귀는 통과했다. W3C·Xbox·Apple·Godot·Material·Nielsen 원칙은 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 사용하며 프로젝트 정본을 대체하지 않는다.
- **Boundary:** 실제 모션 시간·색·간격·폰트·사운드·햅틱, Scene·script·asset 경로, 렌더·기기·플레이어 결과는 프로젝트에 유지한다. Base 문서 반영은 런타임·사람 검증 완료가 아니다.
- **Learning state:** 공용 구조와 drift 방지 계약은 `PATTERN` 후보이며, 여러 프로젝트에서 이해 시간·오입력·반복 피로·재작업 감소를 확인하기 전 실제 효과는 `OBSERVATION`이다.
- **Next trigger:** 서로 다른 두 프로젝트 이상에서 `polishing-pass`와 전후 Artifact를 사용하고 P0~P3 finding·입력 오류·피로·성능·사람 이해 결과를 비교할 때 재검토한다.
## 2026-07-29 — 난이도·전투 AI 설계 책임 통합

- **Trigger:** 적 AI를 영리하면서도 사용자 수준에 맞게 균형을 유지하고 아슬아슬한 긴장감을 만들 수 있도록 게임 설계·난이도 설계 Skill과 작업 구조로 공용화하라는 요청.
- **Finding:** 기존 `analyzing-and-refining-game-concepts`가 플레이어 경험·게임 요소 정렬·벤치마크·플레이테스트·PoC를 이미 책임한다. 별도 난이도·전투 AI Skill을 만들면 주 책임 분야와 Evidence·검증 절차가 중복된다.
- **Decision:** **새 Skill을 추가하지 않음**. 기존 Skill에 `system-design`과 `difficulty-and-combat-ai` Mode를 추가하고, 개별 적 판단·전투 조율자·난이도/페이싱 디렉터, 공격·위협 예산, 공정성 안전 규칙, 고정·적응형 난이도, 텔레메트리·플레이테스트를 전용 reference와 Template로 분리한다.
- **Boundary:** 반응시간·예산·배율·적 역할·스테이지 규칙·Godot 구현 상태는 프로젝트 전용 유지다. Base는 입력·판정·검증·공용화 경계만 제공한다.
- **Learning state:** 구조와 계약은 `HYPOTHESIS`이며 **프로젝트 Pilot 검증 대기**다.
- **Promotion guard:** 한 프로젝트나 한 번의 성공을 공용 강제 규칙으로 승격하지 않음. 실제 문구는 **한 번의 성공을 공용 강제 규칙으로 승격하지 않음**이며, 서로 다른 프로젝트에서 공정성·긴장도·오라우팅·밸런스 조정 비용을 비교한 뒤 재검토한다.
- **Next trigger:** 모바일 실시간 전투와 PC 전술·액션 프로젝트에서 각각 적용해 사망 원인 설명 가능성, 피해 폭증, 동시 공격, 플레이어 자기보고, 조정 비용을 비교할 때 재검토한다.

## 2026-07-29 — 프로젝트 Google Sheets의 시각형 GDD 역할

- **Trigger:** 각 프로젝트 Google Sheets를 사용자의 전체 흐름 확인·정보 갱신 확인·직접 수정용 GDD로 사용하고, AI도 GitHub와 함께 방향성·메인 시스템을 참조하라는 요청.
- **Finding:** Sheet를 단순 운영 mirror로만 두면 사용자 편집의 의미가 약하고, 반대로 Sheet를 단일 정본으로 승격하면 GitHub 상세 정본·실제 구현과 충돌한다. 기존 Intake·운영체계·문서 Skill이 이미 Sheet 비교·동기화를 책임지므로 새 광역 Skill은 중복이다.
- **Decision:** **새 Skill을 추가하지 않음**. Sheet를 `USER_FACING_GDD_WORKSPACE`로 정의하고, 사용자 편집은 `PROPOSED_SHEET_CHANGE`로 보존한 뒤 GitHub 정본·실제 구현과 비교한다. 시각화 우선·지속 갱신·단위·초기 시험값·조정 범위·검증 상태를 공용 계약으로 추가한다.
- **Boundary:** GitHub 등록 정본과 실제 파일의 권한을 유지한다. HTML 대시보드는 사용자 명시 요청 또는 기존 유지보수에만 선택적으로 사용한다.
- **Learning state:** 정책·Template·회귀 계약은 `PATTERN` 후보이며, 여러 프로젝트에서 사용자 수정 누락 감소·AI 방향 복원·운영 비용을 확인하기 전까지 실제 효과는 `OBSERVATION`이다.
- **Next trigger:** 서로 다른 두 프로젝트 이상에서 Sheet 편집→승인→GitHub 정본→Sheet 재동기화 흐름과 시각 GDD 사용성을 검증할 때 재검토한다.

## 2026-07-29 — 근거 기반 게임 개발 지식체계

- **Trigger:** 게임 기획·아트 기획뿐 아니라 Godot 개발·AI 활용·벤치마킹·유저리서치·접근성·프로덕션·출시 전반을 공식·현업·개발자·플레이어 근거로 개선하고 Base main에 통합하라는 요청.
- **Finding:** 기존 Base에는 컨셉 분석·GUR 11영역·아트 프롬프트·Vertical Slice·AI 결과 검증·적대적 검토·Skill 진화가 이미 존재하므로 새 광역 Skill을 추가하면 책임이 중복된다. 또한 새 테스트 파일을 만들었지만 기존 CI의 명시적 테스트 목록에 연결되지 않아 첫 실행에서 검증되지 않는 소비처 누락을 확인했다.
- **Decision:** **새 Skill을 추가하지 않음**. 기존 Skill이 실행 권한을 유지하고, `docs/knowledge/game-development/`에 Method·Guide·Reference를, `templates/research/`에 Evidence Pack·Case Card를 추가해 조건부로 소비한다. 성공·실패·혼합 사례와 공식 사실·현업 경험·플레이어 행동·자기보고·AI 추론을 분리한다.
- **Evidence:** TDD RED Workflow에서 지식 패키지 미생성으로 계약 테스트 실패를 확인하고, README·Documentation Map·기획 근거 정책·전용 CI까지 소비 경로를 연결해 GREEN으로 전환한다. 외부 자료는 공식·학술·현업 원출처와 확인일·버전·사용 한계·재검증 조건을 기록한다.
- **Learning state:** 구조와 계약은 `PATTERN` 후보지만, 다섯 게임 프로젝트에서 실제 결과물 품질·오라우팅·조사 비용·검증 효과를 측정하지 않았으므로 **프로젝트 Pilot 검증 대기**다.
- **Promotion guard:** 한 번의 Base 문서 통합 성공이나 외부 사례만으로 **반복 검증 전 공용 강제 규칙으로 승격하지 않음**. 프로젝트별 세계관·수치·경로·승인 자산·실제 플레이테스트 결과는 프로젝트에 유지한다.
- **Next trigger:** 십보강호·Blacksmith·OMENWARD·괴이기록국·GRIMOIRE 중 서로 다른 두 프로젝트 이상에서 Evidence Pack·Case Card·Guide를 사용하고, 기획 품질·누락 감소·토큰/조사 비용·플레이테스트 연결 결과를 비교할 때 재검토한다.

## 2026-07-28 — 통합 실행문과 저장소 전체 감사

- **Trigger:** v6 상세 참고 계약과 축약 실행문을 한 파일로 통합하고, 전체 파일에서 누락·구형 계약·untouched 소비자를 검수해야 했다.
- **Finding:** 새 광역 Skill을 추가하면 기존 적대적 검토·reference freshness·legacy governance와 책임이 중복된다. 또한 활성 Vertical Slice 오케스트레이션에는 별도 `CORE_POC` 흐름이 남았고 관련 계약 테스트는 CI에서 직접 소비되지 않았다.
- **Decision:** `running-adversarial-review-and-refinement`에 `repository-wide-audit` mode와 전문 Reference를 추가하고, 상세 정본과 인터뷰를 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` 한 파일로 통합했다.
- **Evidence:** Registry trigger, Migration Traceability, entrypoint, reference-freshness coupled rule, Demo-First·v6·v7 contract tests로 전파를 검증한다.
- **Next trigger:** Prompt·Gate·Skill·Template 변경 뒤 활성 구형 용어 또는 untouched 소비자가 발견될 때 재감사한다.

## 2026-07-28 내용 보존·근거 묶음·Demo-First 기획 순서 교훈

- 문서·Skill의 줄 수나 분량을 품질 Gate로 사용하면 실행 계약·예외·검증 조건을 삭제해 테스트만 통과하는 회귀를 만들 수 있다. 수치형 컴팩트 제한 대신 내용 보존·책임 분리·한 단계 발견성을 검증한다.
- 작업 시작 전에 이전 Decision·정본·PR·실제 구현을 비교하지 않으면 같은 질문·작업을 반복하고 승인 누락과 소비처 미반영을 뒤늦게 발견한다.
- 새 정책·Template·Skill은 생성 여부가 아니라 README·START_HERE·운영 정본·Registry·프로젝트 설치·분야 소비자·Test에서 실제 소비되는지 확인해야 한다.
- 중요한 기획은 벤치마킹·플레이어 반응·현업 또는 공식 권장의 세 층 근거를 Approval Bundle에 연결한다.
- 사용자의 프로젝트 운영은 별도 Core PoC 마일스톤을 생략하고 제작 의도 자산을 사용하는 완성 품질 Vertical Slice 데모와 플레이테스트로 직접 검증한다. 기술 Spike는 Slice 내부의 제한된 위험 검증으로만 둔다.
- Base 자체는 프로젝트 Google Sheets 범위에서 제외하고 개별 프로젝트만 구성된 Sheet에 동기화한다.
- 현재 지식 상태: 사용자 승인과 Base 정본·회귀 검증으로 승격할 `PATTERN`.

## 2026-07-28 병합 후 결정 복원 진입점 누락 교훈

- 승인 결정 동기화 정책과 템플릿만 추가해도 프로젝트 기본 읽기 순서와 운영체계 `install/audit/verify`가 이를 명시적으로 소비하지 않으면 새 채팅·신규 설치에서 복원 정본을 건너뛸 수 있다.
- `CURRENT_CONFIRMED_DECISIONS.md`, 동일 Goal의 열린·최근 병합 PR, 분야 정본, GitHub `main`, 프로젝트 Google Sheets를 Intake와 운영체계 Skill의 Required inputs·Read order·설치·감사·검증 계약에 모두 연결한다.
- 병합 후 적대적 검토는 새 파일의 존재가 아니라 실제 소비 진입점과 콜드 스타트 경로까지 검사해야 한다.
- 현재 지식 상태: Base 회귀 검사와 병합 후 정본 대조로 확인한 `PATTERN`.

## 2026-07-28 승인 즉시 정본화·중복 질문 방지·병합 후 검토 교훈

- 장시간 기획·Grill Me에서 사용자 승인을 댓글이나 하위 시스템 checkpoint까지 누적하면 최근 결정이 분야 정본·현재 상태·Google Sheets에 승격되지 않는 운영 실패가 발생한다.
- 질문 전에 최신 main, 동일 Goal의 열린·최근 병합 PR, `CURRENT_CONFIRMED_DECISIONS.md`, 분야 책임 원본, 실제 구현과 Google Sheets를 대조하고 이미 답한 질문은 다시 묻지 않는다.
- 프로젝트 방향을 바꾸지 않는 기술 세부와 초기 수치는 `RECOMMENDED_DEFAULT`로 처리하고, 코어·중요 기획·방향성·정본 충돌만 `USER_DECISION_REQUIRED`로 올린다.
- 승인 답변은 GitHub 추적 근거 → 현재 확정 결정 → 분야 정본 → 허용된 main 문서 Commit → Google Sheets → 양쪽 재조회까지 같은 승인 단위에서 완료하고 `SYNCED`를 증명한다.
- 모든 병합 뒤 새 main과 실제 diff를 다시 읽어 최근 승인 누락, 이전 Decision 부활, 정본·Sheets 불일치, 중복 PR과 회귀를 적대적으로 검토한다.
- 현재 지식 상태: 사용자 승인과 Base 정책 통합은 `PATTERN`, 여러 프로젝트에서의 실제 누락 감소 효과는 후속 관찰 전까지 `OBSERVATION`.

## 2026-07-25 승인 기획 결정 지속 기록·하위 시스템 통합 교훈

- 십보강호 기획에서 승인 결정이 대화·PR 댓글에 누적되면 책임 원본·상태·Context와 drift가 생길 수 있음을 확인했다.
- 승인·수정 직후 GitHub 추적 근거를 남기고, 전투·성장·경제·진행·콘텐츠 등 하위 시스템 완료 checkpoint에서 책임 원본으로 통합한다.
- GitHub 댓글·Issue·PR·Discussion은 추적 근거이며 책임 원본의 대체물이 아니다. 최신 승인안의 대체 범위, 공식, 예시, 예외, 미결정, 검증 상태를 함께 보존한다.
- checkpoint에서는 누락·충돌·중복·대체 누락·참조 drift를 검사하고, 실행하지 않은 검수·플레이테스트·CI는 `UNVERIFIED`를 유지한다.
- 출처: `Ten-Paces-Hidden-Moves` PR #42 승인 기록 `5078806296`; Base 적용 PR #41.
- 현재 지식 상태: 프로젝트 적용과 사용자 승인은 `PATTERN`, 여러 프로젝트에서의 누락 감소 효과는 후속 관찰 전까지 `OBSERVATION`.

## 2026-07-24 GPT–Codex 역할 분리·Grill Me·비용 최적화 CI 교훈

- Grill Me는 요구 확인과 승인 상태를 다시 만드는 독립 Skill이 아니라 `managing-project-intake-and-work-contract`의 `clarify` Mode에 통합하는 편이 중복 질문과 상태 충돌을 줄인다.
- GPT는 기획·벤치마킹·시스템·데이터·UX·비-Godot 파일·GitHub 계약과 검수를 완료하고, Codex Plan은 최신 Godot 저장소를 읽기 전용으로 재검수하며, Codex Build는 지정 Branch의 Godot 구현만 담당하도록 의사결정 권한과 파일 권한을 분리했다.
- 동일한 플레이어 결과와 데이터 계약을 유지하는 구조·성능·안정성·테스트 개선은 기술 변경으로 허용하되 프로젝트 코어·Core Loop·플레이 규칙·MVP·주요 UX·저장 호환성 변경은 `CHANGE_PROPOSAL`로 구현과 분리한다.
- 전체 설계는 마스터 구현계획 하나로 유지하고 실제 구현은 검증 가능한 패키지, 상위 Issue, 패키지별 Branch·PR, 순차 진행, 영향도 기반 승인 게이트로 나누는 것이 회귀·롤백·중단 후 재개에 유리하다.
- GitHub Actions 첫 실제 실행에서 `actions/setup-node`의 `cache: pnpm`이 Corepack 활성화 전에 pnpm을 요구해 Ubuntu·Windows 발행 Job이 모두 실패했다. 패키지 관리자 캐시는 해당 실행 파일의 준비 순서를 보장한 뒤에만 활성화해야 한다.
- 같은 실행에서 Skill 본문만 바꾸고 Registry·Learning Log·집중 회귀 테스트를 함께 갱신하지 않은 coupled-change 누락이 정본 최신성 검사에 의해 차단됐다. Skill 계약 변경은 본문·Registry·학습·검증을 하나의 변경 단위로 취급한다.
- 현재 지식 상태: 역할 경계와 승인 정책은 사용자 승인된 `PATTERN`, 실제 여러 게임 프로젝트의 단계별 Codex 인계 효과는 `OBSERVATION`, 변경 위험별 CI 비용 절감 효과는 후속 실행량 데이터 전까지 `HYPOTHESIS`.

## 2026-07-22 원문 책임 전수 매핑·Skill 구조 최적화

- 1,201줄 학습 텍스트의 책임을 `skills/SKILL_COVERAGE.json`에 전수 매핑했다.
- 가지치기·본문 간소화·행동 보존 리팩토링은 입력·산출물·삭제 권한·검증이 달라 독립 Skill로 분리했다.
- 동기화·장기 작업 연속성·Games User Research 11영역·학습 노트·시각 대시보드·엔진 디버깅도 기존 Skill로 흡수할 수 없는 독립 계약으로 판정했다.
- 요청 명세화·Issue/Goal·MVP·벤치마킹·문서 기억·검증은 기존 Skill에 이미 기능이 있어 중복 신설하지 않았다.
- 코어 판정·코어 확정·적대적 검토·컨셉 분석·Skill 진화 본문을 compact router로 리팩토링하고 상세 판정표를 reference로 이동했다.
- 전용 checker와 PR 회귀 테스트로 coverage, Registry, front matter, 파일 존재, 본문 최소 계약과 compact line budget을 검증한다.
- 현재 지식 상태: 실제 Base 적용은 `OBSERVATION`, 여러 프로젝트 반복 전까지 새 Skill 계약은 `HYPOTHESIS`.
## 2026-07-21 프로젝트 코어·적대적 검토 Skill 분리 교훈

- 프로젝트 코어 판정은 기존 프로젝트의 승인 원본·실제 구현·의존 관계를 읽기 전용으로 대조하는 작업이며, 새 프로젝트의 코어를 제안·확정하는 기획 권한과 분리한다.
- `identifying-project-core`는 기획·시스템·코드 코어와 코어 기능·MVP 지원 기능을 제거·대체 테스트로 구분한다.
- `establishing-project-core`는 PLAN Work Mode에서 불변 조건과 변경 가능한 외피를 제안하고, 반례 검토 뒤 사용자의 명시적 승인만 `CORE_CONFIRMED`로 인정한다.
- 적대적 검토는 레드팀 공격, 비판 검증, 승인된 finding의 최소 개선, 회귀 재검토를 분리한다. 비판도 취향·과잉 요구·잘못된 전제일 수 있으므로 그대로 반영하지 않는다.
- 세 Skill은 읽기 권한, 승인 경계, 산출물이 달라 독립 Skill로 유지하되 실제 여러 프로젝트에서 오라우팅·코어 과대 판정·비판 과수용을 검증하기 전까지 지식 상태는 `OBSERVATION` 또는 `HYPOTHESIS`로 둔다.


## 2026-07-21 Work Mode·자동 Skill 라우팅·구형본 정리 교훈

- `Mode`라는 단어를 세션 전체 작업 방식과 Skill 내부 절차에 함께 쓰면 라우팅 순서가 모호해진다. Base에서는 전자를 `Work Mode`, 후자를 `Skill Mode`로 구분한다.
- 요청 처리 순서는 `Prompt 의도·현재 단계 파악 → PLAN/BUILD/REVIEW Work Mode 선택 → Registry trigger 기반 Skill 자동 선택 → Skill Mode 선택 → 실행·검증 → 사용 이유·결과·증거 보고`가 기본이다.
- 사용자는 Skill 이름이나 Skill Mode를 선언할 필요가 없다. `load_by_default=false`는 자동 사용 금지가 아니라 trigger가 없을 때 불필요하게 로드하지 않는다는 뜻이다.
- `PLAN`은 읽기·조사·계약, `BUILD`는 승인 범위 구현, `REVIEW`는 적대적 검토·반례·증거를 기본 권한으로 둔다. 검토 중 수정이 필요하면 `REVIEW → BUILD → REVIEW`로 전환한다.
- Skill 자동 사용은 숨겨진 절차가 되어서는 안 된다. L1 이상 작업은 실제 사용한 Work Mode·Skill·Skill Mode, 선택 이유, 수행 내용, 얻은 결과, 증거와 미검증을 보고한다.
- 구형 파일 정리는 단순 삭제가 아니다. `CURRENT / UPDATE_IN_PLACE / MERGE_TO_CANONICAL / COMPATIBILITY_STUB / ARCHIVE_HISTORY / DELETE_APPROVED / KEEP_UNRESOLVED`로 판정하고 고유 정보·활성 참조·파생본·복구·승인을 확인한다.
- 구형본 탐지·정리·마이그레이션은 같은 책임 원본과 삭제 권한을 공유하므로 신규 독립 Skill보다 `managing-game-project-operating-system: reconcile-legacy` Skill Mode로 통합하는 편이 중복과 오삭제를 줄인다.
- 자동 라우팅과 구형본 정리 계약은 구조 회귀로 검증하되, 실제 서로 다른 프로젝트에서 오라우팅·과도한 보고·호환 stub 누락·오삭제 빈도를 확인하기 전까지 지식 상태는 `OBSERVATION` 또는 `HYPOTHESIS`로 유지한다.

## 2026-07-21 DDD 빠른 보상 설계 교훈

- 이 Base의 게임 기획 맥락에서 `DDD`는 `Digital Dopamine Design`이다. 플레이 시작 또는 행동 직후 짧은 시간 안에 의미 있는 보상·변화·성취와 다음 기대를 체감시키는 빠른 보상 설계축을 뜻한다.
- DDD는 실제 도파민 분비량을 측정하거나 의학적 중독을 진단하는 표현이 아니다. `첫 의미 있는 보상까지의 시간`, `행동-피드백 지연`, `보상 명료성`, `보상 밀도`, `micro-session-meta 보상 사다리`, `다음 행동 유도`, `피로·인플레이션`을 관찰한다.
- 빠른 보상은 뾰족한 재미를 더 빨리 이해시키는 수단이어야 한다. 의미 있는 선택 없이 이펙트·팝업·숫자·알림만 반복하면 핵심 재미를 자극으로 대체한 실패다.
- 빠른 보상을 설계할 때 가치·확률·비용 은폐, 인위적인 불편 뒤 결제 해소, 손실 압박, 중단을 방해하는 연속 알림 같은 위험을 별도 표시한다.
- Base 내부 DDD 정의는 확정했지만, 외부 자료나 다른 프로젝트에서 같은 약어를 사용할 때는 해당 출처의 정의를 확인하기 전 임의 해석하지 않는다.

## 2026-07-21 외부 근거·작업 순서·플레이 검증 교훈

- 벤치마크는 인기 게임의 기능 목록을 모방하는 절차가 아니다. 현재 결정을 바꿀 질문과 비교 차원을 먼저 고정하고, 공식 제품 사실·플레이어 자기보고·행동 이벤트·퍼널·통제 실험·해석을 서로 다른 근거 층위로 관리한다.
- 플레이어 리뷰는 기대가 어떻게 설정되고 실제 경험과 어디서 어긋나는지 찾는 채널이지만, 버전·패치·플레이타임·플랫폼·언어·긍정·부정·리뷰 폭탄을 구분하지 않으면 현재 기획을 정당화하는 선택 편향이 된다.
- 외부 조사 결과는 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 변환해야 하며, 평점·판매량·강한 표현만으로 핵심 컨셉을 변경하지 않는다.
- 작업 분해는 “코딩”, “문서 수정” 같은 활동 목록이 아니라 독립 검증 가능한 결과, `BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES` 의존성, 병렬 경계, 단계별 게이트·롤백으로 표현한다.
- 실행 순서는 의존성 해소, 가장 위험한 가설, 핵심 사용자 가치, 피드백 속도, 되돌리기 난이도와 자원 충돌을 함께 고려하고 새 사실·실패가 생기면 이후 계획을 재구성한다.
- 플레이테스트는 빌드·버전·대상 집단·기존 노출·과제·피드백 채널·관찰 행동·이벤트·퍼널·성공 기준이 있는 검증 계약이어야 한다. A/B 테스트는 한 주요 가설과 사전 선언한 주 지표·가드레일을 비교한다.
- 접근성은 옵션 존재나 법적 준수 선언이 아니라 핵심 정보·입력·UI·시간·난이도·모션에서 실제 장벽과 대체 경로를 검수한다.
- 성능은 평균 FPS 하나가 아니라 목표 플랫폼·동일 빌드·대표·최악 장면에서 frame time, CPU·GPU·메모리·네트워크·로딩을 baseline과 비교한다.
- 위 기능은 별도 Skill을 늘리지 않고 `decompose-and-sequence`, `benchmark-and-player-research`, `playtest-and-experiment`, `accessibility-review`, `performance-profile` mode로 기존 생명주기에 흡수한다. 활성 Skill 수는 13개를 유지한다.
- 공식 자료를 근거로 계약을 만들었지만 여러 실제 프로젝트에서 오라우팅·표본 편향·측정 비용을 검증하기 전까지 신규 mode의 지식 상태는 `OBSERVATION` 또는 `HYPOTHESIS`로 유지한다.

## 2026-07-21 정본·참조 최신성 감사 교훈

- 패치 검수는 변경된 파일만 보는 것으로 충분하지 않다. 정본이 바뀌면 **변경됐어야 하지만 untouched인 소비자·템플릿·테스트·Workflow·파생본**을 함께 찾아야 한다.
- 오래된 경로·Skill ID·문서 ID와 실제 실행 참조는 차단하되, Legacy Alias·Change Log·과거 case·Git 이력의 역사 참조는 별도 허용 상태로 구분해야 한다.
- 문자열이 최신이어도 여러 활성 문서가 서로 다른 mode·정책·상태·완료 기준을 설명하면 content drift다. 자동 검색과 책임 원본 기반 수동 검토를 함께 사용한다.
- 정본 변경 전파 검사는 범용 변경 검증의 `reference-freshness` mode에서 오케스트레이션하고, 영향 지도·오래된 참조·파생본 최신성은 독립 전문 Skill이 담당하는 구조가 중복을 줄인다.
- 자동 검사 규칙은 Legacy ID 잔존, 필수 정본 링크, coupled-change 누락을 담당하고 PDF·Manifest·해시·실제 렌더는 분야별 발행·운영체계 검증과 연결한다.
- 신규 전문 Skill은 실제 여러 프로젝트에서 오탐·누락률을 확인하기 전까지 `OBSERVATION`으로 유지한다.

## 2026-07-21 핵심 컨셉·변경 검증 스킬 교훈

- 게임 기획 방향을 잡는 작업은 GDD 문장 작성이나 Vertical Slice 제작과 다르다. 핵심 컨셉·제약·뾰족한 재미·요소 정렬·PoC·재조정을 하나의 상태 흐름으로 다뤄야 한다.
- SWOT은 장단점 목록이 아니라 SO·WO·ST·WT 실행 방향으로 변환해야 의사결정 도구가 된다.
- MDA·DDE·DDD·3C·루프 같은 프레임워크는 많이 적용하는 것이 목적이 아니라 핵심 재미와 불일치를 찾아 개선 우선순위를 만드는 데 사용한다.
- PoC는 전체 게임이나 Vertical Slice가 아니라 가장 위험한 가설을 최소 비용으로 틀릴 수 있게 만드는 검증 계약이다.
- 변경 검증은 외부 AI 결과에만 필요한 절차가 아니다. 사람·Codex·자동화가 만든 코드·데이터·문서·자산 모두 승인 계약, 실제 diff, 정적·런타임·회귀 증거로 같은 기준에서 검증한다.
- 외부 AI 검수는 범용 변경 검증 Skill의 `external-source-review` mode로 흡수하고, 이전 ID는 Legacy Alias로 보존한다.

## 2026-07-21 스킬·운영 구조 통합 교훈

- 하나의 요청 생명주기를 라우팅·인터뷰·실행 계약처럼 여러 Foundation Skill로 분리하면 같은 상태·범위·검증을 반복 판정하게 된다. 하나의 통합 Skill과 mode·상태 머신으로 우선 표현한다.
- 신규 설치·기존 감사·승인된 마이그레이션·Health Review처럼 같은 구조를 다른 권한으로 다루는 작업은 mode를 분리하고 기본 권한을 읽기 전용으로 둔다.
- 기획 내용 작성과 PDF 발행이 같은 Registry·원본·상태를 읽는 경우 하나의 문서 생명주기 Skill로 통합한다.
- Skill 통합 시 이전 ID를 즉시 소실시키지 않고 `LEGACY_SKILL_ALIASES.md`에서 새 Skill과 mode로 연결한다.
- Method·Checklist·START_HERE는 실행 절차를 반복하지 않고 `OPERATING_MODEL`과 실행 Skill을 연결하는 원칙·라우터로 축소한다.
- 모든 문서에 PDF를 강제하지 않고 `source_only`, `milestone_sync`, `always_sync` 발행 정책으로 비용과 검수 수준을 구분한다.

> Base 실행 Skill의 실제 적용 결과, 실패, 예외와 갱신 결정을 기록한다. 이 문서는 기본 작업 컨텍스트가 아니며 `skills/SKILL_REGISTRY.json`에서 특정 Skill의 학습 검토가 필요할 때만 읽는다.

## 2026-07-19 운영체계 감사에서 확인한 재사용 교훈

- 프로젝트 운영 문서의 최신성은 파일 존재 검사가 아니라 활성 참조와 설치 매핑을 함께 검사해야 한다.
- 발행본의 `CURRENT` 상태와 사람의 시각 검수 완료 상태는 서로 독립적으로 관리해야 한다.
- Learning Log는 모든 호출이 아니라 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있을 때 기록한다.
- 11개 분야는 공용 카탈로그이며 프로젝트가 선택하지 않은 분야를 필수 진입점으로 강제하지 않는다.
- 작업에 필요한 도구·파일·인증·권한이 없으면 사용자에게 이유와 설치·적용·확인 방법을 안내하고, 완료 통보 뒤 실제 환경을 다시 검증한다.

## 기록 원칙

- Skill을 호출했다는 이유만으로 본문을 매번 바꾸지 않는다.
- 실패, 중요한 결정, 재사용 가능한 교훈 또는 실제 검증 결과가 있는 실행을 기록한다.
- 반복 실패, 새 예외, 경로·도구·검증 변경이 발생하면 Skill 계약을 검토한다.
- 한 번의 성공은 `관찰` 또는 `가설`이다.
- 여러 조건에서 재현되기 전에는 `검증`이나 공용 강제 규칙으로 승격하지 않는다.
- 프로젝트 고유 이름·수치·파일 경로·승인 자산은 Base 로그에 복사하지 않는다.

## 2026-07-19 schema v3 발행 검증 교훈

- LibreOffice의 자동 TOC 필드는 headless PDF 변환에서 빈 목차가 될 수 있으므로 고정 섹션 목록을 직접 생성해야 한다.
- 구조화 JSON의 목록 항목은 상세 객체뿐 아니라 간단 문자열도 안전하게 렌더할 수 있어야 한다.
- Mermaid는 고정 CLI와 lockfile만으로 부족하며 브라우저 실행 경로도 사전 점검해야 한다.
- 강제 LibreOffice 재빌드의 플랫폼별 바이너리 동일성을 과장하지 않고, 동일 입력 정상 재실행 무재작성·diff 0을 공식 결정성 계약으로 둔다.
- 생성 실패를 대표 fixture에서 재현해 기존 PDF·Manifest 해시 보존을 확인해야 한다.

## 실행 기록 템플릿

```md
### [날짜] [skill_id]
- 프로젝트·작업:
- 기준 스킬 커밋:
- 호출 트리거:
- 입력 범위:
- 실제 산출물:
- 실행한 검증:
- 결과: 성공 / 부분 성공 / 실패 / 미검증
- 성공 조건:
- 실패·예외·재현 조건:
- 사용자 피드백:
- 불필요하게 호출한 스킬:
- 누락된 스킬·검증:
- 스킬 본문 변경 필요: 예 / 아니오
- 변경하지 않는 이유:
- 지식 상태: 관찰 / 가설 / 패턴 / 검증 / 승격 후보
- 프로젝트 전용으로 유지할 내용:
- Base Method·Skill·Template·Test 환류 후보:
- 다음 검토 트리거:
```

## 학습 상태 승격 기준

| 상태 | 최소 근거 | 허용 사용 |
|---|---|---|
| 관찰 | 1회 실행·피드백 | 참고만 가능 |
| 가설 | 원인·적용 조건·실패 조건 제시 | 제한적 시험 적용 |
| 패턴 | 서로 다른 작업에서 반복 | 프로젝트 권장 절차 |
| 검증 | 여러 조건에서 재현·회귀 검증 | Base 공용 계약 후보 |
| 승격 후보 | 프로젝트 독립성과 중복 검수 완료 | Method·Skill·Template·Test 반영 검토 |

## 정기 Health Review

다음 중 하나가 발생하면 `managing-game-project-operating-system`의 `verify` mode 또는 `evolving-project-discipline-skills`를 호출한다.

- 동일 실패가 두 번 이상 반복됨
- 90일 이상 검토 기록이 없음
- 등록된 Markdown 또는 JSON 책임 원본·실제 경로·검증 명령 변경
- 새 분야·반복 작업 유형 추가
- Skill 절차 중복
- 새 채팅이 필요한 Skill·기획서를 찾지 못함
- 과도한 Skill 호출
- PDF·다이어그램 발행본이 Registry보다 오래됨

## 기록

### 2026-07-21 project core and adversarial review skills

- 프로젝트·작업: 프로젝트 코어 판정, PLAN 단계 코어 확정, 적대적 검토·개선 루프를 독립 Skill로 추가
- 호출 트리거: 사용자가 사람도 이해하기 쉬운 컨텍스트를 Base Skill로 분리하고 기획 모드의 코어 확정 Skill을 추가하도록 요청
- 실제 산출물: `identifying-project-core`, `establishing-project-core`, `running-adversarial-review-and-refinement`, Registry·라우팅·회귀 동기화
- 실행한 검증: Registry Schema, Skill 패키지 1:1, 진입점 발견성, 구조 회귀, 정본 최신성 검사
- 결과: 부분 성공 — 공용 계약 추가, 실제 여러 프로젝트 적용은 미검증
- 성공 조건: 코어와 MVP를 구분하고, 사용자 승인 없이 코어를 확정하지 않으며, 레드팀 비판을 검증한 뒤 유효한 문제만 수정하고 회귀를 재검사함
- 실패·예외: 모든 중요 기능을 코어로 판정, 기술 부채를 불변 코어로 고정, 비판 전부 수용, 기능 팽창, 회귀 누락
- 지식 상태: 코어 판정은 관찰, 코어 확정과 적대적 개선 루프는 가설
- 다음 검토 트리거: 서로 다른 프로젝트 적용, 승인 없는 확정, 코어 과대 판정, 비판 과수용·기각 오류


### 2026-07-21 automatic Work Mode routing and legacy reconciliation

- 프로젝트·작업: Work Mode와 Skill Mode를 분리하고, 사용자 선언 없이 필요한 Skill을 자동 선택하며, 구형 파일을 안전하게 갱신·통합·아카이브·삭제하는 운영 계약 추가
- 기준 스킬 커밋: `agent/automatic-skill-routing-and-legacy-reconcile`
- 호출 트리거: Skill과 mode의 차이 확인, main 병합, 구형 파일 갱신·삭제 절차 확인, 별도 요청 없이 Skill 자동 사용과 사용 이유·결과 보고 요구
- 입력 범위: 통합 Skill Registry, 요청 접수 Skill, 운영체계 Skill, 정본 최신성 감사, 프로젝트 Registry 템플릿, 구조 회귀와 기존 Learning Log
- 실제 산출물: `PLAN/BUILD/REVIEW` Work Mode, Skill Mode 용어 계약, automatic-trigger-match 정책, `execution-report`, `reconcile-legacy`, Skill 실행 보고·구형 파일 정리 템플릿, Registry Schema와 구조 회귀
- 실행한 검증: Registry Schema·13개 활성 경로·Work Mode·자동 선택·구형 파일 판정·템플릿 존재 회귀를 추가했으며 GitHub Actions 전체 실행으로 최종 확인한다.
- 결과: 부분 성공 — 구조·계약·회귀 반영 완료, 실제 여러 프로젝트 적용은 미검증
- 성공 조건: 사용자가 Skill을 선언하지 않아도 최소 Skill·Skill Mode가 선택되고, 최종 보고에서 이유·결과·증거가 보이며, 구형 파일 삭제 전 고유 정보·참조·파생본·복구·승인이 확인됨
- 실패·예외·재현 조건: Work Mode와 Skill Mode 혼용, 모든 작업에서 과도한 Skill 보고, 파일명만 보고 구형본 삭제, 외부 호환 경로 제거, REVIEW에서 finding 없이 즉시 수정하는 위험
- 사용자 피드백: 의도 파악→해당 Mode→Skill 실행 구조가 최선인지 확인하고, Skill은 자동 사용되며 이유와 결과를 명시할 것
- 불필요하게 호출한 스킬: 신규 독립 구형 파일 정리 Skill은 만들지 않고 운영체계 Skill Mode로 통합함
- 누락된 스킬·검증: 실제 프로젝트의 버전 복제본·외부 링크·대형 바이너리·장기 호환성 사례
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 용어·라우팅 계약은 패턴 후보, 구형본 자동 판정은 관찰·가설
- 프로젝트 전용으로 유지할 내용: 실제 정본 경로, 삭제 승인자, 외부 소비자, 보존 기간, 호환 stub 정책
- Base Method·Skill·Template·Test 환류 후보: 이번 Work Mode 문서, 두 통합 Skill, Registry 정책, 두 템플릿과 구조 회귀
- 다음 검토 트리거: 첫 두 프로젝트 적용, 오라우팅, Skill 실행 보고 누락·과다, 오삭제, 호환 stub 누락, 사용자가 자동 선택 이유를 이해하지 못함

### 2026-07-21 benchmark, sequencing, playtest, accessibility and performance modes

- 프로젝트·작업: 게임 개발 벤치마크·유저 반응 조사, 작업 분해·순서, 플레이테스트·행동 계측, 접근성·성능 검증 공백을 기존 통합 Skill mode로 흡수
- 기준 스킬 커밋: `agent/add-reference-freshness-audit-v3`
- 호출 트리거: 벤치마킹 게임·유저 반응을 인터넷에서 조사해 분석·반영·개선하고, 작업 순서·스텝을 나누며, 추가로 필요한 게임 개발 스킬을 공식 자료에서 찾아 통합하라는 사용자 요청
- 입력 범위: PR #19 DDD 기준선, PR #22 정본 최신성 구조, Steamworks Reviews·Playtest·Testing, Unity Analytics Events·Funnels·A/B testing, Scrum Guide, GitHub Issues·Dependencies·Milestones, Xbox Accessibility Guidelines, Unreal performance profiling, Unity Edit·Play·target player test 문서
- 실제 산출물: `decompose-and-sequence`, `benchmark-and-player-research`, `playtest-and-experiment`, `accessibility-review`, `performance-profile`, Vertical Slice의 `slice-contract/quality-bar/pipeline-proof/playtest-evidence/decision-gate`, 3개 상세 reference, 2개 템플릿, Registry·Operating Model·프로젝트 Workflow·Skill Adoption Guide·회귀 테스트 동기화
- 실행한 검증: 독립 Skill 추가 없이 활성 Skill 13개 유지, mode·trigger·공식 출처·참조 파일·라우팅 회귀 추가, 전체 GitHub Actions 실행 대기
- 결과: 부분 성공
- 성공 조건: 벤치마크가 기능 복사가 아니라 근거 층위와 `ADOPT/ADAPT/AVOID/TEST/IGNORE` 결정으로 연결되고, 작업 단계가 의존성·게이트·롤백을 가지며, 플레이테스트·접근성·성능이 실제 증거 계약으로 연결됨
- 실패·예외·재현 조건: 리뷰 표본·버전·플랫폼 편향, 이벤트와 감정의 혼동, 한 실험에서 여러 변수 변경, 근거 없는 일정 추정, 접근성의 법적 준수 과장, 평균 FPS만으로 성능 통과를 주장할 위험이 있음
- 사용자 피드백: 위 두 기능은 각각 별도 Skill이 아니라 통합 mode로 추가하고, 인터넷에서 필요한 게임 개발·작업 스킬을 더 찾아 통합·참고·개선할 것
- 불필요하게 호출한 스킬: 없음. 신규 독립 Skill 2개 대신 기존 Intake·Concept·Validation·Vertical Slice 생명주기에 흡수함
- 누락된 스킬·검증: 실제 프로젝트의 리뷰 표본 코딩, 외부 Playtest 모집·피드백 회수, 실제 target hardware 프로파일과 접근성 사용자 검수
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 작업 분해 원리는 패턴, 벤치마크·플레이테스트·접근성·성능 통합 계약은 관찰·가설
- 프로젝트 전용으로 유지할 내용: 실제 비교 게임, 리뷰 데이터, 테스트 빌드·표본, 이벤트 Schema·퍼널, 장르별 목표 지표, 접근성 우선순위, 성능 예산·하드웨어
- Base Method·Skill·Template·Test 환류 후보: 이번 mode·reference·template·Registry·회귀 전체
- 다음 검토 트리거: 첫 두 프로젝트 적용, 오라우팅, 표본 편향, 실험 인과 오류, 작업 단계 과분해·과병렬화, 접근성·성능 검증 비용 과다

### 2026-07-21 Digital Dopamine Design definition and reward-analysis contract

- 프로젝트·작업: Base 기획 분석의 DDD 의미를 Digital Dopamine Design으로 확정하고 빠른 보상·즉각 피드백 분석 계약을 구체화
- 기준 스킬 커밋: `agent/consolidate-skills-and-structure@5679303d056a14bfeb41c8f3a35e2271815c3982`
- 호출 트리거: DDD는 빠른 시간 안에 사용자가 보상을 체감하도록 하는 도파민형 빠른 보상 요소라는 사용자 정의
- 입력 범위: `analyzing-and-refining-game-concepts`, GAME_CONCEPT_DIRECTION_REVIEW 템플릿, Base Skill Registry, 통합 Skill 참조 회귀 테스트
- 실제 산출물: DDD 프로젝트 정의, 첫 의미 있는 보상·행동 피드백·보상 명료성·밀도·보상 사다리·다음 행동·피로 분석축, PoC 관찰 필드, 위험 가드레일, `digital-dopamine-design`·`rapid-reward`·`instant-feedback`·`reward-latency` 라우팅 태그
- 실행한 검증: Registry Schema·활성 경로, DDD 정의·측정축·가드레일·템플릿·라우팅 회귀, Python 문법, Documentation·Skill Routing·Design Publication Governance, 전체 구조·생성 회귀 79개, Windows 실제 발행 스모크 테스트, whitespace
- 결과: 성공 — GitHub Actions run #73, 79 tests 성공·1 skipped, Windows 발행·whitespace 성공
- 성공 조건: DDD가 명확한 내부 용어와 관찰 가능한 설계축을 가지며, 뾰족한 재미를 단순 자극으로 대체하지 않고 외부 동명 약어와 구분됨
- 실패·예외·재현 조건: 최초 run #71에서 기존 회귀가 요구한 `임의 해석하지 않는다` 정확 문구가 새 표현에 없어 1건 실패했다. 의미를 바꾸지 않고 호환 문장을 복원한 뒤 run #72와 Learning Log 동기화 후 run #73에서 전체 통과했다.
- 사용자 피드백: DDD는 도파민 중독형 빠른 보상, 즉 빠른 시간 안에 사용자가 도파민성 보상을 느끼게 하는 요소를 의미함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 실제 게임의 첫 보상 시간·피드백 지연·다음 행동 전환과 장기 피로 데이터는 아직 없음
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: DDD 용어 정의는 사용자 승인, 보상 설계 효과와 공용 목표 수치는 가설
- 프로젝트 전용으로 유지할 내용: 장르별 목표 시간, 보상 간격, 실제 UX·경제·연출, 플레이테스트 결과와 허용 자극 강도
- Base Method·Skill·Template·Test 환류 후보: DDD 측정 필드, PoC 관찰 계약, 자극 대 핵심 재미 판정, 위험 가드레일
- 다음 검토 트리거: 서로 다른 두 프로젝트 적용, 빠른 보상이 핵심 선택을 약화함, 보상 인플레이션·피로, 목표 수치 일반화 시도

### 2026-07-21 canonical reference freshness audit

- 프로젝트·작업: Base 변경 시 오래된 파일·경로·Skill ID·정책 참조와 갱신 누락을 찾는 전문 Skill·자동 검사 추가
- 기준 스킬 커밋: `agent/add-reference-freshness-audit-v3`
- 호출 트리거: 패치나 변경 뒤 모든 활성 파일이 최신 정본을 따르는지, 오래된 파일을 참조하거나 갱신되지 않은 소비자가 있는지 찾는 Skill을 추가하라는 사용자 요청
- 입력 범위: PR #19 최종 DDD head, 통합 Skill Registry, 범용 변경 검증 Skill, Operating Model, 프로젝트 AI Workflow, Legacy Alias, 구조·참조 회귀 테스트와 Actions
- 실제 산출물: `auditing-canonical-reference-freshness`, `reference-freshness` 검증 mode, 감사 템플릿, `.github/reference-freshness.json`, 표준 라이브러리 기반 checker, 단위 테스트와 CI 연결, 13개 활성 Skill Registry
- 실행한 검증: checker 단위 테스트 4개 추가, Registry·구조·활성 진입점 테스트 갱신, Python 문법·Actions 실행 대기
- 결과: 부분 성공
- 성공 조건: DDD 정의·라우팅·PoC 관찰 계약을 보존하면서 정본 변경 영향 지도, Legacy·History 허용, stale reference·content drift·파생본·untouched 소비자 검사와 자동 coupled-change 차단이 하나의 검증 흐름으로 연결됨
- 실패·예외·재현 조건: 문자열 검색만으로 의미 drift를 완전히 판정할 수 없으며, 프로젝트별 History 허용 glob과 coupled-change 규칙이 과도하면 오탐이 발생할 수 있음
- 사용자 피드백: 모든 파일이 최신 파일을 기준으로 내용을 따르는지와 오래된 파일 참조·갱신 누락을 찾아야 하며, 완료된 DDD 스킬과 최종 검증 결과를 기준선에 포함할 것
- 불필요하게 호출한 스킬: 없음. 범용 검증에 직접 흡수하지 않고 독립 자동화·증거가 있는 specialist로 유지함
- 누락된 스킬·검증: 실제 서로 다른 프로젝트의 rename·Schema·문서 통합 사례에서 오탐·누락률 검증
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 관찰
- 프로젝트 전용으로 유지할 내용: 실제 정본 경로, History 허용 범위, 프로젝트별 coupled-change 규칙과 파생본 정책
- Base Method·Skill·Template·Test 환류 후보: reference freshness config·checker·감사 템플릿·CI 게이트
- 다음 검토 트리거: 첫 두 프로젝트 적용, Legacy 오탐, stale reference 누락, coupled-change 과도 차단, Manifest가 CURRENT지만 실제 입력과 불일치

### 2026-07-21 concept analysis and unified project-change validation

- 프로젝트·작업: Base 핵심 컨셉·뾰족한 재미·PoC 기획 분석 스킬 추가와 외부 AI 검수의 범용 변경 검증 통합
- 기준 스킬 커밋: `agent/consolidate-skills-and-structure@e679219ab1e2f993602d9e928ddf98640b69df41`
- 호출 트리거: SWOT·DDD 요소 분석과 개선 방향, 핵심 컨셉→제약→뾰족한 재미→구체화→PoC→재조정→Production 흐름을 반복 가능한 스킬로 만들고 일반 변경 검증 공백을 해소하라는 사용자 요청
- 입력 범위: 활성 Skill Registry, Operating Model, START_HERE, AGENTS, Documentation Map, Workflow·Checklist, 프로젝트 템플릿, 기존 Vertical Slice·외부 AI 검수 스킬과 구조 회귀 테스트
- 실제 산출물: `analyzing-and-refining-game-concepts`, `reviewing-and-validating-project-changes`, 기획 방향·변경 검증 템플릿, 12개 활성 Skill Registry, Legacy Alias와 프로젝트 라우터 갱신
- 실행한 검증: Registry Schema·활성 경로, 12개 선택적 라우팅, 기획 8개 mode·7단계 상태 흐름·SWOT 전략·MDA/DDE·DDD 계약, 변경 검증 6개 mode·5개 판정, 삭제 경로·Legacy Alias·프로젝트 템플릿 참조, Python 문법·BCP·Documentation·Skill Routing·Design Publication Governance, 구조·생성 회귀 78개, Windows 실제 발행 스모크 테스트, whitespace
- 결과: 성공
- 성공 조건: 기존 기획 문서·Vertical Slice·UI 감사 경계를 보존하고 새 Skill의 trigger·mode·템플릿·라우팅·회귀·Actions가 통과함
- 실패·예외·재현 조건: `BIG BLIND`와 초기 미정의 `DDD`를 외부 표준 용어로 단정하지 않고 프로젝트 정의형 용어로 처리했다. 최초 큰 파일 생성 요청이 보안 판정 불명으로 차단돼 동일 기능의 표현을 축약해 재시도했다. 1차 Actions에서 기획 템플릿의 trailing whitespace 1건을 검출해 제거했으며 최종 run #67에서 전체 통과했다.
- 사용자 피드백: 핵심 컨셉과 지속 플레이 원동력 탐색, 모든 게임 요소의 정렬, PoC 결과 기반 기획 재조정, 7단계 Production 흐름을 포함할 것
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 실제 서로 다른 게임 프로젝트에서의 반복 적용 결과와 PoC 관찰 데이터는 아직 없음
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 핵심 컨셉 분석은 가설, 범용 변경 검증은 패턴
- 프로젝트 전용으로 유지할 내용: 실제 게임의 컨셉 문장·SWOT 항목·DDD 목표·PoC 결과·수치·콘텐츠·Production 판정
- Base Method·Skill·Template·Test 환류 후보: 기획 방향 상태 머신, SWOT-to-action, DDD 정의 계약, 범용 검증 판정·증거 템플릿과 Legacy Alias
- 다음 검토 트리거: 첫 두 프로젝트 적용, PoC 범위 팽창, DDD 목표 오라우팅, SWOT 일반론화, 통합 검증 Skill 비대화

### 2026-07-21 consolidated Base skills and operating structure

- 프로젝트·작업: Base 활성 Skill과 공용 운영 문서 통합
- 기준 스킬 커밋: `main@eb40b912e5f5a0e4d369105a4f0a770e0a6179a9`
- 호출 트리거: 유사하거나 순차 의존하는 Skill·Method·Checklist가 과도해 최소 호출과 책임 원본 원칙을 위반한다는 사용자 검토
- 입력 범위: 활성 Skill 17개, Skill Registry, START_HERE, AGENTS, README, Documentation Map, 공용 Rules·Workflow·Checklist, 운영·마이그레이션·발행·Handoff·Skill Evolution Method
- 실제 산출물: 활성 Skill 11개, 통합 Skill 4개, Legacy Alias, 통합 Operating Model, 축소된 라우터·원칙 문서, 발행 정책 3단계와 정책 선택 생성 도구
- 실행한 검증: Python 문법, Base Skill Registry Schema·활성 경로, Legacy Alias·삭제 경로·잔여 템플릿 참조, Documentation·Skill Routing·Design Publication Governance, 정책 선택 생성기 통합, 구조·콜드 스타트·BCP·딥인터뷰·UI 감사·DOCX/PDF 생성 회귀 78개, Ubuntu와 Windows 실제 발행 검증, whitespace
- 결과: 성공
- 성공 조건: 기존 고유 절차 보존, 활성 이전 ID 제거, 새 ID 라우팅, 자동 검사·회귀·Actions 통과, 콜드 스타트에서 최소 Skill 탐색
- 실패·예외·재현 조건: 1차 CI에서 역인터뷰와 별도 구현 PR 계약 문구 2개가 불일치해 통합 Skill 표현을 정렬했다. 추가 감사에서 3단계 발행 정책이 기존 Schema의 `always_sync` 단일 허용과 충돌한 것을 발견해 Schema·정책 선택기·Governance·회귀 테스트까지 함께 구현했다.
- 사용자 피드백: 유사하거나 통합 가능한 Skill·구조를 합치고 통합 후 정상 작동과 추가 개선을 다시 점검할 것
- 불필요하게 호출한 스킬: 통합 후 요청 접수 Foundation 연쇄 호출 3개를 1개로 축소
- 누락된 스킬·검증: 실제 게임 프로젝트에 적용한 장기 사용성·오라우팅 빈도는 아직 프로젝트 검증 전
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 패턴
- 프로젝트 전용으로 유지할 내용: 각 게임의 세계관·수치·실제 경로·승인 자산·프로젝트 Skill
- Base Method·Skill·Template·Test 환류 후보: 통합 Skill mode·Legacy Alias·발행 정책·정책 선택기·잔여 참조 회귀 검사
- 다음 검토 트리거: 첫 대상 프로젝트 적용, Legacy Alias 오라우팅, 하나의 통합 Skill이 과도하게 비대해짐, 3단계 발행 정책의 실제 운영 비용 불균형

### 2026-07-19 structured design documents and human publication pipeline

- 프로젝트·작업: Base PR #8 — 모든 프로젝트·분야 기획서의 AI JSON + 사람용 DOCX/PDF + 다이어그램·승인 이미지 구조
- 기준 스킬 커밋: `51d3535afa3eea5b19d262e1fe87d06f183c2224`
- 호출 트리거: 스킬맵뿐 아니라 모든 기획서가 이미지 확인 가능한 사람용 문서를 가져야 한다는 사용자 피드백
- 입력 범위: Base 시작 규칙·운영 Method·기획서 작성·마이그레이션·발행·스킬 진화·Health Review·프로젝트 템플릿·GitHub 검사·회귀 테스트
- 실제 산출물: Design Document Registry·JSON 본책 템플릿·DOCX/PDF·다이어그램 생성기·승인 이미지 포함·세 번째 Governance Checker·실제 생성 통합 테스트
- 실행한 검증: Python 문법, Documentation Governance, Skill Routing Governance, Design Publication Governance, JSON 기획서와 Skill Registry의 DOCX/PDF·다이어그램 실제 생성, 승인 이미지 포함, PDF 전 페이지 렌더, 구조 회귀, whitespace
- 결과: 성공
- 성공 조건: 기획서·스킬맵 실제 생성, 세 Governance Checker, 구조 회귀, PDF 렌더와 whitespace가 최종 head의 GitHub Actions run #18에서 모두 통과
- 실패·예외·재현 조건: 초기 CI에서 pip 캐시 입력 파일 부재로 Python 설정이 실패해 캐시를 제거함. 다음 실행에서 Skill 진화 Method와 Health Review Skill 연결 문구 누락이 구조 테스트에 검출돼 계약을 보완함.
- 사용자 피드백: AI는 JSON을 읽고 사람은 DOCX/PDF와 이미지·다이어그램을 한눈에 확인해야 함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 기존 구조에는 프로젝트 전체·분야 기획서용 구조화 Registry, 승인 이미지 포함 DOCX, 생성기 해시와 전 페이지 PDF 렌더 검사가 없었음
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 패턴
- 프로젝트 전용으로 유지할 내용: 실제 게임의 세계관·수치·구현 경로·승인 이미지·생성된 기획서 바이너리
- Base Method·Skill·Template·Test 환류 후보: 이번 PR의 JSON 계약·생성기·Checker·통합 테스트 전체
- 다음 검토 트리거: 첫 대상 프로젝트 실제 마이그레이션, DOCX/PDF 렌더 실패 반복, Registry와 발행본 불일치

### 2026-07-19 operating-system skill routing and learning audit

- 프로젝트·작업: Base PR #7 — 선택적 Skill 호출·지속 학습·루트 `[기획서]` 검수
- 기준 스킬 커밋: `c65ffe2e589caf8e38c546dbdfcd37e669b09f9f`
- 호출 트리거: 분야별·Foundation Skill의 항상 학습, 필요한 경우에만 호출, 운영체계 연결 검증, 루트 `[기획서]` 요청
- 입력 범위: Base START_HERE·AGENTS·README·Documentation Map·운영체계 Method·Installer·Project Operations 템플릿·GitHub 검사·회귀 테스트
- 실제 산출물: 공용·프로젝트 Skill Registry, 라우팅·Handoff·Health Review Skill, Learning Log 계약, 루트 기획서·Registry 자동 검사와 회귀 테스트
- 실행한 검증: Python 문법, Documentation Governance, Skill Routing Governance, Base 구조 테스트, `git diff --check`
- 결과: 성공
- 성공 조건: Registry·루트 기획서·동기화 실패 테스트와 whitespace 정상
- 실패·예외·재현 조건: `[기획서]` 대괄호 glob 해석 문제를 실제 폴더명 비교로 수정
- 사용자 피드백: Skill이 항상 학습 가능하고 필요한 때만 호출되며 활성 기획서는 최상위 폴더에서 보여야 함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 요청 라우팅, Context·Handoff, Health Review와 Skill Registry 검사
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 패턴
- 프로젝트 전용으로 유지할 내용: 대상 게임의 구체 Skill·실제 경로·승인 자산
- Base Method·Skill·Template·Test 환류 후보: Method·Skill·Registry·Health Report·Checker·회귀 테스트
- 다음 검토 트리거: 대상 프로젝트 첫 실제 적용, 동일 라우팅 실패 반복, 90일 이상 미검토

## 2026-07-25 — Base 공용 Skill 어댑터와 Godot 자산 선행 검색

- 상태: `PATTERN`
- 추가 Skill: `governing-legacy-retention-and-archives`, `evaluating-godot-assets-and-plugins-before-creation`
- 결정: Base 공용 Skill은 프로젝트에 복제하지 않고 route Registry와 프로젝트 경로 어댑터로 연결한다.
- 결정: Godot 기능·에셋·상용 플러그인은 직접 제작 전에 기본 기능, 공식 Store, 기존 Asset Library, GitHub, itch.io와 제작자 원본을 조사한다.
- 안전 경계: 구매·계정 연결·설치는 별도 사용자 승인, 기존 로컬 공용 Skill 복사본 삭제는 별도 레거시 감사가 필요하다.
- 검증: Base Registry·Learning Log·운영체계 구조 테스트·프로젝트별 route·adapter의 정합성을 확인한다.
## 2026-07-28 — BCA Sheet·GPT 이미지 생성·검수 통합

- `designing-art-prompts-and-technique-cards`에 `planning-visualization`, `final-visual-candidate`, `visual-qa-and-approval` mode를 통합했다.
- 프로젝트 Sheet 의미 구조에 세계관·핵심루프·주요인물·조연·핵심시스템·이미지 계획·검수 tab을 추가했다.
- 정확한 Sheet URL이 없으면 `NOT_CONFIGURED`로 유지하며 중복 생성을 금지한다.
- v7은 호환본, v8은 활성 통합 실행문으로 전환한다.

## 2026-07-30 — 시각 협업은 도구명이 아닌 책임 어댑터

- Figma·Whimsical은 GDD 내부·외부·양쪽에서 조합 가능하되 GitHub 정본과 Godot 증거를 대체하지 않는다.
- 새 도구명 Skill 대신 기존 컨셉·UX/UI·문서·인계 Skill에 정책·Artifact 계약을 연결한다.

## 2026-08-01 — Base v9.4 AI operations

- BCP-2026-003: 모델 하향의 재시도·상위 모델 재작업 비용까지 포함해야 비용 최적화가 성립한다.
- BCP-2026-004: 강한 안전 규칙은 보존하되 예시는 Fixture로, 표현·배치는 검증 가능한 판단 공간으로 분리한다.
- 신규 제안은 사용자 승인 근거가 있어도 제안 PR에서 `SUBMITTED`로 시작하고 승인 상태는 별도 구현 PR에서 전환해야 한다.
- UI 모션은 표현이며 도메인 결과의 권위가 아니다. 중단·즉시 완료·빠른 반복과 접근성 폴백을 함께 검증한다.

## 2026-08-01 — Base v9.5 Skill 탐색·행동 평가 정비 후보

- 상태: `OBSERVATION`
- 기준 커밋: `87a0b54`
- 호출 트리거: Base 전체 구조 감사, Skill·작업 연결 개선, 모호성·구형 참조·장문 축소, GitHub Issue #74의 가설 검증형·요소 분해 요구 통합
- 실제 산출물: 28개 활성 Skill 설명 축약, 요청→예상 Skill 행동 평가 계약·Fixture·fail-closed 검사기, `behavior-eval` mode, 가설·최소 검증 단위·요소 통합·다각도 검토·회고 계약, 권위·릴리스 문서 정합화, description-only frontmatter 변경과 본문 계약 변경을 구분하는 참조 전파 검사
- 검증 결과: v9.5 집중 회귀 11개와 reference-freshness 회귀 11개 통과, 전체 회귀 355개 통과·환경 의존 5개 건너뜀, 커밋 간 정적 참조 425개 파일 통과, 행동 평가 계약 `PASS`, 실제 모델 실행 `NOT_RUN`, Skill 탐색 메타데이터 예산 9,632자에서 6,279자로 축소, Registry SHA-256 유지
- 실패·예외·재현 조건: Work Mode의 실행 불가능한 LibreOffice·Poppler 래퍼가 경로에 존재해 초기 전체 회귀가 3개 실패했다. 실제로 사용할 수 없는 래퍼를 PATH에서 제외하자 환경 의존 검사는 skip되고 전체 회귀가 통과했다. 첫 커밋 간 reference-freshness는 모든 Skill 파일 변경에 Registry·분야별 소비자 갱신을 강제해 설명 전용 축약을 본문 계약 변경으로 오판했으며, frontmatter key 차이와 본문 차이를 분리하는 회귀로 수정했다.
- 지식 상태: 실제 모델 결과가 없는 행동 평가 Fixture와 검사기는 `OBSERVATION`; 여러 모델·프로젝트에서 오라우팅 감소가 재현될 때 `PATTERN` 승격 검토
- 프로젝트 전용으로 유지할 내용: 실제 게임의 프롬프트·모델 결과·세계관·수치·데이터·자산·프로젝트 Skill
- Base Method·Skill·Template·Test 환류 후보: 행동 평가 계약, 가설 검증·요소 분해·다각도 검토·Golden Path/Edge/Regression, Base 공용 후보와 프로젝트 전용 학습의 분리
- 다음 검토 트리거: 실제 모델 결과 채점, 모델별·프로젝트별 오라우팅, 8,000자 탐색 예산 회귀, 평가 Fixture가 구현 세부사항에 과적합되는 징후

## 2026-08-02 — Required Check 단일 소유와 내부 비용 분류

- 상태: `OBSERVATION`
- 문제: 서로 다른 Workflow가 같은 `ci-gate` check name을 만들고, Required Check 소유 Workflow의 path filter가 일부 PR에서 check를 생성하지 않을 수 있었다.
- 결정: Required Check 이름은 저장소 전체에서 단일 소유하고, 소유 Workflow는 모든 PR에서 시작한 뒤 내부 classifier로 비용을 제어한다.
- 검증: 실행형 topology checker, fixture RED→GREEN, focused Python 회귀, 전체 Python 회귀 388개 통과·환경 의존 5개 건너뜀.
- 미실행 검증: 실제 PR Actions `PENDING`.
- 다음 검토 트리거: Required Check Pending 재발, Workflow 추가·이름 변경, Ruleset context 변경.

## 2026-08-01 — 중립적 적대 검토와 기능 생명주기

- 상태: `OBSERVATION`
- 호출 트리거: 기능 구현 전반과 전체 제작 생명주기를 결합하고, 사용자 의견에 무조건 긍정하지 말며 중립적 적대 검토로 최선의 결론을 도출하라는 사용자 결정
- 결정: 새 광역 Skill을 만들지 않고 `managing-project-intake-and-work-contract`를 상위 라우터로 유지한다. 사용자안과 AI 최초안에 같은 평가 기준을 적용하며, 근거 없는 동의와 반대를 위한 반대를 모두 실패 조건으로 둔다.
- 적용 경계: 권장안·판정에는 경량 중립성 Gate를 적용한다. L1 이상 기능·설계·아키텍처·정책·방향 결정은 PLAN 사전판정 `attack → validate-critique → decision-report`를 거친다. 승인 finding은 `refine-approved-findings`에서 분야 Skill BUILD가 한 번만 반영하고 `regression-recheck → decision-report`로 이동해 전체 루프를 닫는다. L0 오탈자·명백한 기계 수정·동일 입력 재실행과 결정·권장안 없는 설명형 요약은 전체 루프에서 제외한다.
- 실제 산출물: 항상 적용 규칙, 운영 모델의 기능 생명주기, 라우팅 경계, intake의 `neutral-recommendation-gate`, 적대 검토의 대칭 평가 규칙, 동의 유도·기계적 반대·불완전 증거·결정 없는 설명형 요약을 각각 다루는 `SBE-011`~`SBE-014` 행동 Fixture와 집중 회귀
- 검증: 집중 계약, 행동 평가 계약, Skill package, 문서 governance, reference freshness, 전체 회귀와 Base v9 integrity의 실제 결과를 PR 증거로 기록한다.
- 미검증: 외부 모델 결과를 사용한 동의 편향 감소율과 실제 프로젝트별 오라우팅 변화는 `NOT_RUN`
- 프로젝트 전용 유지: 실제 기능 요구, 기술 스택, PyTorch·머신러닝 데이터·모델·수치, 프로젝트 코드·자산·Google Sheets
- 다음 검토 트리거: 과도한 REVIEW 호출, 명백한 사실에 불필요한 대안 생성, 사용자 결정권 약화, 모델 결과에서 근거 없는 동의 또는 기계적 반대 재발

## 2026-08-02 — 실행형 발행 준비도와 로컬 검증 격리

- 상태: `OBSERVATION`
- 문제: 경로 존재만 확인한 두 생성 테스트의 gate가 실행 불가능한 래퍼와 누락 폰트를 준비 완료로 오판했다. 396개 기준 회귀에서 생성 class가 진입해 폰트 관련 실패 2건이 발생했다.
- 구현 가설: LibreOffice의 실제 PDF 변환, Poppler 실행, regular/bold 폰트를 하나의 공유 준비도 계약으로 검사하고, 전체 로컬 검증은 저장소가 소유한 `.tmp/local-validation-*` 세션에 `TMPDIR`·`TMP`·`TEMP`를 고정한다.
- 현재 결과: 공유 준비도 fixture와 소비자 회귀는 통과했다. 현재 환경에는 필수 폰트가 없어 생성 검사는 이유가 표시된 `SKIPPED`이며 발행 검증 `PASSED`가 아니다.
- 적대적 검토: `MUST_FIX`로 공용 probe가 Windows `.cmd/.bat` 안전 실행 계약을 우회한 회귀를 발견해 기존 안전 command-array 생성기로 복구했다. `SHOULD_FIX`로 timeout pipe 잔존과 세션 경로 바꿔치기가 자식 실패 코드를 가리는 문제를 확인해 process drain·세션 identity·원래 실패 코드 보존 회귀를 추가했다.
- 독립 코드 리뷰: 자손이 probe pipe를 상속한 timeout의 무제한 drain, root-only readiness cache의 stale override, Windows 전체 readiness fixture skip을 `Important`로 확인했다. 자손 process-group 종료와 bounded drain, resolved tool·file identity cache key, Windows 전용 실제 `.cmd` 실행 회귀로 수정했으며 재리뷰 결과 Critical/Important 0건이었다. Windows 실제 실행 결과는 exact-head Actions 전까지 `NOT_RUN`이다.
- 첫 exact-head Windows Actions: 실제 `.cmd` probe는 성공했지만 안전 runner가 정규화한 8.3 경로와 테스트 원문 경로 비교가 달라 smoke가 실패했다. 동시에 Chrome GUI의 `--version` timeout에 따른 preflight 실패가 뒤 unittest의 성공 코드로 덮일 수 있음을 확인했다. 경로 비교를 정규화하고, Chrome은 기존 계약처럼 파일 존재만 확인하되 실제 Mermaid 생성 회귀로 실행성을 검증하며, PowerShell이 preflight non-zero에서 즉시 종료하도록 수정했다. 재실행 전 상태는 `PENDING`이다.
- 안전 경계: 정리 대상은 현재 실행이 만든 정확한 세션 하나뿐이며 일반 `tmp*`, 사용자 파일, `.venv`, 캐시는 삭제하지 않는다. `.gitignore`도 `.tmp/`와 `.venv/`만 숨긴다.
- 지식 상태: Base 한 저장소의 성공만으로 외부 프로젝트 전체에 적용할 범용 의무를 확정하지 않는다. 서로 다른 프로젝트와 Windows/Linux 실제 발행 환경에서 재현될 때 `PATTERN` 승격을 검토한다.
- 다음 검토 트리거: 준비된 CI에서 생성 검사가 skip되거나 실패하는 경우, 임시 파일 잔존 재발, 외부 프로젝트 어댑터 적용 결과.

## 2026-08-05 — 게임 개발 YouTube 제작 Skill 독립 경계

- 상태: `OBSERVATION`
- BCP: `BCP-2026-006-game-youtube-devlog-marketing-workflow`
- 승인 근거: `https://github.com/alsdmlals4-eng/Base/pull/167#issuecomment-5192600204`
- 결정: `producing-game-development-youtube-videos`를 선택형 독립 전문 Skill로 등록한다. 실제 빌드에서 영상의 시청자 약속·대본·샷·제목·썸네일 패키지·게시 Gate·표본 제한 Analytics까지 반복되는 고유 입력·산출물·도구·실패 조건이 있어 게임 기획이나 아트 Skill에 흡수하지 않는다.
- 책임 경계: 게임 코어와 밸런스는 `analyzing-and-refining-game-concepts`, 대표 빌드 품질은 `designing-vertical-slices`, 썸네일 이미지 생성은 `designing-art-prompts-and-technique-cards`, 권리·등급·provenance는 기존 플랫폼 심사·에셋 권리 Workflow, 최종 변경 검증은 `reviewing-and-validating-project-changes`가 유지한다.
- Route 결정: 프로젝트 Adapter가 없으므로 `skills/BASE_SHARED_SKILL_ROUTES.json`에는 추가하지 않는다. Base Registry 선택과 프로젝트 정본의 실제 Episode Packet으로 연결한다.
- 검증 경계: Repository 계약·라우팅·회귀는 구현 증거일 뿐 실제 영상 품질·시청 유지·클릭·데모·위시리스트·후원·구매 전환의 사람 검증이 아니다. `HUMAN_NOT_RUN`, `CONVERSION_UNVERIFIED`, `INSUFFICIENT_SAMPLE`, `NOT_PROVEN`을 증거가 생길 때까지 유지한다.
- 롤백: 활성 Skill, Episode Packet Template, Registry·entrypoint·행동 평가·구현 증거·전용 Test를 구현 PR 하나로 되돌린다. 프로젝트가 채운 Packet과 실제 Analytics는 프로젝트 증거로 보존한다.
- 다음 검토 트리거: 실제 프로젝트 Pilot, 제목·썸네일 약속 불일치, 권리·스포일러·보안 누출, 작은 표본 과잉 해석, 영상 제작의 핵심 개발 잠식, 프로젝트 Adapter 필요가 반복 확인되는 경우.

## 2026-08-06 — BCP-008 선택형 명세·디자인·UI 조달 통합

- 관찰: Base는 요구·문서·검증 생명주기를 이미 소유했지만 L2 이상 Requirement의 구현·검증 연결 ID, 선택형 시각 토큰 정본, 외부 UI 소스 admission과 설치/품질 Gate 분리가 약했다.
- 결정: 새 ACTIVE Skill을 만들지 않고 기존 owner Skill에 Traceability Packet, 교차 분야 Lens, DESIGN.md Adapter, 외부 UI 조달·anti-generic Gate를 조건부로 통합한다.
- 보호: `skills/SKILL_REGISTRY.json`, released lock, 단일 주 책임 Skill, `GAME_UX_UI_SYSTEM`의 경험·행동 권위, Godot 중심 구조를 유지한다.
- 행동 압력: L2 추적성 선택, L1 비선택, Web 조달 선택, Godot shadcn 직접 설치 비선택 fixture를 추가한다.
- 실제 조달: shadcn-ui/ui exact commit의 source·package metadata·MIT license를 확인했다. source의 미배포 버전 `4.16.2`는 npm `ETARGET`으로 실패했으며, 배포된 CLI `4.16.1`을 사용한 격리 Vite fixture에서는 button 조달과 TypeScript/Vite build가 통과했다. Base·실제 프로젝트에는 설치하지 않았다.
- 증거 상한: 계약·fixture·source receipt와 격리 Web build는 실제 독립 모델 행동 향상, 목표 프로젝트 설치, 브라우저 상호작용, 접근성, 사람 미감 통과를 증명하지 않는다. `MODEL_RUN_STATUS: NOT_RUN`, target installation `NOT_RUN`, `HUMAN_NOT_RUN`을 유지한다.

## 2026-08-08 — BCP-2026-009 — developing-and-revising-serial-fiction

- 새 specialist가 필요한 이유: 게임 기획과 benchmark 활동은 일부 공유하지만 소설은 정본·POV·voice·회차 payoff·setup-payoff·원고 diff라는 독립 입력·산출물·Quality Bar를 가진다.
- 통합하지 않은 책임: 적대적 검토, 정본 발행, 게임 시스템 기획, 단순 proofreading, 마케팅 카피.
- 반례 학습: 성공작끼리 문체·정보량·속도·개그 강도가 상반되므로 인기작 표면 스타일을 Base 규칙으로 만들지 않는다.
- 증거 상한: Skill/Registry/behavior 계약은 검증 가능하지만 실제 독자 만족·판매 개선은 `PROJECT_PILOT_NOT_RUN`, `HUMAN_NOT_RUN`, `NOT_RUN`이다.

## 2026-08-14 — GitHub 도구가 아니라 capability를 선행조건으로 판정

- 상태: `PATTERN`
- 관찰: 검증된 변경을 게시하는 작업이 `gh: command not found`에서 중단됐지만, 연결된 GitHub connector에는 Branch·Git object·PR·status·merge capability가 이미 있었다.
- 결정: 기존 `synchronizing-local-and-github-state`가 `GITHUB_CAPABILITY_FALLBACK`을 소유한다. connector가 정확한 동작을 지원하면 optional `gh` 부재나 로컬 push 인증 실패를 전역 blocker로 승격하지 않는다.
- 안전 경계: connector/local Git/gh 어느 것도 필요한 정확한 capability와 증거를 제공하지 못할 때만 `BLOCKED_UNVERIFIED`로 유지한다. 사용자 Windows token 복사, 비밀이 아닌 `GH_TOKEN` 지속, force ref update, exact-SHA·Required Check·리뷰·post-merge gate 우회는 금지한다.
- 검증: Registry 라우팅, 현실적인 행동 평가, Skill system coverage, reference freshness, 전체 회귀와 실제 PR Actions를 각각 확인한다. connector 게시 성공은 CI·merge·release 성공과 분리한다.
- 다음 검토 트리거: connector coverage 확인 전 반복 인증 요구, missing optional CLI를 전체 작업 중단으로 확대, stale parent 위 Git-object write, 다른 HEAD의 CI를 병합 증거로 사용.

## 2026-08-30 — 프로젝트 선언형 머신 우선 검증 정책

- 상태: `OBSERVATION`
- 호출 트리거: 명시적 사용자 결정으로, 특정 Godot 프로젝트는 결정적·runtime·export·package·CI 머신 증거를 주 acceptance route로 사용하고 5인 이해도 및 player-experience 연구를 필수 Gate로 두지 않는다.
- 결정: `governing-game-user-research-coverage`와 Work five-phase template/router에 `PROJECT_DECLARED_VALIDATION_POLICY`의 선택형 `MACHINE_PRIMARY_FINAL_USER_REVIEW` 경로를 추가한다. Base는 고정 표본 수나 보편적 human-study 순서를 강제하지 않는다.
- 안전 경계: 이 경로는 machine evidence를 human evidence로 승격하지 않으며, 프로젝트가 명시적으로 승인한 연구 질문, target-platform/device, 법무·접근성·release 의무를 제거하지 않는다. `FINAL_USER_REVIEW`는 같은 exact candidate/build에 대해 사용자가 요청할 때만 기록한다.
- 검증: 전용 정책 회귀, Games User Research coverage companion test, five-phase/work-template/evidence-knowledge 회귀, canonical-reference freshness를 실행한다. 전 저장소 release-baseline 검증 실패는 별도 pinned evidence drift로 분리한다.
- 다음 검토 트리거: 프로젝트가 machine evidence를 human PASS로 오기재하는 경우, participant study를 명시 승인 없이 재도입하는 경우, 또는 platform/release 의무와 충돌하는 경우.

## 2026-08-31 — CANDIDATE_REPORT_BOUNDARY_AND_MINIMAL_CORRECTION_REQUEST

- 상태: `OBSERVATION`
- 호출 트리거: 서로 다른 Godot 프로젝트의 수정제안서·후보 보고서를 Base에 제출하기 전에, 후보 자료를 곧바로 공용 규칙·구현 증거로 승격하지 않으면서도 공통 교훈과 실제 수정 요청을 재사용 가능하게 정리할 필요가 확인됐다.
- 실제 관찰: 후보 보고서는 프로젝트별 경로·런타임 상태·기획 결론을 포함할 수 있으며, 생성·정리·검수됐다는 사실만으로 다른 프로젝트의 구현, 사용자 검증 또는 Base 정본 변경을 증명하지 않는다. 반대로 단순 제목·요약만 있으면 공통화 조건, 기존 owner의 빈틈, 최소 수정 범위를 판정할 수 없다.
- 결정: 새 Skill·새 정본·후보 보고서 사본을 만들지 않고 `managing-base-change-proposals`와 `BASE_CHANGE_PROPOSAL.md`에 `CANDIDATE_REPORT_IS_NOT_BASE_CANON`, 공통 교훈, 기존 owner gap, 최소 correction request, project-only 제외 범위, evidence ceiling·non-use condition을 함께 요구한다. 제안은 `ADOPT`·`ADAPT`·`REJECT` 또는 보류 판단의 근거를 남기되, 실제 구현과 검증은 별도 exact revision 증거가 있을 때만 주장한다.
- 검증: `tests/test_base_change_proposals.py`, `tests/test_skill_implementation_evidence.py`, exact-head canonical-reference freshness.
- 안전 경계: 이 기록과 템플릿은 후보 보고서의 주장이나 첨부 PDF를 Base canon·runtime PASS·human PASS·사용자 승인으로 바꾸지 않는다. 특정 프로젝트의 세계관·경로·자산·수치·개별 결론은 project-only로 유지한다.
- 다음 검토 트리거: 후보 보고서가 공통 교훈 없이 다시 Base 변경으로 승격되려 할 때, 동일한 correction request가 서로 다른 owner를 중복할 때, 또는 actual observation과 추측이 혼합돼 evidence ceiling을 잃을 때.
