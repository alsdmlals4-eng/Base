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

## 10. 화면·페이지·탭·스킨 제작 준비의 채택과 재개

`UI_SURFACE_PRODUCTION_READINESS`

화면·메뉴·페이지·탭·시스템 창·대화창·프레임·스킨을 기획, 제작, 구현 또는 검수할 때는
[ui-surface-production-readiness.md](ui-surface-production-readiness.md)를 먼저 읽고
외부 벤치마크 → 후보 구조 → 프로젝트 정합화 → 개별 모듈 제작·조합 순서로 진행하며
기존 `flow-and-information-architecture / design-system-contract / godot-ui-contract / runtime-ui-audit`에 결합한다.
새 Skill이나 두 번째 UI 정본을 만들지 않는다. 승인 목표의 미구현 surface도 준비·누락 검사에 포함한다.

프로젝트 반영은 최신 AGENTS가 사용하는 existing owner/overlay에 채택 source commit,
기존 UI·화면·자산·capture owner, 적용 scope, 보호된 고유 결정과 다음 실제 작업을 연결한다.
기존 Base version lock과 generated adapter는 임의로 교체하지 않는다. 미병합 PR은 적용 완료가 아니다.
새 채팅의 cold-start에서 entrypoint → 채택 reference → 실제 owner를 따라 readback한 뒤 적용 완료를 보고한다.
문서·라우팅 검증과 실제 메뉴 동작·이미지 생성·사용자 승인·Godot capture는 별도 상태로 유지한다.
