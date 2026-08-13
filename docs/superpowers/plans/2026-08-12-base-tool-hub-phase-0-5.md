# Base Tool Hub Phase 0.5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish one versioned project identity contract and one canonical Figma routing loader before Tool Hub implementation.

**Architecture:** A small `base-tool-contracts` Python package owns Figma registry validation and typed targets for all Studios and the future Hub. Project adapter v1 stays readable and unchanged; v2 adds required canonical project identity through a coordinated builder/checker/template/docs migration, with v1 failing closed for Hub production use.

**Tech Stack:** Python 3.12, Pydantic v2, JSON Schema 2020-12, unittest/pytest.

## Global Constraints

- Do not mutate frozen release artifacts or reinterpret v1 identity.
- `project.project_id` uses `^[a-z0-9]+(?:-[a-z0-9]+)*$`.
- Raw strings in project adapter `validators` are never executed by Tool Hub or the shared contract package.
- Static Figma routing is `ROUTING_CONFIGURED`, never live-node or upload proof.
- Existing project migrations remain project-owned follow-up work.

---

### Task 1: Canonical Figma registry schema and package

**Files:**
- Create: `schemas/project-figma-target-registry-v1.schema.json`
- Create: `tools/base-tool-contracts/pyproject.toml`
- Create: `tools/base-tool-contracts/src/base_tool_contracts/__init__.py`
- Create: `tools/base-tool-contracts/src/base_tool_contracts/figma_routing.py`
- Create: `tools/base-tool-contracts/tests/test_figma_routing.py`

**Interfaces:**
- Produces: `ProjectFigmaRegistry.load(path: Path) -> ProjectFigmaRegistry`.
- Produces: `resolve_ready_target(project_id: str) -> ProjectFigmaTarget`.
- Produces: `validate_anchor_url(project_id: str, url: str) -> str`.

- [ ] **Step 1: Write failing schema and behavior tests using valid and hostile fixtures**
- [ ] **Step 2: Verify RED because package does not exist**
- [ ] **Step 3: Implement closed schema and typed loader**

```python
def validate_anchor_url(self, project_id: str, url: str) -> str:
    target = self.target(project_id)
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "www.figma.com":
        raise DeliveryBlockedError("anchor must use https://www.figma.com")
    if parsed.path.split("/")[2] != target.figma_file_key:
        raise DeliveryBlockedError("anchor Figma file must match the bound project")
    node_id = parse_qs(parsed.query).get("node-id", [""])[0].replace("-", ":")
    if not re.fullmatch(r"\d+:\d+", node_id):
        raise DeliveryBlockedError("anchor node-id must use canonical numeric form")
    return node_id
```

- [ ] **Step 4: Run package tests GREEN**
- [ ] **Step 5: Commit Task 1 files**

### Task 2: Migrate both Studios to the single routing owner

**Files:**
- Modify: `tools/expression-studio/pyproject.toml`
- Modify: `tools/sprite-animation-studio/pyproject.toml`
- Replace: `tools/expression-studio/src/expression_studio/delivery.py` with packet-only types importing `base_tool_contracts`
- Replace: `tools/sprite-animation-studio/src/sprite_animation_studio/delivery.py` with packet-only types importing `base_tool_contracts`
- Modify: `tools/expression-studio/tests/test_delivery.py`
- Modify: `tools/sprite-animation-studio/tests/test_delivery.py`
- Modify: `tools/expression-studio/README.md`
- Modify: `tools/sprite-animation-studio/README.md`

**Interfaces:**
- Consumes: Task 1 `ProjectFigmaRegistry`, `ProjectFigmaTarget`, and `DeliveryBlockedError`.
- No Studio-local `_RegistryDocument` or `_RegistryEntry` remains.

- [ ] **Step 1: Add a failing source/behavior test proving both packages use the shared class**
- [ ] **Step 2: Verify RED**
- [ ] **Step 3: Migrate imports and keep packet public JSON stable**
- [ ] **Step 4: Run shared package and both Studio suites independently**
- [ ] **Step 5: Commit Task 2 files**

### Task 3: Versioned project adapter v2 identity contract

**Files:**
- Create: `schemas/project-base-adapter-v2.schema.json`
- Create: `templates/project-operations/PROJECT_BASE_ADAPTER_V2.json`
- Modify: `tools/project_operating_contract.py`
- Modify: `tests/test_v9_1_project_operating_contract.py`
- Create: `tests/test_project_base_adapter_v2.py`

**Interfaces:**
- Produces: v2 adapter requiring `project.project_id` and rejecting unknown project identity shapes.
- v1 validation remains available for audit/migration.
- Hub readiness reports `IDENTITY_MIGRATION_REQUIRED` for v1.

- [ ] **Step 1: Write failing tests for required kebab-case ID, v1 preservation, and v1 readiness block**
- [ ] **Step 2: Verify RED**
- [ ] **Step 3: Add v2 schema/template and version-dispatch validation**
- [ ] **Step 4: Add deterministic v1-to-v2 migration requiring explicit `--project-id`**
- [ ] **Step 5: Run focused v9.1/v2 compatibility tests**
- [ ] **Step 6: Commit Task 3 files**

### Task 4: Discovery, migration, and compatibility route

**Files:**
- Modify: `README.md`, `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md`
- Create: `docs/operations/PROJECT_BASE_ADAPTER_V2_MIGRATION.md`
- Modify: `templates/project-operations/README.md`
- Create: `tests/test_project_base_adapter_v2_docs.py`

- [ ] **Step 1: Write failing consumer/reference tests**
- [ ] **Step 2: Verify RED**
- [ ] **Step 3: Document owner, rollout, rollback, and exact commands**
- [ ] **Step 4: Run reference freshness and adapter suites**
- [ ] **Step 5: Commit Task 4 files**

### Task 5: Phase 0.5 regression and adversarial review

- [ ] **Step 1: Run `base-tool-contracts`, Expression, and Sprite tests separately**
- [ ] **Step 2: Run exact-main Base local validation**
- [ ] **Step 3: Attack duplicate parser, raw validator execution, inferred ID, Figma key mismatch, malformed node, and v1 in-place mutation**
- [ ] **Step 4: Fix proven P0/P1 findings with fresh RED/GREEN cycles**
- [ ] **Step 5: Report project migrations and live Figma verification as separate unrun work**
