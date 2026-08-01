# Base 문서·스킬 역할표

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** 작업 원칙, Skill, Template, Test와 일반화된 Case를 관리한다. 프로젝트의 세계관·실제 수치·구현 상태·파일 경로·승인 자산·테스트 결과는 각 프로젝트 저장소가 책임진다.

## 1. 최소 시작 경로

```text
START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업에 필요한 Skill·Skill Mode·reference·Template·Test
→ 대상 프로젝트의 책임 원본과 실제 파일
```

최소 호출문:

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 작업해줘.`

`전부 살펴본다`는 전체 파일·전체 Skill을 기본 로드한다는 뜻이 아니다. Registry와 이 역할표로 현재 요청의 책임 원본·활성 소비자·검증 파일을 선별한다. 백업·보류·제거 후보·Archive는 감사·재개·구형본 정리 요청이 없는 한 기본 읽기에서 제외한다.

## 2. 권한 경계

### Base 저장소

```text
확정 운영 계약 → AGENTS.md·START_HERE.md·docs/OPERATING_MODEL.md
문서 위치·책임 → docs/DOCUMENTATION_MAP.md
활성 Skill → skills/SKILL_REGISTRY.json
이전 Skill ID → skills/LEGACY_SKILL_ALIASES.md
완료 변경 → docs/CHANGELOG.md
검토 대기 제안 → [수정제안서]/PROPOSAL_REGISTRY.json
진행 중 구현 → GitHub Issue·PR·Actions
과거 기록 → docs/archive/ARCHIVE_MANIFEST.json·Git 이력
```

Base 콜드 스타트에서는 프로젝트 설치 템플릿을 활성 상태 문서로 오인하지 않는다. Base에는 프로젝트별 활성 `ACTIVE_CONTEXT`, `CURRENT_STATUS`, `ROADMAP`을 두 번째 정본으로 유지하지 않는다. `docs/ACTIVE_HANDOFF.md`는 과거 링크 보존용 `COMPATIBILITY_ONLY` Stub이며 현재 상태를 소유하지 않는다.

### 대상 프로젝트

```text
프로젝트 AGENTS.md
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md·DOCUMENTATION_MAP.md·DEVELOPMENT_GATES.md
→ CURRENT_CONFIRMED_DECISIONS.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 분야 책임 원본
→ SKILL_REGISTRY.json
→ Roadmap·Issue·Plan·실행 순서
→ 실제 코드·데이터·Scene·Resource·자산·테스트
```

한 질문에는 현행 책임 원본 하나만 둔다. 외부 사례·리뷰·Google Sheets·Archive·과거 대화는 요구사항이나 구현 사실의 정본을 대체하지 않는다.

## 3. Base 공용 책임 원본

| 구분 | 파일 | 책임 |
|---|---|---|
| 최초 라우터 | `START_HERE.md` | 요청 유형별 최소 읽기와 실행 Skill·Skill Mode 연결 |
| 항상 적용 규칙 | `AGENTS.md` | 우선순위·보안·승인·완료 보고 금지 규칙 |
| 통합 운영 모델 | `docs/OPERATING_MODEL.md` | 작업 생명주기·책임 원본·상태·발행·근거·검증 정책 |
| Work Mode·Skill 라우팅 | `docs/WORK_MODE_AND_SKILL_ROUTING.md` | PLAN·BUILD·REVIEW, 자동 선택, Grill Me, 실행 보고 |
| GPT–Codex 역할·인계 | `docs/GPT_CODEX_WORKFLOW_POLICY.md` | GPT 비-Godot 완료, Codex Plan 검토, 단계별 Godot 구현·PR Gate |
| GitHub Pro 운영 | `docs/GITHUB_PRO_OPERATING_POLICY.md` | Ruleset·`ci-gate`·자동 병합·사용량 Budget |
| GitHub 작업 항목 수명주기 | `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` | Issue·Goal·Branch·PR·Run·Artifact·Release 보존·종료 |
| 승인 결정 동기화 | `docs/CONFIRMED_DECISION_SYNC_POLICY.md` | 질문 전 대조, 중복 질문 방지, 승인 즉시 정본화, 병합 후 검토 |
| 기획 순서·근거·Demo-First | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` | 누락·충돌 선감사, Evidence Pack, Approval Bundle, Vertical Slice |
| 프로젝트 GDD Google Sheets | `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md` | `USER_FACING_GDD_WORKSPACE`, 단일 결정·GDD Module·선택적 시각 Artifact 색인, Sheet 제안·GitHub 동기화 |
| 시각 협업 도구 | `docs/VISUAL_COLLABORATION_TOOL_POLICY.md` | Figma·Whimsical의 GDD/외부 협업 역할·Artifact·정본 경계 |
| 재사용 Capability 조합 | `docs/CAPABILITY_COMPOSITION_MAP.md` | 허용 context·조합·금지 경계·필요 증거 |
| 이미지 생성·검수·Sheet 구조 | `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md` | 기획 시각화, 이미지 QA·승인 원장·의미 구조 |
| 근거 기반 게임 개발 허브 | `docs/knowledge/game-development/README.md` | 기획·아트·개발·AI·연구·출시 Method·Guide·Case 라우팅 |
| CI 실행·비용 | `docs/CI_EXECUTION_COST_POLICY.md` | 변경 등급별 검증·concurrency·Windows·비용 Gate |
| 활성 Skill 기계 원본 | `skills/SKILL_REGISTRY.json` | trigger·상태·경로·Skill Mode 라우팅 |
| 활성 Skill 생성 뷰 | `docs/generated/BASE_ACTIVE_SKILLS.md` | Registry에서 생성한 사람용 목록; 직접 편집 금지 |
| 이전 Skill 별칭 | `skills/LEGACY_SKILL_ALIASES.md` | 통합 전 ID를 현행 Skill·Mode로 연결 |
| Skill 실행 학습 | `skills/SKILL_LEARNING_LOG.md` | 실패·결정·검증·갱신 판정 |
| Skill 행동 평가 | `skills/SKILL_BEHAVIOR_EVALS.json` | 실제 Prompt의 예상 Work Mode·Skill·Mode·금지 라우팅·필수 증거 |
| 로컬 통합 검증 | `tools/run_local_validation.py` | 저장소 소유 임시 환경에서 전체 회귀·CI topology·v9 무결성·Skill coverage·Git 검사를 실행하는 단일 진입점 |
| Base 수정제안서 | `[수정제안서]/PROPOSAL_REGISTRY.json` | 프로젝트발 공용화 후보·승인·구현 상태 |
| 실행 체크 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 운영 모델에서 파생한 시작·Gate·종료 체크 |
| 변경 기록 | `docs/CHANGELOG.md` | 완료된 Base 변경과 동기화 기준 |
| Handoff 호환 경로 | `docs/ACTIVE_HANDOFF.md` | `COMPATIBILITY_ONLY`; 프로젝트별 현재 상태를 소유하지 않음 |
| Archive 운영 | `docs/archive/README.md`, `docs/archive/ARCHIVE_MANIFEST.json` | 비활성 원문·hash·replacement·rollback·권한 기록 |

