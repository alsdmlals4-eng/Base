const state = {
  runId: null,
  request: null,
  frameCount: 0,
  selected: [],
  active: null,
  transforms: {},
  timer: null,
  exported: false,
  runDeliveryEligible: false,
  uploadQueue: [],
  deliveryConfirmed: false,
  config: { project_id: null, delivery_eligible: false, engine_provenance: "unavailable" }
};
const $ = (selector) => document.querySelector(selector);

function setStatus(text, blocked = false) {
  const badge = $("#run-status");
  badge.textContent = text;
  badge.classList.toggle("blocked", blocked);
}

async function api(path, options = {}) {
  const request = { ...options, headers: { ...(options.headers || {}) } };
  if ((request.method || "GET").toUpperCase() !== "GET") {
    request.headers["X-Studio-CSRF"] = state.config.csrf_token;
  }
  const response = await fetch(path, request);
  const result = await response.json();
  if (!response.ok) throw new Error(result.detail || "요청이 차단되었습니다.");
  return result;
}

function resetRunState() {
  if (state.timer) clearInterval(state.timer);
  state.runId = null;
  state.request = null;
  state.frameCount = 0;
  state.selected = [];
  state.active = null;
  state.transforms = {};
  state.timer = null;
  state.runDeliveryEligible = false;
  state.exported = false;
  state.deliveryConfirmed = false;
  $("#source-image").removeAttribute("src");
  $("#source-path").textContent = "";
  $("#anchor-proof").textContent = "";
  $("#figma-delivery-status").textContent = "";
  $("#warning-panel").textContent = "";
  const download = $("#confirmed-download");
  download.hidden = true;
  download.removeAttribute("href");
  renderAll();
}

function applyRunModeUi() {
  const importMode = state.config.run_mode === "subscription_handoff_import";
  const pinnedMode = state.config.run_mode === "pinned_sprite_gen";
  $("#import-controls").hidden = !importMode;
  $("#frame-files").required = importMode;
  $("#frame-files").disabled = !importMode;
  $("#declared-source").disabled = !importMode;
  $("#mode-title").textContent = importMode ? "애니메이션 가져오기" : "애니메이션 후보 생성";
  $("#cost-title").textContent = importMode
    ? "추가 비용 없는 가져오기"
    : pinnedMode ? "고정 sprite-gen 실행 모드" : "시뮬레이션 검토 모드";
  $("#cost-detail").textContent = importMode
    ? "ChatGPT·Figma 구독 또는 로컬 도구에서 만든 프레임을 검증하며, 이 도구는 유료 API를 호출하지 않습니다."
    : pinnedMode
      ? "검증된 고정 sprite-gen 어댑터를 실행합니다. 연결된 생성기의 비용·라이선스는 해당 구성에 따릅니다."
      : "테스트 프레임만 만들며 외부 provider를 호출하지 않고 내보내기와 Figma 전달을 차단합니다.";
  $("#submit-button").textContent = importMode ? "프레임 가져오기 및 검증" : "애니메이션 후보 생성";
}

function frameUrl(index) {
  return `/api/runs/${state.runId}/frames/${index}`;
}

function curationPayload() {
  return {
    selected: state.selected,
    transforms: state.transforms,
    rejected: [...Array(state.frameCount).keys()].filter((index) => !state.selected.includes(index))
  };
}

function mutationHeaders() {
  return { "Content-Type": "application/json", "X-Studio-CSRF": state.config.csrf_token };
}

function moveUpload(position, offset) {
  const target = position + offset;
  if (target < 0 || target >= state.uploadQueue.length) return;
  [state.uploadQueue[position], state.uploadQueue[target]] = [state.uploadQueue[target], state.uploadQueue[position]];
  renderImportQueue();
}

function renderImportQueue() {
  const root = $("#import-queue");
  root.replaceChildren();
  state.uploadQueue.forEach((entry, position) => {
    const row = document.createElement("div");
    row.className = "import-file";
    row.dataset.uploadId = entry.id;
    const label = document.createElement("span");
    label.textContent = `${position + 1}. ${entry.file.name}`;
    const previous = document.createElement("button");
    previous.type = "button";
    previous.textContent = "앞";
    previous.disabled = position === 0;
    previous.addEventListener("click", () => moveUpload(position, -1));
    const next = document.createElement("button");
    next.type = "button";
    next.textContent = "뒤";
    next.disabled = position === state.uploadQueue.length - 1;
    next.addEventListener("click", () => moveUpload(position, 1));
    const remove = document.createElement("button");
    remove.type = "button";
    remove.textContent = "제거";
    remove.addEventListener("click", () => {
      state.uploadQueue = state.uploadQueue.filter((item) => item.id !== entry.id);
      renderImportQueue();
    });
    row.append(label, previous, next, remove);
    root.append(row);
  });
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
    button.addEventListener("click", () => {
      state.active = index;
      renderAll();
    });
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
    remove.addEventListener("click", () => {
      if (confirm("이 프레임을 채택 목록에서 제거할까요?")) {
        state.selected = state.selected.filter((value) => value !== index);
        if (state.active === index) state.active = state.selected[0] ?? null;
        renderAll();
      }
    });
    item.append(image, title, controls);
    sequence.append(item);
  });
}

