"""
Модуль констант и конфигурации приложения.

Этот модуль содержит:
1. Настройки подключения к базе данных
2. Настройки временной зоны для планировщика
3. Токен Telegram бота
"""

import os

from dotenv import load_dotenv
from pytz import timezone

# Загрузка переменных окружения из .env файла
load_dotenv()

# Настройки подключения к базе данных
DB_USER = os.getenv("DB_USER")  # Имя пользователя базы данных
PASSWORD = os.getenv("PASSWORD")  # Пароль пользователя базы данных
HOST = os.getenv("HOST")  # Хост базы данных
PORT = os.getenv("PORT")  # Порт базы данных
DATABASE = os.getenv("DATABASE")  # Имя базы данных

# Настройки временной зоны для планировщика задач
moscow = timezone('Europe/Moscow')  # Временная зона Москвы

# Настройки Telegram бота
TOKEN = os.getenv("TOKEN")  # Токен бота
