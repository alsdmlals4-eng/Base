const childStates = new Map();
const state = { csrf: "", catalog: null, projectId: null, windowsLauncherState: "UNKNOWN" };
const statusBox = document.querySelector("#status");

const VISUAL_TOOLS = new Set(["expression-studio", "sprite-animation-studio"]);

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

function childStateKey(projectId, toolId) {
  return `${projectId}:${toolId}`;
}

function defaultChildState(tool) {
  if (!state.projectId) return { status: "PROJECT_SELECTION_REQUIRED", detail: "먼저 프로젝트를 선택하세요.", tone: "idle" };
  if (tool.launch_state !== "RUNNABLE") return { status: "BLOCKED_PLATFORM", detail: "프로젝트는 선택됐지만 이 운영체제의 도구 실행은 아직 검증되지 않았습니다.", tone: "blocked" };
  const detail = VISUAL_TOOLS.has(tool.tool_id)
    ? "subscription_handoff_import · provider 호출 없음 · routing/anchor gate는 시작 전에 서버가 검증"
    : "프로젝트별 QA evidence child가 아직 시작되지 않았습니다.";
  return { status: "REGISTERED", detail, tone: "ready" };
}

function childStateFor(tool) {
  const key = childStateKey(state.projectId, tool.tool_id);
  if (!childStates.has(key)) childStates.set(key, defaultChildState(tool));
  return childStates.get(key);
}

function setChildState(projectId, toolId, nextState) {
  childStates.set(childStateKey(projectId, toolId), nextState);
  render();
}

function blockedChildState(message) {
  if (message === "PROJECT_ANCHOR_EVIDENCE_UNAVAILABLE") {
    return { status: "ANCHOR_EVIDENCE_MISSING", detail: "프로젝트 소유 anchor 증거를 확인한 뒤 다시 시작하세요.", tone: "blocked" };
  }
  if (message === "PROJECT_FIGMA_ROUTING_UNAVAILABLE") {
    return { status: "BLOCKED_UNVERIFIED", detail: "ROUTING_REGISTERED 상태를 서버에서 확인할 수 없습니다.", tone: "blocked" };
  }
  return { status: "START_FAILED", detail: message, tone: "blocked" };
}

function requireAuthenticatedChildUrl(childUrl) {
  if (childUrl.protocol !== "http:" || childUrl.hostname !== "127.0.0.1" || !childUrl.port || childUrl.username || childUrl.password) {
    throw new Error("AUTHENTICATED_LOOPBACK_URL_REQUIRED");
  }
}

function renderKnownProjects() {
  const knownProjects = document.querySelector("#known-project");
  const selected = knownProjects.value;
  knownProjects.replaceChildren();
  const prompt = document.createElement("option");
  prompt.value = "";
  prompt.textContent = "연결할 프로젝트를 선택하세요";
  knownProjects.append(prompt);
  for (const project of state.catalog.known_projects) {
    const option = document.createElement("option");
    option.value = project.project_id;
    option.textContent = `${project.display_name} · ${project.project_id}`;
    knownProjects.append(option);
  }
  if ([...knownProjects.options].some(option => option.value === selected)) knownProjects.value = selected;
  const list = document.querySelector("#known-project-list"); list.replaceChildren();
  for (const project of state.catalog.known_projects) {
    const card = document.createElement("article"); card.className = "project-card";
    const title = document.createElement("strong"); title.textContent = project.display_name;
    const meta = document.createElement("span"); meta.textContent = `${project.repository_name} · ${project.local_state}`;
    const button = document.createElement("button"); button.textContent = project.action_label;
    button.disabled = project.local_state === "ONBOARDING";
    button.addEventListener("click", () => onboardProject(project));
    card.append(title, meta, button); list.append(card);
  }
}

async function onboardProject(project) {
  project.local_state = "ONBOARDING";
  project.action_label = "설치 중";
  render();
  show(`${project.display_name} 연결 상태를 확인하는 중입니다.`);
  try {
    const connected = await api(`/api/projects/${project.project_id}/onboard`, { method: "POST", body: JSON.stringify({}) });
    state.projectId = connected.project_id;
    await refresh();
    show(`${project.display_name} 연결됨`);
  } catch (error) {
    await refresh();
    show(`${project.display_name}: ${error.message}`, true);
  }
}

function renderRegisteredProjects() {
  const projects = document.querySelector("#registered-project-list"); projects.replaceChildren();
  for (const project of state.catalog.projects) {
    const button = document.createElement("button");
    button.textContent = `${project.display_name} · ${project.state}`;
    button.addEventListener("click", () => { state.projectId = project.project_id; render(); });
    if (state.projectId === project.project_id) button.classList.add("selected");
    projects.append(button);
  }
  if (!state.catalog.projects.length) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "아직 연결된 프로젝트가 없습니다.";
    projects.append(empty);
  }
}

