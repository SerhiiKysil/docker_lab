import pandas as pd
from sqlalchemy import create_engine
import os
import json

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db:5432/cars_db")
REPORT_PATH = "/app/reports/research_report.json"


def conduct_research():
    print("📈 Початок дослідження даних...")
    engine = create_engine(DATABASE_URL)
    df = pd.read_sql("SELECT * FROM cars", engine)

    # Аналіз популярних марок (топ-5)
    top_brands = df['brand'].value_counts().head(5).to_dict() if 'brand' in df.columns else {}

    # Розподіл за типом пального
    fuel_types = df['fuel'].value_counts().to_dict() if 'fuel' in df.columns else {}

    # Середній рік випуску (відкидаємо аномальні значення, наприклад, рік < 1900)
    if 'make_year' in df.columns:
        df['make_year'] = pd.to_numeric(df['make_year'], errors='coerce')
        valid_years = df[(df['make_year'] > 1900) & (df['make_year'] <= 2026)]
        avg_year = float(valid_years['make_year'].mean()) if not valid_years.empty else 0
    else:
        avg_year = 0

    report = {
        "top_5_brands": top_brands,
        "fuel_distribution": fuel_types,
        "average_make_year": round(avg_year, 1)
    }

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=4)

    print(f"✅ Звіт дослідження збережено: {REPORT_PATH}")


if __name__ == "__main__":
    conduct_research()