const Auth = {
  user: null,
  async init() {
    const token = localStorage.getItem('staymart_token');
    if (token) {
      try {
        this.user = await AuthAPI.getCurrentUser();
      } catch (error) {
        this.logout();
      }
    }
  },
  isLoggedIn() {
    return !!this.user;
  },
  isAdmin() {
    if (!this.user) return false;
    if (this.user.role) return this.user.role === 'ADMIN';
    if (Array.isArray(this.user.roles)) return this.user.roles.includes('ADMIN');
    return false;
  },
  async login(email, password) {
    const result = await AuthAPI.login({ email, password });
    if (result && result.token) {
      localStorage.setItem('staymart_token', result.token);
      localStorage.setItem('staymart_user', JSON.stringify(result.user));
      this.user = result.user;
    }
  },
  async register(userData) {
    const result = await AuthAPI.register(userData);
    if (result && result.token) {
      localStorage.setItem('staymart_token', result.token);
      localStorage.setItem('staymart_user', JSON.stringify(result.user));
      this.user = result.user;
    }
  },
  logout() {
    localStorage.removeItem('staymart_token');
    localStorage.removeItem('staymart_user');
    this.user = null;
  },
  redirectByRole() {
    if (this.isAdmin()) {
      window.location.href = `${depthPrefix()}pages/admin/dashboard.html`;
    } else {
      window.location.href = `${depthPrefix()}index.html`;
    }
  },
  updateNavbar() {
    const navActions = document.querySelector('.navbar .nav-actions');
    if (!navActions) return;
    if (this.isLoggedIn() && this.user) {
      const user = this.user;
      navActions.innerHTML = `
        <a href="post-property.html" class="btn btn-primary btn-sm btn-post">+ Post Property</a>
        <a href="post-product.html" class="btn btn-secondary btn-sm">+ Sell / Rent</a>
        <div class="avatar-menu">
          <div class="avatar" onclick="toggleDropdown(event)">
            ${user.profilePic ? `<img src="${user.profilePic}" alt=""/>` : (user.name ? user.name[0].toUpperCase() : 'U')}
          </div>
          <div class="dropdown" id="profileDropdown">
            <div class="dropdown-header">
              <div class="dropdown-name">${user.name || ''}</div>
              <div class="dropdown-mail">${user.email || ''}</div>
            </div>
            <a href="${depthPrefix()}pages/user/dashboard.html"><span>📊</span> Dashboard</a>
            <a href="${depthPrefix()}pages/user/profile.html"><span>👤</span> My Profile</a>
            <a href="${depthPrefix()}pages/user/my-listings.html"><span>🏠</span> My Listings</a>
            <a href="${depthPrefix()}pages/user/bookings.html"><span>📅</span> My Bookings</a>
            <a href="${depthPrefix()}pages/user/orders.html"><span>📦</span> My Orders</a>
            <a href="${depthPrefix()}pages/user/requests-received.html"><span>📨</span> Requests</a>
            <a href="${depthPrefix()}pages/user/wishlist.html"><span>❤️</span> My Wishlist</a>
            <a href="${depthPrefix()}pages/user/chat.html"><span>💬</span> Messages</a>
            ${this.isAdmin() ? '<div class="dropdown-divider"></div><a href="' + depthPrefix() + 'pages/admin/dashboard.html"><span>🛡️</span> Admin Dashboard</a>' : ''}
            <div class="dropdown-divider"></div>
            <button onclick="handleLogout()"><span>🚪</span> Logout</button>
          </div>
        </div>
      `;
    } else {
      navActions.innerHTML = `
        <a href="login.html" class="btn btn-secondary btn-sm">Login</a>
        <a href="register.html" class="btn btn-primary btn-sm">Get Started</a>
      `;
    }
  },
  guardPage() {
    if (!this.isLoggedIn()) {
      window.location.href = '../../login.html';
      return false;
    }
    return true;
  },
  guardAdmin() {
    if (!this.isLoggedIn()) {
      window.location.href = '../../login.html';
      return false;
    }
    if (!this.isAdmin()) {
      window.location.href = '../../pages/user/dashboard.html';
      return false;
    }
    return true;
  }
};

function toggleDropdown(event) {
  event.stopPropagation();
  const dd = document.getElementById('profileDropdown');
  if (dd) dd.classList.toggle('open');
}

function depthPrefix() {
  const depth = window.location.pathname.split('/').filter(Boolean).length - 1;
  return depth >= 2 ? '../../' : '';
}

function handleLogout() {
  Auth.logout();
  window.location.href = `${depthPrefix()}login.html`;
}

document.addEventListener('click', function (event) {
  const dd = document.getElementById('profileDropdown');
  if (dd && dd.classList.contains('open') && !event.target.closest('.avatar-menu')) {
    dd.classList.remove('open');
  }
});

function initAuth() {
  return Auth.init().then(function () {
    Auth.updateNavbar();
  });
}