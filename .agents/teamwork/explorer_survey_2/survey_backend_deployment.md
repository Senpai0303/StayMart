# StayMart Deep Technical Survey: Backend, ML, Database, Free-Tier Deployment & Automated Verification

**Author**: Explorer 2 (Backend, ML, DB, Free-Tier Deployment & Verification Survey)  
**Date**: November 2, 2026  
**Scope**: Complete architectural inspection of StayMart multi-tier platform (Spring Boot backend, Flask ML service, MySQL database, static frontend deployment configurations, and automated verification infrastructure).

---

## 1. Executive Summary

StayMart is a multi-tier student accommodation and re-commerce platform tailored for universities and colleges across Uttarakhand (Dehradun, Rishikesh, Haridwar, Mussoorie, Roorkee, etc.). 

### Architectural Overview
```
+-----------------------------------------------------------------------------------+
|                                  USER BROWSER                                     |
|               Mobile (375px) | Tablet (768px) | Desktop (1280px+)                  |
+-----------------------------------------------------------------------------------+
             |                                              |
     Static Web Assets                               Direct API or Vercel Proxy
             v                                              v
+-------------------------+                     +-----------------------------------+
|     FRONTEND TIER       |                     |        BACKEND REST API           |
|      (Vercel CDN)       |                     |    (Spring Boot 3.3.5 / Java 17)   |
| HTML5 / CSS3 / VanillaJS|                     |   Port: 8080 (Docker on Render)   |
+-------------------------+                     +-----------------------------------+
                                                              |            |
                                       Internal REST Client   |            | JDBC (HikariCP)
                                       (2s connect, 3s read)  v            v
                                                +----------------+   +--------------+
                                                |  ML SERVICE    |   |   DATABASE   |
                                                | (Flask / Py11) |-->|   (MySQL 8 / |
                                                | TF-IDF / CF    |   | TiDB Cloud)  |
                                                | Port: 5000     |   | Port: 3306   |
                                                +----------------+   +--------------+
```

### Key Survey Findings
1. **Spring Boot Backend**: Highly structured, modular Spring Boot 3.3.5 application running on Java 17/21. Features 16 REST controllers, 17 service classes, 12 JPA entities, JWT stateless security, and an internal `RestClient` with automatic fallback to database records if the ML service is unreachable.
2. **ML Recommendation Service**: Python Flask microservice using scikit-learn, pandas, and numpy. Implements a hybrid recommendation engine: 60% collaborative filtering (user interaction weights with time decay) + 40% content-based TF-IDF cosine similarity. Pre-trained models (`property_tfidf.pkl`, `product_tfidf.pkl`) reside in `ml-service/models/`.
3. **Database Architecture**: 12 relational tables with foreign keys, indexes, and JSON column support for images and amenities. Hibernate is configured with `ddl-auto: validate`, requiring database schema initialization before application boot.
4. **Free-Tier Deployment (R4)**: Full-stack platform can be hosted 100% free with zero monthly charges using **Vercel** (Frontend), **Render Free Web Service** (Spring Boot via Docker + Flask ML), and **TiDB Serverless** (5 GB forever-free managed MySQL 8 compatible).
5. **Test Infrastructure (R5)**: 13 existing backend unit/integration tests run via `scripts/run_backend_tests.py` and pass with 100% success rate (exit code 0). Comprehensive specifications for 3 new automated test suites (build verification, viewport responsiveness check via headless Chrome, and multi-tier API smoke testing) are defined.

---

## 2. Spring Boot Backend Architecture

