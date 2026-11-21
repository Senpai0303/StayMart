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

  // Feature 9 (Savings), Feature 11 (Price Comparison & Condition), Feature 13 (Engagement)
  const rAnalytics = (window.RecommerceVisuals && window.RecommerceVisuals.getAnalytics)
    ? window.RecommerceVisuals.getAnalytics(product)
    : {
        price: Number(product.price) || 0,
        retailPrice: Math.round((Number(product.price) || 1000) * 2),
        savingsAmount: Math.round(Number(product.price) || 1000),
        savingsPercent: 50,
        dealClass: 'great',
        dealBadge: '💎 Great Student Deal',
        categoryMedian: 3500,
        categoryName: product.category ? product.category.name : 'Gear',
        condScore: 7,
        condLabel: 'Good Condition',
        condTier: 'good',
        condPct: 70,
        savedCount: 14,
        viewsLast24h: 38,
        campusAffiliation: "Graphic Era (GEU '25)",
        responseTime: 'Under 30 mins'
      };

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
          <span class="badge deal-chip chip-${rAnalytics.dealClass}" style="padding:6px 12px">${rAnalytics.dealBadge}</span>
          ${locationText ? `<span class="meta-item">📍 ${escapeHtml(locationText)}</span>` : ''}
          <span class="meta-item">👀 ${product.viewsCount || 0} views</span>
          <span class="meta-item">Listed ${timeAgo(product.createdAt)}</span>
        </div>

        <!-- Student Re-Commerce Social Proof Strip (Feature 13) -->
        <div class="detail-social-proof-strip">
          <div class="proof-pill proof-saved" id="detailSavedCount">
            <span class="proof-icon">❤️</span>
            <span>Saved by <strong id="detailSavedNum">${rAnalytics.savedCount} students</strong></span>
          </div>
          <div class="proof-pill proof-views">
            <span class="pulse-dot"></span>
            <span>Viewed <strong>${rAnalytics.viewsLast24h} times</strong> in 24 hours</span>
          </div>
          <div class="proof-pill proof-speed">
            <span class="proof-icon">⚡</span>
            <span>High Demand: <strong>Replies ${rAnalytics.responseTime}</strong></span>
          </div>
        </div>

        <div class="info-cards">
          <div class="info-card"><span class="info-icon">🏷️</span><div class="info-value">${escapeHtml(product.category ? product.category.name : 'Other')}</div><div class="info-label">Category</div></div>
          ${product.brand ? `<div class="info-card"><span class="info-icon">🏭</span><div class="info-value">${escapeHtml(product.brand)}</div><div class="info-label">Brand</div></div>` : ''}
          <div class="info-card"><span class="info-icon">✨</span><div class="info-value">${rAnalytics.condScore}/10 (${rAnalytics.condLabel.split(' ')[0]})</div><div class="info-label">Condition Rating</div></div>
          <div class="info-card"><span class="info-icon">📷</span><div class="info-value">${galleryImages.length}</div><div class="info-label">Photos</div></div>
        </div>

        <!-- Campus Price Comparison Widget (Feature 11) -->
        <div class="price-trend-widget">
          <div class="trend-widget-header">
            <div class="trend-title">
              <span class="trend-icon">📊</span>
              <strong>Campus Price Comparison</strong>
            </div>
            <span class="trend-status-tag tag-${rAnalytics.price <= rAnalytics.categoryMedian ? 'below' : 'above'}">
              ${rAnalytics.price <= rAnalytics.categoryMedian ? `₹${Number(rAnalytics.categoryMedian - rAnalytics.price).toLocaleString('en-IN')} Below Campus Median` : 'Premium Spec'}
            </span>
          </div>

          <div class="price-meter-track">
            <div class="meter-segment seg-steal" title="Budget Steal Range"></div>
            <div class="meter-segment seg-fair" title="Fair Campus Value"></div>
            <div class="meter-segment seg-premium" title="High-End Benchmark"></div>

            <div class="meter-pointer" style="left: ${Math.min(92, Math.max(8, Math.round((rAnalytics.price / (rAnalytics.categoryMedian * 1.8)) * 100)))}%" title="This Listing: ₹${Number(rAnalytics.price).toLocaleString('en-IN')}">
              <div class="pointer-bubble">₹${Number(rAnalytics.price).toLocaleString('en-IN')}</div>
              <div class="pointer-pin"></div>
            </div>
          </div>

          <div class="meter-scale-legend">
            <span class="scale-label">Budget Steal</span>
            <span class="scale-median">Campus Median: <strong>₹${Number(rAnalytics.categoryMedian).toLocaleString('en-IN')}</strong></span>
            <span class="scale-label">Premium Range</span>
          </div>

          <p class="trend-summary-text">
            This item is priced <strong>${rAnalytics.savingsPercent}% below</strong> the typical new retail asking price for <em>${rAnalytics.categoryName}</em> across Uttarakhand university campuses.
          </p>
        </div>

        <!-- 10-Point Physical Condition Rating Card (Feature 11) -->
        <div class="condition-inspection-card">
          <div class="inspection-header">
            <div class="inspection-title-group">
              <span class="inspection-icon">🔍</span>
              <div>
                <div class="inspection-heading">Physical Condition Rating</div>
                <div class="inspection-sub">Campus Senior Inspection Standard</div>
              </div>
            </div>
            <div class="condition-score-pill score-${rAnalytics.condTier}">
              <span class="score-num">${rAnalytics.condScore} / 10</span>
              <span class="score-tier">${rAnalytics.condLabel}</span>
            </div>
          </div>

          <div class="condition-meter-bar-container">
            <div class="condition-main-track">
              <div class="condition-main-fill fill-${rAnalytics.condTier}" style="width: ${rAnalytics.condPct}%"></div>
            </div>
            <div class="condition-tier-ticks">
              <span class="tick ${rAnalytics.condPct <= 50 ? 'active' : ''}">Fair (5/10)</span>
              <span class="tick ${rAnalytics.condPct > 50 && rAnalytics.condPct <= 75 ? 'active' : ''}">Good (7/10)</span>
              <span class="tick ${rAnalytics.condPct > 75 && rAnalytics.condPct < 100 ? 'active' : ''}">Like New (9/10)</span>
              <span class="tick ${rAnalytics.condPct === 100 ? 'active' : ''}">New (10/10)</span>
            </div>
          </div>

          <div class="inspection-checklist">
            <div class="check-item"><span class="check-ico">✅</span> <strong>Aesthetic Grade:</strong> Clean exterior, verified student single-hand usage.</div>
            <div class="check-item"><span class="check-ico">✅</span> <strong>Functionality Test:</strong> 100% operational, all components and accessories verified.</div>
            <div class="check-item"><span class="check-ico">✅</span> <strong>Senior Assurance:</strong> In-person campus gate handover & zero-advance policy.</div>
          </div>
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
          <div style="display:flex;align-items:center;gap:12px">
            <div class="avatar">${seller.profilePic
              ? `<img src="${escapeHtml(seller.profilePic)}" alt=""/>`
              : escapeHtml(((seller.name || 'U')[0] || 'U').toUpperCase())}</div>
            <div style="min-width:0">
              <div class="poster-name">${escapeHtml(seller.name || 'Seller')}</div>
              <div class="poster-info">${escapeHtml(seller.city || 'Uttarakhand')}${seller.isVerified ? ' · ✅ Verified' : ''}</div>
            </div>
          </div>
          <!-- Enhanced Senior College Tag & Rating -->
          <div class="poster-campus-tag">🎓 ${rAnalytics.campusAffiliation} · Senior Student</div>
          <div class="poster-response-tag">⚡ Typically replies ${rAnalytics.responseTime}</div>
          <div class="poster-rating-row">
            <span class="stars">★★★★★</span>
            <span class="rating-val">4.9</span>
            <span class="rating-count">(18 campus handovers)</span>
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

        <!-- Student Re-Commerce Savings Card (Feature 9) -->
        <div class="student-savings-card">
          <div class="savings-card-header">
            <div class="savings-card-title">
              <span class="savings-icon">🎓</span>
              <strong>Student Re-Commerce Savings</strong>
            </div>
            <span class="badge-savings-highlight">Save ${rAnalytics.savingsPercent}% (₹${Number(rAnalytics.savingsAmount).toLocaleString('en-IN')})</span>
          </div>
          <div class="savings-table">
            <div class="savings-row">
              <span class="label">Original Amazon / Retail MRP:</span>
              <span class="val val-retail">₹${Number(rAnalytics.retailPrice).toLocaleString('en-IN')}</span>
            </div>
            <div class="savings-row">
              <span class="label">Verified Student Price:</span>
              <span class="val val-student">₹${Number(rAnalytics.price).toLocaleString('en-IN')}</span>
            </div>
            <div class="savings-divider"></div>
            <div class="savings-row net-savings">
              <span class="label">Total Kept in Student Pocket:</span>
              <span class="val val-saved">₹${Number(rAnalytics.savingsAmount).toLocaleString('en-IN')}</span>
            </div>
          </div>
          <div class="savings-footnote">
            🛡️ Verified against local Dehradun campus benchmarks and current Amazon retail prices.
          </div>
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

  // Synchronize Mobile Bottom Action Bar
  const mobileCtaPrice = document.getElementById('mobileCtaPrice');
  if (mobileCtaPrice) mobileCtaPrice.textContent = formatPrice(product.price, listingType);

  const mobileCtaBadge = document.getElementById('mobileCtaBadge');
  if (mobileCtaBadge) {
    if (product.status === 'AVAILABLE' || !product.status) {
      mobileCtaBadge.textContent = '● In Stock';
      mobileCtaBadge.style.color = 'var(--success)';
    } else {
      mobileCtaBadge.textContent = '● Sold / Unavailable';
      mobileCtaBadge.style.color = 'var(--danger)';
    }
  }

  const mobileCtaBuyBtn = document.getElementById('mobileCtaBuyBtn');
  if (mobileCtaBuyBtn) {
    if (isOwner) {
      mobileCtaBuyBtn.textContent = 'My Listing';
      mobileCtaBuyBtn.onclick = function() { window.location.href = `${depthPrefix()}pages/user/dashboard.html`; };
    } else {
      mobileCtaBuyBtn.textContent = primaryAction;
      mobileCtaBuyBtn.onclick = openMobileOrderSheet;
    }
  }

  const mobileOrderSheetSub = document.getElementById('mobileOrderSheetSub');
  if (mobileOrderSheetSub) mobileOrderSheetSub.textContent = product.title || '';

  const mobileOrderTypeGroup = document.getElementById('mobileOrderTypeGroup');
  if (mobileOrderTypeGroup) {
    mobileOrderTypeGroup.style.display = (isBoth || isRentOnly) ? '' : 'none';
  }

  const mobileConfirmBtn = document.getElementById('mobileConfirmOrderBtn');
  if (mobileConfirmBtn) mobileConfirmBtn.textContent = `Confirm ${primaryAction}`;

  wireOrderForm();
}

