# 서사·세계관·캐릭터 전문 Source Radar

```yaml
radar_role: narrative-world-character-specialty-source-extension
status: ACTIVE_DISCOVERY_EXTENSION
parent_radar: docs/knowledge/game-development/PERIODIC_SPECIALTY_SOURCE_RADAR.md
owner_policy: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
scheduler_authority: EXTERNAL_TO_BASE
new_active_skill: false
independent_ledger: false
candidate_count_limit: NONE
capture_all_material_candidates: true
minimum_candidate_quota: NONE
forced_filler_candidates: false
```

## 1. 목적과 권위 경계

이 문서는 소설·게임·세계관·캐릭터·관계·장르·현실 고증·현지화·추리·중국 무협·서브컬처를 조사할 때 사용할 전문 Source와 적용 Gate를 정리한다.

이 문서는 두 번째 Watchlist가 아니다. Source role·Evidence tier·원출처 역추적·scan 상태·영구 승격·Ledger·scheduler는 기존 Watchlist와 Evidence Method가 소유한다. 실제 기획·집필·구현·검증은 기존 Skill·Method·Guide와 각 프로젝트 정본이 소유한다.

외부 자료는 다음을 대신하지 않는다.

- 프로젝트의 확정 세계관·인물·관계·사건·무공·문파·해답·단서·밈 사용 결정
- 실제 원고·대사·코드·데이터·씬·자산
- 실제 독자·플레이어 관찰·인터뷰·플레이테스트
- 저작권·상표·계약·문화적 민감성에 대한 개별 검토

```text
현재 질문·실패 증상·바뀔 결정
→ 정확한 시대·지역·언어·매체·장르·플랫폼·대상 독자/플레이어
→ 공식·원자료 / 학술·현업 / 발견 자료 / 실제 반응 분리
→ 원출처·날짜·버전·표본·상업 이해관계·권리
→ 현재 Base owner·프로젝트 consumer·정본 충돌
→ 반례·실패·소수 관점
→ 가장 작은 validation artifact
→ ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID | BLOCKED_UNVERIFIED
```

## 2. 후보 수와 Candidate Packet

유용한 후보를 임의 상한 때문에 누락하지 않는다. 실제로 관련성이 있는 후보는 수에 관계없이 기록할 수 있다. 반대로 숫자를 채우기 위한 후보는 만들지 않는다.

```yaml
candidate_count_limit: NONE
capture_all_material_candidates: true
minimum_candidate_quota: NONE
forced_filler_candidates: false
```

모든 후보는 최소 다음을 가진다.

```yaml
candidate_id:
source_domain:
current_question_or_failure:
project_scope:
source_name:
source_role: AUTHORITY_TARGET | PROFESSIONAL_PRACTICE | DISCOVERY_FEED | OBSERVATIONAL_DATA_OR_VENDOR_GUIDE
original_url:
published_or_updated_at:
checked_at:
exact_era_region_language_medium_version:
target_reader_or_player:
sample_or_method:
commercial_or_creator_interest:
claim_or_practice:
original_source_backtrace:
current_base_owner:
current_project_consumer:
project_canon_conflict:
rights_or_representation_risk:
failure_or_counterevidence:
validation_artifact:
rollback_or_discard_condition:
disposition: ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID | IGNORE | BLOCKED_UNVERIFIED | PROMOTION_CANDIDATE
```

현재 consumer·검증·폐기 조건을 특정할 수 없으면 채택하지 않고 `REFERENCE_ONLY` 또는 `BLOCKED_UNVERIFIED`로 남긴다. 후보가 없으면 억지로 만들지 않고 `NO_CHANGE`로 닫는다.

## 3. `WORLD_LORE_AND_SETTING_RESEARCH`

세계관은 고유명사와 설정량이 아니라 인물의 선택·생활·갈등·위험·기회를 만드는 조건으로 조사한다.

### 조사 축

