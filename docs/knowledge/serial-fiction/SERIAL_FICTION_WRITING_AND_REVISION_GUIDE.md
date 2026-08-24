# 연재소설 집필·퇴고 Guide

## 1. 목적

연재소설의 품질은 특정 인기작의 문체를 따라 쓰거나 매회 같은 공식에 맞추는 것으로 보장되지 않는다. 이 Guide는 장르와 문체가 달라도 반복해서 점검할 수 있는 **정본·독자 약속·장면 체험·POV·인과·후폭풍**을 공용 기준으로 삼는다.

핵심:

```text
Canon before adaptation
→ Reader Promise
→ Scene Experience
→ POV as Filter
→ Cause / Reaction / Choice / Result
→ Episode Value
→ Consequence Memory
→ Revision Evidence
```

## 2. Canon before adaptation

각색·퇴고 전에 무엇을 바꿀 수 없는지 먼저 확인한다.

```yaml
protected_facts:
protected_event_results:
protected_relationship_state:
protected_information_timing:
adaptable_gaps:
```

원작·TRPG 로그·이전 승인본처럼 보호된 결과가 있더라도 **빈 감정, 빈 인과, 행동의 구체화, 장면 미장센, 대사와 내면**은 각색할 수 있다. 다만 결과를 만들기 위해 인물이 당시 알 수 없는 정보를 갑자기 알거나, 기존 능력·관계를 편의적으로 바꾸지 않는다.

### 2-A. Canon 변경과 legacy 원고 이관은 다른 상태다

새 Canon/Decision이 승인되면 현재 판단에는 즉시 적용한다. 하지만 승인 전에 이미
작성된 활성 DRAFT가 모두 새 Canon을 준수한다는 뜻은 아니다. 의미·인과·관계가
얽힌 원고를 단어 치환으로 blind rewrite하지 않기 위해 다음 enforcement class를
구분한다.

| Class | 적용 범위 | 완료 해석 |
| --- | --- | --- |
| `STRICT_NOW` | 현재 활성 artifact 전체 | 즉시 검증 또는 이미 끝난 안전 migration이 필요하다. |
| `FORBIDDEN_IN_NEW_OR_REVISED` | 새 원고와 현재 실질적으로 고치는 원고 | 과거 DRAFT 전체의 자동 재작성은 요구하지 않는다. |
| `BOUNDED_LEGACY_RECONCILIATION_DEBT` | 정확히 선언한 legacy active consumer | source/Canon/continuity 대조를 거쳐 묶음 단위로 줄인다. |
| `SCOPED_STRICT` | 선언한 아크·시점·플랫폼·버전 | 범위 밖으로 전역화하지 않는다. |

`BOUNDED_LEGACY_RECONCILIATION_DEBT`는 backlog 면허가 아니다. 다음 invariant가
깨지면 새 legacy 확산 또는 오래된 ledger를 조사한다.

```text
actual_legacy_debt_consumers == declared_debt_consumers
```

정확한 일치는 `PASS_WITH_KNOWN_DEBT`일 수 있다. 이 상태는 새 원고로의 확산을
막았다는 뜻이지 `CANON_MIGRATION_COMPLETE`가 아니다. `archive/reference-only`
artifact는 active debt consumer로 등록하지 않는다.

### 2-B. reconciliation frontier 밖의 연속성을 발명하지 않는다

부분 이관에는 다음 네 상태가 필요할 수 있다.

```text
VERIFIED_PREFIX
+ DECLARED_MIGRATION_BOUNDARY
+ LEGACY_TAIL
+ FRONTIER_VERIFICATION_STATUS
```

`candidate frontier`는 다음 묶음의 원고 또는 파생 데이터가 저장된 상태일 수
있다. declared validation gate가 Green이기 전에는 verified prefix를 늘리거나
whole-manuscript reconciliation complete를 주장하지 않는다.

미검증 migration boundary의 양쪽 artifact는 같은 번호나 파일명만으로 인과가
이어진다고 볼 수 없다. derived consumer가 index, reverse outline, synopsis, graph
등을 만들 때 그 사이를 `normal continuity`의 previous/next로 자동 연결하지
않는다. project-local marker는 사용할 수 있지만 Base는 field 이름을 강제하지
않는다.

