# 벤치마크·플레이어 반응·플레이테스트 근거 모델

이 문서는 `analyzing-and-refining-game-concepts`의 `benchmark-and-player-research`, `playtest-and-experiment` mode가 사용하는 상세 근거 모델이다. 외부 사례를 복사하는 절차가 아니라 **현재 기획 가설을 반증하고 개선 결정을 만드는 절차**다.

## 1. 조사 질문을 먼저 고정한다

```yaml
decision_to_make:
current_hypothesis:
what_would_change_the_decision:
target_player_segment:
platform_region_language:
release_or_patch_window:
comparable_dimension:
excluded_questions:
```

“비슷한 게임을 조사한다”로 시작하지 않는다. 다음처럼 현재 결정을 바꿀 수 있는 질문으로 좁힌다.

- 같은 핵심 행동이 다른 게임에서 어떤 기대와 불만을 만드는가?
- 첫 의미 있는 보상·튜토리얼·세션 길이에서 이탈이 발생하는가?
- 플레이어가 상점 설명·영상으로 기대한 경험과 실제 플레이가 일치하는가?
- 경쟁작의 강점이 우리 핵심 컨셉에 필요한가, 장르 관습일 뿐인가?
- 특정 개선안이 행동 데이터와 자기보고 반응에서 모두 지지되는가?

## 2. 근거 층위

| 층위 | 예시 | 사용 방식 |
|---|---|---|
| 제품 사실 | 공식 상점 페이지, 패치 노트, 개발 문서, 실제 플레이·영상 | 기능·규칙·버전·플랫폼 상태 확인 |
| 플레이어 반응 | Steam 리뷰, 커뮤니티, 포럼, 설문, 플레이테스트 기록 | 기대 충족·불만·반복 패턴 탐색 |
| 행동 근거 | 이벤트, 퍼널, 세션 기록, 성공·실패·이탈 | 실제 행동과 자기보고를 분리해 검증 |
| 통제 실험 | A/B 테스트, 동일 과제의 변형 빌드 | 한 가설의 인과 비교 |
| 해석·제안 | 기사, 영상 해설, 모델 추론 | 후보 가설로만 사용하고 상위 근거로 검증 |

한 출처가 다른 층위의 권한을 대신하지 않는다. 리뷰는 구현 사실의 정본이 아니고, 이벤트 수치는 플레이어가 왜 그렇게 행동했는지 단독으로 설명하지 못한다.

## 2.1 중요 기획의 필수 Evidence Pack

중요 기획·방향성·제품 결정은 다음 세 층을 함께 검토한다. 단순 오탈자·기계 수정·동일 입력 검사 재실행은 예외다.

- `BENCHMARK_EVIDENCE`: 직접 경쟁작, 인접 장르, 실패·혼합 반응 사례에서 비교 원리와 실패 조건을 추출한다.
- `PLAYER_RESPONSE_EVIDENCE`: 긍정·부정·혼합 리뷰, 커뮤니티, 플레이테스트와 행동 근거에서 기대·불만·맥락을 구분한다.
- `PROFESSIONAL_OFFICIAL_EVIDENCE`: 현업 발표·사후 분석과 공식 플랫폼·엔진·접근성·운영 문서에서 권장 조건과 제약을 확인한다.

한 층이 다른 층을 대체하지 않는다. 세 층을 모두 찾지 못하면 없는 근거를 만들어내지 않고 `BLOCKED_UNVERIFIED` 또는 제한된 신뢰도로 기록한다.

## 3. 비교 대상 선정

비교 게임은 장르 이름보다 **비교 차원**으로 고른다.

- 같은 핵심 행동·판단
- 같은 세션 길이·입력 환경
- 같은 성장·보상 구조
- 같은 가격·운영 방식
- 같은 대상 플레이어·난이도 약속
- 같은 제작 제약이나 플랫폼
- 성공 사례뿐 아니라 실패·혼합 반응 사례

최소 구성:

```text
직접 경쟁작 2~3
+ 핵심 행동이 유사한 인접 장르 1~2
+ 실패·혼합 반응 사례 1
+ 게임 밖 상호작용 참고 1 (필요한 경우)
```

## 4. 플레이어 반응 표본

- 긍정·부정·혼합 반응을 모두 본다.
- 최신 반응과 누적 반응을 구분한다.
- 초보·장기 플레이어, 짧은·긴 플레이타임, 플랫폼·언어·지역을 구분한다.
- 특정 패치 전후를 섞지 않는다.
- 반복되는 구체 상황과 영향도를 우선하고, 강한 표현의 수를 중요도로 착각하지 않는다.
- 리뷰 폭탄·오프토픽·밈·복사 리뷰는 별도 표시한다.
- 플레이어가 요구한 해결책보다 **겪은 문제·기대·맥락**을 먼저 추출한다.

