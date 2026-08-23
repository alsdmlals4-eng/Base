# 서사·세계관 Knowledge Model · 조사 → 정본 → 요약 → 상세 → 시각화

- 상태: 공용 방법
- 목적: 인물·세력·장소·세계 규칙·사건·관계·근거를 서로 다른 책임으로 구조화해, 장문 Bible 오염과 이미지 선행 오류를 줄인다.
- 적용: 서사 게임, 소설, TRPG 기반 각색, 세계관 중심 프로젝트, NPC/세력/지역이 장기 누적되는 프로젝트
- 비적용: 단순 문장 교정, 일회성 짧은 설정 메모, 정본 영향이 없는 단발 이미지

이 Method는 새 서사 작성 Skill이 아니다. 기존 책임과 다음처럼 연결된다.

- 장면·대사·관계 실행: `NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- 캐릭터·서사 아트: `CHARACTER_AND_NARRATIVE_ART_METHOD.md`
- 외부 Source 탐색: `../game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`
- 연재소설 실행: `../../../skills/developing-and-revising-serial-fiction/SKILL.md`
- 정본 freshness·legacy: `../../../skills/auditing-canonical-reference-freshness/SKILL.md`

프로젝트의 최신 사용자 Decision·`AGENTS.md`·Current Canon이 이 Method보다 우선한다.

## 1. 핵심 문제

다음은 같은 데이터처럼 보여도 같은 책임이 아니다.

```text
“밀리는 누구인가?”        → Entity
“제10화에서 무엇을 했나?” → Event
“이안과 어떤 관계인가?”   → Relation
“같은 얼굴은 무엇을 뜻하나?” → Rule / Unknown
“왜 그렇게 말할 수 있나?” → Evidence
```

한 Character Bible 페이지에 이 다섯 종류를 전부 복사하면 다음 문제가 생긴다.

- 사건이 바뀔 때 인물 페이지 전체가 stale해진다.
- 관계의 방향성과 시점이 사라진다.
- 인물의 주장과 세계의 실제 규칙이 섞인다.
- legacy/candidate 문장이 current fact처럼 보인다.
- 이미지가 먼저 만들어진 뒤 텍스트가 그 이미지를 따라가는 역전이 생긴다.

따라서 개념은 다섯 층으로 분리한다.

```text
ENTITY
EVENT
RELATION
RULE
EVIDENCE
```

물리 저장소는 유지보수 비용을 줄이기 위해 세 개로 압축할 수 있다.

```text
NARRATIVE KNOWLEDGE · Master
  = Entity + Relation + Rule

NARRATIVE EVENT · Ledger
  = Event

CANON EVIDENCE · Ledger
  = Evidence
