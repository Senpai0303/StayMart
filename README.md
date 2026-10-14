# StayMart 🏠

StayMart is a full-stack accommodation and second-hand marketplace for **Dehradun and Uttarakhand**. Users can post and discover PGs, hostels, rooms, flats and hotels, buy or rent pre-loved products, book/view rooms, place orders, chat with owners and sellers, and leave reviews. Admins moderate listings, manage users, and view platform analytics. A Python ML microservice provides personalized and trending recommendations.

---

## 🧱 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Java 17, Spring Boot 3.3, Spring Web, Spring Data JPA, Spring Security (JWT), Bean Validation, Lombok |
| Database | MySQL 8 (`ddl-auto: validate`, schema managed by SQL scripts) |
| API Docs | springdoc-openapi (Swagger UI) |
| ML Service | Python 3, Flask, scikit-learn, scikit-surprise (SVD), pandas, MySQL Connector |
| Frontend | Vanilla HTML5 / CSS3 / JavaScript (no build step), Chart.js (admin dashboards) |

---

## 📁 Project Structure

```
Mini5th/
├── pom.xml                     # Spring Boot / Maven project
├── database/
│   ├── 01_schema.sql           # Tables: users, locations, categories, properties, rooms,
│   │                           #         products, bookings, orders, wishlists, reviews,
│   │                           #         chats, user_behaviors
│   ├── 02_seed.sql             # Seed locations + categories
│   └── 03_seed_listings.sql    # Demo sellers + 12 accommodations + 24 products
├── src/main/java/com/staymart/
│   ├── config/                 # Security, JWT filter, DataSeeder, CORS, OpenAPI
│   ├── controller/             # 16 REST controllers
│   ├── dto/                    # request/ and response/ records
│   ├── entity/                 # JPA entities (+ enums/)
│   ├── repository/             # Spring Data repositories
│   ├── service/                # Business logic (16 services)
│   └── common/                 # ApiResponse<T>, PageResponse<T>, exceptions
├── src/main/resources/
│   ├── application.yml         # Main config (port, datasource, JWT, CORS, ML URL)
│   └── application-dev.yml     # Dev profile overrides
├── ml-service/
│   ├── app.py                  # Flask app + routes
│   ├── config.py               # DB config, weights, cities, constants
│   ├── db_connector.py         # MySQL access layer
│   ├── model_trainer.py        # Trains SVD + TF-IDF models
│   ├── recommender.py          # Hybrid recommendation logic
│   ├── requirements.txt
│   └── README_ML.md            # ML service documentation
└── frontend/
    ├── index.html              # Landing page (hero search, trending)
    ├── login.html / register.html
    ├── search-properties.html / search-products.html
    ├── post-property.html / post-product.html
    ├── property-detail.html / product-detail.html
    ├── css/
    │   ├── global.css          # Shared theme (dark, indigo + mint)
    │   └── dashboard.css       # Sidebar dashboard layouts
    ├── js/                     # api.js, auth.js, utils.js, dashboard.js + page scripts
    └── pages/
        ├── user/               # dashboard, my-listings, bookings, orders,
        │                       # requests-received, wishlist, chat, profile
        └── admin/              # dashboard, pending-properties, pending-products,
                                # all-users, all-properties, all-products,
                                # categories, locations
```

---

## ✨ Features

### Public / User
- **Browse & search** properties and products by city (Dehradun, Rishikesh, Haridwar, Mussoorie, Nainital, Roorkee) and area.
- **Post listings** — properties (PG / Room / Hostel / Hotel / Flat / Dormitory) and products (buy or rent).
- **Bookings** — request a property/room booking; owners confirm, complete or cancel.
- **Orders** — buy or rent products; sellers confirm, complete or cancel.
- **Wishlist** — save properties and products.
- **Reviews & ratings** — rate properties, products and users.
- **Chat** — real-time-style messaging between users with unread counts.
- **Dashboards** — personal stats, recent activity and recommendations.
- **Recommendations** — personalized properties/products, similar items, trending and top-rated.

### Admin
- **Analytics dashboard** — totals plus Chart.js graphs: monthly listings, monthly registrations, properties by type, products by category, users by city.
- **Moderation** — approve/reject pending properties and products.
- **User management** — list users, activate/deactivate, delete (only when they have no listings).
- **Category management** — full CRUD.
- **Location management** — full CRUD (city, area, state, pincode, lat/lng).
- **Property & product management** — browse all listings, filter by status, moderate.

---

## ✅ Prerequisites

