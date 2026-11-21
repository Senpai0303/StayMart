const cityOptions = ['Uttarakhand', 'Dehradun', 'Rishikesh', 'Haridwar', 'Mussoorie', 'Nainital', 'Roorkee'];

function formatPrice(amount, listingType) {
  if (amount === undefined || amount === null || isNaN(amount)) return '₹ —';
  if (listingType && listingType !== 'SELL') {
    return `₹${Number(amount).toLocaleString('en-IN')}/month`;
  }
  return `₹${Number(amount).toLocaleString('en-IN')}`;
}

function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return dateString;
  return date.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function toLocalDate(dateValue) {
  const date = dateValue instanceof Date ? dateValue : new Date(dateValue);
  if (isNaN(date.getTime())) return '';
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function timeAgo(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return '';
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  if (seconds < 60) return 'just now';
  const intervals = {
    year: 31536000,
    month: 2592000,
    week: 604800,
    day: 86400,
    hour: 3600,
    minute: 60
  };
  for (const [unit, secondsInUnit] of Object.entries(intervals)) {
    const value = Math.floor(seconds / secondsInUnit);
    if (value >= 1) {
      return value === 1 ? `1 ${unit} ago` : `${value} ${unit}s ago`;
    }
  }
  return 'just now';
}

function escapeHtml(str) {
  if (str === undefined || str === null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function showToast(message, type = 'success') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  requestAnimationFrame(function () {
    toast.classList.add('show');
  });
  setTimeout(function () {
    toast.classList.remove('show');
    setTimeout(function () {
      container.removeChild(toast);
    }, 350);
  }, 3000);
}

function showModal(message, title = 'Confirm', confirmText = 'OK') {
  return new Promise(function (resolve) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
      <div class="modal">
        <h3 class="modal-title">${escapeHtml(title)}</h3>
        <p class="modal-text">${escapeHtml(message)}</p>
        <div class="modal-actions">
          <button class="btn btn-secondary modal-cancel">Cancel</button>
          <button class="btn btn-primary modal-confirm">${escapeHtml(confirmText)}</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    requestAnimationFrame(function () {
      overlay.classList.add('open');
    });
    overlay.querySelector('.modal-confirm').onclick = function () {
      overlay.classList.remove('open');
      setTimeout(function () { overlay.remove(); }, 300);
      resolve(true);
    };
    overlay.querySelector('.modal-cancel').onclick = function () {
      overlay.classList.remove('open');
      setTimeout(function () { overlay.remove(); }, 300);
      resolve(false);
    };
  });
}

function renderStars(rating) {
  if (rating === undefined || rating === null || isNaN(rating)) {
    return '<span class="star-rating"><span class="rating-value">No ratings yet</span></span>';
  }
  const full = Math.floor(rating);
  const half = rating - full >= 0.5;
  const empty = 5 - full - (half ? 1 : 0);
  let stars = '<span class="star-rating">';
  for (let i = 0; i < full; i++) stars += '★';
  if (half) stars += '<span class="star-half">★<span>★</span></span>';
  for (let i = 0; i < empty; i++) stars += '<span class="star-empty">★</span>';
  stars += `<span class="rating-value">${Number(rating).toFixed(1)}</span>`;
  stars += '</span>';
  return stars;
}

function getIcon(keywords) {
  if (!keywords) return '📌';
  const k = String(keywords).toLowerCase();
  if (k.includes('wifi')) return '📶';
  if (k.includes('parking')) return '🅿️';
  if (k.includes('water')) return '🚰';
  if (k.includes('power')) return '⚡';
  if (k.includes('security')) return '🔒';
  if (k.includes('cleaning')) return '🧹';
  if (k.includes('furnish')) return '🛋️';
  if (k.includes('lunch') || k.includes('dinner')) return '🍲';
  if (k.includes('laundry')) return '🧺';
  if (k.includes('hot water')) return '🚿';
  if (k.includes('gym')) return '🏋️';
  if (k.includes('study')) return '📚';
  return '📌';
}

function getPropertyTypeLabel(type) {
  const labels = {
    PG: 'Paying Guest',
    ROOM: 'Room',
    HOSTEL: 'Hostel',
    HOTEL: 'Hotel',
    FLAT: 'Flat',
    DORMITORY: 'Dormitory'
  };
  return labels[type] || escapeHtml(type);
}

function getGenderLabel(preference) {
  const labels = {
    MALE: 'Boys Only',
    FEMALE: 'Girls Only',
    ANY: 'Any Gender'
  };
  return labels[preference] || escapeHtml(preference);
}

function getListingTypeLabel(type) {
  const labels = {
    SELL: 'For Sale',
    RENT: 'For Rent',
    BOTH: 'Buy or Rent'
  };
  return labels[type] || escapeHtml(type);
}

function getConditionLabel(condition) {
  const labels = {
    NEW: 'New',
    LIKE_NEW: 'Like New',
    GOOD: 'Good',
    FAIR: 'Fair',
    OLD: 'Old'
  };
  return labels[condition] || escapeHtml(condition);
}

function getTypeBadgeClass(type) {
  const map = {
    PG: 'badge-pg',
    ROOM: 'badge-room',
    HOSTEL: 'badge-hostel',
    HOTEL: 'badge-hotel',
    FLAT: 'badge-flat',
    DORMITORY: 'badge-dormitory',
    SELL: 'badge-sell',
    RENT: 'badge-rent',
    BOTH: 'badge-both'
  };
  return map[type] || 'badge-pending';
}

function getStatusBadgeClass(status) {
  const map = {
    PENDING: 'badge-pending',
    APPROVED: 'badge-approved',
    ACTIVE: 'badge-approved',
    REJECTED: 'badge-rejected',
    SUSPENDED: 'badge-rejected'
  };
  return map[status] || 'badge-pending';
}

function getFirstImage(images) {
  if (Array.isArray(images) && images.length) return images[0];
  return null;
}

function toggleCardFav(event, type, id) {
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }
  const key = 'staymart_wishlist_items';
  let list = [];
  try {
    list = JSON.parse(localStorage.getItem(key) || '[]');
  } catch (e) {
    list = [];
  }
  const itemKey = `${type}_${id}`;
  const idx = list.indexOf(itemKey);
  const btn = event ? event.currentTarget : null;
  if (idx > -1) {
    list.splice(idx, 1);
    localStorage.setItem(key, JSON.stringify(list));
    if (btn) {
      btn.innerHTML = '♡';
      btn.classList.remove('active');
    }
    showToast('Removed from favorites', 'info');
  } else {
    list.push(itemKey);
    localStorage.setItem(key, JSON.stringify(list));
    if (btn) {
      btn.innerHTML = '❤️';
      btn.classList.add('active');
    }
    showToast('Saved to favorites! ❤️', 'success');
  }
}

