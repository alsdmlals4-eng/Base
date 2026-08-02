---
contract_name: BASE_PROJECT_INTEGRATED_WORK_INSTRUCTION
contract_version: "1.0"
status: ACTIVE_GENERAL_EXECUTION_PROMPT
language: ko-KR
base_repository: "https://github.com/alsdmlals4-eng/Base"
observed_base_main: "896d2e6fd257084b6aa29b1703cd0bbfa3b18daa"
observed_at: "2026-08-02"
usage: "Base와 대상 프로젝트의 최신 정본·실제 구현·작업 환경을 먼저 복원한 뒤 [핵심 내용]을 누락 없이 PLAN → BUILD → REVIEW로 실행하는 범용 단일 첨부 작업지시문"
authority_boundary: "최신 사용자 지시, 프로젝트 정본·실제 구현, 프로젝트가 채택한 Base 계약보다 높은 권한을 갖지 않는다."
specialized_prompt:
  vertical_slice: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
reference_prompts:
  - templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
  - templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md
  - templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md
core_policies:
  - CORE_CONTENT_PRESERVATION
  - ENVIRONMENT_FIRST
  - REPOSITORY_FIRST
  - MINIMUM_SKILL_ROUTING
  - PLAN_BUILD_REVIEW
  - NEUTRAL_RECOMMENDATION_GATE
  - ADVERSARIAL_LIFECYCLE
  - BENCHMARK_BEFORE_INVENTION
  - PRACTICAL_OPERABILITY
  - SOURCE_CONSUMER_PROPAGATION
  - EVIDENCE_BEFORE_COMPLETION
  - DRAFT_PR_DELIVERY
---

# Base·프로젝트 통합 작업지시문 v1

## 0. 사용자 입력

이 파일과 함께 아래 블록을 제공한다. 비어 있는 값은 저장소·도구·연결 자료에서 먼저 복원하고, 사용자만 결정할 수 있는 차단 항목만 질문한다.

```yaml
base_repository: https://github.com/alsdmlals4-eng/Base
project_repository:
requested_work_mode: AUTO   # AUTO / PLAN / BUILD / REVIEW
requested_result:
protected_decisions: []
protected_files_or_assets: []
explicit_exclusions: []
required_delivery_format: []
```

### [핵심 내용] — 목적 보존 구역

```text
[핵심 내용]
이번 작업에서 반드시 달성해야 하는 목적, 변경 대상, 기존 결정, 제약, 산출물과 완료 조건을 원문 그대로 붙여 넣는다.
```

`[핵심 내용]`은 요약·리팩터링 중 삭제·약화·다른 목표로 치환할 수 없는 보호 입력이다. 시작과 종료에 아래 추적표를 대조한다.

| 원문 요구 | 실행 요구 | 책임 원본·대상 | 검증 | 상태 |
|---|---|---|---|---|
|  |  |  |  | `PENDING` |

- 충돌 요구는 임의 삭제하지 않고 `CANON_CONFLICT` 또는 `USER_DECISION_REQUIRED`로 분리한다.
- 저장소 사실로 채울 수 있는 누락은 조사로 해결한다.
- 범위 밖 개선은 몰래 포함하지 않고 `DEFERRED_OPTION`으로 분리한다.
- 핵심 요구가 구현·검증 항목에 연결되지 않으면 완료로 판정하지 않는다.

---

## 1. 역할과 권한

이 파일은 Base 규칙을 복제하는 새 정본이 아니라, 현재 작업의 책임 원본·최소 Skill·실행·검증·전파를 연결하는 범용 실행 Prompt다.

```text
최신 사용자 지시와 승인
→ 프로젝트 AGENTS.md·보안·엔진·데이터 규칙
→ Active Context·Decision·승인 작업 계약
→ 등록된 책임 원본과 실제 코드·데이터·자산·테스트
→ 프로젝트가 채택한 Base 계약
→ Base 최신 main의 START_HERE·AGENTS·운영 정본·Registry
→ 이 Prompt
→ 외부 벤치마크·리뷰·과거 대화·초안·추정
```

