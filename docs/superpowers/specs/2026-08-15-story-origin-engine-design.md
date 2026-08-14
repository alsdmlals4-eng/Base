# 다중 진입 이야기 생성 엔진 설계

- 날짜: 2026-08-15
- 상태: `APPROVED`
- 대상 저장소: `alsdmlals4-eng/Base`
- 작업 브랜치 시작점: `main@1e9a9ae4b2e480ba7cc1549e7627264889d51610`
- 목적: 세계관·성격·가치관·관계·소속기관·직업·능력·질문·사건·전제·독자 약속 등 서로 다른 재료에서 출발해 실제 이야기 압력·선택·결과로 변환하는 공용 생성 절차를 Base에 추가한다.

## 1. 문제 정의

현재 Base에는 이미 다음 책임이 있다.

- `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`는 세계·인물·관계·직업·조직·가치·능력·사건을 조사하는 축과 외부 Source를 관리한다.
- `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`는 장면·대사·선택·관계와 `RELATIONAL_APPEAL`을 실행·검수한다.
- `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md`는 Reader Promise, POV, 인과, 선택, 결과, 후폭풍을 검수한다.
- `skills/developing-and-revising-serial-fiction`은 연재소설의 실제 consumer다.
- `templates/planning/NARRATIVE_CONTENT_PLAN.md`는 게임 프로젝트의 서사 계획 surface다.

그러나 “흥미로운 설정이나 인물 재료를 하나 발견했을 때, 그것을 어떤 순서로 사건·갈등·선택·결과가 있는 이야기로 발전시키는가”는 한 공용 owner에 정식화되어 있지 않다.

이 공백 때문에 다음 실패가 가능하다.

```text
흥미로운 세계관은 많지만 행동해야 하는 사람이 없다.
캐릭터 설정은 많지만 무엇이 그 성격을 시험하는지 없다.
직업과 소속기관은 있으나 책임·권한·절차가 사건을 만들지 않는다.
가치관은 대사로 설명되지만 선택 비용이 없다.
큰 사건은 있으나 인물의 판단이 결과를 바꾸지 않는다.
작법 프레임워크를 먼저 고른 뒤 작품을 그 칸에 맞춰 억지로 변형한다.
```

이번 변경은 이 공백만 책임진다.

## 2. Existing Solution First 판정

```yaml
existing_solution_first:
  narrative_source_radar: REUSE
  narrative_relationship_method: REUSE_AS_DOWNSTREAM_CONSUMER
  serial_fiction_guide_and_skill: ABSORB_AS_CONSUMER
  narrative_content_plan: ABSORB_AS_CONSUMER
  new_active_skill: REJECT
  new_skill_mode: REJECT
  new_registry_entry: REJECT
  new_story_origin_method: BUILD_NEW_BOUNDED_OWNER
```

새 공용 Method 파일이 필요한 이유는 기존 `NARRATIVE_AND_RELATIONSHIP_METHOD.md`가 **이미 선택된 장면·대화·관계의 실행과 검수**를 소유하고 있기 때문이다. 이번 책임은 그보다 한 단계 앞선 **이야기 발생과 확장**이다. 같은 파일에 계속 누적하면 “발상 → 생성 → 장면 실행 → 관계 검수”의 경계가 흐려진다.

따라서 새 Skill이나 Mode는 만들지 않고, 지식 Method 하나만 공용 owner로 추가한다.

권장 owner:

`docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`

## 3. 외부 작법 벤치마크와 흡수 기준

외부 방법은 Base의 보편 법칙이 아니라 `Lens`와 설계 재료로만 사용한다. 프로젝트 정본과 실제 원고·게임 상태가 항상 우선한다.

### 3.1 MICE Quotient / Writing Excuses

Source:

- `https://writingexcuses.com/16-35-what-is-the-m-i-c-e-quotient/`
- `https://writingexcuses.com/15-25-using-the-mice-quotient-for-conflict/`

확인한 핵심:

- Milieu, Inquiry, Character, Event처럼 서로 다른 종류의 story thread가 존재할 수 있다.
- thread 종류에 따라 방해 방식과 해결 조건이 달라질 수 있다.
- 여러 thread를 함께 쓸 수 있지만 관련 없는 새 thread를 계속 열면 이야기 초점이 약해질 수 있다.

