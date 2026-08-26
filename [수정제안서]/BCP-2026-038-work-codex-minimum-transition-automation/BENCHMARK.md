# BCP-2026-038 Benchmark Evidence

## 조사일과 범위

- 조사일: `2026-08-27`
- 목적: 중간 승인·전환을 줄이되 required checks, high-risk approval, evidence ceiling을 보존하는 현업 패턴 확인
- source policy: 공식 문서·공식 repository 우선

## 1. GitHub auto-merge

Source:

- <https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/automatically-merging-a-pull-request>

관찰:

- auto-merge는 required review와 required status check를 제거하지 않는다.
- 모든 merge requirement가 충족된 뒤 자동으로 병합한다.
- head/base identity가 바뀌는 경우 자동 병합 상태가 무효화될 수 있다.

판정:

- `ADOPT`: routine 병합 확인을 반복하는 대신 exact head·required check·ruleset 충족 뒤 자동 병합한다.
- `REJECT`: 검사 생략, 다른 SHA의 PASS 재사용, ruleset/admin bypass를 자동화로 부르지 않는다.

## 2. OpenAI Agents SDK Human-in-the-loop

Source:

- <https://openai.github.io/openai-agents-python/human_in_the_loop/>

관찰:

- approval rule은 호출별 조건 함수로 만들 수 있다.
- local shell/apply-patch와 hosted MCP는 programmatic approval callback을 통해 interruption 없이 자동 승인·거절할 수 있다.
- 안전하게 판정할 수 없는 malformed/unknown input은 fail closed로 manual approval에 남긴다.
- sticky approval은 같은 run의 동일 tool identity에 한정할 수 있다.

판정:

- `ADAPT`: current Slice와 protected scope 안의 routine 작업만 자동 승인하고, high-risk/unknown input은 보류한다.
- `ADOPT`: 미해결 approval 전체 때문에 run을 버리지 않고 승인된 호출은 계속하며 미해결 항목은 durable state로 보존한다.
- `REJECT`: project 전체·모든 tool·모든 미래 run에 무제한 always-approve를 부여하지 않는다.

## 3. DORA Working in small batches

Source:

- <https://dora.dev/capabilities/working-in-small-batches/>

관찰:

- 유효한 batch는 independent, negotiable, valuable, estimable, small, testable해야 한다.
- 독립적으로 검증 가능한 batch는 feedback과 rollback 비용을 낮춘다.

판정:

- `ADAPT`: Work→Codex 전환을 줄이되 작업 범위는 프로젝트 전체가 아니라 하나의 `PLAYABLE_MEANINGFUL_SLICE`로 고정한다.
- `REJECT`: 전환 횟수를 줄인다는 이유로 여러 Slice·장기 roadmap을 하나의 거대 구현 batch로 합치지 않는다.

## 4. GUT

Source:

- <https://github.com/bitwes/Gut>

관찰:

- GUT은 GDScript로 GDScript를 검증하는 Godot unit-test framework다.
- GUT 9.x는 Godot 4.x 계열을 대상으로 하며 exact compatibility 확인이 필요하다.

판정:

- `ADOPT`: 프로젝트가 이미 채택한 경우 deterministic domain/state regression에 사용한다.
- `REJECT`: 실제 UI render, build/export, device, human/player evidence를 GUT 하나로 대체하지 않는다.

## 5. Base HiGodot/GUT/Hera owner

Source:

- `docs/knowledge/godot/HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md`

관찰:

- HiGodot은 sole persistent authoring authority다.
- GUT은 adopted deterministic GDScript test authority다.
- Hera는 live QA and observability only이며 persistent source mutation은 금지한다.
- Hera는 normal gameplay input, runtime state assertion, screenshot, diagnostics에 사용할 수 있지만 Human/Player PASS를 만들지 않는다.

판정:

- `ADOPT`: Codex 구현 window에서 author → GUT → Hera → source-delta NONE → full diff 순서를 사용한다.
- `REJECT`: Hera를 두 번째 persistent writer로 사용하거나 screenshot diff를 미감·가독성·재미 승인으로 과장하지 않는다.

## 종합 결론

가장 강한 공통 패턴은 다음이다.

```text
bounded valuable Slice
→ safe calls use programmatic delegated approval
→ unknown/high-risk calls fail closed or defer
→ one consolidated implementation batch
→ deterministic + runtime machine evidence
→ required checks remain mandatory
→ automatic merge only after actual gates
→ human/player judgment remains a separate final milestone
```

이는 BCP-2026-038의 `대안 C — 승인된 Slice 안의 권장 기본값을 위임하고 고위험 항목만 국소 보류`를 지지한다.
