let pendingType = 'properties';
let pendingPage = 0;

async function initPending() {
  pendingType = document.body.dataset.pending || 'properties';
  const isProps = pendingType === 'properties';
  const ok = await Dashboard.init({
    role: 'admin',
    active: isProps ? 'pending-properties' : 'pending-products',
    title: isProps ? 'Pending Properties' : 'Pending Products',
    subtitle: isProps ? 'Review and moderate property listings' : 'Review and moderate product listings'
  });
  if (!ok) return;
  loadPending();
}

async function loadPending() {
  const box = document.getElementById('pendingBox');
  const count = document.getElementById('pendingCount');
  const pager = document.getElementById('pendingPagination');
  pager.innerHTML = '';
  renderListSkeleton(box, 3);
  try {
    const res = pendingType === 'properties'
      ? await AdminAPI.getPendingProperties(pendingPage, 10)
      : await AdminAPI.getPendingProducts(pendingPage, 10);
    const list = (res && res.content) || [];
    count.textContent = `${res.totalElements || 0} pending`;
    if (!list.length) {
      renderInlineEmpty(box, '✅', 'Nothing to moderate. All caught up!');
      return;
    }
    box.innerHTML = list.map(pendingType === 'properties' ? pendingPropertyRow : pendingProductRow).join('');
    renderPagination(pager, res.page || 0, res.totalPages || 1, (p) => { pendingPage = p; loadPending(); });
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

function pendingPropertyRow(p) {
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
    <div class="list-actions">
      <a href="../../property-detail.html?id=${p.id}" class="btn btn-secondary btn-sm" target="_blank">Review</a>
      <button class="btn btn-success btn-sm" onclick="approveListing(${p.id})">Approve</button>
      <button class="btn btn-danger btn-sm" onclick="rejectListing(${p.id})">Reject</button>
    </div>
  </div>`;
}

function pendingProductRow(p) {
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
    <div class="list-actions">
      <a href="../../product-detail.html?id=${p.id}" class="btn btn-secondary btn-sm" target="_blank">Review</a>
      <button class="btn btn-success btn-sm" onclick="approveListing(${p.id})">Approve</button>
      <button class="btn btn-danger btn-sm" onclick="rejectListing(${p.id})">Reject</button>
    </div>
  </div>`;
}

async function approveListing(id) {
  await moderate(id, 'APPROVED');
}

async function rejectListing(id) {
  const confirmed = await showModal('Reject this listing? It will not be visible to users.', 'Reject Listing', 'Reject');
  if (!confirmed) return;
  await moderate(id, 'REJECTED');
}

async function moderate(id, status) {
  try {
    await AdminAPI.changeStatus(pendingType, id, status);
    showToast(status === 'APPROVED' ? 'Listing approved' : 'Listing rejected');
    loadPending();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initPending);
