# Loop A2 Integration Evidence

## Identity

- Tracking issue: `#357`
- PR: `#358`
- Source main: `141fcab50d55e050637f736840d257bef9f6413c`
- Prerequisites already on main: M2 `#333`, M3 `#337`, Capsule→SHADOW `#356`, A2 Foundation `#343`, Git worktree/Diff `#351`, Project Test Executor `#354`.

## Initial TDD RED

- Test-only head: `698b9e22d03fa9b2f5c0f8b2b76a068fe23feff4`
- A2 run: `31782988414`
- Existing A2 tests passed.
- New integration module failed to import because `tools.loop_a2_runtime.integration` did not exist.
- Result boundary: one expected new-module error; no existing A2 regression was attributed to the new tests.

## Minimum GREEN

- Minimal production module head: `739c3b12f0ef18b400d6aef58e46c1f54067fa38`.
- It implemented closed receipt verification, actual changed-path equality, generated branch naming, non-force branch push, typed PR provider boundary, merged-head/check/thread/main gates, and immutable `CLOSED` receipt publication.
- A2 Foundation validation passed after the minimal implementation.

## Adversarial RED

Independent review found two integration gaps that filename-only handoff could not safely cover:

1. an operational provider must not accept FAKE/non-eligible A2 receipts;
2. content could change under an already-reviewed path while `changed_paths` remained identical.

Adversarial tests were committed at `2a837590292b69d4465894773faee01f6e78daf6`. The intentional RED was the missing operational `GhPullRequestProvider` / content-attestation API while all existing integration and A2 tests remained GREEN.

## Adversarial remediation

Production head `a601a8abad3c915a7fce1e01070cb249d368e47f` added:

- `compute_worktree_diff_sha256()` over HEAD, binary tracked diff, and all untracked bytes/symlink targets;
- operational-provider requirement for `provider_mode=REAL` plus `integration_eligible=true`;
- mandatory reviewed Diff SHA-256 for operational handoff;
- same-path content-drift detection;
- `GhPullRequestProvider` with fail-closed CLI/auth preflight, argv-only subprocesses, bounded secret-free environment, PR creation, direct PR/check/main/review-thread readback, and merge-in-main comparison;
- `close_postmerge_from_provider()` so production closure can source GitHub evidence directly instead of trusting model inference;
- reviewed Diff digest in handoff and immutable closure receipts.

The A2 Foundation run on that remediation passed.

## Boundaries

This slice does not:

- invoke Codex, GPT, or another model;
- create or approve new product scope;
- merge a PR;
- force-push, push `main`, delete refs, or alter repository settings;
- mutate Planning Lock, Visual Lock, Figma, assets, or project product data outside the reviewed worktree;
- enable A3 auto-merge;
- configure a Scheduler;
- persist API keys, GitHub tokens, or hidden reasoning.

The integration layer may create a commit, push only its generated `loop-a2/<project>/<run>` branch, and request a PR through its provider. Merge remains outside this slice. Closure occurs only after direct merged evidence passes all gates.

## Final integration gate

Before merge:

1. dedicated Ubuntu/Windows integration jobs PASS on the exact head;
2. A2 Foundation PASS;
3. Base-v9 PASS;
4. Game Project OS PASS;
5. Dependency Review PASS;
6. unresolved review threads `0`;
7. current-main compatibility check;
8. expected-head squash merge;
9. postmerge main readback and push validation.

## Rollback

Revert the eventual PR #358 squash merge. No project data migration or design change is part of this slice.
