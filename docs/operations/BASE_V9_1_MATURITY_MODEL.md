# Base v9.1 dual-axis maturity model

Operating maturity and product evidence answer different questions. They never average, roll up, compensate for one another, or replace critical gates.

## Operating maturity

| Level | Meaning |
|---|---|
| `OM-L0` | Canonical adapter is absent or invalid. |
| `OM-L1` | Canonical adapter, registries, and required paths exist. |
| `OM-L2` | Pins, hashes, routes, aliases, and generated views validate. |
| `OM-L3` | Protected paths and collaboration workflow are enforced in local checks and CI contracts. |
| `OM-L4` | Project change evidence demonstrates repeatable migration and recovery. |
| `OM-L5` | Multiple release cycles demonstrate stable maintenance without authority drift. |

## Product-evidence maturity

| Level | Meaning |
|---|---|
| `PE-0` | No product evidence has been run. |
| `PE-1` | Intent and measurable player hypothesis are recorded. |
| `PE-2` | Static or prototype evidence exists. |
| `PE-3` | Representative runtime/play evidence exists. |
| `PE-4` | Target-device, accessibility, and human evidence covers critical flows. |
| `PE-5` | Repeated release evidence supports product decisions across cohorts or cycles. |

## Critical gates

Static, runtime, device, accessibility, and human gates use `PASS / FAIL / NOT_RUN / NOT_APPLICABLE / BLOCKED`. A `FAIL` remains visible regardless of `OM-L*` or `PE-*`. `NOT_RUN` is not failure and never becomes PASS through documentation volume.

Every claimed maturity step consumes one structured evidence record, so a
self-reported level is capped by available metadata. `OM-L5`, `PE-5`, and GDD
Sheet `CURRENT` therefore require their respective operating, product, or Sheet
evidence. A gate `FAIL` derives verdict `FAIL`; otherwise any `BLOCKED` derives
`BLOCKED`; otherwise any applicable `NOT_RUN` derives
`PASS_WITH_NOT_RUN_GATES`; only fully evidenced applicable gates derive `PASS`.