## 4. 프로젝트 책임 원본

```text
현재 상태 → ACTIVE_CONTEXT.md 또는 프로젝트가 선언한 CURRENT_STATUS.md
문서 위치·책임 → DESIGN_DOCUMENT_REGISTRY.json
프로젝트·분야 방향 → 등록된 Markdown 또는 JSON 원본
현재 승인 결정 복원 → CURRENT_CONFIRMED_DECISIONS.md
현재 실행 범위 → Issue·승인된 직접 요청·Plan
Work Mode → PLAN / BUILD / REVIEW
실행 순서 → 단계·의존성·병렬 묶음·Gate
Skill 선택·상태 → SKILL_REGISTRY.json
Skill 실행 증거 → 사용 이유·수행 내용·결과·미검증 보고
전체 구현 기준 → MASTER_IMPLEMENTATION_PLAN
현재 Godot 구현 범위 → 구현 패키지 계약·Branch·PR
외부 근거 → 출처·날짜·버전·표본·해석이 있는 조사 기록
플레이 증거 → build·tester·행동·feedback·funnel·experiment 기록
실제 상태 → 코드·데이터·Scene·Resource·자산·테스트·캡처·프로파일
발행 최신성 → Publication Manifest
과거 상태 → Git 이력·승인된 Archive
```

일반 프로젝트의 기획·상태 확인은 GitHub 정본과 구성된 프로젝트 GDD Google Sheets를 우선한다. HTML 대시보드는 사용자 명시 요청 또는 기존 유지보수에만 사용한다.