Base 흡수:

- **하나의 보편 출발점을 강제하지 않는다.**
- 세계·질문·인물·사건 등 다른 seed를 동등한 출발점으로 인정한다.
- seed 종류를 작품 장르 공식이나 필수 taxonomy로 강제하지 않는다.

### 3.2 Snowflake Method / Advanced Fiction Writing

Source:

- `https://www.advancedfictionwriting.com/articles/snowflake-method/`

확인한 핵심:

- 작은 이야기 아이디어를 한 문장 수준에서 시작해 단계적으로 확장한다.
- 확장 과정에서 인물·동기·갈등·줄거리·장면을 더 구체화한다.

Base 흡수:

- 처음부터 세계관·캐릭터·플롯 전체를 완성하지 않는다.
- `Primary Seed` 하나에서 작은 story packet을 만든 뒤 필요한 만큼만 확장한다.
- Snowflake의 전체 10단계를 Base 필수 절차로 복제하지 않는다.

### 3.3 Lisa Cron / Story Genius

Source:

- `https://www.penguinrandomhouse.com/books/252747/story-genius-by-lisa-cron/`

확인한 핵심:

- 이야기는 외부 사건만 나열하는 것보다 인물이 왜 그 사건을 중요하게 받아들이는지와 내부 판단 논리를 연결할 때 강해진다.

Base 흡수:

- `CHARACTER`, `VALUE_BELIEF` seed에서 **현재 판단 규칙과 사건 압력의 연결**을 점검한다.
- 모든 이야기를 인물의 과거·오해에서만 시작하게 만들지 않는다.

### 3.4 K. M. Weiland / Character Arc

Source:

- `https://www.helpingwritersbecomeauthors.com/what-does-your-character-want/`
- `https://www.helpingwritersbecomeauthors.com/character-arcs-3/`

확인한 핵심:

- Want, Need, Lie, Truth 같은 내부 축은 인물의 현재 욕망과 더 깊은 변화 방향을 구분하는 데 사용할 수 있다.

Base 흡수:

- `VALUE_BELIEF` seed와 character arc 진단에서 선택적으로 사용한다.
- 모든 인물에게 Want/Need/Lie/Truth 네 칸을 강제하지 않는다.
- 고정 Positive Change Arc를 성공 조건으로 삼지 않는다.

### 3.5 John Truby / The Anatomy of Story

Source:

- `https://truby.com/books-2025/`
- `https://truby.com/anatomyofstory-2025/`

확인한 핵심:

- premise, character, moral argument/theme, story world, plot, scene 등을 서로 분리된 체크리스트가 아니라 연결된 이야기 구성 요소로 다룬다.

Base 흡수:

- 하나의 seed가 다른 요소를 **발생·압박·변형**하게 만드는지를 본다.
- 22-step 구조나 특정 moral argument 형식을 Base 필수 구조로 복제하지 않는다.

### 3.6 Save the Cat — Institutionalized

Source:

- `https://savethecat.com/institutionalized`

확인한 핵심:

- 가족·회사·조직·집단과 개인의 위치 자체가 강한 이야기 엔진이 될 수 있다.
- group과 개인의 choice, sacrifice가 해당 genre lens의 핵심 요소다.

Base 흡수:

- `INSTITUTION`을 독립적인 story seed로 인정한다.
- 조직 목적, 규칙, 권한, 보상, 비용, 개인 가치와의 충돌을 조사한다.
- 모든 기관 이야기에서 `join / burn it down / self-destruction` 결말이나 sacrifice를 강제하지 않는다.

### 3.7 Story Grid

Source:

- `https://storygrid.com/scenes/`
- `https://storygrid.com/value-shift-101/`

확인한 핵심:

- 작동하는 scene은 인물 또는 맥락의 가치·상태가 장면 전후에 의미 있게 변하는지 진단할 수 있다.

Base 흡수:

- story seed가 단순 설명으로 끝나지 않고 `STATE / VALUE / RELATIONSHIP_SHIFT`를 만들었는지 확인하는 downstream validation lens로 사용한다.
- 모든 장면을 동일한 polarity table에 맞추지 않는다.

