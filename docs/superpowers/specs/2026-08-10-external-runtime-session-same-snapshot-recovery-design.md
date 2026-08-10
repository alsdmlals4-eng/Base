# External Runtime Session Same-Snapshot Recovery Design

## Status and authority

- Proposal: `BCP-2026-015-external-runtime-session-same-snapshot-recovery`
- Approval: `APPROVED_FOR_IMPLEMENTATION` in `[수정제안서]/PROPOSAL_REGISTRY.json`
- Approval reference: `[수정제안서]/BCP-2026-015-external-runtime-session-same-snapshot-recovery/PROPOSAL.md#승인과-구현`
- Scope decision: the approved proposal and the user's 2026-08-10 continuation instruction.

## Goal

When an external Editor/MCP runtime session is absent from a server registry or disagrees with process and transport observations, classify recovery only from a short same-snapshot evidence window.  Prevent unsafe mutation, stale identity reuse, and shared-server disruption while keeping product/runtime validation separate.

## Existing-solution decision

| Approach | Decision | Reason |
| --- | --- | --- |
| Add a new runtime-recovery Skill | Reject | The existing Godot Live Editor safety contract owns the identity, transport, recovery, and runtime boundaries. |
| Add a schema, validator, or transport implementation | Reject | This proposal defines a fail-closed operating classification; it does not provide a production external transport or a reproducible runtime server harness. |
| Extend the current Godot Live Editor security/recovery contract, project-local adapter guidance, and handoff boundary | Adopt | It adds the missing same-snapshot classification where current consumers look for safe recovery rules without duplicating responsibility. |

## Design

### Recovery evidence and classification

The canonical Godot Live Editor security/recovery document will require four observations within one bounded observation window:

1. current exact target process identity;
2. live expected transport owned by that current process;
3. bounded server-side connection, handshake, authentication, reconnect, or registration logs; and
4. an immediate exact-target session-registry read.

The resulting classification is limited to these states:

- `EXACT_SESSION_RECOVERED` only when the exact current process, its expected live transport, and exact target registry session are all present.
- `SAME_SERVER_HANDSHAKE_REGISTRATION_BLOCKER` only when the exact current process and its transport are present, the immediate registry omits the exact target, and bounded server logs belong to the same observation window.
- `PROCESS_OR_TRANSPORT_BLOCKER` when the exact process is absent or the expected transport is not currently owned and live.
- `BLOCKED_UNVERIFIED` when the observation window or any required evidence is missing.

If a previously observed process is no longer present, the record must use `PROCESS_EXITED_OR_NO_LONGER_RUNNING` with `REASON = UNVERIFIED`; it must not infer crash, kill, timeout, or normal exit.

### Safety and ownership boundaries

One absent target session never authorizes restarting a shared server, ending unrelated Editors, selecting a different project session, sending a mutation to another project, or patching executor/session matching before root-cause evidence exists.  Historical PID, WebSocket connection, and session ID values remain historical evidence only; a fresh current read is required before they can guide a new action.

`SESSION_RECOVERY_GREEN` allows only the approved target-specific runtime work to resume. It does not imply a product test, import, smoke, human QA, release, or production-readiness pass.

### Consumers

- `docs/knowledge/godot/GODOT_LIVE_EDITOR_SECURITY_AND_RECOVERY.md` is the canonical recovery authority.
- `templates/project-operations/godot-live-editor/addons/base_live_editor_adapter/README.md` gives project adopters the same safe operational sequence without claiming that the network-disabled adapter can perform external-session diagnosis.
- `skills/maintaining-project-context-and-handoff/SKILL.md` adds only the stale PID/session handoff boundary, not a second recovery procedure.
- Tests assert the required classification words and safety rules, then the proposal lifecycle is updated after an implementation PR exists.

## Excluded and protected scope

- No new Skill, Registry entry, schema, validator, external transport, MCP server, runtime debugger, network listener, or process-control implementation.
- No OMENWARD PID, port, session ID, Windows path, feature data, PR/Issue number, or runtime metric in active Base guidance.
- No change to release locks, generated release artifacts, v2 schemas, existing BCP-005 implementation records, or product repositories.

## Error handling and rollback

Missing same-window evidence remains `BLOCKED_UNVERIFIED`; it never becomes a more specific diagnosis.  The implementation is documentation and focused contract tests only, so rollback is one implementation-PR revert restoring the prior operational wording and Registry lifecycle state.

## Acceptance criteria

- The canonical recovery source names all four same-snapshot observations and all four permitted classifications.
- The `SAME_SERVER_HANDSHAKE_REGISTRATION_BLOCKER` path requires current process, current transport, immediate registry omission, and bounded same-window logs.
- Shared-server restart, unrelated session selection/mutation, stale identity reuse, and false product-Green inference are explicitly forbidden.
- The template and Handoff consumers retain their focused responsibilities and do not claim external transport support.
- Focused tests fail before the contract wording is added, then pass after the minimal implementation.
- Proposal Registry and proposal metadata record the implementation PR only after the PR is actually created and merged.

## Verification

- Focused standard-library contract tests for canonical wording and boundary separation.
- Existing BCP lifecycle and Godot Live Editor contract suites using the repository's `jsonschema` environment.
- Canonical-reference freshness check against the exact fetched `origin/main` base and implementation head.
- Adversarial mutation: remove a same-snapshot guard and prove the focused test fails before restoration.
