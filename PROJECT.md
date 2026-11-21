# Project: StayMart Full-Stack Platform Enhancement

## Architecture
StayMart is a multi-tier student accommodation and re-commerce marketplace designed for university students in Uttarakhand.
- **Frontend**: Native HTML5, CSS3, and ES6+ JavaScript Multi-Page Application (MPA) in `frontend/`, deployed statically to Vercel with clean URLs and reverse proxy rewrites.
- **Backend**: Spring Boot 3.3.5 on Java 17 in `src/main/java/com/staymart/`, exposing RESTful APIs with stateless JWT authentication.
- **ML Microservice**: Python Flask microservice in `ml-service/` providing dual-engine hybrid recommendations (TF-IDF content-based + collaborative filtering) with database fallback.
- **Database**: MySQL 8.0 compatible relational database with 12 tables managed via SQL migration scripts in `database/`.
- **Documentation & Reports**: Academic project reports and LaTeX documentation in `report/` and generation scripts in `scripts/`.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Mobile Viewport Layout Fixes | Remove inline 260px grid style in search pages, fix horizontal overflow on mobile (375px), tablet (768px), desktop (1280px+) | M1 | Survey E1 |
| 2 | Mobile Navigation Overhaul | Replace overcrowded desktop navbar with responsive mobile header, hamburger drawer, and bottom navigation bar | M1 | Survey E1 |
| 3 | Mobile Search & Filter Drawer | Implement collapsible filter drawer / bottom sheet for mobile search views | M1 | Survey E1 |
| 4 | Sticky Action Bar on Detail Pages | Floating bottom CTA bar for mobile accommodation booking and product inquiry | M1 | Survey E1 |
| 5 | Design Token Harmonization | Unify CSS custom properties between `global.css` and `dashboard.css` (`--dark*`, `--primary*`, light theme accents) | M1 | Survey E1 |
| 6 | 404 Broken Redirect Bug Fix | Correct redirect path in `property-detail.js` from `my-bookings.html` to `bookings.html` | M1 | Survey E1 |
| 7 | Micro-Interactions & Visual Polish | Smooth transitions, hover elevations, card micro-interactions, replacing raw emojis with styled badges | M1 | Survey E1 |
| 8 | Animated Metric Counters | Dynamic counters with easing for listings, active students, savings, and verified properties using `IntersectionObserver` | M2 | Survey E1 |
| 9 | Student Savings Calculators | Interactive calculators for accommodation (brokerage savings) and re-commerce (second-hand equipment savings) | M2 | Survey E1 |
| 10 | Occupancy & Availability Meters | Real-time visual capacity bars and pulsing availability badges for PG rooms and accommodation | M2 | Survey E1 |
| 11 | Price Trend Indicators | Visual price indicators comparing listing rates with campus/regional medians | M2 | Survey E1 |
| 12 | Public Creative Visual Charts | Interactive charts showing price trends, category distribution, and student savings over time | M2 | Survey E1 |
| 13 | Listing Engagement Indicators | View counts, inquiry frequency badges, and bookmark activity indicators on listing cards | M2 | Survey E1 |
| 14 | Academic Report Humanization | Rewrite `report/main.tex` and chapters 1-9 to remove pseudo-intellectual AI jargon, passive filler, and AI signatures | M3 | Survey E3 |
| 15 | Report Technical Fact Correction | Align report with actual codebase: Java 17 (not 21), accurate JWT security scope, real Docker & deployment setup, light OLX/Amazon UI | M3 | Survey E3 |
| 16 | Script Hardcoded Template Humanization | Update `scripts/compile_report_pdf.py` HTML templates to match humanized academic report text and recompile PDF | M3 | Survey E3 |
| 17 | Frontend UI Copy Humanization | Replace robotic marketing copy on landing and public pages with authentic, student-authored voice | M3 | Survey E3 |
| 18 | Listing Seed Data Humanization | Polish sample listings in database SQL seeds to reflect genuine student classifieds around Uttarakhand campuses | M3 | Survey E3 |
| 19 | Vercel Deployment Configuration | Complete static hosting config with clean URLs and reverse proxy rewrites in `vercel.json` | M4 | Survey E2 |
| 20 | Spring Boot Free Cloud Deployment | Multi-stage Dockerfile and Render/Koyeb free-tier configuration with `-Xmx384m` memory guardrails | M4 | Survey E2 |
| 21 | Flask ML Free Cloud Deployment | Dedicated `ml-service/Dockerfile` using Python 3.11-slim + Gunicorn with health check endpoint | M4 | Survey E2 |
| 22 | Free Managed MySQL Setup | TiDB Serverless (5GB free forever) and Aiven MySQL integration guides with SSL configs | M4 | Survey E2 |
| 23 | Master Free Deployment Guide | Step-by-step `DEPLOYMENT.md` covering env vars, DB initialization sequence, cross-tier networking, and smoke test checks | M4 | Survey E2 |
| 24 | Backend Automated Test Execution | Verification of existing 13 JUnit 5 backend tests via `scripts/run_backend_tests.py` | M5 | Survey E2 |
| 25 | Automated Mobile Viewport Layout Tests | Automated headless Chrome test suite checking zero horizontal overflow across 375px, 768px, 1280px viewports | M5 | Survey E1, E2 |
| 26 | Multi-Tier API Smoke Test Suite | Automated Python smoke tests verifying health, listings, recommendations, and public stats endpoints | M5 | Survey E2 |
| 27 | Unified Test Master Runner | Top-level runner `scripts/run_all_verifications.py` executing all test suites with exit code 0 | M5 | Survey E2 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Frontend Mobile-First Overhaul & Visual Polish | Features 1–7: Responsive CSS/HTML, mobile navigation, drawers, sticky CTAs, token sync, 404 fix, animations | None | PLANNED |
| M2 | Marketplace Statistics & Creative Visuals | Features 8–13: Animated counters, savings calculators, occupancy meters, price trends, public visual charts, engagement stats | M1 | PLANNED |
| M3 | Content Humanization & AI Artifact Removal | Features 14–18: Humanize LaTeX report chapters 1-9, compile script, UI copy, sample listings, remove AI traces | None | PLANNED |
| M4 | Complete Free Full-Stack Deployment Configs & Docs | Features 19–23: Vercel config, backend Dockerfile, ML Dockerfile, TiDB free DB setup, DEPLOYMENT.md guide | None | PLANNED |
| M5 | Comprehensive Automated Verification Suite | Features 24–27: Backend tests, mobile viewport layout checks, API smoke tests, master runner | M1, M2, M3, M4 | PLANNED |

