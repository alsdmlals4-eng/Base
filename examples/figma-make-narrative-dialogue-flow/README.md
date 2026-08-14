# Figma Make Narrative Dialogue Reference

이 예제는 사용자가 제공한 Figma Make 흐름을 `FIGMA_NARRATIVE_DIALOGUE_FLOW_PROFILE.md`의 Stable-ID 계약에 맞춰 다시 구성한 **Make용 reference source**다.

## 기존 Make에서 해결한 구조 문제

기존 Make 소스는 `Dialogue = {speaker, text}`, `Choice = {text, next}` 구조라 개별 대화/선택지에 durable identity가 없고, 실행용 `SCENES`와 시각화용 `MNODES/MEDGES`를 따로 유지한다.

이 예제는 다음으로 변경한다.

- `scene_id / beat_id / dialogue_id / choice_id` Stable ID
- `STAY_IN_SCENE / MOVE_SCENE / END` typed transition
- Preview와 Edit가 같은 `DialogueFlow` 상태 사용
- 분기 표시는 `choices`에서 derived되며 수동 edge canon 없음
- Scene / Beat / Dialogue / Choice 각각 Inspector에서 독립 선택
- Stable ID는 read-only, 내용/대상/transition은 WIP에서 수정 가능
- 관계 오류는 화면 상단에 즉시 표시
- 현재 draft JSON을 복사하여 책임 narrative source에 proposal로 전달 가능

## 실행

```bash
cd examples/figma-make-narrative-dialogue-flow
npm install --ignore-scripts --no-audit --no-fund
npm run build
```

`src/sample_dialogue.json`은 Godot reference fixture의 샘플과 **동일 Git blob**을 사용한다. 이것은 Base 검증용 mirror fixture이며 실제 프로젝트의 canonical narrative DB를 뜻하지 않는다.

## Figma Make 반영 경계

현재 연결된 Figma 도구는 `/make/` 파일의 소스를 읽을 수 있지만 Make 소스 쓰기 API는 제공하지 않는다. 따라서 이 저장소 예제가 build-pass하더라도 사용자가 제공한 Make URL 자체를 이 작업이 자동 변경했다고 주장하면 안 된다.

실제 Make에 적용할 때는 이 예제의 `src/App.tsx`, `src/styles.css`, `src/sample_dialogue.json`을 Make 프로젝트에 반영하고 Preview/Edit 동작을 다시 확인한다. Figma에서 변경한 narrative 내용은 계속 `DRAFT_VISUAL`/proposal이며 프로젝트 canonical data에 자동 승격하지 않는다.
