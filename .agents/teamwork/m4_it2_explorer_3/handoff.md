# Milestone 4 Investigation Report: Frontend Reverse-Proxy Integration & API Client Architecture

**Explorer**: Milestone 4 Iteration 2 Explorer 3 (Frontend Reverse-Proxy & API Client Investigator)  
**Date**: November 2, 2026  
**Working Directory**: `d:\Mini5th\.agents\teamwork\m4_it2_explorer_3\`  
**Target Files**: `frontend/js/api.js`, `frontend/js/behavior.js`, `vercel.json`, `frontend/vercel.json`, `report/appendices/app_frontend_code.tex`  
**Milestone**: Milestone 4 (Free Full-Stack Deployment Configurations & Documentation)  

---

## 1. Observation

### 1.1 Existing `frontend/js/api.js` Implementation
Direct inspection of `frontend/js/api.js` (lines 1–32):
```javascript
1: // Auto-detect local development vs cloud deployment
2: const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
3: const BASE_URL = isLocal
4:   ? 'http://localhost:8080/api'
5:   : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || 'https://staymart.onrender.com/api');
6: 
7: 
8: async function apiCall(endpoint, method = 'GET', body = null) {
9:   const headers = {
10:     'Content-Type': 'application/json'
11:   };
12:   const token = localStorage.getItem('staymart_token');
13:   if (token) {
14:     headers['Authorization'] = `Bearer ${token}`;
15:   }
16:   const config = { method, headers };
17:   if (body) {
18:     config.body = JSON.stringify(body);
19:   }
20:   const res = await fetch(BASE_URL + endpoint, config);
21:   const data = await res.json();
22:   if (!data || data.success === false) {
23:     throw new Error((data && data.message) || 'Something went wrong');
24:   }
25:   if (res.ok === false) {
26:     throw new Error((data && data.message) || 'Something went wrong');
27:   }
28:   if (data && typeof data === 'object' && 'success' in data && 'data' in data) {
29:     return data.data;
30:   }
31:   return data;
32: }
```

### 1.2 Discrepancies with Cloud Configuration & Reverse-Proxy Rewrites
1. **Render Service Name Discrepancy**:
   - In `render.yaml` (lines 5–6):
     ```yaml
     5:   - type: web
     6:     name: staymart-backend
     ```
   - In `DEPLOYMENT.md` (lines 195 & 227):
     The backend URL is specified as `https://staymart-backend.onrender.com`.
   - In `frontend/js/api.js` line 5:
     The fallback domain is `'https://staymart.onrender.com/api'` (missing the `-backend` suffix).
2. **Vercel Reverse-Proxy Configuration**:
   - In `vercel.json` (lines 4–9) and `frontend/vercel.json` (lines 4–9):
     ```json
     "rewrites": [
       { "source": "/", "destination": "/frontend/index.html" },
       { "source": "/api/(.*)", "destination": "https://staymart-backend.onrender.com/api/$1" },
       { "source": "/uploads/(.*)", "destination": "https://staymart-backend.onrender.com/uploads/$1" },
       { "source": "/(.*)", "destination": "/frontend/$1" }
     ]
     ```
   - In `DEPLOYMENT.md` Section 5.2 (lines 219–237):
     ```markdown
     ### 5.2 How the Reverse Proxy Eliminates CORS
     Both `vercel.json` (at repo root) and `frontend/vercel.json` contain reverse proxy rewrites:
     ...
     **Key Advantages:**
     1. **No Cross-Origin Restrictions**: The browser communicates with the same origin (`https://staymart.vercel.app/api/...`), so no CORS pre-flight `OPTIONS` requests are needed.
     2. **No Mixed-Content Warnings**: All requests are routed through Vercel's edge HTTPS certificates.
     ```
   - When `BASE_URL` in `api.js` is an absolute URL (`https://staymart.onrender.com/api`), the browser bypasses Vercel's edge reverse proxy completely. Every `fetch` request is directed across origins to Render, triggering mandatory CORS preflight (`OPTIONS`) roundtrips.
   - When `BASE_URL` is relative (`/api`), the browser calls `https://staymart.vercel.app/api/...` as same-origin requests, which Vercel Edge proxies server-to-server to Render.