migration debt가 남아도 한 artifact의 current authority는 하나여야 한다.
중복 current authority는 `DUPLICATE_CURRENT_AUTHORITY`로 fail-closed 한다.

이 lifecycle은 다음에는 사용하지 않는다.

- active legacy artifact가 없을 때
- schema migration test가 보장한 안전한 단순 rename을 한 번에 끝낼 때
- legacy artifact가 `archive/reference-only`일 때
- 인접 continuity가 이미 source/Canon 대조로 검증됐을 때

## 3. Reader Promise

Reader Promise는 작품이 독자에게 반복적으로 주는 핵심 경험이다. 장르 이름보다 구체적이어야 한다.

예시 형태:

```text
[어떤 인물]이 [어떤 방식으로] [어떤 종류의 문제]를 겪으며
독자는 반복적으로 [감정/판단/관계 경험]을 얻는다.
```

매 회차가 동일 사건을 반복할 필요는 없다. 하지만 Reader Promise와 장기간 무관한 전개가 이어지면 `READER_PROMISE_MISSING`을 의심한다.

### 3-A. 새 이야기·아크·에피소드 기원이 비어 있을 때 — `STORY_ORIGIN_ENGINE`

새 이야기·아크·에피소드를 발상하거나 기존 Reader Promise에서 다음 사건을 생성해야 할 때 `docs/knowledge/methods/STORY_ORIGIN_AND_GENERATION_METHOD.md`를 선택적으로 사용한다.

```text
Reader Promise 또는 현재 seed
→ AFFECTED_AGENT
→ PRESSURE
→ DESIRE / GOAL
→ RESISTANCE
→ CONSEQUENTIAL_CHOICE
→ CONSEQUENCE / SHIFT
→ 다음 회차가 소비할 NEXT_PRESSURE
```

이미 정본 사건·인과·회차 목표가 확정된 단순 퇴고에서는 story origin을 다시 만들지 않는다. 정본을 더 흥미롭게 만들기 위해 보호된 사건 결과를 바꾸지 않는다.

## 4. 사건 요약과 장면 체험을 구분한다

압축 초안은 사건 배치에 유용하지만 완성 원고와 다르다.

요약:

```text
그는 단서를 발견했다.
둘은 다투었고 결국 함께 가기로 했다.
적을 물리친 뒤 마을을 떠났다.
```

장면 체험은 독자가 판단 과정을 따라갈 수 있게 한다.

```text
목표
→ 저항
→ 보고·듣고·만지는 구체적 자극
→ 대사·행동
→ 해석·오해·판단
→ 선택
→ 관찰 가능한 결과
→ 남은 감정·관계·정보 변화
```

분량을 늘리기 위해 배경·감정 형용사만 추가하지 않는다. **새 문장은 독자가 장면을 더 정확히 보고, 인물의 선택을 더 잘 이해하거나, 감정을 더 직접 체험하게 해야 한다.**

## 5. POV는 카메라가 아니라 정보·주의·가치의 필터다

POV는 다음 다섯 축으로 구분한다.

1. **Information** — 무엇을 알고 모르는가
2. **Attention** — 무엇을 먼저 보는가
3. **Interpretation** — 같은 사실을 어떻게 해석하는가
4. **Value** — 무엇을 중요·위험·우스운 것으로 판단하는가
5. **Suppression** — 무엇을 인정하거나 말하기 싫어하는가

POV 교체 검수:

- 이름을 가려도 누가 보고 있는지 어느 정도 구분되는가?
- 다른 인물이라면 주의할 대상과 비유가 달라지는가?
- 현재 POV가 알 수 없는 정보가 작가 편의로 들어오지 않는가?
- 작가의 철학적 결론이 모든 인물의 동일한 내면 문장으로 반복되지 않는가?

강한 voice는 특이한 말버릇만 뜻하지 않는다. **선택하는 정보와 판단 방식의 일관성**이 먼저다.

## 6. 내면 독백은 해설이 아니라 편견과 욕망을 보여준다

좋은 내면은 다음 중 하나를 한다.

- 외부 행동과 다른 진짜 욕망을 드러낸다.
- 자기합리화나 오해를 보여준다.
- 선택의 비용을 체감시킨다.
- 같은 사실에 대한 그 인물만의 판단을 만든다.

