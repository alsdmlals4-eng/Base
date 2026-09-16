# 사용자 제공 TRPG 룰북 코퍼스 — 2026-08-24 1차 분석

```yaml
case_role: user-provided-trpg-rulebook-corpus-observation
status: PARTIAL_CORPUS_PASS
owner_reference: docs/knowledge/game-development/TRPG_RULE_DESIGN_REFERENCE_RADAR.md
observed_at: 2026-08-24
source_container: user-provided ZIP
copyright_boundary: summaries-and-structure-only
project_canon_authority: none
```

## 1. 목적

사용자가 직접 제공한 룰북 ZIP을 `TRPG_RULE_DESIGN_REFERENCE_RADAR.md`의 공통 분석 카드에 맞춰 비교한다. 원문 룰북·번역문·표·고유 데이터는 Base에 복제하지 않고 다음만 남긴다.

- 어떤 플레이 경험을 전제로 하는가
- 핵심 판정·캐릭터·갈등을 어떤 구조로 푸는가
- 룰북이 어떤 순서로 독자를 가르치는가
- 예시·시트·플레이세트·서머리 등 support artifact를 어떻게 분리하는가
- 프로젝트에 옮길 수 있는 원리와 실패 조건

이 문서는 현재 ZIP의 **최상위 PDF 33개를 식별하고 첫 10~12페이지/목차 중심으로 분류한 1차 pass**다. 긴 코어 룰북은 후속 pass에서 `첫 등장 → 첫 예시 → 심화 → 플레이 중 참조` 위치를 더 추적해야 한다.

## 2. 코퍼스 성격 분류

| 자료군 | 대표 자료 | 설명 구조에서 볼 것 |
|---|---|---|
| Full/Core Rulebook | Maid RPG, D&D 3.5 PHB, Harry Potter RPG, GURPS, Heroine Crisis | 장기 참조성과 신규 학습 순서가 어떻게 타협되는가 |
| Lite/Quickstart | GURPS 경량판, CoC 간편 입문, Shadowrun Quickstart, Never Going Home Basic Training | 무엇을 버리고 첫 세션에 필요한 것만 남기는가 |
| Player Guide | ZombieLine Player's Guide | 세계관→캐릭터→플레이 절차를 플레이어 책임만으로 자르는 방식 |
| SRD/Reference | Pathfinder 2 SRD | teaching보다 검색성·정확한 분류를 우선하는 구조 |
| Summary/Aid | D&D 핸드아웃, 팀 셜록 룰서머리 | 실제 플레이 중 lookup 비용을 줄이는 법 |
| Character/Play Sheet | 천하제일문 시트, 파라노이아 캐매 | 캐릭터 작성 과정 자체를 UI/대화로 가르치는 방식 |
| Playset/Scenario Aid | 용잡이들(피아스코), 고대해 플레이세트, 강호행 | 코어 룰을 반복하지 않고 장르·역할·갈등만 제공하는 방식 |
| Setting/Worldbook | 별의 바다 | 설정을 고정 데이터가 아니라 질문·플레이 생성 장치로 제시하는 방식 |
| Supplement/Data Book | Monster Codex | 규칙보다 데이터 반복형 Reference의 분리 방식 |

## 3. 룰북별 1차 관찰

### 3.1 이모크로어 룰북(통합본)

**설명 순서:** 세계와 괴이의 한 줄 정체성 → TRPG란 무엇인가 → 참가자 역할 → 준비물 → 플레이어 섹션 → 딜러 상세.

**풀어낸 방식:** 먼저 감정과 괴이라는 게임의 정체성을 설명하고, 플레이어가 당장 알아야 할 것과 딜러가 알아야 할 상세 규칙을 분리한다. 신규 플레이어에게 “딜러 섹션을 전부 읽을 필요가 없다”고 명시해 progressive disclosure를 강하게 사용한다.

**일반화:** `PLAYER_FIRST_PROGRESSIVE_DISCLOSURE` — PL에게 필요한 최소 규칙을 먼저 주고 GM/정밀 규칙을 뒤로 보낸다.

