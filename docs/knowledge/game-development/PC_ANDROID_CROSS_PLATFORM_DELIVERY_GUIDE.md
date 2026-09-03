# PC·Android 공용 코어·플랫폼 적응·단계 출시 Guide

## 1. 목적과 상태

이 Guide는 Godot 게임이 Windows PC와 Android 모바일을 함께 고려할 때 **어디까지 공용화하고, 어디부터 플랫폼별로 적응하며, 어떤 순서로 검증·출시할지** 결정한다.

기본 후보 상태는 다음과 같다.

```text
PC_ANDROID_DUAL_TARGET_CANDIDATE
```

이 값은 모든 게임의 의무가 아니다. 프로젝트는 근거에 따라 다음 중 하나를 선택한다.

```text
DUAL_TARGET_APPROVED
DUAL_TARGET_CONDITIONAL
SINGLE_TARGET_FIRST
BLOCKED_UNVERIFIED
```

이 Guide는 Windows와 Android를 지원하거나 STOVE·Google Play·Steam 출시 순서를 검토하는 프로젝트에서만 사용한다. 콘솔·iOS·Web은 별도 목표 플랫폼으로 추가 검토한다.

게임 빌드 용량·폰트·텍스처·오디오·패키징·패치 최적화가 범위에 포함되면 상세 규칙을 이 문서에 복제하지 않고 `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`를 함께 읽는다.

## 2. 결론

권장 기본 전략은 다음과 같다.

```text
처음부터 Windows + Android를 실행 가능한 목표로 설계
→ 게임 규칙·콘텐츠·데이터·저장은 하나의 공용 코어로 유지
→ 입력·레이아웃·앱 생명주기·성능 품질·상점 연동은 플랫폼 어댑터로 분리
→ 첫 Vertical Slice부터 Windows와 실제 Android 기기에서 확인
→ 제품·계정·테스터·지원 준비도에 따라 출시 wave를 나눔
```

**동시 구현 가능성**과 **동시 공개 출시 필요성**은 다른 결정이다. `same_day_launch_required: false`를 기본값으로 둔다.

## 3. 적용 적합성 Gate

### 3.1 `DUAL_TARGET_APPROVED` 후보

다음 조건이 대부분 충족되면 Windows와 Android를 처음부터 함께 유지하는 비용이 비교적 낮다.

- 턴제, 방치형, 카드·보드·퍼즐·관리·선택 중심이다.
- 실시간 반응보다 생각·읽기·계획이 중요하고 시간 압박이 낮다.
- 핵심 행동 수가 적고 한 손가락 또는 단순 포인터 입력으로 표현 가능하다.
- 일시정지·중단·복귀가 게임 규칙을 깨뜨리지 않는다.
- UI 정보를 모바일에서 계층화·탭·팝업으로 재배치할 수 있다.
- 저사양 Android 기기의 메모리·발열·로딩 예산 안에서 핵심 경험을 보존할 수 있다.
- Windows와 Android 빌드를 계속 검사할 QA·지원 역량이 있다.

### 3.2 `DUAL_TARGET_CONDITIONAL` 후보

핵심 규칙은 맞지만 다음 중 하나가 열려 있으면 조건부 상태로 둔다.

- 모바일 레이아웃을 아직 검증하지 않았다.
- 저장·background·foreground 복구 경계가 정해지지 않았다.
- 실제 Android 기기 성능 측정이 없다.
- Google Play 계정 유형·테스트 자격·테스터 확보가 미확정이다.
- STOVE·Steam·Google Play 플랫폼 서비스의 공용 경계가 없다.
- 두 플랫폼의 패치·고객지원·회귀 QA를 감당할 인력이 불명확하다.

### 3.3 `SINGLE_TARGET_FIRST` 또는 비사용 조건

다음 조건에서는 처음부터 두 플랫폼을 동일 우선순위로 개발하지 않는다.

