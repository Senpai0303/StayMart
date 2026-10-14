let property = null;
let currentUserId = null;
let galleryImages = [];
let galleryIndex = 0;
let selectedRoomId = null;
let isInWishlist = false;
const monthOptions = [1, 2, 3, 4, 6, 8, 9, 12];
const propertyId = new URLSearchParams(window.location.search).get('id');

async function loadProperty() {
  const root = document.getElementById('detailRoot');
  if (!propertyId) {
    renderError(root, 'No property selected.');
    return;
  }
  try {
    property = await PropertyAPI.getById(propertyId);
  } catch (error) {
    renderError(root, error.message || 'This property could not be found.');
    return;
  }
  logBehavior('VIEW', 'PROPERTY', property.id, null, property.location && property.location.city);
  document.title = `${property.title} - StayMart`;
  galleryImages = Array.isArray(property.images) ? property.images.filter(Boolean) : [];
  renderDetail(root);
  loadReviews();
  loadSimilar();
  loadBookingRooms();
}

function renderError(root, message) {
  root.innerHTML = `
    <div class="not-found">
      <h1>404</h1>
      <p>${escapeHtml(message)}</p>
      <a href="search-properties.html" class="btn btn-primary">Browse Properties</a>
    </div>
  `;
}

function renderDetail(root) {
  if (!galleryImages.length) galleryImages = [null];
  const postedBy = property.postedBy || {};
  const locationText = [property.area, property.location && property.location.city]
    .filter(Boolean).join(', ');
  const isOwner = currentUserId && postedBy.id === currentUserId;

  root.innerHTML = `
    <section class="detail-layout">
      <div>
        <div class="gallery">
          <div class="gallery-main" onclick="openLightbox(${galleryIndex})">
            ${galleryImages[0]
              ? `<img id="mainGalleryImg" src="${escapeHtml(galleryImages[0])}" alt="${escapeHtml(property.title)}"/>`
              : `<div class="img-fallback" id="mainGalleryImg">🏠</div>`}
          </div>
          <div class="gallery-thumbs">
            ${galleryImages.map(function (img, i) {
              return img
                ? `<img src="${escapeHtml(img)}" class="${i === 0 ? 'active' : ''}" onclick="switchGallery(${i})" alt="Image ${i + 1}"/>`
                : `<div class="img-fallback" style="border-radius:8px" onclick="switchGallery(${i})">🏠</div>`;
            }).join('')}
          </div>
        </div>

        <div style="position:relative">
          <span class="badge ${getTypeBadgeClass(property.type)}" style="margin-bottom:10px">${getPropertyTypeLabel(property.type)}</span>
          ${property.genderPreference && property.genderPreference !== 'ANY' ? `<span class="badge badge-both" style="margin-bottom:10px">${getGenderLabel(property.genderPreference)}</span>` : ''}
          ${property.isAvailable ? '<span class="badge badge-approved" style="margin-bottom:10px">● Available</span>' : '<span class="badge badge-rejected" style="margin-bottom:10px">● Occupied</span>'}
          <button id="wishlistBtn" class="wishlist-btn" onclick="toggleWishlist(event)" title="Save to wishlist">♡</button>
        </div>

        <h1 class="detail-title" style="margin-top:10px">${escapeHtml(property.title)}</h1>

        <div class="detail-meta">
          ${locationText ? `<span class="meta-item">📍 ${escapeHtml(locationText)}</span>` : ''}
          <span class="meta-item">👁️ Listed ${timeAgo(property.createdAt)}</span>
          <span class="meta-item"><span id="inplaceStars"></span></span>
        </div>

        <div class="info-cards">
          <div class="info-card"><span class="info-icon">🛏️</span><div class="info-value">${property.availableRooms ?? property.totalRooms ?? 0} / ${property.totalRooms || 0}</div><div class="info-label">Rooms Available</div></div>
          <div class="info-card"><span class="info-icon">👥</span><div class="info-value">${getGenderLabel(property.genderPreference || 'ANY')}</div><div class="info-label">Preferred</div></div>
          <div class="info-card"><span class="info-icon">🔑</span><div class="info-value">${formatPrice(property.depositAmount)}</div><div class="info-label">Deposit</div></div>
          <div class="info-card"><span class="info-icon">📷</span><div class="info-value">${galleryImages.length}</div><div class="info-label">Photos</div></div>
        </div>

        <h2 class="section-title" style="font-size:20px;margin-bottom:14px">Facilities</h2>
        <div class="amenities-grid" id="amenitiesGrid"></div>

        <h2 class="section-title" style="font-size:20px;margin:28px 0 14px">About this ${getPropertyTypeLabel(property.type).toLowerCase()}</h2>
        <p class="text-secondary-text" style="white-space:pre-line">${escapeHtml(property.description || 'No description provided.')}</p>
        ${property.address ? `<p class="text-muted-text" style="margin-top:12px">📮 ${escapeHtml(property.address)}</p>` : ''}

        <div class="section" style="padding-top:40px">
          <div class="reviews-header containerless" id="reviewsHeader"></div>
          <div id="reviewsList"></div>
          <div id="reviewFormWrap"></div>
        </div>

        <div class="section" style="padding-top:0">
          <div class="section-header">
            <h2 class="section-title">Similar Properties</h2>
            <a class="section-link" href="search-properties.html">View more →</a>
          </div>
          <div id="similarGrid" class="grid-3"></div>
        </div>
      </div>

      <aside class="sidebar-sticky">
        <div class="poster-card" style="margin-bottom:16px">
          <div class="avatar">${postedBy.profilePic
            ? `<img src="${escapeHtml(postedBy.profilePic)}" alt=""/>`
            : escapeHtml(((postedBy.name || 'U')[0] || 'U').toUpperCase())}</div>
          <div style="min-width:0">
            <div class="poster-name">${escapeHtml(postedBy.name || 'Owner')}</div>
            <div class="poster-info">${escapeHtml(postedBy.city || 'Uttarakhand')}${postedBy.isVerified ? ' · ✅ Verified' : ''}</div>
          </div>
        </div>

        <div class="action-card">
          <div class="action-price">${formatPrice(property.pricePerMonth, 'RENT')}</div>

          ${isOwner ? `
            <div class="safety-tip">👋 This is your own listing. Manage its status from <strong>My Listings</strong>.</div>
          ` : `
            ${property.isAvailable ? `
            <div class="input-group">
              <label for="roomSelect">Choose room</label>
              <select id="roomSelect"><option value="">Any room</option></select>
            </div>
            <div class="input-group">
              <label for="monthsSelect">Staying for (Months)</label>
              <select id="monthsSelect">${monthOptions.map(function (m) { return `<option value="${m}">${m} month${m > 1 ? 's' : ''}</option>`; }).join('')}</select>
            </div>
            <div class="input-group">
              <label for="bookingMessage">Message to owner<span class="text-muted-text"> (optional)</span></label>
              <textarea id="bookingMessage" rows="2" placeholder="e.g. I'm a 3rd year student at Doon University, looking for a quiet room." maxlength="300"></textarea>
            </div>
            <div class="total-display">
              <span class="total-label">Total rent</span>
              <span class="total-value" id="totalRent">—</span>
            </div>
            <button class="btn btn-primary btn-block" onclick="bookProperty()">Book This Property</button>
            ` : `
            <div class="safety-tip">😔 This property is currently occupied. Check back soon or browse similar listings.</div>
            `}
            <div class="safety-tip" style="margin-top:16px">🛡️ <strong>Safety Tip:</strong> Never pay an advance or deposit before visiting the property in person. All payments happen directly between you and the owner.</div>
          `}
        </div>

        ${!isOwner ? `
        <button class="btn btn-secondary btn-block mt-8" onclick="contactOwner()">💬 Message Owner</button>
        ` : ''}
        ${postedBy.phone ? `
        <a class="btn btn-success btn-block mt-8" href="tel:+91${escapeHtml(postedBy.phone)}">📞 Call +91 ${escapeHtml(postedBy.phone)}</a>
        ` : ''}
      </aside>
    </section>
  `;
}

