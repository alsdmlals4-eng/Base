---
name: designing-art-prompts-and-technique-cards
description: Use when recommending an art or UI visual technique, designing image-generation or image-editing prompts, generating planning or final-candidate images and mockups with GPT, recording reusable prompt patterns, or reviewing generated visuals before project approval.
---

# Designing Art Prompts and Technique Cards

이 스킬은 생성·편집 전 프롬프트, GPT 이미지·목업 생성 단계, 기술 카드와 승인 전 시각 검수를 책임진다. 이미 구현된 Godot/Web UI의 실제 시각 품질 감사와 승인된 개선은 `auditing-and-refining-ui-art`를 사용한다.

## Skill modes

- `technique-card`: 재사용 가능한 아트·UI 기술과 프롬프트 패턴을 기록한다.
- `planning-visualization`: 기획 중 세계관·인물·핵심루프·시스템·UI·대표 장면을 시각화해 방향과 모순을 비교한다.
- `intermediate-visual-checkpoint`: 사용자가 중간 점검·예상 게임 화면·UI 포함 화면을 요청하거나 P1 해석 위험이 있을 때, 현재 정본만으로 한 화면 흐름을 `DRAFT_VISUAL` 또는 대체 와이어프레임으로 검토한다.
- `final-visual-candidate`: 승인된 기획을 바탕으로 Demo-First·상점·홍보·UI·캐릭터·시스템 설명에 사용할 고품질 후보를 만든다.
- `visual-qa-and-approval`: 생성물의 기획 일치성·실제 화면·구현 가능성·권리·오류·재사용성을 검수하고 승인 후보 상태를 판정한다.

## Core principle

좋은 아트 프롬프트는 형용사를 많이 나열하는 문장이 아니라 **사용 목적, 유지할 정체성, 변경할 축, 화면 구성, 산출물 규격, 실패 기준**을 가진 제작 계약이다. 생성 결과는 자동 최종 자산이 아니다.

## Required inputs

- 자산의 사용 화면과 사용자·플레이어 경험.
- 관련 세계관·핵심루프·인물·시스템·아트·UI 책임 원본과 Decision ID.
- 원본 이미지 또는 캐릭터 디자인 카드.
- 유지해야 할 정체성·의상·소품·스타일.
- 변경할 표정·포즈·색·구도·정보 레이아웃.
- 출력 비율·해상도·크롭·알파·텍스트 처리 방식.
- 사용할 모델·서비스·버전과 실제 확인 가능한 기능.
- 프로젝트 Sheet 상태와 `71_이미지기획_생성목록`, `72_이미지검수_승인로그` 연결.

## Process

1. `planning-visualization`, `intermediate-visual-checkpoint`, `final-visual-candidate` 중 필요한 mode를 정한다.
2. 결과물이 쓰일 화면과 가장 먼저 전달할 정보를 정한다.
3. 원본에서 유지할 요소와 변경할 요소를 분리한다.
4. Pinterest를 포함한 발견 레퍼런스는 원작자·원출처·라이선스·유사성을 확인하고 표면 복제를 금지한다.
5. 프롬프트를 다음 모듈로 작성한다.

```text
목적과 자산 역할
→ 관련 정본·Decision·프로젝트 정체성 고정
→ 변경할 표정·포즈·상태
→ 구도와 정보 위계
→ 형태·색·재질·광원
→ 텍스트·레이아웃 슬롯
→ 실제 화면비·해상도·크롭
→ 금지·보호 요소
→ QA와 재생성 기준
```

6. 짧은 제어어가 필요한 경우 자연어 설명 뒤에 코드·태그를 보조 어휘로 넣는다.
7. 표정 편집은 FACS AU를 참고할 수 있지만 모델의 공식 명령 체계로 가정하지 않는다.
8. 포스터는 일러스트, 정보 슬롯, 실제 타이포그래피를 분리해 수정 가능하게 만든다.
9. 성공 사례뿐 아니라 실패 조건과 수정 프롬프트를 기록한다.
10. 생성 뒤 `visual-qa-and-approval`을 실행하고 `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`에 기록한다.
11. 승인된 Decision만 정본·GitHub·Sheet·Asset Ledger에 동기화한다.
12. 모델·버전·입력 이미지·확인일이 달라지면 재검증한다.

## Intermediate visual checkpoint

정본·Decision ID·화면 제약이 없는 경우에는 이미지를 추정 생성하지 말고 `MISSING_CANON`으로 반환한다. 한 번에 한 화면 흐름만 다루고, 화면 목적·첫 시선·주요 행동·플랫폼/화면비/입력·위험/비용/보상·성공/실패/복구·긴 한글·접근성·확인 사실과 미결정을 Brief에 쓴다. 이미지 생성 도구가 없거나 권한이 없으면 텍스트 와이어프레임·Mermaid·Figma 대체안을 쓴다.

생성 직후 `Screen Interpretation Review`에 정본과 일치한 요소, `MISSING_CANON`, `VISUAL_CANONICAL_CONFLICT`, `TECHNICAL_REVIEW_PROPOSAL`, 버린 표현을 기록한다. 이 mode의 결과는 `DRAFT_VISUAL`이며 최종 리소스·라이선스 승인·Figma 구현 명세·Godot 구현·런타임/사람 검증을 뜻하지 않는다. 사용자 Decision 없이 정본이나 Visual Artifact Registry의 승인 상태로 올리지 않는다.