- 하위 자료가 상위 자료를 자동으로 덮어쓰지 않는다.
- 외부 사례는 개선 가설이지 요구사항·구현 상태의 정본이 아니다.
- 이 Prompt가 최신 Base와 다르면 최신 Base를 적용하고 `STALE_PROMPT_CONTRACT`를 기록한다.
- 버티컬 슬라이스 전 과정은 이 Prompt를 비대하게 만들지 말고 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md`로 라우팅한다.

---

## 2. 환경 우선 기준선 복원

설계·수정 전에 Base·프로젝트·실행 환경을 확인한다. 저장소 접근 없이 설치·검수·완료를 주장하지 않는다.

### 2.1 Base 읽기 순서

```text
최신 main·정확한 HEAD
→ 같은 Goal의 열린·최근 병합 PR
→ START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ trigger가 일치하는 최소 Skill·reference·Template·Test
```

`전부 살펴본다`는 모든 파일·Skill을 무작정 읽는다는 뜻이 아니다. Registry와 Documentation Map으로 현재 요청의 책임 원본과 영향 소비자를 선택하고, 새 연결이 발견될 때만 범위를 확장한다.

### 2.2 프로젝트 읽기 순서

```text
최신 main·정확한 HEAD·열린/최근 PR·Issue
→ 프로젝트 AGENTS.md·START_HERE
→ ACTIVE_CONTEXT·Decision·작업 계약
→ DOCUMENTATION_MAP·DESIGN_DOCUMENT_REGISTRY
→ 현재 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 생성본·발행본·외부 작업면 동기화
```

Base Template을 프로젝트 활성 상태로 오인하지 않는다. 어댑터·Snapshot·router를 사용하면 실제 경로와 Base pin을 확인한다.

### 2.3 실행 환경

```yaml
repository_access:
write_permission:
current_branch_and_head:
working_tree_state:
required_tools_and_versions:
runtime_or_engine_path:
dependencies:
credentials_and_minimum_permissions:
inputs_and_assets:
validation_commands:
ci_and_required_checks:
rollback_path:
```

확인하지 못한 항목은 `NOT_AVAILABLE / NOT_RUN / BLOCKED_UNVERIFIED`로 남긴다. 누락 환경은 `필요 항목 / 이유 / 설치·적용 / 확인 명령 / 최소 권한`으로 안내한다. 시스템 전역 설치·권한 확대·보안 설정·branch protection 변경은 별도 승인 없이 수행하지 않는다.

### 2.4 Baseline Recovery Record

```yaml
base_main_sha:
project_main_sha:
current_branch_and_head:
related_open_and_recent_prs:
canonical_sources:
actual_implementation_state:
active_decisions:
protected_scope:
available_tools_and_permissions:
unverified_inputs:
stale_prompt_or_reference_findings:
```

---

## 3. Work Mode·Skill·Superpowers 라우팅

한 시점의 주 Work Mode는 하나다.

- `PLAN`: 사실·요구·대안·근거·계약·순서 확정
- `BUILD`: 승인 범위의 최소 구현
- `REVIEW`: 공격·검증·회귀 판정

복합 작업은 `PLAN → BUILD → REVIEW`로 전환한다.

새 L1 이상 요청은 `managing-project-intake-and-work-contract`로 한 번만 접수한다. Registry trigger·비사용 조건에 따라 주 책임 분야 Skill 최대 하나와 필요한 검증·참조 최신성·Handoff Skill만 선택한다. Skill 파일을 읽은 것과 실제 실행을 구분한다.

실행 환경에 Superpowers Skill이 실제로 제공될 때만 다음을 적용한다.

```text
using-superpowers
→ creative/design: brainstorming
→ approved multi-step work: writing-plans
→ feature/bug implementation: test-driven-development
→ failure investigation: systematic-debugging
→ completion/PR claim: verification-before-completion
→ major change review: requesting-code-review
```

| Superpowers 책임 | Base 대응 책임 |
|---|---|
| `brainstorming` | intake 요구 모델·중립성 Gate·필요한 Grill Me |
| `writing-plans` | `decompose-and-sequence` |
| `test-driven-development` | 분야 BUILD의 실패 재현·수용 기준·회귀 |
| `systematic-debugging` | 런타임 진단 또는 변경 검증의 원인 격리 |
| `verification-before-completion` | 증거 기반 변경 검증 |
| `requesting-code-review` | 독립 리뷰·적대 검토·PR Gate |

외부 Skill을 Base Registry에 중복 생성하지 않는다. 사용할 수 없으면 Base 동등 책임으로 진행하고 `NOT_AVAILABLE`을 기록한다.

---

## 4. 요구 확정과 실행 계약

사용자에게 묻기 전에 저장소에서 다음을 확인한다.

- 현재 구현·경로·버전·테스트 명령
- 승인 Decision·보호 대상
- 동일 Goal의 열린·최근 병합 PR
- 기존 Skill·Template·정본의 책임
- 명백한 오류·누락·참조 drift

사용자 질문은 둘 이상의 유효한 선택지가 프로젝트 코어, 사용자/플레이어 경험, 주요 UX, 콘텐츠 의미, 범위·비용 우선순위를 다르게 만들 때로 제한한다.

```yaml
problem_to_solve:
user_or_player_value:
core_content_traceability:
current_state:
target_state:
in_scope:
out_of_scope:
protected_decisions_and_assets:
deliverables:
acceptance_criteria:
validation:
rollback:
```

사용자가 `진행`, `승인`, `권장안대로` 또는 명확한 수정·구현 명령을 이미 제공했고 중대한 미결정이 없으면 같은 질문을 반복하지 않는다. 감사만 요청했으면 구현으로 확대하지 않는다.

실행 계약:

```md
# 작업 제목
## 목적과 [핵심 내용] 추적
## Work Mode와 기준 HEAD
## 범위·비목표·보호 대상
## 자동 선택 Skill·Skill Mode
## 변경 대상·영향 소비자
## 산출물·완료 기준
## 검증·위험·롤백
## PR·병합·동기화 경계
```

---

## 5. 브레인스토밍·대안 설계

브레인스토밍은 아이디어 수를 늘리는 행위가 아니라 잘못된 문제 정의와 조기 확정을 줄이는 PLAN 절차다.

1. 현재 상태와 사용자 가치를 한 문장으로 재정의한다.
2. 제약·비타협 조건·실패 비용을 확인한다.
3. 기존 유지·최소 수정안을 포함해 2~3개 실질 대안을 만든다.
4. 같은 기준으로 비교한다.
5. 권장안, 미검증, 되돌리기 조건을 함께 제시한다.

| 대안 | 사용자 가치 | 정본 적합성 | 비용 | 운영 부담 | 회귀 위험 | 되돌리기 | 근거·미검증 |
|---|---:|---:|---:|---:|---:|---:|---|
| 기존 유지·최소 수정 |  |  |  |  |  |  |  |
| 대안 A |  |  |  |  |  |  |  |
| 대안 B |  |  |  |  |  |  |  |

현재 Goal에 필요하지 않은 아이디어는 `DEFERRED_OPTION`으로 분리한다.

---

## 6. 벤치마킹과 실무적 조언

벤치마킹은 인기 기능 복사가 아니다. 현재 결정을 바꿀 질문·비교 기준을 먼저 정하고 사실, 운영 경험, 사용자 반응, 행동 증거, 표본 한계를 분리한다.

실행 조건:

- 최신 버전·가격·정책·도구 동작 확인이 필요하다.
- 설계안 선택에 외부 근거가 필요하다.
- 보안·플랫폼·접근성·성능·배포 리스크가 있다.
- 직접 제작 전에 기본·무료·오픈소스·상용 대안을 비교해야 한다.
- 사용자가 실무 사례·최신 권장안을 요청했다.

```yaml
decision_question:
comparison_dimensions:
sources_and_dates:
versions_compared:
product_facts:
operator_experience:
user_or_player_reactions:
behavioral_evidence:
sample_and_bias_limits:
implication_for_current_project:
```

출처 우선순위는 공식 문서·1차 저장소/릴리스 노트·표준/연구·유지보수자/운영 증거·표본 한계를 명시한 커뮤니티 경험이다.

실무 관점:

- 설치·온보딩·반복 호출 비용
- 로컬·CI·Windows·Linux 차이
- 인증·최소 권한·비밀정보
- 유지보수 주체·업데이트·지원 종료
- 로그·진단·재시도·롤백
- 저장 호환성·마이그레이션
- 접근성·성능·비용·라이선스
- 사람 검토가 필요한 최종 Gate

프롬프트 운영에는 다음을 적용한다.

- 항상 적용되는 저장소 지침과 작업별 Prompt를 분리한다.
- 경로별 규칙은 작업 위치에 가까이 두고 전역 지침 과부하를 피한다.
- 여러 지침이 함께 적용될 수 있으므로 중복보다 충돌 제거를 우선한다.
- 구체적인 빌드·테스트·검증 명령과 아키텍처 관례를 제공한다.
- Prompt를 버전 관리하고 정상·실패·경계 사례로 평가한다.
- 모델이 지침을 항상 동일하게 따를 것이라 가정하지 않고 결과 증거로 판정한다.

2026-08-02 기준 참고한 1차 자료는 GitHub repository instructions/prompt files 문서, Anthropic Claude Code project-memory 문서, OpenAI의 pinned model·evals 지침과 OpenAI Evals 저장소다. 외부 근거는 정본이 아니므로 작업 시 최신 문서를 재조회한다.

---

## 7. 중립적 권장안 Gate

사용자안과 AI 최초안을 같은 기준으로 검토한다. 무조건 동의와 반대를 위한 반대를 모두 금지한다.

```yaml
evaluation_criteria: []
user_proposal:
ai_initial_proposal:
alternatives: []
counterevidence: []
benefits_costs_and_risks: []
reversibility:
unknowns_and_evidence_limits: []
recommended_conclusion:
agreement_or_disagreement_reason:
```

- 사용자안이 가장 강하면 근거와 함께 동의한다.
- 다른 안이 더 강하면 차이를 만드는 근거와 함께 이견을 제시한다.
- 증거가 부족하면 `BLOCKED_UNVERIFIED`와 확인 조건을 남긴다.
- L0 기계 수정은 전체 적대 검토를 강제하지 않는다.
- L1 이상 기능·설계·아키텍처·정책·방향 결정은 전체 적대 검토 생명주기를 적용한다.

---

## 8. 적대적 검토·개선 생명주기

```text
PLAN: attack → validate-critique → decision-report
→ 승인 finding
BUILD: 주 책임 분야 Skill이 최소 수정
REVIEW: regression-recheck → decision-report
```

공격 관점:

- `[핵심 내용]` 목적 왜곡
- 사용자·프로젝트·Base·외부 근거의 권한 충돌
- 정본·소비자·테스트·문서·마이그레이션 누락
- 중복 정본·Skill·Prompt·PR·파일
- 구형 경로·ID·Schema·Prompt의 활성화
- 도구·권한·입력 없는 허위 실행 가능성
- 기존 장점·호환성·정상 경로 회귀
- 빈 입력·부분 실패·재시도·중단·롤백
- 보안·개인정보·라이선스·최소 권한
- 설치·로그·진단·유지보수·비용
- 완료 조건의 실제 검증 가능성

비판도 사실성, 발생 가능성, 영향, 범위, 수정 비용, 회귀 위험으로 재검증한다.

- `MUST_FIX`
- `SHOULD_FIX`
- `USER_DECISION_REQUIRED`
- `DEFER`
- `REJECTED_CRITIQUE`
- `BLOCKED_UNVERIFIED`
- `ALLOWED_LEGACY`

`MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정한다. 분야 방향은 몰래 바꾸지 않는다. 수정 뒤 `[핵심 내용]`, 보호 대상, untouched 소비자, 새 중복·충돌·stale reference, 테스트·발행 drift와 롤백을 다시 공격한다.

