const pageType = document.title.toLowerCase().includes('product') ? 'products' : 'properties';

let state = {
  q: '',
  city: '',
  page: 0,
  size: 12,
  sort: 'newest',
  minPrice: '',
  maxPrice: '',
  gender: '',
  types: [],
  amenities: [],
  categoryId: '',
  listingType: '',
  conditions: []
};

function initState() {
  const params = new URLSearchParams(window.location.search);
  state.q = params.get('q') || '';
  state.city = params.get('city') || '';
  state.categoryId = params.get('category') || '';
  const page = parseInt(params.get('page'), 10);
  state.page = !isNaN(page) && page > 0 ? page - 1 : 0;
  document.getElementById('searchInput').value = state.q;
  document.getElementById('citySelect').value = state.city;
  if (pageType === 'products' && state.categoryId) {
    markCategoryRadio(state.categoryId);
  }
}

function markCategoryRadio(id) {
  const radios = document.querySelectorAll('input[name="category"]');
  radios.forEach(function (r) {
    if (r.value === String(id)) r.checked = true;
  });
}

async function loadProductCategories() {
  const list = document.getElementById('categoryList');
  if (!list) return;
  try {
    const categories = await CategoryAPI.getAll();
    const accommodationHints = ['PG', 'ROOM', 'HOSTEL', 'HOTEL', 'FLAT', 'DORMITORY', 'APARTMENT', 'BEDSPACE', 'STAY'];
    const productCategories = (categories || []).filter(function (c) {
      if (c.type) return c.type === 'PRODUCT';
      const name = String(c.name || '').toUpperCase();
      return !accommodationHints.some(function (hint) { return name.includes(hint); });
    });
    let html = '<label class="check-row"><input type="radio" name="category" value="" checked/> All Categories</label>';
    productCategories.forEach(function (c) {
      const checked = c.id === Number(state.categoryId) ? ' checked' : '';
      html += `<label class="check-row"><input type="radio" name="category" value="${c.id}"${checked}/> ${escapeHtml(c.icon || '🏷️')} ${escapeHtml(c.name)}</label>`;
    });
    list.innerHTML = productCategories.length ? html : 'No categories available.';
  } catch (error) {
    list.innerHTML = 'Could not load categories.';
  }
}

function readFilterState() {
  state.q = document.getElementById('searchInput').value.trim();
  state.city = document.getElementById('citySelect').value || '';
  state.minPrice = document.getElementById('minPrice') ? document.getElementById('minPrice').value : '';
  state.maxPrice = document.getElementById('maxPrice') ? document.getElementById('maxPrice').value : '';
  if (pageType === 'properties') {
    state.types = Array.from(document.querySelectorAll('[data-group="types"] input[type="checkbox"]'))
      .filter(function (cb) { return cb.checked; })
      .map(function (cb) { return cb.value; });
    state.amenities = Array.from(document.querySelectorAll('[data-group="amenities"] input[type="checkbox"]'))
      .filter(function (cb) { return cb.checked; })
      .map(function (cb) { return cb.value; });
    const gender = document.querySelector('input[name="gender"]:checked');
    state.gender = gender ? gender.value : '';
  } else {
    state.categoryId = (document.querySelector('input[name="category"]:checked') || {}).value || '';
    state.listingType = (document.querySelector('input[name="listingType"]:checked') || {}).value || '';
    state.conditions = Array.from(document.querySelectorAll('[data-group="conditions"] input[type="checkbox"]'))
      .filter(function (cb) { return cb.checked; })
      .map(function (cb) { return cb.value; });
  }
}

function buildQueryParams() {
  const p = {
    q: state.q || '',
    city: state.city || '',
    page: state.page,
    size: state.size,
    available: true
  };
  if (pageType === 'properties') {
    p.type = state.types.length === 1 ? state.types[0] : '';
    p.gender = state.gender;
    p.minPrice = state.minPrice;
    p.maxPrice = state.maxPrice;
  } else {
    p.categoryId = state.categoryId;
    p.listingType = state.listingType;
    p.minPrice = state.minPrice;
    p.maxPrice = state.maxPrice;
    if (state.conditions.length === 1) p.condition = state.conditions[0];
  }
  Object.keys(p).forEach(function (k) {
    if (p[k] === '' || p[k] === undefined || p[k] === null) delete p[k];
  });
  return p;
}

