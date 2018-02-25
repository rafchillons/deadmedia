# quick_publisher/celery.py
from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deadmedia.settings')

app = Celery('deadmedia')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'download-2ch-schedule': {
        'task': 'deadtasks.tasks.do_2ch_download_tasks',
        'schedule': 30*60.0,  #seconds change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
    'remove-old-schedule': {
        'task': 'deadtasks.tasks.do_remove_old_tasks',
        'schedule': 3*60*60.0,  #seconds change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}

