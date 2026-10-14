let product = null;
let currentUserId = null;
let galleryImages = [];
let galleryIndex = 0;
let isInWishlist = false;
const productId = new URLSearchParams(window.location.search).get('id');

async function loadProduct() {
  const root = document.getElementById('detailRoot');
  if (!productId) {
    renderError(root, 'No product selected.');
    return;
  }
  try {
    product = await ProductAPI.getById(productId);
  } catch (error) {
    renderError(root, error.message || 'This product could not be found.');
    return;
  }
  logBehavior('VIEW', 'PRODUCT', product.id, null, product.location && product.location.city);
  document.title = `${product.title} - StayMart`;
  galleryImages = Array.isArray(product.images) ? product.images.filter(Boolean) : [];
  renderDetail(root);
  loadReviews();
  loadSimilar();
}

function renderError(root, message) {
  root.innerHTML = `
    <div class="not-found">
      <h1>404</h1>
      <p>${escapeHtml(message)}</p>
      <a href="search-products.html" class="btn btn-primary">Browse Products</a>
    </div>
  `;
}

function renderDetail(root) {
  if (!galleryImages.length) galleryImages = [null];
  const seller = product.postedBy || {};
  const locationText = [product.area, product.location && product.location.city].filter(Boolean).join(', ');
  const isOwner = currentUserId && seller.id === currentUserId;
  const listingType = product.listingType || 'SELL';
  const isRentOnly = listingType === 'RENT';
  const isBoth = listingType === 'BOTH';
  const primaryAction = isRentOnly ? 'Rent Now' : (isBoth ? 'Buy or Rent' : 'Buy Now');

  root.innerHTML = `
    <section class="detail-layout">
      <div>
        <div class="gallery">
          <div class="gallery-main" onclick="openLightbox(0)">
            ${galleryImages[0]
              ? `<img id="mainGalleryImg" src="${escapeHtml(galleryImages[0])}" alt="${escapeHtml(product.title)}"/>`
              : `<div class="img-fallback" id="mainGalleryImg">📦</div>`}
          </div>
          ${galleryImages.length > 1 ? `
          <div class="gallery-thumbs">
            ${galleryImages.map(function (img, i) {
              return img
                ? `<img src="${escapeHtml(img)}" class="${i === 0 ? 'active' : ''}" onclick="switchGallery(${i})" alt="Image ${i + 1}"/>`
                : '';
            }).join('')}
          </div>` : ''}
        </div>

        <div style="position:relative">
          <button id="wishlistBtn" class="wishlist-btn" onclick="toggleWishlist(event)" title="Save to wishlist">♡</button>
        </div>

        <h1 class="detail-title" style="margin-top:10px">${escapeHtml(product.title)}</h1>

        <div class="detail-meta">
          <span class="badge ${getTypeBadgeClass(listingType)}" style="padding:6px 12px">${getListingTypeLabel(listingType)}</span>
          <span class="badge ${getConditionBadgeClass(product.condition)}" style="padding:6px 12px">${getConditionLabel(product.condition)}</span>
          ${locationText ? `<span class="meta-item">📍 ${escapeHtml(locationText)}</span>` : ''}
          <span class="meta-item">👀 ${product.viewsCount || 0} views</span>
          <span class="meta-item">Listed ${timeAgo(product.createdAt)}</span>
        </div>

        <div class="info-cards">
          <div class="info-card"><span class="info-icon">🏷️</span><div class="info-value">${escapeHtml(product.category ? product.category.name : 'Other')}</div><div class="info-label">Category</div></div>
          ${product.brand ? `<div class="info-card"><span class="info-icon">🏭</span><div class="info-value">${escapeHtml(product.brand)}</div><div class="info-label">Brand</div></div>` : ''}
          <div class="info-card"><span class="info-icon">✨</span><div class="info-value">${getConditionLabel(product.condition)}</div><div class="info-label">Condition</div></div>
          <div class="info-card"><span class="info-icon">📷</span><div class="info-value">${galleryImages.length}</div><div class="info-label">Photos</div></div>
        </div>

        <h2 class="section-title" style="font-size:20px;margin:28px 0 14px">About this item</h2>
        <p class="text-secondary-text" style="white-space:pre-line">${escapeHtml(product.description || 'No description provided.')}</p>

        <div class="section" style="padding-top:40px">
          <div class="reviews-header" id="reviewsHeader"></div>
          <div id="reviewsList"></div>
          <div id="reviewFormWrap"></div>
        </div>

        <div class="section" style="padding-top:0">
          <div class="section-header">
            <h2 class="section-title">Similar Products</h2>
            <a class="section-link" href="search-products.html">View more →</a>
          </div>
          <div id="similarGrid" class="grid-3"></div>
        </div>
      </div>

      <aside class="sidebar-sticky">
        <div class="poster-card" style="margin-bottom:16px">
          <div class="avatar">${seller.profilePic
            ? `<img src="${escapeHtml(seller.profilePic)}" alt=""/>`
            : escapeHtml(((seller.name || 'U')[0] || 'U').toUpperCase())}</div>
          <div style="min-width:0">
            <div class="poster-name">${escapeHtml(seller.name || 'Seller')}</div>
            <div class="poster-info">${escapeHtml(seller.city || 'Uttarakhand')}${seller.isVerified ? ' · ✅ Verified' : ''}</div>
          </div>
        </div>

        <div class="action-card">
          <div class="action-price">${formatPrice(product.price, listingType)}</div>

          ${isOwner ? `
            <div class="safety-tip">👋 This is your own listing. Manage its status from <strong>My Listings</strong>.</div>
          ` : `
            <div class="input-group">
              <label for="qtySelect">Quantity</label>
              <select id="qtySelect"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select>
            </div>
            ${(isBoth || isRentOnly) ? `
            <div class="input-group">
              <label for="orderTypeSelect">Order type</label>
              <select id="orderTypeSelect">
                ${isBoth ? '<option value="BUY">Buy (one-time)</option><option value="RENT">Rent (monthly)</option>' : '<option value="RENT">Rent (monthly)</option>'}
              </select>
            </div>
            <div class="input-group" id="rentDatesWrap">
              <label for="rentStart">Rent from</label>
              <input id="rentStart" type="date"/>
            </div>
            <div class="input-group" id="rentMonthsWrap">
              <label for="rentMonths">Rent duration</label>
              <select id="rentMonths">
                ${[1, 2, 3, 4, 6].map(function (m) { return `<option value="${m}">${m} month${m > 1 ? 's' : ''}</option>`; }).join('')}
              </select>
            </div>
            ` : ''}
            <div class="input-group">
              <label for="orderMessage">Message to seller<span class="text-muted-text"> (optional)</span></label>
              <textarea id="orderMessage" rows="2" maxlength="300" placeholder="e.g. Available this weekend for pickup?"></textarea>
            </div>
            <div class="total-display">
              <span class="total-label">Total</span>
              <span class="total-value" id="orderTotal">—</span>
            </div>
            <button class="btn btn-primary btn-block" onclick="placeOrder()">${primaryAction}</button>
            <div class="safety-tip" style="margin-top:16px">🛡️ <strong>Safety Tip:</strong> Meet in a public place, inspect the item, and pay only after you're satisfied.</div>
          `}
        </div>

        ${!isOwner ? `
        <button class="btn btn-secondary btn-block mt-8" onclick="contactSeller()">💬 Message Seller</button>
        ` : ''}
        ${seller.phone ? `
        <a class="btn btn-success btn-block mt-8" href="tel:+91${escapeHtml(seller.phone)}">📞 Call +91 ${escapeHtml(seller.phone)}</a>
        ` : ''}
      </aside>
    </section>
  `;

  wireOrderForm();
}