약한 내면:

- 방금 본 사건을 다시 설명한다.
- 이미 대사로 말한 감정을 재진술한다.
- 독자를 위해 설정집 내용을 인물 머릿속에 넣는다.
- 장면 의미를 작가가 대신 결론 내린다.

## 7. 대사는 정보 전달보다 관계 행동이다

대사 검수 순서:

```text
이 인물은 지금 무엇을 얻으려 하는가?
→ 상대에게 무엇을 숨기거나 압박하는가?
→ 말과 행동이 일치하는가, 어긋나는가?
→ 말 뒤 관계의 거리가 바뀌는가?
```

대사 중 미장센을 사용한다. 인물은 공간을 이동하고 물건을 다루며 시선을 피하거나 거리를 좁힌다. 행동이 대사의 뜻을 그대로 반복하지 않게 한다.

고정 `대사 40% / 행동 30% / 묘사 20%` 같은 비율은 universal 규칙이 아니다. 비율은 설명 과다·독백 과다를 발견하는 참고 Lens로만 사용한다.

## 8. 구체적 물성을 우선한다

긴장·전투·공포에서 추상 형용사보다 인물이 당장 확인할 수 있는 정보를 먼저 준다.

- 거리와 출구
- 손에 든 물건
- 소리의 방향
- 빛·온도·냄새
- 부상의 기능 저하
- 상대의 위치
- 남은 시간·탄약·자원

모든 것을 수치화하라는 뜻은 아니다. 독자가 인물과 같은 공간에서 같은 위험을 판단할 수 있을 만큼만 구체화한다.

## 9. 공포와 미스터리는 정답이 아니라 인과를 숨기지 않는다

공포에서 설명을 제한하는 것은 유효하다. 그러나 독자가 아무것도 이해하지 못하게 만드는 것은 다른 문제다.

`Information Legibility` 최소값:

```yaml
current_pov:
immediate_goal:
obstacle_or_risk:
changed_state_after_action:
```

괴이의 이름·우주적 원리·배후는 숨겨도 된다. 현재 행동의 이유와 결과까지 흐리면 `INFORMATION_LEGIBILITY_FAILURE`다.

## 10. 느림과 정체를 분리한다

느린 장면을 자동 삭제하지 않는다.

느리지만 움직이는 장면:

- 관계가 변한다.
- 새 의심이 생긴다.
- 인물이 과거 사건을 다시 해석한다.
- 결정 비용을 이해한다.
- 평범한 루틴을 만들어 이후 비일상의 대비를 강화한다.

정체 장면:

- 같은 감정·정보를 새 변화 없이 반복한다.
- 이미 끝난 판단을 다른 표현으로 다시 설명한다.
- 전투·이동은 빠르지만 목표·위험·관계·자원이 바뀌지 않는다.

따라서 공용 기준은 **“느린 구간 없음”이 아니라 “정지된 구간 없음”**이다.

## 11. Consequence Memory

중대한 사건은 다음 장면에 흔적을 남긴다.

```text
실패 → 정보·상흔·금기 이해
폭력 → 관계·죄책감·평판·작전 조건
능력 사용 → 육체·정신·관계·자원 비용
선택 → 새 책임·적대·부채·포기한 가능성
```

다음 장면이 아무 영향 없이 초기 상태로 복원되면 `CONSEQUENCE_MEMORY_MISSING`을 의심한다.

## 12. 장면 기능은 수가 아니라 우선순위를 본다

기존의 “장면은 사건·감정·정보·관계 중 2개 이상 수행”은 좋은 밀도 Lens지만 Hard Rule로 쓰지 않는다.

기본:

```yaml
primary_function: PLOT | EMOTION | INFORMATION | RELATIONSHIP | ATMOSPHERE | CONSEQUENCE
secondary_functions: []
```

주 기능 하나가 분명하면 보조 기능은 필요할 때만 추가한다. 짧은 공포 이미지, 장례, 침묵, 관계 결산처럼 단일 기능이 강하게 작동하는 장면을 기능 개수 때문에 과밀하게 만들지 않는다.

## 13. Framework는 진단 Lens다

