# AI-Assisted Solo/Indie Reverse-Engineering Pattern Pack — 2026-08-24

```yaml
status: RESEARCH_CAPTURE_COMPLETE
checked_at: 2026-08-24_KST
specialty_radar: docs/knowledge/game-development/AI_GAME_AND_AI_ASSISTED_INDIE_RADAR.md
source_policy_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
reuse_owner: docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md
ai_workflow_owner: docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md
module_registry_owner: docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md
project_adoption: PROJECT_ADOPTION_NOT_RUN
runtime_ai_implementation: NOT_RUN
notion_mutation: NOT_RUN
new_skill: false
new_base_scheduler: false
paid_dependency_added: false
```

## 1. 목적과 판정 한계

이 문서는 2026-08-24 KST 기준 공개된 AI-assisted 1인/소규모 게임들을 역기획·역공학해, **플레이어 가치와 생산 효율로 재사용 가능한 최소 패턴**을 추출한 첫 AI 인디 전문 Pattern Pack이다.

핵심 원칙:

```text
AI 사용 사실 != 성공 원인
출시 사실 != 흥행 증거
리뷰 수 != 품질의 완전한 측정
위시리스트/CCU self-report != 독립 감사
빠른 제작 != 낮은 총비용
많은 콘텐츠 != 좋은 게임
AI novelty != player value
```

현재 사례들은 서로 Evidence 강도가 다르다. 따라서 각 사례는 `OFFICIAL_PRODUCT_FACT`, `DEVELOPER_SELF_REPORT`, `PLAYER_REPORT`, `SECONDARY_REPORT`, `ANALYST_INFERENCE`를 섞지 않고 기록한다.

## 2. 이번 Wave의 핵심 결론

이번 사례군에서 반복된 가장 강한 패턴은 다음이다.

1. **AI는 구현 throughput을 올릴 수 있지만 재미·밸런스·명료성의 최종 판단자는 아니다.**
2. **한 문장으로 이해되는 플레이 훅과 작은 playable core가 먼저 있어야 AI가 breadth를 늘려도 방향을 잃지 않는다.**
3. **AI가 만든 breadth는 QA·성능·저장·회귀·맥락 유지 부채를 함께 늘릴 수 있다.**
4. **실제 플레이어 피드백 뒤 core system을 버리고 다시 만드는 능력은 생성 속도보다 중요하다.**
5. **플레이어에게 직접 보이는 AI 산출물은 disclosure만으로 품질 문제가 상쇄되지 않는다.**
6. **랜덤성이 강한 게임은 RNG 자체보다 RNG를 다루는 플레이어의 agency surface가 재미의 핵심이다.**
7. **AI-assisted production과 runtime generative AI는 별도 문제다.** 이번 사례 대부분은 전자이며, 후자를 정당화하지 않는다.

## 3. Case Matrix

| Case | Release state @ 2026-08-24 KST | AI lane | 현재 Evidence 신호 | 역공학 가치 | Disposition |
|---|---|---|---|---|---|
| Slotbound | DEMO, full game upcoming | PRODUCTION_ASSISTED + PLAYER_FACING_GENERATED_ASSET | Steam demo 466 reviews / 81% positive at current crawl; developer-announced 50k wishlists | 강한 플레이/생산/피드백 사례 | ADAPT |
| Ashen Crown | RELEASED 2026-07-11 | PRODUCTION_ASSISTED + PLAYER_FACING_GENERATED_ASSET | 출시 확인, 리뷰 표본 매우 작음 | breadth/architecture 실험 | TEST / REFERENCE_ONLY |
| Express 404 | UPCOMING 2026-08-25; demo available | PRODUCTION_ASSISTED | 출시 전, 사용자 리뷰 없음 | experienced-dev + AI expansion workflow | MONITOR / REFERENCE_ONLY |
| Infinite Arcana | RELEASED 2026-07-30 | PRODUCTION_ASSISTED | Steam user reviews 2 | solo bottleneck coverage workflow | REFERENCE_ONLY |
| Vapor World: Over the Mind | EARLY_ACCESS 2026-08-18 | PLAYER_FACING_GENERATED_ASSET | Steam 62 reviews / 37% positive at current crawl | visible-AI quality failure/mixed evidence | REJECT shortcut / ADOPT gate |
| Grimoire of Hecate: Tower of Starlight | DEMO | PRODUCTION_ASSISTED | developer self-report, no success claim | context/checkpoint discipline | ADOPT existing discipline |
| FARLUME: Into the Silent Dark | RELEASED 2026-06-01 | PRODUCTION_ASSISTED + PROCEDURAL_OUTPUT | Steam user reviews 2 at current crawl | constraint-driven procedural production | TEST / REFERENCE_ONLY |

