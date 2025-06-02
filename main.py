"""
Основной модуль приложения, который запускает бота и планировщик задач.

Этот модуль отвечает за:
1. Настройку логирования
2. Запуск планировщика задач для обновления базы данных
3. Запуск Telegram бота
"""

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.fill_db import fill_db_sync
from bot.bot import start_bot
from constants import moscow

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('asyncpg').setLevel(logging.DEBUG)


async def fill_db_async_wrapper():
    """
    Асинхронная обертка для синхронной функции заполнения базы данных.
    Запускает fill_db_sync в отдельном потоке.
    """
    await asyncio.to_thread(fill_db_sync)


async def main():
    """
    Основная функция приложения.
    
    Инициализирует и запускает:
    1. Планировщик задач для ежедневного обновления базы данных в 3:00
    2. Telegram бота
    """
    scheduler = AsyncIOScheduler(timezone=moscow)
    scheduler.add_job(fill_db_async_wrapper, "cron", hour=3, minute=0)
    scheduler.start()
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
