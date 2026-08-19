/** Same origin when UI is served from Flask :5000; else call API on :5000 (e.g. python http.server :5500). */
function apiOrigin() {
  const host = window.location.hostname;
  const port = window.location.port;
  if ((host === "localhost" || host === "127.0.0.1") && port === "5000") {
    return "";
  }
  return "http://127.0.0.1:5000";
}

const form = document.getElementById("analyze-form");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const headlinesEl = document.getElementById("headlines");

const tickerEl = document.getElementById("ticker");
const periodEl = document.getElementById("period");
const intervalEl = document.getElementById("interval");

let chart;

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.style.color = isError ? "#b00020" : "#1f5fbf";
}

function renderResults(data) {
  document.getElementById("r-ticker").textContent = data.ticker;
  document.getElementById("r-trend").textContent = Number(data.trend_slope).toFixed(4);
  document.getElementById("r-vol").textContent = `${(Number(data.annualized_volatility) * 100).toFixed(2)}%`;
  document.getElementById("r-dd").textContent = `${(Number(data.max_drawdown) * 100).toFixed(2)}%`;
  document.getElementById("r-sent").textContent = `${Number(data.sentiment_score).toFixed(3)} (${data.sentiment_label})`;

  headlinesEl.innerHTML = "";
  for (const h of data.headlines || []) {
    const li = document.createElement("li");
    li.textContent = h;
    headlinesEl.appendChild(li);
  }

  const ctx = document.getElementById("priceChart");
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.series.dates,
      datasets: [
        {
          label: `${data.ticker} Close`,
          data: data.series.close,
          borderColor: "#1f77b4",
          borderWidth: 2,
          fill: false,
          pointRadius: 0,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: { display: true },
        y: { display: true },
      },
    },
  });

  resultsEl.classList.remove("hidden");
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  setStatus("Analyzing...");

  const ticker = tickerEl.value.trim();
  const period = periodEl.value.trim();
  const interval = intervalEl.value.trim();

  try {
    const url = `${apiOrigin()}/api/analyze?ticker=${encodeURIComponent(ticker)}&period=${encodeURIComponent(period)}&interval=${encodeURIComponent(interval)}`;
    const res = await fetch(url);
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.error || "Request failed");
    }
    renderResults(data);
    setStatus("Done");
  } catch (err) {
    setStatus(err.message, true);
  }
});
