# Base Postmerge Trade Study and Adversarial Follow-up

Date: 2026-08-18

```text
SNAPSHOT_ROLE: HISTORICAL_EVIDENCE_NOT_CURRENT_STATUS
CURRENT_STATUS_AUTHORITY: repository main + exact PR/workflow readback
SOURCE_MERGE: PR #516
SOURCE_MERGE_SHA: a6a788cbdec82b2b7dce36f4355d8c78d5a30da8
FOLLOWUP_PR: #517
```

이 기록은 “벤치마킹/현행조사/적대적 검토를 했다”는 선언을 대신하는 **실제 실행 증거**다. 현재 상태는 이 파일의 문장보다 최신 `main`, PR head, workflow 결과를 다시 읽는다.

## 1. Current-state comparison actually executed

### Before #516

- completed `main`: `5a4be1affc6ec78dc63fab8a04c1e4808b9a42d2`
- long-horizon 공용 정책 파일이 없었다.
- Git 동기화 Skill은 same-goal overlap을 standing copy-integration 대상으로 보았지만 other-chat/different-workstream을 먼저 분리하는 명시 Gate가 없었다.
- Loop A2 foundation 문서는 역사 snapshot과 current mutable status가 한 문서에서 혼동될 여지가 있었다.

### After #516

- merged `main`: `a6a788cbdec82b2b7dce36f4355d8c78d5a30da8`
- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`가 추가되어 방향 우선, 여러 사례 benchmark synthesis, 대안 비교, 정확히 5개 공격면, core-loop/balance/story/reuse, Figma/repo-native data, Tool Hub/Loop evidence boundary, bounded completion을 연결한다.
- `INDEPENDENT_WORKSTREAM_ISOLATION`과 `EXPLICIT_USER_ABSORPTION_AUTHORIZATION`가 Git sync owner까지 전파되었다.
- 기존 `GITHUB_CAPABILITY_FALLBACK`, exact-head, fail-closed 의미를 회귀 테스트로 보존했다.
- Loop mutable status authority는 `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`으로 단일화되고 foundation 문서는 `SUPERSEDED_STATUS_SNAPSHOT` 역할을 명시한다.
- Tool Hub Windows process smoke는 catalog 세 도구를 `RUNNABLE`로 요구하고 실제 Windows publication/Tool Hub smoke가 #516 exact head GPO에서 PASS했다. 이 증거는 user-PC live 실행을 자동 의미하지 않는다.

Repository compare used:

```text
base: 5a4be1affc6ec78dc63fab8a04c1e4808b9a42d2
head: a6a788cbdec82b2b7dce36f4355d8c78d5a30da8
result: 1 squash commit, 19 changed files
```

## 2. Alternatives considered before this follow-up

### Option A — add another broad “research/benchmark/best-method” Skill

- benefit: discoverability can be explicit.
- cost: duplicates intake, adversarial review, validation, and Existing Solution First owners.
- long-term risk: more tool/Skill routing ambiguity and context load.
- disposition: `REJECT`.

### Option B — add a new independent policy layer with another authority chain

- benefit: exact new wording can be centralized.
- cost: `AGENTS.md`, long-horizon policy, adversarial owner, and claim-verification owner already cover the material responsibilities.
- long-term risk: second canon and synchronization burden.
- disposition: `REJECT`.

### Option C — preserve existing owners, harden regression coverage, and record executed evidence

- benefit: strengthens behavior without new broad responsibility or duplicated canon.
- cost: tests must cover cross-owner composition rather than one magic token.
- long-term risk: lower, provided current-state readback remains mandatory.
- disposition: `ADOPT`.

### Option D — rely on narrative instructions only and add no regression evidence

- benefit: zero code change.
- cost: future refactors can silently drop the behavior.
- disposition: `REJECT` for material L1+ governance behavior.

Recommended direction: **Option C**.

## 3. External benchmark/trade-study evidence actually checked

External sources do not become Base authority. They were used to challenge the design and decide `ADOPT / ADAPT / REJECT`.

| Source | Observed principle | Base disposition |
|---|---|---|
| NASA Systems Engineering Handbook — Decision Analysis / Analysis of Alternatives (`https://www.nasa.gov/reference/6-8-decision-analysis/`, `https://www.nasa.gov/reference/system-engineering-handbook-appendix/`) | define alternatives, criteria, evaluation methods/results, cost/risk and recommendation instead of starting from one preferred answer; analysis depth should fit decision complexity | `ADAPT`: material Base decisions compare viable alternatives before commitment without forcing a heavyweight report on trivial work |
| NASA System Design Processes (`https://www.nasa.gov/reference/4-0-system-design-processes/`) | evaluate alternative designs against effectiveness, achievability, cost, schedule and risk; select the best alternative | `ADAPT`: use user/player value, correctness, life-cycle cost, risk, reversibility, maintenance and evidence as trade criteria |
| DORA — Working in small batches (`https://dora.dev/capabilities/working-in-small-batches/`) | small independent batches improve feedback and counter instability as AI accelerates development | `ADOPT`: repository-wide discovery can be broad, implementation remains bounded/testable |
| Google Engineering Practices — Small CLs (`https://google.github.io/eng-practices/review/developer/small-cls.html`) | small self-contained changes are easier to review deeply, reason about, merge and roll back | `ADOPT`: do not turn a Base-wide audit into one opaque unrelated mega-change |
| Git `git-worktree` documentation (`https://git-scm.com/docs/git-worktree`) | one repository can support multiple linked working trees for different branches | `ADOPT`: isolated worktrees/branches are the standard concurrency mechanism; ownership still needs Base policy |
| Figma plan/branching documentation (`https://help.figma.com/hc/en-us/articles/360040328273-Team-plans-in-Figma`, `https://help.figma.com/hc/en-us/articles/360063144053-Guide-to-branching`) | Professional has unlimited version history; Branching/Merging is Organization/Enterprise | `ADAPT`: current Figma Pro workflow uses Pages/Sections, lifecycle states and version history; branching is optional only when actually available |