## 5. Active Skill Registry View

- `skills/SKILL_REGISTRY.json`: 기계 권한
- `docs/generated/BASE_ACTIVE_SKILLS.md`: 생성된 현재 목록·책임·trigger
- `skills/BASE_V9_SKILL_SNAPSHOT.json`: frozen v9.0 release contract projection; 현재 라우팅 권한 아님
- `skills/LEGACY_SKILL_ALIASES.md`: 이전 ID 호환 경로
- `skills/SKILL_BEHAVIOR_EVALS.json`: 정상·비사용·경계·교차 Skill 행동 fixture
- `tools/check_skill_behavior_evals.py`: fixture 계약 검사와 외부 모델 결과 채점

활성 Skill 수는 Registry 관찰값이며 설계 제약이 아니다. 사용자는 Skill·Skill Mode를 선언할 필요가 없고, Prompt 의도와 현재 단계에서 trigger가 일치하는 최소 Skill만 자동 선택한다.

```json
{
  "load_all_skills": false,
  "default_selection": "automatic-trigger-match",
  "automatic_selection": true,
  "user_skill_declaration_required": false,
  "require_trigger_match": true,
  "require_execution_report": true,
  "work_modes": ["PLAN", "BUILD", "REVIEW"],
  "max_primary_discipline_skills": 1,
  "max_foundation_skills": 3
}
```

- `PLAN`: 요구·근거·설계·정본·실행 순서
- `BUILD`: 승인 범위의 구현·제작·갱신
- `REVIEW`: 적대적 검토·반례·검증·판정
- `clarify` + Grill Me: 사용자만 결정할 수 있는 중요 충돌
- `decompose-and-sequence`: 승인된 L2 이상·다중 의존성
- `reconcile-legacy`: 구형·중복·stale 파생본
- `reference-freshness`: 정본·경로·ID·Schema·생성기 변경 전파
- `accessibility-review`·`performance-profile`: 변경 영향과 목표 플랫폼이 있을 때만 적용

## 6. 질문별 Reference·Template

| 질문 | 먼저 읽을 Reference | 출력 Template |
|---|---|---|
| Work Mode·Skill·Skill Mode 선택 | `docs/WORK_MODE_AND_SKILL_ROUTING.md` | `templates/project-operations/SKILL_EXECUTION_REPORT.md` |
| Grill Me 핵심 결정 | `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md` | `templates/project-operations/GRILL_ME_DECISION_RECORD.md` |
| 실행 단계·의존성·병렬화 | `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md` | `templates/planning/EXECUTION_SEQUENCE_PLAN.md` |
| GPT→Codex 구현 인계 | `skills/maintaining-project-context-and-handoff/references/gpt-codex-implementation-handoff.md` | `templates/project-operations/MASTER_IMPLEMENTATION_PLAN.md`, `templates/project-operations/CODEX_PACKAGE_PLAN_REPORT.md`, `templates/project-operations/IMPLEMENTATION_PACKAGE_CONTRACT.md` |
| GitHub 보호·Ruleset·자동 병합 | `docs/GITHUB_PRO_OPERATING_POLICY.md` | `templates/project-operations/github/GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md` |
| PR·Run·Artifact 무손실 정리 | `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md` | `.github/pull_request_template.md`, `templates/pull_request_template.md` |
| 구형 파일 분류·보존·Archive | `skills/governing-legacy-retention-and-archives/SKILL.md` | `templates/project-operations/LEGACY_ARTIFACT_RECONCILIATION.md` |
| 게임 코어 판정·확정 | `skills/identifying-project-core/SKILL.md`, `skills/establishing-project-core/SKILL.md` | 프로젝트 코어 책임 원본 |
| 게임 시스템·난이도·전투 AI (`system-design` / `difficulty-and-combat-ai`) | `skills/analyzing-and-refining-game-concepts/references/game-system-difficulty-and-combat-ai.md` | `templates/planning/GAME_SYSTEM_DIFFICULTY_AND_COMBAT_AI_CONTRACT.md` |
| 벤치마크·플레이어 근거·실험 | `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md` | `templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md` |
| 게임 기획·아트·개발·AI·출시 근거 | `docs/knowledge/game-development/README.md` | `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`, `templates/research/GAME_DEVELOPMENT_CASE_CARD.md` |
| UI 설계·폴리싱·런타임 감사 | `skills/auditing-and-refining-ui-art/SKILL.md` | `templates/planning/GAME_UX_UI_SYSTEM.md`, `templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md` |
| 접근성·성능 | `skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md` | `templates/quality/PROJECT_CHANGE_VALIDATION.md` |
| 정본 변경 전파 | `skills/auditing-canonical-reference-freshness/SKILL.md` | `templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md` |
| 저장소 전체 누락·stale·Prompt drift | `skills/running-adversarial-review-and-refinement/references/repository-wide-audit-protocol.md` | 저장소 전체 적대적 감사 보고 |

