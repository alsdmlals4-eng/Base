# 이야기 기원·생성 방법

- 상태: 공용 방법
- 목적: 세계·인물·가치·관계·기관·직업·능력·질문·사건·전제·Reader Promise 중 하나의 seed를 실제 이야기 압력·선택·변화로 발전시킨다.
- 외부 Source 발견: `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`의 `STORY_ARCHITECTURE_GENRE_AND_SERIALIZATION`

외부 작법 프레임워크는 프로젝트 정본보다 높은 권한을 갖지 않는다. 이 Method는 MICE, Snowflake, Story Genius, Want/Need/Lie/Truth, Truby, Save the Cat, Story Grid를 선택적 Lens로만 사용하며 어느 하나를 모든 작품의 필수 구조로 만들지 않는다.

## 1. 핵심 공용 원칙 — `STORY_ORIGIN_ENGINE`

이야기는 특정한 하나의 출발점에서만 시작하지 않는다. 흥미로운 세계·인물·가치·관계·직업·기관·능력·질문·사건·전제·경험 약속 중 하나를 seed로 잡고, 그 seed가 누군가에게 만드는 압력과 선택을 추적해 실제 변화가 있는 이야기로 변환한다.

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

이 흐름은 고정 beat sheet가 아니다. 현재 seed가 아직 설정·소재 수준인지, 아니면 행동과 변화가 있는 이야기로 발전했는지 확인하는 생성·진단 순서다.

### `PRESSURE`

`PRESSURE`는 전투·폭력·재난만 뜻하지 않는다.

- 의무와 책임
- 원하는 것과 현재 상태의 간극
- 호기심과 미해결 질문
- 사회적 기대와 역할
- 기회와 유혹
- 관계의 비대칭
- 시간·자원·정보 제약
- 가치관의 모순
- 일상 루틴을 깨는 작은 변화

조용한 관계극·일상물·코미디·탐험·미스터리에서도 같은 원리를 사용할 수 있다.

### `AFFECTED_AGENT`

항상 전통적 단일 주인공일 필요는 없다.

- 개인
- 두 사람의 관계
- 팀
- 가족
- 조직
- 공동체
- 플레이어가 조종하는 여러 인물

중 하나일 수 있다. 핵심은 seed가 **누구의 행동 조건을 바꾸는지**를 특정하는 것이다.

## 2. Seed 예산

처음부터 모든 출발점을 채우지 않는다.

```yaml
primary_seed_count: 1
secondary_seed_count: 0..2
all_seed_completion_required: false
```

Primary Seed 하나로 먼저 story pressure를 만든다. Secondary Seed는 갈등·선택·관계·장면 가치가 실제로 좋아질 때만 0~2개 추가한다. 설정표가 길어지는 것 자체는 진전이 아니다.

## 3. Seed Catalog

### `CHARACTER`

성격, 욕망, 공포, 결점, 과거 경험, 판단 습관에서 시작한다.

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

Want/Need/Lie/Truth 같은 캐릭터 아크 프레임은 필요할 때만 진단 Lens로 사용한다. 모든 인물에게 네 칸을 강제하지 않는다.

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

세계관의 고유명사와 연표가 많아지는 것보다, 생활·책임·선택 조건이 달라지는지가 우선이다.

### `INSTITUTION`

회사, 군대, 가족, 학교, 길드, 문파, 정부, 종교, 범죄조직 등에서 시작한다.

```text
조직은 무엇을 위해 존재하는가?
→ 구성원에게 무엇을 주고 무엇을 요구하는가?
→ 공식 규칙과 실제 관행은 같은가?
→ 개인 가치·관계·생존과 어디에서 충돌하는가?
→ 복종·협상·이탈·개혁 중 어떤 선택이 실제 비용을 만드는가?
```

특정 조직 서사 프레임의 희생 구조나 몇 가지 정해진 결말을 보편 결말로 강제하지 않는다.

### `OCCUPATION_ROLE`

직업, 임무, 사회적 역할, 전문성, 업무 절차에서 시작한다.

```text
무엇을 책임져야 하는가?
→ 평소 어떤 절차로 문제를 푸는가?
→ 절차가 통하지 않는 예외는 무엇인가?
→ 직업윤리와 개인 욕망은 어디서 충돌하는가?
→ 전문성이 해결과 새로운 문제를 동시에 만드는가?
```

직업 이름은 실제 책임·언어·절차·권한·문제 해결법을 대신하지 않는다.

### `ABILITY_RESOURCE_RULE`

능력, 마법, 기술, 장비, 자원, 시스템 규칙, 금지 규칙에서 시작한다.

```text
무엇을 가능하게 하는가?
→ 누가 접근할 수 있고 누가 배제되는가?
→ 존재하는 비용·제약·책임은 무엇인가?
→ 같은 능력을 인물마다 왜 다르게 사용하는가?
→ 사용 뒤 어떤 상태·관계·자원 변화가 남는가?
```