---

## 9. 작업 분해와 BUILD

L2 이상 또는 다중 의존성 작업은 독립 검증 가능한 결과 단위로 분해한다.

```yaml
step_id:
outcome:
work_mode:
inputs:
files_or_systems:
owner_or_skill:
dependencies:
protected_scope:
acceptance_criteria:
validation:
rollback:
```

기본 순서:

```text
환경·권한·입력
→ 정본·인터페이스·Schema
→ 가장 위험한 가설
→ 핵심 사용자 경로
→ 인접 시스템 통합
→ 정상·실패·경계·회귀 검증
→ 문서·발행·참조 최신성
→ 통합·인수인계
```

BUILD 규칙:

1. 최신 main에서 별도 브랜치를 만든다.
2. 같은 Goal의 열린 PR을 비교해 중복을 막는다.
3. 승인 범위와 보호 경계를 지킨다.
4. 최소 diff와 기존 관례를 따른다.
5. 코드는 가능한 경우 실패 재현 → 최소 구현 → 통과 → 회귀 순서로 진행한다.
6. 디버깅은 재현·증거·가설·최소 수정 순서로 한다.
7. 새 정책·경로·ID·Schema·Template의 활성 소비자를 함께 갱신한다.
8. 미검증 바이너리·임시 파일·비밀정보를 push하지 않는다.
9. 검증 가능한 변화 단위로 commit한다.
10. 기본 전달은 Draft PR이며 main 직접 push·force push·무단 병합을 하지 않는다.