### 1.3 Complete Inventory of Frontend Callers
A comprehensive grep audit across all 29 JavaScript files in `frontend/js/` revealed:
1. **Direct `fetch(` usage**:
   - `frontend/js/api.js:20`: `const res = await fetch(BASE_URL + endpoint, config);`
   - `frontend/js/behavior.js:5`: `await fetch(`${BASE_URL}/behaviors`, { ... });`
   - **Zero** `fetch(` calls exist in any other `.js` or `.html` file.
2. **Exported API Modules in `frontend/js/api.js`**:
   The file exposes 13 client API namespaces:
   - `PropertyAPI` (lines 34–42): `getAll`, `getMy`, `getById`, `create`, `update`, `delete`, `getRooms`
   - `ProductAPI` (lines 44–51): `getAll`, `getMy`, `getById`, `create`, `update`, `delete`
   - `AuthAPI` (lines 53–57): `register`, `login`, `getCurrentUser`
   - `UserAPI` (lines 59–65): `getMe`, `updateProfile`, `changePassword`, `getMyProperties`, `getMyProducts`
   - `BookingAPI` (lines 67–73): `create`, `getMy`, `getReceived`, `getById`, `updateStatus`
   - `OrderAPI` (lines 75–81): `create`, `getMy`, `getReceived`, `getById`, `updateStatus`
   - `WishlistAPI` (lines 83–88): `getAll`, `add`, `remove`, `check`
   - `ReviewAPI` (lines 90–97): `getAll`, `add`, `getByItem`, `getSummary`, `getMine`, `remove`
   - `CategoryAPI` (lines 99–105): `getAll`, `getById`, `create`, `update`, `remove`
   - `ChatAPI` (lines 107–113): `send`, `getConversations`, `getWith`, `markRead`, `getUnreadCount`
   - `LocationAPI` (lines 115–122): `getAll`, `getCities`, `search`, `create`, `update`, `remove`
   - `RecommendationAPI` (lines 124–132): `getForUser`, `getRecommendedProperties`, `getSimilarProperties`, `getTrendingProperties`, `getRecommendedProducts`, `getSimilarProducts`, `getTopRatedProducts`
   - `AdminAPI` (lines 134–145): `getStats`, `getAnalytics`, `getPendingProperties`, `getPendingProducts`, `getProperties`, `getProducts`, `getAllUsers`, `changeStatus`, `toggleUserStatus`, `deleteUser`
3. **Consumer Modules**:
   - `auth.js`: calls `AuthAPI` methods
   - `home.js`: calls `CategoryAPI`, `RecommendationAPI`, `PropertyAPI`, `ProductAPI`
   - `search.js`: calls `PropertyAPI`, `ProductAPI`, `CategoryAPI`, `LocationAPI`, `WishlistAPI`, `logBehavior`
   - `property-detail.js`: calls `PropertyAPI`, `BookingAPI`, `WishlistAPI`, `ChatAPI`, `ReviewAPI`, `RecommendationAPI`, `logBehavior`
   - `product-detail.js`: calls `ProductAPI`, `OrderAPI`, `WishlistAPI`, `ChatAPI`, `ReviewAPI`, `RecommendationAPI`, `logBehavior`
   - `post-property.js` & `post-product.js`: call `LocationAPI`, `PropertyAPI` / `ProductAPI`, `logBehavior`
   - `bookings.js`, `orders.js`, `chat.js`, `my-listings.js`, `user-dashboard.js`, `profile.js`, `requests-received.js`, `wishlist.js`: call their respective `*API` objects
   - `stats.js` & `charts.js`: pure client-side mathematical/visual models and chart renderers; zero direct network calls
4. **Endpoint URI Formatting**:
   In `frontend/js/api.js`, every single endpoint string passed to `apiCall` begins with a leading forward slash `/` (e.g. `apiCall('/properties')`, `apiCall('/auth/login')`, `apiCall('/users/me')`).
   When `BASE_URL = '/api'`, `BASE_URL + endpoint` evaluates to `'/api/properties'`, exactly matching Vercel's rewrite rule `/api/(.*)`.

