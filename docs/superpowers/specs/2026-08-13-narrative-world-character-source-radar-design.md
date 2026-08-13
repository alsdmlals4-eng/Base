# 서사·세계관·캐릭터 전문 Source Radar 설계

```yaml
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: 2026-08-13 사용자 요청 — 권장안 B 승인, 추리·단서 공정성·중국 무협·서브컬처 밈 포함
baseline_main_sha: 23e418ec2e4a801c90aff85611f10a5ab062d53c
parent_radar: docs/knowledge/game-development/PERIODIC_SPECIALTY_SOURCE_RADAR.md
source_policy_owner: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
evidence_owner: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
new_active_skill: false
new_work_mode: false
scheduler_authority: EXTERNAL_TO_BASE
independent_ledger: false
candidate_count_limit: NONE
```

## 1. 문제

현재 Base에는 연재소설 집필·퇴고, POV·voice, 캐릭터 개성·상대 위상, 관계·대화, 캐릭터 시각 디자인 방법이 이미 있다. 그러나 외부 정보를 주기적으로 조사할 때 다음 분야의 Source가 작법 일반 항목에 섞여 있거나 전용 권위·검증 경계가 부족하다.

- 세계관·역사·문화·제도·생활·물질문화 조사
- 캐릭터 설정·인물군 기능·관계·직업·대표성 조사
- 장르·연재·장기 서사 구조
- 현실 전문분야 사실 확인
- 문화·정신건강·장애·계층 등 표현 위험
- 이름·호칭·언어·현지화·문화화
- 추리·단서·오답·힌트의 공정성
- 무술·무림·중국 무협의 역사·사회·영화 문법·현대 경기 규칙
- 서브컬처·팬덤·밈의 기원·확산·현재 의미·권리·안전

이들을 각각 새 Skill로 만들면 `developing-and-revising-serial-fiction`, `analyzing-and-refining-game-concepts`, `NARRATIVE_AND_RELATIONSHIP_METHOD`, `CHARACTER_AND_NARRATIVE_ART_METHOD`, 아트·검증 owner와 중복된다. 반대로 기존 317줄 상위 Radar에 전부 넣으면 문서가 비대해지고 프롬프트·Godot Source와 서사 Source가 한 파일에서 경쟁한다.

## 2. 채택 구조 — 권장안 B

```text
PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
= Source role·scan·승격·Ledger 정책 owner

PERIODIC_SPECIALTY_SOURCE_RADAR.md
= 전문 Radar 상위 진입점

NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md
= 서사·세계관·캐릭터 계열 Source·claim ceiling·consumer·검증·rollback

기존 Skill·Method·Guide·프로젝트 정본
= 실제 기획·집필·구현·검증 owner
```

새 하위 Radar는 두 번째 Watchlist, 실행 Skill, scheduler, 독립 Ledger, 자동 수집기, 자동 Canon 생성기가 아니다. 외부 Source는 프로젝트 정본·실제 원고·코드·씬·데이터·플레이테스트·독자 반응을 대체하지 않는다.

## 3. Domain

### `WORLD_LORE_AND_SETTING_RESEARCH`

지리·환경·생태·역사·연표·문화·종교·의례·제도·세력·경제·생활·기술·마법·물질문화를 조사한다. Archive·박물관·도서관·공식 역사 데이터와 공동체 기반 living heritage를 우선한다.

### `CHARACTER_CAST_AND_RELATIONSHIP_DESIGN`

욕망·필요·두려움·가치관·자기기만·모순·agency·능력과 비용·직업·사회적 위치·말투·몸짓·관계 권력·인물군 기능·변화 Arc를 조사한다. 성격 유형표나 진단명을 완성된 캐릭터로 사용하지 않는다.

### `STORY_ARCHITECTURE_GENRE_AND_SERIALIZATION`

Reader Promise·장르 약속·Story Engine·아크·회차·장면·setup/payoff·미스터리·반전·엔딩·각색 경계를 조사한다. 단일 구조 공식을 모든 매체에 강제하지 않는다.

### `REAL_WORLD_DOMAIN_RESEARCH_AND_FACT_CHECKING`

역사·법·행정·수사·군사·의료·직업·건축·생태·경제 등 프로젝트별 현실 전문분야의 1차 Source를 선택한다. 한 국가·시대·직업 자료를 다른 지역·시대에 자동 일반화하지 않는다.

### `CULTURE_REPRESENTATION_AND_SENSITIVITY`

문화·종교·장애·정신건강·성별·연령·계층·전쟁·폭력·질병·이주 등 표현 위험을 공식 정보, 연구, 당사자·전문가 관점, 실제 독자·플레이어 검토로 분리한다. 피해·진단·정체성을 악역 약칭이나 장식으로 쓰지 않는다.

### `LANGUAGE_NAMING_LOCALIZATION_AND_CULTURALIZATION`

이름 구조·호칭·존대·언어·문자 방향·고유명사·Glossary·현지화 데이터·문화적 상징·번역 가능성을 조사한다. 하나의 이름 필드·날짜 형식·어순을 전 언어에 강제하지 않는다.

### `MYSTERY_CLUE_AND_FAIRNESS_RESEARCH`

Truth model, question-answer matrix, clue inventory, 공개 시점, 발견 가능성, 의미 해석, 대안 가설, red herring의 인과, 단서 중복, hint ladder, 실패 복구, 해답 유일성, 실제 플레이어 추론을 조사한다.

```text
clue logic != clue discoverability
fair != easy
historical fair-play code != universal genre law
author self-test != unknown-player evidence
pixel hunt != deduction
```

### `MARTIAL_ARTS_WUXIA_AND_JIANGHU_RESEARCH`

