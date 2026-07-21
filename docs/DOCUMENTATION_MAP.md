# Base 문서·스킬 역할표

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** 작업 원칙, Skill, Template, Test와 일반화된 Case를 관리한다. 프로젝트의 세계관, 실제 수치, 구현 상태, 파일 경로, 승인 이미지와 테스트 결과는 프로젝트 저장소가 책임진다.

## 1. 최초 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업의 Skill·Template·Test·Case
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
→ 현재 요청에 필요한 통합 Skill과 mode
→ Roadmap·Issue·Plan
→ 실제 코드·데이터·자산·테스트
```

저장소 전체나 전체 스킬을 무작정 읽지 않는다. 백업·보류·제거 후보는 감사·재개 요청이 없는 한 기본 읽기에서 제외한다.

Base 저장소 자체의 콜드 스타트에서는 프로젝트 설치 템플릿을 활성 상태 문서로 오인하지 않는다. 완료 상태는 `docs/CHANGELOG.md`, 검토 대기 작업은 `[수정제안서]/PROPOSAL_REGISTRY.json`, 진행 중 구현은 GitHub PR·Actions가 책임진다. 활성 인터뷰가 없으면 `등록 없음`으로 명시한다.

## 2. 공용 책임 원본

| 구분 | 파일 | 책임 |
|---|---|---|
| 최초 라우터 | `START_HERE.md` | 요청 유형별 최소 읽기와 실행 Skill 연결 |
| 항상 적용 규칙 | `AGENTS.md` | 우선순위·보안·승인·완료 보고 금지 규칙 |
| 통합 운영 모델 | `docs/OPERATING_MODEL.md` | 공용 작업 생명주기·책임 원본·상태·발행 정책의 단일 설명 원본 |
| 저장소 개요 | `README.md` | 사용 목적·구조·활성 스킬 안내 |
| 문서·스킬 지도 | `docs/DOCUMENTATION_MAP.md` | 질문별 책임 원본과 최소 읽기 |
| Base Skill Registry | `skills/SKILL_REGISTRY.json` | 활성 Skill trigger·상태·경로 |
| 이전 ID 별칭 | `skills/LEGACY_SKILL_ALIASES.md` | 통합 전 Skill ID를 새 Skill mode로 연결 |
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
스킬 선택·상태 → SKILL_REGISTRY.json
반복 절차 → Skill
실제 상태 → 코드·데이터·자산·테스트·캡처
사람용 발행 → Registry 정책이 요구하는 PDF·선택 DOCX·assets
발행 최신성 → Publication Manifest
과거 상태 → Git 이력
```

한 질문에는 현행 책임 원본 하나만 둔다. 같은 서술을 Markdown과 JSON 양쪽에 독립 원본으로 유지하지 않는다.

## 4. 활성 실행 스킬

