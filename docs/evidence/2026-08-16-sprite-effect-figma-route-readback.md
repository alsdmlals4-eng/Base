# Sprite / Effect Figma Route Readback Evidence

- Approved plan provenance: PR #451 (read-only draft)
- Integration base: `faff4bfdf6d5cd07d79e8352d1a3f6cd8d957906`
- Figma write/readback date: 2026-08-17 (Asia/Seoul)
- Figma authenticated user: 민곤 (`mingong994@gmail.com`), Professional plan, Full seat
- `LOCALHOST_BRIDGE_RECEIPT`: `NOT_RUN`
- `USER_PC_TOOL_HUB_IRG`: `NOT_RUN`

| project_id | figma_file_key | parent | marker | expression | sprite_action_runs | effect_runs | result |
|---|---|---:|---:|---:|---:|---:|---|
| coc-fiction | `PEa5zDbPHll3eHiNKX0e1k` | `12:3` | `23:2` | `15:2` | `25:2` | `25:5` | PASS |
| ten-paces-hidden-moves | `pVQ2e6aK45iL8BLBJWDSw4` | `22:3` | `38:2` | `28:2` | `40:2` | `40:5` | PASS |
| ninja-survival | `xNm1xbYPftEaAE2jOENlvt` | `12:3` | `20:2` | `15:2` | `22:2` | `22:5` | PASS |
| switchy-express-cargo-puzzle | `QMbylbdAi96PGSdHIT3AGa` | `11:3` | `19:2` | `14:2` | `21:2` | `21:5` | PASS |
| urban-legend | `Z7J3eLeavEytKN20H4HfoP` | `11:3` | `19:2` | `14:2` | `39:2` | `39:5` | PASS |
| grimoire-how-to-rewrite-the-world | `AdOGNMp61AZSMMvBVxsVBd` | `8:3` | `16:2` | `11:2` | `18:2` | `18:5` | PASS |
| blacksmith | `xy6W4ga6ldkF3TvP0eRmtN` | `13:3` | `24:2` | `18:2` | `26:2` | `26:5` | PASS |
| omenward | `IhxUJaS6ik6MpBzdxt6o8D` | `10:3` | `19:2` | `13:2` | `21:2` | `21:5` | PASS |

## Readback contract

For every file, the existing `Generated Assets` parent, existing `Expression Runs` node, and existing hidden `Base Tool Hub Route · <project_id>` marker were checked before mutation. `Sprite Action Runs` and `Effect Runs` were created retry-safely from the existing Expression frame, then read back.

Required geometry and identity were verified for all 16 new frames:

- `Sprite Action Runs`: `FRAME`, exact parent, `x=40`, `y=408`, `1360×148`
- `Effect Runs`: `FRAME`, exact parent, `x=40`, `y=576`, `1360×148`
- exactly one canonical sibling of each destination name per project
- existing Expression node and hidden project marker preserved

No generic `Generated Assets` fallback and no `Expression Runs` fallback is authorized for Sprite/Effect delivery.
