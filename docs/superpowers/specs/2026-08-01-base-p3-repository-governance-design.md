# Base P3 Repository Governance Baseline Design

## Scope and baseline

- Repository: `alsdmlals4-eng/Base` (public, user-owned).
- Baseline: `main@4f49f1ed30d7f849417fb936fb1d5ab70ea8217f`.
- Work branch: `codex/base-p3-repository-governance`.
- This change governs repository reuse, vulnerability reporting, code ownership, and dependency update discovery. It does not change Base Registry bytes, released locks, generated artifacts, project repositories, Google Sheets, game code, or assets.

## Evidence

The baseline has no `LICENSE`, `SECURITY.md`, `CODEOWNERS`, or `.github/dependabot.yml`. It does have one root `package.json` declaring `pnpm@11.9.0` with `pnpm-lock.yaml`, one root `requirements-publication.txt`, SHA-pinned GitHub Actions, and a capability-aware dependency-review workflow.

Official GitHub references:

- [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository): a public repository without a license remains under default copyright; reuse, distribution, and derivative works are not granted.
- [Adding a security policy](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/add-security-policy): `SECURITY.md` should state supported versions and private reporting instructions.
- [About code owners](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners): `.github/CODEOWNERS` has highest location precedence, owners need write access, and the CODEOWNERS path itself should be owned.
- [About `dependabot.yml`](https://docs.github.com/en/code-security/concepts/supply-chain-security/about-the-dependabot-yml-file): the file belongs under `.github/` and each ecosystem needs a directory and schedule.
- [Supported Dependabot ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories): pnpm uses `npm`, requirements files use `pip`, and workflow actions use `github-actions`. The current table lists pnpm v7-v10, not the repository's pnpm v11.
- [Dependabot options](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference): groups may match `*` and restrict grouped updates to `minor` and `patch`; major updates can remain separately reviewable.

## Considered approaches

### A. Add only placeholder community files

Rejected. Placeholder ownership or contact data creates false safety, and an untested Dependabot file can be silently ignored.

### B. Add the four files with no repository contract

Rejected. This improves GitHub presentation but does not stop duplicate precedence files, unsupported ecosystems, public vulnerability disclosure, or owner drift.

### C. Add a minimal interlocked baseline with semantic regression coverage

Selected. The four platform surfaces remain small, while a mutable Base repository profile owns current identity without rewriting frozen release locks. One regression suite validates unique locations, current repository identity, supported scope, and real manifest/ecosystem mapping. The unconditional lightweight CI tier and conditional contract tier both run that suite.

## Decisions

### License

Use the standard MIT License with copyright `2026 alsdmlals4-eng`. Base presents itself as a reusable public operating kit; MIT supplies the missing permission to use, copy, modify, merge, publish, distribute, sublicense, and sell while preserving the notice and warranty disclaimer. README states `MIT` and links to the root file. This is a project policy choice, not legal advice, and it does not relicense third-party material that may carry its own notice.

### Security policy

Support the current `main` branch only. Frozen release snapshots are historical identities, and downstream project copies are supported by their project repository. If a defect originates in shared Base material, reporters should also notify Base.

Sensitive details must not be posted in a public issue. The first route is GitHub private vulnerability reporting at `https://github.com/alsdmlals4-eng/Base/security/advisories/new`. Repository-setting availability remains `UNVERIFIED_REPOSITORY_SETTING` until verified; if the form is unavailable, a reporter may open a detail-free issue asking the owner for a private channel.

### Code ownership

Create `.github/CODEOWNERS`, GitHub's highest-precedence location. Use the verified repository owner with admin/write access, `@alsdmlals4-eng`, as the default owner, and explicitly cover `/.github/` so ownership policy owns itself. Record the current owner in the mutable `docs/operations/BASE_GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`, and expose the same `owner` field in the project profile template; released `base*.lock.json` files stay frozen historical identities and are not current ownership inputs. Do not invent teams or domain owners that do not exist.

CODEOWNERS does not by itself prove required approval. The solo-maintainer Ruleset continues to require zero approvals, exact required checks, and resolved threads; repository settings remain separately verified.

### Dependabot

Enable the two root ecosystems that are currently documented as supported and retain a fail-closed deferral for pnpm:

| Ecosystem | Evidence | Schedule | Grouping |
|---|---|---|---|
| `npm` / pnpm | `package.json` declares `pnpm@11.9.0`, `pnpm-lock.yaml` | `DEPENDABOT_DEFERRED_PNPM_11` | GitHub currently documents pnpm v7-v10; do not downgrade or claim coverage |
| `pip` | `requirements-publication.txt` | weekly Monday 03:00 UTC | minor/patch grouped; major separate |
| `github-actions` | `.github/workflows/*.yml` | weekly Monday 03:15 UTC | minor/patch grouped; major separate |

Each enabled ecosystem has an open version-PR limit of five. Dependabot creates proposals only; it does not auto-merge and does not replace dependency review, exact-head CI, or human risk judgment. Security alerts and private vulnerability reporting are repository settings, not claims made true by this file. Add the `npm` entry only after GitHub officially documents pnpm 11 support and a real update run is available; do not solve this governance task by silently downgrading the project's package manager.

## Mechanical acceptance

- Exactly one supported location exists for each of LICENSE, SECURITY, CODEOWNERS, and Dependabot configuration.
- README links to the root MIT license and security policy.
- MIT grant, notice, disclaimer, year, and repository owner are present.
- Security policy marks `main` supported, historical releases/downstream copies unsupported, and forbids public sensitive disclosure.
- CODEOWNERS default and `.github/` owner equal the repository owner.
- Dependabot has exactly the supported `pip` and `github-actions` entries rooted at `/`, weekly and staggered in UTC, with minor/patch groups and major updates outside those groups; pnpm 11 is visibly deferred and not falsely claimed as covered.
- The unconditional docs-validation tier and conditional contract tier both run the new governance regression, so governance Markdown changes cannot bypass it.
- Registry, released locks, generated artifacts, and plugin metadata remain unchanged.

## Evidence limits

- License selection is not legal advice.
- Private vulnerability reporting enabled state is `UNVERIFIED_REPOSITORY_SETTING` until the repository setting or live form is verified.
- Dependabot parsing and first scheduled run are `NOT_RUN` until GitHub consumes the exact PR/merged configuration; pnpm 11 remains `DEFERRED_UNTIL_OFFICIAL_SUPPORT`.
- CODEOWNERS auto-request and Ruleset enforcement are `NOT_RUN` until exercised from the merged base branch.