`MONITOR` is a release-state handling label here, not a new Base disposition enum. Reuse disposition remains `ADOPT | ADAPT | TEST | REJECT | REFERENCE_ONLY`.

---

## 4. Slotbound — 가장 강한 현재 Pilot 사례

### 4.1 Evidence

Primary/store:
- Steam Demo: <https://store.steampowered.com/app/4906570/Slotbound_Demo/>
- Steam Community announcements: <https://steamcommunity.com/app/4459590/allnews/>

Developer self-report:
- 8-month AI-assisted build report: <https://www.reddit.com/r/aigamedev/comments/1usuhxn/i_still_cant_code_but_after_8_months_the_steam/>
- demo traction report: <https://www.reddit.com/r/IndieDev/comments/1uv5ipw/i_opened_steam_and_saw_the_first_game_i_ever_made/>

Evidence ceiling:

```text
OFFICIAL_PRODUCT_FACT
+ OFFICIAL_UPDATE_HISTORY
+ DEVELOPER_SELF_REPORT
+ public Steam review signal
!= independent causal proof that AI caused traction
```

2026-08-24에 확인한 Steam crawl은 demo에 466개 평가와 81% 긍정을 표시했다. 50,000 위시리스트는 2026-07-27 공식 개발자 공지의 self-reported milestone이다.

### 4.2 One-sentence hook

```text
What if a slot machine built your army?
```

이 훅은 시스템 설명을 거의 그대로 플레이 기대감으로 바꾼다.

```text
3x3 slot spin
→ unit summon
→ keep / absorb / strengthen
→ Items + Cores alter probabilities/build rules
→ battle/wave
→ survive / boss
→ repeat with stronger run identity
```

### 4.3 실제 재미 구조

표면은 슬롯머신이지만 플레이어가 하는 일은 단순 운 확인이 아니다.

```text
RNG produces candidates
→ player interprets current board/build
→ keep valuable outcomes
→ absorb expendable outcomes
→ protect units that should not be consumed
→ alter odds with Items/Cores
→ commit to wave
→ learn which build rule matters
```

즉, **랜덤 결과를 받은 뒤 어떤 결과를 보존·희생·전환할지 결정하는 것**이 전략층이다.

### 4.4 중요한 업데이트 역공학

2026-07-23 v0.3.0은 Core system을 거의 처음부터 다시 만들었다. 목적은 Core가 실제 플레이 방식을 더 명확하게 바꾸고, 조합과 run variety를 강화하는 것이었다. 같은 업데이트에서 absorption 재료가 되지 않도록 하는 manual lock과 mid-run save도 추가됐다.

2026-07-27 v0.3.1은 frame drop, Stage 1 난이도, Core activation 문제를 hotfix했다.

여기서 중요한 것은 기능 수가 아니다.

```text
player feedback
→ identify core-choice weakness
→ local parameter tweak로 덮지 않음
→ Core system rebuild
→ new agency/clarity affordance (manual lock)
→ save/usability/stability fixes
→ performance/balance hotfix
```

이 흐름은 `PLAYER_FEEDBACK_REBUILD_LOOP`의 강한 공개 사례다.

### 4.5 AI production 역공학

개발자는 코딩 경험이 거의 없다고 밝히면서 AI coding tool에 원하는 동작을 설명하고, 결과를 직접 실행·테스트하고, 깨진 부분을 다시 고치는 과정을 반복했다고 설명한다. 동시에 AI가 재미, 밸런스, 이해 가능성을 결정해 주지는 못했기 때문에 UI 재구축, 아이디어 폐기, 반복 테스트를 직접 수행했다고 적었다.