```text
지리·기후·생태·자원·이동
역사·연표·세대 기억·공식 기록과 민간 기억
문화·종교·의례·금기·가족·호칭·음식·의복
국가·법·행정·군사·종교기관·길드·범죄조직
생산·소유·희소성·노동·가격·물류·주거·위생·여가
기술·마법·괴이의 가능 범위·비용·위험·접근 권한
도구·가구·문서·무기·건축·교통 등 물질문화
평범한 사람이 거대한 설정을 하루 일과에서 체감하는 방식
```

### Source

| Source | role | use | claim ceiling |
|---|---|---|---|
| **Library of Congress** | `AUTHORITY_TARGET` + `DISCOVERY_FEED` | `https://www.loc.gov/collections/` — 지도·사진·신문·문서·녹음·시대별 물질문화 원자료 발견 | 소장 자료의 제작 맥락·권리·누락을 항목별 확인 |
| **Smithsonian Open Access** | `AUTHORITY_TARGET` + `DISCOVERY_FEED` | `https://www.si.edu/openaccess` — 박물관 사물·이미지·3D·기술·생활 자료 | CC0 표시가 없는 항목, 제3자 권리, 문화적으로 민감한 자료는 별도 검토 |
| **UNESCO Intangible Cultural Heritage** | `AUTHORITY_TARGET` | `https://ich.unesco.org/` — 공동체가 전승하는 의례·기술·생활 지식과 safeguarding 자료 | 등재 설명을 고정된 민족 특성이나 판타지 장식 목록으로 복제하지 않음 |
| **국가·지역별 도서관·박물관·기록원·공식 통계** | `AUTHORITY_TARGET` | 대상 시대·지역의 법령·관보·지도·가격·직업·도구·구술사 | 한 국가·시대 자료를 다른 지역·계층에 자동 일반화하지 않음 |
| **학술 논문·전문 역사서·고고학·인류학 연구** | `PROFESSIONAL_PRACTICE` | 원자료의 해석·논쟁·방법·반례 | 한 학설이나 대중적 통설을 확정 사실로 만들지 않음 |

### 검증 Artifact

```yaml
world_promise:
research_question:
era_region_class_scope:
source_conflicts:
everyday_life_proof:
institution_and_resource_flow:
material_culture_reference:
scene_or_system_consumer:
canon_decision_required:
```

설정은 최소 한 장면·선택·시스템·환경·대사에서 관찰 가능해야 한다. 사용되지 않는 백과사전 항목은 현재 제작 범위에 흡수하지 않는다.

## 4. `CHARACTER_CAST_AND_RELATIONSHIP_DESIGN`

캐릭터는 유형표가 아니라 서로 다른 주의·가치·선택·해결법·대가·관계 변화로 구분한다.

### 조사 축

```yaml
identity_and_role:
public_role_and_private_self:
core_desire_and_actual_need:
fear_and_avoidance:
formative_experience:
belief_value_and_self_deception:
contradiction:
moral_boundary:
attention_filter:
decision_rule:
problem_solving_method:
competence_and_limitation:
cost_of_strength:
failure_pattern:
voice_thought_and_body_language:
social_mask:
relationship_power_debt_dependency:
cast_function:
arc_start_pressure_choice_consequence:
signature_scene_proof:
visual_identity:
```

### Source

| Source | role | use | claim ceiling |
|---|---|---|---|
| **Writers Guild Foundation Library** | `PROFESSIONAL_PRACTICE` | `https://www.wgfoundation.org/library` — 실제 제작된 Script·Outline·Pitch·Show Bible과 초안 변화 연구 | 현장 열람·권리·기증 조건을 지키며 구조와 기능만 참고 |
| **O*NET** | `AUTHORITY_TARGET` | `https://www.onetcenter.org/overview.html` — 미국 직업의 실제 과업·기술·지식·작업 맥락 출발점 | 미국 현재 노동시장 자료이며 시대·국가·조직별 현장 차이를 별도 확인 |
| **NIMH** | `AUTHORITY_TARGET` | `https://www.nimh.nih.gov/health/topics` — 정신건강 관련 공식 정보와 연구 출발점 | 진단명을 성격·폭력성·악역성의 약칭으로 사용하지 않음 |
| **전문 직업 인터뷰·구술사·회고록·현장 관찰** | `PROFESSIONAL_PRACTICE` | 직업 언어·절차·감정 노동·조직 관계 | 한 사람의 경험을 직업 전체로 일반화하지 않음 |
| **실제 독자·플레이어 관찰** | `T3/T4 project evidence` | 인물 구분·욕망 이해·선택 인과·관계 기억·호감과 불편의 원인 | 인기 투표만으로 캐릭터 구조의 인과를 확정하지 않음 |

