# 아트 디렉션·에셋 기획 Guide

## 1. 목적

이 Guide는 “예쁜 그림을 만든다”가 아니라 **플레이어 경험·정보 전달·게임 정체성·제작성·시장 첫인상을 하나의 시각 체계로 연결하는 방법**을 설명한다.

실행 책임은 `designing-art-prompts-and-technique-cards`, `auditing-and-refining-ui-art`, `designing-vertical-slices`, `reviewing-and-validating-project-changes`, 프로젝트 아트·UX Skill이 가진다.

현업 참고:

- Art Direction은 key art만이 아니라 예술·창작·기술·마케팅 조건을 연결한 visual identity framework가 필요하다: https://gdcvault.com/free/gdc-23/play/1028731/Art-Direction-Summit-Building-a
- Graphic design은 typography·iconography·logo·colour·UI·key art·motion을 잇는 visual signature를 만든다: https://www.gdcvault.com/play/1023276/Art-Direction-Graphic-Design-is
- Pre-production은 Art Bible·평가 지점·생산 진입 조건을 명확히 해야 한다: https://gdcvault.com/play/1034593/Art-Direction-Summit-Pre-Production
- 대규모 외주 자산 생산은 상세 brief와 품질 보호 파이프라인이 필요하다: https://www.gdcvault.com/play/1023575/Art-Direction-Bootcamp-Guerrilla-Games

## 2. 아트 문제 정의

이미지를 만들기 전에 다음을 고정한다.

```yaml
player_experience:
information_role:
fantasy_and_emotion:
market_first_impression:
mascot_or_symbol:
target_platform_and_viewing_distance:
production_capacity:
asset_reuse_and_variation:
technical_constraints:
approval_decision:
```

질문:

- 플레이어가 첫 3초에 무엇을 알아야 하는가?
- 플레이 중 무엇을 구분·예측·선택해야 하는가?
- 어떤 감정·판타지·세계관을 즉시 느껴야 하는가?
- 상점 썸네일·캡슐·영상에서 무엇이 기억점인가?
- 마스코트·상징은 플레이·서사·UI·홍보에서 어떤 역할을 하는가?
- 실제 인게임 크기와 거리는 얼마인가?
- 같은 유형의 자산을 몇 개 반복 제작해야 하는가?
- 혼자·AI·외주·에셋스토어 중 무엇이 적합한가?

키워드만 있는 “귀엽고 아름다운 판타지”는 Art Direction 계약이 아니다.

## 3. Visual Pillar

Visual Pillar는 3~5개로 제한하고 서로 다른 책임을 가진다.

예시 구조:

```yaml
pillar_id:
player_promise:
visual_rule:
observable_examples:
anti_examples:
implementation_scope:
validation_capture:
```

좋은 Visual Pillar:

- 플레이어 경험과 연결된다.
- 실제 캐릭터·배경·UI·이펙트에서 관찰 가능하다.
- 포함 예시와 금지 예시가 있다.
- 제작 비용과 기술 제약을 고려한다.
- 다른 Pillar와 중복되지 않는다.

나쁜 Visual Pillar:

- `고퀄리티`
- `예쁨`
- `독창적`
- `AAA 느낌`

## 4. Visual Identity 구조

```text
플레이어 약속
→ Visual Pillar
→ Shape Language·실루엣
→ Color·Value·Composition
→ Typography·Iconography·Logo
→ 캐릭터·환경·UI·VFX·Animation
→ Store·Trailer·Marketing
→ 실제 인게임 캡처
```

### Shape Language

`Shape Language`는 진영·문화·성격·기능을 공통 형태로 표현한다.

현업 사례에서 shape language는 추상 형태를 차량·의상·건축·환경으로 확장해 세계관을 일관되게 만드는 방법으로 사용된다: https://www.gdcvault.com/play/1025897/Art-Direction-Bootcamp-Building-Worlds

검수:

- 원·삼각·사각·곡선·각진 형태가 어떤 의미를 갖는가?
- 캐릭터·장비·건물·UI가 같은 형태 문법을 공유하는가?
- 모든 대상이 같은 모양이라 구분성이 사라지지 않는가?
- 세계관의 문화·재료·기능과 연결되는가?

### 실루엣

실루엣은 디테일을 제거한 상태에서도 역할·진영·위험·방향을 구분하게 한다.

