---
name: designing-vertical-slices
description: Use when a project needs to validate its core experience, target quality, cross-system integration, or content-production pipeline through one representative playable segment.
---

# Designing Vertical Slices

## Core principle

게임 전체를 얕게 만드는 대신, 핵심 경험을 대표하는 작은 구간을 최종 품질에 가까운 깊이로 연결해 **재미·품질·제작성**을 동시에 검증한다.

## Distinguish

| 형태 | 검증 대상 |
|---|---|
| Prototype | 핵심 가설 또는 기술 가능성 |
| Vertical Slice | 대표 경험, 목표 품질, 시스템 연결, 제작 파이프라인 |
| MVP | 최소 전체 제품 구조 |
| Demo | 외부 플레이어를 설득하는 공개 구간 |

## Required inputs

- 핵심 플레이어 약속과 반복 루프
- 가장 위험한 재미·기술·제작 가설
- 현재 시스템과 자산 상태
- 목표 플랫폼·품질·시간·인력 제약

## Process

1. 한 문장 핵심 가설을 정한다.
2. 진입→행동→판단→반응→결과→기록·복귀가 연결되는 대표 구간을 고른다.
3. 핵심 세일즈포인트와 일반 플레이를 함께 보여주는지 확인한다.
4. 포함 시스템·콘텐츠·아트·UI·사운드·데이터를 최소화한다.
5. 전체 분량, 모든 캐릭터, 장기 경제 등 제외 범위를 고정한다.
6. 조작감, 정보 전달, 아트, 연출, 사운드, 성능의 품질 기준을 관찰 가능하게 쓴다.
7. 기획→데이터→자산→구현→QA→문서화의 제작 흐름을 실제로 한 번 통과시킨다.
8. 성공·실패 시 다음 개발 결정을 미리 정의한다.
9. 내부·외부 플레이테스트로 재미와 제작 비용을 기록한다.

## Output contract

- 검증 목적과 핵심 가설
- 목표 플레이어 경험
- 대표 플레이 흐름과 예상 시간
- 포함·제외 범위
- 시스템·콘텐츠·자산 목록
- 품질 기준
- 제작 파이프라인
- 기술·콘텐츠 위험
- 테스트 대상과 측정 방법
- 성공·실패·중단 기준
- 후속 개발 결정

## Failure conditions

- 기능 목록만 있고 처음부터 끝까지 플레이할 수 없음
- 특수 보스전처럼 일반 제작성을 대표하지 않는 구간
- 임시 자산만 사용해 목표 품질을 검증할 수 없음
- 전체 게임 분량을 슬라이스에 포함
- “재미있다”, “완성도 높다”만 있고 관찰 기준이 없음
- 제작 시간과 반복 생산 가능성을 기록하지 않음

## Validation scenarios

1. 카드 전투 게임은 카드 획득→선택→사용→적 반응→보상→덱 상태 기록까지 한 전투 구간으로 연결한다.
2. 조사 게임은 사건 진입→관찰→규칙 추론→위험 선택→기록·회수 결과까지 연결한다.
3. Prototype 결과가 좋더라도 아트·UI·사운드·파이프라인이 검증되지 않으면 Vertical Slice 완료로 표시하지 않는다.

Template: `templates/planning/VERTICAL_SLICE_PLAN.md`