## 4. 핵심 공용 원칙 — `STORY_ORIGIN_ENGINE`

정의:

> 이야기는 특정한 하나의 출발점에서만 시작하지 않는다. 흥미로운 세계·인물·가치·관계·직업·기관·능력·질문·사건·전제·경험 약속 중 하나를 seed로 잡고, 그 seed가 누군가에게 만드는 압력과 선택을 추적해 실제 변화가 있는 이야기로 변환한다.

핵심 흐름:

```text
SEED
→ AFFECTED_AGENT
→ PRESSURE
→ DESIRE / GOAL
→ RESISTANCE
→ CONSEQUENTIAL_CHOICE
→ CONSEQUENCE
→ STATE / VALUE / RELATIONSHIP_SHIFT
→ NEXT_PRESSURE
```

### 4.1 `PRESSURE`의 의미

`PRESSURE`는 전투·폭력·재난만 뜻하지 않는다.

다음도 포함한다.

- 의무와 책임
- 원하는 것과 현재 상태의 간극
- 호기심과 미해결 질문
- 사회적 기대와 역할
- 기회와 유혹
- 관계의 비대칭
- 시간·자원·정보 제약
- 가치관의 모순
- 일상 루틴을 깨는 작은 변화

따라서 조용한 관계극·일상물·코미디·탐험·미스터리에도 사용할 수 있다.

### 4.2 `AFFECTED_AGENT`의 의미

항상 전통적 단일 주인공일 필요는 없다.

- 개인
- 두 사람의 관계
- 팀
- 가족
- 조직
- 공동체
- 플레이어가 조종하는 여러 인물

중 하나일 수 있다.

핵심은 seed가 **누구의 행동 조건을 바꾸는지**를 특정하는 것이다.

## 5. Seed Catalog

처음부터 모두 채우지 않는다.

기본:

```yaml
primary_seed_count: 1
secondary_seed_count: 0..2
all_seed_completion_required: false
```

### `CHARACTER`

성격, 욕망, 공포, 결점, 과거 경험, 판단 습관에서 시작한다.

질문:

```text
이 특성이 평소에는 어떻게 유용한가?
→ 언제 가장 불리해지는가?
→ 무엇을 지키려다 더 큰 문제를 만드는가?
→ 어떤 선택이 이 사람의 진짜 성격을 증명하는가?
```

### `VALUE_BELIEF`

가치관, 신념, 도덕선, 자기기만, 세계 해석에서 시작한다.

```text
무엇을 옳다고 믿는가?
→ 그 믿음을 지키면 무엇을 잃는가?
→ 버리면 무엇을 얻는가?
→ 실제 선택 뒤 믿음은 강화·수정·붕괴·복잡화되는가?
```

### `RELATIONSHIP`

사랑, 경쟁, 부채, 의존, 권력, 보호, 배신, 신뢰에서 시작한다.

```text
서로에게 무엇을 원하는가?
→ 힘·정보·책임은 어떻게 비대칭인가?
→ 같은 사건을 왜 다르게 판단하는가?
→ 무엇을 선택하면 관계의 상태가 실제로 달라지는가?
```

### `WORLD_MILIEU`

세계관, 장소, 문화, 역사, 제도, 계층, 경제, 금기에서 시작한다.

```text
이 세계 조건 때문에 누가 가장 불편하거나 유리한가?
→ 평범한 하루에서 무엇이 달라지는가?
→ 어떤 선택 비용·기회·위험을 만드는가?
→ 그 조건을 서로 다르게 해석하는 사람은 누구인가?
```

### `INSTITUTION`

회사, 군대, 가족, 학교, 길드, 문파, 정부, 종교, 범죄조직 등에서 시작한다.

```text
조직은 무엇을 위해 존재하는가?
→ 구성원에게 무엇을 주고 무엇을 요구하는가?
→ 공식 규칙과 실제 관행은 같은가?
→ 개인 가치·관계·생존과 어디에서 충돌하는가?
→ 복종·협상·이탈·개혁 중 어떤 선택이 실제 비용을 만드는가?
```

### `OCCUPATION_ROLE`

직업, 임무, 사회적 역할, 전문성, 업무 절차에서 시작한다.

