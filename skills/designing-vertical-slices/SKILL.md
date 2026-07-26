---
name: designing-vertical-slices
description: Use when a project must move from an approved concept and CORE_POC to a playable vertical-slice integrated demo that proves core experience, target quality, cross-system integration, content-production pipeline, external playtest evidence, storefront and crowdfunding readiness, accessibility barriers, or target-platform performance.
---

# Designing Vertical Slices

## Core principle

게임 전체를 얕게 만드는 대신, 핵심 경험을 대표하는 작은 구간을 최종 품질에 가까운 깊이로 연결해 **재미·품질·제작성·실제 플레이 증거·외부 설득력**을 동시에 검증한다.

버티컬 슬라이스는 단순한 첫 플레이 가능 상태가 아니다. 승인된 콘셉트와 내부 `CORE_POC`를 이어받아 실제 데모, 외부 플레이 검증, 상점 자료, 후원 준비도와 본제작 판단 근거까지 연결하는 제품 게이트다.

## Distinguish

| 형태 | 검증 대상 |
|---|---|
| Prototype / `CORE_POC` | 가장 위험한 핵심 재미·기술·제작 가설의 최소 내부 검증 |
| Vertical Slice | 대표 경험, 목표 품질, 시스템 연결, 제작 파이프라인, 실제 플레이 증거 |
| Demo | 외부 플레이어를 설득하는 공개·제한 공개 구간 |
| `SLICE_VALIDATION` | 완성된 Slice를 이용한 외부 플레이·시장 검증 |
| MVP | 최소 전체 제품 구조 |

`CORE_POC`와 외부 검증을 모두 PoC라고 부르지 않는다. 핵심 가설이 실패한 상태에서 아트·UI·사운드와 콘텐츠 양으로 문제를 덮지 않는다.

## Modes

- `slice-contract`: 핵심 가설, 대표 구간, 포함·제외 범위와 다음 결정을 고정한다.
- `quality-bar`: 조작·정보·아트·UI·사운드·접근성·성능의 관찰 가능한 목표 품질을 정한다.
- `pipeline-proof`: 기획→데이터→자산→구현→QA→문서화 흐름과 반복 생산 비용을 실제로 통과시킨다.
- `playtest-evidence`: 내부·외부 테스터 집단, 과제, 피드백 채널, 행동 이벤트·퍼널과 관찰 결과를 수집한다.
- `integrated-demo-package`: 플랫폼별 데모·상점·피드백·Playtest·후원 준비물을 하나의 Slice 산출물로 연결한다.
- `decision-gate`: 재미·품질·제작성·시장 증거로 확장·재작업·반복 검증·보류·중단을 판정한다.
- `skill-coverage-audit`: 현재 Gate에 필요한 Skill·산출물·검증 책임이 실제로 실행됐는지 감사한다.

## Product stage model

```text
CONCEPT_APPROVAL
→ PROTOTYPE_AND_VERTICAL_SLICE
→ PRODUCTION_APPROVAL
→ RELEASE_CANDIDATE_APPROVAL
```

이 Skill의 주 책임은 `PROTOTYPE_AND_VERTICAL_SLICE`와 그 결과를 이용한 `PRODUCTION_APPROVAL` 판단이다. 다른 Gate의 상세 계약은 `references/integrated-demo-stage-gates.md`를 현재 단계에서만 읽는다.

## Required inputs

```yaml
current_product_stage:
current_work_mode:
execution_profile:
core_player_promise_and_loop:
pointed_fun_and_sales_points:
approved_project_core_and_nonnegotiables:
highest_risk_fun_technical_production_hypotheses:
core_poc_result_and_recalibration:
current_system_asset_and_pipeline_state:
target_platform_quality_time_team_and_budget_constraints:
representative_and_worst_case_play_flow:
accessibility_and_performance_targets:
protected_decisions_and_assets:
platform_package:
  pc: STEAM_STOVE_ITCHIO
  mobile: GOOGLE_PLAY
playtest_contract:
  build_and_version:
  tester_segment_and_prior_exposure:
  recruitment_and_access:
  tasks_or_play_window:
  observation_points:
  feedback_channel:
  telemetry_events_and_funnel:
  success_failure_stop:
open_design_conflicts:
blocked_unverified:
```

세부 공격력·체력·비용·확률·쿨타임 등은 최종 확정 입력이 아니다. 테스트용 임시값과 조정 범위는 `Balance Tuning Backlog`로 분리한다.

## Routing and Skill orchestration

전체 Skill을 한 번에 불러오지 않는다. 각 하위 작업에 필요한 최소 충분 Skill을 선택하고 단계가 바뀌면 다음 Skill로 명시적으로 전환한다.

