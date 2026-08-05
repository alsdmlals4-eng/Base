# 기술 기획·프로덕션·출시 Guide

## 1. 목적

이 Guide는 게임 기획을 실제 Godot 프로젝트, 반복 가능한 콘텐츠 제작 파이프라인, 목표 플랫폼 성능·접근성, 출시 전후 증거로 연결한다.

기술은 플레이어 경험과 분리된 구현 세부가 아니다.

```text
플레이어 경험
→ 시스템·정보·콘텐츠 요구
→ Godot·데이터·저장·플랫폼 계약
→ 제작 파이프라인·품질 기준
→ Vertical Slice
→ 목표 기기·플랫폼 검증
→ 출시 약속·플레이어 반응
→ 다음 기획 결정
```

실행 책임은 프로젝트 Engineering Skill, `designing-vertical-slices`, `evaluating-godot-assets-and-plugins-before-creation`, `diagnosing-game-engine-runtime-failures`, `reviewing-and-validating-project-changes`가 가진다.

공식 참고:

- Godot multiple resolutions 문서는 base resolution과 stretch mode·aspect가 화면 크기와 렌더링에 미치는 차이를 설명한다: https://docs.godotengine.org/en/latest/tutorials/rendering/multiple_resolutions.html
- Android 게임 최적화 문서는 GPU·CPU·메모리·열·기기별 병목을 측정하는 도구와 API를 제공한다: https://developer.android.com/games/optimize/overview
- Steam Playtest는 본 게임과 분리된 AppID로 테스트 접근과 데이터를 운영할 수 있다: https://partner.steamgames.com/doc/features/playtest
- Steam User Reviews는 제품이 플레이어 기대와 얼마나 맞았는지 파악하는 피드백 채널 중 하나다: https://partner.steamgames.com/doc/store/reviews

## 2. 기술 기획 질문

기능 구현 전에 다음을 작성한다.

```yaml
player_value:
critical_play_flow:
target_platforms_devices:
engine_and_version:
input_methods:
base_resolution_and_aspect:
data_and_save_ownership:
performance_budget:
accessibility_barriers:
content_volume_and_repetition:
asset_plugin_dependency:
validation_environment:
rollback_and_migration:
```

필수 질문:

- 플레이어 경험을 만들기 위해 꼭 필요한 상태·입력·피드백은 무엇인가?
- 무엇이 코어 규칙이고 무엇이 표현·UI·도구인가?
- 어떤 상태를 누가 단일 책임 원본으로 소유하는가?
- 저장·불러오기·버전 이관이 필요한가?
- 목표 PC·모바일 기기에서 가장 위험한 장면은 무엇인가?
- 사람 입력·플랫폼·네트워크·외부 에셋이 실패하면 어떻게 복구하는가?
- 같은 유형의 두 번째 콘텐츠를 만들 수 있는 구조인가?

## 3. Godot 책임 경계

### Scene

`Scene`은 재사용 가능한 노드 구성·화면·게임플레이 단위를 표현한다.

검수:

- Scene의 목적과 진입점이 명확한가?
- 게임 규칙·UI·데이터 책임이 한 Scene에 뒤섞였는가?
- 상위 Scene이 하위 구현 세부를 과도하게 아는가?
- 교체·테스트 가능한 경계가 있는가?
- 인스턴스마다 달라지는 값과 공용 정적 데이터가 분리됐는가?

### Resource

`Resource`는 재사용 가능한 설정·정적 데이터·자산 참조에 적합하다.

- 런타임 상태를 실수로 공용 Resource에 공유하지 않는다.
- inspector 편의와 정본 데이터 계약을 혼동하지 않는다.
- JSON·Resource·Script 기본값 중 누가 수치를 소유하는지 정한다.
- 저장할 값과 다시 계산할 값을 분리한다.

### Autoload

`Autoload`는 여러 Scene이 반드시 공유해야 하는 서비스·상태에만 사용한다.

후보:

- 저장 서비스
- Scene 전환
- 전역 설정
- 오디오 라우팅
- 앱 생명주기

피해야 할 사용:

- 모든 게임 규칙을 전역 관리자 하나에 모음
- UI가 Autoload 상태를 직접 수정
- 테스트 격리가 불가능한 숨은 의존성
- 같은 상태를 Scene과 Autoload가 동시에 소유

