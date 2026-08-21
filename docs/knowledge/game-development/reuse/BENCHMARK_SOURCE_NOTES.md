# Reusable Module Benchmark Source Notes

- 확인일: 2026-08-22
- 역할: `REUSABLE_MODULE_REGISTRY.md`의 외부 benchmark provenance 보조 자료
- 권위: 외부 사례는 Base/project 요구사항 정본이 아니다.

## Evidence boundary

이 문서는 “어떤 작품이 유명하므로 따라 한다”는 근거가 아니다. 각 Source에서 **반복되는 문제 해결 원리**만 추출하고, 현재 프로젝트 정본·권리·비용·실제 검증보다 우선하지 않는다.

```text
external source
→ observed contract
→ ADOPT | ADAPT | TEST | REJECT | DIRECT_LICENSED_REUSE_CANDIDATE
→ project fit
→ project evidence
```

## Godot 4.7 · reusable scene/data composition

Primary:
- https://docs.godotengine.org/en/4.7/tutorials/scripting/resources.html
- https://docs.godotengine.org/en/4.7/tutorials/best_practices/what_are_godot_classes.html
- https://docs.godotengine.org/en/4.7/getting_started/step_by_step/nodes_and_scenes.html

Observed:
- `Resource`는 data container로 사용 가능.
- Godot은 scripts와 scenes를 주요 reusable object 방식으로 설명.
- `PackedScene`은 scene을 resource로 저장/instance할 수 있음.

Disposition: `ADOPT` as implementation option for small data + rule + project adapter modules. 거대 global manager를 요구하는 근거로 사용하지 않는다.

## ink · branching narrative runtime

Primary:
- https://github.com/inkle/ink
- https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md
- https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md

Observed:
- 선택, 분기, gather/rejoin, runtime state를 content 흐름과 연결.
- runtime이 current choices와 story state를 노출.
- MIT license.

Disposition: `ADAPT` for `RM-NAR-001` / `RM-SYS-005`; ink 자체를 Base 표준 narrative language로 강제하지 않는다.

## Yarn Spinner · runner / presentation / state separation

Primary:
- https://docs.yarnspinner.dev/yarn-spinner-for-other-engines/godot/components/dialogue-runner
- https://docs.yarnspinner.dev/yarn-spinner-for-other-engines/godot/components/dialogue-presenters/custom-dialogue-presenters

Observed:
- Dialogue Runner가 lines/options/commands를 게임에 전달.
- presentation과 variable storage를 별도 component로 둘 수 있음.
- project-specific presenter를 작성할 수 있음.

Disposition: `ADAPT` for narrative flow/presentation boundary; dependency adoption은 project별 Existing Solution First에서 별도 판정.

## 서울 2033 · choice-driven event consequences

Current public/developer surfaces:
- https://banjihagames.com/
- https://play.google.com/store/apps/details?id=com.banjihagames.seoul2033
- https://apps.apple.com/kr/app/%EC%84%9C%EC%9A%B8-2033/id1439604101

Verified from current developer-supplied store description:
- 폐허가 된 서울을 탐험하는 선택 중심 어드벤처로 소개된다.
- 한 순간의 선택과 판단이 플레이어와 서울의 운명을 바꿀 수 있다고 명시한다.
- 350개 이상의 story가 있다고 설명한다.

Not established by these public descriptions alone:
- 내부 능력/아이템/돈/건강의 exact state schema.
- 특정 event trigger formula나 수치.
- 반복 플레이의 exact unlock/branch algorithm.

Disposition: `ADAPT` for `RM-SYS-005`, `RM-SYS-006`, `RM-NAR-001`의 **선택→상태/후속 귀결** 설계 가설만 사용한다. exact 내부 규칙이 필요하면 실제 플레이/추가 1차 근거를 별도 수집하며, 사건 문구·세계관·고유 조건/수치를 복제하지 않는다.

## Slay the Spire · composable action/build units + iterative balance

Primary / developer:
- https://www.megacrit.com/press-kits/slay-the-spire/
- https://www.gdcvault.com/play/1025731/-Slay-the-Spire-Metrics

