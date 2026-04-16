from flask import Flask, render_template, send_from_directory
import pandas as pd
from sqlalchemy import create_engine
import os
import json

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@db:5432/cars_db")
REPORTS_DIR = "/app/reports"
PLOTS_DIR = "/app/plots"

@app.route('/')
def index():
    # Завантаження 10 рядків з БД для демонстрації
    engine = create_engine(DATABASE_URL)
    try:
        df = pd.read_sql("SELECT * FROM cars LIMIT 10", engine)
        data_html = df.to_html(classes="table table-striped table-hover", index=False)
    except Exception as e:
        data_html = f"<p>Помилка завантаження даних з БД: {e}</p>"

    # Зчитування звітів (читаємо з файлів, які згенерували попередні контейнери)
    quality_report = {}
    research_report = {}
    try:
        with open(os.path.join(REPORTS_DIR, 'quality_report.json'), 'r', encoding='utf-8') as f:
            quality_report = json.load(f)
        with open(os.path.join(REPORTS_DIR, 'research_report.json'), 'r', encoding='utf-8') as f:
            research_report = json.load(f)
    except FileNotFoundError:
        pass # Якщо файлів ще немає, передамо порожні словники

    return render_template('index.html', tables=data_html, quality=quality_report, research=research_report)

# Окремий маршрут для того, щоб віддавати картинки графіків у браузер
@app.route('/plots/<filename>')
def get_plot(filename):
    return send_from_directory(PLOTS_DIR, filename)

if __name__ == '__main__':
    # Запускаємо сервер
    app.run(host='0.0.0.0', port=5000)