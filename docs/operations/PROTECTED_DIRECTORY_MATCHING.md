# Protected Directory Matching

## Contract

Project adapter `protected_paths` entries ending in `/` represent one exact repository directory and every descendant path.

```text
data/        → data, data/file.json, data/deep/file.json
scripts/     → scripts/main.gd, scripts/domain/item.gd
scenes/      → scenes/main/main.tscn
assets/      → assets/ui/icon.png
addons/      → addons/plugin/plugin.gd
```

A directory pattern does not match a similarly prefixed sibling.

```text
data/        does not match database/
data/        does not match data_backup/
scripts/     does not match scripts-old/
```

Path comparison uses the existing repository normalizer:

- Windows `\` separators become `/`;
- Unicode is normalized to NFC;
- matching is case-folded;
- explicit-file and wildcard patterns keep their existing `fnmatch` behavior.

## Adoption

Existing project adapters that already use canonical entries such as `data/`, `scripts/`, `scenes/`, `assets/`, and `addons/` do not need content migration. They gain descendant protection only after adopting a Base validator commit that contains the fixed matcher.

Projects pinned to an older validator remain affected until their adapter/workflow pin is separately upgraded and verified. This Base change does not silently rewrite project pins.

## Approval reconciliation

Externally approved protected-path changes remain exact-path approvals. The approval manifest must equal the detected normalized protected path set; parent directories, wildcard approvals, subsets, supersets, and prefix-only approvals do not reconcile the error.

## Loop Engineering boundary

Generic A2 product writers must not rely on descendant protection until the project has adopted the fixed Base validator and its exact nested-path pilot has passed. A3 auto-merge remains fail-closed unless a project later adopts a separately validated allowlist.

## Evidence

Base issue: `#314`.

Focused regression: `tests/test_protected_path_descendant_matching.py`.

The complete Base v9 workflow consumes that regression from `.github/workflows/validate-base-v9-rc.yml`.
