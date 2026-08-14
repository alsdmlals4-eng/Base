# 캐릭터 관계적 매력 공용 원칙 설계

- 날짜: 2026-08-15
- 상태: `WRITTEN_SPEC_REVIEW_REQUIRED`
- 대상 저장소: `alsdmlals4-eng/Base`
- 목적: “이야기는 캐릭터가 만든다”를 단순 표어가 아니라 소설·게임 서사에서 함께 소비할 수 있는 공용 작법 원칙으로 정식화한다.

## 1. 배경

현재 Base에는 이미 다음 책임이 존재한다.

- `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`: 장면·대사·선택·관계를 공용 서사 방법으로 다룬다.
- `skills/developing-and-revising-serial-fiction/SKILL.md`: 연재소설의 POV·캐릭터 voice·개성·관계·장면 집필을 소유한다.
- `skills/developing-and-revising-serial-fiction/references/character-distinctiveness-and-opponent-threat.md`: attention filter, problem-solving method, strength proof, human charm, flaw, signature highlight를 통해 캐릭터 식별성을 감사한다.
- `docs/knowledge/game-development/NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md`: 캐릭터·관계 연구 Source를 발견하고 기존 consumer로 연결하지만, 실제 작법 권위는 기존 Method·Skill·Guide에 둔다.

현행 구조는 캐릭터를 “개별 인물의 욕망·판단·목소리·행동 방식”으로 구분하는 데 강하다. 그러나 **캐릭터 × 캐릭터 / 캐릭터 × 세계·배경 / 캐릭터 × 능력·역할의 조합이 새로운 선택·갈등·행동·대사·결과를 만들어야 한다**는 공용 원칙은 명시적으로 정의되어 있지 않다.

## 2. 결정

새 Skill이나 새 Work Mode를 만들지 않는다.

공용 owner는 `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`로 둔다. 이 문서에 `RELATIONAL_APPEAL` 원칙을 추가하고, 연재소설 Skill과 캐릭터 감사 reference가 이를 실제 집필·검수에서 소비하도록 연결한다.

```text
COMMON OWNER
NARRATIVE_AND_RELATIONSHIP_METHOD
        ↓
SERIAL FICTION CONSUMER
SKILL + character audit reference
        ↓
PROJECT CONSUMER
게임/소설별 캐릭터·관계·장면 정본
```

`NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR`는 연구 Source 발견 계층이므로 작법 원칙의 새 권위로 승격하지 않는다.

## 3. 공용 원칙

사람이 읽는 기본 문구는 다음 의미를 유지한다.

> 캐릭터는 단독 설정표보다 관계와 상황 속에서 증명한다. 캐릭터 × 캐릭터, 캐릭터 × 세계·배경, 캐릭터 × 능력·역할의 조합에서 서로의 욕망·결점·강점·가치관·제약이 충돌하거나 보완되며 생기는 관계적 매력을 찾는다. 좋은 조합은 설정을 더 붙이는 데서 끝나지 않고 새로운 선택·갈등·대사·행동·결과를 자연스럽게 발생시켜야 한다.

기계적으로 사용할 식별자는 `RELATIONAL_APPEAL`로 통일한다.

## 4. 세 조합 축

### 4.1 `CHARACTER_X_CHARACTER`

두 인물의 설정을 나란히 놓는 것이 아니라 상호작용 때문에 각각의 다른 면이 드러나는지 본다.

검토 대상:

- 욕망과 우선순위의 충돌·보완
- 가치관·도덕 경계의 차이
- 신뢰·경계·부채·경쟁·보호·의존 등 관계 압력
- 권력·정보·책임의 비대칭
- 상대에게만 나오는 말투·행동·취약성
- 함께 있을 때만 가능한 선택·실패·하이라이트

### 4.2 `CHARACTER_X_WORLD`

배경·세계관을 이력서 장식으로 붙이지 않고 인물의 실제 선택 비용과 생활 방식에 연결한다.

검토 대상:

- 출신·계층·직업·조직·문화·세대 경험
- 제도·금기·자원·기술·괴이·마법 규칙
- 같은 세계 조건을 인물마다 다르게 해석하는 방식
- 세계 조건 때문에 가능한 선택과 불가능한 선택
- 배경이 관계·책임·위험·기회에 남기는 흔적

### 4.3 `CHARACTER_X_ABILITY`

능력·전투 역할·전문 기술을 캐릭터와 분리된 기능 목록으로 두지 않는다.

검토 대상:

- 능력을 어떤 문제에 먼저 쓰는가
- 무엇에는 일부러 사용하지 않는가
- 능력의 비용·한계·부작용을 어떻게 받아들이는가
- 같은 능력이라도 가치관과 경험 때문에 다른 해결법이 나오는가
- 강점이 결점·책임·관계 문제를 새로 만드는가
- 능력 사용의 결과가 이후 관계·신념·자원 상태에 남는가

## 5. 성공 판정

조합을 잘 설계했다는 이유로 설정 항목 수를 세지 않는다.

최소 하나 이상의 **관찰 가능한 차이**가 있어야 한다.

```yaml
relational_appeal_proof:
  new_choice:
  new_conflict_or_cooperation:
  new_dialogue_or_behavior:
  new_consequence:
```

