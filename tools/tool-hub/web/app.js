const state = { csrf: "", catalog: null, projectId: null };
const statusBox = document.querySelector("#status");

function show(message, error = false) {
  statusBox.textContent = message;
  statusBox.classList.toggle("error", error);
}

async function api(path, options = {}) {
  const headers = new Headers(options.headers || {});
  if (options.body) headers.set("Content-Type", "application/json");
  if ((options.method || "GET") !== "GET") headers.set("X-Hub-CSRF", state.csrf);
  const response = await fetch(path, { ...options, headers });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || `HTTP ${response.status}`);
  return payload;
}

function render() {
  const projects = document.querySelector("#project-list"); projects.replaceChildren();
  for (const project of state.catalog.projects) {
    const button = document.createElement("button");
    button.textContent = `${project.display_name} · ${project.state}`;
    button.addEventListener("click", () => { state.projectId = project.project_id; render(); });
    if (state.projectId === project.project_id) button.classList.add("selected");
    projects.append(button);
  }
  const tools = document.querySelector("#tool-catalog"); tools.replaceChildren();
  for (const tool of state.catalog.tools) {
    const card = document.createElement("article"); card.className = "tool-card";
    const title = document.createElement("h3"); title.textContent = tool.display_name;
    const description = document.createElement("p"); description.textContent = tool.capabilities.join(" · ");
    const button = document.createElement("button"); button.textContent = tool.launch_state === "RUNNABLE" ? "열기" : "등록됨 · Hub 실행은 후속 단계";
    button.disabled = tool.launch_state !== "RUNNABLE";
    button.addEventListener("click", async () => {
      if (!state.projectId) return show("먼저 프로젝트를 선택하세요.", true);
      try {
        const child = await api("/api/launch", { method: "POST", body: JSON.stringify({ tool_id: tool.tool_id, project_id: state.projectId }) });
        window.open(child.url, "_blank", "noopener");
        show(`${tool.display_name} · ${state.projectId} 실행됨`);
      } catch (error) { show(error.message, true); }
    });
    card.append(title, description, button); tools.append(card);
  }
}

async function refresh() { state.catalog = await api("/api/catalog"); if (!state.projectId && state.catalog.projects[0]) state.projectId = state.catalog.projects[0].project_id; render(); }

document.querySelector("#project-registration").addEventListener("submit", async event => {
  event.preventDefault();
  try {
    const project = await api("/api/projects", { method: "POST", body: JSON.stringify({ project_root: document.querySelector("#project-root").value }) });
    state.projectId = project.project_id; await refresh(); show(`${project.project_id} 연결됨`);
  } catch (error) { show(error.message, true); }
});

api("/api/config").then(async config => { state.csrf = config.csrf_token; await refresh(); show("검토된 도구와 프로젝트 상태를 불러왔습니다."); }).catch(error => show(error.message, true));