### 1.4 Verification Suite Expectations
In `scripts/test_m4_adversarial_audit.py` (lines 136–141):
```python
api_js_audit = {
    "has_isLocal_detection": "window.location.hostname === 'localhost'" in api_js_content,
    "has_window_override": "window.STAYMART_API_URL" in api_js_content,
    "has_localStorage_override": "localStorage.getItem('STAYMART_API_URL')" in api_js_content,
    "hardcoded_fallback": re.search(r":\s*\((.*?)\);", api_js_content, re.DOTALL).group(1) if re.search(r":\s*\((.*?)\);", api_js_content, re.DOTALL) else None
}
```
The audit harness checks for:
- Exact substring: `"window.location.hostname === 'localhost'"`
- Exact substring: `"window.STAYMART_API_URL"`
- Exact substring: `"localStorage.getItem('STAYMART_API_URL')"`
- Regex extraction: `r":\s*\((.*?)\);"`

In `report/appendices/app_frontend_code.tex` (lines 9–12):
The LaTeX appendix contains an verbatim code listing of `api.js` lines 9–12. When `api.js` is modified, this appendix should be synchronized to keep the project report aligned.

---

## 2. Logic Chain

1. **Step 1 (Root Cause of Latency and Broken Fallback — Observation 1.1 & 1.2)**:
   In `frontend/js/api.js:5`, the fallback is `'https://staymart.onrender.com/api'`.
   If a user visits the Vercel-deployed application (`https://staymart.vercel.app`), `window.STAYMART_API_URL` and `localStorage` are unset.
   The browser attempts to send fetch calls to `https://staymart.onrender.com/api/properties`.
   Because the service on Render is named `staymart-backend`, this domain fails or routes incorrectly.
   Even if it resolved, sending requests to an external origin forces the browser to issue CORS preflight `OPTIONS` requests before sending data.
   *Inference*: The fallback must be changed from `'https://staymart.onrender.com/api'` to `'/api'`.

2. **Step 2 (Vercel Edge Rewrite Alignment — Observation 1.2 & 1.3)**:
   In `vercel.json`, rule 2 is `{ "source": "/api/(.*)", "destination": "https://staymart-backend.onrender.com/api/$1" }`.
   When `BASE_URL` is `'/api'`, every call from `apiCall('/properties')` issues a relative `fetch('/api/properties')`.
   Because this request is made to the same origin (`staymart.vercel.app`), the browser executes it as a standard same-origin request:
   - No `OPTIONS` preflight request is generated.
   - Vercel's Edge CDN proxies the request directly to Render backend over TLS.
   - Cold starts on Render only suffer a single request delay rather than a preflight failure.
   *Inference*: Relative `'/api'` delivers zero-configuration, zero-preflight proxying for all Vercel deployments.

3. **Step 3 (Consumer Compatibility Audit — Observation 1.3)**:
   Across the entire frontend codebase (all 29 JS files and 26 HTML pages):
   - Only `api.js` and `behavior.js` invoke `fetch()`.
   - In `behavior.js:5`, the code executes `fetch(`${BASE_URL}/behaviors`, ...)`.
     With `BASE_URL = '/api'`, this becomes `fetch('/api/behaviors', ...)`, which matches `/api/(.*)` in `vercel.json` ($1 = `behaviors`).
   - All other 27 files use the exported `*API` methods, which invoke `apiCall(endpoint)`.
   *Inference*: Modifying `BASE_URL` in `api.js` fixes 100% of network interactions across all pages without requiring changes across other frontend consumer files.

4. **Step 4 (Trailing-Slash Defensiveness & Localhost Support — Observation 1.1, 1.3 & 1.4)**:
   If a user configures `window.STAYMART_API_URL = 'https://staymart-backend.onrender.com/api/'` with a trailing slash, `BASE_URL + '/properties'` produces `.../api//properties`.
   Adding trailing-slash normalization (`.replace(/\/+$/, '')`) in `apiCall` and `behavior.js` prevents path malformation.
   Ensuring `isLocal` continues to test `window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:'` ensures developers running locally continue to connect directly to `http://localhost:8080/api`.
   *Inference*: A clean ternary expression retaining the test harness substrings while changing the fallback to `'/api'` satisfies all automated audits and runtime conditions.

---

## 3. Caveats

1. **Direct Render Deployments without Reverse Proxy**:
   If a user chooses to deploy the static frontend to a service without reverse proxy support (e.g. GitHub Pages or Render Static Site without rewrites), relative `'/api'` would point to that static host's `/api` (which 404s). In that specific non-Vercel scenario, the user must set `window.STAYMART_API_URL = 'https://staymart-backend.onrender.com/api'` or configure `localStorage.setItem('STAYMART_API_URL', 'https://staymart-backend.onrender.com/api')`. This is already supported and documented.
