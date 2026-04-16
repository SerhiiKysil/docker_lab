import pandas as pd
from sqlalchemy import create_engine
import matplotlib

# Використовуємо 'Agg' бекенд, бо в Docker немає графічного інтерфейсу для відмальовки вікон
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db:5432/cars_db")
PLOTS_DIR = "/app/plots"


def create_visualizations():
    print("🎨 Початок створення візуалізацій...")
    engine = create_engine(DATABASE_URL)
    df = pd.read_sql("SELECT * FROM cars", engine)

    os.makedirs(PLOTS_DIR, exist_ok=True)

    # Налаштування стилю
    sns.set_theme(style="whitegrid")

    # --- Графік 1: Топ-10 найпопулярніших марок авто ---
    if 'brand' in df.columns:
        plt.figure(figsize=(10, 6))
        top_brands = df['brand'].value_counts().head(10)
        sns.barplot(x=top_brands.values, y=top_brands.index, palette="viridis")
        plt.title('Топ-10 найпопулярніших марок автомобілів')
        plt.xlabel('Кількість')
        plt.ylabel('Марка')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'top_brands.png'))
        plt.close()
        print("✅ Графік 1 (top_brands.png) збережено.")

    # --- Графік 2: Розподіл типів пального ---
    if 'fuel' in df.columns:
        plt.figure(figsize=(10, 6))
        fuel_counts = df['fuel'].value_counts()
        sns.barplot(x=fuel_counts.values, y=fuel_counts.index, palette="magma")
        plt.title('Розподіл автомобілів за типом пального')
        plt.xlabel('Кількість')
        plt.ylabel('Тип пального')
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, 'fuel_distribution.png'))
        plt.close()
        print("✅ Графік 2 (fuel_distribution.png) збережено.")

    print("🎉 Всі візуалізації успішно створено!")


if __name__ == "__main__":
    create_visualizations()