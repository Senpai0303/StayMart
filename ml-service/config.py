import os

MODEL_DIR = os.getenv(
    'ML_MODEL_DIR',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
)

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USERNAME', os.getenv('DB_USER', 'root')),
    'password': os.getenv('DB_PASSWORD', 'root'),
    'database': os.getenv('DB_NAME', os.getenv('DB_DATABASE', 'staymart')),
    'connection_timeout': int(os.getenv('DB_CONNECT_TIMEOUT', '5')),
}

ACTION_WEIGHTS = {
    'VIEW': 1,
    'SEARCH': 1,
    'WISHLIST': 3,
    'CONTACT': 3,
    'BOOK': 5,
    'ORDER': 5
}

UTTARAKHAND_CITIES = [
    'Dehradun', 'Rishikesh', 'Haridwar',
    'Mussoorie', 'Nainital', 'Roorkee',
    'Haldwani', 'Kashipur', 'Rudrapur'
]

DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'Dehradun')

MIN_INTERACTIONS_FOR_CF = int(os.getenv('MIN_INTERACTIONS_FOR_CF', '5'))

TRENDING_DAYS = int(os.getenv('TRENDING_DAYS', '7'))

TIME_DECAY_FACTOR = float(os.getenv('TIME_DECAY_FACTOR', '0.9'))