모든 능력에 반드시 대가·부작용을 새로 만들지는 않는다. 현재 정본에 존재하는 비용·한계·책임만 사용하고, 없다면 능력의 사용 우선순위·접근권·사회적 의미·결과에서 압력을 찾을 수 있다.

### `INQUIRY`

수수께끼, 조사 질문, 비밀, 미확인 사실에서 시작한다.

```text
무엇을 알고 싶은가?
→ 왜 지금 알아야 하는가?
→ 누가 답을 숨기거나 잘못 알고 있는가?
→ 답을 알면 무엇을 선택해야 하는가?
→ 답 자체가 새로운 문제를 여는가?
```

질문 자체보다 답을 알아야 할 현재 이유와 답 이후의 판단이 중요하다.

### `EVENT`

사고, 실종, 만남, 전쟁, 재난, 발견, 기회, 상태 변화에서 시작한다.

```text
누구의 기존 상태가 깨졌는가?
→ 되돌리려 하는가, 이용하려 하는가, 받아들이려 하는가?
→ 무엇이 그것을 막는가?
→ 사건보다 중요한 판단 지점은 어디인가?
```

사건 규모는 story value의 대리값이 아니다.

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

장르명만 적지 말고 반복해서 제공할 구체적 경험을 적는다.

## 4. Story Origin Packet

공용 권장 형식은 다음과 같다. 모든 필드를 억지로 채우지 않는다.

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

## 5. Seed에서 이야기로 확장하는 절차

### A. Seed를 한 문장으로 제한한다

처음부터 lore bible을 만들지 않는다.

```text
“기억을 치료하는 마법을 쓸수록 자신의 기억을 잃는다.”
“전투 중 민간인 보호가 최우선인 용병.”
“괴이를 연구하지만 제거를 명령하는 국가기관.”
```

### B. 가장 큰 압력을 받는 Agent를 찾는다

“누가 이 설정 때문에 가장 많이 행동해야 하는가?”를 묻는다. 흥미로운 seed가 있지만 affected agent를 찾을 수 없다면 현재 제작 범위에서는 `LORE_WITHOUT_AGENT` 후보로 본다.

### C. 압력을 행동 목표로 번역한다

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

### D. `RESISTANCE`를 만든다

Resistance는 무조건 악당이 아니다.

- 다른 사람의 합리적인 목표
- 제도와 규칙
- 정보 부족
- 시간
- 자원
- 자신의 습관과 믿음
- 관계에서 지켜야 할 약속
- 선택하면 사라지는 다른 가능성

중 하나일 수 있다.

### E. `CONSEQUENTIAL_CHOICE`를 만든다

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

### F. `STATE / VALUE / RELATIONSHIP_SHIFT`를 확인한다

사건이 컸다는 사실보다 전후 상태가 실제로 달라졌는지 본다. Story Grid의 value shift는 여기서 선택적 진단 Lens로 사용할 수 있지만 모든 장면을 동일 polarity 표에 맞추지 않는다.

### G. `NEXT_PRESSURE`를 생성한다

좋은 결과는 모든 문제를 초기 상태로 리셋하지 않는다.

```text
선택 결과
→ 새 책임 / 새 적대 / 새 의문 / 새 기회 / 잃은 가능성
→ 다음 episode·scene·quest·relationship pressure
```

연속작에서는 `NEXT_PRESSURE`가 Reader Promise를 계속 소비할 수 있는지 본다.

## 6. `RELATIONAL_APPEAL`과의 책임 분리

```text
STORY_ORIGIN_ENGINE
= 무엇에서 이야기를 시작하고 어떻게 압력·선택·변화로 변환할지 생성한다.

RELATIONAL_APPEAL
= 선택된 요소들의 조합이 실제로 더 흥미로운 선택·갈등·대사·행동·결과를 만드는지 검수한다.
```

권장 handoff:

```text
Primary Seed 선정
→ STORY_ORIGIN_ENGINE으로 story pressure 생성
→ 필요한 Secondary Seed만 결합
→ RELATIONAL_APPEAL로 조합의 실제 장면 가치 검수
→ docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md로 장면·대화·선택 실행
→ 매체별 Guide/Skill에서 continuity·reader/player evidence 검수
```

따라서 새 Method는 기존 관계 설계, 대사 설계, 장면 연출을 다시 소유하지 않는다.

## 7. Interactive Narrative 경계

게임에서는 모든 좋은 이야기가 분기형일 필요가 없다.

- 플레이어가 접근 순서를 고를 수 있다.
- 같은 목표를 다른 방법으로 수행할 수 있다.
- 선택은 하나지만 준비 과정에서 판단이 드러날 수 있다.
- 시스템 사용이 후속 자원·관계·정보를 바꿀 수 있다.
- 주인공의 강제 선택을 플레이어가 관찰하되 다른 시스템에서 그 의미를 해석할 수 있다.

