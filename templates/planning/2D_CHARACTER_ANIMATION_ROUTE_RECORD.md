# 2D Character Animation Route Record

> 이 Template은 프로젝트의 실제 consumer 하나에 대한 route 선택·trial·검증 기록이다. Base 공용 정본이나 모든 캐릭터의 자동 결론이 아니다.

```yaml
route_record_id:
project:
repository:
source_sha:
created_at:
updated_at:
owner:
status: IDEA | RESEARCHED | FEASIBLE | TRIAL_APPROVED | ASSET_READY | IMPLEMENTED | MACHINE_VERIFIED | RUNTIME_VERIFIED | HUMAN_APPROVED | SHIP_APPROVED | DEFERRED | REJECTED

actual_consumer:
  consumer_id:
  consumer_surface:
  scene_or_planned_scene:
  player_value:
  camera_scale:
  screen_time:
  concurrent_instance_peak:
  target_platforms: []

production_shape:
  animation_count:
  direction_count:
  outfit_variant_count:
  weapon_attachment_count:
  expression_variant_count:
  requires_continuous_deformation:
  requires_extreme_smear_or_redraw:
  silhouette_priority:
  performance_budget:

current_path:
  renderer:
  asset_paths: []
  scene_resource_paths: []
  animation_nodes_or_resources: []
  current_runtime_evidence:

alternatives:
  - route: FRAME
    fit:
    lifecycle_cost:
    risks: []
    evidence:
    disposition: ADOPT | ADAPT | TEST | REJECT | NOT_APPLICABLE
  - route: GODOT_NATIVE_RIG
    fit:
    lifecycle_cost:
    risks: []
    evidence:
    disposition: ADOPT | ADAPT | TEST | REJECT | NOT_APPLICABLE
  - route: EXTERNAL_RIG_RUNTIME
    fit:
    lifecycle_cost:
    risks: []
    evidence:
    disposition: ADOPT | ADAPT | TEST | REJECT | NOT_APPLICABLE
  - route: EXTERNAL_RIG_BAKED
    fit:
    lifecycle_cost:
    risks: []
    evidence:
    disposition: ADOPT | ADAPT | TEST | REJECT | NOT_APPLICABLE

selected_route: FRAME | GODOT_NATIVE_RIG | EXTERNAL_RIG_RUNTIME | EXTERNAL_RIG_BAKED
selected_reason:
rejected_routes:
  - route:
    reason:
recheck_conditions: []

state_family:
  Idle:
  Locomotion:
  Turn:
  Wind-up:
  Active:
  Recovery:
  Guard:
  Evade:
  Hit:
  Stagger:
  Knockdown:
  Rise:
  Defeat:
  Interaction:
  Expression:
  Transition:

rig_source_contract:
  required: true | false
  source_path:
  source_sha256:
  parts:
    - part_id:
      pivot:
      parent_bone:
      draw_order:
      hidden_underlap:
      overlap_margin:
      deformation_safe_area:
      attachment_slot:
      skin_group:
  protected_identity: []
  not_applicable_reason:

interruption_contract:
  can_interrupt:
  interrupt_windows: []
  next_state_priority: []
  same_state_reentry:
  rapid_repeat_behavior:
  instant_complete_behavior:
  pause_resume:
  save_resume_pose:
  reduced_motion_fallback:
  missing_asset_fallback:

domain_authority_boundary:
  state_owner:
  visual_adapter:
  animation_events_allowed: []
  forbidden_authority:
    - damage
    - cost
    - reward
    - save
    - progress
  exactly_once_predicate:

external_runtime_trial:
  applicable: true | false
  candidate_name:
  adoption_state: CANDIDATE | TRIAL_APPROVED | ADOPTED_ACTIVE | DEFERRED | REJECTED
  editor_exact_version:
  runtime_exact_version_or_commit:
  godot_exact_version:
  integration_type:
  export_format:
  atlas_profile:
  license_evidence:
  price_checked_at:
  source_available:
  consumption_path:
  performance_baseline:
  platform_export_validation:
  removal_or_rollback:
  unverified: []

validation_matrix:
  contract_static:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:
  source_asset:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:
  import_machine:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:
  runtime_windows:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:
  runtime_android_or_other_target:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED | NOT_APPLICABLE
    evidence:
  performance_peak:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:
  interruption_and_reentry:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:
  reduced_motion:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:
  human_visual_readability:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:
  license_and_distribution:
    status: NOT_RUN | PASS | FAIL | BLOCKED_UNVERIFIED
    evidence:

rollback:
  preserved_fallback:
  files_to_remove_or_restore: []
  import_cache_rebuild:
  test_commands: []
  runtime_readback:

remaining_risks: []
next_safe_action:
evidence_ceiling:
```

상태를 축약하지 않는다.

```text
RESEARCHED != TRIAL_APPROVED != INSTALLED != IMPORTED != MACHINE_VERIFIED != RUNTIME_VERIFIED != HUMAN_APPROVED != SHIP_APPROVED
```
