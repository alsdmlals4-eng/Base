# BCA Visual Planning and Project Sheet Rollout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base와 5개 진행 프로젝트에 B(프로젝트 Google Sheets 구조) → C(GPT 이미지 생성·검수 실행 흐름) → A(Base 공용 정책·Skill·라우팅) 순서의 운영 계약을 설치하고 통합 실행문 v8로 승계한다.

**Architecture:** Base는 공용 정책·Template·Skill mode·검증 계약의 단일 원본이다. 각 프로젝트는 공용 Skill 본문을 복제하지 않고 프로젝트 Sheet 계약, 이미지 생성·검수 기록, Base v8 참조와 프로젝트별 정본 연결만 설치한다. 실제 Google Sheet URL이 확인되지 않은 프로젝트는 중복 생성을 막기 위해 `NOT_CONFIGURED`로 유지한다.

**Tech Stack:** Markdown, JSON Skill Registry, GitHub Actions, Python unittest, GitHub PR/Actions.

## Global Constraints

- Base 저장소는 `BASE_EXCLUDED`이며 프로젝트 Sheet를 직접 만들지 않는다.
- 정확한 기존 Sheet URL이 없는 프로젝트는 `NOT_CONFIGURED`로 기록한다.
- GPT는 기획 중 시각화와 기획 종료 시 실사용 후보 이미지·목업을 생성할 수 있다.
- 생성 이미지는 자동 최종 자산이 아니며 검수·승인·원장 반영을 거쳐야 한다.
- 기존 프로젝트 코어·정본·제품 경로는 이 문서 작업에서 변경하지 않는다.
- 모든 단계는 `repository-wide-audit`와 reference-freshness를 거친다.

---

### Task 1: Base Sheet Workbook Contract

**Files:**
- Modify: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- Modify: `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`
- Create: `templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md`

- [ ] 필수 탭에 세계관, 핵심루프, 주요인물, 조연·세력·관계, 핵심시스템·메인콘텐츠, 이미지 기획, 이미지 검수·승인을 추가한다.
- [ ] 각 탭의 공통 열과 분야별 열을 정의한다.
- [ ] `PROJECT_SHEET_CONFIGURED / NOT_CONFIGURED / BASE_EXCLUDED` 상태를 보존한다.
- [ ] Sheet URL이 없는 프로젝트에서 자동 신규 Sheet를 만들지 않는 중복 방지 조건을 추가한다.

### Task 2: GPT Image Generation and Review Workflow

**Files:**
- Create: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Modify: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- Create: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`

- [ ] `planning-visualization`, `final-visual-candidate`, `visual-qa-and-approval` mode를 정의한다.
- [ ] `PLANNED → GENERATED_EXPLORATION → IN_REVIEW → REVISION_REQUIRED → APPROVED_CANDIDATE → PROJECT_ASSET_APPROVED` 상태를 정의한다.
- [ ] 기획 일치성, 실제 화면 가독성, 구현 가능성, 재사용성, 권리·유사성, 출처·프롬프트·모델 기록을 검수한다.
- [ ] 승인된 이미지만 정본·Sheet·자산 원장에 반영한다.

### Task 3: Base Policy and Integrated Prompt v8

**Files:**
- Create: `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`
- Modify: `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md`
- Create: `docs/knowledge/VERTICAL_SLICE_V7_TO_V8_MIGRATION.md`
- Modify: `START_HERE.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `templates/project-operations/README.md`
- Modify: `skills/SKILL_REGISTRY.json`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `.github/reference-freshness.json`

- [ ] v7의 상세 계약을 무손실 승계한다.
- [ ] BCA 순서와 새 Sheet·이미지 계약을 v8에 추가한다.
- [ ] v7을 `SUPERSEDED_COMPATIBILITY`로 표시한다.
- [ ] 활성 진입점·Registry·Reference Freshness 소비처를 v8로 전환한다.

### Task 4: Base Regression and Adversarial Review

**Files:**
- Create: `tests/test_bca_visual_sheet_workflow.py`
- Create: `.github/workflows/validate-bca-visual-sheet-workflow.yml`

- [ ] v8 정본, v7 대체 표기, 필수 Sheet 탭, 이미지 상태·검수 계약, Registry trigger를 테스트한다.
- [ ] tracked-file inventory와 구형 v7 활성 참조 후보를 Artifact로 남긴다.
- [ ] Base 전체 CI와 전용 CI를 통과한다.
- [ ] PR 병합 후 새 main에서 재검사한다.

### Task 5: Five Project Adapters

**Repositories:**
- `Ten-Paces-Hidden-Moves`
- `Blacksmith`
- `omenward`
- `urban-legend`
- `Spell`

**Files per project:**
- Create: project-local Sheet workbook contract
- Create: project-local GPT image generation and review workflow
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: local Skill Registry or Base integration route when present
- Modify: Documentation Map or START_HERE when present
- Create: project-specific regression test or audit record when practical

- [ ] 프로젝트 코어·현재 Gate·기존 문서 구조를 보존한다.
- [ ] Base v8 merged SHA를 고정한다.
- [ ] 프로젝트별 필수 탭의 실제 책임 원본을 매핑한다.
- [ ] 기획 중 이미지와 기획 종료 이미지의 우선 생성 목록을 프로젝트 특성에 맞춰 기록한다.
- [ ] 정확한 Sheet URL이 없으므로 `NOT_CONFIGURED`로 기록한다.
- [ ] 프로젝트별 적대적 검토와 CI를 통과한 뒤 Squash 병합한다.