```text
무엇을 책임져야 하는가?
→ 평소 어떤 절차로 문제를 푸는가?
→ 절차가 통하지 않는 예외는 무엇인가?
→ 직업윤리와 개인 욕망은 어디서 충돌하는가?
→ 전문성이 해결과 새로운 문제를 동시에 만드는가?
```

### `ABILITY_RESOURCE_RULE`

능력, 마법, 기술, 장비, 자원, 시스템 규칙, 금지 규칙에서 시작한다.

```text
무엇을 가능하게 하는가?
→ 누가 접근할 수 있고 누가 배제되는가?
→ 존재하는 비용·제약·책임은 무엇인가?
→ 같은 능력을 인물마다 왜 다르게 사용하는가?
→ 사용 뒤 어떤 상태·관계·자원 변화가 남는가?
```

모든 능력에 반드시 대가·부작용을 새로 만들지는 않는다.

### `INQUIRY`

수수께끼, 조사 질문, 비밀, 미확인 사실에서 시작한다.

```text
무엇을 알고 싶은가?
→ 왜 지금 알아야 하는가?
→ 누가 답을 숨기거나 잘못 알고 있는가?
→ 답을 알면 무엇을 선택해야 하는가?
→ 답 자체가 새로운 문제를 여는가?
```

### `EVENT`

사고, 실종, 만남, 전쟁, 재난, 발견, 기회, 상태 변화에서 시작한다.

```text
누구의 기존 상태가 깨졌는가?
→ 되돌리려 하는가, 이용하려 하는가, 받아들이려 하는가?
→ 무엇이 그것을 막는가?
→ 사건보다 중요한 판단 지점은 어디인가?
```

### `PREMISE`

“만약 ○○라면?” 같은 가정에서 시작한다.

```text
이 가정이 실제라면 누구의 삶이 가장 크게 달라지는가?
→ 가장 흥미로운 압력은 무엇인가?
→ 이 premise를 설명이 아니라 행동으로 증명할 첫 상황은 무엇인가?
```

### `GENRE_READER_PROMISE`

독자·플레이어가 반복적으로 얻어야 하는 경험에서 시작한다.

```text
어떤 감정·판단·관계·문제 해결 경험을 반복해서 주는가?
→ 그 경험을 가장 잘 발생시키는 인물과 세계 조건은 무엇인가?
→ 첫 story seed가 이 약속을 실제 선택과 결과로 어떻게 보여주는가?
```

## 6. Story Origin Packet

공용 Method는 아래를 권장하지만 모든 필드를 의무화하지 않는다.

```yaml
story_origin_packet:
  primary_seed:
  secondary_seeds: []
  seed_statement:
  affected_agent:
  pressure:
  desire_or_goal:
  resistance:
  consequential_choice:
  consequence:
  shift:
  next_pressure:
  reader_or_player_value:
  canon_constraints:
```

최소 실행 가능 조건:

```text
SEED
+ AFFECTED_AGENT
+ PRESSURE
+ CHOICE_OR_COMMITMENT
+ OBSERVABLE_CHANGE
```

`CHOICE_OR_COMMITMENT`는 항상 메뉴식 선택지가 아니다. 인물이 행동을 결심하거나, 플레이어가 하나의 접근법을 실행하거나, 관계가 되돌리기 어려운 방향으로 움직이는 것도 포함한다.

## 7. Seed에서 이야기로 확장하는 절차

### 단계 A — Seed를 한 문장으로 제한한다

처음부터 lore bible을 쓰지 않는다.

```text
“기억을 치료하는 마법을 쓸수록 자신의 기억을 잃는다.”
“전투 중 민간인 보호가 최우선인 용병.”
“괴이를 연구하지만 제거를 명령하는 국가기관.”
```

### 단계 B — 가장 큰 압력을 받는 Agent를 찾는다

“누가 이 설정 때문에 가장 많이 행동해야 하는가?”를 묻는다.

흥미로운 seed가 있지만 affected agent를 찾을 수 없다면 현재 제작 범위에서는 `LORE_WITHOUT_AGENT` 후보로 본다.

### 단계 C — 압력을 행동 목표로 번역한다

