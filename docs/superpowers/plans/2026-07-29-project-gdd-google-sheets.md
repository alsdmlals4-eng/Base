# Project GDD Google Sheets Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 프로젝트 Google Sheets를 사용자 중심 시각형 GDD 작업면으로 정의하고 GitHub 정본과의 편집·동기화·AI 참조 계약을 Base 전반에 연결한다.

**Architecture:** 새 광역 Skill을 만들지 않는다. `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`가 공용 정책을 소유하고, 기존 Workbook·tab Template과 Intake·운영체계·문서 Skill이 이를 소비한다. 전용 계약 테스트와 기존 BCA Workflow가 파일 존재가 아니라 실제 라우팅·동기화·시각화·수치화 계약을 검증한다.

**Tech Stack:** Markdown, JSON Registry read contract, Python 3.12 `unittest`, GitHub Actions, GitHub contents API.

## Global Constraints

- Base 자체 Google Sheets 상태는 `BASE_EXCLUDED`다.
- 개별 프로젝트 Google Sheets는 `USER_FACING_GDD_WORKSPACE`다.
- GitHub의 등록된 Markdown·JSON 정본과 실제 코드·데이터·자산·테스트를 Sheet가 대체하지 않는다.
- 사용자의 Sheet 편집은 `PROPOSED_SHEET_CHANGE`로 보존하며 자동 폐기·덮어쓰지 않는다.
- AI는 GitHub와 Sheet를 함께 읽고 차이를 판정한다.
- 긴 텍스트보다 흐름도·관계도·와이어프레임·이미지·수치 표를 우선한다.
- 모호한 수치 표현은 단위·초기 시험값·조정 범위·검증 상태로 바꾼다.
- HTML 대시보드는 명시 요청 또는 기존 유지보수에만 사용한다.
- 핵심 통합 실행 Skill 13개 + 구조·운영·지원 Skill 14개 = 전체 ACTIVE Skill 27개로 표기한다.
- 제품 코드·Scene·Resource·게임 데이터는 변경하지 않는다.

---

### Task 1: RED 계약 테스트

**Files:**
- Create: `tests/test_project_gdd_google_sheets_contract.py`
- Modify: `.github/workflows/validate-bca-visual-sheet-workflow.yml`

**Interfaces:**
- Consumes: 현재 `main`의 문서·Template·Skill 경로.
- Produces: 새 GDD Sheet 정책과 구조 정합성이 없으면 실패하는 `unittest` 계약.

