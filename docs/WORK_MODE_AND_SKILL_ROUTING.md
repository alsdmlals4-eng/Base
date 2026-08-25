# Work Mode·Skill·Skill Mode 라우팅 계약

## 1. 용어

### Work Mode

요청을 처리하는 동안 AI의 주된 작업 자세·권한·증거 기준이다.

| Work Mode | 핵심 목적 | 기본 행동 |
|---|---|---|
| `PLAN` | 의도·요구·근거·설계·순서 확정 | 조사·정본 복원·대안 비교, 구현 전 승인/준비 Gate |
| `BUILD` | 승인된 계약의 실제 구현 | Codex가 코드·데이터·Scene·Resource·test·runtime 변경 수행 |
| `REVIEW` | 결과를 적대적으로 검토·검증·판정 | GPT가 기획 일치·증거·회귀·누락을 공격하고 필요한 반환 경로 결정 |

복합 작업은 `PLAN → BUILD → REVIEW`로 전환한다. 한 시점의 주 Work Mode는 하나다.

### Skill

특정 책임을 반복 수행하는 전문 작업 계약이다. trigger, 입력, 절차, 산출물, 실패 조건과 검증을 가진다.

### Skill Mode

한 Skill 내부에서 현재 필요한 세부 절차·권한을 선택한다.

### Grill Me

`managing-project-intake-and-work-contract`의 `clarify` Skill Mode에서 실행하는 핵심 의사결정 인터뷰다. 저장소·Notion에서 답할 수 있는 사실을 묻지 않고 프로젝트 방향을 바꾸는 사용자 결정만 질문한다.

### Continuous Work

`[연속작업] 진행해`는 현재 승인된 작업 계약의 남은 범위를 중간 승인 대기로 끊지 않고 연속 수행하라는 opt-in flag다. 새 권한이나 새 승인 자체를 만들지 않는다.

## 2. 역할 분리 라우팅

공용 정본: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

```text
GPT PLAN
→ GitHub + Notion current canon 복원
→ 조사·벤치마킹·대안 비교
→ 기획·Flow·UI/UX·데이터·시각 요구 설계
→ 적대적 검토·IRG
→ 이미지가 필요하고 사용자가 생성/편집을 요청한 경우 GPT visual pipeline
→ Notion 승인 Visual upload/readback
→ IMPLEMENTATION_READY

구현/코딩 없음
→ GPT REVIEW / canon readback / 종료

구현/코딩 있음
→ CODEX_IMPLEMENTATION_HANDOFF
→ Codex CODEX_REHYDRATE_GITHUB_AND_NOTION
→ 필요 시 CODEX_PREFLIGHT_OPTIONAL
→ Codex BUILD
→ 실제 test/runtime/play evidence
→ GPT REVIEW
→ 승인/수정/기획반환/Visual반환
```

