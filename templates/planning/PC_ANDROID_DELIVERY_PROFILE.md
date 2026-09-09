# PC·Android Delivery Profile

`docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`를 읽고 프로젝트별 값과 증거를 기록한다. 게임 빌드 용량·자산 최적화가 범위에 포함되면 `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`를 함께 읽는다. 이 Template는 설계·계정·QA·출시 결정을 연결하지만 실제 build, 기기 실행, 플랫폼 승인 또는 사람 사용성을 대신하지 않는다.

## 1. Profile Identity

```yaml
delivery_profile_id:
project_id:
project_name:
owner:
created_at:
updated_at:
source_commit:
candidate_status: DUAL_TARGET_APPROVED | DUAL_TARGET_CONDITIONAL | SINGLE_TARGET_FIRST | BLOCKED_UNVERIFIED
target_platforms:
  - WINDOWS_PC
  - ANDROID_MOBILE
primary_player_context:
core_experience:
```

## 2. Eligibility

```yaml
gameplay_fit:
  turn_based_or_low_time_pressure:
  core_action_count:
  touch_feasibility:
  interruption_tolerance:
  mobile_information_hierarchy:
  low_end_android_feasibility:
  qa_and_support_capacity:

blocking_or_escalation_factors:
  precision_or_high_speed_input:
  hover_or_right_click_dependency:
  dense_information_loss:
  mobile_performance_risk:
  platform_specific_core_dependency:
  physical_device_gap:
  tester_or_support_gap:
```

근거:

-

## 3. Shared Core Contract

```yaml
shared_core_contract:
  shared_gameplay_rules:
  shared_content_data:
  shared_save_schema:
  shared_deterministic_state:
  shared_progression_and_economy:
  shared_localization_keys:
  shared_domain_tests:
  source_of_truth_paths:
```

공용 코어가 소유하지 않는 책임:

-

## 4. Platform Adapters

```yaml
platform_adapters:
  input_adapter:
    windows:
    android:
  layout_profile:
    windows:
    android:
  lifecycle_adapter:
    windows:
    android:
  quality_profile:
    windows:
    android:
  platform_service_adapter:
    stove:
    google_play:
    steam:
```

플랫폼 SDK 없이도 실행 가능한 core/local fallback:

-

## 5. Display and UI

```yaml
base_resolution: 1280 × 720
orientation: LANDSCAPE
stretch_mode: canvas_items
stretch_aspect: expand
minimum_supported_aspect:
maximum_supported_aspect:
safe_area_policy:
ui_scale_policy:
text_expansion_languages:
touch_target_min_dp: 48
touch_spacing_recommended_dp: 8
hover_alternatives:
  inspect:
  tooltip:
  context_action:
```

### Windows Layout

```yaml
information_visible_at_once:
mouse_and_keyboard_flow:
controller_or_steam_deck_scope:
minimum_window_size:
fullscreen_modes:
```

### Android Layout

```yaml
phone_layout:
tablet_or_foldable_layout:
portrait_profile_if_any:
collapsed_or_tabbed_information:
finger_occlusion_controls:
android_back_behavior:
```

### 5.1 Android Large-Screen Configuration Continuity

정상 상태의 태블릿·폴더블 화면이 한 번 잘 보이는 것과 **화면 구성 전환 중 상태·입력·레이아웃이 보존되는 것**은 별도 증거다. 프로젝트가 해당 form factor/window mode를 지원한다고 선언했거나 `level_up_program_scope`가 `CANDIDATE | ENROLLED`이면 적용 가능한 transition을 실제 build에서 검증한다. 지원 범위 밖 transition은 이유를 남긴 `NOT_APPLICABLE`로 둘 수 있다.

`Google Play Games Level Up`은 voluntary program이므로 프로그램 전용 요구를 일반 Google Play submission Gate로 승격하지 않는다. 프로그램 후보/참여 프로젝트는 적용 시점의 현재 공식 guideline을 다시 읽는다. Android 16/17의 일반 app resizability 동작도 `android:appCategory="game"` 예외와 target/version 조건을 확인한 뒤 적용한다.

