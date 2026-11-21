# Scope: StayMart Full-Stack Platform Enhancement (Generation 2)

## Architecture
StayMart is a multi-tier student accommodation and re-commerce marketplace designed for university students in Uttarakhand.
- **Frontend**: Native HTML5, CSS3, and ES6+ JavaScript Multi-Page Application (MPA) in `frontend/`.
- **Backend**: Spring Boot 3.3.5 on Java 17 in `src/main/java/com/staymart/`.
- **ML Microservice**: Python Flask microservice in `ml-service/` providing recommendations with DB fallback.
- **Database**: MySQL 8.0 compatible database (TiDB Serverless for free deployment).
- **Documentation & Reports**: Academic project reports and LaTeX documentation in `report/`.

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Frontend Mobile-First Overhaul & Visual Polish | Features 1–7 | None | DONE |
| M2 | Marketplace Statistics & Creative Visuals | Features 8–13 | M1 | DONE |
| M3 | Content Humanization & AI Artifact Removal | Features 14–18 | None | DONE |
| M4 | Complete Free Full-Stack Deployment Configs & Docs | Features 19–23 | None | DONE |
| M5 | Comprehensive Automated Verification Suite | Features 24–27 | M1, M2, M3, M4 | IN_PROGRESS |

---

## Milestone 3 Completion Summary
- Features Delivered:
  - Feature 14: Academic Report Humanization (`report/main.tex`, Chapters 1–9, Appendices rewritten in authentic student voice).
  - Feature 15: Report Technical Fact Correction (Java 17 LTS, OLX/Amazon light theme, TiDB Serverless, Render/Koyeb 384MB heap guardrails).
  - Feature 16: Script Hardcoded Template Humanization & PDF Compilation (`scripts/compile_report_pdf.py` upgraded with LaTeX table parser, balanced-brace heading parser, recompiled `StayMart_Project_Report.pdf` 5.77 MB).
  - Feature 17: Frontend UI Copy Humanization (`frontend/index.html` and public page footers updated to clean student value propositions).
  - Feature 18: Listing Seed Data Humanization (`database/03_seed_listings.sql` and `database/05_olx_amazon_listings.sql` updated with realistic student classifieds).
- Verification Results:
  - Adversarial AI scan: 0 violations across 87 target files.
  - PDF Compilation: Exit code 0, 5,772,433 bytes.
  - Viewport tests: 30/30 PASS across 320px–1920px.
  - Navigation tests: 8/8 test suites PASS.
  - Backend tests: 13/13 JUnit 5 tests PASS.
  - Forensic audit: CLEAN.
  - Reviewers: APPROVE.
  - Challengers: APPROVE.

---

## Milestone 4 Completion Summary
- Features Delivered:
  - Feature 19: Vercel Static Hosting & Reverse Proxy Rewrites (`vercel.json`, `frontend/vercel.json`, routing `/api/(.*)` to Render backend).
  - Feature 20: Spring Boot Multi-Stage Production Dockerfile (`Dockerfile` with Java 17 Temurin, `-Xmx384m` JVM memory limits, dynamic `$PORT` shell wrapper).
  - Feature 21: Flask ML Microservice Production Dockerfile (`ml-service/Dockerfile` with `python:3.11-slim`, Gunicorn single worker 4 threads, pre-trained TF-IDF vectorizers).
  - Feature 22: Free Managed MySQL on TiDB Cloud Serverless (5GB storage, 50M RUs/mo, TLS 1.3 `useSSL=true&sslMode=VERIFY_IDENTITY`, sequential database initialization requirement).
  - Feature 23: Master Step-by-Step Free Deployment Guide (`DEPLOYMENT.md` 450+ lines, environment variables tables including `UPLOAD_BASE_URL`, Section 5.3 runtime endpoint resolution, PowerShell Test 7, keep-warm strategies, troubleshooting).
  - Cross-tier Interconnect & Frontend Reverse Proxy: `render.yaml` fully aligned with `UPLOAD_BASE_URL` and `ML_BASE_URL: https://staymart-ml.onrender.com`; `frontend/js/api.js` updated with relative `'/api'` fallback and path trimming.
- Verification Results:
  - Adversarial audit script: `python scripts/test_m4_adversarial_audit.py` PASS.
  - Deep stress runtime tests: `python scripts/test_m4_adversarial_deep_stress.py` 8/8 scenarios PASS.
  - Viewport tests: 30/30 PASS across 320px–1920px.
  - Navigation tests: 8/8 suites PASS.
  - Backend tests: 13/13 JUnit 5 tests PASS.
  - AI Artifact scan: 0 violations across 87 target files.
  - Forensic audit: CLEAN.
  - Reviewer: APPROVE.
  - Challenger: APPROVE.
