const state = { runId: null, request: null, frameCount: 0, selected: [], active: null, transforms: {}, timer: null };
const $ = (selector) => document.querySelector(selector);

function setStatus(text, blocked = false) {
  const badge = $("#run-status");
  badge.textContent = text;
  badge.classList.toggle("blocked", blocked);
}

function frameUrl(index) { return `/api/runs/${state.runId}/frames/${index}`; }

function curationPayload() {
  return { selected: state.selected, transforms: state.transforms, rejected: [...Array(state.frameCount).keys()].filter((index) => !state.selected.includes(index)) };
}

function renderCandidates() {
  const grid = $("#candidate-grid");
  grid.replaceChildren();
  for (let index = 0; index < state.frameCount; index += 1) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `frame-card${state.selected.includes(index) ? " selected" : ""}${state.active === index ? " active" : ""}`;
    button.setAttribute("aria-pressed", String(state.selected.includes(index)));
    const image = document.createElement("img");
    image.src = frameUrl(index);
    image.alt = `후보 프레임 ${index + 1}`;
    const label = document.createElement("span");
    label.textContent = `후보 ${index + 1}`;
    button.append(image, label);
    button.addEventListener("click", () => { state.active = index; renderAll(); });
    grid.append(button);
  }
}

function renderSequence() {
  const sequence = $("#sequence");
  sequence.replaceChildren();
  state.selected.forEach((index, position) => {
    const item = document.createElement("article");
    item.className = "selected-frame";
    const image = document.createElement("img");
    image.src = frameUrl(index);
    image.alt = `채택 프레임 ${position + 1}`;
    const title = document.createElement("strong");
    title.textContent = `${position + 1}. 후보 ${index + 1}`;
    const controls = $("#frame-actions-template").content.cloneNode(true);
    const previous = controls.querySelector('[data-action="previous"]');
    previous.disabled = position === 0;
    previous.addEventListener("click", () => move(position, -1));
    const next = controls.querySelector('[data-action="next"]');
    next.disabled = position === state.selected.length - 1;
    next.addEventListener("click", () => move(position, 1));
    const remove = controls.querySelector('[data-action="remove"]');
    remove.addEventListener("click", () => { if (confirm("이 프레임을 채택 목록에서 제거할까요?")) { state.selected = state.selected.filter((value) => value !== index); if (state.active === index) state.active = state.selected[0] ?? null; renderAll(); } });
    item.append(image, title, controls); sequence.append(item);
  });
}

function move(position, offset) {
  const target = position + offset;
  [state.selected[position], state.selected[target]] = [state.selected[target], state.selected[position]];
  renderAll();
}

function renderPreview() {
  const image = $("#preview-image");
  const index = state.active ?? state.selected[0];
  if (index === undefined) { image.removeAttribute("src"); return; }
  image.src = frameUrl(index);
  const transform = state.transforms[index] || { dx: 0, dy: 0, scale: 1 };
  image.style.transform = `translate(${transform.dx}px, ${transform.dy}px) scale(${transform.scale})`;
}

function renderAll() {
  renderCandidates(); renderSequence(); renderPreview();
  $("#selection-count").textContent = `선택 ${state.selected.length} / 요청 ${state.frameCount} 프레임`;
  $("#export-button").disabled = state.selected.length !== state.frameCount;
  $("#play-preview").disabled = state.selected.length === 0;
}

$("#request-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const request = {
    project_id: form.get("project_id"), asset_id: form.get("asset_id"), asset_kind: form.get("asset_kind"), output_root: `art/animation-runs/${form.get("asset_id")}`,
    anchor: { source_path: form.get("source_path"), figma_node_url: form.get("figma_node_url"), approval_status: "approved" },
    action: { name: form.get("action_name"), direction: form.get("direction"), frame_count: Number(form.get("frame_count")), fps: Number(form.get("fps")), loop_mode: form.get("loop_mode"), prompt: form.get("prompt") }
  };
  setStatus("후보 생성 중…");
  const response = await fetch("/api/runs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(request) });
  const result = await response.json();
  if (!response.ok || result.status === "blocked") { $("#warning-panel").textContent = result.detail || result.warnings?.join(" ") || "생성이 차단되었습니다."; setStatus("차단됨", true); return; }
  state.runId = result.run_id; state.request = request; state.frameCount = result.frame_count; state.selected = [...Array(result.frame_count).keys()]; state.active = 0; state.transforms = {};
  $("#source-path").textContent = request.anchor.source_path;
  $("#source-image").src = `/api/runs/${state.runId}/anchor`;
  $("#anchor-proof").textContent = `승인됨 · ${request.anchor.figma_node_url}`;
  $("#warning-panel").textContent = "후보 생성 완료. 채택 순서를 검토하세요.";
  setStatus("후보 생성됨"); renderAll();
});

$("#select-all").addEventListener("click", () => { state.selected = [...Array(state.frameCount).keys()]; state.active ??= 0; renderAll(); });
$("#toggle-guides").addEventListener("change", (event) => $("#candidate-grid").classList.toggle("guide-grid", event.target.checked));
$("#apply-transform").addEventListener("click", () => { if (state.active === null) return; state.transforms[state.active] = { dx: Number($("#transform-x").value), dy: Number($("#transform-y").value), scale: Number($("#transform-scale").value) }; renderAll(); });
$("#export-button").addEventListener("click", async () => { const response = await fetch(`/api/runs/${state.runId}/export`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(curationPayload()) }); const result = await response.json(); setStatus(result.status === "exported" ? "내보내기 완료" : "내보내기 차단됨", result.status !== "exported"); $("#warning-panel").textContent = result.detail || (result.status === "exported" ? "프로젝트 출력 경로에 프레임·GIF·아틀라스·Godot 핸드오프를 저장했습니다." : "선택을 확인하세요."); });
$("#play-preview").addEventListener("click", () => { if (state.timer) { clearInterval(state.timer); state.timer = null; return; } let position = 0; const fps = state.request.action.fps; state.timer = setInterval(() => { state.active = state.selected[position % state.selected.length]; position += 1; renderAll(); }, 1000 / fps); });
