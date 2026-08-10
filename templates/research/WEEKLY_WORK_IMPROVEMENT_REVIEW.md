# Weekly Work Improvement Review

> 역할: 외부 근거·현재 프로젝트 상태·최근 PR·지난 보고서의 차이를 **행동 가능한 주간 개선안**으로 합성하는 비정본 Template.
>
> 이 Template은 새 Skill이나 새 정책 owner가 아니다. 실제 근거와 변경 권한은 각 현행 owner가 유지한다.

## 0. 책임 경계와 Read First

```text
최신 Base main + 대상 프로젝트 최신 정본/실제 구현
→ 같은 Goal의 열린·최근 병합 PR
→ 지난 주간 보고서
→ docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
→ 현재 결정에 필요한 domain owner만 선택
→ ORIGINAL_SOURCE_BACKTRACE
→ 적대적 검토
→ Base 승격 / 기존 owner 흡수 / 프로젝트 전용 / 실험 / NO_CHANGE
```

필요한 기존 owner:

- Source discovery/evidence: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
- Game benchmark/player evidence: `analyzing-and-refining-game-concepts`
- Fiction/serial writing: `developing-and-revising-serial-fiction`
- Prompt/Skill boundary: `docs/AI_SKILL_ADOPTION_GUIDE.md` + `evolving-project-discipline-skills`
- Player-experience evidence ceiling: `docs/knowledge/game-development/GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE.md`
- Independent attack/critique validation: `running-adversarial-review-and-refinement`
- Base promotion: `managing-base-change-proposals`

독립 tool/permission/authority/입출력/검증 경계가 없는 한 `weekly-work-improvement` 또는 `conducting-weekly-improvement` 같은 새 ACTIVE Skill을 만들지 않는다.

## 1. 보고서 실행 메타데이터

```yaml
report_week:
checked_at:
base_main_sha:
project_snapshots:
  - project:
    main_sha_or_canonical_revision:
    current_goal:
    actual_implementation_checked:
previous_report:
PREVIOUS_REPORT_DELTA:
  changed_since_last_report: []
  priority_increased: []
  priority_decreased: []
  repeated_finding_with_new_evidence: []
  intentionally_not_repeated: []
open_and_recent_prs_checked: []
source_domains_checked: []
source_coverage:
  full_index_review: []
  partial_index_review: []
  static_reference_review: []
unverified_scope: []
```

### 중복 억제

지난 보고서와 동일한 작품·자료·권고는 자동 반복하지 않는다. 다시 다룰 조건은 `NEW_EVIDENCE_OR_NEW_COMPARISON_DIMENSION`이다.

```yaml
repeat_item:
NEW_EVIDENCE_OR_NEW_COMPARISON_DIMENSION:
  new_source_or_update:
  changed_project_context:
  new_failure_or_player_evidence:
  new_comparison_dimension:
why_repeat_is_decision_relevant:
```

새로운 근거나 비교 가치가 없으면 `N/A — reason: previous report already covers this`로 줄인다.

## 2. Evidence 카드

외부 자료마다 최소 다음을 남긴다.

```yaml
source:
discovered_from:
ORIGINAL_SOURCE_BACKTRACE:
published_or_updated_at:
freshness:
scope:
platform_or_medium:
sample_or_method:
commercial_or_vendor_interest:
evidence_status:
claim_type: SOURCE_FACT | PLAYER_OR_READER_EVIDENCE | PROFESSIONAL_OFFICIAL_GUIDANCE | MODEL_INFERENCE | PROJECT_RECOMMENDATION
base_overlap: NONE | PARTIAL | ALREADY_COVERED | CONFLICT
candidate_disposition: ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
```

원출처가 없는 뉴스·newsletter·DISCOVERY_FEED·vendor benchmark는 정본으로 올리지 않는다. 숫자는 표본·관찰 기간·수집 방법을 함께 보존하고 상관관계를 인과로 바꾸지 않는다.

## 3. 벤치마킹 선택 규칙

가능하면 각 영역에서 다음 비교군을 찾되 **결정을 바꿀 때만** 사용한다.