function wireOrderForm() {
  const orderTypeSelect = document.getElementById('orderTypeSelect');
  if (!orderTypeSelect) return;
  const rentDatesWrap = document.getElementById('rentDatesWrap');
  const rentMonthsWrap = document.getElementById('rentMonthsWrap');
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('rentStart').min = today;
  document.getElementById('rentStart').value = today;
  document.getElementById('rentMonths').value = '1';
  function refresh() {
    const isRent = orderTypeSelect.value === 'RENT';
    rentDatesWrap.style.display = isRent ? '' : 'none';
    rentMonthsWrap.style.display = isRent ? '' : 'none';
    updateTotal();
  }
  orderTypeSelect.addEventListener('change', refresh);
  document.getElementById('qtySelect').addEventListener('change', updateTotal);
  document.getElementById('rentMonths').addEventListener('change', updateTotal);
  refresh();
}

function updateTotal() {
  const totalEl = document.getElementById('orderTotal');
  const qty = Number(document.getElementById('qtySelect').value);
  const orderTypeSelect = document.getElementById('orderTypeSelect');
  if (!totalEl) return;
  if (orderTypeSelect && orderTypeSelect.value === 'RENT') {
    const months = Number(document.getElementById('rentMonths').value);
    totalEl.textContent = formatPrice(Number(product.price) * qty * months, 'RENT');
  } else {
    totalEl.textContent = formatPrice(Number(product.price) * qty, 'SELL');
  }
}

