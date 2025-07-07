

from celery import Celery
from celery.schedules import crontab

from app.users.security import fastmail, send_email

from app.notifications.auto_create_notifications import auto_sending

# Налаштування Celery з RabbitMQ
celery = Celery('tasks', broker="pyamqp://guest:guest@rabbitmq:5672//")




@celery.task
def send_email_task(message):
    send_email(message)
    # send_email(subject, email_to, body)


@celery.task
def send_daily_notifications():
    auto_sending()

# Налаштування для Celery Beat
celery.conf.beat_schedule = {
    'send-daily-notifications': {
        'task': 'celery_worker.send_daily_notifications',
        'schedule': crontab(hour="14", minute="56"),
    },
}