function renderAmenities() {
  const grid = document.getElementById('amenitiesGrid');
  if (!grid) return;
  if (!Array.isArray(property.amenities) || !property.amenities.length) {
    grid.innerHTML = '<div class="text-muted-text">No facilities listed.</div>';
    return;
  }
  grid.innerHTML = property.amenities.map(function (a) {
    return `<div class="amenity-item"><span class="amenity-icon">${getIcon(a)}</span>${escapeHtml(a)}</div>`;
  }).join('');
}

async function loadBookingRooms() {
  const select = document.getElementById('roomSelect');
  if (!select) return;
  try {
    const rooms = await PropertyAPI.getRooms(property.id);
    const available = rooms.filter(function (r) { return r.isAvailable !== false; });
    if (available.length) {
      available.forEach(function (room) {
        select.insertAdjacentHTML('beforeend', `<option value="${room.id}">Room ${escapeHtml(room.roomNumber || room.name || room.id)} · ₹${room.pricePerMonth}/mo · ${room.capacity || 1} bed</option>`);
      });
    }
    select.addEventListener('change', updateTotal);
  } catch (error) {
    // rooms endpoint unavailable -> booking without a specific room
  }
  updateTotal();
}

function updateTotal() {
  const select = document.getElementById('monthsSelect');
  const roomSelect = document.getElementById('roomSelect');
  if (!select) return;
  const months = Number(select.value);
  const totalEl = document.getElementById('totalRent');
  if (!totalEl) return;
  totalEl.textContent = formatPrice(Number(property.pricePerMonth) * months, 'RENT');
}