흡수:

```text
ADOPT:
- one-sentence playable hook
- human-directed AI build loop
- public demo feedback loop
- willingness to rebuild a weak core
- RNG agency/control lens
- bad-output recovery/absorption

ADAPT:
- content breadth only after core identity is legible
- AI-assisted visual pipeline only behind quality/rights gate

REJECT:
- "AI가 만들었으니 빠르게 더 많이 추가"를 품질 근거로 쓰기
- demo traction을 AI 사용의 인과적 성공 증거로 쓰기
- stability/performance debt를 generation speed와 상쇄하기
```

---

## 5. Ashen Crown — breadth 실험은 성공 증거가 아니다

Primary:
- Steam: <https://store.steampowered.com/app/4826250/Ashen_Crown/>

Steam disclosure에 따르면 이 게임은 generative AI를 거의 전체 제작에 사용했고, Claude와의 대화로 code를 작성하면서 사람이 directing/correcting/testing/deciding을 맡았다. 시각은 code-drawn이며 sound/music도 AI 생성이라고 공개한다. Godot 사용도 공개돼 있다.

공개 제품 설명은 12 weapons, 24 classes, 53 subspecs, 247 skills, 94 masteries 등 매우 넓은 content surface를 내세운다. 그러나 현재 리뷰 표본은 시장 성공이나 장기 재미를 판단하기에 너무 작다.

역공학:

```text
AI strength:
small team/solo → breadth generation becomes feasible

AI risk:
breadth → more combinations → more balance surfaces → more QA surfaces
       → more architecture/context surfaces
```

판정:

```text
TEST:
- AI로 variant/content breadth를 늘리는 생산 방식

ADOPT:
- human directs/corrects/tests/decides라는 책임 분리

REJECT:
- content count를 player value 증거로 사용
- 작은 리뷰 표본을 AI-production 성공 증거로 승격
```

이 사례는 `BREADTH_AFTER_CORE_IDENTITY_LOCK`와 `CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET`의 필요성을 강화한다.

---

## 6. Express 404 — experienced developer가 AI를 확장기로 사용

Primary:
- Steam: <https://store.steampowered.com/app/4329710/Express_404/>

Developer self-report:
- <https://www.reddit.com/r/aigamedev/comments/1vqf990/in_9_days_my_experimental_aiassisted_game_will_be/>

2026-08-24 기준 Steam은 2026-08-25 출시 예정이며 사용자 리뷰가 없다. 따라서 **출시 성공 사례로 사용하지 않는다.**

개발자는 약 10년의 gamedev 경험이 있으며, 초기 code base는 직접 만든 뒤 ChatGPT로 구조를 분석하고 세부 구현을 확장했으며 모든 변경을 직접 확인했다고 self-report했다. Art는 여러 AI 도구를 사용했으나 초기 결과가 매우 나빴고 반복 수정으로 일관성을 높였다고 설명한다.

플레이 훅:

```text
night train
+ speed/quota management
+ 4–8 passengers
+ one mimic
+ lightning-only kill clues
+ wrong accusation loses profit
+ upgrades can turn danger/death into economy
```

흡수 포인트:

```text
ADOPT workflow hypothesis:
human architecture seed
→ AI analyses existing structure
→ bounded expansion
→ every change manually reviewed

ADAPT gameplay:
hidden threat + economic cost + environmental reveal window

MONITOR:
release reception after 2026-08-25
```

현재 단계에서 흥행·장기 유지성·AI 생산성의 실측 성공을 주장할 수 없다.

---

## 7. Infinite Arcana — AI가 ‘프로그래밍 외 1인 제작 병목’을 메우는 방식

Primary:
- Steam: <https://store.steampowered.com/app/4754330/Infinite_Arcana/>

Developer self-report:
- <https://www.reddit.com/r/aigamedev/comments/1udqyt2/after_10_years_as_a_programmer_i_finally_built/>

Steam 기준 2026-07-30 출시, 현재 crawl에서 user review 2개다. 따라서 market validation은 매우 약하다.

