# BCP-2026-014 Evidence — Handoff Contract-Surface Preservation

## Evidence status

- collected_at: `2026-08-10`
- source project: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- project evidence ceiling: exact GitHub PR/main/workflow evidence
- external evidence: official engineering/operations documentation only
- human cross-project pilot: `NOT_RUN`
- Base active implementation: `NOT_STARTED_IN_THIS_STAGE`

## 1. Project evidence

### 1.1 Handoff compression exposed hidden consumers

Source PR: Ten Paces `#135` — `docs: refresh current session handoff state`.

Baseline project main at work start:

```text
43841d3cc6667d821c10df75272b239f314f3df0
```

The goal was to replace a stale, overgrown Active Context/Handoff with a compressed live router while preserving existing canonical owners.

The rewrite did not change product code, Scene, Resource, data, `project.godot`, or export preset. Nevertheless, exact-head validation failed as text that appeared historical or duplicative had been serving as machine/discovery contract surface.

The recovery sequence found several categories rather than one accidental token:

```text
historical lineage locator
canonical owner locator
current mutable-state token
core-rule discovery locator
product/observation/growth authority marker
```

Concrete examples discovered by existing validation included:

- historical lineage markers such as earlier PR/Issue/review state;
- canonical combat owner locator;
- a current product validation state marker;
- the project's `3/3/4` combat timing discovery locator;
- product/observation/growth discovery anchors.

The correct fix was **not** to restore stale values as current truth. The final Active Context explicitly separated current mutable state from historical/discovery compatibility markers.

Final exact PR head:

```text
c18d384b537ec3eaf49370d454d23e98c44ba3f4
```

Merge commit:

```text
69eba09c6d18f5b4a473c0be14361ddd745983a0
```

At the final PR head the project validation suite, including canonical/reference checks, was green and unresolved review threads were zero.

### 1.2 A second failure in the same work showed why consumer intent matters

After PR #135 merged, the default-branch `Validate Godot Live-Editor Pilot` workflow failed on main.

Run:

```text
31352827843
```

Observed failure:

```text
tests/test_godot_live_editor_adoption.py
1 failed, 5 passed
```

The test expected the entire editor plugin list to be exactly the historical Godot AI singleton representation. Current approved project state legitimately enabled:

```text
Godot AI
GUT
Hera
```

The actual contract was “Godot AI remains installed/preserved,” not “no other plugin may coexist.”

The same workflow had already failed on the prior main `43841d3c...` in run `31349838418`, proving this was not introduced by the handoff PR.

Follow-up project PR #136 changed only the assertion from singleton-array equality to semantic presence of the Godot AI plugin path.

Exact PR #136 head:

```text
4b9b12554b236c42ef24fa00d77af0c13c3406f7
```

At that exact head:

- `Validate Godot Live-Editor Pilot`: `SUCCESS`
- `PR Validation`: `SUCCESS`
- `Full Validation`: `SUCCESS`
- active toolchain/product/platform regressions: `SUCCESS`
- unresolved review threads: `0`

PR #136 merged as:

```text
dc95883873ccd8718f6aa5cb11f936ef39db42c7
```

Post-merge main run `31353193715` then passed both `adoption-contract` and the reusable `project-pilot` job.

### 1.3 Generalized project conclusion

The two failures support one bounded principle:

```text
Before rewriting/compressing a live router or other coordination surface,
inventory the consumers of its fields/markers/locators.

If a surface is required:
- preserve it in the correct current/historical/compatibility role, OR
- migrate the consumer to the actual semantic contract.

Do not preserve accidental representation merely because a brittle test exists.
Do not delete a consumed surface merely because it looks stale to a human editor.
```

This is still `PATTERN`, not `VALIDATED_PATTERN`, because a second independent project application has not yet been run.

## 2. Existing Base coverage and neighboring proposal

Current Base owner `maintaining-project-context-and-handoff` already defines Active Context/Handoff as compressed routers and owns `context-refresh`, `session-handoff`, and `resume`.

Current supporting owner `auditing-canonical-reference-freshness` covers stale/untouched consumers after canonical changes.

BCP-2026-013, already stored in Base main as `SUBMITTED`, addresses a different phase:

```text
BCP-013:
valid pre-merge live state
→ merge changes repository truth
→ live state becomes immediately stale
→ post-merge reconcile
```

BCP-014 addresses:

```text
live router rewrite/compression
→ required contract/discovery surface is removed or fossilized
→ exact-head consumer regression
→ preserve/migrate the semantic contract
```