async function bookProperty() {
  if (!Auth.isLoggedIn()) {
    showToast('Please login to book this property.', 'info');
    setTimeout(function () { window.location.href = 'login.html'; }, 1200);
    return;
  }
  const months = Number(document.getElementById('monthsSelect').value);
  const message = document.getElementById('bookingMessage') ? document.getElementById('bookingMessage').value.trim() : '';
  const roomId = document.getElementById('roomSelect') && document.getElementById('roomSelect').value ? Number(document.getElementById('roomSelect').value) : null;
  const checkIn = new Date();
  const body = {
    propertyId: property.id,
    roomId,
    months,
    checkIn: toLocalDate(checkIn),
    message
  };
  try {
    const booking = await BookingAPI.create(body);
    logBehavior('BOOK', 'PROPERTY', property.id, null, null);
    showToast('Booking request sent to the owner. 🎉', 'success');
    setTimeout(function () { window.location.href = `${depthPrefix()}pages/user/my-bookings.html`; }, 1200);
  } catch (error) {
    await showModal(error.message || 'Booking failed.', 'Booking failed', 'Try again');
  }
}

async function toggleWishlist(event) {
  event.stopPropagation();
  if (!Auth.isLoggedIn()) {
    showToast('Please login to save listings.', 'info');
    setTimeout(function () { window.location.href = 'login.html'; }, 1200);
    return;
  }
  const btn = document.getElementById('wishlistBtn');
  try {
    if (isInWishlist) {
      await WishlistAPI.remove('PROPERTY', property.id);
      isInWishlist = false;
      btn.classList.remove('active');
      btn.innerHTML = '♡';
      logBehavior('WISHLIST', 'PROPERTY', property.id, null, null);
      showToast('Removed from wishlist.', 'info');
    } else {
      await WishlistAPI.add('PROPERTY', property.id);
      isInWishlist = true;
      btn.classList.add('active');
      btn.innerHTML = '❤️';
      logBehavior('WISHLIST', 'PROPERTY', property.id, null, null);
      showToast('Saved to your wishlist! ❤️', 'success');
    }
  } catch (error) {
    showToast(error.message || 'Could not update wishlist.', 'error');
  }
}

async function contactOwner() {
  const postedBy = property.postedBy || {};
  if (!postedBy.id) return;
  if (!Auth.isLoggedIn()) {
    showToast('Please login to message the owner.', 'info');
    setTimeout(function () { window.location.href = 'login.html'; }, 1200);
    return;
  }
  try {
    await ChatAPI.send({
      receiverId: postedBy.id,
      listingType: 'PROPERTY',
      listingId: property.id,
      message: `Hi! I'm interested in "${property.title}".`
    });
    logBehavior('CONTACT', 'PROPERTY', property.id, null, null);
    showToast('Message sent! The owner will reply in your Chats. 💬', 'success');
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
    summary = await ReviewAPI.getSummary('PROPERTY', property.id);
  } catch (error) {
    // summary endpoint may be unavailable; fall through to list
  }
  header.innerHTML = `
    <div class="reviews-avg">
      <div class="big">${summary.averageRating ? Number(summary.averageRating).toFixed(1) : '—'}</div>
      <div class="sub">${summary.count || 0} review${(summary.count || 0) === 1 ? '' : 's'}</div>
    </div>
    <div class="review-bars">${renderReviewBars(summary.count || 0)}</div>
  `;
  try {
    const page = await ReviewAPI.getByItem('PROPERTY', property.id, 0, 5);
    const reviews = page.content || [];
    if (reviews.length) {
      list.innerHTML = reviews.map(renderReviewCard).join('');
    } else {
      list.innerHTML = '<div class="empty-state" style="padding:24px"><span class="empty-icon">💬</span><p>No reviews yet — be the first to share your stay experience.</p></div>';
    }
  } catch (error) {
    list.innerHTML = '<div class="text-muted-text">Reviews are loading…</div>';
  }
  const wrap = document.getElementById('reviewFormWrap');
  if (Auth.isLoggedIn() && !(property.postedBy && property.postedBy.id === currentUserId)) {
    wrap.innerHTML = `
      <div class="card" style="padding:22px;margin-top:16px">
        <h3 style="font-size:17px;font-weight:700;margin-bottom:14px">✍️ Write a Review</h3>
        <div class="star-rating" style="margin-bottom:12px" id="reviewStars"></div>
        <div class="input-group">
          <textarea id="reviewComment" rows="3" placeholder="How was your stay? Share the experience to help others." maxlength="500"></textarea>
        </div>
        <button class="btn btn-primary" onclick="submitReview()">Submit Review</button>
      </div>
    `;
    renderStarInput();
  }
}