```text
전체 크기
→ 머리·몸통·부속 비율
→ 대표 도구·장식
→ 포즈·무게 중심
→ 이동·공격 시 외곽 변화
```

썸네일과 실제 플레이 거리 양쪽에서 검사한다.

### Color

`Color`는 분위기뿐 아니라 진영·상태·상호작용을 전달한다.

- 핵심 상태를 색 하나에만 의존하지 않는다.
- 배경과 플레이 요소의 분리 기준을 둔다.
- 일반·위험·보상·선택·비활성 상태의 색 역할을 정의한다.
- 플랫폼·디스플레이·밝기·색각 조건을 고려한다.

### Value

`Value`는 명도 구조다.

- 흑백으로 보아도 핵심 요소가 분리되는가?
- 가장 밝거나 어두운 영역이 의도한 시선을 받는가?
- UI·텍스트·이펙트가 배경과 충돌하지 않는가?
- 공포를 “전부 어둡게” 만드는 방식으로 해결하지 않는가?

### Composition

`Composition`은 플레이어의 시선과 정보 순서를 설계한다.

- 첫 시선
- 두 번째 판단 정보
- 행동 대상
- 위험·보상
- 다음 이동 방향
- 서사·감정 강조

카메라·UI·캐릭터·이펙트가 서로 같은 위치를 경쟁하지 않게 한다.

## 5. 시각적 위계

```text
1차: 지금 반드시 알아야 하는 정보
2차: 다음 선택에 필요한 정보
3차: 숙련·최적화 정보
4차: 분위기·세계관·장식
```

장식이 1차·2차 정보를 가리면 Art Quality가 아니라 UX 결함이다.

검수 방법:

- 3초 테스트
- 흑백 테스트
- 축소 썸네일 테스트
- 모션 중 정지 화면 테스트
- 색 제거 테스트
- 텍스트·아이콘 제거 후 형태 테스트
- 실제 인게임 캡처 비교

## 6. 마스코트·상징

마스코트·상징은 귀여운 부속물이 아니라 다음 역할을 가질 수 있다.

- 첫인상과 기억점
- 플레이어 안내
- 세계관·기관·진영 표현
- 감정 완충
- 진행·성장·관계 피드백
- UI 상태 전달
- 상점·캡슐·트레일러 대표 이미지

```yaml
symbol_role:
player_relationship:
core_loop_touchpoints:
narrative_role:
ui_role:
marketing_role:
non_negotiable_traits:
changeable_traits:
production_scope:
```

마스코트가 핵심 판단을 대신하거나 기능 설명을 독점하지 않게 한다.

## 7. Concept Exploration

`Concept Exploration`은 정답 이미지 한 장을 빨리 만드는 단계가 아니다.

```text
문제 정의
→ reference axis
→ 서로 다른 방향 3개 안팎
→ 동일 구도·조건 비교
→ 채택·비채택 요소 분리
→ 선택 이유 기록
```

비교 차원 예:

- 현실성↔도식성
- 귀여움↔위엄
- 따뜻함↔불안
- 장식 밀도
- 형태 복잡도
- 색 채도
- 실제 제작 난이도
- UI·이펙트와 결합성

후보마다 다음을 기록한다.

- 강화하는 플레이어 경험
- 약화하는 정보
- 세일즈포인트
- 제작 비용
- 반복 생산 위험
- 기술·플랫폼 위험
- 채택 요소
- 비채택 요소

## 8. Concept → Art Bible → Asset Specification

### Concept Exploration

- 방향 후보와 핵심 질문을 검증한다.
- 최종 자산으로 사용하지 않는다.
- 임시 텍스트·수치·UI를 공식 기획값으로 해석하지 않는다.

### Art Bible

`Art Bible`은 프로젝트의 시각 결정과 판단 규칙을 가진다.

필수 내용:

- 플레이어 약속과 Visual Pillar
- Shape Language·실루엣
- Color·Value·Composition
- 캐릭터·환경·UI·VFX·Animation 원칙
- 재료·광원·카메라·렌더 규칙
- Typography·Iconography·Logo
- 포함·금지 예시
- 접근성·가독성
- 승인 상태와 대체 관계

### Asset Specification