function passClientFilters(item) {
  if (pageType === 'properties') {
    if (state.types.length > 1 && !state.types.includes(item.type)) return false;
    if (state.amenities.length) {
      if (!Array.isArray(item.amenities)) return false;
      const normalized = item.amenities.map(function (a) { return String(a).toLowerCase(); });
      if (!state.amenities.every(function (want) {
        return normalized.some(function (have) { return have.includes(want.toLowerCase()); });
      })) return false;
    }
  } else {
    if (state.conditions.length > 1 && !state.conditions.includes(item.condition)) return false;
  }
  return true;
}

function applySort(items) {
  const sorted = items.slice();
  if (state.sort === 'price-asc') sorted.sort(function (a, b) { return Number(a.pricePerMonth || a.price) - Number(b.pricePerMonth || b.price); });
  if (state.sort === 'price-desc') sorted.sort(function (a, b) { return Number(b.pricePerMonth || b.price) - Number(a.pricePerMonth || a.price); });
  return sorted;
}

async function loadResults() {
  const grid = document.getElementById('resultsGrid');
  const countEl = document.getElementById('resultsCount');
  grid.innerHTML = '<div class="skeleton" style="grid-column:1/-1"></div>';
  countEl.textContent = 'Searching…';

  readFilterState();
  renderActiveFilters();

  if (pageType === 'products') {
    await loadProductCategories();
  }

  let items = [];
  let totalElements = 0;
  let totalPages = 0;

  try {
    const params = buildQueryParams();
    let page;
    if (pageType === 'properties') {
      logBehavior('SEARCH', null, null, state.q, state.city);
      page = await PropertyAPI.getAll(params);
    } else {
      logBehavior('SEARCH', 'PRODUCT', null, state.q, state.city);
      page = await ProductAPI.getAll(params);
    }
    items = applySort((page.content || []).filter(passClientFilters));
    totalElements = page.totalElements || 0;
    totalPages = page.totalPages || 0;
  } catch (error) {
    grid.innerHTML = emptyHtml('😕', 'Something went wrong', error.message || 'Please try again in a moment.');
    countEl.textContent = '0 results';
    renderPagination(document.getElementById('pagination'), state.page, 0, goToPage);
    return;
  }

  if (!items.length) {
    grid.innerHTML = pageType === 'properties'
      ? emptyHtml('🏠', 'No properties match your filters yet', 'Try clearing filters or searching a different city.')
      : emptyHtml('🛒', 'No products match your filters yet', 'Try clearing filters or browsing a different category.');
    countEl.textContent = `${totalElements} listing${totalElements === 1 ? '' : 's'} found`;
  } else {
    grid.innerHTML = items.map(pageType === 'properties' ? buildPropertyCard : buildProductCard).join('');
    countEl.textContent = `${totalElements} listing${totalElements === 1 ? '' : 's'} found`;
  }

  renderPagination(document.getElementById('pagination'), state.page, totalPages, goToPage);
}