- **Java 17+** and **Maven**
- **MySQL 8+**
- **Python 3.9+** (for the ML service)
- A static file server for the frontend (e.g. VS Code **Live Server**, or `python -m http.server 5500`)

---

## 🚀 Getting Started

### ⚡ Quick Start (Windows — one command)

If all prerequisites are installed (see above), start everything with PowerShell:

```powershell
pwsh -File scripts/start-all.ps1
```

This will: start the MySQL Docker container → wait for it → use JDK 21 → start the backend (`:8080`), ML service (`:5000`) and frontend (`:5500`).

**Then open your browser at → http://localhost:5500**

To stop everything:

```powershell
pwsh -File scripts/stop-all.ps1
```

> Requirements for the script: **Docker Desktop must be running**, and Temurin **JDK 21** must be installed at `C:\Program Files\Eclipse Adoptium\jdk-21*`.

The manual steps below are the equivalent if you prefer starting each service yourself.

### 1. Database

```bash
mysql -u root -p < database/01_schema.sql
mysql -u root -p staymart < database/02_seed.sql
mysql -u root -p staymart < database/03_seed_listings.sql   # optional demo listings
```

This creates the `staymart` schema, all tables, and seeds locations and categories. The optional `03_seed_listings.sql` adds **demo sellers plus 12 accommodations and 24 marketplace products** (all pre-approved) so the catalogue is populated — see [Demo Listings](#-demo-listings).

> The backend datasource defaults to `root` / `root` on `localhost:3306`. Override with the `DB_USERNAME` and `DB_PASSWORD` environment variables if needed.

### 2. Backend (Spring Boot)

```bash
mvn clean install
mvn spring-boot:run
```

- API base URL: `http://localhost:8080/api`
- Swagger UI: `http://localhost:8080/swagger-ui.html`
- OpenAPI JSON: `http://localhost:8080/v3/api-docs`

On first startup, `DataSeeder` creates the default admin account and seeds categories (if empty).

### 3. ML Service (optional but recommended)

```bash
cd ml-service
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

- Starts on `http://localhost:5000`.
- On startup it loads models from `models/`; missing models are trained from the DB automatically.
- If MySQL is unreachable it still runs and recommendations degrade gracefully (empty/fallback results).

See [`ml-service/README_ML.md`](ml-service/README_ML.md) for endpoints and retraining.

> The backend talks to this service via `app.ml.base-url` (default `http://localhost:5000`). If it is down, the backend falls back to latest-approved listings.

### 4. Frontend

Serve the `frontend/` folder over HTTP (not `file://`, because of CORS/fetch):

```bash
# from the frontend directory
python -m http.server 5500
```

Then open `http://localhost:5500`.

Allowed CORS origins are configured in `application.yml` (`app.cors.allowed-origins`), including `:5500`, `:3000`, `:4200`, `:5173`, `:8081`.

---

## 🔑 Default Accounts

Seeded automatically on first backend start (see `DataSeeder` / `application.yml`):

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@staymart.com` | `Admin@123` |

Regular users can be created via the **Register** page. The admin account is redirected to `pages/admin/dashboard.html` after login; normal users land on the home page.

> Credentials can be overridden with `SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD`.

If you loaded `database/03_seed_listings.sql`, these demo seller accounts also exist (all with password `User@123`):

| Name | Email | Password |
|------|-------|----------|
| Rohit Rawat | `rohit.rawat@staymart.com` | `User@123` |
| Priya Negi | `priya.negi@staymart.com` | `User@123` |
| Sunita Bisht | `sunita.bisht@staymart.com` | `User@123` |
| Aman Chauhan | `aman.chauhan@staymart.com` | `User@123` |

---

## 📦 Demo Listings

`database/03_seed_listings.sql` populates the marketplace so the catalogue is not empty. Everything is inserted with `status = APPROVED`, so listings appear immediately in the public pages.

- **12 accommodations** (PG, hostel, flat, room, hotel, dormitory) across Dehradun, Rishikesh, Haridwar, Mussoorie and Roorkee — OYO / PG / hostel style, with amenities, monthly rent, deposits and images.
- **8 rooms** attached to the first three PGs/hostels (shown on the property detail page).
- **24 products** — OLX-style used goods (laptops, phones, furniture, books, appliances, bikes, sports gear, fashion) with price, condition, listing type, brand, location and images.

Images use [`picsum.photos`](https://picsum.photos) placeholder URLs (reliable, no API key). Descriptions and prices are realistic demo data modelled on typical OYO/OLX listings for Uttarakhand.

```bash
# Reload just the demo listings into an existing database
mysql -u root -p staymart < database/03_seed_listings.sql
```

---

## 🔌 API Overview

All responses use a consistent envelope:

```json
{ "success": true, "message": "optional", "data": { } }
```

Paged endpoints return `{ content, page, size, totalElements, totalPages, last }` inside `data`.

| Area | Base path | Highlights |
|------|-----------|-----------|
| Auth | `/api/auth` | `POST /register`, `POST /login` |
| Users | `/api/users` | `GET/PUT /me`, `PUT /me/password`, `GET /me/properties`, `GET /me/products`, `GET /{id}` |
| Properties | `/api/properties` | list/search/filter, `GET /{id}`, `POST`, `PUT /{id}`, `DELETE /{id}`, `GET /{id}/rooms` |
| Rooms | `/api/properties/{id}/rooms` | room CRUD |
| Products | `/api/products` | list/search/filter, CRUD |
| Bookings | `/api/bookings` | `POST`, `GET /mine`, `GET /incoming`, `PATCH /{id}/status` |
| Orders | `/api/orders` | `POST`, `GET /mine`, `GET /sales`, `PATCH /{id}/status` |
| Wishlist | `/api/wishlist` | `GET`, `POST`, `DELETE`, `GET /check` |
| Reviews | `/api/reviews` | `GET`, `POST`, `GET /summary`, `GET /mine`, `DELETE /{id}` |
| Chats | `/api/chats` | `POST`, `GET /conversations`, `GET /with/{userId}`, `POST /read/{userId}`, `GET /unread-count` |
| Categories | `/api/categories` | `GET`, `GET /{id}`, admin CRUD |
| Locations | `/api/locations` | `GET`, `GET /cities`, `GET /search`, admin CRUD |
| Recommendations | `/api/recommendations` | `GET /{userId}`, `GET /properties`, `GET /properties/trending`, `GET /properties/{id}/similar`, `GET /products`, `GET /products/top-rated` |
| Admin | `/api/admin` | `GET /stats`, `GET /analytics`, listings with `?status=`, `PATCH .../status`, `GET /users`, `PATCH /users/{id}/status`, `DELETE /users/{id}` |
| Files | `/api/files` | image upload |

Protected endpoints require a `Authorization: Bearer <token>` header (JWT, 24h expiry).

---

## ⚙️ Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DB_USERNAME` | `root` | MySQL username |
| `DB_PASSWORD` | `root` | MySQL password |
| `JWT_SECRET` | built-in dev secret | JWT signing key |
| `UPLOAD_DIR` | `uploads` | Upload directory |
| `UPLOAD_BASE_URL` | `http://localhost:8080` | Base URL for uploaded files |
| `CORS_ORIGINS` | see `application.yml` | Comma-separated allowed origins |
| `ML_BASE_URL` | `http://localhost:5000` | ML service base URL |
| `SEED_ADMIN_EMAIL` | `admin@staymart.com` | Seeded admin email |
| `SEED_ADMIN_PASSWORD` | `Admin@123` | Seeded admin password |

---

## 🤖 Recommendation Engine

The Flask service builds a hybrid recommender:

- **New users** (< `MIN_INTERACTIONS_FOR_CF` = 5 behaviours) → trending items in their city (default **Dehradun**).
- **Active users** (≥ 5 interactions) → 60% SVD collaborative filtering + 40% TF-IDF content similarity, blended into a 0–1 score.
- **Similar items** → TF-IDF + cosine similarity over text features.
- **Trending** → time-decayed score over the last 7 days, weighted by action (VIEW/SEARCH=1, WISHLIST/CONTACT=3, BOOK/ORDER=5).
- Excludes items already booked/ordered and only returns `APPROVED` + available items.

Models are auto-generated into `ml-service/models/` (`property_svd.pkl`, `product_svd.pkl`, `property_tfidf.pkl`, `product_tfidf.pkl`) and can be rebuilt via `POST /retrain`.

---

## 🧪 Verifying the Build

```bash
# Backend compiles
mvn -q compile

# Frontend scripts are syntactically valid
Get-ChildItem frontend/js/*.js | ForEach-Object { node --check $_.FullName }
```

---

## 📝 Notes

- The frontend is framework-free and must be served over HTTP so `fetch` and CORS work correctly.
- The backend uses `ddl-auto: validate`, so the schema must exist before starting (run the SQL scripts first).
- Uploaded images are stored under `uploads/` and served from the backend base URL.