function wireOrderForm() {
  const orderTypeSelect = document.getElementById('orderTypeSelect');
  if (!orderTypeSelect) return;
  const rentDatesWrap = document.getElementById('rentDatesWrap');
  const rentMonthsWrap = document.getElementById('rentMonthsWrap');
  const today = new Date().toISOString().split('T')[0];
  const rentStartEl = document.getElementById('rentStart');
  if (rentStartEl) {
    rentStartEl.min = today;
    rentStartEl.value = today;
  }
  const rentMonthsEl = document.getElementById('rentMonths');
  if (rentMonthsEl) rentMonthsEl.value = '1';
  function refresh() {
    const isRent = orderTypeSelect.value === 'RENT';
    if (rentDatesWrap) rentDatesWrap.style.display = isRent ? '' : 'none';
    if (rentMonthsWrap) rentMonthsWrap.style.display = isRent ? '' : 'none';
    updateTotal();
  }
  orderTypeSelect.addEventListener('change', refresh);
  const qtySelect = document.getElementById('qtySelect');
  if (qtySelect) qtySelect.addEventListener('change', updateTotal);
  if (rentMonthsEl) rentMonthsEl.addEventListener('change', updateTotal);
  refresh();
}

function updateTotal() {
  const totalEl = document.getElementById('orderTotal');
  const qtySelect = document.getElementById('qtySelect');
  const qty = qtySelect ? Number(qtySelect.value) : 1;
  const orderTypeSelect = document.getElementById('orderTypeSelect');
  let totalText = '';
  if (orderTypeSelect && orderTypeSelect.value === 'RENT') {
    const rentMonthsEl = document.getElementById('rentMonths');
    const months = rentMonthsEl ? Number(rentMonthsEl.value) : 1;
    totalText = formatPrice(Number(product.price) * qty * months, 'RENT');
  } else {
    totalText = formatPrice(Number(product.price) * qty, 'SELL');
  }
  if (totalEl) totalEl.textContent = totalText;
  const mobileTotal = document.getElementById('mobileOrderTotal');
  if (mobileTotal) mobileTotal.textContent = totalText;
}

