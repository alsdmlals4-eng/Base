# 에이전트 명세·디자인·외부 UI 조달 통합 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 기존 Base owner를 유지하면서 L2 이상 명세 추적성, 교차 분야 적대 검토 Lens, 프로젝트 선택형 DESIGN.md, 외부 UI 코드 조달·anti-generic 검수 계약을 추가한다.

**Architecture:** 새 활성 Skill을 만들지 않는다. intake·design documents·validation·adversarial review·UI audit의 기존 mode와 output contract에 얇은 route를 추가하고, 상세 절차는 세 Reference와 두 Project Template으로 분리한다. 구현은 이 BCP가 `APPROVED_FOR_IMPLEMENTATION`으로 승인된 뒤 최신 main에서 별도 Draft PR로 수행한다.

**Tech Stack:** Markdown contracts, JSON Registry invariants, Python `pytest`, Base reference-freshness and local validation tools

## Global Constraints

- `skills/SKILL_REGISTRY.json`은 byte-identical을 기본 계약으로 유지한다.
- 새 ACTIVE Skill을 추가하지 않는다.
- L0·L1 변경에는 명세 추적성 Packet과 전체 Lens를 강제하지 않는다.
- Requirement Packet은 상세 책임 원본이 아니라 ID 연결·coverage 검사 산출물이다.
- 프로젝트 `DESIGN.md`는 시각 token만 소유하고 `GAME_UX_UI_SYSTEM`의 경험·흐름·상태·접근성·Godot 권위를 대체하지 않는다.
- Google Labs DESIGN.md `alpha` 형식은 exact source release 또는 commit과 확인일을 기록한다.
- 외부 MCP·Registry·CLI·Skill은 기본 설치하지 않고 source·license·hash·dependency·script·secret·overwrite·rollback 검토 뒤 승인한다.
- 유명 브랜드 참고 자료의 로고·상표·사진·고유 일러스트·저작물을 복제하지 않는다.
- 구현 PR은 BCP 제안 PR과 분리한다.
- 런타임·실기기·사람 검증을 실행하지 않았으면 `NOT_RUN` 또는 `HUMAN_NOT_RUN`으로 유지한다.

---

### Task 1: L2 이상 Feature Spec Traceability Packet

**Files:**
- Create: `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/managing-design-documents/SKILL.md`
- Modify: `skills/reviewing-and-validating-project-changes/SKILL.md`
- Test: `tests/test_feature_spec_traceability_contract.py`

**Interfaces:**
- Consumes: existing Decision ID, registered canonical source, approved work contract, actual implementation paths and validation artifacts
- Produces: `requirement_id`, `acceptance_criteria_ids`, `task_ids`, `implementation_paths`, `verification_ids`, `coverage_status`

- [ ] **Step 1: Write the failing contract test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_traceability_packet_is_l2_plus_and_noncanonical():
    template = (ROOT / "templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md").read_text(encoding="utf-8")
    assert "L2 이상" in template
    assert "별도 책임 원본이 아니다" in template
    for token in (
        "decision_id",
        "requirement_id",
        "acceptance_criteria_ids",
        "task_ids",
        "implementation_paths",
        "verification_ids",
        "coverage_status",
        "BLOCKED_UNVERIFIED",
    ):
        assert token in template