모든 항목을 강제하지 않는다. 현재 장면·아크·시스템에서 필요한 증거 하나 이상이면 된다.

다음은 실패 신호다.

- `DECORATIVE_SYNERGY`: 설정상 관계·배경·능력 조합은 있으나 실제 장면과 선택이 달라지지 않는다.
- `FORCED_CHEMISTRY`: 조합을 보여주기 위해 인물의 기존 욕망·판단·정본을 억지로 비튼다.
- `BIOGRAPHY_WITHOUT_PRESSURE`: 과거·계층·문화 설정이 현재 선택과 비용에 영향을 주지 않는다.
- `ABILITY_AS_GIMMICK`: 능력이 캐릭터의 가치·비용·문제 해결 방식과 무관한 장식이다.
- `RELATIONSHIP_TAG_ONLY`: 신뢰·경쟁 같은 태그만 바뀌고 대사·행동·정보·후속 장면의 차이가 없다.
- `CROSS_PRODUCT_OVERDESIGN`: 모든 캐릭터 조합을 의무적으로 설계해 장면·콘텐츠 예산을 폭증시킨다.

## 6. YAGNI와 보호 대상

다음을 강제하지 않는다.

- 모든 캐릭터 쌍에 고유 이벤트를 만들기
- 모든 관계에 수치·호감도·성능 보너스를 추가하기
- 모든 능력에 서사적 트라우마나 대가를 붙이기
- 모든 배경 설정을 장면에 노출하기
- 기존 프로젝트의 확정 캐릭터·세계관·관계 정본을 공용 원칙에 맞추기 위해 소급 변경하기

공용 원칙은 **새 설계와 실질적으로 재작성하는 장면을 더 잘 판단하기 위한 Lens**다. 프로젝트 정본보다 높은 권한을 갖지 않는다.

## 7. 구현 범위

최소 구현 대상:

1. `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
   - 공용 `RELATIONAL_APPEAL` 정의와 세 조합 축을 추가한다.
   - 기존 캐릭터 목소리·관계 설계와 중복하지 않도록 “조합이 실제 선택·행동·결과를 만드는가”에 책임을 한정한다.
2. `skills/developing-and-revising-serial-fiction/SKILL.md`
   - 새 Skill Mode를 만들지 않고 기존 `pov-and-character-voice` 또는 `character-and-opponent-integrity`에서 공용 원칙을 선택적으로 소비하도록 연결한다.
3. `skills/developing-and-revising-serial-fiction/references/character-distinctiveness-and-opponent-threat.md`
   - 캐릭터 식별 카드 또는 별도 짧은 감사 절에 관계적 매력 증거를 추가한다.
4. 필요한 기존 계약 테스트
   - 새 문서·Skill을 등록하는 테스트가 아니라, 공용 owner와 기존 serial-fiction consumer의 연결이 유지되는지만 검증한다.

명시적 제외:

- 새 Skill 생성
- 새 Skill Mode 생성
- Registry 항목 추가
- 새 Source Radar 생성
- 게임 프로젝트별 캐릭터 데이터 스키마 변경
- 호감도/관계 수치 시스템 구현
- 기존 원고 일괄 재작성

## 8. 검증

구현 완료 조건:

```text
COMMON_OWNER_PRESENT
AND THREE_RELATIONAL_AXES_PRESENT
AND OBSERVABLE_PROOF_REQUIRED
AND SERIAL_FICTION_CONSUMER_LINKED
AND NO_NEW_SKILL
AND NO_NEW_MODE
AND NO_REGISTRY_EXPANSION
AND EXISTING_TESTS_GREEN
```

회귀 검토에서는 다음 질문을 사용한다.

1. 이 원칙이 기존 캐릭터 개성 규칙을 단순 반복하는가?
2. “시너지”라는 이름으로 모든 조합을 과설계하게 만드는가?
3. 세계관 설정량을 늘리는 방향으로 잘못 읽힐 수 있는가?
4. 능력에 불필요한 서사 대가를 강제하는가?
5. 관계 태그나 호감도 수치가 실제 관계 경험을 대체하게 만드는가?
6. 선형 소설과 인터랙티브 게임의 매체 차이를 침범하는가?

하나라도 Yes이면 최소 수정 후 재검사한다.

## 9. 롤백

변경은 공용 Method와 기존 serial-fiction consumer의 문서 연결만 수정한다.

회귀가 발견되면:

1. `RELATIONAL_APPEAL` 추가 절과 consumer 연결만 되돌린다.
2. 기존 캐릭터·관계·POV·상대 위상 규칙은 유지한다.
3. Registry·Skill 수·프로젝트 정본에는 변화가 없으므로 별도 데이터 migration은 필요하지 않는다.

## 10. 기대 효과

이 변경의 목적은 “캐릭터 설정을 더 많이 만든다”가 아니다.

```text
개별 설정
→ 조합에서 생기는 압력
→ 새로운 선택·갈등·행동
→ 장면에서 관찰 가능한 차이
→ 독자가 기억하는 캐릭터 관계와 매력
```

따라서 캐릭터를 프로필의 합으로 보지 않고 **서로와 세계에 부딪힐 때 어떤 장면을 스스로 발생시키는가**를 작법과 검수의 공용 기준으로 만든다.
