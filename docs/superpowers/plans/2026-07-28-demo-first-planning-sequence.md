# Demo-First Planning Sequence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base의 기획 작업을 누락·충돌 선감사, 근거 묶음, 분야별 승인 묶음, 소비처 전파 검증 순서로 재구성하고, 별도 `CORE_POC` 단계 없이 완성 품질의 Vertical Slice 데모를 직접 제작·플레이테스트하는 기본 경로를 확정한다.

**Architecture:** `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`를 공용 정책 원본으로 추가하고, 기존 승인 동기화·작업 분해·근거 조사·Vertical Slice Gate 문서가 이 정책을 소비하도록 연결한다. 프로젝트 Google Sheets는 Base 자체에는 적용하지 않고 개별 프로젝트에서만 탭 구조 Template을 설치한다. 기존 PoC 분석 능력은 제거하지 않되, 별도 제품 단계가 아닌 Vertical Slice 내부의 선택적 기술 spike로만 허용한다.

**Tech Stack:** Markdown policy and templates, Base Skill references, Python unittest regression checks, GitHub Branch/PR/Actions

## Global Constraints

- Base 저장소 자체는 프로젝트 Google Sheets 동기화 대상에서 제외한다.
- 개별 프로젝트만 Sheet URL이 있을 때 프로젝트 탭과 Decision 동기화를 수행한다.
- 문서·Skill의 줄 수·문자 수·분량 상한을 두지 않는다.
- 내용 보존, 실행 가능성, 한 단계 발견성, 소비처 전파가 간결성보다 우선한다.
- 모든 L1 이상 작업은 이전 기록과 비교해 중복·누락·충돌·구형 참조·미반영을 먼저 판정한다.
- 모든 중요 기획 묶음은 벤치마킹·플레이어 반응·현업 또는 공식 권장 근거를 포함한다.
- 유사한 결정은 분야별 Approval Bundle로 묶어 승인하고, 승인 뒤 정본·소비처·개별 프로젝트 Sheet를 갱신한다.
- 별도 `CORE_POC` 제품 단계는 사용하지 않는다.
- 첫 통합 플레이 제품은 제작 의도 자산과 최종 방향 품질을 갖춘 Vertical Slice 데모다.
- 기술 불확실성 검사는 Vertical Slice 내부의 제한된 spike로만 수행하며 별도 Gate나 폐기형 데모가 아니다.

---

### Task 1: Planning sequence and evidence canonical policy

**Files:**
- Create: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`, current Work Mode and Skill routing, project operating system contracts
- Produces: pre-work audit statuses, evidence pack, Approval Bundle sequence, propagation audit, project sheet scope, demo-first milestone order

- [ ] **Step 1:** Write the policy with `BASE_EXCLUDED`, `PROJECT_SHEET_CONFIGURED`, and `NOT_CONFIGURED` Sheet scope states.
- [ ] **Step 2:** Define pre-work statuses for duplicate work, duplicate questions, missing canon, missing consumers, canon conflict, implementation conflict, stale references, and no conflict.
- [ ] **Step 3:** Define the eight-stage loop: baseline recovery, audit, evidence pack, approval bundle, canonical update, propagation audit, validation, gate close.
- [ ] **Step 4:** Define the approved project planning order and per-project Sheet tab names.
- [ ] **Step 5:** Link the new policy from always-read entrypoints and Documentation Map.

### Task 2: Remove compact-size authority without losing progressive disclosure

**Files:**
- Modify: `skills/simplifying-skill-bodies/SKILL.md`
- Modify: `skills/simplifying-skill-bodies/references/progressive-disclosure-rules.md`
- Modify: `tests/test_skill_system_coverage.py`

**Interfaces:**
- Consumes: current progressive-disclosure responsibility split
- Produces: completeness-first Skill organization with no numeric size ceiling

- [ ] **Step 1:** State that line, character, and document-length limits are prohibited as completion criteria.
- [ ] **Step 2:** Preserve one-hop discoverability and responsibility-based reference extraction.
- [ ] **Step 3:** Replace the 150-line regression assertion with checks for no-loss and discoverability language.

### Task 3: Pre-work comparison, evidence pack, and Approval Bundles

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md`
- Modify: `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`
- Create: `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`

**Interfaces:**
- Consumes: approved work contract, current decisions, repository and project Sheet state
- Produces: ordered discipline bundles with evidence and propagation gates

- [ ] **Step 1:** Require duplicate·omission·conflict audit before decomposition.
- [ ] **Step 2:** Define Approval Bundle fields, dependencies, evidence IDs, and gate close states.
- [ ] **Step 3:** Require benchmark, player-reaction, and professional/official evidence for material design bundles while exempting mechanical L0 changes.
- [ ] **Step 4:** Add the project Sheet tab template and common columns.

### Task 4: Demo-first Vertical Slice contract

**Files:**
- Modify: `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md`
- Modify: `docs/knowledge/VERTICAL_SLICE_V6_REQUIREMENT_COVERAGE.md`
- Modify: `templates/planning/VERTICAL_SLICE_PLAN.md`
- Modify: `tests/test_vertical_slice_v6_contract.py`

**Interfaces:**
- Consumes: approved concept, discipline bundles, target quality, production constraints
- Produces: production-intent Vertical Slice demo and playtest evidence without a standalone Core PoC milestone

- [ ] **Step 1:** Replace the `CORE_POC → ...` product flow with demo contract → production-intent build → integrated QA → internal/external playtest → demo validation.
- [ ] **Step 2:** Remove mandatory Core PoC deliverables and replace them with a demo critical-risk register.
- [ ] **Step 3:** Allow only bounded technical spikes inside the Slice when needed; they cannot become a separate product gate or disposable milestone.
- [ ] **Step 4:** Update coverage and regression expectations to mark the old Core PoC stage as superseded by the latest user decision.

### Task 5: Registry, learning, entrypoints, and regression integration

**Files:**
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `templates/project-operations/README.md`
- Modify: `docs/CHANGELOG.md`
- Create: `tests/test_demo_first_planning_sequence.py`

**Interfaces:**
- Consumes: all changed policies, references, and templates
- Produces: discoverable routing, change history, and regression protection

- [ ] **Step 1:** Update affected Skill triggers and review triggers without creating duplicate Skill IDs.
- [ ] **Step 2:** Record lessons for completeness-first organization, consumer propagation, evidence packs, and demo-first Vertical Slice.
- [ ] **Step 3:** Add regression tests for Base Sheet exclusion, no compact ceiling, audit-before-work, three-layer evidence, tab order, propagation audit, and no standalone Core PoC stage.
- [ ] **Step 4:** Run repository CI and fix only validated compatibility findings.

### Task 6: Merge and post-merge adversarial review

**Files:**
- Review: all changed files
- Validate: GitHub Actions and new `main`

**Interfaces:**
- Consumes: PR diff, CI evidence, merged main HEAD
- Produces: final conflict report and branch cleanup evidence

- [ ] **Step 1:** Confirm there is no duplicate open PR or overlapping Goal.
- [ ] **Step 2:** Run documentation, reference freshness, contract/governance, publication, and `ci-gate` checks.
- [ ] **Step 3:** Squash merge after validation.
- [ ] **Step 4:** Re-read new `main` and verify every new policy/template is consumed by entrypoints, Skills, templates, and tests.
- [ ] **Step 5:** Report `NO_CONFLICT`, `CONFLICT_FIXED`, `USER_DECISION_REQUIRED`, or `BLOCKED_UNVERIFIED` with evidence.
