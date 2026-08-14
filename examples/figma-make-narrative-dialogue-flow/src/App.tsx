import { useMemo, useState } from "react";

type TransitionKind = "STAY_IN_SCENE" | "MOVE_SCENE" | "END";
type DialogueLine = { dialogue_id: string; speaker_id: string | null; text: string };
type Choice = { choice_id: string; text: string; target_beat_id: string | null; transition_kind: TransitionKind };
type DialogueBeat = { beat_id: string; title: string; dialogues: DialogueLine[]; choices: Choice[] };
type SceneGroup = {
  scene_id: string;
  location_id: string;
  title: string;
  background_ref: string;
  entry_beat_id: string;
  beats: DialogueBeat[];
};
type DialogueFlow = { format_version: 1; flow_id: string; entry_beat_id: string; scenes: SceneGroup[] };
type Selection =
  | { kind: "scene"; scene_id: string }
  | { kind: "beat"; beat_id: string }
  | { kind: "dialogue"; dialogue_id: string }
  | { kind: "choice"; choice_id: string };

type Indexes = {
  sceneById: Map<string, SceneGroup>;
  beatById: Map<string, DialogueBeat>;
  sceneIdByBeat: Map<string, string>;
  dialogueById: Map<string, { line: DialogueLine; beat_id: string }>;
  choiceById: Map<string, { choice: Choice; beat_id: string }>;
};

import sampleDialogue from "./sample_dialogue.json";

const INITIAL_FLOW = sampleDialogue as DialogueFlow;

function buildIndexes(flow: DialogueFlow): Indexes {
  const sceneById = new Map<string, SceneGroup>();
  const beatById = new Map<string, DialogueBeat>();
  const sceneIdByBeat = new Map<string, string>();
  const dialogueById = new Map<string, { line: DialogueLine; beat_id: string }>();
  const choiceById = new Map<string, { choice: Choice; beat_id: string }>();
  for (const scene of flow.scenes) {
    sceneById.set(scene.scene_id, scene);
    for (const beat of scene.beats) {
      beatById.set(beat.beat_id, beat);
      sceneIdByBeat.set(beat.beat_id, scene.scene_id);
      beat.dialogues.forEach((line) => dialogueById.set(line.dialogue_id, { line, beat_id: beat.beat_id }));
      beat.choices.forEach((choice) => choiceById.set(choice.choice_id, { choice, beat_id: beat.beat_id }));
    }
  }
  return { sceneById, beatById, sceneIdByBeat, dialogueById, choiceById };
}

function validateFlow(flow: DialogueFlow, indexes: Indexes): string[] {
  const errors: string[] = [];
  const ids = { scene: new Set<string>(), beat: new Set<string>(), dialogue: new Set<string>(), choice: new Set<string>() };
  const unique = (kind: keyof typeof ids, id: string) => {
    if (!id) errors.push(`${kind} id is empty`);
    else if (ids[kind].has(id)) errors.push(`duplicate ${kind} id: ${id}`);
    else ids[kind].add(id);
  };

  flow.scenes.forEach((scene) => {
    unique("scene", scene.scene_id);
    if (!scene.beats.some((beat) => beat.beat_id === scene.entry_beat_id)) errors.push(`${scene.scene_id}: entry beat is outside the scene`);
    scene.beats.forEach((beat) => {
      unique("beat", beat.beat_id);
      if (beat.dialogues.length === 0) errors.push(`${beat.beat_id}: at least one dialogue line is required`);
      if (beat.choices.length === 0) errors.push(`${beat.beat_id}: explicit END or transition choice is required`);
      beat.dialogues.forEach((line) => unique("dialogue", line.dialogue_id));
      beat.choices.forEach((choice) => {
        unique("choice", choice.choice_id);
        const sourceScene = scene.scene_id;
        const targetScene = choice.target_beat_id ? indexes.sceneIdByBeat.get(choice.target_beat_id) : undefined;
        if (choice.transition_kind === "END") {
          if (choice.target_beat_id) errors.push(`${choice.choice_id}: END must not have a target`);
          return;
        }
        if (!choice.target_beat_id || !targetScene) {
          errors.push(`${choice.choice_id}: target beat is missing`);
          return;
        }
        if (choice.transition_kind === "STAY_IN_SCENE" && sourceScene !== targetScene) errors.push(`${choice.choice_id}: STAY_IN_SCENE crosses scene boundary`);
        if (choice.transition_kind === "MOVE_SCENE" && sourceScene === targetScene) errors.push(`${choice.choice_id}: MOVE_SCENE stays in the same scene`);
      });
    });
  });
  if (!indexes.beatById.has(flow.entry_beat_id)) errors.push("flow entry beat does not exist");
  return errors;
}

