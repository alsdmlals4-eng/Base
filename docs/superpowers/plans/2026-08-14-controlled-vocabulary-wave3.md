# Controlled Vocabulary Wave 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the existing Base controlled vocabulary with six bounded technical-development term groups while preserving one canonical terminology surface and semantic regression coverage.

**Architecture:** Keep `docs/CONTROLLED_VOCABULARY.md` as the single `BASE_SHARED` terminology canon. Add only semantic documentation and tests; do not introduce runtime behavior, a new Skill, Registry entry, Schema, route, workflow, or project migration. Use GitHub Actions on a Draft PR as the executable RED/GREEN evidence source.

**Tech Stack:** Markdown, Python `unittest`, GitHub Actions, GitHub connector.

## Global Constraints

- Baseline: `0701cfb6c3bcbdd81df92a313025c03e4154e574` unless `main` moves before merge.
- Expected final changed paths are exactly five:
  - `docs/CONTROLLED_VOCABULARY.md`
  - `docs/CHANGELOG.md`
  - `docs/superpowers/specs/2026-08-14-controlled-vocabulary-wave3-design.md`
  - `docs/superpowers/plans/2026-08-14-controlled-vocabulary-wave3.md`
  - `tests/test_controlled_vocabulary_contract.py`
- Do not modify `AGENTS.md`, `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`, `skills/**`, `skills/SKILL_REGISTRY.json`, `schemas/**`, `.github/workflows/**`, released/generated artifacts, or project product files.
- Preserve all Wave 1/2 terminology and canonical-row uniqueness.
- `Metrics` is the only added companion term beyond the previously approved candidate list.
- No runtime, render, device, gameplay, player-experience, deployment, or store PASS may be inferred from documentation tests.

---

### Task 1: Add Wave 3 semantic RED contracts

**Files:**
- Modify: `tests/test_controlled_vocabulary_contract.py`

**Interfaces:**
- Consumes: existing `VOCABULARY` path and `unittest` pattern.
- Produces: seven semantic tests that fail only because Wave 3 vocabulary is absent or under-specified.

- [ ] **Step 1: Add work-tracking boundary test**

```python
def test_work_tracking_terms_separate_issue_bug_defect_and_incident(self) -> None:
    vocabulary = VOCABULARY.read_text(encoding="utf-8")
    for term in ("Issue", "Bug", "Defect", "Incident"):
        self.assertIn(term, vocabulary)

    self.assertIn("Issue ≠ Bug", vocabulary)
    self.assertIn("Incident ≠ 개별 Bug/Defect", vocabulary)
    self.assertIn(
        "Bug와 Defect를 모든 조직에서 완전히 동일하거나 완전히 다른 용어로 강제하지 않는다",
        vocabulary,
    )
```

- [ ] **Step 2: Add requirement boundary test**

```python
def test_requirement_terms_separate_requirement_specification_and_constraint(self) -> None:
    vocabulary = VOCABULARY.read_text(encoding="utf-8")
    for term in ("Requirement", "Specification", "Constraint"):
        self.assertIn(term, vocabulary)

    self.assertIn("Requirement ≠ Specification", vocabulary)
    self.assertIn("Constraint를 Requirement의 보편적 하위형으로 강제하지 않는다", vocabulary)
    self.assertIn("Acceptance Criteria ≠ Requirement 전체", vocabulary)
```

- [ ] **Step 3: Add dependency/coupling/cohesion boundary test**

```python
def test_structure_terms_distinguish_dependency_coupling_and_cohesion(self) -> None:
    vocabulary = VOCABULARY.read_text(encoding="utf-8")
    for term in ("Dependency", "Coupling", "Cohesion"):
        self.assertIn(term, vocabulary)

    self.assertIn("Dependency 존재 ≠ Tight Coupling 확정", vocabulary)
    self.assertIn("Coupling = 모듈 간 상호의존 정도", vocabulary)
    self.assertIn("Cohesion = 한 모듈 내부 책임들의 논리적 관련성", vocabulary)
```