function isCardFaved(type, id) {
  try {
    const list = JSON.parse(localStorage.getItem('staymart_wishlist_items') || '[]');
    return list.includes(`${type}_${id}`);
  } catch (e) {
    return false;
  }
}

function buildPropertyCard(property) {
  const image = getFirstImage(property.images);
  const imgHtml = image
    ? `<img class="card-img" src="${escapeHtml(image)}" alt="${escapeHtml(property.title)}" loading="lazy"/>`
    : `<div class="card-img flex-center" style="font-size:48px;background:#f1f5f9;display:flex;align-items:center;justify-content:center;">🏠</div>`;
  
  const isFav = isCardFaved('property', property.id);
  const favIcon = isFav ? '❤️' : '♡';
  const favClass = isFav ? 'active' : '';

  const loc = property.area || (property.location && property.location.city) || 'Dehradun';
  const ago = timeAgo(property.createdAt).toUpperCase();
  const gender = property.genderPreference && property.genderPreference !== 'ANY' ? getGenderLabel(property.genderPreference) : 'Any Gender';

  // Feature 10 (Occupancy), Feature 9 (Savings), Feature 13 (Engagement)
  const occ = (window.StayMartAccommodationStats && window.StayMartAccommodationStats.getOccupancy)
    ? window.StayMartAccommodationStats.getOccupancy(property)
    : { total: Math.max(1, Number(property.totalRooms) || 1), available: property.isAvailable ? Math.max(1, Number(property.availableRooms) || 1) : 0, rate: 65, status: property.isAvailable ? 'AMPLE' : 'FULL', badgeText: property.isAvailable ? 'Immediate Move-In' : 'Fully Occupied' };
  
  const savings = (window.StayMartAccommodationStats && window.StayMartAccommodationStats.getSavings)
    ? window.StayMartAccommodationStats.getSavings(property)
    : { brokerage: Number(property.pricePerMonth) || 0, diff: 0, zoneShort: 'Campus' };

  const eng = (window.StayMartAccommodationStats && window.StayMartAccommodationStats.getEngagement)
    ? window.StayMartAccommodationStats.getEngagement(property.id)
    : { viewsThisWeek: 28, inquiriesToday: 2 };

  const unitLabel = property.type === 'HOSTEL' ? 'beds' : 'rooms';

  return `
    <a class="card property-card" href="property-detail.html?id=${property.id}">
      <div class="card-img-wrapper">
        ${imgHtml}
        <span class="card-badge-top badge-verified">${getPropertyTypeLabel(property.type).toUpperCase()}</span>
        <button class="card-fav-btn ${favClass}" onclick="toggleCardFav(event, 'property', ${property.id})" title="Save to favorites">${favIcon}</button>
      </div>
      <div class="card-body">
        <div class="card-price-row">
          <div class="card-price">${formatPrice(property.pricePerMonth, 'RENT')}</div>
        </div>

        <!-- Zero Brokerage & Campus Zone Savings Strip (Feature 9) -->
        <div class="card-savings-strip">
          <span class="brokerage-badge">
            <span class="sparkle-icon">✨</span> Zero Brokerage · Save ₹${Number(savings.brokerage).toLocaleString('en-IN')}
          </span>
          ${savings.diff > 400 ? `<span class="zone-discount-pill">-₹${Number(savings.diff).toLocaleString('en-IN')}/mo vs ${savings.zoneShort}</span>` : ''}
        </div>

        <div class="card-specs">
          <span>👥 ${escapeHtml(gender)}</span>
          <span class="specs-dot">•</span>
          <span>🚪 ${property.totalRooms || 0} Rooms</span>
        </div>

        <!-- Real-Time Occupancy & Availability Meter (Feature 10) -->
        <div class="card-occupancy-meter" data-status="${occ.status}">
          <div class="occupancy-meta-row">
            <span class="occupancy-badge status-${occ.status}">
              <span class="pulse-indicator pulse-${occ.status}"></span>
              ${occ.badgeText}
            </span>
            <span class="occupancy-ratio-text">${occ.available} of ${occ.total} ${unitLabel} free</span>
          </div>
          <div class="occupancy-progress-track" role="progressbar" aria-valuenow="${occ.rate}" aria-valuemin="0" aria-valuemax="100">
            <div class="occupancy-progress-bar fill-${occ.status}" style="width: ${occ.rate}%"></div>
          </div>
        </div>

        <div class="card-title" title="${escapeHtml(property.title)}">${escapeHtml(property.title)}</div>

        <!-- Listing Engagement & Peer Inquiry Stats (Feature 13) -->
        <div class="card-engagement-row">
          <span class="eng-stat"><span class="eng-ico">👁️</span> ${eng.viewsThisWeek} viewed</span>
          <span class="eng-dot">•</span>
          <span class="eng-stat eng-hot"><span class="eng-ico">⚡</span> ${eng.inquiriesToday} inquiries today</span>
        </div>

        <div class="card-footer-olx">
          <span class="card-loc">📍 ${escapeHtml(loc)}</span>
          <span class="card-date">${escapeHtml(ago)}</span>
        </div>
      </div>
    </a>
  `;
}