- 정밀·고속 입력, 프레임 단위 반응, 다중 동시 입력, 광범위한 키 조합이 핵심 재미다.
- 작은 화면에서 정보량을 줄이면 핵심 의사결정이 훼손된다.
- `hover-only` 정보, 오른쪽 클릭, 드래그 정밀도, 키보드 중심 단축키가 필수다.
- 모바일 저사양 대응을 위해 핵심 연출·시뮬레이션·콘텐츠를 크게 희생해야 한다.
- 플랫폼별 온라인·결제·DRM·UGC·모드 기능이 게임 코어와 강하게 결합되어 있다.
- 실제 Android 기기와 테스터가 없어 모바일 위험을 검증할 수 없다.
- 두 플랫폼의 빌드·패치·지원 책임을 감당할 QA·지원 역량이 없다.

이 프로필을 모든 프로젝트에 강제하지 않는다. 적합하지 않은 프로젝트는 주력 플랫폼 하나를 먼저 증명하되, 향후 이식을 막는 불필요한 결합만 피한다.

## 4. 공용 코어와 플랫폼 어댑터

### 4.1 공용 책임

```yaml
shared_gameplay_rules:
shared_content_data:
shared_save_schema:
shared_deterministic_state:
shared_progression_and_economy:
shared_localization_keys:
shared_domain_tests:
```

공용 코어는 다음을 소유한다.

- 턴·행동·판정·보상·성장 규칙
- 아이템·적·이벤트·스테이지·대사 등 콘텐츠 데이터
- 저장 Schema·마이그레이션·결정론·재현 가능한 상태
- 플랫폼과 무관한 도메인 서비스와 테스트

UI가 규칙을 계산하거나 Steam·STOVE·Google Play SDK가 게임 상태의 단일 원본이 되지 않는다.

### 4.2 플랫폼별 책임

```yaml
input_adapter:
layout_profile:
lifecycle_adapter:
quality_profile:
platform_service_adapter:
```

- `input_adapter`: mouse·keyboard·touch·back·controller를 게임의 의미 행동으로 변환한다.
- `layout_profile`: 같은 정보 모델을 PC·모바일에 맞게 배치한다.
- `lifecycle_adapter`: pause·background·foreground·suspend·resume·process recreation을 처리한다.
- `quality_profile`: 해상도·그림자·파티클·후처리·텍스처·프레임 목표를 기기별로 조정한다. 원본 품질 의도는 공유하되 실제 texture format·packaged resolution·asset delivery는 플랫폼별로 분리할 수 있으며 세부 계약은 `GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`가 책임진다.
- `platform_service_adapter`: 업적·클라우드 저장·소유권·결제·통계·오버레이·로그인을 플랫폼 API 뒤에 둔다.

코드 공유율이나 LOC 비율을 목표로 삼지 않는다. 공용화가 잘됐는지는 **중복 줄 수**가 아니라 규칙 정본이 하나인지, 플랫폼 교체가 코어를 오염시키지 않는지, 양쪽 빌드가 같은 테스트를 통과하는지로 판정한다.

## 5. 화면·UI 기본값

### 5.1 Godot 논리 해상도

일반적인 비픽셀 2D·UI 중심 가로형 게임의 시작점:

```yaml
base_resolution: 1280 × 720
orientation: LANDSCAPE
stretch_mode: canvas_items
stretch_aspect: expand
```

Godot 공식 문서는 모바일 가로형 예시로 1280 × 720을 사용하고, 여러 화면비를 지원할 때 `expand`, 고해상도 2D/UI에서는 `canvas_items`를 선택할 수 있다고 설명한다. 이 값은 프로젝트별 아트·텍스트·카메라·성능 검증 전의 시작점이며 강제값이 아니다.

1920 × 1080을 논리 기준으로 사용할 수 있지만 저사양 기기에서 텍스처·메모리·다운스케일 비용이 커질 수 있으므로 실제 기기 예산이 먼저다. 세로형 게임은 `720 × 1280` 같은 별도 `layout_profile`을 명시한다.

