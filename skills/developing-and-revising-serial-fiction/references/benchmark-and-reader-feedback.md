# 작품 벤치마크·독자 반응 실행 Reference

외부 작품과 독자 반응은 프로젝트 정본이 아니다. 성공작 표본은 선택 편향이 있고 플랫폼 지표의 정의도 서로 다르므로, 사실·반응·가설·전이 판단을 분리한다.

## Benchmark record

```yaml
source:
source_tier: PLATFORM | INDUSTRY | PUBLISHER | READER
observed_at:
platform_metric_name:
product_fact:
reader_response:
craft_hypothesis:
transfer_decision: ADOPT_INVARIANT | ADAPT_AS_LENS | PROJECT_ONLY | REJECT_COPY | INSUFFICIENT_EVIDENCE
sample_limits:
```

규칙:

- 조회·관심·선호·추천을 `고유 독자 수`로 임의 환산하지 않는다.
- 성공과 특정 문체·장치의 인과를 증명했다고 주장하지 않는다.
- 작품의 대표 문장·대사·비유·scene text를 Base에 복사하지 않는다.
- 특정 작가의 식별 가능한 voice를 재현하지 않는다. 그런 방향은 `STYLE_COPY_RISK`다.
- 반대되는 성공 사례를 최소 하나 찾아 최초 가설을 공격한다.

## Reader feedback pipeline

```text
RAW_REACTION
→ SYMPTOM_CLUSTER
→ REVISION_HYPOTHESIS
→ 원고·회차 위치 대조
→ 최소 수정
→ 회귀 검토
```

예:

```yaml
raw_reaction: "전개가 답답하다"
symptom_cluster: AGENCY_OR_PAYOFF
candidate_causes:
  - 주인공 주도권이 여러 회차 연속 없음
  - 같은 정보 반복
  - local payoff 지연
  - 목표 변화 불명확
revision_hypothesis: "전투를 추가"가 아니라 원고에서 실제 원인을 먼저 확인
```

한두 댓글의 해결책을 바로 요구사항으로 승격하면 `COMMENT_AS_CANON`이다.

## Adversarial comparison

외부 사례마다 다음을 묻는다.

1. 그 작품의 강점이라고 믿는 근거가 실제 제품 사실인가, 독자 반응인가, 내 추론인가?
2. 같은 원칙을 쓰지 않고 성공한 반례가 있는가?
3. 장르·POV·연재주기·독자층이 달라도 유지되는 기능인가?
4. 우리 프로젝트의 Reader Promise와 보호 정본을 강화하는가?
5. 표면 장치를 복사하지 않고 기능으로 추상화할 수 있는가?
6. 전이했을 때 새 실패 모드가 생기지 않는가?

불충분하면 `INSUFFICIENT_EVIDENCE`, 작품 전용이면 `PROJECT_ONLY`, 표현 복제 위험이면 `REJECT_COPY`로 둔다.
