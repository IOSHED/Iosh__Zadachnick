#!/bin/bash

sudo apt update
sudo apt install redis-server

sudo systemctl start redis-server
sudo systemctl enable redis-server
sudo systemctl status redis-server


# Переход в директорию проекта
cd backend

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Выполнение миграций
python manage.py migrate

# Сборка статических файлов
python manage.py collectstatic --noinput
