const DASH_ROOT = '../../';

const DASH_NAV = {
  user: [
    { key: 'dashboard', icon: '📊', label: 'Dashboard', href: 'dashboard.html' },
    { key: 'my-listings', icon: '🏠', label: 'My Listings', href: 'my-listings.html' },
    { key: 'bookings', icon: '📅', label: 'My Bookings', href: 'bookings.html' },
    { key: 'orders', icon: '📦', label: 'My Orders', href: 'orders.html' },
    { key: 'requests-received', icon: '📨', label: 'Requests Received', href: 'requests-received.html' },
    { key: 'wishlist', icon: '❤️', label: 'Wishlist', href: 'wishlist.html' },
    { key: 'chat', icon: '💬', label: 'Messages', href: 'chat.html', badge: 'unreadChat' },
    { key: 'profile', icon: '👤', label: 'Profile', href: 'profile.html' },
    { divider: true },
    { key: 'browse', icon: '🌐', label: 'Browse Listings', href: DASH_ROOT + 'index.html', external: true }
  ],
  admin: [
    { group: 'Overview' },
    { key: 'dashboard', icon: '📊', label: 'Dashboard', href: 'dashboard.html' },
    { group: 'Moderation' },
    { key: 'pending-properties', icon: '🏠', label: 'Pending Properties', href: 'pending-properties.html' },
    { key: 'pending-products', icon: '📦', label: 'Pending Products', href: 'pending-products.html' },
    { group: 'Manage' },
    { key: 'all-users', icon: '👥', label: 'All Users', href: 'all-users.html' },
    { key: 'all-properties', icon: '🏘️', label: 'All Properties', href: 'all-properties.html' },
    { key: 'all-products', icon: '🛍️', label: 'All Products', href: 'all-products.html' },
    { key: 'categories', icon: '🏷️', label: 'Categories', href: 'categories.html' },
    { key: 'locations', icon: '📍', label: 'Locations', href: 'locations.html' },
    { divider: true },
    { key: 'browse', icon: '🌐', label: 'View Site', href: DASH_ROOT + 'index.html', external: true }
  ]
};

const Dashboard = {
  config: {},
  unreadCount: 0,

  async init(config) {
    this.config = config || {};
    await Auth.init();
    const isAdminArea = this.config.role === 'admin';
    if (isAdminArea ? !Auth.guardAdmin() : !Auth.guardPage()) {
      return false;
    }
    this.renderSidebar();
    this.renderUserCard();
    this.bindSidebar();
    if (this.config.role === 'user') {
      this.loadUnread();
    }
    const titleEl = document.querySelector('[data-dash-title]');
    if (titleEl && this.config.title) titleEl.textContent = this.config.title;
    const subEl = document.querySelector('[data-dash-subtitle]');
    if (subEl && this.config.subtitle) subEl.textContent = this.config.subtitle;
    return true;
  },

  currentUser() {
    return Auth.user || {};
  },

  navItems() {
    return DASH_NAV[this.config.role] || DASH_NAV.user;
  },

  renderSidebar() {
    const nav = document.getElementById('dashNav');
    if (!nav) return;
    const active = this.config.active;
    let html = '';
    this.navItems().forEach((item) => {
      if (item.divider) {
        html += '<div class="nav-divider"></div>';
        return;
      }
      if (item.group) {
        html += `<div class="nav-group-title">${escapeHtml(item.group)}</div>`;
        return;
      }
      const badge = item.badge === 'unreadChat' && this.unreadCount > 0
        ? `<span class="nav-badge">${this.unreadCount}</span>`
        : '';
      html += `<a href="${item.href}" class="${item.key === active ? 'active' : ''}">
        <span class="nav-ico">${item.icon}</span><span>${escapeHtml(item.label)}</span>${badge}
      </a>`;
    });
    nav.innerHTML = html;
  },

  renderUserCard() {
    const box = document.getElementById('dashUser');
    if (!box) return;
    const user = this.currentUser();
    const initial = user.name ? user.name[0].toUpperCase() : 'U';
    const avatar = user.profilePic
      ? `<img src="${escapeHtml(user.profilePic)}" alt=""/>`
      : initial;
    box.innerHTML = `
      <div class="avatar">${avatar}</div>
      <div class="dash-user-info">
        <div class="du-name">${escapeHtml(user.name || 'User')}</div>
        <div class="du-role">${escapeHtml((user.role || 'USER').toLowerCase())}</div>
      </div>
      <button class="du-logout" title="Logout" onclick="handleLogout()">⏻</button>
    `;
  },

  bindSidebar() {
    const burger = document.getElementById('dashHamburger');
    const sidebar = document.getElementById('dashSidebar');
    const overlay = document.getElementById('dashOverlay');
    if (burger && sidebar && overlay) {
      burger.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('open');
      });
      overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('open');
      });
    }
  },

  async loadUnread() {
    try {
      const count = await ChatAPI.getUnreadCount();
      this.unreadCount = typeof count === 'number' ? count : (count && count.count) || 0;
      if (this.unreadCount > 0) this.renderSidebar();
    } catch (error) {
      this.unreadCount = 0;
    }
  }
};

function dashboardStatusBadge(status) {
  const label = (status || 'PENDING').charAt(0) + (status || 'PENDING').slice(1).toLowerCase();
  return `<span class="badge ${getStatusBadgeClass(status)}">${escapeHtml(label)}</span>`;
}

function dashboardInitials(name) {
  if (!name) return '?';
  return name.trim().split(/\s+/).slice(0, 2).map((part) => part[0].toUpperCase()).join('');
}

function dashboardAvatar(user, cls) {
  const klass = cls || 'avatar';
  if (user && user.profilePic) {
    return `<div class="${klass}"><img src="${escapeHtml(user.profilePic)}" alt=""/></div>`;
  }
  return `<div class="${klass}">${escapeHtml(dashboardInitials(user && user.name ? user.name : ''))}</div>`;
}

function renderListSkeleton(container, rows = 4) {
  let html = '<div class="loading-block">';
  for (let i = 0; i < rows; i++) html += '<div class="row-skeleton"></div>';
  html += '</div>';
  container.innerHTML = html;
}

function renderInlineEmpty(container, icon, message, actionHtml) {
  container.innerHTML = `
    <div class="inline-empty">
      <span class="empty-icon">${icon}</span>
      <p>${escapeHtml(message)}</p>
      ${actionHtml || ''}
    </div>
  `;
}

function dashboardPageUrl(page) {
  return `${DASH_ROOT}pages/user/${page}`;
}

window.Dashboard = window.Dashboard || Dashboard;
