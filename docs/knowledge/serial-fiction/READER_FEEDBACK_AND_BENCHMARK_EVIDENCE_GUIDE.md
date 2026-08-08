# 독자 반응·작품 벤치마크 Evidence Guide

## 1. 목적

인기작·현업 자료·댓글·리뷰는 작품 개선의 외부 Evidence다. **not canon**이며, 프로젝트 정본이나 독자의 해결책을 자동으로 요구사항으로 만들지 않는다.

벤치마크 목적은 성공작의 문장·사건을 복제하는 것이 아니라 현재 작품의 판단을 바꿀 수 있는 높은 수준의 원리와 반례를 찾는 것이다.

## 2. 네 층을 분리한다

```text
PRODUCT_FACT
→ READER_RESPONSE
→ CRAFT_HYPOTHESIS
→ TRANSFER_DECISION
```

### PRODUCT_FACT

플랫폼·출판사·작가·현업 기관에서 직접 확인한 것.

예:
- 연재 상태
- 회차 수
- 플랫폼이 표시한 조회·관심·선호·추천 지표
- 작품 소개에 명시된 장르·설정
- 현업 교육 과정의 실제 커리큘럼

조회수는 조회수다. 고유 독자 수로 임의 환산하지 않는다.

### READER_RESPONSE

리뷰·댓글·커뮤니티에서 반복되는 체감 반응.

예:
- 쉽게 읽힌다
- 원패턴 같다
- 복선 회수가 만족스럽다
- 후반 인과를 따라가기 어렵다
- 조연에게 애착이 간다

독자 반응은 작품 내부 사실의 권위가 아니다.

### CRAFT_HYPOTHESIS

제품 사실과 독자 반응을 실제 텍스트 구조와 대조해 만든 가설.

예:
- 실패가 정보로 누적돼 반복 구조 피로를 낮춘다.
- 생활 루틴이 비일상 장면의 기준점 역할을 한다.
- 해결보다 떡밥 설치가 계속 빨라져 payoff 부채가 커진다.

하나의 성공작만으로 인과를 확정하지 않는다.

### TRANSFER_DECISION

- `ADOPT_INVARIANT`: 장르가 달라도 공용 품질 원칙으로 채택
- `ADAPT_AS_LENS`: 특정 상황에서만 진단 Lens로 사용
- `PROJECT_ONLY`: 작품·장르·플랫폼 특수성이 커서 프로젝트 내부에만 사용
- `REJECT_COPY`: 표현·사건·voice 복제 위험 또는 잘못된 일반화
- `INSUFFICIENT_EVIDENCE`: 근거 부족

## 3. Source tier와 최신성

```yaml
source_tier: PLATFORM | INDUSTRY | PUBLISHER | READER
source:
observed_at:
metric_name:
metric_definition_known: true | false
sample_size_or_scope:
known_bias:
```

플랫폼 규칙·분량·가격·연재 정책처럼 변할 수 있는 내용은 실제 적용 시 다시 확인한다. 과거 정보뿐이면 `PLATFORM_REVERIFY_REQUIRED`다.

## 4. 반례를 의무적으로 찾는다

성공 사례에서 원칙을 추출했다면 반대 방식으로 성공한 사례를 찾는다.

예:

```text
가설: 성공 웹소설은 설명이 적어야 한다.
반례: 복잡한 규칙·정보 추론 자체가 핵심 재미인 장기 미스터리.
수정: 설명량이 아니라 정보의 기능·가독성·독자 추론 가능성을 본다.
```

```text
가설: 전개는 항상 빨라야 한다.
반례: 학교·업무·여행·관계 루틴이 애착을 만드는 장기작.
수정: 느림이 아니라 상태 변화 없는 정체를 줄인다.
```

반례 없이 인기작 하나의 표면 특징을 universal 규칙으로 올리지 않는다.

## 5. Reader feedback pipeline

```text
RAW_REACTION
→ SYMPTOM_CLUSTER
→ REVISION_HYPOTHESIS
→ 실제 원고 대조
→ 최소 수정
→ 회귀 검토
```

### RAW_REACTION

독자의 원래 반응. 예: `답답하다`, `짧다`, `누가 누군지 모르겠다`, `이번 화 좋다`.

### SYMPTOM_CLUSTER

해결책이 아니라 체감 문제를 묶는다.

- `AGENCY`: 주인공 주도권
- `PAYOFF`: 보상·결과
- `LEGIBILITY`: 인과·공간·정보 추적
- `REPETITION`: 원패턴
- `CHARACTER_ATTACHMENT`: 캐릭터 애착
- `TENSION`: 위험·비용
- `TONE`: 개그·공포·감정의 충돌
- `SETUP_PAYOFF`: 떡밥 기대·회수
- `PROSE`: 문장 호응·가독성

### REVISION_HYPOTHESIS

원고에서 검증할 수 있는 수정 가설로 바꾼다.

```yaml
symptom:
episodes_affected:
possible_causes:
textual_evidence:
minimal_change:
protected_strength:
recheck_question:
```

`답답하다 → 전투 추가`, `짧다 → 묘사 증량`처럼 독자 표현에서 해결책으로 바로 점프하지 않는다. 그러면 `COMMENT_AS_CANON`이다.

## 6. 표본 편향

댓글·리뷰는 다음 편향을 가질 수 있다.

- 댓글을 쓰는 독자만 보이는 자기선택 편향
- 강한 호감·불만이 과대표집되는 극단 반응
- 무료/유료 구간의 독자 구성이 다름
- 플랫폼 이벤트가 특정 감정 표현을 늘림
- 장기 독자와 신규 독자의 요구가 다름
- 완결 후 평가와 실시간 연재 평가가 다름

따라서 반응을 `몇 명이 말했는가`뿐 아니라 **어느 회차에서, 어떤 독자층이, 같은 증상을 얼마나 반복했는가**로 본다.

## 7. 벤치마크 작품의 표현 독립성

다른 작품에서 Base로 옮길 수 있는 것:

- 실패가 누적되는 기능
- 루틴을 변주하는 기능
- 외부 반응으로 성과를 보여주는 기능
- 강한 POV 필터
- 정보 비대칭 관리
- local payoff와 장기 질문의 조합

옮기지 않는 것:

- 대표 대사·문장
- 고유 비유
- 작가 고유 개그 리듬
- 사건 순서나 장면을 이름만 바꾼 복제
- 식별 가능한 캐릭터 voice

표현 복제 위험이면 `REJECT_COPY`와 `STYLE_COPY_RISK`를 기록한다.

## 8. Benchmark record

```yaml
work_or_source:
source_tier:
observed_at:
PRODUCT_FACT:
READER_RESPONSE:
CRAFT_HYPOTHESIS:
contrary_example:
TRANSFER_DECISION:
project_fit:
risks:
sample_limits:
```

한 작품에서 여러 원칙을 뽑을 수 있지만, Base에 승격하는 것은 서로 다른 장르·반례를 통과한 공용 원칙뿐이다.

## 9. Evidence ceiling

```yaml
platform_metric: SOURCE_DEFINED_ONLY
unique_reader_count: UNVERIFIED_UNLESS_PLATFORM_DEFINES_IT
craft_causality: HYPOTHESIS_UNLESS_TESTED
project_improvement: PROJECT_PILOT_REQUIRED
human_quality: HUMAN_NOT_RUN
commercial_outcome: NOT_RUN
```