- [ ] **Step 4: Add API/ABI/protocol/schema boundary test**

```python
def test_interface_terms_distinguish_api_abi_protocol_and_schema(self) -> None:
    vocabulary = VOCABULARY.read_text(encoding="utf-8")
    for term in ("API", "ABI", "Protocol", "Schema"):
        self.assertIn(term, vocabulary)

    self.assertIn("API compatibility ≠ ABI compatibility", vocabulary)
    self.assertIn("Protocol ≠ Endpoint 목록", vocabulary)
    self.assertIn("Schema ≠ Protocol", vocabulary)
    self.assertIn("OpenAPI ≠ 모든 종류의 API", vocabulary)
    self.assertIn("JSON Schema ≠ 모든 종류의 Schema", vocabulary)
```

- [ ] **Step 5: Add build/package/artifact/deployment/release boundary test**

```python
def test_delivery_terms_distinguish_build_package_artifact_deployment_and_release(self) -> None:
    vocabulary = VOCABULARY.read_text(encoding="utf-8")
    for term in ("Build", "Package", "Artifact", "Deployment", "Release"):
        self.assertIn(term, vocabulary)

    self.assertIn("Build process ≠ Build output", vocabulary)
    self.assertIn("Artifact ≠ Package", vocabulary)
    self.assertIn("Deployment ≠ Release", vocabulary)
    self.assertIn("Release Candidate ≠ Release", vocabulary)
```

- [ ] **Step 6: Add observability-signal boundary test**

```python
def test_observability_terms_distinguish_telemetry_metrics_logs_traces_and_profiles(self) -> None:
    vocabulary = VOCABULARY.read_text(encoding="utf-8")
    for term in ("Telemetry", "Metrics", "Logging / Logs", "Tracing / Traces", "Profiling / Profiles"):
        self.assertIn(term, vocabulary)

    self.assertIn("Metrics ≠ Logs", vocabulary)
    self.assertIn("Logs ≠ Traces", vocabulary)
    self.assertIn("Tracing ≠ Profiling", vocabulary)
    self.assertIn("관측 signal 존재 ≠ 원인 규명 완료", vocabulary)
```

- [ ] **Step 7: Add overclaim/canonical uniqueness test**

```python
def test_wave3_preserves_canonical_rows_and_context_limits(self) -> None:
    vocabulary = VOCABULARY.read_text(encoding="utf-8")

    self.assertEqual(vocabulary.count("| **Release Candidate** |"), 1)
    self.assertEqual(vocabulary.count("| **Regression Recheck** |"), 1)
    self.assertEqual(vocabulary.count("| **Release** |"), 1)
    self.assertIn("ARTIFACT Kind ≠ Build Artifact", vocabulary)
    self.assertIn("OpenTelemetry Profiles의 Alpha 상태 ≠ Profiling 일반의 Alpha 상태", vocabulary)
```

- [ ] **Step 8: Commit test-only RED**

Use GitHub contents update on `feat/controlled-vocabulary-wave3-20260814` with commit message:

```text
test: define controlled vocabulary wave3 contracts
```

Expected state: only the spec, plan, and test file differ from baseline; production vocabulary remains unchanged.

---

### Task 2: Capture executable RED evidence

**Files:**
- No additional file edits.

**Interfaces:**
- Consumes: Task 1 test-only head.
- Produces: GitHub Actions evidence proving the new tests fail for missing Wave 3 semantics while Wave 1/2 tests remain green.

- [ ] **Step 1: Open Draft PR**

Create a Draft PR from `feat/controlled-vocabulary-wave3-20260814` to `main` with the changed-path contract and RED expectation in the body.

- [ ] **Step 2: Read `ubuntu-contract` result and logs**

Expected:

```text
existing Wave 1/2 controlled-vocabulary tests: PASS
new Wave 3 tests: FAIL
failure cause: missing Wave 3 terms/boundaries, not syntax/proposal/freshness harness failure
```