### 5.2 레이아웃 원칙

- Anchor·Container·최소/최대 크기·safe area를 사용하고 고정 좌표 복제를 피한다.
- PC UI를 축소해서 모바일 UI로 통과시키지 않는다.
- 같은 기능과 데이터는 공유하되, 모바일에서는 우선순위가 낮은 정보를 탭·접기·팝업·상세 패널로 이동할 수 있다.
- 휴대폰 16:9와 장형 화면, 태블릿·폴더블의 4:3 또는 16:10에 가까운 비율을 확인한다.
- 핵심 결과가 손가락에 가려지지 않게 배치한다.
- `hover-only` 설명은 탭·길게 누르기·정보 버튼·선택 상태 같은 대안을 제공한다.
- 긴 한국어·영어·수치 증가·접근성 글자 크기에서 잘림과 겹침을 확인한다.

### 5.3 터치 목표

Android의 일반 접근성 권장에 따라 핵심 상호작용의 터치 영역은 최소 `48 dp × 48 dp`를 기본으로 한다. Base 프로젝트 프로필에서는 오입력 방지를 위한 시작점으로 주요 터치 목표 사이 `8 dp` 간격을 권장하되, 화면 밀도와 기능 위험에 따라 더 넓힐 수 있다.

시각 아이콘이 48 dp보다 작아도 실제 hit area는 확장할 수 있다. 파괴·구매·저장 삭제 같은 위험 행동은 인접 버튼과 더 멀리 두고 확인·취소·undo 경로를 둔다.

## 6. 입력 계약

장치 이벤트를 도메인 규칙에서 직접 읽지 않고 `semantic action`으로 변환한다.

```text
confirm
cancel
inspect
open_menu
end_turn
select_next
select_previous
zoom
pan
```

예:

```text
mouse left click / keyboard Enter / touch tap
→ confirm
→ 동일한 게임 규칙 호출
```

검수:

- 모든 핵심 행동에 touch 대안이 있는가?
- 마우스 hover·오른쪽 클릭·휠만으로 접근 가능한 정보가 없는가?
- Android back이 무조건 앱 종료가 아니라 현재 화면의 취소·뒤로가기 계약을 따르는가?
- 장치 전환 시 prompt와 focus가 갱신되는가?
- 연타·hold·복합 입력을 강제하지 않거나 대안이 있는가?

## 7. 저장·중단·복귀

Android에서는 앱이 background로 이동한 뒤 process가 종료될 수 있으므로, 단순 pause만으로 복구를 보장하지 않는다.

```yaml
save_and_lifecycle:
  safe_state_boundaries:
  autosave_triggers:
  background_behavior:
  foreground_behavior:
  process_recreation:
  duplicate_reward_protection:
  interrupted_transaction_recovery:
```

권장 안전 경계:

- 턴 판정 완료 후
- 선택 확정 후
- 보상 지급과 원장 기록이 원자적으로 끝난 후
- Scene 전환 전후의 명시된 snapshot
- 앱이 background로 이동할 때 가능한 범위의 저장
- foreground 복귀 시 Schema·버전·중복 지급·미완료 작업 검사

복귀가 같은 턴을 두 번 실행하거나 재화·보상을 중복 지급하지 않게 operation ID·snapshot·결정론 기록을 사용한다.

## 8. 성능·기기 예산

보편적인 FPS 숫자 하나를 모든 게임에 강제하지 않는다. 프로젝트가 대표 Scene과 최악 Scene을 정하고 다음을 실제 Android 기기에서 측정한다.

```yaml
frame_time_target_ms:
cpu_budget:
gpu_budget:
memory_budget:
loading_budget:
thermal_and_battery:
package_and_download_size:
quality_tiers:
```

`package_and_download_size`는 기존 호환 요약 필드다. 용량 최적화가 실제 작업 범위이면 `GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`와 `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`의 `build_size_and_asset_optimization`에서 다음을 분리 측정한다.

