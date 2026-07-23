# Base 문서·스킬 역할표

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** 작업 원칙, Skill, Template, Test와 일반화된 Case를 관리한다. 프로젝트의 세계관, 실제 수치, 구현 상태, 파일 경로, 승인 이미지와 테스트 결과는 프로젝트 저장소가 책임진다.

## 1. 최초 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업의 Work Mode·Skill·Skill Mode·reference·Template·Test·Case
→ 대상 프로젝트의 Registry·책임 원본·실제 파일
```

최소 호출문:

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 작업해줘.`

대상 프로젝트 읽기 순서:

```text
프로젝트 AGENTS.md
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md·DOCUMENTATION_MAP.md·DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 책임 원본
→ SKILL_REGISTRY.json
→ Prompt 의도와 현재 단계
→ PLAN / BUILD / REVIEW Work Mode
→ 자동 선택된 최소 Skill과 Skill Mode
→ Roadmap·Issue·Plan·실행 순서
→ 실제 코드·데이터·자산·테스트
```

저장소 전체나 전체 스킬을 무작정 읽지 않는다. 백업·보류·제거 후보는 감사·재개·구형본 정리 요청이 없는 한 기본 읽기에서 제외한다.

Base 저장소 자체의 콜드 스타트에서는 프로젝트 설치 템플릿을 활성 상태 문서로 오인하지 않는다. 완료 상태는 `docs/CHANGELOG.md`, 검토 대기 작업은 `[수정제안서]/PROPOSAL_REGISTRY.json`, 진행 중 구현은 GitHub PR·Actions가 책임진다. 활성 인터뷰가 없으면 `등록 없음`으로 명시한다.

## 2. 공용 책임 원본

| 구분 | 파일 | 책임 |
|---|---|---|
| 최초 라우터 | `START_HERE.md` | 요청 유형별 최소 읽기와 실행 Skill·Skill Mode 연결 |
| 항상 적용 규칙 | `AGENTS.md` | 우선순위·보안·승인·완료 보고 금지 규칙 |
| 통합 운영 모델 | `docs/OPERATING_MODEL.md` | 공용 작업 생명주기·책임 원본·상태·발행·근거·검증 정책의 단일 설명 원본 |
| Work Mode·Skill 라우팅 | `docs/WORK_MODE_AND_SKILL_ROUTING.md` | PLAN·BUILD·REVIEW, Skill·Skill Mode 구분, 자동 선택·실행 보고 상세 계약 |
| 저장소 개요 | `README.md` | 사용 목적·구조·활성 스킬 안내 |
| 문서·스킬 지도 | `docs/DOCUMENTATION_MAP.md` | 질문별 책임 원본과 최소 읽기 |
| Base Skill Registry | `skills/SKILL_REGISTRY.json` | 자동 Skill trigger·상태·경로·Skill Mode 라우팅 신호 |
| 이전 ID 별칭 | `skills/LEGACY_SKILL_ALIASES.md` | 통합 전 Skill ID를 새 Skill Mode로 연결 |
| Base Skill Learning Log | `skills/SKILL_LEARNING_LOG.md` | 실행 결과·실패·갱신 판정 |
| Base 수정제안서 | `[수정제안서]/PROPOSAL_REGISTRY.json` | 프로젝트발 승격 후보·승인·구현 상태 |
| 실행 체크 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 운영 모델에서 파생한 시작·게이트·종료 체크 |
| 변경 기록 | `docs/CHANGELOG.md` | Base 변경과 동기화 기준 |

## 3. 프로젝트 책임 원본

```text
현재 상태 → ACTIVE_CONTEXT.md
문서 위치·책임 → DESIGN_DOCUMENT_REGISTRY.json
프로젝트·분야 방향 → 등록된 Markdown 또는 JSON 원본
현재 실행 범위 → Issue·승인된 직접 요청·Plan
Work Mode → 현재 단계의 PLAN / BUILD / REVIEW
실행 순서 → 단계·의존성·병렬 묶음·게이트 계획
Skill 선택·상태 → SKILL_REGISTRY.json
Skill 실행 증거 → 사용 이유·수행 내용·결과·미검증 보고
반복 절차 → Skill과 Skill Mode
외부 근거 → 출처·날짜·버전·표본·해석이 있는 조사 기록
플레이 증거 → 빌드·테스터·행동·피드백·퍼널·실험 기록
실제 상태 → 코드·데이터·자산·테스트·캡처·프로파일
사람용 발행 → Registry 정책이 요구하는 PDF·선택 DOCX·assets
발행 최신성 → Publication Manifest
과거 상태 → Git 이력
```