### 반과장 Gate

```text
MBTI / 에니어그램 / 별자리 / 혈액형 != 완성된 성격
정신건강 진단 != 악역·위험성·기행의 약칭
직업명 != 실제 능력·일과·계층·조직 경험
설정상 강함 != 장면 안의 강함 증거
비극적 과거 != 자동 깊이
유명 캐릭터의 인기 != 식별 가능한 성격·관계·외형 복제 권한
```

기존 consumer:

- `developing-and-revising-serial-fiction`
- `skills/developing-and-revising-serial-fiction/references/character-distinctiveness-and-opponent-threat.md`
- `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- `docs/knowledge/methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md`

## 5. `STORY_ARCHITECTURE_GENRE_AND_SERIALIZATION`

### 조사 축

```text
Reader Promise·장르 약속·주요 질문
Story Engine·장기 Arc·회차 Arc·장면 변화
갈등·stakes·정보 공개·미스터리 질문
setup·recall·recontextualize·payoff·aftermath
반복 구조의 변주·Open Loop·Local Payoff
엔딩·후일담·다음 시즌/후속작 연결
선형 소설·연재·게임·웹툰·영상의 각색 경계
```

Source는 기존 `Reedsy`, `Writing Excuses`, `Scriptnotes`, GDC narrative, IGDA Game Writing, Emily Short, ink, Yarn Spinner와 **Writers Guild Foundation Library**를 함께 사용한다.

```text
three-act / hero's journey / beat sheet / 장르 공식
!= 모든 작품과 매체의 필수 구조

회차 조회·댓글·판매 성과
!= 특정 장면·구조 선택의 단독 인과
```

실제 consumer는 프로젝트 원고·게임 빌드·독자/플레이어 evidence다. 구조 프레임워크는 `ADAPT` 또는 `TEST`로만 들어간다.

## 6. `REAL_WORLD_DOMAIN_RESEARCH_AND_FACT_CHECKING`

프로젝트 질문에 맞는 분야별 1차 Source를 동적으로 선택한다.

| 분야 | 우선 Source 예시 | 필수 범위 |
|---|---|---|
| 역사·행정·법 | 정부·국가기록원·법령·관보·공식 통계·원문 | 국가·시대·관할·효력일 |
| 의료·정신건강 | 공공보건기관·전문학회·peer-reviewed 연구 | 응급/일상·지역·현재 지침·표현 위험 |
| 군사·수사·재난 | 공식 교범·보고서·전문 기관·사후 분석 | 조직·시대·법적 권한·기밀/안전 경계 |
| 직업·산업 | O*NET, 직업별 공식 표준·전문 협회·현장 인터뷰 | 실제 과업·도구·교육·조직·지역 차이 |
| 건축·교통·생태·경제 | 규격·공공기관·학술 연구·현장 데이터 | 단위·기후·지역·기간·표본 |

```yaml
domain_question:
jurisdiction_or_region:
era_or_effective_date:
primary_authority:
professional_interpretation:
known_disagreement:
fictionalization_boundary:
safety_or_legal_boundary:
scene_system_or_data_consumer:
```

외부 자료가 불완전하면 합리적으로 보이는 사실을 꾸미지 않고 `BLOCKED_UNVERIFIED`로 남긴다.

## 7. `CULTURE_REPRESENTATION_AND_SENSITIVITY`

### 대상

```text
문화·민족·지역·종교·의례
성별·성정체성·연령·계층
장애·정신건강·질병·중독
전쟁·학살·식민지·재난·이주
성폭력·가정폭력·학대·자살·자해·범죄 피해
```

### 검토 순서

```text
공식·원자료와 연구
→ 대상 시대·지역·집단 안의 다양성
→ 당사자·전문가의 복수 관점
→ 작품에서 해당 특성의 기능
→ agency·일상성·관계·선택
→ 고정관념·낙인·자극적 소비·권력 비대칭
→ 실제 독자·플레이어 또는 적절한 reviewer 검토
```

하나의 당사자 의견도 전체 집단의 정답이 아니다. 당사자 검토가 필요한 고위험 표현을 AI 추론이나 체크리스트만으로 통과시키지 않는다.

```text
사실 정확성 != 존중되는 표현
선한 의도 != 영향 검증
피해 묘사 강도 != 서사 깊이
문화적 요소 존재 != 살아 있는 문화 이해
```

## 8. `LANGUAGE_NAMING_LOCALIZATION_AND_CULTURALIZATION`

| Source | role | use | claim ceiling |
|---|---|---|---|
| **Unicode CLDR** | `AUTHORITY_TARGET` | `https://cldr.unicode.org/` — 언어·지역별 숫자·날짜·시간·화폐·단위·정렬·Person Name 데이터 | Locale Data가 자연스러운 캐릭터 이름·대사·문화 표현을 자동 생성하지 않음 |
| **W3C Internationalization** | `AUTHORITY_TARGET` | `https://www.w3.org/International/` — UTF-8·언어 선언·bidirectional text·현지화 가능한 Web 구조·문화 편향 질문 | 웹 구현 지침을 Godot·소설의 전체 현지화 workflow로 그대로 강제하지 않음 |
| **국립국어원과 대상 언어의 공식 사전·표기 기관** | `AUTHORITY_TARGET` | 표기·맞춤법·발음·로마자·용례 | 언어 규범 != 인물 voice·문학적 완성도 |
| **전문 번역가·현지화 담당자·대상 문화 reviewer** | `PROFESSIONAL_PRACTICE` | 호칭·농담·금기·UI 길이·음성·문화화 | 한 번역가의 선택을 모든 지역의 보편 정답으로 만들지 않음 |