```text
managing-project-intake-and-work-contract
→ analyzing-and-refining-game-concepts
→ identifying-project-core / establishing-project-core
→ managing-design-documents
→ designing-vertical-slices
→ 필요한 경우 evaluating-godot-assets-and-plugins-before-creation
→ maintaining-project-context-and-handoff
→ Codex 구현과 검증
→ reviewing-and-validating-project-changes
→ running-adversarial-review-and-refinement
→ auditing-canonical-reference-freshness
→ decision-gate
```

- 핵심 콘셉트·뾰족한 재미·`CORE_POC`가 미확정이면 먼저 `analyzing-and-refining-game-concepts`를 사용한다.
- 프로젝트 코어의 사실 판정과 사용자 승인은 코어 Skill이 담당한다.
- 이미지·UI·사운드·플러그인·기존 자산은 신규 제작 전에 `evaluating-godot-assets-and-plugins-before-creation`을 사용한다.
- 실제 Godot 구현 패키지는 `maintaining-project-context-and-handoff`의 구현 인계 계약을 거친다.
- 변경 결과는 `reviewing-and-validating-project-changes`의 정적·런타임·접근성·성능·회귀 증거로 검증한다.
- 적대적 검토는 기술 Finding을 일괄화하고 기획 충돌만 한 번에 하나씩 사용자에게 제시한다.
- 실행 프로필·Grill Me 단계·P0~P3·Skill 실행 증거·완전성 감사는 `references/skill-orchestration-and-evidence.md`를 사용한다.

## Process

### 1. Slice contract

1. 한 문장 핵심 가설과 이 구간이 바꿀 개발 결정을 정한다.
2. `CORE_POC` 결과와 기획 재조정 내용을 확인한다.
3. 진입→행동→판단→반응→결과→복구→보상→기록·복귀가 연결되는 대표 구간을 고른다.
4. 핵심 세일즈포인트와 일반 반복 플레이를 함께 보여주는지 확인한다.
5. 포함 시스템·콘텐츠·아트·UI·사운드·데이터를 최소화한다.
6. 전체 분량, 모든 캐릭터, 장기 경제 등 제외 범위를 고정한다.
7. 성공·실패·미검증 시 다음 개발 결정을 미리 정의한다.
8. 세부 수치는 테스트 상태와 조정 지표만 정하고 미세 튜닝하지 않는다.

### 2. Quality bar

조작감, 정보 전달, 아트, 연출, 사운드, 접근성, 성능의 품질 기준을 관찰 가능하게 쓴다.

```yaml
controls_and_feedback:
readability_and_information:
art_animation_audio:
mascot_or_symbolic_companion_role:
accessibility_barriers_and_alternatives:
target_hardware_frame_time_memory_loading:
content_and_system_integrity:
save_resume_error_recovery:
store_trailer_screenshot_readiness:
```

“완성도 높음”, “부드러움”, “접근 가능함”, “귀여움”처럼 측정할 수 없는 표현만으로 통과시키지 않는다.

### 3. Pipeline proof

기획→데이터→자산→구현→QA→문서화의 제작 흐름을 실제로 한 번 통과시킨다.

- 각 단계의 입력·출력·소유자·도구·검증·재작업 원인을 기록한다.
- 대표 자산과 일반 반복 자산을 모두 포함한다.
- 임시 자산만으로 목표 품질을 증명하지 않는다.
- 제작 시간보다 병목·대기·반복 가능성·자동화 후보를 우선 기록한다.
- 같은 유형의 두 번째 콘텐츠를 만들 수 없는 구조라면 Production 준비로 판정하지 않는다.
- 기존 승인 자산→보유 자산→에셋스토어·라이선스 검토→부적합 시 신규 생성 순서를 지킨다.

### 4. Integrated demo package

플랫폼에 맞는 외부 설득 패키지를 Slice 제작과 동시에 준비한다.

- PC: Steam 메인, STOVE 피드백·국내 유통, itch.io 제한 테스트·직접 배포.
- 모바일: Google Play 테스트 빌드·스토어 자료·터치 UX·실기기·저장·광고·결제·개인정보 검수.
- PC의 Steam 출시 예정 페이지, 실제 플레이 트레일러, 스크린샷, 장르·태그, Steam Playtest와 텀블벅 준비도는 별도 사후 작업이 아니라 Slice 추적표에 연결한다.
- 플랫폼 정책은 실제 제출 시 최신 공식 출처로 다시 확인한다.

상세 항목은 `references/integrated-demo-stage-gates.md`를 읽는다.

### 5. Playtest evidence

`analyzing-and-refining-game-concepts: playtest-and-experiment`에서 정의한 가설과 표본 계약을 이어받는다.