- [ ] **Step 3: Stop if failure is unrelated**

If syntax, canonical freshness, or an existing Wave 1/2 test fails, classify it before production edits. Do not make vocabulary changes to mask a harness or concurrent-main problem.

---

### Task 3: Implement six Wave 3 vocabulary sections

**Files:**
- Modify: `docs/CONTROLLED_VOCABULARY.md`
- Test: `tests/test_controlled_vocabulary_contract.py`

**Interfaces:**
- Consumes: seven Wave 3 semantic tests.
- Produces: one canonical row per new term and explicit confusion-prevention text.

- [ ] **Step 1: Add `작업·결함·운영 문제` section**

Rows:

```text
Issue — INDUSTRY_COMMON + GitHub platform context
Bug — INDUSTRY_COMMON
Defect — INDUSTRY_COMMON / testing context
Incident — INDUSTRY_COMMON / SRE operations context
```

Required text:

```text
Issue ≠ Bug
Incident ≠ 개별 Bug/Defect
Bug와 Defect를 모든 조직에서 완전히 동일하거나 완전히 다른 용어로 강제하지 않는다.
```

- [ ] **Step 2: Add `요구·명세·제약` section**

Rows:

```text
Requirement
Specification
Constraint
```

Required text:

```text
Requirement ≠ Specification
Constraint를 Requirement의 보편적 하위형으로 강제하지 않는다.
Acceptance Criteria ≠ Requirement 전체
```

- [ ] **Step 3: Add `구조·의존 관계` section**

Rows:

```text
Dependency
Coupling
Cohesion
```

Required text:

```text
Dependency 존재 ≠ Tight Coupling 확정
Coupling = 모듈 간 상호의존 정도
Cohesion = 한 모듈 내부 책임들의 논리적 관련성
High Cohesion / Low Coupling은 설계 휴리스틱이며 단독 품질 PASS 증거가 아니다.
```

- [ ] **Step 4: Add `인터페이스·호환성·데이터 계약` section**

Rows:

```text
API
ABI
Protocol
Schema
```

Required text:

```text
API ≠ Web API만
API compatibility ≠ ABI compatibility
Protocol ≠ Endpoint 목록
Schema ≠ Protocol
OpenAPI ≠ 모든 종류의 API
JSON Schema ≠ 모든 종류의 Schema
```

- [ ] **Step 5: Add `빌드·산출물·배포·출시` section**

Rows:

```text
Build
Package
Artifact
Deployment
Release
```

Required text:

```text
Build process ≠ Build output
Artifact ≠ Package
Deployment ≠ Release
Release Candidate ≠ Release
ARTIFACT Kind ≠ Build Artifact
```

The `Artifact` row must state that workflow/test/evidence outputs can be artifacts and that not all artifacts are installable/distributable packages.

- [ ] **Step 6: Add `관측·진단` section**

Rows:

```text
Telemetry
Metrics
Logging / Logs
Tracing / Traces
Profiling / Profiles
```

Required text:

```text
Metrics ≠ Logs
Logs ≠ Traces
Tracing ≠ Profiling
관측 signal 존재 ≠ 원인 규명 완료
OpenTelemetry Profiles의 Alpha 상태 ≠ Profiling 일반의 Alpha 상태
```

- [ ] **Step 7: Extend `자주 헷갈리는 구분` and `금지 용례`**

Add only the Wave 3 high-value confusion boundaries; do not duplicate every table sentence.

- [ ] **Step 8: Commit production vocabulary**

Commit message:

```text
docs: expand controlled vocabulary for technical development
```

---

### Task 4: Record change and verify GREEN

**Files:**
- Modify: `docs/CHANGELOG.md`
- Test: `tests/test_controlled_vocabulary_contract.py`

**Interfaces:**
- Consumes: production vocabulary from Task 3.
- Produces: changelog trace and exact-head GREEN evidence.

