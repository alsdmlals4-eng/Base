# 캐릭터 개성·상대 위상 감사

## 목적

캐릭터를 강하게 보이게 하려고 상대를 무능·약체로 낮추거나, 설정문만으로 인물의 개성·강함을 주장하는 실패를 막는다. 인물과 상대 모두 **장면 안에서 자기 방식·자기 턴·대가**를 가져야 한다.

## 적용 시점

- 주요 인물·조연·적대자 설계
- 전투·추격·협상·수술·마법 대결처럼 능력 차이가 중요한 장면
- 원작·TRPG 로그·기존 초안을 압축/각색하며 원래 인물 기능이 약해졌는지 감사할 때
- “설정상 강한데 약해 보인다”, “다들 말투가 같다”, “주인공 때문에 적이 바보가 된다”는 증상이 있을 때

## 1. 캐릭터 식별 카드

주요 인물마다 최소 다음을 분리한다.

```yaml
attention_filter: 무엇을 먼저 보는가
voice_and_thought: 어떤 말투·판단·비유를 쓰는가
problem_solving_method: 문제를 어떤 방식으로 푸는가
strength_proof: 유능함·강함을 실제로 보여준 장면
human_charm: 능력 외에 사람이 좋아지거나 기억되는 면
flaw_with_cost: 실제 문제를 일으키는 결점과 대가
signature_highlight: 이 인물을 한 장면으로 설명할 대표 하이라이트
```

이름을 지우고 대사·판단·행동을 읽었을 때 여러 인물이 서로 교환 가능하면 `CHARACTER_IDENTITY_BLUR`다.

### 관계적 매력 감사 — `RELATIONAL_APPEAL`

개별 캐릭터 카드가 충분해도 조합이 장면을 만들지 못하면 설정은 정지해 있을 수 있다. 필요할 때 공용 owner `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`의 `RELATIONAL_APPEAL`을 사용한다.

```text
CHARACTER_X_CHARACTER | CHARACTER_X_WORLD | CHARACTER_X_ABILITY
→ 현재 조합에서 생기는 압력
→ 새 선택 / 갈등·협력 / 대사·행동 / 결과 중 관찰 가능한 차이
→ 기존 정본·욕망·판단과의 정합성
```

`DECORATIVE_SYNERGY`, `FORCED_CHEMISTRY`, `CROSS_PRODUCT_OVERDESIGN`이 보이면 설정을 더 붙이기보다 현재 장면에 필요한 최소 조합만 남긴다.

## 2. 상대 위상 장부

중요 상대마다 다음을 기록한다.

```yaml
opponent:
threat_rule:
on_screen_threat_proof:
first_success_or_own_turn:
protagonist_crisis:
why_the_protagonist_survived_or_won:
frontal_outcome_if_conditions_changed:
best_pov:
post_defeat_dignity:
later_payoff:
```

### Own Turn 원칙

강적은 최소 한 번 자신의 규칙을 주인공에게 강제해야 한다. 등장 직후 필살기에 무력화되면 위상은 설명문으로 복구하지 않는다.

좋은 예의 구조:

```text
상대의 규칙·강점 제시
→ 상대가 실제로 성공
→ 주인공이 위기/비용을 감수
→ 주인공 고유 방식으로 규칙을 읽거나 우회
→ 승리·생존
→ 패배한 상대의 위상도 남음
```

## 3. 승리 방식 다양화

전투를 항상 더 큰 화력으로 끝내지 않는다.

- `SKILL`: 순수 숙련·기량
- `TACTIC`: 기만·협공·지형·시간벌기
- `RULE`: 괴이·마법·시스템 규칙 해석
- `RELATION`: 협상·의무·신뢰·목표 충돌 이용

같은 인물이 반복해서 이길 때도 방법·비용·실패 형태 중 하나 이상을 변주한다.

## 4. 강함은 화면 안에서 증명한다

설정상 전투 강자인 주요 인물이 중요 구간 내내 보고·결과·소문으로만 강하면 `OFFSCREEN_STRENGTH_ONLY`다. 단, 미스터리 보존을 위해 의도적으로 감추는 경우는 후속 공개 장면과 회수 위치가 명시되어야 한다.

- 조연의 강함을 증명하려고 주인공의 결정을 빼앗지 않는다.
- 주인공의 강함을 증명하려고 상대의 판단력·훈련·목표를 갑자기 낮추지 않는다.
- 패배·사망은 약함과 동일하지 않다. 패배 전 성공, 비용 부과, 목표 달성 일부, 후속 흔적 중 하나 이상으로 위상을 남길 수 있다.

## 5. 각색·원본 비교 규칙

원본이나 기존 초안에 캐릭터의 강함·매력·관계 기능을 증명하는 장면이 있었다면, 새 장면을 발명하기 전에 그 기능이 현행에서 왜 사라졌는지 대조한다.

```text
SOURCE FUNCTION
→ CURRENT REPRESENTATION
→ KEEP / RESTORE / REWORK / NEW / REMOVE
→ CANON CONFLICT CHECK
→ CAUSALITY CHECK
```

`RESTORE`는 원문을 복사하는 뜻이 아니라 **사건 결과·관계 변화·위상 증명 기능을 최신 정본에 맞게 복원**하는 것이다.

## 6. 개연성 체크

주요 대결마다 확인한다.

1. 상대가 왜 강하거나 위험한가?
2. 독자가 그 위험을 실제 장면에서 봤는가?
3. 상대가 먼저 성공하는 순간이 있는가?
4. 주인공이 이긴 이유가 주인공의 성격·능력·준비와 연결되는가?
5. 상대의 실수가 있다면 성격·정보·목표로 설명되는가?
6. 정면전·다른 조건이라면 결과가 달라질 여지가 있는가?
7. 패배 뒤 상대가 우스워지지 않는가?
8. 조연 하이라이트가 주연의 중앙 결정권을 빼앗지 않는가?

## Failure states

- `CHARACTER_IDENTITY_BLUR`: 인물의 말투·관찰·해결법·결점이 교환 가능함
- `ROLE_HOMOGENIZATION`: 여러 강자가 같은 방식으로만 강함
- `OPPONENT_THREAT_UNPROVEN`: 위험성이 설정·소문에만 있음
- `OFFSCREEN_STRENGTH_ONLY`: 중요 강자의 강함이 장면 밖 결과로만 제시됨
- `VICTORY_BY_OPPONENT_DEFLATION`: 승리를 위해 상대가 갑자기 멍청하거나 약해짐
- `SUPPORTING_CAST_STEALS_CLIMAX`: 조연 위상 증명이 주연의 핵심 선택·결말을 대신함

## 출력

필요한 범위만 사용한다.

```yaml
character_identity_matrix:
opponent_threat_ledger:
source_function_reconciliation:
highlight_keep_restore_rework_new_remove:
causality_findings:
revision_targets:
remaining_unknowns:
```
