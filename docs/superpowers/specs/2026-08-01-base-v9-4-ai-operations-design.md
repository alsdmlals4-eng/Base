# Base v9.4 AI Operations Design

## 1. 승인·권위

- Base Issues: `#113`, `#115`
- Decisions: Issue #113의 모델·비용 최적화 승인, `DEC-2026-08-01-001`
- Approved proposals:
  - `BCP-2026-003-ai-model-prompt-cost-optimization`
  - `BCP-2026-004-ai-instruction-context-ui-motion`
- Baseline: Base main after PR #117, released Base v9.3 preserved
- Work Mode: `PLAN → BUILD → REVIEW`

사용자 최신 지시에 따라 두 제안을 Base v9.4 후보 하나에서 구현하지만 책임·입력·출력·검증을 합치지 않는다.

## 2. 목표

Base v9.4는 다음 두 독립 기능군을 제공한다.

### A. 모델·추론·Prompt 비용 운영

- 작업 위험과 재작업 비용을 포함해 Luna / Terra / Sol과 추론 단계를 추천한다.
- 사용자가 `[모델 추천]`이라고 말하면 모델·추론 단계·이유·변경 checkpoint를 먼저 제시한다.
- 반복 Prompt를 안정 접두부와 변동 접미부로 나눈다.
- provider별 가격·context·cache 조건은 확인일이 있는 profile로 관리하며 영구 상수로 만들지 않는다.
- 실제 usage·재시도·상위 모델 재작업까지 포함해 총비용을 재평가한다.

### B. AI 지시·Context·UI 모션 운영

- 지시를 `HARD_CONSTRAINT / RECOMMENDED_DEFAULT / JUDGMENT_SPACE`로 분류한다.
- Prompt는 예시보다 입출력 인터페이스·불변조건·실패조건·검증을 먼저 정의한다.
- 예시는 정상·실패·경계·회귀 Fixture로 보존한다.
- Context는 현재 결정 질문과 권위·신선도·표현 방식·재조회 조건으로 큐레이션한다.
- 설명만보다 작업에 적합한 화면·Schema·Fixture·Plan·Vertical Slice Artifact를 우선한다.
- UI 모션은 상태 변화·입력 접수·공간 관계·결과를 설명하며 중단·반복·Reduced Motion·성능·상태 권위를 검증한다.

## 3. 책임 경계

### 신규 활성 Skill

`optimizing-ai-model-and-prompt-costs`

고유 책임:

```text
작업 난도·품질 위험·재작업 비용
→ 모델·추론 단계 추천
→ cacheable prefix 설계
→ 비용 추정
→ 실제 usage 측정
→ 재보정
```

이 Skill은 다음을 소유하지 않는다.

- 프로젝트 코어·기획 결정
- 일반 Prompt 요구 확정
- Context Pack 정본화
- UI 설계·모션 품질
- 실제 ChatGPT 모델 설정 변경

### 기존 Skill 확장

- `managing-project-intake-and-work-contract`
  - 지시 권위 예산
  - Interface-first 작업 계약
  - 결정 질문 중심 Context 큐레이션
- `simplifying-skill-bodies`
  - 반복 지시 제거
  - Example → Fixture 재분류
  - 안전 규칙 보존과 판단 공간 분리
- `auditing-and-refining-ui-art`
  - UI motion-and-interaction reference 라우팅
  - 중단·반복·즉시 완료·Reduced Motion 검증

새로운 `AI Prompt Skill`, `Context Skill`, `UI Motion Skill`은 만들지 않는다.

## 4. 파일 구조

### 신규

```text
skills/optimizing-ai-model-and-prompt-costs/
├─ SKILL.md
└─ references/
   ├─ model-stack-routing.md
   └─ prompt-caching.md

docs/knowledge/game-development/
└─ AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md

skills/auditing-and-refining-ui-art/references/
└─ ui-motion-and-interaction-principles.md

base-v9.4.lock.json
schemas/base-v9-4-candidate-lock-v1.schema.json
schemas/base-v9-4-release-evidence-v1.schema.json
docs/operations/BASE_V9_4_RELEASE_CONTRACT.md
tests/test_base_v9_4_ai_operations_contract.py
```

