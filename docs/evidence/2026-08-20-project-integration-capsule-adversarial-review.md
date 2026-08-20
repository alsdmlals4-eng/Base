# Project Integration Capsule Adversarial Review

## Scope and rule

Every loop reviewed the full feature: plan feasibility, authority, Git identity,
Notion identity/readback, Godot/HiGodot boundary, evidence, cost, schema, validator,
CLI, tests, documentation, CI, rollback, and PR overlap. A loop was not counted until
its new failure was reproduced RED, fixed, and the complete focused suite returned GREEN.

## Loop 1 — terminal state and no-write truth

- Attack: set top-level status to `BLOCKED_UNVERIFIED` while all nested claims passed.
- Attack: use different base/result commits or a dirty tracked worktree while declaring read-only.
- RED: missing `CAPSULE_STATUS_NOT_READY`, `READ_ONLY_COMMIT_DELTA`, and
  `TRACKED_WORKTREE_DIRTY` findings.
- Fix: require the exact verified terminal state, base=result, HEAD equality, and exact
  index/tree plus raw tracked worktree bytes.
- GREEN: focused suite passed.

## Loop 2 — cross-project identity

- Attack: point the capsule at another repository, nonexistent base branch, nested
  directory under a parent Git worktree, unapproved/missing Decision, or another Notion key.
- RED: all could avoid a specific identity failure.
- Fix: bind GitHub origin slug, exact Git top level, local branch/ref, Decision content,
  Project ID, repository, Notion Project Key, and Record Key.
- GREEN: focused suite passed.

## Loop 3 — evidence meaning and provenance

- Attack: hash `{}` as Notion or writer evidence; use malformed Last Edited; use an
  untracked evidence file with a matching hash.
- RED: arbitrary bytes could support the former readiness claim.
- Fix: require RFC3339 time, exact semantic receipt fields, official Notion MCP
  search/fetch source label, writer canary actor/path/result, required evidence levels,
  and existence at `result_sha`.
- GREEN: focused suite passed.

## Loop 4 — existing authority and cost reclassification

- Attack: copy arbitrary HiGodot version/pin into the Capsule, point Base project
  identity elsewhere, omit protected Godot path classes, or label `OPENAI_API` as included.
- RED: duplicated/unverified authority and cost self-classification were accepted.
- Fix: remove duplicated version/pin ownership, hash-bind and parse existing
  `PROJECT_BASE_ADAPTER` and `HIGODOT_ADOPTION_RECORD`, require canonical forbidden
  paths, and close the included-service allowlist.
- GREEN: focused suite passed.

## Loop 5 — hidden Git state and evidence graph

- Attack: add untracked or ignored Godot files, hide a tracked mutation with
  `skip-worktree`, advance `origin/main`, orphan the writer receipt, or use another rollback ref.
- RED: the snapshot and Evidence graph could overstate exactness.
- Fix: scan untracked and ignored authoring paths, reject index visibility overrides,
  require local/fetched origin refs to match, require exactly one of each receipt and map
  both to PASS Acceptance, and require rollback=base=result.
- GREEN: focused suite passed with 21 tests; two further RED/GREEN tests added tracked
  Decision and deterministic three-part Notion Record Key enforcement.

## Independent final attack — raw bytes, release identity, and crash safety

- Attack: use a committed Git clean filter to hide changed `project.godot` bytes.
- Attack: hide `.gdshader` through ignore rules, point an adapter version at another
  existing Base commit, or provide list/dict shapes that crash nested semantic checks.
- RED: filtered bytes and shader passed; malformed Adapter, Adoption, and writer receipts
  raised exceptions; any existing Base commit passed the former release check.
- Fix: initially compare critical raw worktree bytes to committed blobs,
  reject ignored paths outside generated `.godot/**` cache and the exact Capsule sidecar,
  reuse the canonical Project Operating Contract release-lock/finalization validation,
  type-guard nested receipts, and fail closed at the CLI boundary.
- GREEN: focused suite passed with 28 tests. A later full-tree attack below superseded
  the critical-file-only implementation and broad `.godot/**` exception.

## Independent deep attack — executable validation and claim-ceiling closure

- Attack: configure a repository clean filter whose command writes into `.git`; the
  former `git diff` cleanliness check executed it even on an otherwise clean project.
- Attack: mutate a non-critical tracked file behind a clean filter, stage different
  index bytes while restoring HEAD bytes in the worktree, or add a gitlink/submodule.
- Attack: hide an autoloaded `.gd` script inside ignored `.godot/**`.
- Attack: make required index/untracked/ignored probes fail through unreadable Git
  index or exclude configuration and rely on the former nonzero-result silence.
- Attack: append free-form `OTHER / E6_HUMAN_PLAYTEST` evidence and a production-pass
  Acceptance, set rollback drill to `FAIL`, or self-attest billing as included.