```yaml
large_screen_configuration_continuity:
  checked_at:
  guideline_source: https://developer.android.com/games/guidelines
  technical_source: https://developer.android.com/games/develop/multiplatform/support-large-screen-resizability
  project_large_screen_scope:
  declared_supported_transitions: []
  unsupported_scope_reason:
  transitions:
    rotation: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
    fold_unfold: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
    split_screen: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
    freeform_resize: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
  active_game_state_preserved: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
  progress_preserved: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
  touch_mapping_status: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
  interactive_ui_visibility_status: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
  distortion_or_overlap_status: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
  focus_resume_path_status: NOT_APPLICABLE | NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
  resume_depends_only_on_focus_reacquire: false | true | UNKNOWN
  evidence_or_capture_refs: []
```

`PASS`는 transition 전후 정지 화면만 비교해서 부여하지 않는다. 동일한 active gameplay state에서 실제 transition을 수행하고, state/progress·touch mapping·interactive UI·resume path를 함께 관찰한 runtime evidence가 있어야 한다. Multi-window 복귀는 focus reacquire 하나만으로 정상 복구를 가정하지 않는다.

## 6. Semantic Input Actions

```yaml
semantic_actions:
  confirm:
    windows:
    android:
  cancel:
    windows:
    android:
  inspect:
    windows:
    android:
  open_menu:
    windows:
    android:
  end_turn:
    windows:
    android:
  select_next:
    windows:
    android:
  select_previous:
    windows:
    android:
  zoom:
    windows:
    android:
  pan:
    windows:
    android:
```

입력 대안·접근성:

-

## 7. Save and Lifecycle

```yaml
save_and_lifecycle:
  schema_version:
  safe_state_boundaries:
  autosave_triggers:
  background_behavior:
  foreground_behavior:
  suspend_and_resume:
  process_recreation:
  interrupted_transaction_recovery:
  duplicate_reward_protection:
  backup_and_corruption_handling:
  migration_from:
```

중단 시 금지되는 상태:

-

## 8. Performance Budget

```yaml
performance_budget:
  windows_reference_device:
  android_minimum_device:
  android_reference_device:
  representative_scene:
  worst_case_scene:
  frame_time_target_ms:
  cpu_budget:
  gpu_budget:
  memory_budget:
  loading_budget:
  thermal_and_battery:
  package_and_download_size:
  quality_tiers:
  baseline_capture:
  measurement_tools:
```

기존 `package_and_download_size`는 호환 필드로 유지한다. 구체적인 다운로드·설치·런타임·패치 용량과 자산별 기여도는 아래 계약에서 분리한다.

### 8.1 Build Size and Asset Optimization

프로젝트별 목표 MB·texture max resolution·bitrate·font family/weight 수는 Base에서 상속하지 않고 실제 baseline·장르·아트·기기·스토어 조건으로 결정한다. 측정하지 않은 값은 `ESTIMATE`와 실제 측정값을 구분한다.

```yaml
build_size_and_asset_optimization:
  baseline_build:
  target_budget_status:
  windows_size_budget:
    download_compressed_bytes:
    installed_bytes:
    first_launch_additional_download_bytes:
    typical_patch_download_bytes:
    worst_expected_patch_download_bytes:
    patch_temporary_disk_bytes:
    runtime_peak_memory_bytes:
  android_size_budget:
    play_served_download_bytes:
    installed_bytes_before_first_launch:
    first_launch_additional_download_bytes:
    first_session_total_download_bytes:
    typical_player_content_bytes:
    full_optional_content_bytes:
    runtime_peak_memory_bytes:
  asset_size_breakdown:
    executable_and_engine:
    font:
    ui_texture:
    world_texture:
    sprite_and_2d_art:
    mesh:
    animation:
    audio_sfx:
    audio_music:
    audio_voice:
    video:
    shader_and_generated_data:
    localization:
    platform_sdk:
    optional_content:
    duplicate_or_unused:
    other:
  top_contributors:
  font_profile:
  texture_profiles:
  audio_profiles:
  delivery_partition:
  duplicate_unused_audit:
  accepted_optimizations:
  rejected_optimizations:
  visual_quality_evidence:
  audio_quality_evidence:
  runtime_evidence:
  patch_evidence:
  unresolved:
```

