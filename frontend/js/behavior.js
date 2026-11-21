async function logBehavior(action, itemType = null, itemId = null, searchQuery = null, cityFilter = null) {
  const token = localStorage.getItem('staymart_token');
  if (!token) return;
  try {
    const baseUrl = (typeof BASE_URL !== 'undefined' ? BASE_URL : '/api').replace(/\/+$/, '');
    await fetch(`${baseUrl}/behaviors`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        action,
        itemType,
        itemId,
        searchQuery,
        cityFilter
      })
    });
  } catch (error) {
    // behavior logging is best-effort; never block the UI
  }
}