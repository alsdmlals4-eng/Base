---
name: designing-art-prompts-and-technique-cards
description: Use when recommending an art or UI visual technique, designing image-generation or image-editing prompts, or recording reusable prompt patterns that GPT, Codex, or a project team should be able to apply and verify.
---

# Designing Art Prompts and Technique Cards

이 스킬은 생성·편집 전 프롬프트와 기술 카드를 책임진다. 이미 구현된 Godot/Web UI의 시각 품질 감사와 승인된 개선은 `auditing-and-refining-ui-art`를 사용한다.

## Core principle

좋은 아트 프롬프트는 형용사를 많이 나열하는 문장이 아니라 **사용 목적, 유지할 정체성, 변경할 축, 화면 구성, 산출물 규격, 실패 기준**을 가진 제작 계약이다.

## Required inputs

- 자산의 사용 화면과 사용자·플레이어 경험.
- 원본 이미지 또는 캐릭터 디자인 카드.
- 유지해야 할 정체성·의상·소품·스타일.
- 변경할 표정·포즈·색·구도·정보 레이아웃.
- 출력 비율·해상도·크롭·알파·텍스트 처리 방식.
- 사용할 모델·서비스와 실제 확인 가능한 기능.

## Process

1. 결과물이 쓰일 화면과 가장 먼저 전달할 정보를 정한다.
2. 원본에서 유지할 요소와 변경할 요소를 분리한다.
3. 프롬프트를 다음 모듈로 작성한다.

```text
목적과 자산 역할
→ 원본·정체성 고정
→ 변경할 표정·포즈·상태
→ 구도와 정보 위계
→ 형태·색·재질·광원
→ 텍스트·레이아웃 슬롯
→ 출력 규격
→ 금지·보호 요소
→ QA와 재생성 기준
```

4. 짧은 제어어가 필요한 경우 자연어 설명 뒤에 코드·태그를 보조 어휘로 넣는다.
5. 표정 편집은 FACS AU를 참고할 수 있지만 모델의 공식 명령 체계로 가정하지 않는다.
6. 포스터는 일러스트, 정보 슬롯, 실제 타이포그래피를 분리해 수정 가능하게 만든다.
7. 성공 사례뿐 아니라 실패 조건과 수정 프롬프트를 기록한다.
8. `templates/planning/ART_TECHNIQUE_CARD.md`로 사람과 AI가 재사용할 기술 카드로 저장한다.
9. 모델·버전·입력 이미지·확인일이 달라지면 재검증한다.

## FACS-assisted expression control

권장 형식:

```text
원본 캐릭터의 얼굴 비율, 헤어, 의상, 안경, 채색과 배경을 유지한다.
표정만 한쪽 눈의 자연스러운 윙크로 변경한다.
보조 제어 어휘: FACS AU46 Wink, 약한 미소는 AU12B.
닫힌 눈의 속눈썹·안경테·눈썹이 겹치지 않게 한다.
```

- AU 번호만 단독 입력하는 방식은 빠른 탐색용이다.
- 최종 편집에는 자연어, 좌우 방향, 강도, 보호 요소를 함께 쓴다.
- 제공된 레퍼런스 그리드의 일부 번호는 표준 FACS와 다를 수 있으므로 `docs/knowledge/research/FACS_ACTION_UNIT_PROMPT_REFERENCE.md`의 구분을 따른다.

## Character poster prompt architecture

포스터 프롬프트는 다음 슬롯을 독립적으로 관리한다.

1. 메인 캐릭터와 전신·반신 포즈.
2. 배경 세계와 상징 오브젝트.
3. 키 컬러와 재질·광원.
4. 이름·엠블럼·태그라인 영역.
5. 특징 설명 모듈.
6. 표정·측면 인셋 이미지.
7. 타이틀·날짜·하단 정보.
8. 실제 후처리와 현지화 계획.

이미지 모델이 한글을 생성하더라도 최종 제품 텍스트는 편집 가능한 UI·그래픽 레이어로 교체하는 것을 기본값으로 한다. 이미지 안의 타이포그래피는 레이아웃 프로토타입 또는 키비주얼 시안으로 취급한다.

## Technique card fields

- 기술명·분류·상태.
- 해결하는 문제와 사용자 가치.
- 사용 조건·사용하지 않을 조건.
- 필요한 입력과 모델 호환성.
- 유지 요소·변경 요소.
- 프롬프트 패턴과 실제 사례.
- 제어 키워드와 수정 포인트.
- 화면·UI·데이터·현지화 영향.
- 실패 패턴·QA·검증 근거.
- Base 공용 원리와 프로젝트 전용 값.

## Output contract

- 아트 기술 카드.
- 기본 생성 프롬프트.
- 원본 이미지 편집 프롬프트.
- 실패 수정 프롬프트.
- 상태·표정·포즈 변형 표.
- 실제 화면 QA 체크리스트.
- 모델별 검증 상태.

## Failure conditions

- 작가명이나 작품명만으로 스타일을 지시한다.
- 원본 정체성과 변경 범위를 분리하지 않는다.
- AU 번호가 모든 모델에서 같은 결과를 보장한다고 쓴다.
- 이미지 안의 가짜 문자·로고를 최종 제품 텍스트로 사용한다.
- 포스터 정보 슬롯이 캐릭터와 핵심 실루엣을 가린다.
- 실제 화면 크롭·현지화·편집 가능성을 검증하지 않는다.
- 한 번 성공한 프롬프트를 검증된 공용 스킬로 표시한다.

## Validation scenarios

1. AU46 편집은 원본 인물과 스타일을 유지하면서 한쪽 눈만 자연스럽게 닫히는지 비교한다.
2. 캐릭터 포스터는 키 컬러와 이름을 바꿔도 정보 위계와 인셋 구조가 재사용되는지 확인한다.
3. 한국어 글자가 깨지면 이미지 전체를 재생성하지 않고 텍스트 없는 마스터와 편집 레이어로 분리한다.

Templates:

- `templates/planning/ART_TECHNIQUE_CARD.md`
- `templates/planning/EXPRESSION_CONTROL_CARD.md`
- `templates/planning/CHARACTER_PROMO_POSTER_BRIEF.md`