function renderActiveFilters() {
  const box = document.getElementById('activeFilters');
  const chips = [];
  if (state.q) chips.push(['q', `🔍 "${state.q}"`]);
  if (state.city) chips.push(['city', `📍 ${state.city}`]);
  if (pageType === 'properties') {
    if (state.types.length) chips.push(['types', `🏠 ${state.types.join(', ')}`]);
    if (state.amenities.length) chips.push(['amenities', `📶 ${state.amenities.join(', ')}`]);
    if (state.gender) chips.push(['gender', state.gender === 'MALE' ? '👨 Boys Only' : '👩 Girls Only']);
  } else {
    if (state.categoryId) chips.push(['category', '🗂️ Category selected']);
    if (state.listingType) chips.push(['listingType', getListingTypeLabel(state.listingType)]);
    if (state.conditions.length) chips.push(['conditions', `✨ ${state.conditions.join(', ')}`]);
  }
  if (state.minPrice) chips.push(['minPrice', `Min ₹${state.minPrice}`]);
  if (state.maxPrice) chips.push(['maxPrice', `Max ₹${state.maxPrice}`]);
  if (!chips.length) {
    box.innerHTML = '';
    return;
  }
  box.innerHTML = chips.map(function (chip) {
    return `<span class="filter-tag">${chip[1]} <button onclick="removeFilter('${chip[0]}')">×</button></span>`;
  }).join('');
  const clearAll = document.createElement('span');
  clearAll.className = 'filter-tag';
  clearAll.style.cursor = 'pointer';
  clearAll.style.background = 'var(--primary)';
  clearAll.style.color = '#fff';
  clearAll.innerHTML = 'Clear all ×';
  clearAll.onclick = function () { resetFilters(); };
  box.appendChild(clearAll);
}

function removeFilter(key) {
  if (key === 'q') state.q = '';
  if (key === 'city') state.city = '';
  if (key === 'types') state.types = [];
  if (key === 'amenities') state.amenities = [];
  if (key === 'gender') state.gender = '';
  if (key === 'category') state.categoryId = '';
  if (key === 'listingType') state.listingType = '';
  if (key === 'conditions') state.conditions = [];
  if (key === 'minPrice') state.minPrice = '';
  if (key === 'maxPrice') state.maxPrice = '';
  document.getElementById('searchInput').value = state.q;
  document.getElementById('citySelect').value = state.city;
  if (key === 'gender') {
    const any = document.querySelector('input[name="gender"][value=""]');
    if (any) any.checked = true;
  }
  if (key === 'category') {
    const allCat = document.querySelector('input[name="category"][value=""]');
    if (allCat) allCat.checked = true;
  }
  if (key === 'listingType') {
    const all = document.querySelector('input[name="listingType"][value=""]');
    if (all) all.checked = true;
  }
  loadResults();
}

function applySearch() {
  state.page = 0;
  loadResults();
}

function resetFilters() {
  state.q = '';
  state.city = '';
  state.page = 0;
  state.minPrice = '';
  state.maxPrice = '';
  state.gender = '';
  state.types = [];
  state.amenities = [];
  state.categoryId = '';
  state.listingType = '';
  state.conditions = [];
  document.getElementById('searchInput').value = '';
  document.getElementById('citySelect').value = '';
  if (document.getElementById('minPrice')) document.getElementById('minPrice').value = '';
  if (document.getElementById('maxPrice')) document.getElementById('maxPrice').value = '';
  document.querySelectorAll('input[type="checkbox"]').forEach(function (cb) { cb.checked = false; });
  document.querySelectorAll('input[type="radio"]:checked').forEach(function (r) {
    if (r.value !== '') r.checked = false;
    const anyNone = r.closest('.filter-group') && r.name === 'gender' && r.value === '';
  });
  const genderAny = document.querySelector('input[name="gender"][value=""]');
  if (genderAny) genderAny.checked = true;
  const listingAny = document.querySelector('input[name="listingType"][value=""]');
  if (listingAny) listingAny.checked = true;
  const catAny = document.querySelector('input[name="category"][value=""]');
  if (catAny) catAny.checked = true;
  loadResults();
}

function goToPage(page) {
  state.page = page;
  loadResults();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function emptyHtml(icon, title, text) {
  return `
    <div class="empty-state" style="grid-column:1/-1">
      <span class="empty-icon">${icon}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(text)}</p>
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', function () {
  const sortEl = document.getElementById('sortSelect');
  if (sortEl) {
    sortEl.addEventListener('change', function () {
      state.sort = this.value;
      state.page = 0;
      loadResults();
    });
  }
  initState();
  initAuth().then(function () {
    loadResults();
  });
});