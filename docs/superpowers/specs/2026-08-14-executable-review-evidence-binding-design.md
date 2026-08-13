# Executable Review Evidence Binding Design

- Date: 2026-08-14
- Status: APPROVED_AND_IMPLEMENTING
- Work Mode: REVIEW
- Owner: `reviewing-and-validating-project-changes`
- Owner Mode: `claim-and-intent-verification`
- Governance disposition: extend implemented BCP-2026-027; do not create a duplicate ACTIVE Skill or duplicate BCP owner
- Source main observed at start: `39936ff6a83410b4169878c1335de9eb3e4c25cf`
- Implementation PR: `#330`

## Problem

Base already requires exact-ref readback, actual diff, exact HEAD execution evidence, Evidence ceiling, and post-merge main readback. The remaining gap was executable binding: policy and tests could prove that the required words and routes existed without independently checking that a material completion claim mapped to the actual diff and a freshly executed check.

The design must distinguish these states:

- a file or test definition exists;
- the implementation path is part of the actual reviewed diff;
- the declared command was executed at the reviewed Git state;
- the command exited successfully and emitted an expected marker;
- the observed evidence level is sufficient for the claim;
- the command preserved the reviewed HEAD, diff, and clean worktree;
- integration was actually merged and read back from `main`.

## Existing Solution First

Decision: `ABSORB`.

BCP-2026-027 already owns Claim and Intent Verification. A new hallucination-prevention Skill or new broad governance proposal would duplicate authority. The executable layer is therefore added to the existing owner through:

- canonical tool: `tools/check_review_evidence.py`;
- input contract: `skills/reviewing-and-validating-project-changes/contracts/review-record.schema.json`;
- generated-result contract: `skills/reviewing-and-validating-project-changes/contracts/review-result.schema.json`;
- task template: `templates/quality/REVIEW_EVIDENCE_RECORD.json`;
- compatibility package entrypoint: `skills/reviewing-and-validating-project-changes/scripts/verify_evidence.py`;
- adversarial behavior tests executed by existing required workflows.

The abandoned `bcp-028` branch is not authoritative and is not merged. No Registry entry is added for it.

## Architecture

```text
approved intent + protected scope + material claims
→ REVIEW_EVIDENCE_RECORD
→ reviewer-supplied trusted base ref
→ exact base SHA + exact HEAD + ancestry + clean worktree
→ actual changed-file inventory
→ slash-aware allowed/protected path gate
→ Acceptance-to-implementation-path gate
→ explicit command execution with shell=False
→ executable allowlist + timeout + exit code + required marker
→ post-command exact Git state recheck
→ Evidence ceiling
→ REVIEW_EVIDENCE_RESULT
→ independent adversarial review
→ existing post-merge main readback gate
```

## Trust boundaries

| Boundary | Rule |
|---|---|
| Producer-authored record | Input only; it cannot self-declare PASS or authoritative SHA |
| Trusted base | Supplied by reviewer/CI and resolved to an actual ancestor commit |
| Current implementation | Derived from Git HEAD, clean status, and actual diff |
| Scope pattern | `*` never crosses `/`; `**` may include descendants; brackets are literal repository characters |
| Command execution | Disabled unless explicitly requested; argv list with `shell=False` |
| Executable authority | Current Python is allowed by default; every other program requires exact reviewer allowlisting |
| Success | Exit code 0, all required output markers, and unchanged post-command repository state |
| Evidence level | Default maximum `TEST`; `RUNTIME` or `RENDER` requires per-check reviewer approval; `HUMAN` is never synthesized |
| Integration | Pre-merge result remains `BLOCKED_UNVERIFIED` until merged state, merge SHA, main readback, and post-merge checks are independently observed |

## Failure behavior

The verifier is fail-closed for:

- malformed Schema, duplicate IDs, or dangling references;
- unresolved/non-ancestor base, dirty worktree, or empty diff;
- changed paths outside scope or protected paths in the diff;
- Acceptance paths that are unchanged, deleted, or absent at HEAD;
- omitted execution, unapproved program, timeout, non-zero exit, or missing marker;
- commands that mutate HEAD, the changed-file set, or the clean worktree;
- evidence below the required level;
- completion claims without passing implementation, verification, and intent evidence.

A confident report cannot override these states.

## Benchmark synthesis

- Chain-of-Verification separates production from verification; producer claims are treated as leads, not evidence.
- OWASP LLM09:2025 identifies misinformation and overreliance risks; independent verification and explicit limits are retained.
- GitHub required checks bind integration decisions to current commit evidence; this design binds local review claims to exact base/HEAD state.
- SLSA provenance demonstrates subject identity; this design adopts exact subject binding without adding signing infrastructure.
- NIST AI 600-1 supports documented automated and human evaluation with confabulation controls; lower evidence is not promoted into human evidence.

Adopted: exact subject identity, deterministic-first checks, independent verification, evidence ceilings, regression cases.

Excluded: a new ACTIVE Skill, mandatory external Eval SaaS, arbitrary shell execution, automatic runtime/human promotion, and pre-merge integration PASS.

## Validation design

The behavior suite covers:

- valid exact-Git PASS;
- `NOT_RUN` when commands are declared but not executed;
- unchanged implementation paths;
- failed command and missing success marker;
- unapproved executable;
- protected and undeclared changes;
- stale/no-op base and dirty worktree;
- default TEST ceiling, rejected self-declared runtime, and explicit runtime approval;
- literal bracket paths such as `[proposal]/**`;
- single-star patterns that must not include nested directories;
- a command that prints a success marker but mutates the reviewed repository.

The existing Skill Behavior Evidence workflow executes the verifier through `tests/test_skill_implementation_evidence.py`. The Game Project Operating System workflow supplies package integrity, reference freshness, governance, and broad regression evidence. No separate implementation-evidence index entry is needed because the existing owner already has executable repository evidence and the new consumer is directly executed by required CI.

## Rollback

Revert the single implementation merge. The tool, schemas, template, tests, Skill link, compatibility entrypoint, reference-freshness companion rule, design/plan/evidence documents, and PR metadata roll back together. BCP-2026-027 and product repositories remain intact.
