let currentUser = {};

async function initUserDashboard() {
  const ok = await Dashboard.init({ role: 'user', active: 'dashboard', title: 'Dashboard', subtitle: 'Your activity at a glance' });
  if (!ok) return;
  currentUser = Dashboard.currentUser();

  const firstName = (currentUser.name || 'there').split(' ')[0];
  const subEl = document.querySelector('[data-dash-subtitle]');
  if (subEl) subEl.textContent = `Welcome back, ${firstName}! Here's what's happening.`;

  loadStats();
  loadRecommended();
  loadRecentBookings();
  loadRecentOrders();
}

async function loadStats() {
  const grid = document.getElementById('statGrid');
  try {
    const [props, products, bookings, orders, wishlist] = await Promise.all([
      UserAPI.getMyProperties(0, 100).catch(() => ({ totalElements: 0 })),
      UserAPI.getMyProducts(0, 100).catch(() => ({ totalElements: 0 })),
      BookingAPI.getMy().catch(() => ({ content: [] })),
      OrderAPI.getMy().catch(() => ({ content: [] })),
      WishlistAPI.getAll().catch(() => [])
    ]);

    const bookingList = (bookings && bookings.content) || [];
    const orderList = (orders && orders.content) || [];
    const activeBookings = bookingList.filter((b) => b.status === 'PENDING' || b.status === 'CONFIRMED').length;
    const activeOrders = orderList.filter((o) => o.status === 'PENDING' || o.status === 'CONFIRMED').length;
    const listingCount = (props.totalElements || 0) + (products.totalElements || 0);

    grid.innerHTML = [
      statTile('🏠', 'sc-green', listingCount, 'My Listings'),
      statTile('📅', '', activeBookings, 'Active Bookings'),
      statTile('📦', 'sc-amber', activeOrders, 'Active Orders'),
      statTile('❤️', 'sc-rose', (wishlist || []).length, 'Wishlist Items')
    ].join('');
  } catch (error) {
    grid.innerHTML = `<p class="field-error">${escapeHtml(error.message)}</p>`;
  }
}

function statTile(icon, variant, value, label) {
  return `<div class="stat-card ${variant}">
    <div class="sc-icon">${icon}</div>
    <div class="sc-value">${value}</div>
    <div class="sc-label">${escapeHtml(label)}</div>
  </div>`;
}

async function loadRecommended() {
  const section = document.getElementById('recommendedSection');
  const grid = document.getElementById('recommendedGrid');
  try {
    const properties = await RecommendationAPI.getRecommendedProperties(currentUser.city, 4);
    if (Array.isArray(properties) && properties.length) {
      grid.innerHTML = properties.map(buildPropertyCard).join('');
      section.style.display = '';
    }
  } catch (error) {
    section.style.display = 'none';
  }
}

async function loadRecentBookings() {
  const box = document.getElementById('recentBookings');
  try {
    const res = await BookingAPI.getMy();
    const list = (res && res.content) || [];
    if (!list.length) {
      renderInlineEmpty(box, '📅', 'No bookings yet', '<a href="../../search-properties.html" class="btn btn-primary btn-sm">Find a PG</a>');
      return;
    }
    box.innerHTML = list.slice(0, 4).map((b) => {
      const title = b.property ? b.property.title : 'Property';
      const area = b.property && b.property.area ? b.property.area : '';
      return `<div class="list-row">
        <div class="list-thumb">🏠</div>
        <div class="list-main">
          <div class="lr-title">${escapeHtml(title)}</div>
          <div class="lr-sub">${formatDate(b.checkIn)} → ${formatDate(b.checkOut)}${area ? ' · ' + escapeHtml(area) : ''}</div>
        </div>
        ${dashboardStatusBadge(b.status)}
      </div>`;
    }).join('');
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

async function loadRecentOrders() {
  const box = document.getElementById('recentOrders');
  try {
    const res = await OrderAPI.getMy();
    const list = (res && res.content) || [];
    if (!list.length) {
      renderInlineEmpty(box, '📦', 'No orders yet', '<a href="../../search-products.html" class="btn btn-primary btn-sm">Shop now</a>');
      return;
    }
    box.innerHTML = list.slice(0, 4).map((o) => {
      const title = o.product ? o.product.title : 'Item';
      const image = o.product && getFirstImage(o.product.images);
      return `<div class="list-row">
        <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '📦'}</div>
        <div class="list-main">
          <div class="lr-title">${escapeHtml(title)}</div>
          <div class="lr-sub">Qty ${o.quantity || 1} · ${formatPrice(o.amount, o.orderType === 'RENT' ? 'RENT' : 'SELL')}</div>
        </div>
        ${dashboardStatusBadge(o.status)}
      </div>`;
    }).join('');
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

document.addEventListener('DOMContentLoaded', initUserDashboard);
