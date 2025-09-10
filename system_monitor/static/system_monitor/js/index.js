/* eslint-env browser */

let systemChart;
let refreshInterval;

function fetchData() {
  const path = '/admin/system_monitor/overview/api.json/';
  fetch(path)
    .then(response => response.json())
    .then(data => {
      updateChart(data);
    })
    .catch(console.error);

  setTimeout(fetchData, refreshInterval);
}

function updateChart(data) {
  const labels = data.map(d => d.name);
  const values = data.map(d => d.value);

  if (systemChart) {
    systemChart.data.labels = labels;
    systemChart.data.datasets[0].data = values;
    systemChart.update();
  } else {
    const ctx = document.getElementById('systemMetricsChart').getContext('2d');
    systemChart = new Chart(ctx, {
      type: 'bar', // You can change this to 'line', 'pie', etc.
      data: {
        labels: labels,
        datasets: [{
          label: 'System Usage (%)',
          data: values,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const overviewDiv = document.getElementById('overview');
  refreshInterval = parseInt(overviewDiv.dataset.refreshInterval, 10) || 5000; // Default to 5 seconds

  // Add Chart.js script dynamically if not already present (for development, in production it should be in template)
  if (typeof Chart === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
    script.onload = () => {
      fetchData();
    };
    document.head.appendChild(script);
  } else {
    fetchData();
  }
});
