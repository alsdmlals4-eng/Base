Warning: truncated output (original token count: 20630)
Total output lines: 630

# Base Skill Learning Log

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
- 현재 지식 상태: 사용자 승인과 B…8630 tokens truncated…ocumentation Map, Workflow·Checklist, 프로젝트 템플릿, 기존 Vertical Slice·외부 AI 검수 스킬과 구조 회귀 테스트
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