개발자 self-report에서 중요한 점은 **기존 프로그래머도 solo game production에서는 art/UI/localization/marketing/trailer/production 병목을 만난다**는 것이다. AI의 가치는 core engineering을 대신했다는 주장보다, 팀이 없어서 막히는 adjacent production surface를 덮는 데 있었다.

플레이 설계도 참고 가치가 있다.

```text
arcane slot-wheel
→ each spin costs mana
→ symbol match produces damage/shield/mana
→ enemy spell charge advances
→ push another spin vs play safe
```

이 구조는 Slotbound와 마찬가지로 랜덤 장치 자체가 아니라 **resource cost + risk clock + player-controlled continue/stop decision**이 핵심이다.

판정:

```text
ADAPT:
- AI for bounded solo-production bottlenecks
- RNG + resource cost + push/stop tension

REJECT:
- multi-discipline output count as validation

REFERENCE_ONLY:
- market success until real player evidence grows
```

---

## 8. Vapor World: Over the Mind — visible AI output의 품질 반례

Primary:
- Steam: <https://store.steampowered.com/app/1996090/Vapor_World_Over_The_Mind/>

Secondary current report:
- GamesRadar, 2026-08-20: <https://www.gamesradar.com/games/action/after-25-percent-positive-steam-reviews-soulslike-dev-realizes-people-hate-ai-slop-and-admits-if-it-looks-like-the-effort-is-not-there-that-is-a-fair-reading-of-what-is-on-screen/>

2026-08-24 current Steam crawl은 Early Access 2026-08-18 출시, 62 reviews, 37% positive를 표시한다. 이 전체 점수를 AI 한 요인에 귀속하지 않는다.

다만 2차 보도에 따르면 launch backlash의 주요 비판 중 하나가 AI-generated cutscenes/voice였고, director가 perceived lack of effort라는 해석을 인정하며 AI cutscenes를 제거/대체하겠다고 밝혔다.

따라서 이 사례의 안전한 교훈은 다음까지다.

```text
player-facing generated asset
+ visible inconsistency / low perceived craft
→ disclosure alone does not repair perceived value
→ replacement/rework cost can erase production-speed savings
```

판정:

```text
ADOPT:
AI_VISIBLE_OUTPUT_QUALITY_GATE

REJECT:
AI-generated presentation as a shortcut that bypasses normal craft/consistency gate

DO NOT CLAIM:
AI alone caused the overall review score
```

---

## 9. Grimoire of Hecate — Context drift를 Markdown checkpoint로 완화

Primary product:
- Steam demo: <https://store.steampowered.com/app/5078840/Grimoire_of_Hecate__Tower_of_Starlight/>

Developer self-report:
- <https://www.reddit.com/r/ChatGPT/comments/1vu6tjv/three_months_of_building_a_steam_demo_with/>

2026-08-21 개발자 글은 Godot 기반 첫 게임 demo를 약 3개월 동안 ChatGPT/Codex와 작업했다고 설명한다. ChatGPT는 design detail 정리에, Codex는 project files에서 code/tests 작성·수정에 사용했다. 사람은 결과를 review/run/play/revise했다.

가장 중요한 실패는 프로젝트가 커질수록 AI가 earlier decisions를 잃거나 잘못된 부분을 바꾸는 문제였다. 개발자는 이를 완화하려고 **각 task 뒤 현재 상태를 Markdown으로 기록**했다고 설명한다.

이 사례는 새 모듈을 요구하지 않는다. Base가 이미 canonical context, evidence checkpoint, scoped owner, changed-surface verification을 갖고 있으므로 기존 discipline을 강화하는 evidence다.

```text
ADOPT existing discipline:
- post-task current-state checkpoint
- canonical owner/context rehydration
- changed-surface review
- human run/play verification

REJECT:
- ever-growing chat memory를 project architecture로 사용
```

---

## 10. FARLUME — 제약을 production multiplier로 사용하는 사례

Primary:
- official: <https://farlume.com/>
- press kit: <https://farlume.com/press/>
- Steam: <https://store.steampowered.com/app/4604120/FARLUME_Into_the_Silent_Dark/>

