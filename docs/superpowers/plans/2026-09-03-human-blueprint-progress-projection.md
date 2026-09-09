# Human Blueprint Progress Projection Implementation Plan

> 승인된 설계: `docs/superpowers/specs/2026-09-03-human-blueprint-progress-projection-design.md`

**Goal:** 기존 사람용 Blueprint PDF 안에서 프로젝트 목표·시스템 기획·플레이 케이스·현재 작업·검증 증거를 같은 source SHA 기준으로 확인하게 한다.

**Architecture:** 새 PM 정본이나 별도 산출물을 만들지 않고 repository owner, AI production spec, `project_work_kanban`, evidence를 읽어 검증 가능한 Markdown projection으로 만든다. V4 machine contract가 contract/template/validator를 라우팅하며, 프로젝트 PDF 생성기는 이 projection을 기존 `HUMAN_MASTER_GDD_PDF` 안에 포함한다.

**Tech Stack:** Markdown, JSON, Python 표준 라이브러리, `unittest`, GitHub Actions.

---

## Task 1. 계약 회귀 테스트를 RED로 추가

**Files:**
- Create: `tests/test_human_blueprint_progress_projection.py`

1. V4 contract route, contract/template 존재, 필수 token을 검사한다.
2. valid projection, source mismatch, 미해소 참조, evidence 없는 PASS, N/A reason 누락을 테스트한다.
3. Markdown projection이 목표·시스템·케이스·작업 섹션과 정확한 분모를 표시하는지 테스트한다.
4. 구현 전 exact test가 실패하는 것을 PR CI에서 확인한다.

## Task 2. 사람용 Blueprint projection contract와 template 추가

**Files:**
- Create: `docs/operations/project-workspace/HUMAN_BLUEPRINT_PROGRESS_PROJECTION_CONTRACT.md`
- Create: `templates/project-operations/HUMAN_BLUEPRINT_PROGRESS_PROJECTION_TEMPLATE.md`

1. 두 산출물 정책과 repository-first 권한을 보존한다.
2. 별도 HTML·PM PDF·상태 저장소를 금지한다.
3. Project dashboard, goal card, system card, case matrix, traceability를 정의한다.
4. 성숙도·작업·evidence 축과 진행률 계산을 분리한다.
5. source SHA, stale snapshot, N/A, evidence ceiling 규칙을 정의한다.

## Task 3. projection validator와 renderer 구현

**Files:**
- Create: `tools/human_blueprint_progress_projection.py`

1. unique ID와 cross-reference를 검증한다.
2. source SHA와 metadata를 검증한다.
3. 상태·필수 evidence·PASS evidence·blocker/recovery를 검증한다.
4. 목표·시스템·케이스·작업 완료 수를 평균 없이 계산한다.
5. PDF source용 Markdown을 렌더한다.
6. 입력 URL·명령·HTML을 실행하지 않는다.

## Task 4. V4 machine contract에 route 추가

**Files:**
- Modify: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`

1. contract/template/validator 경로를 등록한다.
2. 필수 ID, 섹션, source, progress rule을 기계 계약에 추가한다.
3. human PDF metadata에 work-status snapshot 항목을 추가한다.
4. 기존 authority, Blueprint pass, Notion migration, asset invariant를 보존한다.

## Task 5. 검증과 교정

1. Targeted unittest를 실행한다.
2. 전체 `run_local_validation.py` 또는 동등한 exact-head GitHub Actions를 실행한다.
3. `CREATIVE → STRUCTURAL → RULE → CONTINUITY → ADVERSARIAL → POLISH` 관점으로 최소 5회 전체 검토한다.
4. 유효 finding을 수정하고 영향받는 테스트를 다시 실행한다.
5. PR diff, exact HEAD, CI, thread 0, mergeability를 확인한다.
6. 정상 squash merge 후 merged main exact SHA에서 contract/tool/test route를 readback한다.

## 완료 기준

- 별도 HTML 0, 별도 PM PDF 0, 새 상태 정본 0
- contract/template/validator/V4 route 존재
- 목표·시스템·케이스·작업 ID 참조 오류 0
- PASS 없는 완료 계산 0, N/A 분모 포함 0, 자식 퍼센트 평균 0
- maturity/work/evidence 상태 혼합 0
- source mismatch 은폐 0
- targeted/full CI 실패 0
- 적대 검토의 열린 MUST_FIX 0
- merged-main readback 완료
