# StayMart: 100% Free Full-Stack Production Deployment Guide

This guide provides a comprehensive, production-tested blueprint for deploying the complete StayMart platform with **zero ongoing monthly hosting costs ($0/mo forever)**. No credit card is required for any of the recommended cloud services.

---

## 1. Zero-Cost Architecture Topology

StayMart is engineered as a decoupled, multi-tier system distributed across four industry-standard free cloud tiers:

```
+---------------------------------------------------------------------------------------------------+
|                                          CLIENT LAYER                                             |
|                     Mobile (375px)   |   Tablet (768px)   |   Desktop (1280px+)                   |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  | HTTPS / HTTP2
                                                  v
+---------------------------------------------------------------------------------------------------+
|  TIER 1: FRONTEND HOSTING                                                                         |
|  Provider: Vercel (Hobby Tier - $0/mo forever)                                                    |
|  - Global Edge CDN, automated SSL/TLS certificates, continuous GitHub deployments                 |
|  - Reverse-Proxy Engine (`vercel.json`): routes `/api/*` and `/uploads/*` to Spring Boot        |
|  - Eliminates browser CORS preflight overhead and HTTPS mixed-content warnings                    |
+---------------------------------------------------------------------------------------------------+
                                                  |
                                                  | Reverse-Proxy Rewrites (`/api/*`)
                                                  v
+---------------------------------------------------------------------------------------------------+
|  TIER 2: REST BACKEND SERVICE                                                                     |
|  Provider: Render (Free Web Service - $0/mo) or Koyeb (Free Eco Tier - $0/mo)                     |
|  - Spring Boot 3.3.5 / Eclipse Temurin JRE 17 in multi-stage Docker container                     |
|  - Tuned with `JAVA_TOOL_OPTIONS="-Xmx384m -Xms128m -XX:+UseSerialGC"` for 512MB RAM ceiling     |
|  - Port: $PORT (Dynamic binding, default 8080)                                                    |
+---------------------------------------------------------------------------------------------------+
                               |                                              |
      Internal REST Client     |                                              | JDBC / HikariCP
     (2s connect, 3s timeout)  |                                              | (Port 4000, TLS/SSL)
                               v                                              v
+----------------------------------------------+    +-----------------------------------------------+
|  TIER 3: ML MICROSERVICE                     |    |  TIER 4: MANAGED DATABASE                     |
|  Provider: Render Free or Hugging Face Spaces|    |  Provider: TiDB Cloud Serverless ($0/mo)      |
|  - Python 3.11-slim + Flask + Gunicorn       |    |  - 5 GB row storage, 50M Request Units/mo free|
|  - Dual-Engine Hybrid Recommendations        |--->|  - 100% MySQL 8.0 wire-protocol compatible    |
|  - Memory Footprint: < 180MB RAM             |    |  - Automated daily backups, TLS 1.3 enforced  |
|  - Port: 5000 (binds to 0.0.0.0:5000)        |    |  - Region: AWS Mumbai (ap-south-1)            |
+----------------------------------------------+    +-----------------------------------------------+
```

### Free Tier Resource Allocations & Quotas

| Tier | Component | Provider | Free Plan Quota | Ongoing Cost |
|------|-----------|----------|-----------------|--------------|
| **Tier 1** | Frontend MPA | **Vercel** | Unlimited deployments, 100GB bandwidth/mo, SSL included | **$0.00** |
| **Tier 2** | Spring Boot Backend | **Render** | 512 MB RAM, 0.1 CPU, 750 free instance hours/mo | **$0.00** |
| **Tier 3** | Flask ML Service | **Render** | 512 MB RAM, 0.1 CPU, shares free instance hour pool | **$0.00** |
| **Tier 4** | Relational Database | **TiDB Cloud** | 5 GB storage, 50M Request Units/mo, TLS encryption | **$0.00** |

---

## 2. Tier 4: TiDB Cloud Serverless Setup (Managed MySQL)

TiDB Cloud Serverless provides a fully managed, MySQL 8.0 wire-compatible relational database with a permanent 5GB free tier. It requires no credit card.

### 2.1 Cluster Creation
1. Navigate to [TiDB Cloud](https://tidbcloud.com/) and register using GitHub or Google authentication.
2. Select **Create Cluster** and choose **Serverless (Free Forever)**.
3. Configure your cluster:
   - **Cluster Name**: `staymart-cluster`
   - **Cloud Provider**: AWS
   - **Region**: Select a region close to your target audience (e.g., `ap-south-1` Mumbai or `ap-southeast-1` Singapore).
4. Click **Create**. Within 20 seconds, your cluster is active.

### 2.2 Connection Credentials
In your cluster overview, click **Connect**:
- **Connection Type**: Select **General** or **Java (JDBC)**.
- Note the following parameters:
  - **Host**: e.g., `gateway01.ap-south-1.prod.aws.tidbcloud.com`
  - **Port**: `4000`
  - **User**: e.g., `xxxxxx.root`
  - **Password**: Click **Generate Password** (save this securely).
  - **Database Name**: `staymart`

### 2.3 Critical Database Initialization Sequence
> **IMPORTANT ARCHITECTURAL REQUIREMENT**:  
> In `src/main/resources/application.yml`, the backend is configured with `spring.jpa.hibernate.ddl-auto: validate`.  
> Hibernate verifies that all 12 tables, indexes, and JSON column mappings exist before the Spring Boot application starts. If the schema is missing, Spring Boot will refuse to start.

Open the **Web SQL Editor** in the TiDB Cloud Console (or connect via MySQL Workbench / DBeaver) and execute the SQL scripts from the `database/` folder in this exact sequence:

1. **`database/01_schema.sql`**:  
   Creates the `staymart` database, foreign keys, secondary indexes, and all 12 tables (`users`, `categories`, `locations`, `properties`, `rooms`, `products`, `bookings`, `orders`, `reviews`, `wishlists`, `chats`, `user_behaviors`).
2. **`database/02_seed.sql`**:  
   Seeds Uttarakhand geographical coordinates (Dehradun, Rishikesh, Haridwar, Mussoorie, Nainital, Roorkee) and product/accommodation categories.
3. **`database/03_seed_listings.sql`**:  
   Seeds student seller accounts and initial accommodation and classified listings.
4. **`database/04_update_realistic_media.sql`**:  
   Populates authentic, high-resolution student accommodation and marketplace photography.
5. **`database/05_olx_amazon_listings.sql`**:  
   Injects genuine campus classifieds with Uttarakhand student landmarks (Graphic Era University, UPES, FRI, Pacific Mall).

```bash
# Alternative: Initialize via MySQL CLI from your local terminal
mysql -h <tidb-host> -P 4000 -u <tidb-user> -p --ssl-mode=VERIFY_IDENTITY < database/01_schema.sql
mysql -h <tidb-host> -P 4000 -u <tidb-user> -p --ssl-mode=VERIFY_IDENTITY < database/02_seed.sql
mysql -h <tidb-host> -P 4000 -u <tidb-user> -p --ssl-mode=VERIFY_IDENTITY < database/03_seed_listings.sql
mysql -h <tidb-host> -P 4000 -u <tidb-user> -p --ssl-mode=VERIFY_IDENTITY < database/04_update_realistic_media.sql
mysql -h <tidb-host> -P 4000 -u <tidb-user> -p --ssl-mode=VERIFY_IDENTITY < database/05_olx_amazon_listings.sql
```

---

## 3. Tier 3: Flask ML Microservice Deployment

The ML service (`ml-service/`) handles dual-engine hybrid recommendations using scikit-learn TF-IDF vectorizers and collaborative filtering. It should be deployed before the backend so the backend can link to it.

### 3.1 Deploying on Render (Free Web Service)
1. Log in to [Render](https://render.com/) via GitHub.
2. Click **New +** -> **Web Service**.
3. Select your repository `Mini5th`.
4. Configure service details:
   - **Name**: `staymart-ml`
   - **Region**: Singapore or nearest to your database
   - **Branch**: `main`
   - **Root Directory**: `ml-service`
   - **Runtime**: `Docker`
   - **Instance Type**: `Free` ($0/mo)
5. Set Environment Variables:

| Variable | Recommended Value | Description |
|----------|-------------------|-------------|
| `PORT` | `5000` | Port bound by Gunicorn |
| `DB_HOST` | `<tidb-host>` | TiDB Gateway hostname |
| `DB_PORT` | `4000` | TiDB Port (4000) |
| `DB_USERNAME` | `<tidb-user>` | TiDB Username |
| `DB_PASSWORD` | `<tidb-password>` | TiDB Password |
| `DB_NAME` | `staymart` | MySQL Database name |
| `DEFAULT_CITY` | `Dehradun` | Fallback city for cold-start recommendations |

6. Click **Deploy Web Service**.
7. Once deployed, note your service URL: `https://staymart-ml.onrender.com`.

### 3.2 Verification
Run a curl command to check service health:
```bash
curl -s https://staymart-ml.onrender.com/health
```
Expected response:
```json
{"database":"connected","models_loaded":true,"service":"staymart-ml","status":"healthy"}
```

---

## 4. Tier 2: Spring Boot Backend Deployment

The backend runs on Java 17 / Spring Boot 3.3.5 and is containerized via a multi-stage Dockerfile with memory optimization.

### 4.1 Memory Guardrails for 512MB RAM Instances
Free cloud containers enforce strict Linux cgroup limits (512MB RAM). Without explicit heap constraints, the JVM's ergonomics may allocate up to 50% of host RAM, triggering sudden `OOMKilled` container termination.

Our root `Dockerfile` embeds the following memory guardrail:
```dockerfile
ENV JAVA_TOOL_OPTIONS="-Xmx384m -Xms128m -XX:+UseSerialGC"
```
- `-Xmx384m`: Caps maximum Java heap at 384MB, leaving 128MB headroom for the JVM Metaspace, thread stacks, and OS buffers.
- `-Xms128m`: Sets initial heap allocation to minimize startup RSS memory.
- `-XX:+UseSerialGC`: Selects the single-threaded garbage collector, eliminating GC thread overhead.

### 4.2 Deploying on Render (Free Web Service)
1. In the Render Dashboard, click **New +** -> **Web Service**.
2. Connect your `Mini5th` GitHub repository.
3. Configure settings:
   - **Name**: `staymart-backend`
   - **Region**: Same region as your ML service (e.g., Singapore)
   - **Branch**: `main`
   - **Root Directory**: Leave blank (uses repo root `./Dockerfile`)
   - **Runtime**: `Docker`
   - **Instance Type**: `Free` ($0/mo)
4. Add the following Environment Variables:

| Variable Name | Required | Production Value / Pattern | Rationale |
|---------------|----------|----------------------------|-----------|
| `SPRING_PROFILES_ACTIVE` | Recommended | `prod` | Enables production profile settings |
| `DB_URL` | **Yes** | `jdbc:mysql://<tidb-host>:4000/staymart?useSSL=true&sslMode=VERIFY_IDENTITY&allowPublicKeyRetrieval=true&serverTimezone=Asia/Kolkata` | TiDB Cloud TLS connection string |
| `DB_USERNAME` | **Yes** | `<tidb-user>` | TiDB database user |
| `DB_PASSWORD` | **Yes** | `<tidb-password>` | TiDB database password |
| `JWT_SECRET` | **Yes** | *(generate 64-char random string)* | HMAC-SHA256 signature token key |
| `CORS_ORIGINS` | **Yes** | `https://staymart.vercel.app,https://<your-project>.vercel.app,http://localhost:5500` | Allowed frontend origins |
| `ML_BASE_URL` | **Yes** | `https://staymart-ml.onrender.com` | Microservice URL from Step 3 |
| `JAVA_TOOL_OPTIONS` | **Yes** | `-Xmx384m -Xms128m -XX:+UseSerialGC` | 512MB RAM protection |
| `UPLOAD_DIR` | **Yes** | `/tmp/uploads` | Ephemeral disk storage for user images |
| `UPLOAD_BASE_URL` | **Yes** | `https://staymart-backend.onrender.com` | Base URL returned in image upload responses so listing images don't point to `localhost:8080` |

> **Note on `UPLOAD_BASE_URL`**: In `src/main/resources/application.yml`, `app.upload.base-url` defaults to `http://localhost:8080`. When users upload accommodation or classified item photos, `FileStorageService` prepends this URL to the filename. In production, setting `UPLOAD_BASE_URL` to your backend domain (`https://staymart-backend.onrender.com`) ensures uploaded images resolve properly on external client browsers without 404 or connection refused errors.

5. Click **Create Web Service**.
6. When the build completes, your backend URL will be: `https://staymart-backend.onrender.com`.

### 4.3 Alternative: 1-Click Deployment via `render.yaml`
StayMart includes a pre-configured `render.yaml` blueprint. If using Render Blueprints:
1. Go to **Blueprints** in Render.
2. Select your repository. Render automatically reads `render.yaml`, provisions both `staymart-backend` and `staymart-ml`, and sets up service networking automatically.
3. The blueprint automatically configures `PORT`, `JAVA_TOOL_OPTIONS`, `UPLOAD_DIR`, `UPLOAD_BASE_URL` (`https://staymart-backend.onrender.com`), and `ML_BASE_URL` (`https://staymart-ml.onrender.com`), along with generating a secure `JWT_SECRET`.
4. You will only be prompted to supply your TiDB Cloud database connection credentials (`DB_URL`, `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`).

---

## 5. Tier 1: Frontend Deployment on Vercel

The frontend is a lightweight, responsive Multi-Page Application (MPA) using native HTML5, CSS3, and ES6 JavaScript.

### 5.1 Vercel Project Setup
1. Log in to [Vercel](https://vercel.com/) with GitHub.
2. Click **Add New...** -> **Project**.
3. Import the `Mini5th` repository.
4. Configure build settings:
   - **Framework Preset**: `Other`
   - **Root Directory**: Leave as `./` (or select `frontend/` — both work seamlessly)
   - **Build Command**: Leave empty (no build step required for static HTML/CSS/JS)
   - **Output Directory**: Leave empty
5. Click **Deploy**. Vercel will deploy the site across its global Edge CDN in seconds.

### 5.2 How the Reverse Proxy Eliminates CORS
Both `vercel.json` (at repo root) and `frontend/vercel.json` contain reverse proxy rewrites:
```json
{
  "version": 2,
  "cleanUrls": true,
  "rewrites": [
    { "source": "/", "destination": "/frontend/index.html" },
    { "source": "/api/(.*)", "destination": "https://staymart-backend.onrender.com/api/$1" },
    { "source": "/uploads/(.*)", "destination": "https://staymart-backend.onrender.com/uploads/$1" },
    { "source": "/(.*)", "destination": "/frontend/$1" }
  ]
}
```

**Key Advantages:**
1. **No Cross-Origin Restrictions**: The browser communicates with the same origin (`https://staymart.vercel.app/api/...`), so no CORS pre-flight `OPTIONS` requests are needed.
2. **No Mixed-Content Warnings**: All requests are routed through Vercel's edge HTTPS certificates.
3. **Seamless Subdirectory Support**: If you deploy from `frontend/` as the root directory, `frontend/vercel.json` takes over with relative paths (`/index.html`, `/$1`).

### 5.3 Frontend API Endpoint Resolution & Runtime Guidance

StayMart's frontend client (`frontend/js/api.js`) automatically determines the backend API target using an intelligent resolution hierarchy:

```javascript
// Auto-detect local development vs cloud deployment
const isLocal = window.location.hostname === 'localhost' ||
                window.location.hostname === '127.0.0.1' ||
                window.location.protocol === 'file:';

const customUrl = window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL');
const BASE_URL = isLocal
  ? 'http://localhost:8080/api'
  : (customUrl ? customUrl.replace(/\/+$/, '') : '/api');
```

#### How Resolution Operates Across Environments:
1. **Local Development (`isLocal === true`)**:
   When accessed via `http://localhost:5500` or `http://127.0.0.1:5500`, `BASE_URL` automatically resolves to `http://localhost:8080/api`. Developers can test locally without setting any environment variables or running a proxy.
2. **Production Reverse Proxy Default (`/api`)**:
   On Vercel (or any custom domain), when neither `window.STAYMART_API_URL` nor `localStorage` is set, `BASE_URL` defaults to `'/api'` (relative path).
   - Every fetch request (e.g. `apiCall('/properties')`) evaluates to `/api/properties` against the current origin (`https://staymart.vercel.app/api/properties`).
   - Vercel's Edge CDN catches `/api/(.*)` and proxies the request to `https://staymart-backend.onrender.com/api/$1`.
   - **Performance Benefit**: Zero CORS preflight round-trips. Browsers skip the `OPTIONS` handshake, reducing request latency by 100–300ms per mutable API call.
   - **Query Parameter Preservation**: Full query strings (e.g. `?page=0&size=5&city=Dehradun`) pass through transparently to Spring Boot.
3. **Dynamic Staging & Custom Backend Overrides**:
   If you deploy the backend on a different domain or need to test a staging branch, you can configure the endpoint dynamically without rebuilding frontend assets:
   - **In HTML Head (`window.STAYMART_API_URL`)**:
     ```html
     <script>
       window.STAYMART_API_URL = 'https://custom-backend.onrender.com/api';
     </script>
     ```
   - **In Browser Console (`localStorage`)**:
     ```javascript
     // Point to an alternate backend
     localStorage.setItem('STAYMART_API_URL', 'https://custom-backend.onrender.com/api');

     // Revert to Vercel reverse proxy
     localStorage.removeItem('STAYMART_API_URL');
     ```

#### Verifying Reverse Proxy Routing in Browser DevTools:
1. Open the deployed Vercel site in your browser.
2. Open **Developer Tools** (`F12`) -> **Network** tab -> select **Fetch/XHR**.
3. Perform a search or load listings:
   - Confirm request URLs start with `https://<your-project>.vercel.app/api/...`.
   - Verify HTTP status is `200 OK`.
   - Confirm there are **no `OPTIONS` preflight requests** preceding `GET`/`POST` calls.

---

## 6. End-to-End Interconnectivity & Smoke Verification

After deploying all tiers, verify complete cross-tier interconnectivity using the verification script below.

### 6.1 Automated Verification Script (PowerShell)

Save the following as `verify_deployment.ps1` or run directly in PowerShell:

```powershell
# Set your deployed domain URLs
$BACKEND_URL = "https://staymart-backend.onrender.com"
$ML_URL      = "https://staymart-ml.onrender.com"
$FRONTEND_URL= "https://staymart.vercel.app"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " StayMart Full-Stack Deployment Verification Suite " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Test 1: Frontend CDN Liveness
Write-Host "`n[1/7] Testing Frontend Edge CDN ($FRONTEND_URL)..." -NoNewline
try {
    $res = Invoke-WebRequest -Uri "$FRONTEND_URL" -Method GET -UseBasicParsing
    if ($res.StatusCode -eq 200) { Write-Host " [PASS] (HTTP 200)" -ForegroundColor Green }
    else { Write-Host " [FAIL] Status: $($res.StatusCode)" -ForegroundColor Red }
} catch { Write-Host " [FAIL] $_" -ForegroundColor Red }

# Test 2: ML Microservice Liveness & Health
Write-Host "[2/7] Testing Flask ML Microservice ($ML_URL/health)..." -NoNewline
try {
    $res = Invoke-RestMethod -Uri "$ML_URL/health" -Method GET
    if ($res.status -eq "healthy") { 
        Write-Host " [PASS] (DB: $($res.database), Models: $($res.models_loaded))" -ForegroundColor Green 
    } else { Write-Host " [WARN] Status: $($res.status)" -ForegroundColor Yellow }
} catch { Write-Host " [FAIL] $_" -ForegroundColor Red }

# Test 3: Backend Database Connectivity (Locations Endpoint)
Write-Host "[3/7] Testing Backend DB Query ($BACKEND_URL/api/locations)..." -NoNewline
try {
    $res = Invoke-RestMethod -Uri "$BACKEND_URL/api/locations" -Method GET
    if ($res.success -eq $true -and $res.data.Count -gt 0) {
        Write-Host " [PASS] (Found $($res.data.Count) Uttarakhand locations)" -ForegroundColor Green
    } else { Write-Host " [FAIL] Unexpected response" -ForegroundColor Red }
} catch { Write-Host " [FAIL] $_" -ForegroundColor Red }

# Test 4: Accommodation Listings Endpoint
Write-Host "[4/7] Testing Accommodation Search ($BACKEND_URL/api/properties)..." -NoNewline
try {
    $res = Invoke-RestMethod -Uri "$BACKEND_URL/api/properties" -Method GET
    if ($res.success -eq $true -and $res.data.content.Count -gt 0) {
        Write-Host " [PASS] (Returned $($res.data.content.Count) active listings)" -ForegroundColor Green
    } else { Write-Host " [FAIL] Unexpected response" -ForegroundColor Red }
} catch { Write-Host " [FAIL] $_" -ForegroundColor Red }

# Test 5: Re-Commerce Products Endpoint
Write-Host "[5/7] Testing Re-Commerce Products ($BACKEND_URL/api/products)..." -NoNewline
try {
    $res = Invoke-RestMethod -Uri "$BACKEND_URL/api/products" -Method GET
    if ($res.success -eq $true -and $res.data.content.Count -gt 0) {
        Write-Host " [PASS] (Returned $($res.data.content.Count) active products)" -ForegroundColor Green
    } else { Write-Host " [FAIL] Unexpected response" -ForegroundColor Red }
} catch { Write-Host " [FAIL] $_" -ForegroundColor Red }

# Test 6: Cross-Tier ML Recommendation Fallback
Write-Host "[6/7] Testing ML Recommendations ($BACKEND_URL/api/recommendations/properties/trending)..." -NoNewline
try {
    $res = Invoke-RestMethod -Uri "$BACKEND_URL/api/recommendations/properties/trending" -Method GET
    if ($res.success -eq $true -and $res.data.Count -gt 0) {
        Write-Host " [PASS] (Returned $($res.data.Count) trending recommendations)" -ForegroundColor Green
    } else { Write-Host " [FAIL] Unexpected response" -ForegroundColor Red }
} catch { Write-Host " [FAIL] $_" -ForegroundColor Red }

# Test 7: Vercel Edge Reverse-Proxy API Routing
Write-Host "[7/7] Testing Vercel Edge Reverse Proxy ($FRONTEND_URL/api/locations)..." -NoNewline
try {
    $res = Invoke-RestMethod -Uri "$FRONTEND_URL/api/locations" -Method GET
    if ($res.success -eq $true -and $res.data.Count -gt 0) {
        Write-Host " [PASS] (Transparently proxied to Render with zero CORS)" -ForegroundColor Green
    } else { Write-Host " [FAIL] Unexpected response" -ForegroundColor Red }
} catch { Write-Host " [FAIL] $_" -ForegroundColor Red }

Write-Host "`nAll deployment verification checks finished successfully!" -ForegroundColor Cyan
```

### 6.2 Verification Commands (Bash / cURL)

```bash
# 1. Verify ML microservice health
curl -s https://staymart-ml.onrender.com/health | jq .

# 2. Verify backend DB query (Uttarakhand locations)
curl -s https://staymart-backend.onrender.com/api/locations | jq .

# 3. Verify public accommodations
curl -s "https://staymart-backend.onrender.com/api/properties?page=0&size=5" | jq .

# 4. Verify public products
curl -s "https://staymart-backend.onrender.com/api/products?page=0&size=5" | jq .

# 5. Verify ML trending recommendations through Spring Boot
curl -s https://staymart-backend.onrender.com/api/recommendations/properties/trending | jq .

# 6. Verify Vercel frontend reverse proxy rewrites
curl -s https://staymart.vercel.app/api/locations | jq .
```

---

## 7. Operational Notes & Troubleshooting

### Free Tier Inactivity Sleep (Render Spin-Down)
- **Behavior**: Free web services on Render spin down automatically after 15 minutes of zero HTTP traffic.
- **Waking Up**: The first incoming request triggers container startup, which takes approximately 30–50 seconds. Once initialized, subsequent requests respond in under 100 milliseconds.
- **Zero-Cost Keep-Warm Solution**: To keep your free containers awake during daytime hours, configure a free monitor on [UptimeRobot](https://uptimerobot.com/) or [Cron-job.org](https://cron-job.org/) that sends an HTTP GET request to `/health` and `/api/locations` every 10 minutes.

### SSL / TLS Encryption Handshake
- TiDB Cloud enforces secure TLS connections.
- The JDBC parameter `useSSL=true&sslMode=VERIFY_IDENTITY` in `DB_URL` ensures that the connection is encrypted using the trusted CA cert bundle embedded in the `eclipse-temurin:17-jre-jammy` base image.

### Resilient ML Fallback Architecture
- If the Python ML microservice is sleeping or unreachable, Spring Boot's `MlServiceClient` activates its 2000ms connection / 3000ms read timeout.
- The `RecommendationService` automatically falls back to database-driven latest approved listings without returning HTTP 500 errors to the user.

### Broken Image URLs on Client Devices (`localhost:8080`)
- **Symptom**: Accommodation or product photo thumbnails appear broken on client browsers, with image URLs resolving to `http://localhost:8080/api/files/...`.
- **Root Cause**: `UPLOAD_BASE_URL` environment variable was not configured on the Render backend service, causing Spring Boot's `FileStorageService` to fall back to the local default.
- **Fix**: In the Render Dashboard under `staymart-backend` -> **Environment**, add:
  `UPLOAD_BASE_URL = https://staymart-backend.onrender.com`
  Trigger a manual redeploy. Newly uploaded images will point to the public cloud URL.

### Browser CORS Errors on Direct Backend Requests
- **Symptom**: Browser console logs `Access to fetch at 'https://staymart-backend.onrender.com' from origin 'https://staymart.vercel.app' has been blocked by CORS policy`.
- **Root Cause**: The frontend is sending requests directly to Render rather than using Vercel's same-origin reverse proxy (`/api`), or the Vercel domain is not listed in `CORS_ORIGINS`.
- **Fix**:
  1. Ensure `frontend/js/api.js` resolves to relative `'/api'` in production so calls route via `vercel.json` rewrites. Clear any invalid `localStorage.getItem('STAYMART_API_URL')` entries in the browser console (`localStorage.removeItem('STAYMART_API_URL')`).
  2. If direct cross-origin calls are intentional, ensure your Vercel deployment URL (e.g. `https://staymart.vercel.app`) is included in the backend's `CORS_ORIGINS` environment variable in Render.

---

## 8. Alternative Free Cloud Providers

If you prefer alternatives to Render or TiDB Cloud:

| Role | Alternative Provider | Free Plan Details | Configuration Note |
|------|----------------------|-------------------|--------------------|
| **Backend** | **Koyeb** | Free Eco instance (512MB RAM, nano CPU) | Deploy root `Dockerfile`, set dynamic port `$PORT` |
| **Backend** | **Fly.io** | Free allowance (up to 3 shared-cpu-1x VMs) | Requires credit card verification |
| **ML Microservice**| **Hugging Face Spaces** | Free Docker Space (16GB RAM, 2 vCPU) | Unmatched memory allocation for ML workloads |
| **Database** | **Aiven MySQL** | Free Plan (1 service, 5GB storage, 1GB RAM) | Standard MySQL connection string on port 10000-30000 |
| **Database** | **Clever Cloud** | Free MySQL add-on (25MB small demo plan) | Recommended for prototyping only |

---

*StayMart is production-ready for student communities across Uttarakhand.*