function buildProductCard(product) {
  const image = getFirstImage(product.images);
  const imgHtml = image
    ? `<img class="card-img" src="${escapeHtml(image)}" alt="${escapeHtml(product.title)}" loading="lazy"/>`
    : `<div class="card-img flex-center" style="font-size:48px;background:#f1f5f9;display:flex;align-items:center;justify-content:center;">📦</div>`;
  
  const isFav = isCardFaved('product', product.id);
  const favIcon = isFav ? '❤️' : '♡';
  const favClass = isFav ? 'active' : '';

  const loc = product.area || (product.location && product.location.city) || 'Dehradun';
  const ago = timeAgo(product.createdAt).toUpperCase();
  const brand = product.brand ? escapeHtml(product.brand) : (product.category ? escapeHtml(product.category.name) : 'Verified');

  // Feature 9 (Savings), Feature 11 (Deal Quality), Feature 13 (Engagement)
  const rAnalytics = (window.RecommerceVisuals && window.RecommerceVisuals.getAnalytics)
    ? window.RecommerceVisuals.getAnalytics(product)
    : {
        retailPrice: Math.round((Number(product.price) || 1000) * 2),
        savingsAmount: Math.round(Number(product.price) || 1000),
        savingsPercent: 50,
        dealClass: 'great',
        dealBadge: '💎 Great Student Deal',
        condScore: 7,
        condLabel: 'Good Condition',
        condTier: 'good',
        condPct: 70,
        savedCount: 12,
        viewsLast24h: 34
      };

  return `
    <a class="card product-card" href="product-detail.html?id=${product.id}">
      <div class="card-img-wrapper">
        ${imgHtml}
        <span class="card-badge-top deal-chip chip-${rAnalytics.dealClass}">${rAnalytics.dealBadge}</span>
        <button class="card-fav-btn ${favClass}" onclick="toggleCardFav(event, 'product', ${product.id})" title="Save to favorites">${favIcon}</button>
      </div>
      <div class="card-body">
        <!-- Re-Commerce Retail Anchoring & Emerald Savings Pill (Feature 9) -->
        <div class="card-price-row">
          <div class="card-price">${formatPrice(product.price, product.listingType)}</div>
          <span class="card-retail-orig">₹${Number(rAnalytics.retailPrice).toLocaleString('en-IN')}</span>
          <span class="card-savings-pill">Save ${rAnalytics.savingsPercent}%</span>
        </div>
        <div class="card-savings-detail">Save ₹${Number(rAnalytics.savingsAmount).toLocaleString('en-IN')} vs Amazon/Retail</div>

        <!-- 10-Point Condition Visual Meter (Feature 11) -->
        <div class="card-specs">
          <span>🏷️ ${brand}</span>
          <span class="specs-dot">•</span>
          <div class="card-condition-meter" title="Condition: ${rAnalytics.condScore}/10 (${rAnalytics.condLabel})">
            <span class="meter-badge">${rAnalytics.condScore}/10</span>
            <div class="mini-bar-track">
              <div class="mini-bar-fill fill-${rAnalytics.condTier}" style="width: ${rAnalytics.condPct}%"></div>
            </div>
            <span class="meter-name">${rAnalytics.condLabel.split(' ')[0]}</span>
          </div>
        </div>

        <div class="card-title" title="${escapeHtml(product.title)}">${escapeHtml(product.title)}</div>

        <!-- Student Re-Commerce Social Proof Strip (Feature 13) -->
        <div class="card-engagement-strip">
          <span class="eng-chip eng-favs">❤️ ${rAnalytics.savedCount} saved</span>
          <span class="eng-dot">•</span>
          <span class="eng-chip eng-views">🔥 ${rAnalytics.viewsLast24h} views today</span>
          <span class="eng-dot">•</span>
          <span class="eng-chip eng-senior">Senior Verified</span>
        </div>

        <div class="card-footer-olx">
          <span class="card-loc">📍 ${escapeHtml(loc)}</span>
          <span class="card-date">${escapeHtml(ago)}</span>
        </div>
      </div>
    </a>
  `;
}

function renderPagination(container, page, totalPages, onPageChange) {
  container.innerHTML = '';
  if (totalPages <= 1) return;
  const prevBtn = document.createElement('button');
  prevBtn.className = 'page-btn';
  prevBtn.textContent = '‹';
  prevBtn.disabled = page === 0;
  prevBtn.onclick = function () { onPageChange(page - 1); };
  container.appendChild(prevBtn);

  const start = Math.max(0, page - 2);
  const end = Math.min(totalPages - 1, page + 2);
  for (let i = start; i <= end; i++) {
    const btn = document.createElement('button');
    btn.className = `page-btn${i === page ? ' active' : ''}`;
    btn.textContent = i + 1;
    btn.onclick = function () { onPageChange(i); };
    container.appendChild(btn);
  }

  const nextBtn = document.createElement('button');
  nextBtn.className = 'page-btn';
  nextBtn.textContent = '›';
  nextBtn.disabled = page >= totalPages - 1;
  nextBtn.onclick = function () { onPageChange(page + 1); };
  container.appendChild(nextBtn);
}

async function getLocations(type) {
  try {
    return await LocationAPI.getAll(type || '');
  } catch (error) {
    return [];
  }
}

window.Auth = window.Auth || Auth;