# Game Feature Design Spec

> 적용: benchmark·PoC·adversarial review를 거쳐 `KEEP / CHANGE / RETEST` 대상으로 살아남았고 여러 직군이 같은 구현 의미를 공유해야 하는 **L2 주요 기능**.
>
> 권한: 이 문서는 기능이 플레이어에게 **무엇을 왜, 어떤 규칙과 상태로, 어떤 피드백을 통해 동작해야 하는지**를 책임지는 canonical detailed design source다.
>
> 비사용: `L0`·`L1` 단순 변경, pre-PoC 아이디어, `REMOVE / DEFER` 항목, 또는 전투 AI·UX/UI·아트·오디오 등 전문 정본이 같은 질문을 더 정확하게 이미 소유하는 경우.
>
> 비소유: **Task progress**, 구현 파일별 완료율, PR 상태, 실제 실행된 **executed verification** 결과는 이 문서가 소유하지 않는다. 승인 뒤 구현·검증 연결은 `FEATURE_SPEC_TRACEABILITY_PACKET.md`가 담당한다.

## 사용 원칙

```text
L0 Project Direction
→ L1 Feature Brief
→ Benchmark / PoC / Adversarial Review
→ L2 Game Feature Design Spec
→ Approval
→ L3 Feature Spec Traceability Packet
→ Implementation / Validation
```

- 불확실성이 싼 검증에서 살아남기 전에 상세 문서를 키우지 않는다.
- 전문 분야 정본이 더 정확하면 이 문서에 전문을 복제하지 않고 `source_id + path + section`으로 reference/compose한다.
- 사람용 기획·승인 요약은 프로젝트 Notion의 현재 Project 관계에 연결하고, 코드·데이터·Scene·Resource·검증 상태는 repository-native owner를 따른다. 이 Spec 전문을 별도 표나 외부 작업면에 복제해 새 정본으로 만들지 않는다.
- 구현 사실, 승인된 설계, 가설, 미결정을 같은 상태로 섞지 않는다.
- benchmark와 prototype은 설계 근거이지 사람 플레이 검증을 자동으로 대신하지 않는다.

---

## 0. Identity & authority

```yaml
feature_id:
feature_name:
work_level: L2
status: DRAFT | PROPOSED | APPROVED | SUPERSEDED
owner:
canonical_path:
related_decision_ids: []
related_pillar_ids: []
related_core_loop_ids: []
related_specialized_sources:
  - source_id:
    path:
    section:
    authority:
source_commit:
created_at:
updated_at:
```

### Authority boundary

- 이 Spec이 책임지는 질문:
- 다른 정본이 책임지는 질문:
- 이 Spec이 소유하지 않는 Task progress / implementation / executed verification:
- 대체하는 이전 Spec·Decision:

---

## 1. Player Problem

플레이어가 현재 어떤 문제·욕구·마찰을 겪고 있으며, 이 기능이 왜 필요한지 정의한다.

```yaml
player_problem:
current_behavior:
undesired_outcome:
desired_change:
evidence_ids: []
```

검사:

- 구현하고 싶은 기능 자체를 문제로 쓰지 않는다.
- 관찰·사용자 연구·기존 플레이테스트가 없다면 `HYPOTHESIS`로 표시한다.

---

## 2. Experience Intent & Core Alignment

### Experience Intent

- 플레이어가 해야 할 행동:
- 플레이어가 내려야 할 판단:
- 플레이어가 받아야 할 즉시 피드백:
- 플레이어가 느껴야 할 변화:
- 기능이 반복될 때 생겨야 할 숙련·전략:

### Core Alignment

| 연결 대상 | ID·원본 | 이 기능의 기여 | 위반 위험 |
|---|---|---|---|
| Project Promise | | | |
| Pillar | | | |
| Core Loop | | | |
| Resource Flow | | | |

기능이 핵심 경험과 직접 연결되지 않으면 `optional / support / remove-candidate` 중 하나로 분류한다.

### Planned evidence & first-session contract

이 Section은 **설계 단계에서 필요한 증거 질문과 관찰 계획**만 정한다. `PASS`·`FAILED` 같은 실제 실행 결과는 L3 Traceability와 변경 검증 원본에 기록한다.

```yaml
planned_evidence_layers:
  TECH_EVIDENCE:
  UI_EVIDENCE:
  HUMAN_USABILITY_EVIDENCE:
  PLAYER_EXPERIENCE_EVIDENCE:
first_session_contract:
  representative_problem:
  representative_action:
  first_meaningful_choice:
  first_observable_result:
  next_question_created:
time_window: FIRST_10_MINUTES_DEFAULT | PROJECT_ADAPTED
```

