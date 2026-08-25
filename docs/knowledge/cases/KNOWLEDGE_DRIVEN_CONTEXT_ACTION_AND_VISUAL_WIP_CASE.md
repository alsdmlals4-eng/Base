# 사례 — 지식 기반 상황 행동 계층과 시각 WIP 의미 보존

- 출처 프로젝트·벤치마킹: `alsdmlals4-eng/urban-legend`
- 출처 기준 커밋: `4c1a7a51edc46a71af2a180a05220cae9254faca` (PR #232)
- 확인 날짜: `2026-08-25`
- 작성 상태: `부분 검증`
- 주제: `knowledge-driven interaction hierarchy / semantic visual review / durable image evidence`
- 사용자 승인 근거: 2026-08-25 작업에서 Recovery 상호작용 수정 방향을 승인했고, 종료 시 Base 승격과 문제·교훈 자료 보존을 명시 요청함.

## 1. 문제

지식 기반 게임의 첫 whole-screen mockup이 분위기와 시각 품질은 목표에 가까웠지만, 너무 많은 상시 행동을 한 레벨에 나열했다. 결과적으로 앞선 조사에서 배운 규칙을 적용하는 게임보다 일반 RPG command palette에서 버튼을 고르는 게임처럼 보였다.

동시에 시각적으로 매력적인 mockup을 의미 검증 없이 승인 자산으로 승격하면 다음 문제가 생긴다.

1. 잘못된 interaction hierarchy가 높은 미술 완성도에 가려진다.
2. 후속 구현자가 mockup을 현재 의미 정본으로 오독한다.
3. 채팅에만 남은 이미지와 판단 근거는 다음 세션에서 복구하기 어렵다.
4. 잘못된 whole-screen 구조를 먼저 component로 쪼개면 오류가 재사용 계층에 고착된다.

## 2. 맥락과 제약

- 플레이어 경험: 조사·기록·추리에서 얻은 지식이 이후 위험 상황의 실제 행동을 바꿔야 한다.
- 장르/플랫폼: Godot 기반 PC 조사·추리 게임이 출처지만 일반화 후보는 Godot 전용이 아니다.
- 제작: 소규모/AI 보조. 반복 생성보다 whole-screen 의미 승인 후 component 분해가 중요하다.
- 증거: 이미지 생성·사용자 스타일 선호·CI 성공은 runtime/Human/product-asset PASS와 분리한다.
- 권리: 생성 이미지는 product asset 승격 전 rights/provenance 검토가 별도다.

## 3. 관찰 근거

직접 확인한 프로젝트 책임 원본:
- `docs/decisions/D-2026-08-25-RECOVERY-CONTEXT-ACTION-HIERARCHY.md`
- `docs/RECOVERY_VISUAL_HANDOFF_2026-08-25.md`
- `docs/CURRENT_VISUAL_WORK_ORDER.md`
- `docs/VISUAL_ANCHOR_SPEC.md`

사용자 검토 결과:
- 상시 기본 행동을 작은 안정 카테고리로 줄이고, 전조/상황에 따른 구체 행동을 별도 층으로 분리하도록 승인했다.
- 앞선 조사·기록·추리에서 얻은 키워드와 규칙을 기억하거나 다시 확인해 상황 행동을 판단하도록 확정했다.
- 현재 화면이 정답을 색·확률·추천 표식으로 미리 알려주지 않도록 했다.

검증 증거:
- 동일 프로젝트 계약을 pre-implementation snapshot에서 RED, successor authority에서 GREEN으로 실행했다.
- Project PR #232 exact-head 일반 CI가 GREEN인 상태에서 main에 병합됐다.
- Recovery WIP는 Notion human authority에 native attachment로 올리고 destination readback했다.
- Recovery WIP receipt: `1672x941`, `2,399,097 bytes`, SHA-256 `606cb6998d4d1d08b44f96fe508b777e631786f05fdbd9a8c0d2b307dbe0e4d2`.

미검증:
- successor interaction의 실제 runtime 구현.
- 실제 플레이어의 기억/재확인 UX.
- 최종 해상도, 입력, 접근성, Human QA.

## 4. 검토한 대안

### A. 모든 행동을 상시 한 레벨에 노출
- 장점: 구현과 탐색이 단순하다.
- 단점: 일반 command와 사건별 지식 적용 행동이 섞여 `command soup`가 된다.
- 판정: 지식 기반 context에서는 `REJECT`.

### B. 전조 발생 시 정답 행동을 UI가 강조
- 장점: 실패율이 낮고 튜토리얼이 쉽다.
- 단점: 플레이어가 prior knowledge가 아니라 UI salience를 읽게 된다.
- 판정: `REJECT_DEFAULT`. 접근성 표현과 정답 노출은 분리한다.

### C. 작은 안정 카테고리 + 별도 contextual world actions
- 장점: 일상 command와 상황별 규칙 실행을 분리하고 prior knowledge를 실제 행동으로 재사용한다.
- 위험: context-action과 과거 지식 연결이 불명확하면 임의 퀴즈가 된다.
- 판정: `ADOPT_AS_PROJECT_DECISION / BASE_CASE_OBSERVATION`.

### D. 첫 whole-screen mockup을 바로 component/final asset으로 분해
- 장점: 빠르다.
- 단점: 의미 오류가 재사용 component로 확산된다.
- 판정: `REJECT`; semantic review를 먼저 한다.

## 5. 결정 구조

```text
prior evidence / learned rule
→ current telegraph or situation
→ context-specific world actions
→ player recalls or re-checks prior knowledge
→ concrete response
→ outcome + new observation
```

UI:
```text
small stable categories
+ separate contextual action layer
+ no answer-salience shortcut
```

Visual production:
```text
whole-screen mockup
→ semantic review
→ APPROVED or REVISION_REQUIRED
→ approved direction only
→ reusable component extraction
→ runtime/readability/rights validation
```

## 6. 결과와 evidence ceiling

- 프로젝트 Recovery interaction 의미 계약이 successor decision으로 고정됐다.
- 의미 hierarchy가 틀린 첫 시안은 삭제하지 않고 `REFERENCE_MOCKUP / REVISION_REQUIRED / NOT_PRODUCT_ASSET`으로 보존했다.
- cold-start handoff에 이미지 receipt, correction contract, evidence ceiling, 다음 image gate를 같이 남겼다.
- 시각 품질이 semantic correctness를 대신하지 못한다는 직접 반례가 확보됐다.
- successor runtime과 Human playtest가 아직 없으므로 이 문서는 `부분 검증` case이며 universal gameplay law나 mandatory Skill이 아니다.

## 7. 재사용 가능한 원칙

### `STABLE_CATEGORY_CONTEXT_ACTION_SPLIT`
지식 기반 상황 대응에서는 소수의 안정 domain category와 현재 상황에서만 유효한 world action을 같은 1차 command 층에 평평하게 섞지 않는 것을 우선 검토한다.

### `PRIOR_KNOWLEDGE_MUST_CHANGE_ACTION`
조사·분석 정보가 핵심이라면 이후 phase에서 그 정보를 다시 설명하는 데 그치지 말고 실제 행동 선택을 바꾸게 한다.

### `SEMANTIC_REVIEW_BEFORE_VISUAL_PROMOTION`
멋진 이미지라도 interaction/mechanic/narrative meaning이 틀리면 승인 asset으로 승격하지 않는다. `REVISION_REQUIRED`와 correction contract를 이미지 옆에 보존한다.

### `WHOLE_MOCKUP_BEFORE_COMPONENT_EXTRACTION`
복잡한 화면은 먼저 전체 composition과 interaction hierarchy를 검수하고, 승인 뒤에만 reusable component로 분해한다.

### `DURABLE_VISUAL_RECEIPT_WITH_EVIDENCE_CEILING`
채팅/임시 URL에만 이미지를 두지 않는다. 사람용 권위 저장소에 durable attachment로 저장하고 destination readback한다. `reference`, `approved candidate`, `product asset`, `runtime pass`, `Human pass`를 분리한다.

### `FAILURE_CAN_BECOME_KNOWLEDGE`
오대응이 있는 지식 기반 시스템에서는 실패를 자원 손실로만 끝낼지 검토한다. 실패 반응이 이후 판단 근거가 될 수 있다면 관찰 기록으로 보존하는 것이 학습 루프를 강화할 수 있다.

현재는 새 Method/Skill 승격 후보로 만들지 않는다. 두 번째 독립 프로젝트에서 같은 문제가 반복되면 기존 game-feature/visual-review owner에 focused checklist를 추가할지 검토한다.

## 8. 그대로 복사하면 안 되는 요소

- 프로젝트 사건명, 캐릭터명, 구체 키워드, 특정 전조/장치.
- 출처 프로젝트의 실제 세 command label 자체. Base의 universal command vocabulary가 아니다.
- 생성 이미지를 Base asset으로 복사하는 것. Base에는 구조·receipt·교훈만 남긴다.

비사용 조건:
- 모든 tactical command가 매 순간 동등하게 상시 필요할 때.
- twitch action처럼 contextual menu 자체가 흐름을 해칠 때.
- prior knowledge 재사용이 핵심이 아닌 시스템.

## 9. 검증 방법

자동:
- current authority가 predecessor와 successor hierarchy를 동시에 current로 주장하지 않는지 확인.
- `REFERENCE/REVISION_REQUIRED`를 `PRODUCT_ASSET`과 혼합하지 않는지 확인.

수동:
- whole-screen에서 stable category와 contextual action을 즉시 구분할 수 있는지.
- 정답 선택지만 시각적으로 두드러지지 않는지.

사용자/Human:
- 이전 조사 기록을 근거로 현재 행동을 설명할 수 있는지.
- 잘못된 선택 뒤 무엇을 새로 배웠는지 설명할 수 있는지.

## 10. 관련 문서와 Base 동시성

Base:
- `skills/managing-base-change-proposals/SKILL.md`
- `templates/KNOWLEDGE_CASE_STUDY.md`

Project:
- `alsdmlals4-eng/urban-legend@4c1a7a51edc46a71af2a180a05220cae9254faca`
- `docs/decisions/D-2026-08-25-RECOVERY-CONTEXT-ACTION-HIERARCHY.md`
- `docs/RECOVERY_VISUAL_HANDOFF_2026-08-25.md`

Concurrency note:
- 제출 시 Base proposal/Registry에는 별도 활성 workstream이 존재한다. 이 case는 그 소유권을 흡수하지 않는다.
- 이 사용자 직접 승인 작업은 active Base Method/Skill을 바꾸지 않는 **additive case promotion**으로만 수행한다.
- 기존 open Base PR은 모두 read-only로 유지한다.
