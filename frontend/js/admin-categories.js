let catType = '';
let categories = [];

async function initAdminCategories() {
  const ok = await Dashboard.init({ role: 'admin', active: 'categories', title: 'Categories', subtitle: 'Manage product & accommodation categories' });
  if (!ok) return;
  loadCategories();
}

function filterCategories(type) {
  catType = type;
  document.querySelectorAll('#catTabs .tab').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.type === type);
  });
  loadCategories();
}

async function loadCategories() {
  const body = document.getElementById('catBody');
  const count = document.getElementById('catCount');
  body.innerHTML = '<tr><td colspan="5" class="inline-empty">Loading…</td></tr>';
  try {
    categories = await CategoryAPI.getAll(catType || undefined);
    categories = Array.isArray(categories) ? categories : [];
    count.textContent = `${categories.length} categor${categories.length === 1 ? 'y' : 'ies'}`;
    if (!categories.length) {
      body.innerHTML = '<tr><td colspan="5" class="inline-empty">No categories found</td></tr>';
      return;
    }
    body.innerHTML = categories.map((c) => `<tr>
      <td style="font-size:20px">${escapeHtml(c.icon || '📁')}</td>
      <td style="font-weight:600">${escapeHtml(c.name)}</td>
      <td><span class="badge ${c.type === 'ACCOMMODATION' ? 'badge-pg' : 'badge-sell'}">${escapeHtml(c.type || '')}</span></td>
      <td>${c.parentId == null ? '—' : c.parentId}</td>
      <td>
        <div class="list-actions">
          <button class="btn btn-secondary btn-sm" onclick="editCategory(${c.id})">Edit</button>
          <button class="btn btn-danger btn-sm" onclick="removeCategory(${c.id})">Delete</button>
        </div>
      </td>
    </tr>`).join('');
  } catch (error) {
    body.innerHTML = `<tr><td colspan="5" class="inline-empty">${escapeHtml(error.message)}</td></tr>`;
  }
}

function editCategory(id) {
  const category = categories.find((c) => c.id === id);
  if (category) openCategoryModal(category);
}

function openCategoryModal(category) {
  const editing = !!category;
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal modal-wide">
      <h3 class="modal-title">${editing ? 'Edit Category' : 'New Category'}</h3>
      <div class="modal-form">
        <div class="input-group">
          <label for="catName">Name</label>
          <input id="catName" type="text" maxlength="100" value="${escapeHtml(category ? category.name : '')}"/>
        </div>
        <div class="input-group">
          <label for="catType">Type</label>
          <select id="catType">
            <option value="ACCOMMODATION"${category && category.type === 'ACCOMMODATION' ? ' selected' : ''}>Accommodation</option>
            <option value="PRODUCT"${category && category.type === 'PRODUCT' ? ' selected' : ''}>Product</option>
          </select>
        </div>
        <div class="input-group">
          <label for="catIcon">Icon (emoji)</label>
          <input id="catIcon" type="text" maxlength="50" value="${escapeHtml(category ? category.icon || '' : '')}"/>
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
    const name = document.getElementById('catName').value.trim();
    if (!name) {
      showToast('Name is required', 'error');
      return;
    }
    const payload = {
      name,
      type: document.getElementById('catType').value,
      icon: document.getElementById('catIcon').value.trim() || null,
      parentId: category ? category.parentId : null
    };
    try {
      if (editing) {
        await CategoryAPI.update(category.id, payload);
        showToast('Category updated');
      } else {
        await CategoryAPI.create(payload);
        showToast('Category created');
      }
      close();
      loadCategories();
    } catch (error) {
      showToast(error.message, 'error');
    }
  };
}

async function removeCategory(id) {
  const confirmed = await showModal('Delete this category? This only works if no listings use it.', 'Delete Category', 'Delete');
  if (!confirmed) return;
  try {
    await CategoryAPI.remove(id);
    showToast('Category deleted');
    loadCategories();
  } catch (error) {
    showToast(error.message, 'error');
  }
}

document.addEventListener('DOMContentLoaded', initAdminCategories);