function patchScene(flow: DialogueFlow, sceneId: string, patch: Partial<SceneGroup>): DialogueFlow {
  return { ...flow, scenes: flow.scenes.map((scene) => scene.scene_id === sceneId ? { ...scene, ...patch } : scene) };
}

function patchBeat(flow: DialogueFlow, beatId: string, patch: Partial<DialogueBeat>): DialogueFlow {
  return { ...flow, scenes: flow.scenes.map((scene) => ({ ...scene, beats: scene.beats.map((beat) => beat.beat_id === beatId ? { ...beat, ...patch } : beat) })) };
}

function patchDialogue(flow: DialogueFlow, dialogueId: string, patch: Partial<DialogueLine>): DialogueFlow {
  return { ...flow, scenes: flow.scenes.map((scene) => ({ ...scene, beats: scene.beats.map((beat) => ({ ...beat, dialogues: beat.dialogues.map((line) => line.dialogue_id === dialogueId ? { ...line, ...patch } : line) })) })) };
}

function patchChoice(flow: DialogueFlow, choiceId: string, patch: Partial<Choice>): DialogueFlow {
  return { ...flow, scenes: flow.scenes.map((scene) => ({ ...scene, beats: scene.beats.map((beat) => ({ ...beat, choices: beat.choices.map((choice) => choice.choice_id === choiceId ? { ...choice, ...patch } : choice) })) })) };
}

export default function App() {
  const [flow, setFlow] = useState<DialogueFlow>(() => structuredClone(INITIAL_FLOW));
  const [mode, setMode] = useState<"preview" | "edit">("preview");
  const indexes = useMemo(() => buildIndexes(flow), [flow]);
  const errors = useMemo(() => validateFlow(flow, indexes), [flow, indexes]);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <strong>NARRATIVE FLOW STUDIO</strong>
          <span>{flow.flow_id}</span>
        </div>
        <div className="toolbar">
          <button className={mode === "preview" ? "active" : ""} onClick={() => setMode("preview")}>Preview</button>
          <button className={mode === "edit" ? "active" : ""} onClick={() => setMode("edit")}>Edit</button>
          <button onClick={() => navigator.clipboard?.writeText(JSON.stringify(flow, null, 2))}>JSON 복사</button>
          <button onClick={() => setFlow(structuredClone(INITIAL_FLOW))}>샘플 복원</button>
        </div>
      </header>
      {errors.length > 0 && <div className="error-banner"><b>검증 오류 {errors.length}</b>{errors.map((error) => <span key={error}>{error}</span>)}</div>}
      {mode === "preview" && errors.length > 0
        ? <main className="preview-blocked"><b>PREVIEW BLOCKED</b><p>관계 오류를 수정해야 실행 미리보기를 시작할 수 있습니다.</p></main>
        : mode === "preview"
          ? <Preview flow={flow} indexes={indexes} />
          : <Editor flow={flow} indexes={indexes} setFlow={setFlow} />}
    </div>
  );
}

function Preview({ flow, indexes }: { flow: DialogueFlow; indexes: Indexes }) {
  const [beatId, setBeatId] = useState(flow.entry_beat_id);
  const [lineIndex, setLineIndex] = useState(0);
  const [ended, setEnded] = useState(false);
  const beat = indexes.beatById.get(beatId) ?? indexes.beatById.get(flow.entry_beat_id)!;
  const sceneId = indexes.sceneIdByBeat.get(beat.beat_id)!;
  const scene = indexes.sceneById.get(sceneId)!;
  const line = beat.dialogues[Math.min(lineIndex, beat.dialogues.length - 1)];
  const waiting = lineIndex >= beat.dialogues.length - 1;

  const reset = () => { setBeatId(flow.entry_beat_id); setLineIndex(0); setEnded(false); };
  const choose = (choice: Choice) => {
    if (choice.transition_kind === "END") { setEnded(true); return; }
    if (!choice.target_beat_id) return;
    setBeatId(choice.target_beat_id);
    setLineIndex(0);
  };

  return (
    <main className="preview-grid">
      <section className={`stage scene-${sceneId}`}>
        <div className="stage-meta"><span>{scene.location_id}</span><code>{scene.scene_id}</code></div>
        <h1>{scene.title}</h1>
        <p className="background-ref">{scene.background_ref}</p>
        <div className="dialogue-card">
          {ended ? <><b>END</b><p>샘플 흐름이 종료되었습니다.</p><button onClick={reset}>처음부터</button></> : <>
            <small>{beat.title} · {beat.beat_id} · {line.dialogue_id}</small>
            <b>{line.speaker_id ?? "내레이션"}</b>
            <p>{line.text}</p>
            {!waiting && <button onClick={() => setLineIndex((value) => value + 1)}>다음</button>}
            {waiting && <div className="choice-list">{beat.choices.map((choice) => <button key={choice.choice_id} onClick={() => choose(choice)}><span>{choice.text}</span><code>{choice.transition_kind}</code></button>)}</div>}
          </>}
        </div>
      </section>
      <FlowMap flow={flow} currentBeatId={beatId} />
    </main>
  );
}