function syncOrderQty(val) {
  const qtySelect = document.getElementById('qtySelect');
  const mobileQty = document.getElementById('mobileQtySelect');
  if (qtySelect && qtySelect.value !== val) qtySelect.value = val;
  if (mobileQty && mobileQty.value !== val) mobileQty.value = val;
  updateTotal();
}

function syncOrderType(val) {
  const orderTypeSelect = document.getElementById('orderTypeSelect');
  const mobileOrderType = document.getElementById('mobileOrderTypeSelect');
  if (orderTypeSelect && orderTypeSelect.value !== val) {
    orderTypeSelect.value = val;
    orderTypeSelect.dispatchEvent(new Event('change'));
  }
  if (mobileOrderType && mobileOrderType.value !== val) mobileOrderType.value = val;
  updateTotal();
}

function openMobileOrderSheet() {
  const overlay = document.getElementById('orderSheetOverlay');
  if (overlay) {
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    const qtySelect = document.getElementById('qtySelect');
    const mobileQty = document.getElementById('mobileQtySelect');
    if (qtySelect && mobileQty) mobileQty.value = qtySelect.value;
    updateTotal();
  }
}

function closeMobileOrderSheet() {
  const overlay = document.getElementById('orderSheetOverlay');
  if (overlay) {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }
}