---

## Interface Contracts

### Frontend ↔ Spring Boot Backend
- Base URL: `/api` (proxied via Vercel rewrites in production, `http://localhost:8080/api` locally).
- Authentication: `Authorization: Bearer <jwt_token>` header for protected routes (`/api/bookings`, `/api/orders`, `/api/user/**`).
- Public Endpoints:
  - `GET /api/properties`: List properties with query params `type`, `locationId`, `status=AVAILABLE`, `minPrice`, `maxPrice`.
  - `GET /api/properties/{id}`: Detailed property object including rooms, amenities, and owner details.
  - `GET /api/products`: List products with query params `categoryId`, `locationId`, `status=AVAILABLE`.
  - `GET /api/products/{id}`: Detailed product object.
  - `GET /api/locations`: Array of Uttarakhand location objects (`id`, `name`, `district`, `state`).
  - `GET /api/categories`: Array of product category objects.
  - `GET /api/properties/stats`: Public marketplace statistics aggregates (total listings, average rent, verified count).
- Error Handling: Standard JSON response `{ "timestamp": "...", "status": 4xx/5xx, "error": "...", "message": "..." }`.

### Spring Boot Backend ↔ Flask ML Microservice
- ML Base URL: Configured via `ml.service.url` (default `http://localhost:5000`).
- Health Check: `GET /health` -> `{ "status": "healthy", "service": "staymart-ml" }`.
- Property Recommendations: `GET /recommend/properties/{propertyId}?limit=6` -> JSON array of recommended property IDs and similarity scores.
- Product Recommendations: `GET /recommend/products/{productId}?limit=6` -> JSON array of recommended product IDs.
- Resilience Contract: Spring Boot `MlServiceClient` enforces 2000ms connect / 3000ms read timeout. If ML service is down or times out, `RecommendationService` automatically falls back to database-driven category/location matching without throwing 500 errors.

