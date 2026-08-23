# Project IA Migration Readback · 2026-08-24

Status: `PHYSICAL_MOVE_COMPLETE_READBACK_VERIFIED`

This receipt closes the physical Notion migration phase defined by `2026-08-24_PROJECT_IA_MIGRATION_MAP.md`. The migration map remains the pre-move inventory and rollback contract; this file records what was observed after the move.

## Verified architecture

All ten active Human Project Homes expose project-specific L2 Domain navigation while retaining human-readable core understanding on L1:

`Project Hub → rich Human Home → 4~6 project-specific L2 Domains → L3 Detail/Record`

Verified Human Homes:
- COC-Fiction
- 괴이기록국
- 오멘워드
- GRIMOIRE
- 닌자 서바이벌
- 블랙스미스
- 십보강호
- Tetris
- Switchy Express
- 마이 리틀 보트

The L2 Domains do not replace Home understanding. Home still carries project identity, full game/story/session flow, core systems and setting where applicable, project-specific representative data, Visual/UX state, AI interpretation for user correction, human edit guidance, current implementation/validation state, blockers/next work, and evidence ceilings.

## Physical owner readback

Representative deep readback verified the physical hierarchy, not only Home links:
- Tetris `08 · 핵심 시스템 · 상세` is under `02 · Combat Design · Data → Tetris · Home`.
- GRIMOIRE planning/core/visual/flow/assets/production/reference owners are under the canonical Direction, Magic Systems, Visual, Production, and Reference Domains.
- 마이 리틀 보트 planning/flow/core/visual/assets/production/reference owners are under the canonical Direction, Voyage, Visual, Production, and Reference Domains.

No L3 source page was copied into a second mutable canon for the migration; existing owners were reparented intact.

## Concurrent-migration duplicate handling

During final GRIMOIRE / 마이 리틀 보트 migration, concurrent work created a second set of L2 structural pages. Fresh ancestor readback showed the earlier set was already receiving the real L3 owners.

Resolution:
- canonical set = the set linked from each Human Home and owning the moved L3 pages;
- later duplicate structural pages were not deleted;
- duplicates were renamed/marked as retired receipts and moved outside Human Homes under `90 · SYSTEM MASTERS / PR630 · Migration Duplicate Quarantine · 2026-08-24`;
- quarantined pages are not current authority and own no production L3 canon.

This preserves evidence and avoids both deletion and duplicate Human navigation.

## Post-move stale-current corrections

### Tetris timing owner

The whole-result review found one valid `STALE_CURRENT` conflict inside Tetris `08 · 핵심 시스템 · 상세`: the page's latest `TETRIS-TIME-025` owner already required one Shared Player Turn Budget with READY carryover, while a lower `Turn Phase Controller` paragraph still called independent Line/Chain/Action timers with no carryover the current production rule.

Correction/readback:
- preserved `Enemy Telegraph → Line → Line Settle → Chain → Chain Settle → Action → Player Action → Enemy Resolve`;
- replaced independent per-phase timer wording with the single Shared Player Turn Budget;
- restored Line/Chain READY carryover and non-consuming Settle/forced-animation/System-Pause semantics;
- labeled the old `30s / 30s / 30s · no carryover` model as superseded, not current production timing;
- fetched the moved L3 page again under `02 · Combat Design · Data → Tetris · Home` and confirmed the corrected current wording.

### Project Hub navigation explanation

The physical Hub → Home links were already correct, but the Project Hub introduction still described the old flat collection of planning/visual/flow/asset/reference/production pages instead of teaching the new shallow hierarchy.

Correction/readback:
- kept each Project Home as the first-click destination;
- changed the Human Hub explanation to `Home에서 전체 Flow·핵심 시스템/설정·핵심 데이터 표 확인 → 4~6 Project Domain → Detail/Record`;
- stated that normal navigation should not deepen beyond that structure;
- fetched the Hub again and confirmed all ten Project Home child links remained intact.

These findings reset the post-change clean-review count to `0/5`; only reviews after both corrections may count toward final clean exit.

## Authority and evidence ceiling

Verified:
- rich Human Home remains physically separate from Project Registry/System records;
- raw operational metadata is not promoted into the Human Home default surface;
- all ten Homes expose project-specific L2 navigation;
- representative and final-gap L3 ancestor paths were read back after reparenting;
- no page deletion was used for migration cleanup;
- no runtime/gameplay mutation, image generation, or paid Notion capability was introduced by this migration.

Not promoted by this receipt:
- `UI_GEOMETRY_VERIFIED` — NOT_RUN;
- Human usability/readability study of the new IA — NOT_RUN;
- device-specific Notion rendering — NOT_RUN;
- project runtime/Human/device evidence — unchanged by this information-architecture migration.

If a future readback finds a moved L3 under the wrong Domain, use the original Human Home in the migration map as the rollback parent and re-run destination readback before claiming the migration is current.