function move(position, offset) {
  const target = position + offset;
  if (target < 0 || target >= state.selected.length) return;
  [state.selected[position], state.selected[target]] = [state.selected[target], state.selected[position]];
  renderAll();
}

function renderPreview() {
  const image = $("#preview-image");
  const index = state.active ?? state.selected[0];
  if (index === undefined) {
    image.removeAttribute("src");
    return;
  }
  image.src = frameUrl(index);
  const transform = state.transforms[index] || { dx: 0, dy: 0, scale: 1 };
  image.style.transform = `translate(${transform.dx}px, ${transform.dy}px) scale(${transform.scale})`;
}

function renderAll() {
  renderCandidates();
  renderSequence();
  renderPreview();
  $("#selection-count").textContent = `선택 ${state.selected.length} / 요청 ${state.frameCount} 프레임`;
  $("#export-button").disabled = state.selected.length !== state.frameCount || !state.runDeliveryEligible;
  $("#confirm-delivery-button").disabled = !state.exported;
  $("#refresh-delivery-button").disabled = !state.deliveryConfirmed;
  $("#play-preview").disabled = state.selected.length === 0;
}

function renderDelivery(result) {
  const panel = $("#figma-delivery-status");
  const pairing = result.pairing_code ? ` · 페어링 코드 ${result.pairing_code}` : "";
  panel.textContent = `${result.target_node_name} · ${result.bridge_state} · ${result.delivery_state}${pairing} · SHA ${result.content_sha256}`;
  const download = $("#confirmed-download");
  download.href = result.download_url;
  download.hidden = false;
  state.deliveryConfirmed = true;
  const verified = result.figma_delivery === "VERIFIED";
  setStatus(verified ? "Figma 전달 검증 완료" : "확정 및 전달 진행 중", false);
  renderAll();
}

$("#request-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  resetRunState();
  const form = new FormData(event.currentTarget);
  const request = {
    project_id: form.get("project_id"),
    asset_id: form.get("asset_id"),
    asset_kind: form.get("asset_kind"),
    mode: form.get("mode"),
    anchor: {
      source_path: form.get("source_path"),
      figma_node_url: form.get("figma_node_url"),
      approval_status: "approved"
    },
    action: {
      name: form.get("action_name"),
      direction: form.get("direction"),
      frame_count: Number(form.get("frame_count")),
      fps: Number(form.get("fps")),
      loop_mode: form.get("loop_mode"),
      prompt: form.get("prompt")
    }
  };
  let response;
  if (state.config.run_mode === "subscription_handoff_import") {
    if (state.uploadQueue.length !== request.action.frame_count) {
      $("#warning-panel").textContent = `프레임 수 ${request.action.frame_count}개와 업로드 ${state.uploadQueue.length}개가 같아야 합니다.`;
      setStatus("가져오기 차단됨", true);
      return;
    }
    setStatus("프레임 가져오기 및 검증 중…");
    const body = new FormData();
    body.append("request_json", JSON.stringify(request));
    body.append("declared_source", $("#declared-source").value);
    state.uploadQueue.forEach((entry) => body.append("frames", entry.file));
    response = await fetch("/api/import-runs", {
      method: "POST",
      headers: { "X-Studio-CSRF": state.config.csrf_token },
      body
    });
  } else {
    setStatus("후보 생성 중…");
    response = await fetch("/api/runs", {
      method: "POST",
      headers: mutationHeaders(),
      body: JSON.stringify(request)
    });
  }
  const result = await response.json();
  if (!response.ok || result.status === "blocked") {
    resetRunState();
    $("#warning-panel").textContent = result.detail || result.warnings?.join(" ") || "생성이 차단되었습니다.";
    setStatus("차단됨", true);
    renderAll();
    return;
  }
  state.runId = result.run_id;
  state.request = request;
  state.frameCount = result.frame_count;
  state.selected = [...Array(result.frame_count).keys()];
  state.active = 0;
  state.transforms = {};
  state.exported = false;
  state.deliveryConfirmed = false;
  state.runDeliveryEligible = Boolean(result.engine.delivery_eligible);
  $("#source-path").textContent = request.anchor.source_path;
  $("#source-image").src = `/api/runs/${state.runId}/anchor`;
  $("#anchor-proof").textContent = `${result.anchor_verification} · ${request.anchor.figma_node_url}`;
  if (result.run_mode === "subscription_handoff_import") {
    $("#warning-panel").textContent = `${result.cost.cost_route} · provider_call_made=false · ${result.warnings.join(" ") || "프레임 가져오기 완료. 채택 순서를 검토하세요."}`;
    setStatus("가져오기 완료");
  } else if (result.engine.delivery_eligible) {
    $("#warning-panel").textContent = "후보 생성 완료. 채택 순서를 검토하세요.";
    setStatus("후보 생성됨");
  } else {
    $("#warning-panel").textContent = `${result.engine.provenance.toUpperCase()} / DELIVERY_BLOCKED · 후보 검토만 가능하며 내보내기와 Figma 전달은 차단됩니다.`;
    setStatus("검토 전용", true);
  }
  renderAll();
});