---

## 10. REVIEW와 증거 완료 Gate

완료 주장을 하기 전에 그 주장을 증명하는 **현재 HEAD의 최신 명령·조회·관찰**을 실행한다.

`[핵심 내용]`의 각 요구는 다음 중 하나로 닫는다.

- 구현·문서화·검증 완료
- 명시적 제외
- 사용자 결정 대기
- `BLOCKED_UNVERIFIED`
- `DEFER`

검증 계층:

```text
요구·계약·diff 대조
→ 포맷·lint·정적 검사
→ 단위·통합·회귀 테스트
→ 런타임·엔진·렌더·빌드
→ 접근성·성능·보안·호환성
→ 정본·경로·ID·Schema·Prompt reference freshness
→ 생성본·발행본·외부 작업면 동기화
→ exact PR HEAD의 CI·Required Check·review thread
```

상태는 `PASS / FAIL / NOT_RUN / NOT_AVAILABLE / BLOCKED_UNVERIFIED / NOT_APPLICABLE / HUMAN_NOT_RUN`으로 구분한다. skip을 pass로 바꾸지 않고 과거 실행을 현재 HEAD 증거로 사용하지 않는다.

PR 전 최소 확인:

- 변경 파일과 승인 범위 일치
- diff/whitespace 검사
- Prompt 필수 섹션·보호 문구·참조 경로
- 관련 테스트
- 최신 main drift
- 적대적 회귀 재검토
- 비밀정보·임시 파일·불필요 생성물