Observed:
- Mega Crit는 card game + roguelike 결합, unique deck/cards/relics 구조를 공식 설명.
- GDC 세션은 early development부터 metrics/data-driven balance와 community feedback을 사용했다고 설명.

Disposition:
- `ADAPT` for `RM-SYS-011 CARD_ACTION_EFFECT_ENGINE`.
- `ADAPT` for `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR`의 data/evidence mindset.
- 카드 UI·고유 카드·유물·수치·맵 구조를 복제하지 않는다.

## DevBawky LOADED · resolution/RNG/lifecycle pattern extraction

Primary / developer repository:
- https://github.com/DevBawky/LOADED
- https://github.com/DevBawky/LOADED/blob/main/README.md
- https://github.com/DevBawky/LOADED/blob/main/Docs/BulletDeckLifecycle.md
- https://github.com/DevBawky/LOADED/blob/main/.agents/skills/loaded-edit-bullet-deck/SKILL.md

Observed:
- 공개 저장소 README는 심사 목적으로만 공개됐고 코드·에셋의 복제, 수정, 재배포, 상업적 이용 및 다른 프로젝트 사용을 금지한다고 명시한다.
- 탄환 instance는 authoritative container 중 하나에만 존재하고 `nextCycleOrder`는 실제 owner가 아닌 preview/reservation 정보로 분리한다.
- 미래 파괴 결과를 preview하기 위해 RNG를 미리 소비하지 않는다고 설계 문서와 project Skill 양쪽에서 명시한다.
- 마지막 자원 소진과 마지막 적 제거처럼 충돌할 수 있는 결과는 개별 effect 중간이 아니라 firing/effect sequence 종료 뒤 우선순위에 따라 확정한다.
- UI도 firing 도중 transient update를 연속 publish하지 않고 settled result 뒤 갱신하도록 계약한다.

Disposition:
- LOADED 코드·에셋·고유 수치·UI 표현의 direct reuse는 `REJECT`.
- 관찰 가능한 원리는 `PATTERN_EXTRACT`로만 사용해 `RM-TOOL-002`의 preview/RNG causal boundary와 `ATOMIC_RESOLUTION_BOUNDARY`를 보강한다.
- zone/container ownership 구조는 현재 이 Source만으로 Base 보편 법칙으로 승격하지 않고 `SINGLE_SOURCE_HYPOTHESIS`로 유지한다. 다른 materially distinct 구현과 프로젝트 소비가 확인되기 전 별도 `RM-SYS-*`를 만들지 않는다.

## DevBawky Kalivra · explainable balance analysis and simulation

Primary / developer repository:
- https://github.com/DevBawky/Kalivra
- https://github.com/DevBawky/Kalivra/blob/main/README.md
- https://github.com/DevBawky/Kalivra/blob/main/LICENSE.md

Observed:
- README는 Monte Carlo 반복 실행, damage/TTK 분포, 승률 신뢰 구간, outlier/long-tail, explainable battle log, preset diff, formula preset, imbalance watchdog, goal-seeking adjustment를 목표 기능으로 설명한다.
- 이러한 기능은 `RM-TOOL-003`이 이미 가진 snapshot/scenario/distribution/dominant-choice/baseline-candidate 계약과 높은 중복을 보인다.
- README badge/설명은 MIT라고 표현하지만 실제 `LICENSE.md`에는 attribution과 함께 **소프트웨어 자체 또는 수정본의 유료 판매·임대 금지** 조건이 추가되어 있다. 따라서 `MIT` 표기만 보고 표준 MIT dependency로 취급하면 안 된다.
- `main.js`의 Electron 설정은 `nodeIntegration: true`, `contextIsolation: false`이므로 Base의 기존 project-isolated Tool Hub에 그대로 drop-in하는 것을 기본 경로로 삼지 않는다.

