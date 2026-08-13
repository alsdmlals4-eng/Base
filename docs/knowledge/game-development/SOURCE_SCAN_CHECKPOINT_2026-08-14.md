# Source Scan Checkpoint — 2026-08-14

```yaml
checkpoint_id: SOURCE_SCAN_CHECKPOINT_2026-08-14
status: MATERIAL_CANDIDATES_REVIEWED
scan_date: 2026-08-14
scan_window: 2025-08-01..2026-08-14
source_policy_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
operational_state_owner: docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json
consumer_radar: docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
new_active_skill: false
new_work_mode: false
new_ledger: false
auto_canon_write: false
candidate_count_limit: NONE
```

## 1. 목적과 사실 경계

이번 checkpoint는 세계관·캐릭터·서사·추리·중국 무협·서브컬처 Source Radar의 첫 증분 조사다. 기존 Source의 최근 글을 확인하고, 반복적으로 가치가 있을 신규 Source 사이트를 추가 탐색했다.

```text
사이트 등록 != 그 사이트의 모든 글 채택
Article abstract != 실제 프로젝트 검증
학술 분석 != 보편 설계 법칙
Archive capture != 현재 의미·현재 호감·현재 유행
Base 흡수 != 프로젝트 Canon 자동 변경
```

원문 전체를 확인하지 못했거나 abstract·공식 소개까지만 확인한 세부 주장은 `UNVERIFIED_DETAIL`로 남긴다. 실제 프로젝트 적용은 해당 owner와 실제 원고·데이터·빌드·unknown-player evidence를 요구한다.

## 2. 신규 Source 사이트 판정

| Source | role | cadence | 확인한 surface | 현재 가치 | claim ceiling | disposition |
|---|---|---|---|---|---|---|
| **DiGRA Digital Library** | `PROFESSIONAL_PRACTICE` | `monthly-or-on-demand` | `https://dl.digra.org/`의 2026 Proceedings, article metadata·abstract·license notice | onboarding·player expertise·narrative system·environmental inference 등 최신 게임 연구 후보 | conference paper 하나를 보편 규칙·프로젝트 검증·시장 성과로 만들지 않음 | `ADOPT_DURABLE_SOURCE` |
| **Game Studies** | `PROFESSIONAL_PRACTICE` | `quarterly-or-when-relevant` | `https://gamestudies.org/`의 2026 issue와 Archive/RSS | 게임 미학·문화·소통·서사·플레이 해석의 장기 peer-reviewed archive | 이론·비평 != 실제 player behavior·인과·매출·구현 검증 | `ADOPT_DURABLE_SOURCE` |
| **MCLC Resource Center** | `PROFESSIONAL_PRACTICE` + `DISCOVERY_FEED` | `monthly-or-on-demand` | `https://u.osu.edu/mclc/`의 web publications·review·bibliography·video lecture·2025/2026 글 | 현대·당대 중국 문학·영화/미디어·시각예술·대중문화·번역·서지의 전문 Source | 현대 중국 연구 != 중국 전체·모든 시대·무협/선협 Canon | `ADOPT_DURABLE_SOURCE` |
| **Library of Congress Web Cultures Web Archive** | `AUTHORITY_TARGET` + `DISCOVERY_FEED` | `quarterly-or-when-relevant` | `https://www.loc.gov/collections/web-cultures-web-archive/`, collection description, selected datasets, access guidance | meme·reaction GIF·emoji·fan fiction·creepypasta·digital vernacular의 보존 자료와 dataset 탐색 | archive capture != 현재 의미·호감·유행; capture lag·access·rights 기록 | `ADOPT_DURABLE_SOURCE` |
| **Data & Society** | `PROFESSIONAL_PRACTICE` | `monthly-or-on-demand` | `https://datasociety.net/`의 About, research themes, media manipulation archive | 플랫폼 incentive·정보 조작·거버넌스·사회기술적 harm·권력 질문 보강 | 미국 정책·정치·극단주의 맥락을 모든 팬덤·밈·지역으로 일반화하지 않음 | `ADOPT_DURABLE_SOURCE_CONDITIONAL` |

### Source 등록 조건

- 모든 Source는 실제 질문과 기존 owner가 있을 때만 읽는다.
- 신규 사이트 수를 목표로 채우지 않는다.
- 발견용 Source가 원출처를 대체하지 않는다.
- `ADOPT_DURABLE_SOURCE`는 자동 Evidence tier 상승이나 모든 글의 영구 채택이 아니다.
- 지속적 material value가 사라지면 cadence 하향·Archive·제거 후보로 재검토한다.

