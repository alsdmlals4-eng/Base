# Base #314 Protected Descendant Matching Evidence

## Scope

- Issue: `#314`
- PR: `#332`
- Source main: `3e3f59b1b835f9675f0b8dbc4543a6c69a526c36`
- Protected owner: `tools/project_operating_contract.py::_protected_match`

## RED

- Test-only exact head: `daed9d7406a1c79a761abfca6f3b0b47533963a2`
- Base v9 workflow: `31722887298`
- Result: `334` tests executed, `10` expected failures, `1` configured Godot skip.
- Expected failures were limited to exact directory and descendant matching under canonical directory patterns, including Windows separators, case-folding, Unicode NFC, and `scripts/`, `scenes/`, `assets/`, and `addons/` descendants.
- Sibling-prefix rejection, explicit-file behavior, wildcard behavior, and exact multiple-path approval reconciliation already passed.

## Minimal GREEN implementation

Production commit created by a bounded temporary mutation workflow:

```text
f8bf40e73a5f380b2d31a5d7c884ad8a5eb66608
```

The implementation adds one normalized-pattern helper. Directory patterns ending in `/` use exact directory-boundary or descendant-prefix semantics; all other patterns retain `fnmatch.fnmatchcase`.

The approval reconciler was not modified because the RED proved its exact-set behavior was already correct.

## Temporary execution boundary

The two temporary mutation workflows and two temporary scripts were removed before final exact-head validation. They are not part of the final PR surface.

## Final verification target

- focused descendant regression;
- v9.1 project operating-contract regressions;
- approved protected-change gate regressions;
- generated/integrity checks;
- complete Base v9 PR workflows;
- independent adversarial review;
- unresolved review threads `0`;
- merge-time main freshness and path-overlap preflight;
- squash merge and postmerge push workflows.

## Non-claims

- Blacksmith product files are not modified by this Base PR.
- Project adapter pins are not automatically upgraded.
- A3 auto-merge and Scheduler are not enabled.
- Android, visual, playtest, and human evidence are not applicable to this matcher-only change.

## Rollback

Revert the eventual PR #332 squash merge. No project data or save migration is required.
