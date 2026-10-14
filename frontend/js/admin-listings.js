let listingsType = 'properties';
let listingsStatus = '';
let listingsPage = 0;

async function initAdminListings() {
  listingsType = document.body.dataset.listings || 'properties';
  const isProps = listingsType === 'properties';
  const ok = await Dashboard.init({
    role: 'admin',
    active: isProps ? 'all-properties' : 'all-products',
    title: isProps ? 'All Properties' : 'All Products',
    subtitle: isProps ? 'Every property listing on the platform' : 'Every product listing on the platform'
  });
  if (!ok) return;
  loadListings();
}

function filterListings(status) {
  listingsStatus = status;
  listingsPage = 0;
  document.querySelectorAll('#statusTabs .tab').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.status === status);
  });
  loadListings();
}

async function loadListings() {
  const box = document.getElementById('listingsBox');
  const count = document.getElementById('listingCount');
  const pager = document.getElementById('listingsPagination');
  pager.innerHTML = '';
  renderListSkeleton(box, 3);
  try {
    const res = listingsType === 'properties'
      ? await AdminAPI.getProperties(listingsStatus, listingsPage, 10)
      : await AdminAPI.getProducts(listingsStatus, listingsPage, 10);
    const list = (res && res.content) || [];
    count.textContent = `${res.totalElements || 0} listing${(res.totalElements || 0) === 1 ? '' : 's'}`;
    if (!list.length) {
      renderInlineEmpty(box, '🗂️', 'No listings found for this filter');
      return;
    }
    box.innerHTML = list.map(listingsType === 'properties' ? adminPropertyRow : adminProductRow).join('');
    renderPagination(pager, res.page || 0, res.totalPages || 1, (p) => { listingsPage = p; loadListings(); });
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

function listingActions(id, status, detailHref) {
  const actions = [`<a href="${detailHref}" class="btn btn-secondary btn-sm" target="_blank">View</a>`];
  if (status !== 'APPROVED') {
    actions.push(`<button class="btn btn-success btn-sm" onclick="moderateListing(${id}, 'APPROVED')">Approve</button>`);
  }
  if (status !== 'REJECTED') {
    actions.push(`<button class="btn btn-danger btn-sm" onclick="moderateListing(${id}, 'REJECTED')">Reject</button>`);
  }
  return actions.join('');
}

function adminPropertyRow(p) {
  const image = getFirstImage(p.images);
  const poster = p.postedBy || {};
  const meta = [getPropertyTypeLabel(p.type)];
  if (p.area) meta.push(p.area);
  if (p.location && p.location.city) meta.push(p.location.city);
  return `<div class="list-row">
    <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '🏠'}</div>
    <div class="list-main">
      <div class="lr-title">${escapeHtml(p.title)}</div>
      <div class="lr-sub">${meta.join(' · ')} · ${formatPrice(p.pricePerMonth, 'RENT')}</div>
      <div class="lr-meta">By ${escapeHtml(poster.name || 'User')} · ${timeAgo(p.createdAt)}</div>
    </div>
    ${dashboardStatusBadge(p.status)}
    <div class="list-actions">${listingActions(p.id, p.status, `../../property-detail.html?id=${p.id}`)}</div>
  </div>`;
}

function adminProductRow(p) {
  const image = getFirstImage(p.images);
  const poster = p.postedBy || {};
  const meta = [];
  if (p.category) meta.push(p.category.name);
  if (p.area) meta.push(p.area);
  if (!p.area && p.location && p.location.city) meta.push(p.location.city);
  return `<div class="list-row">
    <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '📦'}</div>
    <div class="list-main">
      <div class="lr-title">${escapeHtml(p.title)}</div>
      <div class="lr-sub">${meta.join(' · ')} · ${formatPrice(p.price, p.listingType)}</div>
      <div class="lr-meta">By ${escapeHtml(poster.name || 'User')} · ${timeAgo(p.createdAt)}</div>
    </div>
    ${dashboardStatusBadge(p.status)}
    <div class="list-actions">${listingActions(p.id, p.status, `../../product-detail.html?id=${p.id}`)}</div>
  </div>`;
}

async function moderateListing(id, status) {
  if (status === 'REJECTED') {
    const confirmed = await showModal('Reject this listing? It will be hidden from users.', 'Reject Listing', 'Reject');
    if (!confirmed) return;
  }
  try {
    await AdminAPI.changeStatus(listingsType, id, status);
    showToast(status === 'APPROVED' ? 'Listing approved' : 'Listing rejected');
    loadListings();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initAdminListings);