- `TECH_EVIDENCE` 또는 `UI_EVIDENCE`가 있어도 사람 이해·경험 증거를 대신하지 않는다.
- 첫 세션은 전체 기능 설명이 아니라 대표 문제 → 행동 → 선택 → 결과 → 다음 질문의 축소판인지 설계한다.
- 프로젝트 코어가 아닌 별도 미니게임 후보는 `MINIGAME_NARRATIVE_FUNCTION_GATE`의 본편 정보·의미 있는 결과·실패 학습·재사용성·제작비를 해당 전문 정본에 연결한다.

---

## 3. Scope / Non-goals

### In scope

- 항목:

### Out of scope

- 항목:

### Non-goals

- 이 기능이 해결하려 하지 않는 문제:
- 다른 시스템에 위임하는 책임:
- 이번 버전에서 의도적으로 지원하지 않는 경우:

### Minimum viable behavior

기능의 정체성을 잃지 않고 잘라낼 수 있는 최소 동작을 한 문단으로 정의한다.

---

## 4. Player Verbs & Decisions

| verb_id | Player Verbs | 입력·행동 | 플레이어 판단 | 비용·위험 | 기대 피드백 | 반복 빈도 |
|---|---|---|---|---|---|---|
| | | | | | | |

검사:

- `볼 수 있다`, `기능이 있다`만 쓰지 않고 플레이어가 실제로 수행하는 동사를 쓴다.
- 선택지가 있다면 각 선택이 무엇을 포기하고 무엇을 얻는지 기록한다.
- 자동 처리라면 플레이어가 언제 개입하거나 결과를 이해할 수 있는지 기록한다.

---

## 5. Entry / Exit / Cancel / Re-entry

| 구분 | 조건 | 허용 입력 | 시스템 처리 | 플레이어 피드백 | 다음 상태 |
|---|---|---|---|---|---|
| Entry | | | | | |
| Exit | | | | | |
| Cancel | | | | | |
| Re-entry | | | | | |

추가 확인:

- 진입 조건을 만족하지 못하면 무엇을 보여주는가?
- 중간 취소가 가능한가?
- 다시 들어왔을 때 초기화·유지·복구되는 것은 무엇인가?
- 장면 전환·재접속·save/load 뒤 상태는 어떻게 복원되는가?

---

## 6. Player Flow

```text
Trigger
→ Player sees/understands
→ Player input
→ Rule check
→ State transition
→ Immediate feedback
→ Reward/cost/consequence
→ Next decision
```

### Main flow

1. 단계 1:
2. 단계 2:
3. 단계 3:

### Alternate flows

- 대체 흐름 A:
- 대체 흐름 B:

### Flow diagram

필요하면 Mermaid 또는 현재 승인된 Notion/repository-linked visual artifact를 사용하되 실제 책임 규칙은 본문의 ID와 연결한다. 시각 자료는 의미를 보조하며 이 Spec의 규칙 권위를 대체하지 않는다.

---

## 7. State & Rules

### States

| state_id | State & Rules | 진입 조건 | 유지 조건 | 종료 조건 | 저장 여부 |
|---|---|---|---|---|---|
| | | | | | |

### State transitions

| from | trigger / condition | priority | to | invalid transition behavior |
|---|---|---|---|---|
| | | | | |

### Rules

| rule_id | 조건 | 판정·공식 | 결과 | 우선순위 | authority |
|---|---|---|---|---|---|
| | | | | | |

규칙 충돌 시 우선순위와 tie-breaker를 명시한다.

---

## 8. Input → Processing → Output

| io_id | Input | validation | internal processing | Output | side effect | failure behavior |
|---|---|---|---|---|---|---|
| | | | | | | |

- Input authority:
- Runtime state authority:
- Persistent data authority:
- Output consumer:

---

## 9. Feedback — UI / VFX / Animation / Audio / Haptics

| event_id | 플레이어가 알아야 할 것 | UI | VFX | Animation | Audio | Haptics | fallback |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

검사:

- 결과만 보여주지 말고 입력 수용·판정 중·성공·실패·복구를 구분한다.
- 색 하나, 소리 하나, 진동 하나에만 의미를 의존하지 않는다.
- 피드백 지연 허용 범위가 있으면 수치로 기록한다.

---

## 10. Success / Failure / Partial Success / Recovery

| outcome | 조건 | 플레이어가 보는 결과 | 비용·보상 | 다음 선택 | Recovery |
|---|---|---|---|---|---|
| Success | | | | | |
| Failure | | | | | |
| Partial Success | | | | | |
| Recovery | | | | | |