한 질문에는 현행 책임 원본 하나만 둔다. 같은 서술을 Markdown과 JSON 양쪽에 독립 원본으로 유지하지 않는다. 벤치마크·리뷰·커뮤니티는 요구사항이나 구현 상태의 정본을 대체하지 않는다.

## 4. 활성 실행 스킬

| 작업 | Skill | Skill Mode 또는 호출 조건 |
|---|---|---|
| 의도·Work Mode·Skill 자동 라우팅·실행 보고 | `managing-project-intake-and-work-contract` | `route` → 필요 시 `clarify` → `contract` → 필요 시 `decompose-and-sequence` → `execution-report` |
| 운영체계 신규 설치·기존 감사·마이그레이션·Health Review | `managing-game-project-operating-system` | `install` / `audit` / `migrate` / `verify` |
| 구형·중복·버전명 파일 갱신·통합·아카이브·승인 삭제 | `managing-game-project-operating-system` | `audit` → `reconcile-legacy` → `verify` |
| 기획 책임 원본 작성·구조 변경·발행·검수 | `managing-design-documents` | `author` / `update` / `restructure` / `publish` / `validate` |
| 분야별 스킬 생성·통합·학습 | `evolving-project-discipline-skills` | 스킬 추가·중복·반복 실패·Registry 변경 |
| Active Context·Handoff | `maintaining-project-context-and-handoff` | 상태·다음 작업·게이트·위험 변경 |
| 컨셉·제약·뾰족한 재미·PoC·기획 재조정 | `developing-game-concepts-and-pocs` | concept → constraints → pointed fun → alignment → PoC → recalibration → production gate |\n| 세그먼트·대안·SWOT·VRIO·포지셔닝 | `analyzing-game-positioning-with-swot-vrio` | comparison frame → SWOT moves → VRIO → positioning → validation |\n| 행동·보상·선택·진척의 코어 루프 | `designing-game-core-loops` | moment / session / meta loop → economy → variation → test |\n| Why→How→What 기획 필연성·기능/모드 명세 | `writing-traceable-game-design-rationales` | issue → strategy → traceability → rules → necessity review |\n| 여러 게임 기획 단계 또는 DDD·벤치마크·플레이어 증거 해석 | `analyzing-and-refining-game-concepts` | frame → focused specialist handoffs / conditional evidence analysis → test → recalibration → production gate |
| 프로젝트 코어 식별·코어/MVP 경계 | `identifying-project-core` | `inventory` / `extract-candidates` / `dependency-map` / `removal-and-change-test` / `classify` / `core-report` |
| PLAN 단계 프로젝트 코어 확정 | `establishing-project-core` | `propose` / `stress-test` / `confirm` / `lock` / `reopen` |
| 적대적 검토·비판 검증·개선·회귀 | `running-adversarial-review-and-refinement` | `attack` / `validate-critique` / `refine-approved-findings` / `regression-recheck` / `decision-report` |
| 경쟁작·플레이어 반응·행동 근거 | `governing-game-user-research-coverage` | evidence coverage를 설치·감사하고, 전략 판단은 `analyzing-game-positioning-with-swot-vrio` 또는 컨셉 PoC로 handoff |\n| 플레이테스트·이벤트·퍼널·A/B | `developing-game-concepts-and-pocs` | PoC 가설·빌드·표본·행동·성공 기준·재조정 판단 |
| Vertical Slice | `designing-vertical-slices` | `slice-contract` / `quality-bar` / `pipeline-proof` / `playtest-evidence` / `decision-gate` |
| 외부 AI 작업 격리 | `orchestrating-deepseek-worktrees` | 대량 초안·분류 위임 |
| 프로젝트 변경 통합 검증 | `reviewing-and-validating-project-changes` | `contract-check` / `external-source-review` / `static-validation` / `runtime-validation` / `regression` / `evidence-report` |
| 접근성 장벽 검수 | `reviewing-and-validating-project-changes` | 핵심 정보·입력·UI·시간·난이도·모션 영향 시 `accessibility-review` |
| 목표 플랫폼 성능 | `reviewing-and-validating-project-changes` | 렌더링·콘텐츠 부하·네트워크·플랫폼 영향 시 `performance-profile` |
| 정본·참조·파생본 최신성 | `auditing-canonical-reference-freshness` | 경로·ID·Schema·정책·생성기·정본 전파 가능성 시 조건부 호출 |
| 아트 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` | 새 아트 방향·생성·편집 프롬프트 |
| Godot·Web UI 아트 감사 | `auditing-and-refining-ui-art` | 실행 결과 A~E 감사·승인된 개선·전후 렌더 재검수 |
| 프로젝트 교훈·BCP 생명주기 | `managing-base-change-proposals` | `extract` / `submit` / `review` / 승인 뒤 `implement` / `verify` |

통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 새 Skill과 Skill Mode로 변환한다. 새 Registry·문서·작업 계약에는 새 ID만 사용한다.

Base 내부에서 `DDD`는 `Digital Dopamine Design`이다. 첫 의미 있는 보상·행동 피드백·보상 사다리·다음 행동·피로를 분석하며 실제 도파민 분비량이나 의학적 중독 진단으로 사용하지 않는다. 외부 자료의 동명 약어는 출처 정의 확인 전 임의 해석하지 않는다.

## 5. 자동 호출 정책

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

사용자는 Skill·Skill Mode를 선언할 필요가 없다. Prompt 의도와 현재 단계에서 Work Mode를 선택하고, Registry trigger가 일치하는 최소 Skill을 자동 선택한다. 같은 요청의 작업 수준·범위·상태를 여러 Skill에서 다시 판정하지 않는다.

- `PLAN`: 요구·근거·설계·정본·실행 순서
- `BUILD`: 승인 범위의 구현·제작·갱신
- `REVIEW`: 적대적 검토·반례·검증·판정
- `decompose-and-sequence`: 승인된 큰 작업·다중 의존성에만 사용
- `reconcile-legacy`: 구형·중복 파일과 stale 파생본이 있을 때 사용
- 외부 근거가 포지셔닝 결정을 바꿀 때: `analyzing-game-positioning-with-swot-vrio`를 사용하고 출처·날짜·버전·표본을 기록한다.
- PoC·플레이테스트·행동·피드백 판정이 필요할 때: `developing-game-concepts-and-pocs`를 사용해 가설·빌드·표본·성공 기준을 고정한다.
- `accessibility-review`·`performance-profile`: 변경 영향과 목표 플랫폼이 있을 때만 사용
- `auditing-canonical-reference-freshness`: 정본 변경 전파 가능성이 있을 때만 사용

L1 이상 작업은 실제 사용한 Work Mode·Skill·Skill Mode, 선택 이유, 수행 내용, 결과·증거·미검증을 보고한다. Skill 파일을 읽은 것과 실제 실행한 것을 구분한다.

## 6. 상세 Reference와 Template

| 질문 | 먼저 읽을 Reference | 출력 Template |
|---|---|---|
| Work Mode·Skill·Skill Mode를 어떻게 고르는가? | `docs/WORK_MODE_AND_SKILL_ROUTING.md` | `templates/project-operations/SKILL_EXECUTION_REPORT.md` |
| 구형 파일을 어떻게 갱신·통합·삭제하는가? | `skills/managing-game-project-operating-system/SKILL.md` | `templates/project-operations/LEGACY_ARTIFACT_RECONCILIATION.md` |
| 작업을 어떤 단계와 순서로 나누는가? | `skills/managing-project-intake-and-work-contract/references/work-decomposition-and-sequencing.md` | `templates/planning/EXECUTION_SEQUENCE_PLAN.md` |
| 어떤 게임·유저 반응을 어떻게 조사하고 반영하는가? | `skills/governing-game-user-research-coverage/SKILL.md`와 필요한 전문 Skill | `templates/planning/GAME_BENCHMARK_PLAYER_EVIDENCE.md` |
| 접근성·성능을 어떤 증거로 검증하는가? | `skills/reviewing-and-validating-project-changes/references/accessibility-and-performance-validation.md` | `templates/quality/PROJECT_CHANGE_VALIDATION.md` |
| 정본 변경이 모두 전파됐는가? | `skills/auditing-canonical-reference-freshness/SKILL.md` | `templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md` |

## 7. 발행 정책

각 문서는 `DESIGN_DOCUMENT_REGISTRY.json`에서 하나의 정책을 선택한다.

| 정책 | 사용 |
|---|---|
| `source_only` | 빠른 운영·라우팅 문서, 원본과 직접 검증만 유지 |
| `milestone_sync` | 주요 게이트·정기 검토·외부 공유 시 PDF·Manifest 동기화 |
| `always_sync` | 원본·승인 이미지·생성기 변경과 같은 작업에서 상시 동기화 |

DOCX·다이어그램은 선언한 경우만 생성한다. `CURRENT`, 자동 렌더, Codex 시각 검수, 사람 시각 검수는 독립 상태다.

## 8. 독립 Method와 호환 문서

독립 개념 책임을 유지하는 Method:

- 작업·제품 게이트: `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`
- 전체 기획·추적성: `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md`
- 콘텐츠·서사·아트·애니메이션 등 분야별 Method
- 조사·근거 평가 Method

다음 기존 Method 경로는 외부 참조 호환성을 위해 유지하되 실행 절차의 최종 원본은 통합 Skill이다.

| 기존 Method | 실행 책임 원본 |
|---|---|
| `GAME_PROJECT_OPERATING_SYSTEM_METHOD.md` | `docs/OPERATING_MODEL.md`, `managing-game-project-operating-system` |
| `EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md` | `managing-game-project-operating-system`의 `audit`·`reconcile-legacy`·`migrate` |
| `DISCIPLINE_PDF_PUBLICATION_METHOD.md` | `managing-design-documents`의 `publish`·`validate` |
| `PROJECT_HANDOFF_CONTEXT_METHOD.md` | `maintaining-project-context-and-handoff` |
| `DISCIPLINE_SKILL_EVOLUTION_METHOD.md` | `evolving-project-discipline-skills` |

## 9. 기존 프로젝트 안전 적용

```text
PLAN: audit only
→ 현행 책임·참조·고유 정보 인벤토리
→ 필요 시 reconcile-legacy 처리표
→ 목표 구조·보존·롤백 제안
→ 사용자 승인
→ BUILD: 승인된 갱신·통합·아카이브·삭제·migrate
→ REVIEW: 보존·참조·발행·복구 대조
→ verify
```

기존 승인 결정·세계관·수치·구현·자산·실패·보류·외부 참조는 조사와 승인 없이 삭제·축약·이동하지 않는다.

## 10. 콜드 스타트와 완료

새 작업자는 저장소만으로 프로젝트 목적, 현재 단계, Work Mode, 보호 범위, 책임 원본, 실제 파일, 자동 선택된 Skill·Skill Mode, 실행 순서, 외부 근거, 플레이테스트, 접근성·성능 검증, 다음 작업과 위험을 찾아야 한다.

완료 보고는 다음을 분리한다.

- 사용한 Work Mode·Skill·Skill Mode와 이유
- 실제 변경
- 얻은 결과·증거
- 실행한 검증
- 실행하지 못한 검증
- 사용자 확인 대기
- 남은 위험·롤백
- 다음 작업·선행 조건

변경 검증은 `reviewing-and-validating-project-changes`로 작업 계약, 실제 diff, 정본·참조, 정적·런타임·접근성·성능·회귀 증거를 연결한다. 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 Skill 호출은 Learning Log에 기록한다. 한 번의 성공은 관찰 또는 가설이며 반복 검증 전에는 공용 강제 규칙으로 승격하지 않는다.

## 구조 최적화·추가 전문 Skill

| 책임 | Skill | 주요 mode |
|---|---|---|
| 무손실 가지치기 | `pruning-stale-and-nonfunctional-material` | `inventory / classify / preserve-unique / prune-approved / verify-no-loss` |
| 본문 간소화 | `simplifying-skill-bodies` | `inventory / extract-references / rewrite-router / validate-disclosure` |
| 동작 보존 리팩토링 | `refactoring-with-contract-preservation` | `baseline-contract / smell-audit / refactor / regression-validate` |
| 로컬·GitHub 동기화 | `synchronizing-local-and-github-state` | `inspect / reconcile / refresh-local / publish-remote / verify-sync` |
| 장기 작업 연속성 | `maintaining-long-running-task-continuity` | `initialize / checkpoint / resume / partial-delivery / close` |
| Games User Research 11영역 | `governing-game-user-research-coverage` | `install / audit / plan-evidence / synthesize / verify-coverage` |
| 사용자 학습 노트 | `creating-user-learning-notes` | `capture / explain / connect / practice / update` |
| 프로젝트 대시보드 | `building-project-visual-dashboards` | `frame / map-sources / build / bind-status / validate` |
| 엔진 런타임 디버깅 | `diagnosing-game-engine-runtime-failures` | `reproduce / isolate / fix-minimally / revalidate / prevent` |

원문 책임 누락 검증: `docs/SKILL_COVERAGE_MAP.md` → `skills/SKILL_COVERAGE.json` → `tools/check_skill_system_coverage.py`.
