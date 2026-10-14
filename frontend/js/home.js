let heroTab = 'properties';
let loggedInUserId = null;

function switchHeroTab(tab) {
  heroTab = tab;
  document.querySelectorAll('.search-tab').forEach(function (btn) {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  const q = document.getElementById('heroQuery');
  q.placeholder = tab === 'properties'
    ? "Search 'PG in Dehradun', 'hostel near Doon'..."
    : "Search 'bike for sale', 'books', 'fridge'...";
}

function heroSearch() {
  const q = document.getElementById('heroQuery').value.trim();
  const city = document.getElementById('heroCity').value;
  const params = new URLSearchParams();
  if (q) params.set('q', q);
  if (city) params.set('city', city);
  const target = heroTab === 'properties' ? 'search-properties.html' : 'search-products.html';
  window.location.href = `${target}?${params.toString()}`;
}

async function loadCategories() {
  const grid = document.getElementById('categoryGrid');
  try {
    const categories = await CategoryAPI.getAll();
    if (!categories || !categories.length) throw new Error('empty');
    const accommodationKeys = ['PG', 'PG/ROOM', 'ROOM', 'HOSTEL', 'FLAT', 'DORMITORY', 'APARTMENT', 'BEDSPACE'];
    categories.forEach(function (category) {
      const type = category.type || '';
      const name = (category.name || '').toUpperCase();
      const isAccommodation = type === 'ACCOMMODATION' || accommodationKeys.some(function (k) {
        return name.includes(k);
      });
      const link = isAccommodation ? 'search-properties.html' : 'search-products.html';
      grid.insertAdjacentHTML('beforeend', `
        <a class="category-card" href="${link}">
          <span class="category-icon">${escapeHtml(category.icon) || '🏷️'}</span>
          <span class="category-name">${escapeHtml(category.name)}</span>
        </a>
      `);
    });
  } catch (error) {
    grid.innerHTML = `
      <div class="empty-state" style="grid-column:1/-1">
        <span class="empty-icon">🏷️</span>
        <h3>Categories coming soon</h3>
        <p>Start by browsing properties and products directly.</p>
      </div>
    `;
  }
}

async function loadFeatured() {
  const grid = document.getElementById('featuredGrid');
  grid.innerHTML = '<div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div><div class="skeleton"></div>';
  let items = [];
  try {
    if (loggedInUserId) {
      const recs = await RecommendationAPI.getForUser(loggedInUserId, 8);
      if (recs && recs.length) items = recs.slice(0, 4);
    }
  } catch (error) {
    // recommendations endpoint not wired up yet -> fall back to latest listings
  }
  if (!items.length) {
    try {
      const page = await PropertyAPI.getAll({ page: 0, size: 4, sort: 'createdAt,desc' });
      items = page.content || [];
    } catch (error) {
      grid.innerHTML = emptyStateHtml('🏠', 'No properties found', 'Be the first to post a listing.');
      return;
    }
  }
  grid.innerHTML = items.map(buildPropertyCard).join('') || emptyStateHtml('🏠', 'No properties found', 'Be the first to post a listing.');
}

async function loadTrending() {
  const row = document.getElementById('trendingRow');
  let items = [];
  try {
    const recs = await RecommendationAPI.getTrendingProperties(8);
    if (recs && recs.length) items = recs;
  } catch (error) {
    // trending endpoint not wired up yet -> fall back to latest listings
  }
  if (!items.length) {
    try {
      const page = await PropertyAPI.getAll({ page: 0, size: 8 });
      items = page.content || [];
    } catch (error) {
      row.innerHTML = emptyStateHtml('🔥', 'No trending listings', 'Latest properties will appear here.');
      return;
    }
  }
  row.innerHTML = items.map(buildPropertyCard).join('') || emptyStateHtml('🔥', 'No trending listings', 'Latest properties will appear here.');
}

async function loadTopProducts() {
  const row = document.getElementById('topProductsRow');
  let items = [];
  try {
    const recs = await RecommendationAPI.getTopRatedProducts(8);
    if (recs && recs.length) items = recs;
  } catch (error) {
    // recommendation endpoint not wired up yet -> fall back to latest products
  }
  if (!items.length) {
    try {
      const page = await ProductAPI.getAll({ page: 0, size: 8 });
      items = page.content || [];
    } catch (error) {
      row.innerHTML = emptyStateHtml('🛒', 'No products found', 'Fresh products will appear here.');
      return;
    }
  }
  row.innerHTML = items.map(buildProductCard).join('') || emptyStateHtml('🛒', 'No products found', 'Fresh products will appear here.');
}

function emptyStateHtml(icon, title, text) {
  return `
    <div class="empty-state">
      <span class="empty-icon">${icon}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(text)}</p>
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    if (Auth.isLoggedIn() && Auth.user) {
      loggedInUserId = Auth.user.id;
    }
    loadCategories();
    loadFeatured();
    loadTrending();
    loadTopProducts();
  });
});