각 실측 기록에는 최소 `source_build`, `platform`, `device_or_store_configuration`, `measured_at`, `tool`, `measured_value`, `state: ESTIMATE | LOCAL_BUILD_MEASURED | DEVICE_MEASURED | STORE_SERVED_MEASURED`를 남긴다.

### 8.2 Google Play Android vitals

로컬 profiler·실기기 memory budget과 Google Play production telemetry를 분리한다. 현재 Android vitals threshold 숫자는 Base에서 상속하지 않고, 공개·운영 시점의 공식 문서와 Play Console을 다시 확인한다.

```yaml
google_play_android_vitals:
  checked_at:
  current_threshold_source: https://developer.android.com/games/optimize/vitals
  visibility_effective_window:
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

`Level Up`은 별도 voluntary program scope다. `NOT_PARTICIPATING`이면 프로그램 전용 요구를 Google Play submission PASS/FAIL로 사용하지 않는다. production field data가 없으면 Android vitals 상태도 PASS로 만들지 않는다.

## 9. Test Matrix

```yaml
test_matrix:
  windows:
    - 1280x720_windowed
    - 1920x1080_fullscreen_or_borderless
    - mouse_keyboard
    - save_update_reinstall_offline
    - platform_adapter_disabled
  android:
    - reference_phone_physical
    - minimum_device_physical
    - long_aspect_phone
    - tablet_or_foldable_when_supported
    - configuration_transition_continuity_when_supported
    - touch_and_android_back
    - background_foreground_process_recreation
    - install_update_save_migration_offline
    - memory_loading_thermal_battery_long_session
    - post_release_android_vitals_when_field_data_exists
    - play_games_services_v2_auth_and_features_when_used
```

```yaml
windows_runtime_evidence:
  build:
  device_or_environment:
  result:
  artifact_or_log:

physical_android_evidence:
  build:
  device_model:
  os_version:
  screen_and_aspect:
  session_duration:
  result:
  artifact_or_log:
  state: DEVICE_NOT_RUN | FAIL | PASS

large_screen_configuration_transition_evidence:
  build:
  environment_type: EMULATOR | PHYSICAL_DEVICE
  device_or_emulator:
  os_version:
  transitions_exercised: []
  active_game_state_before:
  active_game_state_after:
  progress_before:
  progress_after:
  touch_mapping_observation:
  ui_visibility_observation:
  focus_resume_observation:
  artifact_or_log_refs: []
  result:
  state: NOT_APPLICABLE | EMULATOR_NOT_RUN | EMULATOR_FAIL | EMULATOR_PASS | DEVICE_NOT_RUN | DEVICE_FAIL | DEVICE_PASS | BLOCKED_UNVERIFIED

human_usability_evidence:
  participants:
  critical_tasks:
  observed_errors:
  result:
  state: HUMAN_NOT_RUN | FAIL | PASS
```

에뮬레이터 transition PASS는 재현 가능한 사전 검증으로 사용할 수 있지만 실제 foldable/tablet hardware 호환성 PASS를 대신하지 않는다. 물리 장치 지원을 주장하려면 해당 범위에 대한 `DEVICE_PASS` evidence가 필요하다.

## 10. Store and Account Readiness

정책·요금·계정 조건은 적용 전에 공식 출처로 재검증한다.

```yaml
official_policy_checked_at:
official_policy_checked_by:

stove:
  studio_account_status:
  project_and_game_id_status:
  pc_sdk_requirement:
  current_fee_and_contract_status: VERIFY_CURRENT_OFFICIAL_SOURCE
  review_and_release_status:

google_play:
  developer_account_status:
  google_play_account_type: PERSONAL | ORGANIZATION | UNKNOWN
  account_created_at:
  registration_fee_status:
  closed_test_requirement:
  tester_capacity:
  continuous_test_days_capacity:
  production_access_status:
  privacy_data_safety_billing_status:

google_play_target_api:
  checked_at:
  new_app_or_update_required_target_api:
  existing_app_discoverability_target_api:
  effective_at:
  extension_if_available:
  project_target_sdk:
  status: VERIFIED_CURRENT | UPDATE_REQUIRED | EXTENSION_REQUIRED | BLOCKED_UNVERIFIED

android_developer_verification:
  checked_at:
  policy_source: https://developer.android.com/developer-verification
  play_console_guide_source: https://developer.android.com/developer-verification/guides/google-play-console
  play_policy_deadline_source: https://developer.android.com/distribute/play-policies
  distribution_path: GOOGLE_PLAY_ONLY | GOOGLE_PLAY_AND_OUTSIDE | OUTSIDE_GOOGLE_PLAY_ONLY | LIMITED_DISTRIBUTION | UNKNOWN
  identity_verification_status: NOT_RUN | VERIFIED | ACTION_REQUIRED | NOT_APPLICABLE_LIMITED_DISTRIBUTION | BLOCKED_UNVERIFIED
  package_name:
  package_registration_status: NOT_RUN | REGISTERED | NOT_REGISTERED | DRAFT | ACTION_REQUIRED | BLOCKED_UNVERIFIED
  signing_key_ownership_status: NOT_RUN | VERIFIED | ACTION_REQUIRED | NOT_APPLICABLE | BLOCKED_UNVERIFIED
  current_enforcement_scope:
  release_readiness_status: NOT_RUN | READY_FOR_CURRENT_SCOPE | ACTION_REQUIRED | BLOCKED_UNVERIFIED
  evidence_or_console_ref:

google_play_games_services:
  checked_at:
  lifecycle_source: https://developer.android.com/games/pgs/deprecation
  migration_source: https://developer.android.com/games/pgs/migration_overview
  downloads_source: https://developer.android.com/games/pgs/downloads
  usage_scope: NOT_USED | PLANNED | IN_USE | UNKNOWN
  integration_surface: NONE | JAVA_KOTLIN | NATIVE | ENGINE_PLUGIN | UNKNOWN
  sdk_or_plugin_ref:
  sdk_or_plugin_version:
  pgs_generation: NONE | V2 | V1_LEGACY | UNKNOWN
  identity_model_status: NOT_APPLICABLE | PLATFORM_AND_INGAME_SEPARATED | V1_PLAYER_ID_PRIMARY_LEGACY | BLOCKED_UNVERIFIED
  dependency_upgrade_compile_status: NOT_APPLICABLE | NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
  migration_status: NOT_APPLICABLE | CURRENT_V2 | MIGRATION_REQUIRED | BLOCKED_UNVERIFIED
  physical_device_auth_and_feature_status: NOT_APPLICABLE | DEVICE_NOT_RUN | FAIL | PASS | BLOCKED_UNVERIFIED
  evidence_or_log_refs: []

steam:
  steamworks_partner_status:
  direct_fee_budget_status:
  store_page_status:
  playtest_or_demo_status:
  sdk_features_required:
