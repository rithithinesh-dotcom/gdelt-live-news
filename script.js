document.addEventListener('DOMContentLoaded', () => {
  initMentionsChart();
  initSentimentDonutChart();
  initSearchAutocomplete();
});

function initMentionsChart() {
  const chartEl = document.getElementById('mentionsLineChart');
  if (!chartEl) return;

  fetch('/api/mentions-over-time?days=7')
    .then(res => res.json())
    .then(data => {
      const trace = {
        x: data.labels, y: data.values,
        type: 'scatter', mode: 'lines+markers',
        line: { color: '#EC4899', width: 3, shape: 'spline' },
        marker: { size: 7, color: '#F472B6', borderColor: '#EC4899', borderWidth: 2 },
        fill: 'tozeroy', fillcolor: 'rgba(236, 72, 153, 0.12)'
      };
      Plotly.newPlot(chartEl, [trace], {
        margin: { t: 10, r: 15, l: 35, b: 35 },
        font: { family: 'Plus Jakarta Sans', size: 10, color: '#94A3B8' },
        xaxis: { showgrid: false },
        yaxis: { gridcolor: 'rgba(255, 255, 255, 0.06)', tickformat: '~s' },
        paper_bgcolor: 'transparent', plot_bgcolor: 'transparent'
      }, { responsive: true, displayModeBar: false });
    });
}

function initSentimentDonutChart() {
  const chartEl = document.getElementById('sentimentDonutChart');
  if (!chartEl) return;

  Plotly.newPlot(chartEl, [{
    values: [65, 25, 10], labels: ['Positive', 'Neutral', 'Negative'],
    type: 'pie', hole: 0.72,
    marker: { colors: ['#10B981', '#F59E0B', '#F43F5E'] },
    textinfo: 'none'
  }], {
    margin: { t: 0, r: 0, l: 0, b: 0 }, showlegend: false,
    paper_bgcolor: 'transparent', plot_bgcolor: 'transparent'
  }, { responsive: true, displayModeBar: false });
}