- 실패가 학습 가능한가?
- 재시도가 의미 있는가, 단순 반복인가?
- 실패 상태가 막다른 길을 만드는가?

---

## 11. Edge Cases

최소 다음을 검토한다. 해당 없음도 이유를 적는다.

| edge_id | 상황 | 기대 규칙 | 피드백 | 데이터 영향 | 검증 방법 |
|---|---|---|---|---|---|
| E01 | 자원 부족 | | | | |
| E02 | 반복·연타 입력 | | | | |
| E03 | 이미 변경된 상태에 재입력 | | | | |
| E04 | Cancel / leave / resume | | | | |
| E05 | Retry | | | | |
| E06 | Save / Load | | | | |
| E07 | Scene change / reconnect | | | | |
| E08 | UI 표시와 실제 state 불일치 | | | | |
| E09 | 중복 보상·중복 소비 | | | | |
| E10 | 최대·최소·0·overflow 경계값 | | | | |

---

## 12. Data & Balance

### Data authority

```yaml
runtime_authority:
persistent_authority:
authoring_source:
export_or_build_step:
```

### Variables and formulas

| data_id | 의미 | 단위 | 공식·관계 | initial recommended value | adjustment range | hard limit |
|---|---|---|---|---|---|---|
| | | | | | | |

### Retuning triggers

- 어떤 관찰이 나오면 수치를 조정하는가?
- 어떤 값은 디자인 상수이고 어떤 값은 밸런스 변수인가?
- 데이터 변경이 save compatibility에 영향을 주는가?

초기 숫자는 검증 전이면 `RECOMMENDED_DEFAULT` 또는 `HYPOTHESIS`로 표시한다.

---

## 13. UX/UI & Accessibility

### Interaction contract

- 주요 화면·surface:
- primary action:
- secondary action:
- focus order:
- keyboard/controller/touch 지원:
- cancel/back 동작:
- destructive action 확인:

### Decision screen check

핵심 화면은 장식이나 기능 목록보다 현재 결정이 먼저 읽혀야 한다. 다음 네 질문을 같은 화면 또는 명확히 연결된 상세 흐름에서 답할 수 있는지 확인한다.

```text
현재 상황은 무엇인가
무엇을 선택할 수 있는가
선택에 필요한 정보는 무엇인가
선택하면 어떤 비용·위험·결과가 예상되는가
```

의도적으로 숨기는 정보가 있어도 행동 목적·선택 가능성·숨김의 결과를 혼동시키지 않는다.

### Blueprint wireframe decision surface

`BLUEPRINT_WIREFRAME_DECISION_SURFACE` · `WIREFRAME_WITHIN_EXISTING_TWO_ARTIFACTS`

