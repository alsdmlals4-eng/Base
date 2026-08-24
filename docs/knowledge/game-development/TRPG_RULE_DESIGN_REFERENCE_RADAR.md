# TRPG 룰 설계·룰북 설명 구조 Reference Radar

```yaml
reference_role: trpg-rule-design-and-rulebook-pedagogy-radar
owner_method: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
benchmark_owner: docs/BENCHMARKING_REFERENCE_GUIDE.md
reuse_owner: docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md
checked_at: 2026-08-24
execution_authority: none
project_canon_authority: none
```

## 1. 목적과 권한

이 문서는 TRPG를 새로 만들거나 기존 룰을 크게 개조할 때 **서로 다른 룰 계열이 어떤 플레이 문제를 어떤 절차로 해결하는지**, 그리고 **룰북이 그 규칙을 어떤 순서와 밀도로 가르치는지** 비교하기 위한 조건부 Reference다.

이 문서는 새 Skill, 두 번째 Watchlist, 프로젝트 룰 정본이 아니다.

- 실행은 기존 `analyzing-and-refining-game-concepts`, research, validation, adversarial-review 책임을 사용한다.
- 프로젝트의 실제 판정식·능력치·세계관·스킬·수치는 프로젝트 정본과 플레이테스트가 소유한다.
- 외부 작품은 표면을 복제하지 않고 `문제 → 원리 → 적용 조건 → 실패 조건`으로 추상화한다.
- 공개 열람, 무료 PDF, Open SRD, 상용 제품은 **서로 다른 권리 상태**다. `FREE_PUBLICATION != OPEN_REUSE`를 기본값으로 둔다.
- 라이선스가 열려 있어도 상표·로고·아트·Product Identity·별도 번역물까지 같은 권리라고 가정하지 않는다.
- 직접 읽지 못한 링크는 `UNVERIFIED_DIRECT_ACCESS`로 남기고 제목·검색 스니펫만으로 세부 룰을 확정하지 않는다.

## 2. 먼저 결정할 질문

TRPG Source를 열기 전에 현재 결정 질문을 먼저 적는다.

```yaml
player_promise:
signature_experience:
core_loop:
character_fantasy:
fictional_permission_need:
resolution_need:
information_model:
conflict_model:
resource_pressure:
role_symmetry_or_asymmetry:
gm_preparation_target:
first_session_target_minutes:
reference_during_play_need:
campaign_growth_need:
complexity_budget:
rights_and_distribution_need:
```

Source 수 자체는 종료 조건이 아니다. 새 자료가 기존 사례와 다른 **판정 가족 / 정보 모델 / 캠페인 루프 / 교육 순서 / support artifact / 권리 모델**을 추가하거나 현재 결정을 바꿀 때만 frontier를 넓힌다.

## 3. 룰북·SRD 공통 분석 카드

사용자 제공 ZIP, 공개 룰북, SRD, Quickstart를 같은 축으로 분석한다.

```yaml
source_id:
system:
edition_or_version:
language:
source_type: FULL_RULEBOOK | SRD | QUICKSTART | PLAYER_AID | DESIGN_ARTICLE | VTT_GUIDE
source_tier:
verification_status:
license_or_usage:
rights_boundary:

core_player_promise:
signature_experience:
problem_solved:
mechanic_solution:
core_loop:
character_model:
freeform_elements:
freeform_bounds:
fictional_permission:
resolution_trigger:
resolution_model:
who_sets_stakes:
who_sets_risk:
who_sets_effect:
outcome_bands:
conflict_or_combat_model:
resource_economy:
core_information_policy:
gm_authority_and_procedure:
progression:

chapter_or_teaching_order: []
teach_first:
progressive_disclosure:
first_example_position:
example_and_reference_strategy:
support_artifacts:
gm_player_information_boundary:
cognitive_load_notes:

strengths:
failure_modes:
adopt:
adapt:
avoid_or_reject:
validation_needed:
recheck_condition:
```

### ZIP 원문 분석 추가 규칙

사용자가 보유 룰북 ZIP을 제공하면 파일별 요약으로 끝내지 않는다.

1. 파일명·판본·언어·출처·권리 메모를 먼저 기록한다.
2. 실제 목차 순서를 추출한다.
3. 핵심 개념마다 **첫 등장 → 첫 예시 → 심화 설명 → 플레이 중 Reference** 위치를 추적한다.
4. 핵심 규칙을 `해결하려는 플레이 문제 / 입력 / 상태 / 절차 / 출력 / 피드백 / 실패·복구`로 분해한다.
5. 캐릭터·GM·시나리오·카드·핸드아웃·전투·관계·단서 시트의 정보 소유 경계를 확인한다.
6. `ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY`로 판정한다.
7. 프로젝트 고유 사실과 Base 공용 원리를 분리한다.
8. 원문 파일 자체나 긴 저작권 텍스트를 Base에 재배포하지 않는다.

## 4. 룰북 설명 구조를 따로 보는 이유

좋은 데이터 Schema와 좋은 teaching order는 같은 것이 아니다.