$("#frame-files").addEventListener("change", (event) => {
  state.uploadQueue = [...event.target.files].map((file) => ({ id: crypto.randomUUID(), file }));
  renderImportQueue();
});

$("#select-all").addEventListener("click", () => {
  state.selected = [...Array(state.frameCount).keys()];
  state.active ??= 0;
  renderAll();
});

$("#toggle-guides").addEventListener("change", (event) => {
  $("#candidate-grid").classList.toggle("guide-grid", event.target.checked);
});

$("#apply-transform").addEventListener("click", () => {
  if (state.active === null) return;
  state.transforms[state.active] = {
    dx: Number($("#transform-x").value),
    dy: Number($("#transform-y").value),
    scale: Number($("#transform-scale").value)
  };
  renderAll();
});

$("#export-button").addEventListener("click", async () => {
  const response = await fetch(`/api/runs/${state.runId}/export`, {
    method: "POST",
    headers: mutationHeaders(),
    body: JSON.stringify(curationPayload())
  });
  const result = await response.json();
  state.exported = result.status === "exported";
  state.deliveryConfirmed = false;
  setStatus(state.exported ? "출력 준비 완료" : "출력 준비 차단됨", !state.exported);
  $("#warning-panel").textContent = result.detail || (state.exported
    ? "프로젝트 작업공간에 프레임·GIF·아틀라스·Godot 핸드오프를 준비했습니다."
    : "선택을 확인하세요.");
  renderAll();
});

$("#confirm-delivery-button").addEventListener("click", async () => {
  try {
    setStatus("확정 및 전달 중…");
    const confirmation = await api(`/api/runs/${encodeURIComponent(state.runId)}/confirm-delivery`, {
      method: "POST"
    });
    renderDelivery(confirmation);
  } catch (error) {
    $("#figma-delivery-status").textContent = `확정 및 전달 차단됨: ${error.message}`;
    setStatus("확정 및 전달 차단됨", true);
  }
});

$("#refresh-delivery-button").addEventListener("click", async () => {
  try {
    const result = await api(`/api/runs/${encodeURIComponent(state.runId)}/delivery-status`);
    renderDelivery(result);
  } catch (error) {
    $("#figma-delivery-status").textContent = `상태 확인 차단됨: ${error.message}`;
    setStatus("전달 상태 확인 차단됨", true);
  }
});

$("#play-preview").addEventListener("click", () => {
  if (state.timer) {
    clearInterval(state.timer);
    state.timer = null;
    return;
  }
  let position = 0;
  const fps = state.request.action.fps;
  state.timer = setInterval(() => {
    state.active = state.selected[position % state.selected.length];
    position += 1;
    renderAll();
  }, 1000 / fps);
});

async function bootstrap() {
  try {
    const response = await fetch("/api/config");
    const config = await response.json();
    if (!response.ok) throw new Error(config.detail || "도구 설정을 불러올 수 없습니다.");
    state.config = config;
    $("[name=project_id]").value = config.project_id || "";
    applyRunModeUi();
    if (!config.delivery_eligible) {
      $("#warning-panel").textContent = `${config.engine_provenance.toUpperCase()} / DELIVERY_BLOCKED · 실제 생성 엔진이 아닙니다.`;
      setStatus("검토 전용", true);
    }
    renderAll();
  } catch (error) {
    $("#warning-panel").textContent = error.message;
    setStatus("설정 오류", true);
  }
}

bootstrap();
