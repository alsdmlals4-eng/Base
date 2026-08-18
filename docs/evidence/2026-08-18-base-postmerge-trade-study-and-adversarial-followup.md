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
| NASA Systems Engineering Handbook — Decision Analysis / Analysis of Alternatives (`https://www.nasa.gov/reference/6-8-decision-analysis/`, `https://www.nasa.gov/reference/system-engineering-handbook-appendix/`) | define alternatives, criteria, evaluation methods/results, cost/risk and recommendation instead of starting from one preferred answer | `ADAPT`: material Base decisions must compare viable alternatives before commitment; complexity of the trade study should match the decision |
| NASA System Design Processes (`https://www.nasa.gov/reference/4-0-system-design-processes/`) | evaluate alternative designs against effectiveness, achievability, cost, schedule and risk; rank and drop weaker alternatives | `ADAPT`: use user/player value, correctness, cost, risk, reversibility, maintenance and evidence as trade criteria |
| DORA — Working in small batches (`https://dora.dev/capabilities/working-in-small-batches/`) | small independent batches improve feedback and counter AI-assisted delivery instability | `ADOPT`: repository-wide discovery can be broad, implementation remains bounded/testable |
| Google Engineering Practices — Small CLs (`https://google.github.io/eng-practices/review/developer/small-cls.html`) | small changes are easier to review deeply, reason about, merge and roll back | `ADOPT`: do not turn a Base-wide audit into one opaque unrelated mega-change |
| Git `git-worktree` documentation (`https://git-scm.com/docs/git-worktree`) | one repository can support multiple linked working trees for different branches | `ADOPT`: isolated worktrees/branches are the standard concurrency mechanism; ownership still needs Base policy |
| Figma plan/branching documentation (`https://help.figma.com/hc/en-us/articles/360040328273-Team-plans-in-Figma`, `https://help.figma.com/hc/en-us/articles/360063144053-Guide-to-branching`) | Professional has unlimited version history; Branching/Merging is Organization/Enterprise | `ADAPT`: Figma Professional workflow uses Pages/Sections, lifecycle states and version history; branching is optional only when actually available |

## 4. Test-first evidence

Test-only head:

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

The test was corrected to lock the **existing composed owners** instead of manufacturing duplicate authority. Corrected test head begins at `ce0ab2d5ed2ec4e0088bce5ea185eb56ab891c41`.

## 5. Exactly five executed adversarial rounds

### Round 1 — Intent / assumptions / scope

**Attack hypothesis:** The latest user requirement could be distorted into “always perform a heavy formal benchmark report and create more Skills,” increasing ceremony rather than decision quality.

**Evidence checked:** user requirement, `AGENTS.md`, long-horizon policy, current Skill ownership.

**Finding:** `P1` if implemented as a new broad Skill or mandatory fixed-size report.

**Disposition:** `FIXED_BY_DESIGN`. Preserve sparse owners. Material decisions require real current-state/alternatives/benchmark evidence; trivial L0 mechanical work does not manufacture a trade study.

**Recheck:** regression test now checks existing owner composition rather than a new broad owner.

**Status:** `PASS`.

### Round 2 — Canon / structure / dependency

**Attack hypothesis:** Adding another evidence/benchmark policy would create a second canon and duplicate claim-verification semantics.

**Evidence checked:** `AGENTS.md`, `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, adversarial Skill, `claim-and-intent-verification.md`, Skill Registry model.

**Finding:** existing owners already divide responsibility correctly: planning/alternatives in entry+long-horizon; attack in adversarial review; material evidence in claim verification.

**Disposition:** `REJECTED_CRITIQUE` for a new broad policy/Skill. Add regression coverage and this evidence record instead.

**Status:** `PASS`.

### Round 3 — Failure / security / concurrency / recovery

**Attack hypothesis:** Postmerge follow-up could mutate main directly, reuse stale CI, or mix stale Dependabot history into the governance fix.

**Evidence checked:** main SHA, new isolated branch, PR #517, #496 compare, exact test run.

**Findings:**

- #517 started from exact merged main and uses its own branch.
- #496 is 14 commits behind current main and one commit ahead, so whole-branch merge is unsafe/stale even though its material delta is only `requirements-publication.txt`.
- cancelled/old workflow evidence is not being reused as current-head PASS.

**Disposition:** keep #496 out of #517; evaluate its one-line material dependency delta separately after governance closeout. No force/direct-main/bypass.

**Status:** `PASS`.

### Round 4 — Value / benchmark / cost / maintainability

**Attack hypothesis:** “More research” can increase latency and maintenance without improving decisions; Figma guidance can accidentally assume a higher paid tier.

**Evidence checked:** NASA trade studies, DORA small batches, Google small CLs, Figma official plan/branching docs, current visual policy/profile.

**Findings:**

- multiple alternatives and explicit criteria improve material decisions, but the analysis method should scale with decision complexity;
- implementation should remain in bounded batches even when discovery is repository-wide;
- Figma Professional does not provide Branching/Merging, but Base already makes branch/checkpoint conditional and uses Pages/Sections + version history as the normal organization/recovery path.

**Disposition:** `ADOPT` multi-option trade study for material decisions, `ADOPT` small-batch implementation, `REJECT` mandatory Figma branching, `REJECT` additional paid tool/API.

**Status:** `PASS`.

### Round 5 — Regression / evidence / completion / freshness

**Attack hypothesis:** “Benchmarking and adversarial review happened” could remain only prose while the actual repository contracts or exact-head tests do not prove it.

**Evidence checked:** before/after commit compare, exact source files, Tool Hub Windows smoke test, Loop current checkpoint, #516 merged main readback, #517 test-only RED.

**Finding:** historical #516 review evidence correctly recorded its at-the-time pending gate but is not a current operational status authority. A follow-up snapshot must clearly declare itself historical and direct current status checks back to repository main/PR/workflows.

**Disposition:** this record uses `SNAPSHOT_ROLE: HISTORICAL_EVIDENCE_NOT_CURRENT_STATUS`. Completion of #517 still requires fresh exact-head GREEN, unresolved threads 0, merge, and postmerge main readback.

**Status:** `PASS_WITH_PROCEDURAL_GATE_PENDING`.

## 6. Current findings

```yaml
P0_remaining: 0
P1_design_or_code_remaining: 0
procedural_gate:
  - exact-head CI for PR #517
  - unresolved review threads == 0
  - normal merge
  - postmerge main readback
separate_evaluated_work:
  - "PR #496: stale/diverged dependency PR; material one-line pypdf security/bugfix bump should be handled as its own bounded successor/rebase, not mixed into #517"
```