## 4. Test-first evidence

Initial test-only head:

```text
307dd6b8701be9a079b2b25e0018803d871f46a4
Validate Base Long-Horizon Work Contract run: 32109021913
result: RED
```

Observed REDs:

1. a new magic-token evidence contract was absent;
2. a new Figma-plan token was absent.

Adversarial validation rejected the naive interpretation that both missing tokens necessarily represented missing behavior:

- Base already has `MATERIAL_CLAIM_LEDGER`, `EXTERNAL_FACT`, `evidence_locator`, `Evidence ceiling`, `LATEST_EXACT_HEAD_ONLY`, `TEST_CONSUMPTION_PROOF`, and `BLOCKED_UNVERIFIED` in the existing `reviewing-and-validating-project-changes` owner.
- current `AGENTS.md` already requires latest main/current decisions/actual implementation and valid alternatives; long-horizon policy already requires multiple benchmark/practice/failure cases and `ADOPT / ADAPT / REJECT`.
- current visual policy already says Library use depends on plan/permission and rollback uses `version history 또는 사용 가능한 branch/checkpoint`; therefore Figma Branching is not a required Professional-plan dependency.

The test was corrected to lock the **existing composed owners** instead of manufacturing duplicate authority. Corrected test head began at `ce0ab2d5ed2ec4e0088bce5ea185eb56ab891c41`.

### User-clarified invariant TDD

The user then made two requirements explicit:

1. work should always use current-state research and benchmarking to consider multiple viable methods from multiple angles, then use adversarial review to select the long-term best method;
2. the currently owned paid plans are exactly GPT Pro and Figma Pro, two plans total.

A fresh test-only head was created:

```text
4984e8a37d9ab1e71830e7ad9036532ea127c3a9
Validate Base Long-Horizon Work Contract run: 32109703237
result: RED
```

The RED was expected because the previous Base expressed related principles but did not expose these two requirements as stable explicit contracts in both the top-level invariant and long-horizon execution policy.

Production implementation then added:

```text
CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY
CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO
PAID_PLAN_COUNT: 2
```

Implementation head after both policy surfaces were updated:

```text
b3682418deb763de1460e46901ddc003a50441db
```

On that exact head, the focused Long-Horizon contract, Base-v9 contract, and Game UX/UI workflow were observed `success`; the final GPO gate was still running at the time this snapshot section was written. This is a historical observation, not permission to reuse stale CI for a later head.

## 5. Exactly five executed adversarial rounds

### Round 1 — Intent / assumptions / scope

**Attack hypothesis:** The requirement could be distorted into “always perform a heavy formal benchmark report and create more Skills,” increasing ceremony rather than decision quality.

**Evidence checked:** user requirement, `AGENTS.md`, long-horizon policy, current Skill ownership, NASA guidance that decision-analysis rigor should fit decision complexity.

**Finding:** `P1` if implemented as a new broad Skill or mandatory fixed-size report.

**Disposition:** `FIXED_BY_DESIGN`. Preserve sparse owners. L1+ material decisions require real current-state/alternatives/benchmark evidence; L0 mechanical work does not manufacture a trade study. Valid alternatives are compared; fake alternatives are forbidden.

