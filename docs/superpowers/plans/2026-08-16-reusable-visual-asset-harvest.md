# Reusable Visual Asset Harvest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `proposal -> user approval -> image production -> primary use -> selective harvest -> reuse` an executable Base contract, with project-local harvest metadata that never auto-promotes visual candidates.

**Architecture:** Reuse the merged Visual Requirement Gate, GPT image review policy, Figma Visual Bible, Project Local Asset Vault, and `ASSET_MANIFEST.yml` promotion boundary. Add only the missing post-primary-use harvest contract: policies classify reusable value, Figma records reusable visual/structural/style references, and Asset Vault stores local-only harvest metadata for actual bytes. No segmentation/decomposition model, new broad Skill/Mode, Tool Hub owner, Figma mutation authority, or parallel product-asset canon is added.

**Tech Stack:** Markdown/YAML/JSON contracts, Python 3.10+ standard library, existing `tools/project_asset_vault.py`, `unittest`, existing Base GitHub Actions.

## Global Constraints

- User-facing order remains `visual proposal -> user approval -> image production -> primary use -> harvest review -> selective structure/layer/rebuild -> reuse`.
- Before a new visual proposal, existing approved assets, Figma Visual Bible references, reusable patterns, and Visual DNA are checked for `REUSE_AS_IS / VARIANT_SEED / STRUCTURE_PATTERN / STYLE_DNA` opportunities.
- Primary-use quality, player/user experience, information hierarchy, emotion, and title-specific identity take precedence over premature componentization.
- `primary-use success` does not imply `reuse promotion`; reuse requires repeat value, non-duplication, independent usability, and acceptable extraction/rebuild cost.
- Harvest classifications are exactly `REUSE_AS_IS`, `VARIANT_SEED`, `STRUCTURE_PATTERN`, `STYLE_DNA`, `REBUILD_FOR_REUSE`, `ONE_OFF_KEEP`, `REJECT_REUSE`.
- Decomposition methods are exactly `SOURCE_LAYER`, `MASK_CUTOUT`, `MANUAL_OR_SEMANTIC_REBUILD`, `DERIVED_GENERATIVE_RECOVERY`.
- `DERIVED_GENERATIVE_RECOVERY` is generated/derived pixels, never observed source truth.
- UI buttons/panels/skins default to semantic Figma Component/Variant or Godot Theme/Scene rebuild; blind raster cropping is not the default reusable implementation.
- Figma remains a visual workspace/reference surface, `.asset-vault` remains local candidate-byte authority, `ASSET_MANIFEST.yml + promote` remains tracked product-asset promotion authority, and Godot runtime evidence remains implementation proof.
- Harvest metadata must remain under `.asset-vault/`, contain no absolute project paths, and never make `PROJECT_ASSET_APPROVED=true` or call `promote` implicitly.
- PR #428 and every path currently changed by PR #428 remain read-only and are not modified by this implementation.
- No new ACTIVE Skill, Skill Mode, Registry owner, provider adapter, image model dependency, or external package is added.
- Existing user changes and unrelated repository files are not refactored.

---

## File Structure

### Existing owners to modify

- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md` — owns reusable-visual value criteria and production/harvest decision rules.
- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md` — owns user-facing proposal/approval/production/review lifecycle and post-use harvest gate.
- `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md` — per-image working record for primary use, harvest classification, and local harvest linkage.
- `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` — keeps Figma reusable references/patterns noncanonical and separate from product-asset approval.
- `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md` — project-local Figma organization for reusable components/patterns/Visual DNA.
- `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json` — links a visual artifact to reuse classification and local harvest record without becoming byte authority.
- `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md` — defines local-only harvest metadata and explicit promotion boundary.
- `tools/project_asset_vault.py` — records validated local harvest metadata only; performs no image decomposition.

### Existing tests to extend

- `tests/test_visual_requirement_gate.py` — policy and planning contract.
- `tests/test_visual_collaboration_capability_contract.py` — Figma/registry reuse and authority contract.
- `tests/test_project_asset_vault.py` — local harvest metadata behavior, path safety, deletion behavior, and no-auto-promotion.
- `tests/test_bca_visual_sheet_workflow.py` — final cross-owner regression proving the full flow does not collapse authority boundaries.

### Explicitly not modified