### 필수 항목

```text
이름 구조·성/이름 순서·호칭·존대·성별·복수
고유명사 Glossary·보존어·번역어·발음표
문장 길이·줄바꿈·RTL·폰트 Coverage
숫자·날짜·시간·화폐·단위·정렬·검색
밈·농담·상징·색·제스처의 지역별 의미
대사·자막·음성·UI·데이터 ID의 분리
```

하나의 `first_name / last_name` 구조나 한국어 어순을 전 언어에 강제하지 않는다.

## 9. `MYSTERY_CLUE_AND_FAIRNESS_RESEARCH`

추리 공정성은 “정답 단서가 어딘가에 있다”만으로 성립하지 않는다. 논리·발견 가능성·해석 가능성·대안 가설·막힘 회복을 분리한다.

### Source

| Source | role | use | claim ceiling |
|---|---|---|---|
| **Game Developer — The Case of the Golden Idol** | `PROFESSIONAL_PRACTICE` | `https://www.gamedeveloper.com/design/case-of-the-golden-idol` — 이미 답을 아는 제작자의 난이도 판단 한계, 반복 플레이테스트, 정보량·오답 피드백·다중 추론 경로 | 한 게임의 입력 방식과 힌트 수준을 보편 공식으로 만들지 않음 |
| **Game Developer — Return of the Obra Dinn** | `PROFESSIONAL_PRACTICE` | `https://www.gamedeveloper.com/design/for-lucas-pope-i-return-of-the-obra-dinn-i-was-a-bunch-of-appealing-design-problems` — 인물 식별 단서·환경·규모·서사 제약의 동시 설계 | 시각 스타일이나 대규모 인물 수를 복제하지 않음 |
| **Detection Club fair-play rules — historical reference** | `PROFESSIONAL_PRACTICE` | 황금기 탐정소설의 독자-작가 공정성 논쟁과 장르 역사 질문 | historical fair-play code != universal genre law |
| **실제 unknown-player 관찰** | `T3 project evidence` | 무엇을 발견·기억·오해·추론했고 어디서 멈췄는지 기록 | 만족도 설문만으로 논리·발견성 문제를 특정하지 않음 |