```text
Windows: compressed download / installed / patch / patch temporary disk / runtime memory
Android: Play-served download / installed / first-launch / first-session / typical / optional / runtime memory
```

품질 정책은 공유하되 Windows와 Android의 texture format·max delivered resolution·asset partition을 동일하게 강제하지 않는다. 폰트는 family/역할과 Theme 사용을 통일하되 CJK·emoji·다국어 fallback을 손상시키는 단일 파일 강제 규칙을 두지 않는다.

검증은 평균 FPS뿐 아니라 hitch, 95/99 percentile, peak memory, Scene 전환, 장시간 발열과 thermal throttling을 포함한다. Android 공식 측정 경로는 current 문서와 프로젝트 build에 맞춰 Perfetto·AGI·APT·Android vitals·ADPF 등을 선택한다. `Memory Advice API`는 2026-08-11 현재 공식 문서에서 beta 종료 및 deprecated로 표시되므로 새 프로젝트의 기본 메모리 관리 경로로 채택하지 않는다. 기존 consumer가 있다면 현재 대체 경로를 검증한 뒤 제거한다.

에디터나 에뮬레이터 성공은 실제 Android 기기 통과가 아니다. 로컬 profiler나 한 대의 기기에서 memory budget을 지킨 것도 Google Play의 production Android vitals 통과를 자동 증명하지 않는다.

### 8.1 Google Play Android vitals Gate

정책 확인일: **2026-09-03**. 이 절은 Google Play의 production 품질 관측과 가시성 위험을 프로젝트의 로컬 성능 예산과 분리하기 위한 **가변 운영 Evidence**다.

- Android vitals의 core vitals에는 `Memory usage (Anonymous RSS + Swap)`와 bitmap memory usage가 포함되고, DEX code optimization도 주의가 필요한 품질 신호로 제공된다.
- 현재 공식 문서는 **2027년 2월부터** memory usage, bitmap memory usage 또는 code optimization의 bad-behavior threshold 초과가 Google Play store visibility에 영향을 줄 수 있다고 안내한다.
- memory threshold는 device RAM tier와 app state에 따라 달라지고 app/game 표도 구분된다. 따라서 현재 표의 숫자를 Base 영구 상수로 복제하지 않는다.
- release candidate 전에는 로컬 peak memory·장시간 세션·background/foreground를 측정한다. Play 배포 뒤에는 실제 Play Console의 Android vitals 또는 공식 reporting surface로 production 상태를 다시 확인한다.
- production field data가 없거나 아직 충분하지 않은 단계는 `NOT_ENOUGH_FIELD_DATA`다. 로컬 PASS를 production-vitals PASS로 승격하지 않는다.

`Google Play Games Level Up`은 일반 Play submission/visibility 규칙과 같은 Gate가 아니다. 현재 공식 페이지는 Level Up 참여가 voluntary라고 명시하며, 프로그램별 UX·stability·performance·memory 자격을 별도로 둔다. 특히 프로그램의 stability threshold와 Play Store visibility bad-behavior threshold가 다름을 공식 문서 자체가 구분한다. Level Up을 사용하지 않는 프로젝트에는 그 프로그램 전용 요구를 release blocker로 강제하지 않는다.

프로젝트 기록:

```yaml
google_play_android_vitals:
  checked_at: 2026-09-03
  current_threshold_source: https://developer.android.com/games/optimize/vitals
  visibility_effective_window: 2027-02
  play_console_data_state: NOT_AVAILABLE_PRE_RELEASE | NOT_ENOUGH_FIELD_DATA | AVAILABLE | NOT_APPLICABLE
  production_observation_window:
  memory_usage_anonymous_rss_plus_swap_status: NOT_RUN | NOT_ENOUGH_FIELD_DATA | WITHIN_CURRENT_THRESHOLD | EXCEEDS_CURRENT_THRESHOLD | BLOCKED_UNVERIFIED
  bitmap_memory_usage_status: NOT_RUN | NOT_ENOUGH_FIELD_DATA | WITHIN_CURRENT_THRESHOLD | EXCEEDS_CURRENT_THRESHOLD | BLOCKED_UNVERIFIED
  dex_code_optimization_status: NOT_RUN | NOT_ENOUGH_FIELD_DATA | WITHIN_CURRENT_THRESHOLD | EXCEEDS_CURRENT_THRESHOLD | NOT_APPLICABLE | BLOCKED_UNVERIFIED
  store_visibility_risk_status: NOT_RUN | NOT_ENOUGH_FIELD_DATA | NO_CURRENT_BAD_BEHAVIOR | CURRENT_BAD_BEHAVIOR | BLOCKED_UNVERIFIED
  level_up_program_scope: NOT_PARTICIPATING | CANDIDATE | ENROLLED | UNKNOWN
  level_up_eligibility_status: NOT_APPLICABLE | NOT_RUN | ELIGIBLE | INELIGIBLE | BLOCKED_UNVERIFIED
  evidence_or_console_ref:
```

이 Gate의 목적은 Base 숫자를 플랫폼 정책으로 굳히는 것이 아니라 `local/device budget → current official threshold → production telemetry → program-specific eligibility`를 분리하는 것이다. 숫자·효력 범위·프로그램 조건은 Play 제출/운영 시점의 공식 문서와 Play Console에서 재검증한다.

## 9. 최소 테스트 Matrix

### Windows

- 1280 × 720 창모드
- 1920 × 1080 전체화면 또는 무테창
- 최소·최대 지원 화면비
- mouse + keyboard
- save path·업데이트·재설치·오프라인
- STOVE 또는 Steam adapter가 꺼진 순수 로컬 실행
- 용량 최적화가 범위이면 clean install과 이전 public-like build 대비 patch/update 크기 및 임시 disk 요구량

### Android

- 실제 Android 기기 1대 이상을 Vertical Slice부터 사용
- 프로젝트가 지원하려는 저사양 또는 기준 하한 기기
- 16:9 및 장형 화면
- 가능하면 태블릿·폴더블 또는 4:3/16:10에 가까운 화면
- touch·Android back·pause·background·foreground·process recreation
- 설치·업데이트·저장 마이그레이션·오프라인
- 메모리·로딩·발열·배터리·긴 세션
- 용량 최적화가 범위이면 실제 served/install/first-session size와 optional delivery 실패·재시도 경로
- Google Play 공개 후에는 Android vitals의 current memory/bitmap/code-optimization 상태를 production evidence로 추적하되 field data가 없으면 PASS로 쓰지 않음

출시 후보에서는 한 대 성공을 전체 Android 지원으로 일반화하지 않는다. 기기 범위는 실제 타깃과 지원 비용에 맞게 선언한다.

## 10. 출시 Wave 결정

### 10.1 기본 후보

사용자 포트폴리오와 같은 저입력·저시간압박 게임의 후보 순서:

```yaml
release_wave_1:
  - STOVE_WINDOWS
  - GOOGLE_PLAY_ANDROID
release_wave_2:
  - STEAM_WINDOWS
same_day_launch_required: false
```

그러나 이는 **검증 조건이 충족될 때만** 적용한다.

### 10.2 현재 확인된 비용·계정 Gate

정책 확인일: 2026-08-05

- Steam Direct Fee는 제품마다 `100달러`이며, 해당 제품의 Steam Store 및 인앱 구매 조정 총매출이 최소 1,000달러에 도달한 뒤 지급에서 회수 가능한 구조다.
- Google Play 개발자 등록은 `25달러` 일회성 비용으로 안내된다.
- 2023-11-13 이후 생성된 신규 Google Play 개인 계정은 Production 접근 신청 전에 최소 `12명`이 연속 `14일` 동안 참여한 closed test가 필요하다고 공식 도움말이 안내한다.
- STOVE 공식 문서는 프로젝트·Game ID·Application Key·PC SDK·개발자 모드·상품 등록 절차를 제공하지만, 이 조사에서 일반 공개된 단일 STOVE 비용표를 권위 있게 확정하지 못했다. 따라서 STOVE 비용·수수료·계약 조건은 `VERIFY_CURRENT_OFFICIAL_SOURCE`다.

