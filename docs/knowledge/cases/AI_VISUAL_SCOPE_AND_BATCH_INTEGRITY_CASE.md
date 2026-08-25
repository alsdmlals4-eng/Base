# 사례 — AI Visual Scope & Batch Integrity

- 연결 제안: `BCP-2026-035`
- 확인 날짜: 2026-08-25
- 작성 상태: 프로젝트 실행에서 관찰·복구된 패턴, 공용 contract 구현 검증 중
- 주제: 생성형 visual의 범위 충실도, 독립 산출물 수량, 판단 정보의 semantic redundancy, evidence ceiling

## 1. 문제

경계가 명확한 visual 요청에서도 생성 결과가 더 넓고 보기 좋은 결과로 drift하면 원래 질문이 해결되지 않을 수 있다. 또 사용자가 여러 개의 독립 이미지를 요청했는데 한 장의 multi-panel 합본이 나오면 검토·교체·배치 단위가 달라진다. 마지막으로 경로·선택·잠금·상태처럼 판단에 필요한 시각 정보가 배경과 경쟁할 때 단순히 스타일 전체를 바꾸거나 색만 강하게 만드는 대응은 기존 제품 정체성이나 접근성 경계를 훼손할 수 있다.

## 2. 관찰된 실패 형태

프로젝트 실행 증거에서 다음 유형이 함께 관찰됐다.

1. single-screen 성격의 요청이 broad dashboard 성격의 결과로 확대됐다.
2. N개의 독립 결과 요청이 한 개의 N-panel collage로 합쳐졌다.
3. decision-critical 상태가 art/background와 경쟁해 즉시 판독성이 약해졌다.
4. 고품질 mock/reference가 실제 runtime 또는 사람 검증처럼 오인될 여지가 생겼다.
5. 생성 파일 존재와 실제 human-facing workspace에서의 지속 소비 가능성이 혼동될 수 있었다.

이 사례는 문제와 복구 패턴을 지지하지만 `human comprehension`, accessibility, runtime/device correctness의 실제 PASS를 증명하지 않는다.

## 3. 대안 비교

### 대안 A — 결과가 보기 좋으면 넓어진 범위를 허용

- 장점: 탐색 단계에서는 우연한 아이디어를 얻을 수 있다.
- 위험: 원래 질문과 화면·상태가 사라져 완료 판정이 왜곡된다.
- 판단: bounded deliverable의 완료 규칙으로는 제외한다. broad concept board를 사용자가 요청한 경우에는 별도 계약으로 허용한다.

### 대안 B — 모든 시각 충돌에서 스타일 전체 교체

- 장점: 큰 대비 변화가 빠르다.
- 위험: 승인된 제품 정체성·기존 asset을 불필요하게 폐기할 수 있다.
- 판단: transformation 자체가 제품 의도인 경우를 제외하면 자동 기본값으로 두지 않는다.

### 대안 C — 기존 정체성을 보존하고 scope·산출물·semantic cue를 분리 관리

- 장점: 원래 visual question과 기존 제품 정체성을 보존하면서 판단 정보를 독립적으로 강화할 수 있다.
- 위험: 신호를 과도하게 겹치면 semantic overload가 생길 수 있다.
- 판단: BCP-2026-035의 기본 검토 경로로 채택한다.

## 4. 재사용 계약

### `VISUAL_TASK_SCOPE_FIDELITY`

bounded image 작업 전에 아래 네 필드를 고정한다.

```text
visual_question / target_screen / target_state / excluded_scope
```

결과가 `excluded_scope`를 넘어 unrelated screen, broad dashboard, 새 규칙·UI를 추가하면 같은 deliverable의 PASS로 세지 않는다. 탐색 가치가 있으면 별도 candidate로 보존할 수 있지만 원래 질문의 완료를 대신하지는 않는다.

### `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`

사용자가 N개의 이미지·결과를 요청하면 기본 의미는 독립 검토·교체·배치 가능한 N개의 deliverable이다. N-panel collage는 collage가 요청되거나 명시적으로 승인된 경우에만 N개와 동등하다. 의미 손실 없이 분리할 수 있으면 독립 결과로 분리하고, panel 의존성 때문에 분리 시 의미가 깨지면 재생성한다.

### `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`

판단 정보가 art/background와 경쟁하면 다음 세 방향을 비교한다.

```text
whole-style replacement
vs color/intensity-only emphasis
vs identity-preserving independent semantic redundancy
```

기존 정체성 보존 가치가 있으면 세 번째 방향을 먼저 검토한다. 필요한 독립 신호는 color, direction, shape, text/icon, brightness/thickness, motion 등에서 프로젝트 상황에 맞게 고른다. 특정 색·화살표·두께를 Base 공용 상수로 고정하지 않는다.

## 5. Notion과 원본 보존 경계

생성 결과의 human-facing 전달은 산출물 수량과 별개로 destination readback이 필요하다. preview를 만들어야 할 때도 approved original과 preview derivative의 책임을 분리한다. preview readback 성공은 Notion에서의 소비 가능성을 지지할 뿐 source-master, runtime, player validation을 자동 승격하지 않는다.

## 6. 적용 조건과 비사용 조건

적용:
- single-screen mock, state sheet, before/after, visual QA reference처럼 한 visual question이 있는 작업.
- 사용자가 산출물 개수 N을 명시한 작업.
- 중요한 상태·경로·선택 정보가 시각적 장식과 경쟁하면서 기존 제품 정체성을 보존할 가치가 있는 작업.

비사용:
- 사용자가 처음부터 poster, broad concept board, dashboard, collage를 원한 경우.
- 여러 panel이 하나의 비교 문맥이어야만 의미가 있는 경우.
- 제품 fantasy가 의도적 full transformation/style replacement인 경우.
- 순수 장식 색상처럼 판단 의미가 없는 표현.

## 7. 증거 상한과 검증

Repository contract 검증으로 확인할 수 있는 것:
- scope 필드와 산출물 단위가 문서·owner에 존재하는지.
- N-result 요청을 독립 deliverable 기본값으로 기록하는지.
- decision-critical semantic redundancy가 특정 프로젝트 값 없이 정의되는지.
- original-first/readback와 runtime evidence 경계를 약화하지 않는지.

Repository contract만으로 확인할 수 없는 것:
- 실제 사용자의 `human comprehension` 향상.
- 접근성 보조기기 적합성.
- 실제 게임 build에서의 판독성·성능·device correctness.
- 특정 이미지 모델이 다음 생성에서 scope drift를 일으키지 않는다는 보장.

따라서 자동 검증은 process contract PASS까지만 주장한다. 제품별 사람/실기기 검증은 각 프로젝트 evidence owner에서 별도로 수행한다.

## 8. 그대로 복사하면 안 되는 요소

- 특정 프로젝트의 art style name, mascot, palette, asset 수량, Candidate ID.
- 특정 숫자의 batch size.
- 특정 색·방향 화살표·선 두께를 모든 게임에 강제하는 규칙.
- mock/reference를 runtime 또는 player evidence로 승격하는 결론.

## 9. 후속 검증 질문

- 다른 프로젝트에서도 four-field scope contract가 broad-result drift를 조기에 발견하는가?
- 독립 산출물 수량 검사가 합본 결과를 올바르게 거부하면서 의도된 collage는 허용하는가?
- semantic redundancy가 기존 visual identity를 보존하면서 실제 플레이 판단 시간을 줄이는가?
- 신호를 추가한 결과가 작은 화면에서 semantic overload를 만들지는 않는가?

세 번째와 네 번째 질문은 실제 플레이·사람 관찰이 필요하므로 Base 문서 검증만으로 답하지 않는다.