다음은 선택적으로 사용할 수 있다.

- Story Grid 5 Commandments
- Save the Cat beats
- Story Circle
- Hero's Journey
- Snowflake Method
- 고정 대화·행동·묘사 비율
- 이분법적 위기 선택
- 특정 문장 길이

장면이 이미 목적을 달성하는데 체크리스트를 채우기 위해 인위적 위기·반전·대사를 추가하면 `FRAMEWORK_OVERFIT`이다.

### 13-A. 외부 작법 자료는 출처와 권한을 정규화한다

외부 작법 조언은 이름이 유명하다는 이유로 Base의 공식 규칙이 되지 않는다. 원출처의 성격과 현재 프로젝트에 옮길 수 있는 기능을 분리한다.

- `EMMA_COATS_STORYBASICS_NOT_OFFICIAL_PIXAR_POLICY`: 널리 “픽사의 22가지 법칙”으로 불리는 Emma Coats의 `#storybasics`는 Pixar 재직 중 얻은 개인적 작법 메모·heuristic으로 취급한다. Pixar의 공식 전사 규정으로 표기하지 않는다.
- Pixar의 실제 교육 자료를 근거로 삼을 때는 Pixar와 Khan Academy가 공개한 `Pixar in a Box`처럼 출처가 명확한 자료를 우선한다. 여기서도 Wants/Needs, Obstacles, Character Arc, Stakes, Story Structure, Pitching/Feedback을 **선택적 Lens**로 추상화한다.
- E. M. Forster의 story/plot 구분은 시간순 사건보다 **인과가 plot을 만든다**는 진단에 사용한다. 문학 전체를 하나의 정의로 고정하지 않는다.
- `HERO_JOURNEY_12_IS_VOGLER_ADAPTATION`: Campbell의 monomyth가 이론적 원류이지만, `Ordinary World`에서 `Return with the Elixir`까지의 익숙한 실무용 12단계 배열은 Christopher Vogler의 각색으로 구분한다. 12단계를 Campbell의 원래 고정 목록으로 잘못 표기하지 않는다.
- Brandon Sanderson의 `Promise / Progress / Payoff` 같은 현업 작법 모델도 특정 작가의 성공 공식이 아니라 중간 진행이 실제 보상을 향해 움직이는지 보는 optional diagnostic으로만 사용한다.

근거 추적용 원출처·근접 원출처:

- Pixar in a Box — `https://www.khanacademy.org/computing/pixar/storytelling`
- Emma Coats `#storybasics` 동시대 아카이브 — `https://www.pixartouchbook.com/blog/2011/5/15/pixar-story-rules-one-version.html`
- Open University의 E. M. Forster story/plot 설명 — `https://www.open.edu/openlearn/mod/oucontent/view.php?id=101090&section=_unit4.2`
- Christopher Vogler의 Hero's Journey handout — `https://chrisvogler.wordpress.com/tag/the-heros-journey/`
- Brandon Sanderson 공식 강의 `Promise, Progress, Payoff` — `https://www.youtube.com/watch?v=ihd76ijy9LU`

`HERO_JOURNEY_OPTIONAL_12_STAGE_LENS`는 Vogler의 실무용 12단계를 **필요할 때만** 구조 진단에 사용한다.

```text
1. Ordinary World / 일상 세계
2. Call to Adventure / 모험의 부름
3. Refusal of the Call / 거부
4. Meeting with the Mentor / 조력자와의 만남
5. Crossing the Threshold / 첫 관문 통과
6. Tests, Allies, Enemies / 시험·동료·적
7. Approach / 가장 깊은 곳으로의 접근
8. Ordeal / 중대한 시험
9. Reward / 보상
10. The Road Back / 귀환의 길
11. Resurrection / 부활
12. Return with the Elixir / 보물과 함께 귀환
```

모든 작품이 12단계를 순서대로 명시적으로 가져야 하는 것은 아니다. 짧은 작품·군상극·미스터리·비선형 서사에서는 단계가 압축·생략·재배열될 수 있으며, 이 Lens 때문에 기존 Reader Promise·정본 인과·캐릭터 고유 선택을 비틀면 `FRAMEWORK_OVERFIT`이다.

