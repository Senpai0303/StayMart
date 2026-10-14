let imageUrls = [];
let selectedCategoryId = null;

function guardForm() {
  if (!Auth.isLoggedIn()) {
    showToast('Please login to post a product.', 'info');
    setTimeout(function () { window.location.href = 'login.html'; }, 1200);
    return false;
  }
  return true;
}

async function loadCategories() {
  const cards = document.getElementById('categoryCards');
  try {
    const categories = await CategoryAPI.getAll();
    const accommodationHints = ['PG', 'ROOM', 'HOSTEL', 'HOTEL', 'FLAT', 'DORMITORY', 'APARTMENT', 'BEDSPACE', 'STAY'];
    const productCategories = (categories || []).filter(function (c) {
      if (c.type) return c.type === 'PRODUCT';
      const name = String(c.name || '').toUpperCase();
      return !accommodationHints.some(function (hint) { return name.includes(hint); });
    });
    if (!productCategories.length) {
      cards.innerHTML = '<div class="text-muted-text">No product categories yet.</div>';
      return;
    }
    cards.innerHTML = productCategories.map(function (c, idx) {
      const checked = idx === 0 ? ' checked' : '';
      return `
        <label class="radio-card">
          <input type="radio" name="category" value="${c.id}"${checked}/>
          <div class="radio-card-body">${escapeHtml(c.icon || '🏷️')} ${escapeHtml(c.name)}</div>
        </label>
      `;
    }).join('');
    selectedCategoryId = productCategories[0].id;
    cards.querySelectorAll('input[name="category"]').forEach(function (radio) {
      radio.addEventListener('change', function () {
        selectedCategoryId = Number(radio.value);
      });
    });
  } catch (error) {
    cards.innerHTML = '<div class="text-muted-text">Could not load categories. Please refresh.</div>';
  }
}

function addImageUrl() {
  const input = document.getElementById('imageInput');
  const url = input.value.trim();
  if (!url) {
    showToast('Paste an image URL first.', 'info');
    return;
  }
  if (imageUrls.some(function (u) { return u === url; })) {
    showToast('This image was already added.', 'info');
    return;
  }
  imageUrls.push(url);
  renderImagePreviews();
  input.value = '';
}

function removeImageUrl(index) {
  imageUrls.splice(index, 1);
  renderImagePreviews();
}

function renderImagePreviews() {
  const box = document.getElementById('imagePreviews');
  box.innerHTML = imageUrls.map(function (url, i) {
    return `
      <div class="image-preview">
        <img src="${escapeHtml(url)}" alt="Image ${i + 1}"/>
        <button type="button" class="remove-img" onclick="removeImageUrl(${i})">×</button>
      </div>
    `;
  }).join('');
}

async function resolveLocationId(city, area) {
  try {
    const locations = await LocationAPI.search(area, city);
    if (!locations || !locations.length) return null;
    const match = locations.find(function (loc) {
      return area && loc.area && loc.area.toLowerCase().includes(area.toLowerCase());
    });
    return (match || locations[0]).id;
  } catch (error) {
    return null;
  }
}

async function handleSubmit(event) {
  event.preventDefault();
  if (!guardForm()) return;

  const title = document.getElementById('title').value.trim();
  const description = document.getElementById('description').value.trim();
  const price = Number(document.getElementById('price').value);
  const brand = document.getElementById('brand').value.trim();
  const city = document.getElementById('city').value;
  const area = document.getElementById('area').value.trim();
  const listingType = document.querySelector('input[name="listingType"]:checked').value;
  const condition = document.querySelector('input[name="condition"]:checked').value;

  if (!selectedCategoryId) {
    showToast('Please select a category.', 'error');
    return;
  }
  if (!title || !description) {
    showToast('Please fill in title and description.', 'error');
    return;
  }
  if (!price || price <= 0) {
    showToast('Please enter a valid price.', 'error');
    return;
  }

  const submitBtn = event.target.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Posting…';

  const locationId = await resolveLocationId(city, area);
  const payload = {
    categoryId: selectedCategoryId,
    title,
    description,
    price,
    listingType,
    condition,
    brand,
    locationId,
    area,
    images: imageUrls
  };

  try {
    await ProductAPI.create(payload);
    logBehavior('POST', 'PRODUCT', null, null, city);
    showToast('Product submitted for review! ✔️', 'success');
    setTimeout(function () { window.location.href = 'index.html'; }, 1400);
  } catch (error) {
    submitBtn.disabled = false;
    submitBtn.textContent = '🚀 Post Product Now';
    await showModal(error.message || 'Something went wrong.', 'Could not post', 'Try again');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    if (!guardForm()) return;
    loadCategories();
    const desc = document.getElementById('description');
    desc.addEventListener('input', function () {
      document.getElementById('descCount').textContent = desc.value.length;
    });
    document.getElementById('productForm').addEventListener('submit', handleSubmit);
  });
});