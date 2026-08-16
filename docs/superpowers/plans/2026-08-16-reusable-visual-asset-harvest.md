# Reusable Visual Asset Harvest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `proposal -> user approval -> image production -> primary use -> selective harvest -> reuse` an executable Base contract, with project-local reuse metadata that never auto-promotes visual candidates.

**Architecture:** Reuse the merged Visual Requirement Gate, GPT image review policy, Figma Visual Bible, Project Local Asset Vault, and `ASSET_MANIFEST.yml` promotion boundary. Add only the missing post-primary-use Harvest contract: planning/policy surfaces classify reusable value, Figma stores reusable visual/structural/style references, and Asset Vault stores local-only hash-bound Harvest metadata for actual bytes. No segmentation/decomposition model, new broad Skill/Mode, Tool Hub owner, Figma mutation authority, or parallel product-asset canon is added.

**Tech Stack:** Markdown/YAML/JSON contracts, Python 3.10+ standard library, existing `tools/project_asset_vault.py`, `unittest`, existing Base GitHub Actions.

## Global Constraints

- User-facing order remains `visual proposal -> user approval -> image production -> primary use -> harvest review -> selective structure/layer/rebuild -> reuse`.
- Before a new visual proposal, existing approved assets, Figma Visual Bible references, reusable patterns, and Visual DNA are checked for reuse/variant opportunities.
- Primary-use quality, player/user experience, information hierarchy, emotion, and title-specific identity take precedence over premature componentization.
- `primary-use success` does not imply `reuse promotion`; reuse requires repeat value, non-duplication, independent usability, and acceptable extraction/rebuild cost.
- Harvest classifications are exactly `REUSE_AS_IS`, `VARIANT_SEED`, `STRUCTURE_PATTERN`, `STYLE_DNA`, `REBUILD_FOR_REUSE`, `ONE_OFF_KEEP`, `REJECT_REUSE`.
- Decomposition/rebuild methods are exactly `SOURCE_LAYER`, `MASK_CUTOUT`, `MANUAL_OR_SEMANTIC_REBUILD`, `DERIVED_GENERATIVE_RECOVERY`.
- `DERIVED_GENERATIVE_RECOVERY` is generated/derived pixels, never observed source truth.
- UI buttons/panels/skins default to semantic Figma Component/Variant or Godot Theme/Scene rebuild; blind raster cropping is not the default reusable implementation.
- Figma remains a visual workspace/reference surface, `.asset-vault` remains local candidate-byte authority, `ASSET_MANIFEST.yml + promote` remains tracked product-asset promotion authority, and Godot runtime evidence remains implementation proof.
- Harvest metadata stays under `.asset-vault/`, contains no absolute project paths, and never sets `PROJECT_ASSET_APPROVED=true` or calls `promote` implicitly.
- PR #428 and every path currently changed by PR #428 remain read-only and are not modified by this implementation.
- No new ACTIVE Skill, Skill Mode, Registry owner, provider adapter, image model dependency, or external package is added.
- Existing user changes and unrelated repository files are not refactored.

---

## File Structure

**Policy/planning owners**
- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`

**Figma/reference owners**
- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`
- `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`

**Local byte/metadata owner**
- `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`
- `tools/project_asset_vault.py`

**Tests**
- `tests/test_visual_requirement_gate.py`
- `tests/test_visual_collaboration_capability_contract.py`
- `tests/test_project_asset_vault.py`

**Explicitly excluded because PR #428 currently owns them**
- `tools/expression-studio/**`
- `tools/tool-hub/**`
- `tools/figma-bridge/**`
- `tools/base-tool-contracts/**`
- `.github/workflows/validate-provisional-*.yml`
- `.github/workflows/validate-tool-hub-windows-child.yml`

---

### Task 1: Add the Produce-First / Harvest-Second policy contract