function renderReviewBars(count) {
  let html = '';
  [5, 4, 3, 2, 1].forEach(function (star) {
    html += `
      <div class="review-bar-row"><span>${star}★</span><div class="review-bar-track"><div class="review-bar-fill" style="width:0%"></div></div></div>
    `;
  });
  return html;
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
  box.style.cursor = 'pointer';
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
    await ReviewAPI.add({ itemType: 'PROPERTY', itemId: property.id, rating: window.__reviewRating, comment });
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
    const recs = await RecommendationAPI.getSimilarProperties(property.id, 3);
    if (recs && recs.length) items = recs;
  } catch (error) {
    // recommendation endpoint not wired up yet -> fall back to same-city listings
  }
  if (!items.length) {
    try {
      const city = property.location && property.location.city;
      const page = await PropertyAPI.getAll({ city: city || '', page: 0, size: 6 });
      items = (page.content || []).filter(function (p) { return p.id !== property.id; }).slice(0, 3);
    } catch (error) {
      grid.innerHTML = '';
      return;
    }
  }
  grid.innerHTML = items.map(buildPropertyCard).join('') || '<div class="text-muted-text">No similar properties right now.</div>';
}

function switchGallery(index) {
  galleryIndex = index;
  const main = document.getElementById('mainGalleryImg');
  if (main && galleryImages[index]) {
    main.src = galleryImages[index];
    main.className = '';
  }
  document.querySelectorAll('.gallery-thumbs img, .gallery-thumbs .img-fallback').forEach(function (thumb, i) {
    thumb.classList.toggle('active', i === index);
  });
}

function openLightbox(index) {
  if (!galleryImages.length || !galleryImages[index]) return;
  galleryIndex = index;
  document.getElementById('lightboxImg').src = galleryImages[index];
  document.getElementById('lightbox').classList.add('open');
}

function lightboxMove(step) {
  galleryIndex = (galleryIndex + step + galleryImages.length) % galleryImages.length;
  if (!galleryImages[galleryIndex]) { lightboxMove(step); return; }
  document.getElementById('lightboxImg').src = galleryImages[galleryIndex];
}

function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
}

document.getElementById('lightbox').addEventListener('click', function (event) {
  if (event.target === this) closeLightbox();
});

window.addEventListener('keydown', function (event) {
  if (!document.getElementById('lightbox').classList.contains('open')) return;
  if (event.key === 'Escape') closeLightbox();
  if (event.key === 'ArrowLeft') lightboxMove(-1);
  if (event.key === 'ArrowRight') lightboxMove(1);
});

document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    currentUserId = Auth.isLoggedIn() ? Auth.user.id : null;
    loadProperty().then(function () {
      renderAmenities();
      preloadInplaceRating();
      if (currentUserId) {
        WishlistAPI.check('PROPERTY', propertyId).then(function (result) {
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

async function preloadInplaceRating() {
  const el = document.getElementById('inplaceStars');
  if (!el) return;
  try {
    const summary = await ReviewAPI.getSummary('PROPERTY', property.id);
    if (summary.count) {
      el.innerHTML = renderStars(summary.averageRating) + `<span class="rating-value">${summary.count} review${summary.count === 1 ? '' : 's'}</span>`;
    } else {
      el.innerHTML = '<span class="badge badge-new">New listing</span>';
    }
  } catch (error) {
    el.innerHTML = '';
  }
}