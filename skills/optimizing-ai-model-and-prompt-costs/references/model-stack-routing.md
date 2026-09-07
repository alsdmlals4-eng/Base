# 모델 스택·추론 단계 라우팅

## 목적

작업을 단순히 “싼 모델 / 비싼 모델”로 나누지 않고, 틀렸을 때의 영향·숨은 판단·검증 가능성·재시도와 재작업 비용으로 분류한다. Luna / Terra / Sol은 논리적 작업 등급이며 실제 provider 모델 ID가 아니다.

## 세 등급

### `SIMPLE_BULK` — Luna 계열

적합 후보:

- 형식이 고정된 로그 요약·정리
- 명시된 Schema에 따른 변환
- 중복 제거·목록화·기계적 분류
- 결과를 자동 또는 표본으로 쉽게 검증할 수 있는 대량 작업

상향 조건:

- 파일 의미·기획 방향·보안·저장 호환성 판단이 섞임
- 누락이 후속 작업 전체를 오염시킴
- 입력이 상충하거나 정본이 불명확함
- 자동 검증이 없고 결과를 전수 재검토해야 함

### `ROUTINE_BALANCED` — Terra 계열

적합 후보:

- 일상적인 코드·문서 분석
- 승인된 계약 안의 작은 설계·리뷰
- 일반적인 Issue·Plan·테스트 초안
- 현재 정본과 실제 파일을 비교하는 중간 난도 작업

상향 조건:

- 다중 시스템 경계·권한·저장 Schema를 바꿈
- 실패 원인이 여러 층에 걸림
- 프로젝트 코어·중요 UX·출시 결정에 영향
- 결과를 되돌리기 어렵거나 배포 위험이 큼

### `HIGH_RISK_REASONING` — Sol 계열

적합 후보:

- 아키텍처·보안·데이터 무결성·복합 디버깅
- 프로젝트 코어·주요 UX·저장 호환성·릴리스 Gate 검토
- 상충하는 정본·근거·실제 구현을 조정하는 판단
- 실패 비용이 크고 독립 반례 검토가 필요한 작업

고성능 모델을 사용해도 검증을 생략하지 않는다. 모델 등급은 권한이나 승인 경계를 대체하지 않는다.

## 추론 단계

```yaml
LOW:
  use_when: 기계적 변환, 짧은 분류, 명확한 정답과 자동 검증
MEDIUM:
  use_when: 일상 분석, 여러 입력의 비교, 작은 설계 판단
HIGH:
  use_when: 복합 의존성, 보안·호환성·코어 위험, 적대적 검토
PROVIDER_SUPPORTED_VALUE:
  use_when: 제품 surface가 다른 이름이나 단계만 제공
```

제품에서 실제 제공하는 reasoning option을 확인하지 못하면 `UNVERIFIED`로 두고 존재하지 않는 설정을 추천하지 않는다.

## 숨은 위험 검사

낮은 등급을 추천하기 전 다음을 확인한다.

```text
정본 선택이 필요한가
→ 데이터 의미를 해석해야 하는가
→ 권한·보안 경계를 건드리는가
→ 저장·Schema·호환성에 영향이 있는가
→ 프로젝트 코어·중요 기획을 바꾸는가
→ 실패 결과가 다음 단계에 조용히 전파되는가
→ 독립 검증이 가능한가
```

하나라도 차단 위험이면 작업을 분리하거나 상향한다.

## 품질 우선 총비용

```text
순비용
= 최초 실행 비용
+ 재시도 비용
+ 결과 검수 비용
+ 상위 모델 재작업 비용
+ 실패 전파 복구 비용
```

Luna 초안을 Terra·Sol이 매번 전면 재작성하면 스택 최적화가 아니다. 낮은 등급의 산출물이 명시된 인터페이스와 검증 Gate를 통과해 다음 단계가 재사용할 수 있어야 한다.

## `[모델 추천]` checkpoint

사용자가 `[모델 추천]`을 말하면 현재 작업을 계속하기 전에 다음을 출력한다.

```yaml
recommended_model:
recommended_reasoning:
classification:
reason:
quality_risk:
retry_and_rework_risk:
next_checkpoint:
provider_profile_status:
continue_without_change_risk:
```

- 변경이 필요하면 현재 checkpoint에서 멈춘다.
- 사용자가 제품 설정을 바꾼 뒤 다음 작업부터 적용한다.
- 실행 중 응답이 자동으로 다른 모델로 바뀌었다고 주장하지 않는다.

## 재보정

실행 중 실패는 아래 **실패 원인별 다음 행동**을 먼저 적용한다. 상향은 추론·작업 난도 추천이지, 누락된 권한·필수 정본·실행 환경을 대신하는 수단이 아니다.

- 하위 등급이 품질 Gate를 지속 통과하고 순비용이 감소: 유지·확대
- 재시도나 누락이 늘어남: 상향 또는 작업 분리
- 상위 등급이 불필요한 장문·과잉 설계를 생성: 범위와 출력 계약을 먼저 줄임
- provider option 변경: profile을 다시 확인하고 `STALE_RECHECK_REQUIRED`