외부 자료는 `ADOPT / ADAPT / REJECT`로 판단하고, 프로젝트 정본·독자 약속·실제 원고 증거보다 높은 권한을 갖지 않는다. 식별 가능한 문장·대사·장면 배열은 복제하지 않는다.

### 13-B. 최소 스토리 기획 — `STORY_PLANNING_MINIMUM`

설정과 아이디어를 모두 채운 뒤 쓰기 시작하지 않는다. 현재 범위에 필요한 최소 뼈대만 먼저 고정한다.

```text
STORY_PLANNING_MINIMUM
→ ONE_SENTENCE_ESSENCE
→ READER_PROMISE
→ FOCAL_AGENT_DECISION_OWNER
→ PRESSURE / RESISTANCE
→ CAUSAL_DIRECTION

OPTIONAL_STORY_PLANNING_FIELDS
→ WANT_NEED_STAKES
→ CLIMAX_CHOICE
→ END_STATE
```

`STORY_PLANNING_MINIMUM`은 모든 칸을 미리 채우는 beat sheet가 아니다. discovery writing이나 결말 탐색이 필요한 작품은 `OPTIONAL_STORY_PLANNING_FIELDS`를 비운 채 시작할 수 있다. 다만 현재 초점 인물, 압력과 저항, 다음 선택이 어떤 인과 방향을 만드는지는 추적 가능해야 한다. 이 packet은 `STORY_ORIGIN_ENGINE`을 대체하지 않고 그 출력과 기존 정본을 집필 전에 빠르게 확인하는 handoff Lens다.

- `ONE_SENTENCE_ESSENCE`: “누가 어떤 압력 속에서 무엇을 선택하며 무엇이 달라지는가”를 한 문장으로 설명할 수 있는지 본다. 마케팅 로그라인 형식을 강제하지 않는다.
- `FOCAL_AGENT_DECISION_OWNER`: 작품 전체에 주인공이 반드시 한 명이어야 한다는 규칙이 아니다. 개인·관계·팀·군상극도 가능하지만, **현재 장면·회차·아크에서 누구의 목표·판단·결정이 중심인지**는 독자가 추적할 수 있어야 한다.
- `MULTI_POV_IS_NOT_AUTOMATIC_FAILURE`: 다중 POV 자체는 실패가 아니다. 다만 POV를 바꾸면서 목표·정보 접근권·voice·결정 주체가 무계획하게 교체되면 다시 설계한다.
- `WANT_NEED_STAKES`: 필요할 때 `Want = 행동을 움직이는 현재 욕망/목표`, `Need = 성장·성공을 위해 배워야 하거나 수정해야 할 믿음/행동`, `Stakes = 선택이 실패하거나 성공할 때 잃고 얻는 것`으로 분리한다. 모든 인물에게 Want/Need 변화를 강제하지 않는다.
- Stakes는 물리적 위험만이 아니라 내부 감정·관계·가치·철학적 기준일 수 있다. 규모보다 **왜 독자가 신경 써야 하는지**가 중요하다.
- Seed·압력·선택이 아직 비어 있으면 `STORY_ORIGIN_ENGINE`을 사용하고, 이미 정본 사건이 있으면 기원을 다시 발명하지 않는다.

주인공을 사랑받게 만들기 위해 성공 횟수를 늘리기보다, 목표를 향해 시도하고 실패를 감수하며 방식이 바뀌는 과정을 보여준다. `EFFORT_PROCESS_OVER_INSTANT_SUCCESS`는 “항상 실패시켜라”가 아니라 **성과를 획득한 과정과 비용을 독자가 볼 수 있게 하라**는 Lens다.

### 13-C. 사건의 순서보다 인과와 선택을 우선한다

`CAUSE_BEFORE_SEQUENCE`는 “그리고 다음에”만 이어지는 사건 목록을 “그 선택 때문에 무엇이 바뀌었는가”로 다시 묻는다.

```text
CAUSAL_BEAT_CHAIN
PRESSURE
→ DECISION / ACTION
→ RESULT
→ NEW_INFORMATION_OR_COST
→ NEXT_PRESSURE
```