## Status lifecycle

```text
PLANNED
→ GENERATED_EXPLORATION
→ IN_REVIEW
├─ REVISION_REQUIRED
├─ REJECTED
└─ APPROVED_CANDIDATE
   → PROJECT_ASSET_APPROVED
   → APPLIED_AND_RUNTIME_VERIFIED
```

`GENERATED_EXPLORATION`은 탐색 이미지, `APPROVED_CANDIDATE`는 기획 승인 후보다. 둘 다 최종 제품 자산이 아니다.

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

1. 메인 캐릭터와 전신·반신 포즈.
2. 배경 세계와 상징 오브젝트.
3. 키 컬러와 재질·광원.
4. 이름·엠블럼·태그라인 영역.
5. 특징 설명 모듈.
6. 표정·측면 인셋 이미지.
7. 타이틀·날짜·하단 정보.
8. 실제 후처리와 현지화 계획.

이미지 모델이 한글을 생성하더라도 최종 제품 텍스트는 편집 가능한 UI·그래픽 레이어로 교체한다. 이미지 안의 타이포그래피는 레이아웃 프로토타입 또는 키비주얼 시안으로 취급한다.

## Visual QA contract

- 기획·세계관·캐릭터·시스템 정본과 일치하는가.
- 핵심 경험과 세일즈포인트가 한눈에 전달되는가.
- 실제 화면 크기, HUD·VFX·배경 위에서 읽히는가.
- 구현 난이도·제작 비용·기술 규격이 현실적인가.
- 다른 자산과 형태·색·재질·광원이 일관적인가.
- 재사용·편집·현지화가 가능한가.
- 손·관절·무기·문자·로고·원근·광원 오류가 없는가.
- 특정 상업 IP·작가 스타일과 과도하게 유사하지 않은가.
- 원본·레퍼런스·모델·버전·프롬프트·생성일이 기록됐는가.
- 승인자·사용처·GitHub·Sheet·Asset Ledger가 연결됐는가.

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
- 기획 시각화 이미지·목업 또는 생성 불가 시 제작 브리프.
- 최종 시각 후보 또는 생성 불가 시 제작 브리프.
- 기본 생성 프롬프트.
- 원본 이미지 편집 프롬프트.
- 실패 수정 프롬프트.
- 상태·표정·포즈 변형 표.
- 실제 화면 QA 체크리스트.
- 모델별 검증 상태.
- 이미지 기획·검수·승인 기록.

## Failure conditions

- 작가명이나 작품명만으로 스타일을 지시한다.
- 원본 정체성과 변경 범위를 분리하지 않는다.
- 생성 이미지를 자동 최종 자산으로 사용한다.
- AU 번호가 모든 모델에서 같은 결과를 보장한다고 쓴다.
- 이미지 안의 가짜 문자·로고를 최종 제품 텍스트로 사용한다.
- 포스터 정보 슬롯이 캐릭터와 핵심 실루엣을 가린다.
- 실제 화면 크롭·현지화·편집 가능성을 검증하지 않는다.
- 원출처·라이선스·유사성 검토를 생략한다.
- 한 번 성공한 프롬프트를 검증된 공용 스킬로 표시한다.
- Sheet가 `NOT_CONFIGURED`인데 `SHEET_SYNCED`로 보고한다.

## Validation scenarios

1. 기획 중 핵심 시스템 목업이 텍스트 기획의 모순과 정보 위계를 드러내는지 비교한다.
2. 기획 종료 키아트 후보가 실제 캡슐 크롭과 UI 오버레이에서도 핵심 경험을 유지하는지 확인한다.
3. AU46 편집은 원본 인물과 스타일을 유지하면서 한쪽 눈만 자연스럽게 닫히는지 비교한다.
4. 캐릭터 포스터는 키 컬러와 이름을 바꿔도 정보 위계와 인셋 구조가 재사용되는지 확인한다.
5. 한국어 글자가 깨지면 이미지 전체를 재생성하지 않고 텍스트 없는 마스터와 편집 레이어로 분리한다.

## Quality gate

- 이미지 단계와 상태가 명시돼 있다.
- 생성·검수·승인·적용이 서로 다른 증거로 분리돼 있다.
- 프로젝트 정본과 실제 화면 기준으로 검수됐다.
- 권리·출처·모델·프롬프트·수정 이력이 기록됐다.
- 승인 결과가 필요한 소비처에 전파됐다.

## Learning Log

반복 성공·실패·모델 변화·검수 누락은 `skills/SKILL_LEARNING_LOG.md`에 기록하고, 공용 승격은 여러 프로젝트에서 재현된 경우에만 수행한다.

Templates:

- `templates/planning/ART_TECHNIQUE_CARD.md`
- `templates/planning/EXPRESSION_CONTROL_CARD.md`
- `templates/planning/CHARACTER_PROMO_POSTER_BRIEF.md`
- `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`
