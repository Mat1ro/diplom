"""
Модуль инициализации и запуска Telegram бота.

Этот модуль отвечает за:
1. Создание экземпляра бота
2. Настройку диспетчера и хранилища состояний
3. Запуск бота
"""

import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from constants import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
telegram_bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Импорт обработчиков команд
import bot.handlers


async def start_bot():
    """
    Асинхронная функция для запуска бота.
    
    Запускает бота в режиме long polling для обработки входящих сообщений.
    """
    await dp.start_polling(telegram_bot)
