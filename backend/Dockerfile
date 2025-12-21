# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости (если понадобятся позже)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Открываем порт 8000
EXPOSE 8000

# Запуск сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]