2. **Read-Only Investigation Protocol**:
   This explorer does not modify source files directly. The exact code diffs and recommendations provided below must be applied by the designated implementation worker.

---

## 4. Conclusion & Concrete Code Specification

### 4.1 Recommended Changes for `frontend/js/api.js`

#### Target File: `d:\Mini5th\frontend\js\api.js`
**Lines to Modify**: Lines 1–25.

#### Code Snippet (Before vs. After):

**Before (Lines 1–6)**:
```javascript
// Auto-detect local development vs cloud deployment
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const BASE_URL = isLocal
  ? 'http://localhost:8080/api'
  : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || 'https://staymart.onrender.com/api');
```

**After (Lines 1–6)**:
```javascript
// Auto-detect local development vs cloud deployment
const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' || window.location.protocol === 'file:';
const BASE_URL = isLocal
  ? 'http://localhost:8080/api'
  : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || '/api');
```

**Before (Lines 8–20 in `apiCall`)**:
```javascript
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
```

**After (Lines 8–23 in `apiCall` with trailing-slash normalization)**:
```javascript
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
  const cleanBase = (BASE_URL || '').replace(/\/+$/, '');
  const cleanPath = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
  const res = await fetch(cleanBase + cleanPath, config);
```

### 4.2 Recommended Defensive Polish for `frontend/js/behavior.js`

#### Target File: `d:\Mini5th\frontend\js\behavior.js`
**Lines to Modify**: Lines 1–7.

**Before**:
```javascript
async function logBehavior(action, itemType = null, itemId = null, searchQuery = null, cityFilter = null) {
  const token = localStorage.getItem('staymart_token');
  if (!token) return;
  try {
    await fetch(`${BASE_URL}/behaviors`, {
```

**After**:
```javascript
async function logBehavior(action, itemType = null, itemId = null, searchQuery = null, cityFilter = null) {
  const token = localStorage.getItem('staymart_token');
  if (!token) return;
  try {
    const baseUrl = (typeof BASE_URL !== 'undefined' ? BASE_URL : '/api').replace(/\/+$/, '');
    await fetch(`${baseUrl}/behaviors`, {
```

### 4.3 Documentation & Report Synchronization Items
1. **`report/appendices/app_frontend_code.tex`**:
   Update line 12 from `'https://staymart.onrender.com/api'` to `'/api'`:
   ```latex
   const BASE_URL = isLocal
     ? 'http://localhost:8080/api'
     : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || '/api');
   ```
2. **`DEPLOYMENT.md` Section 5.2**:
   Add a brief note explaining that `frontend/js/api.js` defaults to `'/api'`, routing automatically through Vercel's edge reverse proxy rewrites without requiring manual environment variables.

---

## 5. Verification Method

To independently verify the proposed architecture and future implementation:

1. **Run Empirical M4 Adversarial Audit Script**:
   ```powershell
   python scripts/test_m4_adversarial_audit.py
   ```
   *Expected Output*:
   - `api_js_client_audit.has_isLocal_detection`: `true`
   - `api_js_client_audit.has_window_override`: `true`
   - `api_js_client_audit.has_localStorage_override`: `true`
   - `api_js_client_audit.hardcoded_fallback`: `"window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || '/api'"`
   - `vercel_rewrite_stress`: All `/api/*` and `/uploads/*` endpoints correctly map to `https://staymart-backend.onrender.com/api/*` and `uploads/*`.

2. **Verify JavaScript Syntax & Navigation Integrity**:
   ```powershell
   python scripts/verify_m1_navigation.py
   ```
   *Expected Output*: Suite 4 parses all 29 JS files cleanly; 8/8 suites pass with exit code `0`.

3. **Verify Mobile Viewports & Interactions**:
   ```powershell
   node scripts/run_viewport_tests.js
   ```
   *Expected Output*: 30/30 viewport tests pass with exit code `0`.

4. **Verify Spring Boot Backend Tests**:
   ```powershell
   python scripts/run_backend_tests.py
   ```
   *Expected Output*: 13/13 JUnit 5 tests pass with exit code `0`.
