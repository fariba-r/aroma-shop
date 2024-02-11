# celery.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    # Name of the task
    'delete-inactive-users-every-day': {
        # Task function to run
        'task': 'tasks.delete_inactive_users',
        # Schedule to run the task every day at midnight
        'schedule': crontab(minute=0, hour=0),
    },
}