공식 사이트에 따르면 solo developer가 Godot 4.6으로 만들었고 모든 pixel을 code/procedural geometry로 그리는 visual constraint를 채택했다. Claude Code가 code development와 store localization에 사용됐고 music/SFX도 code generation 경로를 사용했다고 공개한다. Steam의 현재 review 표본은 2개이므로 흥행 증거는 아니다.

여기서 가져올 것은 “AI가 아티스트를 대체한다”가 아니다.

```text
solo constraint
→ choose visual identity compatible with procedural/code output
→ narrow asset ontology
→ reuse geometry/shader/rule vocabulary
→ scale variants without thousands of hand-authored files
```

Candidate lens:

### CONSTRAINT_DRIVEN_PROCEDURAL_ASSET_PIPELINE

```text
art/production constraint
→ deliberately narrow visual grammar
→ code/procedural generator
→ deterministic reusable primitives
→ visual identity gate
→ performance/readability/accessibility check
```

Disposition: `TEST / REFERENCE_ONLY`.

아직 Base 공용 모듈로 승격하지 않는다. 여러 프로젝트에서 같은 interface가 실제로 재사용될 때까지 technical-art production pattern으로만 보관한다.

---

# 11. 재사용 Production Contracts

## 11.1 HUMAN_DIRECTED_AI_BUILD_LOOP

**Evidence:** Slotbound, Ashen Crown, Express 404, Grimoire of Hecate.

```text
human intent / acceptance criteria
→ bounded AI change
→ changed-surface audit
→ test/build/run
→ player-value judgement
→ accept | revise | revert
→ evidence/context refresh
```

기존 owner:

- `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`
- `RM-WORK-002 SKILL_WORKFLOW_PATTERN_EVAL`
- repository/project verification contracts

판정: **ADOPT as a reusable lens, not a new Skill.**

AI가 code를 작성하는가보다 중요한 것은 누가 acceptance criteria와 최종 판단을 소유하는가다.

## 11.2 SILENT_OMISSION_GATE

AI-assisted change 뒤 다음을 반드시 공격한다.

```text
What requested behavior is still missing?
What was simplified or silently skipped?
Which consumers were not updated?
Which failure paths were not tested?
Did the change add hidden architecture debt?
```

기존 owner:
- AI workflow verification
- changed-surface/repository validation
- adversarial review lifecycle

판정: **ADOPT.**

## 11.3 CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET

AI throughput은 monolith 허가가 아니다.

각 change는 최소 다음 owner를 식별한다.

```text
canonical owner
mutable state owner
resolver
presenter
persistence
validation/tests
rollback
```

AI가 관련 contract를 반복해서 놓치거나 잘못된 부분을 수정하면 prompting만 늘리지 말고 책임을 더 작은 owner로 분리하거나 current-state checkpoint를 갱신한다.

기존 owner overlap:
- `PROJECT_SUBSYSTEM_CHANGE_MAP`
- project canon/context contracts
- AI-assisted development guide

판정: **ADOPT by strengthening existing owners; no duplicate framework.**

## 11.4 BREADTH_AFTER_CORE_IDENTITY_LOCK

```text
small playable core
→ core player promise verified
→ state/schema ownership stabilized
→ visual/UX identity bar stabilized
→ cheap rejection criteria exist
→ only then multiply variants/content with AI
```

Ashen Crown/FARLUME/Infinite Arcana의 넓은 content surface는 가능성의 증거지만, broad content 자체가 success evidence는 아니다.

판정: **ADOPT as production gate.**

## 11.5 PLAYER_FEEDBACK_REBUILD_LOOP

Slotbound의 공개 업데이트 흐름에서 가장 강하게 관찰된다.

```text
public demo / real player evidence
→ classify:
   bug
   clarity
   balance
   weak core choice
→ local defect: hotfix
→ player promise failure: rebuild system
→ regression check
→ new player evidence
```

`Core system overhaul`처럼 기존 기능을 보존하는 것보다 **의사결정 품질을 살리기 위해 다시 만드는 것**이 더 효율적인 경우를 인정한다.

판정: **ADOPT.**

## 11.6 AI_VISIBLE_OUTPUT_QUALITY_GATE

Player-facing AI output은 사람이 만든 output과 다른 품질 기준을 적용받지 않는다.

