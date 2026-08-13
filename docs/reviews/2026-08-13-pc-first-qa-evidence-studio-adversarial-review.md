# PC-First QA Evidence Studio Adversarial Review

## Review scope

- Initial inspected base: `1e5f8c1ce297898597d1afc52776d9592a790051`
- Final rebased main parent: `c5dff35af099647937233ed0f2cfa3269e70db75`
- Reviewed PR head: `255e502470369e1779ad34716e12cbe31c2f293a`
- Squash merge: `07ca8366e6007f13ecb6ae945abfb4564fa2e4d7` via PR `#328`
- Product slice: reviewed Tool Registry, machine-local project binding, typed QA child launch, developer-only PC evidence workflow
- Explicit exclusion: Android connection, external tester recruitment, product image/UX quality approval, Expression/Sprite Hub launch

## Attack and critique validation

| Attack | Validation | Decision |
|---|---|---|
| The tool could turn a developer checkbox into false playtest proof. | Real risk. The current user is the only tester. | Reviewer identity is fixed to `DEVELOPER_OWNER`; external tester state remains explicit; no usability-population claim is emitted. |
| PC PASS could hide untested Android. | Real risk. Many projects target Android later. | Android is a separate immutable `DEFERRED_NOT_CONNECTED` axis with a release-preparation gate; PC finalization cannot change it. |
| Review could start before the visuals and UX exist. | Real risk and directly contradicts the approved sequence. | Result writes fail until a non-empty developer acknowledgement moves the session out of `PREPARING_VISUAL_UX`. |
| A Hub endpoint could become arbitrary local command execution. | Real risk. | Registry forbids raw command fields; `/api/launch` accepts only tool/project IDs; the first adapter constructs a fixed argv list and uses `shell=False` with a clean environment. |
| A project path containing spaces could split or route to another project. | Valid attack. | Root is one argv element; v2 adapter project ID, locator fingerprint, startup report, nonce, PID, health project ID, and root fingerprint are cross-checked. |
| Local evidence could escape or become tracked project content. | Valid attack. | Exact Git root, project `.gitignore`, untracked Asset Vault, component link/reparse checks, and fixed output root are enforced. |
| The evidence folder could be replaced with a link after session creation. | Valid time-of-check/time-of-use attack. | Every atomic write now rechecks that its immediate output directory is a real directory rather than a symlink or reparse point; a regression test verifies no outside file is created. |
| A caller could label evidence with an invented 40-character commit. | Valid provenance attack. A syntactically valid SHA is not proof that the reviewed build exists. | Session creation now fails unless `git cat-file` confirms the value is a commit in the bound project repository. |
| A project-controlled display label could execute script in the Hub. | Valid stored-XSS attack. | Hub rendering constructs DOM nodes and assigns the label through `textContent`; a regression contract forbids user labels in `innerHTML`. |
| Automated tests could be reported as actual game UX validation. | Real reporting risk. | Documentation and final evidence distinguish tool-flow tests from game-specific human image/UX review. |
| Starting all three registered Studios would satisfy the Hub goal faster. | Invalid for this slice; it expands process and secret boundaries without need. | Only QA is runnable. Expression/Sprite remain discoverable and independently runnable until separate typed adapters are reviewed. |

## Findings

- `MUST_FIX`: none after commit-provenance and stored-XSS fixes passed their regression tests.
- `SHOULD_FIX`: add a real Windows multi-project/process-tree smoke before labeling Tool Hub Phase 1 production-ready.
- `USER_DECISION_REQUIRED`: none inside the approved PC-first slice.
- `DEFER`: Android device connection and external-user usability testing.
- `BLOCKED_UNVERIFIED`: real project image/UX quality, browser pixel/render inspection (Chromium unavailable in the verification environment), Windows PowerShell execution, long-running child supervision, Expression/Sprite Hub launch.

## Integration evidence

- PR exact-head workflows: Dependency Review, Game UX/UI, Evidence Knowledge, Base v9, and Game Project Operating System all `SUCCESS`.
- Post-merge main workflows: Game UX/UI run `31717421783`, Base v9 run `31717421828`, and Game Project Operating System/`ci-gate` run `31717421892` all `SUCCESS`.
- Merge SHA readback confirmed `tools/TOOL_REGISTRY.json`, `tools/tool-hub/README.md`, and `tools/qa-evidence-studio/README.md` on `main`.
- The Windows CI result is a publication smoke only; it does not promote the unexecuted real Windows multi-project Tool Hub runtime to verified.

## Rollback

Revert the feature merge commit. No project canon, Godot scene, runtime asset, Figma file, Android setting, or external service is modified. Machine-local project locator and Asset Vault QA session folders may be preserved as evidence or removed manually after stopping the local processes.