## 실패 조건

- 분량만으로 `SIMPLE_BULK` 판정
- 고위험 판단을 비용 때문에 하향
- 모델 이름을 능력·가용성의 영구 사실로 사용
- checkpoint 없이 작업 중 모델이 바뀌었다고 주장
- 재작업 비용을 절감 계산에서 제외

## 작업별 실행 방식 선택

이 절은 **판단용 reference**다. 모델 전환·위임·도구 호출·patch 적용을 실행하는 라우터가 아니며 현재 host의 권한을 만들지 않는다. 기존 Skill의 `route-model-and-effort` 또는 기존 작업 owner가 보고서 작성 시 필요 범위만 읽는다. 단일 모델 환경에서는 Registry 비사용 조건을 우회해 비용 Skill을 활성화하지 않는다.

먼저 기존 결정적 도구·validator로 끝낼 수 있는지 확인한다. 충분하면 그 도구를 재사용하며 아래 AI 패턴은 `NOT_APPLICABLE`로 기록할 수 있다. AI가 필요한 경우 **필수 품질·안전 기준을 만족할 수 있는 가장 단순한 방식**을 고른다. 가격이나 파일 수만으로 선택하지 않는다.

| 방식 | 선택 근거 | 단계 연결과 한계 |
|---|---|---|
| `Single` | 범위·정답·consumer가 명확하고 기존 검증으로 충분한 작업 | 한 실행자 → 실제 validator. 프로젝트의 필수 독립 검토·CI·runtime gate를 면제하지 않는다. |
| `Cascade` | 허용된 초기 실행의 결과를 객관적으로 평가할 수 있고 실패 때 상향의 이득을 설명할 수 있는 작업 | 초안 → gate → 통과 결과 재사용 / 실패 원인 분류 → 허용된 수정 또는 상향 추천. 처음부터 고위험인 판단을 값싼 실험으로 시작하지 않는다. |
| `Critique` | 계약·의존성·숨은 전제에 별도 관점이 필요한 작업 | 초안·exact revision·승인 요구·실제 증거 → 별도 문맥 검토 → 유효 finding만 수정 → 재검증. 검토자는 승인·병합 권한을 대신하지 않는다. |

이 방식은 `PLAN / BUILD / REVIEW`, 기획·검수·구현 단계, 기존 승인·검증·적대적 검토의 최소 전체 루프 수를 대체하지 않는다. Critique 한 번으로 기존 review floor를 충족했다고 보고하지 않는다. Human/UX 검증은 기존 사용자 선언·승인 계약을 유지하며 기계 검토로 대체하지 않는다.

실행 전 **실제 사용 가능한** 도구/실행자, 승인된 권한·비용 surface, 입력·산출물·검증 방법, 단계별 timeout/cancellation, retry/상향 한도를 확인한다. 값은 현행 owner와 작업 계약에서 가져오고 새 공용 횟수·모델명·가격 상수를 만들지 않는다. 한도가 없으면 해당 재시도/상향 계획은 미준비로 남겨 기존 owner에서 먼저 정한다. capability가 없으면 그 경로를 `UNVERIFIED`로 두며 호출했다고 보고하지 않는다.

### 실패 원인별 다음 행동

아래는 결과 설명용 분류이며 새 runtime 상태 머신이 아니다. 여러 원인이 겹치면 권한·안전·외부 효과 불명·필수 근거 차단을 먼저 해결한다.

| 관측 원인 | 다음 행동 | 허용하지 않는 해석 |
|---|---|---|
| 산출물 결함 | 실제 assertion/반례를 확보하고 승인 범위에서 bounded 수정·재검증; 현재 실행으로 해결하기 어렵다는 근거가 있을 때만 상향 추천 | 모든 실패에 무조건 더 강한 모델 사용 |
| 환경·도구 문제 | 실행 경로/환경을 현재 owner에서 복구; 검사 미실행은 `NOT_RUN`, 필수 증거 부족은 `BLOCKED_UNVERIFIED` | 엔진 부재를 코드 실패 또는 모델 역량 실패로 단정 |
| 정본·권한·의미 결정 부족 | 필수 source를 복원하고 권한·비용 gate 또는 `USER_DECISION_REQUIRED`로 연결 | 추론 강화로 승인·정본을 대체하거나 비용 경로 우회 |
| 외부 효과 불명·중단 | [기존 복구 owner](../../managing-project-intake-and-work-contract/references/task-recovery-protocol.md)의 RESUME으로 대상·request/result identity·postcondition을 확인 | Git 상태만으로 외부 성공을 판단하거나 timeout 뒤 blind replay |

필수 사용자 제공 source를 읽을 수 없는 경우 root `AGENTS.md`의 즉시 중단·검증 가능한 원문 요청 경계가 우선한다. 그 외 국소 blocker의 복구·보류·독립 작업은 [기존 연속작업 owner](../../managing-project-intake-and-work-contract/references/continuous-work-execution.md)에 위임한다. source 접근 불가와 읽은 source 간 충돌을 구분한다.

