import json
import logging
import os
import pickle
from datetime import datetime

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import db_connector
from config import (ACTION_WEIGHTS, DEFAULT_CITY, MIN_INTERACTIONS_FOR_CF,
                    MODEL_DIR, TIME_DECAY_FACTOR, TRENDING_DAYS)

logger = logging.getLogger(__name__)

CF_WEIGHT = 0.6
CB_WEIGHT = 0.4

property_tfidf_data = None
product_tfidf_data = None


def _ensure_model_dir():
    os.makedirs(MODEL_DIR, exist_ok=True)


def _model_path(item_type, kind='tfidf'):
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


def _build_content_model(item_type, rows, text_builder):
    ids = [int(row['id']) for row in rows]
    texts = [text_builder(row) for row in rows]

    if texts:
        vectorizer = TfidfVectorizer(stop_words='english', max_features=5000, ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(texts)
        similarity_matrix = cosine_similarity(tfidf_matrix)
    else:
        vectorizer = None
        tfidf_matrix = None
        similarity_matrix = None

    data = {
        'vectorizer': vectorizer,
        'tfidf_matrix': tfidf_matrix,
        'similarity_matrix': similarity_matrix,
        'ids': ids
    }

    with open(_model_path(item_type), 'wb') as handle:
        pickle.dump(data, handle)

    logger.info("Built %s TF-IDF model with %d items", item_type, len(ids))
    return data


def build_property_content_matrix():
    global property_tfidf_data
    _ensure_model_dir()
    rows = db_connector.fetch_approved_properties()
    property_tfidf_data = _build_content_model('PROPERTY', rows, _property_text)
    return property_tfidf_data


def build_product_content_matrix():
    global product_tfidf_data
    _ensure_model_dir()
    rows = db_connector.fetch_approved_products()
    product_tfidf_data = _build_content_model('PRODUCT', rows, _product_text)
    return product_tfidf_data


def save_all_models():
    _ensure_model_dir()

    global property_tfidf_data, product_tfidf_data

    property_tfidf_data = build_property_content_matrix()
    product_tfidf_data = build_product_content_matrix()

    summary = {
        'property_tfidf_items': len(property_tfidf_data['ids']),
        'product_tfidf_items': len(product_tfidf_data['ids'])
    }
    logger.info("ML models saved: %s", summary)
    return summary


def _load_content_model(item_type):
    with open(_model_path(item_type), 'rb') as handle:
        data = pickle.load(handle)
    required = ('vectorizer', 'tfidf_matrix', 'similarity_matrix', 'ids')
    if not all(key in data for key in required):
        raise ValueError(f"{item_type} model file is from an older format and must be rebuilt")
    return data


def load_all_models():
    global property_tfidf_data, product_tfidf_data

    property_tfidf_data = _load_content_model('PROPERTY')
    product_tfidf_data = _load_content_model('PRODUCT')

    logger.info("Loaded TF-IDF models from %s", MODEL_DIR)
    return True


def load_or_train_all_models():
    _ensure_model_dir()
    try:
        paths = [_model_path('PROPERTY'), _model_path('PRODUCT')]
        if all(os.path.exists(path) for path in paths):
            try:
                load_all_models()
                return True
            except (ValueError, EOFError, pickle.UnpicklingError) as exc:
                logger.warning("Stored ML models are unusable (%s); rebuilding from MySQL", exc)

        logger.info("Model files missing or stale, training fresh TF-IDF models")
        save_all_models()
        return True
    except Exception:
        logger.exception("Could not prepare ML models")
        return False


def _data_for(item_type):
    return property_tfidf_data if item_type == 'PROPERTY' else product_tfidf_data


def _text_for(item_type, row):
    return _property_text(row) if item_type == 'PROPERTY' else _product_text(row)


def _details_for(item_type, ids):
    if item_type == 'PROPERTY':
        return db_connector.fetch_property_details_bulk(ids)
    return db_connector.fetch_product_details_bulk(ids)


def _approved_item_ids(item_type, city=None):
    if item_type == 'PROPERTY':
        rows = db_connector.fetch_approved_properties(city=city)
    else:
        rows = db_connector.fetch_approved_products(city=city)
    return [int(row['id']) for row in rows]


def get_profile_scores(user_id, item_type, all_item_ids, already_interacted):
    """Score candidates against a TF-IDF profile built from the user's own interactions."""
    data = _data_for(item_type)
    if data is None or data.get('vectorizer') is None or not data.get('ids'):
        return {}

    behaviors = db_connector.fetch_user_behaviors(user_id)
    if behaviors.empty:
        return {}

    relevant = behaviors[(behaviors['item_type'] == item_type) & (behaviors['item_id'] > 0)].copy()
    if relevant.empty:
        return {}

    weights = relevant.groupby('item_id')['action'].apply(
        lambda actions: sum(ACTION_WEIGHTS.get(action, 1) for action in actions)
    ).to_dict()

    rows = _details_for(item_type, list(weights.keys()))
    if not rows:
        return {}

    texts = []
    for row in rows:
        weight = int(min(max(round(float(weights.get(row['id'], 1))), 1), 5))
        texts.extend([_text_for(item_type, row)] * weight)

    if not texts:
        return {}

    profile_vector = data['vectorizer'].transform([' '.join(texts)])
    similarities = cosine_similarity(profile_vector, data['tfidf_matrix'])[0]

    candidates = set(all_item_ids)
    scores = {}
    for item_id, score in zip(data['ids'], similarities):
        if item_id in candidates and item_id not in already_interacted and score > 0:
            scores[item_id] = float(score)
    return scores


def get_item_similarity_scores(user_id, item_type, limit=30):
    """Item-to-item cosine scores derived from the items a user most recently viewed."""
    data = _data_for(item_type)
    if data is None or not data.get('ids') or data.get('similarity_matrix') is None:
        return {}

    behaviors = db_connector.fetch_user_behaviors(user_id)
    if behaviors.empty:
        return {}

    views = behaviors[(behaviors['item_type'] == item_type) &
                      (behaviors['action'] == 'VIEW') &
                      (behaviors['item_id'] > 0)].copy()
    if views.empty:
        return {}

    views = views.sort_values('timestamp', ascending=False).head(10)

    ids = data['ids']
    index_of = {item_id: index for index, item_id in enumerate(ids)}
    similarity_matrix = data['similarity_matrix']
    interacted = set(db_connector.get_user_interacted_ids(user_id, item_type, strong_only=False))

    scores = {}
    for position, (_, behavior) in enumerate(views.iterrows()):
        viewed_id = int(behavior['item_id'])
        viewed_index = index_of.get(viewed_id)
        if viewed_index is None:
            continue

        recency_weight = 1.0 / (position + 1)
        for index, candidate_id in enumerate(ids):
            if candidate_id == viewed_id or candidate_id in interacted:
                continue
            contribution = float(similarity_matrix[viewed_index][index]) * recency_weight
            if contribution > 0:
                scores[candidate_id] = scores.get(candidate_id, 0.0) + contribution

    ranked = sorted(scores.items(), key=lambda pair: pair[1], reverse=True)
    return dict(ranked[:limit * 3])


def _similar_items(item_type, item_id, limit=5):
    data = _data_for(item_type)
    if data is None or not data.get('ids') or data.get('similarity_matrix') is None:
        return []

    ids = data['ids']
    if item_id not in ids:
        return []

    row = data['similarity_matrix'][ids.index(item_id)]
    ranked = sorted(range(len(row)), key=lambda index: row[index], reverse=True)

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
    return _similar_items('PROPERTY', int(property_id), limit)


def get_similar_products(product_id, limit=5):
    return _similar_items('PRODUCT', int(product_id), limit)


def hybrid_recommend(user_id, item_type, city=None, limit=10):
    approved_ids = _approved_item_ids(item_type, city=city)
    if not approved_ids:
        return []

    strong_excluded = set(db_connector.get_user_interacted_ids(user_id, item_type, strong_only=True))
    already_interacted = set(db_connector.get_user_interacted_ids(user_id, item_type, strong_only=False))

    candidates = [item_id for item_id in approved_ids if item_id not in strong_excluded]
    if not candidates:
        return []

    profile_scores = get_profile_scores(user_id, item_type, candidates, already_interacted)
    item_scores = {item_id: score for item_id, score in
                   get_item_similarity_scores(user_id, item_type, limit).items()
                   if item_id in set(candidates)}

    if profile_scores and item_scores:
        profile_normalized = _min_max_normalize(profile_scores)
        item_normalized = _min_max_normalize(item_scores)
        final_scores = {}
        for item_id in candidates:
            combined = (CF_WEIGHT * profile_normalized.get(item_id, 0.0) +
                        CB_WEIGHT * item_normalized.get(item_id, 0.0))
            if combined > 0:
                final_scores[item_id] = combined
        return [item_id for item_id, _ in
                sorted(final_scores.items(), key=lambda pair: pair[1], reverse=True)][:limit]

    if profile_scores:
        profile_normalized = _min_max_normalize(profile_scores)
        return [item_id for item_id, _ in
                sorted(profile_normalized.items(), key=lambda pair: pair[1], reverse=True)][:limit]

    if item_scores:
        item_normalized = _min_max_normalize(item_scores)
        return [item_id for item_id, _ in
                sorted(item_normalized.items(), key=lambda pair: pair[1], reverse=True)][:limit]

    return _cold_start_recommendations(item_type, city or DEFAULT_CITY, limit)


def _cold_start_recommendations(item_type, city, limit=10):
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
        return _cold_start_recommendations(item_type, city, limit)

    valid_set = set(_approved_item_ids(item_type, city=city))
    filtered = [item_id for item_id in ranked_ids if item_id in valid_set]
    return filtered[:limit]