`Asset Specification`은 개별 제작물이 실제 엔진과 파이프라인에서 작동하기 위한 계약이다.

```yaml
asset_id:
role:
canonical_path:
source_and_license:
dimensions_and_aspect:
viewing_distance:
pivot_and_alignment:
frames_and_states:
export_format:
import_settings:
performance_budget:
size_quality_class:
platform_import_profile:
quality_validation:
accessibility_role:
approval_status:
validation_scene_and_capture:
```

`size_quality_class`, `platform_import_profile`, `quality_validation`은 용량 최적화가 해당 자산에 적용될 때만 구체화한다. byte·압축·전달·패치 trade-off의 공용 방법은 `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`가 책임지고, 이 문서는 시각 의도·가독성·실제 인게임 품질을 계속 소유한다.

Art Bible이 “어떤 방향인가”를, Asset Specification이 “정확히 무엇을 어떻게 납품하는가”를 책임진다.

## 9. 캐릭터·환경·UI·VFX·Animation 연결

### 캐릭터

- 실루엣·비율·대표 소품
- 성격·직업·진영
- 실제 인게임 크기
- 표정·포즈·애니메이션 범위
- 다른 캐릭터와 구분성
- 마스코트·세일즈 역할

### 환경

- 이동·전투·조사의 길 찾기
- 위험·상호작용·보상 affordance
- 장소의 이야기
- 캐릭터와 명도·채도 분리
- 반복 모듈과 대표 landmark

### UI

- visual identity와 인게임 가독성의 균형
- Typography·Iconography·Focus·State
- 입력 장치별 일관성
- 화면 비율·안전 영역
- 색 외 정보 채널

GDC의 UI Art Direction 사례는 인지 과정·이론·엔진 지식을 결합해 concept부터 release까지 일관된 표현을 만드는 접근을 다룬다: https://www.gdcvault.com/play/1025498/Art-Direction-for-AAA

### VFX

- 판정·방향·범위·속성·위험·보상 전달
- VFX가 게임 디자인 언어로 작동하는가?
- 이펙트가 캐릭터·UI·배경을 가리지 않는가?
- 모션 감소·번쩍임·반복 피로 대안이 있는가?

VFX가 넓은 게임 디자인 개념을 시각 언어로 전달할 수 있다는 현업 관점을 참고한다: https://www.gdcvault.com/play/1027899/Visual-Effects-Summit-VFX-as

### Animation

- key pose와 silhouette 변화
- anticipation·contact·follow-through·recovery
- 입력·판정·피드백 타이밍
- 무기·장비·의상 continuity
- 루프·1회성·전환 상태
- 프레임 수보다 의미 있는 동작 차이

## 10. 실제 인게임 검수

아트는 분리된 일러스트가 아니라 실제 게임 화면에서 검수한다.

필수 증거:

- 실제 해상도
- 대표·최악 장면
- 실제 UI와 텍스트
- 이동·전투·이펙트 중 화면
- 밝은·어두운 배경
- 목표 플랫폼 화면 크기
- 접근성 옵션 적용 전후
- 성능 capture
- 용량 최적화 전후 동일 장면 비교(해당 시)
- texture compression·resolution·font fallback 변경의 artifact/가독성 확인(해당 시)

상태 예:

```text
CONCEPT_EXPLORATION
→ VISUAL_REFERENCE_CANDIDATE
→ USER_APPROVED_VISUAL_REFERENCE
→ ART_BIBLE_APPROVED
→ ASSET_SPEC_APPROVED
→ IMPLEMENTED_IN_ENGINE
→ RUNTIME_ASSET_APPROVED
```

`Runtime Asset Approval`은 실제 인게임 캡처·성능·가독성 검수 뒤에만 사용한다. 용량 최적화가 적용된 자산은 byte 절감만으로 승인하지 않고 변경 후 동일 quality bar를 다시 확인한다.

## 11. 생산 파이프라인

```text
Brief
→ Concept
→ Review
→ Specification
→ Production
→ Export
→ Import
→ Integration
→ Runtime QA
→ Revision
→ Approval Ledger
```

각 단계에 입력·출력·담당·도구·검증·재작업 원인을 기록한다.

### 두 번째 같은 유형의 자산

첫 자산 하나를 멋지게 만든 것으로 Production 준비를 판단하지 않는다.

