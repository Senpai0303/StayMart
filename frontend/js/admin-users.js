let usersPage = 0;
let usersCache = [];
let currentAdminId = null;

async function initAdminUsers() {
  const ok = await Dashboard.init({ role: 'admin', active: 'all-users', title: 'All Users', subtitle: 'Manage platform accounts' });
  if (!ok) return;
  currentAdminId = (Dashboard.currentUser() || {}).id;
  loadUsers();
}

async function loadUsers() {
  const body = document.getElementById('usersBody');
  const count = document.getElementById('userCount');
  const pager = document.getElementById('usersPagination');
  pager.innerHTML = '';
  body.innerHTML = '<tr><td colspan="7" class="inline-empty">Loading…</td></tr>';
  try {
    const res = await AdminAPI.getAllUsers(usersPage, 15);
    usersCache = (res && res.content) || [];
    count.textContent = `${res.totalElements || 0} users`;
    renderUsers(usersCache);
    renderPagination(pager, res.page || 0, res.totalPages || 1, (p) => { usersPage = p; loadUsers(); });
  } catch (error) {
    body.innerHTML = `<tr><td colspan="7" class="inline-empty">${escapeHtml(error.message)}</td></tr>`;
  }
}

function filterUsers() {
  const q = document.getElementById('userSearch').value.trim().toLowerCase();
  if (!q) {
    renderUsers(usersCache);
    return;
  }
  const filtered = usersCache.filter((u) =>
    (u.name || '').toLowerCase().includes(q) || (u.email || '').toLowerCase().includes(q));
  renderUsers(filtered);
}

function renderUsers(users) {
  const body = document.getElementById('usersBody');
  if (!users.length) {
    body.innerHTML = '<tr><td colspan="7" class="inline-empty">No users found</td></tr>';
    return;
  }
  body.innerHTML = users.map((u) => {
    const isSelf = String(u.id) === String(currentAdminId);
    const active = u.isActive !== false;
    const status = active
      ? '<span class="badge badge-approved">Active</span>'
      : '<span class="badge badge-rejected">Inactive</span>';
    const verified = u.isVerified ? ' <span class="badge badge-new">✔</span>' : '';
    return `<tr>
      <td>
        <div style="display:flex;align-items:center;gap:10px">
          ${dashboardAvatar(u)}
          <div>
            <div style="font-weight:600">${escapeHtml(u.name || 'User')}${verified}</div>
            <div style="font-size:12px;color:var(--text-muted)">#${u.id}</div>
          </div>
        </div>
      </td>
      <td>
        <div>${escapeHtml(u.email || '')}</div>
        <div style="font-size:12px;color:var(--text-muted)">${escapeHtml(u.phone || '—')}</div>
      </td>
      <td>${escapeHtml([u.city, u.state].filter(Boolean).join(', ') || '—')}</td>
      <td><span class="badge ${u.role === 'ADMIN' ? 'badge-pg' : 'badge-used'}">${escapeHtml(u.role || 'USER')}</span></td>
      <td>${status}</td>
      <td>${formatDate(u.createdAt)}</td>
      <td>
        <div class="list-actions">
          <button class="btn btn-secondary btn-sm" onclick="toggleUser(${u.id}, ${active})">${active ? 'Deactivate' : 'Activate'}</button>
          ${isSelf ? '' : `<button class="btn btn-danger btn-sm" onclick="deleteUser(${u.id})">Delete</button>`}
        </div>
      </td>
    </tr>`;
  }).join('');
}

async function toggleUser(id, isActive) {
  try {
    await AdminAPI.toggleUserStatus(id, !isActive);
    showToast(isActive ? 'User deactivated' : 'User activated');
    loadUsers();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

async function deleteUser(id) {
  const confirmed = await showModal('Delete this user? This only works if they have no listings.', 'Delete User', 'Delete');
  if (!confirmed) return;
  try {
    await AdminAPI.deleteUser(id);
    showToast('User deleted');
    loadUsers();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initAdminUsers);