def test_existing_owners_route_traceability_without_new_skill():
    intake = (ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md").read_text(encoding="utf-8")
    docs = (ROOT / "skills/managing-design-documents/SKILL.md").read_text(encoding="utf-8")
    validation = (ROOT / "skills/reviewing-and-validating-project-changes/SKILL.md").read_text(encoding="utf-8")
    assert "FEATURE_SPEC_TRACEABILITY_PACKET.md" in intake
    assert "FEATURE_SPEC_TRACEABILITY_PACKET.md" in docs
    assert "FEATURE_SPEC_TRACEABILITY_PACKET.md" in validation
```

- [ ] **Step 2: Run the focused test and confirm RED**

```bash
python -m pytest tests/test_feature_spec_traceability_contract.py -q
```

Expected: FAIL because the Template and owner routes do not exist.

- [ ] **Step 3: Add the minimal Packet and owner routes**

The Template must contain:

```yaml
decision_id:
scope_level: L2 | L3 | L4
canonical_sources: []
requirements:
  - requirement_id:
    statement:
    acceptance_criteria_ids: []
    task_ids: []
    implementation_paths: []
    verification_ids: []
    coverage_status: CONVERGED | GAP | BLOCKED_UNVERIFIED
unmapped_items: []
result: PASS | PARTIAL | FAIL | BLOCKED
```

Each owner Skill receives only its phase responsibility: intake creates IDs and scope, design documents links canon, validation compares actual implementation and evidence.

- [ ] **Step 4: Run focused GREEN**

```bash
python -m pytest tests/test_feature_spec_traceability_contract.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit Task 1**

```bash
git add templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md \
  skills/managing-project-intake-and-work-contract/SKILL.md \
  skills/managing-design-documents/SKILL.md \
  skills/reviewing-and-validating-project-changes/SKILL.md \
  tests/test_feature_spec_traceability_contract.py
git commit -m "feat: add L2 feature traceability contract"
```

### Task 2: Cross-Discipline Adversarial Review Lenses

**Files:**
- Create: `skills/running-adversarial-review-and-refinement/references/cross-discipline-review-lenses.md`
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`
- Test: `tests/test_cross_discipline_review_lenses.py`

**Interfaces:**
- Consumes: approved scope, affected disciplines, Requirement IDs, canonical sources and actual diff
- Produces: Finding with `lens`, `evidence`, `affected_requirement`, `severity`, `owner_skill`, `status`

- [ ] **Step 1: Write the failing Lens contract test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_review_lenses_preserve_single_owner_and_selective_use():
    reference = (ROOT / "skills/running-adversarial-review-and-refinement/references/cross-discipline-review-lenses.md").read_text(encoding="utf-8")
    for lens in (
        "제품·플레이어 가치",
        "UX·접근성",
        "아키텍처·상태 소유권",
        "구현·성능·플랫폼",
        "QA·회귀·출시",
        "문서·추적성·인수인계",
    ):
        assert lens in reference
    assert "결정을 소유하지 않는다" in reference
    assert "L2 이상" in reference
```

- [ ] **Step 2: Run the focused test and confirm RED**

```bash
python -m pytest tests/test_cross_discipline_review_lenses.py -q
```

Expected: FAIL because the Reference is missing.

- [ ] **Step 3: Add selective Lens routing**

The Reference must define relevance selection, non-applicable recording, Finding schema, owner handoff and rejection of duplicate Named Agent authority. The main Skill links the Reference only for L2+ multi-discipline attack or repository-wide audit.

- [ ] **Step 4: Run focused GREEN**

```bash
python -m pytest tests/test_cross_discipline_review_lenses.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit Task 2**

```bash
git add skills/running-adversarial-review-and-refinement/SKILL.md \
  skills/running-adversarial-review-and-refinement/references/cross-discipline-review-lenses.md \
  tests/test_cross_discipline_review_lenses.py
git commit -m "feat: add cross-discipline adversarial lenses"
```

### Task 3: Optional Project DESIGN.md Adapter

**Files:**
- Create: `skills/auditing-and-refining-ui-art/references/design-md-project-adapter.md`
- Create: `templates/planning/PROJECT_DESIGN_MD_TEMPLATE.md`
- Modify: `skills/auditing-and-refining-ui-art/SKILL.md`
- Modify: `skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md`
- Modify: `templates/planning/GAME_UX_UI_SYSTEM.md`
- Test: `tests/test_project_design_md_adapter.py`

**Interfaces:**
- Consumes: approved visual direction, GAME_UX_UI_SYSTEM, target platform, existing Theme/CSS, source format identity and provenance
- Produces: project-root `DESIGN.md` visual token canon with engine/web mappings and validation state

- [ ] **Step 1: Write the failing Adapter test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_design_md_template_is_visual_only_and_version_pinned():
    template = (ROOT / "templates/planning/PROJECT_DESIGN_MD_TEMPLATE.md").read_text(encoding="utf-8")
    for token in (
        "format_version",
        "source_commit_or_release",
        "last_verified_at",
        "colors:",
        "typography:",
        "spacing:",
        "components:",
        "godot_theme_mapping",
        "web_token_mapping",
        "reference_provenance",
    ):
        assert token in template
    assert "게임 규칙" in template
    assert "소유하지 않는다" in template

def test_game_ux_ui_remains_behavior_owner():
    ux = (ROOT / "templates/planning/GAME_UX_UI_SYSTEM.md").read_text(encoding="utf-8")
    assert "DESIGN.md" in ux
    assert "시각 토큰" in ux
    assert "플레이어 경험" in ux
```

- [ ] **Step 2: Run the focused test and confirm RED**

```bash
python -m pytest tests/test_project_design_md_adapter.py -q
```

Expected: FAIL because the Adapter and Template are missing.

- [ ] **Step 3: Implement the visual-only Template and mapping rules**

Use Google Labs DESIGN.md-compatible front matter fields where practical, but add Base metadata for exact source identity, Godot/Web mapping, provenance, accessibility constraints and validation status. Do not copy third-party example prose or brand assets.

- [ ] **Step 4: Run focused GREEN**

```bash
python -m pytest tests/test_project_design_md_adapter.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit Task 3**

```bash
git add skills/auditing-and-refining-ui-art/SKILL.md \
  skills/auditing-and-refining-ui-art/references/design-md-project-adapter.md \
  skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md \
  templates/planning/PROJECT_DESIGN_MD_TEMPLATE.md \
  templates/planning/GAME_UX_UI_SYSTEM.md \
  tests/test_project_design_md_adapter.py
git commit -m "feat: add optional project DESIGN.md adapter"
```

### Task 4: External UI Procurement and Anti-Generic Quality Gate

**Files:**
- Create: `skills/auditing-and-refining-ui-art/references/external-ui-procurement-and-anti-generic-quality.md`
- Modify: `skills/auditing-and-refining-ui-art/SKILL.md`
- Test: `tests/test_external_ui_procurement_gate.py`

**Interfaces:**
- Consumes: external registry/MCP item, exact source identity, project UX/UI and DESIGN.md, actual diff and rendered output
- Produces: procurement decision `ADOPT | ADAPT | REJECT | BLOCKED_UNVERIFIED` and quality Findings

- [ ] **Step 1: Write the failing procurement test**

```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_external_ui_gate_is_fail_closed_and_platform_aware():
    reference = (ROOT / "skills/auditing-and-refining-ui-art/references/external-ui-procurement-and-anti-generic-quality.md").read_text(encoding="utf-8")
    for token in (
        "registry_source",
        "exact_version_or_commit",
        "content_hash",
        "license",
        "dependencies",
        "scripts",
        "secrets",
        "files_added_or_replaced",
        "accessibility_review",
        "runtime_review",
        "rollback",
        "BLOCKED_UNVERIFIED",
    ):
        assert token in reference
    assert "MCP 연결 성공" in reference
    assert "설치 승인" in reference
    assert "Godot" in reference
    assert "Web" in reference
```

- [ ] **Step 2: Run the focused test and confirm RED**

```bash
python -m pytest tests/test_external_ui_procurement_gate.py -q
```

Expected: FAIL because the Reference is missing.

- [ ] **Step 3: Add procurement and quality rules**

The Reference must separate source admission from visual quality. Anti-generic checks require a project-specific Design Read and real render evidence; intended gradients, cards, glass or asymmetry are not defects merely because a third-party taste guide discourages them.

- [ ] **Step 4: Run focused GREEN**

```bash
python -m pytest tests/test_external_ui_procurement_gate.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit Task 4**

```bash
git add skills/auditing-and-refining-ui-art/SKILL.md \
  skills/auditing-and-refining-ui-art/references/external-ui-procurement-and-anti-generic-quality.md \
  tests/test_external_ui_procurement_gate.py
git commit -m "feat: gate external UI code and anti-generic review"
```

### Task 5: Governance, Learning, and Full Verification

**Files:**
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/OPERATING_MODEL.md` only if discoverability requires one concise route
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `skills/SKILL_IMPLEMENTATION_EVIDENCE.json` only when new executable evidence paths are required
- Modify: existing Base operating regression test selected from current main
- Verify unchanged: `skills/SKILL_REGISTRY.json`
- Verify unchanged: released lock and frozen snapshots

**Interfaces:**
- Consumes: Task 1–4 files and tests
- Produces: discoverable owner routes, learning record, exact validation evidence, rollback-ready Draft PR

- [ ] **Step 1: Capture immutable baseline hashes**

```bash
sha256sum skills/SKILL_REGISTRY.json > /tmp/bcp008-registry-before.sha256
sha256sum base.lock.json base-v9.4.lock.json > /tmp/bcp008-locks-before.sha256
```

- [ ] **Step 2: Add only required discoverability and learning links**

Documentation Map points users to the existing owner Skills and new Templates/References without duplicating their procedures. Learning Log records external source versions, rejected full-framework adoption, non-selection conditions and Pilot status.

- [ ] **Step 3: Run focused contract tests**

```bash
python -m pytest \
  tests/test_feature_spec_traceability_contract.py \
  tests/test_cross_discipline_review_lenses.py \
  tests/test_project_design_md_adapter.py \
  tests/test_external_ui_procurement_gate.py -q
```

Expected: PASS.

- [ ] **Step 4: Verify Registry and released locks are unchanged**

```bash
sha256sum -c /tmp/bcp008-registry-before.sha256
sha256sum -c /tmp/bcp008-locks-before.sha256
```

Expected: all files `OK`.

- [ ] **Step 5: Run Base validation**

```bash
git diff --check
python tools/check_skill_behavior_evals.py
python tools/run_local_validation.py --trusted-history-commit <exact-trusted-main-sha>
```

Expected: all configured checks PASS; unavailable publication/runtime/human checks remain explicit `SKIPPED` or `NOT_RUN` rather than PASS. Replace `<exact-trusted-main-sha>` with the 40-character main SHA re-fetched immediately before implementation.

- [ ] **Step 6: Run adversarial regression review**

Attack at minimum:

```text
duplicate canon
L0/L1 over-trigger
new hidden Skill owner
Registry drift
DESIGN.md UX authority takeover
brand or third-party code copying
MCP install treated as approval
Godot/Web boundary loss
taste preference treated as defect
untouched Documentation Map/Test/Learning consumer
```

Resolve only validated in-scope Findings, then rerun focused and full validation.

- [ ] **Step 7: Commit governance and verification links**

```bash
git add docs/DOCUMENTATION_MAP.md docs/OPERATING_MODEL.md \
  skills/SKILL_LEARNING_LOG.md skills/SKILL_IMPLEMENTATION_EVIDENCE.json \
  tests
git commit -m "docs: connect spec and design integration evidence"
```

Stage only files that actually changed; omit unchanged optional files from `git add`.

- [ ] **Step 8: Open a separate Draft implementation PR**

The PR body must include:

```yaml
source_bcp: BCP-2026-008-agentic-spec-design-ui-procurement-integration
approval_ref:
base_main_sha:
head_sha:
new_active_skill_count: 0
registry_byte_identical:
focused_tests:
full_validation:
runtime_status:
human_status:
rollback:
```

Do not merge without exact-head checks, unresolved thread 0, P0/P1 0 and explicit user authorization.
