# Narrative Dialogue Runtime Sample Evidence — 2026-08-14

## Scope

Base의 Figma narrative dialogue contract를 실제 Godot 4.7.1 reference fixture로 소비할 수 있는지 검증한다. 이 기록은 실제 사용자 프로젝트 adoption이나 HiGodot authoring을 증명하지 않는다.

## TDD RED

- branch commit: `88d1683c1219267cc0ae325d08017f942083eb6a`
- workflow: `Validate Narrative Dialogue Runtime`
- run: `31809786699`
- job: `94797381873`
- Godot: `4.7.1.stable.official.a13da4feb`
- Godot archive SHA-256: `c7ff14fd28472c8d4f193043de30278dcf7e5241a1dcf7566b02e27addaa33ba`
- result: expected failure, exit 1
- root cause: `res://src/dialogue_flow_model.gd` intentionally absent
- evidence marker: `NARRATIVE_DIALOGUE_RUNTIME_TEST_FAIL count=1`

RED가 production implementation 부재 때문에 실패했으므로 TDD 전제와 일치한다.

## GREEN

- implementation commit: `33147794eb2732e63242b3db84adcdedd72a7142`
- workflow run: `31810129465`
- job: `94798479842`
- Godot: `4.7.1.stable.official.a13da4feb`
- result: success

실제 Godot 프로세스에서 확인된 항목:

1. model/session script load
2. sample JSON load + validation
3. stable flow entry beat
4. same-scene/moved-scene beat indexing
5. `STAY_IN_SCENE` background continuity
6. session start
7. first `dialogue_id` addressability
8. choice wait state
9. typed `STAY_IN_SCENE`
10. STAY does not change scene
11. STAY reaches target beat
12. typed `MOVE_SCENE`
13. MOVE changes scene
14. MOVE reaches target scene
15. moved scene starts at target beat first line
16. typed `END`
17. END closes session
18. terminal session state
19. invalid cross-scene `STAY_IN_SCENE` fail-closed

로그 terminal marker: `NARRATIVE_DIALOGUE_RUNTIME_TEST_PASS`.

별도 main scene headless smoke도 성공했고 다음 marker를 출력했다.

```text
NARRATIVE_DIALOGUE_SAMPLE_READY flow=after_school_sample beat=beat_intro scene=scene_hallway
```

## Implementation Reality Gate

```yaml
figma_rule_contract: MERGED
base_reference_json_model: IMPLEMENTED
base_reference_godot_model_loader: RUNTIME_PASS
base_reference_godot_session: RUNTIME_PASS
stable_id_lookup: RUNTIME_PASS
stay_in_scene_semantics: RUNTIME_PASS
move_scene_semantics: RUNTIME_PASS
end_semantics: RUNTIME_PASS
invalid_transition_fail_closed: RUNTIME_PASS
sample_main_scene_headless_startup: RUNTIME_PASS
figma_make_reference_source: IMPLEMENTED_IN_BASE
figma_make_reference_build: PENDING_THIS_PR
supplied_figma_make_url_mutation: BLOCKED_TOOL_SURFACE
figma_to_project_canon_round_trip: NOT_IMPLEMENTED
higodot_project_authoring: NOT_RUN
real_project_adoption: NOT_RUN
human_visual_ux_validation: NOT_RUN
production_ready: NO
```

## Adversarial boundaries

- Base reference runtime success를 실제 게임 프로젝트의 `VERIFIED`로 승격하지 않는다.
- Figma Make reference build 성공을 제공된 `/make/` URL 수정 성공으로 오인하지 않는다.
- Figma/Make는 narrative canon이 아니다.
- `STAY_IN_SCENE`/`MOVE_SCENE` 관계 검증을 우회하는 별도 edge 목록을 만들지 않는다.
- 조건/변수/세이브/현지화는 증거 없이 지원한다고 주장하지 않는다.
