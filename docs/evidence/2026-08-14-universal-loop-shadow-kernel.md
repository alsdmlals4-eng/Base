# Universal Loop SHADOW Kernel Evidence

## Identity

- Program issue: `#321`
- M3 implementation issue: `#335`
- M3 PR: `#337`
- Source main: `39936ff6a83410b4169878c1335de9eb3e4c25cf`
- Isolated branch: `m3-shadow-kernel-20260814`
- M2 dependency owned by another workstream: PR `#333`

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

It does not modify M2 Schema, Template, Capsule validator, Capsule test, or Base-v9 workflow paths.

## Initial TDD RED

- Exact test-only head: `b74fb7a8e7c1c98e69b61c4c16c1c42fdebe1c63`
- Dedicated GitHub Actions run: `31752366270`
- Ubuntu job: `94620699012`
- Windows job: `94620699002`
- Result on both platforms: `17` expected failures.
- Failure boundary: the production package `tools.loop_shadow_kernel` and CLI `tools/loopctl.py` did not exist.
- No pre-existing Base contract failure was attributed to the new tests.

## Minimal GREEN and adversarial loop

The first minimum implementation passed the original `17` tests locally. Independent adversarial inspection then introduced four new failing regressions before remediation:

1. path-like `project_id` or `run_id` values could escape status/lease namespaces;
2. a corrupt historical receipt could be skipped instead of blocking the run;
3. an internal `.loop-engineering/projects` symlink could redirect trusted state;
4. the mutable lease ledger lacked an exclusive concurrent-update guard.

The minimum remediation added:

- closed identifier validation for state lookup paths;
- physical and lexical state-tree confinement;
- receipt digest verification and corruption blocking;
- exclusive receipt publication without overwrite;
- bounded exclusive lease guard and atomic lease replacement;
- stable blocked outcomes for busy or unsafe state.

## Fresh local verification

On the production source used for the final branch upload:

```text
python -m compileall -q tools \
  tests/test_loop_shadow_kernel.py \
  tests/test_loop_shadow_kernel_cli.py \
  tests/test_loop_shadow_kernel_adversarial.py

python -m unittest \
  tests.test_loop_shadow_kernel \
  tests.test_loop_shadow_kernel_cli \
  tests.test_loop_shadow_kernel_adversarial \
  -v
```

Result:

```text
Ran 21 tests
OK
```

A separate deterministic replay created two independent project workspaces with the same normalized request and fixed timestamp. Both generated the same immutable receipt digest:

```text
7e65e426293c49b96fc1f853f365b0a7ece95e7f6e5917c18835112f16148b98
```

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
- Planning conflict and unverified drift;
- new visual design without human Visual Lock;
- semantic lease conflict and busy lease guard;
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
- M2 PR #333 is not modified or completed by this work.
- No project migration or real A2 Builder/Critic runtime is claimed.

## Final integration gate

Before PR #337 can leave Draft or merge:

1. dedicated exact-head Ubuntu and Windows jobs must pass;
2. all repository-required jobs for the exact head must pass;
3. open-PR changed-path overlap must be zero;
4. unresolved review threads must be zero;
5. independent review must report P0/P1 `0`;
6. M2 dependency #333 must be merged or a separately reviewed proof must show M3 can integrate without it.

Final exact-head run IDs and merge evidence are recorded in the PR and issue after those external gates complete.

## Rollback

Revert PR #337. M3 does not migrate product data; test and pilot state under disposable `.loop-engineering/` directories may be deleted after evidence export.