- 빌드·버전·대상 플레이어·이전 노출을 고정한다.
- 내부 팀의 숙련된 플레이와 목표 플레이어의 첫 경험을 구분한다.
- 외부 테스트는 피드백 위치와 원하는 질문을 게임 안팎에 명확히 안내한다.
- 기존 지식이 결과를 오염시키면 새로운 테스터 집단으로 반복한다.
- 관찰된 행동, 이벤트·퍼널, 인터뷰·설문 반응을 분리한다.
- 핵심 흐름의 진입·이해·선택·실패·복구·보상·복귀 단계와 소요 시간·이탈을 기록한다.
- 플레이어가 제안한 해결책보다 혼란·기대·행동 이유·중단 지점을 먼저 분석한다.
- STOVE 피드백에서는 튜토리얼·UI 가독성·UX·조작성·난이도·핵심 재미 시작점을 검증한다.
- Steam Playtest는 기능 존재가 아니라 표본·빌드·피드백 채널·행동 계측·판정 기준을 별도 계약한다.
- 접근성 장벽과 목표 플랫폼 성능은 `reviewing-and-validating-project-changes`의 전문 mode로 독립 검증한다.

### 6. Decision gate

```text
재미 가설
+ 목표 품질
+ 접근성·성능
+ 시스템 연결
+ 제작 반복성
+ 플레이테스트 행동·반응
+ 상점·후원·시장 설득력
→ APPROVED / APPROVED_WITH_CONDITIONS / REWORK / REPEAT_VALIDATION / HOLD / STOP / UNVERIFIED
```

- `APPROVED`: 대표 경험과 반복 생산 흐름이 증명됐다.
- `APPROVED_WITH_CONDITIONS`: 코어는 유효하지만 명시된 수정 조건이 남았다.
- `REWORK`: 핵심 가설은 유효하지만 품질·장벽·파이프라인 문제가 명확하다.
- `REPEAT_VALIDATION`: 표본·구간·가설이 대표적이지 않아 다른 조건으로 다시 검증한다.
- `HOLD`: 외부 의존성·환경·비용 때문에 판정을 보류한다.
- `STOP`: 핵심 재미·제작성·제품 약속이 함께 성립하지 않는다.
- `UNVERIFIED`: 필수 실행 증거가 없다.

## Output contract

- 현재 제품 단계·Work Mode·실행 프로필
- 실제 사용한 Skill·Mode·Trigger·산출물·검증 증거
- 검증 목적과 핵심 가설
- 목표 플레이어 경험·뾰족한 재미·세일즈포인트
- 대표 플레이 흐름과 예상 시간
- 포함·제외 범위
- 시스템·콘텐츠·자산 목록
- 조작·정보·아트·UI·사운드·마스코트·접근성·성능 품질 기준
- 제작 파이프라인·병목·반복 생산 비용
- 기술·콘텐츠·플랫폼 위험
- Balance Tuning Backlog
- 테스터 집단·빌드·과제·피드백 채널
- 이벤트·퍼널·행동·자기보고 결과
- Steam·STOVE·itch.io 또는 Google Play 통합 데모 준비도
- 텀블벅 준비도와 남은 제작 범위·비용·기간 설명 가능성
- Finding 분류와 기술 검수안
- 성공·실패·중단 기준
- Gate 판정과 후속 개발 결정
- Requirement·Skill·Artifact Coverage 감사

## Definition of Done

- 처음부터 끝까지 플레이 가능한 대표 구간이다.
- 핵심 세일즈포인트와 일반 반복 플레이를 함께 검증한다.
- `CORE_POC`와 `SLICE_VALIDATION`의 빌드·판정이 구분된다.
- 목표 품질이 관찰 가능한 기준과 실제 결과로 대조됐다.
- 핵심 정보·입력·시간·난이도에서 주요 접근성 장벽을 확인했다.
- 목표 플랫폼의 대표·최악 장면 성능을 예산과 비교했다.
- 실제 제작 파이프라인을 통과하고 다음 콘텐츠 반복 가능성을 확인했다.
- 내부·외부 플레이테스트의 빌드·표본·행동·자기보고가 분리 기록됐다.
- PC 또는 모바일 통합 데모 패키지의 필수 산출물과 게임 장면이 추적된다.
- 세계관에 맞는 마스코트 또는 상징 동반자가 실제 역할을 증명하거나, 제외 이유가 기록됐다.
- 세부 수치는 테스트 상태로 관리되고 근거 없이 최종 확정되지 않았다.
- 필요한 Skill 책임이 실제 실행 증거와 연결됐다.
- 결과가 다음 제품 Gate 결정으로 연결됐다.

## Failure conditions

