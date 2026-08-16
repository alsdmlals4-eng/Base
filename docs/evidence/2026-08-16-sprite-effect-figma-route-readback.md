# Sprite / Effect Figma Route Readback Evidence

- Base preflight SHA: `ab3afa4aab1d5f56958dc53a4ba1649ee70b1d8d`
- Implementation branch: `feat/sprite-effect-figma-routes-20260816`
- User-approved design source: PR #451 (read-only)
- Figma mutation/readback date: 2026-08-16
- `LOCALHOST_BRIDGE_RECEIPT: NOT_RUN`
- `USER_PC_TOOL_HUB_IRG: NOT_RUN`

All rows were preflighted against the exact existing `Generated Assets` parent, `Expression Runs` node, and hidden `Base Tool Hub Route · <project_id>` marker. Each route frame was created or safely reused through the Figma Plugin API, then read back with exact parent/name/type/geometry and sibling uniqueness checks.

| project_id | file_key | parent | marker | Sprite Action Runs | Effect Runs | result |
|---|---|---:|---:|---:|---:|---|
| coc-fiction | `PEa5zDbPHll3eHiNKX0e1k` | `12:3` | `23:2` | `25:2` | `25:5` | PASS |
| ten-paces-hidden-moves | `pVQ2e6aK45iL8BLBJWDSw4` | `22:3` | `38:2` | `40:2` | `40:5` | PASS |
| ninja-survival | `xNm1xbYPftEaAE2jOENlvt` | `12:3` | `20:2` | `22:2` | `22:5` | PASS |
| switchy-express-cargo-puzzle | `QMbylbdAi96PGSdHIT3AGa` | `11:3` | `19:2` | `21:2` | `21:5` | PASS |
| urban-legend | `Z7J3eLeavEytKN20H4HfoP` | `11:3` | `19:2` | `39:2` | `39:5` | PASS |
| grimoire-how-to-rewrite-the-world | `AdOGNMp61AZSMMvBVxsVBd` | `8:3` | `16:2` | `18:2` | `18:5` | PASS |
| blacksmith | `xy6W4ga6ldkF3TvP0eRmtN` | `13:3` | `24:2` | `26:2` | `26:5` | PASS |
| omenward | `IhxUJaS6ik6MpBzdxt6o8D` | `10:3` | `19:2` | `21:2` | `21:5` | PASS |

## Geometry contract

- `Sprite Action Runs`: `x=40`, `y=408`, `w=1360`, `h=148`
- `Effect Runs`: `x=40`, `y=576`, `w=1360`, `h=148`
- one canonical sibling of each name per project
- existing `Expression Runs` and hidden route marker preserved

## Evidence ceiling

This evidence proves live Figma account access and actual Plugin API write/readback for the 16 route nodes. It does not prove the user's Windows PC Tool Hub process, localhost bridge delivery receipt, real Sprite/Effect generation quality, or Godot consumption.