### 3.2 Dungeon World 2 Final Alpha

**설명 순서:** 소개/게임이 무엇인가 → Getting Started/Playing the Game → Safety/Session Zero → Character Creation → 클래스 → Advancements → Conflicts → Relationships 등.

**풀어낸 방식:** 캐릭터 수치보다 먼저 “이 게임이 어떤 판타지를 다루며 대화가 어떻게 규칙으로 이어지는가”를 설명한다. 안전도구와 세션 제로를 캐릭터 생성보다 앞에 둬 테이블 합의 자체를 플레이 전 규칙으로 취급한다.

**일반화:** `TABLE_CONSENSUS_BEFORE_BUILD` — 자유도와 공동 창작 비중이 높을수록 tone/safety/expectation을 캐릭터 생성 전에 닫는다.

### 3.3 크툴루의 부름 간편 입문 가이드

**설명 순서:** 게임 소개와 장르 약속 → 플레이 방법/기본 규칙 → 캐릭터 작성과 판정 → 실제로 바로 플레이 가능한 입문 시나리오.

**풀어낸 방식:** 전체 코어 룰을 축약하는 대신 “평범한 사람이 미지의 공포를 조사한다”는 플레이 약속을 먼저 주고, 즉시 필요한 BRP 핵심만 설명한 뒤 시나리오로 이전한다.

**일반화:** `QUICKSTART_RULE_TO_SCENARIO_TRANSFER` — 설명이 끝나는 지점을 룰 숙지가 아니라 실제 시나리오 시작으로 잡는다.

### 3.4 GURPS 경량판 1.2

**설명 순서:** GURPS란? → 용어집 → 기본 룰 → 캐릭터 포인트/특성치 → 사회적 배경/장단점/기능 → 장비 → 플레이 진행 → 신체/정신 활동 → 전투 → 부상·피로.

**풀어낸 방식:** 범용 시스템의 거대한 선택지를 그대로 보여주지 않고 기본 룰과 캐릭터 구성요소를 먼저 정의한 다음 세부 행동군을 단계적으로 붙인다. 목차 자체가 Reference index 역할을 강하게 한다.

**일반화:** `GENERIC_ENGINE_NEEDS_EARLY_VOCABULARY` — 범용 룰은 설정보다 공통 용어와 캐릭터 구성 단위를 먼저 고정해야 뒤의 모듈을 읽을 수 있다.

### 3.5 Shadowrun Sixth World Quickstart 번역

**설명 순서:** 소개 → 퀵스타트 룰 → 게임의 리듬 → 판정/액션 → 전투와 장비/매트릭스·마법 등 대표 subsystem → 샘플 캐릭터/시나리오 계열.

**풀어낸 방식:** 복잡한 원 시스템을 모두 설명하지 않고 “게임의 리듬”을 먼저 제시해 여러 subsystem이 언제 나타나는지 문맥을 준다. 번역자는 역주를 시각적으로 분리해 원문 규칙과 해설 권위를 구분한다.

**일반화:** `COMPLEX_SYSTEM_TEACH_THE_RHYTHM_FIRST`, `COMMENTARY_MUST_NOT_MASQUERADE_AS_RULE`.

### 3.6 Maid RPG Core Rulebook

**설명 순서:** Introduction → Core Rules → Character Creation → Action Resolution/Combat → Stress/Favor → NPC/Random Event → 이후 장르별 데이터·시나리오 도구.

**풀어낸 방식:** 매우 강한 장르 판타지를 먼저 제시하고, 캐릭터 생성에서 그 판타지를 랜덤 표와 개성 데이터로 바로 구현한다. 이후 행동 해결과 자원 루프를 설명해 “캐릭터가 먼저 재미를 보이고 규칙은 뒤에서 받치는” 구조다.

