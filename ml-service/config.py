DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'staymart'
}

MODEL_DIR = 'models/'

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

DEFAULT_CITY = 'Dehradun'

MIN_INTERACTIONS_FOR_CF = 5

TRENDING_DAYS = 7

TIME_DECAY_FACTOR = 0.9