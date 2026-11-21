## 2026-11-02T20:01:43Z
[Message] timestamp=2026-11-02T20:01:43Z sender=e8442687-110f-4189-bec3-f0fa5c033ec1 priority=MESSAGE_PRIORITY_HIGH content=You are the Implementation Worker for Milestone 4: Complete Free Full-Stack Deployment Configurations & Documentation.
Your identity: Milestone 4 Implementation Worker (Generation 2)
Working directory: d:\Mini5th\.agents\teamwork\m4_worker_1\
Parent Conversation ID: e8442687-110f-4189-bec3-f0fa5c033ec1

## MANDATORY INTEGRITY WARNING
> DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## MANDATORY: Read Specifications and Blueprints First
1. Read the original user request record: `d:\Mini5th\.agents\teamwork\ORIGINAL_REQUEST.md`
2. Read the master project plan: `d:\Mini5th\PROJECT.md`
3. Read the exhaustive deployment survey report: `d:\Mini5th\.agents\teamwork\explorer_survey_2\survey_backend_deployment.md` (Specifically Section 5: Zero-Cost Deployment Topology).

## Write Ownership Boundaries
You have exclusive write ownership of:
- `vercel.json` and `frontend/vercel.json`
- `Dockerfile` (root Spring Boot container build)
- `ml-service/Dockerfile` (new Flask microservice container build)
- `DEPLOYMENT.md` (master free deployment guide)
- Any optional deployment manifests like `render.yaml`

DO NOT modify frontend JavaScript, CSS, Java source files, or report LaTeX sources.

## Implementation Tasks

### 1. Frontend Vercel Configuration (`vercel.json` & `frontend/vercel.json`):
- Configure static hosting with clean URLs and reverse proxy rewrites:
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
- Ensure both root `vercel.json` and `frontend/vercel.json` work seamlessly whether deploying root or `frontend/` as root directory.

### 2. Spring Boot Multi-Stage Production Dockerfile (`Dockerfile`):
- Ensure a clean, reproducible multi-stage build:
  - Stage 1: Build stage with `maven:3.9.6-eclipse-temurin-17` compiling `pom.xml` and creating `target/staymart-0.0.1-SNAPSHOT.jar`.
  - Stage 2: Minimal runtime image with `eclipse-temurin:17-jre-jammy`.
  - Memory guardrails for 512MB RAM free cloud tiers:
    Set `ENV JAVA_TOOL_OPTIONS="-Xmx384m -Xms128m -XX:+UseSerialGC"`
  - Expose port `8080`.
  - Handle Render `$PORT` environment variable substitution via `ENTRYPOINT ["sh", "-c", "java $JAVA_TOOL_OPTIONS -Dserver.port=${PORT:-8080} -jar app.jar"]`.

### 3. Flask ML Microservice Production Dockerfile (`ml-service/Dockerfile`):
- Create lightweight, production-ready container build:
  - Base: `python:3.11-slim`.
  - Install dependencies from `ml-service/requirements.txt` plus `gunicorn`.
  - Copy `ml-service/` files and models (`property_tfidf.pkl`, `product_tfidf.pkl`).
  - Configure `CMD ["gunicorn", "-w", "1", "--threads", "4", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]` to keep memory footprint under 180MB RAM.
  - Expose port `5000`.

### 4. Master Free Full-Stack Deployment Guide (`DEPLOYMENT.md`):
- Author an authoritative, step-by-step, 100% free deployment guide enabling anyone to deploy StayMart completely free forever:
  1. **Architecture Topology**: Complete diagram of 4 free tiers:
     - Tier 1: Frontend on Vercel (Hobby Tier - $0/mo forever)
     - Tier 2: Spring Boot Backend on Render / Koyeb (Free Web Service - $0/mo)
     - Tier 3: Flask ML Microservice on Render / Hugging Face Spaces ($0/mo)
     - Tier 4: Managed MySQL on TiDB Serverless (5GB free forever, 50M Request Units/mo, SSL default)
  2. **TiDB Cloud Serverless Setup**:
     - Step-by-step account creation (no credit card required).
     - Cluster creation and obtaining connection string, host, port (4000), username, and password.
     - Critical Database Initialization sequence: executing `database/01_schema.sql` through `05_olx_amazon_listings.sql` (explain why: Spring Boot uses `ddl-auto: validate`).
  3. **Backend Service Deployment (Render / Koyeb)**:
     - Step-by-step GitHub connection, Docker runtime selection.
     - Environment Variables table (`DB_URL`, `DB_USERNAME`, `DB_PASSWORD`, `JWT_SECRET`, `CORS_ORIGINS`, `ML_BASE_URL`, `JAVA_TOOL_OPTIONS`, `PORT`).
     - Memory tuning explanation (`-Xmx384m`).
  4. **Flask ML Microservice Deployment**:
     - Step-by-step deployment on Render free tier.
     - Environment variables (`PORT`, `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME`).
     - Verification via `GET /health`.
  5. **Frontend Deployment (Vercel)**:
     - Step-by-step import from GitHub.
     - Build and output settings.
     - Reverse-proxy rewrite verification to eliminate CORS.
  6. **Interconnectivity & End-to-End Smoke Verification**:
     - Complete `curl` and PowerShell verification script to test health, properties, products, and recommendation endpoints.

## Verification
After creating all files, execute:
1. `node scripts/run_viewport_tests.js` (30/30 viewport tests pass)
2. `python scripts/verify_m1_navigation.py` (8/8 navigation test suites pass)
3. `python scripts/run_backend_tests.py` (13/13 backend tests pass)
4. Verify file existence and syntax for `Dockerfile`, `ml-service/Dockerfile`, `vercel.json`, and `DEPLOYMENT.md`.

## Output
Write your comprehensive implementation handoff report to:
`d:\Mini5th\.agents\teamwork\m4_worker_1\handoff.md`

When complete, send a message to the parent orchestrator.