```text
generated output
→ art direction consistency
→ readability / UX
→ animation/audio continuity
→ copyright/license/provenance
→ platform disclosure/compliance
→ human quality review
→ in-game context test
→ accept | rework | replace
```

핵심:

```text
disclosure != quality waiver
generation speed != replacement/rework cost saved
```

Vapor World의 current reception은 이 Gate를 강화하는 failure/mixed evidence다. 전체 리뷰 점수의 원인을 AI 하나로 단정하지 않는다.

판정: **ADOPT.**

---

# 12. 재사용 Gameplay Contract Candidate

## RNG_AGENCY_AND_RECOVERY

**Primary evidence:** Slotbound.
**Supporting structural evidence:** Infinite Arcana.

```text
unpredictable outcome
→ player control surface
   reroll
   lock
   weight shift
   banish
   convert
   absorb
   sell
   bank
   combine
→ control has cost/tradeoff
→ bad outcome still creates a decision, information, or future resource
→ build/run identity becomes legible
```

### 왜 중요한가

랜덤 결과가 재미를 주는 것이 아니라 다음 질문이 재미를 만든다.

```text
이 결과를 받아들일까?
다시 굴릴까?
보존할까?
희생할까?
다른 자원으로 바꿀까?
확률 자체를 바꿀까?
이번 Run의 정체성을 여기서 고정할까?
```

### Existing Solution First

새 `RM-SYS-*`를 만들지 않는다. 우선 아래 기존 owner에 adapter/lens로 시험한다.

- `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE`
- `RM-SYS-018 ROULETTE_TOKEN_SOURCE_ENGINE`
- `RM-SYS-019 PUSH_YOUR_LUCK_ENHANCEMENT_ENGINE`
- `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE`
- `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR`

새 공용 모듈 승격 조건:

```text
>= 2 materially distinct project pilots
+ existing modules cannot express common interface cleanly
+ deterministic replay/balance evidence
+ no duplicated state authority
```

현재 disposition: **ADAPT / TEST, no new module.**

---

# 13. Runtime Generative AI 후보와 경계

이번 Pattern Pack의 주 사례는 대부분 production-assisted다. 따라서 runtime AI를 자동 도입하지 않는다.

앞선 AI-game benchmark에서 남길 가치가 있는 최소 후보 구조는 다음이다.

```text
freeform player input
→ AI semantic interpretation/proposal
→ project-owned deterministic validator
→ authoritative GameState mutation by game rules only
→ result presentation
→ bounded memory update
```

후보 기능:

- semantic action interpretation
- layered memory / canon retrieval
- capability contract preventing impossible promises/actions
- semantic combination with cache
- discovery/codex reward
- emotion/relationship state interpreted but numerically resolved by deterministic rules

프로젝트 Pilot 전 필수:

```text
PLAYER_VALUE_UNIQUE_TO_AI
CAPABILITY_CONTRACT
DETERMINISTIC_STATE_VALIDATION
MEMORY_CANON_BOUNDARY
LATENCY_OFFLINE_FALLBACK
PRIVACY_MODERATION_SECURITY
COST_SURFACE_APPROVED
PLATFORM_STORE_COMPLIANCE
REPLAY_DEBUG_EVIDENCE
```

현재 disposition: **TEST only. runtime implementation NOT_RUN.**

---

# 14. Project-fit Hypothesis

아래는 Base 수준 후보 routing이다. 각 프로젝트 최신 정본을 읽고 독립 승인/검증하기 전까지 모두 `PROJECT_ADOPTION_NOT_RUN`이다.