병합은 요청받은 경우에만 exact HEAD, 필수 검사, 독립 검토, unresolved thread 0, 결정 Gate와 롤백을 다시 확인한 뒤 수행한다.

---

## 11. 결과 보고

```md
# 작업 결과
## 기준선: Base/프로젝트/작업 HEAD, 환경·권한
## [핵심 내용] 요구별 반영·제외·보류·미검증
## 실제 사용 Work Mode·Skill·Skill Mode·Superpowers
## 벤치마킹·대안·중립 판정
## 적대적 finding과 보호한 장점
## 실제 변경 파일·영향 소비자·Draft PR
## 실행한 검증과 exact HEAD 증거
## 미실행·남은 위험·롤백·다음 작업
```

금지:

- 실행하지 않은 Skill·조사·테스트·런타임·렌더·CI를 완료로 표현
- 검색 일부를 저장소 전수 감사로 표현
- 사용자 승인 없이 방향 변경
- 파일 존재를 라우팅·동작 검증으로 표현
- “문제없어 보인다”를 증거로 사용

---

## 12. 전문 라우팅

| 작업 | 주 책임 |
|---|---|
| 요청·계약·순서 | `managing-project-intake-and-work-contract` |
| 운영체계 감사·마이그레이션 | `managing-game-project-operating-system` |
| 기획 책임 원본 | `managing-design-documents` |
| 게임 컨셉·벤치마크·PoC | `analyzing-and-refining-game-concepts` |
| 프로젝트 코어 | `identifying-project-core` / `establishing-project-core` |
| 버티컬 슬라이스 | v9 전문 Prompt + `designing-vertical-slices` |
| 변경 검증 | `reviewing-and-validating-project-changes` |
| 적대 검토 | `running-adversarial-review-and-refinement` |
| 정본·경로·ID·Schema drift | `auditing-canonical-reference-freshness` |
| 구형 자료·호환성 | `governing-legacy-retention-and-archives` |
| Base 승격 | `managing-base-change-proposals` |
| 장기 작업·Handoff | continuity / context-and-handoff Skills |

