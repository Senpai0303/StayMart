async function initWishlist() {
  const ok = await Dashboard.init({ role: 'user', active: 'wishlist', title: 'Wishlist', subtitle: 'Your saved properties and products' });
  if (!ok) return;
  loadWishlist();
}

async function loadWishlist() {
  const box = document.getElementById('wishlistBox');
  const count = document.getElementById('wishCount');
  renderListSkeleton(box, 3);
  try {
    const items = await WishlistAPI.getAll();
    const list = Array.isArray(items) ? items : [];
    count.textContent = `${list.length} item${list.length === 1 ? '' : 's'}`;
    if (!list.length) {
      renderInlineEmpty(box, '❤️', 'Your wishlist is empty',
        '<a href="../../search-properties.html" class="btn btn-primary btn-sm">Discover listings</a>');
      return;
    }
    box.innerHTML = `<div class="grid-4" style="padding:22px">${list.map(wishlistCard).join('')}</div>`;
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

function wishlistCard(item) {
  const isProperty = item.itemType === 'PROPERTY';
  const href = isProperty
    ? `../../property-detail.html?id=${item.itemId}`
    : `../../product-detail.html?id=${item.itemId}`;
  const imageHtml = item.image
    ? `<img class="card-img" src="${escapeHtml(item.image)}" alt="${escapeHtml(item.title)}" loading="lazy"/>`
    : `<div class="card-img flex-center" style="font-size:44px;background:var(--gradient-card)">${isProperty ? '🏠' : '📦'}</div>`;
  return `<div class="card">
    <div class="card-img-wrapper" style="position:relative">${imageHtml}</div>
    <div class="card-body">
      <div class="card-title">${escapeHtml(item.title || (isProperty ? 'Property' : 'Product'))}</div>
      <div class="small-number-row"><span class="badge ${isProperty ? 'badge-pg' : 'badge-sell'}">${isProperty ? 'Property' : 'Product'}</span></div>
      <div class="card-footer">
        <div class="card-price">${formatPrice(item.price, isProperty ? 'RENT' : 'SELL')}</div>
      </div>
      <div style="display:flex;gap:8px;margin-top:12px">
        <a href="${href}" class="btn btn-secondary btn-sm" style="flex:1">View</a>
        <button class="btn btn-danger btn-sm" onclick="removeWishlist('${item.itemType}', ${item.itemId})">Remove</button>
      </div>
    </div>
  </div>`;
}

async function removeWishlist(itemType, itemId) {
  try {
    await WishlistAPI.remove(itemType, itemId);
    showToast('Removed from wishlist');
    loadWishlist();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initWishlist);