### 수정

```text
skills/SKILL_REGISTRY.json
skills/SKILL_LEARNING_LOG.md
docs/generated/BASE_ACTIVE_SKILLS.md
skills/managing-project-intake-and-work-contract/SKILL.md
skills/simplifying-skill-bodies/SKILL.md
skills/simplifying-skill-bodies/references/progressive-disclosure-rules.md
skills/auditing-and-refining-ui-art/SKILL.md
skills/auditing-and-refining-ui-art/references/ux-ui-design-system-method.md
docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md
docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md
docs/DOCUMENTATION_MAP.md
docs/BASE_RULES_VERSION.md
templates/project-operations/AI_WORKFLOW.md
templates/planning/GAME_UX_UI_SYSTEM.md
templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md
tools/check_base_v9_integrity.py
[수정제안서]/PROPOSAL_REGISTRY.json
[수정제안서]/BCP-2026-003-ai-model-prompt-cost-optimization/PROPOSAL.md
[수정제안서]/BCP-2026-004-ai-instruction-context-ui-motion/PROPOSAL.md
docs/CHANGELOG.md
```

## 5. 데이터 계약

### 5.1 모델 추천 출력

```yaml
recommended_model: Luna | Terra | Sol | PROVIDER_EQUIVALENT
recommended_reasoning: LOW | MEDIUM | HIGH | PROVIDER_SUPPORTED_VALUE
classification: SIMPLE_BULK | ROUTINE_BALANCED | HIGH_RISK_REASONING
reason:
quality_risk:
retry_and_rework_risk:
next_checkpoint:
provider_profile_status: VERIFIED | STALE_RECHECK_REQUIRED | UNVERIFIED
continue_without_change_risk:
```

실제 제품 surface에 존재하지 않는 모델·추론 옵션을 단정하지 않는다. 사용자가 설정을 변경하기 전 현재 응답이 자동 전환됐다고 주장하지 않는다.

### 5.2 Provider profile

```yaml
provider:
model_id:
verified_at:
official_source:
input_rate:
output_rate:
cache_write_rate:
cache_read_rate:
cache_minimum:
cache_ttl:
context_limit:
reasoning_options:
status: VERIFIED | STALE_RECHECK_REQUIRED | UNVERIFIED
```

수치는 profile에만 존재하며 공용 Skill 본문에 상수로 고정하지 않는다.

### 5.3 Prompt cache 구조

```yaml
stable_prefix:
  shared_rules:
  schemas:
  tool_contracts:
  invariant_examples:
dynamic_suffix:
  current_project_state:
  issue_and_goal:
  current_request:
  volatile_values:
excluded_sensitive_data:
refresh_trigger:
```

### 5.4 지시 권위

```yaml
instruction:
authority: HARD_CONSTRAINT | RECOMMENDED_DEFAULT | JUDGMENT_SPACE
reason:
source:
adjustment_condition:
validation:
```

### 5.5 Context 큐레이션

```yaml
decision_question:
include_criteria:
exclude_criteria:
authority_level:
freshness:
representation:
deduplication:
known_conflicts:
context_budget:
progressive_load_trigger:
refresh_trigger:
```

## 6. UI 모션 계약

모션은 다음 순서를 따른다.

```text
화면 중심 질문과 상태 변화
→ 첫 시선·staging
→ anticipation이 필요한지 판정
→ timing·easing·공간 연속성
→ 입력 접수와 처리 중·결과 분리
→ follow-through와 결과 위치
→ 중단·즉시 완료·빠른 반복·재진입
→ Reduced Motion·mute·haptic-off 동등 경로
→ 목표 플랫폼 성능
→ 도메인 상태 권위와 회귀
```

금지:

- 애니메이션 완료를 구매·저장·보상·진행 결과의 권위 시점으로 사용
- 모든 요소에 확대·흔들림·점멸을 적용
- 모션이 없으면 핵심 상태를 알 수 없는 구조
- 웹/SaaS 패턴이나 12원칙을 프로젝트 코어·입력·플랫폼 검토 없이 복제

## 7. Release 구조