**Files:**
- Modify: `tests/test_visual_requirement_gate.py`
- Modify: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- Modify: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Modify: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`

**Interfaces:**
- Consumes: existing `Visual Requirement Gate`, Figma Visual Bible, Asset Vault, and `PROJECT_ASSET_APPROVED` contracts.
- Produces: `Primary Use Gate`, `Reusable Visual Harvest Gate`, seven classifications, four methods, and fields `primary_use_status`, `harvest_status`, `reuse_classification`, `decomposition_method`, `asset_vault_harvest_record_id`, `second_use_validation`.

- [ ] **Step 1: Write failing policy tests.**

Append to `VisualRequirementGateTests`:

```python
    def test_visual_workflow_produces_first_and_harvests_only_after_primary_use(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        plan = read("templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md")

        for content in (guide, policy):
            for token in (
                "Primary Use Gate",
                "Reusable Visual Harvest Gate",
                "REUSE_AS_IS",
                "VARIANT_SEED",
                "STRUCTURE_PATTERN",
                "STYLE_DNA",
                "REBUILD_FOR_REUSE",
                "ONE_OFF_KEEP",
                "REJECT_REUSE",
                "SOURCE_LAYER",
                "MASK_CUTOUT",
                "MANUAL_OR_SEMANTIC_REBUILD",
                "DERIVED_GENERATIVE_RECOVERY",
            ):
                self.assertIn(token, content)

        for token in (
            "primary_use_status",
            "harvest_status",
            "reuse_classification",
            "decomposition_method",
            "asset_vault_harvest_record_id",
            "second_use_validation",
        ):
            self.assertIn(token, plan)

    def test_reuse_never_auto_promotes_or_overrides_primary_quality(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        for content in (guide, policy):
            self.assertIn("primary-use success", content)
            self.assertIn("reuse promotion", content)
            self.assertIn("PROJECT_ASSET_APPROVED", content)
            self.assertIn("title-specific identity", content)
```

- [ ] **Step 2: Run RED.**

```bash
python -m unittest tests.test_visual_requirement_gate -v
```

Expected: the two new tests fail only because the Harvest contract/fields are missing; pre-existing tests remain green.

- [ ] **Step 3: Add `Primary Use Gate` and `Reusable Visual Harvest Gate` to the Art Direction guide.**

Insert after the existing Visual Requirement Gate:

```text
existing approved asset / Visual Bible lookup
→ visual proposal
→ user approval
→ image production
→ Primary Use Gate
→ Reusable Visual Harvest Gate
→ selective structure / layer / semantic rebuild
→ reusable asset / pattern / Visual DNA
→ next-task reuse or variant
```

The Harvest Gate asks:

```text
1. Is another screen/scene likely to need the same role?
2. Does an equivalent reusable asset/pattern already exist?
3. Can this candidate stand independently without damaging title-specific identity?
4. Is extraction/rebuild cheaper than expected future recreation?
5. Does the method preserve source/provenance truth?
```

Define all seven classifications. `ONE_OFF_KEEP` must be a valid success state for strong narrative/hero/title-specific visuals.

- [ ] **Step 4: Extend the GPT image policy.**

Add the user-facing sequence:

```text
proposal -> user approval -> production -> primary use -> harvest review
```

Rules:
- low-cost separation hints (`textless master`, `clean plate`, `transparent source`) are kept only when natural;
- they cannot dictate the primary composition;
- `DERIVED_GENERATIVE_RECOVERY` must be identified as generated/derived pixels;
- Harvest decisions never imply `PROJECT_ASSET_APPROVED`, `promote`, Figma finalization, or Godot runtime success.

- [ ] **Step 5: Extend `GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`.**

Add to Context YAML:

```yaml
primary_use_status: NOT_RUN | IN_REVIEW | ACCEPTED | REVISION_REQUIRED
harvest_status: NOT_REVIEWED | NO_REUSE_VALUE | CANDIDATES_FOUND | STRUCTURED | SECOND_USE_VALIDATED
reuse_classification: UNASSESSED | REUSE_AS_IS | VARIANT_SEED | STRUCTURE_PATTERN | STYLE_DNA | REBUILD_FOR_REUSE | ONE_OFF_KEEP | REJECT_REUSE
decomposition_method: NONE | SOURCE_LAYER | MASK_CUTOUT | MANUAL_OR_SEMANTIC_REBUILD | DERIVED_GENERATIVE_RECOVERY
asset_vault_harvest_record_id:
second_use_validation: NOT_RUN | PASS | FAIL | NOT_APPLICABLE
```

Add:

```markdown
### Reusable Visual Harvest Review

| Harvest ID | Image ID | Primary Use | Candidate | Classification | Existing Reuse Conflict | Method | Derived Pixels | Target Reuse | Second Use | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
```

State that the table is a working review surface, not an asset manifest or promotion authority.

- [ ] **Step 6: Run GREEN.**

```bash
python -m unittest tests.test_visual_requirement_gate -v
```

Expected: all tests pass.

- [ ] **Step 7: Commit.**

```bash
git add tests/test_visual_requirement_gate.py \
  docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md \
  docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md \
  templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md
git commit -m "docs: add reusable visual harvest gate"
```

---

### Task 2: Make Figma store reusable references without becoming asset authority

**Files:**
- Modify: `tests/test_visual_collaboration_capability_contract.py`
- Modify: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- Modify: `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`
- Modify: `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`

**Interfaces:**
- Consumes: Task 1 classifications and current Figma lifecycle.
- Produces: `01.10_REUSABLE_COMPONENTS`, `01.11_STRUCTURE_PATTERNS`, `01.12_VISUAL_DNA`; registry fields `reuse_classification`, `reuse_source_artifact_id`, `asset_vault_harvest_record_id`, `derived_pixel_status`.

- [ ] **Step 1: Write failing Figma reuse test.**

Add to `VisualCollaborationCapabilityContractTests`:

```python
    def test_figma_visual_bible_tracks_reuse_without_becoming_asset_authority(self):
        policy = (ROOT / "docs/VISUAL_COLLABORATION_TOOL_POLICY.md").read_text(encoding="utf-8")
        profile = (ROOT / "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md").read_text(encoding="utf-8")
        registry = json.loads(
            (ROOT / "templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json").read_text(encoding="utf-8")
        )
        item = registry["artifacts"][0]

        for token in (
            "01.10_REUSABLE_COMPONENTS",
            "01.11_STRUCTURE_PATTERNS",
            "01.12_VISUAL_DNA",
            "REBUILD_FOR_REUSE",
            "ONE_OFF_KEEP",
        ):
            self.assertIn(token, profile)

        for field in (
            "reuse_classification",
            "reuse_source_artifact_id",
            "asset_vault_harvest_record_id",
            "derived_pixel_status",
        ):
            self.assertIn(field, item)

        self.assertIn("reuse promotion", policy)
        self.assertIn("PROJECT_ASSET_APPROVED", policy)
        self.assertIn("Asset Vault", policy)
        self.assertIn("Godot", policy)
```

- [ ] **Step 2: Run RED.**

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

Expected: only the new reuse assertions fail.

- [ ] **Step 3: Extend the Figma Visual Bible profile.**

Under `01_APPROVED_REFERENCE`, add optional sections:

```text
01.10_REUSABLE_COMPONENTS
01.11_STRUCTURE_PATTERNS
01.12_VISUAL_DNA
```

Add a `Reusable harvest card`:

```yaml
source_visual_artifact_id:
primary_use_status:
reuse_classification:
reuse_reason:
existing_reuse_conflict:
asset_vault_harvest_record_id:
derived_pixel_status:
second_use_validation:
product_asset_status: NOT_APPROVED
```

Meaning:
- `01.10`: repeated primitives/components, not one-off hero art;
- `01.11`: layout/hierarchy/interaction patterns, not copied game-rule canon;
- `01.12`: palette/shape/material/lighting/camera/spacing with Keep/Avoid/Do Not Drift.

- [ ] **Step 4: Extend the Visual Artifact Registry example.**

Add without changing `schema_version`:

```json
"reuse_classification": "UNASSESSED|REUSE_AS_IS|VARIANT_SEED|STRUCTURE_PATTERN|STYLE_DNA|REBUILD_FOR_REUSE|ONE_OFF_KEEP|REJECT_REUSE",
"reuse_source_artifact_id": "",
"asset_vault_harvest_record_id": "",
"derived_pixel_status": "NONE|SOURCE_LAYER|MASK_CUTOUT|MANUAL_OR_SEMANTIC_REBUILD|DERIVED_GENERATIVE_RECOVERY"
```

Do not add bytes, absolute local paths, approval authority, or runtime-completion claims.

- [ ] **Step 5: Extend the shared visual policy.**

State that Figma `reuse promotion` means promotion to a reusable **visual reference/component/pattern**, not `PROJECT_ASSET_APPROVED`. Actual candidate bytes remain Asset Vault-owned; tracked asset approval remains Manifest/promote-owned; Godot reusable Scene/Resource/Theme status requires runtime evidence.

- [ ] **Step 6: Run GREEN.**

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

Expected: all tests pass.

- [ ] **Step 7: Commit.**

```bash
git add tests/test_visual_collaboration_capability_contract.py \
  docs/VISUAL_COLLABORATION_TOOL_POLICY.md \
  templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md \
  templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json
git commit -m "docs: connect visual harvest to Figma references"
```

---

### Task 3: Record local Harvest metadata in Asset Vault without decomposing or promoting images

**Files:**
- Modify: `tests/test_project_asset_vault.py`
- Modify: `tools/project_asset_vault.py`
- Modify: `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`

**Interfaces:**
- Consumes: existing `load_config`, `paths`, `_safe_relative`, `_safe_target_under`, `_supported`, `sha256_file`, `_read_json`, `_write_json`.
- Produces: `.asset-vault/harvest.json`; `record_harvest(project_root: Path, *, record_id: str, source_key_text: str, classification: str, method: str, member_key_texts: list[str]) -> dict[str, Any]`; CLI `record-harvest`.
- Does not produce layers, masks, inpainting, Figma changes, tracked assets, or approval state.

- [ ] **Step 1: Write failing happy-path test.**

Add to `ProjectAssetVaultTests`:

```python
    def test_record_harvest_writes_local_only_hash_bound_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            source = project / ".asset-vault/library/scenes/source.png"
            layer = project / ".asset-vault/library/scenes/layers/background.png"
            source.parent.mkdir(parents=True)
            layer.parent.mkdir(parents=True)
            source.write_bytes(b"source")
            layer.write_bytes(b"background")

            result = run_tool(
                "record-harvest",
                "--project-root", str(project),
                "--record-id", "HARVEST-SCENE-001",
                "--source-key", "scenes/source.png",
                "--classification", "REUSE_AS_IS",
                "--method", "MASK_CUTOUT",
                "--member-key", "scenes/layers/background.png",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            path = project / ".asset-vault/harvest.json"
            record = json.loads(path.read_text(encoding="utf-8"))["records"][0]
            self.assertEqual(record["record_id"], "HARVEST-SCENE-001")
            self.assertEqual(record["review_status"], "IN_REVIEW")
            self.assertFalse(record["project_asset_approved"])
            self.assertNotIn(str(project), path.read_text(encoding="utf-8"))
            self.assertFalse((project / "assets/approved").exists())
```

- [ ] **Step 2: Write failing guard tests.**

```python
    def test_record_harvest_rejects_invalid_classification_and_missing_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            source = project / ".asset-vault/library/ui/source.png"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"source")

            bad = run_tool(
                "record-harvest", "--project-root", str(project),
                "--record-id", "HARVEST-UI-001", "--source-key", "ui/source.png",
                "--classification", "AUTO_PROMOTE", "--method", "SOURCE_LAYER",
            )
            self.assertNotEqual(bad.returncode, 0)

            missing = run_tool(
                "record-harvest", "--project-root", str(project),
                "--record-id", "HARVEST-UI-002", "--source-key", "ui/missing.png",
                "--classification", "ONE_OFF_KEEP", "--method", "SOURCE_LAYER",
            )
            self.assertNotEqual(missing.returncode, 0)

    def test_record_harvest_marks_generated_recovery_as_derived_and_never_promotes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            source = project / ".asset-vault/library/background/source.png"
            recovered = project / ".asset-vault/library/background/recovered.png"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"source")
            recovered.write_bytes(b"generated-recovery")

            result = run_tool(
                "record-harvest", "--project-root", str(project),
                "--record-id", "HARVEST-BG-001", "--source-key", "background/source.png",
                "--classification", "VARIANT_SEED",
                "--method", "DERIVED_GENERATIVE_RECOVERY",
                "--member-key", "background/recovered.png",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            record = json.loads(
                (project / ".asset-vault/harvest.json").read_text(encoding="utf-8")
            )["records"][0]
            self.assertTrue(record["contains_derived_generated_pixels"])
            self.assertFalse(record["project_asset_approved"])
            self.assertFalse((project / "assets/approved").exists())
```

- [ ] **Step 3: Run RED.**

```bash
python -m unittest \
  tests.test_project_asset_vault.ProjectAssetVaultTests.test_record_harvest_writes_local_only_hash_bound_metadata \
  tests.test_project_asset_vault.ProjectAssetVaultTests.test_record_harvest_rejects_invalid_classification_and_missing_source \
  tests.test_project_asset_vault.ProjectAssetVaultTests.test_record_harvest_marks_generated_recovery_as_derived_and_never_promotes \
  -v
```

Expected: fail because `record-harvest` does not exist.

- [ ] **Step 4: Add constants/storage helpers.**

Near existing state constants:

```python
HARVEST_NAME = "harvest.json"
HARVEST_CLASSIFICATIONS = {
    "REUSE_AS_IS", "VARIANT_SEED", "STRUCTURE_PATTERN", "STYLE_DNA",
    "REBUILD_FOR_REUSE", "ONE_OFF_KEEP", "REJECT_REUSE",
}
HARVEST_METHODS = {
    "SOURCE_LAYER", "MASK_CUTOUT", "MANUAL_OR_SEMANTIC_REBUILD",
    "DERIVED_GENERATIVE_RECOVERY",
}
```

Extend `paths()`:

```python
"harvest": vault / HARVEST_NAME,
```

Add:

```python
def _default_harvest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "authority": "local-vault-harvest-metadata",
        "local_only": True,
        "records": [],
    }


def load_harvest(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return _default_harvest()
    data = _read_json(path)
    if not isinstance(data.get("records"), list):
        raise VaultError("harvest records must be a list")
    data["schema_version"] = 1
    data["authority"] = "local-vault-harvest-metadata"
    data["local_only"] = True
    return data
```

- [ ] **Step 5: Implement safe library-key validation and `record_harvest`.**

```python
def _harvest_library_asset(
    p: dict[str, Path], config: dict[str, Any], key_text: str
) -> tuple[str, Path, str]:
    key = _safe_relative(key_text, "harvest asset key")
    candidate = _safe_target_under(p["library"], key, "Harvest asset path")
    if candidate.is_symlink() or not candidate.is_file():
        raise VaultError(f"Harvest asset does not exist as a regular file: {key.as_posix()}")
    if not _supported(candidate, set(config["supported_extensions"])):
        raise VaultError(f"Harvest asset uses an unsupported extension: {key.as_posix()}")
    return key.as_posix(), candidate, sha256_file(candidate)


def record_harvest(
    project_root: Path,
    *,
    record_id: str,
    source_key_text: str,
    classification: str,
    method: str,
    member_key_texts: list[str],
) -> dict[str, Any]:
    init_project(project_root)
    config = load_config(project_root)
    p = paths(project_root, config)
    if classification not in HARVEST_CLASSIFICATIONS:
        raise VaultError(f"Unsupported harvest classification: {classification}")
    if method not in HARVEST_METHODS:
        raise VaultError(f"Unsupported harvest method: {method}")
    if not record_id or any(
        ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_."
        for ch in record_id
    ):
        raise VaultError("record_id must use only letters, digits, '-', '_', or '.'")

    source_key, _, source_hash = _harvest_library_asset(p, config, source_key_text)
    members = []
    for member_text in member_key_texts:
        member_key, _, member_hash = _harvest_library_asset(p, config, member_text)
        members.append({"source_key": member_key, "sha256": member_hash})

    harvest = load_harvest(p["harvest"])
    if any(
        item.get("record_id") == record_id
        for item in harvest["records"]
        if isinstance(item, dict)
    ):
        raise VaultError(f"Harvest record already exists: {record_id}")

    record = {
        "record_id": record_id,
        "source_key": source_key,
        "source_sha256": source_hash,
        "classification": classification,
        "method": method,
        "members": members,
        "contains_derived_generated_pixels": method == "DERIVED_GENERATIVE_RECOVERY",
        "review_status": "IN_REVIEW",
        "project_asset_approved": False,
    }
    harvest["records"].append(record)
    _write_json(p["harvest"], harvest)
    return record
```

Do not call `sync_project`, `promote_asset`, Figma code, or any provider.

- [ ] **Step 6: Add CLI parser/dispatch.**

Parser:

```python
harvest = sub.add_parser(
    "record-harvest", help="Record local-only reusable visual harvest metadata"
)
harvest.add_argument("--project-root", type=Path, required=True)
harvest.add_argument("--record-id", required=True)
harvest.add_argument("--source-key", required=True)
harvest.add_argument(
    "--classification", required=True, choices=sorted(HARVEST_CLASSIFICATIONS)
)
harvest.add_argument("--method", required=True, choices=sorted(HARVEST_METHODS))
harvest.add_argument("--member-key", action="append", default=[])
```

Dispatch:

```python
elif args.command == "record-harvest":
    record = record_harvest(
        args.project_root,
        record_id=args.record_id,
        source_key_text=args.source_key,
        classification=args.classification,
        method=args.method,
        member_key_texts=args.member_key,
    )
    print(
        "Visual harvest recorded: "
        f"record_id={record['record_id']} "
        f"classification={record['classification']} method={record['method']}"
    )
```

- [ ] **Step 7: Document the local metadata boundary.**

Add to the vault tree:

```text
.asset-vault/
├─ library/
├─ archive/
├─ inbox/
├─ state.json
├─ sync.json
└─ harvest.json        # local-only reusable-visual classification/provenance metadata
```

State verbatim:

```text
record-harvest != image decomposition
record-harvest != PROJECT_ASSET_APPROVED
record-harvest != promote
```

Example:

```powershell
python tools/project_asset_vault.py record-harvest --project-root . `
  --record-id "HARVEST-UI-001" `
  --source-key "gpt-imports/2026-08-16/ui-screen.png" `
  --classification "REBUILD_FOR_REUSE" `
  --method "MANUAL_OR_SEMANTIC_REBUILD"
```

- [ ] **Step 8: Run GREEN.**

```bash
python -m unittest tests.test_project_asset_vault -v
```

Expected: all existing vault behavior and the three new tests pass. Existing tombstone, promotion, path-safety, local-only, and no-resurrection tests must remain green.

- [ ] **Step 9: Commit.**

```bash
git add tools/project_asset_vault.py tests/test_project_asset_vault.py \
  docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md
git commit -m "feat: record local reusable visual harvest metadata"
```

---

### Task 4: Final integration, adversarial regression, and exact-head validation

**Files:**
- No planned production-file change. Patch only validated findings within Tasks 1-3 scope.

**Interfaces:**
- Consumes: Tasks 1-3 final interfaces, all using `asset_vault_harvest_record_id` as the one linkage name.
- Produces: verified repository contract and a bounded pilot handoff; no new schema/owner.

- [ ] **Step 1: Run all focused suites together.**

```bash
python -m unittest \
  tests.test_visual_requirement_gate \
  tests.test_visual_collaboration_capability_contract \
  tests.test_project_asset_vault \
  -v
```

Expected: PASS with no feature-introduced skips.

- [ ] **Step 2: Run syntax/freshness validation.**

```bash
python -m compileall tools/project_asset_vault.py tests
python tools/check_canonical_reference_freshness.py
```

If current `main` uses a different canonical freshness invocation, read the existing workflow and execute that exact command rather than adding a duplicate checker/workflow.

- [ ] **Step 3: Run the adversarial regression loop.**

Attack these failures:

```text
A. one-off visuals accidentally become reusable-library obligations
B. primary-use quality becomes subordinate to separability
C. Figma reuse classification becomes product-asset approval
D. record-harvest implicitly syncs/promotes or calls a provider
E. generated occlusion recovery is represented as source truth
F. harvest metadata stores absolute project paths
G. deleted local candidates are resurrected from harvest metadata
H. UI raster crops are treated as semantic/reflow-safe components
I. PR #428 changed-file overlap appears after main moves
```

Validate every critique against current files/tests. Patch only `MUST_FIX` or approved in-scope `SHOULD_FIX`, then repeat Steps 1-2.

- [ ] **Step 4: Recheck open/recent PR ownership before merge.**

```text
1. Read current main SHA.
2. Re-read PR #428 changed filenames.
3. Compare this PR's changed filenames to #428.
4. If overlap is non-empty, do not touch #428; classify/defer the overlap under repository governance.
5. If main advanced through completed non-overlapping work, synchronize using repository-approved history policy.
6. Re-run exact-head CI.
```

- [ ] **Step 5: Require exact-head GitHub validation.**

Before any ready/merge claim:

```text
Validate Base v9 Operating Contracts = SUCCESS
Validate Game Project Operating System = SUCCESS
Validate BCA Visual and Sheet Workflow = SUCCESS when triggered/applicable
Dependency Review = SUCCESS when triggered/applicable
unresolved review threads = 0
same-goal duplicate PR check = clear
main freshness = current
```

Do not claim these from repository tests:

```yaml
real_image_layer_quality: NOT_RUN
real_figma_reusable_component_mutation: NOT_RUN
real_godot_runtime_reuse: NOT_RUN
real_project_scene_background_ux_pilot: NOT_RUN
human_visual_quality_improvement: NOT_RUN
```

- [ ] **Step 6: Prepare the post-merge pilot handoff.**

After implementation is merged and a real project has eligible inputs, test only:

```text
1. one in-game composite
2. one background
3. one UX screen
```

Per pilot record:

```yaml
primary_use_success:
reuse_candidates_found:
rejected_one_off_elements:
reuse_classification:
decomposition_method:
manual_repair_required:
recomposition_result:
second_use_or_variant_result:
style_drift_findings:
asset_duplication_avoided:
figma_reference_status:
godot_runtime_status:
```

Only pilot evidence can justify a later segmentation/decomposition adapter. Do not install SAM 2, LayerDecomp, DiffDecompose, Qwen-Image-Layered, or another model merely because this contract exists.

---

## Rollback

- Tasks 1-2 are documentation/template/test changes and can be reverted as isolated commits.
- Task 3 adds only local `.asset-vault/harvest.json` metadata behavior; reverting the code leaves any existing local harvest file inert and does not delete candidate or promoted assets.
- No existing project asset migration is performed.
- No tracked product asset is automatically created or removed.
- No Figma file mutation is part of this implementation.
- If a later implementation needs a different Harvest schema, migrate local metadata explicitly; do not silently reinterpret old records.
