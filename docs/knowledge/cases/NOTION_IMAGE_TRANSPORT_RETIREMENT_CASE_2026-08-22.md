# Notion Image Transport Retirement Case · 2026-08-22

## Status

`PATTERN`

## Trigger

v4.7 workspace cleanup had already established:

```text
Notion = human-facing project / visual / decision workspace
Repository = structured / implementation / runtime truth
Google Sheets = MIGRATION_ONLY_UNTIL_REMOVAL
Local project-management/file bridge = not an active/default route
```

A post-merge Notion readback then exposed a contradiction: the current image-delivery correction still used a temporary Google Sheet as a binary URL relay and kept a local binary bridge as fallback.

## Incident

The transport worked historically, but its success no longer made it an acceptable current architecture.

```text
historical technical success
!= current workflow authority
```

The stale path created three long-term problems:

1. a migration-only Sheet could silently return as a new active dependency;
2. a local helper could force PowerShell/installation/manual state back into a workflow explicitly simplified away from local tools;
3. future agents could read the presence of source/tests/plans as evidence that the bridge remained a preferred fallback.

## Alternatives compared

### A. Keep temporary Sheets transport

**Rejected.** It works, but directly violates the current no-new-Sheets boundary and recreates a second transport surface.

### B. Remove Sheets but keep the local binary bridge fallback

**Rejected.** It removes one stale dependency but preserves another retired project route and adds user environment/setup cost.

### C. Direct Notion attachment when actually callable; otherwise fail closed

**Adopted.**

```text
trusted direct HTTPS source or connector-native attachment source
→ current Notion attachment function
→ returned Notion-owned attachment representation
→ exact Project placement
→ destination readback
→ target-client observation when rendering matters
```

If the current client cannot expose a supported direct source/schema:

```text
BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT
```

Do not substitute Google Sheets, a local bridge, a new CDN relay, a paid automation service, or another retired workspace.

## What was preserved

The old transport still contributed reusable evidence:

- Notion can copy an external source into a Notion-owned attachment.
- The connector-returned attachment representation should be consumed as-is rather than reconstructed.
- destination readback is required.
- `READBACK_PASS != HUMAN_VISIBLE_PASS`.
- Android/iOS/browser pixel visibility requires actual client observation.
- Page/Home image success does not prove database Files/Gallery Preview support.

These principles were absorbed into the current connector/layout contracts before the obsolete implementation was removed.

## What was removed from active state

- temporary Google Sheet binary relay;
- local binary bridge default/fallback route;
- local bridge source package and Windows installer;
- bridge-specific active root regression;
- superseded bridge design/implementation/closure documents.

Git history remains the rollback/audit source. Removed files are not default discovery candidates.

## Validation rule

A future image-delivery path must prove, in order:

```text
DISCOVERED_AVAILABLE
→ CALLABLE_SCHEMA_PRESENT
→ INVOCATION_PASS
→ READBACK_PASS
→ HUMAN_VISIBLE_PASS when the claim depends on rendering
```

No step may be inferred from the next or previous step.

## Reuse condition

Apply this pattern when a previously successful transport/helper conflicts with a newer authority simplification or retirement decision.

The lesson is not “always delete fallback tools.” The lesson is:

> Once a fallback is explicitly retired, preserve its validated principles and evidence, remove its active consumers, and fail closed rather than silently resurrecting it.

## Reconsider condition

A new binary transport helper may be reconsidered only if:

- repeated real projects are blocked by `BLOCKED_NO_DIRECT_NOTION_BINARY_TRANSPORT`;
- the missing capability materially prevents approved project delivery;
- current Notion/connector capabilities and maintained existing solutions are rechecked;
- at least three viable approaches are compared;
- zero-incremental-cost and security/secret boundaries are satisfied;
- the user explicitly approves a new active tool boundary.
