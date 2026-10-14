let requestTab = 'bookings';

async function initRequests() {
  const ok = await Dashboard.init({ role: 'user', active: 'requests-received', title: 'Requests Received', subtitle: 'Booking and order requests on your listings' });
  if (!ok) return;
  loadRequests();
}

function switchRequestTab(tab) {
  if (requestTab === tab) return;
  requestTab = tab;
  document.querySelectorAll('.tabs .tab').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  document.getElementById('reqPanelTitle').textContent = tab === 'bookings' ? 'Incoming Bookings' : 'Incoming Orders';
  loadRequests();
}

async function loadRequests() {
  const box = document.getElementById('requestsBox');
  const count = document.getElementById('reqCount');
  renderListSkeleton(box, 3);
  try {
    if (requestTab === 'bookings') {
      const res = await BookingAPI.getReceived();
      const list = (res && res.content) || [];
      count.textContent = `${list.length} request${list.length === 1 ? '' : 's'}`;
      if (!list.length) {
        renderInlineEmpty(box, '📅', 'No booking requests received yet');
        return;
      }
      box.innerHTML = list.map(incomingBookingRow).join('');
    } else {
      const res = await OrderAPI.getReceived();
      const list = (res && res.content) || [];
      count.textContent = `${list.length} request${list.length === 1 ? '' : 's'}`;
      if (!list.length) {
        renderInlineEmpty(box, '📦', 'No order requests received yet');
        return;
      }
      box.innerHTML = list.map(incomingOrderRow).join('');
    }
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

function incomingBookingRow(b) {
  const booker = b.booker || {};
  const property = b.property || {};
  const image = getFirstImage(property.images);
  const actions = statusActions('booking', b.id, b.status);
  return `<div class="list-row">
    <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '🏠'}</div>
    <div class="list-main">
      <div class="lr-title">${escapeHtml(booker.name || 'User')} · ${escapeHtml(property.title || 'Property')}</div>
      <div class="lr-sub">${formatDate(b.checkIn)} → ${formatDate(b.checkOut)}${b.months ? ' · ' + b.months + ' month(s)' : ''}${b.totalAmount ? ' · ' + formatPrice(b.totalAmount) : ''}</div>
      <div class="lr-meta">${booker.phone ? '📞 ' + escapeHtml(booker.phone) + ' · ' : ''}${timeAgo(b.createdAt)}</div>
    </div>
    ${dashboardStatusBadge(b.status)}
    <div class="list-actions">${actions}</div>
  </div>`;
}

function incomingOrderRow(o) {
  const buyer = o.buyer || {};
  const product = o.product || {};
  const image = getFirstImage(product.images);
  const actions = statusActions('order', o.id, o.status);
  const period = o.orderType === 'RENT' && o.rentStart ? ` · ${formatDate(o.rentStart)} → ${formatDate(o.rentEnd)}` : '';
  return `<div class="list-row">
    <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '📦'}</div>
    <div class="list-main">
      <div class="lr-title">${escapeHtml(buyer.name || 'User')} · ${escapeHtml(product.title || 'Product')}</div>
      <div class="lr-sub">Qty ${o.quantity || 1} · ${formatPrice(o.amount, o.orderType === 'RENT' ? 'RENT' : 'SELL')}${period}</div>
      <div class="lr-meta">${buyer.phone ? '📞 ' + escapeHtml(buyer.phone) + ' · ' : ''}${timeAgo(o.createdAt)}</div>
    </div>
    ${dashboardStatusBadge(o.status)}
    <div class="list-actions">${actions}</div>
  </div>`;
}

function statusActions(kind, id, status) {
  const buttons = [];
  if (status === 'PENDING') {
    buttons.push(`<button class="btn btn-success btn-sm" onclick="updateRequest('${kind}', ${id}, 'CONFIRMED')">Confirm</button>`);
    buttons.push(`<button class="btn btn-danger btn-sm" onclick="updateRequest('${kind}', ${id}, 'CANCELLED')">Reject</button>`);
  } else if (status === 'CONFIRMED') {
    buttons.push(`<button class="btn btn-primary btn-sm" onclick="updateRequest('${kind}', ${id}, 'COMPLETED')">Mark Complete</button>`);
    buttons.push(`<button class="btn btn-danger btn-sm" onclick="updateRequest('${kind}', ${id}, 'CANCELLED')">Cancel</button>`);
  }
  return buttons.join('');
}

async function updateRequest(kind, id, status) {
  try {
    if (kind === 'booking') {
      await BookingAPI.updateStatus(id, status);
    } else {
      await OrderAPI.updateStatus(id, status);
    }
    showToast('Request updated');
    loadRequests();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initRequests);