## 3. 최근 글 Candidate Packet

### CANDIDATE-2026-08-14-01 — 게임 숙련도와 Puzzle Onboarding

```yaml
source: DiGRA Digital Library
article: How General Game Expertise Shapes Player Experience and Problem-Solving Across Different Onboarding Approaches in a Puzzle Video Game
published_at: 2026-06-16
original_url: https://dl.digra.org/index.php/dl/article/view/2820
source_role: PROFESSIONAL_PRACTICE
sample_or_method: over 120 players; commercial puzzle game Baba is You; three onboarding conditions; self-reported weekly hours and years of play plus behavior data
claim_or_practice: 일반 게임 숙련도는 enjoyment·completed levels·exploratory tinkering과 관련되고 일부 효과는 onboarding condition에 따라 달라질 수 있음
current_base_owner: docs/knowledge/game-development/TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md
current_project_consumer: 실제 프로젝트 first-session tutorial·telemetry·novice/expert playtest
claim_ceiling: one game + self-report expertise + study sample != universal causal onboarding law
validation_artifact: prior_game_expertise·expertise_measure·novice_expert_segment·expertise_by_onboarding_interaction
rollback_or_discard_condition: 프로젝트에서 segment 차이가 재현되지 않거나 다른 변수가 더 강하면 project rule로 사용하지 않음
disposition: ADAPT | TEST
```

흡수: 완료율 평균 외에 prior expertise를 participant covariate/segment로 기록한다. 초보자와 숙련자의 탐색·힌트·독립 수행·전이를 분리한다.

### CANDIDATE-2026-08-14-02 — Holarchic Narrative

```yaml
source: DiGRA Digital Library
article: Aesthetics of Holarchic Narrative Design: Participatory Pleasures of Game Storyworlds
published_at: 2026-06-29
original_url: https://dl.digra.org/index.php/dl/article/view/3124
source_role: PROFESSIONAL_PRACTICE
claim_or_practice: notes·recordings·environmental details·short sub-stories 같은 선택적 조각이 독립적인 narrative experience이면서 공유 storyworld coherence에 기여하고, 탐색·pattern recognition·inference가 미학적 경험이 될 수 있음
current_base_owner: docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
current_project_consumer: mystery clue packet·environmental narrative·unknown-player observation
claim_ceiling: fragmentation != depth; interpretive labour != missing causal information; cited examples != copy target
validation_artifact: story_holon_local_coherence·shared_storyworld_contribution·fragment_inference_burden·optional_fragment_redundancy_and_recovery
rollback_or_discard_condition: unknown player가 조각 자체와 전체 인과를 복구하지 못하면 파편 수를 늘리지 않고 정보 구조를 재설계
disposition: ADAPT | TEST
```

### CANDIDATE-2026-08-14-03 — Cultivation Games와 Cosmotechnics

```yaml
source: Social Media + Society
article: Cultivation games and cosmotechnics: Reimagining Sinofuturism in Chinese cultivation narratives
first_online_at: 2025-08-04
issue_context: 2026
original_url: https://journals.sagepub.com/doi/10.1177/20594364251364733
source_role: PROFESSIONAL_PRACTICE
claim_or_practice: wuxia와 cultivation/xianxia 계열의 구분, 중국 우주론·기술 실천과 game mechanics의 관계를 질문하게 함
current_base_owner: docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
current_project_consumer: 무공·수련·경지·자원·우주론·세계 규칙을 가진 프로젝트 정본
claim_ceiling: 한 논문의 Sinofuturism/cosmotechnics 해석 != 모든 중국 게임·수련물의 단일 정의
validation_artifact: wuxia_xianxia_cultivation_boundary·cosmology_and_technical_practice·translation_and_cross_cultural_boundary
rollback_or_discard_condition: 장르 경계가 프로젝트 핵심 경험을 흐리거나 역사·종교를 장식으로 소비하면 PROJECT_ONLY 또는 AVOID
disposition: ADAPT
```

### CANDIDATE-2026-08-14-04 — Bilibili Graphicon의 Platform Stage