핵심 불변식:

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING
GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED
```

과거 `GPT 평상시 Godot 구현 보조·POC → 사용자 요청 시 Codex` 라우팅은 사용하지 않는다. `USER_REQUESTED_CODEX_HANDOFF`는 사용자가 명시적으로 인계를 요구할 때의 호환 trigger로 남을 수 있으나 구현 전환의 필수 조건이 아니다.

## 3. 자동 실행 순서

```text
사용자 Prompt
→ 의도·현재 단계·위험 파악
→ Project/Base/Notion/GitHub 권위 복원
→ 주 Work Mode 자동 선택
→ Skill Registry trigger 대조
→ 필요한 최소 Skill/Skill Mode 선택
→ 승인·연속작업 범위 확인
→ PLAN이면 GPT 수행
→ BUILD가 필요하면 Codex handoff
→ REVIEW는 GPT가 결과·증거 검수
→ readback / 병합 Gate / 다음 Slice
```

사용자가 Skill 이름이나 mode를 지정하면 강한 힌트로 사용하지만 실제 trigger·권한·정본과 충돌하면 current canon을 우선한다.

## 4. 자동 선택 규칙

- `load_by_default=false`는 trigger가 없을 때 불필요하게 읽지 않는다는 뜻이다.
- 주 책임 분야 Skill은 최대 하나를 기본으로 하고 Foundation·검증·발행·Handoff Skill은 필요한 만큼만 추가한다.
- 같은 책임을 여러 Skill로 중복 실행하지 않는다.
- 새 사실·실패·범위 변경·정본 변경이 생기면 다시 라우팅한다.
- Skill 파일을 읽은 것과 실제 절차를 실행한 것을 구분한다.
- 새 독립 Skill보다 기존 owner의 Skill Mode/reference로 책임을 보존할 수 있는지 먼저 확인한다.
- `[연속작업] 진행해`는 현재 `CONFIRMED` 또는 `REUSED_APPROVAL` 범위 안에서만 `CONTINUOUS_WORK_ACTIVE`를 부여한다.

## 5. 경량 중립성 Gate와 적대적 검토

권장안·설계 선택은 `평가 기준 → 대안 → 반증 → 이익·비용·위험 → 되돌리기 → 미검증 → 권장 결론`으로 본다.

- `L0`: 오탈자·명백한 기계 수정·동일 입력 재검사는 전체 적대 검토를 강제하지 않는다.
- `L1+`: 중요한 기능·설계·아키텍처·정책·방향은 `running-adversarial-review-and-refinement`의 전체 review lifecycle을 적용한다.
- 승인된 finding은 실제 owner BUILD에서 한 번 수정하고 REVIEW로 복귀한다.
- 최소 full loop count와 clean exit는 latest Base adversarial owner를 따른다.
- 증거가 부족하면 `BLOCKED_UNVERIFIED`로 남긴다.

## 6. 권한 전환

### PLAN — GPT

- 읽기·조사·벤치마킹·기획·계약 작성
- Notion 사람용 기획/Flow/Visual/표 교정
- 이미지 brief·생성·편집·검수와 승인 Visual delivery
- 구현 준비 판정과 Codex handoff
- 제품 code/Scene/Resource/runtime 구현은 수행하지 않음

### BUILD — Codex

- 실제 GitHub + relevant Notion 재수화
- 승인 범위 code/data/Scene/Resource/config/test/build/runtime 구현
- 안전한 기술 세부 결정·리팩터링
- 실제 test/runtime evidence
- 이미지 생성·생성형 편집 금지
- 현재 용도로 승인되어 Notion에 attach/readback된 Visual만 소비
- 이미지 부족 시 `GPT_VISUAL_REQUEST`
- 프로젝트 코어·주요 UX·경제·서사·범위 변경 시 `CHANGE_PROPOSAL`

### REVIEW — GPT

- 승인 기획과 실제 diff/Commit/test/runtime 대조
- Notion/GitHub sync와 evidence ceiling 검사
- Codex image-generation 금지 준수 검사
- 승인 Visual provenance/사용처 검사
- 적대적 finding과 회귀 검사
- `PACKAGE_APPROVED | PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES | USER_REVIEW_REQUIRED | CHANGE_PROPOSAL | WAITING_GPT_VISUAL | REVISE | BLOCKED | UNVERIFIED` 판정

## 7. Codex 구현 인계

`CODEX_IMPLEMENTATION_HANDOFF` 최소 입력:

```yaml
intent_and_player_outcome:
implementation_ready: true
actual_state_verification_required: true
notion_sources:
  project_home:
  relevant_domain_pages: []
  ai_system_detail_pages: []
  approved_visual_records: []
github_sources:
  repository:
  agents:
  active_context:
  structured_canon: []
  implementation_paths: []
protected_behavior_and_contracts: []
acceptance_criteria: []
required_tests_and_runtime_checks: []
forbidden_or_high_risk_changes: []
visual_policy:
  generation_by_codex: FORBIDDEN
  approved_notion_visuals_only: true
  missing_visual_action: GPT_VISUAL_REQUEST
```

Codex는 handoff를 정본으로 맹신하지 않고 current GitHub+Notion을 다시 읽는다.

### `CODEX_PREFLIGHT_OPTIONAL`

고위험·불확실·다중 의존성에서만 읽기 전용 기술 Plan을 추가한다.

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
```

Plan 생략은 rehydration 생략이 아니다.

## 8. Visual 반환 경로

Codex가 별도 image asset 필요성을 발견하면 직접 만들지 않는다.

```yaml
GPT_VISUAL_REQUEST:
  implementation_task:
  why_required:
  player_or_ui_role:
  asset_type:
  target_screen_or_scene:
  required_dimensions_or_ratio:
  transparency_or_format:
  visual_constraints:
  existing_approved_references: []
  notion_destination:
  acceptance_criteria: []
```

흐름:

```text
WAITING_GPT_VISUAL
→ GPT brief / 사용자 승인 / 생성·편집 / 검수
→ exact Notion Visual/Asset upload + Approved + readback
→ Codex fresh-read
→ BUILD resume
```