Steamworks는 리뷰를 기대가 올바르게 설정되고 충족되는지 이해하는 피드백 채널로 설명하지만, 리뷰 하나가 제품 개선 전체를 지배하게 하지 말라고 안내한다.

## 5. 반응 코딩

각 근거를 다음 구조로 기록한다.

```yaml
source:
date_and_version:
player_context:
observed_fact:
reported_experience:
trigger_or_situation:
impact:
frequency_signal:
confidence:
possible_explanations:
```

반응 클러스터 예:

- 기대 불일치
- 이해·가독성·온보딩
- 조작·피드백 지연
- 난이도·공정성
- 반복·콘텐츠 피로
- 보상·경제·진행
- 성능·안정성
- 접근성·입력 장벽
- 가격·운영·신뢰
- 핵심 재미 강화·차별화

## 6. 개선 변환

근거마다 다음 중 하나로 판정한다.

- `ADOPT`: 핵심 컨셉과 제약에 맞고 직접 채택한다.
- `ADAPT`: 원리는 유효하지만 우리 핵심 행동에 맞게 변형한다.
- `AVOID`: 반복 실패·기대 불일치·제작 위험이 크다.
- `TEST`: 근거가 상충하거나 프로젝트 적용성이 미확정이다.
- `IGNORE`: 비교 차원·대상 플레이어·버전이 달라 현재 결정과 무관하다.

```yaml
finding:
evidence:
core_concept_alignment:
player_value:
production_cost:
risk:
decision: ADOPT/ADAPT/AVOID/TEST/IGNORE
change_candidate:
validation_needed:
```

유행·평점·판매량만으로 핵심 컨셉을 변경하지 않는다. 사례의 기능을 복사하지 말고 문제를 해결한 원리와 실패 조건을 추출한다.

## 7. 플레이테스트·실험 계약

Steam Playtest는 메인 게임과 분리된 저위험 테스트 앱으로 외부 플레이 데이터를 모을 수 있고, 개발자가 원하는 피드백 채널을 게임 안에 명확히 안내하도록 권장한다. 기존 지식이 결과를 오염시키면 새 테스터 집단으로 다시 확인한다.

```yaml
hypothesis:
build_and_version:
tester_segment:
cohort_size_and_recruitment:
prior_exposure:
tasks_or_play_window:
observation_points:
feedback_questions:
feedback_channel:
telemetry_events:
funnel_steps:
control_and_variants:
primary_metric:
guardrail_metrics:
success_failure_stop:
```

- 관찰된 행동, 이벤트·퍼널, 인터뷰·설문 자기보고를 분리한다.
- 질문은 해결책을 유도하지 않고 경험·혼란·기대·결정 이유를 묻는다.
- A/B 테스트는 한 번에 하나의 주요 가설을 비교하고, 통제군·변형·주 지표·가드레일을 미리 선언한다.
- 이벤트는 플레이어 행동과 당시 맥락을 함께 기록하고, 퍼널은 순서가 있는 단계와 이탈·소요 시간을 확인한다.
- 결과를 본 뒤 성공 기준을 바꾸지 않는다.

## 8. 실패 조건

- 인기 게임 기능 목록을 그대로 모방한다.
- 리뷰 수나 평점만으로 원인을 단정한다.
- 긍정 또는 부정 반응만 골라 현재 기획을 정당화한다.
- 버전·패치·플레이타임·플랫폼 차이를 무시한다.
- 플레이어가 제안한 해결책을 문제 분석 없이 그대로 구현한다.
- 자기보고만으로 실제 행동을 단정하거나, 행동 수치만으로 감정·이유를 단정한다.
- 여러 변수를 동시에 바꾼 실험을 인과 근거로 사용한다.
- 출처·날짜·표본·불확실성을 기록하지 않는다.

## 공식 참고 자료

- Steamworks — User Reviews: https://partner.steamgames.com/doc/store/reviews
- Steamworks — Steam Playtest: https://partner.steamgames.com/doc/features/playtest
- Steamworks — Testing On Steam: https://partner.steamgames.com/doc/store/testing
- Unity Analytics — Events: https://docs.unity.com/en-us/analytics/events/events
- Unity Analytics — Funnels: https://docs.unity.com/en-us/analytics/funnels/funnels
- Unity Game Overrides — A/B testing: https://docs.unity.com/en-us/game-overrides/ab-testing

---

## 9. 시장조사 Source와 숫자 해석

시장조사의 목표는 “인기 게임 목록”을 만드는 것이 아니라 **우리 결정에 필요한 비교 차원, 시장의 기본 기대(table-stakes), 실패 패턴, 빠르게 읽히는 차별화 후보를 찾는 것**이다.

### 9.1 Source hierarchy

