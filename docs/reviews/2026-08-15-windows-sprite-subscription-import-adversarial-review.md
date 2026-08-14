# Adversarial Review — Windows Sprite Subscription Import Portability

Date: 2026-08-15
Issue: #407
PR: #410

## Attack → validate critique → minimal refinement → regression recheck

### Attack 1 — Is `CHATGPT_INCLUDED` actually accepted by the real Sprite endpoint?

**Validation:** A new FastAPI `/api/import-runs` regression sends four ordered PNGs with `declared_source=CHATGPT_INCLUDED` for both `sprite_action` and `effect_stages` and requires `subscription_handoff_import`, `INCLUDED_OR_LOCAL_HANDOFF`, and `provider_call_made=false`.

**Finding:** Ubuntu passed. Windows initially failed before provenance handling completed.

### Attack 2 — Was the first Windows failure a provenance defect?

**Finding:** No. The normal PNG anchor existed, but Sprite `_read_project_image` used POSIX-only `dir_fd + O_NOFOLLOW` operations.

**Refinement:** Reuse Base's reviewed `read_regular_nofollow` on POSIX and `read_regular_portable_nofollow` on Windows. Do not duplicate another Windows file-validation implementation.

### Attack 3 — Did anchor portability fully unblock Windows?

**Finding:** No. The next RED moved forward to Asset Vault run creation and failed because shared staging still used POSIX `dir_fd` and `/proc/self/fd` assumptions.

**Refinement:** Preserve all existing POSIX descriptor-backed code unchanged. Add Windows-only portable branches for directory creation, stable-tree revalidation, file write, and confined read using lstat/reparse checks and pre/post file/directory identity validation.

### Attack 4 — Can a Windows reparse/symlink route escape the Asset Vault?

**Validation:** A Windows-only regression places a directory link at `.asset-vault/library/generated` and attempts run creation. The run fails closed before any `outside/sprite` directory is created. On the observed runner the earlier Git-ignore gate rejects the linked route before the later reparse gate; the test accepts any reviewed fail-closed gate rather than overfitting one error string.

**Verdict:** no outside write observed.

### Attack 5 — Can an existing hard link make a write overwrite an external inode?

**Validation:** Existing Base regression `test_staging_write_replaces_a_hard_link_without_overwriting_its_external_inode` is now run in the Ubuntu/Windows focused workflow. Windows portable write unlinks the reviewed regular target and creates a fresh `O_EXCL` file before writing.

**Verdict:** protected external inode remains unchanged in the observed run.

### Attack 6 — Did Windows support weaken POSIX staging?

**Validation:** Every new path is guarded by `os.name == "nt"`. Existing POSIX descriptor opens, `dir_fd`, `/proc/self/fd` stable aliases, inode comparisons, and no-follow writes remain in their original branch. Focused Ubuntu import/staging regressions remain green.

**Verdict:** no intentional POSIX semantic downgrade.

### Attack 7 — Is Windows claiming the same anti-race guarantee as POSIX?

**Validation:** No. Base's existing portable trusted-file threat model treats the local OS account as trusted while rejecting links/reparse points and checking identity around operations. Windows staging follows that same model. It does not claim the stronger POSIX guarantee of continuing writes through an already-open directory inode after a malicious same-user rename swap.

**Verdict:** truthful platform-specific security ceiling retained.

### Attack 8 — Was a test dependency hidden in the environment?

**Finding:** Current Starlette `TestClient` requires `httpx2`, but `sprite-animation-studio[dev]` did not declare it. Tests only worked where another environment happened to supply the client dependency.

**Refinement:** Add `httpx2>=2.9,<3` to Sprite's dev extra so the focused environment is reproducible.

### Attack 9 — Does this overlap protected in-progress PRs?

**Validation:** #373 does not own Sprite/shared staging files; #376 does not modify shared staging; #386 owns Tool Hub process supervision, not Studio Asset Vault implementation. No protected PR file is modified here.

**Verdict:** no changed-file collision with protected in-progress product work.

## Evidence history

- RED 1: focused workflow could not collect Sprite tests from repo root; workflow working directory corrected.
- RED 2: TestClient dependency missing; `httpx2` declared in Sprite dev extra.
- RED 3: Windows normal anchor read failed; portable trusted reader reuse added.
- RED 4: Windows Asset Vault directory creation failed; portable staging branch added.
- GREEN: run `31830967809` — Ubuntu and Windows real pose/effect import endpoint both passed.
- Security refinement run `31831351669`: Ubuntu all PASS; Windows normal staging + hard-link tests PASS, linked-directory test correctly failed closed but its expected error text was too narrow; assertion refined to accept any reviewed fail-closed gate while retaining the outside-write assertion.
- Final exact-head run after this review/workflow cleanup is required before merge; this document alone is not PASS evidence.

## Findings

- P0: 0
- P1: 0 after Windows staging portability and reproducible-test refinements
- P2: Windows portable path intentionally has a weaker same-user race guarantee than POSIX descriptor pinning; accepted by the pre-existing Base portable trusted-file threat model and explicitly not overclaimed.

## IRG ceiling

Proved after final GREEN: fixture PNG transport/validation/provenance, project-confined Windows/Ubuntu staging, and safe local import lifecycle. Not proved: AI pose/effect visual quality, ChatGPT browser generation, Figma delivery/readback, Tool Hub Windows child ownership (#386), or real game-project asset consumption.
