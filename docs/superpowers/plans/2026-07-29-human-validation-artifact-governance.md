# Human Validation Artifact Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 작은 표본의 저충실도 사람 검증 Artifact가 실제 제품 성능이나 통계적 확증으로 과장되지 않도록 Base 공용 Governance·Template·회귀 테스트를 추가하고, 다섯 프로젝트 Pilot 문서를 동일 기준으로 교정한다.

**Architecture:** 기존 `governing-game-user-research-coverage` Skill이 실행 권한을 유지한다. 공용 원리는 `docs/knowledge/game-development/`에 두고, 기존 GUR 11영역 Reference가 조건부로 라우팅한다. 실행 양식은 `templates/research/`가 책임지며 프로젝트 고유 시나리오·ID·수치는 각 저장소에 남긴다.

**Tech Stack:** Markdown 계약, Python `unittest`, GitHub branch/PR/Actions.

## Global Constraints

- 새 GUR 광역 Skill을 만들지 않는다.
- 작은 표본 비율을 통계적 일반화나 자동 `ADOPT` 판정으로 사용하지 않는다.
- 행동 관찰, 자기보고, 진행자 개입, 시스템·Artifact 로그를 분리한다.
- simulated·scripted·fixed Artifact는 실제 알고리즘 정확도·확률·성능을 주장하지 않는다.
- 최초 시도와 피드백 후 수정 시도를 분리한다.
- 제품 코드·Scene·Resource·밸런스·정본 변경 권한은 프로젝트별 별도 승인으로 유지한다.
- 사람 세션을 실행하지 않은 상태는 `NOT_RUN`으로 유지한다.

---

### Task 1: 공용 Governance와 GUR 라우팅

**Files:**
- Create: `docs/knowledge/game-development/HUMAN_VALIDATION_ARTIFACT_GOVERNANCE.md`
- Modify: `skills/governing-game-user-research-coverage/references/eleven-domain-coverage.md`

- [x] `artifact_fidelity`, `claim_ceiling`, simulated/scripted/fixed component 계약을 정의한다.
- [x] `first_attempt`, `post_feedback_attempt`, 행동·자기보고·진행자 개입·로그를 분리한다.
- [x] `PROMISING_DIRECTION / ADAPT / REWORK / REJECT / STOP`을 작은 표본 판정으로 정의한다.
- [x] GUR 11영역 Reference에서 Governance와 Template을 조건부 라우팅한다.
- [x] Skill package 내부 고아 Reference를 만들지 않는다.

### Task 2: 공용 Session Packet Template

**Files:**
- Create: `templates/research/HUMAN_VALIDATION_SESSION_PACKET.md`

- [x] 기준선·보호 경계·Artifact fidelity·claim ceiling을 기록한다.
- [x] 프로젝트마다 같은 표본 수를 강제하지 않는다.
- [x] 행동·자기보고·진행자 개입·로그를 별도 필드로 둔다.
- [x] 최초 시도와 교정 후 시도를 별도 필드로 둔다.
- [x] 반복 결함·반례·경험군 차이·미실행 검증을 우선하는 판정표를 둔다.
- [x] 익명화와 실제 세션 뒤 보고서 저장 계약을 정의한다.

### Task 3: 계약 테스트와 Workflow 연결

**Files:**
- Create: `tests/test_human_validation_artifact_governance.py`
- Modify: `tests/test_evidence_knowledge_workflow_contract.py`
- Modify: `.github/workflows/validate-evidence-knowledge.yml`

- [x] Governance·Template·GUR 라우팅·중복 Skill 금지를 검사한다.
- [x] 새 테스트를 Evidence Workflow의 compile·unittest·artifact 목록에 직접 연결한다.
- [x] 전용 Workflow와 저장소 전체 운영체계 Workflow에서 실행한다.

### Task 4: Base PR 검증·병합

**Files:**
- Review: `main...gpt/human-validation-artifact-governance-20260729`

- [ ] 변경 파일이 Governance·Template·GUR Reference·계획·테스트·Workflow로 제한되는지 확인한다.
- [ ] Evidence Workflow와 전체 운영체계 Required Checks를 통과시킨다.
- [ ] 미해결 리뷰 스레드와 mergeability를 확인한다.
- [ ] expected HEAD 고정으로 squash merge한다.
- [ ] Base `main`에서 Governance와 Template을 재조회한다.

### Task 5: 다섯 프로젝트 계획 교정

**Files:**
- Modify: 십보강호 `docs/superpowers/plans/2026-07-29-enemy-intent-human-validation-artifact.md`
- Modify: Blacksmith `docs/superpowers/plans/2026-07-29-plus5-plus10-human-validation-artifact.md`
- Modify: OMENWARD `docs/superpowers/plans/2026-07-29-roulette-agency-validation-artifact.md`
- Modify: 괴이기록국 `docs/superpowers/plans/2026-07-29-hypothesis-board-human-validation-artifact.md`
- Modify: GRIMOIRE `docs/superpowers/plans/2026-07-29-magic-writing-input-validation-artifact.md`

- [ ] 모든 프로젝트의 자동 `ADOPT` 표현을 `PROMISING_DIRECTION` 중심으로 낮춘다.
- [ ] 십보강호에 fixture/seed 없는 실제 전투 인과 주장 금지와 카드 이해/전투 인과 분리를 추가한다.
- [ ] Blacksmith에 표준 scripted 실패 결과와 실제 선택/결과 회상 분리를 추가한다.
- [ ] OMENWARD에 동일 구조의 유리/불리 RNG 결과 교차 배정을 추가한다.
- [ ] 괴이기록국에 최초 연결과 피드백 후 수정 연결을 분리한다.
- [ ] GRIMOIRE에서 실제 인식률 지표를 제거하고 simulated recognition UX 책임만 판정한다.

### Task 6: 프로젝트별 PR 검증·병합

- [ ] 프로젝트별 제품 경로 비침범을 확인한다.
- [ ] 자동 CI가 있는 네 저장소의 Required Checks를 확인한다.
- [ ] GRIMOIRE는 자동 Actions 부재를 수동 검증 증거로 기록한다.
- [ ] 미해결 리뷰 스레드와 mergeability를 확인한다.
- [ ] 각 PR을 expected HEAD 고정으로 squash merge한다.
- [ ] 각 프로젝트 `main`에서 교정된 계획을 재조회한다.