### Mystery Evidence Packet

```yaml
truth_model:
question_answer_matrix:
clue_inventory:
clue_timing:
clue_discoverability:
clue_interpretation:
alternative_hypotheses:
redundancy_and_independent_paths:
red_herring_causality:
hint_ladder:
failure_and_recovery_path:
solution_uniqueness_or_accepted_range:
input_expression_boundary:
unknown_player_observation:
revision_and_retest:
```

### 공정성 Gate

```text
clue logic != clue discoverability
fair != easy
author self-test != unknown-player evidence
pixel hunt != deduction
red herring != 무관한 거짓 정보
힌트 제공 != 정답 대리 수행
복수 단서 != 같은 단서를 다른 문장으로 반복
오답 피드백 != 정답 위치 누설
```

검수 질문:

1. 정답을 모르는 사람이 핵심 단서를 실제로 찾을 수 있는가?
2. 찾은 단서가 현재 언어·UI·시각 규모에서 해석 가능한가?
3. 대안 가설을 어떤 증거로 제거하는가?
4. 단서 하나를 놓쳐도 독립 경로나 회복 수단이 있는가?
5. Red herring은 세계·인물·사건 인과에 속하는가?
6. 막힘을 완화하면서 Aha와 선택권을 보존하는가?
7. 결론 입력 방식이 추론보다 문구 맞히기·Brute force를 시험하지 않는가?

기존 consumer:

- `analyzing-and-refining-game-concepts`
- `docs/CONTENT_DESIGN_METHOD.md`
- `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- 프로젝트의 사건·단서·힌트·실패 기록 데이터와 플레이테스트

## 10. `MARTIAL_ARTS_WUXIA_AND_JIANGHU_RESEARCH`

무술·무림·중국 무협은 다음 층을 섞지 않는다.

```text
역사 기록과 물질문화
살아 있는 전승·공동체·사제 관계
현대 경기 규칙과 채점
현대 건강·연행·교육 실천
무협문학의 장르 관습
홍콩·중화권 영화의 편집·와이어·액션 문법
프로젝트의 허구 무공·강호·게임 시스템
```

### Source

| Source | role | use | claim ceiling |
|---|---|---|---|
| **Martial Arts Studies** | `PROFESSIONAL_PRACTICE` | `https://www.martialartsstudies.org/journal` — 무술의 역사·사회·문화·미디어·정체성에 대한 학제 연구 | 개별 논문 하나를 실전성·역사 전체의 결론으로 사용하지 않음 |
| **International Wushu Federation** | `AUTHORITY_TARGET` | `https://www.iwuf.org/` — 현재 경기종목·기술 규정·채점·안전·대회 사실 | modern competition rules != historical combat |
| **UNESCO Taijiquan** | `AUTHORITY_TARGET` | `https://ich.unesco.org/en/RL/taijiquan-00424` — 공동체·전승·사제관계·다양한 실천의 living heritage 자료 | living heritage != fixed ancient form |
| **Chinese Text Project** | `AUTHORITY_TARGET` + `DISCOVERY_FEED` | `https://ctext.org/` — 중국 고전 원문·주석·전거 탐색 | 번역·OCR·AI 번역은 원문과 대조; 고전 문구의 후대 의미 변화를 별도 확인 |
| **China Biographical Database** | `AUTHORITY_TARGET` | `https://cbdb.hsites.harvard.edu/` — 역사 인물·관직·친족·사회관계·지명 연결 | 데이터 Coverage와 시대·신분 편향을 기록 |
| **China Historical GIS** | `AUTHORITY_TARGET` | `https://gis.harvard.edu/china-historical-gis` — 역사 지명·행정·이동·공간 맥락 | 지도 데이터가 실제 여행 시간·지형·사회적 접근성을 모두 증명하지 않음 |
| **Hong Kong Film Archive** | `AUTHORITY_TARGET` + `PROFESSIONAL_PRACTICE` | `https://www.filmarchive.gov.hk/` — 무협·검술영화의 작품·제작·복원·영화사 자료 | wuxia film choreography != safe real technique |
| **박물관·고고학·무기·의복·건축 원자료** | `AUTHORITY_TARGET` | 무기·복식·교통·도시·사찰·문서·생활 도구 | 시대·지역·계층을 혼합하지 않음 |

