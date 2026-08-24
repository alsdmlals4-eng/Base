# AI Game & AI-Assisted Indie Specialty Radar

```yaml
radar_role: ai-game-and-ai-assisted-indie-specialty-discovery
status: ACTIVE_DISCOVERY_EXTENSION
owner_policy: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
reuse_owner: docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md
ai_workflow_owner: docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md
current_project_adoption_receipt: docs/knowledge/game-development/reuse/AI_ASSISTED_INDIE_PROJECT_ADOPTION_RECEIPT_2026-08-24.md
scheduler_authority: EXTERNAL_TO_BASE
recommended_cadence: weekly
compare_with_previous_scan: true
popularity_is_not_authority: true
new_active_skill: false
new_runtime_framework: false
project_auto_adoption: false
```

## 1. 역할

이 문서는 `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`에 종속된 **AI 게임·AI 활용 1인/소규모 게임 전문 discovery extension**이다.

이 문서가 하지 않는 일:

- 두 번째 Watchlist가 되지 않는다.
- Base scheduler를 소유하지 않는다.
- 새 Skill/Agent를 만들지 않는다.
- 프로젝트 정본을 자동으로 바꾸지 않는다.
- AI 런타임 프레임워크를 자동 채택하지 않는다.
- 외부 게임의 인기·평가를 곧바로 인과 증거로 취급하지 않는다.

후보를 발견한 뒤 실제 역기획·역공학, Existing Solution First, 재사용 후보 추출·승격은 `REVERSE_ENGINEERING_REUSE_PIPELINE.md`가 계속 소유한다.

## 2. AI 사용 Lane 분리

모든 사례는 최소 하나의 Lane을 명시한다.

```text
PRODUCTION_ASSISTED
RUNTIME_GENERATIVE
HYBRID
PLAYER_FACING_GENERATED_ASSET
AI_MARKETING_OR_PROMOTION
```

핵심 경계:

```text
PRODUCTION_ASSISTED != RUNTIME_GENERATIVE
```

- AI로 코드를 작성한 게임의 성공은 런타임 생성형 AI가 재미있다는 증거가 아니다.
- 런타임 자유대화가 흥미롭다는 사실은 AI-assisted production이 싸거나 빠르다는 증거가 아니다.
- AI 생성 아트/음악이 쓰였다는 사실은 품질·권리·일관성이 검증됐다는 뜻이 아니다.

## 3. 주간 탐색 범위

주간 스캔에서는 후보 수를 임의 상한으로 자르지 않되, 아래 우선순위를 적용한다.

1. 최근 출시·데모·Early Access에서 실제 플레이어 반응이 생긴 사례
2. Steam/itch/공식 사이트에서 AI 사용 공개와 제품 구조를 확인할 수 있는 사례
3. 개발자가 실제 제작 루프·실패·재작업을 공개한 1인/소규모 사례
4. AI 사용 때문에 평가가 나빠졌거나 운영비·성능·품질 문제가 드러난 실패/혼합 사례
5. 기존 인기 게임의 플레이 시스템을 AI 프로젝트가 새 방식으로 조합한 사례
6. 아직 출시 전이면 `MONITOR`로 유지하고 성공 사례로 승격하지 않는다.

## 4. 출처 사다리

가능하면 다음 순서로 원출처를 우선한다.

1. 공식 Steam/스토어/패치 노트 — 출시 상태, 제품 기능, 리뷰/평가 같은 공개 상태
2. 개발자 공식 블로그·사이트·공개 저장소 — 제작 구조·기술 주장
3. 개발자가 직접 작성한 Reddit/커뮤니티 글 — self-report workflow
4. 플레이어 리뷰·커뮤니티 — 체감 문제·반복 불만·사용성
5. 독립 기사/2차 보도 — 별도 검증된 맥락을 보충할 때만

다음은 반드시 구분한다.

```text
OFFICIAL_PRODUCT_FACT
DEVELOPER_SELF_REPORT
PLAYER_REPORT
SECONDARY_REPORT
ANALYST_INFERENCE
```

## 5. 인기 신호와 Evidence 권위 분리

리뷰 수, 긍정률, 위시리스트, 동시접속자, Steam 순위, Reddit 반응은 **탐색 우선순위를 정하는 신호**다. 성공 원인이나 시스템 품질을 단독으로 증명하지 않는다.

```yaml
popularity_signal:
  metric:
  value:
  observed_at:
  source:
  causality_claim_allowed: false
```

특히 개발자 self-report 위시리스트/순위는 독립 검증이 없으면 그대로 `DEVELOPER_SELF_REPORT`로 남긴다.

## 6. 주간 Candidate Packet

