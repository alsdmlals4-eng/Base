# Blacksmith Canon / Visual / Handoff Learning Evidence · 2026-08-25

- Source project: `alsdmlals4-eng/Blacksmith`
- Source work: Blacksmith PR `#207` core-simplification planning/handoff, merged as `5c29af1e0bb633f8d4513aee16987a3ff9889a4b`
- Base original branch baseline: `4c49c8b79b52483713247ae22bd39f1bd60c733c`
- Classification: `VERIFIED_PROJECT_EVIDENCE_WITH_BOUNDED_BASE_PROMOTION`
- No Blacksmith gameplay values are promoted to Base.

## 1. Existing owner reuse and concurrency

The Blacksmith work exposed reusable failures in **current-state propagation**, **Visual approval boundaries**, **Notion visual delivery evidence**, and **handoff evidence**.

Reuse-first disposition:

- `auditing-canonical-reference-freshness` already owns `VERIFIED_SUCCESSOR_STATE / PREDECESSOR_CEILING_FREEZE`; this PR adds recurrence evidence instead of creating a new Skill.
- Base PR `#679 / BCP-2026-033` already owns adjacent scoped generated-visual approval proposal semantics; it remains read-only from this branch.
- Base main now contains merged PR `#683`, which submitted a proposal also named `BCP-2026-032` for AI visual continuity + Notion preview fallback and includes a verified low-resolution inline-SVG raster preview route.
- Independently, Base PR `#678` remains open with a different proposal also named `BCP-2026-032` for visual reference batching/delivery readback.

Therefore Base currently exposes an **existing proposal ID collision**:

```text
BCP-2026-032
  -> merged #683 / ninja-survival source
  -> open   #678 / Ten-Paces source
```

This Blacksmith PR does **not** rename, absorb, close, rebase, merge, or edit #678/#683. Treat the collision as `BASE_PROPOSAL_ID_COLLISION / INTEGRATION_RECONCILIATION_REQUIRED` and fail closed before creating another proposal with either identity.

## 2. Verified recurrence — predecessor ceiling freeze

Three independent current consumers in Blacksmith froze predecessor state after a verified successor decision advanced current authority:

1. `Validate Visual GDD Canon Scrub`
   - predecessor expectation: schema v1 + CURRENT/MAX structure owner + old repair semantics;
   - successor: Decisions `BS-ENHANCE-20260825-25 / BS-DAMAGE-20260825-26 / BS-CHRONICLE-20260825-27`;
   - correction: historical scrub assertions kept their old meaning while current binding assertions moved to the successor owner.

2. `Blacksmith Living GDD Home contract`
   - predecessor expectation: `BS-ART-20260825-02 / ART_STYLE_STATUS = REWORK_REQUIRED`;
   - successor: `BS-ART-20260825-03 / ILLUSTRATED_WORKSHOP_BOOK / USER_APPROVED_DIRECTION`;
   - correction: historical Decision03 snapshot checks stayed immutable while current `AGENTS.md` assertions advanced.

3. `test_current_active_context_priority_overlay`
   - predecessor expectation: old `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION` and frozen 2026-08-20 Active Context as current router;
   - successor: `BLOCKED_UNTIL_CURRENT_PLANNING_COMPLETE_DECLARATION`, Decisions25~27/Art03, and the new session handoff/current owner;
   - correction: current resume routing moved to `AGENTS.md` + `BS-OPS-20260825-08` + successor canon while the old Active Context remained compatibility/history.

Promotion disposition: `PROMOTE_EXISTING_OWNER_EVIDENCE`.

Reinforced rule:

```text
1. identify every current-state consumer/regression assertion;
2. classify as CURRENT_MUTABLE or HISTORICAL_DISCOVERY;
3. advance CURRENT_MUTABLE to the verified successor;
4. preserve HISTORICAL_DISCOVERY values;
5. never re-inject predecessor tokens merely to satisfy a stale current test;
6. rerun the actual consuming workflow, not only a new standalone test.
```

## 3. Visual approval boundary lesson

Blacksmith required four independent claims:

```text
A. INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD approved
B. GAMEPLAY_VALUE_AUTHORITY from current canon
C. ART_DIRECTION approved
D. FINAL_PRODUCT_ASSET / RUNTIME / RELEASE evidence
```

Observed failure mode:
- a board can remain approved for layout/decision hierarchy while example numbers, gameplay semantics, or rendering language become stale;
- one generic `Approved=true` cannot safely prove all four meanings.

Disposition: `RECURRENCE_EVIDENCE_FOR_BCP-2026-033 / PR #679 / P05`.