모든 beat가 거대한 결정을 요구하지는 않지만, 핵심 beat는 최소한 **앞 사건의 결과이거나 인물의 판단·행동이 다음 상태를 만든다는 연결**을 가져야 한다. `STORY_VS_PLOT_CAUSALITY`는 사건의 시간순 목록과 인과를 강조한 배열을 구분하는 진단 Lens다.

- 시도와 실패를 반복할 때는 정보·전략·관계·비용·위험 중 하나가 달라져야 한다. 실패 뒤 원상복구되면 과정이 아니라 지연이다.
- `COINCIDENCE_CAN_START_NOT_SOLVE`: 우연은 사건의 발단, 만남, 기회, 예상 밖의 문제를 만들 수 있다. 그러나 핵심 갈등·클라이맥스를 기존 setup·인물 선택·유능함·관계·규칙·대가와 무관한 우연이 해결하면 개연성과 주체성이 약해진다.
- 갈등을 키울 때는 `CONFLICT_ESCALATION_LENS`로 목표의 표적을 선명하게 하고, 소중한 관계·가치·자원·시간을 압박하거나 선택 비용을 높일 수 있다. 단순 고통량을 늘리는 것이 목적은 아니다.
- `TRAGEDY_OR_VILLAIN_NOT_REQUIRED`: 비극·빌런·라이벌은 선택지이지 의무가 아니다. Resistance는 다른 사람의 합리적 목표, 제도, 시간, 자원, 환경, 정보 부족, 자기기만, 관계 의무일 수도 있다.
- 캐릭터가 잘하는 방식만 반복해 통과한다면, 그 장점이 통하지 않거나 장점의 그림자를 드러내는 압력을 후보로 검토한다. 기존 정본에 없는 약점·트라우마를 편의상 새로 만들지는 않는다.

### 13-D. 관객이 인식하는 순서와 장면의 구체성을 설계한다

`AUDIENCE_PERCEPTION_ORDER`는 작가가 알고 있는 정보량이 아니라 **현재 POV를 따라가는 독자가 지금 무엇을 보고, 어떻게 해석하고, 무엇에 반응할 수 있는지**를 기준으로 장면을 점검한다.

최소 질문:

```yaml
who_is_focal_now:
where_are_they_and_what_is_nearby:
immediate_goal_or_attention:
visible_obstacle_or_pressure:
observable_reaction:
what_changed_after_action:
what_question_remains:
```

- 정보의 제시 순서는 독자의 이해·동정·긴장·반전 체감에 영향을 준다. 무조건 연대기순으로 설명하지 않되, 현재 행동을 이해할 맥락까지 숨기지는 않는다.
- “불안했다”, “화가 났다”만 적기보다 시선·거리·말의 끊김·손의 행동·회피·접근처럼 상황에 맞는 관찰 가능한 반응을 우선한다.
- 공간이 선택이나 위험에 영향을 주는 장면은 인물 위치, 거리, 출구, 장애물, 손에 닿는 물건 중 필요한 것만 구체화한다. 배경 설정집을 장면에 전부 옮기지 않는다.
- 감정은 앞 장면의 사건과 선택 비용을 기억해야 한다. 큰 충격 뒤 이유 없이 초기 감정 상태로 돌아가면 `Consequence Memory`를 다시 확인한다.
- 중요한 정보는 독자가 추론할 수 있게 단계적으로 제공하되, 독자만 속이기 위한 `FALSE_SUSPENSE_BY_POV_SUPPRESSION`은 사용하지 않는다.

### 13-E. 끝에서 역산하되 중간의 진행을 비우지 않는다

`END_BACKWARD_PLANNING`은 결말이 흐려 중간이 방황할 때 사용할 수 있는 optional 도구다.

```text
END_STATE / CLIMAX_CHOICE
→ 그 선택에 필요한 가치·정보·관계 변화
→ 필요한 setup과 이전 실패
→ 현재 장면에서 시작할 pressure
```

엔딩을 먼저 정했다고 해서 과정이 정답 맞히기가 되어서는 안 된다. 인물의 선택이 실제 압력과 이전 결과에서 자연스럽게 축적되어야 한다.

`PROMISE_PROGRESS_PAYOFF`는 다음을 분리한다.

