# PC·Android Delivery Profile

`docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`를 읽고 프로젝트별 값과 증거를 기록한다. 이 Template는 설계·계정·QA·출시 결정을 연결하지만 실제 build, 기기 실행, 플랫폼 승인 또는 사람 사용성을 대신하지 않는다.

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
    - touch_and_android_back
    - background_foreground_process_recreation
    - install_update_save_migration_offline
    - memory_loading_thermal_battery_long_session
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

human_usability_evidence:
  participants:
  critical_tasks:
  observed_errors:
  result:
  state: HUMAN_NOT_RUN | FAIL | PASS
```

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

steam:
  steamworks_partner_status:
  direct_fee_budget_status:
  store_page_status:
  playtest_or_demo_status:
  sdk_features_required:
```

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
background_foreground_recovery:
performance_budget:
stove_readiness:
google_play_readiness:
steam_readiness:
human_usability:
final_profile_status:
```

문서 작성만으로 `DUAL_TARGET_APPROVED`를 부여하지 않는다. 실행하지 않은 build·device·human·store 검증은 각각 `NOT_RUN`, `DEVICE_NOT_RUN`, `HUMAN_NOT_RUN`, `BLOCKED_UNVERIFIED`로 유지한다.
