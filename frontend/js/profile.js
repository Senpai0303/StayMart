let profileUser = {};

async function initProfile() {
  const ok = await Dashboard.init({ role: 'user', active: 'profile', title: 'My Profile', subtitle: 'Manage your account details and security' });
  if (!ok) return;
  try {
    profileUser = await UserAPI.getMe();
  } catch (error) {
    profileUser = Dashboard.currentUser();
  }
  renderProfileHead();
  fillProfileForm();
  document.getElementById('profileForm').addEventListener('submit', saveProfile);
  document.getElementById('passwordForm').addEventListener('submit', savePassword);
}

function renderProfileHead() {
  const head = document.getElementById('profileHead');
  const verifiedBadge = profileUser.isVerified
    ? '<span class="badge badge-approved" style="margin-top:8px">✔ Verified</span>'
    : '<span class="badge badge-pending" style="margin-top:8px">Unverified</span>';
  head.innerHTML = `
    ${dashboardAvatar(profileUser, 'avatar')}
    <div>
      <div class="ph-name">${escapeHtml(profileUser.name || 'User')}</div>
      <div class="ph-meta">${escapeHtml(profileUser.email || '')}</div>
      <div class="ph-meta">${escapeHtml([profileUser.city, profileUser.state].filter(Boolean).join(', ')) || 'Location not set'}</div>
      ${verifiedBadge}
    </div>
  `;
}

function fillProfileForm() {
  document.getElementById('name').value = profileUser.name || '';
  document.getElementById('phone').value = profileUser.phone || '';
  document.getElementById('city').value = profileUser.city || '';
  document.getElementById('state').value = profileUser.state || '';
  document.getElementById('profilePic').value = profileUser.profilePic || '';
  document.getElementById('bio').value = profileUser.bio || '';
}

async function saveProfile(event) {
  event.preventDefault();
  const btn = document.getElementById('saveProfileBtn');
  const payload = {
    name: document.getElementById('name').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    city: document.getElementById('city').value.trim(),
    state: document.getElementById('state').value.trim(),
    profilePic: document.getElementById('profilePic').value.trim(),
    bio: document.getElementById('bio').value.trim()
  };
  if (!payload.name) {
    showToast('Name is required', 'error');
    return;
  }
  btn.disabled = true;
  btn.textContent = 'Saving...';
  try {
    profileUser = await UserAPI.updateProfile(payload);
    localStorage.setItem('staymart_user', JSON.stringify(profileUser));
    Auth.user = profileUser;
    renderProfileHead();
    Dashboard.renderUserCard();
    showToast('Profile updated');
  } catch (error) {
    showToast(error.message, 'error');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Save Changes';
  }
}

async function savePassword(event) {
  event.preventDefault();
  const errorEl = document.getElementById('pwError');
  errorEl.style.display = 'none';
  const currentPassword = document.getElementById('currentPassword').value;
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  if (newPassword.length < 6) {
    return showPwError('New password must be at least 6 characters');
  }
  if (newPassword !== confirmPassword) {
    return showPwError('New password and confirmation do not match');
  }

  const btn = document.getElementById('savePasswordBtn');
  btn.disabled = true;
  btn.textContent = 'Updating...';
  try {
    await UserAPI.changePassword({ currentPassword, newPassword });
    document.getElementById('passwordForm').reset();
    showToast('Password changed successfully');
  } catch (error) {
    showPwError(error.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Update Password';
  }
}

function showPwError(message) {
  const errorEl = document.getElementById('pwError');
  errorEl.textContent = message;
  errorEl.style.display = 'block';
  return null;
}

document.addEventListener('DOMContentLoaded', initProfile);
