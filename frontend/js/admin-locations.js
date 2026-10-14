let locations = [];

async function initAdminLocations() {
  const ok = await Dashboard.init({ role: 'admin', active: 'locations', title: 'Locations', subtitle: 'Cities and areas across Uttarakhand' });
  if (!ok) return;
  loadLocations();
}

async function loadLocations() {
  const body = document.getElementById('locBody');
  const count = document.getElementById('locCount');
  body.innerHTML = '<tr><td colspan="6" class="inline-empty">Loading…</td></tr>';
  try {
    locations = await LocationAPI.getAll();
    locations = Array.isArray(locations) ? locations : [];
    count.textContent = `${locations.length} location${locations.length === 1 ? '' : 's'}`;
    renderLocations(locations);
  } catch (error) {
    body.innerHTML = `<tr><td colspan="6" class="inline-empty">${escapeHtml(error.message)}</td></tr>`;
  }
}

function filterLocations() {
  const q = document.getElementById('locSearch').value.trim().toLowerCase();
  if (!q) {
    renderLocations(locations);
    return;
  }
  renderLocations(locations.filter((l) =>
    (l.city || '').toLowerCase().includes(q) || (l.area || '').toLowerCase().includes(q)));
}

function renderLocations(list) {
  const body = document.getElementById('locBody');
  if (!list.length) {
    body.innerHTML = '<tr><td colspan="6" class="inline-empty">No locations found</td></tr>';
    return;
  }
  body.innerHTML = list.map((l) => `<tr>
    <td style="font-weight:600">${escapeHtml(l.city || '')}</td>
    <td>${escapeHtml(l.area || '—')}</td>
    <td>${escapeHtml(l.state || '—')}</td>
    <td>${escapeHtml(l.pincode || '—')}</td>
    <td style="font-size:12px;color:var(--text-muted)">${l.latitude != null && l.longitude != null ? `${l.latitude}, ${l.longitude}` : '—'}</td>
    <td>
      <div class="list-actions">
        <button class="btn btn-secondary btn-sm" onclick="editLocation(${l.id})">Edit</button>
        <button class="btn btn-danger btn-sm" onclick="removeLocation(${l.id})">Delete</button>
      </div>
    </td>
  </tr>`).join('');
}

function editLocation(id) {
  const location = locations.find((l) => l.id === id);
  if (location) openLocationModal(location);
}

function openLocationModal(location) {
  const editing = !!location;
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal modal-wide">
      <h3 class="modal-title">${editing ? 'Edit Location' : 'New Location'}</h3>
      <div class="modal-form">
        <div class="input-group">
          <label for="locCity">City *</label>
          <input id="locCity" type="text" maxlength="100" value="${escapeHtml(location ? location.city || '' : '')}"/>
        </div>
        <div class="input-group">
          <label for="locArea">Area</label>
          <input id="locArea" type="text" maxlength="100" value="${escapeHtml(location ? location.area || '' : '')}"/>
        </div>
        <div class="input-group">
          <label for="locState">State</label>
          <input id="locState" type="text" maxlength="100" value="${escapeHtml(location ? location.state || '' : '')}"/>
        </div>
        <div class="input-group">
          <label for="locPincode">Pincode</label>
          <input id="locPincode" type="text" maxlength="10" value="${escapeHtml(location ? location.pincode || '' : '')}"/>
        </div>
        <div class="input-group">
          <label for="locLat">Latitude</label>
          <input id="locLat" type="number" step="any" value="${location && location.latitude != null ? location.latitude : ''}"/>
        </div>
        <div class="input-group">
          <label for="locLng">Longitude</label>
          <input id="locLng" type="number" step="any" value="${location && location.longitude != null ? location.longitude : ''}"/>
        </div>
      </div>
      <div class="modal-actions">
        <button class="btn btn-secondary modal-cancel">Cancel</button>
        <button class="btn btn-primary modal-save">${editing ? 'Save' : 'Create'}</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
  requestAnimationFrame(() => overlay.classList.add('open'));

  const close = () => {
    overlay.classList.remove('open');
    setTimeout(() => overlay.remove(), 300);
  };
  overlay.querySelector('.modal-cancel').onclick = close;
  overlay.querySelector('.modal-save').onclick = async () => {
    const city = document.getElementById('locCity').value.trim();
    if (!city) {
      showToast('City is required', 'error');
      return;
    }
    const lat = document.getElementById('locLat').value;
    const lng = document.getElementById('locLng').value;
    const payload = {
      city,
      area: document.getElementById('locArea').value.trim() || null,
      state: document.getElementById('locState').value.trim() || null,
      pincode: document.getElementById('locPincode').value.trim() || null,
      latitude: lat === '' ? null : Number(lat),
      longitude: lng === '' ? null : Number(lng)
    };
    try {
      if (editing) {
        await LocationAPI.update(location.id, payload);
        showToast('Location updated');
      } else {
        await LocationAPI.create(payload);
        showToast('Location created');
      }
      close();
      loadLocations();
    } catch (error) {
      showToast(error.message, 'error');
    }
  };
}

async function removeLocation(id) {
  const confirmed = await showModal('Delete this location? This only works if no listings use it.', 'Delete Location', 'Delete');
  if (!confirmed) return;
  try {
    await LocationAPI.remove(id);
    showToast('Location deleted');
    loadLocations();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initAdminLocations);