- `tools/expression-studio/**`
- `tools/tool-hub/**`
- `tools/figma-bridge/**`
- `tools/base-tool-contracts/**`
- `.github/workflows/validate-provisional-*.yml`
- `.github/workflows/validate-tool-hub-windows-child.yml`
- any other path owned by open PR #428

---

### Task 1: Add the Produce-First / Harvest-Second policy contract

**Files:**
- Modify: `tests/test_visual_requirement_gate.py`
- Modify: `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- Modify: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Modify: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`

**Interfaces:**
- Consumes: existing `Visual Requirement Gate`, `PROJECT_ASSET_APPROVED`, Asset Vault, and Figma Visual Bible contracts.
- Produces: canonical text tokens `Primary Use Gate`, `Reusable Visual Harvest Gate`, the seven harvest classifications, the four decomposition methods, and planning fields `primary_use_status`, `harvest_status`, `reuse_classification`, `decomposition_method`, `harvest_record_id`, `second_use_validation`.

- [ ] **Step 1: Add focused RED tests to `tests/test_visual_requirement_gate.py`.**

Append these methods inside `VisualRequirementGateTests`:

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
            "harvest_record_id",
            "second_use_validation",
        ):
            self.assertIn(token, plan)

    def test_reuse_does_not_override_primary_visual_quality_or_auto_promote(self) -> None:
        guide = read(
            "docs/knowledge/game-development/"
            "ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md"
        )
        policy = read("docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md")
        for content in (guide, policy):
            self.assertIn("primary-use success", content)
            self.assertIn("reuse promotion", content)
            self.assertIn("PROJECT_ASSET_APPROVED", content)
            self.assertIn("자동", content)
            self.assertIn("title-specific identity", content)
```

- [ ] **Step 2: Run the focused test and verify RED.**

Run:

```bash
python -m unittest tests.test_visual_requirement_gate -v
```

Expected: existing tests stay green; the two new methods fail because `Primary Use Gate` / `Reusable Visual Harvest Gate` and the planning fields are not yet present.

- [ ] **Step 3: Add `Primary Use Gate` and `Reusable Visual Harvest Gate` to the Art Direction guide.**

Add a bounded subsection after the existing Visual Requirement Gate. It must include this lifecycle verbatim:

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

Define the Harvest Gate questions:

```text
1. Is the candidate likely to serve the same role in another screen/scene?
2. Is it non-duplicative with an existing reusable asset/pattern?
3. Can it be edited/placed independently without destroying title-specific identity?
4. Is extraction/rebuild cost lower than expected future recreation cost?
5. Does the chosen decomposition/rebuild method preserve source/provenance truth?
```

Define all seven classifications and state that `ONE_OFF_KEEP` is a valid success state for strong title-specific/narrative visuals.

- [ ] **Step 4: Extend the GPT image policy with the user-facing production/harvest sequence.**

Add a section after generation/review lifecycle that explicitly states:

```text
proposal -> user approval -> production -> primary use -> harvest review
```

Require low-cost separation hints only when natural (`textless master`, `clean plate`, `transparent source`) and state that they cannot dictate the primary composition. Require `DERIVED_GENERATIVE_RECOVERY` provenance for occlusion-recovered pixels and prohibit automatic `PROJECT_ASSET_APPROVED` or `promote` from a harvest decision.

- [ ] **Step 5: Add planning fields and a Harvest Review table to `GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`.**

Add these fields to the Context YAML:

```yaml
primary_use_status: NOT_RUN | IN_REVIEW | ACCEPTED | REVISION_REQUIRED
harvest_status: NOT_REVIEWED | NO_REUSE_VALUE | CANDIDATES_FOUND | STRUCTURED | SECOND_USE_VALIDATED
reuse_classification: UNASSESSED | REUSE_AS_IS | VARIANT_SEED | STRUCTURE_PATTERN | STYLE_DNA | REBUILD_FOR_REUSE | ONE_OFF_KEEP | REJECT_REUSE
decomposition_method: NONE | SOURCE_LAYER | MASK_CUTOUT | MANUAL_OR_SEMANTIC_REBUILD | DERIVED_GENERATIVE_RECOVERY
harvest_record_id:
second_use_validation: NOT_RUN | PASS | FAIL | NOT_APPLICABLE
```

Add this table after the normal image Review section:

```markdown
### Reusable Visual Harvest Review

