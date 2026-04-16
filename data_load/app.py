import pandas as pd
from sqlalchemy import create_engine
import os
import time

# Отримуємо URL бази даних зі змінних середовища (задано в compose.yaml)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db:5432/cars_db")
DATA_PATH = "/app/data/dataset.csv"


def load_data():
    print("⏳ Підключення до бази даних...")
    engine = create_engine(DATABASE_URL)

    print(f"📖 Зчитування файлу {DATA_PATH}...")
    try:
        # Читаємо CSV, вказуємо роздільник ;
        # Датасети з відкритих даних України часто мають кодування cp1251, тому додаємо обробку
        try:
            df = pd.read_csv(DATA_PATH, sep=';', low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(DATA_PATH, sep=';', encoding='cp1251', low_memory=False)

        # Переводимо назви колонок у нижній регістр для зручності в SQL
        df.columns = [col.strip().lower() for col in df.columns]

        print(f"📊 Зчитано {len(df)} рядків. Завантаження в PostgreSQL...")

        # Записуємо дані у таблицю 'cars'
        df.to_sql('cars', engine, if_exists='replace', index=False)
        print("✅ Дані успішно завантажено в таблицю 'cars'!")

    except Exception as e:
        print(f"❌ Виникла помилка: {e}")


if __name__ == "__main__":
    # Робимо невеличку паузу, щоб переконатися, що база приймає з'єднання
    time.sleep(3)
    load_data()