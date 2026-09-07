# Godot Asset·Plugin Source Catalog

- 기준 확인일: `2026-07-25`
- 목적: Godot 기능·에셋·플러그인을 직접 제작하기 전에 검색할 원본과 검증 순서를 제공한다.
- 주의: 가격, 라이선스, Godot 호환 버전, 판매 상태는 바뀔 수 있으므로 채택 시점에 다시 확인한다.

## 0. 현재 사용자 PC의 로컬 참고 라이브러리

외부 검색 전에 현재 프로젝트·Base 현행 상태를 먼저 확인하고, 관련성이 있으면 다음 로컬 참고 라이브러리를 확인한다.

```text
C:\Users\user\Documents\GitHub\Godot_Reference
```

역할은 `LOCAL_TEMPLATE_AND_OFFICIAL_DEMO_REFERENCE_LIBRARY`이며 세부 경계는 `docs/knowledge/godot/LOCAL_GODOT_REFERENCE_LIBRARY.md`가 책임진다.

```text
현재 프로젝트·Base 현행 구현
→ Local Godot Reference Library
→ Godot 공식 문서·Store·Asset Library·upstream 원본
```

- 현재 등록된 공식 데모 참고 코퍼스에 `godot-demo-projects-master`가 포함된다. upstream은 `godotengine/godot-demo-projects`이며 기본 상태는 `REFERENCE_ONLY`다.
- `godot-demo-projects-master`의 예제는 엔진 네이티브 구현 패턴 탐색에 활용하되, 로컬 폴더명의 `master`를 exact upstream version으로 간주하지 않는다. 실제 채택 시 commit/tag와 현재 Godot 버전 호환성을 다시 검증한다.
- 이 경로는 현재 사용자 Windows PC 전용이며 다른 PC·CI·원격 agent의 필수 경로가 아니다.
- 경로가 없거나 접근할 수 없으면 `UNAVAILABLE_LOCAL_REFERENCE`로 두고 정상 외부 검색을 계속한다.
- 템플릿·공식 데모·플러그인 원본은 기본 `REFERENCE_ONLY`다. 다운로드 또는 폴더 존재만으로 프로젝트 채택을 선언하지 않는다.
- 실제 채택 전에는 exact version, Godot 호환성, 원본 source, 라이선스, 현재 유지보수 상태, consumption path, 제거·rollback을 다시 확인한다.
- 템플릿 전체 복사보다 현재 프로젝트에 필요한 패턴·컴포넌트의 선택적 `REUSE / ABSORB / REFACTOR`를 우선 검토한다.
- 로컬 참고 라이브러리 전체를 Base 또는 게임 프로젝트 저장소에 복제하지 않는다.

## 1. 필수 검색 소스

| 우선 | 소스 | 주소 | 주 용도 | 검증 포인트 |
|---|---|---|---|---|
| 1 | Godot 공식 문서 | https://docs.godotengine.org/ | 엔진 기본 기능·API·플러그인 설치 방식 | 프로젝트 Godot 버전 문서를 선택했는가 |
| 2 | Godot Asset Store | https://store.godotengine.org/ | 공식 신규 에셋 탐색 | 2026-07 기준 무료 자산 중심이며 유료 판매 기능은 재확인 필요 |
| 3 | Godot Asset Library | https://godotengine.org/asset-library/asset | 기존 무료 애드온·데모·도구 | 신규 Store로 자동 이전되지 않은 자산이 있어 전환 기간 함께 검색 |
| 4 | GitHub Godot addon topic | https://github.com/topics/godot-addon | 오픈소스 애드온·소스·Release | 기본 브랜치보다 안정 Release·태그, 라이선스, 최근 이슈를 우선 확인 |
| 5 | itch.io Godot assets | https://itch.io/game-assets/tag-godot | 2D·3D 아트, UI, 오디오, 템플릿 | 상업 사용·수정·재배포·크레딧 조건을 상품별 확인 |
| 6 | itch.io Godot tools | https://itch.io/tools/tag-godot | 에디터 도구·상용 플러그인·제작 툴 | 지원 Godot 버전, 업데이트 권리, 환불·지원 범위 확인 |
| 7 | 제작자 공식 사이트 | 후보의 README·Store 페이지에서 연결 | 공식 문서·라이선스·지원·결제 | 제3자 재판매 페이지보다 제작자 원본 우선 |
| 8 | Godot Foundry | https://godot-foundry.com/ | Godot 전문 제3자 마켓 후보 탐색 | 공식 Godot 재단 마켓으로 오인하지 말고 판매자·라이선스·지원 검증 |

## 2. 공식 Store와 기존 Asset Library 병행 규칙

공식 Godot Asset Store가 열렸더라도 기존 Asset Library 자산이 모두 자동 이전된 것은 아니다. 검색 누락을 줄이기 위해 다음을 함께 수행한다.

```text
Godot Asset Store 검색
+ 기존 Asset Library 동일 키워드 검색
+ GitHub 원본·Release·라이선스 대조
```

Asset Store 또는 Asset Library의 등록 정보만으로 유지보수와 상업 사용을 확정하지 않는다. 제작자 저장소와 라이선스 원문을 확인한다.

## 3. 검색 쿼리 템플릿

### 일반 기능

```text
Godot 4.7 <기능명> addon
Godot 4 <기능명> plugin release
site:store.godotengine.org <기능명>
site:godotengine.org/asset-library <기능명>
site:github.com <기능명> godot addon
site:itch.io <기능명> Godot plugin
```

### 프로젝트 유형별