- [ ] **Step 1: Add one Unreleased changelog bullet**

The bullet must state:

```text
Expanded the existing BASE_SHARED controlled vocabulary with work-tracking, requirements, dependency-design, interface/compatibility, build/delivery, and observability terms without adding a new Skill, Registry entry, Schema, route, workflow, or terminology framework.
```

- [ ] **Step 2: Commit changelog**

Commit message:

```text
docs: record controlled vocabulary wave3
```

- [ ] **Step 3: Read exact-head CI**

Required success on the same head:

```text
docs-validation
ubuntu-contract
publication-validation
base-v9-contract
adversarial-gate
ci-gate
```

A skipped PR Windows job is not Windows runtime evidence.

---

### Task 5: Run adversarial review and TDD any finding

**Files:**
- Modify only `docs/CONTROLLED_VOCABULARY.md` and/or `tests/test_controlled_vocabulary_contract.py` if a validated in-scope finding exists.

**Interfaces:**
- Consumes: exact diff, approved scope, current canon, official-source boundaries.
- Produces: `attack → validate-critique → refine-approved-findings → regression-recheck → decision-report` evidence.

- [ ] **Step 1: Attack the specific failure modes**

Check:

```text
Issue collapsed into Bug
Bug/Defect false universal distinction
Incident severity overclaim
Requirement/Specification/Constraint false hierarchy
Dependency presence treated as tight coupling
API/ABI compatibility collapse
OpenAPI/JSON Schema universalization
Artifact/Package collapse
Deployment/Public Release collapse
Release Candidate duplicate row
Telemetry signals collapsed together
OpenTelemetry Profiles Alpha generalized to all profiling
signal existence promoted to root-cause proof
```

- [ ] **Step 2: Validate criticisms**

Only keep `MUST_FIX` or in-scope high-value `SHOULD_FIX`. Reject preference-only wording changes and scope expansion.

- [ ] **Step 3: For a valid semantic flaw, add failing regression first**

Expected RED: only the newly added adversarial assertion fails.

- [ ] **Step 4: Make the minimum vocabulary fix**

Do not add new terms or new files to satisfy a narrow finding unless the approved scope requires it.

- [ ] **Step 5: Re-run exact-head CI and record P0/P1**

Required before merge:

```text
P0 = 0
P1 = 0
unresolved review threads = 0
```

---

### Task 6: Freshness, merge, and post-merge closure

**Files:**
- No planned new paths.

**Interfaces:**
- Consumes: reviewed exact head and current `main`.
- Produces: merged `main` with post-merge evidence.

- [ ] **Step 1: Re-read current `main` and open PRs**

Compare the original/current merge base with latest `main`. Compute actual path intersection with all same-goal or adjacent open PRs.

- [ ] **Step 2: If `main` moved with zero path overlap, synchronize without force**

Use the latest `main` tree plus the exact reviewed five Wave 3 blobs. Preserve concurrent changes byte-for-byte outside the Wave 3 paths.

- [ ] **Step 3: Verify final exact-head checks and review threads**

Required:

```text
branch behind latest main = 0
changed paths = exactly 5
P0/P1 = 0
unresolved review threads = 0
required checks = success
```

- [ ] **Step 4: Mark PR ready and merge with expected head SHA**

Use squash merge and bind the expected head SHA.

- [ ] **Step 5: Read merged main**

Confirm:

```text
main SHA = merge SHA
all six Wave 3 sections exist
Wave 1/2 canonical rows remain unique
Wave 3 semantic tests are present
changelog entry exists
```

- [ ] **Step 6: Verify post-merge push full matrix**

Required success:

```text
base-v9-contract
adversarial-gate
docs-validation
ubuntu-contract
publication-validation
platform-smoke-windows
ci-gate
```

- [ ] **Step 7: Report evidence limits and rollback**

State that the change improves terminology/context compression only; it does not prove product runtime, gameplay, player experience, deployment, or store readiness. Rollback is one squash-merge revert.
