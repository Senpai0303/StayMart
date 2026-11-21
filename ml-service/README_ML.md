# StayMart ML Recommendation Service

Python Flask microservice that powers StayMart's recommendation engine (TF-IDF user-profile and item-similarity scoring) and feeds the Spring Boot backend.

## Setup

```bash
cd ml-service
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Database credentials are read from environment variables (defaults match local dev):

```text
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=root
DB_PASSWORD=root
DB_NAME=staymart
```

The service expects the `staymart` MySQL schema (from Part 1) — `user_behaviors`, `properties`, `products`, `users`, `locations`, `reviews`, `categories`.

## Run

```bash
python app.py
```

The service starts on `http://localhost:5000`. On startup it loads the TF-IDF models from `models/` (created automatically); if a model file is missing or stale it rebuilds both from MySQL. If MySQL is unreachable `/health` reports `503` with `database: disconnected` and the failure is logged explicitly.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommend/properties/<user_id>?city=Dehradun&limit=10` | Ordered property ID array |
| GET | `/recommend/products/<user_id>?city=Dehradun&limit=10` | Ordered product ID array |
| GET | `/recommend/properties?userId=1&city=Dehradun&limit=10` | Personalized property recommendations (full objects) |
| GET | `/recommend/products?userId=1&city=Dehradun&limit=10` | Personalized product recommendations (full objects) |
| GET | `/similar/property?propertyId=1&limit=5` | Content-similar properties |
| GET | `/similar/product?productId=1&limit=5` | Content-similar products |
| GET | `/trending?city=Dehradun&type=PROPERTY&limit=10` | Time-decayed trending items |
| GET | `/health` | `{"status":"healthy","database":"connected","models_loaded":true}` when MySQL is reachable (`503` otherwise) |
| POST | `/retrain` | Rebuild all models (body: `{"secret": "admin123"}`) |

All responses are JSON. The ID-path endpoints return a plain ordered array such as `[2, 10, 3]`. The query endpoints return `{"success": true, "count": N, "items": [...]}`. Failures return `{"success": false, "error": "..."}` (or a `503` health payload when MySQL is down).

## How it works

- **New users** (fewer than `MIN_INTERACTIONS_FOR_CF` = 5 behavior records) → trending items in their city (`Dehradun` by default).
- **Users with 5+ interactions** → Hybrid (60% TF-IDF user-profile similarity + 40% item-to-item cosine similarity), min-max normalized into a 0–1 blended score.
- **"Similar items"** → TF-IDF + cosine similarity over text features:
  - Property: title + description + type + area + city + amenities
  - Product: title + description + category + condition + brand + area + city
- **Trending** → time-decayed score over the last `TRENDING_DAYS` (7):
  `score += ACTION_WEIGHTS[action] * TIME_DECAY_FACTOR ^ days_ago`
  Action weights: VIEW/SEARCH=1, WISHLIST/CONTACT=3, BOOK/ORDER=5.
- Results always exclude items the user already booked (properties) or ordered (products), and only include `status='APPROVED'` and `is_available=TRUE` items.
- **Cold start / no behavior data** → location-based popularity (products by `views_count DESC`, properties by recency).

## Model files (auto-generated in `models/`)

- `property_tfidf.pkl`, `product_tfidf.pkl` — `{vectorizer, tfidf_matrix, similarity_matrix, ids}` built with scikit-learn TF-IDF + cosine similarity

Run `POST /retrain` (or restart the service) after moderation churn, or add a scheduler to rebuild models periodically.

## Retraining

```bash
curl -X POST http://localhost:5000/retrain \
     -H "Content-Type: application/json" \
     -d '{"secret": "admin123"}'
```

## Uttarakhand cities supported

Dehradun, Rishikesh, Haridwar, Mussoorie, Nainital, Roorkee, Haldwani, Kashipur, Rudrapur