# Human Validation Artifact Governance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 작은 표본의 저충실도 사람 검증 Artifact가 실제 제품 성능이나 통계적 확증으로 과장되지 않도록 Base 공용 규칙·Template·회귀 테스트를 추가하고, 다섯 프로젝트 Pilot 문서를 동일 기준으로 교정한다.

**Architecture:** 기존 `governing-game-user-research-coverage` Skill이 실행 권한을 유지한다. 공용 규칙은 Skill package Reference에, 실행 양식은 `templates/research/`에 배치하고, 프로젝트별 고유 시나리오·ID·수치는 각 저장소에 남긴다. Base 병합을 선행 게이트로 사용한 뒤 프로젝트 문서를 독립 PR로 수정한다.

**Tech Stack:** Markdown 계약, Python `unittest`, GitHub branch/PR/Actions.

## Global Constraints

- 새 GUR 광역 Skill을 만들지 않는다.
- 작은 표본의 비율 임계값은 통계적 일반화나 자동 `ADOPT` 판정으로 사용하지 않는다.
- 행동 관찰, 자기보고, 진행자 개입, 시스템 로그를 분리한다.
- simulated·scripted·fixed Artifact는 실제 알고리즘 정확도·확률·성능을 주장하지 않는다.
- 최초 시도와 피드백 후 수정 시도를 분리한다.
- 제품 코드·Scene·Resource·밸런스·정본 변경 권한은 프로젝트별 별도 승인으로 유지한다.
- 사람 세션을 실행하지 않은 상태는 `NOT_RUN`으로 유지한다.

---

### Task 1: 공용 사람 검증 Governance Reference

**Files:**
- Create: `skills/governing-game-user-research-coverage/references/human-validation-artifact-governance.md`
- Modify: `skills/governing-game-user-research-coverage/SKILL.md`

**Interfaces:**
- Consumes: 기존 GUR 11영역 상태·책임 계약.
- Produces: fidelity별 주장 범위, 작은 표본 판정 언어, 자극물·진행자·원자료 분리 계약.

- [ ] Reference에 `artifact_fidelity`, `claim_ceiling`, `simulated_component`, `first_attempt`, `post_feedback_attempt`, `behavior`, `self_report`, `facilitator_intervention`, `limitations` 필드를 정의한다.
- [ ] 판정 언어를 `PROMISING_DIRECTION / ADAPT / REWORK / REJECT / STOP`으로 정의하고 `ADOPT`는 반복 증거와 실제 제품 검증 뒤에만 허용한다.
- [ ] Skill의 `plan-evidence` 경로가 사람 검증 계획일 때 Reference와 Template을 읽도록 연결한다.
- [ ] Skill Quality gate에 simulated 결과를 실제 성능으로 주장하거나 작은 표본 비율을 자동 합격선으로 사용하는 경우를 실패로 추가한다.

### Task 2: 공용 세션 패킷 Template

**Files:**
- Create: `templates/research/HUMAN_VALIDATION_SESSION_PACKET.md`

**Interfaces:**
- Consumes: Task 1의 상태·판정 언어.
- Produces: 프로젝트가 복제해 채우는 세션 패킷 구조.

- [ ] 기준선·결정 질문·보호 경계·Artifact fidelity·claim ceiling을 기록한다.
- [ ] 참가자 구성은 고정 숫자를 강제하지 않고 목적·세그먼트·모집 한계를 기록한다.
- [ ] 행동·자기보고·진행자 개입·로그를 별도 표로 둔다.
- [ ] 최초 시도와 교정 후 시도를 별도 필드로 둔다.
- [ ] 반복 결함, 반례, 경험군 차이, 미실행 검증을 우선하는 판정표를 둔다.
- [ ] 원자료 익명화와 보고서 저장 경로를 정의한다.

### Task 3: 라우팅·학습·변경 기록

**Files:**
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Consumes: Task 1~2의 경로.
- Produces: 콜드 스타트·학습·변경 이력에서 발견 가능한 공용 계약.

