let listingTab = 'properties';
let listingPage = 0;

async function initMyListings() {
  const ok = await Dashboard.init({ role: 'user', active: 'my-listings', title: 'My Listings', subtitle: 'Manage your properties and products' });
  if (!ok) return;
  loadListings();
}

function switchListingTab(tab) {
  if (listingTab === tab) return;
  listingTab = tab;
  listingPage = 0;
  document.querySelectorAll('.tabs .tab').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  document.getElementById('listPanelTitle').textContent = tab === 'properties' ? 'My Properties' : 'My Products';
  loadListings();
}

async function loadListings() {
  const box = document.getElementById('listingsBox');
  const count = document.getElementById('listCount');
  const pager = document.getElementById('listingsPagination');
  pager.innerHTML = '';
  renderListSkeleton(box, 3);
  try {
    const res = listingTab === 'properties'
      ? await UserAPI.getMyProperties(listingPage, 10)
      : await UserAPI.getMyProducts(listingPage, 10);
    const list = (res && res.content) || [];
    count.textContent = `${res.totalElements || 0} listing${(res.totalElements || 0) === 1 ? '' : 's'}`;
    if (!list.length) {
      renderInlineEmpty(box, listingTab === 'properties' ? '🏠' : '📦',
        `You haven't posted any ${listingTab} yet`,
        `<a href="../../post-${listingTab === 'properties' ? 'property' : 'product'}.html" class="btn btn-primary btn-sm">Create one</a>`);
      return;
    }
    box.innerHTML = list.map(listingTab === 'properties' ? propertyRow : productRow).join('');
    renderPagination(pager, res.page || 0, res.totalPages || 1, (p) => { listingPage = p; loadListings(); });
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

function propertyRow(p) {
  const image = getFirstImage(p.images);
  const meta = [getPropertyTypeLabel(p.type)];
  if (p.area) meta.push(p.area);
  if (p.location && p.location.city) meta.push(p.location.city);
  return `<div class="list-row">
    <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '🏠'}</div>
    <div class="list-main">
      <div class="lr-title">${escapeHtml(p.title)}</div>
      <div class="lr-sub">${meta.join(' · ')}</div>
      <div class="lr-meta">Posted ${timeAgo(p.createdAt)}</div>
    </div>
    <div class="list-price">${formatPrice(p.pricePerMonth, 'RENT')}</div>
    ${dashboardStatusBadge(p.status)}
    <div class="list-actions">
      <a href="../../property-detail.html?id=${p.id}" class="btn btn-secondary btn-sm">View</a>
      <button class="btn btn-danger btn-sm" onclick="deleteProperty(${p.id})">Delete</button>
    </div>
  </div>`;
}

function productRow(p) {
  const image = getFirstImage(p.images);
  const meta = [];
  if (p.category) meta.push(p.category.name);
  if (p.area) meta.push(p.area);
  if (!p.area && p.location && p.location.city) meta.push(p.location.city);
  return `<div class="list-row">
    <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '📦'}</div>
    <div class="list-main">
      <div class="lr-title">${escapeHtml(p.title)}</div>
      <div class="lr-sub">${meta.join(' · ')}</div>
      <div class="lr-meta">Posted ${timeAgo(p.createdAt)}</div>
    </div>
    <div class="list-price">${formatPrice(p.price, p.listingType)}</div>
    ${dashboardStatusBadge(p.status)}
    <div class="list-actions">
      <a href="../../product-detail.html?id=${p.id}" class="btn btn-secondary btn-sm">View</a>
      <button class="btn btn-danger btn-sm" onclick="deleteProduct(${p.id})">Delete</button>
    </div>
  </div>`;
}

async function deleteProperty(id) {
  const confirmed = await showModal('Delete this property listing? This cannot be undone.', 'Delete Property', 'Delete');
  if (!confirmed) return;
  try {
    await PropertyAPI.delete(id);
    showToast('Property deleted');
    loadListings();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

async function deleteProduct(id) {
  const confirmed = await showModal('Delete this product listing? This cannot be undone.', 'Delete Product', 'Delete');
  if (!confirmed) return;
  try {
    await ProductAPI.delete(id);
    showToast('Product deleted');
    loadListings();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initMyListings);