**일반화:** `HIGH_CONCEPT_CHARACTER_FIRST` — 캐릭터 생성 자체가 판매 포인트인 게임은 코어 수학보다 캐릭터 결과물을 먼저 보여주는 편이 진입 동기를 만든다.

### 3.7 RWBY RPG 팬 룰

**설명 순서:** Introduction → Basics → Rule of Cool → Playing the Game → Base Attributes → Derived Statistics → Semblance → Weapon Design → Modifications.

**풀어낸 방식:** 수치보다 먼저 “Rule of Cool”을 명시해 판정 해석의 미학적 기준을 제공한다. 원작 판타지에서 중요한 Semblance와 무기 설계를 캐릭터 기초 능력 직후 배치한다.

**일반화:** `AESTHETIC_RULE_BEFORE_BUILD_OPTIONS` — 자유작성 능력이 많을수록 무엇이 “좋은 플레이”인지 미학/톤 원칙을 수치 규칙 전에 선언할 가치가 있다.

### 3.8 Never Going Home — Basic Training

**설명 방식:** 짧은 신병 훈련 교범 형식을 통해 세계/역할과 +One 시스템의 최소 규칙을 빠르게 주입한다.

**풀어낸 방식:** 룰북 외부의 군사 교범이라는 fiction과 실제 튜토리얼 문서 형식을 일치시켜 설명 자체를 세계 체험으로 만든다.

**일반화:** `DIEGETIC_ONBOARDING_WHEN_CHEAP` — 장르와 잘 맞을 때 설명 문서의 화자·형식도 세계관 몰입 장치가 될 수 있다. 단, 검색성을 희생하면 안 된다.

### 3.9 ZombieLine Player's Guide

**설명 순서:** 세계관 → 샘플 캐릭터 시트 → 캐릭터 제작 → 시트 읽는 법 → 추천 제작법 → 실제 플레이의 사건/진행.

**풀어낸 방식:** 빈 규칙부터 설명하지 않고 **완성된 시트를 먼저 보여준 뒤** 각 칸을 어떻게 만드는지 역으로 설명한다. 신규 플레이어가 최종 결과물을 알고 생성 절차를 따라가게 한다.

**일반화:** `SHOW_FINISHED_ARTIFACT_BEFORE_FORM_FILLING` — 캐릭터 시트가 복잡할수록 완성 예시를 먼저 보여주면 각 필드의 목적을 이해하기 쉽다.

### 3.10 Pathfinder 2 SRD

**설명 순서:** 소개 → 선조/배경 → 클래스 → 기술 → 특기 → 장비 → 주문 → 게임 플레이/변형 → 제작/보물 → 부록.

**풀어낸 방식:** 신규 학습서라기보다 규칙 자료망을 체계적으로 찾게 하는 Reference다. 캐릭터를 구성하는 데이터 taxonomy가 플레이 절차보다 앞선다.

**일반화:** `SRD_IS_REFERENCE_NOT_TUTORIAL` — 데이터 정본의 최적 순서를 사람용 첫 학습 순서로 그대로 복사하지 않는다.

### 3.11 Heroine Crisis Advanced

**설명 순서:** 개요 → 세계관 → 캐릭터 메이킹 → 특징/마법/Crisis 계열/아이템 데이터 → 플레이 진행 → 판정과 전투 → 성장 → 몬스터 작성 → 옵션 룰 → 시트.

**풀어낸 방식:** 장르와 캐릭터 옵션을 먼저 충분히 보여주고 실제 플레이/판정은 뒤에 둔다. 이는 빌드 선택 자체가 핵심 매력인 데이터 중심 게임의 전형적인 “캐릭터 카탈로그 우선” 구조다.

**일반화:** `CATALOG_FIRST_HAS_MOTIVATION_BUT_HIGH_ONBOARDING_COST` — 선택 구경은 재미있지만 초심자는 규칙이 무엇을 의미하는지 모른 채 긴 카탈로그를 읽게 될 위험이 있다.

### 3.12 Harry Potter RPG Core Rule Book