각 사례는 아래 포맷으로 축적한다.

```yaml
case_id:
checked_at:
release_state: RELEASED | DEMO | EARLY_ACCESS | UPCOMING | UNKNOWN
team_context:
engine_or_stack_when_verified:
ai_use_lanes: []
primary_sources: []
supporting_sources: []
evidence_classes: []
popularity_signals:
  - metric:
    value:
    observed_at:
    source:
core_player_promise:
core_loop:
player_agency:
production_loop:
feedback_and_update_loop:
observed_strengths: []
observed_failures: []
source_ceiling:
reusable_candidates: []
existing_owner_overlap: []
project_fit_candidates: []
disposition: ADOPT | ADAPT | TEST | REJECT | REFERENCE_ONLY
falsification:
rollback_or_discard:
```

## 7. 역기획·역공학 질문

### 플레이 구조

- 한 문장으로 설명되는 판매/플레이 훅은 무엇인가?
- 30초·5분·한 Run에서 플레이어가 반복하는 선택은 무엇인가?
- 랜덤성, 정보, 비용, 위험, 보상이 어떤 식으로 선택을 만든다?
- 나쁜 결과가 단순 손실인가, 다음 판단을 위한 자원/정보가 되는가?
- 플레이어가 기억하고 공유할 순간은 어디서 발생하는가?

### 제작 구조

- AI가 무엇을 작성했고 사람이 무엇을 결정했는가?
- AI 산출물 뒤 사람의 수정·통합·QA 비용은 얼마나 남았는가?
- 작은 POC 뒤 범위를 늘렸는가, 처음부터 breadth를 쌓았는가?
- 프로젝트가 커졌을 때 Context drift·중복 owner·monolith·회귀가 발생했는가?
- 개발자가 실제로 무엇을 버리고 다시 만들었는가?

### 운영 구조

- 데모/출시 후 피드백이 어느 시스템 변경으로 연결됐는가?
- hotfix와 core rebuild를 어떻게 구분했는가?
- 성능·save·stability·platform 문제는 제작 속도와 별도로 검증됐는가?

### AI 런타임

- AI가 없어서는 안 되는 플레이 가치가 있는가?
- authoritative GameState를 AI가 직접 수정하는가?
- deterministic validator와 capability contract가 있는가?
- latency/offline/provider failure에서 게임이 계속 가능한가?
- memory/canon/privacy/moderation/replay/debug 비용을 감당할 수 있는가?

## 8. 재사용 후보 추출 규칙

새 사례에서 좋은 아이디어가 보여도 바로 새 `RM-SYS-*`/`RM-WORK-*`를 만들지 않는다.

```text
observed pattern
→ smallest reusable contract
→ search existing Base owner/module
→ overlap >= meaningful
   ├─ YES: existing owner를 보강하거나 project adapter로 시험
   └─ NO: materially distinct multi-case evidence가 쌓일 때만 promotion candidate
```

현재 주요 교차검사 대상:

- `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE`
- `RM-SYS-017 SPELL_COMPOSE_VALIDATE_COMMIT_ENGINE`
- `RM-SYS-018 ROULETTE_TOKEN_SOURCE_ENGINE`
- `RM-SYS-019 PUSH_YOUR_LUCK_ENHANCEMENT_ENGINE`
- `RM-TOOL-002 DETERMINISTIC_SEED_REPLAY_CAPTURE`
- `RM-TOOL-003 BALANCE_SCENARIO_BATCH_SIMULATOR`
- `RM-WORK-001 PROJECT_REUSE_OPPORTUNITY_SCAN`
- `RM-WORK-002 SKILL_WORKFLOW_PATTERN_EVAL`

## 9. 생산 AI용 필수 Gate

AI-assisted 개발 사례에서 아래를 반복 확인한다.

```text
HUMAN_DIRECTED_AI_BUILD_LOOP
SILENT_OMISSION_GATE
CONTEXT_SCOPE_AND_ARCHITECTURE_BUDGET
BREADTH_AFTER_CORE_IDENTITY_LOCK
PLAYER_FEEDBACK_REBUILD_LOOP
AI_VISIBLE_OUTPUT_QUALITY_GATE
```

이 Gate는 `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`를 대체하지 않는다. 실제 프로젝트 실행 시 Guide의 Prompt/Context/Eval/권리/비용/검증 계약을 따른다.

## 10. 런타임 AI용 보수적 Gate

런타임 생성형 AI는 기본 `TEST`이며 다음을 모두 증명하기 전 `ADOPT`하지 않는다.

