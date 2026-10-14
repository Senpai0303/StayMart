const BASE_URL = 'http://localhost:8080/api';

async function apiCall(endpoint, method = 'GET', body = null) {
  const headers = {
    'Content-Type': 'application/json'
  };
  const token = localStorage.getItem('staymart_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  const config = { method, headers };
  if (body) {
    config.body = JSON.stringify(body);
  }
  const res = await fetch(BASE_URL + endpoint, config);
  const data = await res.json();
  if (!data || data.success === false) {
    throw new Error((data && data.message) || 'Something went wrong');
  }
  if (res.ok === false) {
    throw new Error((data && data.message) || 'Something went wrong');
  }
  if (data && typeof data === 'object' && 'success' in data && 'data' in data) {
    return data.data;
  }
  return data;
}

const PropertyAPI = {
  getAll: (params) => apiCall(`/properties${buildQuery(params)}`),
  getMy: () => apiCall('/users/me/properties'),
  getById: (id) => apiCall(`/properties/${id}`),
  create: (propertyData) => apiCall('/properties', 'POST', propertyData),
  update: (id, propertyData) => apiCall(`/properties/${id}`, 'PUT', propertyData),
  delete: (id) => apiCall(`/properties/${id}`, 'DELETE'),
  getRooms: (id) => apiCall(`/properties/${id}/rooms`)
};

const ProductAPI = {
  getAll: (params) => apiCall(`/products${buildQuery(params)}`),
  getMy: () => apiCall('/users/me/products'),
  getById: (id) => apiCall(`/products/${id}`),
  create: (productData) => apiCall('/products', 'POST', productData),
  update: (id, productData) => apiCall(`/products/${id}`, 'PUT', productData),
  delete: (id) => apiCall(`/products/${id}`, 'DELETE')
};

const AuthAPI = {
  register: (userData) => apiCall('/auth/register', 'POST', userData),
  login: (credentials) => apiCall('/auth/login', 'POST', credentials),
  getCurrentUser: () => apiCall('/users/me')
};

const UserAPI = {
  getMe: () => apiCall('/users/me'),
  updateProfile: (data) => apiCall('/users/me', 'PUT', data),
  changePassword: (data) => apiCall('/users/me/password', 'PUT', data),
  getMyProperties: (page = 0, size = 20) => apiCall(`/users/me/properties?page=${page}&size=${size}`),
  getMyProducts: (page = 0, size = 20) => apiCall(`/users/me/products?page=${page}&size=${size}`)
};

const BookingAPI = {
  create: (bookingData) => apiCall('/bookings', 'POST', bookingData),
  getMy: () => apiCall('/bookings/mine'),
  getReceived: () => apiCall('/bookings/incoming'),
  getById: (id) => apiCall(`/bookings/${id}`),
  updateStatus: (id, status) => apiCall(`/bookings/${id}/status?status=${encodeURIComponent(status)}`, 'PATCH')
};

const OrderAPI = {
  create: (orderData) => apiCall('/orders', 'POST', orderData),
  getMy: () => apiCall('/orders/mine'),
  getReceived: () => apiCall('/orders/sales'),
  getById: (id) => apiCall(`/orders/${id}`),
  updateStatus: (id, status) => apiCall(`/orders/${id}/status?status=${encodeURIComponent(status)}`, 'PATCH')
};

const WishlistAPI = {
  getAll: () => apiCall('/wishlist'),
  add: (itemType, itemId) => apiCall('/wishlist', 'POST', { itemType, itemId }),
  remove: (itemType, itemId) => apiCall(`/wishlist?itemType=${itemType}&itemId=${itemId}`, 'DELETE'),
  check: (itemType, itemId) => apiCall(`/wishlist/check?itemType=${itemType}&itemId=${itemId}`)
};

const ReviewAPI = {
  getAll: (params) => apiCall(`/reviews${buildQuery(params)}`),
  add: (reviewData) => apiCall('/reviews', 'POST', reviewData),
  getByItem: (type, itemId, page, size = 5) => apiCall(`/reviews?itemType=${type}&itemId=${itemId}&page=${page || 0}&size=${size}`),
  getSummary: (type, itemId) => apiCall(`/reviews/summary?itemType=${type}&itemId=${itemId}`),
  getMine: (page = 0, size = 20) => apiCall(`/reviews/mine?page=${page}&size=${size}`),
  remove: (id) => apiCall(`/reviews/${id}`, 'DELETE')
};

const CategoryAPI = {
  getAll: (type) => apiCall(`/categories${type ? `?type=${type}` : ''}`),
  getById: (id) => apiCall(`/categories/${id}`),
  create: (data) => apiCall('/categories', 'POST', data),
  update: (id, data) => apiCall(`/categories/${id}`, 'PUT', data),
  remove: (id) => apiCall(`/categories/${id}`, 'DELETE')
};

const ChatAPI = {
  send: (messageData) => apiCall('/chats', 'POST', messageData),
  getConversations: () => apiCall('/chats/conversations'),
  getWith: (userId) => apiCall(`/chats/with/${userId}`),
  markRead: (userId) => apiCall(`/chats/read/${userId}`, 'POST'),
  getUnreadCount: () => apiCall('/chats/unread-count')
};

const LocationAPI = {
  getAll: () => apiCall('/locations'),
  getCities: () => apiCall('/locations/cities'),
  search: (q, city) => apiCall(`/locations/search?q=${encodeURIComponent(q || '')}&city=${encodeURIComponent(city || '')}`),
  create: (data) => apiCall('/locations', 'POST', data),
  update: (id, data) => apiCall(`/locations/${id}`, 'PUT', data),
  remove: (id) => apiCall(`/locations/${id}`, 'DELETE')
};

const RecommendationAPI = {
  getForUser: (userId, limit = 8, city) => apiCall(`/recommendations/${userId}?limit=${limit}${city ? `&city=${encodeURIComponent(city)}` : ''}`),
  getRecommendedProperties: (city, limit = 8) => apiCall(`/recommendations/properties?limit=${limit}${city ? `&city=${encodeURIComponent(city)}` : ''}`),
  getSimilarProperties: (propertyId, limit = 4) => apiCall(`/recommendations/properties/${propertyId}/similar?limit=${limit}`),
  getTrendingProperties: (limit = 8, city) => apiCall(`/recommendations/properties/trending?limit=${limit}${city ? `&city=${encodeURIComponent(city)}` : ''}`),
  getRecommendedProducts: (city, limit = 8) => apiCall(`/recommendations/products?limit=${limit}${city ? `&city=${encodeURIComponent(city)}` : ''}`),
  getTopRatedProducts: (limit = 8, city) => apiCall(`/recommendations/products/top-rated?limit=${limit}${city ? `&city=${encodeURIComponent(city)}` : ''}`)
};

const AdminAPI = {
  getStats: () => apiCall('/admin/stats'),
  getAnalytics: () => apiCall('/admin/analytics'),
  getPendingProperties: (page = 0, size = 10) => apiCall(`/admin/properties?status=PENDING&page=${page}&size=${size}`),
  getPendingProducts: (page = 0, size = 10) => apiCall(`/admin/products?status=PENDING&page=${page}&size=${size}`),
  getProperties: (status, page = 0, size = 10) => apiCall(`/admin/properties?${status ? `status=${status}&` : ''}page=${page}&size=${size}`),
  getProducts: (status, page = 0, size = 10) => apiCall(`/admin/products?${status ? `status=${status}&` : ''}page=${page}&size=${size}`),
  getAllUsers: (page = 0, size = 10) => apiCall(`/admin/users?page=${page}&size=${size}`),
  changeStatus: (type, id, status) => apiCall(`/admin/${type}/${id}/status`, 'PATCH', { status }),
  toggleUserStatus: (id, active) => apiCall(`/admin/users/${id}/status?active=${active}`, 'PATCH'),
  deleteUser: (id) => apiCall(`/admin/users/${id}`, 'DELETE')
};

function buildQuery(params) {
  if (!params) return '';
  const parts = Object.entries(params)
    .filter(([key, value]) => value !== undefined && value !== null && value !== '')
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
  return parts.length ? `?${parts.join('&')}` : '';
}