**설명 순서:** 소개/롤플레잉이란 → 캐릭터 제작과 성장 → 자질 → 혈통 → 기숙사 → 기술 → 장단점 → 능력 → 코어 판정/시간/전투 → 마법 → 장비/서비스 → 퀴디치 → 부록.

**풀어낸 방식:** 원작 팬이 먼저 원하는 “나는 어떤 마법사인가”를 캐릭터 파트에서 오래 다룬 뒤 범용 CODA 판정 엔진을 후반에 배치한다.

**일반화:** 강한 IP/세계 판타지에서는 `IDENTITY_BEFORE_ENGINE`이 진입 동기를 만들 수 있으나, 실제 플레이 시작까지 필요한 읽기량이 길어지는 trade-off가 있다.

### 3.13 Himekishi

**설명 순서:** 시작하며 → 세계관 → 룰(캐릭터 작성 → 판정 → 전투 → 결과) → 데이터(적/고유 요소) → 시나리오.

**풀어낸 방식:** 매우 압축된 소형 룰북의 전형으로, 세계관을 짧게 주고 “만들기→굴리기→싸우기→끝내기”의 사용 순서대로 설명한다.

**일반화:** `SMALL_RULEBOOK_FOLLOW_SESSION_DEPENDENCY_ORDER`.

### 3.14 D&D 계열 — PHB / Basic / 초보자 가이드 / 핸드아웃

**관찰:** 같은 시스템도 목적에 따라 설명 순서가 크게 다르다.

- PHB: 능력치 → 종족 → 클래스 → 세부 캐릭터 데이터 → 모험/전투/마법 같은 대형 taxonomy.
- Basic: 세계·게임 사용법 → 캐릭터/기본 규칙 → 모험 → 전투 → 마법 등 핵심만 축약.
- 초보자 가이드: DM/Player 같은 용어와 실제 플레이의 의미부터 설명.
- 핸드아웃: 판정 공식·능력치 역할 같은 lookup 정보만 압축.

**일반화:** `ONE_SYSTEM_NEEDS_MULTIPLE_INFORMATION_SURFACES` — 코어 룰북 하나로 tutorial/reference/table aid를 동시에 해결하려 하지 않는다.

### 3.15 CoC 팬 종합 자료 vs 공식 간편 입문

**관찰:** 팬 종합본은 자료 출처·해석·세계관 설명을 넓게 모으는 archive 성격이 강하고, 공식 Quickstart는 첫 게임으로 이전하는 데 집중한다.

**일반화:** `COLLECTION_IS_NOT_ONBOARDING` — 정보량과 친절함은 같은 것이 아니다. 입문 문서에는 버리는 판단이 필요하다.

### 3.16 팀 셜록 룰서머리

**설명 방식:** 세계관 소개와 근미래 생활상 같은 fiction context를 먼저 주고 플레이에 필요한 규칙만 요약한다.

**일반화:** 사건/추리 게임은 수치보다 “이 세계에서 상식적으로 가능한 것”을 먼저 맞추면 판정 분쟁을 줄일 수 있다.

### 3.17 전광세계 배스천랜드 샘플 페이지

**설명 방식:** 캐릭터 생성 결과를 극도로 빠르게 내고, 빚·탐험 같은 캠페인 동기를 캐릭터 규칙과 바로 연결한다.

**일반화:** `CHARACTER_CREATION_SHOULD_CREATE_A_REASON_TO_PLAY` — 수치 작성만 끝나지 않고 첫 세션 목표가 함께 생기게 한다.

### 3.18 별의 바다 월드북

**설명 방식:** 일반적인 세계관 백과를 제공하기보다 Dungeon World의 공동 설정 생성 원칙을 보존하기 위해 고정 설정을 줄이고 질문/생성 재료를 제공한다.

**일반화:** `SETTING_REFERENCE_CAN_PRESERVE_BLANK_SPACE` — 공동창작 게임의 세계관 문서는 빈칸을 결함이 아니라 플레이 공간으로 설계할 수 있다.