- RED: every attack either passed with no Finding or caused a validator-side effect.
- Fix: remove worktree `git diff`; compare index mode/object/stage with `result_sha` and
  raw bytes for every tracked regular file; disable lazy fetch, optional locks, and
  fsmonitor; reject gitlinks and tracked symlinks; narrow generated-cache allowlists and
  forbid authoring/executable suffixes; close v1 to one fixed Acceptance and exactly two
  receipt kinds; require every snapshot probe to fail closed on nonzero; require rollback
  `NOT_APPLICABLE`; reclassify cost as a declared policy.
- GREEN: focused suite passed with 49 tests at that checkpoint, including clean-filter non-execution,
  full-tree raw bytes, hidden index state, gitlink, `.godot` script, Evidence ceiling,
  rollback contradiction, and cost-claim regressions.

## Independent closure attack — process context, mode, time, and release reads

- Attack: inherit `GIT_DIR`, `GIT_WORK_TREE`, or `GIT_INDEX_FILE` so every nominal
  `git -C <project>` probe reads another repository.
- Attack: toggle only a tracked file's POSIX executable bit while keeping its blob and
  index unchanged.
- Attack: use `datetime.fromisoformat()`-accepted ISO8601 spellings with a space separator
  or colonless offset even though the contract requires RFC3339.
- Attack: let canonical Base release/evidence/finalization validation fall back to the
  older Git helper, where a partial clone could lazy-fetch or write optional locks and an
  `OSError` could escape the Capsule finding boundary.
- RED: all four paths reproduced as false-pass, unsafe process context, or uncaught error.
- Fix: scrub inherited `GIT_*`; compare POSIX executable state with tree mode; require a
  full RFC3339 lexical match before date parsing; inject the Capsule's no-lazy-fetch,
  no-lock, fail-closed Git runner into the complete Base release-lock/finalization path;
  preserve the release index's legacy two-argument validator call compatibility when no
  runner override is requested.
- GREEN: focused suite passed with 55 tests, and the focused plus Base v9.4.1/v9.4.2/
  v9.4.3 release compatibility set passed with 79 tests.

## Independent review

Three read-only reviewers independently identified false-pass paths. Their blocking
findings covered terminal status, dirty/untracked/hidden Git state, executable Git
filters, gitlinks, project/remote/base
identity, Decision approval, arbitrary receipt bytes, duplicated HiGodot authority,
cost reclassification, claim-ceiling expansion, empty Acceptance mapping, and rollback
ambiguity. Every concrete local false-pass reproduced during this review was converted
to a regression test and remediated; this is not a claim that no future attack exists.

The reviewers also correctly noted that a locally created receipt is not a cryptographic
attestation from Notion, GitHub, or a running editor. The design therefore changed from
`READ_ONLY_READY` to `READ_ONLY_BINDING_VERIFIED` and caps evidence at
`LOCAL_RECEIPT_BINDING_ONLY`.

## Open PR isolation

PR #556 was inspected read-only. None of its known paths were modified. In particular,
this change does not touch `README.md`, `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`,
the operating/retirement policies, the reusable module registry, or #556's tests/evidence.
Discovery is limited to `templates/project-operations/README.md`, the dedicated contract,
CLI, tests, and the existing validation workflow.

## Evidence ceiling and residual risks

- A user with repository write access can fabricate local receipts; Git history and
  review make that auditable, not impossible.
- `refs/remotes/origin/*` is only as fresh as the immediately preceding fetch.
- No target project or Notion workspace was supplied, so no live connector, editor,
  mutation, runtime, visual, or playtest evidence exists.
- ChatGPT Pro custom MCP is read/fetch only under current OpenAI guidance; a custom
  ChatGPT write surface would require a plan/capability change.
- Cost fields are a declared architecture policy. They do not attest plan, invoice,
  quota, or remaining Actions allowance.
- The required caller-side fetch may update `.git` metadata. The no-write boundary is
  product/Notion/Godot mutation, not immutable Git metadata.
- v1 rejects gitlinks/submodules and tracked symlinks instead of claiming recursive
  verification it does not perform.
- v1 accepts only 40-hex SHA-1 commit identities. SHA-256-format repositories are
  explicitly out of scope and fail schema validation rather than receiving partial support.

These are not hidden behind PASS. The highest permitted claim is local receipt binding.

## Validation ledger

| Check | Result |
|---|---|
| Focused integration suite | PASS — 55 tests |
| Focused + Base release compatibility regression | PASS — 79 tests |
| Required Base v9 CI-equivalent suite | PASS — 429 tests, 1 intentional skip |
| Full unittest discovery | 1,972 tests; same 19 unrelated failures as clean `e222e93` baseline (1,917 tests), 37 skips; feature adds 55 passing tests and no failure |
| Generated artifacts/integrity + v9.4.1/v9.4.2/v9.4.3 | PASS at trusted `e222e93` |
| `git diff --check` / `git fsck --strict` / `py_compile` | PASS |
| Independent final code review | PASS — two latest-tree approvals, no P0/P1 |
| GitHub PR checks and post-merge main | pending |