- **Promise**: 독자가 어떤 경험·질문·갈등의 보상을 기대하게 되었는가.
- **Progress**: 중간이 답을 미루기만 하지 않고 시도·실패·정보·관계·비용·전략을 실제로 바꾸는가.
- **Payoff**: 처음 만든 기대가 결과·선택·감정·정보 변화로 결산되는가.

마지막 장면은 주제를 해설하는 문장보다 **초반과 달라진 행동·관계·세계 상태를 관찰 가능하게 보여주는 것**을 우선 검토한다. 강한 엔딩 이미지나 여운은 Reader Promise와 맞을 때 사용한다.

서브 플롯과 주변 인물은 `SIMPLIFY_BY_FUNCTION`으로 감사한다. 새 압력·선택·대비·관계 변화·정보·payoff를 만들지 못하고 같은 기능을 반복하면 합치기·축약·삭제·후순위 이동 후보로 둔다. 반대로 주인공 한 명에 집중한다는 이유로 필요한 관계와 세계 반응까지 제거하지 않는다.

### 13-F. 아이디어·초고·피드백·재작성 단계를 분리한다

`IDEA_DIVERGENCE_BEFORE_COMMIT`은 첫 번째 아이디어를 자동 폐기하라는 규칙이 아니다. 중요한 사건·해결·반전에서 첫 안이 관습적이거나 정본과 충돌할 위험이 있으면 **2개 이상의 대안**을 더 만들어 기능·비용·독창성으로 비교한다.

- `NEGATIVE_NEXT_BEAT_LIST`: 다음 전개가 막힐 때 “절대 일어나지 않을 일”, “이 작품에서는 원치 않는 상투안”, “현재 정본상 불가능한 해결”을 먼저 적어 배제 기준을 드러낸 뒤, 남는 압력·선택·인과 후보를 다시 만든다. 이 목록 자체를 정답 공식으로 사용하지 않는다.
- `IDEA_PARKING_LOT`: 지금 버린 아이디어는 current canon으로 억지 보존하지 않고 non-canon reference로 분리해 둘 수 있다. 나중에 다른 장면·프로젝트에서 기능이 맞을 때만 재평가하며, “이미 만들었으니 써야 한다”는 매몰비용으로 되살리지 않는다.
- `SYMBOL_MOTIF_METAPHOR_OPTIONAL`: 상징·모티프·비유·은유는 특정 사물·이미지·행동을 반복해 주제·관계·감정 변화를 압축해서 보여줄 때 사용할 수 있다. 독자가 장면 자체를 이해하려면 숨은 상징 해석이 반드시 필요하도록 만들지 않고, 상징을 넣기 위해 기존 인과나 인물 행동을 비틀지 않는다.
- `VOICE_TONE_CONTINUITY`: 작품의 genre promise, 현재 POV, 관계 거리와 장면 상태에 맞는 voice·tone을 유지한다. 큰 톤 변화는 사건·POV·상태 변화로 설명될 수 있어야 하며, “작가의 목소리”는 다른 작가의 식별 가능한 문체를 모사하는 것이 아니라 반복되는 정보 선택·판단·리듬 원칙에서 형성한다.

`DRAFT_FEEDBACK_REWRITE`:

```text
rough spine / outline
→ imperfect complete draft or pitch
→ feedback evidence
→ symptom / intent extraction
→ multiple fix candidates
→ structural rewrite
→ scene/prose revision
→ proofreading
```

- 완벽한 첫 문장을 기다리며 전체 구조 검증을 미루지 않는다. 현재 범위의 초고를 끝낸 뒤 더 큰 구조 문제부터 고친다.
- `FEEDBACK_IS_EVIDENCE_NOT_CANON`: 피드백은 독자가 어디서 혼란·지루함·기대·감정을 느꼈는지 보여주는 Evidence다. 제안된 해결책을 그대로 정본으로 승격하지 않는다.
- 피드백의 “문장”보다 지적의 의도를 찾고, 중요한 문제에는 복수 수정안을 시험한 뒤 다시 읽거나 재피칭한다.
- 주제는 초고 전 가설로 둘 수 있지만 완성된 초고에서 더 정확한 의미가 보일 수 있다. 그때 `THEME_EMERGES_AND_REWRITE`로 사건·선택·결말이 주제를 실제로 증명하도록 재작성하고, 주제 설명 대사만 추가하지 않는다.
- 사실성·직업·장소·역사·기술이 인과나 독자 신뢰에 영향을 주면 리서치하고 불확실성을 구분한다. 리서치 양 자체를 이야기 품질로 간주하지 않는다.
- 좋아하는 작품·다른 장르·다른 매체·실패한 작품을 분석할 때는 표현을 베끼지 말고 **무슨 독자 경험과 기능을 만들었는지**만 추출한다.