### 2.1 Build System & Java Environment
- **Framework**: Spring Boot 3.3.5 (`spring-boot-starter-parent`)
- **Java Target**: Java 17 (`<java.version>17</java.version>` in `pom.xml`). Development workstation contains Eclipse Adoptium Temurin JDK 21 (`jdk-21.0.12.101-hotspot`), which compiles and runs Java 17 bytecode seamlessly.
- **Build Tool**: Apache Maven (`pom.xml` at repo root). The workstation uses `.m2` repository cache at `C:\Users\divya\.m2\repository`.
- **Primary Dependencies**:
  - `spring-boot-starter-web`: Spring MVC and embedded Tomcat.
  - `spring-boot-starter-data-jpa`: Spring Data JPA with Hibernate 6.5.
  - `spring-boot-starter-security`: Spring Security 6 with custom filters.
  - `spring-boot-starter-validation`: Jakarta Bean Validation (`@Valid`, `@NotNull`, `@NotBlank`).
  - `mysql-connector-j`: Official MySQL JDBC driver (`com.mysql.cj.jdbc.Driver`).
  - `io.jsonwebtoken` (`jjwt-api`, `jjwt-impl`, `jjwt-jackson` v0.12.6): Modern JWT token generation and verification.
  - `springdoc-openapi-starter-webmvc-ui` (v2.6.0): Swagger UI at `/swagger-ui.html` and OpenAPI JSON at `/v3/api-docs`.
  - `org.projectlombok:lombok`: Boilerplate reduction (`@Getter`, `@Setter`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`).
  - `spring-boot-starter-test` & `spring-security-test`: JUnit 5, AssertJ, Mockito, Spring TestContext.

### 2.2 Controller & API Endpoint Catalog (16 Controllers)

| Controller | Base Path | Key Endpoints & Methods | Auth Level | Description |
|------------|-----------|-------------------------|------------|-------------|
| `AuthController` | `/api/auth` | `POST /register`, `POST /login` | Public | User registration and JWT issuance |
| `PropertyController` | `/api/properties` | `GET /` (search/filter), `GET /{id}`, `POST /`, `PUT /{id}`, `DELETE /{id}`, `GET /{id}/rooms` | Public GET / Auth POST/PUT/DELETE | Accommodation listings (PG, Hostel, Flat, Room) |
| `ProductController` | `/api/products` | `GET /` (search/filter), `GET /{id}`, `POST /`, `PUT /{id}`, `DELETE /{id}` | Public GET / Auth POST/PUT/DELETE | Student re-commerce marketplace (Buy/Sell/Rent) |
| `RoomController` | `/api/properties/{pId}/rooms`, `/api/rooms` | `POST /{pId}/rooms`, `PUT /{id}`, `DELETE /{id}` | Authenticated | Room inventory under specific properties |
| `BookingController` | `/api/bookings` | `POST /`, `GET /mine`, `GET /incoming`, `GET /{id}`, `PATCH /{id}/status` | Authenticated | Student accommodation booking lifecycle |
| `OrderController` | `/api/orders` | `POST /`, `GET /mine`, `GET /sales`, `GET /{id}`, `PATCH /{id}/status` | Authenticated | Student product buy/rent orders |
| `ReviewController` | `/api/reviews` | `GET /` (by item), `POST /`, `GET /summary`, `GET /mine`, `DELETE /{id}` | Public GET / Auth POST/DELETE | 1-5 star ratings & reviews for properties/products |
| `WishlistController` | `/api/wishlist` | `GET /`, `POST /`, `DELETE /`, `GET /check` | Authenticated | User favorites/bookmarks |
| `ChatController` | `/api/chats` | `GET /conversations`, `GET /{userId}`, `POST /`, `PATCH /{msgId}/read` | Authenticated | Real-time / persistent direct chat between buyers and sellers |
| `BehaviorController` | `/api/behaviors` | `POST /`, `GET /mine` | Authenticated | Logs actions (VIEW, SEARCH, WISHLIST, BOOK, ORDER, CONTACT) |
| `CategoryController` | `/api/categories` | `GET /`, `POST /`, `PUT /{id}`, `DELETE /{id}` | Public GET / Admin POST/PUT/DELETE | Product & Accommodation categories |
| `LocationController` | `/api/locations` | `GET /`, `POST /`, `PUT /{id}`, `DELETE /{id}` | Public GET / Admin POST/PUT/DELETE | Uttarakhand cities, areas, coordinates, pincodes |
| `UserController` | `/api/users` | `GET /me`, `PUT /me`, `PUT /me/password`, `GET /me/properties`, `GET /me/products`, `GET /{id}` | Authenticated | User profiles and personal listing queries |
| `AdminController` | `/api/admin` | `GET /stats`, `GET /analytics`, `GET /users`, `PATCH /users/{id}/status`, `DELETE /users/{id}`, `GET /properties`, `PATCH /properties/{id}/status`, `GET /products`, `PATCH /products/{id}/status` | Admin Only (`ROLE_ADMIN`) | Administrative platform analytics, moderation, and user management |
| `RecommendationController` | `/api/recommendations` | `GET /{userId}`, `GET /properties`, `GET /properties/trending`, `GET /properties/{id}/similar`, `GET /products`, `GET /products/{id}/similar`, `GET /products/top-rated` | Public | ML-powered personalized recommendations with resilient fallbacks |
| `FileController` | `/api/files` | `POST /upload`, `POST /upload-multiple`, `GET /{fileName}` | Public GET / Auth POST | Multipart image uploads and file serving |

### 2.3 Service Layer & Business Logic (17 Services)
- `PropertyService` & `ProductService`: Dynamic query filtering using Spring Data JPA `Specification` (title, category, city, area, price range, condition, amenities, type, gender preference). Enforces listing status filters (`APPROVED` for public, pending for admin).
- `RecommendationService`: Orchestrates ML recommendations. Calls `MlServiceClient`. If ML returns empty list or throws timeout/network exceptions, automatically falls back to `latestApproved()` properties or products.
- `MlServiceClient`: Spring 6 `RestClient` with strict 2-second connection timeout and 3-second read timeout. Safely parses diverse ML response shapes (`[1, 2]`, `{"property_ids": [...]}`, `{"items": [...]}`).
- `AdminService`: Computes platform-wide statistics (`DashboardStats`) and time-series analytics (`AdminAnalyticsResponse` with `ChartDataPoint` distributions by city, type, category, and month).
- `FileStorageService`: Validates file extensions (`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.svg`), generates UUID filenames, and persists to configured upload directory.
- `AuthService` & `JwtService`: Generates HS256 JWT tokens containing user ID, email, role, and 24-hour expiration (`expiration-ms: 86400000`).

### 2.4 Entity Models & JPA Mapping (12 Entities)

| Entity | Table Name | Key Attributes | Enums / Types | Relations |
|--------|------------|----------------|---------------|-----------|
| `User` | `users` | id, name, email, passwordHash, phone, profilePic, city, state, bio, isActive, isVerified | `Role` (ADMIN, USER) | 1:N properties, products, bookings, orders |
| `Location` | `locations` | id, city, area, state, pincode, latitude, longitude | Decimal(10,8) coords | 1:N properties, products |
| `Category` | `categories` | id, name, type, icon, parent | `CategoryType` (ACCOMMODATION, PRODUCT) | Self-referencing parent-child |
| `Property` | `properties` | id, title, description, address, area, pricePerMonth, depositAmount, totalRooms, availableRooms, amenities, images, isAvailable, createdAt | `PropertyType` (PG, ROOM, HOSTEL, HOTEL, FLAT, DORMITORY), `GenderPreference`, `ModerationStatus` | ManyToOne User (postedBy), Location; OneToMany Rooms |
| `Room` | `rooms` | id, roomNumber, price, capacity, floorNumber, isAvailable, images | `RoomType` (SINGLE, DOUBLE, TRIPLE, DORMITORY) | ManyToOne Property |
| `Product` | `products` | id, title, description, price, brand, area, images, viewsCount, isAvailable, createdAt | `ListingType` (SELL, RENT, BOTH), `ProductCondition` (NEW, LIKE_NEW, GOOD, FAIR, OLD), `ModerationStatus` | ManyToOne User, Category, Location |
| `Booking` | `bookings` | id, checkIn, checkOut, totalAmount, months, message, createdAt | `BookingStatus` (PENDING, CONFIRMED, CANCELLED, COMPLETED) | ManyToOne User (booker), Property, Room |
| `Order` | `orders` | id, quantity, amount, rentStart, rentEnd, message, createdAt | `OrderType` (BUY, RENT), `OrderStatus` (PENDING, CONFIRMED, COMPLETED, CANCELLED) | ManyToOne User (buyer, seller), Product |
| `Review` | `reviews` | id, rating (1-5), comment, createdAt | `ReviewItemType` (PROPERTY, PRODUCT, USER) | ManyToOne User (reviewer) |
| `Wishlist` | `wishlists` | id, createdAt | `WishlistItemType` (PROPERTY, PRODUCT) | ManyToOne User; unique constraint on (user_id, item_type, item_id) |
| `Chat` | `chats` | id, message, isRead, timestamp | `ChatListingType` (PROPERTY, PRODUCT) | ManyToOne User (sender, receiver) |
| `UserBehavior` | `user_behaviors` | id, searchQuery, cityFilter, timestamp | `BehaviorItemType` (PROPERTY, PRODUCT), `BehaviorAction` (VIEW, SEARCH, WISHLIST, BOOK, ORDER, CONTACT) | ManyToOne User |

*Special JPA Feature*: JSON columns (`properties.amenities`, `properties.images`, `rooms.images`, `products.images`) use Hibernate 6 `@JdbcTypeCode(SqlTypes.JSON)` to map directly to `List<String>`.

### 2.5 Security & CORS Configuration
- **Stateless Architecture**: `SessionCreationPolicy.STATELESS`.
- **Authentication**: `JwtAuthenticationFilter` intercepts requests, extracts Bearer token, validates against `JwtService`, and populates `SecurityContextHolder`.
- **Public Bypasses**: Pre-flight `OPTIONS /**`, `/api/auth/**`, GET endpoints for listings, categories, locations, reviews, uploaded files, Swagger UI (`/swagger-ui.html`, `/v3/api-docs`), and public recommendations.
- **CORS Setup**: `UrlBasedCorsConfigurationSource` binds `app.cors.allowed-origins`. If contains `*` or specific origins (`http://localhost:5500`, `http://127.0.0.1:5500`, Vercel production domains), configures `setAllowedOriginPatterns` with `AllowCredentials(true)`.

---

## 3. Python Flask ML Recommendation Microservice

### 3.1 Structure & Dependency Analysis
- **Location**: `d:\Mini5th\ml-service`
- **Entry Point**: `app.py`
- **Port**: 5000 (binds to `0.0.0.0:5000`)
- **Dependencies** (`requirements.txt`):
  ```text
  flask==2.3.3
  flask-cors==4.0.0
  mysql-connector-python==8.1.0
  scikit-learn==1.3.0
  pandas==2.0.3
  numpy==1.24.4
  scipy==1.11.2
  ```
- **Virtual Environment**: `.venv` exists inside `ml-service/`.

### 3.2 Machine Learning Architecture & Algorithms
The recommendation engine uses a dual-engine hybrid architecture:

1. **Content-Based Filtering (CBF)**:
   - Uses `TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))`.
   - Feature string synthesis:
     - Properties: `title` + `description` + `type` + `area` + `city` + space-joined `amenities`.
     - Products: `title` + `description` + `category` + `condition` + `brand` + `area` + `city`.
   - Cosine similarity matrix computed via `sklearn.metrics.pairwise.cosine_similarity`.
   - Pre-trained models stored in `models/property_tfidf.pkl` (55.7 KB) and `models/product_tfidf.pkl` (131.7 KB).

2. **Collaborative Filtering (CF) & User Interaction Matrix**:
   - Queries `user_behaviors` table for interaction events.
   - Interaction Action Weights:
     - `VIEW`: 1 pt
     - `SEARCH`: 1 pt
     - `WISHLIST`: 3 pts
     - `CONTACT`: 3 pts
     - `BOOK`: 5 pts
     - `ORDER`: 5 pts
   - Time Decay Formula:
     $$\text{Decayed Score} = \text{ACTION\_WEIGHT} \times (0.9)^{\text{days\_ago}}$$
   - Interaction Threshold: If user has $\ge 5$ interactions (`MIN_INTERACTIONS_FOR_CF = 5`), the hybrid model executes:
     $$\text{Hybrid Score} = 0.6 \times \text{CF\_Score} + 0.4 \times \text{CB\_Score}$$
     Normalized using min-max scaling ($[0, 1]$).
   - If user has $< 5$ interactions (Cold-Start Problem), falls back to time-decayed trending items in their city.

3. **Exclusion Filter**:
   - Items the user has already strongly interacted with (booked properties or ordered products) are automatically filtered out.
   - Only `status = 'APPROVED'` and `is_available = TRUE` items are returned.

### 3.3 Microservice Endpoints

| Endpoint | Method | Response Structure | Purpose |
|----------|--------|--------------------|---------|
| `/health` | GET | `{"status":"healthy","database":"connected","models_loaded":true}` | Service & DB liveness probe |
| `/recommend/properties/<int:user_id>` | GET | `[2, 10, 3]` (Array of IDs) | Consumed by Spring Boot backend |
| `/recommend/products/<int:user_id>` | GET | `[5, 12, 1]` (Array of IDs) | Consumed by Spring Boot backend |
| `/recommend/properties` | GET | `{"success":true,"count":N,"property_ids":[...],"items":[...]}` | Full objects for direct client |
| `/recommend/products` | GET | `{"success":true,"count":N,"product_ids":[...],"items":[...]}` | Full objects for direct client |
| `/similar/property` | GET | `{"success":true,"property_ids":[...],"items":[...]}` | Content similarity by `propertyId` |
| `/similar/product` | GET | `{"success":true,"product_ids":[...],"items":[...]}` | Content similarity by `productId` |
| `/trending` | GET | `{"success":true,"type":"...","items":[...]}` | Location & time-decayed trending |
| `/retrain` | POST | `{"success":true,"models":{...}}` | Triggers retraining (protected by secret `"admin123"`) |

### 3.4 Fault Tolerance & Self-Healing
- **Startup Resilience**: If MySQL is unreachable at startup, `MODELS_LOADED` is set to `False` without crashing the Flask process.
- **Lazy Retry**: `ensure_models()` attempts to reload/rebuild models on incoming requests with a 15-second throttle lock (`MODEL_RETRY_SECONDS = 15`), allowing the service to self-heal as soon as MySQL comes online.
- **503 Degradation**: When the database is down, endpoints return HTTP 503 `{"success": false, "error": "database unavailable"}` which Spring Boot intercepts and gracefully falls back to local database queries.

---

## 4. Database Architecture & Schema

### 4.1 MySQL Schema Analysis (`database/01_schema.sql`)
The database contains 12 tables optimized for student accommodation and classified re-commerce:
- All tables use `ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci`.
- Foreign key constraints enforce referential integrity with `ON DELETE CASCADE` on parent user deletions and `ON DELETE SET NULL` on locations/categories.
- Targeted secondary indexes:
  - `idx_property_status`, `idx_property_type`, `idx_property_area`, `idx_property_location`
  - `idx_product_status`, `idx_product_category`, `idx_product_area`, `idx_product_location`
  - `idx_booking_booker`, `idx_booking_property`
  - `idx_order_buyer`, `idx_order_seller`, `idx_order_product`
  - `unique_wishlist (user_id, item_type, item_id)`
  - `idx_behavior_user`, `idx_behavior_item (item_type, item_id)`

### 4.2 Seed Scripts & Sample Data
The `database/` directory contains 5 SQL migration and seed scripts:
1. `01_schema.sql` (9.5 KB): Creates `staymart` database, drops old tables with foreign key checks disabled, creates all 12 tables and indexes.
2. `02_seed.sql` (1.8 KB):
   - 15 Uttarakhand locations: Rajpur Road, Clock Tower, ISBT, Patel Nagar, Ballupur, Sahastradhara Road, Raipur Road (Dehradun), Laxman Jhula, Tapovan (Rishikesh), Har Ki Pauri, SIDCUL (Haridwar), Mall Road (Mussoorie), Mall Road (Nainital), Civil Lines (Roorkee).
   - 16 categories: 6 accommodation categories (PG, Hostel, Flat, Room, Hotel, Dormitory) and 10 product categories (Electronics, Mobile Phones, Furniture, Books & Stationery, Home Appliances, Vehicles, Sports & Fitness, Home & Kitchen, Fashion, Others).
3. `03_seed_listings.sql` (23.0 KB):
   - 4 demo seller accounts: Rohit Rawat, Priya Negi, Sunita Bisht, Aman Chauhan (all using password `User@123`).
   - 12 realistic accommodations with amenities, room breakdowns, and monthly rents.
   - 20 realistic marketplace products (laptops, study tables, cycles, textbooks, mini-fridges, coolers).
4. `04_update_realistic_media.sql` (10.3 KB): Updates listings with verified, high-resolution Unsplash student photography.
5. `05_olx_amazon_listings.sql` (19.7 KB): Updates listings with realistic classified copy, authentic Uttarakhand student landmarks (e.g., Graphic Era University, UPES, FRI, Pacific Mall), and condition descriptions.

### 4.3 Database Configuration & Connection Pooling
- **Spring Boot Datasource**:
  ```yaml
  spring:
    datasource:
      url: ${DB_URL:jdbc:mysql://localhost:3306/staymart?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=Asia/Kolkata&createDatabaseIfNotExist=true&characterEncoding=utf8}
      username: ${DB_USERNAME:root}
      password: ${DB_PASSWORD:root}
      driver-class-name: com.mysql.cj.jdbc.Driver
    jpa:
      hibernate:
        ddl-auto: validate
  ```
- **Critical Deployment Note on `ddl-auto: validate`**:
  Spring Boot validates that all entity tables and column types exist in MySQL. If the database is empty, the application will fail during startup. Therefore, database seed scripts must be executed prior to the Spring Boot backend container starting.
- **HikariCP Free-Tier Recommendations**:
  Managed free-tier MySQL instances (TiDB Serverless, Aiven, Clever Cloud) enforce connection concurrency caps (typically 10 to 20 connections). To ensure stability on free cloud tiers:
  ```yaml
  spring:
    datasource:
      hikari:
        maximum-pool-size: 5
        minimum-idle: 2
        idle-timeout: 300000
        max-lifetime: 1800000
        connection-timeout: 20000
  ```

---

## 5. Free-Tier Multi-Tier Deployment Plan (Requirement R4)

A complete, production-ready full-stack deployment can be achieved with **zero ongoing monthly hosting costs ($0/mo)** using completely free tiers:

```
+------------------------------------------------------------------------------------------+
|                                    FREE DEPLOYMENT TOPOLOGY                              |
+------------------------------------------------------------------------------------------+
|  TIER 1: FRONTEND                                                                        |
|  Provider: Vercel (Hobby Tier - $0/mo forever)                                           |
|  - Edge CDN, automatic SSL/TLS, global asset caching                                     |
|  - Configured with vercel.json reverse-proxy to bypass browser CORS completely           |
+------------------------------------------------------------------------------------------+
|  TIER 2: BACKEND API                                                                     |
|  Provider: Render (Free Web Service - $0/mo) or Koyeb (Free Eco Tier - $0/mo)             |
|  - Multi-stage Docker build from repo Dockerfile                                         |
|  - Tuned with JAVA_TOOL_OPTIONS="-Xmx384m -Xms128m" to run comfortably in 512MB RAM    |
+------------------------------------------------------------------------------------------+
|  TIER 3: ML MICROSERVICE                                                                 |
|  Provider: Render (Free Web Service - Python 3.11 - $0/mo) or Hugging Face Spaces Docker |
|  - Lightweight Flask + Gunicorn worker (< 180 MB RAM footprint)                          |
+------------------------------------------------------------------------------------------+
|  TIER 4: MANAGED DATABASE                                                                |
|  Provider: TiDB Serverless (Free Forever - $0/mo) or Aiven MySQL Free Plan               |
|  - 5 GB row storage, 50 million Request Units/month free forever, TLS/SSL enabled        |
|  - 100% MySQL 8.0 wire-protocol compatible                                               |
+------------------------------------------------------------------------------------------+
```

### 5.1 Tier 1: Frontend on Vercel
- **Repository Setup**: Static files located in `frontend/`.
- **Root `vercel.json` Configuration**:
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
  *Key Advantage*: Proxying `/api/(.*)` to Render directly eliminates browser CORS preflight overhead and eliminates HTTPS mixed-content warnings.
- **Frontend `api.js` Dynamic Auto-Detection**:
  `frontend/js/api.js` lines 1-6 already contain dynamic host resolution:
  ```javascript
  const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  const BASE_URL = isLocal
    ? 'http://localhost:8080/api'
    : (window.STAYMART_API_URL || localStorage.getItem('STAYMART_API_URL') || '/api');
  ```

### 5.2 Tier 2: Spring Boot Backend on Render / Koyeb
- **Container Build**: Multi-stage `Dockerfile` (already present at root):
  - Stage 1: `maven:3.9.6-eclipse-temurin-17` builds `app.jar`.
  - Stage 2: `eclipse-temurin:17-jre-jammy` minimal runtime image.
- **Memory Optimization for Free Tiers (512 MB RAM)**:
  To prevent Render cgroup kills (`OutOfMemoryError`), configure:
  `JAVA_TOOL_OPTIONS="-Xmx384m -Xms128m -XX:+UseSerialGC"`
- **Required Environment Variables**:

| Variable | Value / Format | Purpose |
|----------|----------------|---------|
| `PORT` | `8080` (Render binds automatically via `$PORT`) | Server HTTP port |
| `DB_URL` | `jdbc:mysql://<tidb-gateway>:4000/staymart?useSSL=true&sslMode=VERIFY_IDENTITY&allowPublicKeyRetrieval=true&serverTimezone=Asia/Kolkata` | MySQL JDBC connection |
| `DB_USERNAME` | `<tidb-user>` | Database user |
| `DB_PASSWORD` | `<tidb-password>` | Database password |
| `JWT_SECRET` | `<64-char-random-hex-key>` | JWT signing token |
| `CORS_ORIGINS` | `https://<your-app>.vercel.app,http://localhost:5500` | Allowed origins |
| `ML_BASE_URL` | `https://staymart-ml.onrender.com` | Microservice interconnect |
| `SPRING_PROFILES_ACTIVE` | `prod` | Profile activation |
| `UPLOAD_DIR` | `/tmp/uploads` | Ephemeral file storage |

### 5.3 Tier 3: Flask ML Microservice on Render / Hugging Face
- **Required Missing File**: Create `ml-service/Dockerfile`:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev && rm -rf /var/lib/apt/lists/*
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt gunicorn
  COPY . .
  ENV PORT=5000
  EXPOSE 5000
  CMD ["gunicorn", "-w", "1", "--threads", "4", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
  ```
- **Required Environment Variables**:

| Variable | Value / Format | Purpose |
|----------|----------------|---------|
| `PORT` | `5000` | Flask port |
| `DB_HOST` | `<tidb-gateway>` | Database host |
| `DB_PORT` | `4000` (TiDB) or `3306` (standard MySQL) | Database port |
| `DB_USERNAME` | `<tidb-user>` | Database user |
| `DB_PASSWORD` | `<tidb-password>` | Database password |
| `DB_NAME` | `staymart` | Database name |
| `DEFAULT_CITY` | `Dehradun` | Regional cold-start default |

### 5.4 Tier 4: Free Managed MySQL on TiDB Serverless
- **Provider**: TiDB Cloud Serverless (PingCAP).
- **Free Quota**: 5 GB storage, 50 million Request Units/month free forever. No credit card required.
- **Compatibility**: Wire-protocol compatible with MySQL 8.0, supports JSON types, indexes, transactions, and foreign keys.
- **Database Initialization Steps**:
  1. Create free cluster in TiDB Cloud Console (region: AWS ap-south-1 Mumbai or nearest).
  2. Open TiDB Cloud Web SQL Editor.
  3. Execute `database/01_schema.sql` through `database/05_olx_amazon_listings.sql`.
  4. Obtain host endpoint, port (typically 4000), username, and password.

---

## 6. Existing Test Infrastructure & Verification Survey (Requirement R5)

### 6.1 Audit of Existing Automated Tests
The repository contains a custom JUnit 5 test execution framework designed to operate cleanly without requiring a local Maven command-line installation:

1. **Test Source Files** (`src/test/java/com/staymart/`):
   - `entity/EntityModelTest.java` (4 tests):
     - `testUserEntity()`: Verifies User entity builder and defaults.
     - `testBookingDefaults()`: Verifies Booking month calculation and default status (`PENDING`).
     - `testOrderDefaults()`: Verifies Order quantity and default status (`PENDING`).
     - `testPropertyDefaults()`: Verifies Property builder and room count defaults.
   - `security/JwtAuthenticationFilterTest.java` (3 tests):
     - `testOptionsShouldNotFilter()`: Verifies OPTIONS preflight requests bypass the JWT filter.
     - `testStaticAndDocsBypassed()`: Verifies `/uploads/**`, `/swagger-ui/**`, and `/v3/api-docs` bypass JWT filter.
     - `testApiEndpointsAreFiltered()`: Verifies `/api/properties`, `/api/recommendations`, and `/api/bookings` are properly intercepted.
   - `service/RecommendationServiceTest.java` (6 tests):
     - `testRecommendedPropertiesFallbackWhenMlEmpty()`: Verifies graceful fallback to `latestApproved()` when ML is empty.
     - `testRecommendedPropertiesSuccess()`: Verifies ML recommended property IDs are fetched and resolved.
     - `testSimilarPropertiesFallback()`: Verifies fallback to latest approved when ML has no similar properties.
     - `testSimilarProducts()`: Verifies ML similar products and fallback handling.
     - `testTrendingPropertiesFallback()`: Verifies trending properties fallback when ML is offline.
     - `testTrendingProductsFallback()`: Verifies trending products fallback when ML is offline.

2. **Test Runner Framework**:
   - `src/test/java/com/staymart/TestRunner.java`: Implements a JUnit 5 Launcher program that selects the test classes, executes them, collects summary statistics via `SummaryGeneratingListener`, and exits with code 0 on success or code 1 on failure.
   - `scripts/run_backend_tests.py`: Python automation script that discovers all cached JAR dependencies in `C:\Users\divya\.m2\repository`, builds an `@argfile` classpath argument, compiles `src/test/java/**/*.java` into `target/test-classes`, and invokes `java com.staymart.TestRunner`.

3. **Current Execution Status**:
   - **Command**: `python scripts/run_backend_tests.py`
   - **Output Result**:
     ```
     === Compiling StayMart Backend Test Suites ===
     Found 4 test source files
     Compilation successful!
     === Running StayMart Backend Tests via JUnit 5 Launcher ===
     [ 4 containers found / 4 successful ]
     [ 13 tests found / 13 tests started / 13 tests successful / 0 failed ]
     ALL TESTS PASSED SUCCESSFULLY!
     SUCCESS: All backend tests passed!
     ```
   - **Exit Code**: 0
   - **Duration**: ~208 ms

### 6.2 Missing Test Coverage & R5 Requirements
Currently, the repository lacks automated tests in three critical areas required by R5:
1. **Automated ML Service Tests**: No test suite exists in `ml-service/` to verify TF-IDF vectorization, cosine similarity, time-decay scoring, or cold-start fallback without requiring a live database.
2. **Responsive Layout & Mobile Viewport Tests**: No automated checks verify that the UI renders properly on 375px (mobile), 768px (tablet), and 1280px+ (desktop) viewports without horizontal scrollbar overflow or component collisions.
3. **Multi-Tier API Smoke Tests**: No automated end-to-end smoke test script validates all public and authenticated endpoints across Frontend, Backend, and ML services.

### 6.3 Comprehensive Automated Verification Suite Design (R5)
To fulfill Requirement R5 with 100% exit-code 0 compliance, three new verification scripts should be implemented under `scripts/`:

#### Verification Script 1: Build & Component Verification (`scripts/verify_build.py`)
- **Backend Build Stability**: Compiles all Java production and test sources against `.m2` dependencies or Maven.
- **ML Microservice Imports & Model Integrity**: Verifies all Python imports (`flask`, `sklearn`, `pandas`, `numpy`, `mysql.connector`) and validates that pickle files (`property_tfidf.pkl`, `product_tfidf.pkl`) deserialize correctly.
- **Frontend Asset Integrity**: Scans all 11 HTML files, 27 JS files, and CSS stylesheets, verifying valid links, script references, and zero 404 resource references.

#### Verification Script 2: Mobile Viewport Responsiveness Verification (`scripts/verify_responsiveness.py`)
- Uses the verified Google Chrome installation (`C:\Program Files\Google\Chrome\Application\chrome.exe`) in `--headless=new` mode (established in `scripts/capture_all_screenshots.py`).
- Tests key application pages (`index.html`, `search-properties.html`, `search-products.html`, `property-detail.html`, `product-detail.html`, `login.html`) across 3 viewports:
  - **Mobile**: 375 x 667 px
  - **Tablet**: 768 x 1024 px
  - **Desktop**: 1280 x 800 px
- Automated checks:
  1. Validates presence of `<meta name="viewport" content="width=device-width, initial-scale=1.0">`.
  2. Executes headless DOM inspection via Chrome DevTools protocol / virtual evaluation: `document.documentElement.scrollWidth <= window.innerWidth` (verifies zero horizontal overflow).
  3. Verifies container elements have responsive CSS flex/grid rules and media queries.

#### Verification Script 3: Multi-Tier API Smoke Tests (`scripts/verify_api_smoke.py`)
- Performs health and contract verification across both Backend and ML service:
  - **Backend Public API Contract**:
    - `GET /api/locations` returns 200 with list of Uttarakhand cities.
    - `GET /api/categories` returns 200 with accommodation and product categories.
    - `GET /api/properties` returns 200 with pagination structure (`content`, `totalElements`).
    - `GET /api/products` returns 200 with pagination structure.
    - `GET /api/recommendations/properties/trending` returns 200 with listing items.
    - `GET /swagger-ui.html` and `GET /v3/api-docs` return 200.
  - **ML Microservice Contract**:
    - `GET /health` returns 200 (or mock health payload).
    - `GET /trending?type=PROPERTY` returns JSON with `property_ids` array.
    - `GET /similar/property?propertyId=1` returns JSON with `property_ids` array.
  - **Offline Fallback Smoke Test**:
    - Validates that when ML service is offline, backend `/api/recommendations/**` still returns HTTP 200 with fallback listings.

#### Master Verification Runner (`scripts/run_all_tests.py`)
- Runs existing backend tests + all 3 verification scripts in sequence.
- Prints a clean, colorized ANSI test report.
- Exits with code 0 if all tests pass.

---

## 7. Actionable Implementation Recommendations

### For Backend Engineers:
1. **Public Marketplace Statistics Endpoint**:
   - `AdminController.java` currently restricts `/api/admin/stats` and `/api/admin/analytics` to `ROLE_ADMIN`.
   - To support Requirement R2 (student marketplace stats on public landing/search pages), add a public endpoint `GET /api/properties/stats` or `GET /api/marketplace/stats` that exposes aggregate counts (total active listings, average rent in Dehradun, total student savings, and occupancy rates) without authentication.
2. **Container JVM Memory Flags**:
   - Add `ENV JAVA_TOOL_OPTIONS="-Xmx384m -Xms128m -XX:+UseSerialGC"` to the root `Dockerfile` to guarantee stability on Render's 512 MB free tier.

### For ML Engineers:
1. **Containerization**:
   - Add `ml-service/Dockerfile` based on `python:3.11-slim` with gunicorn.
2. **Dynamic Admin Secret**:
   - Update `app.py` line 262 to read `ML_ADMIN_SECRET = os.getenv('ML_ADMIN_SECRET', 'admin123')` instead of hardcoding `'admin123'`.

### For Frontend Engineers:
1. **Vercel Reverse Proxy Rewrites**:
   - Include `/api/(.*)` rewrite in `vercel.json` pointing to the deployed backend URL to eliminate cross-origin request issues.
2. **Mobile Viewport Optimization**:
   - Ensure all tables, filter sidebars, and cards use CSS grid/flex wrapping with `max-width: 100%` and `overflow-x: hidden` to prevent mobile horizontal scrollbar leakage.

### For QA / Testing Engineers:
1. **Implement R5 Test Suite**:
   - Create `scripts/verify_build.py`, `scripts/verify_responsiveness.py`, `scripts/verify_api_smoke.py`, and `scripts/run_all_tests.py`.
   - Ensure all scripts execute with exit code 0.

---

## 8. Summary Conclusion

The StayMart repository possesses a solid, well-architected foundation across its Spring Boot backend, Python Flask ML service, MySQL database, and static frontend. All 13 existing backend unit/integration tests pass with 100% success rate. The deployment plan to free cloud tiers (Vercel + Render + TiDB Serverless) is completely viable with zero monthly hosting costs. Clear architectural paths for the public statistics endpoint (R2) and the automated verification suite (R5) are established.
