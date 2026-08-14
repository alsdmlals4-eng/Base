# Adversarial Review — Expression Windows Subscription Import Portability

Date: 2026-08-15
Issue: #413
PR: #417

## Attack → validate critique → minimal refinement → regression recheck

### Attack 1 — Is the Expression test environment actually clean?

**Risk:** Installing Sprite Studio first can pull in `httpx2` and hide an Expression dependency gap.

**Finding:** The first consolidated workflow installed Expression and Sprite together, so its Ubuntu pass was not accepted as clean dependency evidence.

**Refinement:** Install only Base contracts + Expression Studio first, run the Expression endpoint test, then install Sprite afterward.

**Result:** Clean Ubuntu Expression-only execution passed. Current pinned `openai==3.0.0` already brings the TestClient dependency transitively, so no duplicate Expression `httpx2` dev dependency was added.

### Attack 2 — Where does Windows fail after #410 shared staging?

**Validation:** On Windows, the shared portable Asset Vault staging regression passed before the Expression endpoint ran. The Expression endpoint then returned 422.

**Diagnostic refinement:** The existing success assertion was changed only to include `response.text`, then RED was rerun.

**Exact RED:** `{"detail":"approved anchor source must be a readable regular file without links"}`.

**Verdict:** shared staging is not the remaining blocker; the failure is Expression-local anchor reading.

### Attack 3 — Is the anchor reader actually POSIX-only?

**Validation:** Expression `_read_project_image` used descriptor-relative `os.open(..., dir_fd=...)` and `O_NOFOLLOW`, matching the Sprite pre-#410 Windows failure pattern.

**Refinement:** Reuse Base's reviewed trusted-file readers:
- POSIX: `read_regular_nofollow`
- Windows/portable: `read_regular_portable_nofollow`

The existing 25 MiB size bound, optional SHA-256 check, PNG/JPEG/WebP allowlist, and 4096 px image limit remain unchanged. Shared staging is not modified in this PR.

### Attack 4 — Did the change weaken link/reparse safety?

**Validation:** The selected Base portable reader rejects symlink/reparse components and revalidates file identity around the bounded read. Expression already has `test_service_rejects_a_source_symlink_before_reading_it`, while Base owns the portable-reader security contract.

**Verdict:** the local reader is reused rather than reimplemented.

### Attack 5 — Did the fix accidentally authorize a paid/provider route?

**Validation:** The exercised endpoint remains `subscription_handoff_import` with `CHATGPT_INCLUDED`, `INCLUDED_OR_LOCAL_HANDOFF`, and `provider_call_made=false`. No OpenAI/provider/Figma/browser code path is added by this PR.

**Verdict:** no cost-authority expansion.

### Attack 6 — Did Expression portability break Sprite or shared staging?

**Validation:** The consolidated Visual Studio portability matrix runs shared staging regression first, then Expression import, then installs Sprite and runs the existing Sprite pose/effect `CHATGPT_INCLUDED` endpoint regression.

**GREEN evidence:** run `31833858095` passed the complete Ubuntu and Windows matrix after the reader fix.

### Attack 7 — Does this collide with protected in-progress PRs?

**Validation:** #373's changed-file inventory does not include Expression `service.py`, `test_import_api.py`, or `pyproject.toml`; this PR does not modify #373-owned models/engine/catalog/web/character tests/Tool Hub adapters. #376 Figma Bridge and #386 Windows child/supervisor files are untouched.

**Verdict:** no protected product-source collision.

## TDD / debugging evidence

- Initial mixed-dependency run was rejected as insufficient evidence because Sprite could mask Expression dependencies.
- Clean-environment RED workflow isolated Expression before Sprite installation.
- Ubuntu: shared staging + Expression import passed before the fix.
- Windows: shared staging passed, Expression import failed 422.
- Diagnostic rerun exposed exact anchor-read error.
- Minimal production fix changed only the Expression anchor reader to reuse Base trusted readers.
- GREEN run `31833858095`: Ubuntu and Windows shared staging, Expression import, and Sprite pose/effect import all passed.
- Final exact-head required gates must be rerun after this review record; this document alone is not merge evidence.

## Findings

- P0: 0
- P1: 0 after the portable anchor-reader refinement
- P2: Windows portable reads retain Base's documented local-account-trusted threat model and do not claim POSIX-equivalent malicious same-user rename-race guarantees.

## IRG ceiling

After final exact-head GREEN, this work proves fixture-PNG local Expression/Sprite import, validation, provenance, and project-confined staging on Ubuntu/Windows. It does not prove ChatGPT Pro-generated pixels, character identity quality, outfit/scene quality, live Figma mutation/readback, Windows Tool Hub child ownership, or real game-project asset consumption.
