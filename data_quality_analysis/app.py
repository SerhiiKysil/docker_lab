import pandas as pd
from sqlalchemy import create_engine
import os
import json

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db:5432/cars_db")
REPORT_PATH = "/app/reports/quality_report.json"


def analyze_quality():
    print("🔍 Початок перевірки якості даних...")
    engine = create_engine(DATABASE_URL)

    # Завантажуємо дані з бази
    df = pd.read_sql("SELECT * FROM cars", engine)

    # 1. Перевірка пропусків
    missing_data = df.isnull().sum().to_dict()

    # 2. Перевірка дублікатів
    duplicates_count = int(df.duplicated().sum())

    # 3. Базова інформація про колонки та типи
    columns_info = {col: str(dtype) for col, dtype in df.dtypes.items()}

    report = {
        "total_rows": len(df),
        "duplicates": duplicates_count,
        "missing_values": missing_data,
        "columns_types": columns_info
    }

    # Зберігаємо у спільний том
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    print(f"✅ Звіт про якість даних збережено: {REPORT_PATH}")


if __name__ == "__main__":
    analyze_quality()