`REFERENCE_SCHEMA_IS_NOT_TEACHING_ORDER`:

- 디자이너용 SRD는 모든 규칙을 정확히 찾는 데 최적화될 수 있다.
- 신규 플레이어용 룰북은 **왜 필요한 규칙인지 이해하는 순서**가 더 중요하다.
- 실제 세션용 요약·캐릭터 시트는 **검색과 즉시 처리**가 더 중요하다.
- 같은 규칙도 `룰북 / Quickstart / Player Aid / GM Aid`에서 서로 다른 순서와 밀도로 보여줄 수 있다.

### 기본 teaching-order 후보

아래는 강제 목차가 아니라 starting pattern이다.

```text
1. Player Promise
2. 30초 / 5분 Flow
3. 짧은 Play Example
4. Character Creation
5. Core Resolution
6. Character Truth / Fictional Permission
7. Special Abilities / Skills
8. Conflict / Harm / Recovery
9. Game-Specific Signature Loop
10. Advancement / Campaign Consequence
11. GM Procedure
12. Quickstart / Sample
13. Reference / Data
14. Support Artifacts
15. Advanced / Optional Modules
```

예외가 더 좋은 경우:

- 낯선 엔진은 `Core Flow → Character`가 더 낫다.
- 공포·관계처럼 감정 체험이 핵심이면 `Replay / Example → Rule`이 더 낫다.
- 자유 설정의 허용 범위가 중요한 게임은 `Setting Consensus → Character`가 더 낫다.
- 강한 클래스/직업 판타지가 진입 동력이면 `Character → Core Rule`을 앞당길 수 있다.

## 5. 반복 재사용할 설계 패턴

### 5.1 FICTIONAL_PERMISSION_BEFORE_MODIFIER — `ADOPT`

먼저 **이 캐릭터·장비·상황이 무엇을 할 수 있는가**를 정한 뒤 수치 보정을 적용한다.

- 장점: 자유작성 능력과 설정을 실제 게임 권한으로 만든다.
- 실패 조건: 넓게 쓴 자연어가 모든 전문영역을 먹어버리는 경우.
- 검증: 같은 컨셉을 좁게/넓게 쓴 두 캐릭터의 해결 범위가 공정한지 비교한다.

### 5.2 FICTION_FIRST_TRIGGER_CONTRACT — `ADAPT`

fiction-triggered system에서 허구의 선언이 규칙 발동 조건을 만족할 때만 판정하고 결과를 다시 허구에 반영한다.

```text
fiction
→ trigger/uncertainty
→ rule
→ consequence
→ changed fiction
```

Dungeon World/PbtA 계열의 강점이지만 모든 TRPG에 Move trigger를 강제하지 않는다.

### 5.3 CORE_INFORMATION_MUST_NOT_BE_SINGLE_ROLL_GATED — `ADOPT`

조사형 시나리오에서 진행에 필수인 핵심 정보를 단 한 번의 성공 굴림 뒤에 잠그지 않는다.

- 실패는 `정보 없음`보다 시간·위험·노출·불완전한 맥락·추가 비용으로 바꾼다.
- 재미를 단서의 존재 여부보다 해석·연결·선택으로 옮긴다.

### 5.4 RISK_AND_EFFECT_ARE_DISTINCT — `ADAPT`

'어렵다'를 하나의 난이도 숫자로만 처리하지 않고 필요하면 다음을 분리한다.

- **Risk**: 실패했을 때 얼마나 위험한가.
- **Effect**: 성공하면 목표에 얼마나 큰 영향을 주는가.

Blades식 Position/Effect를 그대로 복사할 필요는 없다. 보스, 거대 대상, 강한 사회적 권력처럼 `성공 가능성`과 `성과 크기`가 다른 문제에서 특히 유효하다.

### 5.5 SUPPORT_ARTIFACT_IS_PLAY_INTERFACE — `ADOPT`

플레이 중 반복 참조하거나 여러 사람이 상태를 갱신하는 정보는 룰북 본문만으로 관리하지 않는다.

후보:

- 캐릭터 시트
- 핵심 규칙 요약
- 비밀/핸드아웃
- 전투·추격·진척 시트
- 사건·단서 시트
- 관계·세력·거점 시트
- NPC/적 관리
- 카드·토큰·Clock

**분리 기준:** 실제 반복 상태·정보 권한·참조 마찰을 줄일 때만 별도 artifact를 만든다. 단순히 자료가 많다는 이유로 시트를 늘리지 않는다.

### 5.6 ROLE_ASYMMETRY_REQUIRES_RECIPROCAL_VALUE — `ADAPT`

탐정/조수처럼 역할 능력이 비대칭이어도 된다. 단, 각 역할이 서로 다른 방식으로 핵심 경험에 기여하고 보상을 받아야 한다.

- '한 명이 해결하고 다른 한 명은 구경'이면 실패.
- 정보·관계·위험 부담·결정 권한 중 하나 이상에서 상호의존이 보여야 한다.

### 5.7 COMPACT_CORE_OPTIONAL_MODULES — `ADOPT`