Blacksmith does not duplicate #679 and does not promote its project art/gameplay values to Base.

## 4. Notion image-delivery lesson — gap detection then bounded closure

Initial fresh Blacksmith readback proved:

- all eight Asset Library records existed and were `Approved=true`;
- hashes and durable full PNG Google Drive `Source` files existed;
- `Asset row / Approved=true / Drive Source` did **not** prove a Notion-native image was present;
- representative Asset pages initially lacked direct Notion image evidence.

That initial fail-closed report was correct:

```text
ASSET_RECORD_EXISTS != NOTION_NATIVE_IMAGE_EVIDENCE
DRIVE_SOURCE_EXISTS != NOTION_NATIVE_IMAGE_EVIDENCE
APPROVED_TRUE != NOTION_NATIVE_IMAGE_EVIDENCE
```

While closing the handoff, Base main advanced through #683 and exposed a verified, bounded fallback for current connector surfaces that have text/SVG attachment upload but no direct local-binary parameter:

```text
local approved raster
-> downscale/compress preview derivative
-> embed raster data URI in UTF-8 SVG
-> Notion create-attachment(content=<svg>)
-> consume returned file-upload:// in the Asset page
-> destination fetch
-> Notion-owned prod-files-secure readback
```

Blacksmith then applied that fallback to **all eight approved Visual GDD Asset pages**:

- preview derivative: 160px wide, preview-only SVG containing compressed raster;
- original full PNG remains authoritative in each `Source` Google Drive record;
- all eight destination pages were freshly fetched after attachment and returned Notion-owned `prod-files-secure` image URLs;
- Asset metadata explicitly records `LOW_RES_DURABLE_PREVIEW_ATTACHED_160PX_SVG_RASTER_DERIVATIVE`;
- `SERVER_READBACK_PASS != HUMAN_CLIENT_VISIBLE_PASS` remains explicit.

Current disposition:

`BLACKSMITH_NOTION_LOW_RES_PREVIEW_DELIVERY = SERVER_READBACK_PASS`

This does **not** prove:
- high-resolution/pixel-equivalent Notion upload;
- that the original PNG moved out of Drive;
- actual Notion app/browser human-visible rendering;
- that SVG fallback is preferable to a typed binary upload when a stronger route exists.

This is additional verified project evidence for the preview-fallback concept now present in merged Base #683. It should not create another BCP-2026-032 while the ID collision above is unresolved.

## 5. Handoff lesson

A strong new-chat handoff is a **locator plus evidence ceiling**, not a frozen substitute for discovery.

Blacksmith `BS-OPS-20260825-08` requires the next session to fresh-read Base, default branch/latest commit/open PRs, Sheet, Notion Human/AI surfaces, and then compare conflicts before mutation. It records:

- exact current decision owners;
- explicitly superseded semantics;
- runtime implementation drift;
- open protected PR boundaries;
- unresolved next design gates;
- visual delivery/evidence state;
- NOT_RUN evidence ceilings.

Disposition: `P01_BASE_PROMOTION_CANDIDATE`, aligned with existing project-intake/context-and-handoff owners.

## 6. New Base operations lesson — proposal identity must be unique before submission

The concurrent #678/#683 observation provides a concrete operations failure mode:

```text
proposal content can be valid
AND
proposal ID can still collide with another concurrent proposal
```

Reusable guard candidate:

```text
before creating/submitting a BCP:
  fresh-read main proposal registry
  + fresh-read open PR proposal IDs
  + reserve/validate exact proposal_id
  + if duplicate => BLOCK / reconcile, never silently reuse
```

Disposition: `BASE_PROBLEM_EVIDENCE / INTEGRATION_RECONCILIATION_REQUIRED`.

This branch records the problem but does not invent a replacement proposal ID for foreign PRs.

## 7. What must NOT be promoted

Remain Blacksmith project-only:

- +9 -> +10 Precision Enhancement cadence;
- item keyword/catalyst semantics;
- four specific damage-state names;
- +11 damage opening point;
- damage probability curve;
- customer/world event damage rules;
- repair economics;
- Illustrated Workshop Book as a project art style.

## 8. Evidence boundary

This packet does not prove:

- Blacksmith player fun;
- Android/readability/accessibility quality;
- final art quality;
- high-resolution Notion visual delivery;
- human-visible Notion client rendering;
- cross-project recurrence for the handoff candidate.

Promotion beyond existing owners, changes to #678/#679/#683, or proposal-ID remediation require those owners' own review/merge lifecycle.