function FlowMap({ flow, currentBeatId, onSelect }: { flow: DialogueFlow; currentBeatId?: string; onSelect?: (selection: Selection) => void }) {
  return (
    <section className="flow-map">
      <div className="section-heading"><b>DERIVED FLOW MAP</b><span>choice 관계에서 자동 파생</span></div>
      <div className="scene-columns">
        {flow.scenes.map((scene) => <div className="scene-column" key={scene.scene_id}>
          <button className="scene-header" onClick={() => onSelect?.({ kind: "scene", scene_id: scene.scene_id })}><b>{scene.title}</b><code>{scene.scene_id}</code></button>
          {scene.beats.map((beat) => <button key={beat.beat_id} className={`beat-card ${beat.beat_id === currentBeatId ? "current" : ""}`} onClick={() => onSelect?.({ kind: "beat", beat_id: beat.beat_id })}>
            <b>{beat.title}</b><code>{beat.beat_id}</code>
            <div>{beat.choices.map((choice) => <span key={choice.choice_id}>{choice.transition_kind === "END" ? "■ END" : `→ ${choice.target_beat_id}`} <em>{choice.transition_kind}</em></span>)}</div>
          </button>)}
        </div>)}
      </div>
    </section>
  );
}

function Editor({ flow, indexes, setFlow }: { flow: DialogueFlow; indexes: Indexes; setFlow: (flow: DialogueFlow) => void }) {
  const [selection, setSelection] = useState<Selection>({ kind: "scene", scene_id: flow.scenes[0].scene_id });
  const [activeBeatId, setActiveBeatId] = useState(flow.entry_beat_id);
  const activeBeat = indexes.beatById.get(activeBeatId) ?? indexes.beatById.get(flow.entry_beat_id)!;
  const activeSceneId = indexes.sceneIdByBeat.get(activeBeat.beat_id)!;

  const select = (next: Selection) => {
    setSelection(next);
    if (next.kind === "beat") setActiveBeatId(next.beat_id);
    if (next.kind === "dialogue") setActiveBeatId(indexes.dialogueById.get(next.dialogue_id)?.beat_id ?? activeBeatId);
    if (next.kind === "choice") setActiveBeatId(indexes.choiceById.get(next.choice_id)?.beat_id ?? activeBeatId);
    if (next.kind === "scene") setActiveBeatId(indexes.sceneById.get(next.scene_id)?.entry_beat_id ?? activeBeatId);
  };

  return (
    <main className="editor-grid">
      <aside className="navigator">
        <div className="section-heading"><b>SCENES / BEATS</b><span>Stable ID navigation</span></div>
        {flow.scenes.map((scene) => <div key={scene.scene_id} className="nav-scene">
          <button onClick={() => select({ kind: "scene", scene_id: scene.scene_id })}><b>{scene.title}</b><code>{scene.scene_id}</code></button>
          {scene.beats.map((beat) => <button key={beat.beat_id} className={beat.beat_id === activeBeatId ? "active" : ""} onClick={() => select({ kind: "beat", beat_id: beat.beat_id })}><span>{beat.title}</span><code>{beat.beat_id}</code></button>)}
        </div>)}
      </aside>

      <section className="workspace">
        <FlowMap flow={flow} currentBeatId={activeBeatId} onSelect={select} />
        <div className="beat-editor">
          <div className="section-heading"><b>{activeBeat.title}</b><span>{activeSceneId} / {activeBeat.beat_id}</span></div>
          <div className="item-grid">
            <div><h3>DIALOGUE LINES</h3>{activeBeat.dialogues.map((line) => <button className="editable-item" key={line.dialogue_id} onClick={() => select({ kind: "dialogue", dialogue_id: line.dialogue_id })}><code>{line.dialogue_id}</code><b>{line.speaker_id ?? "내레이션"}</b><span>{line.text}</span></button>)}</div>
            <div><h3>CHOICES</h3>{activeBeat.choices.map((choice) => <button className="editable-item" key={choice.choice_id} onClick={() => select({ kind: "choice", choice_id: choice.choice_id })}><code>{choice.choice_id}</code><b>{choice.text}</b><span>{choice.transition_kind} → {choice.target_beat_id ?? "END"}</span></button>)}</div>
          </div>
        </div>
      </section>

      <Inspector selection={selection} flow={flow} indexes={indexes} setFlow={setFlow} />
    </main>
  );
}

