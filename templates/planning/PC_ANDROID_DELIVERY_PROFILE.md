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

steam:
  steamworks_partner_status:
  direct_fee_budget_status:
  store_page_status:
  playtest_or_demo_status:
  sdk_features_required:
```

`google_play_target_api`는 프로젝트의 실제 `target SDK`와 현재 Google Play 정책을 대조하는 가변 Gate다. Base의 기록값을 영구 상수로 간주하지 않고 출시·업데이트 제출 직전에 공식 원문과 Play Console에서 다시 확인한다.

`google_play_android_vitals`는 제출 전 local/device performance와 제출 후 production quality evidence를 합치지 않기 위한 별도 Gate다. current threshold, 효력 시점, Play Console field data를 확인하지 않은 상태를 `WITHIN_CURRENT_THRESHOLD` 또는 `NO_CURRENT_BAD_BEHAVIOR`로 승격하지 않는다.

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
build_size_and_asset_optimization:
stove_readiness:
google_play_readiness:
steam_readiness:
human_usability:
final_profile_status:
```

문서 작성만으로 `DUAL_TARGET_APPROVED`를 부여하지 않는다. 실행하지 않은 build·device·human·store 검증은 각각 `NOT_RUN`, `DEVICE_NOT_RUN`, `HUMAN_NOT_RUN`, `BLOCKED_UNVERIFIED`로 유지한다. Large-screen configuration continuity도 실제 transition runtime evidence 없이 `PASS`로 만들지 않는다. Google Play production field data가 없으면 `google_play_android_vitals`도 `NOT_ENOUGH_FIELD_DATA` 또는 해당 pre-release 상태로 유지한다.