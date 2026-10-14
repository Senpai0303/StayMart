let bookingFilter = '';

async function initBookings() {
  const ok = await Dashboard.init({ role: 'user', active: 'bookings', title: 'My Bookings', subtitle: 'Booking requests you have sent' });
  if (!ok) return;
  loadBookings();
}

function filterBookings(status) {
  bookingFilter = status;
  document.querySelectorAll('#bookingTabs .tab').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.status === status);
  });
  loadBookings();
}

async function loadBookings() {
  const box = document.getElementById('bookingsBox');
  const count = document.getElementById('bookingCount');
  renderListSkeleton(box, 3);
  try {
    const res = await BookingAPI.getMy();
    let list = (res && res.content) || [];
    if (bookingFilter) list = list.filter((b) => b.status === bookingFilter);
    count.textContent = `${list.length} booking${list.length === 1 ? '' : 's'}`;
    if (!list.length) {
      renderInlineEmpty(box, '📅', bookingFilter ? `No ${bookingFilter.toLowerCase()} bookings` : 'You have not booked anything yet',
        '<a href="../../search-properties.html" class="btn btn-primary btn-sm">Browse PGs</a>');
      return;
    }
    box.innerHTML = list.map(bookingRow).join('');
  } catch (error) {
    renderInlineEmpty(box, '⚠️', error.message);
  }
}

function bookingRow(b) {
  const property = b.property || {};
  const image = getFirstImage(property.images);
  const canCancel = b.status === 'PENDING' || b.status === 'CONFIRMED';
  const room = b.room ? `Room #${b.room.roomNumber || b.room.id}` : '';
  return `<div class="list-row">
    <div class="list-thumb">${image ? `<img src="${escapeHtml(image)}" alt="" style="width:100%;height:100%;object-fit:cover;border-radius:12px"/>` : '🏠'}</div>
    <div class="list-main">
      <div class="lr-title">${escapeHtml(property.title || 'Property')}</div>
      <div class="lr-sub">${formatDate(b.checkIn)} → ${formatDate(b.checkOut)}${room ? ' · ' + escapeHtml(room) : ''}${b.months ? ' · ' + b.months + ' month(s)' : ''}</div>
      <div class="lr-meta">Requested ${timeAgo(b.createdAt)}${b.totalAmount ? ' · Total ' + formatPrice(b.totalAmount) : ''}</div>
    </div>
    ${dashboardStatusBadge(b.status)}
    <div class="list-actions">
      ${property.id ? `<a href="../../property-detail.html?id=${property.id}" class="btn btn-secondary btn-sm">View</a>` : ''}
      ${canCancel ? `<button class="btn btn-danger btn-sm" onclick="cancelBooking(${b.id})">Cancel</button>` : ''}
    </div>
  </div>`;
}

async function cancelBooking(id) {
  const confirmed = await showModal('Cancel this booking request?', 'Cancel Booking', 'Yes, cancel');
  if (!confirmed) return;
  try {
    await BookingAPI.updateStatus(id, 'CANCELLED');
    showToast('Booking cancelled');
    loadBookings();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initBookings);
