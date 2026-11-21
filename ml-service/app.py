import logging
import threading
import time
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

import db_connector
import model_trainer
import recommender
from config import DEFAULT_CITY, MIN_INTERACTIONS_FOR_CF

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s - %(message)s'
)
logger = logging.getLogger('staymart-ml')

app = Flask(__name__)
CORS(app)

MODELS_LOADED = False
MODEL_RETRY_SECONDS = 15
_model_lock = threading.Lock()
_last_model_attempt = 0.0

VALID_ITEM_TYPES = ('PROPERTY', 'PRODUCT')


def ensure_models():
    """Load/train models lazily so the service self-heals if MySQL was down at startup."""
    global MODELS_LOADED, _last_model_attempt
    if MODELS_LOADED:
        return True
    with _model_lock:
        if MODELS_LOADED:
            return True
        if time.monotonic() - _last_model_attempt < MODEL_RETRY_SECONDS:
            return False
        _last_model_attempt = time.monotonic()
        MODELS_LOADED = recommender.load_or_train_all_models()
        if MODELS_LOADED:
            logger.info("Models loaded successfully (lazy retry)")
        return MODELS_LOADED


try:
    MODELS_LOADED = recommender.load_or_train_all_models()
    logger.info("Startup models_loaded=%s", MODELS_LOADED)
except Exception:
    logger.exception("Startup model loading failed")
    MODELS_LOADED = False


@app.errorhandler(Exception)
def handle_uncaught_error(error):
    logger.exception("Unhandled exception")
    return jsonify({'success': False, 'error': str(error)}), 500


def _database_unavailable_response():
    return jsonify({
        'success': False,
        'error': 'database unavailable'
    }), 503


def _parse_limit(default=10):
    value = request.args.get('limit', default, type=int)
    if value is None:
        value = default
    return min(max(value, 1), 50)


def _recommend_ids(item_type, user_id, city, limit):
    ensure_models()

    behaviors = db_connector.fetch_user_behaviors(user_id)
    if len(behaviors) >= MIN_INTERACTIONS_FOR_CF:
        item_ids = recommender.hybrid_recommend(user_id, item_type, city, limit)
    else:
        item_ids = recommender.get_trending(item_type, city, limit)

    excluded = set(db_connector.get_user_interacted_ids(user_id, item_type, strong_only=True))
    return [item_id for item_id in item_ids if item_id not in excluded][:limit]


def _items_for(item_type, item_ids):
    if item_type == 'PROPERTY':
        return db_connector.fetch_property_details_bulk(item_ids)
    return db_connector.fetch_product_details_bulk(item_ids)


def _recommend_payload(item_type, user_id, city, limit):
    item_ids = _recommend_ids(item_type, user_id, city, limit)
    items = _items_for(item_type, item_ids)
    id_key = 'property_ids' if item_type == 'PROPERTY' else 'product_ids'
    return {
        'success': True,
        'user_id': user_id,
        'city': city,
        'count': len(items),
        id_key: [int(item['id']) for item in items],
        'items': items
    }


@app.route('/health', methods=['GET'])
def health():
    connected = db_connector.database_healthy()
    if not connected:
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected'
        }), 503

    ensure_models()
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'models_loaded': MODELS_LOADED
    }), 200


@app.route('/recommend/properties', methods=['GET'])
def recommend_properties():
    if not db_connector.database_healthy():
        return _database_unavailable_response()

    user_id = request.args.get('userId', 0, type=int)
    city = request.args.get('city', DEFAULT_CITY)
    limit = _parse_limit()
    payload = _recommend_payload('PROPERTY', user_id, city, limit)
    logger.info("[%s] user=%s city=%s type=PROPERTY -> %d results",
                datetime.now(), user_id, city, payload['count'])
    return jsonify(payload)


@app.route('/recommend/properties/<int:user_id>', methods=['GET'])
def recommend_properties_for_user(user_id):
    if not db_connector.database_healthy():
        return _database_unavailable_response()

    city = request.args.get('city', DEFAULT_CITY)
    limit = _parse_limit()
    item_ids = _recommend_ids('PROPERTY', user_id, city, limit)
    logger.info("[%s] user=%s city=%s type=PROPERTY ids -> %d results",
                datetime.now(), user_id, city, len(item_ids))
    return jsonify(item_ids)


