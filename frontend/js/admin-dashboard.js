const CHART_COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#a855f7', '#3b82f6', '#14b8a6'];
let analytics = null;

async function initAdminDashboard() {
  const ok = await Dashboard.init({ role: 'admin', active: 'dashboard', title: 'Admin Dashboard', subtitle: 'Platform overview and analytics' });
  if (!ok) return;
  try {
    const [stats, data] = await Promise.all([
      AdminAPI.getStats(),
      AdminAPI.getAnalytics()
    ]);
    analytics = data || {};
    renderStatTiles(stats, data);
    renderCharts(data);
    document.getElementById('ppCount').textContent = stats.pendingProperties ? `(${stats.pendingProperties})` : '';
    document.getElementById('pprodCount').textContent = stats.pendingProducts ? `(${stats.pendingProducts})` : '';
  } catch (error) {
    document.getElementById('statGrid').innerHTML = `<p class="field-error">${escapeHtml(error.message)}</p>`;
  }
}

function renderStatTiles(stats, data) {
  const grid = document.getElementById('statGrid');
  const totals = data || stats || {};
  const tiles = [
    ['👥', '', totals.totalUsers, 'Total Users'],
    ['🏠', 'sc-green', totals.totalProperties, 'Properties'],
    ['🛍️', 'sc-amber', totals.totalProducts, 'Products'],
    ['📅', 'sc-cyan', totals.totalBookings, 'Bookings'],
    ['📦', 'sc-rose', totals.totalOrders, 'Orders'],
    ['⏳', 'sc-amber', stats.pendingProperties, 'Pending Properties'],
    ['⏳', 'sc-rose', stats.pendingProducts, 'Pending Products'],
    ['💬', '', stats.unreadChatCount, 'Unread Messages']
  ];
  grid.innerHTML = tiles.map(([icon, variant, value, label]) => `
    <div class="stat-card ${variant}">
      <div class="sc-icon">${icon}</div>
      <div class="sc-value">${value == null ? 0 : value}</div>
      <div class="sc-label">${escapeHtml(label)}</div>
    </div>`).join('');
}

function renderCharts(data) {
  if (!data || typeof Chart === 'undefined') return;
  const gridColor = 'rgba(148, 163, 184, 0.15)';
  const tickColor = '#94a3b8';

  const baseOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { labels: { color: tickColor } } },
    scales: {
      x: { ticks: { color: tickColor }, grid: { color: gridColor } },
      y: { ticks: { color: tickColor }, grid: { color: gridColor }, beginAtZero: true }
    }
  };

  lineChart('monthlyListingsChart', data.monthlyListings, '#4f46e5', baseOptions);
  lineChart('monthlyUsersChart', data.monthlyRegistrations, '#10b981', baseOptions);
  doughnutChart('propertiesByTypeChart', data.propertiesByType);
  barChart('productsByCategoryChart', data.productsByCategory, '#f59e0b', baseOptions);
  barChart('usersByCityChart', data.usersByCity, '#06b6d4', baseOptions);
}

function lineChart(id, points, color, options) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  const list = points || [];
  new Chart(canvas, {
    type: 'line',
    data: {
      labels: list.map((p) => p.label),
      datasets: [{
        label: 'Count',
        data: list.map((p) => p.value),
        borderColor: color,
        backgroundColor: color + '33',
        fill: true,
        tension: 0.35,
        pointBackgroundColor: color
      }]
    },
    options
  });
}

function doughnutChart(id, points) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  const list = points || [];
  new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: list.map((p) => p.label),
      datasets: [{ data: list.map((p) => p.value), backgroundColor: CHART_COLORS, borderWidth: 0 }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom', labels: { color: '#94a3b8' } } }
    }
  });
}

function barChart(id, points, color, options) {
  const canvas = document.getElementById(id);
  if (!canvas) return;
  const list = points || [];
  new Chart(canvas, {
    type: 'bar',
    data: {
      labels: list.map((p) => p.label),
      datasets: [{ label: 'Count', data: list.map((p) => p.value), backgroundColor: color, borderRadius: 6 }]
    },
    options: {
      ...options,
      plugins: { legend: { display: false } }
    }
  });
}

document.addEventListener('DOMContentLoaded', initAdminDashboard);