They share an owner but have different triggers and failure times. The proposed disposition is therefore `ABSORB`, not a new Skill and not a duplicate of BCP-013.

## 3. External benchmark

### 3.1 Google Engineering Practices — Small CLs

Source:

```text
https://google.github.io/eng-practices/review/developer/small-cls.html
```

Observed official guidance:

- prefer one self-contained change;
- include related tests;
- smaller changes are easier to review, reason about, merge, and roll back;
- separate significant refactoring from unrelated behavior changes.

Application to this proposal:

```text
External pattern
→ focused, self-contained change plus related test

Current failure
→ context compression and hidden consumer behavior were initially reasoned about as one editing task

Adopted principle
→ when a consumer contract needs repair, keep that repair narrowly scoped and validate it independently
```

Limit:
Google's CL guidance does not prescribe handoff schemas, compatibility markers, or historical lineage fields. BCP-014 borrows only the scope/review/test discipline.

### 3.2 GitHub Docs — required status checks

Source:

```text
https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
```

Observed official guidance:

- required checks must succeed on the latest required commit SHA;
- earlier commit results do not satisfy the current required state;
- depending on repository state, the head or test-merge commit can be the required target;
- skipped required workflows can leave checks pending.

Application:

```text
Contract-surface rewrite
→ new exact HEAD
→ rerun the affected reference/contract validation
→ do not reuse pre-rewrite GREEN
```

Limit:
GitHub does not define what a Handoff locator is. This source supports evidence freshness, not the proposed surface classification itself.

### 3.3 AWS Prescriptive Guidance — ADR history and supersession

Sources:

```text
https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html
https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
```

Observed official guidance:

- preserve ADR history;
- old decisions can be marked Superseded rather than erased;
- accepted/rejected decisions form a decision log;
- non-compliant legacy artifacts may need separate gradual migration/technical-debt work.

Application:

```text
Historical/discovery information
→ do not mislabel it as current truth
→ but do not erase provenance merely because a newer current state exists
```

Limit:
An Active Context/Handoff is not an ADR. This benchmark supports the separation of current state from preserved history/provenance only.

### 3.4 Kubernetes — deprecation/compatibility discipline

Source:

```text
https://kubernetes.io/docs/reference/using-api/deprecation-policy/
```

Observed official guidance:

Kubernetes uses explicit compatibility/deprecation rules for consumed API/CLI surface and does not treat established stable surface as freely removable implementation detail.

Application by analogy only:

```text
Consumed coordination surface
→ identify consumers before removal
→ provide a migration path when representation changes
```

Limit:
A handoff Markdown marker is not a Kubernetes API. BCP-014 does **not** propose API-style versioning, minimum support periods, or formal deprecation windows for project documentation. The comparison is limited to consumer-aware removal discipline.

## 4. Adopt / reject / limit matrix

| External pattern | BCP-014 disposition | Reason |
|---|---|---|
| focused self-contained change + related test | `ADOPT` | lowers review and rollback risk for contract repairs |
| exact-current-head verification | `ADOPT` | directly matches observed regression recovery |
| preserve superseded history rather than overwrite | `ADAPT` | keep provenance, but current router must remain compact |
| compatibility-aware removal of consumed surface | `ADAPT` | use consumer inventory without importing API versioning machinery |
| mandatory preservation of every old string | `REJECT` | would fossilize stale/brittle representation |
| mandatory schema/version for every handoff field | `REJECT` | unjustified complexity at current evidence level |
| automatic post-merge writer | `DEFER` | belongs to separate evidence/security/BCP-013 implementation analysis |

## 5. Counterevidence and non-use conditions

The proposal should not apply when:

- the file is a dated historical snapshot rather than a live router;
- repository/reference/test/routing inspection finds no consumer;
- the surface is truly dead and canonical responsibility exists elsewhere;
- the edit is formatting-only and contract meaning does not change;
- a brittle consumer asserts accidental text shape and can be safely migrated to semantic intent.

A project with no machine-consumed handoff surface should not be forced to add compatibility sections or classification boilerplate.

## 6. Validation ceiling

Current evidence proves:

```text
Ten Paces project-level repeated failure mode: OBSERVED
focused project fixes: EXACT_HEAD_GREEN_AND_MERGED
post-merge PR #136 live-editor pilot: PASS
second independent project pilot of BCP-014: NOT_RUN
Base active implementation: NOT_RUN
human usability benefit: NOT_RUN
```

Therefore the proposal remains:

```yaml
knowledge_state: PATTERN
proposal_status: SUBMITTED
implementation_authority: NOT_GRANTED_IN_THIS_STAGE
```
