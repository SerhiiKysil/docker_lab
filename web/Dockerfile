FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копіюємо всі файли (включаючи папку templates)
COPY . .
# Відкриваємо порт 5000 для доступу ззовні
EXPOSE 5000
CMD ["python", "app.py"]