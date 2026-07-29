# Base v9 Integrity Audit

## Scope

This report defines the repository-wide integrity audit required for the v9 RC.
It covers tracked Base files and Base-generated derivatives. Project repositories,
their adapters, and Google Sheets are excluded from this audit.

## Checks and evidence

| Check | Evidence path | Status before final verification |
| --- | --- | --- |
| link | `check_base_v9_integrity.py` local Markdown-link scan | `PASSED` locally |
| Registry path | Registry/frontmatter generator validation | `PASSED` locally |
| template consumer | Package-integrity regression and linked-template checks | `PASSED` locally |
| legacy alias | Alias inventory, replacement, consumer, rollback path | `UNVERIFIED` for a new repository-wide manual disposition review |
| provenance | Lock, snapshot hashes, generator source, generated manifest | `PASSED` locally |
| orphan | Packaged reference/script and generated artifact checks | `PASSED` locally |
| cycle | Declared Skill dependency graph check | `PASSED` locally (no declared cycles) |
| duplicate responsibility | Generated responsibility-boundary check | `PASSED` locally |
| policy conflict | Canonical policy comparison and adversarial review | `UNVERIFIED` pending an evidence-backed adversarial review |
| test connection | Workflow definition and focused/full regression checks | `PASSED` locally; GitHub Actions `NOT_RUN` |

## Disposition protocol

No finding is deleted merely because it is old or redundant. Each finding records
consumers, replacement, provenance, and rollback before it receives one of:

- `KEEP`: current and referenced.
- `CONSOLIDATE`: preserve the surviving authority and migrate consumers.
- `ARCHIVE`: retain historical evidence outside active routing.
- `RETIRE`: remove active use only after consumer and rollback checks.
- `BLOCKED`: insufficient evidence, unknown consumer, or missing replacement.

## Final report rule

The final RC report replaces `PENDING` only with evidence-backed `PASSED`,
`FAILED`, `NOT_RUN`, or `UNVERIFIED`. A complete file inventory is not inferred
from a successful documentation check.