```text
Godot dialogue editor branching localization
Godot card game framework deck hand tooltip
Godot inventory crafting save system addon
Godot behavior tree state machine addon
Godot Android safe area billing analytics plugin
Godot visual novel timeline dialogue plugin
Godot 2D shader pixel art VFX pack
Godot UI theme icon pack commercial license
```

### 버전·유지보수 확인

```text
<후보명> Godot 4.7 compatibility
<후보명> releases changelog migration
<후보명> license commercial use
<후보명> issues Godot 4.7
<후보명> uninstall migration save format
```

## 4. 후보 기록 최소 필드

```yaml
candidate_name:
category:
source_url:
creator:
checked_at:
version:
supported_godot_versions:
platforms:
license:
price_and_purchase_model:
source_available:
latest_release:
maintenance_signal:
dependencies:
data_and_save_ownership:
version_control_impact:
removal_plan:
security_and_privacy:
project_fit:
decision: ADOPT | ADAPT | TRIAL | REJECT | BUILD_CUSTOM | DEFER | UNVERIFIED
reason:
validation:
```

## 5. 구매·설치 안전 규칙

- 조사와 구매·설치는 별개다.
- 사용자 승인 없이 유료 구매, 계정 연결, API 키 발급, 네이티브 SDK 설치를 수행하지 않는다.
- 프로젝트 브랜치에 바로 설치하지 않고 가능한 경우 샘플 프로젝트나 격리 브랜치에서 시험한다.
- `addons/`, Autoload, Project Settings, import 설정, Android plugin, 빌드 템플릿 변경을 기록한다.
- 채택된 제3자 자산은 버전·원본·라이선스·수정 내역·크레딧·제거 방법을 프로젝트의 제3자 기록에 남긴다.

## 6. 프로젝트별 기본 검색 초점

| 프로젝트 | 먼저 찾을 범주 |
|---|---|
| Ten-Paces-Hidden-Moves | 카드 UI·툴팁·턴/행동 시퀀스·그리드·전투 로그·테스트 보조 |
| Blacksmith | 모바일 UI·Safe Area·인벤토리·제작 데이터·Android 빌드·터치 피드백 |
| urban-legend | 대화·분기·로컬라이제이션·타임라인·조사 기록 UI·오디오 이벤트 |
| omenward | 룰렛·결정론 테스트·3라인 전투·상태 머신·디버그 시각화·데이터 검증 |

이 표는 검색 우선순위이며 자동 채택 목록이 아니다. 각 프로젝트의 코어 경험과 실제 구현 상태를 먼저 확인한다.

## 7. 외부 Agent·CLI·Skill·Workspace 후보

Godot addon 범위를 넘어 코드 리뷰 도구, 출력 압축 프록시, 외부 모델 CLI, 에이전트 Skill·hook, 통합 workspace를 평가할 때도 이 Skill의 현재 환경 인벤토리·중복 권위·비용·라이선스·보안·제거 가능성 Gate를 재사용한다.

- 2026-08-31 후보 10종의 원문 대조와 `ADOPT / ADAPT / TRIAL_OPTIONAL / REFERENCE_ONLY / REJECT_AS_REQUIRED_DEPENDENCY` 판정: `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_TOOL_ADOPTION_REVIEW_2026-08-31.md`
- 선택형 외부 reviewer·output proxy·model CLI·agent workspace의 권위·원문 fallback·비용·비밀·실행 안전·킬 스위치 계약: `docs/knowledge/ai/agent-tools/EXTERNAL_AGENT_ADAPTER_CONTRACT.md`

이 두 문서는 새 실행 권위나 설치 승인이 아니다. 후보의 버전·라이선스·가격·telemetry·auth·model·hook·출력 의미가 바뀌거나 프로젝트별 A/B 결과가 달라지면 현재 1차 자료로 재검증한다. ordinary Godot 에셋 검색에서는 불필요하게 로드하지 않는다.

## 8. 2D 캐릭터 애니메이션·리깅 Route

2D 캐릭터·생물·초상·전투 유닛의 제작 방식을 정할 때는 특정 제품 검색 전에 다음 active reference를 읽는다.

- `skills/evaluating-godot-assets-and-plugins-before-creation/references/2d-character-animation-routing-and-rigging.md`
- 프로젝트 기록 Template: `templates/planning/2D_CHARACTER_ANIMATION_ROUTE_RECORD.md`

```text
actual consumer + current implementation
→ FRAME / GODOT_NATIVE_RIG / EXTERNAL_RIG_RUNTIME / EXTERNAL_RIG_BAKED
→ same-axis comparison
→ selected route + rejected-route reasons
→ isolated trial when required
→ exact version / license / platform / performance / rollback evidence
```

검색 예시:

```text
Godot 4.7 Skeleton2D Bone2D Polygon2D official
Godot 4.7 2D skeletal animation runtime GDExtension
<후보명> Godot exact version GDExtension release
<후보명> editor runtime version compatibility
<후보명> runtime license game distribution
<후보명> Android Windows export performance removal
```

유명세나 부드러운 보간만으로 외부 runtime을 채택하지 않는다. 프레임·Godot native rig·external runtime·rig-to-baked를 실제 consumer, 화면 크기, 동시 개체, 상태·방향·Skin·Attachment 수, 실루엣, 플랫폼, 성능, 라이선스, 업데이트, 제거 비용으로 비교한다. 외부 tool trial, 구매, 설치, production adoption, 모든 프로젝트 rollout은 서로 다른 승인·증거 상태다.
