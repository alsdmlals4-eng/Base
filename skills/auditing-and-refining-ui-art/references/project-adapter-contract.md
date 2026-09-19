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

`PROJECT_PRESENTATION_BINDING`: [경험→표현 명세 가이드](../../../docs/knowledge/game-development/EXPERIENCE_TO_PRESENTATION_GUIDE.md)는 Base 공용 작성 방법이다. 프로젝트 적용 시 기존 원본에 다음 차이만 연결한다.

| 기존 프로젝트 원본 | 연결할 프로젝트별 값 |
|---|---|
| 핵심 기획·Experience Intent | 해당 기능이 지킬 감정·판단·표현, 공개/숨김 정보와 승인 상태 |
| 시스템·데이터 | 규칙 효과의 trigger·대상·값·지속·중첩·실패와 state_owner |
| Art/Visual Bible·Asset Catalog | 보호할 시각 언어, 승인 자산·실제 슬롯·상태군·제작/승격 상태 |
| UX/UI·기능 Spec | 선택한 상태·입력·피드백, 실제 해상도/언어/설정, 반복·중단과 복귀 |
| 실제 코드·검증 owner | runtime_consumer·이벤트·구현 경로·대표 구간·기계/실행/사람 증거 |

하나의 `requirement_id`로 연결하고 `source_id + path + section` 참조를 우선한다. L1은 짧은 기존 기록으로 충분하며 L2만 필요한 상세 Spec/Packet을 쓴다. 고정 전투 예시·수치·색·타이밍·새 파일명을 프로젝트 전체에 복사하지 않는다.

Base main 채택 시 기존 adopted lock을 보존한 선택 동기화로 해당 절과 정확한 commit을 기록한다. 프로젝트 내부/정확한 Base commit 링크로 재연결하고 AGENTS/router → 기존 owner → 실제 consumer → 검증 위치를 readback한다. 경로가 계획뿐이면 `PLANNED`, 사람 결과는 `NOT_RUN`; 이 연결의 실제 채택 전에는 `PENDING_PROJECT_ADOPTION`이다. 템플릿·어댑터 변경이 게임 구현이나 재미 통과를 뜻하지 않는다.

## 11. 프로젝트 작업에서의 재구체화와 교정 연결

`PROJECT_SPECIFIC_PRESENTATION_SPECIALIZATION`: Base는 공용 질문과 방법이고, 실제 기능 명세는 **프로젝트 작업 시 한 번 더 구체화**한다. §10의 원본 연결을 입력으로 다음 순서를 기존 작업 계약·기획·검증 기록에서 수행한다. 새로운 문서·상태 schema·승인 단계를 만들지 않는다.