Disposition:
- 기능/UX 원리는 `ADAPT` for `RM-TOOL-003`.
- `DIRECT_LICENSED_REUSE_CANDIDATE`는 실제 source import가 필요할 때만 별도 rights/security review 후 판단한다. 현재는 `RIGHTS_REVIEW_REQUIRED · LICENSE_METADATA_CONFLICT`.
- Base 기본 경로는 **read-only project snapshot + deterministic runner + machine-readable report → 반복 가치 검증 후 Tool Hub thin surface**다.
- external Electron app 직접 탑재와 독립 거대 Balance GUI 신규 구축은 기본값에서 제외한다.
- output을 상업 게임 설계에 사용하는 것과 소프트웨어 코드를 Base에 편입·재배포하는 것은 별도 권리 질문으로 분리한다.

## Vampire Survivors · auto-action pressure + bounded growth choices

Primary/developer source:
- https://poncle.games/adventures-faq

Public store developer-supplied description may be used as supporting product observation.

Observed:
- run 중 weapon 획득/장착과 이후 level-up choice pool의 연결.
- run progression과 Adventure-specific unlock/state 경계.

Disposition: `ADAPT` for `RM-SYS-012 SURVIVOR_AUTO_COMBAT_PROGRESSION_CORE`; Ninja Survival의 REST/backpack/style 구조를 대체하지 않는다.

## Backpack Battles · spatial inventory as strategic input

Developer-supplied product page:
- https://store.steampowered.com/app/2427700/Backpack_Battles/

Observed:
- inventory-management auto battler로 소개.
- 아이템을 구매/제작한 뒤 backpack에 **배치하는 것 자체**가 전략 입력임.

Disposition: `ADAPT` for `RM-SYS-001 GRID_PLACEMENT_RULE_ENGINE`의 inventory adapter evidence. Backpack Battles의 item/art/UI/crafting을 복제하지 않는다.

## Kenney · direct licensed prototype material

Primary:
- https://kenney.nl/assets/ui-pack-rpg-expansion
- https://www.kenney.nl/assets/ui-pack-adventure
- https://www.kenney.nl/assets/pixel-ui-pack
- https://www.kenney.nl/assets/ui-audio

Observed:
- 해당 asset pages는 Creative Commons CC0 license를 명시.

Disposition: `DIRECT_LICENSED_REUSE_CANDIDATE` for prototype/UI/icon/audio material. 실제 다운로드 시점의 license/source/hash와 프로젝트 시각 적합성을 다시 기록한다. Kenney branding/logo는 재사용 자산으로 간주하지 않는다.

## Tetris · abstract spatial/line-completion observation with rights boundary

Primary:
- https://tetris.com/
- https://www.tetris.com/about

Observed:
- 공식 Tetris site는 Tetris logos, theme song and Tetriminos를 trademarks로, Tetris trade dress를 Tetris Holding 소유로 명시.

Disposition:
- `PATTERN_EXTRACT` only for abstract grid placement/completion reasoning.
- `TETRIS_TRADE_DRESS_BOUNDARY` + `RIGHTS_REVIEW_REQUIRED`.
- 로고·음악·Tetrimino 표현·공식 시각 체계·trade dress를 재사용/복제 대상으로 취급하지 않는다.

## Why these sources were selected

1. 현재 10개 프로젝트의 실제 반복 문제와 직접 연결됨.
2. 원리 수준에서 서로 다른 장르/도구가 같은 문제를 해결하는 사례를 제공함.
3. Godot/ink/Yarn/Kenney/Tetris/Mega Crit처럼 공식/1차 자료로 권리·구조·개발 의도를 확인할 수 있는 축을 우선함.
4. LOADED/Kalivra처럼 개발자가 공개한 repository·설계 문서·license는 영상/검색 snippet보다 구현·권리 경계를 직접 확인할 수 있을 때 우선한다.
5. Store description은 제품의 공개 동작/포지셔닝을 관찰할 때만 사용하며 개발 의도나 성공 원인 증거로 과장하지 않음.

## Recheck triggers

- 외부 tool/engine/package를 실제 dependency로 채택할 때.
- license/terms가 바뀌었을 때.
- 특정 benchmark의 exact mechanic/rule 수치가 결정에 필요할 때.
- project identity와 benchmark similarity가 가까워져 rights/trade-dress 검토가 필요할 때.
- Kalivra source를 실제 Base code에 편입하려 할 때 `README`의 MIT 표기와 `LICENSE.md`의 추가 제한 충돌을 다시 검토한다.
