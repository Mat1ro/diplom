from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from app.fill_db import fill

moscow = timezone('Europe/Moscow')
scheduler = BlockingScheduler(timezone=moscow)

scheduler.add_job(fill, CronTrigger(hour=23, minute=44))

if __name__ == "__main__":
    scheduler.start()
