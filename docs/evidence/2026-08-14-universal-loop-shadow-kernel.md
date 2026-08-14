# Universal Loop SHADOW Kernel Evidence

## Identity

- Program issue: `#321`
- M3 implementation issue: `#335`
- M3 PR: `#337`
- Original TDD source main: `39936ff6a83410b4169878c1335de9eb3e4c25cf`
- Final integration refresh source main: `b8481e5e9a2e7f0def7dc9fd4487f440e24fc83b`
- Isolated branch: `m3-shadow-kernel-20260814`
- Pre-refresh branch preserved as: `backup-m3-shadow-kernel-pre-refresh-20260814`
- M2 dependency: PR `#333`, merged as `b1317f2c1b83e57f016ce4efd4e169bf7c0acd90`

## Path ownership

M3 writes only:

```text
tools/loop_shadow_kernel/**
tools/loopctl.py
tests/test_loop_shadow_kernel*.py
tests/fixtures/loop-shadow-kernel/**
docs/LOOP_ENGINEERING_SHADOW_KERNEL.md
docs/evidence/2026-08-14-universal-loop-shadow-kernel.md
.github/workflows/validate-loop-shadow-kernel.yml
```

It does not modify M2 Schema, Template, Capsule validator, Capsule test, Base-v9 workflow, A2 Runtime, Project Adapter v2, Tool Hub, or project-product paths.

## Initial TDD RED

- Exact test-only head: `b74fb7a8e7c1c98e69b61c4c16c1c42fdebe1c63`
- Dedicated GitHub Actions run: `31752366270`
- Ubuntu job: `94620699012`
- Windows job: `94620699002`
- Result on both platforms: `17` expected failures.
- Failure boundary: the production package `tools.loop_shadow_kernel` and CLI `tools/loopctl.py` did not exist.
- No pre-existing Base contract failure was attributed to the new tests.

## Minimal GREEN and adversarial loop

The first minimum implementation passed the original `17` tests locally. Independent adversarial inspection then introduced new failing regressions before remediation, including:

1. path-like `project_id` or `run_id` values could escape status/lease namespaces;
2. a corrupt historical receipt could be skipped instead of blocking the run;
3. an internal `.loop-engineering/projects` symlink could redirect trusted state;
4. the mutable lease ledger lacked an exclusive concurrent-update guard;
5. missing authority references were not yet exercised by the hardening suite;
6. nested state roots could produce ambiguous state placement;
7. duplicate normalized lease entries needed explicit fail-closed handling.

The remediation added:

- closed identifier validation for state lookup paths;
- physical and lexical state-tree confinement;
- receipt digest verification and corruption blocking;
- exclusive receipt publication without overwrite;
- bounded exclusive lease guard and atomic lease replacement;
- missing-reference and duplicate-lease regressions;
- stable blocked outcomes for busy, corrupt, or unsafe state.

## Covered adversarial injections

- stale source-main SHA;
- cross-project identity;
- `../` and `..\\` path escape;
- absolute/drive/path normalization rejection;
- Unicode NFC duplicate path collision;
- symlink reference escape;
- internal state-root symlink;
- path-like status/lease identifiers;
- missing Requirement Coverage;
- incomplete Coverage and missing Evidence;
- unapproved output;
- missing authority reference;
- Planning conflict and unverified drift;
- new visual design without human Visual Lock;
- semantic lease conflict, corrupt ledger, and busy lease guard;
- duplicate successful input;
- repeated failure and `NO_PROGRESS`;
- immutable receipt overwrite;
- corrupt prior receipt;
- transition budget and illegal transition;
- forbidden model/network/subprocess imports;
- A3, Scheduler, and autonomy escalation.

## Production surface

- typed states, findings, request, coverage, reference, budget, and outcome records;
- deterministic canonical JSON and SHA-256 digests;
- closed request parser;
- project-bound path and state isolation;
- typed state machine;
- atomic state storage, leases, and immutable receipts;
- deterministic `ShadowKernel`;
- read-only `loopctl validate|shadow|status|leases` CLI;
- dedicated Ubuntu and Windows CI.

## Preserved boundaries and non-claims

- No model Provider was called.
- No credential or paid API was used.
- No product, planning Canon, scene, data, asset, or Figma file was changed.
- No pull request is created or merged by the Kernel itself.
- A3 auto-merge remains disabled.
- Scheduler remains `NOT_CONFIGURED`.
- M2 PR #333 is consumed only as a merged prerequisite and is not modified by M3.
- M4/A2 Runtime paths are not modified by this work.
- No project migration or real A2 Builder/Critic runtime is claimed.

## Final integration gate

Before PR #337 can merge:

1. dedicated exact-head Ubuntu and Windows jobs must pass;
2. all repository-required jobs for the exact head must pass;
3. open-PR changed-path overlap must be zero;
4. unresolved review threads must be zero;
5. independent review must report P0/P1 `0`;
6. current `main` must remain compatible at merge time;
7. squash merge must use expected-head protection;
8. postmerge `main` readback and push workflows must pass.

Final exact-head run IDs and merge evidence are recorded in the PR after those external gates complete.

## Rollback

Revert PR #337. M3 does not migrate product data; disposable SHADOW state may be deleted only after evidence export and only outside trusted project Canon.
