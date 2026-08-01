# Security Policy

## Supported versions

Base is a living operating kit rather than a deployed service. Security fixes are made against the current default branch.

| Surface | Status |
|---|---|
| `main` | Supported |
| Frozen release snapshots | Not supported |
| Downstream project copies | Not supported |

Frozen locks and snapshots preserve historical identity and are not independently patched. A downstream project must report vulnerabilities in its own repository; if the defect originates in shared Base material, report it to Base as well.

## Reporting a vulnerability

Do not disclose sensitive vulnerability details in a public issue, pull request, discussion, commit message, or log.

1. Prefer [GitHub private vulnerability reporting](https://github.com/alsdmlals4-eng/Base/security/advisories/new).
2. Include the affected path and commit, impact, reproducible steps or proof of concept, and any known mitigation. Remove secrets, credentials, personal data, and unrelated private material.
3. If the private reporting form is unavailable, open a detail-free public issue asking `@alsdmlals4-eng` to establish a private channel. Do not include the vulnerability itself.

Private vulnerability reporting availability is `UNVERIFIED_REPOSITORY_SETTING` until the live repository setting or form is verified. This policy does not claim that a file can enable that GitHub setting.

The maintainer will acknowledge a usable report when it is reviewed, communicate the next step through the private channel, and close or publish it only after the disclosure boundary and remediation status are agreed. No fixed response or remediation deadline is promised.

## Scope

Security reports may include unsafe code execution in repository tools or workflows, credential or private-data exposure, dependency or supply-chain compromise, path traversal or destructive file handling, and permission-boundary bypasses. General bugs, feature requests, game design disputes, and third-party project defects without a Base origin belong in their normal project tracker.