**Recheck:** regression test locks the composed owners and the explicit `CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY` contract.

**Status:** `PASS`.

### Round 2 — Canon / structure / dependency

**Attack hypothesis:** Adding another evidence/benchmark policy or cost owner would create a second canon and duplicate claim-verification semantics.

**Evidence checked:** `AGENTS.md`, `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, adversarial Skill, `claim-and-intent-verification.md`, Skill Registry model.

**Findings:**

- existing owners already divide responsibility correctly: top-level invariant/entry in `AGENTS.md`, long-horizon detailed execution in its policy, attack in adversarial review, material evidence in claim verification;
- the paid-plan statement is intentionally mirrored in the top-level invariant and long-horizon machine contract so drift is caught by regression rather than creating an independent third authority.

**Disposition:** `REJECTED_CRITIQUE` for a new broad policy/Skill or standalone paid-plan system. Use the existing authority chain and regression tests.

**Status:** `PASS`.

### Round 3 — Failure / security / concurrency / recovery

**Attack hypothesis:** Postmerge follow-up could mutate main directly, reuse stale CI, mix stale Dependabot history into the governance fix, or silently spend money through a feature nested inside an allowed subscription.

**Evidence checked:** main SHA, isolated branch, PR #517, #496 compare, exact test runs, cost wording.

**Findings:**

- #517 started from exact merged main and uses its own branch.
- #496 is 14 commits behind the #516-era main snapshot and one commit ahead, so whole-branch merge is unsafe/stale even though its material delta is only `requirements-publication.txt`.
- cancelled/old workflow evidence is not reused as current-head PASS.
- `GPT Pro`/`Figma Pro` being allowed does not authorize separately metered API, credits, marketplace, runner, compute, storage, or a higher paid tier.

**Disposition:** keep #496 out of #517; evaluate its one-line material dependency delta separately after governance closeout. No force/direct-main/bypass. New paid routes require fresh user approval.

**Status:** `PASS`.

### Round 4 — Value / benchmark / cost / maintainability

**Attack hypothesis:** “More research” can increase latency and maintenance without improving decisions; a formal trade study can become ritual; Figma guidance can accidentally assume a higher paid tier.

**Evidence checked:** NASA Decision Analysis/AoA, DORA small batches, Google small CLs, Figma official plan/branching docs, current visual policy/profile.

**Findings:**

- NASA supports defining alternatives and criteria before recommendation and explicitly says the analysis method should fit decision complexity;
- DORA and Google support bounded, self-contained implementation units for feedback, review and rollback;
- Figma Professional does not provide Branching/Merging, but Base already makes branch/checkpoint conditional and uses Pages/Sections + version history as the normal organization/recovery path;
- long-term selection should include life-cycle cost and supportability, not only immediate implementation size.

**Disposition:** `ADOPT` multi-option trade study for material decisions, `ADOPT` small-batch implementation, `REJECT` fixed-count fake alternatives, `REJECT` mandatory Figma branching, `REJECT` additional paid tool/API without new approval.

**Status:** `PASS`.

### Round 5 — Regression / evidence / completion / freshness

**Attack hypothesis:** “Benchmarking and adversarial review happened” could remain only prose while actual contracts or exact-head tests do not prove it; current paid-plan facts could drift later.

**Evidence checked:** before/after commit compare, exact source files, Tool Hub Windows smoke test, Loop current checkpoint, #516 merged main readback, #517 RED/implementation heads, current tests.

**Findings:**

- historical #516 review evidence correctly recorded its at-the-time pending gate but is not a current operational status authority;
- a current paid-plan snapshot is intentionally phrased as “current” and remains subordinate to the user’s latest instruction; if the plans change, Base must be updated rather than pretending the old count remains current;
- exact-head regression tests now require the explicit trade-study and paid-plan boundaries.

**Disposition:** this record uses `SNAPSHOT_ROLE: HISTORICAL_EVIDENCE_NOT_CURRENT_STATUS`; current repository/PR/workflow readback remains authoritative. Completion of #517 still requires a fresh exact-head GREEN after this evidence update, unresolved threads 0, merge, and postmerge main readback.

**Status:** `PASS_WITH_PROCEDURAL_GATE_PENDING`.

## 6. Current findings

```yaml
P0_remaining: 0
P1_design_or_code_remaining: 0
procedural_gate:
  - exact-head CI for PR #517 after final evidence update
  - unresolved review threads == 0
  - normal merge
  - postmerge main readback
separate_evaluated_work:
  - "PR #496: stale/diverged dependency PR; material one-line pypdf security/bugfix bump should be handled as its own bounded successor/rebase, not mixed into #517"
```
