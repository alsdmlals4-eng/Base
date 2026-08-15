const controlOptions = [
  ["", "제어 없음"], ["AU1", "AU1 내측 눈썹 올리기"], ["AU2", "AU2 외측 눈썹 올리기"], ["AU4", "AU4 눈썹 내리기"],
  ["AU5", "AU5 상안검 올리기"], ["AU6", "AU6 뺨 올리기"], ["AU7", "AU7 안검 조이기"], ["AU9", "AU9 코 주름"],
  ["AU10", "AU10 상순 올리기"], ["AU12", "AU12 입꼬리 올리기"], ["AU14", "AU14 보조개"], ["AU15", "AU15 입꼬리 내리기"],
  ["AU16", "AU16 하순 내리기"], ["AU17", "AU17 턱 올리기"], ["AU18", "AU18 입술 오므리기"], ["AU20", "AU20 입술 옆 늘리기"],
  ["AU23", "AU23 입술 조이기"], ["AU24", "AU24 입술 누르기"], ["AU25", "AU25 입술 벌리기"], ["AU26", "AU26 턱 내리기"],
  ["AU27", "AU27 입 크게 벌리기"], ["AU28", "AU28 입술 안으로"], ["AU41", "AU41 안검 처짐"], ["AU42", "AU42 가는 눈"],
  ["AU43", "AU43 눈 감기"], ["AU44", "AU44 눈 찌푸리기"], ["AU45", "AU45 깜박임"], ["AU46", "AU46 윙크"],
];
const intensities = ["A", "B", "C", "D", "E"];
let currentRunId = null;
let selectedCandidate = null;
let currentRunDeliveryEligible = false;
let studioConfig = { project_id: null, delivery_eligible: false, engine_provenance: "unavailable" };

const status = document.querySelector("#status");
const candidateGrid = document.querySelector("#candidate-grid");
const confirmDeliveryButton = document.querySelector("#confirm-delivery-button");
const downloadCopyButton = document.querySelector("#download-copy-button");
const figmaOpenLink = document.querySelector("#figma-open-link");
const pairingInfo = document.querySelector("#pairing-info");
const refreshDeliveryButton = document.querySelector("#refresh-delivery-button");

function resetDeliveryActions() {
  downloadCopyButton.disabled = true;
  downloadCopyButton.dataset.url = "";
  figmaOpenLink.hidden = true;
  figmaOpenLink.removeAttribute("href");
  pairingInfo.hidden = true;
  pairingInfo.textContent = "";
  refreshDeliveryButton.disabled = true;
  refreshDeliveryButton.dataset.url = "";
}

function resetRunState() {
  currentRunId = null;
  selectedCandidate = null;
  currentRunDeliveryEligible = false;
  candidateGrid.replaceChildren();
  confirmDeliveryButton.disabled = true;
  resetDeliveryActions();
  document.querySelector("#run-result").hidden = true;
  document.querySelector("#delivery-result").textContent = "";
  document.querySelector("#resolved-prompt").textContent = "";
  document.querySelector("#review-metadata").textContent = "";
}

function trustedFigmaUrl(value) {
  const parsed = new URL(value);
  if (
    parsed.protocol !== "https:" ||
    parsed.hostname !== "www.figma.com" ||
    !parsed.pathname.startsWith("/design/") ||
    parsed.username ||
    parsed.password ||
    (parsed.port && parsed.port !== "443")
  ) {
    throw new Error("검증되지 않은 Figma 주소는 열 수 없습니다.");
  }
  return parsed.toString();
}

function currentEditMode() {
  return document.querySelector("#edit-mode").value;
}

function editModeLabel(mode = currentEditMode()) {
  if (mode === "outfit") return "복장";
  if (mode === "scene") return "장소·배경";
  return "표정";
}

function updateSubmitLabel() {
  const importMode = studioConfig.run_mode === "subscription_handoff_import";
  const noun = editModeLabel();
  document.querySelector("#submit-button").textContent = importMode
    ? `${noun} 후보 가져오기 및 검증`
    : `${noun} 후보 생성`;
}

function applyRunModeUi() {
  const importMode = studioConfig.run_mode === "subscription_handoff_import";
  const openaiMode = studioConfig.run_mode === "openai";
  document.querySelector("#import-controls").hidden = !importMode;
  document.querySelector("#candidate-files").required = importMode;
  document.querySelector("#candidate-files").disabled = !importMode;
  document.querySelector("#declared-source").disabled = !importMode;
  document.querySelector("#cost-title").textContent = importMode
    ? "추가 비용 없는 가져오기"
    : openaiMode ? "OpenAI API 별도 과금 모드" : "시뮬레이션 검토 모드";
  document.querySelector("#cost-detail").textContent = importMode
    ? "ChatGPT·Figma 구독 또는 로컬 도구에서 만든 이미지를 검증하며, 이 도구는 유료 API를 호출하지 않습니다."
    : openaiMode
      ? "ChatGPT 구독과 별개인 OpenAI API 크레딧을 사용합니다. 요청 실행 시 비용이 발생할 수 있습니다."
      : "테스트 후보만 만들며 provider를 호출하지 않고 내보내기와 Figma 전달을 차단합니다.";
  updateSubmitLabel();
}