```

`google_play_target_api`는 프로젝트의 실제 `target SDK`와 현재 Google Play 정책을 대조하는 가변 Gate다. Base의 기록값을 영구 상수로 간주하지 않고 출시·업데이트 제출 직전에 공식 원문과 Play Console에서 다시 확인한다.

`google_play_android_vitals`는 제출 전 local/device performance와 제출 후 production quality evidence를 합치지 않기 위한 별도 Gate다. current threshold, 효력 시점, Play Console field data를 확인하지 않은 상태를 `WITHIN_CURRENT_THRESHOLD` 또는 `NO_CURRENT_BAD_BEHAVIOR`로 승격하지 않는다.

### 10.1 Android Developer Verification Release Gate

2026-09-07에 재확인한 공식 Android 문서에서 다음 enforcement milestone은 **2026-09-30**이다. 참여 store의 Brazil·Indonesia·Singapore·Thailand에서 certified Android 7+ 기기 설치·업데이트에 developer verification이 적용되기 시작하고, broader rollout은 2027로 예고되어 있다. Google Play 쪽은 별도로 Play Console에서 Play 배포 package name을 관리하며, 기존 앱 대부분은 자동 등록되지만 남은 package를 확인·등록하지 않으면 Play distribution continuity가 막힐 수 있다.

이 날짜·지역·store 범위와 2027 확대 계획은 가변 platform policy다. Base 영구 상수로 간주하지 않고 실제 release/update 시점의 `policy_source`, `play_console_guide_source`, `play_policy_deadline_source`, Play Console 또는 Android Developer Console 상태를 다시 읽는다. 2026-09-30의 지역 install enforcement와 Google Play package registration의 distribution consequence도 같은 claim으로 합치지 않는다.

`identity_verification_status`, `package_registration_status`, `signing_key_ownership_status`는 독립 상태다. 자동 등록 가능성만으로 package registration을 PASS로 만들지 않는다. 실제 Play Console 또는 적용 가능한 Android Developer Console의 package/status readback이 있어야 `REGISTERED`를 기록한다. signing key ownership proof가 필요한 경우에도 private signing key, 신분증 원본, recovery code, secret/account credential을 repository evidence에 저장하지 않고 안전한 status/receipt reference만 남긴다.

ADB 또는 advanced flow 성공을 consumer release PASS로 사용하지 않는다. ADB는 개발·테스트 install 경로이고 advanced flow는 power-user용 예외 경로이므로, 해당 경로 성공은 일반 플레이어가 intended distribution path에서 설치·업데이트할 수 있다는 증거가 아니다. 현재 enforcement에 참여하지 않는 off-Play 경로는 적용 조건을 확인해 `NOT_APPLICABLE` 또는 `READY_FOR_CURRENT_SCOPE`를 사용할 수 있지만 2027 확대 전에 다시 검증한다.

### 10.2 Google Play Games Services SDK Lifecycle Gate

Play Games Services(PGS)를 사용하지 않는 프로젝트에는 이 Gate를 강제하지 않는다. `usage_scope: NOT_USED`이면 관련 상태는 `NOT_APPLICABLE`로 둘 수 있다. 반대로 achievements·leaderboards·events·cloud save·Play Games platform authentication 중 하나라도 실제 consumer라면 사용 중인 SDK 또는 engine plugin의 **정확한 generation과 version을 먼저 확인**한다.

2026-09-07에 갱신된 Android 공식 deprecation 문서는 PGS v1이 Google Sign-In for Android에 의존해 이미 deprecated 상태이며 v2 migration을 요구한다. 같은 문서 안에서도 v1 shutdown 시점 표기에는 May/June 2027 차이가 있으므로 Base에 단일 종료일을 영구 상수로 복제하지 않는다. 출시·업데이트·dependency upgrade 직전에 `lifecycle_source`를 다시 읽고 현재 deadline을 확인한다.

새 통합은 PGS v1을 선택하지 않는다. 기존 v1 통합은 현재 build가 성공한다는 이유만으로 장기 release-ready로 간주하지 않는다. 특히 다른 Google/third-party SDK가 authentication dependency를 올리면 v1의 GSI 의존성 때문에 compile failure가 생길 수 있으므로, SDK/plugin update 뒤에는 실제 release-like Android build를 다시 compile하고 관련 platform feature를 물리 기기에서 실행한다.

PGS v2의 platform identity는 게임의 primary in-game account identity와 분리한다. achievements·leaderboards 같은 platform feature용 Player ID를 재화·inventory·progress의 단일 primary account key로 사용하지 않는다. 이미 v1 Player ID에 primary in-game account를 묶어 둔 프로젝트는 단순 SDK 교체가 아니라 account binding/migration 문제로 별도 검증한다.

Android 공식 downloads page는 third-party engine extension 중 일부가 PGS v1, 일부가 v2일 수 있으므로 제품 문서에서 지원 generation을 확인하라고 명시한다. 따라서 Godot addon을 쓰는 경우 Asset Library에 존재한다는 사실만으로 `CURRENT_V2`를 부여하지 않는다. exact plugin release/source에서 PGS dependency generation을 확인하고, Godot version·Gradle build·package name·signing credential·Play Console configuration과 실제 Android runtime을 함께 검증한다. third-party addon은 project dependency로 채택되기 전 license·maintenance·permissions·tests·rollback을 별도로 검토한다.

## 11. Release Waves

```yaml
release_wave_1:
  candidate_platforms:
    - STOVE_WINDOWS
    - GOOGLE_PLAY_ANDROID
  prerequisites:
  shared_content_milestone:
  stagger_within_wave_allowed: true
  release_decision:

