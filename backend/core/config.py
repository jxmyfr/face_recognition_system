from dotenv import load_dotenv
import os

load_dotenv()

MATCH_THRESHOLD = 0.5
IOU_THRESHOLD = 0.5
LOG_INTERVAL_SECONDS = 10
ENCODING_FILE = 'data/known_faces.pkl'
DB_PATH = 'data/logs/logs.db'
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

MYSQL_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'charset': 'utf8mb4',
}