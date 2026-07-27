# Confirmed Decision Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 승인된 기획 결정을 즉시 GitHub 정본·`main`·프로젝트 Google Sheets에 동기화하고, 중복 질문과 PR 누적을 막으며, 모든 병합 뒤 정본 충돌을 적대적으로 재검사하는 공용 운영 계약을 추가한다.

**Architecture:** `docs/CONFIRMED_DECISION_SYNC_POLICY.md`를 공용 단일 정책 원본으로 두고, 프로젝트에는 `CURRENT_CONFIRMED_DECISIONS.md` 템플릿을 설치한다. 기존 Intake/Grill Me와 적대적 검토 Skill은 새 정책을 참조하며, 질문·승인 기록은 하나의 활성 GitHub 추적 surface를 재사용하고 구현 PR은 기존 생명주기 정책을 따른다.

**Tech Stack:** Markdown policy and templates, GitHub Branch/PR/Actions, Google Sheets connector contract

## Global Constraints

- 승인된 기획 결정은 임시 누적하지 않고 같은 승인 단위에서 정본·`main`·Google Sheets에 반영한다.
- 코드·데이터 Schema·Scene·Workflow·대규모 구조 변경은 직접 `main` 반영 대상이 아니며 구현 PR을 사용한다.
- 질문 전 최신 `main`, 열린 PR, 최근 병합 PR, 현재 확정 결정, 분야 정본, Google Sheets를 비교한다.
- 기술적 세부와 초기 튜닝값은 `RECOMMENDED_DEFAULT`로 처리하며, 프로젝트 코어·중요 기획·방향성·정본 충돌만 사용자에게 묻는다.
- 병합된 PR은 기록으로 보존하고 안전 조건을 만족한 head branch는 삭제한다.
- 모든 병합 뒤 적대적 검토와 회귀 재검사를 수행하고 미검증을 성공으로 표시하지 않는다.

---

### Task 1: Confirmed decision synchronization policy

**Files:**
- Create: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`

**Interfaces:**
- Consumes: `docs/OPERATING_MODEL.md`, `docs/GITHUB_WORK_ITEM_LIFECYCLE_POLICY.md`, `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- Produces: 질문 전 대조, 승인 즉시 3중 동기화, 사용자 결정 분류, 동기화 상태, 오류 처리, 병합 후 검토 계약

- [x] **Step 1:** 공용 정책에 책임·우선순위·상태·정상 흐름·실패 흐름을 작성한다.
- [x] **Step 2:** GitHub 댓글은 추적 증거, `CURRENT_CONFIRMED_DECISIONS.md`는 승인 결정 복원 원본, 분야 문서는 상세 규칙 원본, Sheets는 동기화 작업면으로 구분한다.
- [x] **Step 3:** 문서 승인 직접 `main` 반영과 구현 PR 범위를 분리한다.
- [x] **Step 4:** 승인 후 GitHub와 Sheets를 재조회해 `SYNCED`를 판정하도록 한다.

### Task 2: Project recovery canonical template

**Files:**
- Create: `templates/project-operations/CURRENT_CONFIRMED_DECISIONS.md`

**Interfaces:**
- Consumes: 승인된 Decision ID, 분야 책임 원본 경로, commit SHA, Sheet row
- Produces: 새 채팅에서 한 파일로 현재 확정 사항과 동기화 상태를 복원하는 프로젝트 템플릿

- [x] **Step 1:** 프로젝트 약속·코어·보호 결정·현재 Decision 표·대체 관계·미결정·동기화 상태를 포함한다.
- [x] **Step 2:** 상세 규칙 전문을 복제하지 않고 책임 원본 경로를 연결한다.
- [x] **Step 3:** 마지막 GitHub main HEAD와 Sheet sync 정보를 기록한다.

### Task 3: Grill Me duplicate-question and immediate-sync enforcement