### Database Schema Contract
- Tables: `users`, `categories`, `locations`, `properties`, `rooms`, `products`, `bookings`, `orders`, `reviews`, `wishlists`, `chats`, `user_behaviors`.
- DDL Mode: `validate`. Database initialization scripts (`01_schema.sql` through `05_olx_amazon_listings.sql`) must be applied before backend startup.

---

## Code Layout
```
d:\Mini5th\
├── frontend/                     # Static Multi-Page Web Application
│   ├── index.html                # Marketplace homepage with hero, search, stats & categories
│   ├── search-properties.html    # Accommodation browsing with filters & map view
│   ├── search-products.html      # Re-commerce classifieds browsing with filters
│   ├── property-detail.html      # Accommodation details, room selector & booking modal
│   ├── product-detail.html       # Classified item details, seller info & inquiry
│   ├── css/
│   │   ├── global.css            # Primary design system, components, mobile utilities
│   │   └── dashboard.css         # User and admin dashboard layouts
│   ├── js/
│   │   ├── api.js                # Centralized Fetch API client with auth token headers
│   │   ├── utils.js              # Formatting helpers, toast alerts, modal handlers
│   │   ├── stats.js              # Marketplace statistics, counters & savings calculators
│   │   ├── charts.js             # Creative visual charts & SVG trend renders
│   │   └── ...                   # Page controllers
│   └── pages/
│       ├── user/                 # User dashboard, bookings, listings, orders, chat
│       └── admin/                # Admin management consoles & analytics
├── src/main/java/com/staymart/   # Spring Boot 3.3.5 Backend (Java 17)
│   ├── controller/               # REST API controllers
│   ├── service/                  # Business logic & ML service client
│   ├── repository/               # Spring Data JPA repositories
│   ├── entity/                   # JPA entity models
│   └── config/                   # Security, JWT, CORS, OpenAPI configs
├── ml-service/                   # Python Flask ML Microservice
│   ├── app.py                    # Flask application & recommendation endpoints
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Lightweight cloud container configuration
│   └── models/                   # Serialized TF-IDF feature models
├── database/                     # MySQL Migration & Seed Scripts
│   ├── 01_schema.sql             # 12 core tables & foreign keys
│   ├── 02_seed.sql               # Locations & categories seed data
│   ├── 03_seed_listings.sql      # Student demo listings
│   └── 05_olx_amazon_listings.sql# Humanized campus classifieds
├── report/                       # Academic Documentation & LaTeX Report
│   ├── main.tex                  # Master report document
│   └── chapters/                 # Humanized chapters 1 through 9
├── scripts/                      # Automation, Build & Verification Suites
│   ├── run_backend_tests.py      # JUnit 5 backend test runner
│   ├── run_viewport_tests.py     # Headless Chrome mobile-first layout verification
│   ├── run_smoke_tests.py        # Multi-tier API smoke verification suite
│   ├── run_all_verifications.py  # Master automated verification test runner
│   └── compile_report_pdf.py     # Clean academic report compiler
├── vercel.json                   # Vercel production deployment configuration
├── Dockerfile                    # Spring Boot production container build
└── DEPLOYMENT.md                 # Complete 100% free-tier deployment guide
```