| Harvest ID | Image ID | Primary Use | Candidate | Classification | Existing Reuse Conflict | Method | Derived Pixels | Target Reuse | Second Use | Decision |
|---|---|---|---|---|---|---|---|---|---|---|
```

State that this table is not an asset manifest and cannot promote bytes.

- [ ] **Step 6: Run Task 1 tests and verify GREEN.**

Run:

```bash
python -m unittest tests.test_visual_requirement_gate -v
```

Expected: all `VisualRequirementGateTests` pass.

- [ ] **Step 7: Commit Task 1.**

```bash
git add \
  tests/test_visual_requirement_gate.py \
  docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md \
  docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md \
  templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md
git commit -m "docs: add reusable visual harvest gate"
```

---

### Task 2: Make Figma store reusable references without becoming product-asset authority

**Files:**
- Modify: `tests/test_visual_collaboration_capability_contract.py`
- Modify: `docs/VISUAL_COLLABORATION_TOOL_POLICY.md`
- Modify: `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`
- Modify: `templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json`

**Interfaces:**
- Consumes: Task 1 harvest classifications and current Figma lifecycle.
- Produces: Figma sections `01.10_REUSABLE_COMPONENTS`, `01.11_STRUCTURE_PATTERNS`, `01.12_VISUAL_DNA`; registry fields `reuse_classification`, `reuse_source_artifact_id`, `asset_vault_harvest_record_id`, `derived_pixel_status`.

- [ ] **Step 1: Add RED tests to `tests/test_visual_collaboration_capability_contract.py`.**

Add:

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

- [ ] **Step 2: Run focused test and verify RED.**

Run:

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

Expected: the new method fails on missing reusable sections/registry fields; existing Figma authority tests remain green.

- [ ] **Step 3: Extend `FIGMA_VISUAL_BIBLE_PROFILE.md`.**

Under `01_APPROVED_REFERENCE`, append optional sections:

```text
01.10_REUSABLE_COMPONENTS
01.11_STRUCTURE_PATTERNS
01.12_VISUAL_DNA
```

Rules:

```text
01.10: repeated visual primitives/components only; title-specific one-offs stay out.
01.11: layout/hierarchy/interaction structures, not copied game rules.
01.12: palette/shape/material/lighting/camera/spacing rules with Keep/Avoid/Do Not Drift.
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

Explicitly state Figma cannot set `PROJECT_ASSET_APPROVED` or replace Asset Vault/Manifest authority.

- [ ] **Step 4: Extend `VISUAL_ARTIFACT_REGISTRY.json` example fields without changing `schema_version`.**

Inside the example artifact add:

```json
"reuse_classification": "UNASSESSED|REUSE_AS_IS|VARIANT_SEED|STRUCTURE_PATTERN|STYLE_DNA|REBUILD_FOR_REUSE|ONE_OFF_KEEP|REJECT_REUSE",
"reuse_source_artifact_id": "",
"asset_vault_harvest_record_id": "",
"derived_pixel_status": "NONE|SOURCE_LAYER|MASK_CUTOUT|MANUAL_OR_SEMANTIC_REBUILD|DERIVED_GENERATIVE_RECOVERY"
```

Do not add bytes, local absolute paths, approval authority, or runtime-completion flags.

- [ ] **Step 5: Add Figma reuse boundary prose to `VISUAL_COLLABORATION_TOOL_POLICY.md`.**

Require that approved visual results may yield reusable component/pattern/Visual DNA references only after primary-use review. State that `reuse promotion` in Figma means reusable **reference/pattern** promotion, not `PROJECT_ASSET_APPROVED`; actual bytes remain in Asset Vault and runtime reusable structures require Godot verification.

- [ ] **Step 6: Run Task 2 tests and verify GREEN.**

```bash
python -m unittest tests.test_visual_collaboration_capability_contract -v
```

Expected: all tests pass.

- [ ] **Step 7: Commit Task 2.**

```bash
git add \
  tests/test_visual_collaboration_capability_contract.py \
  docs/VISUAL_COLLABORATION_TOOL_POLICY.md \
  templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md \
  templates/project-operations/VISUAL_ARTIFACT_REGISTRY.json
git commit -m "docs: connect visual harvest to Figma references"
```

---

### Task 3: Record local Harvest metadata in Project Asset Vault without generating or promoting images

**Files:**
- Modify: `tests/test_project_asset_vault.py`
- Modify: `tools/project_asset_vault.py`
- Modify: `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`

