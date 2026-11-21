function escHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>'"]/g, tag => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  }[tag] || tag));
}

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
    const drawerUserCard = document.getElementById('drawerUserCard');
    const drawerAccountSection = document.getElementById('drawerAccountSection');
    const drawerAccountLinks = document.getElementById('drawerAccountLinks');
    const drawerFooter = document.getElementById('drawerFooter');
    const bottomTabAccount = document.getElementById('bottomTabAccount');
    const bottomTabChat = document.getElementById('bottomTabChat');
    const prefix = depthPrefix();

    if (this.isLoggedIn() && this.user) {
      const user = this.user;

      // 1. Desktop Nav Actions
      if (navActions) {
        navActions.innerHTML = `
          <a href="${prefix}pages/user/chat.html" class="nav-icon-btn" title="Messages">💬</a>
          <a href="${prefix}pages/user/wishlist.html" class="nav-icon-btn" title="Saved Wishlist">❤️</a>
          <div class="avatar-menu">
            <div class="avatar" onclick="toggleDropdown(event)">
              ${user.profilePic ? `<img src="${escHtml(user.profilePic)}" alt=""/>` : escHtml(user.name ? user.name[0].toUpperCase() : 'U')}
            </div>
            <div class="dropdown" id="profileDropdown">
              <div class="dropdown-header">
                <div class="dropdown-name">${escHtml(user.name || 'User')}</div>
                <div class="dropdown-mail">${escHtml(user.email || '')}</div>
              </div>
              <a href="${prefix}pages/user/dashboard.html"><span>📊</span> Dashboard</a>
              <a href="${prefix}pages/user/profile.html"><span>👤</span> My Profile</a>
              <a href="${prefix}pages/user/my-listings.html"><span>🏠</span> My Listings</a>
              <a href="${prefix}pages/user/bookings.html"><span>📅</span> My Bookings</a>
              <a href="${prefix}pages/user/orders.html"><span>📦</span> My Orders</a>
              <a href="${prefix}pages/user/requests-received.html"><span>📨</span> Requests</a>
              <a href="${prefix}pages/user/wishlist.html"><span>❤️</span> Wishlist</a>
              <a href="${prefix}pages/user/chat.html"><span>💬</span> Messages</a>
              ${this.isAdmin() ? '<div class="dropdown-divider"></div><a href="' + prefix + 'pages/admin/dashboard.html"><span>🛡️</span> Admin Dashboard</a>' : ''}
              <div class="dropdown-divider"></div>
              <button onclick="handleLogout()"><span>🚪</span> Logout</button>
            </div>
          </div>
          <a href="${prefix}post-product.html" class="btn-olx-sell">
            <span class="sell-plus">+</span> SELL
          </a>
        `;
      }

      // 2. Mobile Drawer User Card
      if (drawerUserCard) {
        drawerUserCard.innerHTML = `
          <div class="drawer-user-avatar">
            ${user.profilePic ? `<img src="${escHtml(user.profilePic)}" alt=""/>` : escHtml(user.name ? user.name[0].toUpperCase() : 'U')}
          </div>
          <div class="drawer-user-meta">
            <div class="drawer-user-name">${escHtml(user.name || 'Student')}</div>
            <div class="drawer-user-role">🎓 Verified Student · ${escHtml(user.city || 'Dehradun')}</div>
          </div>
        `;
      }

      // 3. Mobile Drawer Account Links
      if (drawerAccountSection && drawerAccountLinks) {
        drawerAccountSection.style.display = 'block';
        drawerAccountLinks.innerHTML = `
          <a href="${prefix}pages/user/dashboard.html" class="drawer-link"><span class="link-icon">📊</span> My Dashboard</a>
          <a href="${prefix}pages/user/bookings.html" class="drawer-link"><span class="link-icon">📅</span> My Bookings</a>
          <a href="${prefix}pages/user/orders.html" class="drawer-link"><span class="link-icon">📦</span> My Orders</a>
          <a href="${prefix}pages/user/my-listings.html" class="drawer-link"><span class="link-icon">🏷️</span> My Listings</a>
          <a href="${prefix}pages/user/requests-received.html" class="drawer-link"><span class="link-icon">📨</span> Incoming Requests</a>
          <a href="${prefix}pages/user/wishlist.html" class="drawer-link"><span class="link-icon">❤️</span> Saved Wishlist</a>
          <a href="${prefix}pages/user/chat.html" class="drawer-link"><span class="link-icon">💬</span> Direct Messages</a>
          <a href="${prefix}pages/user/profile.html" class="drawer-link"><span class="link-icon">⚙️</span> Profile & Settings</a>
          ${this.isAdmin() ? `<a href="${prefix}pages/admin/dashboard.html" class="drawer-link"><span class="link-icon">🛡️</span> Admin Console</a>` : ''}
        `;
      }

      // 4. Mobile Drawer Footer
      if (drawerFooter) {
        drawerFooter.innerHTML = `
          <button class="btn btn-secondary btn-block" onclick="handleLogout()" style="color:var(--danger);width:100%;">
            <span>🚪</span> Log Out
          </button>
        `;
      }

      // 5. Update Bottom Nav Targets
      if (bottomTabAccount) {
        bottomTabAccount.href = `${prefix}pages/user/dashboard.html`;
      }
      if (bottomTabChat) {
        bottomTabChat.href = `${prefix}pages/user/chat.html`;
      }

    } else {
      // Guest / Logged-out state
      if (navActions) {
        navActions.innerHTML = `
          <a href="${prefix}login.html" class="nav-login-link" style="color:#ffffff;font-weight:700;margin-right:8px;">Login</a>
          <a href="${prefix}login.html" class="btn-olx-sell">
            <span class="sell-plus">+</span> SELL
          </a>
        `;
      }

      if (drawerUserCard) {
        drawerUserCard.innerHTML = `
          <div class="drawer-user-avatar">👤</div>
          <div class="drawer-user-meta">
            <div class="drawer-user-name">Welcome, Student!</div>
            <div class="drawer-user-role">Zero Brokerage Uttarakhand Hub</div>
          </div>
        `;
      }

      if (drawerAccountSection) {
        drawerAccountSection.style.display = 'none';
      }

      if (drawerFooter) {
        drawerFooter.innerHTML = `
          <div style="display:flex;gap:10px;">
            <a href="${prefix}login.html" class="btn btn-primary" style="flex:1;text-align:center;">Log In</a>
            <a href="${prefix}register.html" class="btn btn-secondary" style="flex:1;text-align:center;">Sign Up</a>
          </div>
        `;
      }

      if (bottomTabAccount) {
        bottomTabAccount.href = `${prefix}login.html`;
      }
      if (bottomTabChat) {
        bottomTabChat.href = `${prefix}login.html`;
      }
    }

    updateBottomNavActive();
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

