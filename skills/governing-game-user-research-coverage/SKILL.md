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

## Boundary

이 Skill은 누락 없는 구조와 증거 계획을 관리한다. 컨셉·PoC·플레이테스트 계약은 `developing-game-concepts-and-pocs`, SWOT·VRIO·포지셔닝 분석은 `analyzing-game-positioning-with-swot-vrio`, DDD·다단계 증거 해석은 `analyzing-and-refining-game-concepts`가 책임진다. 문서 생성은 `managing-design-documents`, 실제 계측 구현과 변경 검증은 프로젝트 계약과 검증 Skill이 책임진다.

## Output contract

```md
## 11영역 coverage matrix
## 영역별 책임 원본·담당·상태
## 현재 근거·표본·버전·한계
## 누락·중복·충돌
## 다음 연구·계측·플레이테스트 우선순위
## 개선안·채택/미채택 근거 연결
```

## Quality gate

빈 섹션 존재를 완료로 보거나, 조사하지 않은 내용을 사실로 작성하거나, 모든 프로젝트에 같은 연구 방법·표본을 강제하거나, 사용자 자기보고와 행동 데이터를 혼동하면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