두 번째 같은 유형의 자산을 만들며 다음을 확인한다.

- Brief가 재사용 가능한가?
- 명명·경로·Export·Import가 반복 가능한가?
- 품질 판단이 개인 감각에만 의존하는가?
- 수정 왕복 횟수와 병목은 무엇인가?
- AI·외주·에셋 사용 시 provenance가 추적되는가?
- 실제 엔진 통합 시간이 예측 가능한가?

## 12. AI 생성·외주·기존 에셋

### 공통 원칙

- 원출처를 기록한다.
- 라이선스와 상업 사용 조건을 확인한다.
- 기존 IP·작가·브랜드와의 유사성을 검수한다.
- 생성·편집·외주·구매·직접 제작 관계를 기록한다.
- 채택·비채택 요소와 사용자 승인 상태를 남긴다.

### 생성 이미지

**생성 이미지는 자동 최종 자산이 아니다.**

기획 시각화, 후보 비교, mood·composition 탐색과 최종 후보 제작을 구분한다. 실제 자산은 Asset Specification과 Runtime 검수를 통과해야 한다.

### Pinterest·커뮤니티 이미지

- 탐색과 mood reference로 사용할 수 있다.
- Pinterest Pin 자체를 원출처로 간주하지 않는다.
- 가능하면 작가·스튜디오·공식 프로젝트 원문으로 추적한다.
- 무단 복제·스타일 사칭·로고·상표·인물 위험을 검수한다.

### 외주

현업 대규모 외주 사례처럼 상세 Brief와 품질 보호 파이프라인이 중요하다. 1인 개발에서는 규모를 복사하지 않고 다음 원리를 ADAPT한다.

- 납품 규격
- 포함·금지 예시
- 리뷰 단계
- 수정 횟수와 책임
- 원본 파일·파생물·권리
- 엔진 통합 검증

## 13. 접근성·성능

- 핵심 정보는 Color 하나에만 의존하지 않는다.
- 텍스트·아이콘·형태·음향·진동 중 가능한 대체 채널을 둔다.
- motion·camera shake·flashing을 조절할 수 있게 한다.
- 실제 frame time·GPU·메모리·로딩 예산을 아트 목표와 연결한다.
- 모바일은 발열·배터리·해상도·텍스처 메모리를 고려한다.
- 접근성 옵션이 visual identity를 파괴하지 않도록 초기부터 설계한다.
- 용량 최적화는 `size_quality_class`와 실제 screen coverage를 사용하며 모든 자산에 동일 resolution·compression을 강제하지 않는다.
- 폰트·texture·animation 압축으로 용량을 줄였으면 실제 장면에서 visual identity·가독성·silhouette·contact timing을 다시 검증한다.

## 14. 실패 조건

- Art Direction을 이미지 검색 결과 모음으로 대체함
- 키워드만 있고 관찰 가능한 Visual Pillar가 없음
- Concept 이미지를 Art Bible·Asset Specification 없이 대량 제작함
- 큰 일러스트만 보고 실제 인게임 가독성을 검증하지 않음
- 배경·캐릭터·UI·VFX가 같은 위치·명도·채도를 경쟁함
- 생성 이미지의 원출처·권리·유사성·승인 상태가 없음
- 첫 자산 하나만 만들고 반복 제작 가능성을 통과 처리함
- 성능·접근성·플랫폼 제약을 구현 후반으로 미룸
- 승인 이미지가 있는데 별도 지시 없이 교체함
- 용량 절감을 이유로 HERO/GAMEPLAY_CRITICAL 품질 저하를 증거 없이 승인함
- PC와 Android에 동일 texture import profile을 무조건 강제함

## 15. Output Contract

```md
## 플레이어 경험·정보 역할·시장 첫인상
## Visual Pillar·포함·금지 예시
## Shape Language·실루엣·Color·Value·Composition
## 시각적 위계·마스코트·상징
## Concept Exploration 후보 비교
## Art Bible 결정
## Asset Specification·경로·규격·Import·size quality profile
## 캐릭터·환경·UI·VFX·Animation 연결
## 실제 인게임 캡처·최적화 전후 품질·Runtime Asset Approval
## 원출처·라이선스·유사성·승인 원장
## 반복 생산성·두 번째 같은 유형의 자산
## 접근성·성능·미검증·다음 결정
```