function Inspector({ selection, flow, indexes, setFlow }: { selection: Selection; flow: DialogueFlow; indexes: Indexes; setFlow: (flow: DialogueFlow) => void }) {
  if (selection.kind === "scene") {
    const scene = indexes.sceneById.get(selection.scene_id)!;
    return <aside className="inspector"><Title kind="SCENE" id={scene.scene_id} /><Field label="title" value={scene.title} onChange={(value) => setFlow(patchScene(flow, scene.scene_id, { title: value }))} /><Field label="location_id" value={scene.location_id} onChange={(value) => setFlow(patchScene(flow, scene.scene_id, { location_id: value }))} /><Field label="background_ref" value={scene.background_ref} onChange={(value) => setFlow(patchScene(flow, scene.scene_id, { background_ref: value }))} /><ReadOnly label="entry_beat_id" value={scene.entry_beat_id} /></aside>;
  }
  if (selection.kind === "beat") {
    const beat = indexes.beatById.get(selection.beat_id)!;
    return <aside className="inspector"><Title kind="BEAT" id={beat.beat_id} /><ReadOnly label="scene_id" value={indexes.sceneIdByBeat.get(beat.beat_id) ?? ""} /><Field label="title" value={beat.title} onChange={(value) => setFlow(patchBeat(flow, beat.beat_id, { title: value }))} /><ReadOnly label="dialogue_ids" value={beat.dialogues.map((line) => line.dialogue_id).join(", ")} /><ReadOnly label="choice_ids" value={beat.choices.map((choice) => choice.choice_id).join(", ")} /></aside>;
  }
  if (selection.kind === "dialogue") {
    const entry = indexes.dialogueById.get(selection.dialogue_id)!;
    return <aside className="inspector"><Title kind="DIALOGUE" id={entry.line.dialogue_id} /><ReadOnly label="beat_id" value={entry.beat_id} /><Field label="speaker_id" value={entry.line.speaker_id ?? ""} onChange={(value) => setFlow(patchDialogue(flow, entry.line.dialogue_id, { speaker_id: value.trim() ? value : null }))} /><Field label="text" value={entry.line.text} multiline onChange={(value) => setFlow(patchDialogue(flow, entry.line.dialogue_id, { text: value }))} /></aside>;
  }
  const entry = indexes.choiceById.get(selection.choice_id)!;
  const choice = entry.choice;
  return <aside className="inspector"><Title kind="CHOICE" id={choice.choice_id} /><ReadOnly label="source_beat_id" value={entry.beat_id} /><Field label="text" value={choice.text} onChange={(value) => setFlow(patchChoice(flow, choice.choice_id, { text: value }))} /><label><span>target_beat_id</span><select value={choice.target_beat_id ?? ""} disabled={choice.transition_kind === "END"} onChange={(event) => setFlow(patchChoice(flow, choice.choice_id, { target_beat_id: event.target.value || null }))}><option value="">—</option>{Array.from(indexes.beatById.keys()).map((id) => <option key={id}>{id}</option>)}</select></label><label><span>transition_kind</span><select value={choice.transition_kind} onChange={(event) => { const transition_kind = event.target.value as TransitionKind; setFlow(patchChoice(flow, choice.choice_id, { transition_kind, target_beat_id: transition_kind === "END" ? null : choice.target_beat_id })); }}><option>STAY_IN_SCENE</option><option>MOVE_SCENE</option><option>END</option></select></label></aside>;
}

function Title({ kind, id }: { kind: string; id: string }) { return <div className="inspector-title"><b>{kind} INSPECTOR</b><code>{id}</code></div>; }
function ReadOnly({ label, value }: { label: string; value: string }) { return <label><span>{label} · read-only</span><input value={value} readOnly /></label>; }
function Field({ label, value, onChange, multiline = false }: { label: string; value: string; onChange: (value: string) => void; multiline?: boolean }) { return <label><span>{label}</span>{multiline ? <textarea value={value} onChange={(event) => onChange(event.target.value)} /> : <input value={value} onChange={(event) => onChange(event.target.value)} />}</label>; }