```text
공식 store / platform / developer·publisher first-party statement
→ 명시된 product fact와 metric에 한해 VERIFIED 후보

SteamDB / GameDiscoverCo / Sensor Tower Game IQ / Video Game Insights(VGI)
→ market intelligence / discovery / estimate evidence

기사 / creator / community 해석
→ context·hypothesis 후보
```

- **SteamDB**는 Steam application/package update, player chart, price/history 등을 조사하는 독립 정보면이다. Steam/Valve의 공식 서비스가 아니며 data accuracy를 보증하지 않는다.
- **GameDiscoverCo**는 PC/console discovery와 market-data 비교를 위한 전문 Source 후보다. 자체 estimator나 affinity/player estimate는 공식 판매 숫자가 아니다.
- **Sensor Tower Game IQ**는 mobile sub-genre, theme, art style, monetization, meta feature와 downloads/revenue 비교에 유용한 전문 market-intelligence Source다. Sensor Tower가 제공하는 추정치는 first-party store/developer 공개값과 구분한다.
- **Video Game Insights(VGI)**는 Steam unit-sales estimate 방법과 정확도 표본을 공개하지만 결과는 여전히 model estimate다. `ESTIMATED_100K_PLUS`를 `VERIFIED_100K_SALES`로 바꾸지 않는다.

시장 Source는 다음을 한 숫자로 합치지 않는다.

```text
downloads / installs
paid sales / copies sold
revenue / gross / IAP revenue
wishlists
reviews
followers
CCU / peak concurrent players
MAU / active users
estimated owners / estimated units
```

## 10. 10만+ 성공 사례 qualification

사용자 승인 기준에 따라 10만+는 **download/install과 paid sales를 별도 성공 라벨로 인정**하며 서로 대체하지 않는다.

```text
VERIFIED_100K_DOWNLOAD_INSTALL
VERIFIED_100K_SALES
ESTIMATED_100K_PLUS
NOT_100K_VERIFIED
```

### `VERIFIED_100K_DOWNLOAD_INSTALL`

공식/public store가 download/install bucket을 공개하거나 개발사·플랫폼 first-party 발표가 downloads >= 100,000을 명시한 경우에만 사용한다.

### `VERIFIED_100K_SALES`

개발사·배급사·플랫폼의 first-party 발표가 paid copies/units sold >= 100,000을 명시한 경우에만 사용한다.

### `ESTIMATED_100K_PLUS`

SteamDB, VGI, Sensor Tower 등 제3자 model이 100,000+를 추정했지만 first-party units/downloads 발표가 없는 경우다. estimate methodology, checked_at, platform, confidence/range를 함께 기록한다.

### `NOT_100K_VERIFIED`

wishlists/reviews/CCU/revenue/rank 같은 다른 지표는 높더라도 download/install 또는 paid sales 100K가 확인되지 않은 상태다.

**100K downloads != 100K paid sales**이며, revenue·wishlists·reviews·followers·CCU 역시 어느 쪽의 대체 지표도 아니다.

## 11. 검증된 10만+ seed examples

아래 사례는 **threshold membership을 확인하는 seed**다. 해당 게임의 특정 기능이 성공을 만들었다는 causal proof가 아니다.

| Game | Platform/source | checked_at | 확인된 threshold | label |
|---|---|---:|---:|---|
| Shattered Pixel Dungeon | Google Play public store | 2026-08-12 | 5M+ downloads | `VERIFIED_100K_DOWNLOAD_INSTALL` |
| Mindustry | Google Play public store | 2026-08-12 | 5M+ downloads | `VERIFIED_100K_DOWNLOAD_INSTALL` |
| Slice & Dice | Google Play public store | 2026-08-12 | 1M+ downloads | `VERIFIED_100K_DOWNLOAD_INSTALL` |
| Sledding Game | Steam developer community announcement | 2026-08-12 | 100,000 copies sold in 5 days | `VERIFIED_100K_SALES` |
| God Of Weapons | Steam developer community announcement | 2026-08-12 | over 100,000 copies sold in 2 weeks | `VERIFIED_100K_SALES` |
| Astrea: Six-Sided Oracles | Steam developer community announcement | 2026-08-12 | over 100,000 copies sold within 4 months | `VERIFIED_100K_SALES` |

이 표에서 확인한 것은 **공개된 숫자와 metric 종류**뿐이다. 그 숫자의 원인을 설명하려면 별도의 플레이어 반응·제품 비교·현업/개발자 설명·실패/혼합 사례가 필요하다.

## 12. Success / comparison card

성공작·경쟁작·인접작은 기능 목록이 아니라 다음 카드로 비교한다.