### Wuxia Research Packet

```yaml
era_region_dynasty_and_class:
historical_source_and_disagreement:
jianghu_institutions_and_state_law:
lineage_teacher_student_and_family:
economy_labor_travel_and_logistics:
weapon_clothing_architecture_and_material_culture:
martial_practice_layer: HISTORICAL | LIVING_HERITAGE | MODERN_SPORT | PERFORMANCE | FICTIONAL
wuxia_literary_convention:
film_choreography_and_editing_convention:
project_fictionalization:
safety_boundary:
culturalization_review:
scene_system_art_or_data_consumer:
```

### 반과장 Gate

```text
modern competition rules != historical combat
living heritage != fixed ancient form
wuxia film choreography != safe real technique
historical record != genre convention
genre convention != historical fact
무공 이름의 고전 한자 != 역사적 실재 증거
한 시대·지역·계층 != 단일한 중국·무림 문화
```

실제 위험한 무술 동작을 따라 하게 하는 실행 지침을 만들지 않는다. 게임 수치·판정·애니메이션은 역사적 사실과 별도의 프로젝트 설계로 검증한다.

## 11. `SUBCULTURE_MEME_AND_FANDOM_RESEARCH`

밈과 서브컬처는 짧은 문구나 이미지가 아니라 커뮤니티·플랫폼·시기·아이러니·권력관계에 따라 의미가 바뀌는 기호로 조사한다.

### Source

| Source | role | use | claim ceiling |
|---|---|---|---|
| **Fanlore** | `DISCOVERY_FEED` + `PROFESSIONAL_PRACTICE` | `https://fanlore.org/wiki/Fanlore:About` — 팬덤 용어·관행·사건·복수 관점과 원자료 링크 발견 | community wiki != canon; Fanlore는 단일한 객관 서술보다 복수 팬 관점을 보존함 |
| **Transformative Works and Cultures** | `PROFESSIONAL_PRACTICE` | `https://www.transformativeworks.org/our-projects/twc/` — 팬 연구·플랫폼·정체성·참여문화의 peer-reviewed 연구 발견 | 학술 분석 != 전체 팬덤의 현재 합의 |
| **Know Your Meme** | `DISCOVERY_FEED` | `https://knowyourmeme.com/` — 밈 명칭·기원 주장·확산 사례·변형 후보 발견 | 항목의 기원·작성·출처·현재 의미를 독립 확인 |
| **Google Trends** | `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE` | `https://trends.google.com/trends/` — 검색 관심의 시기·지역·비교 신호 | trend interest != positive sentiment or sales; 검색 관심은 절대 인구·전체 플랫폼 사용량이 아님 |
| **대상 플랫폼 공식 정책·공개 게시물·커뮤니티 표본** | `AUTHORITY_TARGET` + `T4 project evidence` | 현재 의미·허용 범위·사용 맥락·반응 확인 | 비공개 커뮤니티 무단 수집·개인 식별 발언 재배포 금지 |

### Meme Context Packet

```yaml
term_meme_or_trope:
earliest_trace_and_confidence:
source_community:
platform_region_language_and_date:
literal_and_current_meaning:
ironic_inversion_or_layered_use:
positive_neutral_negative_or_hostile_use:
inside_joke_entry_barrier:
associated_harassment_hate_or_extremist_signal:
rights_trademark_and_identifiable_execution:
trend_shape_and_durability:
target_audience_recognition:
project_transfer_value:
fallback_for_nonrecognition:
human_review_and_recheck_date:
```

### 반과장 Gate

```text
community wiki != canon
trend interest != positive sentiment or sales
viral != durable
one platform != target audience
literal meaning != current ironic meaning
meme recognition != permission to copy protected execution
팬덤 내부 사용 != 외부 사용자에게 안전·친절한 표현
```

유행을 따라가기 위해 프로젝트의 기본 Tone·세계관·캐릭터 voice를 훼손하지 않는다. 인식하지 못하는 사용자도 장면·UI·대사의 기본 의미를 이해할 수 있어야 한다.