- 직접 경쟁작 — 장르·핵심 행동·독자 약속이 직접 겹침
- 인접 장르 — 구조·감정·운영 문제는 유사하지만 핵심 플레이가 다름
- 장르 밖 참고작 — UI, 감정, 반복 보상, 정보 공개, 상징, 제작 방식 등 현재 질문에 직접 도움
- 실패·혼합 반응 — 평가 하락, 과도한 복잡성, UI 마찰, 반복 피로, 제작비 폭증 등 반례

세 칸을 채우기 위한 작품 나열은 금지한다. 관련 후보가 없으면 `N/A — reason`을 기록한다.

각 benchmark는 결론을 다음으로 닫는다.

```yaml
reference:
comparison_dimension:
observed_strength_or_failure:
context_limit:
그대로_참고할_요소:
현재_프로젝트에_맞게_변형할_요소:
도입하지_말아야_할_요소:
작은_실험으로_검증할_요소와_성공_기준:
```

---

# A. 메인게임

메인게임은 핵심 플레이 루프, 전투·탐사·성장·휴식, 세션 구조, 시스템 연결, 빌드 다양성, 플레이어 감정, 세일즈포인트를 우선한다.

## 1) 이번 주 핵심 변화와 근거

- 변경된 프로젝트 사실:
- 새 외부 근거:
- `PREVIOUS_REPORT_DELTA`:
- 판단:

## 2) 현재 작업 방식의 개선점

- 유지할 강점:
- 누락/마찰:
- Existing Solution First 판정:
- 가장 작은 개선 단위:

## 3) 직접 경쟁작·인접 장르·장르 밖 참고작 벤치마킹

- 직접 경쟁작:
- 인접 장르:
- 장르 밖 참고작:
- 실패·혼합 반응:
- 새 근거가 없는 반복 작품: `N/A — reason`

## 4) 핵심 플레이어 또는 독자 경험

- 한 문장 경험 약속:
- 반복 감정:
- 제거 시 약속이 무너지는 요소:

## 5) 첫 10분 또는 첫 장면의 인상

- 첫 문제:
- 대표 행동:
- 첫 선택:
- 첫 결과:
- 다음 질문:

## 6) 핵심 루프 또는 장면 진행 구조

```text
입력/징후
→ 판단
→ 행동
→ 피드백
→ 결과/비용
→ 다음 선택
```

## 7) 반복 피로도와 감정 곡선

- 반복되는 구조:
- 변주가 필요한 축:
- 긴장/회복/보상 곡선:

## 8) 선택과 결과, 보상 또는 정보 공개 구조

- 무엇을 선택하는가:
- 무엇을 포기하는가:
- 결과를 언제 확인하는가:
- 실패해도 무엇을 배우는가:

## 9) 온보딩·UI/UX 또는 문장 가독성

- 첫 행동까지의 마찰:
- 현재 상황/선택/필요 정보/비용·위험·결과:
- 접근성·입력·화면 제약:

## 10) 비주얼 아이덴티티·마스코트·상징·문체

- 한 장면/한 상징으로 전달되는 정체성:
- 현재 프로젝트의 고유 자산:
- 모방 금지/권리 위험:

## 11) 콘텐츠 제작 비용과 1인 제작 현실성

| 항목 | 구현 비용 | 반복 콘텐츠 비용 | 유지/QA 비용 | 재사용성 | 판정 |
|---|---:|---:|---:|---:|---|
|  |  |  |  |  | KEEP / SIMPLIFY / TEST / CUT |

## 12) 판매 포인트 또는 독자 유입 포인트

- 플레이 장면으로 증명 가능한 한 문장:
- 스크린샷/GIF/데모에서 보이는가:
- 외부 지표와 실제 구매의도를 혼동하지 않았는가:

## 13) 성공 요인과 실패·이탈 요인

- 성공 가설:
- 이탈/피로 가설:
- 근거 상태:

## 14) 그대로 참고할 요소

- 

## 15) 현재 프로젝트에 맞게 변형할 요소

- 

## 16) 도입하지 말아야 할 요소

- 

## 17) 작은 실험으로 검증할 요소와 성공 기준

