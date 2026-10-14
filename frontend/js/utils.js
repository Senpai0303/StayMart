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

function buildPropertyCard(property) {
  const image = getFirstImage(property.images);
  const imgHtml = image
    ? `<img class="card-img" src="${escapeHtml(image)}" alt="${escapeHtml(property.title)}" loading="lazy"/>`
    : `<div class="card-img flex-center" style="font-size:48px;background:var(--gradient-card)">🏠</div>`;
  const meta = [];
  if (property.area) meta.push(`📍 ${escapeHtml(property.area)}`);
  if (property.genderPreference && property.genderPreference !== 'ANY') meta.push(getGenderLabel(property.genderPreference));
  const location = property.location && property.location.city ? escapeHtml(property.location.city) : '';
  return `
    <a class="card property-card" href="property-detail.html?id=${property.id}">
      <div class="card-img-wrapper" style="position:relative">${imgHtml}</div>
      <div class="card-body">
        <div class="card-title">${escapeHtml(property.title)}</div>
        <span class="badge ${getTypeBadgeClass(property.type)}">${getPropertyTypeLabel(property.type)}</span>
        <div class="card-subtitle">${meta.join(' · ')}</div>
        <div class="small-number-row">
          <span>🚪 ${property.totalRooms || 0} rooms</span>
          ${property.isAvailable ? '<span class="badge badge-available" style="background:rgba(16,185,129,.15);color:#34d399">Available</span>' : ''}
        </div>
        <div class="card-footer">
          <div class="card-price">${formatPrice(property.pricePerMonth, 'RENT')}</div>
          ${property.avgRating ? renderStars(property.avgRating) : '<span class="badge badge-new">New</span>'}
        </div>
      </div>
    </a>
  `;
}

function buildProductCard(product) {
  const image = getFirstImage(product.images);
  const imgHtml = image
    ? `<img class="card-img" src="${escapeHtml(image)}" alt="${escapeHtml(product.title)}" loading="lazy"/>`
    : `<div class="card-img flex-center" style="font-size:48px;background:var(--gradient-card)">📦</div>`;
  const meta = [];
  if (product.brand) meta.push(`🏷️ ${escapeHtml(product.brand)}`);
  if (product.area) meta.push(`📍 ${escapeHtml(product.area)}`);
  if (meta.length === 0 && product.location && product.location.city) meta.push(`📍 ${escapeHtml(product.location.city)}`);
  return `
    <a class="card product-card" href="product-detail.html?id=${product.id}">
      ${imgHtml}
      <div class="card-body">
        <div class="card-title">${escapeHtml(product.title)}</div>
        <div class="card-subtitle">${meta.join(' · ')}</div>
        <div class="small-number-row">
          <span class="badge ${getTypeBadgeClass(product.listingType)}">${getListingTypeLabel(product.listingType)}</span>
          <span class="badge badge-used">${getConditionLabel(product.condition)}</span>
        </div>
        <div class="card-footer">
          <div class="card-price">${formatPrice(product.price, product.listingType)}</div>
          ${product.avgRating ? renderStars(product.avgRating) : '<span class="badge badge-new">New</span>'}
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