function applyEditModeUi() {
  const mode = currentEditMode();
  const expressionMode = mode === "expression";
  const promptGroup = document.querySelector("#edit-prompt-group");
  const editPrompt = document.querySelector("#edit-prompt");
  document.querySelector("#expression-controls").hidden = !expressionMode;
  promptGroup.hidden = expressionMode;
  editPrompt.disabled = expressionMode;
  editPrompt.required = !expressionMode;

  if (!expressionMode) {
    document.querySelector("#preset").value = "";
    document.querySelector("#gaze").value = "center";
    document.querySelector("#head-pose").value = "neutral";
  }

  const scope = document.querySelector("#edit-scope-note");
  if (mode === "outfit") {
    editPrompt.placeholder = "예: 짙은 남색 야전 코트와 황동 잠금장치";
    scope.textContent = "얼굴·헤어·체형·포즈·구도·배경·화풍은 유지하고 복장·의상·착용 장비만 변경합니다.";
  } else if (mode === "scene") {
    editPrompt.placeholder = "예: 비 오는 밤의 네온 골목";
    scope.textContent = "캐릭터 얼굴·헤어·복장·체형·포즈·구도·화풍은 유지하고 장소·환경·배경만 변경합니다.";
  } else {
    scope.textContent = "";
  }
  updateSubmitLabel();
}

function option(value, label) {
  const element = document.createElement("option");
  element.value = value;
  element.textContent = label;
  return element;
}

function buildControlRows() {
  const root = document.querySelector("#control-rows");
  for (let index = 0; index < 4; index += 1) {
    const row = document.createElement("div");
    row.className = "control-row";
    const code = document.createElement("select");
    code.dataset.controlCode = String(index);
    controlOptions.forEach(([value, label]) => code.append(option(value, label)));
    const intensity = document.createElement("select");
    intensity.dataset.intensity = String(index);
    intensities.forEach((value) => intensity.append(option(value, `강도 ${value}`)));
    intensity.value = "C";
    const side = document.createElement("select");
    side.dataset.side = String(index);
    side.append(option("", "윙크 눈 선택"), option("left", "왼쪽 눈"), option("right", "오른쪽 눈"));
    row.append(code, intensity, side);
    root.append(row);
  }
}

function controlsFromForm() {
  const controls = [];
  document.querySelectorAll("[data-control-code]").forEach((codeInput) => {
    if (!codeInput.value) return;
    const index = codeInput.dataset.controlCode;
    const control = {
      code: codeInput.value,
      intensity: document.querySelector(`[data-intensity="${index}"]`).value,
    };
    if (control.code === "AU46") {
      const side = document.querySelector(`[data-side="${index}"]`).value;
      if (!side) throw new Error("AU46 윙크에는 왼쪽 또는 오른쪽 눈을 지정해야 합니다.");
      control.side = side;
    }
    controls.push(control);
  });
  return controls;
}

function requestPayload() {
  const editMode = currentEditMode();
  const expressionMode = editMode === "expression";
  const preset = expressionMode ? (document.querySelector("#preset").value || null) : null;
  const controls = expressionMode ? controlsFromForm() : [];
  if (preset && controls.length) throw new Error("프리셋과 직접 얼굴 제어를 동시에 선택할 수 없습니다.");
  const editPrompt = expressionMode ? null : document.querySelector("#edit-prompt").value.trim();
  if (!expressionMode && !editPrompt) throw new Error(`${editModeLabel(editMode)} 변경 요청을 입력하세요.`);
  return {
    project_id: document.querySelector("#project-id").value,
    asset_id: document.querySelector("#asset-id").value,
    anchor: {
      source_path: document.querySelector("#source-path").value,
      figma_node_url: document.querySelector("#figma-url").value,
      approval_status: "approved",
    },
    edit_mode: editMode,
    edit_prompt: editPrompt,
    controls,
    gaze: expressionMode ? document.querySelector("#gaze").value : "center",
    head_pose: expressionMode ? document.querySelector("#head-pose").value : "neutral",
    preset,
    candidate_count: Number(document.querySelector("#candidate-count").value),
  };
}