비용·테스터·심사·계정 Gate는 변경될 수 있으므로 실제 출시 직전에 계정 화면과 공식 원문으로 다시 확인한다.

### 10.2.1 Google Play Target API Gate

정책 확인일: **2026-08-11**. 이 절의 숫자는 Google Play의 현재 제출·가용성 정책을 기록한 **가변 정책 Evidence**이며 Base 영구 상수가 아니다.

- **2026-08-31**부터 일반 Android 모바일의 새 앱과 앱 업데이트는 Google Play에 제출하려면 **Android 16 / API 36** 이상을 target SDK로 사용해야 한다.
- 같은 날짜부터 기존 일반 Android 앱은 신규 사용자가 더 높은 Android OS 기기에서 계속 찾을 수 있으려면 **Android 15 / API 35** 이상을 target해야 한다.
- 영향을 받는 앱이 업데이트에 시간이 더 필요하면 Play Console에서 **2026-11-01**까지의 연장을 요청할 수 있다고 현재 공식 도움말이 안내한다. 연장 가능 여부와 실제 양식 제공 상태는 앱·계정별로 다시 확인한다.
- Wear OS, Android Automotive OS, Android TV, Android XR은 별도 target API 예외가 있으므로 일반 모바일 값을 그대로 적용하지 않는다.

프로젝트 Gate:

```yaml
google_play_target_api:
  checked_at: 2026-08-11
  new_app_or_update_required_target_api: Android 16 / API 36
  existing_app_discoverability_target_api: Android 15 / API 35
  effective_at: 2026-08-31
  extension_if_available: 2026-11-01
  project_target_sdk:
  status: VERIFIED_CURRENT | UPDATE_REQUIRED | EXTENSION_REQUIRED | BLOCKED_UNVERIFIED
```

`VERIFIED_CURRENT`는 문서에 API 숫자를 적었다는 뜻이 아니라 실제 프로젝트 manifest/build 설정의 target SDK를 확인했다는 뜻이다. **출시·업데이트 제출 직전** `developer.android.com/google/play/requirements/target-sdk`, `support.google.com/googleplay/android-developer/answer/11926878`, 그리고 Play Console 계정 알림을 다시 확인한다.

### 10.3 Wave 1 승인 조건

STOVE + Google Play를 첫 공개 wave로 묶으려면:

- Windows와 Android의 동일 콘텐츠 milestone이 준비됨
- 각 플랫폼의 빌드·저장·입력·레이아웃·성능 Gate가 통과됨
- Google Play 계정 유형과 closed test requirement가 확인됨
- Google Play target SDK가 제출 시점의 current requirement를 충족하거나 승인된 extension 경로가 확인됨
- Google Play 공개 전 current Android vitals 기준과 post-launch production monitoring 계획이 기록됨; 아직 production field data가 없으면 그 상태를 `NOT_ENOUGH_FIELD_DATA`로 유지함
- tester_capacity가 현재 요구치를 충족함
- STOVE 계약·심사·SDK·정산 조건이 확인됨
- 두 플랫폼의 지원·패치·개인정보·결제 책임자가 정해짐

동일 wave라도 같은 날짜에 공개할 필요는 없다.

### 10.4 Google Play Gate를 충족하지 못할 때

테스터를 확보하지 못했다고 제품 전체를 멈추지 않는다.

```text
STOVE 공개 후보
+ Android 내부 테스트 또는 closed test 준비
→ Google Play Production 자격 충족 후 Android 공개
```

Steam의 100달러 비용보다 Google Play의 테스터·계정 운영 위험이 더 크다면, 실제 프로젝트에서는 `STOVE → Steam → Google Play`가 더 합리적일 수 있다. Base는 비용 하나만으로 출시 순서를 자동 결정하지 않는다.