```yaml
experiment:
research_question:
method: observation | interview | analytics | survey | mixed | deterministic_check
evidence_type: TECH_EVIDENCE | UI_EVIDENCE | HUMAN_USABILITY_EVIDENCE | PLAYER_EXPERIENCE_EVIDENCE | PLAYER_OR_READER_EVIDENCE
participants_or_sample:
controlled_variables:
success_criteria:
failure_or_stop_condition:
```

---

# B. 미니게임

미니게임은 독립 재미보다 메인게임/에피소드/글쓰기 흐름에서 수행하는 기능을 먼저 검증한다. 규칙 학습 시간, 반복성, 실패 부담, 보상 연결, 재사용성, 제작비, 서사 흐름 방해 여부를 우선한다. 핵심 플레이 자체가 퍼즐/액션이면 미니게임이 아니라 core interaction으로 분류한다.

## 1) 이번 주 핵심 변화와 근거
- 

## 2) 현재 작업 방식의 개선점
- 

## 3) 직접 경쟁작·인접 장르·장르 밖 참고작 벤치마킹
- 직접 경쟁작:
- 인접 장르:
- 장르 밖 참고작:
- 실패·혼합 반응:
- 새 근거가 없는 반복 작품: `N/A — reason`

## 4) 핵심 플레이어 또는 독자 경험
- 미니게임이 강화해야 하는 본편 경험:

## 5) 첫 10분 또는 첫 장면의 인상
- 진입 전 목적 이해:
- 첫 30초 규칙 학습:

## 6) 핵심 루프 또는 장면 진행 구조
- 본편 정보 → 검증 행동 → 결과 → 본편 상태 변화:

## 7) 반복 피로도와 감정 곡선
- 반복 횟수/시간:
- 정답을 안 뒤 남는 조작 부담:

## 8) 선택과 결과, 보상 또는 정보 공개 구조
- 실패가 주는 정보/비용:
- 본편 보상 연결:

## 9) 온보딩·UI/UX 또는 문장 가독성
- 규칙을 30초 안에 설명 가능한가:
- 실패 이유가 UI로 구분되는가:

## 10) 비주얼 아이덴티티·마스코트·상징·문체
- 본편 UI/세계관 도구처럼 보이는가:

## 11) 콘텐츠 제작 비용과 1인 제작 현실성
- 공통 프레임/데이터 교체 재사용성:
- 에피소드별 전용 코드·아트 비용:

## 12) 판매 포인트 또는 독자 유입 포인트
- “미니게임 수”가 아니라 본편 경험을 어떻게 증명하는가:

## 13) 성공 요인과 실패·이탈 요인
- 독립 재미가 있어도 서사 흐름을 끊는가:
- 준비/육성/장비가 정답을 대신하는가:

## 14) 그대로 참고할 요소
- 

## 15) 현재 프로젝트에 맞게 변형할 요소
- 

## 16) 도입하지 말아야 할 요소
- 

## 17) 작은 실험으로 검증할 요소와 성공 기준

```yaml
experiment:
research_question:
method:
evidence_type:
success_criteria:
removal_test: "미니게임을 선택지/간단 인터랙션으로 대체했을 때 무엇이 약해지는가?"
```

---

# C. 글쓰기

글쓰기는 로그라인, Reader Promise/테마, 캐릭터 욕망과 갈등, 장면 목적, 정보 공개, 복선, 선택지, 대사, 서술, 감정 변화, 사건 타임라인, 에피소드 구조, 독자 정보 관리, 첫 장면 흡입력, 연재 반복 제작 현실성을 우선한다.

## 1) 이번 주 핵심 변화와 근거
- 

## 2) 현재 작업 방식의 개선점
- developmental/structure 문제와 line/copy/proof 문제를 분리한다.

## 3) 직접 경쟁작·인접 장르·장르 밖 참고작 벤치마킹
- 직접 경쟁작:
- 인접 장르:
- 장르 밖 참고작:
- 실패·혼합 반응:
- 새 근거가 없는 반복 작품: `N/A — reason`

## 4) 핵심 플레이어 또는 독자 경험
- Reader Promise:
- 이번 회차/장면이 주는 Episode Value:

