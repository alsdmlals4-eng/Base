const state = { csrf: "", session: null };
const statusBox = document.querySelector("#status");

function show(message, isError = false) {
  statusBox.textContent = message;
  statusBox.classList.toggle("error", isError);
}

async function api(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (options.body && !(options.body instanceof FormData)) headers.set("Content-Type", "application/json");
  if ((options.method || "GET") !== "GET") headers.set("X-QA-CSRF", state.csrf);
  const response = await fetch(path, { ...options, headers });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || `HTTP ${response.status}`);
  return payload;
}

function checklistFromText(value) {
  return value.split("\n").map(line => line.trim()).filter(Boolean).map(line => {
    const [item_id, ...label] = line.split("|");
    return { item_id, label: label.join("|") || item_id, required: true };
  });
}

function renderChecklist() {
  const root = document.querySelector("#checklist-results");
  root.replaceChildren();
  for (const item of state.session.checklist) {
    const row = document.createElement("div");
    row.className = "result-row";
    const label = document.createElement("strong"); label.textContent = item.label;
    const select = document.createElement("select"); select.setAttribute("aria-label", `${item.label} 결과`);
    for (const value of ["NOT_RUN", "PASS", "FAIL", "BLOCKED"]) {
      const option = document.createElement("option"); option.value = value; option.textContent = value; select.append(option);
    }
    const note = document.createElement("input"); note.setAttribute("aria-label", `${item.label} 메모`); note.placeholder = "확인 내용 또는 차단 이유";
    const button = document.createElement("button"); button.textContent = "저장";
    select.value = item.status;
    note.value = item.note || "";
    button.addEventListener("click", async () => {
      try {
        state.session = await api(`/api/sessions/${state.session.session_id}/results`, {
          method: "POST", body: JSON.stringify({ item_id: item.item_id, status: select.value, note: note.value })
        });
        show(`${item.label}: ${select.value} 저장됨`);
      } catch (error) { show(error.message, true); }
    });
    row.append(label, select, note, button); root.append(row);
  }
}

document.querySelector("#session-form").addEventListener("submit", async event => {
  event.preventDefault();
  try {
    state.session = await api("/api/sessions", { method: "POST", body: JSON.stringify({
      title: document.querySelector("#title").value,
      build_commit: document.querySelector("#build-commit").value,
      checklist: checklistFromText(document.querySelector("#checklist").value)
    })});
    document.querySelector("#readiness-gate").hidden = false;
    show(`세션 ${state.session.session_id} 준비됨 · 아직 실제 검증 전`);
  } catch (error) { show(error.message, true); }
});

document.querySelector("#ready-button").addEventListener("click", async () => {
  try {
    state.session = await api(`/api/sessions/${state.session.session_id}/visual-ux-ready`, {
      method: "POST", body: JSON.stringify({ acknowledgement: document.querySelector("#acknowledgement").value })
    });
    document.querySelector("#review-workspace").hidden = false;
    renderChecklist();
    show("이미지·UX 배치 확인됨 · 개발자 PC 검토 가능");
  } catch (error) { show(error.message, true); }
});

document.querySelector("#upload-button").addEventListener("click", async () => {
  const file = document.querySelector("#evidence-file").files[0];
  if (!file) return show("이미지 파일을 선택하세요.", true);
  const body = new FormData(); body.append("image", file);
  try {
    const evidence = await api(`/api/sessions/${state.session.session_id}/evidence`, { method: "POST", body });
    show(`이미지 증거 저장됨 · SHA-256 ${evidence.sha256.slice(0, 12)}…`);
  } catch (error) { show(error.message, true); }
});

document.querySelector("#finalize-button").addEventListener("click", async () => {
  try {
    state.session = await api(`/api/sessions/${state.session.session_id}/finalize`, { method: "POST" });
    show(`PC 검토 ${state.session.overall_result} · Android는 ${state.session.platforms.android.status}`);
  } catch (error) { show(error.message, true); }
});

api("/api/config").then(config => {
  state.csrf = config.csrf_token;
  show(`${config.project_id} 연결됨 · 검토자: 개발자 본인 · Android: 연결 보류`);
}).catch(error => show(error.message, true));