취소·검증 실패 시 후보를 완료 결과로 적용·병합하지 않는다. 이미 수정된 격리 작업본은 미검증 상태로 보존하고 기존 사용자 변경을 reset/discard하지 않는다. 외부 부작용이 발생했을 가능성은 위 복구 owner로 재조회한다. 이 문서는 원자적 patch 적용이나 exactly-once 실행을 구현했다는 증거가 아니다.

### 독립 검토의 증거 상한

별도 문맥과 다른 모델 계열은 구분해 기록한다. 같은 모델의 별도 문맥이면 그 사실을 표시하고, 현행 프로젝트/리뷰 계약이 요구하는 독립성 충족 여부를 따로 확인한다. 다른 계열은 실제 가용·권한·비용이 허용될 때의 선택지이며 강제 구매 조건이 아니다. 필요한 독립성이 없으면 해당 gate는 미충족으로 남긴다.

도구 없는 비평은 전달된 자료만 검토한 것이다. 저장소 읽기가 가능한 독립 리뷰와 동일시하지 않는다. 검토 입력은 승인 요구·exact revision/diff·필요한 consumer·검사 근거와 미검증 항목으로 제한하고 작성자의 결론을 정답으로 주입하지 않는다. 실제 파일·통합·runtime·Human 증거는 [기존 변경 검증 owner](../../reviewing-and-validating-project-changes/SKILL.md)와 [적대적 검토 owner](../../running-adversarial-review-and-refinement/SKILL.md)를 따른다.

### 기존 결과에 기록하기

새 파일/보드/스키마를 강제하지 않는다. 실행 방식을 실제 비교할 때만 아래 판단을 기존 Skill output의 `execution_strategy` 또는 현행 작업 계약/보고서에 기록한다. 단순 호출마다 반복 문서를 만들지 않는다. 키는 보고용 예시이며 실행기가 소비하는 JSON schema가 아니다.

```yaml
execution_strategy:
  pattern: Single | Cascade | Critique | NOT_APPLICABLE
  reason: 선택 근거와 비교한 대안
  capability_evidence: 현재 도구·실행자·권한·비용 surface 근거
  acceptance_gate: 기존 검사 owner와 실제 완료 조건
  limits: 현행 계약의 timeout·취소·retry·상향 한도 참조
  failure_and_next_action: 관측 원인·안전한 다음 행동·checkpoint
  review_independence: 별도 문맥/모델 계열/도구 접근의 실제 범위 또는 NOT_APPLICABLE
  observations: 실행 단계·결과·검증·재시도·재작업·시간/usage 근거와 미관측 항목
```

[기존 Skill 실행 보고](../../../templates/project-operations/SKILL_EXECUTION_REPORT.md)의 `사용 이유·Trigger`에 pattern/reason, `수행한 작업`에 실제 단계, `증거·경로`에 capability/gate/관측 근거, `미검증·실패`와 `다음 작업`에 원인·한도·checkpoint를 연결한다. 원래 과제 상태는 기존 Issue/계약이 소유하며 이 요약이 완료를 결정하지 않는다.

작업 전체의 초안·비평·수정·상향·재시도·fallback을 빠짐없이 관측하되 같은 호출을 중복 계수하지 않는다. 모델 식별자·실제 usage·시간·결과가 제공되지 않으면 관측 불가로 표시하고 0으로 채우지 않는다. 구독 포함 사용량은 재작업·실패·시간 지표로 평가하며 가상의 API 금액을 붙이지 않는다. 금액 절감률은 기존 비용 gate와 실제 청구/usage 근거를 만족하고, 같은 과제·품질 기준·환경에서 비교할 때만 계산한다.

**가상 예:** 승인된 작은 수정의 검증이 엔진 부재로 실행되지 않았다면 `Cascade` 상향 근거가 아니다. `failure_and_next_action`에 환경 문제·`NOT_RUN`·기존 엔진 경로 복구를 기록하고 검사부터 재개한다. 검사 후 실제 결함이 재현되면 그때 수정·상향 여부를 다시 판단한다. 예시 작성은 실제 작업 성공이나 절감의 증거가 아니다.

### 외부 사례의 채택 경계

2026-09-07 확인한 [GitHub HydraFusion 공식 발표](https://github.blog/ai-and-ml/github-copilot/project-hydrafusion-frontier-quality-via-multi-model-orchestration/)는 선택적 실행 조합·단계 제한·전체 호출 관측의 참고 근거다. `ADAPT`: 위 기존 owner 연결과 판단 기준만 흡수한다. `REJECT`: 제품 설치, 자동 모델 교체, 다른 계열 강제 사용, 단일 비평으로 Base review floor 대체, 발표 절감률을 프로젝트 실측으로 바꾸어 주장하는 행위. 연구 프리뷰와 통제된 오프라인 결과를 장기 Godot 작업 효과로 일반화하지 않는다. 프로젝트 성과와 모델 전환은 별도 실험 전 `NOT_RUN / NOT_MEASURED`다.