첫 세션에 필요한 core와 campaign/advanced option을 분리한다.

```text
Quickstart
→ Core
→ Reference
→ Optional / Advanced modules
```

범용 엔진의 모든 선택 규칙을 처음부터 읽게 하지 않는다.

### 5.8 PLAYER_POST_ROLL_AGENCY — `TEST`

Resistance, push, reroll처럼 결과를 본 뒤 자원을 써서 대가를 줄이거나 다시 시도할 권한을 줄 수 있다.

- 장점: 실패가 즉시 통제 상실로 느껴지는 문제를 줄인다.
- 위험: 자원 기대값을 잘못 잡으면 모든 실패를 상쇄한다.

### 5.9 PROGRESS_VISIBLE_AS_STATE — `ADAPT`

한 번의 굴림으로 끝나지 않는 목표를 Clock/track/체크박스로 가시화한다.

- 봉인 해제, 추적, 세력 계획, 대형 재난, 연구 등에 유효.
- 단순 HP 바의 다른 이름이 되지 않도록 **무엇이 진행되고 어떤 사건에서 변하는지**를 명시한다.

### 5.10 VTT_IS_PRESENTATION_AND_OPERATION_LAYER — `REFERENCE_ONLY`

Cocofolia, Roll20, Foundry 등 VTT/ORPG 자료를 볼 때 룰 엔진과 다음 UX를 분리한다.

- 장면 전환
- 캐릭터 표현
- BGM/효과음
- 공개/비공개 정보
- 채팅 로그
- 주사위/매크로 자동화
- 핸드아웃/이미지

VTT 기능이 편리하다는 이유로 해당 UI나 플랫폼을 프로젝트 룰의 정본으로 만들지 않는다.

## 6. 사용자 지정 한국어 Source

### KTRPG-CYMPUB-001 — 도서출판 초여명

```yaml
url: https://cympub.kr/
source_tier: T2_PROFESSIONAL_PRACTICE
verification_status: VERIFIED_SOURCE
rights_status: PER_ITEM_RECHECK_REQUIRED
use_for: 한국어 TRPG 출판·공개판·Quickstart/demo·디자인 담론 discovery
```

관찰:

- 초여명은 2023년 Fate Core System 시리즈 PDF 무료 공개 공지를 두었고, 2025-05-14에 현재 Dropbox 링크를 갱신했다.
- 2025년에는 일반 PDF 제공 정책 종료도 별도로 공지했다. 따라서 과거의 'PDF 제공'과 현재의 개별 무료 공개를 혼동하지 않는다.
- `무료 공개` 자체는 개별 번역·편집물의 변형/상업 이용 허가를 자동 의미하지 않는다.

**ADOPT:** 한국어 source discovery와 publisher provenance.

### KTRPG-DW-KO-001 — 던전월드 한국어 공개판

```yaml
url: https://sites.google.com/view/dwtemporary/
source_tier: T1_PRIMARY_OFFICIAL_TRANSLATION
verification_status: VERIFIED_SOURCE
rights_status: CC_BY_3_0_WITH_ATTRIBUTION
```

핵심 특징 / 해결 방식:

- 플레이를 먼저 **대화**로 정의한다.
- 허구에서 특정 조건이 성립하면 규칙이 개입하고, 결과가 다시 허구를 바꾼다.
- GM에게 강령·원칙·액션을 주어 GM 역할을 '무제한 재량'으로 두지 않는다.
- 캐릭터 생성도 참가자들이 서로 질문하며 세계를 세우는 플레이 절차로 다룬다.

설명 순서:

```text
서문
→ 플레이하는 법
→ 플레이의 예
→ 캐릭터 만들기
→ 액션
→ 직업
→ 마스터
→ 첫 세션
→ 국면 / 세계
→ 괴물 / 장비
→ 고급·변환·NPC Reference
```

교육상 강점:

- `개념 → 실제 대화 예 → 캐릭터 → 반복 규칙 → 역할별 상세 → 첫 세션 → Reference`.
- 플레이 키트와 캐릭터 시트에 필요한 규칙을 상당량 담아 플레이 중 책 검색을 줄이는 방향을 명시한다.
- '가르치기' 장에서는 첫 세션을 수정·재시작할 수 있는 학습 단계로 다룬다.

**ADOPT:** fiction-first loop, GM procedure, play example, player aid.

### KTRPG-CLUB-001 — TRPG Club

```yaml
url: https://www.trpgclub.com/
source_tier: T2_PUBLISHER_SUPPORT_MATERIAL
verification_status: VERIFIED_SOURCE
rights_status: REFERENCE_ONLY_UNLESS_FILE_LICENSE_SAYS_OTHERWISE
```

직접 확인 가능한 현재 카탈로그에는 시노비가미, 인세인, 둘이서 수사, 마기카로기아, 톱니바퀴탑의 탐공사, 스트라토 샤우트, 로그호라이즌 TRPG, 새비지월드 등 서로 다른 장르의 작품과 `통합 자료실`이 있다.

핵심 학습:

- 룰북만이 제품의 사용 인터페이스가 아니다.
- 캐릭터/비밀/시나리오/전투/관계/사건/요약 등 **반복 절차와 정보 권한에 맞는 artifact**를 분리하는 사례군으로 사용한다.
- 상용 작품의 고유 시트·문구·표는 복제하지 않고 정보 구조만 관찰한다.

#### 둘이서 수사 — `REFERENCE_ONLY / ADAPT`

- 탐정과 조수의 비대칭 역할을 장르 판타지로 사용한다.
- 사건 조사와 관계 변화를 별도 support artifact로 관리하는 사례.
- 적용 시 `ROLE_ASYMMETRY_REQUIRES_RECIPROCAL_VALUE`를 검증한다.

#### 시노비가미 — `REFERENCE_ONLY / ADAPT`

공개 설명/자료 구조에서 읽을 수 있는 teaching pattern:

```text
캐릭터
→ 실제 플레이 규칙
→ 인법/배경 데이터
→ GM·시나리오·적
→ 세계 설정
```

- 공개 사명과 비밀 같은 정보 권한을 물리적 artifact로 분리하는 사례.
- 세계관 숙독을 플레이 시작 전 필수로 만들지 않는 구성의 대조군.

#### 인세인 — `REFERENCE_ONLY / ADAPT`

- 호러와 비밀/광기 같은 내부 위협을 support artifacts로 가시화하는 사례.
- 리플레이/체험을 규칙 이해보다 앞에 두는 `replay-first` pedagogy의 대조군으로 사용한다.

#### 마기카로기아 — `REFERENCE_ONLY / ADOPT`

- 제품 설명 단계에서 수치보다 `어떤 감정·사건을 체험하는가`를 먼저 약속하는 사례.
- 룰북 첫 장의 feature list보다 **experience promise**를 먼저 쓰는 원리를 참고한다.

### KTRPG-FATE-DROPBOX-001 — 초여명 Fate Core 공개 폴더

```yaml
url: https://www.dropbox.com/scl/fo/ujjpyxy96tem420xotrpy/AKPLR0cPK7cifVgK5mTdYh8?rlkey=05ohszhw1foeoyvib0etc95qd&st=b25ypv0k&e=1&dl=0
verification_status: UNVERIFIED_DIRECT_ACCESS
publisher_link_verified: true
rights_status: PER_FILE_RECHECK_REQUIRED
```

현재 직접 폴더 목록을 안정적으로 읽지 못했다. 초여명 홈페이지가 이 주소를 Fate Core System PDF 무료 공개 폴더로 연결하는 사실만 정본으로 기록한다.

사용자가 ZIP/원문 파일을 제공하면 **한국어 용어 선택, 실제 목차, 예시 위치, 표·시트 구조**를 직접 분석한다.

### KTRPG-COCOFOLIA-GUIDE-001 — adventurekeeper Naver blog

```yaml
url: https://blog.naver.com/adventurekeeper
verification_status: UNVERIFIED_DIRECT_ACCESS
source_tier: T4_COMMUNITY_GUIDE_CANDIDATE
rights_status: REFERENCE_ONLY
```

현재 direct fetch가 실패했다. 구체 기능·절차는 확정하지 않는다. 사용자가 원문/캡처를 제공하기 전까지 VTT/ORPG presentation layer의 discovery source로만 유지한다.

### KTRPG-HANGYUL-001 — 사용자 지정 TRPG 정리 참고 사이트

```yaml
url: https://hangyul219-prog.github.io/TRPG-/
verification_status: VERIFIED_OR_RECHECK_WHEN_APPLYING
rights_status: REFERENCE_ONLY_UNLESS_LICENSE_VERIFIED
use_for: SECTION 단위 문서 구조, 전체 흐름→세부 규칙→reference 정리 비교
```

사용 시 표면 문구를 복제하지 않고 **독자가 어디서 전체 흐름을 알고 어디서 세부 규칙을 찾는가**만 비교한다.

## 7. 공식/Open Source 대조군

### TRPG-FATE-001 — Fate Condensed

```yaml
url: https://fate-srd.com/fate-condensed
source_tier: T1_PRIMARY_OFFICIAL_SRD
verification_status: VERIFIED_SOURCE
rights_status: CC_BY_3_0_FOR_SRD_CONTENT_WITH_SEPARATE_TRADEMARK_BOUNDARY
signature_experience: 캐릭터의 정체성·관계·문제가 실제 사건 해결과 대가를 움직임
```

어떻게 풀었는가:

- **Aspect**는 중요한 사실·정체성·관계를 담는다.
- **Fate Point**는 그 사실을 강하게 끌어오거나 곤란을 받아들이는 자원 순환을 만든다.
- **Stunt**는 특정 Skill의 우수성이나 규칙 예외를 별도 단위로 둔다.
- 캐릭터의 '사실'과 기계적 전문 효과가 완전히 같은 필드가 되지 않게 분리한다.

설명 방식:

- Fate Condensed 자체가 Fate Core를 명료성과 reference 용이성을 위해 압축한 standalone 버전이라고 밝힌다.
- setting/character의 사실을 먼저 잡고, 필요한 core를 보여준 뒤 세부 절차를 reference 가능한 단위로 깊게 설명하는 progressive disclosure의 대조군이다.

**ADOPT:** character truth와 mechanical exception 분리, compact core.
**TEST:** Fate Point 경제를 다른 게임에 그대로 가져오는 것.

### TRPG-BITD-001 — Blades in the Dark

```yaml
url: https://bladesinthedark.com/
license_url: https://bladesinthedark.com/licensing
player_kit_url: https://bladesinthedark.com/downloads
source_tier: T1_PRIMARY_OFFICIAL_SRD
verification_status: VERIFIED_SOURCE
rights_status: CC_BY_3_0_SRD_WITH_PRODUCT_IDENTITY_EXCLUSIONS
```

어떻게 풀었는가:

- 플레이어가 목표와 Action을 고른다.
- GM은 **Position = 위험**과 **Effect = 성과 크기**를 분리한다.
- Resistance로 결과 뒤에도 플레이어가 일부 대가를 줄일 수 있게 하되 Stress를 비용으로 둔다.
- Clock으로 장기 목표·위험 진행을 가시화한다.
- 개인 캐릭터와 Crew를 함께 만들어 개인 성장과 캠페인 조직 성장을 연결한다.

설명 방식:

```text
The Game
→ Players
→ Characters
→ Crew
→ GM
→ Session loop
→ action/position/effect 상세
```

공식 Player Kit는 core overview와 procedure, character/crew/faction tracking을 책 본문과 별도 reference surface로 제공한다.

**ADOPT:** risk/effect 분리, authority mapping, progress visibility, player kit.

### TRPG-GUMSHOE-001 — GUMSHOE SRD

```yaml
landing_url: https://pelgranepress.com/2013/10/24/the-gumshoe-system-reference-document/
pdf_url: https://pelgranepress.com/gumshoe/files/GUMSHOESRDCC-3%20241209.pdf
source_tier: T1_PRIMARY_OFFICIAL_SRD
verification_status: VERIFIED_SOURCE_WITH_RATE_LIMIT_ON_RECHECK
rights_status: CC_BY_3_0_SRD_WITH_TRADED_MARK_BOUNDARY
```

어떻게 풀었는가:

- Investigative ability와 일반 행동 능력을 분리한다.
- 핵심 단서의 획득 여부보다 **어떻게 해석하고 다음 선택으로 연결하는가**에 플레이를 집중시킨다.
- 공식 설명은 SRD가 디자이너용 reference이며 완성된 teaching/playable rulebook과 역할이 다르다고 명시한다.

**ADOPT:** `CORE_INFORMATION_MUST_NOT_BE_SINGLE_ROLL_GATED`, `REFERENCE_SCHEMA_IS_NOT_TEACHING_ORDER`.

### TRPG-YZE-001 — Year Zero Engine SRD

```yaml
srd_url: https://freeleaguepublishing.com/wp-content/uploads/2023/11/YZE-Standard-Reference-Document.pdf
license_url: https://freeleaguepublishing.com/wp-content/uploads/2023/11/Year-Zero-Engine-License-Agreement.pdf
source_tier: T1_PRIMARY_OFFICIAL_SRD
verification_status: VERIFIED_SOURCE
rights_status: YEAR_ZERO_ENGINE_FREE_TABLETOP_LICENSE_V1_0
```

공식 SRD 목차:

```text
Introduction
→ Player Characters
→ Skills & Specialties
→ Combat & Damage
→ Magic
→ Travel
```

Introduction에서 player/GM 역할과 '대화 → 불확실한 위기 → dice'의 흐름을 설명하고, accessible / fast and decisive / risks & rewards 같은 엔진 설계 특성을 세부 규칙보다 먼저 선언한다.

Push/re-roll은 성공 확률을 올리는 대신 비용을 요구해 위험-보상 선택을 만든다.

**ADOPT:** engine design pillars before details, core→domain modules.
**ADAPT:** push/reroll economy.

권리 주의: 전용 라이선스는 YZE SRD 기반 tabletop RPG/VTT module에 대한 조건이며 Free League의 다른 text/art/brand 전체를 허용하지 않는다.

### TRPG-BRP-001 — Basic Roleplaying Universal Game Engine

```yaml
product_url: https://www.chaosium.com/basic-roleplaying-universal-game-engine-pdf/
orc_url: https://www.chaosium.com/orc-license/
orc_content_url: https://www.chaosium.com/content/orclicense/BasicRoleplaying-ORC-Content-Document.pdf
source_tier: T1_PRIMARY_OFFICIAL_RULE_REFERENCE
verification_status: VERIFIED_SOURCE
rights_status: ORC_LICENSED_RULE_CONTENT_WITH_PRODUCT_IDENTITY_EXCLUSIONS
```

어떻게 풀었는가:

- d100 roll-under에서 Skill 수치가 성공 확률과 직접 연결되어 확률 이해가 쉽다.
- 사용한 기술이 성장하는 구조로 행동과 성장의 의미를 연결한다.
- 범용 엔진은 많은 선택 규칙을 toolkit으로 제공한다.

