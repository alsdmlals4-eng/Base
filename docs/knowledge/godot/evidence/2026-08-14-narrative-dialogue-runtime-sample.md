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

## GREEN + adversarial recheck

최종 실행 로직 보완 후 검증한 head:

- executable head: `98551cb026ed45da2a3afe56a4daea9b9cf46494`
- workflow run: `31812031354`
- job: `94804706542`
- Godot: `4.7.1.stable.official.a13da4feb`
- Figma Make reference: Vite `6.3.5` production build success (`28 modules transformed`)
- result: success

실제 Godot 프로세스는 **22개 assertion을 모두 PASS**했다.

1. model implementation exists
2. session implementation exists
3. sample JSON loads and validates
4. stable flow entry beat
5. same-scene beat indexing
6. moved-scene beat indexing
7. `STAY_IN_SCENE` background continuity
8. session start
9. first `dialogue_id` addressability
10. choice wait state
11. typed `STAY_IN_SCENE`
12. STAY does not change scene
13. STAY reaches target Beat
14. typed `MOVE_SCENE`
15. MOVE changes Scene
16. MOVE reaches target Scene
17. moved Scene starts at target Beat first Line
18. typed `END`
19. END closes Session
20. terminal Session state
21. invalid cross-scene `STAY_IN_SCENE` fail-closed
22. Beat without explicit `END` or transition fail-closed

Godot terminal marker:

```text
NARRATIVE_DIALOGUE_RUNTIME_TEST_PASS
```

별도 main scene headless smoke도 성공했고 다음 marker를 출력했다.

```text
NARRATIVE_DIALOGUE_SAMPLE_READY flow=after_school_sample beat=beat_intro scene=scene_hallway
```

Make reference는 같은 run에서 `npm run build`가 exit 0으로 완료됐다. Edit WIP에서 관계 오류가 생기면 `PREVIEW BLOCKED` 상태를 렌더하도록 구현했으며, 이 동작의 존재는 Base contract test가 소스 계약으로 검사한다. 브라우저에서 사람의 포인터/키보드 상호작용을 수행한 UX 검증은 별도다.

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
implicit_dead_end_fail_closed: RUNTIME_PASS
sample_main_scene_headless_startup: RUNTIME_PASS
figma_make_reference_source: IMPLEMENTED_IN_BASE
figma_make_reference_build: BUILD_PASS
figma_make_invalid_preview_block_contract: IMPLEMENTED_BUILD_PASS
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
- implicit dead-end를 정상 종료처럼 취급하지 않는다. 종료는 명시적 `END`로 표현한다.
- 조건/변수/세이브/현지화는 증거 없이 지원한다고 주장하지 않는다.