### 3.19 용잡이들(피아스코) / 고대해 플레이세트 / 강호행

**설명 방식:** 코어 판정 규칙을 반복하지 않고 관계·역할·갈등·장면 씨앗을 제공한다. 플레이세트는 “룰 위에서 돌아가는 콘텐츠 데이터”다.

**일반화:** `CONTENT_PACK_SHOULD_NOT_DUPLICATE_ENGINE` — 시나리오/플레이세트는 엔진 설명 대신 이번 세션의 선택과 갈등을 만드는 정보에 집중한다.

### 3.20 파라노이아 캐매

**설명 방식:** 완성된 설명문보다 실제 캐릭터 메이킹 대화/로그 자체가 절차 예시 역할을 한다.

**일반화:** `REPLAY_CAN_TEACH_SOCIAL_PROCEDURE` — 규칙이 협상·질문·GM 판정에 의존할수록 실제 대화 예시가 정적 규칙 설명보다 효과적일 수 있다.

## 4. 나머지 최상위 PDF의 현재 분류

| 자료 | 현재 분류 | 후속 상세 분석 포인트 |
|---|---|---|
| 3.5 초보자 가이드 | tutorial | 용어→플레이 예시→전투/주문의 teaching transfer |
| D&D 3.5 Player's Handbook | full core | taxonomy-first 장기 Reference |
| D&D 핸드아웃 | player aid | 한 장 lookup 밀도 |
| Dungeon Master's Guide | GM reference | 세계 구축→모험 설계→운영/보상 분리 |
| Fallout PnP 2.01 Kor | full fan core | 세계 소개와 규칙 규모의 균형 |
| Monster Codex | supplement/data | 반복 데이터와 encounter example 결합 |
| Orientation | compact custom rules | 맵 없는 카드 기반 룰의 최소 설명 순서 |
| the mage 번역본 | class/playbook | 직업 한 장 안의 fiction→수치→move 구조 |
| 강호행 - 양상군자 | scenario sheet | 경쟁시계와 장면 전개의 정보 압축 |
| 고대해 플레이세트 | playset | 인쇄/접기 artifact가 캐릭터 선택 UI가 되는 방식 |
| 너냐 F | compact party RPG | 목표/톤을 첫 페이지에서 강하게 고정하는 방식 |
| 댄디 베이직 | core/basic | 모험→전투→마법 계층과 신규 입문 구조 |
| 섀도런 퀵스타트 | quickstart | subsystem 복잡도 축약 방식 |
| 천하제일문 시트 | campaign sheet | 문파 성장·자산을 시트 자체로 표현 |
| 패스파인더2 SRD | SRD | 검색 taxonomy와 tutorial 분리 |
| gurps (1) | full core scan | 텍스트 추출 불가/별도 page inspection 필요 |

## 5. 코퍼스에서 반복된 설명 패턴

### 5.1 설명 순서는 크게 4계열로 나뉜다

1. **Promise → Flow → Character → Rule**: Quickstart/PbtA 계열. 첫 플레이 전환이 빠르다.
2. **Promise → Character Fantasy → Rule**: Maid/RWBY/IP 팬룰. 캐릭터 만들기 자체가 매력일 때 강하다.
3. **Vocabulary/Taxonomy → Character Data → Play**: GURPS/PF/D&D 대형 코어. 검색성과 완전성이 강하지만 입문 비용이 높다.
4. **Finished Artifact → How to Fill It**: ZombieLine/시트 중심 자료. 복잡한 양식을 배울 때 유효하다.

한 프로젝트의 모든 문서를 하나의 순서로 통일할 이유는 없다.

### 5.2 좋은 룰북은 '본문' 외의 표면을 사용한다

반복 관찰된 표면:

- Quickstart
- 캐릭터/직업 시트
- GM aid
- 룰 서머리
- 전투/사건/광기/관계 시트
- 플레이세트
- 리플레이
- 샘플 캐릭터
- 데이터 카탈로그/SRD