교육 관점:

- 범용 reference와 first-session teaching surface를 분리해 보는 대조군이다.
- 범용 엔진은 `Quickstart → Core → Optional Toolkit`의 3층이 특히 유리한지 검토한다.

**ADOPT:** probability legibility, modular core/options, support artifact separation.
**TEST:** percentile 자체의 적합성.

### TRPG-CAIRN-001 — Cairn

```yaml
url: https://cairnrpg.com/second-edition/players-guide/core-rules/
source_tier: T1_PRIMARY_OFFICIAL_RULES
verification_status: VERIFIED_SOURCE
rights_status: CC_BY_SA_SITE_TEXT_RECHECK_PER_ASSET
```

주요 비교점:

- player principles를 core rules와 함께 명시한다.
- 필요할 때만 Save를 굴리고, 전투에서는 명중 굴림을 없애 피해/자원/위험 관리로 시간을 이동한다.
- inventory와 Fatigue처럼 작은 가시적 자원을 탐험 선택과 연결한다.

**ADAPT:** player-principles-first, inventory-as-pressure.
**TEST:** auto-hit combat은 목표 경험이 맞을 때만.

### TRPG-IRONSWORN-001 — Ironsworn

```yaml
url: https://tomkinpress.com/products/ironsworn-digital-edition
source_tier: T1_PRIMARY_AUTHOR_RELEASE
verification_status: VERIFIED_SOURCE
rights_status: FREE_DOWNLOAD_RIGHTS_RECHECK_FOR_REUSE
```

주요 비교점:

- Guided / co-op / solo를 같은 규칙 계열에서 지원하는 대조군.
- Vow, Progress, Oracle, Move를 통해 GM이 없거나 낮은 prep에서도 목표·불확실성·진척을 생성한다.
- Playkit/asset/truth 자료를 룰북과 분리한다.

**ADOPT:** unfamiliar engine에서 core flow를 creation보다 충분히 앞에서 가르치는 패턴, playkit separation.
**ADAPT:** oracle/GM-less support.

### TRPG-MOTHERSHIP-001 — Mothership Player's Survival Guide

```yaml
url: https://www.tuesdayknightgames.com/products/mothership-players-survival-guide
source_tier: T1_PRIMARY_PUBLISHER
verification_status: VERIFIED_SOURCE
rights_status: FREE_PDF_DOES_NOT_IMPLY_OPEN_REUSE
```

주요 비교점:

- d100 기반 생존/공포에서 Stress/Panic을 장르 핵심 자원으로 집중한다.
- Player's Survival Guide와 Warden/monster/ship domain reference를 분리하는 제품 구조가 강점이다.
- 캐릭터 생성 flowchart 같은 지원 면으로 시작 마찰을 줄이는 사례다.

**ADOPT:** player/GM/domain split, character creation flowchart, genre resource concentration.

### TRPG-24XX-001 — 24XX

```yaml
url: https://jasontocci.itch.io/24xx
source_tier: T1_PRIMARY_AUTHOR_RELEASE
verification_status: RECHECK_WHEN_APPLYING
rights_status: CC_BY_4_0_RECHECK_CURRENT
```

주요 비교점:

- 극소 규칙량에서 fictional positioning을 유지한다.
- 위험이 있을 때만 굴리고, GM이 가능성·추가 단계·비용·위험을 알려준 뒤 플레이어가 행동을 조정할 여지를 주는 rules-light 대조군.

**ADOPT:** microgame information density, roll-only-when-risk-matters.

### TRPG-LF-001 — Lasers & Feelings

```yaml
url: https://johnharper.itch.io/lasers-feelings
source_tier: T1_PRIMARY_AUTHOR_RELEASE
verification_status: RECHECK_WHEN_APPLYING
rights_status: CC_BY_4_0_RECHECK_CURRENT
```

주요 비교점:

- 1페이지에서 premise, character, resolution, GM adventure generator까지 연결하는 Quickstart 극단의 대조군.
- 단 하나의 수치가 상반된 행동 성향과 확률을 함께 정의한다.

**ADAPT:** one-page quickstart benchmark.
**TEST:** single-stat engine 자체.

### TRPG-DND-SRD-001 — D&D SRD 5.2

```yaml
url: https://www.dndbeyond.com/srd
source_tier: T1_PRIMARY_OFFICIAL_SRD
verification_status: RECHECK_WHEN_APPLYING
rights_status: CC_BY_4_0_FOR_SRD_CONTENT
```

주요 비교점:

- 방대한 옵션이 있어도 기본 플레이 언어를 먼저 설명하고 character options와 encyclopedia/reference를 뒤에서 분리하는 전통 d20 대조군.

**ADAPT:** `HOW_PLAY_WORKS_BEFORE_BUILD_OPTIONS`.
**AVOID:** 경량 게임에 방대한 옵션량 자체를 복제.

## 8. 한국어 개수룰 / 권리 경계 반례 Source