## 5) 첫 10분 또는 첫 장면의 인상
- 첫 질문:
- 첫 상태 변화:
- 설명보다 먼저 보이는 사건/욕망/이상:

## 6) 핵심 루프 또는 장면 진행 구조

```text
장면 질문
→ 관찰 사실
→ 인물 해석/욕망
→ 충돌/모순
→ 행동/선택
→ 결과/감정 변화
→ 새 질문 또는 Local Payoff
```

## 7) 반복 피로도와 감정 곡선
- 직전 유사 회차와 달라진 규칙/비용/관계/정보/실패 형태:

## 8) 선택과 결과, 보상 또는 정보 공개 구조
- 관찰 사실 / 인물 진술 / 공식 기록 / 규칙 후보 / 확정 정보 / 미해결:
- 선택의 consequence memory:

## 9) 온보딩·UI/UX 또는 문장 가독성
- POV/즉시 목표/장애/행동 뒤 변화가 추적되는가:
- 한 화면/한 문단 정보 밀도:

## 10) 비주얼 아이덴티티·마스코트·상징·문체
- 고유 voice/상징:
- 특정 작가의 식별 가능한 style imitation은 금지:

## 11) 콘텐츠 제작 비용과 1인 제작 현실성
- 회차당 신규 장소/인물/분기/아트/대사 비용:
- 완전 분기 대신 반응/정보/후일담 변형 가능성:

## 12) 판매 포인트 또는 독자 유입 포인트
- 로그라인/첫 장면/연재 hook이 같은 약속을 하는가:

## 13) 성공 요인과 실패·이탈 요인
- 구조·pacing·character 문제:
- 문장·일관성 문제:
- 독자 self-report와 실제 원고 증거를 구분했는가:

## 14) 그대로 참고할 요소
- 

## 15) 현재 프로젝트에 맞게 변형할 요소
- 소설 craft를 게임 스토리에 옮길 때 agency/state/branch/runtime 차이는 별도 TEST:

## 16) 도입하지 말아야 할 요소
- 단일 story structure의 보편 강제:
- game branching 규칙을 선형 소설 모든 장면에 강제:

## 17) 작은 실험으로 검증할 요소와 성공 기준

```yaml
experiment:
research_question:
method: blind_read | comparative_read | reader_interview | revision_audit | mixed
evidence_type: PLAYER_OR_READER_EVIDENCE | HUMAN_USABILITY_EVIDENCE | MODEL_INFERENCE
success_criteria:
revision_layer: DEVELOPMENTAL_STRUCTURE | SCENE_AND_CHARACTER | DIALOGUE_AND_INFORMATION | LINE_AND_PROSE | COPY_AND_PROOF
```

---

# D. 종합 반영안

## 1) 세 영역 사이의 충돌과 시너지

| 관계 | 메인게임 | 미니게임 | 글쓰기 | 시너지/충돌 | 조치 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 2) 이번 주 최우선 실행 제안

최대 1~3개. “중요해 보임”이 아니라 실제 현재 Goal·리스크·의존성으로 정렬한다.

## 3) 추가하면 좋은 요소
- 

## 4) 제거하거나 단순화할 요소
- 

## 5) 공용 규칙 저장소 Base에 승격할 후보

```yaml
candidate:
disposition: BASE_PROMOTION_CANDIDATE | ABSORB_EXISTING_OWNER | EVIDENCE_ONLY | NO_CHANGE
existing_owner:
repeatability_across_projects:
independent_boundary_if_new_skill_is_proposed:
evidence:
BCP_or_low_risk_path:
```

`BASE_PROMOTION_CANDIDATE`는 즉시 정본 변경이 아니다. 현행 BCP/저위험 흡수 경계를 따른다.

## 6) 프로젝트 전용으로 남길 반영사항

각 항목에 반드시 목적지를 쓴다.

```yaml
finding:
disposition: PROJECT_ONLY | TEST | AVOID | NO_CHANGE
target_project_or_consumer:
project_canon_owner:
why_not_base:
next_action:
```

캐릭터명·세계관·수치·저장 구조·특정 UI layout·특정 채널 방향은 기본 `PROJECT_ONLY`다.