- 기능 목록만 있고 처음부터 끝까지 플레이할 수 없음
- 프로토타입에서 멈추고 버티컬 슬라이스 완료를 주장함
- 특수 보스전처럼 일반 제작성을 대표하지 않는 구간
- 임시 자산만 사용해 목표 품질을 검증할 수 없음
- 전체 게임 분량을 Slice에 포함
- “재미있다”, “완성도 높다”만 있고 관찰 기준이 없음
- 제작 시간과 반복 생산 가능성을 기록하지 않음
- 내부 개발자 반응만으로 목표 플레이어 검증을 대체함
- 빌드·버전·표본·피드백 채널 없이 리뷰·감상을 모음
- 자기보고만으로 실제 행동을, 퍼널만으로 감정·원인을 단정함
- 평균 FPS나 옵션 존재만으로 성능·접근성 통과를 주장함
- 이미지·UI·사운드를 기존 자산 조사 없이 바로 생성함
- 마스코트가 세계관·핵심 루프와 무관한 장식으로만 존재함
- 공격력·비용·확률 같은 값을 플레이테스트 없이 최종 확정함
- Grill Me나 적대적 검토만 수행하고 필요한 콘셉트·Slice·검증 Skill을 생략함
- Skill 이름만 나열하고 실행 증거가 없음
- 실제 제출·실행하지 않은 스토어·후원·GitHub·PDF 작업을 완료로 보고함

## Validation scenarios

1. 카드 전투 게임은 카드 획득→선택→사용→적 반응→보상→덱 상태 기록까지 한 전투 구간으로 연결한다.
2. 조사 게임은 사건 진입→관찰→규칙 추론→위험 선택→기록·회수 결과까지 연결한다.
3. Prototype 결과가 좋더라도 아트·UI·사운드·접근성·성능·파이프라인이 검증되지 않으면 Vertical Slice 완료로 표시하지 않는다.
4. 상위 능력·특수 장면·보너스 결말이 선택적 하이라이트라면 보유·미보유 양쪽 경로가 최종 구간에 진입하고 정상 완료되는지 검증한다.
5. PC 게임은 Slice 장면이 Steam 페이지·트레일러·스크린샷·STOVE 피드백·Playtest·텀블벅 설명에 연결되는지 확인한다.
6. 모바일 게임은 Google Play 테스트 빌드에서 터치·작은 화면·백그라운드 전환·저장·저사양 기기·발열·광고·결제를 확인한다.

## Applied case — 선택적 하이라이트와 정상 완주 경로

한 대회형 프로젝트는 높은 성과와 성장 운으로 최종전 직전에 대표 상위 능력을 조기 해금하게 설계했다. 이 능력은 공개 데모의 기억점이지만 모든 회차에 보장되지 않았다.

다음 세 접근을 비교했다.

- 하이라이트 필수: 대표 장면은 보장하지만 기본 루프와 성장 선택을 진행 게이트로 왜곡한다.
- 하이라이트 제거: 제작 범위는 줄지만 상위 품질과 장기 성장 약속을 검증하지 못한다.
- 선택적 하이라이트: 획득하면 새 선택과 연출을 제공하되, 미획득 회차도 기존 빌드와 판단으로 정상 완주한다.

채택한 완료 기준은 다음과 같다.

```text
보유 경로
- 신규 선택과 연출이 작동한다.
- 사용을 강제하지 않는다.
- 핵심 판단을 자동 정답으로 대체하지 않는다.

미보유 경로
- 같은 최종 구간에 정상 진입한다.
- 기존 시스템으로 공략 가능하다.
- 결말과 다음 목표가 완전하게 전달된다.
```

이 패턴은 특수 능력뿐 아니라 관계 장면, 추가 반전, 보너스 동료, 확장 후일담에도 적용할 수 있다. 단, 해당 하이라이트 자체가 제품의 핵심 조작이거나 반드시 전달해야 하는 사실이면 선택 보상으로 두지 않는다.

관련 사례: `docs/knowledge/cases/TEN_PACES_OPTIONAL_HIGHLIGHT_VERTICAL_SLICE_CASE.md`

## References and templates

현재 mode와 Gate에서 필요한 파일만 읽는다.

- `skills/analyzing-and-refining-game-concepts/references/concept-evidence-and-gates.md`
- `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`
- `skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md`
- `skills/designing-vertical-slices/references/integrated-demo-stage-gates.md`
- `skills/designing-vertical-slices/references/skill-orchestration-and-evidence.md`
- `skills/designing-vertical-slices/references/asset-mascot-and-tuning.md`
- `templates/planning/VERTICAL_SLICE_PLAN.md`
- `templates/project-operations/SKILL_EXECUTION_EVIDENCE.md`

## Learning Log

실제 플레이 증거, 반복 제작 병목, 잘못된 대표 구간, Skill 과다·누락 호출, 에셋 채택·제외, 마스코트 역할 검증, 수치 조정 규칙과 Gate 판정을 `skills/SKILL_LEARNING_LOG.md`에 기록한다. 근거 없는 일반론은 기록하지 않는다.