## 7. 안정 호환 라우팅 인덱스

아래 문자열과 경로는 기존 Template·Test·외부 참조가 현재 책임 원본을 찾는 안정 경로다. 설명을 중복 확장하지 않되 제거하거나 임의로 축약하지 않는다.

- 현행 Vertical Slice 통합 첨부 Prompt: `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md`
- v8 → v9 이관·첨부 변형 hash: `docs/knowledge/VERTICAL_SLICE_V8_TO_V9_MIGRATION.md`
- Grill Me 핵심 의사결정 인터뷰
- `clarify` + `references/grill-me-protocol.md`
- GPT→Codex 단계별 Godot 구현 인계
- `implementation-package-handoff`
- GitHub Pro 저장소 운영
- GitHub Pro 보호·Ruleset·자동 병합
- `GITHUB_REPOSITORY_GOVERNANCE_PROFILE.md`
- `GITHUB_USAGE_BUDGET.md`

## 8. Archive·호환 문서

- `docs/ACTIVE_HANDOFF.md`: 과거 링크 보존용 `COMPATIBILITY_ONLY` Stub
- `docs/archive/README.md`: Archive 권한·복구 규칙
- `docs/archive/ARCHIVE_MANIFEST.json`: archive ID·원문 hash·replacement·rollback·검증 상태
- `docs/archive/handoffs/2026-07-29-ux-ui-common-system-expansion.md`: 2026-07-29 UX/UI 공용 체계 확산 Handoff 원문 (`ARCHIVE_HISTORY`)

Archive는 기본 콜드 스타트·현재 정본·자동 실행 계획에 포함하지 않는다. 복원은 Archive 파일을 직접 현행으로 복사하지 않고 현재 정본과 충돌을 검토한 별도 변경안으로 수행한다.

## 9. 발행 정책

각 문서는 Registry에서 하나의 정책을 선택한다.

| 정책 | 사용 |
|---|---|
| `source_only` | 원본과 직접 검증만 유지 |
| `milestone_sync` | 주요 Gate·정기 검토·외부 공유 시 PDF·Manifest 동기화 |
| `always_sync` | 원본·승인 이미지·생성기 변경 시 상시 동기화 |

DOCX·다이어그램은 선언한 경우만 생성한다. `CURRENT`, 자동 렌더, Codex 시각 검수, 사용자 시각 검수는 독립 상태다.

## 10. 구조 최적화·지원 Skill

| 책임 | Skill | 주요 Mode |
|---|---|---|
| 무손실 가지치기 | `pruning-stale-and-nonfunctional-material` | `inventory / classify / preserve-unique / prune-approved / verify-no-loss` |
| 본문 간소화 | `simplifying-skill-bodies` | `inventory / extract-references / rewrite-router / validate-disclosure` |
| 계약 보존 리팩토링 | `refactoring-with-contract-preservation` | `baseline-contract / smell-audit / refactor / regression-validate` |
| 적대적 검토 | `running-adversarial-review-and-refinement` | `repository-wide-audit / attack / validate-critique / regression-recheck` |
| 변경 검증 | `reviewing-and-validating-project-changes` | `contract-check / static-validation / regression / evidence-report` |
| 로컬·GitHub 동기화 | `synchronizing-local-and-github-state` | `inspect / reconcile / refresh-local / publish-remote / verify-sync` |
| 장기 작업 연속성 | `maintaining-long-running-task-continuity` | `initialize / checkpoint / resume / partial-delivery / close` |
| Games User Research | `governing-game-user-research-coverage` | `install / audit / plan-evidence / synthesize / verify-coverage` |
| 사용자 학습 노트 | `creating-user-learning-notes` | `capture / explain / connect / practice / update` |
| 엔진 런타임 디버깅 | `diagnosing-game-engine-runtime-failures` | `reproduce / isolate / fix-minimally / revalidate / prevent` |

