<!-- ✅ Place this near the end of your body -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
async function fetchData(endpoint) {
  try {
    const res = await fetch('?fetch=' + endpoint);
    const rows = await res.json();
    return Array.isArray(rows) ? rows : [];
  } catch (err) {
    console.error('Error fetching ' + endpoint + ':', err);
    return [];
  }
}

function buildChart(canvasId, label, color, labels, data) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  if (window[canvasId]) window[canvasId].destroy(); // Destroy old chart if exists

  window[canvasId] = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: label,
        data: data,
        borderColor: color,
        backgroundColor: color.replace('1)', '0.2)'),
        tension: 0.3,
        fill: true,
        pointRadius: 2
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: { display: true, text: 'Timestamp' },
          ticks: { maxRotation: 0, autoSkip: true, maxTicksLimit: 10 }
        },
        y: {
          beginAtZero: true,
          title: { display: true, text: label }
        }
      },
      plugins: {
        legend: { display: true, position: 'top' }
      }
    }
  });
}

async function updateCharts() {
  // ✅ Air Quality
  const airData = await fetchData('air_recent');
  if (airData.length) {
    const airLabels = airData.map(r => r.recorded_at);
    const airValues = airData.map(r => Number(r.value));
    buildChart('aqChart', 'Air Quality Value', 'rgba(54, 162, 235, 1)', airLabels, airValues);
  }

  // ✅ Flame
  const flameData = await fetchData('flame_recent');
  if (flameData.length) {
    const flameLabels = flameData.map(r => r.recorded_at);
    const flameValues = flameData.map(r => Number(r.value));
    buildChart('flameChart', 'Flame Detection (1=Fire)', 'rgba(255, 99, 132, 1)', flameLabels, flameValues);
  }
}

// Initial load
updateCharts();

// ✅ Auto-refresh every 10 seconds
setInterval(updateCharts, 10000);
</script>
