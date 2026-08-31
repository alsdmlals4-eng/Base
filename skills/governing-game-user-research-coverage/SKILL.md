---
name: governing-game-user-research-coverage
description: Use when a game project must install, audit, plan, or synthesize Games User Research coverage across its eleven evidence domains.
---

# Governing Games User Research Coverage

## Core principle

`RESEARCH_QUESTION_FIRST`: 연구 방법이나 11영역 채우기보다 **어떤 개발 결정을 바꾸기 위해 무엇을 배워야 하는지**를 먼저 고정한다.

11개 연구 영역은 누락을 찾기 위한 coverage taxonomy다. 모든 영역에서 즉시 조사를 강제하지 않으며, 근거가 없으면 `NOT_STARTED`, 현재 결정에 적용 불가면 이유가 있는 `NOT_APPLICABLE`로 표시한다. `11/11`을 채우는 것이 완료 조건이 아니다.

`DECISION_RELEVANT_COVERAGE`: 현재 결정·위험·플레이어 약속에 영향을 주는 영역만 실제 연구·계측·플레이테스트 우선순위를 요구한다. 나머지 영역은 책임 위치와 상태를 유지하되 조사량을 부풀리지 않는다.

### Project-declared validation policy

`PROJECT_DECLARED_VALIDATION_POLICY` is required before turning a research or human-evidence state into an implementation, candidate, release, or cutover blocker. Base provides evidence vocabulary and a coverage taxonomy; it does not impose one fixed participant count, a universal player-experience study, or a mandatory human-study sequence on every project.

```text
MACHINE_PRIMARY_FINAL_USER_REVIEW
→ deterministic/runtime/export/package/CI evidence is the primary acceptance route
→ FINAL_USER_REVIEW is separately recorded only when the project/user requests it
→ FIVE_PERSON_COMPREHENSION_NOT_BASE_DEFAULT
→ PLAYER_EXPERIENCE_STUDY_NOT_BASE_DEFAULT
```

This selectable policy never promotes a machine result into human evidence. It also never suppresses an explicitly approved project research question, a target-platform/device requirement, a legal/accessibility obligation, or a user-requested human study. Those requirements remain decision-specific and must be recorded by their existing owners.

## Modes

`install → audit → plan-evidence → synthesize → verify-coverage`

## Required 11 domains

1. 시장·장르 분석
2. 벤치마킹·경쟁 게임 비교
3. SWOT·포지셔닝
4. 사용자 조사
5. 플레이테스트
6. 튜토리얼 이해도
7. UX 문제 분석
8. 텔레메트리·퍼널
9. 밸런스 데이터
10. 가설·실험·결과
11. 개선안과 채택·미채택 근거

책임·필드·상태·최소 증거는 `references/eleven-domain-coverage.md`를 필요할 때만 읽는다.

## Boundary

이 Skill은 누락 없는 구조와 증거 계획을 관리한다. 먼저 `research_question`, `decision_to_change`, `evidence_needed`, `evidence_ceiling`을 고정하고 어떤 domain이 그 질문에 실제로 필요한지 감사한다.

실제 컨셉·벤치마크·플레이테스트 해석과 `DECISION_SPECIFIC_RESEARCH` 실행은 `analyzing-and-refining-game-concepts`, 문서 생성은 `managing-design-documents`, 실제 계측 구현과 변경 검증은 프로젝트 계약과 검증 Skill이 책임진다. 따라서 이 Skill은 연구 실행을 중복 수행하거나 11개 domain 모두에 같은 방법·표본을 강제하지 않는다.

## Output contract

```md
## research question·바꿀 결정·evidence ceiling
## 11영역 coverage matrix
## decision-relevant / NOT_APPLICABLE 영역과 근거
## 영역별 책임 원본·담당·상태
## 현재 근거·표본·버전·한계
## 누락·중복·충돌
## 다음 연구·계측·플레이테스트 우선순위
## 개선안·채택/미채택 근거 연결
```

## Quality gate

빈 섹션 존재나 `11/11` 상태 채우기를 완료로 보거나, 조사하지 않은 내용을 사실로 작성하거나, 현재 결정과 무관한 domain을 억지로 조사하거나, 모든 프로젝트에 같은 연구 방법·표본을 강제하거나, 사용자 자기보고와 행동 데이터를 혼동하면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