### 데이터 책임 경계

```text
정적 정의
→ JSON / Resource / canonical data

런타임 상태
→ Run/Session/Model object

영구 상태
→ Save Schema

표현 상태
→ UI/ViewModel
```

UI는 표시 데이터를 받아 사용자 의도를 반환하며 코어 규칙을 직접 계산하지 않는다.

## 4. 저장 Schema와 마이그레이션

`저장 Schema`는 단순 Dictionary가 아니라 제품 호환성 계약이다.

```yaml
schema_version:
required_fields:
optional_fields:
defaults:
value_constraints:
source_of_truth:
migration_from:
rollback_or_backup:
corruption_handling:
```

규칙:

- 필드 추가 이유와 소비자를 기록한다.
- 누락 필드·구형 값·잘못된 타입을 처리한다.
- 기존 저장을 자동 덮어쓰기 전에 백업·복구 경로를 둔다.
- 같은 값을 여러 위치에 중복 저장하지 않는다.
- 계산 가능한 캐시와 영구 결정을 구분한다.
- 마이그레이션 테스트는 대표·최소·최대·손상 데이터를 포함한다.
- 저장 성공과 실제 플레이 복구 성공을 분리한다.

## 5. 결정론·재현성·디버그

전략·룰렛·밸런스·지연 결과처럼 재현이 중요한 시스템은 `결정론` 계약을 둔다.

```yaml
seed_source:
input_sequence:
clock_dependency:
random_streams:
snapshot_boundary:
expected_result:
replay_or_debug_record:
```

- 랜덤 생성기와 시간·프레임 의존성을 분리한다.
- 테스트에서 seed·입력·버전을 기록한다.
- UI 애니메이션과 도메인 판정을 분리한다.
- 실제 결과를 immutable snapshot으로 남길 필요가 있는지 판정한다.
- 실패를 재현할 개발자 패널·로그·상태 dump를 준비한다.

디버그 도구가 제품 규칙을 대신 소유하지 않게 한다.

## 6. 화면·해상도·입력

### base resolution

`base resolution`은 기획·아트·UI가 공유하는 논리 화면 기준이다.

```yaml
base_resolution:
orientation:
minimum_supported_aspect:
maximum_supported_aspect:
stretch_mode:
stretch_aspect:
safe_area:
ui_scale_policy:
asset_density:
```

Godot의 stretch mode는 base size를 실제 화면에 어떻게 맞출지 정한다. `Canvas Items`와 `Viewport`는 2D 렌더링·스케일링 결과가 다르므로 실제 프로젝트 목표에 맞춰 선택하고 여러 비율로 확인한다.

### aspect ratio

`aspect ratio`가 달라질 때 다음을 정의한다.

- 늘어나는 플레이 공간
- letterbox·pillarbox
- UI anchor와 margin
- 카메라 노출 범위
- 터치·자막·팝업 안전 영역
- 배경 자산 확장·crop
- 정보 우선순위

### UI scale

`UI scale`은 해상도 숫자 하나로 해결되지 않는다.

- 실제 화면 크기와 viewing distance
- 텍스트·아이콘 최소 크기
- touch target
- DPI·OS scale
- Steam Deck·노트북·모바일·고해상도 모니터
- 언어별 텍스트 팽창

### 터치·키보드·마우스·패드

`터치·키보드·마우스·패드`는 입력 장치가 아니라 플레이 방식이다.

검수:

- 모든 핵심 행동이 장치에 맞는가?
- hover가 없는 터치에서 정보가 사라지지 않는가?
- 손가락이 핵심 결과를 가리지 않는가?
- 키보드·패드 focus가 예측 가능한가?
- hold·rapid press·복합 입력 대안이 있는가?
- 취소·undo·확인 경로가 있는가?
- 장치 전환 시 prompt와 focus가 갱신되는가?

Microsoft XAG는 다양한 입력 방식과 대체 디지털 입력을 고려하도록 권장한다: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107

## 7. 접근성

접근성은 옵션 개수가 아니라 실제 플레이 장벽과 대안이다.

검토 영역:

- 텍스트·대비·명도
- 색 외 정보 채널
- 자막·caption·중요 효과음
- 입력 재지정·hold·연타·복합 입력
- UI navigation·focus·context
- 시간 제한·일시정지·연장
- 난이도·도움·실패 복구
- camera shake·motion·flashing
- 오디오 채널별 음량

Microsoft XAG는 핵심 시각·음향 신호를 여러 감각 채널로 제공하고, 일관된 UI navigation과 focus를 유지하며, motion을 조절할 수 있게 하는 가드레일을 제공한다:

- https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103
- https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/112
- https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/113
- https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/117

이 가이드는 법적 준수 인증이 아니다. 프로젝트의 실제 플레이 경로와 목표 플랫폼에서 검증한다.

## 8. 성능 예산

평균 FPS 하나로 통과시키지 않는다.

```yaml
platform_device:
build_version:
representative_scene:
worst_case_scene:
frame_time_target_ms:
cpu_budget:
gpu_budget:
memory_budget:
loading_budget:
network_budget:
thermal_and_battery:
baseline_capture:
measurement_tool:
```

### frame time

`frame time`은 FPS보다 병목과 변동을 분석하기 좋다.

- 평균
- 95/99 percentile
- 긴 hitch
- Scene 전환
- shader compilation
- asset loading
- garbage collection

### CPU·GPU·메모리

`CPU·GPU·메모리`를 분리한다.

- script·physics·AI·pathfinding
- draw calls·overdraw·shader·particles
- texture·audio·mesh·runtime allocation
- peak와 지속 사용량
- memory pressure와 crash/LMK

### 로딩·발열

`로딩·발열`은 특히 모바일에서 플레이 경험을 바꾼다.

- 첫 실행·재실행·Scene 전환
- background/foreground 복귀
- 장시간 플레이 후 thermal throttling
- battery mode와 성능 mode
- 저사양 기기 quality tier

Android 공식 문서는 AGI·APT·ADPF·Memory Advice·Perfetto 등으로 지속 가능한 성능과 기기별 병목을 분석하도록 안내한다: https://developer.android.com/games/optimize/overview

## 9. 에셋·플러그인·외부 의존성

직접 만들기 전에 다음 순서로 평가한다.

```text
Godot 기본 기능
→ 프로젝트에 이미 채택된 도구
→ 무료·오픈소스
→ 상용 에셋·플러그인
→ 직접 제작
```

평가표:

```yaml
need_and_player_value:
core_or_support:
source_and_license:
maintenance_activity:
godot_version_compatibility:
platform_support:
performance_cost:
security_and_network:
export_support:
data_ownership:
customization_cost:
replacement_and_rollback:
```

코어 판단·게임 데이터·결정론 규칙을 검증 불가능한 외부 플러그인에 맡기지 않는다. 보조 도구는 채택할 수 있지만 제거·교체 seam을 둔다.