던전월드 공개판에서 파생되었다고 해서 모든 2차 룰의 권리가 동일하지는 않다.

### Oriental Spirits

```yaml
url: https://sites.google.com/site/orientalspiritstrpg/
verification_status: VERIFIED_DISCOVERY
```

Dungeon World 기반 개수룰이며 원 Dungeon World의 CC BY 3.0 출처를 명시한다. 장르 변환에서 무엇을 유지/교체하는지 비교하는 후보로 사용한다.

### Phantasy Star TRPG

```yaml
url: https://sites.google.com/site/phantasystartrpg/
verification_status: VERIFIED_DISCOVERY
```

동일 Dungeon World 계열의 SF 변환 사례. 단일 원 엔진에서 장르만 바꾼 여러 파생작을 보편 법칙의 독립 증거로 중복 계산하지 않는다.

### Ghost in the Shell TRPG

```yaml
url: https://sites.google.com/site/ghostintheshelltrpg/
verification_status: VERIFIED_DISCOVERY
```

Dungeon World 기반 근미래/사이버펑크 변환 사례. IP 권리와 rule license를 별도 문제로 본다.

### Nova Stella / Nova Fantasia

```yaml
urls:
  - https://sites.google.com/site/novastellatrpg/
  - https://sites.google.com/site/novafantasiatrpg/
verification_status: VERIFIED_DISCOVERY
rights_status: CUSTOM_RESTRICTION_PRESENT
```

공개 페이지가 제작자/출처 표시를 요구하면서 **원작자의 동의 없는 개수·차용은 불허**한다고 명시한다.

공용 교훈:

```text
open base system
!=
all derivatives are open under identical terms
```

각 파생물의 별도 권리 문구를 확인한다.

## 9. 추가 Source frontier

아래는 materially distinct한 해법을 더 비교할 때 우선 확인할 후보다. 상세 룰을 아직 검증하지 않았다면 `DISCOVERY_ONLY`로 유지한다.

| Source | 우선 비교 질문 | 상태 |
|---|---|---|
| 13th Age SRD | 자유작성 Background가 broad skill list를 대체할 때의 경계 | RECHECK |
| QuestWorlds SRD | 자유 능력 문장과 contest 구조 | RECHECK |
| Cypher System Open License/SRD | player-facing effort/resource spend와 GM 난이도 | RECHECK |
| Fudge SRD | custom trait와 공통 trait ladder의 균형 | RECHECK |
| Freeform Universal | descriptor + binary/qualified outcome language | RECHECK |
| Risus | Cliché 하나에 직업·배경·능력을 묶을 때의 광범위성 | RECHECK |
| Savage Worlds Test Drive | traditional action RPG를 Quickstart가 어떤 순서로 가르치는가 | RECHECK |
| Mausritter | inventory card/slot가 실제 플레이 인터페이스가 되는 방식 | RECHECK |
| City of Mist | freeform tag와 standardized status의 연결 | RECHECK |
| Resistance System | 실패·저항 비용을 테마적 손실과 연결하는 방식 | RECHECK |

이 표는 권리·세부 룰의 정본이 아니다. 적용할 때 공식 원출처와 현재 라이선스를 다시 확인한다.

## 10. ADOPT / ADAPT / AVOID 선택표

| 문제 | 우선 살펴볼 패턴 | 기본 판정 |
|---|---|---|
| 캐릭터 자유도가 높아 행동 가능 범위가 흔들림 | fictional permission / aspect/tag boundary | ADOPT |
| 조사 실패로 시나리오가 멈춤 | Core Clue non-gating | ADOPT |
| '난이도' 하나로 보스/위험/성과를 다 표현하기 어려움 | risk/effect split | ADAPT |
| 장기 목표가 보이지 않음 | clocks/progress track | ADAPT |
| 역할 비대칭을 살리고 싶음 | reciprocal asymmetric value | TEST |
| 첫 세션 진입이 느림 | Quickstart / example / flowchart / player kit | ADOPT |
| 룰북이 너무 두꺼움 | compact core + optional modules | ADOPT |
| GM 재량이 지나치게 불투명함 | agenda/principles/procedure / explicit authority | ADOPT |
| 자유작성 스킬이 만능 문장이 됨 | permission와 mechanical effect 분리 + bounds | ADOPT |
| VTT 기능이 룰을 대신하기 시작함 | presentation layer 분리 | AVOID |
| 무료 PDF라서 그대로 복제하려 함 | rights boundary | AVOID |

## 11. 룰북 pedagogy 검수

각 룰북/초안에 대해 다음을 묻는다.

### 첫 5분

- 플레이어가 **무슨 게임인지** 한 문장으로 설명할 수 있는가?
- 자신이 반복해서 무엇을 선택하는지 알 수 있는가?
- 주사위를 언제 굴리고 언제 안 굴리는지 알 수 있는가?
- 실패가 단순 '아무것도 못함'이 아니라 어떤 이야기 결과를 만드는지 알 수 있는가?

### 캐릭터 생성

