import json
import logging
from datetime import datetime

import recommender

logger = logging.getLogger(__name__)


def train_and_save_all():
    try:
        summary = recommender.save_all_models()
        result = {
            'success': True,
            'models': summary,
            'timestamp': datetime.now().isoformat()
        }
        logger.info("Retraining completed: %s", json.dumps(summary))
        return result
    except Exception as exc:
        logger.exception("Retraining failed")
        return {
            'success': False,
            'error': str(exc),
            'timestamp': datetime.now().isoformat()
        }