`base-v9.4.lock.json`은 v9.4 후보의 기계 신원이다.

```json
{
  "schema_version": 1,
  "artifact_role": "BASE_V9_4_RELEASE_CANDIDATE_LOCK",
  "release_line": "v9.4.0",
  "release_state": "RELEASE_CANDIDATE",
  "repository": "alsdmlals4-eng/Base",
  "github_issue": 113,
  "linked_issue": 115,
  "candidate_release_commit": null,
  "candidate_release_evidence_commit": null,
  "candidate_registry": {
    "path": "skills/SKILL_REGISTRY.json",
    "sha256": "<RAW_FILE_BYTES_SHA256>",
    "hash_definition": "RAW_FILE_BYTES_SHA256"
  }
}
```

후보 PR은 자체 release/evidence SHA를 기록하지 않는다. 순서는 다음과 같다.

```text
v9.4 candidate implementation PR
→ trusted-main evidence PR
→ pin-finalization PR
→ 프로젝트별 adapter/snapshot 적용
```

Base v9.3의 lock·payload·evidence·pin은 수정하지 않는다.

## 8. 검증

### 자동

- 신규 계약 테스트를 먼저 추가하고 실패를 확인한다.
- Skill frontmatter·Registry·경로·trigger·negative trigger 검사
- BCP 상태·approval_ref·implementation PR 연결
- v9.4 lock schema·null pin·raw Registry hash 검사
- Documentation Map·AI Workflow·UI Template·Checklist 소비자 검사
- hard constraint·example fixture·counterevidence·Artifact claim limit 검사
- 모델/비용 책임과 지시/UI 책임의 교차 오염 검사
- Base integrity·reference freshness·full Python suite·generation·`git diff --check`

### 수동/외부

- 실제 provider billing·cache hit·비용 절감: `NOT_RUN`
- 실제 ChatGPT 모델 변경: `NOT_APPLICABLE`
- Godot 런타임 UI 모션·성능·사람 이해: Base에서는 `NOT_RUN`; 프로젝트 적용 단계에서 수행
- Windows smoke가 조건부 skip이면 성공으로 과장하지 않는다.

## 9. 적대적 검토

필수 공격:

- 비용 절감을 품질보다 우선하는가
- Luna/Terra/Sol 이름이 실제 provider 모델 존재를 의미한다고 오해시키는가
- 캐시 수치를 stale 상수로 고정하는가
- 민감 정보가 stable prefix에 들어가는가
- 안전 규칙이 판단 공간으로 완화되는가
- 프로젝트 코어 결정이 `RECOMMENDED_DEFAULT`로 숨겨지는가
- Example·Golden Set이 삭제되는가
- Context 큐레이션이 반대 근거를 제거하는가
- Artifact가 런타임·사람 이해를 과장하는가
- UI 모션이 결과 중복·입력 지연·반복 피로를 만드는가
- 새 파일이 존재하지만 Registry·Map·Template·Test에서 발견되지 않는가
- v9.3 history가 재작성되는가

## 10. 프로젝트 적용 경계

Base v9.4가 candidate → evidence → pin-finalization을 모두 통과한 뒤 다음 프로젝트를 각각 최신 main 기준으로 감사한다.

1. `Ten-Paces-Hidden-Moves`
2. `Blacksmith`
3. `omenward`
4. `urban-legend`
5. `GRIMOIRE-`
6. `Switchy-Express-Cargo-Puzzle`

프로젝트 적용은 공용 Method·Skill snapshot·adapter·AI Workflow·UI 책임 원본을 동기화하는 작업이다. 프로젝트 코어·세계관·수치·저장 Schema·승인 자산을 공용 기본값으로 덮어쓰지 않는다.

## 11. 완료 판정

```text
BCP_APPROVED_AND_LINKED
SKILL_BOUNDARIES_PRESERVED
V9_4_CANDIDATE_VALIDATED
ADVERSARIAL_P0_P1_ZERO
TRUSTED_EVIDENCE_RECORDED
PINS_FINALIZED
READY_FOR_PROJECT_ADOPTION
```

실행하지 않은 provider·Godot·사람 검증은 `NOT_RUN`으로 유지한다.