- 항목이 나오기 전에 **왜 필요한지** 보여줬는가?
- 세계관 설명을 전부 읽지 않아도 첫 캐릭터를 만들 수 있는가?
- 자유작성 필드는 좋은/나쁜 예와 경계가 있는가?
- 한 페이지/한 시트만 보고 생성 흐름을 따라갈 수 있는가?

### 핵심 규칙

- 규칙 정의 직후 실제 대화/판정 예가 있는가?
- 예시가 '성공'만 보여주지 않고 실패·부분 성공·비용도 보여주는가?
- 서로 다른 장에서 같은 용어를 다른 의미로 쓰지 않는가?
- 핵심 절차에 `누가 결정하는가`가 명시돼 있는가?

### GM

- GM section이 분위기 조언만이 아니라 **실행 절차**를 제공하는가?
- 실패 결과·난도·정보·NPC·위협을 만드는 기준이 있는가?
- 첫 세션 준비량과 하지 말아야 할 준비를 구분하는가?

### 플레이 중 Reference

- 룰을 이해하는 순서와 룰을 찾는 순서가 분리돼 있는가?
- 요약·카드·시트로 반복 참조 비용을 줄였는가?
- 공개/비공개 정보가 같은 artifact에 섞여 있지 않은가?
- 고급/드문 규칙이 core를 가리지 않는가?

## 12. 실패 패턴

### RULEBOOK_AS_DATABASE_DUMP

규칙을 정확히 나열했지만 독자가 왜 필요한지 모른다.

**교정:** player promise → flow → example을 먼저 제공한다.

### EXAMPLE_TOO_LATE

추상 용어를 수십 페이지 설명한 뒤에야 실제 플레이가 보인다.

**교정:** 첫 core rule 근처에 짧은 대화 예를 둔다.

### EVERY_RULE_ON_CHARACTER_SHEET

시트가 mini-rulebook이 되어 작성·플레이 모두 느려진다.

**교정:** 플레이 중 반복 확인하는 최소 필드만 둔다.

### SUPPORT_ARTIFACT_SPRAWL

벤치마크 게임이 여러 시트를 쓴다는 이유로 우리도 모두 만든다.

**교정:** `누가 / 얼마나 자주 / 어떤 상태를 갱신하는가`가 없으면 분리하지 않는다.

### FREEFORM_REWARDS_WORDSMITHING

자유작성 능력이 문장을 넓고 애매하게 쓰는 사람을 보상한다.

**교정:** permission, scope, mechanical effect, limitation을 분리하고 exemplar/anti-exemplar로 검수한다.

### FAMOUS_MECHANIC_CARGO_CULT

유명 게임의 Aspect, Move, Clock, Core Clue를 현재 게임의 문제와 관계없이 붙인다.

**교정:** 먼저 `problem_solved`와 `validation_needed`를 적고 decision delta가 없으면 `REFERENCE_ONLY`로 남긴다.

## 13. 적용 순서

```text
PROJECT CANON / PLAYER PROMISE
→ 현재 문제 정의
→ materially distinct Source 3개 이상 비교 가능한지 확인
→ Source authority / access / rights precheck
→ problem → mechanic → experience → pedagogy 추출
→ ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY
→ 프로젝트 고유 합성안 2~3개 비교
→ 최소 규칙 PoC
→ 실제 플레이테스트
→ 결과에 따라 유지 / 수정 / 폐기
→ 반복 가치가 있는 교훈만 Base case/reference로 환류
```

## 14. 완료 판정과 claim ceiling

이 Radar를 읽고 룰을 선택한 것만으로 다음을 주장하지 않는다.

- 재미가 검증됨
- 밸런스가 검증됨
- 신규 플레이어가 이해함
- GM 준비시간이 줄어듦
- 온라인/VTT 운영성이 좋음
- 상업적 사용 권리가 확보됨

실제 프로젝트에서 최소한 다음을 확인한다.

- 캐릭터 생성 시간과 막힌 지점
- 첫 판정까지 걸린 시간
- 판정 규칙 재질문 횟수
- 한 세션에서 실제 사용된 스킬/면모/행동 분포
- GM 즉석 판정 분쟁과 소요
- 실패 후 이야기가 이어지는지
- 플레이어가 기억한 선택·감정·장면
- Quickstart만 읽은 신규 사용자의 독립 수행

## 15. 현재 Source 상태 요약

```yaml
verified_direct:
  - cympub.kr
  - Dungeon World Korean public edition
  - trpgclub.com
  - Fate SRD
  - Blades in the Dark SRD/player kit/licensing
  - Year Zero Engine SRD/license
  - Basic Roleplaying ORC material
  - Cairn official rules
  - Ironsworn official page
  - Mothership official page
partial_or_recheck:
  - hangyul219-prog TRPG structure reference
  - 24XX
  - Lasers & Feelings
  - D&D SRD 5.2
unverified_direct_access:
  - cympub-linked Dropbox Fate folder listing
  - blog.naver.com/adventurekeeper body
future_user_evidence:
  - user-provided rulebook ZIP files
```

Source 상태와 라이선스는 실제 적용·배포 결정 직전에 다시 확인한다.
