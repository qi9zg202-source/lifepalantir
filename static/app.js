let state = null;

const $ = (selector) => document.querySelector(selector);

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function subsystemName(id) {
  return state?.subsystems?.find((item) => item.id === id)?.name || id;
}

function renderMetrics() {
  $("#systemState").textContent = "Online";
  $("#dbPath").textContent = state.platform.database;
  $("#metricSubsystems").textContent = state.metrics.subsystems;
  $("#metricObjects").textContent = state.metrics.ontology_objects;
  $("#metricDecisions").textContent = state.metrics.decisions;
  $("#metricActions").textContent = state.metrics.open_actions;
}

function renderSubsystems() {
  $("#subsystemRows").innerHTML = state.subsystems
    .map(
      (item) => `
        <a class="subsystem-row" href="${escapeHtml(item.repo_url)}" target="_blank" rel="noreferrer">
          <span class="code">${escapeHtml(item.id)}</span>
          <span>
            <strong>${escapeHtml(item.name)}</strong>
            <small>${escapeHtml(item.domain)}</small>
          </span>
          <span class="mission">${escapeHtml(item.mission)}</span>
          <span class="status">${escapeHtml(item.status)}</span>
        </a>
      `
    )
    .join("");

  $("#decisionSubsystem").innerHTML = state.subsystems
    .map((item) => `<option value="${escapeHtml(item.id)}">${escapeHtml(item.name)}</option>`)
    .join("");
}

function renderOntology() {
  const groups = state.ontology_objects.reduce((acc, item) => {
    acc[item.subsystem_id] = acc[item.subsystem_id] || [];
    acc[item.subsystem_id].push(item);
    return acc;
  }, {});

  $("#ontologyMap").innerHTML = Object.entries(groups)
    .map(
      ([subsystemId, objects]) => `
        <section class="ontology-group">
          <h3>${escapeHtml(subsystemName(subsystemId))}</h3>
          <div>
            ${objects
              .map(
                (object) => `
                  <article class="object-node">
                    <span>${escapeHtml(object.object_type)}</span>
                    <strong>${escapeHtml(object.name)}</strong>
                    <small>${escapeHtml(object.description)}</small>
                  </article>
                `
              )
              .join("")}
          </div>
        </section>
      `
    )
    .join("");
}

function renderIntegrations() {
  $("#integrationRows").innerHTML = state.integrations
    .map(
      (item) => `
        <div class="integration-row">
          <span class="code">${escapeHtml(item.kind)}</span>
          <strong>${escapeHtml(item.name)}</strong>
          <span class="status">${escapeHtml(item.status)}</span>
        </div>
      `
    )
    .join("");
}

function renderDecisions() {
  $("#decisionRows").innerHTML = state.decisions
    .map(
      (item) => `
        <article class="decision-card">
          <div>
            <span class="code">${escapeHtml(item.decision_type)} / ${escapeHtml(item.impact)}</span>
            <h3>${escapeHtml(item.title)}</h3>
            <p>${escapeHtml(item.rationale)}</p>
          </div>
          <footer>
            <span>${escapeHtml(subsystemName(item.subsystem_id))}</span>
            <strong>${escapeHtml(item.status)}</strong>
          </footer>
          ${item.next_action ? `<small>Next: ${escapeHtml(item.next_action)}</small>` : ""}
        </article>
      `
    )
    .join("");
}

function renderActions() {
  $("#actionRows").innerHTML = `
    <div class="table-row table-head">
      <span>Subsystem</span>
      <span>Action</span>
      <span>Owner</span>
      <span>Status</span>
    </div>
    ${state.action_items
      .map(
        (item) => `
          <div class="table-row">
            <span>${escapeHtml(subsystemName(item.subsystem_id))}</span>
            <strong>${escapeHtml(item.title)}</strong>
            <span>${escapeHtml(item.owner)}</span>
            <span class="status">${escapeHtml(item.status)}</span>
          </div>
        `
      )
      .join("")}
  `;
}

function renderAll() {
  renderMetrics();
  renderSubsystems();
  renderOntology();
  renderIntegrations();
  renderDecisions();
  renderActions();
}

async function loadState() {
  state = await api("/api/bootstrap");
  renderAll();
}

function bindForm() {
  $("#decisionForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const payload = Object.fromEntries(new FormData(event.currentTarget).entries());
    payload.status = "review";
    payload.confidence = 0.7;
    state = await api("/api/decisions", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    event.currentTarget.reset();
    renderAll();
    $("#formStatus").textContent = "已写入 SQLite 决策库。";
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  bindForm();
  try {
    await loadState();
  } catch (error) {
    $("#systemState").textContent = "Offline";
    $("#dbPath").textContent = error.message;
  }
});
