# 서사·세계관 Knowledge Model · 조사 → 정본 → 요약 → 상세 → 시각화

- 상태: 공용 방법
- 목적: 인물·세력·장소·세계 규칙·사건·관계·근거를 서로 다른 책임으로 구조화해 장문 Bible 오염과 이미지 선행 오류를 줄인다.
- 적용: 서사 게임, 소설, TRPG 기반 각색, 세계관 중심 프로젝트, NPC·세력·지역이 장기 누적되는 프로젝트
- 비적용: 단순 문장 교정, 일회성 짧은 설정 메모, 정본 영향이 없는 단발 이미지

이 Method는 새 서사 작성 Skill이 아니다. 기존 책임과 다음처럼 연결한다.

- 장면·대사·관계 실행: `NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- 캐릭터·서사 아트: `CHARACTER_AND_NARRATIVE_ART_METHOD.md`
- 외부 Source 탐색: `../game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`
- 연재소설 실행: `../../../skills/developing-and-revising-serial-fiction/SKILL.md`
- 정본 freshness·legacy: `../../../skills/auditing-canonical-reference-freshness/SKILL.md`

프로젝트의 최신 사용자 Decision·`AGENTS.md`·Current Canon이 이 Method보다 우선한다.

## 1. 왜 분리하는가

다음 질문은 한 페이지에 섞기 쉽지만 서로 다른 데이터다.

```text
“밀리는 누구인가?”              → Entity
“제10화에서 무엇을 했나?”       → Event
“이안과 어떤 관계인가?”         → Relation
“같은 얼굴은 무엇을 뜻하나?”    → Rule / Unknown
“왜 그렇게 말할 수 있나?”       → Evidence
```

한 Character Bible에 전부 복사하면 다음 문제가 생긴다.

- 사건이 바뀔 때 인물 페이지 전체가 stale해진다.
- 관계의 방향성과 시점이 사라진다.
- 인물의 주장과 세계의 실제 규칙이 섞인다.
- legacy/candidate 문장이 current fact처럼 보인다.
- 생성 이미지가 먼저 만들어진 뒤 텍스트가 이미지를 따라가는 역전이 생긴다.

따라서 개념은 다섯 층으로 분리한다.

```text
ENTITY
EVENT
RELATION
RULE
EVIDENCE
```

물리 저장소는 유지보수 비용을 줄이기 위해 세 개로 압축한다.

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

인물·세계관을 읽기 전에 자료의 권위 순서를 먼저 기록한다.

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

처음에는 장문 설명을 쓰지 않는다. 실제 존재하는 대상만 식별한다.

```yaml
name:
type: Character | Faction | Location | World Rule | Relationship | Item | Clue | Setting
aliases:
scope:
current_state:
source_presence:
```

핵심 질문은 `무엇이 실제로 존재하는가?`다.

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

캐릭터 페이지에는 Event 전체 문장을 복제하지 않는다. 중요한 Event를 Relation으로 연결하고 사람용 화면에는 5~8개의 핵심 행적만 요약한다.

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
- Part·Arc·시대 경계
- 관계 시작·파탄·고백·동맹
- 미스터리 정답·미확정 경계

근거가 없으면 `UNKNOWN` 또는 `UNVERIFIED`로 둔다.

### 2.6 `CONTRADICTION_AUDIT`

최소 검수 항목:

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

- 누구·무엇인가
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

`Text Approval != APPROVED`이면 기본적으로 `READY_FOR_VISUAL`로 전진하지 않는다.

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
Relation Type:
Source → Target:
Target → Source:
Relation State:
Power / Debt / Dependency:
Gate Check:
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

`Character Engine`은 필요할 때 다음을 사용한다.

- public role / private self
- core desire / actual need
- fear / avoidance
- contradiction / self-deception
- moral boundary
- attention filter
- decision rule
- competence / limitation / cost of strength
- voice / body language / social mask

전부 채우는 것이 목표가 아니다. 실제 장면 구분과 선택에 필요한 항목만 쓴다.

### World / Faction / Location / Rule detail

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

Authority Tier:

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

## 6. 승인·시각 Gate

`Text Approval`과 `Visual Gate`는 별도 축이다.

| Text Approval | 허용 Visual Gate | 의미 |
| --- | --- | --- |
| DRAFT | BLOCKED_BY_TEXT | 조사·초안 단계 |
| REVIEW_REQUIRED | BLOCKED_BY_TEXT | 사용자 판단 대기 |
| APPROVED | BLOCKED_BY_TEXT / READY_FOR_VISUAL / VISUAL_CANDIDATE / VISUAL_APPROVED | 승인 텍스트 기반 시각 작업 가능 |
| REPLACED | REPLACED | 현재 제작 입력으로 사용 금지 |

`Gate Check`는 모순 상태를 `INVALID`로 표시해야 한다.

최소 위반 예:

- DRAFT + READY_FOR_VISUAL
- REVIEW_REQUIRED + VISUAL_CANDIDATE
- REPLACED + VISUAL_APPROVED

이 감사 필터는 시각 제작 전에 확인한다.

## 7. Notion 사람용 UX · 요약 → 상세 팝업

사람용 Home/Bible 첫 화면은 `Gallery` 또는 짧은 Primer를 우선한다.

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

Notion Gallery는 database page를 `Center Peek`로 열 수 있다. 별도 복제 페이지를 만들어 popup을 흉내내지 않는다.

상세 페이지 안에서도 첫 화면을 짧게 유지한다. 긴 `Major Events`, `Evidence`, `Conflict Notes`, `Visual Variants`는 toggle 또는 별도 linked view로 접는다.

프로젝트 Home 자체도 같은 원칙을 따른다.

```text
프로젝트 요약
→ 현재 상태
→ 대표 승인 시각자료
→ 빠른 탐색
→ 핵심 시스템·Flow 상세 보기(toggle)
→ 하위 전문 페이지
```

`Project Registry`의 runtime·binding·SHA·PR·CI·path 같은 시스템 속성은 Project Home의 기본 화면으로 복제하지 않는다.

모바일·앱의 정확한 폭·크롭·스크롤 위치를 실제로 보지 않았다면 `UI_GEOMETRY_NOT_VERIFIED`를 유지한다.

## 8. 3안 비교와 기본 선택

### A · 5개 DB 완전 분리

- 장점: Entity, Event, Relation, Rule, Evidence가 가장 엄격하게 분리된다.
- 단점: solo/small-team 프로젝트에서 관계·필터·마이그레이션 비용이 높다.
- 판정: 대형 프로젝트에서 선택적 사용.

### B · 3 DB / 5 conceptual layers

- 장점: Entity/Flow 분리와 Evidence 추적을 유지하면서 운영 복잡도가 낮다.
- 단점: Knowledge Master가 type-aware template을 필요로 한다.
- 판정: **ADOPT / DEFAULT**.

### C · Asset Library 확장

- 장점: 새 DB가 필요 없다.
- 단점: 이미지·Reference와 서사 정본이 다시 섞이고 Visual이 Canon처럼 보일 위험이 크다.
- 판정: **REJECT**.

## 9. 벤치마크에서 흡수한 원리

### articy:draft 계열 Narrative Tool

- Entity와 Flow를 분리한다.
- References로 story/location/dialogue/entity를 연결한다.
- Template은 project-specific field만 추가한다.

흡수: `Knowledge Master ↔ Event Ledger` 분리와 관계 연결.

### World Anvil 계열 World Bible

- 짧은 article introduction/primer를 먼저 보여준다.
- Character/Organization/Location 등 type별 article을 연결한다.
- 관계·조직 관계·timeline을 상세 도구로 분리한다.

흡수: Primer-first와 type-aware 상세 페이지.

### Notion 관계형 Workspace

- Relation으로 정본 객체를 연결한다.
- Gallery는 사람이 빠르게 훑는 표면으로 사용한다.
- Linked view는 프로젝트·Type·승인 상태별로 같은 데이터를 재사용한다.

흡수: 하나의 공용 데이터 저장소 + 프로젝트별 filtered human view.

### 실무형 Living Documentation

- 요약 문서와 근거·변경 기록을 분리한다.
- 동일 사실을 여러 문서에 복사하기보다 정본 객체를 연결한다.
- 검증되지 않은 상태를 빈칸이나 확정 사실로 위장하지 않는다.

흡수: `UNKNOWN / UNVERIFIED / CONFLICT`를 실제 상태로 유지한다.

## 10. 프로젝트 적용 규칙

### 공통

1. 프로젝트 current canon과 decision source를 먼저 찾는다.
2. Entity를 추출한다.
3. Event를 분리한다.
4. Relation과 Rule을 구조화한다.
5. 고위험 Claim에 Evidence를 연결한다.
6. Contradiction Audit를 수행한다.
7. 사람이 읽는 Primer를 작성한다.
8. 사용자가 의미를 승인한다.
9. 승인 후에만 visual production을 연다.

### COC-Fiction pilot

COC는 다음 경계를 보호한다.

- Part 1 / Bridge / Part 2 / Rift Accord를 섞지 않는다.
- 동일 얼굴·유사 이름·임시 협력 표현을 동일 인물·동일 세력 증거로 쓰지 않는다.
- 이미지 후보에서 인물 성격·성별·세력·능력을 역추론하지 않는다.
- 사용자 승인 전 Part 1 조사 결과를 `APPROVED`로 올리지 않는다.
- 인물과 세계관·세력은 요약 Gallery에서 시작하고 상세는 `Center Peek`로 연다.

## 11. 품질 Gate

### 구조 Gate

- [ ] Entity와 Event가 복제되지 않았는가
- [ ] Relation 방향이 필요한데 단순 tag로 축약되지 않았는가
- [ ] Rule과 Character Belief가 분리됐는가
- [ ] Evidence가 고위험 Claim과 연결됐는가

### Canon Gate

- [ ] current / candidate / legacy가 구분됐는가
- [ ] unknown을 임의로 채우지 않았는가
- [ ] image/AI summary가 canon authority로 승격되지 않았는가
- [ ] Part·Arc·시대 경계가 보존됐는가

### Human UX Gate

- [ ] 첫 화면이 Primer·요약 중심인가
- [ ] 상세는 Gallery click / Center Peek / toggle로 내려갔는가
- [ ] 시스템 메타데이터가 Home 기본 화면에 노출되지 않는가
- [ ] 사람이 수정해야 할 정본 링크가 짧게 보이는가

### Visual Gate

- [ ] `Text Approval=APPROVED`가 확인됐는가
- [ ] Visual Contract가 텍스트와 충돌하지 않는가
- [ ] `Gate Check=INVALID` 레코드가 없는가
- [ ] visual approval을 runtime·reader validation으로 과장하지 않는가

## 12. Implementation Reality Gate

다음 주장은 서로 대체하지 않는다.

- Method exists ≠ every project migrated
- DB exists ≠ project knowledge extracted
- Entity/Event extracted ≠ canon approved
- Text approved ≠ visual approved
- Visual approved ≠ runtime/reader validation
- Center Peek capability ≠ mobile layout verified

현재 프로젝트에 실제 데이터 이관·사용자 승인·이미지 제작·runtime 검증이 없으면 그 단계는 완료로 보고하지 않는다.
