# Base Structure and BCP Conflict Recovery Design

## Approval and scope

- Approval source: the user's current request, including permission to adjust skills or work order after adversarial review.
- Work class: repository-wide audit with a bounded five-file mutation surface: one evidence-preserving BCP documentation repair, one executable regression-test update, and three audit/design/plan records.
- Protected boundaries: do not invent missing BCP content, do not mix unrelated proposal lineages, do not add a Skill without an independent responsibility boundary, and do not commit, push, or create a PR without explicit GitHub mutation authorization.

## Findings that shape the design

1. Base already has a coherent canonical chain: `AGENTS.md` routes to `START_HERE.md`, `docs/OPERATING_MODEL.md`, the Skill Registry, trigger-selected Skill packages, and focused validators.
2. The root instruction file is below the current Codex default project-instruction byte ceiling, and detailed procedures are already routed into Skills and references.
3. All 30 ACTIVE Skills have registered package and behavior-coverage contracts. The BCP lifecycle already has one clear owner: `managing-base-change-proposals`.
4. No registered behavior-evaluation result demonstrates a BCP-concurrency routing failure. Session-only exploratory controls informed brainstorming but are not persisted independent model evidence and are not reported as a formal PASS. Existing responsibility boundaries therefore remain the deciding evidence against a new Skill.
5. Current BCP-023 is the Ten Paces retained-instance proposal. Its body hash is unchanged from its first PR #298 proposal commit through current `main`.
6. The GRIMOIRE proposal that temporarily used BCP-023 in PR #295 was reallocated to current BCP-024. Two provenance facts disappeared at different transitions: the transient external HTTP 525 followed by same-head Star Runtime POC success was present in PR #293's BCP-022 but absent by PR #295's BCP-023; `GM-GODOT-AUTHORING-GUT-TEST-AUTHORITY-01` remained through PR #296 and disappeared in PR #297's final BCP-024.

## Chosen approach

Use a minimal, lineage-correct repair:

1. Add a regression assertion that current BCP-023 remains Ten Paces, current BCP-024 remains GRIMOIRE, and the latter's collision-recovery audit retains both recovered markers, the distinct PR transitions, and its non-approved implementation boundary without making project-only facts an active Base implementation contract.
2. Restore only those facts to current BCP-024. Do not alter current BCP-023.
3. Record the repository structure, benchmarks, BCP-021 through BCP-025 collision lineage, hashes, omissions, and no-change decisions in one audit report.
4. Run focused BCP tests, the proposal checker, repository validation, diff checks, and a fresh remote PR/status read.

## Rejected alternatives

| Alternative | Rejection reason |
|---|---|
| Add a new BCP-concurrency Skill | No independent input/output/authority boundary and no reproduced routing failure. |
| Expand `managing-base-change-proposals` | No registered behavior-evaluation result demonstrates a failure, and the responsibility already has an owner; extra text would increase context cost without demonstrated benefit. |
| Put old GRIMOIRE content into current BCP-023 | Current BCP-023 belongs to Ten Paces and is byte-identical across its proposal history. This would corrupt provenance. |
| Restore every wording difference from old drafts | Most differences are intentional compression or project-only detail. Only independently evidenced omissions are restored. |
| Adopt merge queue or repository-wide workflow changes | Operationally broader than the demonstrated documentation defect and requires repository governance decisions outside this repair. |

## Definition of done

- The regression test fails before the repair and passes after it; a targeted mutation of either recovered audit marker also fails.
- Current BCP-023 remains uncontaminated and traceable to Ten Paces.
- Current BCP-024 contains the two recovered provenance facts and the existing PR #293/#295/#296 collision record.
- The audit report classifies every BCP-021 through BCP-025 conflict outcome and states evidence limits.
- No new Skill, Registry entry, dependency, or broad workflow is introduced.
- Full available validation passes; environment-only skips remain explicitly classified rather than promoted to PASS.