## 12. 기존 Owner Routing

```text
소설·웹소설 집필·퇴고
→ developing-and-revising-serial-fiction
→ docs/knowledge/serial-fiction/**

장면·대사·관계·동적 서사
→ docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md

캐릭터 시각 설정·표정·실루엣·자산
→ docs/knowledge/methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md
→ docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md

게임 기획·추리·시스템·플레이테스트
→ analyzing-and-refining-game-concepts
→ docs/CONTENT_DESIGN_METHOD.md

정본·문서·결정·프로젝트 소비처
→ managing-design-documents
→ 프로젝트 GDD·Google Sheets·실제 데이터

사실·권리·표현·구현 증거
→ reviewing-and-validating-project-changes

실패 가정·과잉 일반화·반례
→ running-adversarial-review-and-refinement
```

새 책임 owner를 추가하지 않는다. 같은 문제를 기존 owner가 해결하면 새 Skill·Guide 대신 현재 계약과 Reference에 흡수한다.

## 13. Cadence와 종료 상태

- `event-or-on-demand`: 현재 프로젝트의 시대·문화·직업·추리·무협·현지화 결정 직전.
- `weekly`: 빠르게 변하는 플랫폼·밈·팬덤·정책·현재 작품 사례.
- `monthly`: 작법·장르·학술·Archive·박물관·영화·전문 연구.
- `quarterly`: Source 중복·stale·권리·소유자·실제 기여·표현 위험 감사.

Cadence는 후보 수 제한이 아니다. 관련성이 있는 후보는 모두 기록할 수 있으며, 관련 후보가 없으면 `NO_CHANGE`다.

```text
NO_CHANGE
EVIDENCE_ONLY_UPDATE
ABSORB_EXISTING_OWNER
PROJECT_ONLY
TEST
REFERENCE_ONLY
AVOID
PROMOTION_CANDIDATE
BLOCKED_UNVERIFIED
```

`PROMOTION_CANDIDATE`는 자동 승격이 아니다. 기존 Watchlist의 새 사이트 Gate, 반복 material value, 원출처, Existing Solution First, 적대적 검토, PR·exact-head 검증을 통과해야 한다.

## 14. 적대적 검토

- 현재 결정·consumer·validation 없는 링크 목록이 되었는가?
- 외부 설정·인물 해석이 프로젝트 정본에 검토 없이 반영됐는가?
- 성격 유형·진단·문화·직업이 캐릭터의 약칭이 되었는가?
- 소수 관점·시대·지역·계층 차이가 지워졌는가?
- 작가가 해답을 아는 상태의 자체 테스트만으로 추리 공정성을 주장했는가?
- 단서 논리와 발견 가능성, 힌트와 정답 대행, Red herring과 무관한 거짓 정보를 혼동했는가?
- 현대 경기무술·살아 있는 전승·역사 전투·무협문학·영화 안무를 한 층으로 섞었는가?
- 중국의 여러 시대·지역·계층을 하나의 고정된 무림으로 만들었는가?
- 밈의 기원·현재 의미·아이러니·유해 신호·권리를 분리했는가?
- Community Wiki·Google Trends·조회수를 Canon·호감·수요·판매 인과로 과장했는가?
- 특정 작품·작가·캐릭터·팬덤의 식별 가능한 실행을 복제했는가?
- 후보 수를 늘리는 일이 실제 프로젝트 가치보다 앞섰는가?

## 15. 완료 경계와 Rollback

이 Radar를 읽고 후보를 기록한 것만으로 세계관·캐릭터·소설·추리·무협·밈 적용이 검증된 것은 아니다. 완료는 해당 프로젝트의 실제 정본·원고·데이터·빌드·독자/플레이어 evidence와 기존 owner의 검증 계약을 따른다.

이 문서는 Runtime·Save/Data Schema·Skill Registry·프로젝트 정본·외부 dependency를 변경하지 않는다. 문제가 있으면 이 Radar와 연결 Hub·계약 테스트를 추가한 squash merge commit을 revert한다.