- [ ] Documentation Map의 플레이테스트 질문에 새 Reference와 Template을 연결한다.
- [ ] Learning Log에 다섯 프로젝트 드라이런에서 발견한 공통 결함과 공용화 경계를 기록한다.
- [ ] Changelog에 작은 표본·저충실도 과장 방지 계약을 기록한다.

### Task 4: 계약 테스트

**Files:**
- Create: `tests/test_human_validation_artifact_governance.py`

**Interfaces:**
- Consumes: Task 1~3의 파일.
- Produces: 공용 계약 누락·새 중복 Skill·과장 판정 회귀를 차단하는 `unittest`.

- [ ] Reference·Template·Skill·Documentation Map·Learning Log의 필수 토큰을 검사한다.
- [ ] `PROMISING_DIRECTION`, `claim_ceiling`, `SIMULATED`, `first_attempt`, `post_feedback_attempt`, `NOT_RUN`을 검사한다.
- [ ] 새 `human-validation-*` Skill ID가 Registry에 생기지 않았음을 검사한다.
- [ ] 기존 Evidence Knowledge 테스트와 함께 Actions에서 실행되는지 확인한다.

### Task 5: Base PR 검증·병합

**Files:**
- Review: `main...gpt/human-validation-artifact-governance-20260729`

**Interfaces:**
- Consumes: Task 1~4 전체.
- Produces: 프로젝트 교정이 참조할 Base `main` commit.

- [ ] 변경 파일이 계획·Reference·Template·Skill·라우터·학습·테스트로 제한되는지 비교한다.
- [ ] PR을 만들고 Required Checks를 확인한다.
- [ ] 미해결 리뷰 스레드와 mergeability를 확인한다.
- [ ] squash merge하고 Base `main`에서 새 Reference·Template을 재조회한다.

### Task 6: 다섯 프로젝트 계획 교정

**Files:**
- Modify: 십보강호 `docs/superpowers/plans/2026-07-29-enemy-intent-human-validation-artifact.md`
- Modify: Blacksmith `docs/superpowers/plans/2026-07-29-plus5-plus10-human-validation-artifact.md`
- Modify: OMENWARD `docs/superpowers/plans/2026-07-29-roulette-agency-validation-artifact.md`
- Modify: 괴이기록국 `docs/superpowers/plans/2026-07-29-hypothesis-board-human-validation-artifact.md`
- Modify: GRIMOIRE `docs/superpowers/plans/2026-07-29-magic-writing-input-validation-artifact.md`

**Interfaces:**
- Consumes: Base Task 5 merge commit과 공용 Governance.
- Produces: 프로젝트별 검증 가능하지만 과장되지 않는 세션 계약.

- [ ] 모든 프로젝트의 자동 `ADOPT` 표현을 `PROMISING_DIRECTION` 중심으로 낮춘다.
- [ ] 십보강호에 fixture/seed 없는 실제 전투 인과 주장 금지와 카드 이해/전투 인과 분리를 추가한다.
- [ ] Blacksmith에 표준 실패 결과 카드와 실제 선택/결과 회상 분리를 추가한다.
- [ ] OMENWARD에 동일 구조의 유리/불리 RNG 결과 교차 배정을 추가한다.
- [ ] 괴이기록국에 최초 연결과 피드백 후 수정 연결을 분리한다.
- [ ] GRIMOIRE에서 실제 인식률 지표를 제거하고 simulated recognition UX 책임만 판정한다.

### Task 7: 프로젝트별 PR 검증·병합

**Files:**
- Review: 각 프로젝트 `main...branch`

**Interfaces:**
- Consumes: Task 6 수정.
- Produces: 5개 프로젝트 `main`의 교정된 사람 검증 계획.

- [ ] 프로젝트별 제품 경로 비침범을 확인한다.
- [ ] 자동 CI가 있는 네 저장소의 Required Checks를 확인한다.
- [ ] GRIMOIRE는 자동 Actions 부재를 수동 검증 증거로 기록한다.
- [ ] 미해결 리뷰 스레드와 mergeability를 확인한다.
- [ ] 각 PR을 expected HEAD 고정으로 squash merge하고 `main`에서 재조회한다.