/* ==========================================================================
   Global Mobile Navigation & Drawer Interactive Functions
   ========================================================================== */
function openMobileDrawer() {
  const drawer = document.getElementById('mobileDrawer');
  const overlay = document.getElementById('mobileDrawerOverlay');
  if (drawer && overlay) {
    drawer.classList.add('open');
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileDrawer() {
  const drawer = document.getElementById('mobileDrawer');
  const overlay = document.getElementById('mobileDrawerOverlay');
  if (drawer && overlay) {
    drawer.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

function toggleMobileSearch() {
  const drawer = document.getElementById('mobileSearchDrawer');
  const input = document.getElementById('mobileSearchInput');
  if (!drawer) return;
  const isOpen = drawer.classList.toggle('open');
  if (isOpen && input) {
    setTimeout(() => input.focus(), 150);
  }
}

function clearMobileSearch() {
  const input = document.getElementById('mobileSearchInput');
  const clearBtn = document.getElementById('mobileSearchClear');
  if (input) {
    input.value = '';
    input.focus();
  }
  if (clearBtn) clearBtn.style.display = 'none';
}

function openPostChooser(event) {
  if (event) event.preventDefault();
  const overlay = document.getElementById('postChooserOverlay');
  if (overlay) {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
}

function closePostChooser(event) {
  const overlay = document.getElementById('postChooserOverlay');
  if (overlay) {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

function updateBottomNavActive() {
  const currentPath = window.location.pathname.toLowerCase();
  const items = document.querySelectorAll('.bottom-nav-item');
  items.forEach(item => {
    const tab = item.dataset.tab;
    let isActive = false;
    if ((tab === 'properties' || tab === 'explore') && (currentPath.includes('search-properties') || currentPath.includes('property-detail') || currentPath.endsWith('index.html') || currentPath.endsWith('/') || currentPath === '')) {
      isActive = true;
    } else if (tab === 'products' && (currentPath.includes('search-products') || currentPath.includes('product-detail'))) {
      isActive = true;
    } else if (tab === 'chat' && currentPath.includes('chat.html')) {
      isActive = true;
    } else if (tab === 'account' && (currentPath.includes('dashboard') || currentPath.includes('profile') || currentPath.includes('bookings') || currentPath.includes('orders') || currentPath.includes('my-listings') || currentPath.includes('login') || currentPath.includes('register'))) {
      isActive = true;
    }
    if (isActive) item.classList.add('active');
    else item.classList.remove('active');
  });
}

// Global click & escape listener
document.addEventListener('click', function (event) {
  const dd = document.getElementById('profileDropdown');
  if (dd && dd.classList.contains('open') && !event.target.closest('.avatar-menu')) {
    dd.classList.remove('open');
  }
});

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    closeMobileDrawer();
    closePostChooser();
    if (typeof closeFilterDrawer === 'function') closeFilterDrawer();
    if (typeof closeMobileBookingSheet === 'function') closeMobileBookingSheet();
  }
});

function initAuth() {
  return Auth.init().then(function () {
    Auth.updateNavbar();
  });
}

document.addEventListener('DOMContentLoaded', () => {
  updateBottomNavActive();
  const mobileInput = document.getElementById('mobileSearchInput');
  const desktopInput = document.getElementById('navSearchInput') || document.getElementById('searchInput');
  const clearBtn = document.getElementById('mobileSearchClear');

  if (mobileInput) {
    if (desktopInput && !mobileInput.value && desktopInput.value) {
      mobileInput.value = desktopInput.value;
    }
    if (desktopInput) {
      mobileInput.addEventListener('input', () => {
        desktopInput.value = mobileInput.value;
        if (clearBtn) clearBtn.style.display = mobileInput.value.length ? 'block' : 'none';
      });
      desktopInput.addEventListener('input', () => {
        mobileInput.value = desktopInput.value;
        if (clearBtn) clearBtn.style.display = mobileInput.value.length ? 'block' : 'none';
      });
    } else if (clearBtn) {
      mobileInput.addEventListener('input', () => {
        clearBtn.style.display = mobileInput.value.length ? 'block' : 'none';
      });
    }
  }

  const mobileForm = document.querySelector('.mobile-search-form');
  if (mobileForm && !mobileForm.getAttribute('onsubmit')) {
    mobileForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const mobInput = document.getElementById('mobileSearchInput');
      const query = mobInput ? mobInput.value.trim() : '';
      const prefix = depthPrefix();
      const kw = query.toLowerCase();
      if (kw.includes('laptop') || kw.includes('phone') || kw.includes('bike') || kw.includes('book') || kw.includes('table') || kw.includes('cooler') || kw.includes('guitar')) {
        window.location.href = `${prefix}search-products.html?q=${encodeURIComponent(query)}`;
      } else {
        window.location.href = `${prefix}search-properties.html?q=${encodeURIComponent(query)}`;
      }
    });
  }
});