`TWO_ARTIFACT_PROFILE_CONDITIONALLY_APPLIES`: 사용자가 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD` profile을 선택했을 때만 이 record를 같은 ID의 사용자용 Blueprint PDF와 AI Markdown 안에 합성한다. 다른 publication profile에서는 그 프로젝트의 현행 design-document owner에 record를 두며, 이 양식이 두 산출물이나 중복 Blueprint 원본을 강제하지 않는다.

`WIRE_FRAME_ONLY_FOR_MATERIAL_PLAYER_FACING_SURFACE`: 이번 feature의 player-facing surface 중 레이아웃, 입력, 상태 또는 화면 동선 결정을 위해 필요한 화면만 기록한다. wireframe는 별도 파일·보드·이미지가 아니라 선택된 정본 안의 text-native 구조 표현이다. 적용하지 않는 surface는 `NOT_APPLICABLE_WITH_REASON`으로 남긴다.

`SMALLEST_REPRESENTATIVE_WIREFRAME_SET`: 같은 navigation/state contract를 재사용하는 화면을 중복 작성하지 말고, 현재 구현·검수 결정을 위해 필요한 최소 대표 집합만 선택한다.

| field | wireframe decision record |
|---|---|
| screen_id | |
| priority | P0 / P1 / P2 |
| target viewport / aspect | |
| input mode | keyboard / controller / touch / mixed |
| entry / exit / cancel / re-entry | |
| player goal / question / visual hierarchy | |
| primary / secondary action | |
| normal state | |
| disabled / error / unavailable state | |
| planned or actual consumer | scene / UI owner / planned surface |
| `SCREEN_LEVEL_COMPOSITION_REQUIRED` reference | screen inventory row or reuse evidence |
| wireframe status | REUSE / ADAPT / NEW_MINIMUM / NOT_APPLICABLE_WITH_REASON |
| evidence reference | capture, test, or `NOT_RUN` reason |

`WIREFRAME_NOT_RUNTIME_OR_USER_APPROVAL_EVIDENCE`: 이 record는 화면 구조와 navigation을 검토하는 `DOCUMENTED` evidence다. 실제 capture가 없으면 runtime은 `NOT_RUN`이며, capture·자동 테스트·wireframe 모두 Human/Player·device·UX·release 승인을 대체하지 않는다.

### Accessibility

| 요구 | 기본 방식 | 대체 방식 | 검증 상태 |
|---|---|---|---|
| 색 정보 | | | NOT_RUN / PASSED / BLOCKED_UNVERIFIED |
| 텍스트 크기·가독성 | | | |
| 모션·깜빡임 | | | |
| 오디오 정보 | | | |
| 입력 반복·홀드 | | | |
| 시간 제한 | | | |

전문 UI 정본이 있으면 이 Section은 핵심 요구와 경로만 유지한다.

---

## 14. Art / Audio / Narrative Dependencies

| dependency_id | 분야 | 필요한 입력 | owner/source | blocking? | fallback / placeholder |
|---|---|---|---|---|---|
| | Art | | | | |
| | Animation | | | | |
| | Audio | | | | |
| | Narrative | | | | |

- 임시 placeholder로 검증 가능한 것과 최종 자산이 필요한 것을 구분한다.
- 미확정 lore·아트 방향을 구현 사실처럼 고정하지 않는다.

---

## 15. Technical / Platform / Save / Online Constraints

| constraint_id | 영역 | 제약 | 설계 영향 | owner | status |
|---|---|---|---|---|---|
| | Performance | | | | CONFIRMED / HYPOTHESIS |
| | Platform | | | | |
| | Save | | | | |
| | Online | | | | |
| | Security / entitlement | | | | |

- target frame/time budget:
- memory/content budget:
- persistence boundary:
- offline/online fallback:
- deterministic/replay requirement:

---

## 16. Content Production Pipeline

반복 제작되는 콘텐츠가 있는 기능만 사용한다.

```text
Authoring source
→ validation
→ export/build
→ runtime load
→ QA sampling
→ live tuning / patch
```

| stage | tool/source | input | output | validation | owner |
|---|---|---|---|---|---|
| | | | | | |

- 사람이 반복 입력해야 하는 부분:
- 자동화 가능한 부분:
- 잘못된 데이터가 runtime에 들어갈 때 fail-closed 방식:
- 대량 콘텐츠 제작 시 대표 sample 검증 방식:

---

## 17. Benchmark Decision

Benchmark는 표면 복제가 아니라 해결 방법 비교에 사용한다.

| evidence_id | 출처·버전·접근일 | 비교 문제 | 관찰 | 한계 | Benchmark Decision | 이 기능 적용 |
|---|---|---|---|---|---|---|
| | | | | | ADOPT / ADAPT / TEST / AVOID / IGNORE | |

### Required comparison

가능하면 다음을 분리한다.

- 직접 경쟁·동일 장르 사례:
- 인접 문제를 다른 방식으로 푼 사례:
- 실패·불만·anti-pattern 사례:

추가 조사가 결정을 바꾸지 않을 정도가 되면 research를 종료하고 PoC로 이동한다.

---

## 18. Risk & Prototype

### Highest-risk hypothesis

```yaml
hypothesis_id:
claim:
why_it_can_kill_the_feature:
cheapest_test:
success_signal:
stop_signal:
evidence:
result: KEEP | CHANGE | RETEST | REMOVE | DEFER | BLOCKED_UNVERIFIED
```

### Risk register

| risk_id | risk | probability | impact | cheapest validation | mitigation | status |
|---|---|---|---|---|---|---|
| | | | | | | |

PoC가 없는 경우 왜 생략 가능한지 명시한다. `HUMAN_NOT_RUN`을 성공으로 바꾸지 않는다.

---

## 19. Acceptance Criteria

각 기준은 **조건 → 플레이어 행동 → 관찰 가능한 결과**로 작성한다.

| acceptance_id | 조건 | 플레이어 행동 | Acceptance Criteria — 관찰 가능한 결과 | failure evidence |
|---|---|---|---|---|
| AC-01 | | | | |

나쁜 예:

- `기능이 잘 동작한다.`
- `UI가 직관적이다.`

좋은 형식:

```text
Given <상태/조건>
When <플레이어 행동>
Then <화면·상태·수치·피드백에서 관찰 가능한 결과>
And <금지되는 부작용>
```

실제 테스트 실행 결과는 이 문서에 기록하지 않고 L3 Traceability의 verification evidence로 연결한다.

---

## 20. Telemetry / Playtest Observation Plan

| question_id | 확인할 질문 | 관찰·metric | segment | success signal | stop / rethink signal | status |
|---|---|---|---|---|---|---|
| | | | | | | NOT_RUN |

### Qualitative observation

- 플레이어가 어디서 멈추는가?
- 기능의 원인과 결과를 설명할 수 있는가?
- 의도한 판단을 실제로 하는가?
- 최적 행동 하나로 수렴하는가?
- 실패 뒤 무엇을 학습하는가?

Telemetry 수치만으로 재미·이해·만족을 자동 판정하지 않는다.

---

## 21. Cut-down / Rollback

### Cut-down order

| order | 제거·축소 대상 | 보존되는 핵심 경험 | 잃는 가치 | dependency impact | decision trigger |
|---|---|---|---|---|---|
| 1 | | | | | |

### Rollback

- 되돌릴 마지막 안전 상태:
- 데이터 migration 필요 여부:
- save compatibility 영향:
- feature flag / disable path:
- 복귀 후 재검증 항목:

---

## 22. Open Decisions

| decision_id | 질문 | 상태 | 권장 기본값·근거 | owner | blocking? | resolve_by |
|---|---|---|---|---|---|---|
| | | CONFIRMED / RECOMMENDED_DEFAULT / USER_DECISION_REQUIRED / HYPOTHESIS / BLOCKED_UNVERIFIED | | | | |

분류 원칙:

- `CONFIRMED`: 승인·정본 근거가 있다.
- `RECOMMENDED_DEFAULT`: 되돌리기 쉬운 기술·초기 시험값이며 AI가 근거와 함께 기본값을 제시할 수 있다.
- `USER_DECISION_REQUIRED`: 프로젝트 코어·방향·큰 범위·정본 충돌처럼 사용자 판단이 필요하다.
- `HYPOTHESIS`: 검증 전 가설이다.
- `BLOCKED_UNVERIFIED`: 필요한 원본·환경·권한·실행 결과가 없어 확인할 수 없다.

---

## 23. Handoff to Traceability

L2 Spec 승인 뒤에만 `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`를 사용한다.

```yaml
design_spec_id: <this feature_id or registered document id>
canonical_design_spec_path: <this file path>
approval_reference:
```

Traceability Packet으로 넘길 항목:

- 승인 Decision ID
- Requirement/Rule ID
- Acceptance Criteria ID
- 실제 구현 Task 연결 대상
- 실제 구현 경로 연결 대상
- Verification ID 생성 대상

넘기지 않을 전문:

- 전체 Player Flow 복사
- 전체 rule/state table 복사
- balance table 복사
- edge-case 설명 복사
- UI/Art/Audio 전문 복사

Packet은 이 Spec을 가리키고 실제 구현·검증 상태를 연결한다. 상세 설계가 바뀌면 먼저 이 canonical source와 승인 Decision을 갱신하고 Packet을 재대조한다.

---

## Final adversarial checklist

상세 Spec 승인 전에 다음을 공격한다.

- [ ] 아직 pre-PoC인데 문서만 과도하게 상세해지지 않았는가?
- [ ] Player Problem보다 솔루션 이름이 먼저 고정되지 않았는가?
- [ ] 플레이어 verb·decision 없이 시스템 내부 처리만 설명하지 않았는가?
- [ ] Entry/Exit/Cancel/Re-entry가 빠지지 않았는가?
- [ ] State transition과 rule priority가 충돌하지 않는가?
- [ ] 성공만 있고 실패·부분 성공·복구가 빠지지 않았는가?
- [ ] save/load·retry·연타·자원 부족·중복 보상 edge case를 놓치지 않았는가?
- [ ] UI·VFX·Audio가 같은 상태를 서로 다르게 말하지 않는가?
- [ ] 전문 분야 정본을 이 문서가 복제·대체하지 않는가?
- [ ] Benchmark를 표면 모방이나 권위 인용으로 사용하지 않았는가?
- [ ] PoC 결과를 실제 사람 검증으로 과장하지 않았는가?
- [ ] Acceptance Criteria가 관찰 가능한가?
- [ ] Cut-down이 핵심 경험을 보존하는 순서인가?
- [ ] USER_DECISION_REQUIRED와 되돌리기 쉬운 RECOMMENDED_DEFAULT를 구분했는가?
- [ ] Task progress·PR state·executed verification을 이 Spec이 소유하지 않는가?

하나라도 살아남은 `MUST_FIX`가 있으면 승인·L3 handoff 전에 수정한다.
