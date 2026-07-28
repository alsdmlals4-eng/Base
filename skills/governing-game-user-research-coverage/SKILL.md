---
name: governing-game-user-research-coverage
description: Use when a game project's design-document system must install, audit, plan, or synthesize complete Games User Research coverage across eleven required evidence domains without inventing findings or forcing irrelevant research activity.
---

# Governing Games User Research Coverage

## Core principle

기획 운영체계에는 11개 연구 영역의 **자리·책임·증거 상태**가 모두 있어야 한다. 모든 영역에서 즉시 조사를 강제하지는 않으며, 근거가 없으면 `NOT_STARTED`, 적용 불가면 이유가 있는 `NOT_APPLICABLE`로 표시한다.

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

사람 검증 계획이 작은 표본, 카드·종이·클릭 Mock, 기존 PoC overlay, simulated recognition, scripted outcome, fixed RNG 결과를 사용하면 다음 두 파일을 함께 읽는다.

- `skills/governing-game-user-research-coverage/references/human-validation-artifact-governance.md`
- `templates/research/HUMAN_VALIDATION_SESSION_PACKET.md`

## Human validation planning contract

`plan-evidence`에서 사람 세션을 설계할 때 다음을 분리한다.

- Artifact fidelity와 `claim_ceiling`.
- 실제 시스템과 simulated·scripted·fixed 구성요소.
- 피드백 전 `first_attempt`와 피드백 후 `post_feedback_attempt`.
- 플레이어 행동, 자기보고, 진행자 개입, 실제 로그 또는 Artifact 결과.
- 작은 표본의 분자/분모, 반복 결함, 심각도 높은 반례, 경험군 차이.
- 제품 코드·정본·기기·접근성·성능·알고리즘 정확도의 미실행 상태.

작은 표본의 기본 판정은 `PROMISING_DIRECTION / ADAPT / REWORK / REJECT / STOP`이다. 실제 제품 또는 목표 fidelity Build의 반복 증거와 프로젝트 승인 전에는 자동 `ADOPT`를 사용하지 않는다.

## Boundary

이 Skill은 누락 없는 구조와 증거 계획을 관리한다. 실제 컨셉·벤치마크·플레이테스트 해석은 `analyzing-and-refining-game-concepts`, 문서 생성은 `managing-design-documents`, 실제 계측 구현과 변경 검증은 프로젝트 계약과 검증 Skill이 책임진다.

저충실도 Artifact가 통과해도 제품 UI·실제 RNG·알고리즘 정확도·접근성·성능·장기 밸런스가 통과한 것은 아니다. 사람 세션을 실행하지 않았다면 `NOT_RUN` 또는 `UNVERIFIED`를 유지한다.

## Output contract

```md
## 11영역 coverage matrix
## 영역별 책임 원본·담당·상태
## 현재 근거·표본·버전·한계
## Artifact fidelity·claim ceiling·simulated 요소
## 행동·자기보고·진행자 개입·로그 분리
## 최초 시도·피드백 후 수정
## 반복 결함·반례·경험군 차이
## 누락·중복·충돌
## 다음 연구·계측·플레이테스트 우선순위
## 개선안·채택/미채택 근거 연결
```

## Quality gate

다음이면 실패다.

- 빈 섹션 존재를 완료로 봄.
- 조사하지 않은 내용을 사실로 작성함.
- 모든 프로젝트에 같은 연구 방법·표본을 강제함.
- 사용자 자기보고와 행동 데이터를 혼동함.
- 작은 표본 비율만으로 제품 방향을 자동 `ADOPT`함.
- simulated·scripted·fixed 결과를 실제 정확도·확률·지연·밸런스로 주장함.
- 피드백 전 최초 시도나 진행자 개입을 기록하지 않음.
- 저충실도 Artifact 통과를 제품 UI·접근성·성능 통과로 확대함.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