| 작업 | Skill | Mode 또는 호출 조건 |
|---|---|---|
| 요청 라우팅·사실 조사·사용자 확인·실행 계약 | `managing-project-intake-and-work-contract` | `route` → 필요 시 `clarify` → `contract` |
| 운영체계 신규 설치·기존 감사·마이그레이션·Health Review | `managing-game-project-operating-system` | `install` / `audit` / `migrate` / `verify` |
| 기획 책임 원본 작성·구조 변경·발행·검수 | `managing-design-documents` | `author` / `update` / `restructure` / `publish` / `validate` |
| 분야별 스킬 생성·통합·학습 | `evolving-project-discipline-skills` | 스킬 추가·중복·반복 실패·Registry 변경 |
| Active Context·Handoff | `maintaining-project-context-and-handoff` | 상태·다음 작업·게이트·위험 변경 |
| 프로젝트 교훈·BCP 생명주기 | `managing-base-change-proposals` | `extract` / `submit` / `review` / 승인 뒤 `implement` / `verify` |
| Vertical Slice | `designing-vertical-slices` | 대표 품질·제작 파이프라인 검증 |
| 외부 AI 작업 격리 | `orchestrating-deepseek-worktrees` | 대량 초안·분류 위임 |
| 외부 AI 결과 검수 | `reviewing-external-ai-drafts` | 외부 AI 결과 실제 반영 전 |
| 아트 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` | 새 아트 방향·생성·편집 프롬프트 |
| Godot·Web UI 아트 감사 | `auditing-and-refining-ui-art` | 실행 결과 A~E 감사·승인된 개선·전후 렌더 재검수 |

통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 새 Skill과 mode로 변환한다. 새 Registry·문서·작업 계약에는 새 ID만 사용한다.

## 5. 선택적 호출 정책

```json
{
  "load_all_skills": false,
  "default_selection": "none",
  "require_trigger_match": true,
  "max_primary_discipline_skills": 1,
  "max_foundation_skills": 3
}
```

같은 요청의 작업 수준·범위·상태를 여러 Skill에서 다시 판정하지 않는다. 통합 Skill 내부 mode는 하나의 조사 결과와 상태를 재사용한다. 검증·발행·Handoff는 해당 단계에서만 실행한다.

## 6. 발행 정책

각 문서는 `DESIGN_DOCUMENT_REGISTRY.json`에서 하나의 정책을 선택한다.

| 정책 | 사용 |
|---|---|
| `source_only` | 빠른 운영·라우팅 문서, 원본과 직접 검증만 유지 |
| `milestone_sync` | 주요 게이트·정기 검토·외부 공유 시 PDF·Manifest 동기화 |
| `always_sync` | 원본·승인 이미지·생성기 변경과 같은 작업에서 상시 동기화 |

DOCX·다이어그램은 선언한 경우만 생성한다. `CURRENT`, 자동 렌더, Codex 시각 검수, 사람 시각 검수는 독립 상태다.

## 7. 독립 Method와 호환 문서

독립 개념 책임을 유지하는 Method:

- 작업·제품 게이트: `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`
- 전체 기획·추적성: `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md`
- 콘텐츠·서사·아트·애니메이션 등 분야별 Method
- 조사·근거 평가 Method

다음 기존 Method 경로는 외부 참조 호환성을 위해 유지하되 실행 절차의 최종 원본은 통합 Skill이다.

| 기존 Method | 실행 책임 원본 |
|---|---|
| `GAME_PROJECT_OPERATING_SYSTEM_METHOD.md` | `docs/OPERATING_MODEL.md`, `managing-game-project-operating-system` |
| `EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md` | `managing-game-project-operating-system`의 `audit`·`migrate` |
| `DISCIPLINE_PDF_PUBLICATION_METHOD.md` | `managing-design-documents`의 `publish`·`validate` |
| `PROJECT_HANDOFF_CONTEXT_METHOD.md` | `maintaining-project-context-and-handoff` |
| `DISCIPLINE_SKILL_EVOLUTION_METHOD.md` | `evolving-project-discipline-skills` |

## 8. 기존 프로젝트 안전 적용

```text
Audit only
→ 현행 책임·참조·고유 정보 인벤토리
→ 목표 구조·보존·롤백 제안
→ 사용자 승인
→ 승인된 처리표만 migrate
→ 보존·참조·발행 대조
→ verify
```

기존 승인 결정·세계관·수치·구현·자산·실패·보류·외부 참조는 조사와 승인 없이 삭제·축약·이동하지 않는다.

## 9. 콜드 스타트와 완료

새 작업자는 저장소만으로 프로젝트 목적, 현재 단계, 보호 범위, 책임 원본, 실제 파일, 필요한 Skill, 검증, 다음 작업과 위험을 찾아야 한다.

완료 보고는 다음을 분리한다.

- 실제 변경
- 실행한 검증
- 실행하지 못한 검증
- 사용자 확인 대기
- 남은 위험·롤백
- 다음 작업·선행 조건

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 Skill 호출은 Learning Log에 기록한다. 한 번의 성공은 관찰 또는 가설이며 반복 검증 전에는 공용 강제 규칙으로 승격하지 않는다.
