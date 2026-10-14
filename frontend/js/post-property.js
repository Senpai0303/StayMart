let imageUrls = [];

function guardForm() {
  if (!Auth.isLoggedIn()) {
    showToast('Please login to post a property.', 'info');
    setTimeout(function () { window.location.href = 'login.html'; }, 1200);
    return false;
  }
  return true;
}

function addImageUrl() {
  const input = document.getElementById('imageInput');
  const url = input.value.trim();
  if (!url) {
    showToast('Paste an image URL first.', 'info');
    return;
  }
  const duplicate = imageUrls.some(function (u) { return u === url; });
  if (duplicate) {
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
  if (!box) return;
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
  const type = document.querySelector('input[name="type"]:checked').value;
  const genderPreference = document.querySelector('input[name="gender"]:checked').value;
  const city = document.getElementById('city').value;
  const area = document.getElementById('area').value.trim();
  const address = document.getElementById('address').value.trim();
  const pricePerMonth = Number(document.getElementById('pricePerMonth').value);
  const depositAmount = document.getElementById('depositAmount').value ? Number(document.getElementById('depositAmount').value) : null;
  const totalRooms = Number(document.getElementById('totalRooms').value || 1);
  const availableRooms = Number(document.getElementById('availableRooms').value ?? totalRooms);
  const amenities = Array.from(document.querySelectorAll('#amenitiesGrid input:checked')).map(function (cb) { return cb.value; });

  if (!title || !description || !area) {
    showToast('Please fill in title, description and area.', 'error');
    return;
  }
  if (!pricePerMonth || pricePerMonth <= 0) {
    showToast('Please enter a valid monthly rent.', 'error');
    return;
  }

  const submitBtn = event.target.querySelector('button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Posting…';

  const locationId = await resolveLocationId(city, area);
  const payload = {
    title,
    description,
    type,
    genderPreference,
    address,
    area,
    locationId,
    pricePerMonth,
    depositAmount,
    amenities,
    totalRooms,
    availableRooms,
    images: imageUrls
  };

  try {
    await PropertyAPI.create(payload);
    logBehavior('POST', 'PROPERTY', null, null, city);
    showToast('Property submitted for review! ✔️', 'success');
    setTimeout(function () { window.location.href = 'index.html'; }, 1400);
  } catch (error) {
    submitBtn.disabled = false;
    submitBtn.textContent = '🚀 Post Property Now';
    await showModal(error.message || 'Something went wrong.', 'Could not post', 'Try again');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  initAuth().then(function () {
    if (!guardForm()) return;
    const desc = document.getElementById('description');
    desc.addEventListener('input', function () {
      document.getElementById('descCount').textContent = desc.value.length;
    });
    document.getElementById('propertyForm').addEventListener('submit', handleSubmit);
  });
});