자산의 직접 포함, 참조 기반 독립 제작, AI·외주와 출시 권리 기준은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`가 책임진다. 상업 사용, `distribution_in_game_build`, 원본 재배포, 수정, attribution·NOTICE와 `REFERENCE_TO_ORIGINAL`을 분리하고 미확인은 `RELEASE_BLOCKED_UNVERIFIED`로 유지한다.

## 10. 프로덕션 구조

### 결과 단위 분해

활동이 아니라 검증 가능한 결과로 나눈다.

```yaml
outcome:
why_now:
inputs:
files_or_systems:
dependencies:
protected_scope:
output:
acceptance_criteria:
validation:
rollback:
```

### 의존성

- `BLOCKS`
- `INFORMS`
- `USES_OUTPUT`
- `SHARES_RESOURCE`
- `VALIDATES`
- `OPTIONAL_FOLLOWUP`

같은 파일·Schema·상태·자산을 동시에 수정하는 작업을 무조건 병렬화하지 않는다.

### 범위 최적화

```text
REMOVE
→ REDUCE
→ MERGE
→ CLARIFY
→ AUTOMATE
→ ADD
```

자동화는 혼란스러운 수동 과정을 그대로 자동화하기 전에 책임·입력·출력·오류를 정리한다.

## 11. Vertical Slice와 반복 제작성

`Vertical Slice`는 대표 플레이 구간과 목표 품질뿐 아니라 제작 파이프라인을 증명한다.

검증:

- 처음부터 끝까지 플레이 가능한가?
- 핵심 세일즈포인트와 일반 반복 플레이가 함께 있는가?
- 최종 방향에 가까운 아트·UI·사운드인가?
- 저장·복구·오류 경로가 있는가?
- 접근성·성능 예산을 확인했는가?
- 외부 플레이어 행동·자기보고를 수집했는가?
- 같은 유형의 두 번째 콘텐츠를 만들 수 있는가?

### 두 번째 콘텐츠

`두 번째 콘텐츠`는 다음을 검증한다.

- 데이터·Scene·Asset Specification을 재사용할 수 있는가?
- 새 ID·수치·자산을 추가할 때 정본과 소비자가 명확한가?
- 수동 복사·숨은 규칙·개인 기억에 의존하는가?
- 제작·리뷰·수정·QA 시간이 반복 가능한가?
- 자동화가 실제 병목을 줄이는가?

두 번째 콘텐츠를 만들 수 없다면 Prototype 성공이지 Production proof가 아니다.

## 12. QA와 완료 증거

```text
작업 계약·baseline
→ actual diff
→ 정본·경로·ID·Schema reference freshness
→ 포맷·문법·정적 검사
→ 자동 테스트
→ Godot import·runtime·render·save
→ 접근성
→ 목표 플랫폼 성능
→ 정상·실패·경계·회귀
→ 사람 플레이·결과 보고
```

구분:

- 파일 존재
- 정적 검사 통과
- CI 통과
- Godot 실행
- 목표 기기 실행
- 접근성 검토
- 성능 프로파일
- 사람 플레이 재미
- 출시 준비

각각 다른 증거다.

## 13. 출시 전 Store 약속

Store page·capsule·trailer·tag·description은 마케팅 장식이 아니라 플레이어 약속이다.

```text
Store 약속
→ Demo·Playtest 첫 경험
→ 실제 제품 플레이
→ User Reviews·지원 요청
→ 약속 일치·불일치 분석
```

검수:

- 첫 이미지와 trailer 초반이 실제 핵심 플레이를 보여 주는가?
- 태그·문구·장르 약속이 실제 제품과 맞는가?
- 대표 하이라이트가 일반 플레이처럼 오해되지 않는가?
- 미구현·미확정 기능을 약속하지 않는가?
- 목표 언어·플랫폼 정보가 정확한가?
- Accessibility·시스템 요구사항·입력 지원이 실제와 맞는가?

## 14. Steam Playtest·User Reviews·Wishlist

### Steam Playtest

`Steam Playtest`는 본 게임의 review·wishlist를 방해하지 않고 별도 AppID로 테스트 접근을 관리할 수 있다.

그러나 기능 존재만으로 플레이테스트가 성립하지 않는다.

- 연구 질문
- build/version
- 참가자 집단
- 접근 규모
- 피드백 채널
- 행동 이벤트
- 성공·실패 기준
- 종료·비활성 시점

을 별도로 계약한다.

### User Reviews

`User Reviews`는 기대 일치·버그·가치·커뮤니티 경험을 이해하는 채널이다.

- 최근/전체
- playtime
- 구매/키/무료
- Early Access·pre-release
- patch 전후
- 언어·지역
- off-topic·review bomb 가능성

을 구분한다. 리뷰만으로 모든 플레이어 행동을 대표하거나 제품 우선순위를 자동 결정하지 않는다.

### Wishlist

`Wishlist`는 관심 신호와 release/discount/demo notification surface지만 판매 예측 공식이 아니다. Steamworks도 사람마다 wishlisting 이유가 달라 정확한 판매 예측 공식이 없다고 설명한다: https://partner.steamgames.com/doc/marketing/wishlist

Wishlist 분석:

- Store page 공개 시점
- capsule·trailer·event·festival 변화
- 지역·언어
- 유입·impression·visit
- additions·deletions
- demo/playtest 이후 변화
- 실제 purchase와 cohort

## 15. Google Play 테스트

`Google Play 테스트`는 내부·비공개·공개 테스트와 출시 track을 제품 단계에 맞게 사용한다.

프로젝트 적용 시 다음을 공식 출처로 재검증한다.

- 계정·앱 등록 요건
- target API와 정책
- 테스트 참가자·기간 요건
- Android App Bundle
- Data Safety·privacy
- device catalog·pre-launch report
- 결제·광고·가족 정책

모바일 검증:

- 실제 Android 기기
- 화면 비율·안전 영역
- touch·back·pause·resume
- 설치·업데이트·저장
- 성능·메모리·로딩·발열
- offline·network error
- 접근성 서비스

에디터·에뮬레이터·CI만으로 실기기 검증을 통과 처리하지 않는다.

## 15.1 등급·설문·자산 권리 출시 Gate

Steam·STOVE·Google Play의 콘텐츠 등급·설문·target audience와 실제 build·store·trailer·screenshot 일치는 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`를 따른다.

