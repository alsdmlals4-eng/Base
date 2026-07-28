# 게임 개발 Case Card

> 성공 사례의 표면 기능을 복사하지 않고, **문제·맥락→접근 방식→관찰된 결과→적용 조건→비복제 요소→검증**을 기록한다. 성공·실패·혼합 사례를 같은 형식으로 비교한다.

## 0. 메타데이터

```yaml
case_id:
title:
classification: SUCCESS | FAILURE | MIXED
case_type: external_game | developer_postmortem | player_research | internal_project | ai_workflow | art_pipeline | technical_pipeline | release_operation
source_project_or_product:
platform_and_version:
observed_period:
created_at:
updated_at:
owner:
status: DRAFT | EVIDENCED | APPLIED | RETEST_REQUIRED | REFERENCE_ONLY | SUPERSEDED
related_evidence_ids: []
related_decision_ids: []
```

## 1. 문제·맥락

### 문제·맥락

- 해결하려던 플레이어 문제:
- 개발·제작 문제:
- 대상 플레이어와 플레이 상황:
- 장르·플랫폼·팀 규모·예산·일정 맥락:
- 당시 제품 단계·버전:
- 보호하려던 코어·약속:
- 비교할 현재 프로젝트 조건:

같은 기능이라도 장르·세션 길이·플랫폼·팀 규모가 다르면 결과를 그대로 일반화하지 않는다.

## 2. 접근 방식

### 접근 방식

```text
문제 정의
→ 선택한 원리·시스템·파이프라인
→ 실제 구현·운영 방식
→ 플레이어에게 노출된 변화
→ 측정·검증 방식
```

- 채택한 설계·기술·아트·운영 방식:
- 왜 이 방식을 선택했는가:
- 비교하거나 버린 대안:
- 필요한 도구·인력·데이터·자산:
- 예상한 성공·실패 조건:
- 실제 변경 범위:

## 3. 관찰된 결과

### 관찰된 결과

공식 사실·개발자 주장·플레이어 행동·플레이어 자기보고·분석자의 해석을 분리한다.

#### 공식·구현 사실

- 

#### 개발자·현업 보고

- 

#### 플레이어 행동

### 플레이어 행동

- 진입·완주·이탈:
- 선택·사용·반복 빈도:
- 소요 시간·실패·재시도:
- 텔레메트리·퍼널·성능:
- 관찰 표본·버전·한계:

#### 플레이어 자기보고

### 플레이어 자기보고

- 기대·이해·감정:
- 긍정·부정·혼합 반응:
- 리뷰·인터뷰·설문 맥락:
- 플랫폼·언어·플레이타임·패치:
- 자기보고 편향·한계:

#### 결과 판정

- `SUCCESS`인 이유:
- `FAILURE`인 이유:
- `MIXED`인 이유:
- 의도하지 않은 결과:
- 확인하지 못한 결과:

## 4. 원인 가설과 상충 근거

| 가설 ID | 원인 가설 | 지지 Evidence | 반박 Evidence | 신뢰도 | 추가 검증 |
|---|---|---|---|---|---|
| HYP-001 |  |  |  | HIGH/MEDIUM/LOW |  |

- 결과가 접근 방식 때문인지 다른 패치·가격·마케팅·콘텐츠·커뮤니티 조건 때문인지 분리한다.
- 상충하는 신뢰 가능한 근거는 숨기지 않고 `CONFLICTING_EVIDENCE`로 유지한다.

## 5. 적용 조건

### 적용 조건

```yaml
required_player_context:
required_game_loop:
required_platform_or_input:
required_content_volume:
required_team_or_tools:
required_data_or_testing:
required_accessibility_and_performance:
required_license_or_rights:
```

- 어떤 조건에서 이 원리가 작동했는가?
- 어떤 조건에서는 작동하지 않았는가?
- 현재 프로젝트와 같은 점:
- 현재 프로젝트와 다른 점:
- 1인 개발자가 축소·변형해야 할 부분:

## 6. 그대로 복제하지 않을 요소

### 그대로 복제하지 않을 요소

- 특정 IP·캐릭터·세계관·문구·시각 스타일:
- 프로젝트 고유 밸런스·수치·경제:
- 대규모 팀·예산·라이브 운영 전제:
- 플랫폼·시장·패치 시점에 종속된 요소:
- 접근성·성능·권리 위험:
- 성공 원인이 검증되지 않은 표면 기능:
- 현재 프로젝트 코어를 약화시키는 요소:

사례의 “모양”이 아니라 문제 해결 원리와 적용 조건을 검토한다.

## 7. 현재 프로젝트 적용 판정

판정:

- `ADOPT`
- `ADAPT`
- `TEST`
- `AVOID`
- `IGNORE`
- `REFERENCE_ONLY`

| 적용 후보 | 플레이어 가치 | 코어 정렬 | 제작 비용 | 기술·아트 위험 | 판정 | 검증 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

### 변형 설계

- 유지할 원리:
- 현재 프로젝트에 맞게 바꿀 부분:
- 제거할 부분:
- 필요한 PoC·Vertical Slice·플레이테스트:
- 정본 반영 위치:

## 8. 공용화 후보

### 공용화 후보

- 반복 가능한 원리:
- 사용 조건:
- 비사용 조건:
- 실패 조건:
- 필요한 Evidence:
- 검증 방법:
- 적용된 다른 프로젝트:
- 반례:

한 번의 성공은 `OBSERVATION` 또는 `HYPOTHESIS`다. 반복 검증 전 공용 강제 규칙으로 승격하지 않는다.

## 9. 프로젝트 전용 유지

### 프로젝트 전용 유지

- 세계관·캐릭터·사건·명칭:
- 밸런스 수치·ID·Schema:
- 실제 파일·경로·자산:
- 프로젝트 승인 이미지·Art Bible:
- 실제 플레이테스트·매출·리뷰 결과:
- 특정 플랫폼·출시 상태:

## 10. 검증·후속

```yaml
hypothesis_to_test:
build_or_artifact:
tester_or_eval_segment:
normal_failure_edge_counterexample:
behavior_and_self_report:
accessibility_and_performance:
security_license:
success_failure_stop:
result:
next_decision:
```

- 자동 검사:
- 런타임·목표 기기:
- 플레이테스트:
- AI Eval·독립 검수:
- 미검증:
- 재검증 시점:
- 롤백:

## 11. 출처

| Evidence ID | 원출처 | 게시일·버전 | 확인일 | 근거 층 | 근거 상태 | 사용 한계 |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

원문 전체를 복제하지 않고 출처와 사용 메모만 기록한다.
