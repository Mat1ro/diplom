import os

from dotenv import load_dotenv
from pytz import timezone

load_dotenv()

# database
DB_USER = os.getenv("DB_USER")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")

# APScheduler
moscow = timezone('Europe/Moscow')

# telegram bot
TOKEN = os.getenv("TOKEN")