function render() {
  renderKnownProjects();
  renderRegisteredProjects();
  const tools = document.querySelector("#tool-catalog"); tools.replaceChildren();
  for (const tool of state.catalog.tools) {
    const card = document.createElement("article"); card.className = "tool-card";
    const title = document.createElement("h3"); title.textContent = tool.display_name;
    const description = document.createElement("p"); description.textContent = tool.capabilities.join(" · ");
    const childState = childStateFor(tool);
    const status = document.createElement("strong"); status.className = `tool-status ${childState.tone}`; status.textContent = childState.status;
    const detail = document.createElement("p"); detail.className = "tool-detail"; detail.textContent = childState.detail;
    const button = document.createElement("button"); button.textContent = childState.status === "RUNNING" ? "다시 열기" : "시작 및 열기";
    button.disabled = tool.launch_state !== "RUNNABLE" || !state.projectId || childState.status === "STARTING";
    button.addEventListener("click", async () => {
      if (!state.projectId) return show("먼저 프로젝트를 선택하세요.", true);
      const launchProjectId = state.projectId;
      setChildState(launchProjectId, tool.tool_id, { status: "STARTING", detail: "서버가 프로젝트 identity와 child health를 검증하는 중입니다.", tone: "busy" });
      try {
        const child = await api("/api/launch", { method: "POST", body: JSON.stringify({ tool_id: tool.tool_id, project_id: launchProjectId }) });
        if (child.project_id !== launchProjectId || child.tool_id !== tool.tool_id) throw new Error("AUTHENTICATED_CHILD_IDENTITY_REQUIRED");
        const childUrl = new URL(child.url);
        requireAuthenticatedChildUrl(childUrl);
        setChildState(launchProjectId, tool.tool_id, {
          status: child.status,
          detail: VISUAL_TOOLS.has(tool.tool_id) ? "ROUTING_REGISTERED · subscription_handoff_import · provider 호출 없음" : "authenticated project-bound QA child",
          tone: "running",
        });
        window.open(childUrl.href, "_blank", "noopener");
        show(`${tool.display_name} · ${launchProjectId} 실행됨`);
      } catch (error) {
        setChildState(launchProjectId, tool.tool_id, blockedChildState(error.message));
        show(`${tool.display_name} 시작 차단: ${error.message}`, true);
      }
    });
    card.append(title, description, status, detail, button); tools.append(card);
  }
}

async function refresh() { state.catalog = await api("/api/catalog"); if (!state.projectId && state.catalog.projects[0]) state.projectId = state.catalog.projects[0].project_id; render(); }

document.querySelector("#project-registration").addEventListener("submit", async event => {
  event.preventDefault();
  const projectId = document.querySelector("#known-project").value;
  const project = state.catalog.known_projects.find(item => item.project_id === projectId);
  if (!project) return show("연결할 프로젝트를 선택하세요.", true);
  await onboardProject(project);
});

document.querySelector("#windows-launcher-install").addEventListener("click", async () => {
  try {
    const result = await api("/api/windows-launcher/install", { method: "POST", body: JSON.stringify({}) });
    state.windowsLauncherState = result.state;
    document.querySelector("#windows-launcher-state").textContent = result.state;
    show("바탕화면 실행 아이콘이 설치되었습니다. 다음부터 터미널을 열지 않아도 됩니다.");
  } catch (error) { show(`실행 아이콘 설치 차단: ${error.message}`, true); }
});

document.querySelector("#hub-shutdown").addEventListener("click", async () => {
  if (!window.confirm("Tool Hub와 Tool Hub가 시작한 도구를 종료할까요?")) return;
  try {
    await api("/api/shutdown", { method: "POST", body: JSON.stringify({}) });
    show("Tool Hub를 종료하고 있습니다. 이 창은 닫아도 됩니다.");
  } catch (error) { show(`종료 요청 실패: ${error.message}`, true); }
});

api("/api/config").then(async config => {
  state.csrf = config.csrf_token;
  state.windowsLauncherState = config.windows_launcher_state;
  document.querySelector("#windows-launcher-state").textContent = config.windows_launcher_state;
  document.querySelector("#windows-launcher-install").disabled = config.windows_launcher_state === "BLOCKED_PLATFORM";
  await refresh();
  show("검토된 도구와 프로젝트 상태를 불러왔습니다.");
}).catch(error => show(error.message, true));