```text
세계 규칙
→ 생활 비용
→ 현재 목표

직업
→ 책임
→ 처리 절차
→ 예외 상황

가치관
→ 지키려는 기준
→ 시험 상황
→ 선택 비용
```

### 단계 D — Resistance를 만든다

Resistance는 무조건 악당이 아니다.

- 다른 사람의 합리적인 목표
- 제도와 규칙
- 정보 부족
- 시간
- 자원
- 자신의 습관과 믿음
- 관계에서 지켜야 할 약속
- 선택하면 사라지는 다른 가능성

이 될 수 있다.

### 단계 E — Consequential Choice를 만든다

좋은 선택은 “정답을 맞힌다”가 아니라 최소 하나를 바꾼다.

- 책임
- 관계
- 정보
- 자원
- 평판
- 목표
- 가치관
- 위치
- 위험
- 앞으로 가능한 선택

### 단계 F — Shift를 확인한다

사건이 컸다는 사실보다 **전후 상태가 실제로 달라졌는지**를 본다.

`Story Grid`의 value shift 개념은 여기서 진단 Lens로만 사용한다.

### 단계 G — Next Pressure를 생성한다

좋은 결과는 모든 문제를 리셋하지 않는다.

```text
선택 결과
→ 새 책임 / 새 적대 / 새 의문 / 새 기회 / 잃은 가능성
→ 다음 episode·scene·quest·relationship pressure
```

연속작은 `NEXT_PRESSURE`가 Reader Promise를 계속 소비할 수 있는지 본다.

## 8. `RELATIONAL_APPEAL`과의 책임 분리

`STORY_ORIGIN_ENGINE`과 `RELATIONAL_APPEAL`은 중복하지 않는다.

```text
STORY_ORIGIN_ENGINE
= 무엇에서 이야기를 시작하고 어떻게 압력·선택·변화로 변환할지 생성한다.

RELATIONAL_APPEAL
= 선택된 요소들의 조합이 실제로 더 흥미로운 선택·갈등·대사·행동·결과를 만드는지 검수한다.
```

권장 흐름:

```text
Primary Seed 선정
→ STORY_ORIGIN_ENGINE으로 story pressure 생성
→ Secondary Seed가 필요할 때만 결합
→ RELATIONAL_APPEAL로 조합의 실제 장면 가치 검수
→ NARRATIVE_AND_RELATIONSHIP_METHOD로 장면·대화·선택 실행
→ 매체별 Guide/Skill에서 continuity·reader/player evidence 검수
```

예:

```text
OCCUPATION_ROLE: 퇴마사
VALUE_BELIEF: 괴이는 무조건 죽이면 안 된다
INSTITUTION: 괴이 제거를 명령하는 협회
RELATIONSHIP: 협회에서 자신을 키운 스승

↓ STORY_ORIGIN_ENGINE
책임과 가치가 충돌하는 선택 발생

↓ RELATIONAL_APPEAL
퇴마사×협회 / 퇴마사×스승 / 퇴마사×능력 조합이
실제 다른 대사·행동·결과를 만드는지 검수
```

## 9. Interactive Narrative 경계

게임에서는 모든 좋은 이야기가 분기형일 필요가 없다.

다음도 유효하다.

- 플레이어가 접근 순서를 고른다.
- 같은 목표를 다른 방법으로 수행한다.
- 선택은 하나지만 준비 과정에서 판단이 드러난다.
- 시스템 사용이 후속 자원·관계·정보를 바꾼다.
- 주인공의 강제 선택을 플레이어가 관찰하되 그 의미를 다른 시스템에서 해석한다.

따라서 `CONSEQUENTIAL_CHOICE`는 `PLAYER_BRANCH_REQUIRED`와 동의어가 아니다.

게임 프로젝트에서는 반드시 기존 Save/Data Schema와 gameplay authority를 확인하고, 이 공용 Method가 새 분기·상태 필드를 자동 요구하지 않게 한다.

## 10. Failure States

### `LORE_WITHOUT_AGENT`

세계·역사·마법은 흥미롭지만 현재 행동해야 하는 agent와 연결되지 않는다.

### `TRAIT_WITHOUT_TEST`

“용감하다 / 냉정하다 / 정의롭다” 같은 trait가 있으나 그것을 시험하는 상황과 선택이 없다.

