# BCP-2026-030 — TTRPG 룰 설계·룰북 설명 구조 Reference Library

## 출처와 상태

- 출처 프로젝트: TRPG 룰 설계 조사 / 이클립스 TRPG 작업에서 파생된 공용 조사 필요
- 기준 Base 커밋: `7de18bc6a941b7be11e747f1cf59ae60cb3e4657`
- 조사일: `2026-08-24`
- 제출일: `2026-08-24`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `공식/공개 원출처 관찰 + 사용자 제공 seed source + 공용 분석 틀 제안`

## 관찰과 증거

TRPG 시스템을 새로 설계하거나 기존 룰북을 역기획할 때, 현재 Base의 범용 게임 벤치마킹 문서만으로도 조사 자체는 가능하지만 **TTRPG 고유 비교축**과 **룰북이 독자에게 규칙을 가르치는 순서**를 반복해서 다시 정의해야 한다.

이번 작업에서 사용자가 직접 제공한 seed source는 다음과 같다.

1. 도서출판 초여명: https://cympub.kr/
2. 던전월드 한국어 공개판: https://sites.google.com/view/dwtemporary/%ED%99%88?authuser=0
3. TRPG Club: https://www.trpgclub.com/
4. 초여명에서 공개한 Fate Core 시리즈 Dropbox 폴더: https://www.dropbox.com/scl/fo/ujjpyxy96tem420xotrpy/AKPLR0cPK7cifVgK5mTdYh8?rlkey=05ohszhw1foeoyvib0etc95qd&st=b25ypv0k&e=1&dl=0
5. Adventure Keeper Naver Blog: https://blog.naver.com/adventurekeeper

확인 상태:

- 초여명 홈페이지는 2023-06-27 공지에서 Fate Core 시스템 시리즈 PDF 무료 공개와 위 Dropbox 링크를 안내한다. Dropbox 폴더 자체는 현재 fetch 환경에서 직접 열리지 않아 `OFFICIAL_LINK_VERIFIED / FOLDER_CONTENT_UNVERIFIED`로 둔다.
- 던전월드 한국어 공개판은 CC BY 3.0 공개판이며, 목차와 플레이 규칙·캐릭터·액션·GM·첫 세션·국면·세계·괴물·장비·커스텀 규칙까지 직접 확인 가능하다.
- TRPG Club은 시노비가미·인세인·둘이서 수사·마기카로기아·새비지 월드 등 여러 상용 룰북의 공식 소개와 자료실을 제공하며, 룰북 구성/역할 분리/플레이 경험을 비교하는 secondary/official-publisher evidence로 유용하다.
- Naver Adventure Keeper는 현재 robots 정책으로 본문을 읽을 수 없어 `USER_SEED / UNVERIFIED_CONTENT`로 보존하며 내용은 추정하지 않는다.

추가로 서로 다른 설계 전제를 비교하기 위해 다음 공개/공식 자료를 조사 대상으로 확장한다.

- Fate Core SRD: https://fate-srd.com/fate-core
- Blades in the Dark SRD: https://bladesinthedark.com/core-system
- Ironsworn 공식 Digital Edition: https://tomkinpress.com/products/ironsworn-digital-edition
- Cairn 2e SRD: https://cairnrpg.com/second-edition/
- Cypher System SRD: https://cyphersrd.quest/
- Year Zero Engine SRD: https://freeleaguepublishing.com/wp-content/uploads/2023/11/YZE-Standard-Reference-Document.pdf
- Mausritter SRD: https://mausritter.com/srd/
- Savage Worlds Test Drive: https://s3-us-west-2.amazonaws.com/peg-freebies/SWTestDriveTheWildHunt.pdf
- Freeform Universal: https://kschnee.xepher.net/rpg/resources/FreeformUniversalRPG.pdf
- Pathfinder 2e Rules / Archives of Nethys: https://2e.aonprd.com/Rules.aspx

관찰된 설계·설명 패턴:

- **Fate**: 캐릭터를 `aspects / skills / stunts`로 분리하고, 면모는 도움이 될 때 자원을 소비하고 곤란을 받아들일 때 자원을 회복하는 양방향 드라마 경제를 만든다. 룰북은 game creation → character creation → aspects/actions → conflict/long game/GM 순으로 확장하며, 캐릭터 생성 자체를 플레이로 본다.
- **Dungeon World**: 먼저 ‘게임은 대화’라는 사용 모델을 설명하고, fiction에서 조건이 성립하면 move가 발동되는 구조를 가르친다. 서문 → 플레이하는 법 → 플레이 예 → 캐릭터 → 액션 → 직업 → GM → 첫 세션 → 국면/세계/괴물 → 장비/커스텀 순서로 플레이 감각을 먼저 익히고 레퍼런스로 확장한다.
- **Shinobigami 공식 소개**: 인물의 서(캐릭터) → 이치의 서(규칙) → 기법의 서(데이터) → 길의 서(GM) → 세계의 서(설정)처럼 독자 역할별 책임을 명시적으로 분리한다.
- **Insane 공식 소개**: 전반부에 리플레이를 두고 후반부에 실제 규칙과 자료를 배치한다. ‘규칙을 읽기 전 플레이 감각을 먼저 보여주는 example-first teaching’ 사례다.
- **Blades in the Dark**: free play → score → downtime의 반복 루프와 position/effect, stress/resistance, flashback으로 계획 정체를 줄인다. 룰 설명도 플레이 phase와 판단 권한을 먼저 제시한다.
- **Ironsworn**: guided/co-op/solo를 같은 엔진으로 지원하며, move/progress/momentum/oracle과 플레이키트·1쪽 요약·세계 구축 워크북을 분리한다. 룰북 본문과 테이블 참조 도구를 분리하는 사례다.
- **Cairn/Mausritter**: fiction-first, 적은 능력치, 자동 명중 또는 최소 굴림, inventory/condition을 물리적 슬롯으로 통합하는 초경량 설계다. 플레이어 원칙과 GM 원칙을 룰보다 앞세워 판정 빈도를 줄인다.
- **Year Zero Engine**: 접근성, 빠른 판정, risk/reward를 엔진의 핵심 특성으로 먼저 선언한 뒤 core mechanic을 설명한다. 범용 엔진 문서는 ‘어떤 경험을 위해 이 규칙이 존재하는가’를 규칙보다 먼저 설명하는 좋은 사례다.
- **Cypher System**: 세 개의 stat, task difficulty, skill/asset/Effort로 거의 모든 상황을 하나의 난이도 축에 환원한다. 범용 시스템의 복잡도를 공통 판정 문법으로 흡수하는 사례다.
- **Pathfinder 2e**: 반대로 풍부한 선택지와 정밀한 규칙을 위해 단계식 캐릭터 생성과 상세 reference를 사용한다. 초경량 설계와 비교할 때 ‘선택지 수가 많을수록 절차·참조 장치가 얼마나 중요해지는가’를 보여주는 대비 사례다.

## 일반화 후보

새 실행 Skill을 만들지 않고 `docs/knowledge/game-development/` 아래에 **TTRPG 전용 Reference Library** 하나를 추가하고 기존 game-development knowledge hub에서 조건부로 라우팅한다.

각 룰북/시스템은 다음 공통 분석 카드로 기록한다.

```yaml
source:
source_type: FULL_RULEBOOK | SRD | QUICKSTART | OFFICIAL_OVERVIEW | COMMUNITY_GUIDE | USER_SEED
access_state: VERIFIED | PARTIAL | UNVERIFIED
rights_boundary:
player_promise:
core_loop:
resolution_grammar:
character_expression:
narrative_authority:
resource_economy:
conflict_or_combat:
gm_authority_and_procedure:
scenario_or_campaign_structure:
complexity_budget:
customization_or_hacking:
rulebook_teaching_order:
example_and_reference_strategy:
quick_reference_strategy:
what_problem_it_solves_well:
failure_or_tradeoff:
adopt:
adapt:
reject:
revalidation_trigger:
```

특히 `rulebook_teaching_order`는 단순 목차 복사가 아니라 아래를 구분한다.

```text
PLAYER_PROMISE
→ FIRST_PLAY_MENTAL_MODEL
→ CORE_RESOLUTION
→ CHARACTER_CREATION
→ SPECIAL_CASES / CONFLICT
→ GM PROCEDURE
→ SETTING / CONTENT DATA
→ ADVANCED / HACKING
→ QUICK REFERENCE
```

실제 룰북이 이 순서를 따르지 않더라도, **왜 해당 순서를 택했고 어떤 독자 부담을 줄이는지**까지 분석한다.

## 프로젝트 전용으로 남길 내용

Base에는 다음을 넣지 않는다.

- 이클립스 세계관의 고유 명칭·세력·수치·캐릭터 예시.
- 이클립스의 최종 판정식·스킬 수치·밸런스 결론.
- 사용자가 제공하는 저작권 룰북 원문/ZIP/PDF 자체.
- 상용 룰북의 장문 전재·표·데이터 복제.

프로젝트에서는 Base의 분석 틀을 사용해 실제 룰 후보를 선택하고, Base에는 **재사용 가능한 설계 원리와 출처 메타데이터만** 남긴다.