맞춤법·띄어쓰기·문법·전문용어 풀이는 중요하지만 구조적 인과·장면 가치·POV 문제를 가리지 않게 후반 prose/proofreading pass에서 처리한다.

### 13-G. 모바일 문단 길이는 화면 기반 선호 Lens다

`PARAGRAPH_SCREEN_BLOCK_PREFERENCE`는 모바일·웹 연재의 시각적 덩어리를 점검한다. 프로젝트 또는 사용자 선호가 “한 덩어리를 약 3~5줄 안팎으로 읽히게 한다”라면 초안 점검의 출발점으로 사용할 수 있다.

`THREE_TO_FIVE_LINES_NOT_UNIVERSAL`: 실제 줄 수는 화면 폭·폰트·글자 크기·플랫폼 렌더링에 따라 달라지므로 3~5줄을 Base의 universal quota로 만들지 않는다.

- 행동 주체, 정보 초점, 대사/반응, 시간·공간 beat가 바뀌는 지점에서 문단 분리를 우선 검토한다.
- 긴 설명벽과 의미 없이 한 문장씩 잘게 부수는 파편화를 모두 피한다.
- 강한 충격·침묵·짧은 결정처럼 독자가 별도 beat로 받아야 하는 반응은 독립 문단이 유효할 수 있다.
- 실제 작업에서는 Skill의 `PARAGRAPH_BREAK_AND_BREATH`, `LINE_BREAK_RHYTHM`, `REACTION_ISOLATION`과 프로젝트별 사용자 선호 Evidence를 함께 사용한다.

## 14. Revision pass order

한 번에 모든 문장을 고치지 않는다.

### Pass 1 — Canon / Continuity

- 사건 결과, 정보 획득 시점, 인물 위치, 관계 상태
- 앞뒤 회차와 모순
- staged migration이면 enforcement class, exact debt set, verified prefix, unresolved
  boundary, declared validation gate와 duplicate current authority를 먼저 대조

### Pass 2 — Episode Value / Structure

- 이 회차에서 무엇이 바뀌는가
- 작은 payoff와 남는 질문
- 장면 순서와 삭제 후보

### Pass 3 — POV / Character

- 정보 접근권
- voice·내면·대사
- 행동 동기와 개연성

### Pass 4 — Scene Experience

- 요약을 극화할 부분
- 감각·행동·미장센·구체적 물성
- 정보 공개 순서

### Pass 5 — Prose / Rhythm

- 문장 호응, 중복, 추상 해설
- 문단 연결, 호흡, 액션 가독성

### Pass 6 — Serial Continuity

- 복선·회수
- 후폭풍
- 다음 회차 Open Loop
- 플랫폼 production target

## 15. Originality boundary

벤치마크에서 가져올 수 있는 것은 높은 수준의 기능이다.

가능:

- 강한 POV 필터
- 실패 누적 구조
- 생활 루틴 변주
- 외부 반응으로 성과 가시화
- 복잡한 미스터리의 정보 상태 관리

금지:

- 특정 작가의 대표 문장 구조를 반복
- 대사·비유·개그 패턴을 식별 가능하게 재현
- 인기 에피소드의 사건 배열을 이름만 바꿔 복제

그 위험이 보이면 `STYLE_COPY_RISK`로 판정하고 독자 경험·정보 기능·갈등 기능으로 다시 추상화한다.

## 16. 검증 상한

문서·Skill 계약이 존재한다고 실제 독자 만족도나 판매가 향상됐다고 주장하지 않는다.

```yaml
base_contract: VERIFIABLE
project_draft_quality: PROJECT_PILOT_REQUIRED
human_reader_response: HUMAN_NOT_RUN
commercial_result: NOT_RUN
future_platform_rules: PLATFORM_REVERIFY_REQUIRED
```