async function request(path, options = {}) {
  if (options.method && options.method !== "GET") {
    options.headers = { ...(options.headers || {}), "X-Studio-CSRF": studioConfig.csrf_token };
  }
  const response = await fetch(path, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || "요청을 처리할 수 없습니다.");
  return payload;
}

function renderCandidates(run) {
  candidateGrid.replaceChildren();
  selectedCandidate = null;
  for (let index = 0; index < run.candidate_count; index += 1) {
    const card = document.createElement("label");
    card.className = "candidate";
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "candidate";
    radio.value = String(index);
    radio.addEventListener("change", () => {
      selectedCandidate = index;
      confirmDeliveryButton.disabled = !currentRunDeliveryEligible;
      resetDeliveryActions();
      document.querySelector("#delivery-result").textContent = "";
    });
    const image = document.createElement("img");
    image.src = `/api/runs/${run.run_id}/candidates/${index}`;
    image.alt = `캐릭터 편집 후보 ${index + 1}`;
    card.append(radio, document.createTextNode(` 후보 ${index + 1}`), image);
    candidateGrid.append(card);
  }
}

function applyDeliveryResult(result) {
  if (typeof result.delivery_status_url !== "string" || result.delivery_status_url !== `/api/runs/${currentRunId}/delivery-status`) {
    throw new Error("검증되지 않은 전달 상태 경로입니다.");
  }
  downloadCopyButton.dataset.url = result.download_url;
  downloadCopyButton.disabled = result.download_state !== "DOWNLOAD_READY";
  figmaOpenLink.href = trustedFigmaUrl(result.figma_url);
  figmaOpenLink.hidden = false;
  refreshDeliveryButton.dataset.url = result.delivery_status_url;
  refreshDeliveryButton.disabled = result.figma_delivery === "VERIFIED" || result.figma_delivery === "EXPIRED";

  if (result.bridge_state === "PAIRING_REQUIRED") {
    if (typeof result.pairing_code !== "string" || !/^\d{6}$/.test(result.pairing_code)) {
      throw new Error("Figma 연결 코드가 유효하지 않습니다.");
    }
    pairingInfo.hidden = false;
    pairingInfo.textContent = `Figma Bridge 연결 필요 · Figma 파일에서 Base Tool Hub Figma Bridge를 열고 연결 코드 ${result.pairing_code}를 입력하세요.`;
  } else {
    pairingInfo.hidden = true;
    pairingInfo.textContent = "";
  }

  const deliveryLabel = result.figma_delivery === "VERIFIED"
    ? "검증 완료"
    : result.figma_delivery === "BRIDGE_REQUIRED"
      ? "연결 필요"
      : result.figma_delivery === "EXPIRED" ? "만료" : "전달 대기";
  const lines = [
    `프로젝트 저장       ${result.project_save}`,
    `Figma 전달          ${result.figma_delivery}`,
    `Figma 상태          ${deliveryLabel}`,
    `Bridge 상태         ${result.bridge_state}`,
    `PC 다운로드         ${result.download_state}`,
    `Figma 대상          ${result.target_node_name}`,
    `전달 ID             ${result.delivery_id}`,
    `SHA-256             ${result.content_sha256}`,
  ];
  if (result.bridge_state === "PAIRING_REQUIRED") lines.push(`연결 코드            ${result.pairing_code}`);
  document.querySelector("#delivery-result").textContent = lines.join("\n");

  if (result.figma_delivery === "VERIFIED") {
    status.textContent = `후보 ${selectedCandidate + 1} 확정 · 프로젝트 저장 및 Figma readback 검증이 완료되었습니다. PC 사본도 선택적으로 받을 수 있습니다.`;
  } else if (result.bridge_state === "PAIRING_REQUIRED") {
    status.textContent = `후보 ${selectedCandidate + 1} 확정 · 프로젝트 저장 완료 · Figma Bridge 연결이 필요합니다. Figma 열기 후 6자리 연결 코드를 입력하세요.`;
  } else if (result.figma_delivery === "EXPIRED") {
    status.textContent = `후보 ${selectedCandidate + 1}의 프로젝트 저장은 유지됐지만 Figma 전달 작업이 만료되었습니다.`;
  } else {
    status.textContent = `후보 ${selectedCandidate + 1} 확정 · 프로젝트 저장 완료 · ${result.target_node_name} 전달이 진행 중입니다.`;
  }
}

