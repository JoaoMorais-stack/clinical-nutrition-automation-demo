const state = { latest: null };

const elements = {
  runButton: document.getElementById("run-button"),
  resetButton: document.getElementById("reset-button"),
  downloadButton: document.getElementById("download-button"),
  careArea: document.getElementById("care-area"),
  caseRows: document.getElementById("case-rows"),
  eventList: document.getElementById("event-list"),
  distributionList: document.getElementById("distribution-list"),
  historyList: document.getElementById("history-list"),
  runLabel: document.getElementById("run-label"),
  metrics: {
    total: document.getElementById("metric-total"),
    alerts: document.getElementById("metric-alerts"),
    followups: document.getElementById("metric-followups"),
    areas: document.getElementById("metric-areas"),
  },
};

function escapeHtml(value) {
  const node = document.createElement("span");
  node.textContent = String(value);
  return node.innerHTML;
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Local request failed");
  return payload;
}

function renderReport(report) {
  state.latest = report;
  elements.downloadButton.disabled = !report;
  const summary = report?.summary || {};
  elements.metrics.total.textContent = summary.total_cases || 0;
  elements.metrics.alerts.textContent = summary.alerts || 0;
  elements.metrics.followups.textContent = summary.follow_ups || 0;
  elements.metrics.areas.textContent = summary.care_areas || 0;

  if (!report) {
    elements.runLabel.textContent = "Ready to demonstrate";
    elements.caseRows.innerHTML = '<tr class="empty-row"><td colspan="5">Run the demonstration to populate this view.</td></tr>';
    elements.eventList.innerHTML = "<li>Waiting for a local run.</li>";
    elements.distributionList.innerHTML = "<p>No results yet.</p>";
    return;
  }

  elements.runLabel.textContent = `${report.mode} · ${report.run_id}`;
  elements.caseRows.innerHTML = report.cases.map((item) => `
    <tr>
      <td><span class="case-name">${escapeHtml(item.display_name)}</span><span class="case-id">${escapeHtml(item.case_id)} · ${escapeHtml(item.room_label)}</span></td>
      <td>${escapeHtml(item.care_area)}</td>
      <td>${escapeHtml(item.nutrition_route)}</td>
      <td><span class="badge risk-${escapeHtml(item.risk_level)}">${escapeHtml(item.risk_level)}</span></td>
      <td>${escapeHtml(item.recommended_action)}</td>
    </tr>
  `).join("") || '<tr class="empty-row"><td colspan="5">No fictional cases matched this scope.</td></tr>';

  elements.eventList.innerHTML = report.events.map((event) => `<li>${escapeHtml(event)}</li>`).join("");
  const maxCount = Math.max(...Object.values(report.distribution), 1);
  elements.distributionList.innerHTML = Object.entries(report.distribution).map(([label, count]) => `
    <div class="distribution-row">
      <div class="distribution-label"><span>${escapeHtml(label)}</span><strong>${count}</strong></div>
      <div class="bar"><span style="width: ${(count / maxCount) * 100}%"></span></div>
    </div>
  `).join("") || "<p>No results in this scope.</p>";
}

function renderHistory(history) {
  elements.historyList.innerHTML = history.map((item) => `
    <div class="history-item">
      <strong>${escapeHtml(item.run_id)}</strong>
      <span>${escapeHtml(item.mode)}</span>
      <span>${item.total_cases} cases · ${item.alerts} alerts</span>
    </div>
  `).join("") || "<p>No saved runs.</p>";
}

async function refresh() {
  const dashboard = await request("/api/dashboard");
  if (elements.careArea.options.length === 1) {
    dashboard.care_areas.forEach((area) => {
      const option = document.createElement("option");
      option.value = area;
      option.textContent = area;
      elements.careArea.appendChild(option);
    });
  }
  renderReport(dashboard.latest);
  renderHistory(dashboard.history);
}

elements.runButton.addEventListener("click", async () => {
  elements.runButton.disabled = true;
  elements.runButton.textContent = "Running...";
  try {
    await request("/api/run", {
      method: "POST",
      body: JSON.stringify({ care_area: elements.careArea.value }),
    });
    await refresh();
  } catch (error) {
    window.alert(error.message);
  } finally {
    elements.runButton.disabled = false;
    elements.runButton.textContent = "Run demonstration";
  }
});

elements.resetButton.addEventListener("click", async () => {
  await request("/api/reset", { method: "POST", body: "{}" });
  await refresh();
});

elements.downloadButton.addEventListener("click", () => {
  if (!state.latest) return;
  const blob = new Blob([JSON.stringify(state.latest, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `fictional-nutrition-report-${state.latest.run_id}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
});

refresh().catch((error) => {
  elements.runLabel.textContent = error.message;
});
