# Base Shared Skill Project Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Base의 공용 Skill route와 Godot 에셋 우선 탐색 정책을 네 프로젝트의 기존 운영체계 정본에 일관되게 연결한다.

**Architecture:** Base는 공용 Skill 본문과 route 계약의 단일 원본을 유지한다. 각 프로젝트는 고정 Base SHA, route Registry, 프로젝트 어댑터, 프로젝트 고유 Skill Registry를 분리하며 Documentation Map과 검증기가 이 연결을 확인하도록 한다.

**Tech Stack:** Markdown, JSON, Python 검증 스크립트, GitHub repositories.

## Global Constraints

- Base 공용 Skill 본문을 프로젝트에 복사하지 않는다.
- 프로젝트 전용 Skill만 프로젝트 내부에서 생성·관리한다.
- 게임 코드·Scene·데이터·자산은 수정하지 않는다.
- 모든 route와 adapter는 Base commit `5c95c8cc4434acc2505957d3ea2385064da99143`을 가리킨다.
- 존재하지 않는 자동 검증 명령을 추가하지 않는다.
- 실제 실행하지 못한 Godot·Android·플레이테스트 검증은 `UNVERIFIED`로 남긴다.

---

### Task 1: Base 기준과 프로젝트 현황 감사

**Files:**
- Read: `skills/BASE_SHARED_SKILL_ROUTES.json`
- Read: `docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md`
- Read per project: `AGENTS.md`, `docs/BASE_RULES_VERSION.md`, Documentation Map, primary Skill Registry, shared route, project adapter

**Interfaces:**
- Consumes: Base shared route registry and adapter contract
- Produces: per-project exact modification list

- [ ] **Step 1:** 각 프로젝트의 현재 Base SHA와 Registry 경로를 확인한다.
- [ ] **Step 2:** 새 route·adapter 파일의 Base SHA와 역할 바인딩을 확인한다.
- [ ] **Step 3:** 기존 운영 문서에서 갱신이 필요한 참조만 목록화한다.

### Task 2: 프로젝트 운영체계 정본 동기화

**Files:**
- Modify per project: `docs/BASE_RULES_VERSION.md`
- Modify per project: primary Skill Registry
- Modify per project: Documentation Map
- Modify only when present and necessary: `AGENTS.md`, `START_HERE.md`

**Interfaces:**
- Consumes: `skills/BASE_SHARED_SKILL_ROUTES.json`, `skills/PROJECT_BASE_SKILL_ADAPTER.json`
- Produces: discoverable and version-consistent shared Skill integration

- [ ] **Step 1:** Base SHA를 `5c95c8cc4434acc2505957d3ea2385064da99143`으로 갱신하고 변경 범위를 설명한다.
- [ ] **Step 2:** primary Skill Registry에서 shared route registry와 adapter 경로를 노출한다.
- [ ] **Step 3:** Documentation Map에 공용 route·adapter와 제3자 자산 기록 문서를 등록한다.
- [ ] **Step 4:** 프로젝트 고유 Skill 목록에는 Base 공용 Skill을 복제해 추가하지 않는다.

### Task 3: 검증기 갱신

**Files:**
- Modify only existing validators under each repository `tools/` or `tests/`

**Interfaces:**
- Consumes: project route registry and adapter JSON
- Produces: checks for file existence, matching Base SHA, required routes, and local skill policy

- [ ] **Step 1:** 기존 검증기가 route·adapter 구조를 검사하는지 확인한다.
- [ ] **Step 2:** 누락된 경우 최소 검사를 추가한다: JSON parse, required files, matching Base SHA, two required route IDs, duplicate body prohibition.
- [ ] **Step 3:** 기존 프로젝트 제품 검증과 운영체계 검증을 혼합하지 않는다.

### Task 4: 증거 확인과 보고

**Files:**
- Read modified files and commit metadata

**Interfaces:**
- Consumes: committed repository state
- Produces: PASS/PARTIAL/UNVERIFIED evidence report

- [ ] **Step 1:** GitHub에서 수정 파일을 다시 읽어 JSON 구조와 SHA를 확인한다.
- [ ] **Step 2:** 실행 가능한 GitHub 상태·정적 검증 결과를 확인한다.
- [ ] **Step 3:** 로컬 실행이 불가능한 Godot·Android·Python 검증은 완료로 주장하지 않고 별도로 기록한다.