`CONSEQUENTIAL_CHOICE`는 `PLAYER_BRANCH_REQUIRED`와 동의어가 아니다. 이 공용 Method는 새 분기, 관계 수치, Save/Data Schema 필드를 자동 요구하지 않는다. 프로젝트의 gameplay·Save/Data authority가 항상 우선한다.

## 8. Failure States

- `LORE_WITHOUT_AGENT`: 세계·역사·마법은 흥미롭지만 현재 행동해야 하는 agent와 연결되지 않는다.
- `TRAIT_WITHOUT_TEST`: 성격 trait가 있으나 그것을 시험하는 상황과 선택이 없다.
- `VALUE_AS_SLOGAN`: 가치관이 설명·대사로만 존재하고 지키거나 버릴 때의 비용이 없다.
- `INSTITUTION_AS_LABEL`: 조직 이름·직급은 있으나 목적·권한·규칙·보상·책임·압력이 없다.
- `JOB_AS_COSTUME`: 직업이 의상·말투·설정 문구일 뿐 문제 해결법과 책임에 영향을 주지 않는다.
- `ABILITY_AS_PREMISE_DECORATION`: 능력 규칙이 멋진 설정으로만 존재하고 실제 선택·자원·관계·결과를 바꾸지 않는다.
- `EVENT_WITHOUT_DECISION`: 사건 규모는 크지만 핵심 agent의 판단·행동이 의미 있는 결과를 만들지 않는다.
- `MYSTERY_WITHOUT_STAKES`: 질문은 있으나 답을 알아야 할 현재 이유와 답 이후의 선택이 없다.
- `SEED_ACCUMULATION_WITHOUT_PRESSURE`: 여러 seed를 계속 추가하지만 story pressure가 강해지지 않고 설정표만 늘어난다.
- `FRAMEWORK_CHECKLIST_OVERFIT`: 외부 작법의 칸을 채우기 위해 프로젝트 정본·장르 약속·매체 장점을 억지로 변형한다.

## 9. 프레임워크 사용 상한

다음을 Base 보편 법칙으로 만들지 않는다.

- 모든 이야기는 캐릭터에서 시작해야 한다.
- 모든 캐릭터는 Want/Need/Lie/Truth 네 항목을 가져야 한다.
- 모든 기관 이야기는 희생이나 정해진 몇 개 결말로 끝나야 한다.
- 모든 장면은 같은 beat 수를 가져야 한다.
- 모든 이야기는 Three Act / Hero's Journey / Save the Cat beat를 따라야 한다.
- 모든 능력은 대가·부작용을 가져야 한다.
- 모든 사건은 폭력적 stakes를 가져야 한다.
- 모든 게임 서사는 플레이어 분기를 가져야 한다.
- 모든 seed 조합을 미리 설계해야 한다.

MICE, Snowflake, Story Genius, Want/Need/Lie/Truth, Truby, Save the Cat, Story Grid는 현재 문제를 더 잘 보게 할 때만 선택한다. 프레임워크보다 프로젝트 정본, Reader/Player Promise, 실제 원고·게임 상태가 우선한다.

## 10. 검증

story origin을 사용할 때 필요한 범위만 기록한다.

```yaml
story_origin_validation:
  primary_seed:
  secondary_seeds: []
  affected_agent:
  pressure:
  consequential_choice_or_commitment:
  observable_shift:
  next_pressure:
  reader_or_player_value:
  relational_appeal_needed:
  project_canon_conflict:
  project_pilot_status:
  human_reader_or_player_status:
```

Base contract가 Green이어도 프로젝트별 이야기 품질·독자/플레이어 반응·상업 효과를 자동 증명하지 않는다. 실제 효과는 프로젝트 story packet과 원고/게임 build, 사람 반응으로 검증한다.

## 11. 완료 기준

- 하나의 Primary Seed에서 affected agent와 pressure를 설명할 수 있다.
- story pressure가 목표·저항·선택 또는 commitment로 번역된다.
- 사건·장면 전후의 observable shift를 설명할 수 있다.
- 결과가 reset되지 않고 필요한 경우 next pressure로 이어진다.
- Secondary Seed는 장면 가치를 높일 때만 추가한다.
- `RELATIONAL_APPEAL`과 장면 실행 Method의 책임을 침범하지 않는다.
- 게임에 불필요한 분기·관계 수치·Save/Data Schema를 강제하지 않는다.
- 외부 작법 프레임워크를 universal formula로 승격하지 않는다.

## 12. Rollback

이 Method를 사용한 공용 Base 변경은 Method와 consumer link를 하나의 변경 단위로 되돌릴 수 있어야 한다. 이 Method 자체는 프로젝트 Canon·Save/Data Schema·런타임 상태를 자동 변경하지 않으므로 별도 데이터 migration을 요구하지 않는다.