## 11. 벤치마크에서 얻은 범위

대표 사례:

- `Into the Breach`: PC와 같은 콘텐츠를 유지하면서 작은 터치 기기를 위해 touch 모바일 인터페이스를 다시 설계했다.
- `Slay the Spire`: PC·Early Access와 플레이어 피드백을 먼저 활용하고 console·mobile port를 이후 단계로 두는 공개 패턴을 보였다.
- `Dicey Dungeons`: PC 출시 후 iOS·Android까지 확장한 턴제 사례다.
- `Balatro`: PC·콘솔 출시 후 모바일판을 별도 시점에 출시한 저입력 카드 게임 사례다.

이 사례들이 증명하는 것은 **공용 코어 + 모바일 적응 + 단계 출시가 실무에서 반복되는 패턴**이라는 점이다. 판매 성공, 일정, 팀 규모, 외주 port, 퍼블리셔, 기술 부채가 서로 다르므로 동시 출시의 보편적 성공 공식이나 특정 출시 간격을 도출하지 않는다.

## 12. 적대적 검토

다음 결론을 거부한다.

- 조작이 적으므로 모바일 UI 검증이 필요 없다.
- 같은 엔진 export가 되므로 두 플랫폼 구현이 끝났다.
- PC UI를 축소하면 모바일 대응이다.
- 코드 공유율이 높을수록 구조가 무조건 좋다.
- 에뮬레이터에서 실행되므로 Android가 검증됐다.
- 두 플랫폼을 구현했으므로 같은 날 출시해야 한다.
- Steam 비용이 있으므로 Google Play가 항상 먼저다.
- 현재 비용·테스터 요건·SDK 정책이 앞으로도 그대로다.
- 2026-08-11에 확인한 Google Play target API 숫자를 출시·업데이트 제출 직전 재검증 없이 영구 규칙으로 사용한다.
- 로컬 profiler·실기기 memory budget PASS만으로 Play production Android vitals도 PASS라고 간주한다.
- 현재 Android vitals threshold 숫자를 Base 영구 상수로 복제한다.
- voluntary인 Google Play Games Level Up 전용 요구를 모든 Google Play 출시의 submission blocker로 강제한다.
- deprecated된 `Memory Advice API`를 새 Android 프로젝트의 기본 메모리 관리 dependency로 추가한다.
- 한 대의 고사양 휴대폰 성공으로 Android 전체를 지원할 수 있다.
- 한 개의 package/download 숫자만 줄이면 용량 최적화가 끝난다.
- 폰트·텍스처·오디오를 플랫폼 구분 없이 하나의 설정으로 강제하면 항상 최적이다.

## 13. 프로젝트 판정

```yaml
candidate_status: DUAL_TARGET_APPROVED | DUAL_TARGET_CONDITIONAL | SINGLE_TARGET_FIRST | BLOCKED_UNVERIFIED
architecture_status:
windows_runtime_status:
android_runtime_status:
physical_device_status:
build_size_and_asset_optimization_status:
google_play_account_and_test_status:
google_play_target_api_status:
google_play_android_vitals_status:
stove_contract_and_sdk_status:
steam_budget_and_readiness_status:
release_wave_decision:
rollback:
```

`DUAL_TARGET_APPROVED`는 문서 작성만으로 부여하지 않는다. 최소한 공용 코어 경계, 양 플랫폼 export/run, 실제 Android 기기, 모바일 UI·입력·복귀, 대표 성능 예산의 증거가 필요하다. 용량 최적화를 완료 상태로 주장하려면 별도로 실제 build/served/patch와 품질 회귀 증거가 필요하다. Google Play production Android vitals는 실제 field telemetry가 생기기 전까지 별도 상태로 유지하며 pre-release local/device PASS와 합치지 않는다.

## 14. Evidence 상태

Base 공용 Guide 작성 시점:

```yaml
research_and_official_source_review: COMPLETE_AS_OF_2026_08_11
android_vitals_policy_review: COMPLETE_AS_OF_2026_09_03
base_contract: ACTIVE_IN_MAIN
actual_project_pilot: NOT_RUN
physical_android_device: DEVICE_NOT_RUN
human_usability: HUMAN_NOT_RUN
build_size_project_measurement: NOT_RUN
google_play_android_vitals_field_data: NOT_ENOUGH_FIELD_DATA
stove_submission: NOT_RUN
google_play_submission: NOT_RUN
steam_submission: NOT_RUN
```

실제 프로젝트 Pilot, 사람 사용성, 재미, 장치 호환성, 플랫폼 승인 결과는 이 문서로 대체하지 않는다.

## 15. Output Contract

```md
## 게임·조작·시간 압박·정보량 적합성
## DUAL_TARGET / SINGLE_TARGET 판정과 근거
## 공용 게임 규칙·콘텐츠·저장·결정론 책임
## input / layout / lifecycle / quality / platform service adapter
## Godot base resolution·화면비·safe area·UI scale
## touch target·hover 대안·semantic action·Android back
## background·foreground·process recreation·중복 지급 방지
## Windows·실제 Android 기기 QA Matrix
## 성능·메모리·로딩·발열·배터리 예산
## Google Play Android vitals·production field data·store visibility risk·Level Up scope
## download/install/runtime/patch 용량·자산 breakdown·품질 회귀
## STOVE·Google Play·Steam 계정·비용·테스트·target API·출시 wave
## 공식 정책 확인일·미확인·재검증 조건
## 결정·롤백·다음 Pilot
```

## 16. 공식·현업 출처

### 공식 기술·플랫폼

- Godot Multiple Resolutions: https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html
- Android Accessibility Touch Targets: https://developer.android.com/guide/topics/ui/accessibility/apps.html
- Android Activity Lifecycle: https://developer.android.com/guide/components/activities/activity-lifecycle.html
- Android Saving UI States: https://developer.android.com/topic/libraries/architecture/saving-states
- Android Game Optimization: https://developer.android.com/games/optimize/overview
- Android vitals for games: https://developer.android.com/games/optimize/vitals
- Android Memory Guide: https://developer.android.com/topic/performance/memory
- Memory Advice API deprecation notice: https://developer.android.com/games/sdk/memory-advice/start
- Google Play Games Level Up guidelines: https://developer.android.com/games/guidelines
- Google Play Target API Requirements: https://developer.android.com/google/play/requirements/target-sdk
- Google Play Target API Console Help / Extension: https://support.google.com/googleplay/android-developer/answer/11926878
- Steamworks Partner Program / Direct Fee: https://partner.steamgames.com/steamdirect/
- Google Play Registration and Access Conditions: https://support.google.com/googleplay/android-developer/answer/14659200
- Google Play Testing Requirements for New Personal Accounts: https://support.google.com/googleplay/android-developer/answer/14151465
- STOVE SDK Development Environment: https://studio-docs.onstove.com/pc/GettingStarted/requisition.html
- STOVE BASIC Release: https://studio-docs.onstove.com/pc/StudioGuide/basicrelease.html

빌드 용량·asset import·Steam patch·Google Play asset delivery의 상세 공식 근거는 `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`와 `REFERENCE_SOURCE_CATALOG.md`가 책임진다.

### 대표 제작·출시 사례

- Subset Games Into the Breach Advanced Edition and Mobile: https://subsetgames.com/itb_ae.html
- Mega Crit FAQ: https://www.megacrit.com/faq/
- Dicey Dungeons official site: https://diceydungeons.com/
- Balatro Steam page: https://store.steampowered.com/app/2379780/Balatro/

외부 출처는 프로젝트 구현·수익·일정·승인을 보장하지 않는다. 공식 정책·요금·계정·SDK·심사 조건은 적용 직전에 다시 확인한다.