따라서 `RULEBOOK_IS_NOT_THE_ONLY_INTERFACE`를 강하게 지지한다.

### 5.3 첫 예시는 두 종류가 필요하다

- **완성 결과 예시**: 캐릭터 시트·스킬·장면이 최종적으로 어떻게 보이는지.
- **절차 예시**: 선언→판정→결과→후속 장면이 어떻게 이어지는지.

둘 중 하나만 있으면 “무엇을 만들어야 하는지” 또는 “어떻게 쓰는지”가 빠진다.

### 5.4 자유작성 규칙은 미학·권한·제한을 함께 가르쳐야 한다

RWBY의 Rule of Cool, Dungeon World의 fiction trigger, 자유형 설정 문서의 blank space처럼 자연어 자유도가 커질수록 단순한 숫자 밸런스표보다 다음이 중요해진다.

```text
무엇이 이 게임다운가
→ 어떤 fictional permission이 생기는가
→ 언제 판정하는가
→ 어떤 범위까지 한 규칙이 책임지는가
→ 어떤 비용/대가/반례가 있는가
```

## 6. 현재 이클립스 설계에 대한 transfer hypothesis

프로젝트 정본이 아니라 후속 플레이테스트용 가설이다.

### ADOPT 후보

- Player Promise와 5분 흐름을 상세 데이터보다 앞에 둔다.
- PL/GM/Reference를 분리한다.
- 완성 캐릭터 시트를 생성법보다 먼저 한 번 보여준다.
- 룰북·퀵스타트·캐릭터 시트·룰 서머리를 서로 다른 정보 표면으로 취급한다.
- 면모/자유작성 스킬은 fictional permission과 기계 효과를 분리한다.

### ADAPT 후보

- Dungeon World식 fiction-first를 그대로 Move 목록으로 복사하지 않고 `의도→방법→불확실할 때만 판정→결과가 fiction 변경`으로 축약한다.
- GURPS/PF식 카탈로그 완전성은 숨김 데이터/Reference에만 적용하고 첫 학습 문서에는 최소 규칙만 노출한다.
- 강한 장르 문서의 diegetic voice는 세계관 소개/예시에만 사용하고 규칙 Reference 문장은 중립적으로 유지한다.

### AVOID 후보

- 캐릭터 옵션 카탈로그 수십 페이지를 기본 판정 이해보다 먼저 읽게 하는 구조.
- 공식 규칙과 번역자/GM 해설을 같은 시각 위계로 섞는 것.
- SRD taxonomy를 그대로 초보자 teaching order로 사용하는 것.
- 모든 룰과 모든 데이터와 모든 예시를 하나의 장문 탭에 유지하는 것.

## 7. 후속 분석 우선순위

1. 긴 코어 룰북 8종에서 핵심 판정의 `첫 등장→첫 예시→심화→reference` 위치 추적.
2. ZIP 내부 nested 자료인 더블크로스/시노비가미/던전월드 HWP·시트 자료 분석.
3. 플레이 중 support artifact를 `상태 소유자 / 공개 범위 / 갱신 주체 / lookup 빈도`로 비교.
4. 외부 공개 Source(Fate, Dungeon World, GUMSHOE, Blades, 13th Age, Freeform Universal 등)와 같은 Schema로 교차 비교.
5. 이클립스 룰북의 teaching order를 최소 3안으로 비교하고 첫 세션 플레이테스트로 결정.

## 8. 권리·증거 한계

- 이 코퍼스에는 상용/팬 번역/비공식 정리/공개판/샘플이 섞여 있다.
- Base는 제목과 구조적 관찰만 저장하며 원문 문구·수치표·고유 데이터의 재배포를 하지 않는다.
- 팬 번역의 정확성·배포 권리는 공식 원출처와 동일하지 않다.
- ZIP 보유 사실은 상업적 재사용 권리를 의미하지 않는다.
- 현재 pass는 일부 대형 PDF의 앞부분/목차 중심이다. 전체 규칙 세부를 모두 검증했다고 주장하지 않는다.