| Project | Candidate | Initial disposition | 이유/경계 |
|---|---|---|---|
| OMENWARD | RNG_AGENCY_AND_RECOVERY + explainable roulette odds/build identity | ADAPT — high | 기존 roulette/token/push-your-luck owner와 직접 겹침. 새 모듈보다 adapter 우선 |
| NINJA_SURVIVAL | bad reward/drop recovery via combine/workbench/convert | ADAPT — high | 나쁜 드랍을 무효시간이 아니라 다음 제작 판단으로 전환 가능 |
| BLACKSMITH | push-your-luck + outcome recovery + visible consequence feedback | ADAPT — high | 강화 긴장과 실패/내구/회수 결정에 적합하나 최신 정본 검증 필요 |
| GRIMOIRE | semantic combination + deterministic rule validation + discovery rewards | TEST — medium-high | runtime AI를 넣더라도 authoritative spell rules는 deterministic 유지 |
| URBAN_LEGEND | layered memory/canon-aware interpretation for investigation | TEST — medium | 자유대화가 아니라 조사 선택/정합성 향상 가치가 증명될 때만 |
| MY_LITTLE_BOAT | relationship memory + capability contract | TEST — medium-low | 대화/관계가 실제 core need로 검증될 때만 |
| TETRIS | AI production workflow | ADOPT workflow / REJECT runtime | 현재 core에 generative runtime의 unique player value가 없음 |
| SWITCHY | AI production workflow; possible RNG lens only if random logistics appears | REFERENCE_ONLY gameplay | 기존 core를 흔들 근거 없음 |
| TEN_PACES | workflow only | ADOPT workflow / REJECT runtime | hidden-plan/deterministic integrity를 자유생성보다 우선 |
| COC_FICTION | canon review/production workflow | ADOPT workflow / REJECT runtime game AI | narrative canon support와 runtime generative game system은 별개 |

이 표는 프로젝트 정본 변경 권한이 아니다.

---

# 15. 최소 3안 비교 — Base 흡수 방식

## A. AI Game 전용 새 Skill/Framework

장점: 이름이 명확하고 한곳에 모임.

문제:
- existing Watchlist 중복
- reverse-engineering pipeline 중복
- AI guide 중복
- module registry 중복
- scheduler 권한 중복

**REJECT.**

## B. 외부 주간 검색만 수행

장점: Base 변경 최소.

문제:
- 이전 주와 비교가 구조화되지 않음
- failure evidence가 사라짐
- 매번 같은 아이디어를 새 모듈처럼 제안할 위험
- project-fit과 owner overlap 학습이 누적되지 않음

**REJECT as insufficient.**

## C. Existing Watchlist + Specialty Radar + Pattern Pack

장점:
- source policy는 기존 owner 유지
- 주간 scheduling은 Base 밖 유지
- Pattern Pack은 evidence를 축적
- 재사용 승격은 기존 registry가 계속 결정
- AI production과 runtime AI를 분리

**ADOPT.**

---

# 16. Implementation Reality Gate

## VERIFIED / 주장 가능

- 2026-08-24 기준 위 사례들의 공개 store/developer evidence를 조사했다.
- AI game/AI-assisted indie specialty weekly capture contract가 Base branch에 작성됐다.
- production AI와 runtime generative AI를 별도 lane으로 분리했다.
- success와 failure/mixed evidence를 함께 기록했다.
- Existing Solution First로 RNG candidate를 기존 `RM-SYS-003/018/019`와 먼저 연결했다.
- 프로젝트별 fit은 hypothesis로만 기록했다.
- 새 Skill, Base scheduler, paid dependency, runtime AI implementation을 만들지 않았다.

## UNVERIFIED / 주장 금지

- 프로젝트가 후보 시스템을 실제 채택했다.
- 후보가 retention, wishlist, sales를 개선한다.
- Slotbound의 traction이 AI 사용 때문에 발생했다.
- AI-assisted production이 human correction/QA를 포함해 항상 더 빠르거나 싸다.
- Ashen Crown/Infinite Arcana/FARLUME가 market success 사례다.
- Express 404가 출시 후 성공할 것이다.
- Vapor World의 전체 negative reception이 AI 하나 때문에 발생했다.
- semantic runtime AI가 현재 프로젝트에서 필요하다.

## 다음 Promotion Gate

```text
research pattern
→ current project canon read
→ project player-value hypothesis
→ existing owner adapter design
→ deterministic POC where possible
→ QA/replay/balance evidence
→ human playtest
→ adversarial review
→ ADOPT | ADAPT | REJECT
```

---

# 17. Adversarial review 5/5

**Result: PASSED_WITH_RESOLVED_FINDINGS**

## Loop 1/5 — Duplication attack

