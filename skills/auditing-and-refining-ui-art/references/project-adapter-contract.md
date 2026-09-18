# 프로젝트 UX/UI 어댑터 계약

## 1. 목적

Base 공용 UX/UI Skill과 reference를 프로젝트에 통째로 복제하지 않고, 프로젝트 코어·플랫폼·입력·책임 원본·검증 차이만 얇게 연결한다.

## 2. 적용 유형

### A. 기존 프로젝트 UX Skill이 있는 경우

기존 Skill을 유지하고 다음을 추가한다.

- Base Skill ID: `auditing-and-refining-ui-art`
- 사용하는 Base Skill Mode
- 프로젝트 고유 책임과 공용 책임의 경계
- 프로젝트 정본·실제 UI 경로
- 프로젝트 패턴 프로필
- 프로젝트 해상도·입력·접근성·사람 검증 상태

새 중복 Skill을 만들지 않는다.

### B. 기존 UX/UI 책임 원본만 있는 경우

현행 원본에 공용 패턴 ID·Godot 계약·검증 매트릭스를 추가한다. 문서가 지나치게 커지거나 질문의 권한이 분리될 때만 별도 프로젝트 UX/UI 원본을 만든다.

### C. 기존 UX Skill과 책임 원본이 모두 없는 경우

`templates/planning/GAME_UX_UI_SYSTEM.md`를 프로젝트 경로와 문서 체계에 맞게 한 번 설치하고 Documentation Map·Registry·Base adapter에서 연결한다.

## 3. 프로젝트 어댑터 필드

```yaml
base:
  repository: alsdmlals4-eng/Base
  commit:
  skill_id: auditing-and-refining-ui-art
  base_path: skills/auditing-and-refining-ui-art/SKILL.md
  modes:
project:
  repository:
  canonical_ux_ui_source:
  project_skill:
  target_platform:
  minimum_resolution:
  target_resolution:
  input_devices:
project_patterns:
  adopt:
  adapt:
  avoid:
  test:
  ignore:
protected:
  project_core:
  domain_state_owners:
  approved_assets:
  product_paths:
validation:
  static:
  runtime:
  device:
  human:
```

JSON adapter가 이미 있으면 해당 구조를 그대로 유지하고 `shared_skill_overrides` 또는 같은 역할의 기존 필드에 최소 정보를 추가한다. 새 schema를 강제하지 않는다.

## 4. 프로젝트 책임 원본 필수 항목

1. 프로젝트 UX 약속
2. 화면·플랫폼·입력 범위
3. 사용자 여정과 화면별 중심 질문
4. 정보 계층과 점진 공개
5. 적용·변환·기각·시험할 공용 패턴
6. 프로젝트 고유 패턴
7. 상태·피드백·입력·포커스
8. 접근성 장벽과 폴백
9. Godot UI 상태 소유·Signal·Theme·Container 계약
10. 자동·런타임·기기·사람 검증 상태
11. Base 승격 후보와 프로젝트 전용 유지 항목

## 5. 프로젝트 전용으로 남기는 것

- 캐릭터·세계관·기관·무공·마법 글자·괴이 규칙
- 실제 수치·확률·해상도·자원 이름
- Scene·script·data·asset 경로
- 승인 아트와 실제 캡처
- 실제 테스트·기기·플레이어 결과
- 프로젝트 고유 UI 상호작용과 상태 이름

## 6. Base로 승격 가능한 것

- 둘 이상의 프로젝트에서 반복된 UX 문제와 해결 패턴
- Godot 상태 소유·Signal·Theme·Container의 재사용 가능한 경계
- 정보 계층·점진 공개·복기·오류 복구 방법
- 접근성 장벽과 검증 방법
- 공식 레퍼런스의 채택·변환·기각 기준
- 검증 상태와 증거 분리 방법

프로젝트 이름·수치·실제 구현 결과를 제거해도 의미가 유지돼야 한다.

## 7. 동기화 순서

```text
Base UX/UI 변경 main 병합
→ Base main commit 재조회
→ 프로젝트 최신 main·열린 PR·최근 결정 확인
→ 기존 UX Skill/정본 선택
→ 프로젝트 adapter와 책임 원본 최소 갱신
→ Documentation Map·Registry·참조 최신성
→ 프로젝트 검증
→ PR 병합
→ 새 main에서 post-merge 적대적 검토
```

## 8. 금지

- Base Skill 본문을 프로젝트에 복사해 독립 수정.
- 프로젝트 구조를 Base 템플릿 경로에 맞춰 강제 이동.
- 기존 UX Skill을 확인하지 않고 새 Skill 추가.
- 공용 패턴을 프로젝트 코어보다 높은 권한으로 사용.
- 문서 반영을 런타임 구현·사람 검증 완료로 표시.
- Base commit만 바꾸고 프로젝트 책임 원본·라우팅 소비자를 갱신하지 않음.
- 제품 코드가 범위 밖인데 함께 수정.

## 9. 완료 판정

- 프로젝트의 같은 UX 질문에 현행 책임 원본 하나가 있다.
- Base commit과 Skill ID·mode가 실제 경로로 연결된다.
- 공용 원칙과 프로젝트 고유 결정이 구분된다.
- 기존 프로젝트 Skill·문서의 고유 기능이 보존된다.
- 제품 경로 변경 여부와 검증·미검증이 명시된다.
- 새 작업자가 프로젝트 저장소만으로 UX/UI 작업 시작점과 검증 경로를 찾을 수 있다.

## 10. 효과·비주얼·UI의 프로젝트별 연결

`PROJECT_PRESENTATION_BINDING`: [경험→표현 명세 가이드](experience-to-presentation-contract.md)는 Base 공용 작성 방법이다. 프로젝트 적용 시 기존 원본에 다음 차이만 연결한다.

| 기존 프로젝트 원본 | 연결할 프로젝트별 값 |
|---|---|
| 핵심 기획·Experience Intent | 해당 기능이 지킬 감정·판단·표현, 공개/숨김 정보와 승인 상태 |
| 시스템·데이터 | 규칙 효과의 trigger·대상·값·지속·중첩·실패와 state_owner |
| Art/Visual Bible·Asset Catalog | 보호할 시각 언어, 승인 자산·실제 슬롯·상태군·제작/승격 상태 |
| UX/UI·기능 Spec | 선택한 상태·입력·피드백, 실제 해상도/언어/설정, 반복·중단과 복귀 |
| 실제 코드·검증 owner | runtime_consumer·이벤트·구현 경로·대표 구간·기계/실행/사람 증거 |

하나의 `requirement_id`로 연결하고 `source_id + path + section` 참조를 우선한다. L1은 짧은 기존 기록으로 충분하며 L2만 필요한 상세 Spec/Packet을 쓴다. 고정 전투 예시·수치·색·타이밍·새 파일명을 프로젝트 전체에 복사하지 않는다.

Base main 채택 시 기존 adopted lock을 보존한 선택 동기화로 해당 절과 정확한 commit을 기록한다. 프로젝트 내부/정확한 Base commit 링크로 재연결하고 AGENTS/router → 기존 owner → 실제 consumer → 검증 위치를 readback한다. 경로가 계획뿐이면 `PLANNED`, 사람 결과는 `NOT_RUN`; 이 연결의 실제 채택 전에는 `PENDING_PROJECT_ADOPTION`이다. 템플릿·어댑터 변경이 게임 구현이나 재미 통과를 뜻하지 않는다.