```yaml
game:
source_and_checked_at:
success_evidence_label: VERIFIED_100K_DOWNLOAD_INSTALL | VERIFIED_100K_SALES | ESTIMATED_100K_PLUS | NOT_100K_VERIFIED
threshold_evidence:
target_player:
core_action:
standard_genre_promise:
observable_twist:
why_player_notices_it_in_30_seconds:
repeated_decision_changed:
store_capsule_or_trailer_legibility:
player_positive_negative_mixed_evidence:
production_cost:
copy_risk:
our_transferable_principle:
do_not_copy:
project_kick_candidate:
validation:
```

성공작을 조사할 때도 기존 비교 구성의 **실패·혼합 반응 사례**를 제거하지 않는다. survivorship bias를 줄이기 위해 같은 장르의 실패/혼합 사례에서 “같은 표현이 왜 먹히지 않았는가”를 함께 본다.

## 13. 개성(킥) 추출법

여기서 **킥(kick)**은 단순히 특이한 기능 하나가 아니라, 플레이어가 빠르게 알아차리고 반복 행동·기대에 영향을 주며 store/trailer/demo에서도 설명 가능한 **뾰족한 차별화 가설**이다.

### 13.1 Kick ladder

```text
market table-stakes
→ 플레이어가 반복하는 core action
→ 그 행동에서 기대하는 tension / power fantasy / mastery
→ 한눈에 보이는 observable twist
→ 한 문장 / 한 GIF / 한 screenshot으로 설명 가능한가
→ 반복 decision을 실제로 바꾸는가
→ 1인/소규모 제작 범위에서 감당 가능한가
→ prototype 또는 store-page comprehension test
```

좋은 후보는 아래 다섯 축 중 최소 세 축에서 근거가 있어야 한다.

- `PLAYER_NOTICEABLE` — 디자인 설명 없이도 플레이어가 빠르게 알아챈다.
- `LOOP_RELEVANT` — lore/cosmetic만이 아니라 반복 플레이의 행동·판단에 영향을 준다.
- `MARKET_LEGIBLE` — capsule, screenshot, trailer, GIF, 짧은 pitch에서 전달된다.
- `PRODUCTION_FIT` — 현재 인력·기간·플랫폼·콘텐츠 예산으로 유지 가능하다.
- `NON_DERIVATIVE` — 경쟁작의 식별 가능한 UI/art/캐릭터/문구/구현을 복제하지 않고 원리를 변형한다.

### 13.2 Table-stakes와 킥을 분리한다

```text
장르 기본 기대를 충족하는 기능
→ TABLE_STAKES

기본 기대를 깨거나 재조합해 반복 선택을 달라지게 하는 표현
→ KICK_CANDIDATE
```

“다른 성공작에도 있다”는 이유만으로 킥이 아니다. 반대로 너무 독특해서 설명·제작·반복 플레이에 연결되지 않으면 market gimmick에 그칠 수 있다.

### 13.3 검증

킥 후보는 다음 중 가장 작은 증거로 시작한다.

```text
one-sentence comprehension
→ 1 screenshot / GIF comparison
→ Figma/FigJam concept board when visual comparison helps
→ paper prototype / rule simulation
→ playable PoC
→ store-page or trailer comprehension
→ player behavior + self-report
```

성공작의 milestone은 **causal attribution**을 제공하지 않는다. `100K+ 성공작이 이 기능을 가졌다 → 이 기능이 성공 원인이다`라는 추론은 금지한다. 우리 프로젝트에서는 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 변환하고, 가능하면 작은 PoC와 실제 플레이어 증거로 반증한다.

## 14. 시장조사 적대적 검토

다음을 발견하면 결론을 낮추거나 다시 조사한다.

- downloads와 paid sales를 합쳐 “다운로드”로 보고함.
- estimated owners/units를 verified sales로 표현함.
- revenue, wishlists, reviews, followers, CCU를 unit sales로 변환함.
- 성공작만 모으고 failure/mixed comparison을 제거함.
- 판매 milestone 이후 기능을 보며 post-hoc causal story를 만듦.
- review 수·평점·viral popularity를 품질 authority로 사용함.
- 경쟁작의 식별 가능한 UI/art/signature execution을 복제함.
- market-data provider의 추정치를 source date/method 없이 영구 사실로 고정함.
- 시장 trend가 현재 프로젝트의 core fun보다 우선함.

## 추가 시장조사 출발점

- SteamDB FAQ: https://steamdb.info/faq/
- GameDiscoverCo: https://gamediscover.co/
- Sensor Tower Game IQ: https://sensortower.com/product/mobile-app/game-iq
- Video Game Insights sales methodology: https://app.sensortower.com/vgi/insights/article/steam-sales-estimation-methodology-and-accuracy/
- Google Play public store pages: https://play.google.com/store/games
- Steam community announcements: https://store.steampowered.com/news/
