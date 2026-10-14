import json
import logging
from datetime import datetime, timedelta

import mysql.connector
import pandas as pd

from config import DB_CONFIG

logger = logging.getLogger(__name__)

BEHAVIOR_COLUMNS = ['user_id', 'item_type', 'item_id', 'action', 'timestamp', 'city_filter']

STRONG_ACTIONS = ('BOOK', 'ORDER')


def get_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn


def _cursor_result_as_frame(cursor):
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    if not rows:
        return pd.DataFrame(columns=columns if columns else BEHAVIOR_COLUMNS)
    return pd.DataFrame(rows, columns=columns)


def _cursor_result_as_dicts(cursor):
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]


def _decode_json(value):
    if value is None:
        return []
    if isinstance(value, (list, dict)):
        return value
    try:
        decoded = json.loads(value)
        return decoded if isinstance(decoded, list) else []
    except (ValueError, TypeError):
        return []


def _enrich_property_row(row):
    return dict(row, amenities=_decode_json(row.get('amenities')),
                images=_decode_json(row.get('images')))


def _enrich_product_row(row):
    return dict(row, images=_decode_json(row.get('images')))


def fetch_all_behaviors():
    query = ("SELECT user_id, item_type, item_id, action, timestamp, city_filter "
             "FROM user_behaviors")
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            return _cursor_result_as_frame(cursor)
    except Exception as exc:
        logger.error("fetch_all_behaviors failed: %s", exc)
        return pd.DataFrame(columns=BEHAVIOR_COLUMNS)


def fetch_user_behaviors(user_id):
    query = ("SELECT user_id, item_type, item_id, action, timestamp, city_filter "
             "FROM user_behaviors WHERE user_id = %s")
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, (int(user_id),))
            return _cursor_result_as_frame(cursor)
    except Exception as exc:
        logger.error("fetch_user_behaviors failed for user %s: %s", user_id, exc)
        return pd.DataFrame(columns=BEHAVIOR_COLUMNS)


def fetch_approved_properties(city=None):
    query = """
        SELECT p.id, p.title, p.description, p.type, p.gender_preference,
               p.area AS area, p.address, p.price_per_month, p.deposit_amount,
               p.amenities, p.total_rooms, p.available_rooms, p.images,
               p.is_available, p.created_at,
               l.city, l.area AS location_area, l.state, l.pincode,
               u.name AS poster_name, u.phone AS poster_phone, u.profile_pic AS poster_pic
        FROM properties p
        JOIN locations l ON p.location_id = l.id
        JOIN users u ON p.posted_by = u.id
        WHERE p.status = 'APPROVED' AND p.is_available = TRUE
    """
    params = []
    if city:
        query += " AND LOWER(l.city) = LOWER(%s)"
        params.append(city)
    query += " ORDER BY p.created_at DESC"
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            return [_enrich_property_row(row) for row in _cursor_result_as_dicts(cursor)]
    except Exception as exc:
        logger.error("fetch_approved_properties failed: %s", exc)
        return []


def fetch_approved_products(city=None):
    query = """
        SELECT p.id, p.title, p.description, p.price, p.listing_type,
               p.condition, p.brand, p.area AS area, p.images,
               p.is_available, p.views_count, p.created_at,
               c.name AS category_name, c.icon AS category_icon,
               l.city, l.area AS location_area, l.state, l.pincode,
               u.name AS poster_name, u.phone AS poster_phone, u.profile_pic AS poster_pic
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        JOIN locations l ON p.location_id = l.id
        JOIN users u ON p.posted_by = u.id
        WHERE p.status = 'APPROVED' AND p.is_available = TRUE
    """
    params = []
    if city:
        query += " AND LOWER(l.city) = LOWER(%s)"
        params.append(city)
    query += " ORDER BY p.created_at DESC"
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            return [_enrich_product_row(row) for row in _cursor_result_as_dicts(cursor)]
    except Exception as exc:
        logger.error("fetch_approved_products failed: %s", exc)
        return []


def fetch_property_by_id(property_id):
    query = """
        SELECT p.id, p.title, p.description, p.type, p.gender_preference,
               p.area AS area, p.address, p.price_per_month, p.deposit_amount,
               p.amenities, p.total_rooms, p.available_rooms, p.images,
               p.is_available, p.created_at,
               l.city, l.area AS location_area, l.state, l.pincode,
               u.name AS poster_name, u.phone AS poster_phone, u.profile_pic AS poster_pic,
               COALESCE((SELECT AVG(rating) FROM reviews
                         WHERE item_type = 'PROPERTY' AND item_id = p.id), 0) AS avg_rating,
               (SELECT COUNT(*) FROM reviews
                WHERE item_type = 'PROPERTY' AND item_id = p.id) AS rating_count
        FROM properties p
        JOIN locations l ON p.location_id = l.id
        JOIN users u ON p.posted_by = u.id
        WHERE p.id = %s
    """
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, (int(property_id),))
            rows = _cursor_result_as_dicts(cursor)
            if not rows:
                return None
            return _enrich_property_row(rows[0])
    except Exception as exc:
        logger.error("fetch_property_by_id failed for %s: %s", property_id, exc)
        return None


