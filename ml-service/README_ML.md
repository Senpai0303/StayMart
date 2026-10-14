# StayMart ML Recommendation Service

Python Flask microservice that powers StayMart's recommendation engine (hybrid collaborative + content-based filtering) and feeds the Spring Boot backend.

## Setup

```bash
cd ml-service
pip install -r requirements.txt
```

Update `config.py` with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'staymart'
}
```

The service expects the `staymart` MySQL schema (from Part 1) — `user_behaviors`, `properties`, `products`, `users`, `locations`, `reviews`, `categories`.

## Run

```bash
python app.py
```

The service starts on `http://localhost:5000`. On startup it loads the 4 trained models from `models/` (created automatically); if any model file is missing it trains fresh ones from the database. If MySQL is unreachable it logs the error and keeps running — recommendations degrade gracefully to empty results.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recommend/properties?userId=1&city=Dehradun&limit=10` | Personalized property recommendations |
| GET | `/recommend/products?userId=1&city=Dehradun&limit=10` | Personalized product recommendations |
| GET | `/similar/property?propertyId=1&limit=5` | Content-similar properties |
| GET | `/similar/product?productId=1&limit=5` | Content-similar products |
| GET | `/trending?city=Dehradun&type=PROPERTY&limit=10` | Time-decayed trending items |
| GET | `/health` | Service health + model status |
| POST | `/retrain` | Rebuild all models (body: `{"secret": "admin123"}`) |

All responses are JSON. Successful calls return `{"success": true, "count": N, "items": [...]}`; failures return `{"success": false, "error": "..."}`.

## How it works

- **New users** (fewer than `MIN_INTERACTIONS_FOR_CF` = 5 behavior records) → trending items in their city (`Dehradun` by default).
- **Users with 5+ interactions** → Hybrid (60% SVD collaborative + 40% content-based TF-IDF), min-max normalized into a 0–1 blended score.
- **"Similar items"** → TF-IDF + cosine similarity over text features:
  - Property: title + description + type + area + city + amenities
  - Product: title + description + category + condition + brand + area + city
- **Trending** → time-decayed score over the last `TRENDING_DAYS` (7):
  `score += ACTION_WEIGHTS[action] * TIME_DECAY_FACTOR ^ days_ago`
  Action weights: VIEW/SEARCH=1, WISHLIST/CONTACT=3, BOOK/ORDER=5.
- Results always exclude items the user already booked (properties) or ordered (products), and only include `status='APPROVED'` and `is_available=TRUE` items.
- **Cold start / no behavior data** → location-based popularity (products by `views_count DESC`, properties by recency).

## Model files (auto-generated in `models/`)

- `property_svd.pkl`, `product_svd.pkl` — Surprise `SVD` (50 factors, 20 epochs) on 1–5 implicit-rating matrices
- `property_tfidf.pkl`, `product_tfidf.pkl` — `{vectorizer, cosine_matrix, ids}` for content similarity

Run `POST /retrain` (or edit `config.py` and restart) after moderation churn, or add a scheduler to rebuild models periodically.

## Retraining

```bash
curl -X POST http://localhost:5000/retrain \
     -H "Content-Type: application/json" \
     -d '{"secret": "admin123"}'
```

## Uttarakhand cities supported

Dehradun, Rishikesh, Haridwar, Mussoorie, Nainital, Roorkee, Haldwani, Kashipur, Rudrapur