from faker import Faker
import random
from connect import create_connect
from logger_config import get_logger

logger = get_logger(__name__)

# Ініціалізація Faker
faker = Faker()

# Попередньо визначені статуси
STATUS_LIST = ["new", "in progress", "completed", "archived"]

def seed_statuses():
    """Заповнює таблицю status"""
    try:
        with create_connect() as conn:
            with conn.cursor() as cursor:
                for status in STATUS_LIST:
                    cursor.execute("""
                        INSERT INTO status (name) VALUES (%s)
                        ON CONFLICT (name) DO NOTHING;
                    """, (status,))
                conn.commit()
                logger.info("Таблиця 'status' заповнена успішно.")
    except Exception as e:
        logger.error(f"Помилка при заповненні таблиці 'status': {e}")

def seed_users(count=10):
    """Заповнює таблицю users випадковими даними"""
    try:
        with create_connect() as conn:
            with conn.cursor() as cursor:
                for _ in range(count):
                    fullname = faker.name()
                    email = faker.email()
                    cursor.execute("""
                        INSERT INTO users (fullname, email)
                        VALUES (%s, %s)
                        ON CONFLICT (email) DO NOTHING;
                    """, (fullname, email))
                conn.commit()
                logger.info("Таблиця 'users' заповнена успішно.")
    except Exception as e:
        logger.error(f"Помилка при заповненні таблиці 'users': {e}")

def seed_tasks(count=20):
    """Заповнює таблицю tasks випадковими даними"""
    try:
        with create_connect() as conn:
            with conn.cursor() as cursor:
                # Отримуємо користувачів та статуси
                cursor.execute("SELECT id FROM users;")
                user_ids = [row[0] for row in cursor.fetchall()]

                cursor.execute("SELECT id FROM status;")
                status_ids = [row[0] for row in cursor.fetchall()]

                if not user_ids or not status_ids:
                    logger.warning("Неможливо заповнити таблицю 'tasks', оскільки користувачі або статуси відсутні.")
                    return

                for _ in range(count):
                    title = faker.sentence(nb_words=6)
                    description = faker.text(max_nb_chars=200)
                    status_id = random.choice(status_ids)
                    user_id = random.choice(user_ids)

                    cursor.execute("""
                        INSERT INTO tasks (title, description, status_id, user_id)
                        VALUES (%s, %s, %s, %s);
                    """, (title, description, status_id, user_id))
                conn.commit()
                logger.info("Таблиця 'tasks' заповнена успішно.")
    except Exception as e:
        logger.error(f"Помилка при заповненні таблиці 'tasks': {e}")

if __name__ == "__main__":
    seed_statuses()
    seed_users(count=10)
    seed_tasks(count=20)
