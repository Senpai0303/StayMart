let orderFilter = '';

async function initOrders() {
  const ok = await Dashboard.init({ role: 'user', active: 'orders', title: 'My Orders', subtitle: 'Purchases and rentals you have ordered' });
  if (!ok) return;
  loadOrders();
}

function filterOrders(status) {
  orderFilter = status;
  document.querySelectorAll('#orderTabs .tab').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.status === status);
  });
  loadOrders();
}

async function loadOrders() {
  const box = document.getElementById('ordersBox');
  const count = document.getElementById('orderCount');
  renderListSkeleton(box, 3);
  try {
    const res = await OrderAPI.getMy();
    let list = (res && res.content) || [];
    if (orderFilter) list = list.filter((o) => o.status === orderFilter);
    count.textContent = `${list.length} order${list.length === 1 ? '' : 's'}`;
    if (!list.length) {
      renderInlineEmpty(box, '📦', orderFilter ? `No ${orderFilter.toLowerCase()} orders` : 'You have not ordered anything yet',
        '<a href="../../search-products.html" class="btn btn-primary btn-sm">Browse products</a>');
      return;
    }
    box.innerHTML = list.map(orderRow).join('');
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

function orderRow(o) {
  const product = o.product || {};
  const image = getFirstImage(product.images);
  const canCancel = o.status === 'PENDING' || o.status === 'CONFIRMED';
  const period = o.orderType === 'RENT' && o.rentStart ? ` · ${formatDate(o.rentStart)} → ${formatDate(o.rentEnd)}` : '';
  const seller = o.seller ? `Seller: ${o.seller.name}` : '';
  return `<div class="list-row">
    <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '📦'}</div>
    <div class="list-main">
      <div class="lr-title">${escapeHtml(product.title || 'Product')}</div>
      <div class="lr-sub">Qty ${o.quantity || 1} · ${formatPrice(o.amount, o.orderType === 'RENT' ? 'RENT' : 'SELL')}${period}</div>
      <div class="lr-meta">${escapeHtml(seller)} · Ordered ${timeAgo(o.createdAt)}</div>
    </div>
    ${dashboardStatusBadge(o.status)}
    <div class="list-actions">
      ${product.id ? `<a href="../../product-detail.html?id=${product.id}" class="btn btn-secondary btn-sm">View</a>` : ''}
      ${canCancel ? `<button class="btn btn-danger btn-sm" onclick="cancelOrder(${o.id})">Cancel</button>` : ''}
    </div>
  </div>`;
}

async function cancelOrder(id) {
  const confirmed = await showModal('Cancel this order?', 'Cancel Order', 'Yes, cancel');
  if (!confirmed) return;
  try {
    await OrderAPI.updateStatus(id, 'CANCELLED');
    showToast('Order cancelled');
    loadOrders();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initOrders);
