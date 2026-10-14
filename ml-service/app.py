import logging
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

try:
    MODELS_LOADED = recommender.load_or_train_all_models()
    logger.info("Startup models_loaded=%s", MODELS_LOADED)
except Exception as exc:
    logger.exception("Startup model loading failed")
    MODELS_LOADED = False


@app.errorhandler(Exception)
def handle_uncaught_error(error):
    logger.exception("Unhandled exception")
    return jsonify({'success': False, 'error': str(error)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'models_loaded': MODELS_LOADED,
        'city': DEFAULT_CITY
    })


@app.route('/recommend/properties', methods=['GET'])
def recommend_properties():
    try:
        user_id = request.args.get('userId', type=int)
        city = request.args.get('city', DEFAULT_CITY)
        limit = min(request.args.get('limit', 10, type=int) or 10, 50)
        user_id = user_id if user_id is not None else 0

        behaviors = db_connector.fetch_user_behaviors(user_id)
        behavior_count = len(behaviors)

        if behavior_count >= MIN_INTERACTIONS_FOR_CF:
            item_ids = recommender.hybrid_recommend(user_id, 'PROPERTY', city, limit)
        else:
            item_ids = recommender.get_trending('PROPERTY', city, limit)

        booked_ids = set(db_connector.get_user_interacted_ids(user_id, 'PROPERTY', strong_only=True))
        item_ids = [item_id for item_id in item_ids if item_id not in booked_ids]

        items = db_connector.fetch_property_details_bulk(item_ids)

        logger.info("[%s] user=%s city=%s type=PROPERTY -> %d results",
                    datetime.now(), user_id, city, len(items))
        return jsonify({
            'success': True,
            'user_id': user_id,
            'city': city,
            'count': len(items),
            'items': items
        })
    except Exception as exc:
        logger.exception("recommend/properties failed")
        return jsonify({'success': False, 'error': str(exc)}), 200


@app.route('/recommend/products', methods=['GET'])
def recommend_products():
    try:
        user_id = request.args.get('userId', type=int)
        city = request.args.get('city', DEFAULT_CITY)
        limit = min(request.args.get('limit', 10, type=int) or 10, 50)
        user_id = user_id if user_id is not None else 0

        behaviors = db_connector.fetch_user_behaviors(user_id)
        behavior_count = len(behaviors)

        if behavior_count >= MIN_INTERACTIONS_FOR_CF:
            item_ids = recommender.hybrid_recommend(user_id, 'PRODUCT', city, limit)
        else:
            item_ids = recommender.get_trending('PRODUCT', city, limit)

        ordered_ids = set(db_connector.get_user_interacted_ids(user_id, 'PRODUCT', strong_only=True))
        item_ids = [item_id for item_id in item_ids if item_id not in ordered_ids]

        items = db_connector.fetch_product_details_bulk(item_ids)

        logger.info("[%s] user=%s city=%s type=PRODUCT -> %d results",
                    datetime.now(), user_id, city, len(items))
        return jsonify({
            'success': True,
            'user_id': user_id,
            'city': city,
            'count': len(items),
            'items': items
        })
    except Exception as exc:
        logger.exception("recommend/products failed")
        return jsonify({'success': False, 'error': str(exc)}), 200


@app.route('/similar/property', methods=['GET'])
def similar_property():
    try:
        property_id = request.args.get('propertyId', type=int)
        limit = min(request.args.get('limit', 5, type=int) or 5, 50)

        if property_id is None:
            return jsonify({'success': False, 'error': 'propertyId is required'}), 400

        item_ids = recommender.get_similar_properties(property_id, limit)
        items = db_connector.fetch_property_details_bulk(item_ids)

        logger.info("[%s] similar property=%s -> %d results",
                    datetime.now(), property_id, len(items))
        return jsonify({
            'success': True,
            'property_id': property_id,
            'count': len(items),
            'items': items
        })
    except Exception as exc:
        logger.exception("similar/property failed")
        return jsonify({'success': False, 'error': str(exc)}), 200


@app.route('/similar/product', methods=['GET'])
def similar_product():
    try:
        product_id = request.args.get('productId', type=int)
        limit = min(request.args.get('limit', 5, type=int) or 5, 50)

        if product_id is None:
            return jsonify({'success': False, 'error': 'productId is required'}), 400

        item_ids = recommender.get_similar_products(product_id, limit)
        items = db_connector.fetch_product_details_bulk(item_ids)

        logger.info("[%s] similar product=%s -> %d results",
                    datetime.now(), product_id, len(items))
        return jsonify({
            'success': True,
            'product_id': product_id,
            'count': len(items),
            'items': items
        })
    except Exception as exc:
        logger.exception("similar/product failed")
        return jsonify({'success': False, 'error': str(exc)}), 200


@app.route('/trending', methods=['GET'])
def trending():
    try:
        city = request.args.get('city', DEFAULT_CITY)
        item_type = request.args.get('type', 'PROPERTY')
        limit = min(request.args.get('limit', 10, type=int) or 10, 50)

        if item_type not in ('PROPERTY', 'PRODUCT'):
            return jsonify({'success': False, 'error': 'type must be PROPERTY or PRODUCT'}), 400

        item_ids = recommender.get_trending(item_type, city, limit)

        if item_type == 'PROPERTY':
            items = db_connector.fetch_property_details_bulk(item_ids)
        else:
            items = db_connector.fetch_product_details_bulk(item_ids)

        logger.info("[%s] trending city=%s type=%s -> %d results",
                    datetime.now(), city, item_type, len(items))
        return jsonify({
            'success': True,
            'city': city,
            'type': item_type,
            'count': len(items),
            'items': items
        })
    except Exception as exc:
        logger.exception("trending failed")
        return jsonify({'success': False, 'error': str(exc)}), 200


@app.route('/retrain', methods=['POST'])
def retrain():
    global MODELS_LOADED

    payload = request.get_json(silent=True) or {}
    if payload.get('secret') != 'admin123':
        return jsonify({'success': False, 'error': 'Invalid secret'}), 403

    result = model_trainer.train_and_save_all()
    if result.get('success'):
        MODELS_LOADED = True
        return jsonify({
            'success': True,
            'message': 'Models retrained',
            'timestamp': result.get('timestamp'),
            'models': result.get('models')
        })

    return jsonify({'success': False, 'error': result.get('error', 'Training failed')}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)