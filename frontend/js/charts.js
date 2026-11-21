/**
 * StayMart Public Creative Visual Charts
 * Milestone 2 - Feature 12
 * Dual-Engine: Chart.js 4.4.1 with Native SVG Fallback Engine
 */

(function () {
  'use strict';

  let rentChartInstance = null;
  let recommerceChartInstance = null;
  let rentFilter = 'all';
  let recommerceMode = 'price'; // 'price' | 'volume'

  // Campus Zone Rent Data across Uttarakhand Hubs
  const campusRentData = {
    zones: ['Clement Town (GEU)', 'Prem Nagar (UPES)', 'Subhash Nagar (ISBT)', 'Rajpur Road (DIT)'],
    pgWithFood: [6800, 8200, 5800, 8800],
    singleRoom: [8500, 10500, 6500, 11000],
    sharedFlat: [4500, 5500, 3800, 6000]
  };

  // Re-Commerce Category Data
  const recommerceData = {
    categories: ['Textbooks', 'Laptops & Tech', 'Furniture', 'Coolers & AC', 'Cycles & Bikes'],
    seniorPrice: [650, 24500, 2400, 2200, 4800],
    retailPrice: [1800, 48000, 6500, 5800, 12000],
    discountPct: [64, 49, 63, 62, 60],
    semesterVolume: [420, 280, 310, 190, 160]
  };

  /* ==========================================================================
     Chart Initializer
     ========================================================================== */
  function initPublicCharts() {
    const rentContainer = document.getElementById('accChartContainer');
    const gearContainer = document.getElementById('gearChartContainer');
    if (!rentContainer && !gearContainer) return;

    if (typeof Chart !== 'undefined') {
      try {
        renderChartJsRent();
        renderChartJsRecommerce();
        return;
      } catch (e) {
        console.warn('Chart.js render failed, falling back to SVG vector renderer:', e);
      }
    }

    // Offline or CDN blocked or Chart.js error -> Render zero-dependency responsive SVG charts
    renderSvgRentChart();
    renderSvgRecommerceChart();
  }

  /* ==========================================================================
     Engine A: Chart.js 4.4.1 Implementation
     ========================================================================== */
  function renderChartJsRent() {
    const canvas = document.getElementById('campusRentChart');
    if (!canvas) return;

    if (rentChartInstance) {
      rentChartInstance.destroy();
      rentChartInstance = null;
    }

    const datasets = [];

    if (rentFilter === 'all' || rentFilter === 'pg') {
      datasets.push({
        label: 'PG with 3 Meals (₹/mo)',
        data: campusRentData.pgWithFood,
        backgroundColor: '#ff9900',
        borderRadius: 6,
        barPercentage: 0.8
      });
    }

    if (rentFilter === 'all') {
      datasets.push({
        label: 'Single Private Room (₹/mo)',
        data: campusRentData.singleRoom,
        backgroundColor: '#002f34',
        borderRadius: 6,
        barPercentage: 0.8
      });
    }

    if (rentFilter === 'all' || rentFilter === 'flat') {
      datasets.push({
        label: 'Shared Flat Bedspace (₹/mo)',
        data: campusRentData.sharedFlat,
        backgroundColor: '#0a883a',
        borderRadius: 6,
        barPercentage: 0.8
      });
    }

    rentChartInstance = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: campusRentData.zones,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              boxWidth: 12,
              font: { family: 'Inter', size: 12, weight: 600 },
              color: '#465666'
            }
          },
          tooltip: {
            backgroundColor: '#002f34',
            titleFont: { family: 'Inter', size: 13, weight: 700 },
            bodyFont: { family: 'Inter', size: 12 },
            padding: 10,
            cornerRadius: 8,
            callbacks: {
              label: function (ctx) {
                return `${ctx.dataset.label}: ₹${ctx.raw.toLocaleString('en-IN')}`;
              }
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
            ticks: {
              font: { family: 'Inter', size: 11, weight: 600 },
              color: '#465666'
            }
          },
          y: {
            beginAtZero: true,
            grid: { color: 'rgba(0, 47, 52, 0.06)' },
            ticks: {
              font: { family: 'Inter', size: 11 },
              color: '#7f9799',
              callback: function (val) {
                return `₹${val / 1000}k`;
              }
            }
          }
        }
      }
    });
  }

  function renderChartJsRecommerce() {
    const canvas = document.getElementById('recommerceChart');
    if (!canvas) return;

    if (recommerceChartInstance) {
      recommerceChartInstance.destroy();
      recommerceChartInstance = null;
    }

    if (recommerceMode === 'price') {
      recommerceChartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: recommerceData.categories,
          datasets: [
            {
              label: 'StayMart Senior Price (₹)',
              data: recommerceData.seniorPrice,
              backgroundColor: '#002f34',
              borderRadius: 6
            },
            {
              label: 'Retail / Amazon New (₹)',
              data: recommerceData.retailPrice,
              backgroundColor: '#cbd5e1',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                boxWidth: 12,
                font: { family: 'Inter', size: 12, weight: 600 },
                color: '#465666'
              }
            },
            tooltip: {
              backgroundColor: '#002f34',
              padding: 10,
              cornerRadius: 8,
              callbacks: {
                label: function (ctx) {
                  return `${ctx.dataset.label}: ₹${ctx.raw.toLocaleString('en-IN')}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { display: false },
              ticks: { font: { family: 'Inter', size: 11, weight: 600 }, color: '#465666' }
            },
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 47, 52, 0.06)' },
              ticks: {
                font: { family: 'Inter', size: 11 },
                color: '#7f9799',
                callback: function (val) {
                  return val >= 1000 ? `₹${val / 1000}k` : `₹${val}`;
                }
              }
            }
          }
        }
      });
    } else {
      // Semester trade volume view
      recommerceChartInstance = new Chart(canvas, {
        type: 'bar',
        data: {
          labels: recommerceData.categories,
          datasets: [
            {
              label: 'Semester Trade Volume (Student Ads)',
              data: recommerceData.semesterVolume,
              backgroundColor: '#ff9900',
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#002f34',
              callbacks: {
                label: function (ctx) {
                  return `Trade Volume: ${ctx.raw} student ads/term`;
                }
              }
            }
          },
          scales: {
            x: { grid: { display: false }, ticks: { font: { family: 'Inter', size: 11, weight: 600 }, color: '#465666' } },
            y: {
              beginAtZero: true,
              grid: { color: 'rgba(0, 47, 52, 0.06)' },
              ticks: { font: { family: 'Inter', size: 11 }, color: '#7f9799' }
            }
          }
        }
      });
    }
  }

  /* ==========================================================================
     Engine B: Zero-Dependency Responsive SVG Fallback
     ========================================================================== */
  function renderSvgRentChart() {
    const container = document.getElementById('accChartContainer');
    if (!container) return;

    const maxVal = 12000;
    const w = 560;
    const h = 260;
    const padL = 45;
    const padR = 20;
    const padT = 30;
    const padB = 45;
    const chartW = w - padL - padR;
    const chartH = h - padT - padB;
    const groupW = chartW / 4;

    let svgHtml = `
      <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%">
        <!-- Grid lines -->
        <line x1="${padL}" y1="${padT}" x2="${w - padR}" y2="${padT}" stroke="#e2e8f0" stroke-dasharray="3"/>
        <text x="${padL - 8}" y="${padT + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹12k</text>
        <line x1="${padL}" y1="${padT + chartH / 2}" x2="${w - padR}" y2="${padT + chartH / 2}" stroke="#e2e8f0" stroke-dasharray="3"/>
        <text x="${padL - 8}" y="${padT + chartH / 2 + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹6k</text>
        <line x1="${padL}" y1="${h - padB}" x2="${w - padR}" y2="${h - padB}" stroke="#cbd5e1"/>
        <text x="${padL - 8}" y="${h - padB + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹0</text>
    `;

    campusRentData.zones.forEach((zone, i) => {
      const gx = padL + i * groupW;
      const barW = 16;

      const hPg = (campusRentData.pgWithFood[i] / maxVal) * chartH;
      const hSingle = (campusRentData.singleRoom[i] / maxVal) * chartH;
      const hFlat = (campusRentData.sharedFlat[i] / maxVal) * chartH;

      if (rentFilter === 'all' || rentFilter === 'pg') {
        svgHtml += `<rect x="${gx + 6}" y="${h - padB - hPg}" width="${barW}" height="${hPg}" rx="3" fill="#ff9900"><title>PG with Food: ₹${campusRentData.pgWithFood[i]}</title></rect>`;
      }
      if (rentFilter === 'all') {
        svgHtml += `<rect x="${gx + 26}" y="${h - padB - hSingle}" width="${barW}" height="${hSingle}" rx="3" fill="#002f34"><title>Single Room: ₹${campusRentData.singleRoom[i]}</title></rect>`;
      }
      if (rentFilter === 'all' || rentFilter === 'flat') {
        svgHtml += `<rect x="${gx + 46}" y="${h - padB - hFlat}" width="${barW}" height="${hFlat}" rx="3" fill="#0a883a"><title>Shared Flat: ₹${campusRentData.sharedFlat[i]}</title></rect>`;
      }

      // X-Axis Zone label
      const shortName = zone.split(' ')[0];
      svgHtml += `<text x="${gx + 34}" y="${h - padB + 16}" font-size="10" font-weight="600" fill="#465666" text-anchor="middle">${shortName}</text>`;
    });

    svgHtml += `
      <!-- Legend -->
      <g transform="translate(${padL}, 12)">
        <rect width="10" height="10" rx="2" fill="#ff9900"/>
        <text x="14" y="9" font-size="10" fill="#465666">PG + Food</text>
        <rect x="90" width="10" height="10" rx="2" fill="#002f34"/>
        <text x="104" y="9" font-size="10" fill="#465666">Single Room</text>
        <rect x="190" width="10" height="10" rx="2" fill="#0a883a"/>
        <text x="204" y="9" font-size="10" fill="#465666">Shared Flat</text>
      </g>
    </svg>`;

    container.innerHTML = svgHtml;
  }

  function renderSvgRecommerceChart() {
    const container = document.getElementById('gearChartContainer');
    if (!container) return;

    const w = 560;
    const h = 260;
    const padL = 45;
    const padR = 20;
    const padT = 30;
    const padB = 45;
    const chartW = w - padL - padR;
    const chartH = h - padT - padB;
    const groupW = chartW / 5;

    if (recommerceMode === 'price') {
      const maxVal = 50000;
      let svgHtml = `
        <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%">
          <line x1="${padL}" y1="${padT}" x2="${w - padR}" y2="${padT}" stroke="#e2e8f0" stroke-dasharray="3"/>
          <text x="${padL - 8}" y="${padT + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹50k</text>
          <line x1="${padL}" y1="${padT + chartH / 2}" x2="${w - padR}" y2="${padT + chartH / 2}" stroke="#e2e8f0" stroke-dasharray="3"/>
          <text x="${padL - 8}" y="${padT + chartH / 2 + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹25k</text>
          <line x1="${padL}" y1="${h - padB}" x2="${w - padR}" y2="${h - padB}" stroke="#cbd5e1"/>
          <text x="${padL - 8}" y="${h - padB + 4}" font-size="10" fill="#7f9799" text-anchor="end">₹0</text>
      `;

      recommerceData.categories.forEach((cat, i) => {
        const gx = padL + i * groupW;
        const barW = 16;
        const hSenior = (recommerceData.seniorPrice[i] / maxVal) * chartH;
        const hRetail = (recommerceData.retailPrice[i] / maxVal) * chartH;

        svgHtml += `<rect x="${gx + 8}" y="${h - padB - hSenior}" width="${barW}" height="${hSenior}" rx="3" fill="#002f34"><title>Senior: ₹${recommerceData.seniorPrice[i]}</title></rect>`;
        svgHtml += `<rect x="${gx + 28}" y="${h - padB - hRetail}" width="${barW}" height="${hRetail}" rx="3" fill="#cbd5e1"><title>Retail: ₹${recommerceData.retailPrice[i]}</title></rect>`;

        const shortCat = cat.split(' ')[0];
        svgHtml += `<text x="${gx + 26}" y="${h - padB + 16}" font-size="10" font-weight="600" fill="#465666" text-anchor="middle">${shortCat}</text>`;
      });

      svgHtml += `
        <g transform="translate(${padL}, 12)">
          <rect width="10" height="10" rx="2" fill="#002f34"/>
          <text x="14" y="9" font-size="10" fill="#465666">StayMart Senior Price</text>
          <rect x="150" width="10" height="10" rx="2" fill="#cbd5e1"/>
          <text x="164" y="9" font-size="10" fill="#465666">Retail Benchmark</text>
        </g>
      </svg>`;

      container.innerHTML = svgHtml;
    } else {
      // Volume view in SVG
      const maxVal = 500;
      let svgHtml = `
        <svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%">
          <line x1="${padL}" y1="${padT}" x2="${w - padR}" y2="${padT}" stroke="#e2e8f0" stroke-dasharray="3"/>
          <text x="${padL - 8}" y="${padT + 4}" font-size="10" fill="#7f9799" text-anchor="end">500</text>
          <line x1="${padL}" y1="${padT + chartH / 2}" x2="${w - padR}" y2="${padT + chartH / 2}" stroke="#e2e8f0" stroke-dasharray="3"/>
          <text x="${padL - 8}" y="${padT + chartH / 2 + 4}" font-size="10" fill="#7f9799" text-anchor="end">250</text>
          <line x1="${padL}" y1="${h - padB}" x2="${w - padR}" y2="${h - padB}" stroke="#cbd5e1"/>
          <text x="${padL - 8}" y="${h - padB + 4}" font-size="10" fill="#7f9799" text-anchor="end">0</text>
      `;

      recommerceData.categories.forEach((cat, i) => {
        const gx = padL + i * groupW;
        const barW = 28;
        const hVol = (recommerceData.semesterVolume[i] / maxVal) * chartH;

        svgHtml += `<rect x="${gx + 12}" y="${h - padB - hVol}" width="${barW}" height="${hVol}" rx="3" fill="#ff9900"><title>Volume: ${recommerceData.semesterVolume[i]} ads</title></rect>`;

        const shortCat = cat.split(' ')[0];
        svgHtml += `<text x="${gx + 26}" y="${h - padB + 16}" font-size="10" font-weight="600" fill="#465666" text-anchor="middle">${shortCat}</text>`;
      });

      svgHtml += `
        <g transform="translate(${padL}, 12)">
          <rect width="10" height="10" rx="2" fill="#ff9900"/>
          <text x="14" y="9" font-size="10" fill="#465666">Semester Trade Volume (Ads)</text>
        </g>
      </svg>`;

      container.innerHTML = svgHtml;
    }
  }

  /* ==========================================================================
     Interactive Filters & Public Controls
     ========================================================================== */
  function filterRentChart(type) {
    rentFilter = type;
    document.querySelectorAll('#accChartFilter .chart-pill').forEach(btn => {
      const onclickAttr = btn.getAttribute('onclick') || '';
      btn.classList.toggle('active', onclickAttr.includes(`'${type}'`));
    });

    if (typeof Chart !== 'undefined' && rentChartInstance) {
      renderChartJsRent();
    } else {
      renderSvgRentChart();
    }
  }

  function toggleRecommerceView(mode) {
    recommerceMode = mode;
    document.querySelectorAll('#gearChartFilter .chart-pill').forEach(btn => {
      const onclickAttr = btn.getAttribute('onclick') || '';
      btn.classList.toggle('active', onclickAttr.includes(`'${mode}'`));
    });

    if (typeof Chart !== 'undefined' && recommerceChartInstance) {
      renderChartJsRecommerce();
    } else {
      renderSvgRecommerceChart();
    }
  }

  // Export functions globally
  window.filterRentChart = filterRentChart;
  window.toggleRecommerceView = toggleRecommerceView;
  window.initPublicCharts = initPublicCharts;

  document.addEventListener('DOMContentLoaded', initPublicCharts);
})();