document.querySelector("#expression-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  resetRunState();
  try {
    const payload = requestPayload();
    status.textContent = studioConfig.run_mode === "subscription_handoff_import"
      ? `${editModeLabel(payload.edit_mode)} 후보 파일을 검증하고 가져오는 중입니다…`
      : `${editModeLabel(payload.edit_mode)} 후보를 생성하는 중입니다…`;
    let run;
    if (studioConfig.run_mode === "subscription_handoff_import") {
      const files = [...document.querySelector("#candidate-files").files];
      if (files.length !== payload.candidate_count) throw new Error(`후보 수 ${payload.candidate_count}개와 선택 파일 ${files.length}개가 같아야 합니다.`);
      const body = new FormData();
      body.append("request_json", JSON.stringify(payload));
      body.append("declared_source", document.querySelector("#declared-source").value);
      files.forEach((file) => body.append("candidates", file));
      run = await request("/api/import-runs", { method: "POST", body });
    } else {
      run = await request("/api/runs", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(payload) });
    }
    if (run.status === "blocked") {
      resetRunState();
      status.textContent = `생성 차단됨 · ${(run.warnings || []).join(" ") || "엔진 결과를 검증할 수 없습니다."}`;
      return;
    }
    currentRunId = run.run_id;
    currentRunDeliveryEligible = Boolean(run.engine.delivery_eligible);
    document.querySelector("#run-result").hidden = false;
    document.querySelector("#resolved-prompt").textContent = run.generation_instruction;
    const resolvedControls = run.resolved_expression.controls
      .map((control) => `${control.code} (강도 ${control.intensity}${control.side ? `, 캐릭터 기준 ${control.side}` : ""})`)
      .join(", ") || "없음";
    const editDetail = payload.edit_mode === "expression"
      ? `해석된 제어: ${resolvedControls}`
      : `변경 모드: ${editModeLabel(payload.edit_mode)} · 변경 요청: ${payload.edit_prompt}`;
    document.querySelector("#review-metadata").textContent =
      `${editDetail} · 원본 SHA-256: ${run.lineage.anchor_sha256}`;
    document.querySelector("#delivery-result").textContent = "";
    confirmDeliveryButton.disabled = true;
    resetDeliveryActions();
    renderCandidates(run);
    status.textContent = run.run_mode === "subscription_handoff_import"
      ? `${run.cost.cost_route} · provider_call_made=false · 후보를 비교하고 하나를 선택하세요.`
      : currentRunDeliveryEligible
        ? "후보를 비교하고 하나를 선택하세요."
        : `${studioConfig.engine_provenance.toUpperCase()} / DELIVERY_BLOCKED · 후보 검토만 가능하며 확정 및 전달은 차단됩니다.`;
  } catch (error) { status.textContent = error.message; }
});

confirmDeliveryButton.addEventListener("click", async () => {
  if (currentRunId === null || selectedCandidate === null) return;
  confirmDeliveryButton.disabled = true;
  resetDeliveryActions();
  status.textContent = `후보 ${selectedCandidate + 1}을 확정하고 프로젝트 저장 및 Figma 전달을 준비하는 중입니다…`;
  try {
    const result = await request(`/api/runs/${currentRunId}/confirm-delivery`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ selected_candidate: selectedCandidate }),
    });
    applyDeliveryResult(result);
  } catch (error) {
    resetDeliveryActions();
    status.textContent = error.message;
  } finally {
    confirmDeliveryButton.disabled = !currentRunDeliveryEligible || selectedCandidate === null;
  }
});

refreshDeliveryButton.addEventListener("click", async () => {
  if (!refreshDeliveryButton.dataset.url) return;
  refreshDeliveryButton.disabled = true;
  status.textContent = "Figma 전달 상태와 readback 영수증을 확인하는 중입니다…";
  try {
    const result = await request(refreshDeliveryButton.dataset.url);
    applyDeliveryResult(result);
  } catch (error) {
    status.textContent = error.message;
    refreshDeliveryButton.disabled = false;
  }
});

downloadCopyButton.addEventListener("click", () => {
  const url = downloadCopyButton.dataset.url;
  if (!url) return;
  const link = document.createElement("a");
  link.href = url;
  link.download = "";
  link.hidden = true;
  document.body.append(link);
  link.click();
  link.remove();
});

async function bootstrap() {
  try {
    studioConfig = await request("/api/config");
    document.querySelector("#project-id").value = studioConfig.project_id || "";
    applyRunModeUi();
    applyEditModeUi();
    if (!studioConfig.delivery_eligible) {
      status.textContent = `${studioConfig.engine_provenance.toUpperCase()} / DELIVERY_BLOCKED · 실제 생성 엔진이 아닙니다.`;
    }
  } catch (error) {
    status.textContent = error.message;
  }
}

buildControlRows();
document.querySelector("#edit-mode").addEventListener("change", () => {
  resetRunState();
  applyEditModeUi();
});
document.querySelector("#candidate-files").addEventListener("change", (event) => {
  document.querySelector("#file-count").textContent = `선택한 후보 ${event.target.files.length}개`;
});
bootstrap();
