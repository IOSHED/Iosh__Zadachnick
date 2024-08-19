#!/bin/bash

# Переход в директорию проекта
cd /backend

# Активация виртуального окружения
source venv/bin/activate

# Запуск Redis
redis-server &

# Запуск Celery worker
celery -A settings worker --loglevel=info -P eventlet &

# Запуск Telegram-бота
python manage.py run_telegram_bot &

# Запуск сервера разработки Django
python manage.py runserver
