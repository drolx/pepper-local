import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", 8080))
DATABASE_URL: str = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://pepper:pepper@localhost:15432/pepper"
)
DATABASE_LOG: bool = eval(os.getenv("DATABASE_LOG", "False"))
API_BASE_URL: str = os.getenv("API_BASE_URL", "")
API_USER: str = os.getenv("API_USER", "")
API_PASS: str = os.getenv("API_PASS", "")
# INFO: Improvements will be required for object list
API_LIST_LIMIT: str = os.getenv("API_LIST_LIMIT", "1000")
LOGIN_ENDPOINT: str = "/api/login"
GET_DEVICES_ENDPOINT: str = "/api/get_devices"
GEOCODE_URL: str = os.getenv("GEOCODE_URL", "https://nominatim.openstreetmap.org")
AUTH_INTERVAL: int = 3600
# NOTE: Value in seconds
FETCH_INTERVAL: int = int(os.getenv("FETCH_INTERVAL", 30))
# NOTE: Value in minutes
OFFLINE_INTERVAL: int = int(os.getenv("OFFLINE_INTERVAL", 90))