def fetch_product_by_id(product_id):
    query = """
        SELECT p.id, p.title, p.description, p.price, p.listing_type,
               p.condition, p.brand, p.area AS area, p.images,
               p.is_available, p.views_count, p.created_at,
               c.name AS category_name, c.icon AS category_icon,
               l.city, l.area AS location_area, l.state, l.pincode,
               u.name AS poster_name, u.phone AS poster_phone, u.profile_pic AS poster_pic,
               COALESCE((SELECT AVG(rating) FROM reviews
                         WHERE item_type = 'PRODUCT' AND item_id = p.id), 0) AS avg_rating,
               (SELECT COUNT(*) FROM reviews
                WHERE item_type = 'PRODUCT' AND item_id = p.id) AS rating_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        JOIN locations l ON p.location_id = l.id
        JOIN users u ON p.posted_by = u.id
        WHERE p.id = %s
    """
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, (int(product_id),))
            rows = _cursor_result_as_dicts(cursor)
            if not rows:
                return None
            return _enrich_product_row(rows[0])
    except Exception as exc:
        logger.error("fetch_product_by_id failed for %s: %s", product_id, exc)
        return None


def fetch_property_details_bulk(ids):
    if not ids:
        return []
    id_list = [int(i) for i in ids if i is not None]
    if not id_list:
        return []
    placeholders = ','.join(['%s'] * len(id_list))
    query = f"""
        SELECT p.id, p.title, p.description, p.type, p.gender_preference,
               p.area AS area, p.address, p.price_per_month, p.deposit_amount,
               p.amenities, p.total_rooms, p.available_rooms, p.images,
               p.is_available, p.created_at,
               l.city, l.area AS location_area, l.state, l.pincode,
               u.name AS poster_name, u.phone AS poster_phone, u.profile_pic AS poster_pic,
               COALESCE((SELECT AVG(rating) FROM reviews
                         WHERE item_type = 'PROPERTY' AND item_id = p.id), 0) AS avg_rating,
               (SELECT COUNT(*) FROM reviews
                WHERE item_type = 'PROPERTY' AND item_id = p.id) AS rating_count
        FROM properties p
        JOIN locations l ON p.location_id = l.id
        JOIN users u ON p.posted_by = u.id
        WHERE p.id IN ({placeholders})
        AND p.status = 'APPROVED' AND p.is_available = TRUE
    """
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, tuple(id_list))
            rows = [_enrich_property_row(row) for row in _cursor_result_as_dicts(cursor)]
        by_id = {row['id']: row for row in rows}
        return [by_id[i] for i in id_list if i in by_id]
    except Exception as exc:
        logger.error("fetch_property_details_bulk failed: %s", exc)
        return []


def fetch_product_details_bulk(ids):
    if not ids:
        return []
    id_list = [int(i) for i in ids if i is not None]
    if not id_list:
        return []
    placeholders = ','.join(['%s'] * len(id_list))
    query = f"""
        SELECT p.id, p.title, p.description, p.price, p.listing_type,
               p.condition, p.brand, p.area AS area, p.images,
               p.is_available, p.views_count, p.created_at,
               c.name AS category_name, c.icon AS category_icon,
               l.city, l.area AS location_area, l.state, l.pincode,
               u.name AS poster_name, u.phone AS poster_phone, u.profile_pic AS poster_pic,
               COALESCE((SELECT AVG(rating) FROM reviews
                         WHERE item_type = 'PRODUCT' AND item_id = p.id), 0) AS avg_rating,
               (SELECT COUNT(*) FROM reviews
                WHERE item_type = 'PRODUCT' AND item_id = p.id) AS rating_count
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        JOIN locations l ON p.location_id = l.id
        JOIN users u ON p.posted_by = u.id
        WHERE p.id IN ({placeholders})
        AND p.status = 'APPROVED' AND p.is_available = TRUE
    """
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, tuple(id_list))
            rows = [_enrich_product_row(row) for row in _cursor_result_as_dicts(cursor)]
        by_id = {row['id']: row for row in rows}
        return [by_id[i] for i in id_list if i in by_id]
    except Exception as exc:
        logger.error("fetch_product_details_bulk failed: %s", exc)
        return []


def fetch_trending_raw(item_type, city, days=7):
    since = datetime.now() - timedelta(days=days)
    query = """
        SELECT item_id, action, timestamp, city_filter
        FROM user_behaviors
        WHERE item_type = %s AND item_id > 0
          AND timestamp >= %s
          AND city_filter LIKE %s
    """
    params = (item_type, since, f"%{city}%")
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, params)
            return _cursor_result_as_dicts(cursor)
    except Exception as exc:
        logger.error("fetch_trending_raw failed: %s", exc)
        return []


def get_user_interacted_ids(user_id, item_type, strong_only=False):
    query = ("SELECT DISTINCT item_id FROM user_behaviors "
             "WHERE user_id = %s AND item_type = %s AND item_id > 0")
    params = [int(user_id), item_type]
    if strong_only:
        query += " AND action IN ('BOOK', 'ORDER')"
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, tuple(params))
            return [int(row[0]) for row in cursor.fetchall()]
    except Exception as exc:
        logger.error("get_user_interacted_ids failed: %s", exc)
        return []


def increment_product_views(product_id):
    query = "UPDATE products SET views_count = views_count + 1 WHERE id = %s"
    try:
        with get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(query, (int(product_id),))
    except Exception as exc:
        logger.error("increment_product_views failed for %s: %s", product_id, exc)