| 순서 | 수행과 남길 연결 |
|---|---|
| 1. 프로젝트 fresh-read | 프로젝트 `AGENTS.md`의 read order로 승인된 경험·현재 기능·자산·입력·엔진 버전과 같은 Goal PR을 확인한다. 프로젝트 exact SHA와 해당 절의 채택 Base SHA를 구분하며 채택 lock을 조용히 교체하지 않는다. |
| 2. 조사·실무 비교 | 현재 구현·승인 자산·Base 재사용 자료를 먼저 비교하고 필요한 공식 문서·개발사 사례·플레이테스트 실무를 확인한다. `source_and_evidence`, 관찰된 방법, 프로젝트 차이와 `ADOPT / ADAPT / REJECT`를 기존 기록에 남긴다. 원문 미확인 해석은 근거로 승격하지 않고, 같은 조건의 유효한 조사는 `REUSED_EVIDENCE`로 재사용한다. |
| 3. 프로젝트 명세 | 같은 `requirement_id`에 경험·승인 원본, 규칙 효과의 `state_owner`, 표시할 정보와 보호할 비공개 정보, 실제 상태·입력·취소·복귀, 표현의 시점·강도·반복, 필요한 승인 자산·상태군을 연결한다. 조정할 값은 초기값·조정 기준·검증 장면을 정하고 미검증이면 `HYPOTHESIS`로 표시한다. `runtime_consumer`는 기존 경로와 새 구현 예정 경로(`PLANNED`)를 구별한다. |
| 4. 적대적 검토 | 프로젝트 정체성·이해·선택·감각·반복 피로·정보 누설·접근성·제작성·규칙/표현 권위를 공격하고 비판도 실제 근거로 재검증한다. 현행 adopted review owner와 같은 승인 계보의 전체 검토 예산을 재사용하며 단계마다 재초기화하지 않는다. 이후 finding은 영향 범위 교정·회귀로 처리한다. 독립 검토를 작성자 자체 검토로 대신하지 않는다. |
| 5. 구현·검증 | 현재 프로젝트가 허용한 실행자가 기존 승인 범위에서 명세→코드/Scene·데이터·자산→검증을 연결한다. 입력 연타·중단·복귀·설정 변경 등 관련 반례와 대표 플레이 구간을 확인한다. `DOC / MACHINE / RUNTIME / HUMAN`을 분리하고 관찰·자기보고·필요 로그를 대조한다. 사람 검증 미실행은 `NOT_RUN`이며 승인된 구현 전체를 순환 차단하지 않는다. |
| 6. 교정·연결 readback | 실패 원인별 최소 수정 후 해당 회귀와 정본·consumer를 다시 읽는다. `기존 Decision`·Active Context·검증 기록·학습 기록 중 실제 영향 owner만 갱신하고, 프로젝트 전용 교훈과 공용 후보를 구별한다. 채택·구현·검증·병합은 각각의 실제 상태로 보고한다. |

### 구체화와 연결 완료의 경계

- `REFERENCE_ONLY_NOT_SPECIFIED`: Base 링크나 `EXAMPLE_ONLY` 예시를 붙여두는 것만으로 기능이 `SPECIFIED`가 되지 않는다. 담당자가 구현할 상태·데이터/자산·consumer·실패 복구·판정 기준을 기존 원본 또는 명시적 계획에서 찾을 수 있어야 한다. 필요한 값은 수치 또는 확정 원본/계산식으로 해소한다. 필수 미정값(`TBD`)은 owner·영향·다음 행동을 남기고 그 의존 작업만 보류한다. 모든 수치를 Base에 고정하거나 무관한 작업까지 막지 않는다.
- `BIDIRECTIONAL_REQUIREMENT_TRACE`: **요구사항 → 구현·자산 → 검증**, **검증·화면 → 구현 → 요구사항·승인 원본**을 모두 따라간다. exact SHA에서 링크 대상·ID·절/record·실제 호출/표시 경로와 의미 일치를 확인한다. 핵심 경로가 존재하지만 호출되지 않거나 다른 요구사항을 검증하면 연결 완료가 아니다. 소비처를 아직 만들지 않았으면 `PLANNED`이지 구현 완료가 아니다.
- 기준/후보 증거는 각각 동일 revision의 코드·데이터·자산·테스트와 설정·입력·대표 상황에 묶는다. 예전 결과는 변경 영향과 유효성을 확인한 뒤 재사용하며, 문서 링크 검사 PASS를 runtime 연결·사람 경험·에이전트 준수 PASS로 올리지 않는다.
- L1 작은 작업은 기존 기록의 목적→상태/표현→consumer→확인 방법으로 위 순서를 축약할 수 있다. L0 비적용·유효 증거 재사용·프로젝트별 채택 경계는 §10과 공용 가이드를 유지한다. 핵심 경험·주요 UX·아트 방향·비용·범위·권한·보안 또는 파괴적 변경을 포함하는 교정은 `USER_DECISION_REQUIRED`로 분리한다. 실제 프로젝트 채택 전에는 `PENDING_PROJECT_ADOPTION`이다.