**Interfaces:**
- Consumes: existing `load_config`, `paths`, `_safe_relative`, `_safe_target_under`, `_supported`, `sha256_file`, `_read_json`, `_write_json`.
- Produces: `.asset-vault/harvest.json`; function `record_harvest(project_root: Path, *, record_id: str, source_key_text: str, classification: str, method: str, member_key_texts: list[str]) -> dict[str, Any]`; CLI command `record-harvest`.
- Does not produce layers, masks, inpainting, Figma changes, tracked assets, or approval state.

- [ ] **Step 1: Add RED behavioral tests to `tests/test_project_asset_vault.py`.**

Add these tests:

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
            data = json.loads(path.read_text(encoding="utf-8"))
            record = data["records"][0]
            self.assertEqual(record["record_id"], "HARVEST-SCENE-001")
            self.assertEqual(record["classification"], "REUSE_AS_IS")
            self.assertEqual(record["method"], "MASK_CUTOUT")
            self.assertEqual(record["review_status"], "IN_REVIEW")
            self.assertFalse(record["project_asset_approved"])
            self.assertNotIn(str(project), path.read_text(encoding="utf-8"))
            self.assertFalse((project / "assets/approved").exists())

    def test_record_harvest_rejects_invalid_enums_missing_files_and_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            source = project / ".asset-vault/library/ui/source.png"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"source")

            bad_class = run_tool(
                "record-harvest", "--project-root", str(project),
                "--record-id", "HARVEST-UI-001", "--source-key", "ui/source.png",
                "--classification", "AUTO_PROMOTE", "--method", "SOURCE_LAYER",
            )
            self.assertNotEqual(bad_class.returncode, 0)

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
            data = json.loads((project / ".asset-vault/harvest.json").read_text(encoding="utf-8"))
            record = data["records"][0]
            self.assertTrue(record["contains_derived_generated_pixels"])
            self.assertFalse(record["project_asset_approved"])
            self.assertFalse((project / "assets/approved").exists())
```

- [ ] **Step 2: Run focused tests and verify RED.**

```bash
python -m unittest tests.test_project_asset_vault.ProjectAssetVaultTests.test_record_harvest_writes_local_only_hash_bound_metadata -v
python -m unittest tests.test_project_asset_vault.ProjectAssetVaultTests.test_record_harvest_rejects_invalid_enums_missing_files_and_links -v
python -m unittest tests.test_project_asset_vault.ProjectAssetVaultTests.test_record_harvest_marks_generated_recovery_as_derived_and_never_promotes -v
```

Expected: all fail because `record-harvest` does not exist.

- [ ] **Step 3: Add local Harvest constants and storage helpers to `tools/project_asset_vault.py`.**

Add near the existing state constants:

```python
HARVEST_NAME = "harvest.json"
HARVEST_CLASSIFICATIONS = {
    "REUSE_AS_IS",
    "VARIANT_SEED",
    "STRUCTURE_PATTERN",
    "STYLE_DNA",
    "REBUILD_FOR_REUSE",
    "ONE_OFF_KEEP",
    "REJECT_REUSE",
}
HARVEST_METHODS = {
    "SOURCE_LAYER",
    "MASK_CUTOUT",
    "MANUAL_OR_SEMANTIC_REBUILD",
    "DERIVED_GENERATIVE_RECOVERY",
}
```

Extend `paths()` with:

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
    records = data.get("records")
    if not isinstance(records, list):
        raise VaultError("harvest records must be a list")
    data["schema_version"] = 1
    data["authority"] = "local-vault-harvest-metadata"
    data["local_only"] = True
    return data
```

- [ ] **Step 4: Implement safe library-key resolution and `record_harvest`.**

Use the existing path safety primitives. The implementation shape must be:

```python
def _harvest_library_asset(p: dict[str, Path], config: dict[str, Any], key_text: str) -> tuple[str, Path, str]:
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
    if not record_id or any(ch not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_." for ch in record_id):
        raise VaultError("record_id must use only letters, digits, '-', '_', or '.'")

    source_key, _, source_hash = _harvest_library_asset(p, config, source_key_text)
    members = []
    for member_text in member_key_texts:
        member_key, _, member_hash = _harvest_library_asset(p, config, member_text)
        members.append({"source_key": member_key, "sha256": member_hash})

    harvest = load_harvest(p["harvest"])
    if any(item.get("record_id") == record_id for item in harvest["records"] if isinstance(item, dict)):
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

- [ ] **Step 5: Add the `record-harvest` CLI parser and dispatch.**

Parser:

```python
    harvest = sub.add_parser("record-harvest", help="Record local-only reusable visual harvest metadata")
    harvest.add_argument("--project-root", type=Path, required=True)
    harvest.add_argument("--record-id", required=True)
    harvest.add_argument("--source-key", required=True)
    harvest.add_argument("--classification", required=True, choices=sorted(HARVEST_CLASSIFICATIONS))
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
                f"record_id={record['record_id']} classification={record['classification']} method={record['method']}"
            )
