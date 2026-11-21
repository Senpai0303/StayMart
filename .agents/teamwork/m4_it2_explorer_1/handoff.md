# Milestone 4 Iteration 2 Investigation Report: Render Blueprint & Container Networking Strategy

**Investigator**: Milestone 4 Iteration 2 Explorer 1 (Blueprint & Container Networking Investigator)  
**Date**: November 2, 2026  
**Working Directory**: `d:\Mini5th\.agents\teamwork\m4_it2_explorer_1\`  
**Target File**: `render.yaml` (and companion docs `DEPLOYMENT.md`, `frontend/js/api.js`)  
**Status**: COMPLETE (Hard Handoff)

---

## 1. Observation

### 1.1 Verbatim Code Locations & Discrepancies

#### A. Missing `UPLOAD_BASE_URL` in `render.yaml` and `DEPLOYMENT.md`
- In `src/main/resources/application.yml` lines 44–46:
  ```yaml
  44:   upload:
  45:     dir: ${UPLOAD_DIR:uploads}
  46:     base-url: ${UPLOAD_BASE_URL:http://localhost:8080}
  ```
- In `src/main/java/com/staymart/service/FileStorageService.java` lines 30–33 and line 64:
  ```java
  30: public FileStorageService(@Value("${app.upload.dir}") String directory,
  31:                           @Value("${app.upload.base-url}") String baseUrl) {
  32:     this.uploadDir = Paths.get(directory).toAbsolutePath().normalize();
  33:     this.baseUrl = baseUrl.endsWith("/") ? baseUrl.substring(0, baseUrl.length() - 1) : baseUrl;
  ...
  64:     return baseUrl + "/api/files/" + filename;
  ```
- In `src/main/java/com/staymart/controller/FileController.java` lines 33–38:
  ```java
  33: @PostMapping("/upload")
  34: @Operation(summary = "Upload an image, returns the public URL", security = @SecurityRequirement(name = "bearerAuth"))
  35: public ApiResponse<Map<String, String>> upload(@RequestParam("file") MultipartFile file) {
  36:     String url = fileStorageService.store(file);
  37:     return ApiResponse.ok(Map.of("url", url));
  38: }
  ```
- In `README.md` line 265:
  ```markdown
  | `UPLOAD_BASE_URL` | `http://localhost:8080` | Base URL for uploaded files |
  ```
- In current `render.yaml` lines 12–36 (`staymart-backend`):
  ```yaml
  12:     envVars:
  13:       - key: PORT
  14:         value: 8080
  15:       - key: SPRING_PROFILES_ACTIVE
  16:         value: prod
  17:       - key: JAVA_TOOL_OPTIONS
  18:         value: "-Xmx384m -Xms128m -XX:+UseSerialGC"
  19:       - key: DB_URL
  20:         sync: false
  21:       - key: DB_USERNAME
  22:         sync: false
  23:       - key: DB_PASSWORD
  24:         sync: false
  25:       - key: JWT_SECRET
  26:         generateValue: true
  27:       - key: CORS_ORIGINS
  28:         value: "https://staymart.vercel.app,https://staymart-frontend.vercel.app,http://localhost:5500,http://127.0.0.1:5500"
  29:       - key: ML_BASE_URL
  30:         fromService:
  31:           type: web
  32:           name: staymart-ml
  33:           property: host
  34:       - key: UPLOAD_DIR
  35:         value: /tmp/uploads
  ```
  **Direct Observation**: `UPLOAD_BASE_URL` is completely absent from `render.yaml` and `DEPLOYMENT.md` Table 4.2. In production, image uploads construct URLs with `http://localhost:8080/api/files/<uuid>.<ext>`, causing client browsers to suffer `net::ERR_CONNECTION_REFUSED` and render broken images.

---

#### B. Defective `ML_BASE_URL` in `render.yaml`
- In current `render.yaml` lines 29–33:
  ```yaml
  29:       - key: ML_BASE_URL
  30:         fromService:
  31:           type: web
  32:           name: staymart-ml
  33:           property: host
  ```
- In `src/main/java/com/staymart/service/MlServiceClient.java` lines 27–34:
  ```java
  27: public MlServiceClient(RestClient.Builder builder,
  28:                        ObjectMapper objectMapper,
  29:                        @Value("${app.ml.base-url:http://localhost:5000}") String mlBaseUrl) {
  30:     if (builder != null) {
  31:         SimpleClientHttpRequestFactory requestFactory = new SimpleClientHttpRequestFactory();
  32:         requestFactory.setConnectTimeout(ML_CONNECT_TIMEOUT_MS);
  33:         requestFactory.setReadTimeout(ML_READ_TIMEOUT_MS);
  34:         this.client = builder.baseUrl(mlBaseUrl).requestFactory(requestFactory).build();
  ```
- In `DEPLOYMENT.md` Table 4.2 line 190:
  ```markdown
  | `ML_BASE_URL` | `https://staymart-ml.onrender.com` | Microservice URL from Step 3 |
  ```
  **Direct Observation**: Render Blueprint `property: host` produces the raw host string without protocol prefix (`staymart-ml` or `staymart-ml.onrender.com`). Spring Boot 3 `RestClient.baseUrl(...)` requires an absolute URI; resolving paths against a scheme-less base URL throws `IllegalArgumentException: URI is not absolute`. Furthermore, Render Free tier explicitly disables private DNS resolution between web services, requiring communication over public HTTPS. Manual deployment in `DEPLOYMENT.md` line 190 already specifies `https://staymart-ml.onrender.com`, but `render.yaml` failed to reflect this.

---

#### C. Frontend API Fallback Typo in `frontend/js/api.js`
- In `frontend/js/api.js` lines 2–5:
  ```javascript
  2: const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  3: const BASE_URL = isLocal
  4:   ? 'http://localhost:8080/api'
  5:   : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || 'https://staymart.onrender.com/api');
  ```
- In `vercel.json` lines 6–7:
  ```json
  6:     { "source": "/api/(.*)", "destination": "https://staymart-backend.onrender.com/api/$1" },
  7:     { "source": "/uploads/(.*)", "destination": "https://staymart-backend.onrender.com/uploads/$1" },
  ```
  **Direct Observation**: Line 5 contains `https://staymart.onrender.com/api` (missing `-backend`). Furthermore, sending direct absolute requests from Vercel bypasses Vercel's edge reverse proxy rewrites, incurring CORS preflight latency.

---

### 1.2 Comprehensive Environment Variable Inventory & Audit Matrix

#### Spring Boot Backend (`staymart-backend` in `render.yaml` vs `application.yml` vs `DEPLOYMENT.md`)

| Key in `application.yml` | `application.yml` Default | `render.yaml` (Current) | `DEPLOYMENT.md` Table 4.2 | Status / Alignment |
|---|---|---|---|---|
| `PORT` | 8080 (line 31) | `value: 8080` (line 14) | Documented (implicit/Render) | **MATCH** |
| `SPRING_PROFILES_ACTIVE` | dev (line 5) | `value: prod` (line 16) | `prod` (line 184) | **MATCH** |
| `JAVA_TOOL_OPTIONS` | (in Dockerfile line 24) | `value: "-Xmx384m -Xms128m -XX:+UseSerialGC"` | `-Xmx384m -Xms128m -XX:+UseSerialGC` | **MATCH** (512MB RAM guardrail) |
| `DB_URL` | `${DB_URL:...}` (line 7) | `sync: false` (line 20) | `jdbc:mysql://<tidb-host>:4000/staymart?...` | **MATCH** (prompted at deploy) |
| `DB_USERNAME` | `${DB_USERNAME:root}` (line 8) | `sync: false` (line 22) | `<tidb-user>` (line 186) | **MATCH** |
| `DB_PASSWORD` | `${DB_PASSWORD:root}` (line 9) | `sync: false` (line 24) | `<tidb-password>` (line 187) | **MATCH** |
| `JWT_SECRET` | `${JWT_SECRET:...}` (line 42) | `generateValue: true` (line 26) | `(generate 64-char random string)` | **MATCH** (auto-generated) |
| `CORS_ORIGINS` | `${CORS_ORIGINS:...}` (line 48) | `value: "https://staymart.vercel.app,https://staymart-frontend.vercel.app,http://localhost:5500,http://127.0.0.1:5500"` | `https://staymart.vercel.app,https://<your-project>.vercel.app,http://localhost:5500` | **MATCH** |
| `ML_BASE_URL` | `${ML_BASE_URL:http://localhost:5000}` (line 50) | `fromService: ... property: host` (lines 29–33) | `https://staymart-ml.onrender.com` (line 190) | **FIX**: Set `value: "https://staymart-ml.onrender.com"` |
| `UPLOAD_DIR` | `${UPLOAD_DIR:uploads}` (line 45) | `value: /tmp/uploads` (line 35) | `/tmp/uploads` (line 192) | **MATCH** |
| `UPLOAD_BASE_URL` | `${UPLOAD_BASE_URL:http://localhost:8080}` (line 46) | **MISSING** | **MISSING** | **FIX**: Add `value: "https://staymart-backend.onrender.com"` |
| `SEED_ADMIN_EMAIL` | `${SEED_ADMIN_EMAIL:admin@staymart.com}` (line 53) | Omitted (uses default fallback) | Omitted (uses default fallback) | **OPTIONAL MATCH** |
| `SEED_ADMIN_PASSWORD` | `${SEED_ADMIN_PASSWORD:Admin@123}` (line 54) | Omitted (uses default fallback) | Omitted (uses default fallback) | **OPTIONAL MATCH** |

#### Flask ML Recommendation Service (`staymart-ml` in `render.yaml` vs `ml-service/config.py` vs `DEPLOYMENT.md`)

| Key in `config.py` | `config.py` Default | `render.yaml` (Current) | `DEPLOYMENT.md` Table 3.1 | Status / Alignment |
|---|---|---|---|---|
| `PORT` | (in Dockerfile: 5000) | `value: 5000` (line 50) | `5000` (line 132) | **MATCH** |
| `DB_HOST` | `os.getenv('DB_HOST', 'localhost')` | `sync: false` (line 52) | `<tidb-host>` (line 133) | **MATCH** (prompted at deploy) |
| `DB_PORT` | `int(os.getenv('DB_PORT', '3306'))` | `value: 4000` (line 54) | `4000` (line 134) | **MATCH** (TiDB port 4000) |
| `DB_USERNAME` | `os.getenv('DB_USERNAME', ...)` | `sync: false` (line 56) | `<tidb-user>` (line 135) | **MATCH** |
| `DB_PASSWORD` | `os.getenv('DB_PASSWORD', 'root')` | `sync: false` (line 58) | `<tidb-password>` (line 136) | **MATCH** |
| `DB_NAME` | `os.getenv('DB_NAME', ...)` | `value: staymart` (line 60) | `staymart` (line 137) | **MATCH** |
| `DEFAULT_CITY` | `os.getenv('DEFAULT_CITY', 'Dehradun')` | `value: Dehradun` (line 62) | `Dehradun` (line 138) | **MATCH** |
| `MIN_INTERACTIONS_FOR_CF` | `5` | Omitted (uses default 5) | Omitted (uses default 5) | **MATCH** |
| `TRENDING_DAYS` | `7` | Omitted (uses default 7) | Omitted (uses default 7) | **MATCH** |
| `TIME_DECAY_FACTOR` | `0.9` | Omitted (uses default 0.9) | Omitted (uses default 0.9) | **MATCH** |

---

### 1.3 Test Suite Baseline Execution Results

All existing regression suites were directly executed and verified:
1. **JUnit 5 Backend Suite**: `python scripts/run_backend_tests.py` -> **13/13 PASS**, Exit code 0.
2. **Mobile Viewport Suite**: `node scripts/run_viewport_tests.js` -> **30/30 PASS**, Exit code 0.
3. **Navigation & Redirect Suite**: `python scripts/verify_m1_navigation.py` -> **8/8 Suites PASS**, Exit code 0.
4. **Adversarial Audit Harness**: `python scripts/test_m4_adversarial_audit.py` -> Exit code 0 (highlighted missing `UPLOAD_BASE_URL` in `render.yaml` and `DEPLOYMENT.md`).
5. **Blueprint YAML Parser Test**: `python .agents/teamwork/m4_it2_explorer_1/validate_blueprint.py` -> Exit code 0, 100% valid YAML structure.

---

## 2. Logic Chain

1. **Step 1 (From Observation 1.1.A)**:
   - In `application.yml`, line 46 defines `base-url: ${UPLOAD_BASE_URL:http://localhost:8080}`.
   - In `FileStorageService.java`, line 64 formats uploaded image URLs as `return baseUrl + "/api/files/" + filename`.
   - In `render.yaml`, `UPLOAD_BASE_URL` was not supplied under `staymart-backend`.
   - Therefore, Spring Boot on Render defaults to `http://localhost:8080`.
   - When any listing with room or product photos is created in production, the image URLs saved into the database and sent to clients begin with `http://localhost:8080`.
   - Remote mobile and desktop browsers fail to connect to `localhost:8080`, breaking all user-uploaded listing images.
   - *Inference*: `UPLOAD_BASE_URL` must be explicitly configured in `render.yaml` as `value: "https://staymart-backend.onrender.com"`, and documented in `DEPLOYMENT.md` Table 4.2.

2. **Step 2 (From Observation 1.1.B)**:
   - In `render.yaml`, lines 29–33 set `ML_BASE_URL` using `fromService: { property: host }`.
   - Render Blueprint specifications state that `property: host` produces the bare host name without any scheme prefix.
   - In `MlServiceClient.java`, line 34 instantiates `RestClient` using `builder.baseUrl(mlBaseUrl)`.
   - Spring Framework 6.1 `RestClient` enforces absolute URIs with `http://` or `https://` schemes. When given `staymart-ml` or `staymart-ml.onrender.com`, HTTP request dispatch throws `IllegalArgumentException: URI is not absolute`.
   - Render Free tier strictly prohibits private inter-service networking between web services. Internal DNS for `staymart-ml` does not resolve across free web services.
   - In `DEPLOYMENT.md` Table 4.2 line 190, the manual deployment guide already documents `ML_BASE_URL: https://staymart-ml.onrender.com`.
   - *Inference*: In `render.yaml`, lines 29–33 must be replaced with `value: "https://staymart-ml.onrender.com"`. This guarantees an absolute HTTPS URI, aligns with Render Free tier networking rules, and eliminates the blueprint discrepancy.

3. **Step 3 (From Observation 1.1.C & 1.2)**:
   - In `frontend/js/api.js`, line 5 references `'https://staymart.onrender.com/api'`, which is missing `-backend`.
   - In `vercel.json`, reverse proxy rewrite rule `{ "source": "/api/(.*)", "destination": "https://staymart-backend.onrender.com/api/$1" }` is designed to route requests from the same origin to Render, completely eliminating CORS preflight overhead.
   - By aligning `frontend/js/api.js` to fallback to `'/api'` or `'https://staymart-backend.onrender.com/api'`, requests will either flow through the Vercel CDN reverse proxy or directly to the exact Render backend domain.
   - *Inference*: Updating `frontend/js/api.js` ensures that production deployments through Vercel take full advantage of edge proxy rewrites.

4. **Step 4 (From Observation 1.2)**:
   - All other 8 Spring Boot environment variables in `render.yaml` (`PORT`, `SPRING_PROFILES_ACTIVE`, `JAVA_TOOL_OPTIONS`, `DB_URL`, `DB_USERNAME`, `DB_PASSWORD`, `JWT_SECRET`, `CORS_ORIGINS`, `UPLOAD_DIR`) perfectly match `application.yml` and `DEPLOYMENT.md`.
   - All 7 ML service environment variables in `render.yaml` (`PORT`, `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME`, `DEFAULT_CITY`) perfectly match `ml-service/config.py` and `DEPLOYMENT.md`.
   - *Inference*: Applying the two precise additions to `staymart-backend` in `render.yaml` will achieve 100% full-stack configuration consistency.

---

## 3. Caveats

1. **Simulation vs Live Cloud Infrastructure**: Verification was conducted locally using strict YAML schema parsers, regex AST inspectors, Spring Boot JUnit suites, and Chromium headless viewport tests. While the configuration matches Render's Blueprint specification, physical Render and TiDB accounts were not provisioned during this read-only investigation.
2. **Render Free Tier Cold Starts**: On Render's Free tier, services spin down after 15 minutes of inactivity. When a request wakes up `staymart-ml`, the first request may take 30–50 seconds. Spring Boot's `MlServiceClient` handles this gracefully: connect timeout is 2000ms, read timeout is 3000ms, and `RecommendationService` automatically falls back to database-driven category/location matching without throwing HTTP 500 errors.
3. **Container Ephemeral Storage**: On free cloud tiers, `/tmp/uploads` is ephemeral. Uploaded files persist across requests while the container is alive, but will reset upon container restart or redeploy. This is standard and expected for free-tier deployments and satisfies all functional criteria without requiring paid AWS S3 credentials.

---

## 4. Conclusion & Concrete Diff Recommendations

The root causes identified by Challenger 2 have been verified and pinpointed to exact lines. The following concrete diffs are recommended for the implementation worker:

### 4.1 Primary Fix: `render.yaml`

```diff
--- a/render.yaml
+++ b/render.yaml
@@ -28,8 +28,8 @@ services:
         value: "https://staymart.vercel.app,https://staymart-frontend.vercel.app,http://localhost:5500,http://127.0.0.1:5500"
       - key: ML_BASE_URL
-        fromService:
-          type: web
-          name: staymart-ml
-          property: host
+        value: "https://staymart-ml.onrender.com"
       - key: UPLOAD_DIR
         value: /tmp/uploads
+      - key: UPLOAD_BASE_URL
+        value: "https://staymart-backend.onrender.com"
```

#### Full Resulting `staymart-backend` Service Block in `render.yaml`:
```yaml
services:
  # -------------------------------------------------------------
  # Tier 2: Spring Boot Backend REST API
  # -------------------------------------------------------------
  - type: web
    name: staymart-backend
    runtime: docker
    dockerfilePath: ./Dockerfile
    plan: free
    region: singapore
    healthCheckPath: /api/properties
    envVars:
      - key: PORT
        value: 8080
      - key: SPRING_PROFILES_ACTIVE
        value: prod
      - key: JAVA_TOOL_OPTIONS
        value: "-Xmx384m -Xms128m -XX:+UseSerialGC"
      - key: DB_URL
        sync: false
      - key: DB_USERNAME
        sync: false
      - key: DB_PASSWORD
        sync: false
      - key: JWT_SECRET
        generateValue: true
      - key: CORS_ORIGINS
        value: "https://staymart.vercel.app,https://staymart-frontend.vercel.app,http://localhost:5500,http://127.0.0.1:5500"
      - key: ML_BASE_URL
        value: "https://staymart-ml.onrender.com"
      - key: UPLOAD_DIR
        value: /tmp/uploads
      - key: UPLOAD_BASE_URL
        value: "https://staymart-backend.onrender.com"
```

---

### 4.2 Companion Fix: `DEPLOYMENT.md` Table 4.2

Add `UPLOAD_BASE_URL` directly after `UPLOAD_DIR` in Table 4.2:

```diff
--- a/DEPLOYMENT.md
+++ b/DEPLOYMENT.md
@@ -192,3 +192,4 @@
 | `JAVA_TOOL_OPTIONS` | `-Xmx384m -Xms128m -XX:+UseSerialGC` | 512MB RAM protection |
 | `UPLOAD_DIR` | `/tmp/uploads` | Ephemeral disk storage for user images |
+| `UPLOAD_BASE_URL` | `https://staymart-backend.onrender.com` | Base URL returned in image upload responses to avoid localhost fallback |
```

---

### 4.3 Recommended Companion Fix: `frontend/js/api.js`

Update line 5 to fix the service name typo and leverage Vercel reverse proxy rewrites:

```diff
--- a/frontend/js/api.js
+++ b/frontend/js/api.js
@@ -2,5 +2,5 @@
 const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
 const BASE_URL = isLocal
   ? 'http://localhost:8080/api'
-  : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || 'https://staymart.onrender.com/api');
+  : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || '/api');
```
*(Alternatively, if external static hosting without reverse proxy is targeted: `window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || 'https://staymart-backend.onrender.com/api'`)*

---

## 5. Verification Method

To independently verify the implementation after applying the diffs:

1. **Verify YAML Syntax and Blueprint Schema**:
   ```powershell
   python -c "import yaml; d = yaml.safe_load(open('render.yaml')); b = {e['key']: e.get('value') for e in d['services'][0]['envVars']}; assert b['UPLOAD_BASE_URL'] == 'https://staymart-backend.onrender.com'; assert b['ML_BASE_URL'] == 'https://staymart-ml.onrender.com'; print('render.yaml Blueprint Verification: PASS')"
   ```
   *Expected Output*: `render.yaml Blueprint Verification: PASS`

2. **Verify Adversarial Audit Compliance**:
   ```powershell
   python -c "content = open('render.yaml').read(); assert 'UPLOAD_BASE_URL' in content, 'UPLOAD_BASE_URL missing from render.yaml'"
   python -c "content = open('DEPLOYMENT.md').read(); assert 'UPLOAD_BASE_URL' in content, 'UPLOAD_BASE_URL missing from DEPLOYMENT.md'"
   python scripts/test_m4_adversarial_audit.py
   ```
   *Expected Output*: Exit code 0, with `UPLOAD_BASE_URL` showing `in_render_yaml: true` and `in_deployment_md: true`.

3. **Run Regression Verification Suites**:
   ```powershell
   python scripts/run_backend_tests.py
   node scripts/run_viewport_tests.js
   python scripts/verify_m1_navigation.py
   ```
   *Expected Output*: All 3 test suites exit with code 0.

---

### Invalidation Conditions
This report is invalidated if:
1. Render Blueprint adds automatic scheme resolution for `fromService: ... property: host`.
2. The backend service name in `render.yaml` is changed from `staymart-backend` to a different slug.
3. Render Free tier begins supporting private internal DNS networking between separate web services without requiring public HTTPS endpoints.