기본 전략은 `LOWEST_VIABLE_RATING`과 `AVOID_ADULTS_ONLY`다. 전체이용가를 강제하지 않고 프로젝트 핵심 경험을 보존하되 청소년이용불가·18+를 기본 회피한다. 콘텐츠 등급과 Google Play target audience는 별도 필드다.

프로젝트는 다음을 유지한다.

- `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`

필수 권리, 참조 독립 제작, questionnaire version 또는 build·store 일치가 확인되지 않으면 `RELEASE_BLOCKED_UNVERIFIED`다.

## 16. 출시 후 학습

```text
출시 build
→ crash·performance·funnel
→ User Reviews·support·community
→ 기대와 실제 경험
→ hotfix·update 가설
→ 검증
→ patch notes·정본·Learning Log
```

- crash·저장 손상·결제·진행 차단을 우선한다.
- 소수의 큰 목소리와 넓은 행동 신호를 분리한다.
- 리뷰에 방어적으로 반응하지 않는다.
- 업데이트가 코어·튜토리얼·밸런스·저장에 미치는 회귀를 검증한다.
- 출시 후 성공 사례도 한 번의 관찰로 Base 강제 규칙으로 승격하지 않는다.

## 17. 최신성

플랫폼 정책·요금·SDK·API·Store UI·알고리즘·검토 기간은 바뀔 수 있다. 적용 직전에 반드시 **공식 출처로 재검증**하고 확인일·버전·지역·계정 조건을 기록한다.

## 18. 실패 조건

- 플레이어 가치 없이 기술 스택부터 결정함
- Scene·Resource·Autoload가 같은 상태를 중복 소유함
- UI가 게임 규칙을 직접 계산함
- 저장 Schema 변경에 마이그레이션·백업·회귀가 없음
- 평균 FPS·에디터 빈 장면만으로 성능을 통과함
- 모바일을 에뮬레이터만으로 검증함
- 첫 콘텐츠 하나로 반복 제작성을 증명했다고 주장함
- 플러그인의 유지·라이선스·교체 경로를 확인하지 않음
- Store page가 실제 플레이와 다른 약속을 함
- Wishlist·review·설문 하나를 매출·재미·행동 전체로 해석함
- 오래된 플랫폼 정책을 현재 사실로 사용함
- 전체이용가를 모든 프로젝트에 강제하거나 등급 설문에서 콘텐츠를 숨김
- 참조 원본 또는 권리 미확인 자산을 shipping build에 포함함

## 19. Output Contract

```md
## 플레이어 가치·핵심 플레이 흐름
## Godot Scene / Resource / Autoload / 데이터 책임 경계
## 저장 Schema·마이그레이션·결정론·디버그
## PC·모바일·base resolution·aspect ratio·UI scale
## 터치·키보드·마우스·패드·접근성
## frame time·CPU·GPU·메모리·로딩·발열
## 에셋·플러그인·라이선스·교체 경로
## 참조 기반 독립 제작·자산 권리 증거
## 작업 분해·의존성·반복 제작성
## Vertical Slice·두 번째 콘텐츠
## QA·자동·런타임·목표 기기 증거
## Store 약속·Steam Playtest·User Reviews·Wishlist
## Steam·STOVE·Google Play 등급·설문·target audience
## Google Play 테스트·공식 출처 재검증
## 출시 후 학습·미검증·롤백
```