```yaml
source: Discourse & Communication
article: A discursive history of platform capitalism: Graphicon evolution and cultural negotiation on Bilibili
first_online_at: 2026-05-20
original_url: https://journals.sagepub.com/doi/10.1177/09579265261446648
source_role: PROFESSIONAL_PRACTICE
claim_or_practice: 14년 동안 graphicon이 platform commercialization·governance·community negotiation과 함께 여러 단계로 변한 사례
current_base_owner: docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
current_project_consumer: meme·sticker·emote·UI symbol·community communication·localization
claim_ceiling: Bilibili 한 플랫폼의 단계 != 모든 플랫폼·지역·팬덤의 동일 역사
validation_artifact: platform_commercialization_and_governance_stage·native_symbol_system_and_recontextualization
rollback_or_discard_condition: 현재 target community의 의미와 일치하지 않거나 nonrecognition fallback이 없으면 사용하지 않음
disposition: ADAPT
```

## 4. Reference-only 후보

| Candidate | Source | 현재 가치 | 제외/보류 이유 | disposition |
|---|---|---|---|---|
| `Close-Playing War Trauma: The Tension Between Agency and Inevitability in My Child Lebensborn and Bury Me, My Love` | DiGRA, 2026 | trauma·agency·inevitability 표현을 공격할 질문 | 특정 작품의 close reading이며 실제 대상 독자·당사자 검토를 대체하지 않음 | `REFERENCE_ONLY` |
| `Neighborhood Making of Story Games: Accessible Joy in Low-Tech Design` | DiGRA, 2026 | low-tech story game·지역 문화·접근 가능한 제작 질문 | 프로젝트 consumer와 실제 community partnership가 아직 없음 | `REFERENCE_ONLY` |
| `Black Myth: Wukong in Heteroglossia: Video Adaptations as Articulations and Remediated Fan Journalism` | Games and Culture, 2026 | transnational fan video·remediation·heteroglossia 분석 질문 | 작품·플랫폼·팬덤 고유 사례이며 마케팅/수요 인과로 사용할 수 없음 | `REFERENCE_ONLY` |
| Game Studies 2026 Issues | Game Studies | death, idleness, ideology, movement, representation 등 폭넓은 새 분석 | 현재 Base 결정과 직접 consumer가 없는 개별 논문은 링크 dump를 피하기 위해 즉시 흡수하지 않음 | `REFERENCE_ONLY_POOL` |

## 5. 적대적 검토 결과

- 신규 Source 수를 성과로 착각하지 않았는가? → 각 Source에 owner·cadence·claim ceiling·퇴출 조건을 요구했다.
- 제목·snippet만으로 기법을 확정했는가? → 공식 metadata·abstract·About/collection page에서 확인한 범위만 기록하고 상세 방법은 `UNVERIFIED_DETAIL`로 제한했다.
- 연구 하나를 Hard Rule로 만들었는가? → player expertise와 holarchic narrative는 `ADAPT | TEST`, 실제 프로젝트 재검증을 요구했다.
- 중국·무협을 단일화했는가? → wuxia/xianxia/cultivation, 역사/장르/우주론/게임 mechanics를 분리했다.
- Archive·platform research를 현재 밈의 정답으로 사용했는가? → capture lag·현재 의미·상업화/거버넌스 단계·target community 검증을 분리했다.
- 프로젝트 Canon을 변경했는가? → 변경하지 않았다.
- 새 Skill·새 Ledger·두 번째 Evidence owner를 만들었는가? → 만들지 않았다.

## 6. 흡수 판정

```text
ADAPT | TEST
- prior game expertise segmentation
- holarchic fragment local coherence/shared storyworld/inference/recovery

ADAPT
- wuxia/xianxia/cultivation + cosmology/mechanics boundary
- platform commercialization/governance + native symbol recontextualization

REFERENCE_ONLY
- war trauma close reading
- neighborhood cultural preservation
- Black Myth fan journalism
- current-decision consumer 없는 Game Studies individual articles
```

## 7. 운영 상태와 Rollback

이번 checkpoint는 실제 Source를 2026-08-14에 확인했다. `PERIODIC_SOURCE_OPERATIONS_LEDGER.json`에는 신규 durable Source의 첫 scan 상태와 material candidate 수만 기록할 수 있다. `last_base_contribution_at`과 contribution count는 이 변경이 실제 `main`에 병합되기 전에는 증가시키지 않는다.

Rollback은 이 checkpoint와 owner 보강을 포함한 eventual squash merge commit을 revert한다. 신규 Source의 Ledger entry를 함께 제거하고 Scheduled Queue Issue에 `DISABLED_BY_ROLLBACK`을 기록한다. Runtime·Save/Data Schema·Skill Registry·프로젝트 Canon·외부 dependency migration은 없다.
