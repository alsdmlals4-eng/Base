# Project IA Migration Map · 2026-08-24

Status: `PRE_MOVE_INVENTORY_COMPLETE`

This record is the rollback-safe inventory required before physical Notion reparenting for Base PR #630. No page is deleted by this migration. Every listed L3 page returns to its Human Home parent if destination readback fails.

Common rules:
- `UNIQUE_CURRENT`: current detailed owner; move intact.
- `HISTORICAL`: provenance/closure record; preserve intact and label by location rather than promote as mutable current truth.
- `home_projection`: the human-facing summary that must remain on L1 after the L3 owner moves.
- `rollback_parent`: original Human Home ID.
- Domain names are project-specific. Empty Domain pages are forbidden.
- Current COC-Fiction #48 and GRIMOIRE #151 product work is already merged; this migration changes navigation only and does not reinterpret their semantic authority.

## Tetris

Home: `3c41b237-eb1c-8199-85b3-e798e938c80b`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Combat Design · Data`
3. `03 · Visual · UX · Assets`
4. `04 · Production · Validation`
5. `05 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c11b237-eb1c-8126-b73a-db28241588d3` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/status | `3c41b237-eb1c-8199-85b3-e798e938c80b` |
| `3c21b237-eb1c-814a-b70c-c04ff6cd09e9` | 12 · Vertical Slice · Production Content Lock | Direction · Planning | UNIQUE_CURRENT | current direction/protected scope | same Home |
| `3c21b237-eb1c-81d5-9d8f-c2a6b092b7da` | 13 · Final Planning Completeness Audit | Direction · Planning | HISTORICAL | current direction only; audit remains provenance | same Home |
| `3c11b237-eb1c-8178-8f1e-fe2f9166c049` | 08 · 핵심 시스템 · 상세 | Combat Design · Data | UNIQUE_CURRENT | full flow + core data table | same Home |
| `3c21b237-eb1c-81d9-9876-f920fa47d9fa` | 07 · 세계관 · 전투 판타지 | Combat Design · Data | UNIQUE_CURRENT | setting/player role | same Home |
| `3c21b237-eb1c-81e1-b584-dcdc9c4856f1` | 09 · 대표 전투 · Gatebreaker Encounter | Combat Design · Data | UNIQUE_CURRENT | representative combat relationship | same Home |
| `3c21b237-eb1c-81c8-b3b8-e6c2a767c20d` | 11 · Vertical Slice · First Run Flow | Combat Design · Data | UNIQUE_CURRENT | full game/session flow | same Home |
| `3c11b237-eb1c-8150-8ebe-d297639a021a` | 02 · 비주얼 바이블 | Visual · UX · Assets | UNIQUE_CURRENT | visual direction/approved anchors | same Home |
| `3c11b237-eb1c-819d-bad7-d0227473fd73` | 03 · UI · 퍼즐 전투 Flow Map | Visual · UX · Assets | UNIQUE_CURRENT | UX flow summary | same Home |
| `3c11b237-eb1c-8176-9118-c4d3dd29baf4` | 04 · 에셋 라이브러리 | Visual · UX · Assets | UNIQUE_CURRENT | approved visual anchors | same Home |
| `3c21b237-eb1c-81dd-92bf-f4c651b2861a` | 10 · 오디오 바이블 | Visual · UX · Assets | UNIQUE_CURRENT | audiovisual direction | same Home |
| `3c21b237-eb1c-817f-849d-e9dc99235869` | 14 · P0 이미지 제작 패키지 | Visual · UX · Assets | UNIQUE_CURRENT | visual state only; no fabricated approval | same Home |
| `3c11b237-eb1c-8160-a1dc-cf2ba119cfab` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c11b237-eb1c-816d-95e6-da87be0108c0` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark decisions when relevant | same Home |

## COC-Fiction