원문 책임 Coverage는 `docs/SKILL_COVERAGE_MAP.md` → `skills/SKILL_COVERAGE.json` → `tools/check_skill_system_coverage.py` 순서로 확인한다.

## 11. Base v9 운영 문서

- [Base Rules Version](BASE_RULES_VERSION.md)
- [System Map](operations/BASE_V9_SYSTEM_MAP.md)
- [Maturity Model](operations/BASE_V9_MATURITY_MODEL.md)
- [Release Design](operations/BASE_V9_RELEASE_DESIGN.md)
- [Implementation Plan](operations/BASE_V9_IMPLEMENTATION_PLAN.md)
- [Migration Map](operations/BASE_V9_MIGRATION_MAP.md)
- [Release Contract](operations/BASE_V9_RELEASE_CONTRACT.md)
- [Integrity Audit](operations/BASE_V9_INTEGRITY_AUDIT.md)
- [Adversarial Review Report](operations/BASE_V9_ADVERSARIAL_REVIEW_REPORT.md)
- [Current Active Base Skills](generated/BASE_ACTIVE_SKILLS.md)
- [Open-Source Godot UI Reference Catalog](knowledge/OPEN_SOURCE_GODOT_UI_REFERENCE_CATALOG.md)
- [Held Common Project Adoption Work Order](../templates/prompts/BASE_V9_COMMON_PROJECT_ADOPTION_WORK_ORDER.md)
- [Base v9.1 Release Contract](operations/BASE_V9_1_RELEASE_CONTRACT.md)
- [Base v9.1 System Map](operations/BASE_V9_1_SYSTEM_MAP.md)
- [Base v9.1 Dual-Axis Maturity](operations/BASE_V9_1_MATURITY_MODEL.md)
- [Base v9.1 Dashboard Contract](operations/BASE_V9_1_DASHBOARD_CONTRACT.md)
- [Base v9.1 Skill Pressure Tests](operations/BASE_V9_1_SKILL_PRESSURE_TESTS.md)
- [Base v9.1 Integrity Audit](operations/BASE_V9_1_INTEGRITY_AUDIT.md)
- `../base-v9.1.lock.json`: machine-readable Base v9.1 `RELEASE_CANDIDATE` identity; v9.0 remains in `../base.lock.json`.
- `superpowers/plans/2026-07-30-base-v9-1-review-remediation.md`: review-blocker TDD remediation plan and verification contract.

## 12. 콜드 스타트·완료

새 작업자는 저장소만으로 다음을 찾아야 한다.

1. Base와 프로젝트가 각각 무엇을 책임지는가.
2. 현재 단계·Work Mode·보호 범위는 무엇인가.
3. 현재 책임 원본·실제 파일·활성 Skill·Skill Mode는 어디인가.
4. 어떤 결정·Issue·PR·실행 순서가 현재 작업을 통제하는가.
5. 정적·런타임·렌더·사람·접근성·성능 검증 중 무엇이 실행됐는가.
6. 미확정·보류·위험·롤백·다음 진입 조건은 무엇인가.

L1 이상 완료 보고는 실제 사용한 Work Mode·Skill·Skill Mode와 이유, 변경 파일, 근거, 검증 결과, 미검증, Archive·호환·롤백, 다음 작업을 분리한다. GitHub Actions·Repository 설정·런타임·Google Sheets를 확인하지 못했으면 성공으로 추정하지 않는다.

## Base v9.4 AI 운영 계약

| 질문 | 책임 원본 |
|---|---|
| 모델·추론 단계·Prompt caching·비용 | `skills/optimizing-ai-model-and-prompt-costs/SKILL.md` |
| 지시 권위·Interface-first·Context 큐레이션·Artifact 주장 상한 | `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md` |
| 게임 UI 모션·중단·반복·Reduced Motion | `skills/auditing-and-refining-ui-art/references/ui-motion-and-interaction-principles.md` |
| Base v9.4 후보·evidence·pin 순서 | `docs/operations/BASE_V9_4_RELEASE_CONTRACT.md` |