```

- [ ] **Step 6: Document `.asset-vault/harvest.json` in `PROJECT_LOCAL_ASSET_VAULT_POLICY.md`.**

Update the vault tree:

```text
.asset-vault/
├─ library/
├─ archive/
├─ inbox/
├─ state.json
├─ sync.json
└─ harvest.json        # local-only reusable-visual classification/provenance metadata
```

State explicitly:

```text
record-harvest != image decomposition
record-harvest != PROJECT_ASSET_APPROVED
record-harvest != promote
```

Document one example command:

```powershell
python tools/project_asset_vault.py record-harvest --project-root . `
  --record-id "HARVEST-UI-001" `
  --source-key "gpt-imports/2026-08-16/ui-screen.png" `
  --classification "REBUILD_FOR_REUSE" `
  --method "MANUAL_OR_SEMANTIC_REBUILD"
```

- [ ] **Step 7: Run the full Asset Vault suite and verify GREEN.**

```bash
python -m unittest tests.test_project_asset_vault -v
```

Expected: all existing vault behavior plus the three harvest tests pass. Existing deletion/tombstone, promotion, path-safety, and local-only assertions must remain green.

- [ ] **Step 8: Commit Task 3.**

```bash
git add tools/project_asset_vault.py tests/test_project_asset_vault.py docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md
git commit -m "feat: record local reusable visual harvest metadata"
```

---

### Task 4: Bind the four owners together with a final cross-surface regression

**Files:**
- Modify: `tests/test_bca_visual_sheet_workflow.py`
- Modify: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`
- Modify: `templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md`

**Interfaces:**
- Consumes: Task 1 policy/planning contract, Task 2 Figma reuse fields, Task 3 `.asset-vault/harvest.json` record.
- Produces: explicit linkage field `asset_vault_harvest_record_id` in the working plan and Figma harvest card, while preserving separate approval authorities.

- [ ] **Step 1: Add one RED cross-owner regression to `tests/test_bca_visual_sheet_workflow.py`.**

Add a test method following the file's existing `ROOT/read_text` style:

```python
    def test_reusable_visual_harvest_links_without_collapsing_authority(self) -> None:
        image_policy = (ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md").read_text(encoding="utf-8")
        vault_policy = (ROOT / "docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md").read_text(encoding="utf-8")
        figma_policy = (ROOT / "docs/VISUAL_COLLABORATION_TOOL_POLICY.md").read_text(encoding="utf-8")
        image_plan = (ROOT / "templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md").read_text(encoding="utf-8")
        figma_profile = (ROOT / "templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md").read_text(encoding="utf-8")

        for content in (image_plan, figma_profile):
            self.assertIn("asset_vault_harvest_record_id", content)

        self.assertIn("Reusable Visual Harvest Gate", image_policy)
        self.assertIn("harvest.json", vault_policy)
        self.assertIn("reuse promotion", figma_policy)
        self.assertIn("PROJECT_ASSET_APPROVED", image_policy)
        self.assertIn("promote", vault_policy)
        self.assertIn("runtime", figma_policy.lower())
```

Before the linkage-field edit, expect failure because Task 1 uses `harvest_record_id` while Task 2 uses `asset_vault_harvest_record_id`.

- [ ] **Step 2: Run the specific test and verify RED for the naming mismatch only.**

Use the actual class name from `tests/test_bca_visual_sheet_workflow.py`:

```bash
python -m unittest tests.test_bca_visual_sheet_workflow -v
```

Expected: existing BCA tests pass; the new method fails only because `asset_vault_harvest_record_id` is not present in both working surfaces.

- [ ] **Step 3: Normalize the linkage field to `asset_vault_harvest_record_id`.**

In `GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`, replace Task 1's provisional field:

```yaml
harvest_record_id:
```

with:

```yaml
asset_vault_harvest_record_id:
```

