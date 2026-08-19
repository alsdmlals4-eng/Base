# Reusable Module Benchmark Source Notes

- 확인일: 2026-08-20
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
4. Store description은 제품의 공개 동작/포지셔닝을 관찰할 때만 사용하며 개발 의도나 성공 원인 증거로 과장하지 않음.

## Recheck triggers

- 외부 tool/engine/package를 실제 dependency로 채택할 때.
- license/terms가 바뀌었을 때.
- 특정 benchmark의 exact mechanic/rule 수치가 결정에 필요할 때.
- project identity와 benchmark similarity가 가까워져 rights/trade-dress 검토가 필요할 때.