**Files:**
- Modify: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`
- Modify: `templates/project-operations/GRILL_ME_DECISION_RECORD.md`

**Interfaces:**
- Consumes: current main, current decisions, domain canon, active/recent PRs, Sheet state
- Produces: 중복 제거된 질문 하나와 승인 후 `SYNCED` 증거

- [x] **Step 1:** 질문 전 대조 순서를 명문화한다.
- [x] **Step 2:** `RECOMMENDED_DEFAULT`와 `USER_DECISION_REQUIRED` 분류를 추가한다.
- [x] **Step 3:** 질문·승인 댓글, 정본·main·Sheet 갱신, 재조회, 실패 시 중단을 추가한다.
- [x] **Step 4:** Decision Record에 정본 비교·PR·Sheet·sync 상태를 기록한다.

### Task 4: Post-merge adversarial review

**Files:**
- Modify: `skills/running-adversarial-review-and-refinement/SKILL.md`
- Create: `templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md`

**Interfaces:**
- Consumes: merged PR diff, new main HEAD, current decisions, domain canon, Sheet state, validation evidence
- Produces: `NO_CONFLICT / CONFLICT_FIXED / USER_DECISION_REQUIRED / BLOCKED_UNVERIFIED`

- [x] **Step 1:** 병합 후 공격 렌즈에 최근 승인 누락, 정본 충돌, Sheet 불일치, 범위 외 변경, 중복 구현, 회귀를 추가한다.
- [x] **Step 2:** 비판 검증 뒤 최소 수정과 재검사를 분리한다.
- [x] **Step 3:** 표준 보고 템플릿을 추가한다.

### Task 5: Integration verification

**Files:**
- Review: all changed files
- Validate: repository Actions and reference freshness

**Interfaces:**
- Consumes: branch HEAD and PR diff
- Produces: merge decision and post-merge conflict report

- [x] **Step 1:** 동일 책임의 기존 정책·열린 PR과 중복 여부를 확인한다.
- [ ] **Step 2:** PR을 생성하고 `Validate Game Project Operating System` 결과를 확인한다.
- [ ] **Step 3:** Squash merge한다.
- [ ] **Step 4:** 새 main을 기준으로 정본·PR·템플릿·Skill·Sheets 계약을 적대적으로 재검사한다.
- [ ] **Step 5:** branch 자동 삭제 여부를 확인하고 확인하지 못하면 `UNVERIFIED_REPOSITORY_SETTING`으로 보고한다.

## Verification findings resolved before merge

- `MUST_FIX`: 기존 `managing-design-documents`의 checkpoint 지연 승격이 승인 즉시 정본화 정책과 충돌했다. 즉시 정본화 후 checkpoint 감사 방식으로 교체했다.
- `MUST_FIX`: Skill 본문 변경에 필요한 Registry·Learning Log·집중 회귀 테스트 동기화가 최초 CI에서 누락됐다. 같은 PR에 보완했다.
- `MUST_FIX`: 새 정책과 템플릿이 Documentation Map·프로젝트 설치 키트·Changelog에서 발견되지 않았다. 활성 진입점과 설치 목록에 연결했다.
- `MUST_FIX`: 적대적 검토 본문과 상세 reference의 finding 상태명이 달랐다. `USER_DECISION_REQUIRED`, `REJECTED_CRITIQUE`, `BLOCKED_UNVERIFIED`로 정렬했다.
- `MUST_FIX`: 기존 회귀 검사가 요구하는 호환 문구 세 개와 compact Skill 150줄 제한을 확인했다. 기능을 바꾸지 않고 호환 표기와 1줄 초과를 수정했다.
- `REJECTED_CRITIQUE`: 과거 Learning Log의 checkpoint 기반 기록은 역사 증거이므로 삭제하지 않는다. 2026-07-28 최신 학습 항목과 현행 정책이 현재 권한을 가진다.
- `NOT_APPLICABLE`: Base 저장소에는 이 작업에서 동기화할 프로젝트 Google Sheets 주소가 없다. 프로젝트 적용 시 Connector 재조회까지 필수다.