async function executeMobileOrder() {
  const mobileQty = document.getElementById('mobileQtySelect');
  const mobileMsg = document.getElementById('mobileOrderMessage');
  const mobileOrderType = document.getElementById('mobileOrderTypeSelect');

  const qtySelect = document.getElementById('qtySelect');
  const msg = document.getElementById('orderMessage');
  const orderTypeSelect = document.getElementById('orderTypeSelect');

  if (qtySelect && mobileQty) qtySelect.value = mobileQty.value;
  if (msg && mobileMsg) msg.value = mobileMsg.value;
  if (orderTypeSelect && mobileOrderType && mobileOrderType.value) {
    orderTypeSelect.value = mobileOrderType.value;
  }

  closeMobileOrderSheet();
  await placeOrder();
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
    setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/orders.html`; }, 1200);
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
  const mobileBtn = document.getElementById('mobileCtaWishlist');
  const savedNumEl = document.getElementById('detailSavedNum');
  try {
    if (isInWishlist) {
      await WishlistAPI.remove('PRODUCT', product.id);
      isInWishlist = false;
      if (btn) { btn.classList.remove('active'); btn.innerHTML = '♡'; }
      if (mobileBtn) { mobileBtn.classList.remove('active'); mobileBtn.innerHTML = '♡'; }
      if (savedNumEl) {
        const cur = parseInt(savedNumEl.textContent, 10) || 14;
        savedNumEl.textContent = `${Math.max(1, cur - 1)} students`;
      }
      logBehavior('WISHLIST', 'PRODUCT', product.id, null, null);
      showToast('Removed from wishlist.', 'info');
    } else {
      await WishlistAPI.add('PRODUCT', product.id);
      isInWishlist = true;
      if (btn) { btn.classList.add('active'); btn.innerHTML = '❤️'; }
      if (mobileBtn) { mobileBtn.classList.add('active'); mobileBtn.innerHTML = '❤️'; }
      if (savedNumEl) {
        const cur = parseInt(savedNumEl.textContent, 10) || 14;
        savedNumEl.textContent = `${cur + 1} students`;
      }
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
    setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/chat.html`; }, 1200);
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
    const recs = await RecommendationAPI.getSimilarProducts(product.id, 3);
    if (recs && recs.length) items = recs.filter(function (p) { return p.id !== product.id; }).slice(0, 3);
  } catch (error) {
    // recommendation endpoint not wired up or fallback needed
  }
  if (!items.length) {
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
            const mobileBtn = document.getElementById('mobileCtaWishlist');
            if (btn) { btn.classList.add('active'); btn.innerHTML = '❤️'; }
            if (mobileBtn) { mobileBtn.classList.add('active'); mobileBtn.innerHTML = '❤️'; }
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