@app.route('/recommend/products', methods=['GET'])
def recommend_products():
    if not db_connector.database_healthy():
        return _database_unavailable_response()

    user_id = request.args.get('userId', 0, type=int)
    city = request.args.get('city', DEFAULT_CITY)
    limit = _parse_limit()
    payload = _recommend_payload('PRODUCT', user_id, city, limit)
    logger.info("[%s] user=%s city=%s type=PRODUCT -> %d results",
                datetime.now(), user_id, city, payload['count'])
    return jsonify(payload)


@app.route('/recommend/products/<int:user_id>', methods=['GET'])
def recommend_products_for_user(user_id):
    if not db_connector.database_healthy():
        return _database_unavailable_response()

    city = request.args.get('city', DEFAULT_CITY)
    limit = _parse_limit()
    item_ids = _recommend_ids('PRODUCT', user_id, city, limit)
    logger.info("[%s] user=%s city=%s type=PRODUCT ids -> %d results",
                datetime.now(), user_id, city, len(item_ids))
    return jsonify(item_ids)


@app.route('/similar/property', methods=['GET'])
def similar_property():
    if not db_connector.database_healthy():
        return _database_unavailable_response()

    property_id = request.args.get('propertyId', type=int)
    limit = _parse_limit(5)
    if property_id is None:
        return jsonify({'success': False, 'error': 'propertyId is required'}), 400

    ensure_models()
    item_ids = recommender.get_similar_properties(property_id, limit)
    items = db_connector.fetch_property_details_bulk(item_ids)
    logger.info("[%s] similar property=%s -> %d results",
                datetime.now(), property_id, len(items))
    return jsonify({
        'success': True,
        'property_id': property_id,
        'count': len(items),
        'property_ids': [int(item['id']) for item in items],
        'items': items
    })


@app.route('/similar/product', methods=['GET'])
def similar_product():
    if not db_connector.database_healthy():
        return _database_unavailable_response()

    product_id = request.args.get('productId', type=int)
    limit = _parse_limit(5)
    if product_id is None:
        return jsonify({'success': False, 'error': 'productId is required'}), 400

    ensure_models()
    item_ids = recommender.get_similar_products(product_id, limit)
    items = db_connector.fetch_product_details_bulk(item_ids)
    logger.info("[%s] similar product=%s -> %d results",
                datetime.now(), product_id, len(items))
    return jsonify({
        'success': True,
        'product_id': product_id,
        'count': len(items),
        'product_ids': [int(item['id']) for item in items],
        'items': items
    })


@app.route('/trending', methods=['GET'])
def trending():
    if not db_connector.database_healthy():
        return _database_unavailable_response()

    city = request.args.get('city', DEFAULT_CITY)
    item_type = request.args.get('type', 'PROPERTY')
    limit = _parse_limit()

    if item_type not in VALID_ITEM_TYPES:
        return jsonify({'success': False, 'error': 'type must be PROPERTY or PRODUCT'}), 400

    ensure_models()
    item_ids = recommender.get_trending(item_type, city, limit)
    items = _items_for(item_type, item_ids)
    id_key = 'property_ids' if item_type == 'PROPERTY' else 'product_ids'

    logger.info("[%s] trending city=%s type=%s -> %d results",
                datetime.now(), city, item_type, len(items))
    return jsonify({
        'success': True,
        'city': city,
        'type': item_type,
        'count': len(items),
        id_key: [int(item['id']) for item in items],
        'items': items
    })


@app.route('/retrain', methods=['POST'])
def retrain():
    global MODELS_LOADED

    payload = request.get_json(silent=True) or {}
    if payload.get('secret') != 'admin123':
        return jsonify({'success': False, 'error': 'Invalid secret'}), 403

    if not db_connector.database_healthy():
        return _database_unavailable_response()

    result = model_trainer.train_and_save_all()
    if result.get('success'):
        MODELS_LOADED = True
        return jsonify({
            'success': True,
            'message': 'Models retrained',
            'timestamp': result.get('timestamp'),
            'models': result.get('models')
        })

    return jsonify({'success': False, 'error': result.get('error', 'Training failed')}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