In `FIGMA_VISUAL_BIBLE_PROFILE.md`, keep the same exact field in the Reusable harvest card. Do not add the local harvest JSON content or absolute paths to Figma.

Update the Task 1 focused test token from `harvest_record_id` to `asset_vault_harvest_record_id` during implementation so all tests use the final interface name.

- [ ] **Step 4: Run all focused suites.**

```bash
python -m unittest \
  tests.test_visual_requirement_gate \
  tests.test_visual_collaboration_capability_contract \
  tests.test_project_asset_vault \
  tests.test_bca_visual_sheet_workflow \
  -v
```

Expected: PASS with no skipped tests introduced by this feature.

- [ ] **Step 5: Run repository contract/freshness validation required by the changed owners.**

Run the repository's existing commands/workflows rather than inventing new checks. At minimum execute locally when available:

```bash
python -m compileall tools/project_asset_vault.py tests
python -m unittest tests.test_visual_requirement_gate tests.test_visual_collaboration_capability_contract tests.test_project_asset_vault tests.test_bca_visual_sheet_workflow
python tools/check_canonical_reference_freshness.py
```

If the exact freshness checker command differs on current `main`, discover it from the existing workflow and use that canonical command; do not add a duplicate workflow.

- [ ] **Step 6: Run adversarial regression review before declaring implementation complete.**

Attack and verify these specific failures:

```text
A. one-off visuals accidentally become reusable library obligations
B. primary-use quality becomes subordinate to separability
C. Figma reuse classification becomes product-asset approval
D. record-harvest implicitly syncs/promotes or calls a provider
E. generated occlusion recovery is represented as source truth
F. harvest metadata stores absolute project paths
G. deleted local candidates are silently resurrected by harvest metadata
H. PR #428 file overlap appears after main moves
```

Only validated `MUST_FIX` / approved `SHOULD_FIX` findings are patched, followed by the same focused tests.

- [ ] **Step 7: Commit Task 4.**

```bash
git add \
  tests/test_bca_visual_sheet_workflow.py \
  tests/test_visual_requirement_gate.py \
  templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md \
  templates/project-operations/FIGMA_VISUAL_BIBLE_PROFILE.md
git commit -m "test: bind reusable visual harvest authority boundaries"
```

- [ ] **Step 8: Refresh against latest `main` without touching open PR branches.**

Before ready/merge:

```text
1. Read current main SHA.
2. Re-read PR #428 changed filenames.
3. Compare this PR's changed filenames to #428.
4. If overlap is non-empty, stop merge and classify `PROVISIONAL_INTEGRATION_REQUIRED` or defer the overlapping file; never edit #428.
5. If main advanced only through non-overlapping completed work, synchronize this branch using repository-approved history policy.
6. Re-run exact-head CI.
```

- [ ] **Step 9: Require exact-head GitHub validation and evidence ceilings.**

Required before any merge claim:

```text
Validate Base v9 Operating Contracts = SUCCESS
Validate Game Project Operating System = SUCCESS
Validate BCA Visual and Sheet Workflow = SUCCESS when triggered/applicable
Dependency Review = SUCCESS when triggered/applicable
unresolved review threads = 0
same-goal duplicate PR check = clear
main freshness = current
```

Do not claim the following from repository tests:

```yaml
real_image_layer_quality: NOT_RUN
real_figma_reusable_component_mutation: NOT_RUN
real_godot_runtime_reuse: NOT_RUN
real_project_scene_background_ux_pilot: NOT_RUN
human_visual_quality_improvement: NOT_RUN
```

---

## Post-implementation pilot contract

After this repository implementation is merged and only when a real project provides eligible visual inputs, run exactly three small pilots rather than bulk-migrating assets:

```text
1. one in-game composite
2. one background
3. one UX screen
```

For each, record:

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

The pilot is the first evidence allowed to justify a later segmentation/decomposition adapter. Do not install SAM 2, LayerDecomp, DiffDecompose, Qwen-Image-Layered, or another model merely because the contract exists.

## Rollback

- Task 1/2/4 are documentation/template/test changes and can be reverted as isolated commits.
- Task 3 adds only local `.asset-vault/harvest.json` metadata behavior; reverting the code leaves any existing local harvest file inert and does not delete candidate or promoted assets.
- No migration of existing project assets is performed.
- No tracked product asset is automatically created or removed.
- No Figma file mutation is part of this implementation.
- If a later implementation needs a different harvest schema, migrate local metadata explicitly; do not reinterpret old records silently.
