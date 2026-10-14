import json
import logging
import os
import pickle
from datetime import datetime

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, PredictionImpossible, Reader, SVD

import db_connector
from config import (ACTION_WEIGHTS, DEFAULT_CITY, MIN_INTERACTIONS_FOR_CF,
                    MODEL_DIR, TIME_DECAY_FACTOR, TRENDING_DAYS)

logger = logging.getLogger(__name__)

CF_WEIGHT = 0.6
CB_WEIGHT = 0.4

property_svd_model = None
product_svd_model = None
property_tfidf_data = None
product_tfidf_data = None


def _ensure_model_dir():
    os.makedirs(MODEL_DIR, exist_ok=True)


def _model_path(item_type, kind='svd'):
    return os.path.join(MODEL_DIR, f"{item_type.lower()}_{kind}.pkl")


def _min_max_normalize(scores):
    if not scores:
        return {}
    values = list(scores.values())
    low, high = min(values), max(values)
    if high == low:
        return {key: 1.0 for key in scores}
    return {key: (value - low) / (high - low) for key, value in scores.items()}


def _to_datetime(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        except ValueError:
            return datetime.min
    return datetime.min


def build_interaction_matrix(behaviors_df, item_type):
    df = behaviors_df[behaviors_df['item_type'] == item_type].copy()
    df = df[df['item_id'] > 0]
    if df.empty:
        return pd.DataFrame(columns=['user_id', 'item_id', 'rating'])

    df['weight'] = df['action'].map(ACTION_WEIGHTS).fillna(1).astype(float)
    grouped = df.groupby(['user_id', 'item_id'])['weight'].sum().reset_index()

    max_score = float(grouped['weight'].max()) if not grouped.empty else 0.0
    if max_score > 0:
        grouped['rating'] = 1 + (grouped['weight'] / max_score) * 4
    else:
        grouped['rating'] = 1.0

    return grouped[['user_id', 'item_id', 'rating']]


def train_cf_model(item_type):
    _ensure_model_dir()
    behaviors = db_connector.fetch_all_behaviors()
    if behaviors.empty:
        logger.info("No behavior data to train %s SVD model", item_type)
        return None

    matrix = build_interaction_matrix(behaviors, item_type)
    if matrix.empty:
        logger.info("No interactions to train %s SVD model", item_type)
        return None

    reader = Reader(rating_scale=(1, 5))
    dataset = Dataset.load_from_df(matrix[['user_id', 'item_id', 'rating']], reader)
    trainset = dataset.build_full_trainset()

    algorithm = SVD(n_factors=50, n_epochs=20, random_state=42)
    algorithm.fit(trainset)

    path = _model_path(item_type, 'svd')
    with open(path, 'wb') as handle:
        pickle.dump(algorithm, handle)

    logger.info("Trained %s SVD model with %d users and %d items",
                item_type, trainset.n_users, trainset.n_items)
    return algorithm


def get_cf_recommendations(user_id, item_type, all_item_ids, already_interacted):
    model = property_svd_model if item_type == 'PROPERTY' else product_svd_model
    if model is None or not all_item_ids:
        return {}

    scores = {}
    for item_id in all_item_ids:
        if item_id in already_interacted:
            continue
        try:
            prediction = model.predict(int(user_id), int(item_id))
            scores[item_id] = float(prediction.est)
        except (PredictionImpossible, ValueError, AttributeError):
            scores[item_id] = 0.0

    return scores


def _property_text(property_row):
    amenities = property_row.get('amenities') or []
    if isinstance(amenities, str):
        try:
            amenities = json.loads(amenities)
        except ValueError:
            amenities = []
    parts = [
        property_row.get('title', ''),
        property_row.get('description') or '',
        property_row.get('type') or '',
        property_row.get('area') or property_row.get('location_area') or '',
        property_row.get('city') or '',
        ' '.join(str(amenity) for amenity in amenities if amenity)
    ]
    return ' '.join(str(part).strip() for part in parts if part)


def _product_text(product_row):
    parts = [
        product_row.get('title', ''),
        product_row.get('description') or '',
        product_row.get('category_name') or '',
        product_row.get('condition') or '',
        product_row.get('brand') or '',
        product_row.get('area') or product_row.get('location_area') or '',
        product_row.get('city') or ''
    ]
    return ' '.join(str(part).strip() for part in parts if part)


def build_property_content_matrix():
    global property_tfidf_data
    _ensure_model_dir()

    properties = db_connector.fetch_approved_properties()
    ids = [int(row['id']) for row in properties]
    texts = [_property_text(row) for row in properties]

    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    if texts:
        tfidf = vectorizer.fit_transform(texts)
    else:
        empty_frame = pd.Series([''])
        tfidf = vectorizer.fit_transform(empty_frame)

    similarity = cosine_similarity(tfidf)
    data = {
        'vectorizer': vectorizer,
        'matrix': similarity,
        'ids': ids
    }

    with open(_model_path('PROPERTY', 'tfidf'), 'wb') as handle:
        pickle.dump(data, handle)

    property_tfidf_data = data
    logger.info("Built property content matrix with %d items", len(ids))
    return data


def build_product_content_matrix():
    global product_tfidf_data
    _ensure_model_dir()

    products = db_connector.fetch_approved_products()
    ids = [int(row['id']) for row in products]
    texts = [_product_text(row) for row in products]

    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    if texts:
        tfidf = vectorizer.fit_transform(texts)
    else:
        empty_frame = pd.Series([''])
        tfidf = vectorizer.fit_transform(empty_frame)

    similarity = cosine_similarity(tfidf)
    data = {
        'vectorizer': vectorizer,
        'matrix': similarity,
        'ids': ids
    }

    with open(_model_path('PRODUCT', 'tfidf'), 'wb') as handle:
        pickle.dump(data, handle)

    product_tfidf_data = data
    logger.info("Built product content matrix with %d items", len(ids))
    return data


def _similar_items(data, item_id, limit=5):
    if data is None or not data.get('ids'):
        return []

    ids = data['ids']
    if item_id not in ids:
        return []

    index = ids.index(item_id)
    row = data['matrix'][index]

    ranked = sorted(range(len(row)), key=lambda j: row[j], reverse=True)

    results = []
    for position in ranked:
        candidate_id = ids[position]
        if candidate_id == item_id or candidate_id is None:
            continue
        results.append(int(candidate_id))
        if len(results) >= limit:
            break
    return results


def get_similar_properties(property_id, limit=5):
    return _similar_items(property_tfidf_data, int(property_id), limit)


def get_similar_products(product_id, limit=5):
    return _similar_items(product_tfidf_data, int(product_id), limit)


def get_cb_recommendations(user_id, item_type, limit=10):
    behaviors = db_connector.fetch_user_behaviors(user_id)
    if behaviors.empty:
        return {}

    views = behaviors[(behaviors['item_type'] == item_type) &
                      (behaviors['action'] == 'VIEW') &
                      (behaviors['item_id'] > 0)].copy()
    if views.empty:
        return {}

    views = views.sort_values('timestamp', ascending=False).head(10)

    data = property_tfidf_data if item_type == 'PROPERTY' else product_tfidf_data
    if data is None or not data.get('ids'):
        return {}

    ids = data['ids']
    matrix = data['matrix']
    interacted = set(db_connector.get_user_interacted_ids(user_id, item_type, strong_only=False))

    scores = {}
    for position, (_, behavior) in enumerate(views.iterrows()):
        viewed_id = int(behavior['item_id'])
        if viewed_id not in ids:
            continue

        viewed_index = ids.index(viewed_id)
        similarity_row = matrix[viewed_index]
        recency_weight = 1.0 / (position + 1)

        for j in range(len(ids)):
            candidate_id = ids[j]
            if candidate_id == viewed_id or candidate_id in interacted or candidate_id is None:
                continue
            contribution = float(similarity_row[j]) * recency_weight
            if contribution > 0:
                scores[candidate_id] = scores.get(candidate_id, 0.0) + contribution

    scores = {item_id: score for item_id, score in scores.items() if score > 0}
    ranked = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
    return dict(ranked[:limit * 3])


def _approved_item_ids(item_type, city=None):
    if item_type == 'PROPERTY':
        rows = db_connector.fetch_approved_properties(city=city)
    else:
        rows = db_connector.fetch_approved_products(city=city)
    return [int(row['id']) for row in rows]


def hybrid_recommend(user_id, item_type, city=None, limit=10):
    approved_ids = _approved_item_ids(item_type, city=city)
    if not approved_ids:
        return []

    strong_excluded = set(db_connector.get_user_interacted_ids(user_id, item_type, strong_only=True))
    already_interacted = set(db_connector.get_user_interacted_ids(user_id, item_type, strong_only=False))

    candidates = [item_id for item_id in approved_ids if item_id not in strong_excluded]
    candidate_set = set(candidates)

    cf_scores = get_cf_recommendations(user_id, item_type, candidates, already_interacted)
    cb_scores = {item_id: score for item_id, score
                 in get_cb_recommendations(user_id, item_type, limit * 3).items()
                 if item_id in candidate_set}

    if cf_scores and cb_scores:
        cf_normalized = _min_max_normalize(cf_scores)
        cb_normalized = _min_max_normalize(cb_scores)

        final_scores = {}
        for item_id in candidates:
            combined = (CF_WEIGHT * cf_normalized.get(item_id, 0.0) +
                        CB_WEIGHT * cb_normalized.get(item_id, 0.0))
            if combined > 0:
                final_scores[item_id] = combined

        sorted_ids = [item_id for item_id, _ in
                      sorted(final_scores.items(), key=lambda pair: pair[1], reverse=True)]
    elif cb_scores:
        cb_normalized = _min_max_normalize(cb_scores)
        sorted_ids = [item_id for item_id, _ in
                      sorted(cb_normalized.items(), key=lambda pair: pair[1], reverse=True)
                      if item_id in candidate_set]
    elif cf_scores:
        cf_normalized = _min_max_normalize(cf_scores)
        sorted_ids = [item_id for item_id, _ in
                      sorted(cf_normalized.items(), key=lambda pair: pair[1], reverse=True)
                      if item_id in candidate_set]
    else:
        return _popularity_fallback(item_type, city or DEFAULT_CITY, limit)

    return sorted_ids[:limit]


def _popularity_fallback(item_type, city, limit=10):
    if item_type == 'PROPERTY':
        rows = db_connector.fetch_approved_properties(city=city)
        rows = sorted(rows, key=lambda row: _to_datetime(row.get('created_at')), reverse=True)
        return [int(row['id']) for row in rows[:limit]]

    rows = db_connector.fetch_approved_products(city=city)
    rows = sorted(rows, key=lambda row: row.get('views_count') or 0, reverse=True)
    return [int(row['id']) for row in rows[:limit]]


def get_trending(item_type, city=DEFAULT_CITY, limit=10):
    rows = db_connector.fetch_trending_raw(item_type, city, TRENDING_DAYS)

    now = datetime.now()
    scores = {}
    for row in rows:
        item_id = int(row['item_id'])
        if item_id <= 0:
            continue

        action = row.get('action')
        timestamp = row.get('timestamp')
        if timestamp is None:
            days_ago = 0.0
        elif isinstance(timestamp, str):
            try:
                parsed = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
                days_ago = max(0.0, (now - parsed).total_seconds() / 86400.0)
            except ValueError:
                days_ago = 0.0
        else:
            days_ago = max(0.0, (now - timestamp).total_seconds() / 86400.0)

        weight = ACTION_WEIGHTS.get(action, 1)
        scores[item_id] = scores.get(item_id, 0.0) + weight * (TIME_DECAY_FACTOR ** days_ago)

    ranked_ids = [item_id for item_id, _ in
                  sorted(scores.items(), key=lambda pair: pair[1], reverse=True)]

    if not ranked_ids:
        ranked_ids = _popularity_fallback(item_type, city, limit)
        return ranked_ids[:limit]

    valid_set = set(_approved_item_ids(item_type, city=city))
    filtered = [item_id for item_id in ranked_ids if item_id in valid_set]
    return filtered[:limit]


def save_all_models():
    _ensure_model_dir()
    summary = {}

    global property_svd_model, product_svd_model, property_tfidf_data, product_tfidf_data

    property_tfidf_data = build_property_content_matrix()
    summary['property_tfidf_items'] = len(property_tfidf_data['ids'])

    product_tfidf_data = build_product_content_matrix()
    summary['product_tfidf_items'] = len(product_tfidf_data['ids'])

    property_svd_model = train_cf_model('PROPERTY')
    product_svd_model = train_cf_model('PRODUCT')

    summary['property_svd'] = property_svd_model is not None
    summary['product_svd'] = product_svd_model is not None

    logger.info("All models saved: %s", summary)
    return summary


def load_all_models():
    global property_svd_model, product_svd_model, property_tfidf_data, product_tfidf_data

    with open(_model_path('PROPERTY', 'svd'), 'rb') as handle:
        property_svd_model = pickle.load(handle)
    with open(_model_path('PRODUCT', 'svd'), 'rb') as handle:
        product_svd_model = pickle.load(handle)
    with open(_model_path('PROPERTY', 'tfidf'), 'rb') as handle:
        property_tfidf_data = pickle.load(handle)
    with open(_model_path('PRODUCT', 'tfidf'), 'rb') as handle:
        product_tfidf_data = pickle.load(handle)

    logger.info("Loaded all models from %s", MODEL_DIR)
    return True


def load_or_train_all_models():
    _ensure_model_dir()
    try:
        paths = [
            _model_path('PROPERTY', 'svd'),
            _model_path('PRODUCT', 'svd'),
            _model_path('PROPERTY', 'tfidf'),
            _model_path('PRODUCT', 'tfidf')
        ]
        if all(os.path.exists(path) for path in paths):
            load_all_models()
            return True

        logger.info("Model files missing, training fresh models")
        save_all_models()
        return True
    except Exception as exc:
        logger.error("Could not prepare ML models: %s", exc)
        return False