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
const exportButton = document.querySelector("#export-button");
const deliveryButton = document.querySelector("#delivery-button");

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
  const preset = document.querySelector("#preset").value || null;
  const controls = controlsFromForm();
  if (preset && controls.length) throw new Error("프리셋과 직접 얼굴 제어를 동시에 선택할 수 없습니다.");
  return {
    project_id: document.querySelector("#project-id").value,
    asset_id: document.querySelector("#asset-id").value,
    anchor: {
      source_path: document.querySelector("#source-path").value,
      figma_node_url: document.querySelector("#figma-url").value,
      approval_status: "approved",
    },
    controls,
    gaze: document.querySelector("#gaze").value,
    head_pose: document.querySelector("#head-pose").value,
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
      exportButton.disabled = !currentRunDeliveryEligible;
    });
    const image = document.createElement("img");
    image.src = `/api/runs/${run.run_id}/candidates/${index}`;
    image.alt = `표정 후보 ${index + 1}`;
    card.append(radio, document.createTextNode(` 후보 ${index + 1}`), image);
    candidateGrid.append(card);
  }
}

document.querySelector("#expression-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  try {
    status.textContent = "표정 제어를 검증하고 후보를 준비하는 중입니다…";
    const run = await request("/api/runs", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(requestPayload()) });
    if (run.status === "blocked") {
      currentRunId = null;
      selectedCandidate = null;
      candidateGrid.replaceChildren();
      exportButton.disabled = true;
      deliveryButton.disabled = true;
      document.querySelector("#run-result").hidden = true;
      status.textContent = `생성 차단됨 · ${(run.warnings || []).join(" ") || "엔진 결과를 검증할 수 없습니다."}`;
      return;
    }
    currentRunId = run.run_id;
    currentRunDeliveryEligible = Boolean(run.engine.delivery_eligible);
    document.querySelector("#run-result").hidden = false;
    document.querySelector("#resolved-prompt").textContent = run.generation_instruction;
    const resolvedControls = run.resolved_expression.controls
      .map((control) => `${control.code} (강도 ${control.intensity}${control.side ? `, 캐릭터 기준 ${control.side}` : ""})`)
      .join(", ") || "중립";
    document.querySelector("#review-metadata").textContent =
      `해석된 제어: ${resolvedControls} · 원본 SHA-256: ${run.lineage.anchor_sha256}`;
    document.querySelector("#packet").textContent = "";
    exportButton.disabled = true;
    deliveryButton.disabled = true;
    renderCandidates(run);
    status.textContent = currentRunDeliveryEligible
      ? "후보를 비교하고 하나를 선택하세요."
      : `${studioConfig.engine_provenance.toUpperCase()} / DELIVERY_BLOCKED · 후보 검토만 가능하며 내보내기와 Figma 전달은 차단됩니다.`;
  } catch (error) { status.textContent = error.message; }
});

exportButton.addEventListener("click", async () => {
  try {
    const run = await request(`/api/runs/${currentRunId}/export`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ selected_candidate: selectedCandidate }) });
    deliveryButton.disabled = false;
    status.textContent = `후보 ${run.selected_candidate + 1}을 프로젝트 내부 출력 경로에 내보냈습니다.`;
  } catch (error) { status.textContent = error.message; }
});

deliveryButton.addEventListener("click", async () => {
  try {
    const packet = await request(`/api/runs/${currentRunId}/figma-delivery`, { method: "POST" });
    document.querySelector("#packet").textContent = JSON.stringify(packet, null, 2);
    status.textContent = "전달 패킷을 준비했습니다. Use this packet only in the matching project GPT workspace with the Figma connector.";
  } catch (error) { status.textContent = error.message; }
});

async function bootstrap() {
  try {
    studioConfig = await request("/api/config");
    document.querySelector("#project-id").value = studioConfig.project_id || "";
    if (!studioConfig.delivery_eligible) {
      status.textContent = `${studioConfig.engine_provenance.toUpperCase()} / DELIVERY_BLOCKED · 실제 생성 엔진이 아닙니다.`;
    }
  } catch (error) {
    status.textContent = error.message;
  }
}

buildControlRows();
bootstrap();