release_wave_2:
  candidate_platforms:
    - STEAM_WINDOWS
  prerequisites:
  release_decision:

same_day_launch_required: false
```

Google Play Production Gate가 열리지 않을 때 대체 순서:

```yaml
google_play_gate_fallback:
  - STOVE_WINDOWS_PUBLIC_CANDIDATE
  - ANDROID_INTERNAL_OR_CLOSED_TEST
  - GOOGLE_PLAY_AFTER_PRODUCTION_ACCESS
  - STEAM_MAY_PRECEDE_GOOGLE_PLAY_WHEN_LOWER_OPERATIONAL_RISK
```

## 12. Decision

```yaml
decision:
  status: DUAL_TARGET_APPROVED | DUAL_TARGET_CONDITIONAL | SINGLE_TARGET_FIRST | BLOCKED_UNVERIFIED
  rationale:
  approved_scope:
  excluded_scope:
  required_before_next_gate:
  approver:
  approval_reference:

rollback:
  trigger:
  preserved_shared_core:
  primary_platform_after_rollback:
  deferred_platform_reentry_gate:

unresolved_evidence:
  -
```

## 13. Completion Evidence

```yaml
architecture_contract:
windows_export_and_runtime:
android_export_and_runtime:
physical_android_device:
mobile_ui_and_input:
large_screen_configuration_continuity:
background_foreground_recovery:
performance_budget:
google_play_android_vitals:
android_developer_verification:
google_play_games_services_lifecycle:
build_size_and_asset_optimization:
stove_readiness:
google_play_readiness:
steam_readiness:
human_usability:
final_profile_status:
```

문서 작성만으로 `DUAL_TARGET_APPROVED`를 부여하지 않는다. 실행하지 않은 build·device·human·store 검증은 각각 `NOT_RUN`, `DEVICE_NOT_RUN`, `HUMAN_NOT_RUN`, `BLOCKED_UNVERIFIED`로 유지한다. Large-screen configuration continuity도 실제 transition runtime evidence 없이 `PASS`로 만들지 않는다. Google Play production field data가 없으면 `google_play_android_vitals`도 `NOT_ENOUGH_FIELD_DATA` 또는 해당 pre-release 상태로 유지한다. Android developer verification도 실제 console/status readback 없이 `READY_FOR_CURRENT_SCOPE`로 승격하지 않는다. PGS를 쓰는 프로젝트도 exact SDK/plugin generation·release-like compile·물리 기기 platform feature evidence 없이 `CURRENT_V2` 또는 release-ready라고 주장하지 않는다.