- [ ] **Step 1: 새 정책 파일과 핵심 권한 용어를 요구하는 테스트 작성**

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectGDDGoogleSheetsContractTests(unittest.TestCase):
    def test_policy_defines_gdd_workspace_and_authority(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        for term in (
            "USER_FACING_GDD_WORKSPACE",
            "PROPOSED_SHEET_CHANGE",
            "SHEET_GITHUB_CONFLICT",
            "GitHub 정본을 대체하지 않는다",
            "AI는 GitHub와 Google Sheets를 함께",
        ):
            self.assertIn(term, policy)
```

- [ ] **Step 2: 표준 GDD 6영역·시각화·지속 갱신·수치화를 요구하는 테스트 추가**

```python
    def test_policy_and_templates_cover_visual_living_quantified_gdd(self) -> None:
        policy = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")
        tabs = read("templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md")
        workbook = read("templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md")
        for section in (
            "1. 문서 개요",
            "2. 핵심 게임플레이",
            "3. 게임 시스템",
            "4. 스토리 및 세계관",
            "5. 아트 및 사운드",
            "6. 기술 및 로드맵",
        ):
            self.assertIn(section, policy)
        for term in ("흐름도", "관계도", "와이어프레임", "마지막 수정 시각"):
            self.assertIn(term, policy)
        for term in ("단위", "초기 시험값", "조정 범위", "검증 상태"):
            self.assertIn(term, policy)
        self.assertIn("05_GDD_요약", tabs)
        self.assertIn("15_조작_게임규칙", tabs)
        self.assertIn("USER_FACING_GDD_WORKSPACE", workbook)
```

- [ ] **Step 3: 스킬 수·대시보드 선택 사용·기존 Skill 소비를 요구하는 테스트 추가**

```python
    def test_entrypoints_report_skill_counts_and_optional_dashboard(self) -> None:
        for path in ("README.md", "AGENTS.md", "docs/OPERATING_MODEL.md", "docs/DOCUMENTATION_MAP.md"):
            text = read(path)
            self.assertIn("전체 ACTIVE Skill", text, path)
            self.assertIn("27개", text, path)
            self.assertIn("핵심 통합", text, path)
            self.assertIn("13개", text, path)
            self.assertIn("지원", text, path)
            self.assertIn("14개", text, path)
        for path in ("README.md", "docs/DOCUMENTATION_MAP.md"):
            text = read(path)
            self.assertIn("HTML 대시보드", text, path)
            self.assertIn("명시", text, path)

    def test_existing_skills_consume_project_gdd_sheet(self) -> None:
        for path in (
            "skills/managing-project-intake-and-work-contract/SKILL.md",
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/managing-design-documents/SKILL.md",
        ):
            text = read(path)
            self.assertIn("PROJECT_GDD_GOOGLE_SHEETS_POLICY.md", text, path)
            self.assertIn("PROPOSED_SHEET_CHANGE", text, path)
```

- [ ] **Step 4: 현재 branch에서 RED 실행**

Run: `python -m unittest tests.test_project_gdd_google_sheets_contract -v`

Expected: FAIL because `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md` and required terms do not yet exist.

- [ ] **Step 5: BCA Workflow path와 test command에 새 테스트 연결**

Add these paths:

```yaml
- "docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md"
- "tests/test_project_gdd_google_sheets_contract.py"
```

Add command:

```bash
python -m py_compile tests/test_project_gdd_google_sheets_contract.py
python -m unittest tests.test_project_gdd_google_sheets_contract -v
```

- [ ] **Step 6: Commit**

```bash
git add tests/test_project_gdd_google_sheets_contract.py .github/workflows/validate-bca-visual-sheet-workflow.yml
git commit -m "test: define project GDD Sheets contract"
```

### Task 2: 공용 정책과 Workbook 계약

**Files:**
- Create: `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`
- Modify: `templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md`
- Modify: `templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`
- Modify: `docs/CONFIRMED_DECISION_SYNC_POLICY.md`

**Interfaces:**
- Consumes: Task 1의 용어와 상태 계약.
- Produces: 프로젝트가 설치·동기화할 수 있는 GDD Workbook 정책과 tab schema.

- [ ] **Step 1: `PROJECT_GDD_GOOGLE_SHEETS_POLICY.md` 작성**

필수 Section:

```text
목적·책임 경계
USER_FACING_GDD_WORKSPACE
AI 공동 읽기 순서
PROPOSED_SHEET_CHANGE 처리
표준 GDD 6영역
시각화 우선
지속 갱신
수치화
동기화 상태
설치·검증·실패 조건
```

- [ ] **Step 2: Workbook 상태와 설치 절차 확장**

`PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md`에 다음을 추가한다.

```yaml
workspace_role: USER_FACING_GDD_WORKSPACE
canonical_authority: GITHUB_CANONICAL_AND_ACTUAL_FILES
user_edit_policy: PROPOSED_SHEET_CHANGE
ai_read_policy: GITHUB_AND_SHEET_COMPARE
```

- [ ] **Step 3: 표준 GDD tab과 시각·수치 열 추가**

`PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md`에 `05_GDD_요약`, `15_조작_게임규칙`을 추가한다. `05_GDD_요약`은 6영역의 현재 요약·대표 시각·정본·마지막 수정·동기화 상태를 가진다. `15_조작_게임규칙`은 입력, 조작 방식, 승패, 점수, 페널티, 단위, 초기 시험값, 조정 범위, 검증 상태를 가진다.

- [ ] **Step 4: Sheet 편집 제안과 승인 동기화 정책 연결**

`CONFIRMED_DECISION_SYNC_POLICY.md`에서 Sheet를 단순 mirror가 아니라 사용자 GDD 작업면으로 정의한다. Sheet-only 변경은 `PROPOSED_SHEET_CHANGE`이며 승인 전 정본으로 사용하지 않고, 승인 후 GitHub 정본·Commit·Sheet 재조회로 `SYNCED` 판정한다.

- [ ] **Step 5: 테스트 실행**

Run: `python -m unittest tests.test_project_gdd_google_sheets_contract -v`

Expected: 일부 PASS, 진입점·Skill 연결 항목은 아직 FAIL.

- [ ] **Step 6: Commit**

```bash
git add docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md docs/CONFIRMED_DECISION_SYNC_POLICY.md templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md templates/planning/PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md
git commit -m "docs: add project GDD Sheets policy"
```

### Task 3: 진입점·Skill 라우팅·구조 정합성

**Files:**
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `START_HERE.md`
- Modify: `docs/OPERATING_MODEL.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md`
- Modify: `skills/managing-project-intake-and-work-contract/SKILL.md`
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `skills/managing-design-documents/SKILL.md`

**Interfaces:**
- Consumes: Task 2의 정책 경로·상태명.
- Produces: 새 채팅과 기존 프로젝트 작업에서 GDD Sheet가 실제로 발견·비교되는 라우팅.

- [ ] **Step 1: 활성 Skill 수 표기를 통일**

모든 사람용 진입 문서에 다음 문구를 사용한다.

```text
핵심 통합 실행 Skill 13개 + 구조·운영·지원 Skill 14개 = 전체 ACTIVE Skill 27개
```

Registry가 기계적 권한임을 함께 적는다.

- [ ] **Step 2: HTML 대시보드 선택 사용 경계 추가**

```text
HTML 대시보드는 사용자 명시 요청 또는 기존 대시보드 유지보수에만 사용한다.
일반 프로젝트 기획·상태 확인은 GitHub 정본과 프로젝트 GDD Google Sheets를 우선한다.
```

- [ ] **Step 3: 시작 문서와 Documentation Map에 정책 연결**

`README.md`, `START_HERE.md`, `DOCUMENTATION_MAP.md`에서 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`와 Workbook·tab Template을 한 단계 안에 발견할 수 있게 연결한다.

- [ ] **Step 4: Planning Sequence의 Google Sheets 정의 갱신**

Sheet를 `USER_FACING_GDD_WORKSPACE`로 정의하고 6영역·시각화·수치화·제안 편집 흐름을 Approval Bundle과 연결한다.

- [ ] **Step 5: 기존 Foundation Skill 세 개에 읽기·판정 계약 추가**

각 Skill은 다음을 수행한다.

```text
정확한 Sheet URL·권한 확인
→ GitHub 정본·실제 파일과 Sheet 비교
→ PROPOSED_SHEET_CHANGE 보존
→ 승인 여부 판정
→ 정본·Commit·Sheet 동기화
→ 재조회·SYNCED 또는 BLOCKED_UNVERIFIED
```

- [ ] **Step 6: 테스트 실행**

Run: `python -m unittest tests.test_project_gdd_google_sheets_contract -v`

Expected: PASS.

- [ ] **Step 7: 기존 BCA 계약 테스트 실행**

Run: `python -m unittest tests.test_bca_visual_sheet_workflow -v`

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add README.md AGENTS.md START_HERE.md docs/OPERATING_MODEL.md docs/DOCUMENTATION_MAP.md docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md skills/managing-project-intake-and-work-contract/SKILL.md skills/managing-game-project-operating-system/SKILL.md skills/managing-design-documents/SKILL.md
git commit -m "docs: route project GDD Sheets across Base"
```

### Task 4: 학습·변경 기록·검증

**Files:**
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `docs/CHANGELOG.md`
- Test: `tests/test_project_gdd_google_sheets_contract.py`
- Test: `tests/test_bca_visual_sheet_workflow.py`

**Interfaces:**
- Consumes: Tasks 1-3의 최종 diff.
- Produces: 반복 적용 전 지식 상태·승격 경계와 PR 검증 증거.

- [ ] **Step 1: Learning Log 추가**

다음을 기록한다.

```text
새 광역 Skill을 만들지 않음
Sheet를 GitHub 정본 대체물로 만들지 않음
사용자 편집을 PROPOSED_SHEET_CHANGE로 보존
여러 프로젝트 실제 적용 효과는 Pilot 전까지 OBSERVATION 또는 HYPOTHESIS
```

- [ ] **Step 2: Changelog 추가**

활성 Skill 수 표기 정합성, 선택형 HTML 대시보드, 프로젝트 GDD Sheet 공용 계약을 기록한다.

- [ ] **Step 3: 변경 파일 비교와 정적 계약 실행**

Run:

```bash
python -m py_compile tests/test_project_gdd_google_sheets_contract.py tests/test_bca_visual_sheet_workflow.py
python -m unittest tests.test_project_gdd_google_sheets_contract tests.test_bca_visual_sheet_workflow -v
```

Expected: PASS.

- [ ] **Step 4: Reference Freshness 실행**

Run:

```bash
python tools/check_canonical_reference_freshness.py --config .github/reference-freshness.json --base <main-sha> --head <branch-sha>
```

Expected: PASS or an exact list of missing consumers to fix.

- [ ] **Step 5: GitHub Actions 확인**

Required evidence:

```text
Validate BCA Visual and Sheet Workflow: PASS
Validate Game Project Operating System: PASS
관련 docs·governance checks: PASS 또는 비대상 사유
```

- [ ] **Step 6: Draft PR 생성**

PR title:

```text
프로젝트 Google Sheets를 시각형 GDD 작업면으로 확장
```

- [ ] **Step 7: 완료 보고**

실행한 Work Mode·Skill·Skill Mode, 실제 변경, Actions 결과, 로컬 미실행, 프로젝트별 후속 적용 범위를 구분한다.
