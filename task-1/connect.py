import psycopg2
from contextlib import contextmanager
from config import DB_CONFIG

from logger_config import get_logger

logger = get_logger(__name__)


@contextmanager
def create_connect():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        try:
            yield conn
        finally:
            conn.close()
    except psycopg2.OperationalError as err:
        logger.error(f"Connection failed: {err}")