공격:
- `RNG_AGENCY_AND_RECOVERY`를 새 범용 gameplay module로 등록하면 기존 draft/roulette/push-your-luck owner와 중복된다.

해결:
- 새 `RM-SYS-*` 생성 금지.
- 기존 `RM-SYS-003`, `RM-SYS-018`, `RM-SYS-019` adapter/lens로 Pilot 후 다중 프로젝트에서 실제 공통 interface가 증명될 때만 승격.

## Loop 2/5 — Causality attack

공격:
- Slotbound의 review/wishlist/CCU 신호를 “AI로 만들었기 때문에 성공”으로 읽을 수 있다.

해결:
- production method와 gameplay traction을 분리.
- developer self-report를 별도 evidence class로 유지.
- popularity signal에 causality 권한을 부여하지 않음.

## Loop 3/5 — Solo-dev reality attack

공격:
- AI가 content breadth를 늘리는 동안 QA, performance, save, balance, architecture, context debt가 은폐될 수 있다.

Evidence:
- Slotbound는 public demo 뒤 major Core rebuild와 performance/stability hotfix를 수행했다.
- Ashen Crown/FARLUME는 큰 breadth를 보여도 현재 market validation이 약하다.

해결:
- `HUMAN_DIRECTED_AI_BUILD_LOOP`
- `SILENT_OMISSION_GATE`
- `CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET`
- `BREADTH_AFTER_CORE_IDENTITY_LOCK`
- 기존 `HUMAN_EDIT_DELTA` 관점 재사용.

## Loop 4/5 — Player-value attack

공격:
- “AI가 가능하니까” runtime AI를 넣으면 플레이어의 선택·감정·보상이 아니라 기술 데모가 된다.

해결:
- runtime AI 기본값을 `TEST`로 유지.
- `PLAYER_VALUE_UNIQUE_TO_AI`를 첫 Gate로 배치.
- authoritative state는 deterministic validator 이후 game rules가 소유.

## Loop 5/5 — Maintenance / rights / cost attack

공격:
- provider/API cost, rights, disclosure, inconsistent generated presentation, model drift, offline failure가 1인 개발 장기 유지비를 높인다.

해결:
- 이번 Base 흡수에는 paid/runtime dependency를 추가하지 않음.
- `AI_VISIBLE_OUTPUT_QUALITY_GATE` 추가.
- runtime Pilot은 cost/platform/privacy/replay/debug gate 전부 통과해야 함.
- procedural/code visual 사례는 style constraint pattern으로만 유지하고 universal solution으로 승격하지 않음.

### Clean-exit check

```text
new unresolved authority conflict: none found
new duplicate module: none created
project canon mutation: none
runtime AI implementation: none
paid dependency: none
upcoming title misrepresented as shipped success: no
popularity used as causality proof: no
```

Adversarial review 5/5 완료 후 새 blocking conflict를 발견하지 못했다.

---

# 18. 다음 주 Scan에서 비교할 항목

```yaml
previous_scan: 2026-08-24
priority_recheck:
  - Slotbound:
      watch: [review_delta, hotfixes, full_release_state, Core/balance changes]
  - Express_404:
      watch: [release_state, early_reviews, launch_hotfixes, AI-art reception]
  - Vapor_World:
      watch: [AI-cutscene replacement, review_delta, patch_response]
  - Ashen_Crown:
      watch: [review_growth, postmortem, architecture_or_QA_updates]
  - Infinite_Arcana:
      watch: [review_growth, developer_postmortem]
  - Grimoire_of_Hecate:
      watch: [demo_feedback, context_process_updates]
  - FARLUME:
      watch: [review_growth, production_postmortem, performance/readability evidence]
new_case_queries:
  - solo AI-assisted Steam demo
  - AI-assisted Godot indie release
  - AI-generated game postmortem
  - generative AI game Steam recent reviews
  - solo developer Claude Code Codex game
  - AI game player backlash removal replacement
```

주간 scan은 새 사례를 찾는 것만이 아니라 **기존 사례의 평가가 뒤집혔는지, 실패가 새로 드러났는지, candidate를 승격/강등해야 하는지**를 비교한다.