```text
PLAYER_VALUE_UNIQUE_TO_AI
CAPABILITY_CONTRACT
DETERMINISTIC_STATE_VALIDATION
MEMORY_CANON_BOUNDARY
LATENCY_OFFLINE_FALLBACK
PRIVACY_MODERATION_SECURITY
COST_SURFACE_APPROVED
PLATFORM_STORE_COMPLIANCE
REPLAY_DEBUG_EVIDENCE
```

AI가 자연어를 해석할 수는 있어도 authoritative state mutation은 프로젝트 규칙/validator가 소유하는 방향을 우선 시험한다.

## 11. 주간 비교 규칙

각 실행은 이전 스캔과 비교한다.

```yaml
compare_with_previous_scan: true
new_cases: []
changed_release_state: []
changed_review_or_popularity_signal: []
new_failure_evidence: []
new_reusable_candidates: []
promoted_candidates: []
demoted_or_rejected_candidates: []
stale_sources_to_recheck: []
```

동일한 교훈이 반복되면 중복 문서를 늘리지 않고 기존 후보의 evidence count와 반례를 보강한다.

## 12. 프로젝트 적용 경계와 current receipt

주간 스캔 결과는 프로젝트에 대해 다음 중 하나만 제안한다.

```text
ADOPT | ADAPT | TEST | REJECT | REFERENCE_ONLY
```

프로젝트의 최신 AGENTS/Active Context/Notion 기획 정본/GitHub 구현 사실을 읽지 않은 상태에서는 항상 `PROJECT_ADOPTION_NOT_RUN`이다. 주간 조사 자체가 프로젝트 기획·코드·Notion을 자동 변경하지 않는다.

`INITIAL_PATTERN_PACK_STATE_IS_HISTORICAL`: `AI_ASSISTED_INDIE_PATTERN_PACK_2026-08-24.md` 안의 `PROJECT_ADOPTION_NOT_RUN`은 **2026-08-24 초기 연구 캡처 당시 상태**다. 이후 사용자가 승인한 10개 프로젝트별 적용 실행은 별도 successor receipt인 `AI_ASSISTED_INDIE_PROJECT_ADOPTION_RECEIPT_2026-08-24.md`가 현재 실행 사실을 소유한다.

따라서 과거 Pattern Pack을 current truth처럼 해석하지 않는다.

```text
initial research capture
→ current project authority read
→ project-specific bounded adoption
→ project merge/readback
→ Notion sync/readback when human-facing meaning changed
→ current_project_adoption_receipt
```

새 주간 조사 결과는 위 receipt가 존재한다는 이유로 자동 프로젝트 적용하지 않는다. 새 프로젝트 의미 변경은 다시 해당 프로젝트 current authority와 승인 범위를 읽어야 한다.

## 13. 실패·폐기 조건

다음이면 후보를 낮추거나 폐기한다.

- AI novelty를 재미와 혼동함
- popularity 신호에서 인과를 과장함
- upcoming/demo를 출시 성공으로 표현함
- 사람의 수정·QA 비용을 빼고 생산성만 계산함
- 기존 Base 모듈과 중복됨
- 런타임 AI가 deterministic rule로 더 싸고 안정적으로 해결 가능함
- player-facing AI output이 현재 quality bar를 통과하지 못함
- provider/API 비용이 zero-incremental-cost 기본 정책과 충돌함
- platform/privacy/rights/replay/debug 경로가 불명확함

## 14. 산출물과 영속 흡수 경계

주간 실행 결과는 최소 다음을 남긴다.

```text
새/변경 사례
→ evidence class + source ceiling
→ 역기획 core loop
→ production/runtime AI lane
→ 성공 + 실패/반례
→ smallest reusable contract
→ existing owner overlap
→ project fit hypothesis
→ ADOPT/ADAPT/TEST/REJECT/REFERENCE_ONLY
→ IRG claim ceiling
→ 다음 재확인 조건
```

Material reusable finding이 기존 Base owner를 실제로 개선해야 하는 경우에는 보고로 끝내지 않는다. 단, 자동으로 프로젝트 canon을 바꾸지 않고 Base의 정상 변경 경로를 따른다.

```text
MATERIAL_BASE_FINDING
→ Existing Solution First / existing owner
→ smallest bounded Base delta
→ separate branch/PR
→ applicable regression + exact-head CI
→ adversarial/review gate
→ merge only when repository gate is satisfied
→ merged-main readback
→ Radar/Pattern Pack/current receipt 또는 해당 canonical owner freshness 갱신
```

`NO_CHANGE`, `REFERENCE_ONLY`, `TEST` 수준이면 PR을 만들기 위해 churn을 제조하지 않는다. open/draft/ready same-goal PR이 있으면 그 workstream은 read-only로 보호하고 중복 변경을 만들지 않는다.