## 7) 문서·GitHub Issue·Codex Goal·테스트 체크리스트에 바로 반영할 구체적 문구

### GitHub Issue

```md
제목:
목표:
플레이어/독자 관찰 결과:
포함:
제외:
완료 기준:
검증:
```

### Codex Goal

```text
목표:
읽을 정본:
실제 구현에서 먼저 확인할 것:
보호 대상:
포함/제외:
완료 기준:
실행할 검증:
미실행 검증 보고 규칙:
```

### 테스트 체크리스트

```text
[ ] 현재 Goal에 연결된다.
[ ] 실제 플레이/원고/데이터에서 확인 가능하다.
[ ] 실패 이유 또는 반례를 설명할 수 있다.
[ ] 실행하지 않은 검증은 NOT_RUN이다.
```

## 8) 확인이 필요한 불확실한 항목

- `BLOCKED_UNVERIFIED`:
- 확인할 정본/도구/사람 증거:
- 확인 전 금지할 결론:

## 9) 이번 주에 바로 실행할 수 있는 소규모 검증 과제 1~3개와 각 성공 기준

각 과제는 먼저 질문을 정하고 그 질문에 맞는 방법을 고른다. 편한 방법을 먼저 고르지 않는다.

```yaml
experiment_id:
research_question:
why_this_question_changes_a_decision:
method: observation | interview | analytics | survey | mixed | deterministic_check | comparative_read
participant_or_sample:
evidence_type:
success_criteria:
stop_or_rollback_condition:
follow_up_decision:
```

관찰은 행동을, 인터뷰는 동기/mental model을, analytics는 규모와 패턴을, survey는 측정·비교 가능한 자기보고를 주로 다룬다. 한 방법이 다른 방법의 약점을 자동으로 보완한다고 가정하지 않는다.

---

## 4. 최종 판정과 적대적 검토

보고서 초안 뒤 반드시 `running-adversarial-review-and-refinement`의 `attack → validate-critique`를 적용한다.

공격 질문:

- 같은 Goal의 열린·최근 병합 PR이 이미 해결하거나 수정 중인가?
- 지난 보고서의 문구를 새 근거 없이 반복했는가?
- 성공작만 골라 기능 증가 편향을 만들었는가?
- 실패·혼합 반응의 맥락을 빼고 성공 공식을 만들었는가?
- vendor/creator/newsletter 수치를 공식 플랫폼 사실로 썼는가?
- CTR/retention/views/review score를 구매·품질·재미의 직접 인과로 해석했는가?
- AI/CI/screenshot/작성자 self-review를 `HUMAN_USABILITY_EVIDENCE` 또는 `PLAYER_EXPERIENCE_EVIDENCE`로 승격했는가?
- 소설 craft를 player agency/state/branch/runtime에 그대로 강제했는가?
- 프로젝트 전용 설정을 Base 공용 규칙으로 올렸는가?
- 기존 owner에 흡수할 수 있는데 새 Skill/Guide를 만들었는가?
- 새 규칙이 없다는 이유로 작은 reference/test/checklist/freshness 개선을 버렸는가?
- 반대로 개선이 없는데 “매주 뭔가 바꿔야 한다”는 이유로 억지 변경을 만들었는가?

최종 결과는 다음 중 하나 이상으로 닫는다.

```text
BASE_PROMOTION_CANDIDATE
ABSORB_EXISTING_OWNER
PROJECT_ONLY
EVIDENCE_ONLY
TEST
AVOID
NO_CHANGE
```

`NO_CHANGE`는 정상 결과다. 단, PR 체크·기존 owner 흡수·stale/freshness·테스트/반례·적대적 질문 보강까지 확인한 뒤 실질 개선이 없을 때만 사용한다.

## 5. 완료 요약

```yaml
source_domains_checked: []
sources_checked:
previous_report_delta:
material_candidates:
absorbed_improvements:
incremental_improvements:
base_promotion_candidates:
project_only_actions:
experiments:
rejected_overgeneralizations:
open_pr_conflicts_or_deferrals:
adversarial_findings:
validation_run:
unverified_scope:
```
