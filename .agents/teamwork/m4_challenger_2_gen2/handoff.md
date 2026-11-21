# Milestone 4 Adversarial Stress Report: Environment, Cross-Tier Interconnect & Networking Audit

**Challenger**: Milestone 4 Challenger 2 (Environment & Cross-Tier Interconnect, Generation 2)  
**Date**: November 2, 2026  
**Working Directory**: `d:\Mini5th\.agents\teamwork\m4_challenger_2_gen2\`  
**Target Milestone**: Milestone 4 (Free Full-Stack Deployment Configurations & Documentation)  
**Final Verdict**: **REQUEST_CHANGES**

---

## 1. Observation

### 1.1 Regression Test Suite Execution Results
All three regression suites requested in the challenge dispatch were executed directly:

1. **Mobile Viewport Test Suite**:
   - Command: `node scripts/run_viewport_tests.js`
   - Result:
     ```
     Total Viewport Tests: 30 | Failures: 0
     Defects Identified: 0
     OVERALL VERDICT: APPROVE
     Command exited with code 0.
     ```
2. **Navigation, Links & DOM Interaction Suite**:
   - Command: `python scripts/verify_m1_navigation.py`
   - Result:
     ```
     Total Test Suites Passed: 8 / 7
     Total Defects Found: 0
     VERDICT: APPROVE
     Command exited with code 0.
     ```
3. **Spring Boot Backend JUnit 5 Suite**:
   - Command: `python scripts/run_backend_tests.py`
   - Result:
     ```
     [ 4 containers found / 4 successful ]
     [ 13 tests found / 13 tests started / 13 tests successful / 0 failed ]
     ALL TESTS PASSED SUCCESSFULLY!
     SUCCESS: All backend tests passed!
     Command exited with code 0.
     ```

---

### 1.2 Environment Variable Integrity Audit Comparisons

#### A. Spring Boot Properties (`src/main/resources/application.yml` vs `render.yaml` & `DEPLOYMENT.md`)
Direct code inspection and automated audit via `scripts/test_m4_adversarial_audit.py`:

| Property in `application.yml` | Line # | Present in `render.yaml`? | Present in `DEPLOYMENT.md` Table 4.2? | Status |
|-------------------------------|--------|---------------------------|---------------------------------------|--------|
| `${DB_URL}` | Line 7 | Yes (line 19) | Yes (line 185) | MATCH |
| `${DB_USERNAME}` | Line 8 | Yes (line 21) | Yes (line 186) | MATCH |
| `${DB_PASSWORD}` | Line 9 | Yes (line 23) | Yes (line 187) | MATCH |
| `${JWT_SECRET}` | Line 42 | Yes (line 25) | Yes (line 188) | MATCH |
| `${UPLOAD_DIR}` | Line 45 | Yes (line 34) | Yes (line 192) | MATCH |
| `${UPLOAD_BASE_URL}` | Line 46 | **NO (MISSING)** | **NO (MISSING)** | **DEFECT** |
| `${CORS_ORIGINS}` | Line 48 | Yes (line 27) | Yes (line 189) | MATCH |
| `${ML_BASE_URL}` | Line 50 | Yes (line 29) | Yes (line 190) | INCONSISTENCY (See 1.3) |
| `${SEED_ADMIN_EMAIL}` | Line 53 | No (default fallback) | No (default fallback) | OPTIONAL |
| `${SEED_ADMIN_PASSWORD}` | Line 54 | No (default fallback) | No (default fallback) | OPTIONAL |

Verbatim excerpt from `src/main/java/com/staymart/service/FileStorageService.java` (lines 30–33, 64):
```java
30: public FileStorageService(@Value("${app.upload.dir}") String directory,
31:                           @Value("${app.upload.base-url}") String baseUrl) {
...
64:     return baseUrl + "/api/files/" + filename;
```
When `UPLOAD_BASE_URL` is omitted, `application.yml` line 46 applies:
```yaml
base-url: ${UPLOAD_BASE_URL:http://localhost:8080}
```
In production, image upload responses return `http://localhost:8080/api/files/<uuid>.jpg`, resulting in broken images on external client browsers.

#### B. ML Microservice Properties (`ml-service/config.py` vs `render.yaml` & `DEPLOYMENT.md`)

| Property in `config.py` | Present in `render.yaml`? | Present in `DEPLOYMENT.md` Table 3.1? | Status |
|-------------------------|---------------------------|---------------------------------------|--------|
| `PORT` | Yes (line 50) | Yes (line 132) | MATCH (5000) |
| `DB_HOST` | Yes (line 51) | Yes (line 133) | MATCH |
| `DB_PORT` | Yes (line 53, value 4000) | Yes (line 134, value 4000) | MATCH |
| `DB_USERNAME` | Yes (line 55) | Yes (line 135) | MATCH |
| `DB_PASSWORD` | Yes (line 57) | Yes (line 136) | MATCH |
| `DB_NAME` | Yes (line 59) | Yes (line 137) | MATCH |
| `DEFAULT_CITY` | Yes (line 61) | Yes (line 138) | MATCH |
| `MIN_INTERACTIONS_FOR_CF` | No (default 5) | No (default 5) | MATCH (default acceptable) |
| `TRENDING_DAYS` | No (default 7) | No (default 7) | MATCH (default acceptable) |
| `TIME_DECAY_FACTOR` | No (default 0.9) | No (default 0.9) | MATCH (default acceptable) |

---

### 1.3 Cross-Tier Interconnect & Blueprint Discrepancies

1. **`render.yaml` Blueprint `ML_BASE_URL` Definition**:
   In `render.yaml` lines 29–33:
   ```yaml
         - key: ML_BASE_URL
           fromService:
             type: web
             name: staymart-ml
             property: host
   ```
   In Render's Blueprint specification, `property: host` produces the raw host (e.g., `staymart-ml` or `staymart-ml.onrender.com`) **without** a protocol scheme (`http://` or `https://`).
   In `src/main/java/com/staymart/service/MlServiceClient.java` line 34:
   ```java
   this.client = builder.baseUrl(mlBaseUrl).requestFactory(requestFactory).build();
   ```
   Spring Framework 6.1 `RestClient.baseUrl()` requires an absolute URI with a valid scheme (`http://` or `https://`). Without a scheme, URI resolution throws `IllegalArgumentException: URI is not absolute`.
   Furthermore, Render Free Web Services do not support private internal networking (`staymart-ml`). They require public HTTPS communication (`https://staymart-ml.onrender.com`).
   *Note*: `DEPLOYMENT.md` line 190 correctly documents `ML_BASE_URL: https://staymart-ml.onrender.com`, but `render.yaml` fails to match this.

2. **Frontend `frontend/js/api.js` Hardcoded Fallback Domain**:
   In `frontend/js/api.js` lines 2–5:
   ```javascript
   const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
   const BASE_URL = isLocal
     ? 'http://localhost:8080/api'
     : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || 'https://staymart.onrender.com/api');
   ```
   - In `render.yaml` line 6, the backend service is named `staymart-backend`, generating the domain `https://staymart-backend.onrender.com`.
   - In `DEPLOYMENT.md` line 195 & 227, the backend URL is `https://staymart-backend.onrender.com`.
   - `frontend/js/api.js` line 5 falls back to `'https://staymart.onrender.com/api'` (missing `-backend`).
   - More crucially, when deployed on Vercel (`window.STAYMART_API_URL` undefined), the frontend sends absolute fetch calls directly to Render rather than relative `/api`, completely bypassing Vercel reverse proxy rewrites and triggering cross-origin CORS checks.

---

### 1.4 SSL and Database Protocol Verification
1. `DEPLOYMENT.md` line 185 specifies:
   ```
   `DB_URL` | `jdbc:mysql://<tidb-host>:4000/staymart?useSSL=true&sslMode=VERIFY_IDENTITY&allowPublicKeyRetrieval=true&serverTimezone=Asia/Kolkata`
   ```
2. `DEPLOYMENT.md` lines 104–108 specify:
   ```bash
   mysql -h <tidb-host> -P 4000 -u <tidb-user> -p --ssl-mode=VERIFY_IDENTITY < database/01_schema.sql
   ```
3. `DEPLOYMENT.md` Section 7 lines 346–349 document the TLS handshake and the trusted CA cert bundle embedded in `eclipse-temurin:17-jre-jammy`.
4. In `pom.xml`, `mysql-connector-j` 8.3+ is used; `sslMode=VERIFY_IDENTITY` enforces TLS 1.2/1.3 and validates server certificate identity against the JDK truststore.

---

### 1.5 Vercel Rewrite Rules & Query Parameter Preservation Stress
Simulation with `scripts/test_m4_adversarial_audit.py` on `vercel.json` rewrites:
- Rule: `{ "source": "/api/(.*)", "destination": "https://staymart-backend.onrender.com/api/$1" }`
- Evaluation:
  - `/api/properties` -> `https://staymart-backend.onrender.com/api/properties` (PASS)
  - `/api/properties/14/rooms` -> `https://staymart-backend.onrender.com/api/properties/14/rooms` (PASS)
  - `/api/products?categoryId=2&locationId=1&status=AVAILABLE` -> Destination preserves query string exactly (PASS)
  - `/api/recommendations/properties/trending?city=Dehradun&limit=8` -> Destination preserves query string exactly (PASS)
  - `/api` (naked root without trailing slash) -> Does not match `/api/(.*)`, falls through to `/(.*)` -> `/frontend/api` (404) (Edge case)

---

## 2. Logic Chain

1. **Step 1 (Observation 1.2.A)**:
   In `application.yml`, `UPLOAD_BASE_URL` defaults to `http://localhost:8080`.
   In `FileStorageService.java`, line 64 formats uploaded image URLs as `baseUrl + "/api/files/" + filename`.
   Because neither `render.yaml` nor `DEPLOYMENT.md` configures `UPLOAD_BASE_URL`, an operator deploying StayMart following the guide will have all uploaded listing images saved with `http://localhost:8080/api/files/...`.
   When visitors load listing cards on their mobile devices or laptops, the browser will attempt to load images from `localhost:8080` and fail.
   *Inference*: `UPLOAD_BASE_URL` is a mandatory production environment variable that must be added to `DEPLOYMENT.md` and `render.yaml`.

2. **Step 2 (Observation 1.3.1)**:
   In `render.yaml`, `ML_BASE_URL` is configured via `fromService: { property: host }`.
   Render's blueprint compiler resolves `property: host` to a hostname string lacking the protocol scheme (`staymart-ml` or `staymart-ml.onrender.com`).
   Spring Boot's `RestClient` requires an absolute URI with `http://` or `https://`. When instantiated without a scheme, it throws `IllegalArgumentException: URI is not absolute`.
   Furthermore, Render Free tier prohibits private inter-service DNS networking between web services.
   *Inference*: `render.yaml` must explicitly define `ML_BASE_URL: https://staymart-ml.onrender.com` or document the blueprint override to ensure 1-click deployments succeed.

3. **Step 3 (Observation 1.3.2)**:
   `frontend/js/api.js` has a default cloud fallback to `'https://staymart.onrender.com/api'`.
   The actual backend service name in `render.yaml` is `staymart-backend` (`https://staymart-backend.onrender.com`).
   More importantly, hardcoding an absolute external URL forces the browser to make cross-origin requests directly to Render, bypassing Vercel's Edge CDN reverse-proxy rewrites (`vercel.json`) and triggering avoidable CORS preflight latency.
   *Inference*: `DEPLOYMENT.md` should clarify the frontend API endpoint binding, and `frontend/js/api.js` fallback should be updated to `'/api'` or `'https://staymart-backend.onrender.com/api'`.

4. **Step 4 (Observation 1.4 & 1.5)**:
   Database SSL parameters (`useSSL=true&sslMode=VERIFY_IDENTITY`) and MySQL CLI flags (`--ssl-mode=VERIFY_IDENTITY`) are correctly specified in `DEPLOYMENT.md`.
   Vercel rewrite rules preserve multi-level path wildcards and query parameter strings without truncation.
   All existing test suites pass with zero defects.
   *Inference*: The deployment foundation is solid; resolving the environment variable omissions in `render.yaml` and `DEPLOYMENT.md` will bring Milestone 4 to 100% production readiness.

---

## 3. Caveats

1. **Simulated Cloud Deployment**: Testing of Render and Vercel infrastructure was performed using static manifest analysis, regex rewrite simulations, and automated test runners on the local host. Physical multi-region cloud deployment was not executed as no external cloud credentials were provided.
2. **Spring Boot Profile Handling**: `application-prod.yml` does not exist in `src/main/resources/`. When `SPRING_PROFILES_ACTIVE=prod` is set, Spring Boot seamlessly falls back to `application.yml` without crashing, but production-specific overrides rely entirely on environment variables.

---

## 4. Conclusion & Required Changes

While the core container configurations, memory guardrails (`-Xmx384m`), TiDB SSL connection string, and Vercel reverse proxy rules are excellently designed, Milestone 4 has two configuration defects that will impair production runtime if deployed as-is:

### Required Action Items:
1. **Fix `render.yaml`**:
   - Add `UPLOAD_BASE_URL` environment variable under `staymart-backend` (e.g. `value: "https://staymart-backend.onrender.com"`).
   - Change `ML_BASE_URL` in `render.yaml` from `fromService: ... property: host` to `value: "https://staymart-ml.onrender.com"` to ensure the required `https://` scheme is present for Spring Boot `RestClient` and avoid Render Free private networking restrictions.
2. **Fix `DEPLOYMENT.md`**:
   - Add `UPLOAD_BASE_URL` to Table 4.2 (`Production Value: https://staymart-backend.onrender.com`, `Rationale: Base URL returned in image upload responses to avoid localhost fallback`).
   - Add a note in Section 5.1/5.2 advising frontend deployment to configure `window.STAYMART_API_URL = '/api'` or align `frontend/js/api.js` with the reverse proxy.
3. **Align `frontend/js/api.js`**:
   - Update fallback from `'https://staymart.onrender.com/api'` to `'/api'` (to utilize Vercel reverse proxy rewrites) or `'https://staymart-backend.onrender.com/api'`.

**Final Verdict**: **REQUEST_CHANGES**

---

## 5. Verification Method

To independently reproduce all findings and verify future fixes:

1. **Run Empirical Audit Harness**:
   ```powershell
   python scripts/test_m4_adversarial_audit.py
   ```
   *Expected Output*: Displays JSON report showing presence/absence of environment variables, rewrite mappings, and SSL directives.

2. **Verify Missing `UPLOAD_BASE_URL`**:
   ```powershell
   python -c "content = open('render.yaml').read(); assert 'UPLOAD_BASE_URL' in content, 'UPLOAD_BASE_URL missing from render.yaml'"
   python -c "content = open('DEPLOYMENT.md').read(); assert 'UPLOAD_BASE_URL' in content, 'UPLOAD_BASE_URL missing from DEPLOYMENT.md'"
   ```

3. **Verify Regression Test Suites**:
   ```powershell
   node scripts/run_viewport_tests.js
   python scripts/verify_m1_navigation.py
   python scripts/run_backend_tests.py
   ```
   *Expected Output*: All 3 commands exit with code 0.