## 적용 조건과 비사용 조건

적용 조건:

- 새 TRPG 시스템·하우스룰·룰북 정보구조를 설계할 때.
- 여러 룰북의 장단점을 비교하고 규칙 자체와 설명 방식을 함께 역기획할 때.
- 캐릭터 자유도, 서사 권한, 전투 선택지, GM 부담, 학습 난이도를 같은 기준으로 비교해야 할 때.

비사용 조건:

- 단일 룰 질문에 답하는 데 전체 library가 필요하지 않은 경우.
- 저작권 자료의 원문 보관소 또는 복제본 저장소로 사용하지 않는다.
- 특정 프로젝트의 승인된 룰을 Base의 공용 정답으로 승격하지 않는다.

## 반례와 위험

### 최소 3안 비교

| 안 | 장점 | 위험/비용 | 판정 |
| --- | --- | --- | --- |
| A. 링크 목록만 Base에 저장 | 가장 작고 빠름 | 무엇을 배울지 매번 재분석, 접근 불가 링크가 섞이면 가치 급감 | `REJECT` |
| B. 새 TRPG 전용 Skill 신설 | 자동화·형식 강제 가능 | 기존 game-design/research Skill과 책임 중복, routing·유지비 증가 | `REJECT` |
| C. 기존 game-development hub 아래 Reference Library 추가 | 실행권한 중복 없이 분석 틀과 source pool 재사용, 프로젝트별 자유도 유지 | 문서가 커질 수 있어 source card를 간결하게 유지해야 함 | `ADOPT` |

위험:

1. 인기 시스템의 고유 규칙을 ‘보편 원칙’으로 과잉 일반화할 수 있다. 서로 다른 전제의 최소 3개 시스템 비교 뒤 shared invariant만 공용화한다.
2. 상용 룰북 소개 페이지는 실제 룰 전문이 아니므로 구조·기능을 단정하지 않는다. `OFFICIAL_OVERVIEW / PARTIAL`로 표시한다.
3. 접근 불가 링크는 검색 스니펫이나 기억으로 보충하지 않는다. URL과 미검증 상태만 보존한다.
4. 공개 SRD라도 라이선스 범위가 서로 다르다. Base는 원문 복제보다 관찰·링크·전이 가능한 원리 중심으로 기록한다.
5. 룰북의 설명 순서는 시스템 설계 자체와 별개다. `MECHANIC_DESIGN`과 `TEACHING_ARCHITECTURE`를 반드시 분리한다.

## 영향 범위와 검증

승인 구현 범위:

- `docs/knowledge/game-development/TTRPG_RULE_DESIGN_AND_RULEBOOK_REFERENCE_LIBRARY.md` 신규 생성.
- `docs/knowledge/game-development/README.md`에 TTRPG 설계/룰북 역기획 라우팅 1행 추가.
- 신규 Skill, 외부 dependency, scheduler, tool, project runtime 변경 없음.

검증:

1. 사용자 제공 5개 seed URL이 모두 library에 존재해야 한다.
2. 최소 10개의 추가 비교 source가 있어야 한다.
3. 각 검증 source는 source type/access state/핵심 특징/설명 순서/ADOPT-ADAPT-REJECT 중 최소 하나를 갖는다.
4. `UNVERIFIED` source의 내용을 추정하지 않는다.
5. 프로젝트 고유 세계관·수치가 공용 문서에 유입되지 않는다.
6. 기존 `REVERSE_ENGINEERING_REUSE_PIPELINE` 및 game-development hub와 실행 책임이 중복되지 않는다.

## 필요한 도구·파일·권한

- GitHub 문서와 공개 웹 조사만 사용.
- 신규 dependency: 없음.
- 추가 비용: 0.
- Base 정상 branch/PR/squash merge 경로만 사용. bypass/force push 없음.

## 승인과 구현

- 사용자 승인 근거: 2026-08-24 현재 대화에서 사용자가 **“base에 trpg 자료로 추가하고. 더 많은 링크를 찾아봐”**, 이어 **“여기도 잊지말고”**라며 5개 seed source를 재확인했고, **“작업계속진행”**이라고 명시했다.
- `approval_ref`: 본 제안의 이 절 + 2026-08-24 current-task user approval.
- 승인 범위: TTRPG 룰 설계·룰북 설명 구조의 공용 Reference Library와 game-development hub routing 추가.
- 승인 제외: 프로젝트별 룰 강제, 신규 Skill/Tool, 저작권 원문 저장, 접근 불가 자료 내용 추정.
- 롤백: 신규 Reference Library와 README routing 행만 되돌리면 된다.