```

## 2. 표준 조사 흐름

```text
AUTHORITY_MAP
→ ENTITY_EXTRACTION
→ EVENT_EXTRACTION
→ RELATION_RULE_EXTRACTION
→ EVIDENCE_LINK
→ CONTRADICTION_AUDIT
→ HUMAN_PRIMER
→ USER_APPROVAL
→ VISUAL_GATE
```

### 2.1 `AUTHORITY_MAP`

인물·세계관을 읽기 전에 먼저 자료의 권위 순서를 적는다.

기본값:

```text
latest user decision
→ project current canon
→ approved planning
→ current candidate
→ legacy material
→ external reference
```

프로젝트 `AGENTS.md`가 더 구체적인 우선순위를 선언하면 그것이 우선한다.

`AI summary`, `generated image`, `visual index`, `benchmark`, `old chat`는 그 자체로 Canon 권위를 얻지 않는다.

### 2.2 `ENTITY_EXTRACTION`

처음에는 설명문을 쓰지 않는다. 실제 존재하는 대상만 식별한다.

```yaml
name:
type: Character | Faction | Location | World Rule | Relationship | Item | Clue | Setting
aliases:
scope:
current_state:
source_presence:
```

이 단계의 질문은 `무엇이 실제로 존재하는가?`이다.

### 2.3 `EVENT_EXTRACTION`

장면·회차·퀘스트에서 행적을 별도 Event로 기록한다.

```yaml
starting_state:
pressure_or_goal:
choice_or_action:
outcome:
cost_or_consequence:
state_change:
relationship_change:
```

캐릭터 페이지에는 Event 전체 문장을 복제하지 않는다. 중요한 Event를 Relation으로 연결하고, 사람용 페이지에서는 5~8개 핵심 행적만 요약한다.

### 2.4 `RELATION_RULE_EXTRACTION`

관계는 태그 하나가 아니라 방향이 있는 상태다.

```yaml
source:
target:
relationship_type:
source_view_of_target:
target_view_of_source:
power_debt_dependency:
current_state:
change_events:
```

`A → B`와 `B → A`가 다를 수 있다.

세계 규칙은 가능·금지·비용·예외로 기록한다.

```yaml
rule_domain:
allows:
forbids:
cost:
exception:
knowledge_holders:
first_observed:
first_confirmed:
```

인물이 믿는 것, 작중 문서가 주장하는 것, 실제로 관측된 현상은 같은 등급으로 합치지 않는다.

### 2.5 `EVIDENCE_LINK`

다음 고위험 Claim에는 근거를 연결한다.

- 이름·별칭·변장
- 성별·정체성·표현 상태가 서사 기능에 영향을 주는 경우
- 생존·사망·소실·부활
- 세력 소속·계약·이탈
- 능력의 가능 범위·비용·공개 시점
- Part/Arc/시대 경계
- 관계 시작·파탄·고백·동맹
- 미스터리 정답·미확정 경계

근거가 없으면 `UNKNOWN` 또는 `UNVERIFIED`로 둔다.

### 2.6 `CONTRADICTION_AUDIT`

최소 검수:

```text
name / alias drift
sex-gender-presentation drift when identity-relevant
scope / part / arc drift
alive / dead / missing / unknown drift
faction membership drift
ability and reveal timing drift
relationship state drift
event order drift
candidate promoted as canon
legacy promoted as current
image or AI summary promoted as canon
```

Conflict는 더 그럴듯한 문장을 선택해 지우지 않는다. Evidence Ledger에 양쪽을 남기고 현재 권위로 판정한다.

### 2.7 `HUMAN_PRIMER`

충돌 검수 뒤에야 사람이 처음 보는 요약을 쓴다.

좋은 Primer는 3~6문장 안에 다음을 답한다.

- 누구/무엇인가
- 작품에서 왜 중요한가
- 현재 핵심 상태가 무엇인가
- 무엇을 오해하면 안 되는가

Primer에 전체 연표·모든 비밀·모든 Source를 넣지 않는다.

### 2.8 `USER_APPROVAL`

사람용 설명과 이미지의 의미를 바꾸는 사실은 사용자 승인 전 `REVIEW_REQUIRED`로 둔다.

```text
DRAFT
→ REVIEW_REQUIRED
→ APPROVED
→ REPLACED
```

최신 사용자 교정은 Evidence와 Current Canon 이관 대상으로 기록한다.

### 2.9 `VISUAL_GATE`

```text
BLOCKED_BY_TEXT
→ READY_FOR_VISUAL
→ VISUAL_CANDIDATE
→ VISUAL_APPROVED
→ REPLACED
```

`Text Approval != APPROVED`면 기본적으로 `READY_FOR_VISUAL`로 전진하지 않는다.

이미지가 승인 텍스트와 충돌하면 텍스트가 우선한다. 이미지에서 새 설정을 역추론해 Canon에 추가하지 않는다.

## 3. `NARRATIVE KNOWLEDGE · Master`

인물·세력·장소·세계 규칙·관계·아이템·단서·Setting의 안정된 정체성과 사람용 Primer를 보관한다.

권장 속성:

```yaml
Name:
Project:
Type:
Scope:
Summary:
Core Function:
Aliases:
Current State:
Canon Status:
Text Approval:
Visual Gate:
Related Knowledge:
Relation Source:
Relation Target:
```

`Canon Status` 기본값:

- `CORE_CONFIRMED`
- `CONFIRMED`
- `CURRENT_CANDIDATE`
- `INFERRED`
- `UNKNOWN`
- `CONFLICT`
- `DEPRECATED`

### Character detail

```text
Primer
→ Character Engine
→ Major Events
→ Relationships
→ Current State
→ Visual Contract
→ Distortion Guards
→ Evidence / Conflict Notes
```

`Character Engine` 권장 요소:

- public role / private self
- core desire / actual need
- fear / avoidance
- contradiction / self-deception
- moral boundary
- attention filter
- decision rule
- competence / limitation / cost of strength
- voice / body language / social mask

전부 채우는 것이 목표가 아니다. 실제 장면 구분과 선택에 필요한 항목만 사용한다.

### World/Faction/Location/Rule detail

```text
Primer
→ Function in the world
→ Observable rules / constraints
→ Major Events
→ Relations
→ Unknowns / conflicts
→ Visual contract if needed
→ Evidence
```

세계관은 백과사전 분량보다 `인물의 생활·선택·위험·기회가 어떻게 달라지는가`로 검수한다.

## 4. `NARRATIVE EVENT · Ledger`

Event는 chronology와 state change의 정본이다.

권장 속성:

```yaml
Name:
Project:
Scope:
Sequence:
Event Type:
Summary:
Participants:
Canon Status:
Starting State:
Choice / Action:
Outcome:
Cost / Consequence:
State Change:
Relationship Change:
```

Event Type 예:

- Plot
- Character
- Relationship
- World
- Faction
- Reveal
- Choice
- Battle
- Other

`Sequence`는 반드시 날짜일 필요가 없다. Chapter, Scene ID, Quest Step, Era key 등 프로젝트가 재현 가능한 순서를 사용한다.

## 5. `CANON EVIDENCE · Ledger`

근거를 사람용 Primer에 쌓지 않고 별도 관리한다.

권장 속성:

```yaml
Name:
Project:
Claim:
Knowledge Targets:
Event Targets:
Source Type:
Source Locator:
Authority Tier:
Verdict:
Checked At:
Notes:
```

Source Type:

- `USER_DECISION`
- `GITHUB_CANON`
- `GITHUB_MANUSCRIPT`
- `NOTION_DECISION`
- `RUNTIME_EVIDENCE`
- `EXTERNAL_SOURCE`

Authority Tier 기본값:

- `A0_USER`
- `A1_CANON`
- `A2_APPROVED_PLANNING`
- `A3_CURRENT_CANDIDATE`
- `A4_LEGACY`
- `A5_EXTERNAL`

Verdict:

- `SUPPORTS`
- `CONFLICTS`
- `UNVERIFIED`
- `SUPERSEDED`

## 6. Notion 사람용 UX · 요약 → 상세 팝업

사람용 Home/Bible 첫 화면은 `Gallery`를 우선한다.

카드에 보일 정보:

```text
Name
Summary
Core Function
Scope
Canon Status
Text Approval
```

상세 본문과 Evidence는 카드에 노출하지 않는다.

Notion Gallery의 카드 클릭을 `상세 보기` 동작으로 사용한다.

```text
요약 카드
→ 카드 클릭
→ Center Peek 중앙 상세
→ Primer 확인
→ 필요한 상세 섹션만 펼치기
```

Notion Gallery는 기본적으로 database page를 `Center peek`로 여는 UI를 제공한다. 별도 복제 페이지를 만들어 popup을 흉내내지 않는다.

상세 페이지 안에서도 첫 화면을 짧게 유지한다. 긴 `Major Events`, `Evidence`, `Conflict Notes`, `Visual Variants`는 toggle 또는 별도 linked view로 접는다.

모바일·앱의 정확한 폭·크롭·스크롤 위치를 실제로 보지 않았다면 `UI_GEOMETRY_NOT_VERIFIED`를 유지한다.

## 7. 3안 비교와 기본 선택

### A · 5개 DB 완전 분리

장점: 가장 엄격한 schema.  
단점: solo/small-team 프로젝트에서 관계·필터·마이그레이션 비용이 높다.  
판정: 대형 프로젝트에서 선택적 사용.

### B · 3 DB / 5 conceptual layers

장점: Entity/Flow 분리와 Evidence 추적을 유지하면서 운영 복잡도가 낮다.  
단점: Knowledge Master가 type-aware template을 필요로 한다.  
판정: **ADOPT / DEFAULT**.

### C · Asset Library 확장

장점: 새 DB 없음.  
단점: 이미지·Reference와 서사 정본이 다시 섞이고 Visual이 Canon처럼 보인다.  
판정: **REJECT**.

## 8. 벤치마크에서 흡수한 원리

### articy:draft

- Entity와 Flow를 분리한다.
- References로 story/location/dialogue/entity를 연결한다.
- Template은 project-specific field만 추가한다.

흡수: `Knowledge Master ↔ Event Ledger` 분리와 Relation.

### World Anvil

- 짧은 article introduction/primer를 먼저 보여준다.
- Character/Organization/Location 등 type별 article을 연결한다.
- 관계·조직 관계·timeline을 상세 도구로 분리한다.

흡수: Summary-first + typed detail + relation/event separation.

### Notion

- DB item은 자체 page다.
- Gallery card는 적은 property만 보여줄 수 있다.
- Gallery는 Center Peek 상세 진입에 적합하다.
- page layout/detail panel로 고밀도 property를 접을 수 있다.

흡수: 한 데이터의 overview/detail 이중 View. 복제 문서 금지.

## 9. COC-Fiction 첫 적용 Gate

COC는 기존 오염된 Visual을 먼저 지우는 방식이 아니라 Source authority를 회복한다.

```text
3 common DB 생성
→ COC filtered views 연결
→ Asset Library를 Visual 전용으로 재정의
→ Part 1 Entity/Event/Evidence 텍스트 조사
→ 사용자 승인
→ Text Approval = APPROVED
→ Visual Gate = READY_FOR_VISUAL
→ 캐릭터/세계관 이미지 제작
```

승인 전 COC 상세 prose를 새 Knowledge record에 확정본처럼 넣지 않는다.

고위험 교정 예:

- 실제 정체성과 위장/표현 상태를 같은 필드로 합치지 않는다.
- 가면·변장·Reveal Variant는 실제 identity와 분리한다.
- Part/Bridge/후속 Part를 이미지 구성 편의로 섞지 않는다.
- migration boundary 양쪽을 같은 Canon Status로 평탄화하지 않는다.

## 10. Implementation Reality Gate

다음을 구분한다.

```text
Method 존재 != 프로젝트 조사 완료
DB 생성 != 데이터 추출 완료
Entity 추출 != Canon 승인
Event 연결 != 전체 continuity PASS
Text 승인 != Visual 승인
Visual 승인 != Runtime/독자 검증
Center Peek 지원 != 모바일 UI geometry 검증
```

## 11. 완료 조건

- 프로젝트가 인물·세계관을 정리할 때 raw source에서 바로 장문 Bible을 쓰지 않는다.
- 인물의 주요 행적은 Event Ledger와 연결된다.
- 관계는 방향성과 변경 Event를 가진다.
- 세계 규칙은 인물 주장과 분리된다.
- high-risk claim은 Evidence에서 근거·충돌을 확인할 수 있다.
- 사람용 첫 화면은 Primer 카드 중심이다.
- 상세는 같은 DB page의 popup/peek에서 확인한다.
- 승인 전 Visual 생성이 기본적으로 차단된다.
- Asset Library와 Narrative Canon의 책임이 분리된다.