독립 구현이 가능하면 Visual 대기 때문에 전체 프로젝트 작업을 멈추지 않는다.

## 9. Continuous Work

`CONTINUOUS_WORK_ACTIVE`에서는 승인 범위의 Global Progress Queue를 유지한다.

```text
ready PLAN task → GPT
ready BUILD task → Codex handoff
Codex result → GPT REVIEW
recoverable blocker → 재조회/대체 evidence/독립 task
WAITING_GPT_VISUAL → GPT visual route
CHANGE_PROPOSAL / USER_DECISION → 관련 범위만 대기
독립 ready task 계속
```

`GLOBAL_TERMINAL_BLOCKER`는 recovery path를 소진하고 독립 ready task가 없을 때만 사용한다.

## 10. 구현 패키지와 승인 게이트

L2 이상·다중 의존성 작업은 전체 설계를 마스터 구현계획 하나로 유지하고 검증 가능한 결과 패키지로 분리한다. 작은 국소 작업에는 형식적 패키지 체계를 강제하지 않는다.

```text
상위 구현 추적 단위
├─ 패키지 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이며 완전히 독립적인 작업만 병렬화한다.

패키지 종료 상태:

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `WAITING_GPT_VISUAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

## 11. 병합

기본 정책은 `AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 사용자의 명시적 승인이 완료된 동일 범위는 추가 확인·재승인·병합 승인 요청 없이 현재 repository의 실제 merge gate를 통과하면 병합할 수 있다.

병합 전 현재 HEAD, required checks, unresolved threads, ruleset, 허용 merge method를 실제로 확인한다. 특정 check 이름을 공용 문서에서 영구 고정하지 않는다.

다른 독립 open/draft/ready PR은 read-only로 보호한다.

## 12. 필수 실행 보고

L1 이상 작업은 실제 사용한 항목을 남긴다.

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
reason:
work_performed:
result:
evidence:
status: PASS | PARTIAL | FAIL | UNVERIFIED
```

Codex 구현을 사용했다면 다음도 포함한다.

```yaml
codex_result:
  changed_files_and_reasons: []
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  runtime_or_play_evidence: []
  approved_notion_visuals_consumed: []
  visual_requests_waiting: []
  change_proposals: []
```

## 13. 예시

### 기능 구현

```text
Prompt: 전투 결과 저장 기능을 구현해줘.
GPT PLAN: 저장 책임·Schema·호환성·Acceptance 설계 + 적대적 검토
→ IMPLEMENTATION_READY
→ CODEX_IMPLEMENTATION_HANDOFF
Codex: GitHub + Notion 재수화
→ 필요 시 CODEX_PREFLIGHT_OPTIONAL
→ BUILD 구현·테스트·Commit/PR
GPT REVIEW: 저장·불러오기·경계·회귀·기획 일치 검수
→ merge gate
```

### 이미지가 필요한 UI 구현

```text
GPT PLAN: 화면 구조·상태·Visual requirement 승인
Codex BUILD: 승인된 Notion Visual로 UI 구현
→ 필요한 portrait가 없음
→ GPT_VISUAL_REQUEST
GPT: brief → 사용자 승인 → image 제작/검수 → Notion upload/readback
Codex: 새 Visual readback → UI 구현 재개
GPT REVIEW
```

### GDD 검수

```text
GPT REVIEW: 영향 범위 → 적대적 공격 → 기술 검수안 / 사용자 결정 분리
문서·Notion만 바뀌면 Codex 없이 종료
실제 구현 변경이 필요하면 CODEX_IMPLEMENTATION_HANDOFF
```

## CLAIM_AND_INTENT_VERIFICATION_GATE

완료·검증·병합 주장은 `reviewing-and-validating-project-changes: claim-and-intent-verification`으로 검증한다.

```text
material claim 원자화
→ authority·freshness·counterevidence
→ 승인 Intent·Acceptance와 actual diff 연결
→ exact HEAD 실행 Evidence
→ Completion Claim Gate
→ merge 뒤 post-merge main readback
```

검색 결과·모델 자신감·테스트 정의·다른 SHA의 PASS는 직접 Evidence가 아니다. 필수 Evidence가 없으면 `CLAIM_UNVERIFIED`, `IMPLEMENTATION_UNVERIFIED` 또는 `BLOCKED_UNVERIFIED`를 유지한다.