### `VALUE_AS_SLOGAN`

가치관이 설명·대사로만 존재하고 지키거나 버릴 때의 비용이 없다.

### `INSTITUTION_AS_LABEL`

조직 이름과 직급은 있으나 목적·권한·규칙·보상·책임·압력이 없다.

### `JOB_AS_COSTUME`

직업이 의상·말투·설정 문구일 뿐 문제 해결법과 책임에 영향을 주지 않는다.

### `ABILITY_AS_PREMISE_DECORATION`

능력 규칙이 멋진 설정으로만 존재하고 실제 선택·자원·관계·결과를 바꾸지 않는다.

### `EVENT_WITHOUT_DECISION`

사건 규모는 크지만 핵심 agent의 판단·행동이 의미 있는 결과를 만들지 않는다.

### `MYSTERY_WITHOUT_STAKES`

질문은 있으나 답을 알아야 할 현재 이유와 답 이후의 선택이 없다.

### `SEED_ACCUMULATION_WITHOUT_PRESSURE`

여러 seed를 계속 추가하지만 story pressure가 강해지지 않고 설정표만 늘어난다.

### `FRAMEWORK_CHECKLIST_OVERFIT`

외부 작법의 칸을 채우기 위해 프로젝트 정본·장르 약속·매체 장점을 억지로 변형한다.

## 11. 명시적 비강제 규칙

다음을 Base 보편 법칙으로 만들지 않는다.

- 모든 이야기는 캐릭터에서 시작해야 한다.
- 모든 캐릭터는 Want/Need/Lie/Truth 네 항목을 가져야 한다.
- 모든 기관 이야기는 희생이나 세 가지 정해진 결말로 끝나야 한다.
- 모든 장면은 같은 beat 수를 가져야 한다.
- 모든 이야기는 Three Act / Hero's Journey / Save the Cat beat를 따라야 한다.
- 모든 능력은 대가·부작용을 가져야 한다.
- 모든 사건은 폭력적 stakes를 가져야 한다.
- 모든 게임 서사는 플레이어 분기를 가져야 한다.
- 모든 seed 조합을 미리 설계해야 한다.

## 12. 소비자 설계

구현 단계에서 다음 consumer를 최소 연결 대상으로 검토한다.

### 공용 narrative Method

`docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`

- 장면 작성 전에 story seed와 pressure가 아직 불명확할 때 새 owner를 읽도록 연결한다.
- 기존 `RELATIONAL_APPEAL` 정의는 중복 작성하지 않는다.

### 연재소설 Guide / Skill

- 새 이야기·아크·에피소드 기획 단계에서 선택적으로 사용한다.
- 이미 확정된 정본의 단순 퇴고에는 강제하지 않는다.
- Reader Promise와 story origin을 연결한다.

### 게임 Narrative Template

`templates/planning/NARRATIVE_CONTENT_PLAN.md`

- 프로젝트 초기 이야기 발상에서 `Primary Seed`와 최소 story packet을 사용할 수 있게 한다.
- 프로젝트 데이터 schema나 런타임 branch 구조를 만들지 않는다.

### Source Radar

`docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`

- 이번 조사에서 채택·조정된 작법 Source와 claim ceiling을 기록한다.
- Source Radar가 craft authority를 직접 소유하지 않는다.

### Learning Log

기존 연재소설 또는 공용 Skill learning surface에 “다중 진입 story origin을 공용 owner로 두고, 개별 프레임워크는 Lens로 제한한다”는 학습을 기록한다.

## 13. 계약 테스트 설계

새 테스트는 다음을 검증한다.

```yaml
story_origin_contract:
  common_method_exists: true
  story_origin_engine_marker_exists: true
  seed_catalog_contains:
    - CHARACTER
    - VALUE_BELIEF
    - RELATIONSHIP
    - WORLD_MILIEU
    - INSTITUTION
    - OCCUPATION_ROLE
    - ABILITY_RESOURCE_RULE
    - INQUIRY
    - EVENT
    - PREMISE
    - GENRE_READER_PROMISE
  all_seeds_required: false
  conversion_chain_contains:
    - SEED
    - AFFECTED_AGENT
    - PRESSURE
    - CONSEQUENTIAL_CHOICE
    - CONSEQUENCE
    - SHIFT
    - NEXT_PRESSURE
  relational_appeal_boundary_is_explicit: true
  serial_fiction_consumer_is_linked: true
  game_narrative_template_consumer_is_linked: true
  source_radar_evidence_is_linked: true
  new_active_skill: false
  new_skill_mode: false
  skill_registry_diff_required: false
```