async function placeOrder() {
  if (!Auth.isLoggedIn()) {
    showToast('Please login to place this order.', 'info');
    setTimeout(function () { window.location.href = 'login.html'; }, 1200);
    return;
  }
  const quantity = Number(document.getElementById('qtySelect').value);
  const message = document.getElementById('orderMessage').value.trim();
  const orderTypeSelect = document.getElementById('orderTypeSelect');
  const orderType = orderTypeSelect && orderTypeSelect.value === 'RENT' ? 'RENT' : 'BUY';
  const body = {
    productId: product.id,
    quantity,
    orderType,
    message
  };
  if (orderType === 'RENT') {
    const start = document.getElementById('rentStart').value;
    const months = Number(document.getElementById('rentMonths').value);
    const startDate = new Date(start);
    const endDate = new Date(startDate);
    endDate.setMonth(endDate.getMonth() + months);
    body.rentStart = toLocalDate(startDate);
    body.rentEnd = toLocalDate(endDate);
  }
  try {
    await OrderAPI.create(body);
    logBehavior('ORDER', 'PRODUCT', product.id, null, null);
    showToast('Order placed! The seller will get in touch. 📦', 'success');
    setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/my-orders.html`; }, 1200);
  } catch (error) {
    await showModal(error.message || 'Order could not be placed.', 'Order failed', 'Try again');
  }
}

async function toggleWishlist(event) {
  event.stopPropagation();
  if (!Auth.isLoggedIn()) {
    showToast('Please login to save items.', 'info');
    setTimeout(function () { window.location.href = 'login.html'; }, 1200);
    return;
  }
  const btn = document.getElementById('wishlistBtn');
  try {
    if (isInWishlist) {
      await WishlistAPI.remove('PRODUCT', product.id);
      isInWishlist = false;
      btn.classList.remove('active');
      btn.innerHTML = '♡';
      logBehavior('WISHLIST', 'PRODUCT', product.id, null, null);
      showToast('Removed from wishlist.', 'info');
    } else {
      await WishlistAPI.add('PRODUCT', product.id);
      isInWishlist = true;
      btn.classList.add('active');
      btn.innerHTML = '❤️';
      logBehavior('WISHLIST', 'PRODUCT', product.id, null, null);
      showToast('Saved to your wishlist! ❤️', 'success');
    }
  } catch (error) {
    showToast(error.message || 'Could not update wishlist.', 'error');
  }
}

async function contactSeller() {
  const seller = product.postedBy || {};
  if (!seller.id) return;
  if (!Auth.isLoggedIn()) {
    showToast('Please login to message the seller.', 'info');
    setTimeout(function () { window.location.href = 'login.html'; }, 1200);
    return;
  }
  try {
    await ChatAPI.send({
      receiverId: seller.id,
      listingType: 'PRODUCT',
      listingId: product.id,
      message: `Hi! I'm interested in "${product.title}".`
    });
    logBehavior('CONTACT', 'PRODUCT', product.id, null, null);
    showToast('Message sent! The seller will reply in your Chats. 💬', 'success');
    setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/messages.html`; }, 1200);
  } catch (error) {
    showToast(error.message || 'Could not send message.', 'error');
  }
}

async function loadReviews() {
  const header = document.getElementById('reviewsHeader');
  const list = document.getElementById('reviewsList');
  let summary = { averageRating: 0, count: 0 };
  try {
    summary = await ReviewAPI.getSummary('PRODUCT', product.id);
  } catch (error) {
    // summary endpoint may be unavailable; fall through to list
  }
  header.innerHTML = `
    <div class="reviews-avg">
      <div class="big">${summary.averageRating ? Number(summary.averageRating).toFixed(1) : '—'}</div>
      <div class="sub">${summary.count || 0} review${(summary.count || 0) === 1 ? '' : 's'}</div>
    </div>
  `;
  try {
    const page = await ReviewAPI.getByItem('PRODUCT', product.id, 0, 3);
    const reviews = page.content || [];
    if (reviews.length) {
      list.innerHTML = reviews.map(renderReviewCard).join('');
    } else {
      list.innerHTML = '<div class="empty-state" style="padding:24px"><span class="empty-icon">💬</span><p>No reviews yet — be the first to review this item.</p></div>';
    }
  } catch (error) {
    list.innerHTML = '<div class="text-muted-text">Reviews are loading…</div>';
  }
  const wrap = document.getElementById('reviewFormWrap');
  if (Auth.isLoggedIn() && !(product.postedBy && product.postedBy.id === currentUserId)) {
    wrap.innerHTML = `
      <div class="card" style="padding:22px;margin-top:16px">
        <h3 style="font-size:17px;font-weight:700;margin-bottom:14px">✍️ Review this item</h3>
        <div id="reviewStars" style="display:flex;gap:2px;margin-bottom:12px"></div>
        <div class="input-group">
          <textarea id="reviewComment" rows="3" maxlength="500" placeholder="How was the item? Worth the price?"></textarea>
        </div>
        <button class="btn btn-primary" onclick="submitReview()">Submit Review</button>
      </div>
    `;
    renderStarInput();
  }
}

function renderReviewCard(review) {
  const reviewer = review.user || review.reviewedBy || {};
  const rating = review.rating || 0;
  return `
    <div class="review-card">
      <div class="review-head">
        <div class="avatar" style="width:36px;height:36px;font-size:15px">${escapeHtml(((reviewer.name || 'U')[0] || 'U').toUpperCase())}</div>
        <strong>${escapeHtml(reviewer.name || 'User')}</strong>
        <span class="star-rating" style="margin-left:4px">${'★'.repeat(Math.floor(rating))}<span class="star-empty">${'★'.repeat(5 - Math.floor(rating))}</span></span>
        <span class="review-date">${timeAgo(review.createdAt)}</span>
      </div>
      <div class="review-comment">${escapeHtml(review.comment || '')}</div>
    </div>
  `;
}

function renderStarInput() {
  const box = document.getElementById('reviewStars');
  box.innerHTML = '';
  const stars = [];
  for (let i = 1; i <= 5; i++) {
    const star = document.createElement('span');
    star.textContent = '☆';
    star.style.fontSize = '26px';
    star.dataset.value = i;
    box.appendChild(star);
    stars.push(star);
  }
  function paint(n) {
    stars.forEach(function (s) {
      s.textContent = Number(s.dataset.value) <= n ? '★' : '☆';
    });
  }
  stars.forEach(function (star) {
    star.addEventListener('mouseenter', function () { paint(Number(star.dataset.value)); });
    star.addEventListener('click', function () {
      window.__reviewRating = Number(star.dataset.value);
      paint(window.__reviewRating);
    });
  });
  box.addEventListener('mouseleave', function () { paint(window.__reviewRating || 0); });
}

async function submitReview() {
  if (!window.__reviewRating) {
    showToast('Please select a star rating first.', 'info');
    return;
  }
  const comment = document.getElementById('reviewComment').value.trim();
  try {
    await ReviewAPI.add({ itemType: 'PRODUCT', itemId: product.id, rating: window.__reviewRating, comment });
    showToast('Thanks for your review! ⭐', 'success');
    loadReviews();
  } catch (error) {
    showToast(error.message || 'Could not submit review.', 'error');
  }
}

async function loadSimilar() {
  const grid = document.getElementById('similarGrid');
  let items = [];
  try {
    const categoryId = product.category && product.category.id;
    const city = product.location && product.location.city;
    const page = await ProductAPI.getAll({ categoryId: categoryId || '', city: city || '', page: 0, size: 6 });
    items = (page.content || []).filter(function (p) { return p.id !== product.id; }).slice(0, 3);
    if (!items.length) {
      const fallback = await ProductAPI.getAll({ page: 0, size: 6 });
      items = (fallback.content || []).filter(function (p) { return p.id !== product.id; }).slice(0, 3);
    }
  } catch (error) {
    grid.innerHTML = '';
    return;
  }
  grid.innerHTML = items.map(buildProductCard).join('') || '<div class="text-muted-text">No similar products right now.</div>';
}

function switchGallery(index) {
  galleryIndex = index;
  const main = document.getElementById('mainGalleryImg');
  if (main && galleryImages[index]) {
    main.src = galleryImages[index];
    main.className = '';
  }
  document.querySelectorAll('.gallery-thumbs img').forEach(function (thumb, i) {
    thumb.classList.toggle('active', i === index);
  });
}

function openLightbox(index) {
  if (!galleryImages.length || !galleryImages[index]) return;
  galleryIndex = index;
  document.getElementById('lightboxImg').src = galleryImages[index];
  document.getElementById('lightbox').classList.add('open');
}

function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
}

document.addEventListener('click', function (event) {
  if (event.target && event.target.id === 'lightbox') closeLightbox();
});

window.addEventListener('keydown', function (event) {
  if (!document.getElementById('lightbox').classList.contains('open')) return;
  if (event.key === 'Escape') closeLightbox();
});

document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    currentUserId = Auth.isLoggedIn() ? Auth.user.id : null;
    loadProduct().then(function () {
      if (currentUserId) {
        WishlistAPI.check('PRODUCT', productId).then(function (result) {
          if (result === true || result === 'true' || result === 1) {
            isInWishlist = true;
            const btn = document.getElementById('wishlistBtn');
            if (btn) { btn.classList.add('active'); btn.innerHTML = '❤️'; }
          }
        }).catch(function () {});
      }
    });
  });
});

function getConditionBadgeClass(condition) {
  const map = {
    NEW: 'badge-new',
    LIKE_NEW: 'badge-like-new',
    GOOD: 'badge-good',
    FAIR: 'badge-fair',
    OLD: 'badge-old'
  };
  return map[condition] || 'badge-used';
}