역사적 무술·현대 경기무술·연행·사상·문파·사제관계·강호의 사회질서·신분·법·교통·경제·무기·의복·지리·무협문학·영화·액션 연출을 분리한다.

```text
modern competition rules != historical combat
living heritage != fixed ancient form
wuxia film choreography != safe real technique
historical record != genre convention
genre convention != historical fact
```

### `SUBCULTURE_MEME_AND_FANDOM_RESEARCH`

밈·속어·팬덤 관행·트로프·패러디·플랫폼별 의미·기원·확산·재맥락화·아이러니·부정적 신호·권리를 조사한다.

```text
community wiki != canon
trend interest != positive sentiment or sales
viral != durable
one platform != target audience
literal meaning != current ironic meaning
meme recognition != permission to copy protected execution
```

## 4. 후보 수 정책

유용한 후보가 충분한데 임의 상한 때문에 누락되는 일을 막기 위해 최소·최대 후보 수를 두지 않는다.

```yaml
candidate_count_limit: NONE
capture_all_material_candidates: true
minimum_candidate_quota: NONE
forced_filler_candidates: false
```

수량 제한을 없애는 것은 검증을 없애는 뜻이 아니다. 각 후보는 현재 문제·consumer·Source role·원출처·날짜·버전·지역·언어·표본·상업 이해관계·권리·표현 위험·반례·검증 artifact·폐기 조건·disposition을 가져야 한다.

후보가 많으면 모두 기록할 수 있지만, 현재 소비자와 검증 경로가 없으면 `REFERENCE_ONLY`, `PROJECT_ONLY`, `BLOCKED_UNVERIFIED`, `AVOID` 중 하나로 닫는다. 후보가 없으면 억지로 채우지 않고 `NO_CHANGE`로 닫는다.

## 5. 기존 consumer

- 소설·웹소설: `developing-and-revising-serial-fiction`, `docs/knowledge/serial-fiction/**`
- 장면·대화·관계·동적 서사: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- 캐릭터 시각 설계: `docs/knowledge/methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md`
- 게임 기획·추리·시스템: `analyzing-and-refining-game-concepts`, `docs/CONTENT_DESIGN_METHOD.md`
- 아트·세계 시각화: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- 정본·발행·결정: `managing-design-documents`, 프로젝트 GDD·Google Sheets
- 사실·권리·표현·구현 검증: `reviewing-and-validating-project-changes`
- 공격·반례·과잉 일반화: `running-adversarial-review-and-refinement`

작품 고유 인물·세계관·무공·문파·사건·밈 사용·해답·단서 배치·수치·실제 데이터는 프로젝트가 소유한다.

## 6. Source 유형

- 공식·원자료: 국가·국제기구·표준·도서관·박물관·Archive·원문·공식 데이터.
- 학술·전문: peer-reviewed 연구, 전문 학회·저널, 현업 postmortem·인터뷰.
- 발견 자료: Wiki·백과·큐레이션·팬 Archive·밈 DB·트렌드 도구.
- 실제 반응: 독자·플레이어 관찰·인터뷰·리뷰·커뮤니티 반응.

발견 자료는 원출처를 찾는 데 유용하지만 Canon·역사적 사실·시장 수요·전체 팬덤의 대표값이 아니다. 비공개 커뮤니티를 무단 수집하거나 식별 가능한 개인 발언을 재배포하지 않는다.

## 7. 검증과 테스트

기존 Evidence Knowledge Workflow가 실행하는 두 계약 파일을 확장한다.

- `tests/test_periodic_external_source_watchlist.py`: 하위 Radar 존재, 상위 권위 종속, 후보 수 무제한, 9개 Domain, claim ceiling, Source와 consumer.
- `tests/test_periodic_external_source_discovery_seeds.py`: 기존 Skill·Method·Guide routing, 새 ACTIVE Skill·Ledger·scheduler 부재.

Hub와 Serial Fiction Hub에서 하위 Radar를 한 단계로 찾을 수 있어야 한다. Workflow·Registry·ACTIVE Skill·Work Mode는 변경하지 않는다.

## 8. 적대적 검토

- 링크 수집이 현재 결정과 consumer 없는 목록으로 변했는가?
- 세계관 조사 결과가 프로젝트 Canon으로 자동 승격됐는가?
- 성격 유형·정신건강 진단·문화 정체성이 캐릭터 약칭이 되었는가?
- Detection Club 규칙을 모든 추리 장르의 법칙으로 만들었는가?
- 단서의 논리와 발견 가능성을 혼동했는가?
- 저자가 해답을 아는 상태의 자체 테스트만으로 공정성을 주장했는가?
- 현대 경기무술·영화 안무·무협 관습·역사적 실전을 섞었는가?
- 중국의 시대·지역·계층 차이를 하나의 고정된 무림 문화로 만들었는가?
- 밈의 기원·현재 의미·아이러니·혐오 신호·권리를 구분했는가?
- Community Wiki·Google Trends·조회수를 Canon·호감·수요·판매 인과로 과장했는가?
- 특정 작품·작가·팬덤의 식별 가능한 표현을 복제했는가?

## 9. 완료·롤백

완료는 RED→GREEN, Exact-head Actions, 적대적 검토, 열린 PR 경로 충돌 0, squash merge, 새 `main` readback과 post-merge CI를 요구한다. 로컬 DNS 차단으로 실행하지 못한 로컬 테스트는 `BLOCKED_ENVIRONMENT_DNS`로 남기며 Actions 결과로 위장하지 않는다.

롤백은 eventual squash merge commit 하나를 revert한다. Runtime·Save/Data Schema·Skill Registry·프로젝트 Canon·외부 dependency migration은 없다.