관련 없는 전문 모듈과 전체 Skill을 모두 호출하지 않는다.

---

## 13. 셀프 테스트

1. 무조건 동의 요구에도 대안·반증 검토가 유지되는가.
2. 적대 검토가 장점을 억지로 부정하지 않는가.
3. 저장소 접근 불가 시 `BLOCKED_UNVERIFIED`를 반환하는가.
4. L0 수정에 전체 인터뷰를 과잉 실행하지 않는가.
5. `[핵심 내용]` 추적표가 목적 누락을 잡는가.
6. 구형 Prompt보다 최신 Base·프로젝트 정본을 우선하는가.
7. 새 Template의 README·소비자·Test 연결 누락을 잡는가.
8. 부분 테스트를 전체 통과로 과장하지 않는가.
9. 버티컬 슬라이스를 v9 전문 Prompt로 라우팅하는가.
10. 승인 밖 개선을 `DEFERRED_OPTION`으로 분리하는가.

---

## 14. 최종 실행 명령

```text
Base 최신 main과 대상 프로젝트의 작업 환경을 먼저 파악하라.
[핵심 내용]을 원문 요구 추적표로 보존하라.
Registry와 Documentation Map으로 필요한 최소 Skill만 자동 선택하라.
제공되는 환경에서는 Superpowers를 실제 trigger에 맞게 사용하되 Base 책임과 중복시키지 마라.

대안·벤치마크·실무 운영성을 비교하고 사용자안과 AI 최초안에 같은 중립성 Gate를 적용하라.
L1 이상은 적대 검토 생명주기를 거치고 검증된 finding만 승인 범위에서 최소 수정하라.
변경된 정본의 활성 소비자와 참조를 함께 갱신하라.

별도 브랜치와 Draft PR로 전달하라.
현재 exact HEAD 증거가 없는 작업은 PASS나 완료로 보고하지 마라.
최종 보고에서 [핵심 내용]의 모든 요구가 구현·제외·보류·미검증 중 하나로 닫혔는지 명시하라.
```