TDD 순서:

1. 새 owner와 consumer 연결을 요구하는 focused contract를 먼저 추가한다.
2. RED가 기존 기능 실패가 아니라 이번 owner 부재만 잡는지 확인한다.
3. 최소 owner와 consumer 연결을 구현한다.
4. focused test와 기존 serial-fiction / documentation / skill governance 회귀를 실행한다.
5. 적대적 검토 후 최소 보완만 허용한다.
6. 최신 `main`과 재동기화하고 exact-head CI를 다시 확인한다.

## 14. 적대적 검토 기준

구현 전후 다음 공격 질문을 사용한다.

```text
“여러 출발점을 인정한다”가 결국 11개 항목 필수 체크리스트가 되지 않았는가?
CHARACTER seed가 사실상 다시 기본값이 되어 다른 seed를 열등하게 취급하지 않는가?
세계관·직업·기관을 모두 CHARACTER_X_WORLD로 흡수해 독립적인 발생 규칙을 잃지 않았는가?
조용한 이야기에도 억지로 위기·폭력·희생을 요구하지 않는가?
게임에 불필요한 분기·관계 수치·Save Schema를 강제하지 않는가?
기존 RELATIONAL_APPEAL과 책임이 중복되지 않는가?
Snowflake, MICE, Story Grid, Save the Cat 등 외부 프레임워크가 보편 법칙으로 승격되지 않았는가?
새 Method가 실제 consumer 없이 고립되지 않는가?
```

유효한 비판만 `ACCEPTED_MINIMAL_REFINEMENT`로 반영한다.

## 15. Done Criteria

Base 수준 완료는 다음이다.

```yaml
common_owner: IMPLEMENTED
multi_entry_seed_catalog: IMPLEMENTED
seed_to_pressure_choice_shift_chain: IMPLEMENTED
relational_appeal_boundary: EXPLICIT
serial_fiction_consumer: CONNECTED
game_narrative_planning_consumer: CONNECTED
source_evidence_record: CONNECTED
learning_record: UPDATED
focused_contract: GREEN
relevant_regression: GREEN
new_skill_or_mode: NONE
registry_growth: NONE
project_canon_rewrite: NONE
project_schema_change: NONE
human_reader_quality: NOT_CLAIMED
commercial_effect: NOT_CLAIMED
```

## 16. Rollback

이 변경은 공용 Method·consumer link·test·learning/evidence 기록에 한정한다.

롤백 시 해당 PR의 변경을 하나의 단위로 revert한다.

다음을 건드리지 않으므로 별도 migration rollback은 없다.

- 프로젝트 Canon
- 게임 Save/Data Schema
- 런타임 코드
- Skill ID
- Skill Registry identity
- Work Mode
- 외부 서비스 설정

## 17. 예상 효과와 검증 상한

예상 효과:

```text
“설정을 더 만든다”
→ “현재 가진 재료에서 누가 어떤 압력을 받고 무엇을 선택하는가를 찾는다”

“캐릭터를 먼저 만들고 플롯을 붙인다”
→ “세계·인물·가치·직업·기관·사건 등 어디서든 시작할 수 있다”

“작법 공식을 고른다”
→ “작품의 seed를 먼저 찾고 필요한 프레임워크만 Lens로 빌린다”
```

하지만 Base contract가 Green이어도 다음은 자동 증명되지 않는다.

```yaml
project_specific_story_quality: PROJECT_PILOT_NOT_RUN
human_reader_response: HUMAN_NOT_RUN
player_response: HUMAN_NOT_RUN
commercial_effect: NOT_RUN
universal_superiority_over_other_methods: NOT_CLAIMED
```

실제 효과는 후속 프로젝트에서 서로 다른 seed 유형을 사용한 story packet을 만들어 비교 검증해야 한다.
