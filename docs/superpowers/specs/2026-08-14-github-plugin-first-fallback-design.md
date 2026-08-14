# GitHub Plugin-First Fallback Design

## Goal

Codex cloud or connector-only work must not stop merely because the `gh` binary or its local authentication is absent. Reuse an authenticated GitHub connector when it can perform the required repository operation, and request user action only when no available capability can complete the exact operation safely.

## Confirmed user outcome

- Do not ask the user to reinstall or re-authenticate GitHub CLI for every cloud chat.
- Apply the rule to Base and project work that consumes Base guidance.
- Preserve PR review, required checks, exact-SHA verification, and no-force-push safety.

## Capability order

1. Use the connected GitHub plugin/connector for supported repository reads and writes: branches, files or Git objects, PRs, merge operations, and available CI/status checks.
2. Use local `git` for checkout inspection, diff, staging, commits, and an authenticated push when available.
3. Use `gh` only for a capability not covered by the connector or local `git`, such as a required detailed Actions-log workflow in an environment where `gh` is already installed and authenticated.
4. If the exact required mutation or evidence is unavailable through every current capability, report that capability as `BLOCKED_UNVERIFIED`. Do not translate a missing optional CLI into a global task blocker.

When an authenticated local push is unavailable but connector Git-object writes are available, publish the already-verified local tree through blobs, a base tree, a commit, and a non-force branch-ref update before opening the PR.

## Repository changes

- Extend `skills/synchronizing-local-and-github-state/SKILL.md` with the capability matrix, fallback contract, and output evidence.
- Add a short invariant to `AGENTS.md` so all Base-guided work discovers the rule without loading every skill.
- Add `github-cli-missing`, `gh-auth-missing`, and `github-connector-fallback` routing triggers to the existing Skill Registry entry. Do not create a new Skill.
- Record the observed incident and correction in the Skill learning log.
- Add a focused contract test that fails on the current policy and passes only when the authority, routing, safety, and learning evidence are connected.

## Security and safety

- Never copy a user's Windows GitHub token into a cloud container.
- Never store `GH_TOKEN` as a non-secret environment variable to keep CLI authentication alive.
- Never force-update a branch to compensate for stale remote state.
- Re-read the remote base/head before the first persistent write, PR creation, and merge.
- Connector availability does not prove branch protection, required checks, or runtime validation; verify each separately.

## Acceptance criteria

1. A future agent encountering `gh: command not found` can identify the connected GitHub connector as the next path.
2. Missing `gh` alone cannot be reported as the reason to stop when connector coverage exists.
3. A genuinely unsupported operation remains fail-closed with the exact missing capability and no false completion claim.
4. Existing concurrent-change, secret, no-force-push, PR, CI, and exact-SHA gates remain intact.
5. Focused Base tests and the repository's relevant contract suite pass.

## Rollback

Revert the policy PR. No credentials, external service settings, generated binaries, or project repositories are migrated by this change.