Home: `3c41b237-eb1c-811d-9579-e5c8ce05daab`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Story · Canon · Events`
3. `03 · Characters · Factions · World`
4. `04 · Visual · Storyboard · Assets`
5. `05 · Production · Continuity · Validation`
6. `06 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c01b237-eb1c-81cd-8416-c60ac01865d7` | 01 · 전체 집필 · 작업계획 | Direction · Planning | UNIQUE_CURRENT | project direction/current canonization state | `3c41b237-eb1c-811d-9579-e5c8ce05daab` |
| `3c01b237-eb1c-8168-9702-cd4311689c98` | 02 · Story Bible · Canon | Story · Canon · Events | UNIQUE_CURRENT | Part/story flow + canon status | same Home |
| `3c01b237-eb1c-818f-9123-d46d927f89b9` | 04 · Character Bible · 인물 | Characters · Factions · World | UNIQUE_CURRENT | major character relationships | same Home |
| `3c01b237-eb1c-8113-9351-c9326252e01f` | 05 · Faction Map · 세력 | Characters · Factions · World | UNIQUE_CURRENT | faction/relationship overview | same Home |
| `3c01b237-eb1c-815c-a723-f0c27935ad13` | 06 · Clue · Location Library | Characters · Factions · World | UNIQUE_CURRENT | world/rule/location understanding | same Home |
| `3c01b237-eb1c-81f1-a8e5-dbbb313645df` | 03 · Storyboard · Scene Flow | Visual · Storyboard · Assets | UNIQUE_CURRENT | story flow/visual sequence | same Home |
| `3c21b237-eb1c-814f-b03d-f8b159796b51` | VISUAL · COC-Fiction Approved Anime Style · 2026-08-20 | Visual · Storyboard · Assets | UNIQUE_CURRENT | approved visual anchor | same Home |
| `3c51b237-eb1c-81eb-a2c1-fea7eb1864e9` | Visual · COC-Fiction Composition Board | Visual · Storyboard · Assets | UNIQUE_CURRENT | approved visual composition reference | same Home |
| `3c01b237-eb1c-81b7-b7aa-d98517dd5c14` | 08 · Continuity · Publication Handoff | Production · Continuity · Validation | UNIQUE_CURRENT | continuity/publication state | same Home |
| `3c01b237-eb1c-81eb-a7c1-e65f2a6fecca` | 07 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark/source context | same Home |

## 괴이기록국

Home: `3c41b237-eb1c-81dc-9bda-d72bf2d5978d`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Investigation · Cases · Narrative`
3. `03 · Systems · Flow · Data`
4. `04 · Visual · UX · Assets`
5. `05 · Production · Validation`
6. `06 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c01b237-eb1c-8164-a2e7-ce98278d06fb` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/state | `3c41b237-eb1c-81dc-9bda-d72bf2d5978d` |
| `3c11b237-eb1c-817e-b9f1-eca14243557c` | 07 · 월간 사건 · 서사 결정 기록 | Investigation · Cases · Narrative | UNIQUE_CURRENT | case/story cadence | same Home |
| `3c11b237-eb1c-816d-af1c-d88db749c90e` | 10 · Content Budget · 월간 사건 제작 범위 | Investigation · Cases · Narrative | UNIQUE_CURRENT | monthly content scope | same Home |
| `3c01b237-eb1c-8152-a74a-d28af9d39c77` | 03 · UI · 조사 Flow Map | Systems · Flow · Data | UNIQUE_CURRENT | full investigation flow | same Home |
| `3c11b237-eb1c-81bf-8390-e5fcd22eb716` | 08 · 핵심 시스템 · 상세 | Systems · Flow · Data | UNIQUE_CURRENT | core systems/data table | same Home |
| `3c11b237-eb1c-81c2-91d8-d45d2747451b` | 09 · Vertical Slice · 플레이 검증 계약 | Systems · Flow · Data | UNIQUE_CURRENT | representative slice/validation boundary | same Home |
| `3c11b237-eb1c-81c8-9490-c01a3534818b` | 11 · First Session · 온보딩 경험 계약 | Systems · Flow · Data | UNIQUE_CURRENT | first-session flow | same Home |
| `3c01b237-eb1c-8161-81c0-cc81bb3d3b3d` | 02 · 비주얼 바이블 | Visual · UX · Assets | UNIQUE_CURRENT | visual direction | same Home |
| `3c01b237-eb1c-81e6-8b50-e4153401f160` | 04 · 에셋 라이브러리 | Visual · UX · Assets | UNIQUE_CURRENT | approved asset anchors | same Home |
| `3c01b237-eb1c-81c0-b70f-fe96425a0e66` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c21b237-eb1c-8174-892f-d10a0948a61c` | Planning Closure Gap Matrix · 2026-08-20 | Production · Validation | HISTORICAL | current state summary only | same Home |
| `3c21b237-eb1c-81ed-854b-e8e175d3618c` | Final Whole-Plan Adversarial Review · 5 Loops | Production · Validation | HISTORICAL | validation ceiling only | same Home |
| `3c01b237-eb1c-8150-858f-f9e7b2516d90` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark decisions when relevant | same Home |

## 오멘워드

Home: `3c41b237-eb1c-816f-bbc8-e2dddc18b6eb`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Forecast · War Systems · Balance`
3. `03 · Stage · World · Content`
4. `04 · Visual · UX · Components`
5. `05 · Production · Validation`
6. `06 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c01b237-eb1c-8119-9eff-d7dd6159ec16` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/status | `3c41b237-eb1c-816f-bbc8-e2dddc18b6eb` |
| `3c01b237-eb1c-8169-ba2f-ec6e9fb1c552` | 07 · 확정 기획 · 병종·건물 Tier 표 | Forecast · War Systems · Balance | UNIQUE_CURRENT | project-specific core data | same Home |
| `3c11b237-eb1c-8127-96ee-c943a4195e27` | 08 · 핵심 시스템 · 상세 | Forecast · War Systems · Balance | UNIQUE_CURRENT | core systems + 3×3 wheel/forecast | same Home |
| `3c21b237-eb1c-8161-96a7-f346dfbcbf49` | 11 · Balance Budget | Forecast · War Systems · Balance | UNIQUE_CURRENT | balance relationships | same Home |
| `3c21b237-eb1c-81e2-9d20-ea6b2a63ca56` | 09 · 세계관 · 핵심 스토리 | Stage · World · Content | UNIQUE_CURRENT | setting/core conflict | same Home |
| `3c21b237-eb1c-81a4-81f0-c5563a45bf5e` | 10 · 20 Stage · Boss 구조 | Stage · World · Content | UNIQUE_CURRENT | full 20-stage progression | same Home |
| `3c01b237-eb1c-81c3-8be5-e3ee9f64b59d` | 02 · 비주얼 바이블 | Visual · UX · Components | UNIQUE_CURRENT | visual direction | same Home |
| `3c01b237-eb1c-812b-935f-caefb3290f61` | 03 · UI · 게임플레이 Flow Map | Visual · UX · Components | UNIQUE_CURRENT | UX/full stage flow | same Home |
| `3c01b237-eb1c-818c-a227-ee34eefd4534` | 04 · 에셋 라이브러리 | Visual · UX · Components | UNIQUE_CURRENT | approved asset anchors | same Home |
| `3c21b237-eb1c-81fb-947f-d5647c9295e1` | 12 · Text UX · 상태전이 | Visual · UX · Components | UNIQUE_CURRENT | information/state readability | same Home |
| `3c21b237-eb1c-81e2-9be2-d6ce397c9c85` | 13 · 비주얼 컴포넌트 · 전장/룰렛/UI | Visual · UX · Components | UNIQUE_CURRENT | component hierarchy | same Home |
| `3c21b237-eb1c-81f5-817d-f253b5eb76e8` | 14 · 전장 스케일 · 전투 가독성 | Visual · UX · Components | UNIQUE_CURRENT | battlefield readability | same Home |
| `3c21b237-eb1c-81a9-ae59-ef43a8e61067` | 15 · 3×3 룰렛 · 조작 컴포넌트 | Visual · UX · Components | UNIQUE_CURRENT | wheel interaction | same Home |
| `3c21b237-eb1c-81de-bbfc-e9ec2dc5d868` | 16 · 룰렛 Token · 병종/Gold/X | Visual · UX · Components | UNIQUE_CURRENT | token semantics | same Home |
| `3c21b237-eb1c-819a-bb42-ea9969198e87` | 17 · 하단 Control Deck · Focus UI | Visual · UX · Components | UNIQUE_CURRENT | control focus hierarchy | same Home |
| `3c01b237-eb1c-810d-b6f9-c5c9046c5e6b` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c01b237-eb1c-812b-b2ab-ceb7bfb712a4` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark decisions when relevant | same Home |

## GRIMOIRE

Home: `3c41b237-eb1c-816c-80d0-dfcfe28ec973`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Magic Systems · Learning`
3. `03 · Visual · UX · Components`
4. `04 · Production · Validation`
5. `05 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c01b237-eb1c-81eb-a86a-cce0eae11b85` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/status | `3c41b237-eb1c-816c-80d0-dfcfe28ec973` |
| `3c11b237-eb1c-8131-bf82-d60126013791` | 08 · 핵심 시스템 · 상세 | Magic Systems · Learning | UNIQUE_CURRENT | magic grammar/core data | same Home |
| `3c01b237-eb1c-819f-959c-debbed69405b` | 02 · 비주얼 바이블 | Visual · UX · Components | UNIQUE_CURRENT | visual direction | same Home |
| `3c01b237-eb1c-8155-b2a0-fd2cdf544613` | 03 · UI · 세계 재작성 Flow Map | Visual · UX · Components | UNIQUE_CURRENT | learning/spell flow | same Home |
| `3c01b237-eb1c-81c7-8acd-d5c199169bf0` | 04 · 에셋 라이브러리 | Visual · UX · Components | UNIQUE_CURRENT | approved asset anchors | same Home |
| `3c01b237-eb1c-81e2-952d-fba2bc650e27` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c01b237-eb1c-81c2-bc67-e40ec0e84182` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark/source context | same Home |

## 닌자 서바이벌

Home: `3c41b237-eb1c-81aa-a4e0-e208ba4fb15e`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Combat · Schools · Backpack`
3. `03 · World · Story · Content`
4. `04 · Visual · UX · Assets`
5. `05 · Production · Validation`
6. `06 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c01b237-eb1c-81d8-9e3a-cd5fcc605ec5` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/status | `3c41b237-eb1c-81aa-a4e0-e208ba4fb15e` |
| `3c11b237-eb1c-8152-8974-cfbd10c889c0` | 08 · 핵심 시스템 · 상세 | Combat · Schools · Backpack | UNIQUE_CURRENT | 4 schools + 6×6 backpack/core data | same Home |
| `3c11b237-eb1c-8142-acf0-db0a7fe0a463` | 09 · 세계관 · 핵심 스토리 | World · Story · Content | UNIQUE_CURRENT | setting/player role/core conflict | same Home |
| `3c01b237-eb1c-8116-9028-c8c8c427e467` | 02 · 비주얼 바이블 | Visual · UX · Assets | UNIQUE_CURRENT | visual direction | same Home |
| `3c01b237-eb1c-81a2-b859-c8155c90ca75` | 03 · UI · 생존 Flow Map | Visual · UX · Assets | UNIQUE_CURRENT | survival/run flow | same Home |
| `3c01b237-eb1c-81e6-9d5b-c467b5ad2b1e` | 04 · 에셋 라이브러리 | Visual · UX · Assets | UNIQUE_CURRENT | approved asset anchors | same Home |
| `3c01b237-eb1c-81b4-a3f5-ec575f3c77b5` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c01b237-eb1c-81c7-99f5-caf371107acb` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark/source context | same Home |

## 블랙스미스

Home: `3c41b237-eb1c-813f-a481-e415e3250d1c`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Enhancement · Durability · Economy`
3. `03 · Visual · UX · Assets`
4. `04 · Production · Validation`
5. `05 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c01b237-eb1c-8125-8e44-ed79bc638813` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/status | `3c41b237-eb1c-813f-a481-e415e3250d1c` |
| `3c01b237-eb1c-81a4-af26-c3057bfdcbbf` | 03 · UI · 제작 · 경제 Flow Map | Enhancement · Durability · Economy | UNIQUE_CURRENT | full item-life/economy flow | same Home |
| `3c11b237-eb1c-8143-baef-ecf4e697a258` | 08 · 핵심 시스템 · 상세 | Enhancement · Durability · Economy | UNIQUE_CURRENT | enhancement/durability/core data | same Home |
| `3c01b237-eb1c-8147-abdf-fab51a8f9ad3` | 02 · 비주얼 바이블 | Visual · UX · Assets | UNIQUE_CURRENT | visual direction | same Home |
| `3c01b237-eb1c-817a-b257-cf6e2d299896` | 04 · 에셋 라이브러리 | Visual · UX · Assets | UNIQUE_CURRENT | approved asset anchors | same Home |
| `3c01b237-eb1c-8178-82e7-dd74ee265309` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c01b237-eb1c-8104-90ad-faeb197996da` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark/source context | same Home |

## 십보강호

Home: `3c41b237-eb1c-8105-a254-d860f3c21638`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Combat · Martial Arts · Route`
3. `03 · Visual · UX · Assets`
4. `04 · Opponents · World · Content`
5. `05 · Production · Validation`
6. `06 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c01b237-eb1c-812a-b2c4-d02959faf046` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/status | `3c41b237-eb1c-8105-a254-d860f3c21638` |
| `3c01b237-eb1c-8106-9e38-e1d182393f0f` | 03 · UI · 전투 Flow Map | Combat · Martial Arts · Route | UNIQUE_CURRENT | full duel/run flow | same Home |
| `3c01b237-eb1c-8106-b80c-e91071dc4b24` | 07 · 확정 기획 · 무공·기술 예산표 | Combat · Martial Arts · Route | UNIQUE_CURRENT | martial-technique core data | same Home |
| `3c11b237-eb1c-8138-b1b3-fbcfb3e242b3` | 08 · 핵심 시스템 · 상세 | Combat · Martial Arts · Route | UNIQUE_CURRENT | 10-grid/3·3·4/core system relations | same Home |
| `3c21b237-eb1c-81e0-a4a2-c892a0d3deba` | 11 · 상대 무공 배정 · Route 예산 · 비전투 Wire | Combat · Martial Arts · Route | UNIQUE_CURRENT | route/martial allocation | same Home |
| `3c01b237-eb1c-814f-80d4-c6140fddebd4` | 02 · 비주얼 바이블 | Visual · UX · Assets | UNIQUE_CURRENT | visual direction | same Home |
| `3c01b237-eb1c-8172-a16d-c7713b75fcc5` | 04 · 에셋 라이브러리 | Visual · UX · Assets | UNIQUE_CURRENT | approved asset anchors | same Home |
| `3c11b237-eb1c-81d2-8aa3-c6890b25d587` | 09 · 세계관 · 강호 비무행 · Vertical Slice | Opponents · World · Content | UNIQUE_CURRENT | setting/journey structure | same Home |
| `3c21b237-eb1c-8188-b925-e9d88ca13e20` | 10 · 상대 15명 · 강호행로 8노드 · 텍스트 UX | Opponents · World · Content | UNIQUE_CURRENT | opponent/route content relationships | same Home |
| `3c01b237-eb1c-8118-9114-ed9bbfcbb438` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c21b237-eb1c-8123-b7a6-d97a43833a0d` | 12 · Vertical Slice · 기획 완료 기준선 | Production · Validation | HISTORICAL | current completion baseline summary only | same Home |
| `3c21b237-eb1c-812a-8c5a-eabed05036e5` | 13 · 기획 완료 · Visual/구현 Handoff | Production · Validation | UNIQUE_CURRENT | implementation/visual handoff state | same Home |
| `3c01b237-eb1c-815c-8d43-f7200be868ea` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark/source context | same Home |

## Switchy Express

Home: `3c41b237-eb1c-8103-9537-ede6dfc5f07e`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Puzzle Systems · First Session`
3. `03 · Visual · UX · Assets`
4. `04 · Production · Validation`
5. `05 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c01b237-eb1c-81b3-aad5-c16ae8368015` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/status | `3c41b237-eb1c-8103-9537-ede6dfc5f07e` |
| `3c01b237-eb1c-81a0-8bae-dee2470e0576` | 03 · UI · 퍼즐 Flow Map | Puzzle Systems · First Session | UNIQUE_CURRENT | full delivery puzzle flow | same Home |
| `3c11b237-eb1c-819a-be15-e130a4092cc4` | 07 · SX-DEC-059 · First-Session Vertical Slice | Puzzle Systems · First Session | UNIQUE_CURRENT | first-session learning | same Home |
| `3c11b237-eb1c-81eb-8554-fbbd3df71958` | 08 · 핵심 시스템 · 상세 | Puzzle Systems · First Session | UNIQUE_CURRENT | LIFO/switch/core data | same Home |
| `3c01b237-eb1c-81b2-8149-fb2ced504495` | 02 · 비주얼 바이블 | Visual · UX · Assets | UNIQUE_CURRENT | visual direction | same Home |
| `3c01b237-eb1c-8104-a97c-e84a637441ad` | 04 · 에셋 라이브러리 | Visual · UX · Assets | UNIQUE_CURRENT | approved asset anchors | same Home |
| `3c01b237-eb1c-81e4-ba8b-e09aafe06738` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c01b237-eb1c-810e-81f6-fb73003e3e2b` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark/source context | same Home |

## 마이 리틀 보트

Home: `3c41b237-eb1c-8194-8b8e-d88362cafafa`

Target L2 Domains:
1. `01 · Direction · Planning`
2. `02 · Voyage · Experience · Systems`
3. `03 · Visual · UX · Assets`
4. `04 · Production · Validation`
5. `05 · Reference · Benchmark`

| page_id | title | target L2 | class | home_projection | rollback_parent |
|---|---|---|---|---|---|
| `3c11b237-eb1c-810c-80dd-e57ab44c9b23` | 01 · 프로젝트 전체 작업계획 | Direction · Planning | UNIQUE_CURRENT | current direction/status | `3c41b237-eb1c-8194-8b8e-d88362cafafa` |
| `3c11b237-eb1c-81c3-8e12-d3f598113c7e` | 03 · UI · 항해 Flow Map | Voyage · Experience · Systems | UNIQUE_CURRENT | full voyage flow | same Home |
| `3c11b237-eb1c-8119-8378-c25d3ebbf658` | 08 · 핵심 시스템 · 상세 | Voyage · Experience · Systems | UNIQUE_CURRENT | voyage/discovery/core data | same Home |
| `3c11b237-eb1c-81ae-97f3-dc28a0905304` | 02 · 비주얼 바이블 | Visual · UX · Assets | UNIQUE_CURRENT | visual direction | same Home |
| `3c11b237-eb1c-8120-b7db-d48e11756146` | 04 · 에셋 라이브러리 | Visual · UX · Assets | UNIQUE_CURRENT | approved asset anchors | same Home |
| `3c11b237-eb1c-81b0-b281-ec54d67c9552` | 06 · Production · Handoff | Production · Validation | UNIQUE_CURRENT | implementation/evidence ceiling | same Home |
| `3c11b237-eb1c-8116-9c53-e3662be2e347` | 05 · Reference · Benchmark 도서관 | Reference · Benchmark | UNIQUE_CURRENT | benchmark/source context | same Home |

## Move protocol

For every row:
1. fresh-fetch the page and its recorded Human Home immediately before the move;
2. fresh-fetch the target L2 Domain;
3. move exactly that page to the Domain;
4. fetch the moved page and verify its ancestor path points to the target Domain;
5. verify content and important mentions still exist;
6. if readback fails, move the page back to `rollback_parent` and mark `ROLLBACK_REQUIRED`.

No page deletion, no branch-only semantic promotion, no gameplay/runtime mutation, and no `UI_GEOMETRY_VERIFIED` claim are authorized by this map.
